"""Módulo 5 - Ejercicio 4: polimorfismo y duck typing.

Las tres clases de exportación no comparten clase base: lo único que tienen
en común es el método ``exportar``.
"""


class ExportadorCsv:
    """Exporta registros como texto CSV separado por punto y coma."""

    extension = "csv"

    def exportar(self, registros: list[dict]) -> str:
        """Devuelve una línea de cabecera y una línea por registro.

        Las columnas son las claves del primer registro. Sin registros
        devuelve la cadena vacía.

        >>> print(ExportadorCsv().exportar([{"id": 1, "nombre": "Ada"}]))
        id;nombre
        1;Ada
        """
        if not registros:
            return ""
        columnas = list(registros[0].keys())
        lineas = [";".join(str(c) for c in columnas)]
        for reg in registros:
            lineas.append(";".join(str(reg.get(c, "")) for c in columnas))
        return "\n".join(lineas)


class ExportadorTexto:
    """Exporta cada registro como una línea "clave=valor, clave=valor"."""

    extension = "txt"

    def exportar(self, registros: list[dict]) -> str:
        """Devuelve una línea por registro.

        >>> ExportadorTexto().exportar([{"id": 1, "nombre": "Ada"}])
        'id=1, nombre=Ada'
        """
        return "\n".join(
            ", ".join(f"{clave}={valor}" for clave, valor in reg.items())
            for reg in registros
        )


class ExportadorMarkdown:
    """Exporta registros como una tabla Markdown."""

    extension = "md"

    def exportar(self, registros: list[dict]) -> str:
        """Devuelve la cabecera, la línea de guiones y una fila por registro.

        Sin registros devuelve la cadena vacía.

        >>> print(ExportadorMarkdown().exportar([{"id": 1, "nombre": "Ada"}]))
        | id | nombre |
        | --- | --- |
        | 1 | Ada |
        """
        if not registros:
            return ""
        columnas = list(registros[0].keys())
        cabecera = "| " + " | ".join(str(c) for c in columnas) + " |"
        separador = "| " + " | ".join("---" for _ in columnas) + " |"
        filas = [
            "| " + " | ".join(str(reg.get(c, "")) for c in columnas) + " |"
            for reg in registros
        ]
        return "\n".join([cabecera, separador, *filas])


def exportar_con(exportador, registros: list[dict]) -> str:
    """Exporta los registros con el exportador recibido.

    No puede comprobar de qué clase es el exportador: tiene que funcionar
    con cualquier objeto que tenga un método ``exportar``.
    """
    return exportador.exportar(registros)


def nombre_de_fichero(exportador, nombre: str) -> str:
    """Devuelve "nombre.extension" usando el atributo ``extension`` del exportador.

    >>> nombre_de_fichero(ExportadorCsv(), "ventas")
    'ventas.csv'
    """
    return f"{nombre}.{exportador.extension}"


def exportar_a_todos(exportadores: list, registros: list[dict]) -> dict[str, str]:
    """Devuelve un diccionario que asocia cada extensión con su texto exportado."""
    return {exp.extension: exp.exportar(registros) for exp in exportadores}


def puede_exportar(objeto) -> bool:
    """Indica si el objeto tiene un método ``exportar`` que se pueda llamar.

    >>> puede_exportar(ExportadorCsv()), puede_exportar("texto")
    (True, False)
    """
    return callable(getattr(objeto, "exportar", None))