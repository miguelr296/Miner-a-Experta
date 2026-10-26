"""Dijkstra propio sobre costos dinámicos, sin modificar la geometría base."""

from dataclasses import dataclass
import heapq
import math
from types import MappingProxyType

from .modelo import Mina, _validar_numero
from .motor import Resultado


@dataclass(frozen=True)
class Ruta:
    nodos: tuple[str, ...]
    aristas: tuple[str, ...]
    distancia_m: float
    costo: float


def costos_desde_hechos(mina: Mina, resultado: Resultado):
    """None representa cierre; domina a los multiplicadores, combinados por máximo."""
    factores = {identificador: 1 for identificador in mina.aristas}
    cerrados = set()
    for entidad, atributo, valor in resultado.hechos:
        if atributo not in ("cerrado", "multiplicador"):
            continue
        if entidad not in mina.aristas:
            raise ValueError(f"Hecho de ruta sobre un túnel inexistente: {entidad}")
        if atributo == "cerrado":
            if type(valor) is not bool:
                raise ValueError("El cierre debe ser booleano")
            if valor:
                cerrados.add(entidad)
        else:
            _validar_numero(valor, "multiplicador")
            if valor < 1:
                raise ValueError("El multiplicador no puede reducir costos")
            factores[entidad] = max(factores[entidad], valor)
    costos = {}
    for identificador, arista in mina.aristas.items():
        costo = arista.longitud_m * factores[identificador]
        _validar_numero(costo, "costo")
        costos[identificador] = None if identificador in cerrados else costo
    return MappingProxyType(costos)


def ruta_menor_costo(mina: Mina, origen: str, destinos=None, costos=None) -> Ruta | None:
    """Busca la salida más barata por defecto; None indica ausencia de ruta.

    Se pueden indicar otros destinos explícitos. No decide automáticamente
    entre evacuación y refugio. El costo se mide en metros ponderados por riesgo.
    """
    if origen not in mina.nodos:
        raise ValueError(f"Origen inexistente: {origen}")
    objetivos = ({n.id for n in mina.nodos.values() if n.tipo == "salida"}
                 if destinos is None else set(destinos))
    if not objetivos or not objetivos <= set(mina.nodos):
        raise ValueError("Los destinos deben existir y no estar vacíos")
    pesos = {id: arista.longitud_m for id, arista in mina.aristas.items()}
    if costos is not None:
        if not set(costos) <= set(pesos):
            raise ValueError("Costo para túnel inexistente")
        pesos.update(costos)
    for identificador, peso in pesos.items():
        if peso is not None:
            _validar_numero(peso, "costo")
            if peso < mina.aristas[identificador].longitud_m:
                raise ValueError("El costo no puede ser menor que la longitud física")
    distancias = {origen: 0}
    anteriores = {}
    pendientes = [(0, origen)]
    while pendientes:
        distancia, identificador = heapq.heappop(pendientes)
        if distancia != distancias[identificador]:
            continue
        if identificador in objetivos:
            nodos, aristas = [identificador], []
            while identificador != origen:
                identificador, arista_id = anteriores[identificador]
                nodos.append(identificador)
                aristas.append(arista_id)
            aristas.reverse()
            return Ruta(tuple(reversed(nodos)), tuple(aristas),
                        math.fsum(mina.aristas[id].longitud_m for id in aristas), distancia)
        for vecino, arista in mina.vecinos(identificador):
            peso = pesos[arista.id]
            if peso is None:
                continue
            nueva = distancia + peso
            _validar_numero(nueva, "costo acumulado")
            if nueva < distancias.get(vecino.id, float("inf")):
                distancias[vecino.id] = nueva
                anteriores[vecino.id] = (identificador, arista.id)
                heapq.heappush(pendientes, (nueva, vecino.id))
    return None
