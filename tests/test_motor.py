import json
from pathlib import Path

from src.motor import Condicion, Hecho, Regla, inferir
from src.reglas import reglas_del_motor


UMBRAL_JSON = Path(__file__).resolve().parents[1] / "data" / "umbrales.json"
CONFIGURACION = json.loads(UMBRAL_JSON.read_text(encoding="utf-8"))


def test_cadena_co_identifica_y_cierra_solo_el_tunel_afectado():
    resultado = inferir(
        [Hecho("afectado", "co_ppm", 101), Hecho("límite", "co_ppm", 100)],
        reglas_del_motor(CONFIGURACION),
    )

    traza = [paso for paso in resultado.traza if paso.conclusion.entidad == "afectado"]
    assert [paso.regla for paso in traza] == [
        "R-CO-03", "R-RIESGO-07", "R-RIESGO-01", "R-RUTA-01",
    ]
    assert traza[0].premisas == (Hecho("afectado", "co_ppm", 101),)
    assert traza[-1].premisas == (Hecho("afectado", "cerrado", True),)
    assert all(paso.fuente == "SUPUESTO" for paso in traza)
    assert Hecho("afectado", "transitable", False) in resultado.hechos
    assert Hecho("límite", "nivel_riesgo", "alto") in resultado.hechos
    assert Hecho("límite", "cerrado", True) not in resultado.hechos


def test_prioridad_protege_conclusion_y_refraccion_es_por_entidad():
    condicion = (Condicion("evento", "=", True),)
    reglas = (
        Regla("BAJA", 10, condicion, "riesgo", "alerta"),
        Regla("ALTA", 20, condicion, "riesgo", "alto"),
    )
    hechos = [Hecho("a", "evento", True), Hecho("b", "evento", True)]
    resultado = inferir(hechos, reglas)

    assert [(paso.regla, paso.conclusion.entidad) for paso in resultado.traza] == [
        ("ALTA", "a"), ("ALTA", "b"),
    ]
    assert inferir(hechos, reglas) == resultado


def test_ausencia_y_booleanos_no_cumplen_condiciones_numericas():
    regla = Regla("MEDICION", 10, (Condicion("co_ppm", ">", 0),), "riesgo", "alerta")
    resultado = inferir(
        [Hecho("a", "evento", True), Hecho("b", "co_ppm", True)],
        [regla],
    )

    assert not resultado.traza
    assert not Condicion("evento", "=", True).cumple(1)


def test_limites_de_los_cinco_gases_y_costos():
    reglas = reglas_del_motor(CONFIGURACION)
    for gas in CONFIGURACION["gases"].values():
        delta = -0.01 if gas["operador"] == "<" else 0.01
        for nivel, previo in (("alerta", "normal"), ("alto", "alerta"), ("peligro", "alto")):
            limite = gas[nivel]
            for valor, esperado in ((limite, previo), (limite + delta, nivel)):
                resultado = inferir([Hecho("t", gas["atributo"], valor)], reglas)
                memoria = {h.atributo: h.valor for h in resultado.hechos}
                assert memoria.get("nivel_riesgo", "normal") == esperado
                assert memoria.get("cerrado", False) is (esperado == "peligro")
                if esperado in ("alerta", "alto"):
                    assert memoria["multiplicador"] == CONFIGURACION["multiplicadores"][esperado]


def test_agregacion_elige_el_gas_mas_severo_y_registra_su_premisa():
    escala = reglas_del_motor(CONFIGURACION)
    resultado = inferir(
        [Hecho("t", "co_ppm", 30), Hecho("t", "no2_ppm", 6), Hecho("t", "o2_pct", 15)],
        escala,
    )
    assert Hecho("t", "nivel_riesgo", "peligro") in resultado.hechos
    assert Hecho("t", "transitable", False) in resultado.hechos
    agregacion = next(p for p in resultado.traza if p.regla == "R-RIESGO-07")
    assert agregacion.premisas == (Hecho("t", "nivel_o2", "peligro"),)
