"""Dijkstra con cierres y costos generados por la memoria de hechos."""

from collections.abc import Iterable
from dataclasses import dataclass
from heapq import heappop, heappush
from math import inf

from .mina import Arista, Mina, es_numero_finito
from .motor import Hecho


@dataclass(frozen=True)
class Ruta:
    nodos: tuple[str, ...]
    aristas: tuple[str, ...]
    longitud: float
    costo: float


def buscar_ruta(
    mina: Mina, origen: str, destinos: Iterable[str], hechos: Iterable[Hecho]
) -> Ruta | None:
    """Devuelve la ruta transitable de menor costo hacia cualquiera de los destinos."""
    metas = set(destinos)
    if origen not in mina.nodos or not metas <= mina.nodos.keys():
        raise ValueError("El origen y los destinos deben ser nodos de la mina.")

    if not metas:
        return None

    estados = {(entidad, atributo): valor for entidad, atributo, valor in hechos}
    distancias = {origen: 0.0}
    previas: dict[str, Arista] = {}
    pendientes = [(0.0, origen)]

    while pendientes:
        distancia, nodo = heappop(pendientes)
        if distancia != distancias[nodo]:
            continue
        if nodo in metas:
            return reconstruir(nodo, previas, distancia)

        for arista in mina.vecinos(nodo):
            if (estados.get((arista.id, "cerrado")) is True
                    or estados.get((arista.id, "transitable")) is False):
                continue
            multiplicador = estados.get((arista.id, "multiplicador"), 1)
            if not es_numero_finito(multiplicador) or multiplicador < 1:
                raise ValueError(f"Multiplicador inválido en {arista.id}.")
            candidato = distancia + arista.longitud * multiplicador
            if not es_numero_finito(candidato):
                raise ValueError(f"Costo fuera de rango en {arista.id}.")
            if candidato < distancias.get(arista.destino, inf):
                distancias[arista.destino] = candidato
                previas[arista.destino] = arista
                heappush(pendientes, (candidato, arista.destino))
    return None


def reconstruir(nodo: str, previas: dict[str, Arista], costo: float) -> Ruta:
    nodos = [nodo]
    aristas: list[Arista] = []
    while nodo in previas:
        arista = previas[nodo]
        aristas.append(arista)
        nodo = arista.origen
        nodos.append(nodo)

    return Ruta(
        tuple(reversed(nodos)),
        tuple(arista.id for arista in reversed(aristas)),
        sum(arista.longitud for arista in aristas),
        costo,
    )
