"""Fronteras, fuentes configurables y efectos de cada regla R08–R23."""

import json
from pathlib import Path
import subprocess
import sys

import pytest

from mina_experta.ambiente import cargar_ambiente, reglas_ambiente
from mina_experta.cargador import cargar_mina
from mina_experta.conocimiento import reglas_co, reglas_costos, reglas_eventos
from mina_experta.escenarios import validar_lecturas
from mina_experta.linea_base import costos_linea_base
from mina_experta.motor import Motor
from mina_experta.planificador import costos_desde_hechos


RAIZ = Path(__file__).resolve().parents[1]
CONFIG = RAIZ / "data/configuracion"


@pytest.fixture
def ambiente():
    return cargar_ambiente(CONFIG / "ambiente.json")


@pytest.fixture
def mina():
    return cargar_mina(RAIZ / "data/mina_prueba.json")


@pytest.mark.parametrize("gas, ids, valores", [
    ("no2_ppm", ["R08", "R09", "R10"], [3, 4, 5, 6, 10, 11]),
    ("co2_ppm", ["R11", "R12", "R13"], [5000, 5001, 30000, 30001, 60000, 60001]),
    ("h2s_ppm", ["R14", "R15", "R16"], [10, 11, 15, 16, 30, 31]),
    ("o2_porcentaje", ["R17", "R18", "R19"], [19.5, 19, 18, 17, 16, 15.9]),
])
def test_cadenas_y_fronteras_gases(ambiente, mina, gas, ids, valores):
    motor = Motor(reglas_ambiente(ambiente))
    for valor, cantidad in zip(valores, [0, 1, 1, 2, 2, 3]):
        hechos = validar_lecturas(mina, [("tunel_3_4", gas, valor)])
        resultado = motor.ejecutar(hechos)
        assert [p.regla_id for p in resultado.traza] == ids[:cantidad]
        costo = costos_desde_hechos(mina, resultado)["tunel_3_4"]
        assert costo == [100, 200, 300, None][cantidad]


@pytest.mark.parametrize("valor, ids", [(22.5, []), (22.51, ["R20"]), (100, ["R20"])])
def test_oxigeno_por_exceso_solo_penaliza(ambiente, valor, ids):
    salida = Motor(reglas_ambiente(ambiente)).ejecutar([("t1", "o2_porcentaje", valor)])
    assert [p.regla_id for p in salida.traza] == ids
    assert ("t1", "cerrado", True) not in salida.hechos


@pytest.mark.parametrize("aire, anfo, ids, base_cierra", [
    (20, False, [], False), (19.9, False, ["R21"], True),
    (22, False, [], False), (22, True, ["R23"], True),
    (25, True, [], False), (20, True, ["R23"], True),
    (19.9, True, ["R21", "R23"], True),
    (250, True, [], False), (250.1, True, ["R22"], True),
])
def test_ventilacion_fronteras_anfo_y_filtro(ambiente, mina, aire, anfo, ids, base_cierra):
    hechos = validar_lecturas(mina, [("tunel_2_3", "aire_m_min", aire),
                                    ("tunel_2_3", "uso_anfo", anfo)])
    salida = Motor(reglas_ambiente(ambiente)).ejecutar(hechos)
    assert [p.regla_id for p in salida.traza] == ids
    assert costos_desde_hechos(mina, salida)["tunel_2_3"] == (300 if ids else 100)
    assert (costos_linea_base(mina, hechos, 25, ambiente)["tunel_2_3"] is None) is base_cierra


@pytest.mark.parametrize("gas, normal, fuera", [
    ("no2_ppm", 3, 3.01), ("co2_ppm", 5000, 5001),
    ("h2s_ppm", 10, 10.01), ("o2_porcentaje", 19.5, 19.49),
    ("o2_porcentaje", 22.5, 22.51),
])
def test_linea_base_mismos_sensores(ambiente, mina, gas, normal, fuera):
    assert costos_linea_base(mina, [("tunel_3_4", gas, normal)], 25, ambiente)["tunel_3_4"] == 100
    assert costos_linea_base(mina, [("tunel_3_4", gas, fuera)], 25, ambiente)["tunel_3_4"] is None
    with pytest.raises(ValueError, match="ambiente"):
        costos_linea_base(mina, [("tunel_3_4", gas, fuera)], 25)


@pytest.mark.parametrize("atributo, valor", [("no2_ppm", -1), ("co2_ppm", True),
    ("h2s_ppm", float("nan")), ("o2_porcentaje", 101),
    ("aire_m_min", -1), ("uso_anfo", 1)])
def test_lecturas_invalidas(mina, atributo, valor):
    with pytest.raises(ValueError):
        validar_lecturas(mina, [("tunel_2_3", atributo, valor)])


def test_contexto_anfo_obligatorio_y_sin_cruces_entre_tuneles(mina):
    with pytest.raises(ValueError, match="uso_anfo"):
        validar_lecturas(mina, [("tunel_2_3", "aire_m_min", 22)])
    with pytest.raises(ValueError, match="uso_anfo"):
        validar_lecturas(mina, [("tunel_2_3", "aire_m_min", 22),
                               ("tunel_3_4", "uso_anfo", True)])


