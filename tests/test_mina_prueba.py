"""Comprueba el entregable S1-09 sin sustituir el futuro cargador genérico."""

import json
import math
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator


RAIZ = Path(__file__).resolve().parents[1]


@pytest.fixture
def mina():
    return json.loads((RAIZ / "data/mina_prueba.json").read_text(encoding="utf-8"))


def test_archivo_cumple_esquema(mina):
    esquema = json.loads((RAIZ / "data/esquemas/mina.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(esquema).validate(mina)


def test_tamano_y_tipos_del_entregable(mina):
    assert 6 <= len(mina["nodos"]) <= 8
    tipos = {nodo["tipo"] for nodo in mina["nodos"]}
    assert {"frente", "refugio", "salida", "interseccion"} <= tipos
    assert {-50, -100} <= {nodo["nivel"] for nodo in mina["nodos"]}


def test_identificadores_referencias_y_pares(mina):
    nodos = {nodo["id"] for nodo in mina["nodos"]}
    assert len(nodos) == len(mina["nodos"])
    assert len({arista["id"] for arista in mina["aristas"]}) == len(mina["aristas"])
    pares = set()
    for arista in mina["aristas"]:
        assert arista["origen"] in nodos
        assert arista["destino"] in nodos
        assert arista["origen"] != arista["destino"]
        par = frozenset((arista["origen"], arista["destino"]))
        assert par not in pares
        pares.add(par)


def test_longitudes_respetan_geometria(mina):
    puntos = {n["id"]: (n["x"], n["y"], n["nivel"]) for n in mina["nodos"]}
    for punto in puntos.values():
        assert all(math.isfinite(coordenada) for coordenada in punto)
    for arista in mina["aristas"]:
        assert math.isfinite(arista["longitud_m"])
        assert arista["longitud_m"] >= math.dist(
            puntos[arista["origen"]], puntos[arista["destino"]])


def test_mina_base_conectada(mina):
    vecinos = {n["id"]: set() for n in mina["nodos"]}
    for arista in mina["aristas"]:
        vecinos[arista["origen"]].add(arista["destino"])
        vecinos[arista["destino"]].add(arista["origen"])
    pendientes = [mina["nodos"][0]["id"]]
    visitados = set()
    while pendientes:
        nodo = pendientes.pop()
        if nodo not in visitados:
            visitados.add(nodo)
            pendientes.extend(vecinos[nodo] - visitados)
    assert visitados == set(vecinos)


RECORRIDOS = [("n5", "n4"), ("n7", "n8", "n4")]


def test_recorridos_documentados_cubren_todos_los_frentes(mina):
    assert {ruta[0] for ruta in RECORRIDOS} == {
        n["id"] for n in mina["nodos"] if n["tipo"] == "frente"}


@pytest.mark.parametrize("ruta, esperado", zip(RECORRIDOS, [150, 220]))
def test_recorrido_real_a_refugio_hasta_500_m(mina, ruta, esperado):
    tipos = {n["id"]: n["tipo"] for n in mina["nodos"]}
    longitudes = {frozenset((a["origen"], a["destino"])): a["longitud_m"]
                  for a in mina["aristas"]}
    assert tipos[ruta[0]] == "frente"
    assert tipos[ruta[-1]] == "refugio"
    total = sum(longitudes[frozenset((origen, destino))]
                for origen, destino in zip(ruta, ruta[1:]))
    assert total == esperado
    assert total <= 500
