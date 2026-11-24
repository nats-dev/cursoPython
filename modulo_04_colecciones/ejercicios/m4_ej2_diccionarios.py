"""Módulo 4 - Ejercicio 2: tuplas y diccionarios."""


def punto_medio(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:
    """Devuelve el punto medio entre dos puntos (x, y)."""
    x1, y1 = a
    x2, y2 = b
    return ((x1 + x2) / 2, (y1 + y2) / 2)


def contar_palabras(texto: str) -> dict[str, int]:
    """Devuelve cuántas veces aparece cada palabra, en minúsculas."""
    conteo = {}
    for palabra in texto.lower().split():
        conteo[palabra] = conteo.get(palabra, 0) + 1
    return conteo


def invertir(diccionario: dict) -> dict:
    """Devuelve un diccionario nuevo con las claves y los valores intercambiados."""
    return {valor: clave for clave, valor in diccionario.items()}


def notas_medias(estudiantes: dict[str, list[float]]) -> dict[str, float]:
    """Devuelve la nota media de cada estudiante, redondeada a dos decimales."""
    medias = {}
    for nombre, notas in estudiantes.items():
        medias[nombre] = round(sum(notas) / len(notas), 2) if notas else 0.0
    return medias


def mejor_estudiante(estudiantes: dict[str, list[float]]) -> str | None:
    """Devuelve el nombre del estudiante con la media más alta."""
    medias = notas_medias(estudiantes)
    if not medias:
        return None
    return max(medias, key=lambda nombre: medias[nombre])


def total_carrito(carrito: list[tuple[str, int, float]]) -> float:
    """Devuelve el importe total de un carrito, redondeado a dos decimales."""
    total = 0.0
    for _, unidades, precio in carrito:
        total += unidades * precio
    return round(total, 2)


def fusionar_inventarios(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    """Devuelve un inventario nuevo con las unidades de ``a`` y ``b`` sumadas."""
    resultado = a.copy()
    for producto, unidades in b.items():
        resultado[producto] = resultado.get(producto, 0) + unidades
    return resultado


def valor_anidado(datos: dict, ruta: str, por_defecto=None):
    """Devuelve el valor situado en ``ruta`` dentro de diccionarios anidados."""
    actual = datos
    for clave in ruta.split("."):
        if not isinstance(actual, dict) or clave not in actual:
            return por_defecto
        actual = actual[clave]
    return actual