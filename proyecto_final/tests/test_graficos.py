import base64

import pytest

from habitos import analisis, graficos
from habitos.gestor import GestorHabitos

CABECERA_PNG = b"\x89PNG\r\n\x1a\n"


def es_png(texto: str) -> bool:
    return base64.b64decode(texto).startswith(CABECERA_PNG)


@pytest.fixture
def datos(hoy):
    gestor = GestorHabitos()
    h = gestor.crear("Leer", hoy)
    gestor.marcar(h.id, hoy, hoy)
    df = analisis.registros_df(gestor)
    return gestor, df


def test_todos_los_graficos_devuelven_png_en_base64(datos, hoy):
    gestor, df = datos
    assert es_png(graficos.grafico_semanas(analisis.registros_por_semana(df, hoy)))
    assert es_png(graficos.grafico_dias_semana(analisis.registros_por_dia_semana(df)))
    assert es_png(graficos.grafico_cumplimiento(analisis.tabla_habitos(gestor, hoy)))
    assert es_png(graficos.mapa_calor(analisis.matriz_semanal(df, hoy, 20), hoy))


def test_graficos_con_datos_vacios_no_fallan(gestor, hoy):
    df = analisis.registros_df(gestor)
    assert es_png(graficos.grafico_semanas(analisis.registros_por_semana(df, hoy)))
    assert es_png(graficos.mapa_calor(analisis.matriz_semanal(df, hoy, 10), hoy))
