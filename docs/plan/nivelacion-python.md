# S1-01 — Nivelación de Python

[← Índice](../../README.md)

Esta práctica corresponde a S1-01 del [tablero](kanban.md). Sigue pendiente hasta que el integrante resuelva y pueda explicar los tres ejercicios. No implementa reglas del sistema ni adelanta el diseño del motor.

## Preparación

Hay una [solución de referencia](../../ejercicios/nivelacion.py) implementada por el asistente a petición del usuario. Se conserva fuera de `src/` porque es material de aprendizaje. Para ejecutarla y comprobar los casos de aceptación desde la raíz del repositorio:

```bash
.venv/bin/python ejercicios/nivelacion.py
.venv/bin/python -m pytest -q
```

Validación realizada: 14 casos pasaron. Esto comprueba las soluciones, pero no acredita todavía el aprendizaje del integrante. Las pruebas automatizadas son apoyo de verificación; el aprendizaje de pytest sigue correspondiendo a S1-06.

Desde `/workspace/Miner-a-Experta`, activa el entorno preparado:

```bash
source .venv/bin/activate
python --version
```

Usa una carpeta local ignorada para tus soluciones, separada de `src/`:

```bash
mkdir -p .venv/ejercicios
```

Crea allí `ejercicio_01.py`, `ejercicio_02.py` y `ejercicio_03.py`. Ejecuta cada archivo con `python .venv/ejercicios/ejercicio_01.py`, cambiando el número según corresponda. Esta carpeta se pierde si eliminas el entorno virtual; no es una entrega versionada. Podemos revisar las soluciones antes de decidir dónde conservarlas.

## Lo que cambia respecto de Java y C#

- La indentación delimita los bloques; no se usan llaves. Usa cuatro espacios.
- No necesitas una clase ni un método `main` para ejecutar un archivo.
- No declaras el tipo de cada variable: los valores tienen tipos y las operaciones deben ser compatibles.
- Una función empieza con `def`, sus parámetros van entre paréntesis y el encabezado termina con `:`. Devuelve resultados con `return`.
- Una lista conserva el orden y admite cambios; una tupla agrupa valores y no permite reemplazar sus elementos.
- Un diccionario relaciona claves con valores; un conjunto elimina duplicados y no garantiza el orden de presentación.
- Una comprensión construye una colección a partir de otra y puede filtrar elementos.

## Ejercicio 1 — Distancia de un recorrido

Escribe una función `distancia_total(tramos)` que reciba una lista de distancias en metros y devuelva su suma usando un bucle. Llámala e imprime el resultado.

| Entrada | Resultado esperado |
|---|---|
| `[120, 80, 150]` | `350` |
| `[]` | `0` |
| `[25]` | `25` |

Practicas variables, indentación, funciones, listas y acumulación. Usa solo distancias no negativas en esta práctica. No necesitas clases ni archivos JSON.

## Ejercicio 2 — Tipos de nodos

Representa los nodos mediante este diccionario, cuyas claves son identificadores y cuyos valores son tipos:

```python
nodos = {
    "n1": "frente",
    "n2": "intersección",
    "n3": "refugio",
    "n4": "salida",
    "n5": "refugio",
}
```

Escribe `buscar_por_tipo(nodos, tipo)` para devolver una lista de identificadores del tipo solicitado, conservando el orden del diccionario. Primero utiliza un bucle; después escribe una segunda versión con una comprensión.

| Tipo solicitado | Resultado esperado |
|---|---|
| `"refugio"` | `["n3", "n5"]` |
| `"salida"` | `["n4"]` |
| `"otro"` | `[]` |

Comprueba también el diccionario vacío. Esta representación es solo un ejercicio; no define el futuro esquema de la mina.

## Ejercicio 3 — Entidades con eventos reportados

Representa cada evento con una tupla `(entidad, atributo, valor)`:

```python
eventos = [
    ("tunel_1_2", "derrumbe_reportado", True),
    ("tunel_2_3", "derrumbe_reportado", False),
    ("tunel_1_2", "derrumbe_reportado", True),
    ("tunel_3_4", "derrumbe_reportado", True),
]
```

Escribe `entidades_con_derrumbe(eventos)` para devolver un conjunto con las entidades cuyo atributo sea `"derrumbe_reportado"` y cuyo valor sea `True`. Descompón cada tupla en tres variables durante el recorrido.

El conjunto esperado contiene `"tunel_1_2"` y `"tunel_3_4"`, una sola vez cada uno. Para imprimir siempre el mismo orden, usa `sorted(resultado)`: debe mostrar `["tunel_1_2", "tunel_3_4"]`.

Comprueba la lista vacía y un evento con otro atributo: no deben añadir entidades. Esto practica tuplas, condiciones y conjuntos; todavía no modifica rutas ni dispara reglas.

## Cierre de la tarea

Para cada ejercicio, ejecuta los casos indicados y compara los resultados. Explica qué recibe la función, qué devuelve y por qué elegiste cada colección. No basta con copiar una solución.

Cuando los tres estén resueltos y revisados, se puede registrar S1-01 como completada para ese integrante. Después corresponde S1-04, práctica de ramas y PR con el equipo, según el orden sugerido del plan. A continuación viene S1-02, clases y módulos, requisito para modelar la mina y aprender el cargador JSON.
