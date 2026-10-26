"""Estructura estática de la mina, sin sensores ni costos de emergencia."""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
import math
import re
from types import MappingProxyType


def _validar_identificador(valor: str) -> None:
    if not isinstance(valor, str) or re.fullmatch(r"[a-z][a-z0-9_]*", valor) is None:
        raise ValueError(f"Identificador inválido: {valor!r}")


def _validar_numero(valor: float, campo: str) -> None:
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f"{campo} debe ser un número finito")
    try:
        finito = math.isfinite(valor)
    except OverflowError:
        finito = False
    if not finito:
        raise ValueError(f"{campo} debe ser un número finito representable")


@dataclass(frozen=True, slots=True)
class Nodo:
    """Lugar identificado por coordenadas espaciales en metros y tipo."""

    id: str
    x: float
    y: float
    nivel: float
    tipo: str

    def __post_init__(self):
        _validar_identificador(self.id)
        for campo in ("x", "y", "nivel"):
            _validar_numero(getattr(self, campo), campo)
        if self.tipo not in ("interseccion", "salida", "refugio", "frente"):
            raise ValueError(f"Tipo de nodo inválido: {self.tipo!r}")

    @property
    def coordenadas(self) -> tuple[float, float, float]:
        return self.x, self.y, self.nivel


@dataclass(frozen=True, slots=True)
class Arista:
    """Túnel bidireccional; la longitud es física, no un costo de riesgo."""

    id: str
    origen: str
    destino: str
    longitud_m: float

    def __post_init__(self):
        for identificador in (self.id, self.origen, self.destino):
            _validar_identificador(identificador)
        if self.origen == self.destino:
            raise ValueError("Un túnel debe conectar dos nodos distintos")
        _validar_numero(self.longitud_m, "longitud_m")
        if self.longitud_m <= 0:
            raise ValueError("La longitud de un túnel debe ser positiva")


class Mina:
    """Colecciones de solo lectura y consulta bidireccional de vecinos.

    Valida la coherencia local del grafo. La conectividad global, los tipos
    requeridos y D10 se comprobarán al cargar una mina completa en S1-11.
    """

    def __init__(self, nombre: str, nodos: Iterable[Nodo], aristas: Iterable[Arista]):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("La mina necesita un nombre no vacío")
        por_nodo = {}
        for nodo in nodos:
            if nodo.id in por_nodo:
                raise ValueError(f"Nodo duplicado: {nodo.id}")
            por_nodo[nodo.id] = nodo

        por_arista = {}
        conexiones = {identificador: [] for identificador in por_nodo}
        pares = set()
        for arista in aristas:
            if arista.id in por_arista:
                raise ValueError(f"Arista duplicada: {arista.id}")
            if arista.origen not in por_nodo or arista.destino not in por_nodo:
                raise ValueError(f"Extremo inexistente en {arista.id}")
            par = frozenset((arista.origen, arista.destino))
            if par in pares:
                raise ValueError(f"Par de nodos repetido en {arista.id}")
            origen, destino = por_nodo[arista.origen], por_nodo[arista.destino]
            if arista.longitud_m < math.dist(origen.coordenadas, destino.coordenadas):
                raise ValueError(f"Longitud menor que la distancia recta en {arista.id}")
            pares.add(par)
            por_arista[arista.id] = arista
            conexiones[origen.id].append((destino, arista))
            conexiones[destino.id].append((origen, arista))

        self._nombre = nombre
        self._nodos = MappingProxyType(por_nodo)
        self._aristas = MappingProxyType(por_arista)
        self._vecinos = {identificador: tuple(lista)
                         for identificador, lista in conexiones.items()}

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def nodos(self) -> Mapping[str, Nodo]:
        return self._nodos

    @property
    def aristas(self) -> Mapping[str, Arista]:
        return self._aristas

    def vecinos(self, identificador: str) -> tuple[tuple[Nodo, Arista], ...]:
        """Devuelve pares (nodo vecino, túnel), en el orden de las aristas."""
        if identificador not in self._vecinos:
            raise KeyError(f"Nodo inexistente: {identificador}")
        return self._vecinos[identificador]
