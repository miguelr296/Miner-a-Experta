"""Memoria de trabajo y encadenamiento hacia adelante por entidad."""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from operator import ge, gt, lt
from typing import Literal, NamedTuple


Valor = str | bool | int | float
ClaveHecho = tuple[str, str]


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
    certeza: float = 1.0


@dataclass(frozen=True)
class Activacion:
    regla: str
    prioridad: int
    fuente: Literal["NORMA", "SUPUESTO"]
    premisas: tuple[Hecho, ...]
    conclusion: Hecho
    certeza: float
    certezas_premisas: tuple[float, ...]


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
    certezas: dict[ClaveHecho, float]


def validar_certeza(valor: float) -> float:
    if type(valor) not in (int, float) or not 0 <= valor <= 1:
        raise ValueError("La certeza debe ser un número entre 0 y 1.")
    return float(valor)


def inferir(
    hechos: Iterable[Hecho], reglas: Iterable[Regla],
    *, certezas_iniciales: Mapping[ClaveHecho, float] | None = None,
) -> Resultado:
    """Dispara cada par regla-entidad como máximo una vez por ejecución."""
    memoria: dict[str, dict[str, Valor]] = {}
    certezas: dict[ClaveHecho, float] = {}
    iniciales = certezas_iniciales or {}
    for entidad, atributo, valor in hechos:
        memoria.setdefault(entidad, {})[atributo] = valor
        certezas[entidad, atributo] = validar_certeza(iniciales.get((entidad, atributo), 1.0))

    ordenadas = sorted(reglas, key=lambda regla: regla.prioridad, reverse=True)
    factores = {regla.id: validar_certeza(regla.certeza) for regla in ordenadas}
    autores: dict[ClaveHecho, Regla] = {}
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

                premisas = premisas_cumplidas(regla, entidad, atributos, certezas)
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

                apoyos = tuple(certezas[h.entidad, h.atributo] for h in premisas)
                certeza = min(apoyos, default=1.0) * factores[regla.id]
                atributos[regla.atributo] = regla.valor
                certezas[destino] = certeza
                autores[destino] = regla
                traza.append(Activacion(
                    regla.id, regla.prioridad, regla.fuente, premisas,
                    conclusion, certeza, apoyos,
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
                certezas,
            )


def premisas_cumplidas(
    regla: Regla, entidad: str, atributos: dict[str, Valor], certezas: dict[ClaveHecho, float],
) -> tuple[Hecho, ...] | None:
    premisas = []
    for condicion in regla.condiciones:
        atributo = condicion.atributo
        cumple = atributo in atributos and condicion.cumple(atributos[atributo])
        if cumple:
            hecho = Hecho(entidad, atributo, atributos[atributo])
            premisas.append(hecho)
        elif not regla.alguna:
            return None
    if regla.alguna:
        if not premisas:
            return None
        return (max(premisas, key=lambda h: certezas[h.entidad, h.atributo]),)
    return tuple(premisas)
