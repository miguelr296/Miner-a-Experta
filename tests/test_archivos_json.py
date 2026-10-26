"""Pruebas con archivos reales y temporales para S1-05."""

import json

import pytest

from ejercicios.archivos_json import leer_json, escribir_json


def test_ida_y_vuelta_con_tipos_json_y_acentos(tmp_path):
    datos = {"nombre": "Intersección", "valores": [1, 2.5, True, False, None],
             "vacio": {}, "lista": []}
    ruta = tmp_path / "datos.json"
    escribir_json(ruta, datos)
    assert leer_json(ruta) == datos
    assert "Intersección" in ruta.read_text(encoding="utf-8")


def test_lectura_de_archivo_externo(tmp_path):
    ruta = tmp_path / "externo.json"
    ruta.write_text('{"nodos": [{"id": "n1"}]}', encoding="utf-8")
    assert leer_json(ruta) == {"nodos": [{"id": "n1"}]}


def test_archivo_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError):
        leer_json(tmp_path / "ausente.json")


def test_json_invalido(tmp_path):
    ruta = tmp_path / "roto.json"
    ruta.write_text('{"nodos":', encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        leer_json(ruta)


def test_no_sobrescribe_datos_existentes(tmp_path):
    ruta = tmp_path / "original.json"
    ruta.write_text("contenido original", encoding="utf-8")
    with pytest.raises(FileExistsError):
        escribir_json(ruta, {"nuevo": True})
    assert ruta.read_text(encoding="utf-8") == "contenido original"


@pytest.mark.parametrize("datos, error", [({"objeto": object()}, TypeError),
                                         ({"valor": float("nan")}, ValueError)])
def test_datos_no_serializables_no_dejan_archivo(tmp_path, datos, error):
    ruta = tmp_path / "invalido.json"
    with pytest.raises(error):
        escribir_json(ruta, datos)
    assert not ruta.exists()
