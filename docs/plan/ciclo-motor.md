# S1-07 — Entender el ciclo del motor

[← Índice](../../README.md)

Este recorrido desarrolla los conceptos del [glosario](../glosario.md) y del [enfoque](enfoque.md). Prepara el diseño de S1-12 y la implementación de S1-13/S1-14; todavía no implementa el motor ni añade reglas de minería.

## De los hechos a las conclusiones

Un hecho representa algo conocido mediante `(entidad, atributo, valor)`. El motor conserva los hechos en su memoria de trabajo. Una regla expresa condiciones y conclusiones: si las condiciones se cumplen, se puede disparar y añadir conocimiento.

El encadenamiento hacia adelante empieza en los hechos disponibles. La conclusión de una regla puede satisfacer las condiciones de otra. No se limita a revisar una lista una única vez: después de cada disparo vuelve a buscar reglas aplicables.

La prioridad solo ordena las reglas que ya son aplicables. Una regla con prioridad alta no se dispara si todavía faltan sus hechos. Según el glosario, un número mayor significa mayor prioridad. El desempate sigue pendiente del diseño del motor.

## Recorrido manual comprobable

Usaremos letras abstractas como hechos para centrarnos en la lógica. No son umbrales, reglas de seguridad ni propuestas para el catálogo de minería.

Memoria inicial: `{A}`.

| Regla de ejemplo | Condición | Conclusión | Prioridad |
|---|---|---|---|
| E1 | A | B | 30 |
| E2 | B | C | 20 |
| E3 | A | D | 10 |

Antes de leer la tabla siguiente, intenta predecir qué reglas se disparan y en qué orden.

| Paso | Aplicables sin repetir un disparo anterior | Elección | Memoria después |
|---|---|---|---|
| 1 | E1 y E3 | E1, por prioridad | `{A, B}` |
| 2 | E2 y E3 | E2, por prioridad | `{A, B, C}` |
| 3 | E3 | E3 | `{A, B, C, D}` |
| 4 | Ninguna | Terminar | `{A, B, C, D}` |

La traza esperada es `E1 → E2 → E3`. E2 no era aplicable al inicio; apareció gracias a B. Esta conclusión intermedia es lo que diferencia el encadenamiento de una colección de comprobaciones independientes.

## Refracción: por qué no repetir E1 para siempre

Después de disparar E1, A sigue presente. Si solo miráramos sus condiciones, E1 seguiría siendo aplicable y podría impedir que otras reglas avancen.

La refracción impide repetir el mismo disparo con los mismos hechos dentro de la ejecución. Guardar B sin duplicados ayuda a mantener la memoria, pero por sí solo no impide ejecutar E1 otra vez.

Tampoco debe interpretarse como prohibir para siempre una regla por su nombre: una misma regla puede necesitar aplicarse a entidades diferentes. Si se evalúan dos túneles, registrar solo el nombre de la regla podría omitir el segundo. El diseño de cómo identificar cada disparo corresponde a S1-12.

Una ejecución nueva con nuevos datos requiere definir qué memoria y registro de disparos se reinician. No asumimos todavía una simulación temporal ni la eliminación automática de hechos.

## Ciclo conceptual

```text
cargar hechos iniciales
preparar registro de disparos y traza de esta ejecución
repetir:
    buscar reglas cuyas condiciones estén satisfechas
    excluir los disparos ya realizados con los mismos hechos
    si no queda ninguna: terminar
    elegir una regla aplicable según prioridad
    dispararla y registrar sus conclusiones y los hechos que la justifican
    registrar el disparo para evitar su repetición
```

En el ejemplo se termina porque hay un número finito de conclusiones y cada disparo se realiza una vez. No es una demostración de terminación para cualquier sistema de reglas que pudiera generar hechos nuevos sin límite.

La traza debe permitir explicar qué regla produjo una conclusión y con qué hechos. El planificador se ejecutará con los costos y cierres derivados; no sustituye el ciclo del motor.

## Comprobación de comprensión

1. Sin mirar el recorrido, explica por qué E2 se dispara antes que E3 aunque E3 era aplicable desde el inicio.
2. Si se elimina A de la memoria inicial, ¿qué sucede? Ninguna regla se dispara.
3. Si se elimina E2, ¿qué sucede? La traza es E1 → E3; C no se deduce.
4. ¿Por qué no basta con impedir hechos duplicados? Eso no impide volver a ejecutar la misma regla.
5. ¿Por qué no debe bloquearse una regla por su nombre para todos los túneles? Porque puede corresponder un disparo distinto a cada entidad.

El criterio de S1-07 es poder explicar el ciclo sin consultar notas. Este documento proporciona el recorrido y las respuestas, pero no acredita por sí solo la comprensión del integrante. No hay pruebas nuevas del motor porque aún no existe su implementación.

El siguiente paso del orden sugerido es S1-08: diseñar el esquema JSON de la mina, aprovechando la práctica de S1-05. Después vendrá la mina de prueba de S1-09. El diseño del motor en S1-12 conserva su lugar en el plan.
