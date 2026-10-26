# Sprint 2 — Costos y rutas con Dijkstra

[← Índice](../../README.md)

Primera integración de las historias S2-H04 y S2-H05: hechos → costos/cierres → ruta. Se apoya en el cargador y motor comprobados del sprint 1. No declara completado el sprint 2: siguen pendientes ampliar las reglas, los escenarios JSON y la línea base con filtro por umbral.

**Avance posterior:** ya se añadieron los [tres escenarios y la línea base](escenarios-comparacion.md). Los resultados de 225 pruebas registrados aquí corresponden a la sesión de integración de rutas.

## Prueba por consola

Con el entorno virtual activado, desde la raíz del repositorio:

```bash
python -m pip install -e . -r requirements-dev.txt
python -m mina_experta --desde n5
python -m mina_experta --desde n5 --co tunel_3_4=120
python -m mina_experta --desde n5 --derrumbe tunel_4_5
python -m pytest -q
```

| Caso | Resultado esperado |
|---|---|
| Sin eventos ni mediciones | `n5 → n4 → n3 → n2 → n1`, 470 m, costo 470 |
| CO de 120 ppm en tunel_3_4 | `n5 → n4 → n8 → n6 → n3 → n2 → n1`, 710 m, costo 710 |
| Derrumbe en tunel_4_5 | `SIN RUTA`, porque n5 queda aislado |

Son resultados bajo los datos y supuestos simulados; el primer caso no demuestra seguridad por ausencia de mediciones. El caso sin ruta es un resultado calculado válido (código de salida 0), distinto de un archivo o argumento inválido (código 2).

Se puede repetir `--desde` para calcular desde varias ubicaciones. Por defecto se elige la salida alcanzable de menor costo. `--hasta n4` permite solicitar explícitamente el refugio. Si se repite `--hasta`, se elige el destino de menor costo entre los indicados. No se decide automáticamente entre evacuar, refugiarse o esperar brigada; esa política pertenece a Nivel 2. Las ubicaciones aún no son registros de mineros con identidad en archivos de escenario.

## De hechos a costos

R06 y R07 concluyen multiplicadores para alerta y riesgo alto por CO. Se leen de [costos.json](../../data/configuracion/costos.json), inicialmente 2 y 3. Todos son supuestos del proyecto, no valores normativos.

`costos_desde_hechos(mina, resultado)` en [planificador.py](../../src/mina_experta/planificador.py) produce una colección de solo lectura con un costo por túnel. Usa la longitud base multiplicada por el **mayor** factor inferido. No multiplica entre sí los escalones de riesgo que describen el mismo fenómeno. Un hecho `cerrado=True` domina a cualquier factor y se representa internamente con `None`, por lo que el túnel se excluye del recorrido en ambos sentidos. `cerrado=False` no deshace un cierre durante la misma ejecución.

Se rechazan factores menores que 1, costos no finitos, booleanos como números y referencias a túneles desconocidos. Cada ejecución vuelve a calcular los costos desde la geometría original y sus hechos; no acumula penalizaciones ni conserva cierres de otra ejecución. El mapa de costos no altera los objetos `Arista`.

## Algoritmo propio

`ruta_menor_costo` usa `heapq` como cola de prioridad; no usa una biblioteca de grafos. Mantiene el mejor costo conocido de cada nodo y el túnel que lo precede. Descarta entradas antiguas de la cola, omite túneles cerrados y termina cuando extrae el primer destino con costo mínimo. Para empates en la cola se usa el identificador del nodo; si dos caminos dan exactamente el mismo costo, se conserva el primero descubierto.

Devuelve una `Ruta` inmutable con nodos, aristas, distancia física y costo. Origen igual a destino produce distancia y costo cero. Si no hay destino alcanzable, devuelve `None`. Los destinos inexistentes o una lista vacía generan `ValueError`.

La distancia se mide en metros. El costo son metros ponderados por riesgo: **no es tiempo de evacuación ni probabilidad de supervivencia**. Se comprueba que ningún peso sea inferior a la longitud física (D01). La búsqueda no implementa todavía A*.

## Evidencia y revisión técnica

La suite completa tiene **225 pruebas aprobadas**. Comprueba caminos con menos aristas pero más costo, cambios de ruta por penalización, cierres bidireccionales, varios destinos, origen igual a destino, ausencia de ruta, independencia entre ejecuciones y errores. La integración usa el JSON real de la mina, las reglas y la consola ejecutada en otro proceso.

Como revisión de transición desde el sprint 1: el motor y el cargador ya tienen pruebas reproducibles; las estimaciones y horas reales siguen sin medirse, por lo que no se inventa velocidad del equipo ni se cierra automáticamente un sprint calendario. Es posible hacer una retrospectiva de aprendizaje aparte sin bloquear este desarrollo técnico.

El siguiente bloque pendiente es la línea base con filtro por umbral y los escenarios JSON reproducibles. El alcance completo de Nivel 1 también exige al menos 15 reglas, otros gases, ventilación y ampliar la mina a 15–20 nodos. Las siete reglas actuales no completan esos objetivos.
