# Anexo B — Registro de decisiones

[← Índice](../README.md)

Formato: fecha · decisión · alternativas consideradas · por qué.

## D01 — Las reglas solo aumentan costos
**Fecha:** 2026-10-17
**Decisión:** las reglas solo pueden cerrar un túnel o multiplicar su costo por un factor ≥ 1.
**Alternativas:** permitir que las reglas reduzcan costos.
**Por qué:** mantiene la distancia euclidiana como heurística admisible, por lo que A\* sigue encontrando la ruta óptima.

## D02 — Datos en JSON, sin base de datos
**Fecha:** 2026-10-17
**Decisión:** la mina y los escenarios se definen en archivos JSON.
**Por qué:** simple, legible y suficiente para el tamaño del problema.

## D03 — Motor y planificador propios
**Fecha:** 2026-10-17
**Decisión:** no se usan librerías de sistemas expertos ni de rutas.
**Por qué:** el objetivo del curso es entender y defender cómo funciona el razonamiento.

## D04 — Mina metálica peruana
**Fecha:** 2026-10-17
**Decisión:** dominio de mina metálica (CO, NO₂, O₂, ventilación, incendio y caída de rocas como evento reportado), no de carbón.
**Por qué:** realismo local. Ningún integrante tiene formación en minería o geología, por eso la caída de rocas no lleva razonamiento geomecánico.

## D05 — Normativa solo como fuente de umbrales
**Fecha:** 2026-10-17
**Decisión:** el DS 024-2016-EM se usa para citar umbrales, no se modela completo.
**Por qué:** el equipo no tiene experto en el dominio ni entrevistas; la norma cumple el rol de fuente experta y da fundamento citable a las reglas, con un costo de 2–3 h.

## D06 — Línea base fuerte
**Fecha:** 2026-10-17
**Decisión:** comparar contra Dijkstra con filtro por umbral de sensor, no contra Dijkstra ciego.
**Por qué:** una línea base ciega siempre pierde y no prueba el aporte del encadenamiento.

## D07 — Prioridades del curso
**Fecha:** 2026-10-17
**Decisión:** factores de certeza en Nivel 2; simulación temporal en Nivel 3.
**Por qué:** el curso es de Sistemas Expertos; la certeza y la explicación son centrales, la simulación no.

## D08 — Documentación como informe en el repositorio
**Fecha:** 2026-10-17
**Decisión:** Markdown en `docs/` + tags por semana (opciones A + B). MkDocs opcional al final.
**Por qué:** costo casi nulo; GitHub lo muestra como informe y los tags dan la cronología del código.

## D09 — Niveles de riesgo según el tipo de límite
**Fecha:** 2026-10-17
**Decisión:** los gases no se tratan como "bajo/sobre el umbral", sino en niveles: bajo TWA (normal), sobre TWA (alerta), sobre STEL o techo (riesgo alto). El nivel de "peligro inmediato" (cierre del túnel) se resolvió en D12.
**Alternativas:** un solo umbral por gas.
**Por qué:** la norma da límites de exposición laboral de 8 h y 15 min, no de emergencia. Cerrar un túnel solo por superar el TWA sería incorrecto. Los niveles encajan con la decisión D01: cada nivel aumenta el costo de la arista.

## D10 — Refugio a 500 m como restricción del modelo de mina
**Fecha:** 2026-10-17
**Decisión:** al diseñar la mina en JSON, todo frente de trabajo tendrá un refugio a no más de 500 m de recorrido.
**Por qué:** lo exige el Anexo 19. Da realismo a la mina y garantiza que la decisión "refugiarse" siempre tenga una opción válida.

## D11 — Distinción entre conocimiento normativo y supuestos
**Fecha:** 2026-10-17
**Decisión:** cada regla del catálogo indica si su fuente es `NORMA` o `SUPUESTO`.
**Por qué:** el equipo no cuenta con un experto. Separar lo citado de lo razonado hace defendible la base de conocimiento.

