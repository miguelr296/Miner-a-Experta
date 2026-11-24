from pathlib import Path
import json
import subprocess
import sys

import pytest

from src.mina import cargar_mina
from src.motor import Hecho, inferir
from src.planificador import buscar_ruta
from src.reglas import reglas_de_cierre_por_co


RAIZ = Path(__file__).resolve().parents[1]
DATOS = RAIZ / "data"


def test_carga_mina_bidireccional_y_frentes_con_refugio():
    mina = cargar_mina(DATOS / "mina_prueba.json")
    assert len(mina.nodos) == 7
    assert any(a.id == "t_i2_f1" and a.destino == "i2" for a in mina.vecinos("f1"))
    assert any(a.id == "t_i2_f1" and a.destino == "f1" for a in mina.vecinos("i2"))
    for frente in ("f1", "f2"):
        ruta = buscar_ruta(mina, frente, ["r1"], [])
        assert ruta.longitud <= 500


@pytest.mark.parametrize(
    ("campo", "valor", "mensaje"),
    [
        ("destino", "desconocido", "Extremos inválidos"),
        ("longitud", -1, "Longitud inválida"),
        ("longitud", True, "Longitud inválida"),
    ],
)
def test_carga_rechaza_aristas_invalidas(tmp_path, campo, valor, mensaje):
    datos = json.loads((DATOS / "mina_prueba.json").read_text(encoding="utf-8"))
    datos["aristas"][0][campo] = valor
    ruta = tmp_path / "mina.json"
    ruta.write_text(json.dumps(datos), encoding="utf-8")
    with pytest.raises(ValueError, match=mensaje):
        cargar_mina(ruta)


def test_inferencia_cierra_el_atajo_y_dijkstra_usa_el_desvio():
    mina = cargar_mina(DATOS / "mina_prueba.json")
    normal = buscar_ruta(mina, "f1", ["s1"], [])
    assert normal.nodos == ("f1", "i2", "i1", "s1")
    assert normal.longitud == 160
    resultado = inferir([Hecho("t_i2_f1", "co_ppm", 101)], reglas_de_cierre_por_co(100))

    desvio = buscar_ruta(mina, "f1", ["s1"], resultado.hechos)
    assert desvio.nodos == ("f1", "i3", "i1", "s1")
    assert desvio.longitud == 265
    assert "t_i2_f1" not in desvio.aristas


def test_dijkstra_usa_costos_y_devuelve_none_si_no_hay_acceso():
    mina = cargar_mina(DATOS / "mina_prueba.json")
    ruta = buscar_ruta(mina, "f1", ["s1"], [Hecho("t_i2_f1", "multiplicador", 5)])
    assert ruta.costo == 265
    assert ruta.nodos[1] == "i3"

    cierres = [
        Hecho("t_i2_f1", "cerrado", True),
        Hecho("t_i3_f1", "transitable", False),
    ]
    assert buscar_ruta(mina, "f1", ["s1", "r1"], cierres) is None


def test_consola_muestra_inferencia_y_rutas():
    resultado = subprocess.run(
        [sys.executable, "-m", "src"], cwd=RAIZ, check=True, capture_output=True,
        text=True, encoding="utf-8",
    )
    assert "R-RUTA-01" in resultado.stdout
    assert "m1: Salida | f1 -> i3 -> i1 -> s1 | 265 m" in resultado.stdout
    assert "m2: Salida | f2 -> i3 -> i1 -> s1 | 205 m" in resultado.stdout
