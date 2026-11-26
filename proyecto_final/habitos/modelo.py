"""Modelo de dominio: el hábito y sus registros.

Un :class:`Habito` guarda las fechas en las que se ha cumplido y sabe
calcular sus propias estadísticas (rachas, cumplimiento). Mantiene siempre un
estado válido: los datos se validan al crearlo y al editarlo.
"""

from dataclasses import dataclass, field
from datetime import date, timedelta

from habitos import rachas
from habitos.excepciones import FechaInvalida, HabitoArchivado, HabitoInvalido

MAX_NOMBRE = 60
MAX_DESCRIPCION = 200
VENTANA_CUMPLIMIENTO = 28  # días sobre los que se mide el cumplimiento


def validar_datos(nombre: str, descripcion: str, veces_semana: int) -> tuple[str, str, int]:
    """Valida y normaliza los datos de un hábito. Lanza HabitoInvalido."""
    if not isinstance(nombre, str) or not nombre.strip():
        raise HabitoInvalido("El nombre es obligatorio.")
    nombre = nombre.strip()
    if len(nombre) > MAX_NOMBRE:
        raise HabitoInvalido(f"El nombre no puede superar {MAX_NOMBRE} caracteres.")

    descripcion = (descripcion or "").strip()
    if len(descripcion) > MAX_DESCRIPCION:
        raise HabitoInvalido(f"La descripción no puede superar {MAX_DESCRIPCION} caracteres.")

    es_entero = isinstance(veces_semana, int) and not isinstance(veces_semana, bool)
    if not es_entero or not 1 <= veces_semana <= 7:
        raise HabitoInvalido("Las veces por semana deben ser un número del 1 al 7.")
    return nombre, descripcion, veces_semana


@dataclass
class Habito:
    id: int
    nombre: str
    veces_semana: int = 7
    descripcion: str = ""
    creado: date = field(default_factory=date.today)
    archivado: bool = False
    fechas: set[date] = field(default_factory=set, repr=False)

    def __post_init__(self):
        self.nombre, self.descripcion, self.veces_semana = validar_datos(
            self.nombre, self.descripcion, self.veces_semana
        )

    # ---- propiedades -----------------------------------------------------
    @property
    def es_diario(self) -> bool:
        return self.veces_semana == 7

    @property
    def total(self) -> int:
        """Número total de veces que se ha cumplido."""
        return len(self.fechas)

    # ---- edición ---------------------------------------------------------
    def editar(self, nombre: str, descripcion: str, veces_semana: int) -> None:
        """Cambia los datos del hábito, validándolos antes de aplicarlos."""
        self.nombre, self.descripcion, self.veces_semana = validar_datos(
            nombre, descripcion, veces_semana
        )

    def archivar(self) -> None:
        self.archivado = True

    def restaurar(self) -> None:
        self.archivado = False

    # ---- registros -------------------------------------------------------
    def _comprobar_marcable(self, fecha: date, hoy: date) -> None:
        if self.archivado:
            raise HabitoArchivado("Un hábito archivado no admite cambios en sus registros.")
        if fecha > hoy:
            raise FechaInvalida("No se puede registrar un hábito en una fecha futura.")

    def marcar(self, fecha: date, hoy: date) -> None:
        """Registra el hábito como cumplido en ``fecha`` (nunca en el futuro).

        Si se registra un día anterior a la fecha de creación, esta se adelanta
        para que el cumplimiento se calcule desde que realmente empezó el hábito.
        """
        self._comprobar_marcable(fecha, hoy)
        self.fechas.add(fecha)
        self.creado = min(self.creado, fecha)

    def desmarcar(self, fecha: date, hoy: date) -> None:
        self._comprobar_marcable(fecha, hoy)
        self.fechas.discard(fecha)

    def alternar(self, fecha: date, hoy: date) -> bool:
        """Marca si estaba sin marcar y desmarca si estaba marcado.

        Devuelve True si tras la operación el día queda marcado.
        """
        if fecha in self.fechas:
            self.desmarcar(fecha, hoy)
            return False
        self.marcar(fecha, hoy)
        return True

    # ---- consultas -------------------------------------------------------
    def cumplido(self, fecha: date) -> bool:
        return fecha in self.fechas

    def marcas_semana(self, hoy: date) -> int:
        """Veces cumplido en la semana (lunes a domingo) de ``hoy``."""
        lunes = rachas.lunes_de(hoy)
        domingo = lunes + timedelta(days=6)
        return sum(1 for f in self.fechas if lunes <= f <= domingo)

    def pendiente(self, hoy: date) -> bool:
        """True si hoy conviene marcarlo: no está hecho y el objetivo semanal sigue abierto."""
        if self.archivado or hoy in self.fechas:
            return False
        return self.es_diario or self.marcas_semana(hoy) < self.veces_semana

    def racha_actual(self, hoy: date) -> int:
        if self.es_diario:
            return rachas.racha_dias_actual(self.fechas, hoy)
        return rachas.racha_semanas_actual(self.fechas, hoy, self.veces_semana)

    def mejor_racha(self) -> int:
        if self.es_diario:
            return rachas.mejor_racha_dias(self.fechas)
        return rachas.mejor_racha_semanas(self.fechas, self.veces_semana)

    def cumplimiento(self, hoy: date, ventana: int = VENTANA_CUMPLIMIENTO) -> float:
        """Proporción (0 a 1) del objetivo cumplida en los últimos ``ventana`` días.

        Si el hábito es más reciente que la ventana, solo cuenta desde su creación.
        """
        dias = min(ventana, (hoy - self.creado).days + 1)
        if dias <= 0:
            return 0.0
        desde = hoy - timedelta(days=dias - 1)
        hechas = sum(1 for f in self.fechas if desde <= f <= hoy)
        esperadas = self.veces_semana * dias / 7
        return min(1.0, hechas / esperadas)
