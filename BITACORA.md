# Bitácora de sesiones

[← Índice](README.md)

Una entrada por sesión, la más reciente arriba. Tres líneas bastan.

## Plantilla

```
### AAAA-MM-DD · [Nombre] · [horas] h
- Hice:
- Falló / dudas:
- Siguiente paso exacto:
```

## Control semanal

| Sem. | Entregable (Sí/Parcial/No) | Horas A | Horas B | ¿Qué se recorta? |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 ⚑ | | | | |
| 5 | | | | |
| 6 ⚑ | | | | |
| 7 | | | | |
| 8 | | | | |

⚑ = punto de decisión

## Sesiones

### 2026-11-26 · S1-06: pytest básico · 1 h
- Hice: instalamos pytest 9.2.0 con `python -m pip install pytest` (el ejecutable quedó fuera del PATH; se usa siempre `python -m pytest`). Tres conceptos: descubrimiento por convención (`test_*.py` y `test_*`), lectura de un fallo con la reescritura de asserts (`assert 780.0 <= 500`) y selección con node id y `-k`. Ejercicio en `Python Practica\S1_06\test_refugio.py`, fuera del repo: una prueba pasa y otra falla a propósito; comprobado `1 failed, 1 passed` y `1 failed, 1 deselected`.
- Falló / dudas: al empezar se escribió `verificar_refugio()` sin `test_`; pytest responde "no tests ran" con código 0, indistinguible de un éxito. Horas estimadas, sin medir.
- Siguiente paso exacto: commit `docs: cerrar S1-06, pytest básico`, push, PR con `Closes #8`, review de B y merge; comprobar en `main` que `contexto.md` quede en 12 de 20. Después, B: S1-10 (#12) → S1-11; A: S1-13 en pareja cuando B cierre S1-10.

### 2026-11-26 · S1-12: diseño de Hecho, Patrón y Regla · 1,5 h
- Hice: revisamos el estado real (S1-09 fusionada en `main`, 10 de 20) y corregimos `contexto.md`, que seguía en 9 de 20. Agregamos a `AGENTS.md` la regla de explicar con analogías, un concepto a la vez. Redactamos **D23**: `Hecho` como `NamedTuple` (tupla, inmutable y hashable por la firma de D21), `Patron` con variables `?x` y operador, `Regla` con prioridad espaciada y desempate por posición en el catálogo, memoria acumulativa y pseudocódigo de `unificar`/`aplicar`. Agregamos tres términos al glosario (patrón, variable de regla, unificación) y ajustamos prioridad y especificidad. Validamos `mina_prueba.json` contra D22 y D10: 185,00 m y 409,87 m. Rama `miguel/s1-12` creada; cambios aún sin `git add`.
- Falló / dudas: primero recomendé `@dataclass(frozen=True)` para `Hecho`; al contrastar `AGENTS.md` y el glosario, que lo definen como tupla, se cambió a `NamedTuple`. El commit 516f52d decía "actualizar contexto" pero `main` seguía en 9 de 20; quedó como trampa. Dos PR (#33 y #34) de la misma rama: no bloquea, pero conviene un PR por tarjeta. Horas estimadas, sin medir.
- Siguiente paso exacto: `git add` de los cinco archivos, dos commits (`docs: contexto a 10 de 20 y regla de analogías` y `docs: D23 diseño de Hecho, Patrón y Regla`), push, PR con `Closes #14` (número confirmado), review de B y merge. Después, A: S1-06 (pytest) y B: S1-10 (clases `Nodo`, `Arista` y `Mina`).

### 2026-11-25 · S1-09: mina de prueba y saneamiento de la documentación · 2 h
- Hice: contrasté la documentación con Git y el tablero y corregí 14 inconsistencias: `sprints.md` decía que las tarjetas de aprendizaje no llevan PR; un ejemplo daba a S1-11 como dependiente de S1-08; S1-13/S1-14 tenían dueño y estimación incompatibles; `alcance.md` omitía el tipo `frente`; el enlace del tag semanal tenía dos `../` de más (capítulo y plantilla); el capítulo no listaba D15–D22; `AGENTS.md` seguía diciendo "siguiente: D22"; el árbol del README omitía `contexto.md`, y otras menores. Decidimos pasar "varios mineros" al Sprint 2 (Nivel 1) y dejar S1-13/S1-14 como `A + B (dueño A)`. Creé `data/escenarios/mina_prueba.json` (7 nodos, 2 niveles, 6 aristas) y verifiqué a mano D10: 185 m y 409,87 m.
- Falló / dudas: la comprobación de D10 se hizo con un script temporal fuera del repo; la prueba automática llega con el planificador. Queda un hueco en los títulos del Backlog (`S3-H06`) y la duda de si B debe figurar en S1-13/S1-14 o solo A. Horas estimadas, sin medir.
- Siguiente paso exacto: push y PR con `Closes #11` (número confirmado). El review del compañero ya está hecho y aprobado; falta el merge y, al fusionar, actualizar el "Estado actual" de `contexto.md` a 10 de 20 tarjetas. Después, A: S1-12 y B: S1-10.

### 2026-11-24 · S1-08: esquema JSON de la mina (D22) · 1,5 h
- Hice: sesión conjunta de S1-08. Cerramos **D22** en `decisiones.md`: tres bloques (`meta`, `nodos`, `aristas`), grafo no dirigido con cada arista escrita una sola vez, `z` y `longitud` derivadas (`z = -(nivel-1) * altura_nivel_m`, `math.dist` en 3D), ids descriptivos que el cargador no parsea, `refugio` como tipo de nodo, `labor` opcional y validación estructural separada de la regla de 500 m (D10). Agregamos seis términos al glosario (altura de nivel, grafo no dirigido, esquema, valor derivado, lista de adyacencia, bucle) y actualizamos `contexto.md` (estado del sprint y poda de la trampa de fechas). Commit `docs: D22 esquema JSON de la mina` hecho en la rama de la tarjeta; falta push y PR #10.
- Falló / dudas: nada técnico, no se escribió código. Dudamos entre guardar `z` por nodo o derivarlo de `nivel`; se resolvió derivarlo para tener una sola fuente de verdad. Riesgo anotado: que alguien agregue `z` o `longitud` al JSON "por comodidad" y rompa el esquema. Horas estimadas, sin medir: ~1,5 h.
- Siguiente paso exacto: push, PR con `Closes #10`, review del compañero y merge; luego S1-09 (crear `mina_prueba.json`: 6–8 nodos, 2 niveles, refugio a ≤ 500 m de cada frente, dueño A).
- Corrección (2026-11-24): el push y el PR #31 se hicieron; `Closes #10` cerró la tarjeta y `main` ya incluye el merge. S1-08 está en Done.

### 2026-11-24 · S1-07: forward chaining y refracción · 1 h
- Hice: repasamos el ciclo del motor (reconocer → conjunto de conflicto → prioridad → disparo → firma de refracción → traza → punto fijo) con el símil de idempotencia con clave de correlación de Java/C#, y lo explicamos sin notas. En el tablero corregimos que S1-18, la tarjeta de cierre del sprint, bloqueaba en silencio a varias tarjetas entre ellas S1-07: el enlace "blocked by" estaba invertido; S1-07 quedó asignada a A y B y en In Progress. Al armar el ejemplo R1→R4 descubrimos que la cadena estaba rota (R1 concluía `nivel_co = alerta` y R2 pedía `riesgo_alto`) y la reescribimos con una regla de escalada `alerta → riesgo_alto`, comprobando que cada ENTONCES alimenta el SI siguiente. Cerramos con D21 (refracción por firma) y dos términos nuevos en el glosario, y abrimos el PR de la tarjeta.
- Falló / dudas: describimos el conjunto de conflicto como "el resultado" del motor cuando en realidad es la entrada del paso de reconocimiento; sobre `hashable` dimos la razón de trazabilidad en vez de la técnica (hash estable para poder usar `set`/`dict`). La memoria no es "set o lista": set para pertenencia y lista para la traza. Sin notas todavía confundimos la variable de R3 con la de R1; las variables son locales a cada regla.
- Siguiente paso exacto: el PR ya está abierto con `Closes #9` y solo toca documentación; falta el review del compañero y el merge, que probablemente ocurra en la próxima sesión. Después, S1-08: esquema JSON de la mina en sesión conjunta (decisión D22).

### 2026-11-23 · S1-05: leer y escribir JSON en Python (sesión 3) · 1 h
- Hice: comparamos el módulo `json` con Gson/`System.Text.Json` y escribimos `leer_json.py` (carga el archivo, cuenta nodos y maneja `JSONDecodeError` con línea y columna) y `escribir_json.py` (lee, agrega `meta` y guarda con `indent=2` y `ensure_ascii=False`), en la carpeta local de nivelación fuera del repositorio. En documentación: `contexto.md` al día con el cierre de S1-02 y la automatización de PR validada con #27; corregimos el capítulo de la semana 1, que decía que las tarjetas de aprendizaje no requieren PR.
- Falló / dudas: `escribir_json.py` sobrescribía `mina_demo.json` y borraba los nodos; se corrigió leyendo antes de escribir. En `leer_json.py` las impresiones quedaban fuera del `try`, así que con un JSON inválido se usaba `datos` sin definir; se movieron a un `else`. Falta ejecutar la prueba con un JSON roto (quitar una coma): el manejo de `JSONDecodeError` está escrito, pero no verificado.
- Siguiente paso exacto: commit `docs: cerrar S1-05, JSON en Python`, push, PR con `Closes #7`, review del compañero y merge; luego S1-07 (forward chaining y refracción), que desbloquea S1-12.

### 2026-11-23 · S1-02: clases y módulos (sesión 2) · 1,5 h
- Hice: explicamos `__init__`/`self`, `@dataclass`, métodos especiales y módulos. Escribí `modelo.py` (`Nodo` con `distancia_a` en 3D vía `math.dist`; `Tunel` con `longitud`, `__len__` y `__repr__`) y `demo.py` en la carpeta local de nivelación, fuera del repositorio: `python demo.py` imprime `Tunel(tunel_ref_1_frente_4, 144.2255... m)` y `2`. Además corregimos la entrada del 2026-10-25 (los 17 en Backlog ya estaban en Ready) y registramos en `contexto.md` que las tarjetas de aprendizaje se cierran con un PR de solo documentación.
- Falló / dudas: pegué los dos archivos en un mismo bloque y hubo que separarlos en `modelo.py` y `demo.py` para que el import funcionara. S1-04 se movió a Done a mano, así que la automatización "PR con `Closes #N` → Done" sigue sin probarse. Horas estimadas, sin medir: ~1,5 h.
- Siguiente paso exacto: rama `<nombre>/s1-02`, PR con `Closes #3`, review del compañero, merge y comprobar que la tarjeta pasa sola a Done; luego S1-05, leer y escribir JSON en Python.

### 2026-11-23 · Nivelación de Python (S1-01) y cierre de S1-04 · 3 h
- Hice: completamos E1–E7 con datos de la mina (variables, f-strings, listas, diccionarios, tuplas, conjuntos, funciones, control y comprensiones); agregamos cinco términos al glosario; S1-01 y S1-04 quedaron cerradas.
- Falló / dudas: confundimos `("tunel_1_2", "cerrado", False)` con un túnel cerrado y promediamos valores de hechos en vez de costos; `False` vale 0 en Python. También usamos `max` como nombre de variable. Se corrigió filtrando por atributo y usando `costos.values()`. El `TypeError` al modificar una tupla fue intencional.
- Siguiente paso exacto: S1-02, clases y módulos en Python.

### 2026-10-25 · Corrección de documentación del tablero
- Hice: actualicé el plan, las decisiones, el glosario, el capítulo de la semana 1 y la bitácora: 20 tarjetas en total, columnas en inglés y una tarjeta compartida cuando el dueño es A y B.
- Falló / dudas: las 17 tarjetas pendientes del sprint 1 estaban en Backlog; según el plan corresponden a Ready. **Resuelto:** se movieron a Ready y hoy quedan 15 (S1-01 y S1-04 ya se cerraron).
- Siguiente paso exacto: (cumplido) mover las tareas pendientes del sprint 1 a Ready y comenzar S1-01, nivelación de Python.

### 2026-10-24 · Tablero del sprint 1 · 2 h
- Hice: cerramos S1-00, S1-03 y S1-03b; configuramos GitHub Projects (columnas, campos, etiquetas, workflows) y cargamos las 20 tarjetas del sprint 1, una por tarea, con dueño, estimación, prioridad e iteración.
- Falló / dudas: S1-03 y S1-03b son de infraestructura y no pasan por PR (excepción consciente a la DoD). Horas estimadas, sin medir: ~2,5 h brutas y ~1,75 h productivas.
- Siguiente paso exacto: S1-01, nivelación de Python con ejercicios del dominio.

### 2026-10-17 · Guía de carga del tablero
- Hice: agregamos a kanban.md la guía paso a paso para cargar tarjetas (6.2.2) y los títulos del Backlog listos para copiar.
- Falló / dudas: ninguna.
- Siguiente paso exacto: S1-03 (configurar el tablero) y S1-03b (cargar tarjetas siguiendo 6.2.2).

### 2026-10-17 · Plantilla del tablero y Backlog
- Hice: elegimos la plantilla Kanban de GitHub Projects; definimos qué va en el Backlog.
- Falló / dudas: ninguna.
- Siguiente paso exacto: crear el proyecto con la plantilla Kanban y continuar con S1-03.

### 2026-10-17 · Aprendizaje de GitHub Projects
- Hice: agregamos `S1-00` (guía oficial, 0,5 h c/u) y extendimos `S1-04` para practicar PR vinculados a tarjetas.
- Falló / dudas: B queda 1,5 h sobre la capacidad en el sprint 1.
- Siguiente paso exacto: S1-00, leer *Quickstart for Projects*; luego S1-03.

### 2026-10-17 · Recalibración y configuración del tablero
- Hice: ajustamos el aprendizaje por la base en Java/C# (D17); documentamos la configuración de GitHub Projects y los sprints como iteraciones (D18).
- Falló / dudas: el tablero recién creado no tiene las columnas del plan.
- Siguiente paso exacto: S1-03, configurar GitHub Projects con los pasos 1–7; luego S1-03b, cargar las tarjetas.

### 2026-10-17 · Sprints y tablero
- Hice: aprobamos 4 sprints de 2 semanas; definimos el tablero Kanban, cómo escribir tareas y las 18 tareas del sprint 1; D15–D16; glosario de gestión.
- Falló / dudas: el núcleo del sprint 1 excede la capacidad en 1,5 h por persona.
- Siguiente paso exacto: S1-03, crear el repositorio en GitHub y el tablero con las tarjetas del sprint 1.

### 2026-10-17 · Niveles de riesgo y glosario
- Hice: elegimos la opción b (supuesto del equipo) para el peligro inmediato; tabla de niveles por gas; glosario; D12–D14.
- Falló / dudas: ninguna.
- Siguiente paso exacto: nivelación en Python y diseño del esquema JSON de la mina (con coordenadas en metros y refugios a ≤ 500 m).

### 2026-10-17 · Umbrales normativos
- Hice: extraje los umbrales del DS 024-2016-EM y sus Anexos (Anexo 15, Art. 246, 248, 151 y Anexo 19) al catálogo de reglas; registré D09–D11.
- Falló / dudas: la norma no da niveles de emergencia para gases. Decidir: segunda fuente o supuesto del equipo.
- Siguiente paso exacto: revisar con el compañero la tabla de umbrales y decidir la fuente del nivel de peligro inmediato.

### 2026-10-17 · Plan inicial
- Hice: definimos enfoque, alcance, cronograma, reparto y flujo de trabajo.
- Falló / dudas: verificar umbrales del DS 024-2016-EM.
- Siguiente paso exacto: reunión del equipo para aceptar el reparto y crear el repositorio en GitHub.
