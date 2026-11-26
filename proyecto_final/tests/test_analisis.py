from datetime import date, timedelta

import numpy as np
import pandas as pd
import pytest

from habitos import analisis
from habitos.gestor import GestorHabitos


@pytest.fixture
def gestor_con_registros(hoy):
    gestor = GestorHabitos()
    inicio = hoy - timedelta(days=20)
    leer = gestor.crear("Leer", inicio)
    gym = gestor.crear("Gimnasio", inicio, veces_semana=3)
    for n in range(0, 14):                       # Leer: últimos 14 días seguidos
        gestor.marcar(leer.id, hoy - timedelta(days=n), hoy)
    for dia in (date(2026, 11, 23), date(2026, 11, 25), date(2026, 11, 16)):  # lun, mié, lun anterior
        gestor.marcar(gym.id, dia, hoy)
    return gestor


def test_registros_df_estructura_y_tipos(gestor_con_registros):
    df = analisis.registros_df(gestor_con_registros)
    assert list(df.columns) == ["habito_id", "habito", "fecha", "dia_semana", "semana"]
    assert pd.api.types.is_datetime64_any_dtype(df["fecha"])
    assert len(df) == 17
    assert df["fecha"].is_monotonic_increasing


def test_registros_df_vacio_conserva_las_columnas(gestor, hoy):
    df = analisis.registros_df(gestor)
    assert df.empty and "dia_semana" in df.columns


def test_registros_df_puede_excluir_archivados(gestor_con_registros):
    gestor_con_registros.archivar(2)
    assert len(analisis.registros_df(gestor_con_registros, incluir_archivados=False)) == 14


def test_semana_es_el_lunes(gestor_con_registros):
    df = analisis.registros_df(gestor_con_registros)
    assert (df["semana"].dt.dayofweek == 0).all()


def test_actividad_diaria_rellena_con_ceros(gestor_con_registros, hoy):
    df = analisis.registros_df(gestor_con_registros)
    serie = analisis.actividad_diaria(df, hoy - timedelta(days=19), hoy)
    assert len(serie) == 20
    assert serie.loc[pd.Timestamp(hoy - timedelta(days=19))] == 0
    assert serie.loc[pd.Timestamp(date(2026, 11, 23))] == 2   # Leer + Gimnasio ese lunes


def test_registros_por_dia_semana(gestor_con_registros):
    serie = analisis.registros_por_dia_semana(analisis.registros_df(gestor_con_registros))
    assert list(serie.index) == analisis.DIAS_SEMANA
    assert serie.sum() == 17
    assert serie["lunes"] == 4      # 2 lunes de «Leer» + 2 lunes de «Gimnasio»
    assert serie["miércoles"] == 3  # 2 de «Leer» + 1 de «Gimnasio»


def test_registros_por_semana_devuelve_las_ultimas_semanas(gestor_con_registros, hoy):
    df = analisis.registros_df(gestor_con_registros)
    serie = analisis.registros_por_semana(df, hoy, semanas=4)
    assert list(serie.index) == [pd.Timestamp(d) for d in
                                 (date(2026, 11, 2), date(2026, 11, 9), date(2026, 11, 16), date(2026, 11, 23))]
    # semana del 23: Leer 4 días (23-26) + Gimnasio 2 = 6
    assert serie.iloc[-1] == 6
    assert serie.iloc[0] == 0
    assert serie.sum() == 17


def test_registros_por_semana_sin_datos(gestor, hoy):
    serie = analisis.registros_por_semana(analisis.registros_df(gestor), hoy, semanas=3)
    assert len(serie) == 3 and serie.sum() == 0


def test_matriz_semanal_forma_y_valores(gestor_con_registros, hoy):
    df = analisis.registros_df(gestor_con_registros)
    leer = df[df["habito_id"] == 1]
    matriz = analisis.matriz_semanal(leer, hoy, semanas=3)
    assert matriz.shape == (7, 3)
    assert matriz[3, 2] == 1                 # jueves de esta semana: hecho
    assert np.isnan(matriz[4, 2])            # viernes de esta semana: futuro
    assert matriz[0, 0] == 0                 # lunes 9 de noviembre: Leer empezó el 13
    assert matriz[4, 0] == 1                 # viernes 13: primer día marcado


def test_tabla_habitos_ordenada_por_cumplimiento(gestor_con_registros, hoy):
    tabla = analisis.tabla_habitos(gestor_con_registros, hoy)
    assert list(tabla["habito"]) == ["Leer", "Gimnasio"]
    assert tabla["cumplimiento"].is_monotonic_decreasing
    fila = tabla.iloc[0]
    assert fila["racha_actual"] == 14 and fila["unidad_racha"] == "días"


def test_tabla_habitos_vacia(gestor, hoy):
    assert analisis.tabla_habitos(gestor, hoy).empty


def test_indicadores(gestor_con_registros, hoy):
    ind = analisis.indicadores(gestor_con_registros, hoy)
    assert ind["habitos_activos"] == 2
    assert ind["registros_total"] == 17
    assert ind["registros_30_dias"] == 17
    assert ind["habito_mas_constante"] == "Leer"
    assert ind["dia_mas_activo"] == "lunes"
    assert 0 < ind["cumplimiento_medio"] <= 1


def test_indicadores_sin_datos(gestor, hoy):
    ind = analisis.indicadores(gestor, hoy)
    assert ind == {"habitos_activos": 0, "registros_total": 0, "registros_30_dias": 0,
                   "cumplimiento_medio": 0.0, "habito_mas_constante": None, "dia_mas_activo": None}
