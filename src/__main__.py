"""Ejecuta una demostración pequeña de la inferencia."""

from argparse import ArgumentParser
import json
from pathlib import Path

from .mina import cargar_mina
from .motor import Hecho, inferir
from .planificador import buscar_ruta
from .reglas import reglas_de_cierre_por_co


DATOS = Path(__file__).resolve().parent.parent / "data"


def main() -> None:
    analizador = ArgumentParser(description="Ejecuta la inferencia por CO y calcula rutas en la mina de prueba.")
    analizador.add_argument(
        "escenario", type=Path, nargs="?", default=DATOS / "escenarios" / "co_demo.json",
        help="archivo JSON con hechos iniciales",
    )
    analizador.add_argument(
        "--mina", type=Path, default=DATOS / "mina_prueba.json",
        help="archivo JSON con la topología",
    )
    argumentos = analizador.parse_args()
    try:
        umbrales = json.loads((DATOS / "umbrales.json").read_text(encoding="utf-8"))
        escenario = json.loads(argumentos.escenario.read_text(encoding="utf-8"))
        hechos = tuple(Hecho(**fila) for fila in escenario["hechos"])
        reglas = reglas_de_cierre_por_co(umbrales["co"]["peligro"])
        resultado = inferir(hechos, reglas)
        mineros = escenario.get("mineros", [])
        rutas = []
        if mineros:
            mina = cargar_mina(argumentos.mina)
            salidas = [n.id for n in mina.nodos.values() if n.tipo == "salida"]
            refugios = [n.id for n in mina.nodos.values() if n.tipo == "refugio"]
            for minero in mineros:
                id_minero, nodo = minero["id"], minero["nodo"]
                ruta = buscar_ruta(mina, nodo, salidas, resultado.hechos)
                if ruta is not None:
                    rutas.append((id_minero, "Salida", ruta))
                    continue
                ruta = buscar_ruta(mina, nodo, refugios, resultado.hechos)
                rutas.append((id_minero, "Refugio", ruta))
    except (OSError, ValueError, KeyError, TypeError) as error:
        analizador.error(f"No se pudieron cargar los datos: {error}")

    for indice, paso in enumerate(resultado.traza, start=1):
        premisas = ", ".join(f"{h.atributo}={h.valor}" for h in paso.premisas)
        entidad, atributo, valor = paso.conclusion
        print(
            f"{indice}. {paso.regla} [prioridad {paso.prioridad}, {paso.fuente}] "
            f"{entidad}: {premisas} -> {atributo}={valor}"
        )
    if not resultado.traza:
        print("Ninguna regla se activó.")
    if rutas:
        print()
        print("Rutas de los mineros:")
    for id_minero, destino, ruta in rutas:
        if ruta is None:
            print(f"{id_minero}: sin ruta a una salida o refugio.")
        else:
            camino = " -> ".join(ruta.nodos)
            print(f"{id_minero}: {destino} | {camino} | {ruta.longitud:g} m | costo {ruta.costo:g}")


if __name__ == "__main__":
    main()
