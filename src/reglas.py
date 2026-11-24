"""Reglas de la demostración de cierre por CO del prototipo."""

from .motor import Condicion, Regla


def reglas_de_cierre_por_co(umbral_co: float) -> tuple[Regla, ...]:
    return (
        Regla("R-CO-03", 50, (Condicion("co_ppm", ">", umbral_co),), "nivel_co", "peligro"),
        Regla("R-RIESGO-07", 79, (Condicion("nivel_co", "=", "peligro"),), "nivel_riesgo", "peligro"),
        Regla("R-RIESGO-01", 90, (Condicion("nivel_riesgo", "=", "peligro"),), "cerrado", True),
        Regla("R-RUTA-01", 95, (Condicion("cerrado", "=", True),), "transitable", False),
    )
