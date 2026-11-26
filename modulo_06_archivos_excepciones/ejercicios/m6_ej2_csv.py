"""Módulo 6 - Ejercicio 2: CSV.

Todos los ficheros se abren con ``encoding="utf-8"`` y ``newline=""``.
"""

import csv
from pathlib import Path


def leer_csv(ruta, delimitador: str = ",") -> list[dict]:
    """Devuelve las filas del CSV como lista de diccionarios.

    Las claves son los nombres de la cabecera y todos los valores son cadenas.
    """
    with open(ruta, encoding="utf-8", newline="") as fichero:
        return list(csv.DictReader(fichero, delimiter=delimitador))


def cabecera(ruta) -> list[str]:
    """Devuelve la lista de nombres de columna. Con el fichero vacío, lista vacía."""
    with open(ruta, encoding="utf-8", newline="") as fichero:
        lector = csv.reader(fichero)
        return next(lector, [])


def escribir_csv(ruta, registros: list[dict], campos: list[str]) -> None:
    """Escribe los registros en un CSV con la cabecera indicada en ``campos``.

    Las claves de los registros que no estén en ``campos`` se ignoran.
    """
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="") as fichero:
        escritor = csv.DictWriter(fichero, fieldnames=campos, extrasaction="ignore")
        escritor.writeheader()
        escritor.writerows(registros)


def leer_ventas(ruta) -> list[dict]:
    """Lee un CSV de ventas y convierte ``unidades`` a ``int`` y ``precio`` a ``float``.

    El resto de los campos se dejan como cadenas.
    """
    ventas: list[dict] = []
    with open(ruta, encoding="utf-8", newline="") as fichero:
        for fila in csv.DictReader(fichero):
            venta = dict(fila)
            venta["unidades"] = int(fila["unidades"])
            venta["precio"] = float(fila["precio"])
            ventas.append(venta)
    return ventas


def total_columna(ruta, columna: str) -> float:
    """Devuelve la suma de los valores de una columna numérica, con dos decimales."""
    with open(ruta, encoding="utf-8", newline="") as fichero:
        total = sum(float(fila[columna]) for fila in csv.DictReader(fichero))
    return round(total, 2)


def filtrar_csv(origen, destino, columna: str, valor: str) -> int:
    """Copia en ``destino`` las filas de ``origen`` en las que ``columna`` vale ``valor``.

    El fichero de destino conserva la cabecera y el orden de las columnas.
    Devuelve el número de filas copiadas.
    """
    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    copiadas = 0
    with (
        open(origen, encoding="utf-8", newline="") as f_origen,
        open(destino, "w", encoding="utf-8", newline="") as f_destino,
    ):
        lector = csv.DictReader(f_origen)
        campos = lector.fieldnames or []
        escritor = csv.DictWriter(f_destino, fieldnames=campos)
        if campos:
            escritor.writeheader()
        for fila in lector:
            if fila[columna] == valor:
                escritor.writerow(fila)
                copiadas += 1
    return copiadas


def convertir_delimitador(origen, destino, de: str = ";", a: str = ",") -> None:
    """Reescribe un CSV cambiando el delimitador.

    Tiene que funcionar aunque algún campo contenga cualquiera de los dos
    delimitadores: usa ``csv.reader`` y ``csv.writer``, no ``replace``.
    """
    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    with (
        open(origen, encoding="utf-8", newline="") as f_origen,
        open(destino, "w", encoding="utf-8", newline="") as f_destino,
    ):
        lector = csv.reader(f_origen, delimiter=de)
        escritor = csv.writer(f_destino, delimiter=a)
        escritor.writerows(lector)