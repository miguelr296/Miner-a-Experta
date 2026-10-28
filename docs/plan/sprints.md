# 5. Sprints

[← Índice](../../README.md)

## 5.1 Estructura

- **4 sprints de 2 semanas.** Cada uno termina en un punto de decisión del [cronograma](cronograma-y-reparto.md).
- **Capacidad:** 20 h por persona por sprint, de las cuales **≈ 2 h son ceremonias**. Quedan **≈ 18 h por persona para tareas**.
- **Aprendizaje justo a tiempo:** en cada sprint se aprende solo lo que ese sprint necesita.

| Sprint | Semanas | Objetivo | % aprendizaje | Cierra con |
|---|---|---|---|---|
| 1 | 1–2 | Fundamentos y motor mínimo | ~40 % | Retro clave: recalibrar estimaciones |
| 2 | 3–4 | Sistema de punta a punta | ~20 % | ⚑ Punto de control (semana 4) |
| 3 | 5–6 | Nivel 2: certeza, decisiones, conflictos, A\* | ~15 % | ⚑ Decisión sobre Nivel 3 |
| 4 | 7–8 | Cierre, documentación y demo | ~5 % | Tag `final` |

Las horas de los sprints 2–4 son **estimaciones brutas**: se recalculan en cada planning con la velocidad real medida en el sprint anterior.

## 5.2 Contenido de cada sprint

### Sprint 1 — Fundamentos y motor mínimo
**Objetivo:** el motor dispara 2–3 reglas encadenadas y deja traza; la mina se carga desde JSON; ambos trabajan con ramas y PR.
Detalle de tareas: [tablero Kanban](kanban.md#7-sprint-1--tareas).

### Sprint 2 — Sistema de punta a punta ⚑
**Objetivo:** los 3 escenarios corren completos con un solo comando (sensores → reglas → costos → rutas → explicación).

| Historia | Dueño | Estimación bruta |
|---|---|---|
| 📚 Depuración, conjuntos, diccionarios anidados | A | 1 h |
| 📚 Colas de prioridad (`heapq`) y Dijkstra | B | 3 h |
| 15 reglas con sus pruebas (incluye borrador de reglas si no se hizo en S1) | A | 9 h |
| Explicación "¿por qué?" | A | 3 h |
| JSON de configuración de umbrales (D13) | A | 2 h |
| Conectar motor con costos de aristas | A | 3 h |
| Dijkstra con costos dinámicos | B | 5 h |
| Línea base con filtro por umbral | B | 3 h |
| Validar refugio a ≤ 500 m | B | 2 h |
| Salida por consola | B | 2 h |
| 3 escenarios JSON | B | 3 h |
| Integración y prueba final | A + B | 2 h c/u |

### Sprint 3 — Nivel 2 ⚑
**Objetivo:** razonamiento con incertidumbre, decisiones y conflictos resueltos, medidos contra la línea base.

| Historia | Dueño | Estimación bruta |
|---|---|---|
| 📚 Factores de certeza (MYCIN) | A | 2 h |
| 📚 A\* y heurística admisible | B | 2 h |
| Factores de certeza en el motor | A | 7 h |
| Explicación "¿cómo?" | A | 3 h |
| Reglas de decisión (evacuar / refugiarse / esperar) | A | 4 h |
| Conflictos de reglas (incluye Art. 248 con ANFO) | A | 3 h |
| A\* | B | 4 h |
| Varios mineros | B | 3 h |
| Escenarios de conflicto | B | 3 h |
| Métricas contra línea base | B | 5 h |

### Sprint 4 — Cierre
**Objetivo:** sistema estable, documentado y demo ensayada.

| Historia | Dueño | Estimación bruta |
|---|---|---|
| Elemento del Nivel 3 **o** pulido | A + B | 6 h c/u |
| Corrección de errores | A + B | 4 h c/u |
| README de ejecución y capítulos pendientes | A + B | 3 h c/u |
| 📚 MkDocs (opcional) | B | 2 h |
| Guion y ensayo de la demo | A + B | 3 h c/u |
| Colchón | A + B | resto |

## 5.3 Ceremonias

| Ceremonia | Cuándo | Duración | Qué se hace |
|---|---|---|---|
| **Planning** | Primer día del sprint | 30–45 min | Confirmar objetivo, convertir historias en tareas, estimar, repartir |
| **Sync** | Sesión conjunta de la semana intermedia | (es trabajo de integración) | Integrar ramas, revisar el tablero, detectar atrasos |
| **Review + retro** | Último día del sprint | 1 h | Mostrar lo que funciona, horas reales vs. estimadas, qué mejorar, tag, capítulo |
| **Daily** | Asíncrona | 2 min | Tres líneas en la bitácora o por chat |

## 5.4 Definición de terminado (DoD)

Una tarea solo pasa a **Done** si:

- [ ] Está en `main` mediante un PR revisado por el otro integrante. *(Excepción: las tareas que no tocan el repositorio —solo tablero o configuración de GitHub— se cierran directamente y se anotan en la bitácora; ver D19.)*
- [ ] Las pruebas pasan.
- [ ] Si es una regla: está en el [catálogo](../reglas.md) con fuente.
- [ ] Los términos nuevos están en el [glosario](../glosario.md).
- [ ] La bitácora está actualizada.

Las tareas de aprendizaje (📚) no requieren PR: se cierran cuando se cumple su criterio de aceptación.

## 5.5 Riesgos

- **Estimaciones poco fiables:** el equipo nunca midió su ritmo. La retro del sprint 1 recalcula el sprint 2.
- **Sprint 1 es el más arriesgado** (≈ 40 % es aprendizaje de Python, Git, pytest y GitHub Projects). Si el motor mínimo no se termina, el sprint 2 hereda el atraso justo antes del punto de control.
