"""Rutas ponderadas, cierres y contrato de costos que respeta D01."""

from pathlib import Path

import pytest

from mina_experta import Arista, Mina, Nodo
from mina_experta.cargador import cargar_mina
from mina_experta.conocimiento import reglas_co, reglas_costos, reglas_eventos
from mina_experta.motor import Motor, Resultado
from mina_experta.planificador import costos_desde_hechos, ruta_menor_costo


RAIZ = Path(__file__).resolve().parents[1]


@pytest.fixture
def mina():
    return Mina("Dos caminos", [Nodo("n1", 0, 0, 0, "frente"),
        Nodo("n2", 1, 0, 0, "refugio"), Nodo("n3", 0, 1, 0, "interseccion"),
        Nodo("n4", 2, 0, 0, "salida")], [
        Arista("t12", "n1", "n2", 1), Arista("t24", "n2", "n4", 1),
        Arista("t13", "n1", "n3", 1), Arista("t34", "n3", "n4", 3),
        Arista("t14", "n1", "n4", 5)])


def resultado(*hechos):
    return Resultado(tuple(hechos), ())


def test_dijkstra_no_confunde_menos_aristas_con_menor_costo(mina):
    ruta = ruta_menor_costo(mina, "n1")
    assert ruta.nodos == ("n1", "n2", "n4")
    assert ruta.aristas == ("t12", "t24")
    assert ruta.distancia_m == ruta.costo == 2


def test_penalizacion_cambia_ruta_sin_cerrar_tunel(mina):
    costos = costos_desde_hechos(mina, resultado(("t12", "multiplicador", 10)))
    ruta = ruta_menor_costo(mina, "n1", costos=costos)
    assert ruta.nodos == ("n1", "n3", "n4")
    assert ruta.distancia_m == ruta.costo == 4
    assert mina.aristas["t12"].longitud_m == 1


def test_factor_maximo_no_producto_y_cierre_domina(mina):
    hechos = resultado(("t12", "multiplicador", 2), ("t12", "multiplicador", 3))
    assert costos_desde_hechos(mina, hechos)["t12"] == 3
    cerrados = costos_desde_hechos(mina, resultado(*hechos.hechos, ("t12", "cerrado", True),
                                                 ("t12", "cerrado", False)))
    assert cerrados["t12"] is None
    with pytest.raises(TypeError):
        cerrados["t12"] = 1


def test_cierre_en_ambos_sentidos(mina):
    costos = costos_desde_hechos(mina, resultado(("t12", "cerrado", True)))
    ida = ruta_menor_costo(mina, "n1", costos=costos)
    vuelta = ruta_menor_costo(mina, "n4", ["n1"], costos)
    assert ida.nodos == ("n1", "n3", "n4")
    assert vuelta.nodos == tuple(reversed(ida.nodos))
    assert "t12" not in ida.aristas + vuelta.aristas


def test_origen_destino_y_falta_de_ruta(mina):
    cero = ruta_menor_costo(mina, "n4")
    assert cero.nodos == ("n4",) and cero.aristas == ()
    assert cero.costo == cero.distancia_m == 0
    assert ruta_menor_costo(mina, "n1", costos={id: None for id in mina.aristas}) is None


def test_varios_destinos_y_costo_distinto_de_distancia(mina):
    assert ruta_menor_costo(mina, "n1", ["n2", "n4"]).nodos == ("n1", "n2")
    ruta = ruta_menor_costo(mina, "n1", costos={"t12": 2})
    assert ruta.costo == 3 and ruta.distancia_m == 2


@pytest.mark.parametrize("origen, destinos", [("ausente", None), ("n1", []), ("n1", ["ausente"])])
def test_extremos_invalidos(mina, origen, destinos):
    with pytest.raises(ValueError):
        ruta_menor_costo(mina, origen, destinos)


@pytest.mark.parametrize("valor", [True, 0, 0.5, -1, float("inf"), float("nan")])
def test_costos_invalidos(mina, valor):
    with pytest.raises(ValueError):
        ruta_menor_costo(mina, "n1", costos={"t12": valor})
    with pytest.raises(ValueError):
        costos_desde_hechos(mina, resultado(("t12", "multiplicador", valor)))


def test_tuneles_desconocidos(mina):
    with pytest.raises(ValueError):
        ruta_menor_costo(mina, "n1", costos={"desconocido": 10})
    with pytest.raises(ValueError):
        costos_desde_hechos(mina, resultado(("desconocido", "cerrado", True)))
    with pytest.raises(ValueError):
        costos_desde_hechos(mina, resultado(("t12", "cerrado", 1)))


def test_integracion_mina_real_motor_y_planificador():
    mina = cargar_mina(RAIZ / "data/mina_prueba.json")
    reglas = (*reglas_co(RAIZ / "data/configuracion/umbrales.json"), *reglas_eventos(),
              *reglas_costos(RAIZ / "data/configuracion/costos.json"))
    limpia = ruta_menor_costo(mina, "n5")
    assert limpia.nodos == ("n5", "n4", "n3", "n2", "n1")
    assert limpia.costo == 470
    inferencia = Motor(reglas).ejecutar([("tunel_3_4", "co_ppm", 120)])
    costos = costos_desde_hechos(mina, inferencia)
    ruta = ruta_menor_costo(mina, "n5", costos=costos)
    assert ruta.nodos == ("n5", "n4", "n8", "n6", "n3", "n2", "n1")
    assert ruta.costo == ruta.distancia_m == 710
    assert "tunel_3_4" not in ruta.aristas
    # Nueva ejecución: el cierre anterior no debe permanecer.
    nuevos = costos_desde_hechos(mina, Motor(reglas).ejecutar([]))
    assert ruta_menor_costo(mina, "n5", costos=nuevos) == limpia
