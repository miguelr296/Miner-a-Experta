# Sprint 1 — Cargador y motor mínimo

[← Índice](../../README.md)

Este entregable reúne el cargador S1-11, el diseño S1-12 y el motor de S1-13/S1-14, con comprobaciones de S1-15/S1-16. Se avanzó por dependencias bajo autorización del usuario. El aprendizaje individual, el registro de horas y la revisión de cierre de S1-18 no se dan por completados automáticamente.

**Evolución posterior:** la [integración de rutas del sprint 2](rutas-costos.md) añade R06/R07 y `--desde`. Los resultados de 195 pruebas que se describen aquí son el registro del entregable anterior; la consola actual tiene más reglas y pruebas.

## Ejecutar de principio a fin

Desde la raíz del repositorio, con Python 3.12 y el entorno virtual activado:

```bash
python -m pip install -e . -r requirements-dev.txt
python -m mina_experta --co tunel_1_2=120 --co tunel_2_3=20
python -m pytest -q
```

La consola carga la mina real (8 nodos y 8 túneles) y encadena R01 → R02 → R03 para `tunel_1_2`. En el entregable original fueron tres disparos; la versión actual añade R06/R07 y muestra cinco. `tunel_2_3` no activa reglas con 20 ppm. El cierre es un hecho derivado, no una modificación del objeto `Arista`. Sin `--desde` no se solicitan rutas.

Validación de esta sesión: **195 pruebas aprobadas**, comprobación de dependencias sin incompatibilidades y ejecución real de la consola. También se construyó una distribución del paquete, se instaló en un entorno virtual limpio sin dependencias externas de ejecución y se probó fuera del checkout pasando rutas absolutas de la mina y los umbrales. La práctica de pytest con fallo deliberado que se describe abajo fue independiente de esas 195 pruebas.

Las rutas de archivos por defecto son relativas al directorio actual. Puedes cambiarlas con `--mina` y `--umbrales`. `--co` acepta una lectura finita no negativa por túnel y ejecución. No pasar lecturas produce cero disparos: ausencia de datos no equivale a afirmar que la mina sea segura. Un error de archivo, dato o configuración termina con código 2, sin presentar un resultado válido.

## S1-11 — Carga estricta

`cargar_mina(ruta)` en [cargador.py](../../src/mina_experta/cargador.py) devuelve objetos `Mina`, `Nodo` y `Arista`. Rechaza JSON mal formado, claves duplicadas, constantes no estándar, versiones incompatibles y campos inesperados. No depende de `jsonschema` en ejecución: las comprobaciones de campos se implementan con biblioteca estándar y el modelo comprueba los valores.

Después valida los tipos requeridos, la conectividad y D10 mediante una búsqueda propia por distancia desde todos los refugios, limitada a 500 m. Este recorrido sirve para aceptar la mina base; aún no constituye el planificador de evacuación con costos dinámicos. Se comprueban exactamente 500 m, un valor superior, rutas alternativas y más de un refugio.

Los errores se convierten en `ErrorCarga`, una subclase de `ValueError`, conservando la causa. En S1-16 se comprueban archivos reales válidos y erróneos, sin sustituirlos por objetos simulados.

## S1-12 — Hechos y reglas

En [motor.py](../../src/mina_experta/motor.py), `Hecho` es una tupla `(entidad, atributo, valor)`. Los valores son escalares JSON finitos. Los booleanos se distinguen de las mediciones numéricas: `True` no satisface una comparación numérica ni equivale al hecho con valor `1`.

`Condicion` declara atributo, operador (`eq`, `gt`, `ge`, `lt`, `le`) y valor. `Regla` declara identificador, condiciones, conclusiones y prioridad. Las conclusiones añaden atributos a la misma entidad. Todas las condiciones de un disparo deben tener soporte en esa entidad; no se cruzan accidentalmente lecturas de túneles distintos.

