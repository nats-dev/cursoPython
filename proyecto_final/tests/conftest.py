"""Fixtures compartidas por todos los tests."""

from datetime import date

import pytest

HOY = date(2026, 11, 26)  # jueves; el lunes de esa semana es el 23


@pytest.fixture
def hoy():
    return HOY


@pytest.fixture
def gestor():
    from habitos.gestor import GestorHabitos  # import local: no hace falta para los tests de rachas o modelo

    return GestorHabitos()
