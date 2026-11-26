from datetime import date, timedelta

import pytest

from habitos.excepciones import FechaInvalida, HabitoArchivado, HabitoInvalido
from habitos.modelo import MAX_NOMBRE, Habito


def nuevo(hoy, **kw):
    return Habito(id=1, nombre="Leer", creado=hoy, **kw)


# ---- validación --------------------------------------------------------
@pytest.mark.parametrize("nombre", ["", "   ", None, 5])
def test_nombre_obligatorio(nombre):
    with pytest.raises(HabitoInvalido):
        Habito(id=1, nombre=nombre)


def test_nombre_se_normaliza_y_tiene_limite():
    assert Habito(id=1, nombre="  Leer  ").nombre == "Leer"
    with pytest.raises(HabitoInvalido):
        Habito(id=1, nombre="x" * (MAX_NOMBRE + 1))


@pytest.mark.parametrize("veces", [0, 8, -1, 2.5, True, "3"])
def test_veces_semana_invalidas(veces):
    with pytest.raises(HabitoInvalido):
        Habito(id=1, nombre="Leer", veces_semana=veces)


def test_editar_valida_y_no_modifica_si_falla(hoy):
    habito = nuevo(hoy, descripcion="antes")
    with pytest.raises(HabitoInvalido):
        habito.editar("", "después", 3)
    assert habito.nombre == "Leer" and habito.descripcion == "antes" and habito.veces_semana == 7
    habito.editar("Estudiar", "después", 3)
    assert (habito.nombre, habito.descripcion, habito.veces_semana) == ("Estudiar", "después", 3)


# ---- registros ---------------------------------------------------------
def test_marcar_y_desmarcar(hoy):
    habito = nuevo(hoy)
    habito.marcar(hoy, hoy)
    assert habito.cumplido(hoy) and habito.total == 1
    habito.marcar(hoy, hoy)  # idempotente
    assert habito.total == 1
    habito.desmarcar(hoy, hoy)
    assert not habito.cumplido(hoy)


def test_alternar_devuelve_el_nuevo_estado(hoy):
    habito = nuevo(hoy)
    assert habito.alternar(hoy, hoy) is True
    assert habito.alternar(hoy, hoy) is False


def test_no_se_puede_marcar_el_futuro(hoy):
    with pytest.raises(FechaInvalida):
        nuevo(hoy).marcar(hoy + timedelta(days=1), hoy)


def test_archivado_no_admite_registros(hoy):
    habito = nuevo(hoy)
    habito.archivar()
    with pytest.raises(HabitoArchivado):
        habito.marcar(hoy, hoy)
    habito.restaurar()
    habito.marcar(hoy, hoy)
    assert habito.total == 1


def test_marcar_dia_anterior_a_la_creacion_adelanta_creado(hoy):
    habito = nuevo(hoy)
    antes = hoy - timedelta(days=10)
    habito.marcar(antes, hoy)
    assert habito.creado == antes


# ---- consultas -----------------------------------------------------------
def test_marcas_semana_solo_cuenta_la_semana_actual(hoy):
    habito = nuevo(hoy, veces_semana=3)
    habito.marcar(date(2026, 11, 23), hoy)   # lunes de esta semana
    habito.marcar(date(2026, 11, 22), hoy)   # domingo anterior
    assert habito.marcas_semana(hoy) == 1


def test_pendiente_hábito_diario(hoy):
    habito = nuevo(hoy)
    assert habito.pendiente(hoy)
    habito.marcar(hoy, hoy)
    assert not habito.pendiente(hoy)


def test_pendiente_hábito_semanal_con_objetivo_cumplido(hoy):
    habito = nuevo(hoy, veces_semana=2)
    habito.marcar(date(2026, 11, 23), hoy)
    assert habito.pendiente(hoy)
    habito.marcar(date(2026, 11, 24), hoy)
    assert not habito.pendiente(hoy)  # objetivo semanal cumplido: hoy toca descansar


def test_racha_y_mejor_racha_diaria(hoy):
    habito = nuevo(hoy)
    for n in (0, 1, 2, 10, 11, 12, 13):
        habito.marcar(hoy - timedelta(days=n), hoy)
    assert habito.racha_actual(hoy) == 3
    assert habito.mejor_racha() == 4


def test_racha_semanal(hoy):
    habito = nuevo(hoy, veces_semana=2)
    for dia in (date(2026, 11, 16), date(2026, 11, 17), date(2026, 11, 23), date(2026, 11, 24)):
        habito.marcar(dia, hoy)
    assert habito.racha_actual(hoy) == 2
    assert habito.mejor_racha() == 2


def test_cumplimiento_completo_y_parcial(hoy):
    habito = Habito(id=1, nombre="Leer", creado=hoy - timedelta(days=27))
    assert habito.cumplimiento(hoy) == 0
    for n in range(14):
        habito.marcar(hoy - timedelta(days=n), hoy)
    assert habito.cumplimiento(hoy) == pytest.approx(0.5)
    for n in range(14, 28):
        habito.marcar(hoy - timedelta(days=n), hoy)
    assert habito.cumplimiento(hoy) == 1.0


def test_cumplimiento_de_un_habito_nuevo_solo_cuenta_desde_su_creacion(hoy):
    habito = nuevo(hoy)          # creado hoy: ventana de 1 día
    habito.marcar(hoy, hoy)
    assert habito.cumplimiento(hoy) == 1.0


def test_cumplimiento_semanal_se_limita_a_100(hoy):
    habito = Habito(id=1, nombre="Gimnasio", veces_semana=1, creado=hoy - timedelta(days=27))
    for n in range(0, 28, 2):
        habito.marcar(hoy - timedelta(days=n), hoy)
    assert habito.cumplimiento(hoy) == 1.0
