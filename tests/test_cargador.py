"""Prueba archivos reales, errores de contrato y el límite D10 por recorrido."""

import json
from pathlib import Path

import pytest

from mina_experta.cargador import ErrorCarga, cargar_mina


@pytest.fixture
def datos():
    return json.loads((Path(__file__).resolve().parents[1]
                       / "data/mina_prueba.json").read_text(encoding="utf-8"))


def guardar(tmp_path, datos):
    ruta = tmp_path / "mina.json"
    ruta.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")
    return ruta


def test_cargar_mina_publicada():
    mina = cargar_mina(Path(__file__).resolve().parents[1] / "data/mina_prueba.json")
    assert len(mina.nodos) == 8
    assert len(mina.aristas) == 8
    assert {n.id for n, _ in mina.vecinos("n4")} == {"n3", "n5", "n8"}


@pytest.mark.parametrize("contenido", ['{', '[]', '{}', '{"version": 1, "version": 1}',
                                         '{"x": NaN}', '{"x": Infinity}'])
def test_json_incorrecto(tmp_path, contenido):
    ruta = tmp_path / "roto.json"
    ruta.write_text(contenido, encoding="utf-8")
    with pytest.raises(ErrorCarga):
        cargar_mina(ruta)


def test_archivo_ausente_y_codificacion(tmp_path):
    with pytest.raises(ErrorCarga, match="No se pudo cargar"):
        cargar_mina(tmp_path / "ausente.json")
    ruta = tmp_path / "invalido.json"
    ruta.write_bytes(b'\xff')
    with pytest.raises(ErrorCarga):
        cargar_mina(ruta)


@pytest.mark.parametrize("campo, valor", [("version", True), ("version", 2),
    ("nombre", ""), ("nodos", []), ("aristas", []), ("nodos", [1])])
def test_campos_invalidos(tmp_path, datos, campo, valor):
    datos[campo] = valor
    with pytest.raises(ErrorCarga):
        cargar_mina(guardar(tmp_path, datos))


@pytest.mark.parametrize("campo, valor", [("x", float("nan")), ("x", float("inf")),
    ("x", 1e309), ("x", True), ("tipo", "otro"), ("id", "n1\n")])
def test_nodo_invalido(tmp_path, datos, campo, valor):
    datos["nodos"][0][campo] = valor
    with pytest.raises(ErrorCarga):
        cargar_mina(guardar(tmp_path, datos))


@pytest.mark.parametrize("ubicacion", ["mina", "nodo", "arista"])
def test_campos_extra(tmp_path, datos, ubicacion):
    objeto = {"mina": datos, "nodo": datos["nodos"][0], "arista": datos["aristas"][0]}[ubicacion]
    objeto["extra"] = 1
    with pytest.raises(ErrorCarga, match="Campos incorrectos"):
        cargar_mina(guardar(tmp_path, datos))


def test_nodo_duplicado(tmp_path, datos):
    datos["nodos"].append(datos["nodos"][0].copy())
    with pytest.raises(ErrorCarga, match="Nodo duplicado"):
        cargar_mina(guardar(tmp_path, datos))


def test_mina_desconectada(tmp_path, datos):
    datos["aristas"] = [a for a in datos["aristas"] if a["id"] != "tunel_4_5"]
    with pytest.raises(ErrorCarga, match="conectada"):
        cargar_mina(guardar(tmp_path, datos))


@pytest.mark.parametrize("tipo", ["salida", "refugio", "frente"])
def test_tipos_requeridos(tmp_path, datos, tipo):
    for nodo in datos["nodos"]:
        if nodo["tipo"] == tipo:
            nodo["tipo"] = "interseccion"
    with pytest.raises(ErrorCarga, match="requiere"):
        cargar_mina(guardar(tmp_path, datos))


@pytest.mark.parametrize("longitud, valido", [(500, True), (500.01, False)])
def test_d10_limite_exacto_no_distancia_recta(tmp_path, longitud, valido):
    datos = {"version": 1, "nombre": "Límite", "nodos": [
        {"id": "n1", "x": 0, "y": 0, "nivel": 0, "tipo": "frente"},
        {"id": "n2", "x": 10, "y": 0, "nivel": 0, "tipo": "refugio"},
        {"id": "n3", "x": 20, "y": 0, "nivel": 0, "tipo": "salida"}],
        "aristas": [{"id": "t1", "origen": "n1", "destino": "n2", "longitud_m": longitud},
                    {"id": "t2", "origen": "n2", "destino": "n3", "longitud_m": 10}]}
    ruta = guardar(tmp_path, datos)
    if valido:
        assert cargar_mina(ruta).nodos["n1"].tipo == "frente"
    else:
        with pytest.raises(ErrorCarga, match="500 m"):
            cargar_mina(ruta)


def test_d10_busca_ruta_alternativa_y_otro_refugio(tmp_path, datos):
    for arista in datos["aristas"]:
        if arista["id"] == "tunel_8_4":
            arista["longitud_m"] = 1000
    # n7 -> n8 -> n6 -> n3 -> n4 suma 420 m, a pesar del túnel directo largo.
    assert cargar_mina(guardar(tmp_path, datos)).nodos["n7"].tipo == "frente"
    datos["nodos"][5]["tipo"] = "refugio"
    for arista in datos["aristas"]:
        if arista["id"] == "tunel_3_4":
            arista["longitud_m"] = 1000
    assert cargar_mina(guardar(tmp_path, datos)).nodos["n6"].tipo == "refugio"
