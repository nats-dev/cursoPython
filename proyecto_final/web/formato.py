"""Pequeñas funciones de formato para las plantillas (todo en español)."""

from datetime import date

from habitos.modelo import Habito

DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def fecha_larga(dia: date) -> str:
    """«jueves, 26 de noviembre»"""
    return f"{DIAS[dia.weekday()]}, {dia.day} de {MESES[dia.month - 1]}"


def racha_texto(habito: Habito, hoy: date) -> str:
    """«1 día», «5 días», «1 semana», «3 semanas»"""
    n = habito.racha_actual(hoy)
    singular, plural = ("día", "días") if habito.es_diario else ("semana", "semanas")
    return f"{n} {singular if n == 1 else plural}"


def etiqueta_frecuencia(veces_semana: int) -> str:
    return "Todos los días" if veces_semana == 7 else f"{veces_semana} {'vez' if veces_semana == 1 else 'veces'} por semana"


def porcentaje(proporcion: float) -> int:
    return round(proporcion * 100)


def unidad(cantidad: int, plural: str) -> str:
    """Pone la unidad en singular si la cantidad es 1: («1 día», «2 días», «1 semana»)."""
    return plural[:-1] if cantidad == 1 else plural
