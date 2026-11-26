from datetime import date, timedelta

import pytest

from habitos import rachas

HOY = date(2026, 11, 26)  # jueves


def dias_atras(*cuantos):
    return {HOY - timedelta(days=n) for n in cuantos}


@pytest.mark.parametrize(
    "atras, esperada",
    [
        ((), 0),
        ((0,), 1),
        ((0, 1, 2), 3),
        ((1, 2, 3), 3),      # hoy aún no marcado: la racha sigue viva
        ((2, 3), 0),         # ayer falló: racha rota
        ((0, 1, 3, 4, 5), 2),  # un hueco corta la racha
    ],
)
def test_racha_dias_actual(atras, esperada):
    assert rachas.racha_dias_actual(dias_atras(*atras), HOY) == esperada


def test_mejor_racha_dias():
    assert rachas.mejor_racha_dias(set()) == 0
    assert rachas.mejor_racha_dias(dias_atras(0, 1, 5, 6, 7, 8, 20)) == 4


def test_lunes_de():
    assert rachas.lunes_de(date(2026, 11, 26)) == date(2026, 11, 23)
    assert rachas.lunes_de(date(2026, 11, 23)) == date(2026, 11, 23)
    assert rachas.lunes_de(date(2026, 11, 29)) == date(2026, 11, 23)  # domingo


def test_semanas_cumplidas():
    fechas = {date(2026, 11, 23), date(2026, 11, 24), date(2026, 11, 25),  # 3 esta semana
              date(2026, 11, 16)}                                          # 1 la anterior
    assert rachas.semanas_cumplidas(fechas, 3) == {date(2026, 11, 23)}


def test_racha_semanas_actual_con_semana_en_curso_cumplida():
    # objetivo 2: semanas del 9, 16 y 23 de noviembre cumplidas
    fechas = {date(2026, 11, 9), date(2026, 11, 10), date(2026, 11, 16), date(2026, 11, 17),
              date(2026, 11, 23), date(2026, 11, 24)}
    assert rachas.racha_semanas_actual(fechas, HOY, 2) == 3


def test_racha_semanas_actual_semana_en_curso_aun_sin_cumplir():
    # las dos semanas anteriores cumplidas; esta solo lleva 1 de 2
    fechas = {date(2026, 11, 9), date(2026, 11, 10), date(2026, 11, 16), date(2026, 11, 17),
              date(2026, 11, 23)}
    assert rachas.racha_semanas_actual(fechas, HOY, 2) == 2


def test_racha_semanas_se_rompe_con_semana_incumplida():
    fechas = {date(2026, 11, 2), date(2026, 11, 3),      # semana del 2 cumplida
              date(2026, 11, 16), date(2026, 11, 17)}    # semana del 16 cumplida; la del 9, no
    assert rachas.racha_semanas_actual(fechas, HOY, 2) == 1


def test_mejor_racha_semanas():
    fechas = {date(2026, 10, 5), date(2026, 10, 6), date(2026, 10, 12), date(2026, 10, 13),
              date(2026, 10, 19), date(2026, 10, 20),  # 3 semanas seguidas
              date(2026, 11, 2), date(2026, 11, 3)}    # 1 aislada
    assert rachas.mejor_racha_semanas(fechas, 2) == 3
    assert rachas.mejor_racha_semanas(set(), 2) == 0
