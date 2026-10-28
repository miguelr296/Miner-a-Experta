# 6. Tablero Kanban

[← Índice](../../README.md)

## 6.1 Herramienta

**GitHub Projects** (tablero del propio repositorio).

- Cada tarjeta es un **Issue** de GitHub.
- Cada sprint es una **Iteración** (campo de tipo *Iteration* de 2 semanas).
- Al abrir un PR se escribe `Closes #N` y la tarjeta se cierra sola al hacer merge.
- Gratis, vinculado al código y visible en el portafolio.

## 6.2 Columnas

| Columna | Qué contiene | Límite WIP |
|---|---|---|
| **Backlog** | Historias de sprints futuros, sin detallar | — |
| **Ready** | Tareas detalladas del sprint actual, pendientes de empezar | — |
| **In Progress** | Lo que alguien está trabajando ahora | **1 por persona** |
| **In Review** | PR abierto esperando revisión del compañero | **2** |
| **Done** | Cumple la [definición de terminado](sprints.md#54-definición-de-terminado-dod) | — |

**Límite WIP** (*work in progress*): máximo de tarjetas en una columna. Con 1 tarea en curso por persona se cumple la regla "una tarea por sesión" del flujo de trabajo. Si **In Review** llega a 2, se revisa antes de empezar algo nuevo.

## 6.2.1 Configuración de GitHub Projects (una sola vez)

En GitHub Projects **las columnas del tablero son las opciones del campo `Status`**. No se crean solas: dependen de la plantilla elegida y hay que ajustarlas.

1. **Crear el proyecto:** perfil → *Projects* → *New project* → *Featured* → plantilla **Kanban**. Trae las columnas Backlog, Ready, In Progress, In Review y Done, y permite límites por columna. Si quedó un proyecto vacío creado antes (*untitled project*), se borra para no tener dos.
2. **Vincular el repositorio:** en el repo → pestaña *Projects* → *Link a project*.
3. **Columnas:** mantener en inglés las opciones predeterminadas del campo `Status` (*Settings → Status*): Backlog, Ready, In Progress, In Review y Done.
4. **Límites WIP:** menú **⋯** de la columna → *Set limit* (In Progress: 2, uno por persona; In Review: 2). GitHub solo lo muestra en rojo, no lo impide.
5. **Campos personalizados** (*Settings → New field*):
   - `Sprint` → tipo *Iteration*, duración 2 semanas, fecha de inicio del sprint 1.
   - `Estimación` → tipo *Number* (horas). Si la plantilla ya trae un campo de tamaño o estimación, se reutiliza en lugar de crear otro.
   - `Prioridad` → tipo *Single select*: Núcleo, Si alcanza.
   - El dueño se asigna con *Assignees* (ya existe).
6. **Etiquetas (labels)** en el repo → *Issues → Labels*: `aprendizaje`, `codigo`, `pruebas`, `docs`, `configuracion`.
7. **Automatizaciones** (menú **⋯** del proyecto → *Workflows*): activar *Item closed → Done*, *Pull request merged → Done* y *Auto-add to project* (filtrando el repo).
8. **Cargar tarjetas:** en la columna *Ready* → *+ Add item* → escribir el título → Enter. Se crea un **borrador**; con **⋯ → Convert to issue** se convierte en Issue para poder cerrarlo con un PR.

> Si la interfaz no coincide con estos pasos (GitHub la cambia con frecuencia), se compara con una captura de pantalla antes de improvisar.

### Cómo se aprende GitHub Projects

- **Antes de configurar** (`S1-00`): guía oficial *Quickstart for Projects* de GitHub Docs (30 min).
- **Configurando** (`S1-03`, `S1-03b`): se aprende haciendo, siguiendo los pasos de arriba.
- **Usándolo** (`S1-04`): el PR de práctica se vincula a una tarjeta con `Closes #N` para comprobar que la automatización funciona.

## 6.2.2 Cargar una tarjeta paso a paso (ejemplo: `S1-11`)

1. En la columna **Ready** → **+ Add item** → escribir el título con su ID: `S1-11 Implementar cargador JSON de la mina` → Enter.
2. Abrir la tarjeta (clic en el título) → **⋯ → Convert to issue** → elegir el repositorio.
3. En el Issue, pegar en la descripción la plantilla de 6.3 y completarla con los datos de la tabla de la sección 7:
   - Criterio de aceptación: *Carga `mina_prueba.json` y crea todos los nodos y aristas*.
   - Depende de: `S1-09`, `S1-10` (cuando existan, se escriben como `#N`).
4. En el panel derecho de la tarjeta:
   - **Assignees** → B.
   - **Labels** → `codigo`.
   - **Sprint** → Sprint 1.
   - **Estimación** → 1,5.
   - **Prioridad** → Núcleo.
5. Repetir con todas las filas de la sección 7, creando **una tarjeta por tarea**. Si los dueños son A y B (indicados como `A y B` o `A + B` sin responsable principal), asignar a ambos a esa misma tarjeta; no duplicarla ni agregar sufijos por persona.
6. Verificar: el tablero filtrado por `Sprint: Sprint 1` debe mostrar 20 tarjetas en total, una por cada tarea, y la suma de estimaciones por persona debe coincidir con la tabla de carga.

## 6.3 Cómo se define una tarea

### Jerarquía

```
Objetivo del sprint  →  Historias (funcionalidades)  →  Tareas (tarjetas)
"motor mínimo"           "motor con refracción"          "S1-13 Ciclo de disparo con refracción"
```

### Reglas para escribir una tarjeta

1. **Título = verbo + resultado.** "Implementar cargador JSON", no "Cargador".
2. **Tamaño: 1 a 3 horas.** Cabe en una sesión. Si es más grande, se divide.
3. **Una tarjeta por tarea.** Si la tabla indica A y B, o A + B sin responsable principal, asignar a ambos integrantes a la misma tarjeta; si indica un solo dueño, asignar solo a esa persona. En trabajo conjunto con responsable explícito (p. ej., A + B, dueño B), el responsable sigue siendo quien responde por la tarea.
4. **Criterio de aceptación verificable:** una frase que diga cómo saber que está terminada.
5. **Dependencias explícitas** si no puede empezar antes que otra.

### Campos de la tarjeta

| Campo | Ejemplo |
|---|---|
| ID | `S1-11` |
| Título | Implementar cargador JSON de la mina |
| Tipo (etiqueta) | 📚 aprendizaje · ⚙️ código · 🧪 pruebas · 📝 docs · 🔧 configuración |
| Dueño | B o A y B |
| Estimación | 2 h |
| Criterio de aceptación | Carga `mina_prueba.json` y crea todos los nodos y aristas |
| Depende de | `S1-08`, `S1-10` |
| Prioridad | Núcleo / Si alcanza |

### Plantilla para el cuerpo del Issue

```
**Dueño:** A / B / A y B / A + B (sin responsable principal)
**Estimación:** _ h
**Depende de:** #_
**Prioridad:** Núcleo / Si alcanza

**Criterio de aceptación:**
- [ ] ...

**Notas:**
```

## 6.4 Cantidad de tareas por sprint

Con 18 h de tareas por persona y tarjetas de 1–3 h (≈ 2 h promedio):

| Cantidad | Tarjetas por sprint (equipo) | Efecto |
|---|---|---|
| Pocas | < 8 | Tarjetas de 5–10 h: no se ve el avance hasta el final y los atrasos se detectan tarde |
| **Regular (recomendado)** | **15–20** | 1 tarjeta ≈ 1 sesión; el tablero muestra el avance real cada día |
| Muchas | > 35 | Más tiempo administrando tarjetas que trabajando |

## 6.4.1 Qué va en el Backlog

| Va en el Backlog | No va en el Backlog |
|---|---|
| Historias de los sprints 2, 3 y 4 (de [sprints.md](sprints.md)), con prefijo: `S2-H01 Dijkstra con costos dinámicos` | Tareas del sprint 1: van directo a **Ready** con `Sprint = Sprint 1` |
| Elementos del Nivel 3 (`N3 Interfaz Streamlit`, `N3 Simulación por turnos`, `N3 Sensor defectuoso`) | Ideas sin relación con el alcance (se descartan o se anotan en la bitácora) |
| Errores o mejoras detectados durante el trabajo que no son del sprint actual | |

- Se cargan como **borradores** (sin convertir en Issue) y sin estimación fina: solo título.
- En cada planning, las historias del sprint que empieza se dividen en tareas de 1–3 h, se convierten en Issues y pasan a **Ready**. La historia original se archiva.

### Títulos listos para copiar al Backlog

```
S2-H01 Reglas del núcleo (15) con pruebas
S2-H02 Explicación "¿por qué?"
S2-H03 JSON de configuración de umbrales
S2-H04 Conectar motor con costos de aristas
S2-H05 Dijkstra con costos dinámicos
S2-H06 Línea base con filtro por umbral
S2-H07 Validar refugio a ≤ 500 m
S2-H08 Salida por consola
S2-H09 3 escenarios JSON
S2-H10 Integración de punta a punta
S3-H01 Factores de certeza en el motor
S3-H02 Explicación "¿cómo?"
S3-H03 Reglas de decisión (evacuar / refugiarse / esperar)
S3-H04 Conflictos de reglas (incluye Art. 248 con ANFO)
S3-H05 A* con heurística admisible
S3-H06 Varios mineros
S3-H07 Escenarios de conflicto
S3-H08 Métricas contra la línea base
S4-H01 Corrección de errores
S4-H02 README de ejecución y capítulos pendientes
S4-H03 Guion y ensayo de la demo
N3 Interfaz Streamlit
N3 Simulación por turnos
N3 Detección de sensor defectuoso
N3 MkDocs + GitHub Pages
```

Se cargan como borradores en **Backlog** (+ Add item, sin convertir en Issue), sin dueño ni estimación.

## 6.5 Cuándo se crean las tareas

- **Solo el sprint actual** se detalla en tareas. Los sprints futuros quedan como historias en el Backlog.
- En cada **planning** se convierten las historias del sprint en tarjetas, usando la velocidad real medida en la retro anterior.
- Motivo: con principiantes, las estimaciones cambian mucho tras el primer sprint; detallar todo ahora sería trabajo perdido.

## 6.6 Prioridad dentro del sprint

- **Núcleo:** sin esto no se cumple el objetivo del sprint.
- **Si alcanza:** se hace solo si el núcleo está terminado. Es lo primero que se recorta.

## 7. Sprint 1 — tareas

**Objetivo:** el motor dispara 2–3 reglas encadenadas y deja traza; la mina se carga desde JSON; ambos trabajan con ramas y PR.

Las tareas de aprendizaje con dueño A y B se crean como **una tarjeta compartida**, asignada a ambos integrantes.

| ID | Tarea | Tipo | Dueño | Est. | Criterio de aceptación | Depende de | Prioridad |
|---|---|---|---|---|---|---|---|
| S1-00 | Aprender GitHub Projects: guía oficial *Quickstart for Projects* + recorrido del tablero | 📚 | A y B | 0,5 h c/u | Saber crear una tarjeta, moverla entre columnas, asignarla, ponerle sprint y estimación, y filtrar el tablero por sprint | — | Núcleo |
| S1-01 | Python para quien viene de Java/C#: sintaxis, indentación, tipado dinámico, funciones, listas, diccionarios, tuplas, conjuntos y comprensiones | 📚 | A y B | 2 h c/u | Reescribir en Python 3 ejercicios que ya sepan hacer en Java/C# | — | Núcleo |
| S1-02 | Clases y módulos en Python: `__init__`, `self`, `@dataclass`, imports entre archivos | 📚 | A y B | 1,5 h c/u | Una clase propia en un módulo, importada y usada desde otro archivo | S1-01 | Núcleo |
| S1-03 | Crear el repositorio, subir la documentación y configurar GitHub Projects (pasos 1–7 de 6.2.1) | 🔧 | A | 1 h | Repo con el contenido actual, compañero invitado, tablero con columnas, campos, etiquetas y automatizaciones | — | Núcleo |
| S1-03b | Cargar las tarjetas del sprint 1 en el tablero (paso 8) | 🔧 | B | 1 h | 20 tarjetas en total, una por tarea, convertidas en Issues, con dueño, estimación, prioridad y sprint | S1-03 | Núcleo |
| S1-04 | Aprender Git y GitHub: clonar, rama, commit, push, PR **vinculado a una tarjeta** | 📚 | A y B | 1,5 h c/u | Cada uno abrió un PR de prueba con `Closes #N`, el otro lo revisó, y al fusionarlo la tarjeta pasó sola a *Done* | S1-03b | Núcleo |
| S1-05 | Aprender a leer y escribir JSON en Python | 📚 | A y B | 1 h c/u | Script personal que lee un JSON y muestra sus datos | S1-02 | Núcleo |
| S1-06 | Aprender pytest básico | 📚 | A y B | 1 h c/u | Una prueba que pasa y otra que falla a propósito | S1-02 | Núcleo |
| S1-07 | Leer forward chaining y refracción (documentación del proyecto + glosario) | 📚 | A y B | 1 h c/u | Explicar al compañero el ciclo del motor sin mirar notas | — | Núcleo |
| S1-08 | Diseñar el esquema JSON de la mina (sesión conjunta) | 📝 | A + B (dueño B) | 1,5 h c/u | Esquema documentado en `decisiones.md`: nodos con coordenadas en metros, tipos, aristas | S1-05 | Núcleo |
| S1-09 | Crear `mina_prueba.json` (6–8 nodos, 1 refugio a ≤ 500 m) | ⚙️ | A | 1 h | Archivo válido que respeta el esquema | S1-08 | Núcleo |
| S1-10 | Implementar clases `Nodo`, `Arista` y `Mina` | ⚙️ | B | 2 h | Se puede crear una mina en código y consultar los vecinos de un nodo | S1-02 | Núcleo |
| S1-11 | Implementar cargador JSON de la mina | ⚙️ | B | 1,5 h | Carga `mina_prueba.json` y crea todos los nodos y aristas | S1-09, S1-10 | Núcleo |
| S1-12 | Diseñar las clases `Hecho` y `Regla` | 📝 | A | 1,5 h | Diseño y pseudocódigo en `decisiones.md` | S1-07 | Núcleo |
| S1-13 | Motor mínimo I: memoria de trabajo y búsqueda de reglas aplicables (en pareja) | ⚙️ | A | 2 h c/u | Dada una lista de hechos, el motor devuelve las reglas cuyas condiciones se cumplen | S1-12 | Núcleo |
| S1-14 | Motor mínimo II: ciclo de disparo, refracción y traza (en pareja) | ⚙️ | A | 2 h c/u | 2–3 reglas encadenadas se disparan una sola vez y la traza se imprime | S1-13 | Núcleo |
| S1-15 | Prueba pytest del motor mínimo | 🧪 | A | 1 h | La prueba verifica la cadena de reglas y pasa | S1-14, S1-06 | Si alcanza |
| S1-16 | Pruebas pytest del cargador | 🧪 | B | 1 h | 2 pruebas pasan (mina válida y archivo con error) | S1-11, S1-06 | Si alcanza |
| S1-17 | Borrador de 5 reglas en el catálogo | 📝 | A | 1 h | 5 reglas con la plantilla completa, sin código | — | Si alcanza |
| S1-18 | Review + retro, capítulos de las semanas 1 y 2, tag `semana-02` | 📝 | A + B | 1 h c/u | Capítulos escritos, horas reales anotadas, tag creado | todo lo anterior | Núcleo |

### Carga por persona

| | Núcleo | Si alcanza | Total |
|---|---|---|---|
| **A** | 18,5 h | 2 h | 20,5 h |
| **B** | 19,5 h | 1 h | 20,5 h |

El núcleo queda prácticamente en la capacidad (≈ 18 h); B la excede en 1,5 h, que absorbe el colchón del fin de semana. Si en el sync de la semana 1 van atrasados, `S1-11` (cargador) pasa al inicio del sprint 2: el motor mínimo puede probarse con hechos escritos a mano.

Son 20 tareas y 20 tarjetas: cada tarjeta representa una tarea; cuando el dueño es A y B, ambos comparten la misma tarjeta. El sprint 1 queda en el límite alto de lo recomendado porque tiene mucho aprendizaje en tareas pequeñas.

### Orden sugerido

El criterio no es el número del issue: primero las **dependencias** (lo que desbloquea a otros), después lo que hay que **aprender justo antes de usarlo** y al final lo **opcional** (`Si alcanza`). Las tareas de aprendizaje van en paralelo; las sesiones conjuntas se reservan para lo que requiere a los dos.

```
Semana 1:  S1-00 → S1-03 → S1-03b → S1-01 → S1-04 → S1-02 → S1-05 → S1-07 → S1-08 (sesión conjunta) → S1-09 (A)
Semana 2:  A: S1-12 → S1-06      B: S1-10 → S1-11 → S1-06
           Juntos: S1-13 → S1-14 → S1-18
           Si alcanza: S1-15, S1-16, S1-17
```
