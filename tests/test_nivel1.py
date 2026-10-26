"""Criterios de mina ampliada y evidencia controlada del riesgo vecino."""

import json
from pathlib import Path
import subprocess
import sys

import pytest
from jsonschema import Draft202012Validator

from mina_experta.ambiente import cargar_ambiente, reglas_ambiente
from mina_experta.conocimiento import cargar_umbrales_co, reglas_co, reglas_costos, reglas_eventos
from mina_experta.escenarios import cargar_escenario
from mina_experta.linea_base import costos_linea_base
from mina_experta.motor import Condicion, Motor, Regla
from mina_experta.planificador import costos_desde_hechos, ruta_menor_costo
from mina_experta.relaciones import cargar_relaciones, hechos_relaciones, reglas_vecindad


RAIZ = Path(__file__).resolve().parents[1]
ESCENARIOS = RAIZ / "data/escenarios"
ORIGEN, VECINO = "tunel_12_14", "tunel_10_12"


@pytest.fixture
def escenario():
    return cargar_escenario(ESCENARIOS / "nivel1_riesgo_vecino.json")


def reglas_locales(escenario):
    return (*reglas_co(escenario.umbrales), *reglas_costos(escenario.costos),
            *reglas_eventos(), *reglas_ambiente(cargar_ambiente(escenario.ambiente)))


