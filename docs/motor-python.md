# Informe de implementación y guion de demo en Python

[Volver al índice](../README.md)

## Alcance entregado

El programa carga la mina y los hechos iniciales desde JSON, infiere el estado de cada tramo y recomienda evacuar, refugiarse o esperar a la brigada. La consola muestra las premisas, las reglas aplicadas, los conflictos de ventilación y la ruta de línea base por minero.

| Componente | Responsabilidad |
|---|---|
| [motor.py](../src/motor.py) | Memoria de hechos, encadenamiento hacia adelante, prioridad, refracción, conflictos y certeza. |
| [reglas.py](../src/reglas.py) y [umbrales.json](../data/umbrales.json) | Diagnósticos de gases y ventilación, eventos de infraestructura, riesgo, cierres y costos. |
| [mina.py](../src/mina.py) y [planificador.py](../src/planificador.py) | Carga y validación del grafo, Dijkstra, A* y comparación con la línea base. |
| [decisiones.py](../src/decisiones.py) | Política simulada de evacuación, refugio o espera y su justificación. |
| [referencia_web.json](../data/referencia_web.json) | Topología esquemática, entradas y resultados esperados de los cinco escenarios web, tomados del commit `46114fb`. |

La línea base busca por distancia y respeta los cierres físicos y los umbrales de peligro. La ruta experta incorpora costos ajustados y desempata por puntaje de riesgo.

## D22 — Factores de certeza en la traza

Cada lectura puede llevar una `certeza` entre 0 y 1. Los factores por regla se configuran en `certeza_reglas` mediante su identificador. Un valor omitido equivale a 1. Para una conjunción se usa la menor certeza de las premisas. Para una disyunción se toma la premisa cumplida con mayor certeza. El resultado se multiplica por el factor de la regla. Los reportes de incendio o derrumbe transmiten su certeza a los tramos vecinos cuando se deriva el hecho de propagación.

La certeza expresa el respaldo declarado dentro del modelo. La prioridad sigue resolviendo conclusiones incompatibles. Una lectura con poca certeza muestra ese respaldo en la traza y el modelo conserva el cierre o costo que resulta de sus reglas. Se mantienen así la reproducibilidad de los casos y la visibilidad de la medición incierta durante la demo.

## D23 — Heurística física para A*

La heurística es la menor distancia euclidiana 3D desde el nodo actual hasta los destinos candidatos. Se comprueba que todos los nodos tengan `x`, `y` y `z` en metros y que la longitud de cada arista cubra la distancia recta entre sus extremos. Como el costo de un tramo transitable es al menos su longitud, la estimación es una cota inferior. El algoritmo conserva el criterio de menor riesgo para rutas de igual costo.

Las coordenadas de los cinco casos web describen un plano esquemático. Dijkstra usa las longitudes declaradas de esos túneles. Para A* usamos la [mina de prueba](../data/mina_prueba.json), que tiene cotas físicas y longitudes coherentes. La consola cuenta los nodos procesados en la búsqueda de la ruta asignada, incluido el destino. Esa cifra excluye la preparación de la heurística y el cálculo de otras opciones.

## Guion para la revisión con Miguel

Ejecutar desde la raíz del repositorio con Python 3.10 o posterior.

| Paso | Comando | Qué mostrar |
|---|---|---|
| 1. Probar decisiones | `python -m src --caso-web ESC-03` | La consola muestra las tres decisiones. m1 espera a la brigada, m3 se refugia en r3 y los demás evacúan. |
| 2. Comparar certeza | `python -m src` y `python -m src data/escenarios/certeza_demo.json` | Comparar las líneas de `t_i2_f1`. La lectura de 101 ppm pasa de certeza 100 % a 45 %. El cierre se conserva, y el 45 % llega hasta `transitable=False`. |
| 3. Comparar buscadores | `python -m src data/escenarios/desvio_riesgo.json --comparar-algoritmos` | Ambos encuentran la ruta experta de costo 265 y puntaje de riesgo 0. Dijkstra procesa 7 nodos y A* 6. La línea base recorre 160 m y obtiene puntaje 2. |
| 4. Ejecutar regresión | `python -m pytest -q` | Las 41 pruebas cubren el motor, los cierres, los desacuerdos de ventilación, la certeza y A*. |

Las pruebas de referencia comprueban las 25 evaluaciones de mineros y los túneles afectados de los cinco escenarios. Las pruebas de A* comparan el costo y el riesgo con Dijkstra desde los siete nodos de la mina de prueba, para destinos únicos y múltiples, cierres, empates e inaccesibilidad. Los escenarios y recomendaciones pertenecen a una simulación académica.
