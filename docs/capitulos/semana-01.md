# Semana 1 — Nivelación, modelo de la mina y fuentes

[← Índice](../../README.md) · Código de esta semana: tag [`semana-01`](../../../../tree/semana-01)

**Fechas:** dd/mm – dd/mm · **Horas reales:** A: __ h · B: __ h · **Entregable:** Sí / Parcial / No

## 1. Objetivo de la semana

- Nivelación en Python (sintaxis, colecciones, clases y lectura de JSON) y Git.
- Diseñar el esquema JSON de la mina y una mina de prueba.
- Extraer y verificar los umbrales normativos que usarán las reglas.
- Acordar las reglas de trabajo del equipo.

## 2. Conceptos aprendidos

- **Límites de exposición ocupacional:** TWA (promedio de 8 h), STEL (15 min) y techo (nunca se supera). No son niveles de emergencia.
- **Adquisición de conocimiento:** sin experto disponible, una norma técnica puede cumplir el rol de fuente experta, pero no cubre todo; lo faltante se declara como supuesto.
- **Python para quien viene de Java/C#:** la indentación delimita los bloques, el tipo se decide al ejecutar (tipado dinámico) y las colecciones básicas son listas, diccionarios, tuplas y conjuntos.
- **Funciones y comprensiones:** `def`/`return` para encapsular lógica; las comprensiones crean listas, diccionarios y conjuntos a partir de un iterable con una condición.
- **PR vinculado a una tarjeta:** una rama, un commit, un push y un PR revisado por el compañero; `Closes #N` cierra la tarjeta al fusionar.

## 3. Decisiones tomadas y por qué

- D09: gases en niveles (normal / alerta / riesgo alto) según TWA y STEL.
- D10: refugio a ≤ 500 m de cada frente como restricción del modelo de mina.
- D11: cada regla declara si su fuente es `NORMA` o `SUPUESTO`.
- D12: el nivel de peligro inmediato (cierre del túnel) es un supuesto del equipo.
- D13: umbrales en un JSON de configuración.
- D14: glosario obligatorio.

## 4. Qué se implementó

- Tabla de umbrales del [catálogo de reglas](../reglas.md), con artículo o anexo de origen: O₂, CO, NO₂, CO₂, H₂S, velocidad del aire y refugios.
- Tabla de niveles de riesgo por gas (normal / alerta / riesgo alto / peligro inmediato).
- [Glosario](../glosario.md) con todas las siglas y términos usados hasta ahora.
- Repositorio en GitHub y tablero del sprint 1 con 20 tarjetas, una por tarea; las tareas asignadas a A y B comparten una tarjeta.
- Nivelación de Python con E1–E7: variables, f-strings, listas, diccionarios, tuplas, conjuntos, funciones, control y comprensiones.
- Práctica de Git y GitHub: rama, commit, push y PR revisado (S1-04).
- *(pendiente: esquema JSON y mina de prueba)*

## 5. Pruebas

Sin pruebas automáticas todavía: los ejercicios se verificaron ejecutándolos y comparando la salida esperada.

## 6. Problemas encontrados

- La norma no define niveles de gas de peligro inmediato; sin ellos no hay base citable para cerrar un túnel por gases. Se resolvió con un supuesto declarado (D12).
- En Python `False` vale 0: confundimos el hecho `(tunel_1_2, cerrado, False)` con un túnel cerrado. Se corrigió filtrando por atributo antes de comparar.
- Promediamos los valores de los hechos (ppm y booleanos) en vez de los costos. Se corrigió usando `costos.values()`.
- Usamos `max` como nombre de variable y ocultamos la función incorporada; se renombró a `max_co`.

## 7. Lecciones aprendidas

- En Python conviene filtrar por atributo antes de comparar o sumar valores de un hecho; un booleano también es un entero (`False` = 0).
- Para armar mensajes, las f-strings son más claras que concatenar con `+` y `str()`.
- Las tareas de aprendizaje no requieren PR; las que cambian el repositorio sí.

## 8. Siguiente semana

Motor de inferencia mínimo, programado en pareja.
