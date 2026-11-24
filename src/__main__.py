"""Ejecuta una demostración pequeña de la inferencia."""

from argparse import ArgumentParser
import json
from pathlib import Path

from .decisiones import evaluar_mineros
from .escenarios import cargar_caso_web, cargar_hechos
from .mina import cargar_mina
from .motor import inferir
from .reglas import estados_linea_base, preparar_entrada, reglas_del_motor


DATOS = Path(__file__).resolve().parent.parent / "data"


def main() -> None:
    analizador = ArgumentParser(description="Compara rutas con los diagnósticos, eventos y la línea base.")
    analizador.add_argument(
        "escenario", type=Path, nargs="?",
        help="archivo JSON con hechos iniciales",
    )
    analizador.add_argument(
        "--mina", type=Path,
        help="archivo JSON con la topología",
    )
    analizador.add_argument("--caso-web", help="escenario de referencia ESC-01 a ESC-05")
    analizador.add_argument("--algoritmo", choices=("dijkstra", "astar"), default="dijkstra")
    analizador.add_argument("--comparar-algoritmos", action="store_true",
                            help="compara las rutas expertas de Dijkstra y A*")
    argumentos = analizador.parse_args()
    if argumentos.caso_web and (argumentos.escenario or argumentos.mina):
        analizador.error("--caso-web ya incluye un escenario y su topología.")
    if argumentos.caso_web and (argumentos.algoritmo == "astar" or argumentos.comparar_algoritmos):
        analizador.error("La referencia web contiene coordenadas esquemáticas. Usa la mina de prueba para A*.")
    try:
        umbrales = json.loads((DATOS / "umbrales.json").read_text(encoding="utf-8"))
        certezas_iniciales = {}
        if argumentos.caso_web:
            referencia = json.loads((DATOS / "referencia_web.json").read_text(encoding="utf-8"))
            mina, hechos, mineros = cargar_caso_web(referencia, argumentos.caso_web.upper())
        else:
            archivo = argumentos.escenario or DATOS / "escenarios" / "co_demo.json"
            escenario = json.loads(archivo.read_text(encoding="utf-8"))
            hechos, certezas_iniciales = cargar_hechos(escenario["hechos"])
            mineros = escenario.get("mineros", [])
            mina = cargar_mina(argumentos.mina or DATOS / "mina_prueba.json")

        reglas = reglas_del_motor(umbrales)
        entrada, certezas = preparar_entrada(hechos, mina, certezas_iniciales)
        resultado = inferir(entrada, reglas, certezas_iniciales=certezas)
        estados_base = estados_linea_base(hechos, resultado.hechos, umbrales)
        evaluaciones = evaluar_mineros(
            mina, mineros, resultado.hechos, estados_base, umbrales["decision"],
            algoritmo=argumentos.algoritmo,
        )
        comparacion = {}
        if argumentos.comparar_algoritmos:
            alternativo = "astar" if argumentos.algoritmo == "dijkstra" else "dijkstra"
            comparacion = {e.id: e.decision.ruta for e in evaluar_mineros(
                mina, mineros, resultado.hechos, estados_base, umbrales["decision"],
                algoritmo=alternativo,
            )}
    except (OSError, ValueError, KeyError, TypeError) as error:
        analizador.error(f"No se pudieron cargar los datos: {error}")

    for indice, paso in enumerate(resultado.traza, start=1):
        premisas = ", ".join(
            f"{h.atributo}={h.valor} ({certeza:.0%})"
            for h, certeza in zip(paso.premisas, paso.certezas_premisas)
        )
        entidad, atributo, valor = paso.conclusion
        print(
            f"{indice}. {paso.regla} [prioridad {paso.prioridad}, {paso.fuente}] "
            f"{entidad}: {premisas} -> {atributo}={valor} (certeza {paso.certeza:.0%})"
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
    if evaluaciones:
        print()
        print("Rutas de los mineros:")
    for evaluacion in evaluaciones:
        decision = evaluacion.decision
        ruta = decision.ruta
        base = evaluacion.linea_base
        if ruta is None:
            print(f"{evaluacion.id}: sin ruta a una salida o refugio.")
        else:
            destino = "Salida" if decision.accion == "evacuar" else "Refugio"
            camino = " -> ".join(ruta.nodos)
            print(f"{evaluacion.id}: {destino} | {camino} | {ruta.longitud:g} m | costo {ruta.costo:g} | riesgo {ruta.puntaje_riesgo}")
        print(f"  {decision.regla} ({decision.accion}): {decision.motivo}")
        if argumentos.comparar_algoritmos:
            otra = comparacion[evaluacion.id]
            dijkstra, astar = (ruta, otra) if argumentos.algoritmo == "dijkstra" else (otra, ruta)
            textos = []
            for nombre, candidata in (("Dijkstra", dijkstra), ("A*", astar)):
                detalle = (f"costo {candidata.costo:g}, {candidata.nodos_explorados} nodos explorados"
                           if candidata is not None else "sin ruta")
                textos.append(f"{nombre}: {detalle}")
            print("  " + " | ".join(textos))
        if base is None:
            print("  Línea base: sin ruta a una salida.")
        else:
            camino_base = " -> ".join(base.nodos)
            print(f"  Línea base: {camino_base} | {base.longitud:g} m | riesgo {base.puntaje_riesgo}")


if __name__ == "__main__":
    main()