def test_mina_nivel1_estructura_y_refugios(escenario):
    datos = json.loads((RAIZ / "data/mina_nivel1.json").read_text(encoding="utf-8"))
    esquema = json.loads((RAIZ / "data/esquemas/mina.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(esquema).validate(datos)
    mina = escenario.mina
    assert len(mina.nodos) == 16 and len(mina.aristas) == 20
    assert {n.nivel for n in mina.nodos.values() if n.nivel < 0} == {-50, -100}
    assert sum(n.tipo == "salida" for n in mina.nodos.values()) == 2
    refugios = [n.id for n in mina.nodos.values() if n.tipo == "refugio"]
    assert len(refugios) == 3
    esperadas = {"n5": 150, "n7": 220, "n13": 60, "n16": 100}
    for frente, distancia in esperadas.items():
        ruta = ruta_menor_costo(mina, frente, refugios)
        assert ruta.distancia_m == distancia <= 500


def test_cadena_real_cierra_vecino_y_muestra_sus_antecedentes(escenario):
    relaciones = cargar_relaciones(escenario.relaciones, escenario.mina)
    locales = reglas_locales(escenario)
    hechos = (*escenario.hechos, *hechos_relaciones(relaciones))
    salida = Motor((*locales, *reglas_vecindad(relaciones))).ejecutar(hechos)
    assert [p.regla_id for p in salida.traza] == ["R04", f"R24_{ORIGEN}__{VECINO}", "R25"]
    cierre = salida.por_que((VECINO, "cerrado", True))
    assert cierre[0].antecedentes == ((VECINO, "expuesto_humo", True),)
    exposicion = salida.por_que((VECINO, "expuesto_humo", True))[0]
    assert exposicion.antecedentes == ((ORIGEN, "foco_incendio", True),
                                      (VECINO, "recibe_humo_de", ORIGEN))
    ruta = ruta_menor_costo(escenario.mina, "n13", escenario.destinos,
                            costos_desde_hechos(escenario.mina, salida))
    assert ruta.nodos == ("n13", "n15", "n6", "n10", "n9", "n11")
    assert ruta.distancia_m == ruta.costo == 500
    assert VECINO not in ruta.aristas and ORIGEN not in ruta.aristas

    base = costos_linea_base(escenario.mina, escenario.hechos,
                            cargar_umbrales_co(escenario.umbrales)["alerta"],
                            cargar_ambiente(escenario.ambiente), relaciones)
    assert base[ORIGEN] is None and base[VECINO] == 100
    ruta_base = ruta_menor_costo(escenario.mina, "n13", escenario.destinos, base)
    assert VECINO in ruta_base.aristas
    assert ruta_base.distancia_m == 420
    # Control: con todas las reglas locales, sin la inferencia vecina,
    # el sistema elige exactamente el mismo camino que el filtro.
    control = Motor(locales).ejecutar(hechos)
    assert ruta_menor_costo(escenario.mina, "n13", escenario.destinos,
                            costos_desde_hechos(escenario.mina, control)) == ruta_base


@pytest.mark.parametrize("invertir, incendio", [(False, False), (True, True)])
def test_no_se_infiere_humo_sin_incendio_o_en_sentido_inverso(escenario, invertir, incendio):
    relaciones = ((VECINO, ORIGEN),) if invertir else ((ORIGEN, VECINO),)
    hechos = [(ORIGEN, "incendio_reportado", incendio), *hechos_relaciones(relaciones)]
    salida = Motor((*reglas_eventos(), *reglas_vecindad(relaciones))).ejecutar(hechos)
    assert not any(h[1] == "expuesto_humo" for h in salida.hechos)


def test_sin_propagar_indefinidamente_y_dos_fuentes(escenario):
    relaciones = ((ORIGEN, VECINO), (VECINO, "tunel_2_10"))
    salida = Motor((*reglas_eventos(), *reglas_vecindad(relaciones))).ejecutar(
        [(ORIGEN, "incendio_reportado", True), *hechos_relaciones(relaciones)])
    assert (VECINO, "expuesto_humo", True) in salida.hechos
    assert ("tunel_2_10", "expuesto_humo", True) not in salida.hechos
    relaciones = ((ORIGEN, VECINO), ("tunel_12_13", VECINO))
    salida = Motor((*reglas_eventos(), *reglas_vecindad(relaciones))).ejecutar(
        [(ORIGEN, "incendio_reportado", True), ("tunel_12_13", "incendio_reportado", True),
         *hechos_relaciones(relaciones)])
    assert len(salida.por_que((VECINO, "expuesto_humo", True))) == 2
    assert len(salida.por_que((VECINO, "cerrado", True))) == 1


@pytest.mark.parametrize("relacion", [
    {"origen": ORIGEN, "destino": ORIGEN},
    {"origen": "ausente", "destino": VECINO},
    {"origen": ORIGEN, "destino": "tunel_1_2"},
    {"origen": True, "destino": VECINO},
])
def test_relaciones_invalidas(tmp_path, escenario, relacion):
    ruta = tmp_path / "relaciones.json"
    ruta.write_text(json.dumps({"version": 1, "flujo_humo": [relacion]}), encoding="utf-8")
    with pytest.raises(ValueError):
        cargar_relaciones(ruta, escenario.mina)


def test_relaciones_repetidas_y_no_inferidas_por_geometria(tmp_path, escenario):
    ruta = tmp_path / "relaciones.json"
    relacion = {"origen": ORIGEN, "destino": VECINO}
    ruta.write_text(json.dumps({"version": 1, "flujo_humo": [relacion, relacion]}), encoding="utf-8")
    with pytest.raises(ValueError, match="repetida"):
        cargar_relaciones(ruta, escenario.mina)
    salida = Motor(reglas_eventos()).ejecutar([(ORIGEN, "incendio_reportado", True)])
    assert (VECINO, "cerrado", True) not in salida.hechos


def test_reglas_genericas_con_entidad_explicita():
    r = Regla("E", (Condicion("a", "eq", True, entidad="origen"),
                    Condicion("relacion", "eq", "origen")), (("b", True),), entidad="destino")
    hechos = [("origen", "a", True), ("destino", "relacion", "origen")]
    assert Motor([r]).ejecutar(hechos).traza[0].entidad == "destino"
    with pytest.raises(ValueError):
        Condicion("a", "eq", True, entidad="")


@pytest.mark.parametrize("archivo, texto", [
    ("nivel1_gases.json", "Ruta [ana] desde n13: n13 -> n15 -> n6 -> n10 -> n9 -> n11; distancia 500 m"),
    ("nivel1_derrumbe.json", "Ruta [luis] desde n16: SIN RUTA"),
    ("nivel1_riesgo_vecino.json", "Ruta [ana] desde n13: n13 -> n15 -> n6 -> n10 -> n9 -> n11; distancia 500 m"),
])
def test_tres_escenarios_nivel1_desde_consola(tmp_path, archivo, texto):
    salida = subprocess.run([sys.executable, "-m", "mina_experta", "--escenario",
                            str(ESCENARIOS / archivo)], cwd=tmp_path,
                           capture_output=True, text=True)
    assert salida.returncode == 0, salida.stderr
    assert "16 nodos, 20 túneles" in salida.stdout
    assert texto in salida.stdout
    assert "Línea base [ana]" in salida.stdout and "Línea base [luis]" in salida.stdout


def test_explicacion_por_consola():
    salida = subprocess.run([sys.executable, "-m", "mina_experta", "--escenario",
        str(ESCENARIOS / "nivel1_riesgo_vecino.json"), "--explicar", VECINO],
        cwd=RAIZ, capture_output=True, text=True)
    assert salida.returncode == 0, salida.stderr
    assert f"Explicación de {VECINO}:" in salida.stdout
    assert f"R25: (('{VECINO}', 'expuesto_humo', True),)" in salida.stdout
