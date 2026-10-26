"""Casos de aceptación de los ejercicios de nivelación."""

import pytest

from ejercicios.nivelacion import (
    buscar_por_tipo,
    buscar_por_tipo_comprension,
    distancia_total,
    entidades_con_derrumbe,
)


@pytest.mark.parametrize("tramos, esperado", [
    ([120, 80, 150], 350), ([], 0), ([25], 25), ([0, 1.5, 2.5], 4),
])
def test_distancia_total(tramos, esperado):
    assert distancia_total(tramos) == esperado


@pytest.mark.parametrize("buscar", [buscar_por_tipo, buscar_por_tipo_comprension])
@pytest.mark.parametrize("tipo, esperado", [
    ("refugio", ["n3", "n5"]), ("salida", ["n4"]), ("otro", []),
])
def test_busqueda_por_tipo(buscar, tipo, esperado):
    nodos = {"n1": "frente", "n2": "intersección", "n3": "refugio",
             "n4": "salida", "n5": "refugio"}
    assert buscar(nodos, tipo) == esperado


@pytest.mark.parametrize("buscar", [buscar_por_tipo, buscar_por_tipo_comprension])
def test_busqueda_sin_nodos(buscar):
    assert buscar({}, "refugio") == []


def test_eventos_repetidos_y_filtros():
    eventos = [("tunel_1_2", "derrumbe_reportado", True),
               ("tunel_2_3", "derrumbe_reportado", False),
               ("tunel_1_2", "derrumbe_reportado", True),
               ("tunel_3_4", "derrumbe_reportado", True),
               ("tunel_4_5", "otro_atributo", True),
               ("tunel_5_6", "derrumbe_reportado", "False")]
    assert entidades_con_derrumbe(eventos) == {"tunel_1_2", "tunel_3_4"}


def test_sin_eventos():
    assert entidades_con_derrumbe([]) == set()
