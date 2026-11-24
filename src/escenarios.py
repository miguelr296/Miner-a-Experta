"""Adaptador de los escenarios compartidos con el prototipo web."""

from .mina import Mina, mina_desde_datos
from .motor import Hecho


def cargar_caso_web(referencia: dict, identificador: str) -> tuple[Mina, tuple[Hecho, ...], list[dict]]:
    mina = mina_desde_datos(referencia["mina"])
    entrada = referencia["casos"][identificador]["entrada"]
    aristas = referencia["mina"]["aristas"]
    sensores = entrada["sensores"]
    hechos = tuple(
        Hecho(arista["id"], atributo, valor)
        for arista in aristas
        for atributo, valor in (
            referencia["lecturas_base"] | sensores.get(arista["id"], {})
        ).items()
    )
    mineros = [
        {"id": id_minero, "nodo": referencia["mineros"][id_minero]}
        for id_minero in entrada["mineros"]
    ]
    return mina, hechos, mineros
