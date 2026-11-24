"""Memoria de trabajo y encadenamiento hacia adelante por entidad."""

from collections.abc import Iterable
from dataclasses import dataclass
from operator import ge, gt, lt
from typing import Literal, NamedTuple


Valor = str | bool | int | float


class Hecho(NamedTuple):
    entidad: str
    atributo: str
    valor: Valor


@dataclass(frozen=True)
class Condicion:
    atributo: str
    operador: Literal["=", ">", "<", ">="]
    valor: Valor

    def cumple(self, valor: Valor) -> bool:
        if self.operador == "=":
            if isinstance(valor, bool) or isinstance(self.valor, bool):
                return valor is self.valor
            return valor == self.valor
        if type(valor) not in (int, float) or type(self.valor) not in (int, float):
            return False
        return {">": gt, "<": lt, ">=": ge}[self.operador](valor, self.valor)


@dataclass(frozen=True)
class Regla:
    id: str
    prioridad: int
    condiciones: tuple[Condicion, ...]
    atributo: str
    valor: Valor
    fuente: Literal["NORMA", "SUPUESTO"] = "SUPUESTO"
    alguna: bool = False


@dataclass(frozen=True)
class Activacion:
    regla: str
    prioridad: int
    fuente: Literal["NORMA", "SUPUESTO"]
    premisas: tuple[Hecho, ...]
    conclusion: Hecho


@dataclass(frozen=True)
class Conflicto:
    regla: str
    prevalece: str
    propuesta: Hecho
    conservado: Hecho


@dataclass(frozen=True)
class Resultado:
    hechos: tuple[Hecho, ...]
    traza: tuple[Activacion, ...]
    conflictos: tuple[Conflicto, ...]


def inferir(hechos: Iterable[Hecho], reglas: Iterable[Regla]) -> Resultado:
    """Dispara cada par regla-entidad como máximo una vez por ejecución."""
    memoria: dict[str, dict[str, Valor]] = {}
    for entidad, atributo, valor in hechos:
        memoria.setdefault(entidad, {})[atributo] = valor

    ordenadas = sorted(reglas, key=lambda regla: regla.prioridad, reverse=True)
    autores: dict[tuple[str, str], Regla] = {}
    procesadas: set[tuple[str, str]] = set()
    traza = []
    conflictos = []

    while True:
        disparo = False
        for regla in ordenadas:
            for entidad, atributos in memoria.items():
                clave = (regla.id, entidad)
                if clave in procesadas:
                    continue

                premisas = premisas_cumplidas(regla, entidad, atributos)
                if premisas is None:
                    continue

                procesadas.add(clave)
                destino = (entidad, regla.atributo)
                anterior = autores.get(destino)
                conclusion = Hecho(entidad, regla.atributo, regla.valor)
                if anterior is not None and anterior.prioridad > regla.prioridad:
                    if not Condicion(regla.atributo, "=", regla.valor).cumple(anterior.valor):
                        conflictos.append(Conflicto(
                            regla.id, anterior.id, conclusion,
                            Hecho(entidad, regla.atributo, anterior.valor),
                        ))
                    continue

                atributos[regla.atributo] = regla.valor
                autores[destino] = regla
                traza.append(Activacion(
                    regla.id, regla.prioridad, regla.fuente, premisas,
                    conclusion,
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
                tuple(conflictos),
            )


def premisas_cumplidas(
    regla: Regla, entidad: str, atributos: dict[str, Valor]
) -> tuple[Hecho, ...] | None:
    premisas = []
    for condicion in regla.condiciones:
        atributo = condicion.atributo
        cumple = atributo in atributos and condicion.cumple(atributos[atributo])
        if cumple:
            hecho = Hecho(entidad, atributo, atributos[atributo])
            if regla.alguna:
                return (hecho,)
            premisas.append(hecho)
        elif not regla.alguna:
            return None
    return None if regla.alguna else tuple(premisas)
