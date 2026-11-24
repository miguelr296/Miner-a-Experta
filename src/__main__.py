"""Ejecuta una demostración pequeña de la inferencia."""

from argparse import ArgumentParser
import json
from pathlib import Path

from .mina import cargar_mina
from .motor import Hecho, inferir
from .planificador import buscar_ruta
from .reglas import estados_linea_base, preparar_hechos, reglas_del_motor


DATOS = Path(__file__).resolve().parent.parent / "data"


def main() -> None:
    analizador = ArgumentParser(description="Compara rutas con los diagnósticos, eventos y la línea base.")
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
        reglas = reglas_del_motor(umbrales)
        mineros = escenario.get("mineros", [])
        mina = cargar_mina(argumentos.mina)
        resultado = inferir(preparar_hechos(hechos, mina), reglas)
        rutas = []
        if mineros:
            salidas = [n.id for n in mina.nodos.values() if n.tipo == "salida"]
            refugios = [n.id for n in mina.nodos.values() if n.tipo == "refugio"]
            estados_base = estados_linea_base(hechos, resultado.hechos, umbrales)
            for minero in mineros:
                id_minero, nodo = minero["id"], minero["nodo"]
                experta = buscar_ruta(mina, nodo, salidas, resultado.hechos)
                destino = "Salida"
                if experta is None:
                    experta = buscar_ruta(mina, nodo, refugios, resultado.hechos)
                    destino = "Refugio"
                base = buscar_ruta(mina, nodo, salidas, estados_base, ponderar_riesgo=False)
                rutas.append((id_minero, destino, experta, base))
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
    conflictos_ventilacion = [
        c for c in resultado.conflictos if c.propuesta.atributo == "nivel_ventilacion"
    ]
    if conflictos_ventilacion:
        print()
        print("Conflictos de ventilación:")
        for conflicto in conflictos_ventilacion:
            print(f"{conflicto.propuesta.entidad}: {conflicto.regla} descartada; prevalece {conflicto.prevalece}.")
    if rutas:
        print()
        print("Rutas de los mineros:")
    for id_minero, destino, ruta, base in rutas:
        if ruta is None:
            print(f"{id_minero}: sin ruta a una salida o refugio.")
        else:
            camino = " -> ".join(ruta.nodos)
            print(f"{id_minero}: {destino} | {camino} | {ruta.longitud:g} m | costo {ruta.costo:g} | riesgo {ruta.puntaje_riesgo}")
        if base is None:
            print("  Línea base: sin ruta a una salida.")
        else:
            camino_base = " -> ".join(base.nodos)
            print(f"  Línea base: {camino_base} | {base.longitud:g} m | riesgo {base.puntaje_riesgo}")


if __name__ == "__main__":
    main()
