"""Cálculo de rachas. Son funciones puras: solo trabajan con fechas.

Hay dos tipos de racha, según la frecuencia del hábito:

* Hábito diario (7 veces/semana): racha en **días** consecutivos.
* Hábito semanal (1 a 6 veces/semana): racha en **semanas** consecutivas en
  las que se alcanzó el objetivo. Las semanas van de lunes a domingo.

La racha actual no se rompe por no haber marcado *todavía* hoy (o esta
semana): el día (o la semana) en curso aún puede completarse.
"""

from collections import Counter
from collections.abc import Iterable
from datetime import date, timedelta

UN_DIA = timedelta(days=1)
UNA_SEMANA = timedelta(weeks=1)


def lunes_de(dia: date) -> date:
    """Devuelve el lunes de la semana a la que pertenece ``dia``."""
    return dia - timedelta(days=dia.weekday())


def _mejor_serie(ordenadas: Iterable[date], paso: timedelta) -> int:
    """Longitud de la serie más larga de fechas separadas exactamente ``paso``."""
    mejor = actual = 0
    anterior = None
    for fecha in ordenadas:
        actual = actual + 1 if anterior is not None and fecha - anterior == paso else 1
        mejor = max(mejor, actual)
        anterior = fecha
    return mejor


def racha_dias_actual(fechas: set[date], hoy: date) -> int:
    """Días consecutivos marcados hasta hoy (o hasta ayer si hoy aún no)."""
    dia = hoy if hoy in fechas else hoy - UN_DIA
    racha = 0
    while dia in fechas:
        racha += 1
        dia -= UN_DIA
    return racha


def mejor_racha_dias(fechas: set[date]) -> int:
    """La racha de días consecutivos más larga de todo el historial."""
    return _mejor_serie(sorted(fechas), UN_DIA)


def semanas_cumplidas(fechas: set[date], objetivo: int) -> set[date]:
    """Lunes de las semanas en las que se marcó al menos ``objetivo`` veces."""
    por_semana = Counter(lunes_de(f) for f in fechas)
    return {lunes for lunes, veces in por_semana.items() if veces >= objetivo}


def racha_semanas_actual(fechas: set[date], hoy: date, objetivo: int) -> int:
    """Semanas consecutivas cumpliendo el objetivo hasta la semana actual.

    Si la semana en curso todavía no ha alcanzado el objetivo, se empieza a
    contar desde la anterior.
    """
    cumplidas = semanas_cumplidas(fechas, objetivo)
    lunes = lunes_de(hoy)
    if lunes not in cumplidas:
        lunes -= UNA_SEMANA
    racha = 0
    while lunes in cumplidas:
        racha += 1
        lunes -= UNA_SEMANA
    return racha


def mejor_racha_semanas(fechas: set[date], objetivo: int) -> int:
    """La racha de semanas cumplidas más larga de todo el historial."""
    return _mejor_serie(sorted(semanas_cumplidas(fechas, objetivo)), UNA_SEMANA)
