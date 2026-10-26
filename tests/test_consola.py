"""Ejecuta la consola real, incluida la carga de datos y reglas."""

from pathlib import Path
import subprocess
import sys

import pytest


RAIZ = Path(__file__).resolve().parents[1]


def ejecutar(*argumentos):
    return subprocess.run([sys.executable, "-m", "mina_experta", *argumentos],
                          cwd=RAIZ, capture_output=True, text=True)


def test_demostracion_completa():
    resultado = ejecutar("--co", "tunel_1_2=120", "--co", "tunel_2_3=20")
    assert resultado.returncode == 0, resultado.stderr
    assert "8 nodos, 8 túneles" in resultado.stdout
    assert "Disparos: 5" in resultado.stdout
    assert "('tunel_1_2', 'cerrado', True)" in resultado.stdout
    assert "[tunel_2_3]" not in resultado.stdout
    assert "Sin origen --desde" in resultado.stdout


@pytest.mark.parametrize("lectura", ["no_existe=120", "tunel_1_2=NaN",
    "tunel_1_2=-1", "tunel_1_2=abc", "sin_igual"])
def test_errores_lectura(lectura):
    resultado = ejecutar("--co", lectura)
    assert resultado.returncode == 2
    assert "Error:" in resultado.stderr
    assert "Traceback" not in resultado.stderr


def test_lectura_duplicada():
    resultado = ejecutar("--co", "tunel_1_2=120", "--co", "tunel_1_2=20")
    assert resultado.returncode == 2
    assert "repetida" in resultado.stderr


def test_archivo_ausente():
    resultado = ejecutar("--mina", "no_existe.json")
    assert resultado.returncode == 2
    assert "No se pudo cargar" in resultado.stderr


def test_eventos_en_consola():
    resultado = ejecutar("--incendio", "tunel_3_4", "--derrumbe", "tunel_4_5")
    assert resultado.returncode == 0, resultado.stderr
    assert "R04 [tunel_3_4]" in resultado.stdout
    assert "R05 [tunel_4_5]" in resultado.stdout
    assert "Disparos: 2" in resultado.stdout


def test_evento_en_tunel_desconocido():
    resultado = ejecutar("--derrumbe", "tunel_ausente")
    assert resultado.returncode == 2
    assert "Túnel desconocido" in resultado.stderr


def test_ruta_y_alternativa_desde_consola():
    limpia = ejecutar("--desde", "n5")
    assert limpia.returncode == 0, limpia.stderr
    assert "n5 -> n4 -> n3 -> n2 -> n1; distancia 470 m; costo 470" in limpia.stdout
    cerrada = ejecutar("--desde", "n5", "--co", "tunel_3_4=120")
    assert cerrada.returncode == 0, cerrada.stderr
    assert "n5 -> n4 -> n8 -> n6 -> n3 -> n2 -> n1; distancia 710 m; costo 710" in cerrada.stdout


def test_sin_ruta_y_destino_refugio_explicito():
    aislada = ejecutar("--desde", "n5", "--derrumbe", "tunel_4_5")
    assert aislada.returncode == 0, aislada.stderr
    assert "Ruta desde n5: SIN RUTA" in aislada.stdout
    refugio = ejecutar("--desde", "n5", "--hasta", "n4")
    assert refugio.returncode == 0, refugio.stderr
    assert "n5 -> n4; distancia 150 m; costo 150" in refugio.stdout


def test_varios_origenes():
    salida = ejecutar("--desde", "n5", "--desde", "n7")
    assert salida.returncode == 0, salida.stderr
    assert "Ruta desde n5:" in salida.stdout and "Ruta desde n7:" in salida.stdout


@pytest.mark.parametrize("argumentos", [("--desde", "inexistente"),
    ("--desde", "n5", "--hasta", "inexistente"), ("--hasta", "n1")])
def test_destinos_invalidos(argumentos):
    salida = ejecutar(*argumentos)
    assert salida.returncode == 2
    assert "Error:" in salida.stderr


def test_comparacion_manual():
    salida = ejecutar("--desde", "n5", "--co", "tunel_2_3=30", "--comparar")
    assert salida.returncode == 0, salida.stderr
    assert "costo 570" in salida.stdout
    assert "Línea base desde n5: SIN RUTA" in salida.stdout


@pytest.mark.parametrize("opcion", ["--mina", "--umbrales", "--costos", "--ambiente",
                                    "--relaciones", "--escenario"])
@pytest.mark.parametrize("ruta", ["", "   "])
def test_ruta_vacia_no_activa_predeterminados(opcion, ruta):
    salida = ejecutar(opcion, ruta)
    assert salida.returncode == 2
    assert "La ruta no puede estar vacía" in salida.stderr
    assert "Mina:" not in salida.stdout
