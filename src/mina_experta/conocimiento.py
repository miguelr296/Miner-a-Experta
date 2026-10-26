"""Conocimiento mínimo R01–R07; separado del motor genérico."""

import json
from pathlib import Path

from .cargador import _objeto_sin_repeticiones, _rechazar_constante
from .modelo import _validar_numero
from .motor import Condicion, Regla


def reglas_eventos() -> tuple[Regla, ...]:
    """Cierres por eventos reportados; supuestos R04/R05, sin geomecánica."""
    return (
        Regla("R04", (Condicion("incendio_reportado", "eq", True),),
              (("cerrado", True), ("foco_incendio", True)), 100),
        Regla("R05", (Condicion("derrumbe_reportado", "eq", True),),
              (("cerrado", True),), 100),
    )


def reglas_costos(ruta: str | Path) -> tuple[Regla, ...]:
    with Path(ruta).open(encoding="utf-8") as archivo:
        datos = json.load(archivo, object_pairs_hook=_objeto_sin_repeticiones,
                          parse_constant=_rechazar_constante)
    claves = ("multiplicador_alerta_co", "multiplicador_riesgo_alto_co")
    if not isinstance(datos, dict) or set(datos) != set(claves):
        raise ValueError("Configuración de costos incorrecta")
    for clave in claves:
        _validar_numero(datos[clave], clave)
        if datos[clave] < 1:
            raise ValueError("Los factores de costo deben ser al menos 1")
    if datos[claves[1]] < datos[claves[0]]:
        raise ValueError("El riesgo alto no debe costar menos que la alerta")
    return (
        Regla("R06", (Condicion("alerta_co", "eq", True),),
              (("multiplicador", datos[claves[0]]),), 5),
        Regla("R07", (Condicion("riesgo_alto_co", "eq", True),),
              (("multiplicador", datos[claves[1]]),), 5),
    )


def cargar_umbrales_co(ruta: str | Path) -> dict:
    with Path(ruta).open(encoding="utf-8") as archivo:
        datos = json.load(archivo, object_pairs_hook=_objeto_sin_repeticiones,
                          parse_constant=_rechazar_constante)
    if not isinstance(datos, dict) or set(datos) != {"co_ppm"}:
        raise ValueError("La configuración requiere co_ppm")
    limites = datos["co_ppm"]
    nombres = ("alerta", "riesgo_alto", "peligro_inmediato")
    if not isinstance(limites, dict) or set(limites) != set(nombres):
        raise ValueError("Los niveles de CO son incorrectos")
    for nombre in nombres:
        _validar_numero(limites[nombre], nombre)
    if not 0 < limites["alerta"] < limites["riesgo_alto"] < limites["peligro_inmediato"]:
        raise ValueError("Los niveles de CO deben ser positivos y crecientes")
    return limites


def reglas_co(ruta: str | Path) -> tuple[Regla, ...]:
    limites = cargar_umbrales_co(ruta)
    return (
        Regla("R01", (Condicion("co_ppm", "gt", limites["alerta"]),),
              (("alerta_co", True),), 30),
        Regla("R02", (Condicion("alerta_co", "eq", True),
                      Condicion("co_ppm", "gt", limites["riesgo_alto"])),
              (("riesgo_alto_co", True),), 20),
        Regla("R03", (Condicion("riesgo_alto_co", "eq", True),
                      Condicion("co_ppm", "gt", limites["peligro_inmediato"])),
              (("cerrado", True),), 10),
    )