@pytest.mark.parametrize("seccion, campo, valor", [
    ("no2_ppm", "alerta", 20), ("o2_porcentaje", "riesgo_alto", 22),
    ("o2_porcentaje", "maximo", 101), ("ventilacion", "minimo_anfo", 10),
    ("ventilacion", "maximo", float("inf")), ("factores", "alerta", 0.5),
    ("factores", "riesgo_alto", 1), ("h2s_ppm", "alerta", True),
])
def test_configuracion_invalida(tmp_path, ambiente, seccion, campo, valor):
    objeto = ambiente[seccion] if seccion in ("ventilacion", "factores") else ambiente["gases"][seccion]
    objeto[campo] = valor
    ruta = tmp_path / "ambiente.json"
    ruta.write_text(json.dumps(ambiente), encoding="utf-8")
    with pytest.raises(ValueError):
        cargar_ambiente(ruta)


def test_configuracion_cambia_comportamiento_y_total_reglas(tmp_path, ambiente):
    ruta = tmp_path / "ambiente.json"
    ambiente["gases"]["no2_ppm"] = dict(alerta=30, riesgo_alto=50, peligro_inmediato=100)
    ruta.write_text(json.dumps(ambiente), encoding="utf-8")
    assert Motor(reglas_ambiente(cargar_ambiente(ruta))).ejecutar([("t1", "no2_ppm", 11)]).traza == ()
    reglas = (*reglas_co(CONFIG / "umbrales.json"), *reglas_costos(CONFIG / "costos.json"),
              *reglas_eventos(), *reglas_ambiente(ambiente))
    assert len(reglas) == len({r.id for r in reglas}) == 23


def test_combinacion_gases_no_multiplica_factores(ambiente, mina):
    hechos = [("tunel_3_4", "no2_ppm", 6), ("tunel_3_4", "h2s_ppm", 11)]
    salida = Motor(reglas_ambiente(ambiente)).ejecutar(hechos)
    assert costos_desde_hechos(mina, salida)["tunel_3_4"] == 300


def test_escenario_anfo_ejecucion_completa(tmp_path):
    salida = subprocess.run([sys.executable, "-m", "mina_experta", "--escenario",
                            str(RAIZ / "data/escenarios/ventilacion_anfo.json")], cwd=tmp_path,
                           capture_output=True, text=True)
    assert salida.returncode == 0, salida.stderr
    assert "R23 [tunel_2_3]" in salida.stdout
    assert "distancia 470 m; costo 670" in salida.stdout
    assert "Línea base [ana] desde n5: SIN RUTA" in salida.stdout


@pytest.mark.parametrize("opcion, valor, esperado", [("--no2", 11, "R10"),
    ("--co2", 60001, "R13"), ("--h2s", 31, "R16"), ("--o2", 15, "R19")])
def test_sensores_en_consola(opcion, valor, esperado):
    salida = subprocess.run([sys.executable, "-m", "mina_experta", "--desde", "n5",
                            opcion, f"tunel_3_4={valor}", "--comparar"], cwd=RAIZ,
                           capture_output=True, text=True)
    assert salida.returncode == 0, salida.stderr
    assert f"{esperado} [tunel_3_4]" in salida.stdout
    assert "distancia 710 m; costo 710" in salida.stdout


def test_escenario_anterior_y_nuevo_sensor_sin_ambiente(tmp_path):
    fuente = RAIZ / "data/escenarios/co_moderado.json"
    datos = json.loads(fuente.read_text(encoding="utf-8"))
    del datos["ambiente"]
    for clave in ("mina", "umbrales", "costos"):
        datos[clave] = str((fuente.parent / datos[clave]).resolve())
    ruta = tmp_path / "anterior.json"
    ruta.write_text(json.dumps(datos), encoding="utf-8")
    comando = [sys.executable, "-m", "mina_experta", "--escenario", str(ruta)]
    salida = subprocess.run(comando, cwd=tmp_path, capture_output=True, text=True)
    assert salida.returncode == 0, salida.stderr
    datos["hechos"][0]["atributo"] = "no2_ppm"
    ruta.write_text(json.dumps(datos), encoding="utf-8")
    salida = subprocess.run(comando, cwd=tmp_path, capture_output=True, text=True)
    assert salida.returncode == 2
    assert "archivo ambiente" in salida.stderr


def test_aire_en_consola_requiere_contexto_y_rechaza_contradiccion():
    comando = [sys.executable, "-m", "mina_experta", "--aire", "tunel_2_3=22"]
    sin_contexto = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    assert sin_contexto.returncode == 2
    assert "uso_anfo" in sin_contexto.stderr
    valido = subprocess.run(comando + ["--sin-anfo", "tunel_2_3"], cwd=RAIZ,
                            capture_output=True, text=True)
    assert valido.returncode == 0, valido.stderr
    assert "Disparos: 0" in valido.stdout
    contradictorio = subprocess.run(comando + ["--sin-anfo", "tunel_2_3", "--anfo", "tunel_2_3"],
                                    cwd=RAIZ, capture_output=True, text=True)
    assert contradictorio.returncode == 2
    assert "repetida" in contradictorio.stderr
