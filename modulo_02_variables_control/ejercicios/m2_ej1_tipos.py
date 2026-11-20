"""Módulo 2 - Ejercicio 1: tipos de datos y conversiones."""

# Nota: Intentado primero por mi cuenta y revisado con apoyo de IA para corregir fallos y mejorar el estilo.

def nombre_del_tipo(valor) -> str:
    """Devuelve el nombre del tipo de ``valor`` en español.

    "entero", "decimal", "booleano", "texto", "nulo" u "otro".

    >>> nombre_del_tipo(3.5)
    'decimal'
    """
    if valor is None:
        return "nulo"
    if type(valor) is bool:
        return "booleano"
    if type(valor) is int:
        return "entero"
    if type(valor) is float:
        return "decimal"
    if type(valor) is str:
        return "texto"
    return "otro"


def a_entero(texto: str) -> int | None:
    """Convierte ``texto`` a entero. Devuelve None si no es un entero válido.

    Admite espacios alrededor y un signo + o - delante.

    >>> a_entero("  -42 ")
    -42
    >>> a_entero("3.5") is None
    True
    """

    limpio = texto.strip()

    if limpio == "":
        return None

    if limpio[0] == "+" or limpio[0] == "-":
        solo_digitos = limpio[1:]
    else:
        solo_digitos = limpio

    if solo_digitos.isdecimal():
        return int(limpio)

    return None
    


def casi_iguales(a: float, b: float, tolerancia: float = 1e-9) -> bool:
    """Indica si dos decimales son iguales dentro de una tolerancia absoluta.

    >>> casi_iguales(0.1 + 0.2, 0.3)
    True
    """
    return abs(a - b) <= tolerancia


def media(a: float, b: float, c: float) -> float:
    """Devuelve la media de tres números redondeada a dos decimales.

    >>> media(5, 6, 8)
    6.33
    """
    return (round((a + b + c) / 3, 2))


def partir_euros(importe: float) -> tuple[int, int]:
    """Separa un importe en euros y céntimos enteros.

    >>> partir_euros(12.34)
    (12, 34)
    """
    return (int(importe), int(round((importe - int(importe)) * 100)))

