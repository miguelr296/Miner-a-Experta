"""Filtro directo sobre datos de entrada, sin usar el motor ni sus conclusiones."""

from types import MappingProxyType

from .escenarios import validar_lecturas
from .modelo import _validar_numero
from .relaciones import validar_relaciones


def costos_linea_base(mina, hechos, limite_co, ambiente=None, relaciones=()):
    # Mismo conocimiento de relaciones disponible; el filtro local no infiere con él.
    validar_relaciones(mina, relaciones)
    _validar_numero(limite_co, "limite_co")
    if limite_co <= 0:
        raise ValueError("El límite de CO debe ser positivo")
    lecturas = validar_lecturas(mina, hechos)
    cerrados = set()
    for entidad, atributo, valor in lecturas:
        if ((atributo == "co_ppm" and valor > limite_co)
                or (atributo in ("incendio_reportado", "derrumbe_reportado") and valor is True)):
            cerrados.add(entidad)
        if atributo in ("no2_ppm", "co2_ppm", "h2s_ppm", "o2_porcentaje", "aire_m_min"):
            if ambiente is None:
                raise ValueError("Se requiere configuración ambiente para estos sensores")
            if atributo in ("no2_ppm", "co2_ppm", "h2s_ppm"):
                fuera = valor > ambiente["gases"][atributo]["alerta"]
            elif atributo == "o2_porcentaje":
                limite = ambiente["gases"][atributo]
                fuera = valor < limite["alerta"] or valor > limite["maximo"]
            else:
                usa_anfo = next(v for e, a, v in lecturas if e == entidad and a == "uso_anfo")
                ventilacion = ambiente["ventilacion"]
                minimo = ventilacion["minimo_anfo" if usa_anfo else "minimo"]
                fuera = valor < minimo or valor > ventilacion["maximo"]
            if fuera:
                cerrados.add(entidad)
    return MappingProxyType({id: None if id in cerrados else a.longitud_m
                             for id, a in mina.aristas.items()})
