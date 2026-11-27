"""Módulo 7 - Práctica 7: análisis de las ventas del año.

Un pequeño proceso de análisis completo: cargar, limpiar, calcular indicadores,
generar gráficos y exportar los resultados.

Uso:

    python m7_practica_analisis.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATOS = Path(__file__).resolve().parent.parent / "datos"
SALIDA = Path(__file__).resolve().parent / "salida_practica_7"
COLUMNAS_TEXTO = ["vendedor", "region", "producto", "categoria"]


def cargar(ruta: str | Path) -> pd.DataFrame:
    """Lee el CSV de ventas con todas las columnas como texto."""
    return pd.read_csv(ruta, dtype=str, encoding="utf-8")


def preparar(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve las ventas limpias y con las columnas calculadas.

    1. Texto sin espacios sobrantes y con la inicial en mayúscula.
    2. Sin filas duplicadas.
    3. ``fecha`` como fecha (formato "AAAA-MM-DD"), ``unidades`` y ``precio``
       como números. ``precio`` admite coma decimal.
    4. Las regiones ausentes pasan a ser "Sin región".
    5. Se descartan las filas sin fecha, vendedor, unidades o precio válidos, y
       las que tienen unidades o precio menores o iguales que cero.
    6. ``unidades`` queda como entero.
    7. Columnas nuevas: ``importe`` (unidades por precio) y ``mes`` ("AAAA-MM").
    8. Filas ordenadas por fecha, con el índice renumerado desde 0. A igual
       fecha se conserva el orden original.

    No modifica el DataFrame recibido.
    """
    copia = df.copy()
    for col in COLUMNAS_TEXTO:
        if col in copia.columns:
            copia[col] = copia[col].str.strip().str.capitalize()

    copia = copia.drop_duplicates(keep="first")

    fecha = copia["fecha"]
    if pd.api.types.is_string_dtype(fecha) or fecha.dtype == "object":
        fecha = fecha.str.strip()
    copia["fecha"] = pd.to_datetime(fecha, format="%Y-%m-%d", errors="coerce")

    copia["unidades"] = pd.to_numeric(copia["unidades"], errors="coerce")

    precio = copia["precio"]
    if pd.api.types.is_string_dtype(precio) or precio.dtype == "object":
        precio = precio.str.strip().str.replace(",", ".", regex=False)
    copia["precio"] = pd.to_numeric(precio, errors="coerce")

    copia["region"] = copia["region"].fillna("Sin región")

    copia = copia.dropna(subset=["fecha", "vendedor", "unidades", "precio"])
    copia = copia[
        (copia["vendedor"] != "")
        & (copia["unidades"] > 0)
        & (copia["precio"] > 0)
    ].copy()

    copia["unidades"] = copia["unidades"].astype(int)
    copia["importe"] = copia["unidades"] * copia["precio"]
    copia["mes"] = copia["fecha"].dt.strftime("%Y-%m")

    return copia.sort_values("fecha", kind="stable").reset_index(drop=True)


def indicadores(df: pd.DataFrame) -> dict:
    """Devuelve los indicadores principales de unas ventas preparadas.

    Claves:

    - "ventas": número de ventas (int).
    - "importe_total": float con dos decimales.
    - "ticket_medio": importe medio por venta, float con dos decimales.
    - "mejor_vendedor": el de mayor importe total.
    - "mejor_mes": el mes "AAAA-MM" de mayor importe total.
    - "producto_mas_vendido": el de más unidades.
    """
    return {
        "ventas": int(len(df)),
        "importe_total": round(float(df["importe"].sum()), 2),
        "ticket_medio": round(float(df["importe"].mean()), 2),
        "mejor_vendedor": str(df.groupby("vendedor")["importe"].sum().idxmax()),
        "mejor_mes": str(df.groupby("mes")["importe"].sum().idxmax()),
        "producto_mas_vendido": str(df.groupby("producto")["unidades"].sum().idxmax()),
    }


