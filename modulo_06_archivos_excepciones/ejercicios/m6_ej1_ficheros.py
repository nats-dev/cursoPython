"""Módulo 6 - Ejercicio 1: lectura y escritura de ficheros de texto.

Todas las rutas pueden llegar como ``str`` o como ``Path``. Todos los
ficheros se abren con ``with`` y con ``encoding="utf-8"``.
"""

from pathlib import Path


def contar_lineas(ruta) -> int:
    """Devuelve el número de líneas del fichero.

    Tiene que recorrer el fichero línea a línea, sin cargarlo entero en memoria.
    """
    with open(ruta, encoding="utf-8") as fichero:
        return sum(1 for _ in fichero)


def leer_lineas_utiles(ruta) -> list[str]:
    """Devuelve las líneas del fichero sin espacios ni saltos alrededor.

    Descarta las líneas vacías y las que empiezan por ``#``.
    """
    utiles: list[str] = []
    with open(ruta, encoding="utf-8") as fichero:
        for linea in fichero:
            limpia = linea.strip()
            if limpia and not limpia.startswith("#"):
                utiles.append(limpia)
    return utiles


def escribir_lineas(ruta, lineas: list[str]) -> None:
    """Escribe cada elemento de la lista en una línea del fichero.

    Si el fichero existe, se sustituye su contenido. Si la carpeta no existe,
    se crea. Cada línea, incluida la última, termina en salto de línea.
    """
    destino = Path(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with open(destino, "w", encoding="utf-8") as fichero:
        for linea in lineas:
            fichero.write(f"{linea}\n")


def anadir_linea(ruta, linea: str) -> None:
    """Añade una línea al final del fichero sin borrar lo que hubiera.

    Si el fichero no existe, lo crea.
    """
    destino = Path(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with open(destino, "a", encoding="utf-8") as fichero:
        fichero.write(f"{linea}\n")


def buscar(ruta, texto: str) -> list[tuple[int, str]]:
    """Devuelve las líneas que contienen el texto, sin distinguir mayúsculas.

    Cada resultado es una tupla (número de línea, línea sin el salto final).
    La primera línea del fichero es la 1.
    """
    objetivo = texto.lower()
    coincidencias: list[tuple[int, str]] = []
    with open(ruta, encoding="utf-8") as fichero:
        for num_linea, linea in enumerate(fichero, start=1):
            sin_salto = linea.rstrip("\r\n")
            if objetivo in sin_salto.lower():
                coincidencias.append((num_linea, sin_salto))
    return coincidencias


def numerar(origen, destino) -> int:
    """Copia ``origen`` en ``destino`` anteponiendo a cada línea su número.

    El formato de cada línea es "  1: texto", con el número alineado a la
    derecha en tres caracteres. Devuelve el número de líneas copiadas.
    """
    ruta_destino = Path(destino)
    ruta_destino.parent.mkdir(parents=True, exist_ok=True)
    copiadas = 0
    with open(origen, encoding="utf-8") as f_origen:
        with open(ruta_destino, "w", encoding="utf-8") as f_destino:
            for num_linea, linea in enumerate(f_origen, start=1):
                sin_salto = linea.rstrip("\r\n")
                f_destino.write(f"{num_linea:3d}: {sin_salto}\n")
                copiadas = num_linea
    return copiadas


def ficheros_por_extension(carpeta, extension: str) -> list[str]:
    """Devuelve, ordenados, los nombres de los ficheros de la carpeta con esa extensión.

    ``extension`` se recibe sin punto. No busca en subcarpetas.

    >>> ficheros_por_extension(".", "no_existe")
    []
    """
    sufijo = f".{extension.lstrip('.')}"
    return sorted(
        entrada.name
        for entrada in Path(carpeta).iterdir()
        if entrada.is_file() and entrada.suffix == sufijo
    )