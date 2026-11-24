"""Módulo 4 - Ejercicio 6: buscar, filtrar, ordenar y agrupar."""


def buscar_por_id(registros: list[dict], identificador: int) -> dict | None:
    """Devuelve el registro cuyo campo "id" coincide, o ``None`` si no existe."""
    for registro in registros:
        if registro["id"] == identificador:
            return registro
    return None


def nombres(registros: list[dict]) -> list[str]:
    """Devuelve la lista con el campo "nombre" de cada registro, en el mismo orden."""
    return [registro["nombre"] for registro in registros]


def filtrar(registros: list[dict], campo: str, valor) -> list[dict]:
    """Devuelve los registros en los que ``campo`` vale ``valor``."""
    return [registro for registro in registros if registro[campo] == valor]


def ordenar_por(registros: list[dict], campo: str, descendente: bool = False) -> list[dict]:
    """Devuelve una lista nueva con los registros ordenados por ``campo``."""
    return sorted(registros, key=lambda r: r[campo], reverse=descendente)


def mejor_pagados(registros: list[dict], cantidad: int = 3) -> list[str]:
    """Devuelve los nombres de los ``cantidad`` empleados con mayor salario."""
    ordenados = sorted(registros, key=lambda r: (-r["salario"], r["nombre"]))
    return [r["nombre"] for r in ordenados[:cantidad]]


def agrupar_por(registros: list[dict], campo: str) -> dict[str, list[dict]]:
    """Agrupa los registros por el valor de ``campo``."""
    grupos = {}
    for registro in registros:
        clave = registro[campo]
        if clave not in grupos:
            grupos[clave] = []
        grupos[clave].append(registro)
    return grupos


def salario_medio_por_departamento(registros: list[dict]) -> dict[str, float]:
    """Devuelve el salario medio de cada departamento, con dos decimales."""
    por_departamento = agrupar_por(registros, "departamento")
    return {
        departamento: round(sum(r["salario"] for r in empleados) / len(empleados), 2)
        for departamento, empleados in por_departamento.items()
    }


def emparejar(claves: list[str], filas: list[list]) -> list[dict]:
    """Convierte filas de valores en diccionarios usando ``claves`` como nombres de campo."""
    return [dict(zip(claves, fila)) for fila in filas]