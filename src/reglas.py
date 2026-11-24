"""Catálogo de diagnóstico, riesgo y efectos sobre los tramos."""

from .mina import Mina
from .motor import Condicion, Hecho, Regla


EVENTOS_BLOQUEANTES = {"incendio", "derrumbe", "inundacion"}
EVENTOS_VECINOS = {"incendio", "derrumbe"}


def preparar_hechos(iniciales: tuple[Hecho, ...], mina: Mina | None) -> tuple[Hecho, ...]:
    """Añade el respaldo por defecto y deriva los reportes de tramos adyacentes."""
    memoria = {(h.entidad, h.atributo): h.valor for h in iniciales}
    for (entidad, atributo), valor in tuple(memoria.items()):
        if atributo == "corte_electrico" and valor is True:
            memoria.setdefault((entidad, "ventilacion_respaldo"), False)

    if mina is not None:
        eventos = {
            entidad for (entidad, atributo), valor in memoria.items()
            if atributo in EVENTOS_VECINOS and valor is True
        }
        for nodo in mina.nodos:
            aristas = mina.vecinos(nodo)
            activas = {a.id for a in aristas if a.id in eventos}
            for arista in aristas:
                if activas.difference((arista.id,)):
                    memoria[arista.id, "vecino_evento"] = True

    return tuple(Hecho(entidad, atributo, valor) for (entidad, atributo), valor in memoria.items())


def diagnosticos_de_infraestructura(configuracion: dict) -> tuple[Regla, ...]:
    ventilacion = configuracion["ventilacion"]
    minimo = ventilacion["minimo"]
    minimo_anfo = ventilacion["minimo_anfo"]
    return (
        Regla("R-VEN-01", 35, (Condicion("vel_m_min", "<", minimo),),
              "nivel_ventilacion", "insuficiente", "NORMA"),
        Regla("R-VEN-02", 60, (Condicion("anfo", "=", True),
                              Condicion("vel_m_min", "<", minimo_anfo)),
              "nivel_ventilacion", "critica", "NORMA"),
        Regla("R-VEN-03", 30, (Condicion("vel_m_min", ">=", minimo),),
              "nivel_ventilacion", "conforme", "NORMA"),
        Regla("R-VEN-04", 61, (Condicion("corte_electrico", "=", True),
                              Condicion("ventilacion_respaldo", "=", False)),
              "nivel_ventilacion", "critica"),
        Regla("R-FUE-01", 80, (Condicion("incendio", "=", True),), "nivel_riesgo", "peligro", "NORMA"),
        Regla("R-DER-01", 85, (Condicion("derrumbe", "=", True),), "cerrado", True, "NORMA"),
        Regla("R-INU-01", 82, (Condicion("inundacion", "=", True),), "nivel_riesgo", "peligro"),
    )


def condicion_gas(configuracion: dict, nivel: str) -> Condicion:
    return Condicion(configuracion["atributo"], configuracion["operador"], configuracion[nivel])


def reglas_del_motor(configuracion: dict) -> tuple[Regla, ...]:
    gases = configuracion["gases"]
    reglas = list(diagnosticos_de_infraestructura(configuracion))
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

    indicadores = {
        "alto": (Condicion("nivel_ventilacion", "=", "critica"),),
        "alerta": (Condicion("nivel_ventilacion", "=", "insuficiente"),
                   Condicion("propagacion", "=", True)),
    }
    for nivel, id_regla, prioridad in (
        ("peligro", "R-RIESGO-07", 79),
        ("alto", "R-RIESGO-02", 75),
        ("alerta", "R-RIESGO-03", 55),
    ):
        condiciones = tuple(Condicion(f"nivel_{gas}", "=", nivel) for gas in gases)
        reglas.append(Regla(id_regla, prioridad, condiciones + indicadores.get(nivel, ()), "nivel_riesgo", nivel, alguna=True))

    costos = configuracion["multiplicadores"]
    reglas.extend((
        Regla("R-RIESGO-04", 54, (Condicion("vecino_evento", "=", True),), "propagacion", True),
        Regla("R-RUTA-02", 50, (Condicion("multiplicador", ">", 1),), "costo_dinamico", True),
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
        if ((atributo in criterios and criterios[atributo].cumple(valor))
            or (atributo in EVENTOS_BLOQUEANTES and valor is True))
    )
    estados.extend(h for h in inferidos if h.atributo == "nivel_riesgo")
    return tuple(estados)
