"""Jerarquía de excepciones propia de la aplicación.

ErrorHabitos
├── HabitoInvalido      datos de un hábito que no cumplen las reglas
├── HabitoDuplicado     ya existe un hábito activo con ese nombre
├── HabitoNoEncontrado  el identificador no existe
├── HabitoArchivado     operación no permitida sobre un hábito archivado
├── FechaInvalida       fecha futura o con formato incorrecto
└── ErrorAlmacen        problemas al leer o escribir los CSV
"""


class ErrorHabitos(Exception):
    """Base de todos los errores de la aplicación."""


class HabitoInvalido(ErrorHabitos):
    """Los datos de un hábito no cumplen las reglas del dominio."""


class HabitoDuplicado(ErrorHabitos):
    """Ya existe un hábito activo con ese nombre."""


class HabitoNoEncontrado(ErrorHabitos):
    """No existe ningún hábito con ese identificador."""

    def __init__(self, id_habito):
        super().__init__(f"No existe el hábito {id_habito}")
        self.id_habito = id_habito


class HabitoArchivado(ErrorHabitos):
    """Un hábito archivado no admite registros nuevos."""


class FechaInvalida(ErrorHabitos):
    """La fecha es futura o no tiene el formato AAAA-MM-DD."""


class ErrorAlmacen(ErrorHabitos):
    """Fallo al leer o escribir los ficheros de datos."""
