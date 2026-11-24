"""Módulo 4 - Ejercicio 5: manipulación de cadenas."""

VOCALES = "aeiouáéíóúü"


def es_palindromo(texto: str) -> bool:
    """Indica si el texto se lee igual en los dos sentidos."""
    limpio = "".join(c.lower() for c in texto if c.isalnum())
    return limpio == limpio[::-1]


def contar_vocales(texto: str) -> int:
    """Cuenta las vocales del texto, con o sin tilde, mayúsculas o minúsculas."""
    return sum(1 for c in texto.lower() if c in VOCALES)


def invertir_palabras(frase: str) -> str:
    """Devuelve la frase con las palabras en orden inverso y un solo espacio entre ellas."""
    return " ".join(frase.split()[::-1])


def a_snake_case(texto: str) -> str:
    """Convierte un texto con palabras separadas por espacios o guiones en snake_case."""
    return "_".join(texto.replace("-", " ").lower().split())


def enmascarar(numero: str, visibles: int = 4) -> str:
    """Sustituye por asteriscos todos los caracteres salvo los últimos ``visibles``."""
    if len(numero) <= visibles:
        return numero
    ocultos = len(numero) - visibles
    return "*" * ocultos + numero[ocultos:]


def son_anagramas(a: str, b: str) -> bool:
    """Indica si las dos palabras tienen las mismas letras en distinto orden."""
    limpio_a = a.replace(" ", "").lower()
    limpio_b = b.replace(" ", "").lower()
    return sorted(limpio_a) == sorted(limpio_b)


def parsear_configuracion(texto: str) -> dict[str, str]:
    """Convierte un texto ``clave=valor;clave=valor`` en un diccionario."""
    config = {}
    for fragmento in texto.split(";"):
        if "=" not in fragmento:
            continue
        clave, valor = fragmento.split("=", 1)
        clave = clave.strip()
        if clave:
            config[clave] = valor.strip()
    return config


def formatear_tabla(filas: list[tuple[str, float]]) -> str:
    """Devuelve una tabla de texto con una línea por fila."""
    return "\n".join(f"{nombre:<12}{importe:>10.2f}" for nombre, importe in filas)