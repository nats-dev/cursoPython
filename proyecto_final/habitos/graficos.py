"""Gráficos con Matplotlib, devueltos como PNG en base64 para incrustarlos en HTML.

Estilo «cyber Y2K»: fondo transparente (se ve el cristal de la tarjeta), texto
lavanda claro, barras de neón con un halo de resplandor y detalles en rosa.
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

CIAN = "#00f0ff"
ROSA = "#ff2bd6"
LIMA = "#b6ff3b"
TEXTO = "#c4bcf5"
EJES = "#6b5fc4"
VACIO = "#ffffff1c"  # blanco translúcido

plt.rcParams["font.family"] = "monospace"


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
        ax.spines[lado].set_color(EJES)
    ax.tick_params(colors=TEXTO, labelsize=9)
    ax.xaxis.label.set_color(TEXTO)
    ax.yaxis.label.set_color(TEXTO)
    ax.set_axisbelow(True)


def _eje_enteros(ax) -> None:
    ax.yaxis.get_major_locator().set_params(integer=True)


def _barras(ax, etiquetas, valores, resaltada=None) -> None:
    """Barras de neón con halo; la barra ``resaltada`` va en rosa."""
    colores = [ROSA if i == resaltada else CIAN for i in range(len(valores))]
    ax.bar(etiquetas, valores, width=0.9, color=colores, alpha=0.14, linewidth=0)  # halo
    ax.bar(etiquetas, valores, width=0.62, color=colores, linewidth=0)
    ax.grid(axis="y", color="#ffffff", alpha=0.07)


def grafico_semanas(serie: pd.Series) -> str:
    """Barras: registros en cada una de las últimas semanas (la actual en rosa)."""
    fig, ax = plt.subplots(figsize=(4.8, 2.5))
    etiquetas = [d.strftime("%d/%m") for d in serie.index]
    _barras(ax, etiquetas, serie.to_numpy(), resaltada=len(serie) - 1)
    _estilo(ax)
    _eje_enteros(ax)
    return _a_base64(fig)


def grafico_dias_semana(serie: pd.Series) -> str:
    """Barras: en qué días de la semana cumples más (el mejor en rosa)."""
    fig, ax = plt.subplots(figsize=(4.8, 2.5))
    etiquetas = [dia[:3].capitalize() for dia in serie.index]
    mejor = int(serie.to_numpy().argmax()) if serie.sum() > 0 else None
    _barras(ax, etiquetas, serie.to_numpy(), resaltada=mejor)
    _estilo(ax)
    _eje_enteros(ax)
    return _a_base64(fig)


def grafico_cumplimiento(tabla: pd.DataFrame) -> str:
    """Barras horizontales: % de cumplimiento de cada hábito (últimos 28 días)."""
    altura = max(1.6, 0.5 * len(tabla) + 0.9)
    fig, ax = plt.subplots(figsize=(4.8, altura))
    # barh dibuja de abajo a arriba: se invierte para que el mejor quede arriba
    nombres = tabla["habito"].to_numpy()[::-1]
    porcentajes = (tabla["cumplimiento"].to_numpy() * 100)[::-1]
    ax.barh(nombres, porcentajes, height=0.86, color=CIAN, alpha=0.14, linewidth=0)  # halo
    ax.barh(nombres, porcentajes, height=0.56, color=CIAN, linewidth=0)
    ax.set_xlim(0, 100)
    ax.set_xlabel("% de cumplimiento (últimos 28 días)", fontsize=9)
    ax.grid(axis="x", color="#ffffff", alpha=0.07)
    _estilo(ax)
    for y, valor in enumerate(porcentajes):
        ax.text(min(valor + 2, 86), y, f"{valor:.0f}%", va="center", fontsize=9, color=LIMA)
    return _a_base64(fig)


def mapa_calor(matriz: np.ndarray, hoy: date) -> str:
    """Mapa de calor tipo «calendario»: semanas en columnas y días en filas.

    Cada día es una celda redondeada; los huecos entre celdas son transparentes.
    Los días futuros no se dibujan y el día de hoy lleva un borde rosa.
    """
    filas, semanas = matriz.shape
    fig, ax = plt.subplots(figsize=(max(4.0, semanas * 0.32), 2.1))
    hoy_dia, hoy_semana = hoy.weekday(), semanas - 1

    for dia in range(filas):
        for semana in range(semanas):
            valor = matriz[dia, semana]
            if np.isnan(valor):
                continue
            es_hoy = (dia, semana) == (hoy_dia, hoy_semana)
            ax.add_patch(FancyBboxPatch(
                (semana - 0.42, dia - 0.42), 0.84, 0.84,
                boxstyle="round,pad=0,rounding_size=0.15",
                linewidth=1.4 if es_hoy else 0,
                edgecolor=ROSA if es_hoy else "none",
                facecolor=LIMA if valor else VACIO,
            ))

    ax.set_xlim(-0.5, semanas - 0.5)
    ax.set_ylim(filas - 0.5, -0.5)  # el lunes arriba
    ax.set_aspect("equal")
    ax.set_yticks(range(filas), ["L", "M", "X", "J", "V", "S", "D"])

    primer_lunes = lunes_de(hoy) - timedelta(weeks=semanas - 1)
    posiciones = list(range(0, semanas, 4))
    ax.set_xticks(posiciones, [(primer_lunes + timedelta(weeks=i)).strftime("%d/%m") for i in posiciones])

    ax.tick_params(length=0, colors=TEXTO, labelsize=8)
    for lado in ax.spines.values():
        lado.set_visible(False)
    return _a_base64(fig)
