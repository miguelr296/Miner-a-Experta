# 4. Flujo de trabajo

[← Índice](../../README.md)

## 4.0 Sprints y tablero

El trabajo se organiza en [sprints de 2 semanas](sprints.md) y se gestiona en el [tablero Kanban](kanban.md). Regla: **1 tarjeta en curso por persona**, que coincide con "una tarea por sesión".

## 4.1 Semana tipo (10 h por persona)

| Bloque | Duración | Qué se hace |
|---|---|---|
| 3 sesiones individuales | ≈ 2,5 h c/u | Trabajo en la tarea asignada |
| 1 sesión conjunta | 1,5–2 h | Integrar ramas, revisión cruzada, planear la semana siguiente, escribir el capítulo semanal (30 min) |

## 4.2 Rutina de cada sesión individual

1. **Retomar (5 min):** leer el último "siguiente paso" en la [bitácora](../../BITACORA.md).
2. **Trabajar:** una sola tarea, con un resultado visible (una prueba que pasa, una regla que se dispara).
3. **Cerrar (10 min):** correr las pruebas, hacer commit y anotar en la bitácora qué se hizo, qué falló y el siguiente paso exacto.

## 4.3 Git (versión mínima)

- `main` **siempre funciona**.
- Una rama por tarea: `nombre/tarea` (ej. `lucas/motor-minimo`).
- Se une a `main` con un **Pull Request revisado por el otro integrante**.
- **Un archivo, un dueño por semana:** los dos no editan el mismo archivo la misma semana.
- Commits pequeños con prefijo: `feat:`, `fix:`, `test:`, `docs:`.
- Al cerrar cada semana (en la sesión conjunta): tag `semana-01`, `semana-02`… y `final` al terminar.

## 4.4 Pruebas

- pytest solo con `assert` simples (se aprende en la semana 2, ≈ 2 h).
- **Cada regla tiene al menos una prueba.**
- No se hace merge si las pruebas fallan.

## 4.5 Documentación (opción A + B)

- Un capítulo por semana en `docs/capitulos/`, a partir de la [plantilla](../capitulos/_plantilla.md).
- Cada capítulo enlaza al tag de su semana.
- Cada decisión de diseño va al [registro de decisiones](../decisiones.md).
- Cada regla nueva va al [catálogo](../reglas.md) con fuente y prueba.
- Cada sigla o término técnico nuevo va al [glosario](../glosario.md) en la misma sesión.
- Opcional en semana 8: migrar a MkDocs + GitHub Pages (reutiliza los mismos `.md`).

## 4.6 Uso del asistente

- El código lo escribe el equipo.
- Se consulta para: explicar conceptos, revisar código, proponer mejoras y detectar errores.
- Inicio de semana: "empezamos la semana N" → concepto, diseño y pruebas esperadas.
- Fin de semana: se comparte lo hecho para revisión contra el entregable.

## 4.7 Reglas para no descarrilarse

- Una tarea por sesión. Lo demás se anota en la bitácora.
- Primero correcto, luego (si hay tiempo) rápido.
- Trabado más de 30 min → anotar y consultar.
- Fines de semana: colchón, no obligación.

## 4.8 Control de los viernes (2 min)

- ¿Entregable cumplido? Sí / Parcial / No.
- Horas reales vs. estimadas (por persona).
- Si "Parcial" o "No": ¿qué se recorta?