Esta versión no une hechos de entidades vecinas, no elimina hechos y no resuelve contradicciones entre mediciones temporales. La consola exige una lectura por túnel; cada ejecución usa una instantánea nueva. Las conclusiones booleanas de la cadena de CO son acumulativas: un túnel de peligro inmediato conserva también los hechos que justificaron las etapas anteriores. No son etiquetas mutuamente excluyentes.

## S1-13/S1-14 — Aplicación y ciclo

`Motor.aplicables(hechos)` construye los disparos con sus antecedentes concretos. `Motor.ejecutar(hechos)` selecciona uno, añade las conclusiones y vuelve a buscar. La prioridad mayor gana; en empate se usa el identificador de regla y después la entidad en orden alfabético. Las combinaciones de antecedentes conservan su orden de entrada.

```text
validar y deduplicar los hechos iniciales
crear memoria, registro de disparos y traza vacíos para esta ejecución
repetir:
    buscar condiciones satisfechas dentro de cada entidad
    ordenar por prioridad descendente, identificador y entidad
    excluir (regla, entidad, antecedentes) ya disparados
    si no quedan disparos: devolver hechos y traza completos
    si se alcanzó el límite: fallar indicando ejecución incompleta
    añadir conclusiones sin duplicarlas y registrar la justificación
```

La refracción registra regla, entidad y hechos de soporte, por lo que una regla puede actuar en dos túneles distintos. Que su conclusión ya exista no obliga a dispararla para siempre. La traza registra también disparos sin hechos nuevos. El límite por defecto es de 10 000 disparos; alcanzarlo con trabajo pendiente genera un error, nunca un resultado parcial presentado como completo.

`Resultado.por_que(hecho)` devuelve los pasos que concluyeron ese hecho con sus antecedentes. Es una explicación directa de la traza; la reconstrucción recursiva de «cómo» del Nivel 2 sigue pendiente.

## S1-06 — Comprobar pytest

Se ejecutó una práctica aislada en un archivo temporal: una prueba con `assert 2 + 2 == 4` y otra con `assert 2 + 2 == 5`. El resultado fue **1 aprobada y 1 fallida deliberadamente**, con código de salida 1. El archivo se eliminó al terminar. No forma parte de la suite habitual ni se ocultó el fallo mediante una marca de omisión.

Para la suite del repositorio usa `python -m pytest -v` y revisa los nombres y el resumen. Un resultado sin pruebas no acredita funcionamiento. La práctica técnica no sustituye que el integrante escriba y comprenda sus propias pruebas.

## Alcance y siguientes pasos

También se cubrió el borrador de cinco reglas de S1-17, con implementación y pruebas para R04/R05: incendio y derrumbe reportados cierran exclusivamente el túnel afectado. Se pueden probar con `python -m mina_experta --incendio tunel_3_4 --derrumbe tunel_4_5`. Ambas reglas tienen prioridad 100, por delante de los escalones de CO. Si varias reglas concluyen el mismo cierre, se conserva una sola copia del hecho y todas sus justificaciones. No se modela propagación a vecinos ni se deduce seguridad por ausencia de reportes.

Las tres reglas de CO están en el [catálogo](../reglas.md) y sus umbrales en [umbrales.json](../../data/configuracion/umbrales.json). La fuente ocupacional del valor 25 ppm no convierte la clasificación instantánea en una evaluación normativa: la política de emergencia es un supuesto académico.

Se mantiene pendiente el resto de gases, ventilación, costos dinámicos, rutas por minero y comparación con la línea base. Las 15 reglas, los 3 escenarios y la mina ampliada de Nivel 1 todavía no están terminados. Antes de ampliar el alcance corresponde revisar el entregable y la bitácora; la revisión de cierre S1-18 sigue pendiente en lo relativo a horas reales, aprendizaje y cierre semanal. No se crearon tags semanales ni se cerraron tarjetas automáticamente.
