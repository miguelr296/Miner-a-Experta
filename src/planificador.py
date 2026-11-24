"""Dijkstra y A* sobre los costos y cierres de la memoria de hechos."""

from collections.abc import Iterable
from dataclasses import dataclass
from heapq import heappop, heappush
from math import dist, inf
from typing import Literal

from .mina import Arista, Mina, es_numero_finito
from .motor import Hecho


Algoritmo = Literal["dijkstra", "astar"]
PUNTAJES_RIESGO = {"normal": 0, "alerta": 1, "alto": 2, "peligro": 3}


@dataclass(frozen=True)
class Ruta:
    nodos: tuple[str, ...]
    aristas: tuple[str, ...]
    longitud: float
    costo: float
    puntaje_riesgo: int
    tramos_altos: int = 0
    nodos_explorados: int = 0


def buscar_ruta(
    mina: Mina, origen: str, destinos: Iterable[str], hechos: Iterable[Hecho],
    *, ponderar_riesgo: bool = True, algoritmo: Algoritmo = "dijkstra",
) -> Ruta | None:
    """Devuelve la ruta transitable de menor costo hacia cualquiera de los destinos."""
    metas = set(destinos)
    if origen not in mina.nodos or not metas <= mina.nodos.keys():
        raise ValueError("El origen y los destinos deben ser nodos de la mina.")

    if not metas:
        return None

    if algoritmo not in ("dijkstra", "astar"):
        raise ValueError(f"Algoritmo desconocido: {algoritmo}.")
    estimaciones = estimar_distancias(mina, metas) if algoritmo == "astar" else {}

    estados = {(entidad, atributo): valor for entidad, atributo, valor in hechos}
    riesgos = {entidad: PUNTAJES_RIESGO[valor] for (entidad, atributo), valor in estados.items()
               if atributo == "nivel_riesgo"}
    distancias = {origen: (0.0, 0)}
    previas: dict[str, Arista] = {}
    pendientes = [(estimaciones.get(origen, 0.0), 0, 0.0, origen)]
    explorados = 0

    while pendientes:
        _, riesgo, distancia_negativa, nodo = heappop(pendientes)
        distancia = -distancia_negativa
        if (distancia, riesgo) != distancias[nodo]:
            continue
        explorados += 1
        if nodo in metas:
            return reconstruir(nodo, previas, distancia, riesgos, explorados)

        for arista in mina.vecinos(nodo):
            if (estados.get((arista.id, "cerrado")) is True
                    or estados.get((arista.id, "transitable")) is False):
                continue
            multiplicador = estados.get((arista.id, "multiplicador"), 1) if ponderar_riesgo else 1
            if not es_numero_finito(multiplicador) or multiplicador < 1:
                raise ValueError(f"Multiplicador inválido en {arista.id}.")
            candidato = distancia + arista.longitud * multiplicador
            if not es_numero_finito(candidato):
                raise ValueError(f"Costo fuera de rango en {arista.id}.")
            riesgo_candidato = riesgo + riesgos.get(arista.id, 0) if ponderar_riesgo else 0
            criterios = (candidato, riesgo_candidato)
            if criterios < distancias.get(arista.destino, (inf, 0)):
                distancias[arista.destino] = criterios
                previas[arista.destino] = arista
                estimado = candidato + estimaciones.get(arista.destino, 0)
                heappush(pendientes, (estimado, riesgo_candidato, -candidato, arista.destino))
    return None


def estimar_distancias(mina: Mina, metas: set[str]) -> dict[str, float]:
    coordenadas = {}
    for nodo in mina.nodos.values():
        if nodo.z is None:
            raise ValueError("A* requiere coordenadas físicas x, y y z para cada nodo.")
        coordenadas[nodo.id] = (nodo.x, nodo.y, nodo.z)

    for origen, aristas in mina.adyacencia.items():
        for arista in aristas:
            distancia_recta = dist(coordenadas[origen], coordenadas[arista.destino])
            if distancia_recta > arista.longitud:
                raise ValueError(f"Longitud menor que la distancia 3D en {arista.id}.")

    metas_3d = [coordenadas[meta] for meta in metas]
    return {
        nodo: min(dist(punto, meta) for meta in metas_3d)
        for nodo, punto in coordenadas.items()
    }


def reconstruir(
    nodo: str, previas: dict[str, Arista], costo: float, riesgos: dict[str, int], explorados: int
) -> Ruta:
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
        sum(riesgos.get(arista.id, 0) for arista in aristas),
        sum(riesgos.get(arista.id, 0) == PUNTAJES_RIESGO["alto"] for arista in aristas),
        explorados,
    )
