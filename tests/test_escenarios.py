"""Contrato de escenarios y ejecución reproducible desde cualquier directorio."""

import json
from pathlib import Path
import subprocess
import sys

import pytest

from mina_experta.escenarios import cargar_escenario


RAIZ = Path(__file__).resolve().parents[1]
ESCENARIOS = RAIZ / "data/escenarios"


@pytest.fixture
def datos():
    ruta = ESCENARIOS / "co_moderado.json"
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    for clave in ("mina", "umbrales", "costos", "ambiente"):
        datos[clave] = str((ruta.parent / datos[clave]).resolve())
    return datos


def guardar(tmp_path, datos):
    ruta = tmp_path / "escenario.json"
    ruta.write_text(json.dumps(datos), encoding="utf-8")
    return ruta


def test_archivo_real():
    escenario = cargar_escenario(ESCENARIOS / "co_moderado.json")
    assert [(m.id, m.nodo) for m in escenario.mineros] == [("ana", "n5"), ("luis", "n7")]
    assert escenario.hechos == (("tunel_2_3", "co_ppm", 30),)
    assert escenario.destinos == ("n1",)


@pytest.mark.parametrize("campo, valor", [("version", True), ("version", 2),
    ("nombre", ""), ("mina", None), ("costos", ""), ("mineros", []),
    ("mineros", [1]), ("destinos", []), ("destinos", ["no_existe"]),
    ("destinos", ["n1", "n1"]), ("hechos", None), ("hechos", [1])])
def test_datos_incorrectos(tmp_path, datos, campo, valor):
    datos[campo] = valor
    with pytest.raises(ValueError):
        cargar_escenario(guardar(tmp_path, datos))


@pytest.mark.parametrize("campo, valor", [("id", ""), ("nodo", "no_existe")])
def test_minero_incorrecto(tmp_path, datos, campo, valor):
    datos["mineros"][0][campo] = valor
    with pytest.raises(ValueError):
        cargar_escenario(guardar(tmp_path, datos))


def test_minero_duplicado_pero_ubicacion_compartida_valida(tmp_path, datos):
    datos["mineros"][1]["nodo"] = "n5"
    assert len(cargar_escenario(guardar(tmp_path, datos)).mineros) == 2
    datos["mineros"][1]["id"] = "ana"
    with pytest.raises(ValueError, match="Minero duplicado"):
        cargar_escenario(guardar(tmp_path, datos))


@pytest.mark.parametrize("atributo, valor", [("cerrado", True), ("multiplicador", 3),
    ("co_ppm", True), ("co_ppm", -1), ("co_ppm", float("nan")),
    ("co_ppm", float("inf")), ("incendio_reportado", 1)])
def test_no_admite_inferencias_ni_mediciones_invalidas(tmp_path, datos, atributo, valor):
    datos["hechos"][0].update(atributo=atributo, valor=valor)
    with pytest.raises(ValueError):
        cargar_escenario(guardar(tmp_path, datos))


def test_lectura_repetida_y_tunel_inexistente(tmp_path, datos):
    datos["hechos"].append(datos["hechos"][0].copy())
    with pytest.raises(ValueError, match="repetida"):
        cargar_escenario(guardar(tmp_path, datos))
    datos["hechos"].pop()
    datos["hechos"][0]["entidad"] = "no_existe"
    with pytest.raises(ValueError, match="Túnel desconocido"):
        cargar_escenario(guardar(tmp_path, datos))


def test_claves_repetidas_y_archivo_ausente(tmp_path):
    ruta = tmp_path / "repetido.json"
    ruta.write_text('{"version": 1, "version": 2}', encoding="utf-8")
    with pytest.raises(ValueError, match="repetida"):
        cargar_escenario(ruta)
    with pytest.raises(ValueError, match="No se pudo cargar el escenario"):
        cargar_escenario(tmp_path / "ausente.json")


@pytest.mark.parametrize("archivo, esperado", [
    ("co_moderado.json", ["Ruta [ana] desde n5: n5 -> n4 -> n3 -> n2 -> n1; distancia 470 m; costo 570",
                           "Línea base [ana] desde n5: SIN RUTA", "Disparos: 2"]),
    ("incendio_alternativa.json", ["Ruta [ana] desde n5: n5 -> n4 -> n8 -> n6 -> n3 -> n2 -> n1; distancia 710 m; costo 710",
                                   "Línea base [ana] desde n5: n5 -> n4 -> n8 -> n6 -> n3 -> n2 -> n1", "Disparos: 1"]),
    ("derrumbe_aislamiento.json", ["Ruta [ana] desde n5: SIN RUTA", "Línea base [ana] desde n5: SIN RUTA",
                                  "Ruta [luis] desde n7: n7 -> n8 -> n6 -> n3 -> n2 -> n1; distancia 540 m; costo 540"]),
])
def test_tres_escenarios_desde_fuera_del_checkout(tmp_path, archivo, esperado):
    salida = subprocess.run([sys.executable, "-m", "mina_experta", "--escenario",
                            str(ESCENARIOS / archivo)], cwd=tmp_path,
                           capture_output=True, text=True)
    assert salida.returncode == 0, salida.stderr
    for texto in esperado:
        assert texto in salida.stdout
    assert "Ruta [luis] desde n7:" in salida.stdout
    assert "Línea base [luis] desde n7:" in salida.stdout


def test_mezcla_de_entradas_rechazada():
    salida = subprocess.run([sys.executable, "-m", "mina_experta", "--escenario",
                            str(ESCENARIOS / "co_moderado.json"), "--co", "tunel_1_2=100"],
                           cwd=RAIZ, capture_output=True, text=True)
    assert salida.returncode == 2
    assert "no se mezcla" in salida.stderr
