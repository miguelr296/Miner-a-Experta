from pathlib import Path
import json
import subprocess
import sys

import pytest

from src.mina import cargar_mina
from src.motor import Hecho, inferir
from src.planificador import buscar_ruta
from src.reglas import estados_linea_base, preparar_hechos, reglas_del_motor


RAIZ = Path(__file__).resolve().parents[1]
DATOS = RAIZ / "data"
CONFIGURACION = json.loads((DATOS / "umbrales.json").read_text(encoding="utf-8"))


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
    resultado = inferir([Hecho("t_i2_f1", "co_ppm", 101)], reglas_del_motor(CONFIGURACION))

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


def test_linea_base_filtra_peligro_pero_ignora_multiplicadores():
    mina = cargar_mina(DATOS / "mina_prueba.json")
    reglas = reglas_del_motor(CONFIGURACION)
    hechos = (Hecho("t_i1_i2", "co_ppm", 55),)
    resultado = inferir(hechos, reglas)
    experta = buscar_ruta(mina, "f1", ["s1"], resultado.hechos)
    base = buscar_ruta(
        mina, "f1", ["s1"], estados_linea_base(hechos, resultado.hechos, CONFIGURACION),
        ponderar_riesgo=False,
    )
    assert (experta.longitud, experta.puntaje_riesgo) == (265, 0)
    assert (base.longitud, base.puntaje_riesgo) == (160, 2)

    critico = (Hecho("t_i2_f1", "o2_pct", 15),)
    base_critica = estados_linea_base(critico, (), CONFIGURACION)
    assert buscar_ruta(mina, "f1", ["s1"], base_critica, ponderar_riesgo=False).longitud == 265


def test_ruta_experta_desempata_por_riesgo():
    mina = cargar_mina(DATOS / "mina_prueba.json")
    hechos = [
        Hecho("t_i1_i2", "nivel_riesgo", "alto"),
        Hecho("t_i1_i2", "multiplicador", 2.75),
    ]
    ruta = buscar_ruta(mina, "f1", ["s1"], hechos)
    assert ruta.costo == 265
    assert ruta.nodos == ("f1", "i3", "i1", "s1")
    assert ruta.puntaje_riesgo == 0


def test_consola_compara_desvio_y_linea_base():
    resultado = subprocess.run(
        [sys.executable, "-X", "utf8", "-m", "src", "data/escenarios/desvio_riesgo.json"],
        cwd=RAIZ, check=True, capture_output=True, text=True, encoding="utf-8",
    )
    assert "R-RIESGO-05" in resultado.stdout
    assert "265 m | costo 265 | riesgo 0" in resultado.stdout
    assert "Línea base: f1 -> i2 -> i1 -> s1 | 160 m | riesgo 2" in resultado.stdout


@pytest.mark.parametrize(
    ("velocidad", "anfo", "esperado", "regla"),
    [
        (19, False, "insuficiente", "R-VEN-01"),
        (20, False, "conforme", "R-VEN-03"),
        (23, True, "critica", "R-VEN-02"),
        (25, True, "conforme", "R-VEN-03"),
    ],
)
def test_ventilacion_con_y_sin_anfo(velocidad, anfo, esperado, regla):
    hechos = (Hecho("t", "vel_m_min", velocidad), Hecho("t", "anfo", anfo))
    resultado = inferir(hechos, reglas_del_motor(CONFIGURACION))
    assert Hecho("t", "nivel_ventilacion", esperado) in resultado.hechos
    assert [p.regla for p in resultado.traza if p.conclusion.atributo == "nivel_ventilacion"] == [regla]
    if esperado == "critica":
        conflicto = next(c for c in resultado.conflictos if c.regla == "R-VEN-03")
        assert conflicto.prevalece == "R-VEN-02"
        assert conflicto.conservado == Hecho("t", "nivel_ventilacion", "critica")


@pytest.mark.parametrize("evento", ["incendio", "derrumbe", "inundacion"])
def test_cierres_fisicos_y_propagacion_a_vecinos(evento):
    mina = cargar_mina(DATOS / "mina_prueba.json")
    tramo = "t_i2_f1"
    hechos = (Hecho(tramo, evento, True),)
    resultado = inferir(preparar_hechos(hechos, mina), reglas_del_motor(CONFIGURACION))
    assert Hecho(tramo, "transitable", False) in resultado.hechos
    alertados = {h.entidad for h in resultado.hechos if h.atributo == "propagacion"}
    assert alertados == ({"t_i3_f1", "t_i1_i2"} if evento != "inundacion" else set())
    base = estados_linea_base(hechos, resultado.hechos, CONFIGURACION)
    assert Hecho(tramo, "cerrado", True) in base
    ruta = buscar_ruta(mina, "f1", ["s1"], base, ponderar_riesgo=False)
    assert tramo not in ruta.aristas


def test_corte_electrico_distingue_el_respaldo():
    hechos = (
        Hecho("sin", "corte_electrico", True), Hecho("sin", "vel_m_min", 85),
        Hecho("con", "corte_electrico", True), Hecho("con", "vel_m_min", 85),
        Hecho("con", "ventilacion_respaldo", True),
    )
    resultado = inferir(preparar_hechos(hechos, None), reglas_del_motor(CONFIGURACION))
    assert Hecho("sin", "nivel_ventilacion", "critica") in resultado.hechos
    assert Hecho("sin", "multiplicador", 3) in resultado.hechos
    assert Hecho("con", "nivel_ventilacion", "conforme") in resultado.hechos
    assert Hecho("con", "multiplicador", 3) not in resultado.hechos
    conflictos = [(c.regla, c.prevalece) for c in resultado.conflictos]
    assert ("R-VEN-03", "R-VEN-04") in conflictos


def test_el_incendio_conserva_el_origen_del_peligro_que_confirma_el_gas():
    hechos = (Hecho("t", "incendio", True), Hecho("t", "co_ppm", 101))
    resultado = inferir(hechos, reglas_del_motor(CONFIGURACION))
    reglas_de_riesgo = [
        paso.regla for paso in resultado.traza if paso.conclusion.atributo == "nivel_riesgo"
    ]
    assert reglas_de_riesgo == ["R-FUE-01"]
    assert Hecho("t", "transitable", False) in resultado.hechos
