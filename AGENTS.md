# AGENTS.md

Proyecto académico (curso Sistemas Expertos, 2 integrantes: A y B). Todo en español: documentación, commits, comentarios y términos del dominio.

## Estado actual

- **Aún no hay código**: `src/`, `tests/` y `data/escenarios/` solo tienen `.gitkeep`. No existen manifiestos, dependencias, CI, linter ni comandos de build/test. No inventes comandos
- Lo que existe es documentación en `docs/` más `BITACORA.md`. El plan es la fuente de verdad de lo que se debe construir.
- Plan: 8 semanas, 4 sprints de 2 semanas. Puntos de control en las semanas 4 y 6 (reglas de recorte en `docs/plan/alcance.md`). La semana actual está en `BITACORA.md`.

## Qué se construye

Sistema experto **híbrido** para emergencias en una mina metálica subterránea peruana (no carbón; sin metano):
1. **Motor de reglas propio** con forward chaining, prioridad y refracción, que produce traza.
2. **Planificador** Dijkstra con costos dinámicos (Nivel 2: A\* con heurística euclidiana 3D) que calcula una ruta por minero.
3. **Explicación** "¿por qué?" (Nivel 1) y "¿cómo?" (Nivel 2).

Las reglas traducen sensores en costos y cierres de aristas; el planificador consume esos costos.

## Restricciones de diseño (no violar)

- **D01:** las reglas solo cierran un túnel o multiplican su costo por un factor ≥ 1. Nunca reducen costos; así la distancia euclidiana sigue siendo admisible para A\*.
- **D03:** el motor y el planificador son propios. No uses librerías de sistemas expertos (clips, experta, durable_rules…) ni de rutas (el grafo/Dijkstra/A\* no vienen de networkx). NetworkX/matplotlib solo aparecen como apoyo de visualización en el Nivel 3.
- **D02:** datos en JSON, sin base de datos.
- **D13:** los umbrales van en un JSON de configuración, no hardcodeados en el código (separar conocimiento y motor).
- Un hecho es una tupla `(entidad, atributo, valor)`, p. ej. `(tunel_4_7, co_ppm, 30)`.
- Lenguaje: Python con pytest. Dependencias mínimas.
- Fuera de alcance: bases de datos, interfaz web elaborada, datos reales, ML, modelado completo del reglamento, geomecánica (la caída de rocas es un evento reportado que bloquea un túnel).
- Sistema: salida por consola, ejecutable con un solo comando.
- Mina de prueba: JSON con nodos `(x, y, nivel)` en metros y tipo (intersección, salida, refugio, frente). Todo frente debe tener un refugio a ≤ 500 m de recorrido (D10). Nivel 1: 15–20 nodos y 2 niveles (la mina de prueba de la semana 2 tiene 6–8 nodos).
- Línea base de comparación: Dijkstra con filtro por umbral de sensor (D06), no Dijkstra ciego.

## Conocimiento y umbrales

- Fuente de umbrales: DS 024-2016-EM (con modificatorias del DS 023-2017-EM). Todos están en `docs/reglas.md` con artículo o anexo.
- Cada regla declara `NORMA` o `SUPUESTO` (D11). La norma da límites de exposición laboral (TWA/STEL/techo), **no** niveles de emergencia.
- Los gases se evalúan por niveles: normal / alerta / riesgo alto / peligro inmediato (D09, D12). Solo el último cierra el túnel. Los valores de peligro inmediato y los multiplicadores de costo son supuestos del equipo y deben presentarse como tales.
- Categorías de regla: `DIAG`, `RIESGO`, `RUTA`, `DEC`. Metas: 15 reglas (Nivel 1) y ≈ 25 (Nivel 2), con al menos una cadena de 3–4 pasos.
- Ventilación: velocidad del aire 20–250 m/min, mínimo 25 con ANFO (Art. 248).

## Reglas de documentación (obligatorias)

- Cada decisión de diseño va a `docs/decisiones.md` (formato `Dnn`, siguiente: D19).
- Cada regla nueva va a `docs/reglas.md` con la plantilla (categoría, SI, ENTONCES, prioridad, fuente, tipo de fuente, justificación, prueba). Cada regla tiene al menos una prueba pytest.
- Cada sigla o término nuevo va a `docs/glosario.md` en la misma sesión (D14).
- Un capítulo por semana en `docs/capitulos/semana-NN.md` desde `_plantilla.md`, enlazando al tag de la semana.
- Al cerrar una sesión se agrega una entrada arriba en `BITACORA.md` (hice / falló / siguiente paso exacto).
- Si se agrega o mueve un documento, actualiza el índice del `README.md`.

## Flujo de Git

- `main` siempre funciona; no se hace merge si las pruebas fallan.
- Ramas `nombre/tarea`, PR revisado por el otro integrante, `Closes #N` para cerrar la tarjeta.
- Un archivo, un dueño por semana (evitar conflictos).
- Commits con prefijo `feat:`, `fix:`, `test:`, `docs:`.
- Tags semanales `semana-01`, `semana-02`… y `final`.
- Tablero Kanban en GitHub Projects. Las tareas del sprint 1 (`S1-xx`) están en `docs/plan/kanban.md` sección 7.

## Uso del asistente

- Según `docs/plan/flujo-de-trabajo.md` (4.6), **el código lo escribe el equipo**; el asistente explica conceptos, revisa código, propone mejoras y detecta errores. Antes de implementar, confirma con el usuario si espera que escribas el código.
- Los integrantes vienen de Java/C# y son nuevos en Python y pytest: explica las diferencias cuando sea relevante.
- Una tarea por sesión; lo demás se anota en la bitácora.

## Mantenimiento del contexto (proactivo, con aprobación)

Nunca edites AGENTS.md, docs/contexto.md ni los anexos de docs/ por iniciativa propia.
Cuando detectes algo que valga la pena recordar, PROPÓNLO al final de tu respuesta.

### Cuándo proponer
- Aparece un comando nuevo (cómo correr pruebas, el sistema, un script).
- Cambia la estructura de carpetas o se crea un módulo nuevo.
- Se adopta una convención de código (nombres, formato de hechos, estilo de pruebas).
- Se toma una decisión de diseño → va a docs/decisiones.md (siguiente número Dxx).
- Aparece una sigla o término nuevo → va a docs/glosario.md.
- Se crea o cambia una regla del motor → va a docs/reglas.md.
- El usuario me corrige algo, o un error se repite → trampa en docs/contexto.md.
- Empieza un sprint nuevo → actualizar "Estado actual" en docs/contexto.md.
- Empieza o termina un sprint (o el usuario menciona "retro", "planning" o
  "cierre de sprint") → ofrece ejecutar /retro antes de seguir con otra tarea.
- Si docs/contexto.md tiene más de 60 líneas o una trampa lleva más de un sprint
  sin ser relevante → propón la poda aunque no sea fin de sprint.
- Sugerencia (Además puedes sugerir cambios según tu criterio)

### Cómo proponer
Usa exactamente este formato, máximo 2 propuestas por respuesta:

> 📌 **Propuesta de contexto**
> - **Archivo:** docs/contexto.md → sección "Trampas"
> - **Texto:** `<texto exacto a agregar o reemplazar>`
> - **Por qué:** <una frase>
> ¿Lo agrego? (sí / no / editar)

Solo escribe después de un "sí". Si dicen "no", no vuelvas a proponerlo.
No propongas cosas triviales ni lo que ya está documentado.

