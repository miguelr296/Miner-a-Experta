"""Consola de mina, inferencia y rutas por costo dinámico."""

import argparse
from .ambiente import cargar_ambiente, reglas_ambiente
from .cargador import cargar_mina
from .conocimiento import cargar_umbrales_co, reglas_co, reglas_eventos, reglas_costos
from .escenarios import cargar_escenario, validar_lecturas
from .linea_base import costos_linea_base
from .motor import Motor
from .planificador import costos_desde_hechos, ruta_menor_costo
from .relaciones import cargar_relaciones, hechos_relaciones, reglas_vecindad


def _ruta_no_vacia(valor):
    if not valor.strip():
        raise argparse.ArgumentTypeError("La ruta no puede estar vacía")
    return valor


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mina", type=_ruta_no_vacia)
    parser.add_argument("--umbrales", type=_ruta_no_vacia)
    parser.add_argument("--costos", type=_ruta_no_vacia)
    parser.add_argument("--ambiente", type=_ruta_no_vacia)
    parser.add_argument("--relaciones", type=_ruta_no_vacia)
    parser.add_argument("--explicar", action="append", default=[], metavar="TUNEL",
                        help="Mostrar las justificaciones directas de sus cierres y penalizaciones")
    parser.add_argument("--escenario", type=_ruta_no_vacia, metavar="ARCHIVO")
    parser.add_argument("--comparar", action="store_true",
                        help="Mostrar también Dijkstra con filtro directo por umbral")
    parser.add_argument("--desde", action="append", default=[], metavar="NODO",
                        help="Origen de una ruta; repetir para más ubicaciones")
    parser.add_argument("--hasta", action="append", default=[], metavar="NODO",
                        help="Destinos permitidos; por defecto, todas las salidas")
    parser.add_argument("--co", action="append", default=[], metavar="TUNEL=PPM",
                        help="Lectura simulada; repetir para túneles distintos")
    parser.add_argument("--incendio", action="append", default=[], metavar="TUNEL")
    parser.add_argument("--derrumbe", action="append", default=[], metavar="TUNEL")
    for opcion in ("no2", "co2", "h2s", "o2", "aire"):
        parser.add_argument(f"--{opcion}", action="append", default=[], metavar="TUNEL=VALOR")
    parser.add_argument("--anfo", action="append", default=[], metavar="TUNEL")
    parser.add_argument("--sin-anfo", action="append", default=[], metavar="TUNEL")
    args = parser.parse_args()
    try:
        escenario = None
        if args.escenario:
            if (args.desde or args.hasta or args.co or args.incendio or args.derrumbe
                    or args.no2 or args.co2 or args.h2s or args.o2 or args.aire or args.anfo or args.sin_anfo
                    or any(v is not None for v in (args.mina, args.umbrales, args.costos, args.ambiente,
                                                   args.relaciones))):
                raise ValueError("--escenario no se mezcla con entradas manuales")
            escenario = cargar_escenario(args.escenario)
        mina = escenario.mina if escenario else cargar_mina(args.mina or "data/mina_prueba.json")
        umbrales = escenario.umbrales if escenario else args.umbrales or "data/configuracion/umbrales.json"
        config_costos = escenario.costos if escenario else args.costos or "data/configuracion/costos.json"
        config_ambiente = (escenario.ambiente if escenario
                           else args.ambiente or "data/configuracion/ambiente.json")
        ambiente = cargar_ambiente(config_ambiente) if config_ambiente else None
        archivo_relaciones = escenario.relaciones if escenario else args.relaciones
        relaciones = cargar_relaciones(archivo_relaciones, mina) if archivo_relaciones else ()
        hechos = []
        for atributo, lecturas in (("co_ppm", args.co), ("no2_ppm", args.no2),
            ("co2_ppm", args.co2), ("h2s_ppm", args.h2s),
            ("o2_porcentaje", args.o2), ("aire_m_min", args.aire)):
            for lectura in lecturas:
                entidad, texto = lectura.split("=", 1)
                hechos.append((entidad, atributo, float(texto)))
        for valor, entidades in ((True, args.anfo), (False, args.sin_anfo)):
            hechos.extend((entidad, "uso_anfo", valor) for entidad in entidades)
        for atributo, reportados in (("incendio_reportado", args.incendio),
                                     ("derrumbe_reportado", args.derrumbe)):
            for entidad in reportados:
                if entidad not in mina.aristas:
                    raise ValueError(f"Túnel desconocido: {entidad}")
                hechos.append((entidad, atributo, True))
        hechos = escenario.hechos if escenario else validar_lecturas(mina, hechos)
        if ambiente is None and any(a not in ("co_ppm", "incendio_reportado", "derrumbe_reportado")
                                    for _, a, _ in hechos):
            raise ValueError("El escenario requiere un archivo ambiente para estas lecturas")
        resultado = Motor((*reglas_co(umbrales), *reglas_eventos(),
                           *reglas_costos(config_costos),
                           *(reglas_ambiente(ambiente) if ambiente else ()),
                           *reglas_vecindad(relaciones))).ejecutar((*hechos, *hechos_relaciones(relaciones)))
        costos = costos_desde_hechos(mina, resultado)
        if any(entidad not in mina.aristas for entidad in args.explicar):
            raise ValueError("El túnel solicitado para explicar no existe")
        if args.hasta and not args.desde:
            raise ValueError("--hasta requiere al menos un origen --desde")
        origenes = ([(m.id, m.nodo) for m in escenario.mineros] if escenario
                    else [(None, origen) for origen in args.desde])
        destinos = escenario.destinos if escenario else args.hasta or None
        rutas = [(id, origen, ruta_menor_costo(mina, origen, destinos, costos))
                 for id, origen in origenes]
        rutas_base = []
        if args.comparar or escenario:
            base = costos_linea_base(mina, hechos, cargar_umbrales_co(umbrales)["alerta"], ambiente,
                                     relaciones)
            rutas_base = [(id, origen, ruta_menor_costo(mina, origen, destinos, base))
                          for id, origen in origenes]
    except (OSError, UnicodeError, ValueError, RuntimeError) as error:
        parser.exit(2, f"Error: {error}\n")
    print(f"Mina: {mina.nombre} ({len(mina.nodos)} nodos, {len(mina.aristas)} túneles)")
    print("Simulación académica: no es una evaluación operativa de seguridad.")
    if escenario:
        print(f"Escenario: {escenario.nombre}")
    for paso in resultado.traza:
        print(f"{paso.regla_id} [{paso.entidad}]: {paso.antecedentes} -> {paso.conclusiones}")
    print(f"Disparos: {len(resultado.traza)}")
    for entidad in args.explicar:
        print(f"Explicación de {entidad}:")
        pasos = [p for p in resultado.traza if p.entidad == entidad
                 and any(a in ("cerrado", "multiplicador") for _, a, _ in p.conclusiones)]
        if not pasos:
            print("  Sin efectos de ruta inferidos.")
        for paso in pasos:
            print(f"  {paso.regla_id}: {paso.antecedentes} -> {paso.conclusiones}")
    if not rutas:
        print("Sin origen --desde: no se calcularon rutas.")
    for etiqueta, recorridos in (("Ruta", rutas), ("Línea base", rutas_base)):
        for id, origen, ruta in recorridos:
            persona = f" [{id}]" if id is not None else ""
            if ruta is None:
                print(f"{etiqueta}{persona} desde {origen}: SIN RUTA a los destinos solicitados")
            else:
                print(f"{etiqueta}{persona} desde {origen}: {' -> '.join(ruta.nodos)}; "
                      f"distancia {ruta.distancia_m:g} m; costo {ruta.costo:g}")


if __name__ == "__main__":
    main()