def ranking_vendedores(df: pd.DataFrame, objetivos: pd.DataFrame) -> pd.DataFrame:
    """Devuelve una fila por vendedor, de mayor a menor importe.

    Columnas, en este orden: vendedor, ventas, importe, objetivo, cumplimiento
    y cumplido. ``importe`` va redondeado a dos decimales, ``cumplimiento`` es
    el porcentaje del objetivo alcanzado con un decimal y ``cumplido`` indica
    si el importe llega al objetivo. El índice va de 0 en adelante.

    ``objetivos`` tiene las columnas vendedor y objetivo.
    """
    res = df.groupby("vendedor", as_index=False).agg(
        ventas=("importe", "size"),
        importe=("importe", "sum"),
    )
    res["importe"] = res["importe"].round(2)
    res = res.merge(objetivos[["vendedor", "objetivo"]], on="vendedor", how="left")
    res["cumplimiento"] = (res["importe"] / res["objetivo"] * 100).round(1)
    res["cumplido"] = res["importe"] >= res["objetivo"]
    return (
        res.sort_values("importe", ascending=False)[
            ["vendedor", "ventas", "importe", "objetivo", "cumplimiento", "cumplido"]
        ]
        .reset_index(drop=True)
    )


def evolucion_mensual(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve una fila por mes, en orden, con las columnas mes, importe y variacion.

    ``importe`` va redondeado a dos decimales. ``variacion`` es el cambio en
    porcentaje respecto al mes anterior, con un decimal; en el primer mes es
    un valor ausente. El índice va de 0 en adelante.
    """
    mensual = (
        df.groupby("mes", as_index=False)["importe"]
        .sum()
        .sort_values("mes")
        .reset_index(drop=True)
    )
    mensual["importe"] = mensual["importe"].round(2)
    mensual["variacion"] = (mensual["importe"].pct_change() * 100).round(1)
    return mensual[["mes", "importe", "variacion"]]


def generar_graficos(df: pd.DataFrame, carpeta: str | Path) -> list[Path]:
    """Guarda dos gráficos en ``carpeta`` y devuelve sus rutas, en este orden.

    1. ``importe_por_vendedor.png``: barras, de mayor a menor importe.
    2. ``evolucion_mensual.png``: líneas con el importe de cada mes.

    Crea la carpeta si no existe. Cada gráfico lleva título y etiqueta en el
    eje Y. Las figuras se cierran después de guardarlas.
    """
    destino = Path(carpeta)
    destino.mkdir(parents=True, exist_ok=True)

    por_vendedor = df.groupby("vendedor")["importe"].sum().sort_values(ascending=False)
    ruta_vendedor = destino / "importe_por_vendedor.png"
    fig1, ax1 = plt.subplots()
    ax1.bar(por_vendedor.index.astype(str), por_vendedor.values)
    ax1.set_title("Importe por vendedor")
    ax1.set_ylabel("Importe (€)")
    fig1.tight_layout()
    fig1.savefig(ruta_vendedor, format="png", dpi=150)
    plt.close(fig1)

    mensual = df.groupby("mes")["importe"].sum().sort_index()
    ruta_mensual = destino / "evolucion_mensual.png"
    fig2, ax2 = plt.subplots()
    ax2.plot(mensual.index.astype(str), mensual.values, marker="o")
    ax2.set_title("Evolución mensual")
    ax2.set_ylabel("Importe (€)")
    ax2.grid(True)
    fig2.tight_layout()
    fig2.savefig(ruta_mensual, format="png", dpi=150)
    plt.close(fig2)

    return [ruta_vendedor, ruta_mensual]


def exportar(tabla: pd.DataFrame, ruta: str | Path) -> None:
    """Escribe la tabla en un CSV en UTF-8, sin la columna del índice.

    Crea la carpeta de destino si no existe.
    """
    destino = Path(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    tabla.to_csv(destino, index=False, encoding="utf-8")


def main() -> None:
    """Ejecuta el análisis completo con los datos del módulo."""
    ventas = preparar(cargar(DATOS / "ventas_2026.csv"))
    objetivos = pd.read_csv(DATOS / "objetivos.csv")

    print("INDICADORES")
    for nombre, valor in indicadores(ventas).items():
        print(f"  {nombre:<22}{valor}")
    print()
    print("RANKING DE VENDEDORES")
    ranking = ranking_vendedores(ventas, objetivos)
    print(ranking.to_string(index=False))
    print()
    print("EVOLUCIÓN MENSUAL")
    print(evolucion_mensual(ventas).to_string(index=False))

    exportar(ranking, SALIDA / "ranking_vendedores.csv")
    exportar(evolucion_mensual(ventas), SALIDA / "evolucion_mensual.csv")
    for ruta in generar_graficos(ventas, SALIDA):
        print(f"Gráfico guardado en {ruta}")


if __name__ == "__main__":
    main()