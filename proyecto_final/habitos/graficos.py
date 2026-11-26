"""Gráficos con Matplotlib, devueltos como PNG en base64 para incrustarlos en HTML.

Los colores de texto y rejilla son neutros y el fondo transparente, así que
se ven bien tanto en modo claro como en modo oscuro.
"""

import base64
import io
from datetime import date, timedelta

import matplotlib

matplotlib.use("Agg")  # sin ventana: se dibuja en memoria
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from habitos.rachas import lunes_de  # noqa: E402

VERDE = "#16a34a"
GRIS_TEXTO = "#6b7280"
GRIS_VACIO = "#9ca3af55"  # gris translúcido


def _a_base64(fig) -> str:
    """Convierte la figura en un PNG en base64 y la cierra para liberar memoria."""
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=140, bbox_inches="tight", transparent=True)
    plt.close(fig)
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def _estilo(ax) -> None:
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(GRIS_TEXTO)
    ax.tick_params(colors=GRIS_TEXTO, labelsize=9)
    ax.yaxis.label.set_color(GRIS_TEXTO)
    ax.xaxis.label.set_color(GRIS_TEXTO)
    ax.title.set_color(GRIS_TEXTO)


def _eje_enteros(ax) -> None:
    ax.yaxis.get_major_locator().set_params(integer=True)


def grafico_semanas(serie: pd.Series) -> str:
    """Barras: registros en cada una de las últimas semanas."""
    fig, ax = plt.subplots(figsize=(6, 2.6))
    etiquetas = [d.strftime("%d/%m") for d in serie.index]
    ax.bar(etiquetas, serie.to_numpy(), color=VERDE, width=0.65)
    ax.set_title("Registros por semana (semana que empieza el…)", fontsize=10)
    _estilo(ax)
    _eje_enteros(ax)
    return _a_base64(fig)


def grafico_dias_semana(serie: pd.Series) -> str:
    """Barras: en qué días de la semana cumples más."""
    fig, ax = plt.subplots(figsize=(6, 2.6))
    etiquetas = [dia[:3].capitalize() for dia in serie.index]
    ax.bar(etiquetas, serie.to_numpy(), color=VERDE, width=0.65)
    ax.set_title("Registros por día de la semana", fontsize=10)
    _estilo(ax)
    _eje_enteros(ax)
    return _a_base64(fig)


def grafico_cumplimiento(tabla: pd.DataFrame) -> str:
    """Barras horizontales: % de cumplimiento de cada hábito (últimos 28 días)."""
    altura = max(1.6, 0.5 * len(tabla) + 0.9)
    fig, ax = plt.subplots(figsize=(6, altura))
    # barh dibuja de abajo a arriba: se invierte para que el mejor quede arriba
    nombres = tabla["habito"].to_numpy()[::-1]
    porcentajes = (tabla["cumplimiento"].to_numpy() * 100)[::-1]
    ax.barh(nombres, porcentajes, color=VERDE, height=0.6)
    ax.set_xlim(0, 100)
    ax.set_xlabel("% de cumplimiento (últimos 28 días)", fontsize=9)
    _estilo(ax)
    for y, valor in enumerate(porcentajes):
        ax.text(min(valor + 2, 88), y, f"{valor:.0f}%", va="center", fontsize=9, color=GRIS_TEXTO)
    return _a_base64(fig)


def mapa_calor(matriz: np.ndarray, hoy: date) -> str:
    """Mapa de calor tipo «calendario»: semanas en columnas y días en filas.

    Cada día es una celda redondeada; los huecos entre celdas son transparentes
    para que se vea bien con cualquier fondo. Los días futuros no se dibujan.
    """
    filas, semanas = matriz.shape
    fig, ax = plt.subplots(figsize=(max(4.0, semanas * 0.32), 2.1))

    for dia in range(filas):
        for semana in range(semanas):
            valor = matriz[dia, semana]
            if np.isnan(valor):
                continue
            celda = FancyBboxPatch(
                (semana - 0.42, dia - 0.42), 0.84, 0.84,
                boxstyle="round,pad=0,rounding_size=0.15",
                linewidth=0, facecolor=VERDE if valor else GRIS_VACIO,
            )
            ax.add_patch(celda)

    ax.set_xlim(-0.5, semanas - 0.5)
    ax.set_ylim(filas - 0.5, -0.5)  # el lunes arriba
    ax.set_aspect("equal")
    ax.set_yticks(range(filas), ["L", "M", "X", "J", "V", "S", "D"])

    primer_lunes = lunes_de(hoy) - timedelta(weeks=semanas - 1)
    posiciones = list(range(0, semanas, 4))
    ax.set_xticks(posiciones, [(primer_lunes + timedelta(weeks=i)).strftime("%d/%m") for i in posiciones])

    ax.tick_params(length=0, colors=GRIS_TEXTO, labelsize=8)
    for lado in ax.spines.values():
        lado.set_visible(False)
    return _a_base64(fig)
