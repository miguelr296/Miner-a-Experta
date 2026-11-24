"""Construcción del catálogo de gases a partir de la configuración JSON."""

from .motor import Condicion, Hecho, Regla


def condicion_gas(configuracion: dict, nivel: str) -> Condicion:
    return Condicion(configuracion["atributo"], configuracion["operador"], configuracion[nivel])


def reglas_de_gases(configuracion: dict) -> tuple[Regla, ...]:
    gases = configuracion["gases"]
    reglas = []
    for gas, parametros in gases.items():
        niveles = (
            ("alerta", 40, "NORMA"),
            ("alto", 45, parametros["fuente_alto"]),
            ("peligro", 50, "SUPUESTO"),
        )
        for numero, (nivel, prioridad, fuente) in enumerate(niveles, start=1):
            reglas.append(Regla(
                f"R-{gas.upper()}-{numero:02d}", prioridad,
                (condicion_gas(parametros, nivel),), f"nivel_{gas}", nivel, fuente,
            ))

    for nivel, id_regla, prioridad in (
        ("peligro", "R-RIESGO-07", 79),
        ("alto", "R-RIESGO-02", 75),
        ("alerta", "R-RIESGO-03", 55),
    ):
        condiciones = tuple(Condicion(f"nivel_{gas}", "=", nivel) for gas in gases)
        reglas.append(Regla(id_regla, prioridad, condiciones, "nivel_riesgo", nivel, alguna=True))

    costos = configuracion["multiplicadores"]
    reglas.extend((
        Regla("R-RIESGO-05", 65, (Condicion("nivel_riesgo", "=", "alto"),), "multiplicador", costos["alto"]),
        Regla("R-RIESGO-06", 60, (Condicion("nivel_riesgo", "=", "alerta"),), "multiplicador", costos["alerta"]),
        Regla("R-RIESGO-01", 90, (Condicion("nivel_riesgo", "=", "peligro"),), "cerrado", True),
        Regla("R-RUTA-01", 95, (Condicion("cerrado", "=", True),), "transitable", False),
    ))
    return tuple(reglas)


def estados_linea_base(
    iniciales: tuple[Hecho, ...], inferidos: tuple[Hecho, ...], configuracion: dict
) -> tuple[Hecho, ...]:
    """Filtra lecturas críticas y conserva el nivel inferido solo para medir riesgo."""
    criterios = {
        gas["atributo"]: condicion_gas(gas, "peligro")
        for gas in configuracion["gases"].values()
    }
    lecturas = {(h.entidad, h.atributo): h.valor for h in iniciales}
    estados = [
        Hecho(entidad, atributo, valor)
        for (entidad, atributo), valor in lecturas.items()
        if atributo in ("cerrado", "transitable")
    ]
    estados.extend(
        Hecho(entidad, "cerrado", True)
        for (entidad, atributo), valor in lecturas.items()
        if atributo in criterios and criterios[atributo].cumple(valor)
    )
    estados.extend(h for h in inferidos if h.atributo == "nivel_riesgo")
    return tuple(estados)
