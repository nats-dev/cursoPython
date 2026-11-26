"""Gestor de hábitos: la colección de hábitos y las operaciones sobre ella.

El gestor delega en cada :class:`Habito` todo lo que le concierne (marcar,
rachas...) y se ocupa solo de lo que afecta al conjunto: identificadores,
nombres duplicados, listados y progreso del día.
"""

import logging
from collections.abc import Iterable
from datetime import date

from habitos.excepciones import HabitoDuplicado, HabitoNoEncontrado
from habitos.modelo import Habito, validar_datos

logger = logging.getLogger(__name__)


class GestorHabitos:
    def __init__(self, habitos: Iterable[Habito] = ()):
        self._habitos: dict[int, Habito] = {h.id: h for h in habitos}
        self._siguiente_id = max(self._habitos, default=0) + 1

    # ---- altas, bajas y edición -----------------------------------------
    def _comprobar_nombre_libre(self, nombre: str, ignorar_id: int | None = None) -> None:
        clave = nombre.casefold()
        for habito in self._habitos.values():
            if habito.id != ignorar_id and not habito.archivado and habito.nombre.casefold() == clave:
                raise HabitoDuplicado(f"Ya tienes un hábito llamado «{habito.nombre}».")

    def crear(self, nombre: str, hoy: date, veces_semana: int = 7, descripcion: str = "") -> Habito:
        nombre, descripcion, veces_semana = validar_datos(nombre, descripcion, veces_semana)
        self._comprobar_nombre_libre(nombre)
        habito = Habito(self._siguiente_id, nombre, veces_semana, descripcion, creado=hoy)
        self._habitos[habito.id] = habito
        self._siguiente_id += 1
        logger.info("Hábito creado: %s (id %d)", habito.nombre, habito.id)
        return habito

    def obtener(self, id_habito: int) -> Habito:
        try:
            return self._habitos[id_habito]
        except KeyError:
            raise HabitoNoEncontrado(id_habito) from None

    def editar(self, id_habito: int, nombre: str, veces_semana: int, descripcion: str = "") -> Habito:
        habito = self.obtener(id_habito)
        nombre, descripcion, veces_semana = validar_datos(nombre, descripcion, veces_semana)
        self._comprobar_nombre_libre(nombre, ignorar_id=id_habito)
        habito.editar(nombre, descripcion, veces_semana)
        logger.info("Hábito editado: %s (id %d)", habito.nombre, habito.id)
        return habito

    def archivar(self, id_habito: int) -> None:
        self.obtener(id_habito).archivar()
        logger.info("Hábito archivado: id %d", id_habito)

    def restaurar(self, id_habito: int) -> None:
        habito = self.obtener(id_habito)
        self._comprobar_nombre_libre(habito.nombre, ignorar_id=id_habito)
        habito.restaurar()
        logger.info("Hábito restaurado: id %d", id_habito)

    def eliminar(self, id_habito: int) -> None:
        self.obtener(id_habito)
        del self._habitos[id_habito]
        logger.info("Hábito eliminado: id %d", id_habito)

    # ---- registros -------------------------------------------------------
    def marcar(self, id_habito: int, fecha: date, hoy: date) -> None:
        self.obtener(id_habito).marcar(fecha, hoy)
        logger.info("Marcado hábito %d el %s", id_habito, fecha)

    def desmarcar(self, id_habito: int, fecha: date, hoy: date) -> None:
        self.obtener(id_habito).desmarcar(fecha, hoy)
        logger.info("Desmarcado hábito %d el %s", id_habito, fecha)

    def alternar(self, id_habito: int, fecha: date, hoy: date) -> bool:
        marcado = self.obtener(id_habito).alternar(fecha, hoy)
        logger.info("Hábito %d el %s: %s", id_habito, fecha, "marcado" if marcado else "desmarcado")
        return marcado

    # ---- consultas -------------------------------------------------------
    def todos(self) -> list[Habito]:
        """Todos los hábitos, archivados incluidos, por orden de creación."""
        return sorted(self._habitos.values(), key=lambda h: h.id)

    def activos(self) -> list[Habito]:
        return [h for h in self.todos() if not h.archivado]

    def archivados(self) -> list[Habito]:
        return [h for h in self.todos() if h.archivado]

    def pendientes(self, hoy: date) -> list[Habito]:
        return [h for h in self.activos() if h.pendiente(hoy)]

    def progreso_hoy(self, hoy: date) -> tuple[int, int]:
        """(hechos, total) de los hábitos que *tocan* hoy.

        Un hábito semanal cuyo objetivo ya se cumplió otro día de la semana
        no cuenta: hoy no toca.
        """
        tocan = [h for h in self.activos() if h.cumplido(hoy) or h.pendiente(hoy)]
        hechos = sum(1 for h in tocan if h.cumplido(hoy))
        return hechos, len(tocan)
