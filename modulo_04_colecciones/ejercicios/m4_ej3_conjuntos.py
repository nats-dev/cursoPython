"""Módulo 4 - Ejercicio 3: conjuntos."""

import string


def elementos_comunes(a: list, b: list) -> list:
    """Devuelve, ordenados y sin repetir, los elementos que están en las dos listas."""
    return sorted(set(a) & set(b))


def solo_en_una(a: list, b: list) -> list:
    """Devuelve, ordenados, los elementos que están en una lista pero no en las dos."""
    return sorted(set(a) ^ set(b))


def tiene_duplicados(elementos: list) -> bool:
    """Indica si algún elemento aparece más de una vez."""
    return len(elementos) != len(set(elementos))


def duplicados(elementos: list) -> list:
    """Devuelve, ordenados y sin repetir, los elementos que aparecen más de una vez."""
    vistos = set()
    repetidos = set()
    for elemento in elementos:
        if elemento in vistos:
            repetidos.add(elemento)
        else:
            vistos.add(elemento)
    return sorted(repetidos)


def es_pangrama(frase: str) -> bool:
    """Indica si la frase contiene todas las letras de la «a» a la «z»."""
    return set(string.ascii_lowercase) <= set(frase.lower())


def permisos_que_faltan(requeridos: list[str], concedidos: list[str]) -> list[str]:
    """Devuelve, ordenados, los permisos requeridos que no están concedidos."""
    return sorted(set(requeridos) - set(concedidos))


def habilidades_compartidas(equipo: dict[str, list[str]]) -> list[str]:
    """Devuelve, ordenadas, las habilidades que tienen todas las personas del equipo."""
    if not equipo:
        return []
    conjuntos = [set(habilidades) for habilidades in equipo.values()]
    return sorted(set.intersection(*conjuntos))