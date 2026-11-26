"""Análisis de los registros con pandas.

Todo se hace con operaciones de columna (``groupby``, ``reindex``, máscaras):
no se recorre ningún DataFrame fila a fila.
"""

from datetime import date, timedelta

import numpy as np
import pandas as pd

from habitos.gestor import GestorHabitos
from habitos.rachas import lunes_de

DIAS_SEMANA = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
COLUMNAS_REGISTROS = ["habito_id", "habito", "fecha"]


def registros_df(gestor: GestorHabitos, incluir_archivados: bool = True) -> pd.DataFrame:
    """Una fila por cada día cumplido, con columnas auxiliares de calendario.

    Columnas: habito_id, habito, fecha (datetime), dia_semana (0 = lunes) y
    semana (el lunes de esa semana).
    """
    habitos = gestor.todos() if incluir_archivados else gestor.activos()
    filas = [(h.id, h.nombre, f) for h in habitos for f in h.fechas]
    df = pd.DataFrame(filas, columns=COLUMNAS_REGISTROS)
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["dia_semana"] = df["fecha"].dt.dayofweek
    df["semana"] = df["fecha"] - pd.to_timedelta(df["dia_semana"], unit="D")
    return df.sort_values(["fecha", "habito_id"]).reset_index(drop=True)


def actividad_diaria(df: pd.DataFrame, desde: date, hasta: date) -> pd.Series:
    """Registros por día entre ``desde`` y ``hasta`` (ambos incluidos), con ceros."""
    dias = pd.date_range(desde, hasta, freq="D")
    return df.groupby("fecha").size().reindex(dias, fill_value=0)


def registros_por_dia_semana(df: pd.DataFrame) -> pd.Series:
    """Registros totales por día de la semana, de lunes a domingo."""
    conteo = df["dia_semana"].value_counts().reindex(range(7), fill_value=0)
    conteo.index = DIAS_SEMANA
    return conteo


def registros_por_semana(df: pd.DataFrame, hoy: date, semanas: int = 8) -> pd.Series:
    """Registros de cada una de las últimas ``semanas`` semanas (índice: lunes)."""
    ultimo_lunes = lunes_de(hoy)
    lunes = pd.date_range(end=ultimo_lunes, periods=semanas, freq="7D")
    return df.groupby("semana").size().reindex(lunes, fill_value=0)


def matriz_semanal(df_habito: pd.DataFrame, hoy: date, semanas: int = 20) -> np.ndarray:
    """Matriz 7 x ``semanas`` para el mapa de calor: 1 = hecho, 0 = no, NaN = futuro.

    Las filas son los días de la semana (lunes arriba) y las columnas las
    semanas, de la más antigua a la actual.
    """
    inicio = lunes_de(hoy) - timedelta(weeks=semanas - 1)
    fin = lunes_de(hoy) + timedelta(days=6)
    actividad = actividad_diaria(df_habito, inicio, fin)
    valores = (actividad.to_numpy() > 0).astype(float)
    valores[actividad.index > pd.Timestamp(hoy)] = np.nan
    return valores.reshape(semanas, 7).T


def tabla_habitos(gestor: GestorHabitos, hoy: date) -> pd.DataFrame:
    """Resumen de los hábitos activos, ordenado de más a menos constante."""
    filas = [
        {
            "habito": h.nombre,
            "veces_semana": h.veces_semana,
            "racha_actual": h.racha_actual(hoy),
            "mejor_racha": h.mejor_racha(),
            "unidad_racha": "días" if h.es_diario else "semanas",
            "total": h.total,
            "cumplimiento": h.cumplimiento(hoy),
        }
        for h in gestor.activos()
    ]
    columnas = ["habito", "veces_semana", "racha_actual", "mejor_racha", "unidad_racha", "total", "cumplimiento"]
    tabla = pd.DataFrame(filas, columns=columnas)
    return tabla.sort_values("cumplimiento", ascending=False, kind="stable").reset_index(drop=True)


def indicadores(gestor: GestorHabitos, hoy: date) -> dict:
    """Las cifras principales para la pantalla de estadísticas."""
    df = registros_df(gestor, incluir_archivados=False)
    tabla = tabla_habitos(gestor, hoy)
    hace_30 = pd.Timestamp(hoy - timedelta(days=29))

    por_dia = registros_por_dia_semana(df)
    dia_mas_activo = por_dia.idxmax() if por_dia.sum() > 0 else None

    return {
        "habitos_activos": len(tabla),
        "registros_total": len(df),
        "registros_30_dias": int((df["fecha"] >= hace_30).sum()),
        "cumplimiento_medio": float(tabla["cumplimiento"].mean()) if len(tabla) else 0.0,
        "habito_mas_constante": tabla.loc[0, "habito"] if len(tabla) and tabla.loc[0, "total"] > 0 else None,
        "dia_mas_activo": dia_mas_activo,
    }
