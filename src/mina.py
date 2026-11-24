"""Modelo de la mina y carga de la topología desde JSON."""

from dataclasses import dataclass
import json
from math import isfinite
from pathlib import Path


TIPOS_NODO = {"interseccion", "salida", "refugio", "frente"}


@dataclass(frozen=True)
class Nodo:
    id: str
    x: float
    y: float
    nivel: int
    tipo: str


@dataclass(frozen=True)
class Arista:
    id: str
    origen: str
    destino: str
    longitud: float


@dataclass(frozen=True)
class Mina:
    nodos: dict[str, Nodo]
    adyacencia: dict[str, tuple[Arista, ...]]

    def vecinos(self, nodo: str) -> tuple[Arista, ...]:
        return self.adyacencia[nodo]


def cargar_mina(ruta: Path) -> Mina:
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    if not isinstance(datos, dict):
        raise ValueError("La mina debe ser un objeto JSON.")
    filas_nodos = datos.get("nodos")
    filas_aristas = datos.get("aristas")
    if not isinstance(filas_nodos, list) or not filas_nodos or not isinstance(filas_aristas, list):
        raise ValueError("La mina requiere listas de nodos y aristas.")

    nodos: dict[str, Nodo] = {}
    for fila in filas_nodos:
        if not isinstance(fila, dict):
            raise ValueError("Cada nodo debe ser un objeto.")
        id_nodo = fila.get("id")
        x, y, nivel, tipo = (fila.get(campo) for campo in ("x", "y", "nivel", "tipo"))
        if not isinstance(id_nodo, str) or not id_nodo.strip() or id_nodo in nodos:
            raise ValueError(f"Identificador de nodo inválido o repetido: {id_nodo!r}.")
        if not (es_numero_finito(x) and es_numero_finito(y) and type(nivel) is int
                and isinstance(tipo, str) and tipo in TIPOS_NODO):
            raise ValueError(f"Coordenadas, nivel o tipo inválidos en {id_nodo}.")
        nodos[id_nodo] = Nodo(id_nodo, x, y, nivel, tipo)

    vecinos: dict[str, list[Arista]] = {id_nodo: [] for id_nodo in nodos}
    ids = set()
    for fila in filas_aristas:
        if not isinstance(fila, dict):
            raise ValueError("Cada arista debe ser un objeto.")
        id_arista, origen, destino, longitud = (
            fila.get(campo) for campo in ("id", "origen", "destino", "longitud")
        )
        if not isinstance(id_arista, str) or not id_arista.strip() or id_arista in ids:
            raise ValueError(f"Identificador de arista inválido o repetido: {id_arista!r}.")
        if not (isinstance(origen, str) and isinstance(destino, str)
                and origen in nodos and destino in nodos and origen != destino):
            raise ValueError(f"Extremos inválidos en la arista {id_arista}.")
        if not es_numero_finito(longitud) or longitud <= 0:
            raise ValueError(f"Longitud inválida en la arista {id_arista}.")
        ids.add(id_arista)
        vecinos[origen].append(Arista(id_arista, origen, destino, longitud))
        vecinos[destino].append(Arista(id_arista, destino, origen, longitud))

    return Mina(nodos, {nodo: tuple(aristas) for nodo, aristas in vecinos.items()})


def es_numero_finito(valor: object) -> bool:
    if type(valor) not in (int, float):
        return False
    try:
        return isfinite(valor)
    except OverflowError:
        return False
