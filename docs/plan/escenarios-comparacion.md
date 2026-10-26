# Sprint 2 — Escenarios reproducibles y línea base

[← Índice](../../README.md)

Este bloque implementa S2-H06 y S2-H09 y amplía la consola S2-H08. Cada escenario define una instantánea de hechos y las ubicaciones de mineros identificados. Ambos enfoques reciben la misma mina, hechos originales, ubicaciones y destinos.

**Avance posterior:** la [ampliación de ambiente](gases-ventilacion.md) añade gases, ventilación y un cuarto escenario ANFO, con la misma cobertura en la línea base. Las cifras de 262 pruebas corresponden a la sesión inicial.

El [punto de control de Nivel 1](nivel1-verificacion.md) añade otros tres escenarios sobre una mina de 16 nodos. El campo opcional relaciones apunta a conocimiento dirigido entre túneles, se resuelve respecto al escenario y no se admite como lectura inyectada. --explicar TUNEL puede usarse con cualquier escenario para consultar las justificaciones directas de efectos de ruta.

## Ejecutar los tres casos

Con Python 3.12 y el entorno virtual activado, desde la raíz del repositorio:

```bash
python -m pip install -e . -r requirements-dev.txt
python -m mina_experta --escenario data/escenarios/co_moderado.json
python -m mina_experta --escenario data/escenarios/incendio_alternativa.json
python -m mina_experta --escenario data/escenarios/derrumbe_aislamiento.json
python -m pytest -q
```

Los escenarios comparan siempre ambos enfoques. Para entradas manuales se puede añadir `--comparar`, por ejemplo `python -m mina_experta --desde n5 --co tunel_2_3=30 --comparar`.

## Resultados comprobados

Todos los casos incluyen a Ana en n5 y Luis en n7, con destino n1.

| Escenario | Sistema experto: Ana / Luis | Línea base: Ana / Luis |
|---|---|---|
| CO moderado (30 ppm en tunel_2_3) | 470 m, costo 570 / 540 m, costo 640 | Sin ruta / Sin ruta |
| Incendio en tunel_3_4 | Desvío de 710 m / 540 m | 710 m / 540 m |
| Derrumbe en tunel_4_5 | Sin ruta / 540 m | Sin ruta / 540 m |

El resultado SIN RUTA es válido y termina con código 0. No significa que el sistema haya decidido esperar brigada o refugiarse; esas decisiones aún no están implementadas. Un escenario inválido termina con código 2.

## Qué hace la línea base

[linea_base.py](../../src/mina_experta/linea_base.py) aplica directamente el filtro a los datos originales: cierra si `co_ppm > alerta`, usando el valor configurable que parte de 25 ppm, o si hay incendio o derrumbe reportado. Después usa el mismo Dijkstra propio con las longitudes físicas de los túneles restantes. No utiliza el motor, sus conclusiones ni sus factores de riesgo. El umbral exacto no cierra el túnel: se usa `>` estricto.

Se implementa así D06 para el subconjunto de sensores actualmente disponible (CO). Al añadir otros sensores deberá ampliarse el filtro correspondiente. La decisión de cerrar al exceder un límite ocupacional es una **política de comparación académica**, no una exigencia normativa de cierre instantáneo.

La comparación no usa un Dijkstra ciego ni deshabilita los eventos para favorecer al sistema experto. Sin embargo, todavía no prueba que el sistema experto sea superior: en el caso de CO moderado la diferencia se debe a políticas distintas (penalizar frente a cerrar), no a conocimiento de un peligro en túneles vecinos. Falta un escenario que demuestre ese aporte del razonamiento según el enfoque del proyecto.

Los costos no son comparables directamente como métricas de calidad: el sistema usa metros ponderados por riesgo, mientras la línea base minimiza metros físicos tras el filtro. Se muestran ambas distancias y costos sin afirmar una mejora porcentual ni inventar exposición al riesgo o tiempos.

## Contrato del archivo de escenario, versión 1

Todos los campos de la tabla son obligatorios. No se admiten campos extra ni claves JSON repetidas.

| Campo | Contenido |
|---|---|
| `version` | Entero 1 |
| `nombre` | Texto no vacío |
| `mina` | Ruta al JSON de mina |
| `umbrales` | Ruta al JSON de umbrales |
| `costos` | Ruta al JSON de factores |
| `mineros` | Lista no vacía de objetos con `id` único y `nodo` existente |
| `destinos` | Lista no vacía de identificadores existentes, sin repetición |
| `hechos` | Lista de objetos con `entidad`, `atributo`, `valor`; puede estar vacía |

Las tres rutas de archivo se interpretan respecto al directorio del escenario, no al directorio desde el que se ejecuta Python. Pasar una ruta absoluta a `--escenario` permite ejecutarlo desde otro directorio con el paquete instalado.

Las entidades deben ser túneles existentes. Además de CO y eventos, se admiten no2_ppm, co2_ppm, h2s_ppm, o2_porcentaje, aire_m_min y uso_anfo con configuración de ambiente. El campo opcional ambiente apunta a un archivo relativo al escenario, como las otras rutas. Las mediciones son finitas y no negativas (O₂ hasta 100 %); eventos y ANFO son booleanos. El aire requiere contexto de ANFO por túnel. No se permite inyectar inferencias como cerrado o multiplicador ni repetir un atributo y entidad. Dos mineros distintos pueden compartir nodo.

`--escenario` no se mezcla con archivos u observaciones manuales, orígenes o destinos manuales: el programa rechaza esa combinación para que el experimento conserve sus datos definidos. `--comparar` sí se permite, aunque en escenarios ya está activado.

## Validación y límites del avance

Pasaron **262 pruebas**. Las nuevas pruebas comprueban fronteras del filtro, independencia del motor, datos inválidos, ubicación de mineros, duplicados, protección frente a conclusiones inyectadas, mezcla de entradas y los tres escenarios con salida real por consola desde un directorio temporal.

Los tres archivos ejecutan el flujo actual de punta a punta sobre la mina de ocho nodos y las siete reglas disponibles. No completan por sí solos el Nivel 1: siguen pendientes ampliar a al menos 15 reglas, otros gases y ventilación, la mina de 15–20 nodos y el caso que demuestre el aporte del encadenamiento sobre riesgos vecinos. Los factores de certeza, A* y decisiones de Nivel 2 continúan fuera de esta entrega.
