"""Módulo 5 - Ejercicio 6: dataclasses y composición."""

from dataclasses import dataclass, field
from math import hypot


@dataclass(frozen=True)
class Punto:
    """Un punto inmutable en el plano."""

    x: float = 0.0
    y: float = 0.0

    def distancia(self, otro: "Punto") -> float:
        """Devuelve la distancia euclídea hasta otro punto, con dos decimales."""
        return round(hypot(self.x - otro.x, self.y - otro.y), 2)


@dataclass
class LineaPedido:
    """Una línea dentro de un pedido."""

    producto: str
    unidades: int
    precio: float

    def __post_init__(self) -> None:
        if self.unidades <= 0:
            raise ValueError("Las unidades deben ser mayores que cero")
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo")

    @property
    def importe(self) -> float:
        """Devuelve el importe de la línea redondeado a dos decimales."""
        return round(self.unidades * self.precio, 2)


@dataclass
class Pedido:
    """Un pedido compuesto por varias líneas."""

    numero: int
    cliente: str
    lineas: list[LineaPedido] = field(default_factory=list)

    def anadir(self, producto: str, unidades: int, precio: float) -> LineaPedido:
        """Crea, añade y devuelve una línea del pedido."""
        linea = LineaPedido(producto, unidades, precio)
        self.lineas.append(linea)
        return linea

    @property
    def total(self) -> float:
        """Devuelve el importe total del pedido con dos decimales."""
        return round(sum((linea.importe for linea in self.lineas), 0.0), 2)

    def __len__(self) -> int:
        """Devuelve el número de líneas del pedido."""
        return len(self.lineas)

    def productos(self) -> list[str]:
        """Devuelve los nombres de los productos sin repetir y ordenados."""
        return sorted({linea.producto for linea in self.lineas})