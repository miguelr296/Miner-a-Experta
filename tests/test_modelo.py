"""Coherencia del modelo y uso público, sin depender del cargador JSON."""

from dataclasses import FrozenInstanceError
from pathlib import Path
import subprocess
import sys

import pytest

from mina_experta import Arista, Mina, Nodo


@pytest.fixture
def nodos():
    return [Nodo("n1", 0, 0, -50, "frente"),
            Nodo("n2", 100, 0, -50, "refugio"),
            Nodo("n3", 200, 0, 0, "salida")]


def test_vecinos_en_ambos_sentidos_y_nodo_aislado(nodos):
    tunel = Arista("t1", "n1", "n2", 100)
    mina = Mina("Prueba", nodos, [tunel])
    assert mina.nombre == "Prueba"
    assert mina.nodos["n1"].coordenadas == (0, 0, -50)
    assert mina.aristas["t1"] == tunel
    assert mina.vecinos("n1") == ((nodos[1], tunel),)
    assert mina.vecinos("n2") == ((nodos[0], tunel),)
    assert mina.vecinos("n3") == ()
    with pytest.raises(KeyError, match="Nodo inexistente"):
        mina.vecinos("ausente")


def test_vecinos_conservan_orden_de_aristas(nodos):
    primera = Arista("t1", "n1", "n2", 100)
    segunda = Arista("t2", "n2", "n3", 120)
    mina = Mina("Prueba", nodos, [primera, segunda])
    assert mina.vecinos("n2") == ((nodos[0], primera), (nodos[2], segunda))


def test_no_se_pueden_modificar_datos_publicos(nodos):
    tunel = Arista("t1", "n1", "n2", 100)
    aristas = [tunel]
    mina = Mina("Prueba", nodos, aristas)
    nodos.clear()
    aristas.clear()
    assert len(mina.nodos) == 3
    assert len(mina.aristas) == 1
    with pytest.raises(TypeError):
        mina.nodos["n4"] = mina.nodos["n1"]
    with pytest.raises(TypeError):
        mina.aristas["t2"] = tunel
    with pytest.raises(FrozenInstanceError):
        mina.nodos["n1"].x = 10
    with pytest.raises(FrozenInstanceError):
        tunel.longitud_m = 1


@pytest.mark.parametrize("valor", [True, "1", None, float("inf"), float("nan"), 10**400])
@pytest.mark.parametrize("campo", ["x", "y", "nivel"])
def test_coordenadas_invalidas(campo, valor):
    datos = dict(id="n1", x=0, y=0, nivel=-50, tipo="frente")
    datos[campo] = valor
    with pytest.raises(ValueError, match="número finito"):
        Nodo(**datos)


@pytest.mark.parametrize("identificador", ["", "N1", "n 1", "n1\n", 1])
def test_identificador_invalido(identificador):
    with pytest.raises(ValueError, match="Identificador"):
        Nodo(identificador, 0, 0, 0, "salida")


def test_tipo_invalido():
    with pytest.raises(ValueError, match="Tipo de nodo"):
        Nodo("n1", 0, 0, 0, "otro")


@pytest.mark.parametrize("longitud", [0, -1, True, "100", float("inf"), float("nan")])
def test_longitud_invalida(longitud):
    with pytest.raises(ValueError):
        Arista("t1", "n1", "n2", longitud)


def test_tunel_hacia_si_mismo():
    with pytest.raises(ValueError, match="distintos"):
        Arista("t1", "n1", "n1", 1)


@pytest.mark.parametrize("nombre", ["", "  ", None])
def test_nombre_invalido(nodos, nombre):
    with pytest.raises(ValueError, match="nombre"):
        Mina(nombre, nodos, [])


def test_nodo_duplicado(nodos):
    with pytest.raises(ValueError, match="Nodo duplicado"):
        Mina("Prueba", nodos + [nodos[0]], [])


@pytest.mark.parametrize("aristas, mensaje", [
    ([Arista("t1", "n1", "n4", 100)], "Extremo inexistente"),
    ([Arista("t1", "n1", "n2", 100), Arista("t1", "n2", "n3", 120)], "Arista duplicada"),
    ([Arista("t1", "n1", "n2", 100), Arista("t2", "n2", "n1", 100)], "Par de nodos repetido"),
    ([Arista("t1", "n1", "n2", 99)], "distancia recta"),
    ([Arista("t1", "n2", "n3", 100)], "distancia recta"),
])
def test_conexiones_invalidas(nodos, aristas, mensaje):
    with pytest.raises(ValueError, match=mensaje):
        Mina("Prueba", nodos, aristas)


def test_demostracion_ejecutable():
    resultado = subprocess.run(
        [sys.executable, "-m", "ejercicios.mina_en_memoria"],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True, text=True, check=True,
    )
    assert resultado.stdout.splitlines() == [
        "Ejemplo en memoria", "Vecinos de n1:", "  n2 por t1: 100 m",
        "Vecinos de n2:", "  n1 por t1: 100 m", "  n3 por t2: 120 m",
        "Vecinos de n3:", "  n2 por t2: 120 m",
    ]
