"""Verifica las clases y la ejecución entre módulos de S1-02."""

from dataclasses import FrozenInstanceError
from pathlib import Path
import subprocess
import sys

import pytest

from ejercicios.modelo_aprendizaje import Minero, PuntoControl


def test_inicializacion_y_descripcion():
    minero = Minero("Ana", PuntoControl("n1", "frente"))
    assert minero.nombre == "Ana"
    assert minero.ubicacion == PuntoControl("n1", "frente")
    assert minero.describir() == "Ana: n1 (frente)"


def test_cambiar_ubicacion_no_modifica_otro_minero():
    frente = PuntoControl("n1", "frente")
    ana = Minero("Ana", frente)
    luis = Minero("Luis", frente)
    refugio = PuntoControl("n3", "refugio")

    ana.cambiar_ubicacion(refugio)

    assert ana.ubicacion == refugio
    assert ana.describir() == "Ana: n3 (refugio)"
    assert luis.ubicacion == frente
    assert luis.describir() == "Luis: n1 (frente)"


def test_dataclass_compara_sus_datos():
    assert PuntoControl("n1", "frente") == PuntoControl("n1", "frente")
    assert PuntoControl("n1", "frente") != PuntoControl("n3", "refugio")


def test_punto_compartido_no_se_puede_modificar():
    punto = PuntoControl("n1", "frente")
    with pytest.raises(FrozenInstanceError):
        punto.tipo = "refugio"
    assert punto.tipo == "frente"


def test_demostracion_desde_otro_modulo():
    raiz = Path(__file__).resolve().parents[1]
    resultado = subprocess.run(
        [sys.executable, "-m", "ejercicios.clases"],
        cwd=raiz, capture_output=True, text=True, check=True,
    )
    assert resultado.stdout.splitlines() == [
        "Estado inicial:",
        "Ana: n1 (frente)",
        "Luis: n1 (frente)",
        "Tras actualizar solo a Ana:",
        "Ana: n3 (refugio)",
        "Luis: n1 (frente)",
    ]


def test_importar_no_ejecuta_la_demostracion():
    resultado = subprocess.run(
        [sys.executable, "-c", "import ejercicios.clases"],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True, text=True, check=True,
    )
    assert resultado.stdout == ""
    assert resultado.stderr == ""
