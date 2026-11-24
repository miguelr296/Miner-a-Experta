from pathlib import Path
import json

import pytest

from src.decisiones import evaluar_mineros, recomendar
from src.escenarios import cargar_caso_web
from src.motor import inferir
from src.planificador import Ruta
from src.reglas import estados_linea_base, preparar_entrada, reglas_del_motor


DATOS = Path(__file__).resolve().parents[1] / "data"
REFERENCIA = json.loads((DATOS / "referencia_web.json").read_text(encoding="utf-8"))
CONFIGURACION = json.loads((DATOS / "umbrales.json").read_text(encoding="utf-8"))


def resumir(ruta):
    if ruta is None:
        return None
    return {
        "destino": ruta.nodos[-1],
        "nodos": list(ruta.nodos),
        "longitud": ruta.longitud,
        "costo": ruta.costo,
        "puntajeRiesgo": ruta.puntaje_riesgo,
    }


@pytest.mark.parametrize("caso", REFERENCIA["casos"])
def test_rutas_y_decisiones_coinciden_con_web(caso):
    mina, hechos, mineros = cargar_caso_web(REFERENCIA, caso)
    entrada, certezas = preparar_entrada(hechos, mina)
    resultado = inferir(entrada, reglas_del_motor(CONFIGURACION), certezas_iniciales=certezas)
    linea_base = estados_linea_base(hechos, resultado.hechos, CONFIGURACION)
    evaluaciones = evaluar_mineros(
        mina, mineros, resultado.hechos, linea_base, CONFIGURACION["decision"],
    )
    actual = [
        {
            "id": evaluacion.id,
            "decision": evaluacion.decision.accion,
            "regla": evaluacion.decision.regla,
            "asignada": resumir(evaluacion.decision.ruta),
            "lineaBase": resumir(evaluacion.linea_base),
        }
        for evaluacion in evaluaciones
    ]
    esperado = REFERENCIA["casos"][caso]["esperado"]
    assert actual == esperado["mineros"]

    memoria = {(h.entidad, h.atributo): h.valor for h in resultado.hechos}
    afectados = []
    for arista in REFERENCIA["mina"]["aristas"]:
        id_arista = arista["id"]
        nivel = memoria.get((id_arista, "nivel_riesgo"), "normal")
        cerrado = memoria.get((id_arista, "cerrado"), False)
        if nivel != "normal" or cerrado:
            costo = arista["longitud"] * memoria.get((id_arista, "multiplicador"), 1)
            afectados.append([id_arista, nivel, cerrado, None if cerrado else costo])
    assert afectados == esperado["tunelesAfectados"]


def test_refugio_por_riesgo_usa_limites_del_prototipo():
    politica = CONFIGURACION["decision"]
    salida = Ruta(("f1", "s1"), ("a",), 500, 251, 2, 1)
    refugio = Ruta(("f1", "r1"), ("b",), 400, 100, 0)
    lejano = Ruta(("f1", "r1"), ("b",), 401, 100, 0)
    empate = Ruta(("f1", "s1"), ("a",), 500, 250, 2, 1)

    assert recomendar(salida, refugio, politica).accion == "refugiarse"
    assert recomendar(salida, lejano, politica).accion == "evacuar"
    assert recomendar(empate, refugio, politica).accion == "evacuar"
    assert recomendar(None, lejano, politica).accion == "refugiarse"
    assert recomendar(None, None, politica).accion == "esperar"
