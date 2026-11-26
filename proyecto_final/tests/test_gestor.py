from datetime import timedelta

import pytest

from habitos.excepciones import (FechaInvalida, HabitoDuplicado, HabitoInvalido,
                                 HabitoNoEncontrado)
from habitos.gestor import GestorHabitos


def test_crear_asigna_ids_consecutivos(gestor, hoy):
    a = gestor.crear("Leer", hoy)
    b = gestor.crear("Correr", hoy, veces_semana=3)
    assert (a.id, b.id) == (1, 2)
    assert [h.nombre for h in gestor.activos()] == ["Leer", "Correr"]


def test_crear_valida_los_datos(gestor, hoy):
    with pytest.raises(HabitoInvalido):
        gestor.crear("", hoy)
    assert gestor.todos() == []


def test_no_permite_nombres_duplicados_sin_importar_mayusculas(gestor, hoy):
    gestor.crear("Leer", hoy)
    with pytest.raises(HabitoDuplicado):
        gestor.crear("  leer ", hoy)


def test_un_nombre_archivado_se_puede_reutilizar(gestor, hoy):
    primero = gestor.crear("Leer", hoy)
    gestor.archivar(primero.id)
    segundo = gestor.crear("Leer", hoy)
    assert segundo.id != primero.id


def test_restaurar_falla_si_el_nombre_ya_esta_en_uso(gestor, hoy):
    primero = gestor.crear("Leer", hoy)
    gestor.archivar(primero.id)
    gestor.crear("Leer", hoy)
    with pytest.raises(HabitoDuplicado):
        gestor.restaurar(primero.id)


def test_obtener_inexistente(gestor):
    with pytest.raises(HabitoNoEncontrado) as info:
        gestor.obtener(99)
    assert info.value.id_habito == 99


def test_editar(gestor, hoy):
    h = gestor.crear("Leer", hoy)
    gestor.editar(h.id, "Leer 20 min", 5, "Antes de dormir")
    assert (h.nombre, h.veces_semana, h.descripcion) == ("Leer 20 min", 5, "Antes de dormir")


def test_editar_no_permite_chocar_con_otro_nombre(gestor, hoy):
    gestor.crear("Leer", hoy)
    otro = gestor.crear("Correr", hoy)
    with pytest.raises(HabitoDuplicado):
        gestor.editar(otro.id, "leer", 7)
    gestor.editar(otro.id, "Correr", 3)  # conservar el propio nombre sí vale


def test_eliminar(gestor, hoy):
    h = gestor.crear("Leer", hoy)
    gestor.eliminar(h.id)
    assert gestor.todos() == []
    with pytest.raises(HabitoNoEncontrado):
        gestor.eliminar(h.id)


def test_marcar_y_alternar_por_id(gestor, hoy):
    h = gestor.crear("Leer", hoy)
    gestor.marcar(h.id, hoy, hoy)
    assert h.cumplido(hoy)
    assert gestor.alternar(h.id, hoy, hoy) is False
    with pytest.raises(FechaInvalida):
        gestor.marcar(h.id, hoy + timedelta(days=1), hoy)
    with pytest.raises(HabitoNoEncontrado):
        gestor.marcar(99, hoy, hoy)


def test_activos_y_archivados(gestor, hoy):
    a = gestor.crear("Leer", hoy)
    gestor.crear("Correr", hoy)
    gestor.archivar(a.id)
    assert [h.nombre for h in gestor.activos()] == ["Correr"]
    assert [h.nombre for h in gestor.archivados()] == ["Leer"]
    assert len(gestor.todos()) == 2


def test_pendientes_y_progreso_hoy(gestor, hoy):
    leer = gestor.crear("Leer", hoy)
    gestor.crear("Correr", hoy)
    assert gestor.progreso_hoy(hoy) == (0, 2)
    gestor.marcar(leer.id, hoy, hoy)
    assert gestor.progreso_hoy(hoy) == (1, 2)
    assert [h.nombre for h in gestor.pendientes(hoy)] == ["Correr"]


def test_un_habito_semanal_ya_cumplido_no_toca_hoy(gestor, hoy):
    from datetime import date
    gym = gestor.crear("Gimnasio", hoy, veces_semana=1)
    gestor.marcar(gym.id, date(2026, 11, 23), hoy)   # ya cumplió su vez de la semana
    assert gestor.progreso_hoy(hoy) == (0, 0)


def test_el_siguiente_id_continua_tras_cargar(hoy):
    from habitos.modelo import Habito
    gestor = GestorHabitos([Habito(id=7, nombre="Leer", creado=hoy)])
    assert gestor.crear("Correr", hoy).id == 8
