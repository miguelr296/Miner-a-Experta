"""Escenarios estrictos con datos de entrada, ubicaciones y archivos relativos."""

from dataclasses import dataclass
import json
from pathlib import Path

from .cargador import cargar_mina, _campos, _objeto_sin_repeticiones, _rechazar_constante
from .modelo import Mina, _validar_identificador, _validar_numero
from .motor import Hecho


def validar_lecturas(mina: Mina, hechos) -> tuple[Hecho, ...]:
    """Una lectura por atributo y túnel; no se aceptan conclusiones inyectadas."""
    vistos = set()
    lecturas = []
    for hecho in hechos:
        if not isinstance(hecho, tuple) or len(hecho) != 3:
            raise ValueError("Lectura incorrecta")
        entidad, atributo, valor = hecho
        if not isinstance(entidad, str) or entidad not in mina.aristas:
            raise ValueError(f"Túnel desconocido: {entidad}")
        if atributo not in ("co_ppm", "no2_ppm", "co2_ppm", "h2s_ppm", "o2_porcentaje",
                            "aire_m_min", "uso_anfo", "incendio_reportado", "derrumbe_reportado"):
            raise ValueError(f"Atributo de entrada no permitido: {atributo}")
        clave = entidad, atributo
        if clave in vistos:
            raise ValueError(f"Lectura repetida para {entidad}: {atributo}")
        if atributo in ("co_ppm", "no2_ppm", "co2_ppm", "h2s_ppm", "o2_porcentaje", "aire_m_min"):
            _validar_numero(valor, atributo)
            if valor < 0:
                raise ValueError(f"{atributo} no puede ser negativo")
            if atributo == "o2_porcentaje" and valor > 100:
                raise ValueError("El porcentaje de O2 no puede superar 100")
        elif type(valor) is not bool:
            raise ValueError(f"{atributo} debe ser booleano")
        vistos.add(clave)
        lecturas.append(hecho)
    for entidad, atributo, _ in lecturas:
        if atributo == "aire_m_min" and (entidad, "uso_anfo") not in vistos:
            raise ValueError(f"Debe indicar uso_anfo para evaluar el aire en {entidad}")
    return tuple(lecturas)


@dataclass(frozen=True)
class MineroEscenario:
    id: str
    nodo: str


@dataclass(frozen=True)
class Escenario:
    nombre: str
    mina: Mina
    umbrales: Path
    costos: Path
    mineros: tuple[MineroEscenario, ...]
    destinos: tuple[str, ...]
    hechos: tuple[Hecho, ...]
    ambiente: Path | None = None
    relaciones: Path | None = None


def cargar_escenario(ruta: str | Path) -> Escenario:
    ruta = Path(ruta).resolve()
    try:
        with ruta.open(encoding="utf-8") as archivo:
            datos = json.load(archivo, object_pairs_hook=_objeto_sin_repeticiones,
                              parse_constant=_rechazar_constante)
        opcionales = tuple(k for k in ("ambiente", "relaciones")
                           if isinstance(datos, dict) and k in datos)
        _campos(datos, ("version", "nombre", "mina", "umbrales", "costos",
                        "mineros", "destinos", "hechos") + opcionales, "escenario")
        if type(datos["version"]) is not int or datos["version"] != 1:
            raise ValueError("La versión del escenario debe ser el entero 1")
        for clave in ("nombre", "mina", "umbrales", "costos") + opcionales:
            if not isinstance(datos[clave], str) or not datos[clave].strip():
                raise ValueError(f"{clave} debe ser un texto no vacío")
        mina = cargar_mina(ruta.parent / datos["mina"])
        if not isinstance(datos["mineros"], list) or not datos["mineros"]:
            raise ValueError("El escenario requiere una lista de mineros no vacía")
        mineros = []
        for persona in datos["mineros"]:
            _campos(persona, ("id", "nodo"), "minero")
            _validar_identificador(persona["id"])
            _validar_identificador(persona["nodo"])
            if persona["nodo"] not in mina.nodos:
                raise ValueError(f"Ubicación de minero inexistente: {persona['nodo']}")
            if any(m.id == persona["id"] for m in mineros):
                raise ValueError(f"Minero duplicado: {persona['id']}")
            mineros.append(MineroEscenario(**persona))
        destinos = datos["destinos"]
        if not isinstance(destinos, list) or not destinos:
            raise ValueError("Los destinos deben ser una lista no vacía")
        for destino in destinos:
            _validar_identificador(destino)
            if destino not in mina.nodos:
                raise ValueError(f"Destino inexistente: {destino}")
        if len(set(destinos)) != len(destinos):
            raise ValueError("Destinos repetidos")
        if not isinstance(datos["hechos"], list):
            raise ValueError("Los hechos deben ser una lista")
        hechos = []
        for hecho in datos["hechos"]:
            _campos(hecho, ("entidad", "atributo", "valor"), "hecho")
            hechos.append((hecho["entidad"], hecho["atributo"], hecho["valor"]))
        hechos = validar_lecturas(mina, hechos)
        return Escenario(datos["nombre"], mina, ruta.parent / datos["umbrales"],
                         ruta.parent / datos["costos"], tuple(mineros), tuple(destinos), hechos,
                         ruta.parent / datos["ambiente"] if "ambiente" in datos else None,
                         ruta.parent / datos["relaciones"] if "relaciones" in datos else None)
    except (OSError, UnicodeError, ValueError) as error:
        raise ValueError(f"No se pudo cargar el escenario {ruta}: {error}") from error
