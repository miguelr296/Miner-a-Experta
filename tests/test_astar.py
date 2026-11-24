from pathlib import Path
import json
import subprocess
import sys

import pytest

from src.mina import cargar_mina, mina_desde_datos
from src.motor import Hecho
from src.planificador import buscar_ruta


RAIZ = Path(__file__).resolve().parents[1]
DATOS = RAIZ / "data"


def test_astar_conserva_costo_y_reduce_exploracion_en_la_demo():
    mina = cargar_mina(DATOS / "mina_prueba.json")
    hechos = (Hecho("t_i1_i2", "multiplicador", 3), Hecho("t_i1_i2", "nivel_riesgo", "alto"))
    dijkstra = buscar_ruta(mina, "f1", ["s1"], hechos)
    astar = buscar_ruta(mina, "f1", ["s1"], hechos, algoritmo="astar")
    assert astar.nodos == dijkstra.nodos == ("f1", "i3", "i1", "s1")
    assert astar.costo == dijkstra.costo == 265
    assert astar.puntaje_riesgo == dijkstra.puntaje_riesgo == 0
    assert astar.nodos_explorados < dijkstra.nodos_explorados


def test_astar_coincide_en_empates_varias_metas_y_cierres():
    mina = cargar_mina(DATOS / "mina_prueba.json")
    escenarios = [
        (),
        (Hecho("t_i2_f1", "cerrado", True),),
        (Hecho("t_i2_f1", "cerrado", True), Hecho("t_i3_f1", "transitable", False)),
        (Hecho("t_i1_i2", "multiplicador", 2.75), Hecho("t_i1_i2", "nivel_riesgo", "alto")),
    ]
    for hechos in escenarios:
        for origen in mina.nodos:
            for metas in (["s1"], ["r1"], ["r1", "s1"]):
                dijkstra = buscar_ruta(mina, origen, metas, hechos)
                astar = buscar_ruta(mina, origen, metas, hechos, algoritmo="astar")
                if dijkstra is None:
                    assert astar is None
                else:
                    assert astar is not None
                    assert astar.nodos[-1] in metas
                    assert (astar.costo, astar.puntaje_riesgo) == (dijkstra.costo, dijkstra.puntaje_riesgo)


def test_astar_rechaza_coordenadas_ausentes_y_longitudes_incoherentes():
    datos = json.loads((DATOS / "mina_prueba.json").read_text(encoding="utf-8"))
    nodo = datos["nodos"][0]
    z = nodo.pop("z")
    with pytest.raises(ValueError, match="x, y y z"):
        buscar_ruta(mina_desde_datos(datos), "f1", ["s1"], [], algoritmo="astar")
    nodo["z"] = z - 500
    with pytest.raises(ValueError, match="distancia 3D"):
        buscar_ruta(mina_desde_datos(datos), "f1", ["s1"], [], algoritmo="astar")


def test_consola_compara_exploracion_y_costos():
    resultado = subprocess.run(
        [sys.executable, "-X", "utf8", "-m", "src",
         "data/escenarios/desvio_riesgo.json", "--comparar-algoritmos"],
        cwd=RAIZ, check=True, capture_output=True, text=True, encoding="utf-8",
    )
    assert "Dijkstra: costo 265, 7 nodos explorados | A*: costo 265, 6 nodos explorados" in resultado.stdout
