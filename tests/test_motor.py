from src.motor import Condicion, Hecho, Regla, inferir
from src.reglas import reglas_de_cierre_por_co


def test_cadena_co_identifica_y_cierra_solo_el_tunel_afectado():
    resultado = inferir(
        [Hecho("afectado", "co_ppm", 101), Hecho("límite", "co_ppm", 100)],
        reglas_de_cierre_por_co(100),
    )

    assert [paso.regla for paso in resultado.traza] == [
        "R-CO-03", "R-RIESGO-07", "R-RIESGO-01", "R-RUTA-01",
    ]
    assert resultado.traza[0].premisas == (Hecho("afectado", "co_ppm", 101),)
    assert resultado.traza[-1].premisas == (Hecho("afectado", "cerrado", True),)
    assert all(paso.fuente == "SUPUESTO" for paso in resultado.traza)
    assert Hecho("afectado", "transitable", False) in resultado.hechos
    assert all(paso.conclusion.entidad == "afectado" for paso in resultado.traza)


def test_prioridad_protege_conclusion_y_refraccion_es_por_entidad():
    condicion = (Condicion("evento", "=", True),)
    reglas = (
        Regla("BAJA", 10, condicion, "riesgo", "alerta"),
        Regla("ALTA", 20, condicion, "riesgo", "alto"),
    )
    hechos = [Hecho("a", "evento", True), Hecho("b", "evento", True)]
    resultado = inferir(hechos, reglas)

    assert [(paso.regla, paso.conclusion.entidad) for paso in resultado.traza] == [
        ("ALTA", "a"), ("ALTA", "b"),
    ]
    assert inferir(hechos, reglas) == resultado


def test_ausencia_y_booleanos_no_cumplen_condiciones_numericas():
    regla = Regla("MEDICION", 10, (Condicion("co_ppm", ">", 0),), "riesgo", "alerta")
    resultado = inferir(
        [Hecho("a", "evento", True), Hecho("b", "co_ppm", True)],
        [regla],
    )

    assert not resultado.traza
    assert not Condicion("evento", "=", True).cumple(1)
