# Sistema Experto para Emergencias y Evacuación en Minería Subterránea

Proyecto del curso **Sistemas Expertos**. Equipo: 2 integrantes. Lenguaje: Python.

Sistema que, ante una emergencia simulada en una mina metálica subterránea, **infiere el estado de riesgo** con un motor de reglas propio (forward chaining), **calcula rutas de evacuación** para varios mineros y **explica cada decisión**.

## Cómo leer este repositorio

Este README es la portada. La documentación se lee como un informe, en orden:

### Parte I — Plan
1. [Enfoque](docs/plan/enfoque.md)
2. [Alcance](docs/plan/alcance.md)
3. [Cronograma y reparto de trabajo](docs/plan/cronograma-y-reparto.md)
4. [Flujo de trabajo](docs/plan/flujo-de-trabajo.md)
5. [Sprints](docs/plan/sprints.md)
6. [Tablero Kanban](docs/plan/kanban.md)

### Parte II — Desarrollo (un capítulo por semana)
- [Semana 1](docs/capitulos/semana-01.md)
- *(se agrega un capítulo cada semana a partir de la [plantilla](docs/capitulos/_plantilla.md))*

### Anexos
- [Catálogo de reglas](docs/reglas.md)
- [Registro de decisiones](docs/decisiones.md)
- [Glosario de siglas y términos](docs/glosario.md)
- [Bitácora de sesiones](BITACORA.md)
- [Contexto vivo del proyecto](docs/contexto.md) *(interno)*

## Cronología del código

Cada semana cerrada se marca con un tag (`semana-01`, `semana-02`, …). Cada capítulo enlaza al tag de su semana, para ver el código exacto de ese momento.

## Estructura

```
mina-experta/
├── README.md            # portada e índice
├── BITACORA.md          # diario de sesiones
├── docs/
│   ├── plan/            # enfoque, alcance, cronograma, flujo, sprints, kanban
│   ├── capitulos/       # un capítulo por semana
│   ├── reglas.md        # catálogo de reglas con fuente y prueba
│   ├── decisiones.md    # decisiones de diseño y su porqué
│   └── glosario.md      # siglas y términos técnicos
├── data/escenarios/     # minas y emergencias en JSON
├── src/                 # código fuente
└── tests/               # pruebas pytest
```

## Ejecución

Desde la raíz del repositorio, ejecuta la primera demostración con Python 3.10 o posterior.

```text
python -m src
```

La demo carga los hechos y las ubicaciones de [co_demo.json](data/escenarios/co_demo.json), los umbrales de [umbrales.json](data/umbrales.json) y la topología de [mina_prueba.json](data/mina_prueba.json). Puedes pasar otro archivo de escenario con el mismo formato y una topología compatible:

```text
python -m src data/escenarios/co_demo.json --mina data/mina_prueba.json
```

La traza muestra las premisas, la regla, su prioridad, la fuente y la conclusión. El motor diagnostica CO, NO₂, CO₂, H₂S y O₂, agrega el nivel más grave por túnel y aplica los multiplicadores de costo del JSON. Los umbrales de peligro y los costos son supuestos de simulación. Para O₂, esta etapa reproduce el rango por deficiencia del prototipo web.

| Nivel inferido | Efecto en la ruta experta |
|---|---|
| Normal | Conserva la longitud como costo. |
| Alerta | Multiplica el costo por 2. |
| Alto | Multiplica el costo por 3. |
| Peligro | Dispara la cadena de cierre y excluye el tramo. |

Dijkstra calcula la ruta experta de menor costo ajustado, con el puntaje de riesgo como desempate. La línea base filtra las lecturas en peligro, los eventos de cierre físico y los cierres explícitos, y usa la longitud para elegir la salida. Ambos resultados se evalúan con la misma suma de niveles por tramo. La salida por consola busca un refugio para el resultado experto si ninguna salida es alcanzable.

Para ver un desvío por costo sin cierre:

```text
python -m src data/escenarios/desvio_riesgo.json
```

En ese caso, la línea base recorre 160 m con puntaje de riesgo 2. La ruta experta evita el tramo de riesgo alto, recorre 265 m y obtiene puntaje 0.

La topología define nodos con identificador, coordenadas en metros, nivel y tipo. Cada arista bidireccional tiene identificador, nodo de origen, nodo de destino y longitud positiva. El escenario puede incluir una lista `mineros` con su `id` y `nodo`. Si se omite, la consola muestra únicamente la traza. La demo usa una mina de siete nodos. Para ver la interacción entre inundación, corte eléctrico y respaldo de ventilación, ejecuta:

```text
python -m src data/escenarios/infraestructura_demo.json
```

| Reglas | Comportamiento del modelo |
|---|---|
| `R-VEN-01` y `R-VEN-03` | Clasifican la ventilación según la velocidad del aire y el mínimo configurado. |
| `R-VEN-02` | Con ANFO activo, usa el umbral específico y prevalece sobre la regla general. |
| `R-VEN-04` | Un corte sin respaldo operativo marca ventilación crítica y, mediante las reglas de riesgo, eleva el costo. |
| `R-FUE-01`, `R-DER-01` y `R-INU-01` | Los reportes de incendio, derrumbe e inundación cierran el tramo mediante la cadena de reglas correspondiente. |
| `R-RIESGO-04` | Los tramos que comparten un nodo con un incendio o derrumbe pueden quedar en alerta. |

Probamos las inferencias de los cinco casos del prototipo web con su topología. Coincidieron los estados, la ventilación, los costos y los bloqueos de línea base en los 105 pares de escenario y túnel. En el incendio, Python conserva el origen de mayor prioridad cuando otra regla propone la misma conclusión. Queda pendiente reproducir en Python las decisiones por minero y las rutas completas de los cinco casos.

Para ejecutar las pruebas, con pytest instalado:

```text
python -m pytest
```