## D12 — Peligro inmediato como supuesto del equipo
**Fecha:** 2026-10-17
**Decisión:** el nivel que cierra un túnel por gases es un `SUPUESTO`: 2 × el valor de riesgo alto (STEL/techo, o 2 × TWA si no hay STEL). Para el O₂: < 18 % riesgo alto y < 16 % peligro inmediato.
**Alternativas:** usar los valores IDLH de NIOSH como segunda fuente citable.
**Por qué:** más rápido y suficiente para una simulación académica. Debilidad aceptada: son valores arbitrarios y deben presentarse como tales en la defensa.

## D13 — Umbrales configurables
**Fecha:** 2026-10-17
**Decisión:** los umbrales y niveles se guardarán en un archivo JSON de configuración, no escritos dentro del código.
**Por qué:** separa el conocimiento del motor (principio de los sistemas expertos) y permite cambiar un supuesto sin reprogramar, lo que reduce la debilidad de D12.

## D14 — Glosario obligatorio
**Fecha:** 2026-10-17
**Decisión:** toda sigla o término técnico se define en `docs/glosario.md` en la misma sesión en que aparece.
**Por qué:** el equipo no tiene formación en minería; sin glosario el informe no se puede leer ni defender.

## D15 — Sprints de 2 semanas
**Fecha:** 2026-10-17
**Decisión:** 4 sprints de 2 semanas; capacidad de ≈ 18 h de tareas por persona y sprint (≈ 2 h van a ceremonias).
**Alternativas:** 8 sprints de 1 semana.
**Por qué:** las ceremonias cuestan la mitad de veces y cada sprint termina en un punto de decisión (semanas 4 y 6).

## D16 — Kanban en GitHub Projects
**Fecha:** 2026-10-17
**Decisión:** tablero con columnas Backlog / Por hacer / En curso / En revisión / Hecho; tarjetas de 1–3 h; WIP de 1 tarea en curso por persona; 15–20 tareas por sprint; solo se detalla el sprint actual. Los nombres de las columnas se actualizaron posteriormente (ver D20).
**Alternativas:** Trello o tabla en Markdown.
**Por qué:** vincula tarjetas con PR y código, es gratis y queda como evidencia en el portafolio.

## D17 — Recalibración por base en Java/C#
**Fecha:** 2026-10-17
**Decisión:** el aprendizaje de Python se enfoca en las diferencias con Java/C# (4 h → 3,5 h por persona en el sprint 1); el descuento por aprendizaje del alcance baja de 30–35 % a 20–25 %.
**Por qué:** ambos integrantes dominan los fundamentos de programación en Java y C#; lo nuevo es la sintaxis y el estilo de Python, no la lógica.

## D18 — Sprints como Iteraciones de GitHub Projects
**Fecha:** 2026-10-17
**Decisión:** los sprints se representan con un campo *Iteration* de 2 semanas, no con Milestones.
**Por qué:** es el mecanismo nativo de GitHub Projects para sprints y permite filtrar el tablero por sprint.

## D19 — Tareas de tablero sin PR
**Fecha:** 2026-10-24
**Decisión:** las tareas que no tocan archivos del repositorio (solo el tablero o la configuración de GitHub) se cierran directamente, sin PR, y la excepción se anota en la bitácora. Las tareas con cambios en el repositorio siguen pasando por PR revisado.
**Por qué:** la DoD exige PR para todas las tareas, pero el tablero no vive en el repositorio; pedir un PR sin cambios reales sería trámite vacío.

## D20 — Columnas en inglés y una tarjeta por tarea compartida
**Fecha:** 2026-10-25
**Decisión:** mantener los nombres predeterminados en inglés (Backlog, Ready, In Progress, In Review y Done). Crear una tarjeta por tarea; cuando A y B son dueños compartidos, asignar a ambos a la misma tarjeta, sin duplicarla.
**Alternativas:** traducir los nombres de las columnas y crear tarjetas separadas para cada integrante en las tareas compartidas.
**Por qué:** conserva las opciones predeterminadas de GitHub Projects y evita duplicar el seguimiento de una misma tarea. Para Sprint 1 son 20 tareas y 20 tarjetas.

