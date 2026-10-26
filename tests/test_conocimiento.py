"""R01–R03, fronteras de umbrales y cambio de conocimiento por configuración."""

import json
from pathlib import Path

import pytest

from mina_experta.conocimiento import reglas_co, reglas_eventos, reglas_costos
from mina_experta.motor import Motor


RUTA = Path(__file__).resolve().parents[1] / "data/configuracion/umbrales.json"


@pytest.mark.parametrize("co, esperadas", [
    (25, []), (25.01, ["R01"]), (50, ["R01"]),
    (50.01, ["R01", "R02"]), (100, ["R01", "R02"]),
    (100.01, ["R01", "R02", "R03"]),
])
def test_cadena_y_fronteras_co(co, esperadas):
    resultado = Motor(reglas_co(RUTA)).ejecutar([("tunel_1_2", "co_ppm", co)])
    assert [p.regla_id for p in resultado.traza] == esperadas
    assert (("tunel_1_2", "cerrado", True) in resultado.hechos) == ("R03" in esperadas)


def test_cambiar_umbrales_sin_cambiar_motor(tmp_path):
    ruta = tmp_path / "umbrales.json"
    ruta.write_text(json.dumps({"co_ppm": {"alerta": 200, "riesgo_alto": 300,
                                          "peligro_inmediato": 400}}), encoding="utf-8")
    assert Motor(reglas_co(ruta)).ejecutar([("t", "co_ppm", 120)]).traza == ()


@pytest.mark.parametrize("valores", [[25, 20, 100], [True, 50, 100], [0, 50, 100],
                                      [25, 50, float("inf")]])
def test_umbrales_invalidos(tmp_path, valores):
    ruta = tmp_path / "umbrales.json"
    ruta.write_text(json.dumps({"co_ppm": dict(zip(
        ("alerta", "riesgo_alto", "peligro_inmediato"), valores))}), encoding="utf-8")
    with pytest.raises(ValueError):
        reglas_co(ruta)


@pytest.mark.parametrize("atributo, regla_id", [("incendio_reportado", "R04"),
                                               ("derrumbe_reportado", "R05")])
@pytest.mark.parametrize("valor, activa", [(True, True), (False, False), (1, False)])
def test_eventos_reportados(atributo, regla_id, valor, activa):
    resultado = Motor(reglas_eventos()).ejecutar([("t1", atributo, valor)])
    assert [p.regla_id for p in resultado.traza] == ([regla_id] if activa else [])
    assert (("t1", "cerrado", True) in resultado.hechos) is activa


def test_varias_causas_de_cierre_conservan_justificacion():
    resultado = Motor((*reglas_co(RUTA), *reglas_eventos())).ejecutar([
        ("t1", "co_ppm", 120), ("t1", "incendio_reportado", True),
        ("t1", "derrumbe_reportado", True)])
    assert [p.regla_id for p in resultado.traza] == ["R04", "R05", "R01", "R02", "R03"]
    assert len(resultado.por_que(("t1", "cerrado", True))) == 3
    assert resultado.hechos.count(("t1", "cerrado", True)) == 1


@pytest.mark.parametrize("co, factores", [(20, []), (30, [2]), (80, [2, 3])])
def test_reglas_costos_co(co, factores):
    reglas = (*reglas_co(RUTA), *reglas_costos(RUTA.with_name("costos.json")))
    salida = Motor(reglas).ejecutar([("t1", "co_ppm", co)])
    assert [h[2] for h in salida.hechos if h[1] == "multiplicador"] == factores


@pytest.mark.parametrize("alerta, alto", [(0.5, 3), (3, 2), (True, 3), (2, float("inf"))])
def test_configuracion_costos_invalida(tmp_path, alerta, alto):
    ruta = tmp_path / "costos.json"
    ruta.write_text(json.dumps({"multiplicador_alerta_co": alerta,
                               "multiplicador_riesgo_alto_co": alto}), encoding="utf-8")
    with pytest.raises(ValueError):
        reglas_costos(ruta)
