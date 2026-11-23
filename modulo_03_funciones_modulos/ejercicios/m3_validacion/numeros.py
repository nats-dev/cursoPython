"""Validación y conversión de números."""


def es_entero(texto: str) -> bool:
    """Indica si el texto representa un número entero, con signo opcional.

    Admite espacios alrededor.

    >>> es_entero(" -42 ")
    True
    >>> es_entero("4.2")
    False
    """
    limpio = texto.strip()
    if not limpio:
        return False
    if limpio[0] in ("+", "-"):
        limpio = limpio[1:]
    return limpio.isdigit() and limpio.isascii()


def es_decimal(texto: str) -> bool:
    """Indica si el texto representa un número, entero o con decimales.

    Admite signo, espacios alrededor y tanto el punto como la coma como
    separador decimal. Debe haber dígitos a ambos lados del separador.

    >>> es_decimal("3,14")
    True
    >>> es_decimal("3.")
    False
    """
    limpio = texto.strip()
    if not limpio:
        return False
    if limpio[0] in ("+", "-"):
        limpio = limpio[1:]

    limpio = limpio.replace(",", ".")
    if "." not in limpio:
        return limpio.isdigit() and limpio.isascii()
    if limpio.count(".") != 1:
        return False

    parte_entera, parte_decimal = limpio.split(".")
    return (
        parte_entera.isdigit()
        and parte_entera.isascii()
        and parte_decimal.isdigit()
        and parte_decimal.isascii()
    )


def a_decimal(texto: str, por_defecto: float | None = None) -> float | None:
    """Convierte el texto en ``float``. Si no es un número devuelve ``por_defecto``.

    >>> a_decimal("3,5")
    3.5
    >>> a_decimal("abc", 0.0)
    0.0
    """
    if not es_decimal(texto):
        return por_defecto
    return float(texto.strip().replace(",", "."))


def en_rango(valor: float, minimo: float | None = None, maximo: float | None = None) -> bool:
    """Indica si ``valor`` está entre ``minimo`` y ``maximo``, ambos incluidos.

    Un límite que vale ``None`` no se comprueba.

    >>> en_rango(5, 1, 10)
    True
    >>> en_rango(5, minimo=6)
    False
    >>> en_rango(5, maximo=10)
    True
    """
    if minimo is not None and valor < minimo:
        return False
    if maximo is not None and valor > maximo:
        return False
    return True