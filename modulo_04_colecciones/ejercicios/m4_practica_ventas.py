"""Módulo 4 - Práctica 4: análisis de ventas en memoria."""

from m4_datos_ventas import VENTAS

ANCHO = 44


def importe(venta: dict) -> float:
    """Devuelve el importe de una venta: unidades por precio, con dos decimales."""
    return round(venta["unidades"] * venta["precio"], 2)


def total_ventas(ventas: list[dict]) -> float:
    """Devuelve la suma de los importes de todas las ventas, con dos decimales."""
    return round(sum((importe(v) for v in ventas), 0.0), 2)


def filtrar_ventas(ventas: list[dict], *, region: str | None = None,
                   categoria: str | None = None, vendedor: str | None = None,
                   desde: str | None = None, hasta: str | None = None) -> list[dict]:
    """Devuelve las ventas que cumplen todos los criterios indicados."""
    resultado = []
    for venta in ventas:
        if region is not None and venta["region"] != region:
            continue
        if categoria is not None and venta["categoria"] != categoria:
            continue
        if vendedor is not None and venta["vendedor"] != vendedor:
            continue
        if desde is not None and venta["fecha"] < desde:
            continue
        if hasta is not None and venta["fecha"] > hasta:
            continue
        resultado.append(venta)
    return resultado


def importe_por(ventas: list[dict], campo: str) -> dict[str, float]:
    """Agrupa las ventas por ``campo`` y devuelve el importe total de cada grupo."""
    totales = {}
    for venta in ventas:
        clave = venta[campo]
        totales[clave] = totales.get(clave, 0.0) + importe(venta)
    return {clave: round(total, 2) for clave, total in totales.items()}


def unidades_por_producto(ventas: list[dict]) -> dict[str, int]:
    """Devuelve las unidades totales vendidas de cada producto."""
    totales = {}
    for venta in ventas:
        producto = venta["producto"]
        totales[producto] = totales.get(producto, 0) + venta["unidades"]
    return totales


def ranking(ventas: list[dict], campo: str, cantidad: int = 3) -> list[tuple[str, float]]:
    """Devuelve los ``cantidad`` grupos con mayor importe, como tuplas (clave, importe)."""
    totales = importe_por(ventas, campo)
    ordenados = sorted(totales.items(), key=lambda par: (-par[1], par[0]))
    return ordenados[:cantidad]


def producto_mas_vendido(ventas: list[dict]) -> str | None:
    """Devuelve el producto con más unidades vendidas, o ``None`` si no hay ventas."""
    totales = unidades_por_producto(ventas)
    if not totales:
        return None
    return min(totales, key=lambda producto: (-totales[producto], producto))


def ticket_medio(ventas: list[dict]) -> float:
    """Devuelve el importe medio por venta, con dos decimales. Sin ventas, 0.0."""
    if not ventas:
        return 0.0
    return round(total_ventas(ventas) / len(ventas), 2)


def generar_informe(ventas: list[dict]) -> str:
    """Devuelve el informe de ventas como texto, con el formato del enunciado."""
    mas_vendido = producto_mas_vendido(ventas) or "-"
    lineas = [
        "=" * ANCHO,
        f"{'INFORME DE VENTAS':^{ANCHO}}",
        "=" * ANCHO,
        f"{'Ventas registradas':<30}{len(ventas):>14}",
        f"{'Importe total':<30}{total_ventas(ventas):>14,.2f}",
        f"{'Ticket medio':<30}{ticket_medio(ventas):>14,.2f}",
        f"{'Producto más vendido':<30}{mas_vendido:>14}",
    ]

    secciones = [
        ("Por región", "region"),
        ("Por categoría", "categoria"),
        ("Por vendedor", "vendedor"),
    ]
    for titulo, campo in secciones:
        lineas.append("-" * ANCHO)
        lineas.append(titulo)
        for clave, total in ranking(ventas, campo, cantidad=len(ventas)):
            lineas.append(f"  {clave:<28}{total:>14,.2f}")

    lineas.append("=" * ANCHO)
    return "\n".join(lineas)


def main():
    print(generar_informe(VENTAS))
    print()
    print("Solo la región Sur, segunda quincena:")
    print(generar_informe(filtrar_ventas(VENTAS, region="Sur", desde="2026-10-16")))


if __name__ == "__main__":
    main()