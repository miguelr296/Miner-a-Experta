from dataclasses import replace
import json
from pathlib import Path

import pytest

from src.escenarios import cargar_hechos
from src.mina import cargar_mina
from src.motor import Condicion, Hecho, Regla, inferir
from src.reglas import preparar_entrada, reglas_del_motor


DATOS = Path(__file__).resolve().parents[1] / "data"
CONFIGURACION = json.loads((DATOS / "umbrales.json").read_text(encoding="utf-8"))


def test_y_usa_minimo_y_o_usa_la_premisa_con_mas_apoyo():
    hechos = (Hecho("t", "a", True), Hecho("t", "b", True))
    condiciones = (Condicion("a", "=", True), Condicion("b", "=", True))
    conjunta = Regla("Y", 10, condiciones, "y", True, certeza=0.5)
    alternativa = replace(conjunta, id="O", atributo="o", alguna=True)
    resultado = inferir(
        hechos, [conjunta, alternativa],
        certezas_iniciales={("t", "a"): 0.3, ("t", "b"): 0.8},
    )
    assert resultado.certezas["t", "y"] == pytest.approx(0.15)
    assert resultado.certezas["t", "o"] == pytest.approx(0.4)
    assert resultado.traza[0].certezas_premisas == (0.3, 0.8)
    assert resultado.traza[1].premisas == (Hecho("t", "b", True),)


def test_certeza_configurada_se_propaga_sin_reabrir_el_tunel():
    escenario = json.loads((DATOS / "escenarios" / "certeza_demo.json").read_text(encoding="utf-8"))
    hechos, certezas = cargar_hechos(escenario["hechos"])
    configuracion = {**CONFIGURACION, "certeza_reglas": {"R-CO-03": 0.8}}
    resultado = inferir(hechos, reglas_del_motor(configuracion), certezas_iniciales=certezas)
    assert resultado.certezas["t_i2_f1", "transitable"] == pytest.approx(0.36)
    assert Hecho("t_i2_f1", "transitable", False) in resultado.hechos


def test_evento_vecino_conserva_certeza_del_reporte():
    mina = cargar_mina(DATOS / "mina_prueba.json")
    entrada, apoyos = preparar_entrada(
        (Hecho("t_i2_f1", "incendio", True),), mina, {("t_i2_f1", "incendio"): 0.6},
    )
    resultado = inferir(entrada, reglas_del_motor(CONFIGURACION), certezas_iniciales=apoyos)
    assert resultado.certezas["t_i3_f1", "propagacion"] == pytest.approx(0.6)
    assert resultado.certezas["t_i3_f1", "nivel_riesgo"] == pytest.approx(0.6)


@pytest.mark.parametrize("valor", [-0.1, 1.1, True, float("nan")])
def test_rechaza_certeza_invalida(valor):
    with pytest.raises(ValueError, match="entre 0 y 1"):
        cargar_hechos([{"entidad": "t", "atributo": "co_ppm", "valor": 101, "certeza": valor}])
