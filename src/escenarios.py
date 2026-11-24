"""Adaptador de los escenarios compartidos con el prototipo web."""

from .mina import Mina, mina_desde_datos
from .motor import ClaveHecho, Hecho, validar_certeza


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


def cargar_hechos(datos: list[dict]) -> tuple[tuple[Hecho, ...], dict[ClaveHecho, float]]:
    hechos = []
    certezas = {}
    for fila in datos:
        hecho = Hecho(fila["entidad"], fila["atributo"], fila["valor"])
        hechos.append(hecho)
        certezas[hecho.entidad, hecho.atributo] = validar_certeza(fila.get("certeza", 1.0))
    return tuple(hechos), certezas
