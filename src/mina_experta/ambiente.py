"""Umbrales y reglas R08–R23 de gases y ventilación, independientes del motor."""

import json
from pathlib import Path

from .cargador import _campos, _objeto_sin_repeticiones, _rechazar_constante
from .modelo import _validar_numero
from .motor import Condicion, Regla


GASES = ("no2_ppm", "co2_ppm", "h2s_ppm", "o2_porcentaje")


def cargar_ambiente(ruta: str | Path) -> dict:
    with Path(ruta).open(encoding="utf-8") as archivo:
        datos = json.load(archivo, object_pairs_hook=_objeto_sin_repeticiones,
                          parse_constant=_rechazar_constante)
    _campos(datos, ("gases", "ventilacion", "factores"), "ambiente")
    _campos(datos["gases"], GASES, "gases")
    niveles = ("alerta", "riesgo_alto", "peligro_inmediato")
    for gas in GASES:
        limite = datos["gases"][gas]
        _campos(limite, niveles + (("maximo",) if gas == "o2_porcentaje" else ()), gas)
        for nombre, valor in limite.items():
            _validar_numero(valor, f"{gas}.{nombre}")
        a, r, p = (limite[n] for n in niveles)
        correcto = (0 < p < r < a < limite["maximo"] <= 100 if gas == "o2_porcentaje"
                    else 0 < a < r < p)
        if not correcto:
            raise ValueError(f"Niveles fuera de orden para {gas}")
    ventilacion = datos["ventilacion"]
    _campos(ventilacion, ("minimo", "minimo_anfo", "maximo"), "ventilación")
    for nombre, valor in ventilacion.items():
        _validar_numero(valor, nombre)
    if not 0 < ventilacion["minimo"] <= ventilacion["minimo_anfo"] < ventilacion["maximo"]:
        raise ValueError("Límites de ventilación fuera de orden")
    factores = datos["factores"]
    _campos(factores, ("alerta", "riesgo_alto", "ventilacion"), "factores")
    for nombre, valor in factores.items():
        _validar_numero(valor, nombre)
        if valor < 1:
            raise ValueError("Los factores no pueden reducir costos")
    if factores["riesgo_alto"] < factores["alerta"]:
        raise ValueError("El riesgo alto no debe costar menos que la alerta")
    return datos


def reglas_ambiente(config: dict) -> tuple[Regla, ...]:
    reglas = []
    factores = config["factores"]
    for indice, gas in enumerate(GASES):
        limite = config["gases"][gas]
        operador = "lt" if gas == "o2_porcentaje" else "gt"
        alerta, alto = f"alerta_{gas}", f"riesgo_alto_{gas}"
        numero = 8 + indice * 3
        reglas.extend((
            Regla(f"R{numero:02d}", (Condicion(gas, operador, limite["alerta"]),),
                  ((alerta, True), ("multiplicador", factores["alerta"])), 30),
            Regla(f"R{numero + 1:02d}", (Condicion(alerta, "eq", True),
                  Condicion(gas, operador, limite["riesgo_alto"])),
                  ((alto, True), ("multiplicador", factores["riesgo_alto"])), 20),
            Regla(f"R{numero + 2:02d}", (Condicion(alto, "eq", True),
                  Condicion(gas, operador, limite["peligro_inmediato"])), (("cerrado", True),), 10),
        ))
    v = config["ventilacion"]
    reglas.extend((
        Regla("R20", (Condicion("o2_porcentaje", "gt", config["gases"]["o2_porcentaje"]["maximo"]),),
              (("alerta_o2_exceso", True), ("multiplicador", factores["alerta"])), 30),
        Regla("R21", (Condicion("aire_m_min", "lt", v["minimo"]),),
              (("ventilacion_insuficiente", True), ("multiplicador", factores["ventilacion"])), 30),
        Regla("R22", (Condicion("aire_m_min", "gt", v["maximo"]),),
              (("ventilacion_excesiva", True), ("multiplicador", factores["ventilacion"])), 30),
        Regla("R23", (Condicion("uso_anfo", "eq", True),
                      Condicion("aire_m_min", "lt", v["minimo_anfo"])),
              (("ventilacion_insuficiente_anfo", True), ("multiplicador", factores["ventilacion"])), 30),
    ))
    return tuple(reglas)
