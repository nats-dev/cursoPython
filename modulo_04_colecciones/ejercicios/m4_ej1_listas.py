"""Módulo 4 - Ejercicio 1: listas."""


def extremos(lista: list) -> tuple:
    """Devuelve una tupla con el primer y el último elemento de la lista."""
    if not lista:
        return (None, None)
    return (lista[0], lista[-1])


def rotar(lista: list, posiciones: int = 1) -> list:
    """Devuelve una lista nueva con los elementos desplazados a la izquierda."""
    if not lista:
        return []
    desplazamiento = posiciones % len(lista)
    return lista[desplazamiento:] + lista[:desplazamiento]


def segundo_mayor(numeros: list[float]) -> float | None:
    """Devuelve el segundo valor más alto, sin contar repetidos."""
    unicos = sorted(set(numeros))
    if len(unicos) < 2:
        return None
    return unicos[-2]


def trocear(lista: list, tamano: int) -> list[list]:
    """Divide la lista en trozos de ``tamano`` elementos."""
    return [lista[i:i + tamano] for i in range(0, len(lista), tamano)]


def sin_duplicados(lista: list) -> list:
    """Devuelve una lista nueva sin repetidos, conservando el orden de aparición."""
    resultado = []
    for elemento in lista:
        if elemento not in resultado:
            resultado.append(elemento)
    return resultado


def insertar_ordenado(ordenada: list[float], valor: float) -> list[float]:
    """Devuelve una lista nueva con ``valor`` insertado en su sitio."""
    resultado = ordenada.copy()
    for i, elemento in enumerate(resultado):
        if valor <= elemento:
            resultado.insert(i, valor)
            return resultado
    resultado.append(valor)
    return resultado


def crear_tablero(filas: int, columnas: int, valor=0) -> list[list]:
    """Devuelve una matriz de ``filas`` x ``columnas`` rellena con ``valor``."""
    return [[valor] * columnas for _ in range(filas)]