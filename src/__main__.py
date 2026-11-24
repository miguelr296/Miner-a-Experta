"""Ejecuta una demostración pequeña de la inferencia."""

from argparse import ArgumentParser
import json
from pathlib import Path

from .motor import Hecho, inferir
from .reglas import reglas_de_cierre_por_co


DATOS = Path(__file__).resolve().parent.parent / "data"


def main() -> None:
    analizador = ArgumentParser(description="Ejecuta la cadena de cierre por CO.")
    analizador.add_argument(
        "escenario", type=Path, nargs="?", default=DATOS / "escenarios" / "co_demo.json",
        help="archivo JSON con hechos iniciales",
    )
    argumentos = analizador.parse_args()
    try:
        umbrales = json.loads((DATOS / "umbrales.json").read_text(encoding="utf-8"))
        escenario = json.loads(argumentos.escenario.read_text(encoding="utf-8"))
        hechos = tuple(Hecho(**fila) for fila in escenario["hechos"])
        reglas = reglas_de_cierre_por_co(umbrales["co"]["peligro"])
    except (OSError, ValueError, KeyError, TypeError) as error:
        analizador.error(f"No se pudieron cargar los datos: {error}")

    resultado = inferir(hechos, reglas)
    for indice, paso in enumerate(resultado.traza, start=1):
        premisas = ", ".join(f"{h.atributo}={h.valor}" for h in paso.premisas)
        entidad, atributo, valor = paso.conclusion
        print(
            f"{indice}. {paso.regla} [prioridad {paso.prioridad}, {paso.fuente}] "
            f"{entidad}: {premisas} -> {atributo}={valor}"
        )
    if not resultado.traza:
        print("Ninguna regla se activó.")


if __name__ == "__main__":
    main()
