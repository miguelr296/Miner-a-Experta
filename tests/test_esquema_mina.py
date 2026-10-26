"""Contrato estructural S1-08; las relaciones del grafo quedan para S1-11."""

from copy import deepcopy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator


ESQUEMA = json.loads((Path(__file__).resolve().parents[1]
                      / "data/esquemas/mina.schema.json").read_text(encoding="utf-8"))
VALIDADOR = Draft202012Validator(ESQUEMA)


@pytest.fixture
def mina():
    return {
        "version": 1, "nombre": "Ejemplo de contrato",
        "nodos": [
            {"id": "n1", "x": 0, "y": 0, "nivel": 0, "tipo": "salida"},
            {"id": "n2", "x": 100, "y": 0, "nivel": 0, "tipo": "refugio"},
            {"id": "n3", "x": 200, "y": 0, "nivel": -20, "tipo": "frente"},
        ],
        "aristas": [
            {"id": "t1", "origen": "n1", "destino": "n2", "longitud_m": 100},
            {"id": "t2", "origen": "n2", "destino": "n3", "longitud_m": 110},
        ],
    }


def test_esquema_bien_formado():
    Draft202012Validator.check_schema(ESQUEMA)


def test_muestra_estructural_valida(mina):
    VALIDADOR.validate(mina)


@pytest.mark.parametrize("campo", ["version", "nombre", "nodos", "aristas"])
def test_campos_raiz_obligatorios(mina, campo):
    del mina[campo]
    assert not VALIDADOR.is_valid(mina)


@pytest.mark.parametrize("campo, valor", [
    ("version", 2), ("version", True), ("nombre", "  "),
    ("nodos", []), ("aristas", []),
])
def test_valores_raiz_invalidos(mina, campo, valor):
    mina[campo] = valor
    assert not VALIDADOR.is_valid(mina)


@pytest.mark.parametrize("campo", ["id", "x", "y", "nivel", "tipo"])
def test_campos_nodo_obligatorios(mina, campo):
    del mina["nodos"][0][campo]
    assert not VALIDADOR.is_valid(mina)


@pytest.mark.parametrize("campo, valor", [
    ("id", ""), ("id", "nodo con espacio"), ("x", "100"),
    ("y", True), ("nivel", None), ("tipo", "intersección"),
])
def test_nodo_invalido(mina, campo, valor):
    mina["nodos"][0][campo] = valor
    assert not VALIDADOR.is_valid(mina)


@pytest.mark.parametrize("campo", ["id", "origen", "destino", "longitud_m"])
def test_campos_arista_obligatorios(mina, campo):
    del mina["aristas"][0][campo]
    assert not VALIDADOR.is_valid(mina)


@pytest.mark.parametrize("longitud", [0, -1, "100", True])
def test_longitud_invalida(mina, longitud):
    mina["aristas"][0]["longitud_m"] = longitud
    assert not VALIDADOR.is_valid(mina)


@pytest.mark.parametrize("ubicacion", ["raiz", "nodo", "arista"])
def test_campos_desconocidos(mina, ubicacion):
    objeto = {"raiz": mina, "nodo": mina["nodos"][0],
              "arista": mina["aristas"][0]}[ubicacion]
    objeto["campo_desconocido"] = 1
    assert not VALIDADOR.is_valid(mina)


def test_tipos_de_nodo_y_coordenadas_decimales(mina):
    for tipo in ("interseccion", "salida", "refugio", "frente"):
        muestra = deepcopy(mina)
        muestra["nodos"][0].update(tipo=tipo, x=-2.5, y=1.25, nivel=-20.5)
        VALIDADOR.validate(muestra)
