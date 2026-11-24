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

La demo carga los hechos y las ubicaciones de [co_demo.json](data/escenarios/co_demo.json), el umbral de [umbrales.json](data/umbrales.json) y la topología de [mina_prueba.json](data/mina_prueba.json). Puedes pasar otro archivo de escenario con el mismo formato y una topología compatible:

```text
python -m src data/escenarios/co_demo.json --mina data/mina_prueba.json
```

La traza muestra las premisas, la regla, su prioridad, la fuente y el hecho que se escribe. El motor vuelve a evaluar las reglas cuando aparece un hecho nuevo y procesa cada par regla–entidad una vez por ejecución.

| Regla de la demo | Condición | Conclusión | Prioridad |
|---|---|---|---|
| `R-CO-03` | CO por encima del umbral simulado | Gas en peligro | 50 |
| `R-RIESGO-07` | CO en peligro | Túnel en peligro | 79 |
| `R-RIESGO-01` | Túnel en peligro | Túnel cerrado | 90 |
| `R-RUTA-01` | Túnel cerrado | Tramo no transitable | 95 |

La cadena reproduce el ejemplo de cierre del prototipo web. Las cuatro reglas de la demo están etiquetadas como `SUPUESTO`. Dijkstra usa los hechos de cierre y transitabilidad para excluir aristas. Puede aplicar un multiplicador de costo de al menos 1 definido en la memoria. Para cada minero, la consola busca primero una salida y, si ninguna es alcanzable, un refugio. En la demo, el cierre obliga a m1 a pasar por i3 y recorrer 265 m. Con el túnel abierto, recorrería 160 m.

La topología define nodos con identificador, coordenadas en metros, nivel y tipo. Cada arista bidireccional tiene identificador, nodo de origen, nodo de destino y longitud positiva. El escenario puede incluir una lista `mineros` con su `id` y `nodo`. Si se omite, la consola muestra únicamente la traza. Esta etapa cubre la cadena de CO en una mina de siete nodos. La línea base y los demás diagnósticos quedan para la siguiente iteración.

Para ejecutar las pruebas, con pytest instalado:

```text
python -m pytest
```
