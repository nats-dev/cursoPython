"""Módulo 4 - Ejercicio 4: comprensiones."""


def cuadrados_de_pares(limite: int) -> list[int]:
    """Devuelve los cuadrados de los números pares entre 0 y ``limite``, incluido."""
    return [n ** 2 for n in range(limite + 1) if n % 2 == 0]


def longitudes(palabras: list[str]) -> dict[str, int]:
    """Devuelve un diccionario que asocia cada palabra con su longitud."""
    return {palabra: len(palabra) for palabra in palabras}


def iniciales(nombres: list[str]) -> set[str]:
    """Devuelve el conjunto de iniciales, en mayúscula, de los nombres no vacíos."""
    return {nombre[0].upper() for nombre in nombres if nombre}


def limpiar(textos: list[str]) -> list[str]:
    """Devuelve los textos sin espacios alrededor y en minúsculas."""
    return [texto.strip().lower() for texto in textos if texto.strip()]


def filtrar_por_precio(precios: dict[str, float], maximo: float) -> dict[str, float]:
    """Devuelve los productos cuyo precio es menor o igual que ``maximo``."""
    return {producto: precio for producto, precio in precios.items() if precio <= maximo}


def aplanar(matriz: list[list]) -> list:
    """Devuelve una lista con todos los elementos de una lista de listas."""
    return [elemento for fila in matriz for elemento in fila]


def trasponer(matriz: list[list]) -> list[list]:
    """Devuelve la matriz traspuesta: las filas pasan a ser columnas."""
    return [list(columna) for columna in zip(*matriz)]


def suma_de_importes(lineas: list[dict]) -> float:
    """Devuelve la suma de ``unidades * precio`` de todas las líneas, con dos decimales."""
    return round(sum(linea["unidades"] * linea["precio"] for linea in lineas), 2)