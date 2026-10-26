"""Relaciones explícitas de exposición a humo y reglas instanciadas R24/R25."""

import json
from pathlib import Path

from .cargador import _campos, _objeto_sin_repeticiones, _rechazar_constante
from .motor import Condicion, Regla


def validar_relaciones(mina, relaciones):
    vistas = set()
    resultado = []
    for origen, destino in relaciones:
        if origen not in mina.aristas or destino not in mina.aristas:
            raise ValueError("Relación de humo con túnel inexistente")
        if origen == destino or (origen, destino) in vistas:
            raise ValueError("Relación de humo repetida o hacia sí mismo")
        a, b = mina.aristas[origen], mina.aristas[destino]
        if not {a.origen, a.destino} & {b.origen, b.destino}:
            raise ValueError("Los túneles relacionados deben compartir un nodo")
        vistas.add((origen, destino))
        resultado.append((origen, destino))
    return tuple(resultado)


def cargar_relaciones(ruta: str | Path, mina):
    with Path(ruta).open(encoding="utf-8") as archivo:
        datos = json.load(archivo, object_pairs_hook=_objeto_sin_repeticiones,
                          parse_constant=_rechazar_constante)
    _campos(datos, ("version", "flujo_humo"), "relaciones")
    if type(datos["version"]) is not int or datos["version"] != 1:
        raise ValueError("La versión de relaciones debe ser el entero 1")
    if not isinstance(datos["flujo_humo"], list):
        raise ValueError("flujo_humo debe ser una lista")
    relaciones = []
    for relacion in datos["flujo_humo"]:
        _campos(relacion, ("origen", "destino"), "relación de humo")
        if not all(isinstance(relacion[k], str) for k in ("origen", "destino")):
            raise ValueError("Los extremos de una relación deben ser identificadores")
        relaciones.append((relacion["origen"], relacion["destino"]))
    return validar_relaciones(mina, relaciones)


def hechos_relaciones(relaciones):
    return tuple((destino, "recibe_humo_de", origen) for origen, destino in relaciones)


def reglas_vecindad(relaciones):
    reglas = [Regla(
        f"R24_{origen}__{destino}",
        (Condicion("foco_incendio", "eq", True, entidad=origen),
         Condicion("recibe_humo_de", "eq", origen)),
        (("expuesto_humo", True),), 40, entidad=destino,
    ) for origen, destino in relaciones]
    if relaciones:
        reglas.append(Regla("R25", (Condicion("expuesto_humo", "eq", True),),
                            (("cerrado", True),), 35))
    return tuple(reglas)
