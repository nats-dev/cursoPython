"""Tests de la capa web con el cliente de pruebas de Flask."""

from datetime import date

import pytest

from habitos.almacen import AlmacenCSV
from web import create_app

HOY = date(2026, 11, 26)


@pytest.fixture
def cliente(tmp_path):
    app = create_app(carpeta_datos=tmp_path, hoy=lambda: HOY)
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture
def datos(tmp_path):
    return AlmacenCSV(tmp_path)


def crear(cliente, nombre="Leer", veces="7", descripcion=""):
    return cliente.post("/habitos/nuevo", data={"nombre": nombre, "veces_semana": veces,
                                                "descripcion": descripcion}, follow_redirects=True)


@pytest.mark.parametrize("ruta", ["/", "/habitos", "/habitos/nuevo", "/estadisticas", "/api/habitos", "/api/resumen"])
def test_las_paginas_cargan_sin_datos(cliente, ruta):
    assert cliente.get(ruta).status_code == 200


def test_pagina_inicial_vacia_invita_a_crear(cliente):
    assert "Crear mi primer hábito" in cliente.get("/").get_data(as_text=True)


def test_crear_habito_lo_guarda_y_lo_muestra(cliente, datos):
    respuesta = crear(cliente, "Leer 20 minutos")
    assert respuesta.status_code == 200
    assert "Leer 20 minutos" in respuesta.get_data(as_text=True)
    assert [h.nombre for h in datos.cargar().activos()] == ["Leer 20 minutos"]


def test_crear_con_datos_invalidos_muestra_el_error_y_conserva_lo_escrito(cliente, datos):
    html = crear(cliente, nombre="   ", descripcion="mi texto").get_data(as_text=True)
    assert "El nombre es obligatorio" in html
    assert "mi texto" in html
    assert datos.cargar().todos() == []


def test_crear_duplicado(cliente):
    crear(cliente, "Leer")
    assert "Ya tienes un hábito" in crear(cliente, "leer").get_data(as_text=True)


def test_marcar_hoy_y_desmarcar(cliente, datos):
    crear(cliente, "Leer")
    cliente.post("/habitos/1/alternar", data={"fecha": "2026-11-26", "next": "/"})
    assert datos.cargar().obtener(1).cumplido(HOY)
    assert "1 de 1 completados" in cliente.get("/").get_data(as_text=True)
    cliente.post("/habitos/1/alternar", data={"fecha": "2026-11-26"})
    assert not datos.cargar().obtener(1).cumplido(HOY)


def test_marcar_sin_fecha_usa_hoy(cliente, datos):
    crear(cliente)
    cliente.post("/habitos/1/alternar")
    assert datos.cargar().obtener(1).cumplido(HOY)


def test_no_se_puede_marcar_el_futuro(cliente, datos):
    crear(cliente)
    respuesta = cliente.post("/habitos/1/alternar", data={"fecha": "2026-11-27"}, follow_redirects=True)
    assert "fecha futura" in respuesta.get_data(as_text=True)
    assert datos.cargar().obtener(1).total == 0


def test_fecha_con_formato_incorrecto(cliente):
    crear(cliente)
    respuesta = cliente.post("/habitos/1/alternar", data={"fecha": "ayer"}, follow_redirects=True)
    assert "AAAA-MM-DD" in respuesta.get_data(as_text=True)


@pytest.mark.parametrize("destino, esperado", [("/habitos", "/habitos"), ("https://malo.com", "/"), ("//malo.com", "/")])
def test_redireccion_solo_a_rutas_internas(cliente, destino, esperado):
    crear(cliente)
    respuesta = cliente.post("/habitos/1/alternar", data={"next": destino})
    assert respuesta.headers["Location"] == esperado


def test_habito_inexistente_da_404(cliente):
    assert cliente.get("/habitos/99").status_code == 404
    assert cliente.post("/habitos/99/alternar").status_code == 404
    assert cliente.get("/api/habitos/99").status_code == 404


def test_detalle_de_un_habito(cliente):
    crear(cliente, "Leer")
    cliente.post("/habitos/1/alternar")
    html = cliente.get("/habitos/1").get_data(as_text=True)
    assert "Leer" in html and "racha actual" in html and "data:image/png;base64," in html


def test_editar(cliente, datos):
    crear(cliente, "Leer")
    cliente.post("/habitos/1/editar", data={"nombre": "Leer más", "veces_semana": "3", "descripcion": "x"})
    habito = datos.cargar().obtener(1)
    assert (habito.nombre, habito.veces_semana) == ("Leer más", 3)


def test_editar_con_error_no_cambia_nada(cliente, datos):
    crear(cliente, "Leer")
    html = cliente.post("/habitos/1/editar", data={"nombre": "", "veces_semana": "3"}).get_data(as_text=True)
    assert "El nombre es obligatorio" in html
    assert datos.cargar().obtener(1).nombre == "Leer"


def test_veces_por_semana_no_numerico(cliente):
    assert "del 1 al 7" in crear(cliente, veces="muchas").get_data(as_text=True)


def test_archivar_restaurar_y_eliminar(cliente, datos):
    crear(cliente, "Leer")
    cliente.post("/habitos/1/archivar")
    assert datos.cargar().obtener(1).archivado
    assert "Archivados" in cliente.get("/habitos").get_data(as_text=True)
    cliente.post("/habitos/1/restaurar")
    assert not datos.cargar().obtener(1).archivado
    cliente.post("/habitos/1/archivar")
    cliente.post("/habitos/1/eliminar")
    assert datos.cargar().todos() == []


def test_un_habito_archivado_no_admite_marcas(cliente, datos):
    crear(cliente)
    cliente.post("/habitos/1/archivar")
    respuesta = cliente.post("/habitos/1/alternar", follow_redirects=True)
    assert "archivado" in respuesta.get_data(as_text=True)
    assert datos.cargar().obtener(1).total == 0


def test_estadisticas_con_datos(cliente):
    crear(cliente, "Leer")
    cliente.post("/habitos/1/alternar")
    html = cliente.get("/estadisticas").get_data(as_text=True)
    assert "Cumplimiento por hábito" in html and html.count("data:image/png;base64,") == 3


def test_api_json(cliente):
    crear(cliente, "Leer")
    cliente.post("/habitos/1/alternar")
    lista = cliente.get("/api/habitos").get_json()
    assert lista[0]["nombre"] == "Leer" and lista[0]["hecho_hoy"] is True and lista[0]["racha_actual"] == 1
    detalle = cliente.get("/api/habitos/1").get_json()
    assert detalle["fechas"] == ["2026-11-26"]
    resumen = cliente.get("/api/resumen").get_json()
    assert resumen["fecha"] == "2026-11-26" and resumen["hechos_hoy"] == 1


def test_manifest_para_instalar_como_app(cliente):
    respuesta = cliente.get("/manifest.webmanifest")
    assert respuesta.mimetype == "application/manifest+json"
    assert respuesta.get_json()["display"] == "standalone"


def test_datos_corruptos_muestran_error_claro_y_no_revientan(cliente, tmp_path):
    (tmp_path / "habitos.csv").write_text("id,nombre\n1,Leer\n", encoding="utf-8")
    respuesta = cliente.get("/")
    assert respuesta.status_code == 500
    assert "habitos.csv" in respuesta.get_data(as_text=True)


def test_el_nombre_se_escapa_en_html(cliente):
    crear(cliente, "<script>alert(1)</script>")
    html = cliente.get("/").get_data(as_text=True)
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html
