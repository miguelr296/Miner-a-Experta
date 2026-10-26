"""Filtro directo independiente del motor y aplicado a los datos originales."""

from pathlib import Path

import pytest

from mina_experta.cargador import cargar_mina
from mina_experta.linea_base import costos_linea_base
from mina_experta.motor import Motor
from mina_experta.planificador import ruta_menor_costo


@pytest.fixture
def mina():
    return cargar_mina(Path(__file__).resolve().parents[1] / "data/mina_prueba.json")


@pytest.mark.parametrize("valor, cerrado", [(25, False), (25.01, True), (100, True)])
def test_frontera_sensor_y_no_motor(mina, monkeypatch, valor, cerrado):
    def prohibido(*args, **kwargs):
        raise AssertionError("La línea base no debe llamar al motor")
    monkeypatch.setattr(Motor, "ejecutar", prohibido)
    costos = costos_linea_base(mina, [("tunel_2_3", "co_ppm", valor)], 25)
    assert (costos["tunel_2_3"] is None) is cerrado
    assert (ruta_menor_costo(mina, "n5", costos=costos) is None) is cerrado
    assert mina.aristas["tunel_2_3"].longitud_m == 100


@pytest.mark.parametrize("atributo", ["incendio_reportado", "derrumbe_reportado"])
def test_eventos_directos(mina, atributo):
    assert costos_linea_base(mina, [("tunel_4_5", atributo, True)], 25)["tunel_4_5"] is None
    assert costos_linea_base(mina, [("tunel_4_5", atributo, False)], 25)["tunel_4_5"] == 150


def test_no_es_dijkstra_ciego_y_umbral_configurable(mina):
    lectura = [("tunel_2_3", "co_ppm", 30)]
    assert costos_linea_base(mina, lectura, 25)["tunel_2_3"] is None
    assert costos_linea_base(mina, lectura, 40)["tunel_2_3"] == 100


def test_rechaza_conclusiones_inferidas_y_umbrales_invalidos(mina):
    with pytest.raises(ValueError, match="no permitido"):
        costos_linea_base(mina, [("tunel_2_3", "cerrado", True)], 25)
    for limite in (0, -1, True, float("nan")):
        with pytest.raises(ValueError):
            costos_linea_base(mina, [], limite)
