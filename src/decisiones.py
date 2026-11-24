"""Política simulada de recomendación por minero."""

from dataclasses import dataclass

from .mina import Mina
from .motor import Hecho
from .planificador import Ruta, buscar_ruta


@dataclass(frozen=True)
class Decision:
    accion: str
    regla: str
    ruta: Ruta | None
    motivo: str


@dataclass(frozen=True)
class EvaluacionMinero:
    id: str
    decision: Decision
    linea_base: Ruta | None


def recomendar(salida: Ruta | None, refugio: Ruta | None, politica: dict) -> Decision:
    if salida is None:
        if refugio is None:
            return Decision("esperar", "DEC-03", None, "Sin salida ni refugio alcanzable.")
        return Decision(
            "refugiarse", "DEC-02", refugio,
            f"Sin salida alcanzable. El refugio {refugio.nodos[-1]} está a {refugio.longitud:g} m.",
        )

    if (refugio is not None and salida.tramos_altos > 0
            and refugio.longitud <= politica["distancia_refugio_maxima"]
            and salida.costo / max(refugio.costo, 1) > politica["relacion_costo_minima"]):
        return Decision(
            "refugiarse", "DEC-02", refugio,
            f"La salida cruza {salida.tramos_altos} tramo(s) de riesgo alto (costo {salida.costo:g}). "
            f"El refugio {refugio.nodos[-1]} está a {refugio.longitud:g} m (costo {refugio.costo:g}).",
        )

    return Decision(
        "evacuar", "DEC-01", salida,
        f"Salida viable hacia {salida.nodos[-1]} con costo ajustado {salida.costo:g}.",
    )


def evaluar_mineros(
    mina: Mina, mineros: list[dict], hechos: tuple[Hecho, ...],
    linea_base: tuple[Hecho, ...], politica: dict,
) -> list[EvaluacionMinero]:
    salidas = [n.id for n in mina.nodos.values() if n.tipo == "salida"]
    refugios = [n.id for n in mina.nodos.values() if n.tipo == "refugio"]
    evaluaciones = []
    for minero in mineros:
        origen = minero["nodo"]
        salida = buscar_ruta(mina, origen, salidas, hechos)
        refugio = buscar_ruta(mina, origen, refugios, hechos)
        base = buscar_ruta(mina, origen, salidas, linea_base, ponderar_riesgo=False)
        evaluaciones.append(EvaluacionMinero(
            minero["id"], recomendar(salida, refugio, politica), base,
        ))
    return evaluaciones
