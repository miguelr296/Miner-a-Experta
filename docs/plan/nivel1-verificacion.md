# Nivel 1 — Mina ampliada y evidencia de encadenamiento

[← Índice](../../README.md)

Este punto de control reúne los criterios funcionales de Nivel 1 sobre [mina_nivel1.json](../../data/mina_nivel1.json): **16 nodos, 20 túneles, dos niveles subterráneos**, dos salidas, tres refugios y cuatro frentes. La mina pequeña de S1-09 se conserva para ejercicios y regresiones. No se modificaron sus ocho nodos.

## Ejecutar el punto de control

Con el entorno virtual activado, desde la raíz del repositorio:

```bash
python -m pip install -e . -r requirements-dev.txt
python -m mina_experta --escenario data/escenarios/nivel1_gases.json
python -m mina_experta --escenario data/escenarios/nivel1_derrumbe.json
python -m mina_experta --escenario data/escenarios/nivel1_riesgo_vecino.json --explicar tunel_10_12
python -m pytest -q
```

Todos los escenarios calculan rutas para Ana y Luis, comparan con el filtro directo y muestran la traza. Las rutas de datos son relativas al escenario; el comando también funciona desde otro directorio pasando una ruta absoluta al archivo.

## Mina base y refugios

Se conservan las cotas subterráneas de −50 y −100 m; las salidas n1 y n11 están en superficie. El cargador comprueba referencias, longitudes, conectividad y D10. Las distancias mínimas a algún refugio en el estado base son:

| Frente | Refugio | Distancia |
|---|---|---|
| n5 | n4 | 150 m |
| n7 | n4 | 220 m |
| n13 | n15 | 60 m |
| n16 | n15 | 100 m |

Cada recorrido es menor o igual a 500 m. Esta garantía se refiere al diseño base, no a que una emergencia preserve esos caminos.

## Relación explícita de humo

[relaciones_humo.json](../../data/configuracion/relaciones_humo.json) define versión 1 y una lista flujo_humo de pares origen/destino. Su único par indica que un incendio en tunel_12_14 puede exponer tunel_10_12. Los túneles deben existir, ser distintos y compartir un nodo; no se admiten pares repetidos. Compartir un cruce por sí solo **no crea** esta relación ni demuestra circulación real de humo.

La dirección procede de conocimiento declarado para la simulación, no se deduce del grafo de tránsito ni del orden origen/destino de una arista bidireccional. Es un SUPUESTO académico de exposición de un salto, no una simulación de fluidos ni una garantía física. Exposición por humo no convierte al vecino en un nuevo foco, por lo que no se propaga indefinidamente.

La configuración se incorpora como hechos estructurales recibe_humo_de. El escenario no puede inyectar esos hechos ni conclusiones como expuesto_humo o cerrado en sus lecturas. La línea base recibe y valida también la relación, pero su definición de filtro local no infiere con ella.

## Cadena y control del experimento

El escenario de riesgo vecino tiene un incendio reportado en tunel_12_14 y CO normal de 10 ppm en tunel_10_12. Ambos enfoques cierran el foco y no detectan un exceso local de CO en el vecino.

1. **R04:** el incendio produce foco_incendio y cierra el túnel de origen.
2. **R24:** combina ese foco con la relación dirigida y concluye expuesto_humo en el destino.
3. **R25:** la exposición deducida produce el cierre del vecino.

R24 se instancia por relación con un identificador como R24_tunel_12_14__tunel_10_12. Esto distingue sus disparos sin copiar una regla conceptual distinta en el catálogo por cada par. El motor mantiene 25 tipos de regla y, en esta configuración de un par, 25 instancias.

| Enfoque | Recorrido de Ana hacia n11 | Distancia |
|---|---|---|
| Filtro local | n13 → n12 → n10 → n9 → n11, atraviesa tunel_10_12 | 420 m |
| Motor con vecindad | n13 → n15 → n6 → n10 → n9 → n11 | 500 m |
| Control sin R24/R25, manteniendo las reglas locales y datos | Igual al filtro local | 420 m |

El control distingue este caso de las diferencias de política entre penalizar y cerrar un gas moderado: aquí solo cambia la inferencia vecina. Se prueba además que invertir la relación o retirar el incendio impide esa deducción.

Esto demuestra que el motor evita **el riesgo definido por el propio modelo** que el filtro local no representa. No demuestra seguridad real, superioridad universal ni una tasa de supervivencia. No se presentan el aumento de longitud ni los costos como una métrica real de exposición.

## Explicación y diseño del motor

Las condiciones siguen siendo locales salvo que nombren explícitamente una entidad. R24 fija la entidad de destino de la regla y la de origen de la condición de foco; la condición estructural se evalúa en el destino. La traza conserva ambos hechos concretos y la refracción los incluye en la identidad del disparo.

`--explicar TUNEL` muestra las justificaciones directas de sus cierres y factores, además de la traza completa. Por ejemplo, R25 explica el cierre por expuesto_humo; el paso R24 anterior muestra el foco y la relación que originaron esa exposición. No se ha añadido una explicación recursiva automática de Nivel 2.

## Estado del punto de control

| Criterio funcional de Nivel 1 | Evidencia |
|---|---|
| Mina de 15–20 nodos y dos niveles | Archivo real con 16 nodos y cotas −50/−100 m |
| Al menos 15 reglas, categorías DIAG/RIESGO/RUTA | 25 tipos de regla documentados, incluidos gases, aire y eventos |
| Prioridad, refracción y cadena de 3 pasos | Motor y pruebas de la cadena de humo y de gases |
| Dijkstra con costos y cierres dinámicos | Rutas comprobadas sin bibliotecas de grafos |
| Varios mineros y tres escenarios completos | Dos mineros en cada escenario de Nivel 1 |
| Explicación directa y comparación filtrada | Traza, --explicar y control de inferencia |
| Refugios a hasta 500 m por recorrido | Cargador estricto y distancias de la tabla |

Pasaron **322 pruebas**, incluidas las regresiones de los entregables previos y la ejecución de los tres escenarios de Nivel 1 desde otro directorio. Los criterios técnicos se han ejercitado en los casos indicados; no se declara terminada una revisión académica, medida de horas, publicación en main o cierre de semana. Las capacidades de Nivel 2 (certeza, A*, decisiones y explicación recursiva) siguen pendientes.
