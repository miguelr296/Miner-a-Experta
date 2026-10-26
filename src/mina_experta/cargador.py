"""Carga estricta del contrato D20 y comprobaciones globales de la mina."""

import heapq
import json
from pathlib import Path

from .modelo import Arista, Mina, Nodo


class ErrorCarga(ValueError):
    """Archivo ilegible o mina que no cumple el contrato de entrada."""


def _objeto_sin_repeticiones(pares):
    objeto = {}
    for clave, valor in pares:
        if clave in objeto:
            raise ValueError(f"Clave JSON repetida: {clave}")
        objeto[clave] = valor
    return objeto


def _rechazar_constante(valor):
    raise ValueError(f"Constante JSON no admitida: {valor}")


def _campos(objeto, esperados, contexto):
    if not isinstance(objeto, dict) or set(objeto) != set(esperados):
        raise ValueError(f"Campos incorrectos en {contexto}; se requieren {', '.join(esperados)}")


def _validar_estructura(datos):
    _campos(datos, ("version", "nombre", "nodos", "aristas"), "mina")
    if type(datos["version"]) is not int or datos["version"] != 1:
        raise ValueError("La versión debe ser el entero 1")
    for coleccion in ("nodos", "aristas"):
        if not isinstance(datos[coleccion], list) or not datos[coleccion]:
            raise ValueError(f"{coleccion} debe ser una lista no vacía")
    for nodo in datos["nodos"]:
        _campos(nodo, ("id", "x", "y", "nivel", "tipo"), "nodo")
    for arista in datos["aristas"]:
        _campos(arista, ("id", "origen", "destino", "longitud_m"), "arista")


def _validar_mina_completa(mina):
    tipos = {nodo.tipo for nodo in mina.nodos.values()}
    if not {"frente", "refugio", "salida"} <= tipos:
        raise ValueError("La mina requiere frente, refugio y salida")
    visitados = set()
    pendientes = [next(iter(mina.nodos))]
    while pendientes:
        identificador = pendientes.pop()
        if identificador not in visitados:
            visitados.add(identificador)
            pendientes.extend(nodo.id for nodo, _ in mina.vecinos(identificador)
                              if nodo.id not in visitados)
    if visitados != set(mina.nodos):
        raise ValueError("La mina base debe estar conectada")

    # Búsqueda propia desde todos los refugios, limitada a los 500 m de D10.
    distancias = {nodo.id: 0 for nodo in mina.nodos.values() if nodo.tipo == "refugio"}
    pendientes = [(0, identificador) for identificador in distancias]
    heapq.heapify(pendientes)
    while pendientes:
        distancia, identificador = heapq.heappop(pendientes)
        if distancia != distancias[identificador]:
            continue
        for vecino, arista in mina.vecinos(identificador):
            nueva = distancia + arista.longitud_m
            if nueva <= 500 and nueva < distancias.get(vecino.id, float("inf")):
                distancias[vecino.id] = nueva
                heapq.heappush(pendientes, (nueva, vecino.id))
    for nodo in mina.nodos.values():
        if nodo.tipo == "frente" and nodo.id not in distancias:
            raise ValueError(f"El frente {nodo.id} no tiene refugio a 500 m de recorrido")


def cargar_mina(ruta: str | Path) -> Mina:
    """Lee UTF-8, rechaza JSON ambiguo y devuelve una mina completa válida."""
    try:
        with Path(ruta).open(encoding="utf-8") as archivo:
            datos = json.load(archivo, object_pairs_hook=_objeto_sin_repeticiones,
                              parse_constant=_rechazar_constante)
        _validar_estructura(datos)
        mina = Mina(datos["nombre"], [Nodo(**nodo) for nodo in datos["nodos"]],
                    [Arista(**arista) for arista in datos["aristas"]])
        _validar_mina_completa(mina)
        return mina
    except (OSError, UnicodeError, ValueError) as error:
        raise ErrorCarga(f"No se pudo cargar {ruta}: {error}") from error
