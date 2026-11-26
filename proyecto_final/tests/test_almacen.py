from datetime import date, timedelta

import pytest

from habitos.almacen import AlmacenCSV
from habitos.excepciones import ErrorAlmacen
from habitos.gestor import GestorHabitos


def gestor_con_datos(hoy):
    gestor = GestorHabitos()
    leer = gestor.crear("Leer, un poco; cada día", hoy - timedelta(days=5), descripcion='Con "comillas" y\ncoma, punto y coma')
    gym = gestor.crear("Gimnasio", hoy - timedelta(days=5), veces_semana=3)
    for n in (0, 1, 2):
        gestor.marcar(leer.id, hoy - timedelta(days=n), hoy)
    gestor.marcar(gym.id, hoy, hoy)
    gestor.archivar(gym.id)
    return gestor


def test_ida_y_vuelta_conserva_todo(tmp_path, hoy):
    almacen = AlmacenCSV(tmp_path / "datos")
    original = gestor_con_datos(hoy)
    almacen.guardar(original)

    leido = almacen.cargar()
    assert [(h.id, h.nombre, h.descripcion, h.veces_semana, h.creado, h.archivado, h.fechas)
            for h in leido.todos()] == \
           [(h.id, h.nombre, h.descripcion, h.veces_semana, h.creado, h.archivado, h.fechas)
            for h in original.todos()]


def test_sin_ficheros_devuelve_gestor_vacio(tmp_path):
    assert AlmacenCSV(tmp_path / "no_existe").cargar().todos() == []


def test_guardar_crea_la_carpeta_y_no_deja_temporales(tmp_path, hoy):
    carpeta = tmp_path / "a" / "b"
    AlmacenCSV(carpeta).guardar(gestor_con_datos(hoy))
    assert sorted(p.name for p in carpeta.iterdir()) == ["habitos.csv", "registros.csv"]


def test_los_registros_se_guardan_ordenados(tmp_path, hoy):
    almacen = AlmacenCSV(tmp_path)
    almacen.guardar(gestor_con_datos(hoy))
    lineas = almacen.ruta_registros.read_text(encoding="utf-8").splitlines()
    assert lineas[0] == "habito_id,fecha"
    assert lineas[1:] == sorted(lineas[1:], key=lambda l: (int(l.split(",")[0]), l.split(",")[1]))


def test_el_siguiente_id_se_conserva(tmp_path, hoy):
    almacen = AlmacenCSV(tmp_path)
    almacen.guardar(gestor_con_datos(hoy))
    assert almacen.cargar().crear("Nuevo", hoy).id == 3


@pytest.mark.parametrize(
    "contenido",
    [
        "id,nombre,descripcion,veces_semana,creado,archivado\nx,Leer,,7,2026-11-01,0\n",       # id no numérico
        "id,nombre,descripcion,veces_semana,creado,archivado\n1,Leer,,9,2026-11-01,0\n",       # veces fuera de rango
        "id,nombre,descripcion,veces_semana,creado,archivado\n1,,,7,2026-11-01,0\n",           # nombre vacío
        "id,nombre,descripcion,veces_semana,creado,archivado\n1,Leer,,7,01/11/2026,0\n",       # fecha mal formateada
        "id,nombre,descripcion,veces_semana,creado,archivado\n1,A,,7,2026-11-01,0\n1,B,,7,2026-11-01,0\n",  # id repetido
        "id,nombre\n1,Leer\n",                                                                   # faltan columnas
    ],
)
def test_habitos_corruptos_lanzan_error_almacen(tmp_path, contenido):
    (tmp_path / "habitos.csv").write_text(contenido, encoding="utf-8")
    with pytest.raises(ErrorAlmacen):
        AlmacenCSV(tmp_path).cargar()


def test_registro_de_habito_inexistente(tmp_path):
    (tmp_path / "habitos.csv").write_text(
        "id,nombre,descripcion,veces_semana,creado,archivado\n1,Leer,,7,2026-11-01,0\n", encoding="utf-8")
    (tmp_path / "registros.csv").write_text("habito_id,fecha\n5,2026-11-02\n", encoding="utf-8")
    with pytest.raises(ErrorAlmacen, match="no existe"):
        AlmacenCSV(tmp_path).cargar()


def test_el_error_de_almacen_indica_el_fichero_y_la_linea(tmp_path):
    (tmp_path / "habitos.csv").write_text(
        "id,nombre,descripcion,veces_semana,creado,archivado\n1,Leer,,7,2026-11-01,0\nx,Mal,,7,2026-11-01,0\n",
        encoding="utf-8")
    with pytest.raises(ErrorAlmacen) as info:
        AlmacenCSV(tmp_path).cargar()
    assert "habitos.csv" in str(info.value) and "línea 3" in str(info.value)
    assert isinstance(info.value.__cause__, ValueError)  # raise ... from
