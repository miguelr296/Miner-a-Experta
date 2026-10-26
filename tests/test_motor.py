"""Cadena, resolución por prioridad, entidades independientes y refracción."""

import pytest

from mina_experta.motor import Condicion, Motor, Regla


def regla(id, atributo, valor, conclusion, prioridad=0):
    return Regla(id, (Condicion(atributo, "eq", valor),), (conclusion,), prioridad)


def test_cadena_recalcula_aplicables_y_explicacion():
    motor = Motor([regla("E3", "a", True, ("d", True), 10),
                   regla("E2", "b", True, ("c", True), 20),
                   regla("E1", "a", True, ("b", True), 30)])
    iniciales = [("t1", "a", True)]
    assert [a.regla.id for a in motor.aplicables(iniciales)] == ["E1", "E3"]
    resultado = motor.ejecutar(iniciales)
    assert [p.regla_id for p in resultado.traza] == ["E1", "E2", "E3"]
    assert set(resultado.hechos) == {("t1", a, True) for a in "abcd"}
    assert resultado.por_que(("t1", "c", True))[0].antecedentes == (("t1", "b", True),)
    assert resultado.por_que(("t1", "inexistente", True)) == ()
    assert iniciales == [("t1", "a", True)]


def test_refraccion_evitar_bucle_y_reiniciar_ejecucion():
    motor = Motor([regla("E1", "a", True, ("a", True))])
    primero = motor.ejecutar([("t1", "a", True)])
    assert len(primero.traza) == 1
    assert primero.traza[0].hechos_nuevos == ()
    assert primero == motor.ejecutar([("t1", "a", True)])
    assert motor.ejecutar([]).traza == ()


def test_misma_regla_para_dos_entidades():
    motor = Motor([regla("E1", "a", True, ("b", True))])
    resultado = motor.ejecutar([("t2", "a", True), ("t1", "a", True), ("t1", "a", True)])
    assert [p.entidad for p in resultado.traza] == ["t1", "t2"]
    assert len(resultado.hechos) == 4


def test_no_combina_condiciones_de_entidades_distintas():
    r = Regla("E", (Condicion("a", "eq", True), Condicion("b", "eq", True)), (("c", True),))
    motor = Motor([r])
    assert motor.ejecutar([("t1", "a", True), ("t2", "b", True)]).traza == ()
    assert len(motor.ejecutar([("t1", "a", True), ("t1", "b", True)]).traza) == 1


def test_desempate_por_id():
    motor = Motor([regla("B", "a", True, ("b", True)),
                   regla("A", "a", True, ("c", True))])
    assert [p.regla_id for p in motor.ejecutar([("t", "a", True)]).traza] == ["A", "B"]


def test_varios_soportes_misma_conclusion():
    r = Regla("E", (Condicion("x", "gt", 10),), (("alerta", True),))
    resultado = Motor([r]).ejecutar([("t", "x", 20), ("t", "x", 30)])
    assert len(resultado.traza) == 2
    assert len(resultado.traza[0].hechos_nuevos) == 1
    assert resultado.traza[1].hechos_nuevos == ()


def test_booleanos_no_son_mediciones():
    motor = Motor([regla("E", "x", True, ("y", True))])
    resultado = motor.ejecutar([("t", "x", 1), ("t", "x", True)])
    assert len(resultado.hechos) == 3
    assert len(resultado.traza) == 1
    assert resultado.traza[0].antecedentes == (("t", "x", True),)
    assert not Condicion("x", "gt", 0).cumple(("t", "x", True))


@pytest.mark.parametrize("operador, valor, cumple", [
    ("eq", 10, True), ("eq", 11, False), ("gt", 10, False), ("gt", 11, True),
    ("ge", 10, True), ("lt", 9, True), ("lt", 10, False), ("le", 10, True)])
def test_operadores(operador, valor, cumple):
    assert Condicion("x", operador, 10).cumple(("t", "x", valor)) is cumple


@pytest.mark.parametrize("hecho", [["t", "x", 1], ("t", "x"), ("", "x", 1),
    ("t", "x", []), ("t", "x", float("nan")), ("t", "x", float("inf"))])
def test_hechos_invalidos(hecho):
    with pytest.raises(ValueError):
        Motor([]).ejecutar([hecho])


def test_rechaza_reglas_ambiguas_y_operadores():
    r = regla("E", "x", True, ("y", True))
    with pytest.raises(ValueError, match="duplicados"):
        Motor([r, r])
    with pytest.raises(ValueError, match="Operador"):
        Condicion("x", "inventado", 1)
    with pytest.raises(ValueError):
        Condicion("x", "gt", True)


def test_limite_no_devuelve_resultado_parcial_como_completo():
    motor = Motor([regla("A", "x", True, ("y", True)), regla("B", "y", True, ("z", True))])
    with pytest.raises(RuntimeError, match="incompleta"):
        motor.ejecutar([("t", "x", True)], max_disparos=1)
    assert len(motor.ejecutar([("t", "x", True)], max_disparos=2).traza) == 2
