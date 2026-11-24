"""Memoria de trabajo y encadenamiento hacia adelante por entidad."""

from collections.abc import Iterable
from dataclasses import dataclass
from operator import gt, lt
from typing import Literal, NamedTuple


Valor = str | bool | int | float


class Hecho(NamedTuple):
    entidad: str
    atributo: str
    valor: Valor


@dataclass(frozen=True)
class Condicion:
    atributo: str
    operador: Literal["=", ">", "<"]
    valor: Valor

    def cumple(self, valor: Valor) -> bool:
        if self.operador == "=":
            if isinstance(valor, bool) or isinstance(self.valor, bool):
                return valor is self.valor
            return valor == self.valor
        if type(valor) not in (int, float) or type(self.valor) not in (int, float):
            return False
        return {">": gt, "<": lt}[self.operador](valor, self.valor)


@dataclass(frozen=True)
class Regla:
    id: str
    prioridad: int
    condiciones: tuple[Condicion, ...]
    atributo: str
    valor: Valor
    fuente: Literal["NORMA", "SUPUESTO"] = "SUPUESTO"


@dataclass(frozen=True)
class Activacion:
    regla: str
    prioridad: int
    fuente: Literal["NORMA", "SUPUESTO"]
    premisas: tuple[Hecho, ...]
    conclusion: Hecho


@dataclass(frozen=True)
class Resultado:
    hechos: tuple[Hecho, ...]
    traza: tuple[Activacion, ...]


def inferir(hechos: Iterable[Hecho], reglas: Iterable[Regla]) -> Resultado:
    """Dispara cada par regla-entidad como máximo una vez por ejecución."""
    memoria: dict[str, dict[str, Valor]] = {}
    for entidad, atributo, valor in hechos:
        memoria.setdefault(entidad, {})[atributo] = valor

    ordenadas = sorted(reglas, key=lambda regla: regla.prioridad, reverse=True)
    prioridades: dict[tuple[str, str], int] = {}
    procesadas: set[tuple[str, str]] = set()
    traza = []

    while True:
        disparo = False
        for regla in ordenadas:
            for entidad, atributos in memoria.items():
                clave = (regla.id, entidad)
                if clave in procesadas or not all(
                    c.atributo in atributos and c.cumple(atributos[c.atributo])
                    for c in regla.condiciones
                ):
                    continue

                procesadas.add(clave)
                destino = (entidad, regla.atributo)
                prioridad_previa = prioridades.get(destino)
                if prioridad_previa is not None and prioridad_previa > regla.prioridad:
                    continue

                premisas = tuple(
                    Hecho(entidad, c.atributo, atributos[c.atributo])
                    for c in regla.condiciones
                )
                atributos[regla.atributo] = regla.valor
                prioridades[destino] = regla.prioridad
                traza.append(Activacion(
                    regla.id, regla.prioridad, regla.fuente, premisas,
                    Hecho(entidad, regla.atributo, regla.valor),
                ))
                disparo = True

        if not disparo:
            return Resultado(
                tuple(
                    Hecho(entidad, atributo, valor)
                    for entidad, atributos in memoria.items()
                    for atributo, valor in atributos.items()
                ),
                tuple(traza),
            )
