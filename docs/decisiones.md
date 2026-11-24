# Anexo B — Registro de decisiones

[← Índice](../README.md)

Las decisiones [D22 y D23](motor-python.md#d22--factores-de-certeza-en-la-traza) documentan la certeza y la heurística de A* en el informe de implementación.

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

## D21 — Refracción por firma de activación
**Fecha:** 2026-11-24
**Decisión:** la refracción se implementa guardando la firma `(regla_id, frozenset(hechos que la activaron))`. Una regla no se dispara dos veces con los mismos hechos, pero sí puede volver a dispararse si la activan hechos distintos. No se usa un indicador `disparada = True` por regla.
**Alternativas:** marcar la regla como disparada para siempre (simple, pero la deja muerta el resto de la ejecución y rompe escenarios con varios mineros o varios túneles).
**Por qué:** el escenario puede tener varios túneles y varios mineros; una regla de costo debe disparar una vez por arista. La firma es además la justificación que necesita la explicación "¿por qué?".
**Consecuencias:** un hecho debe ser hashable (tupla o `dataclass(frozen=True)`); la refracción se consulta en el paso de reconocimiento; S1-13 y S1-14 se implementan sobre esta decisión.

## D22 — Esquema JSON de la mina

**Fecha:** 2026-11-24
**Decisión:** la mina se describe en un JSON con tres bloques: `meta`, `nodos` y `aristas`. El grafo es no dirigido, la altura y la longitud de cada arista se calculan y no se guardan, y los identificadores son descriptivos pero el cargador nunca los interpreta.

**Estructura:**

| Bloque | Campo | Obligatorio | Significado |
|---|---|---|---|
| `meta` | `nombre` | sí | Nombre de la mina. |
| `meta` | `version` | sí | Versión del esquema; permite evolucionarlo sin adivinar. |
| `meta` | `unidad` | sí | Siempre `"m"`: evita mezclar metros con pies. |
| `meta` | `altura_nivel_m` | sí | Separación vertical entre niveles (30 m, **SUPUESTO** del equipo). |
| `nodos` | `id` | sí | Identificador único y legible. |
| `nodos` | `x`, `y` | sí | Posición en metros dentro del nivel. |
| `nodos` | `nivel` | sí | Nivel de la mina, entero ≥ 1. |
| `nodos` | `tipo` | sí | `interseccion`, `salida`, `refugio` o `frente`. |
| `nodos` | `nombre` | no | Texto para la salida por consola. |
| `aristas` | `id` | sí | Identificador único y legible. |
| `aristas` | `desde`, `hasta` | sí | Nodos que conecta. |
| `aristas` | `labor` | no | `galeria` (por defecto), `rampa`, `chimenea` o `crucero`. |

**Por qué cada pieza:**

- **`nivel` es la coordenada y `z` se deduce.** `nivel` es una etiqueta (Nivel 1, Nivel 2), no una altura en metros, y para calcular distancias en 3D hace falta una altura. Se deduce con `z = -(nivel - 1) * altura_nivel_m` en vez de guardar `z` en cada nodo, porque dos datos para lo mismo terminan contradiciéndose: alguien mueve un nodo al Nivel 2 y deja el `z` viejo. Es la misma razón por la que no se guarda un campo calculado en Java/C#. Consecuencia: dos nodos en niveles distintos solo pueden unirse por una rampa o una chimenea, no por una galería.
- **`altura_nivel_m` es un SUPUESTO del equipo.** La norma no fija la separación entre niveles de una mina concreta; 30 m es una elección razonable y debe presentarse como tal (mismo criterio que D11 y D12).
- **La longitud se calcula, no se guarda.** `longitud(a, b) = math.dist((a.x, a.y, a.z), (b.x, b.y, b.z))`, igual que en el ejercicio de S1-02. Si se guardara, mover un nodo dejaría longitudes falsas y el planificador elegiría rutas por datos viejos. Además el modelo asume túneles rectos: la distancia recta es menor o igual que la longitud real de un túnel curvo, así que la heurística euclidiana nunca sobreestima el costo y sigue siendo admisible (D01).
- **El grafo es no dirigido.** Un túnel se recorre en ambos sentidos. Cada arista se escribe una sola vez y el cargador la agrega a la lista de adyacencia en las dos direcciones (como un `addEdge(a, b)` que hace `adj.get(a).add(b)` y `adj.get(b).add(a)`). Guardarla dos veces duplica los datos y permite olvidar una dirección; con una sola arista, el hecho `(tunel_int_1_int_2, cerrado, True)` cierra el túnel en ambos sentidos sin casos especiales. No se agrega un campo `dirigida`: si algún día hace falta un túnel de un solo sentido, se documenta como cambio de esquema.
- **Los identificadores son descriptivos y no se parsean.** El `id` aparece en los hechos, en la traza y en la explicación "¿por qué?", así que debe ser estable y legible: `n1`/`e1` harían ilegible la traza. Convención: nodo `<prefijo_tipo>_<n>` (`int_1`, `ref_1`, `frente_1`); arista `<labor>_<idA>_<idB>` (`tunel_int_1_int_2`, `rampa_int_1_sal_1`). El cargador **nunca** deduce el tipo leyendo el prefijo: el tipo real está en `tipo` y en `labor`. Parsear identificadores para sacar información es una trampa clásica y rompe el código en cuanto alguien renombra un nodo.
- **`refugio` es un tipo de nodo, no un atributo.** Un refugio real es una cámara aparte al final de un tramo corto, no una intersección con etiqueta. Modelarlo como nodo propio permite que el planificador calcule una ruta hasta él, que es exactamente lo que necesita la decisión "refugiarse". Con un booleano `es_refugio` habría que buscar un nodo cercano, más código y más confusión.
- **`labor` es opcional, con `galeria` por defecto.** Las reglas de ventilación del Nivel 2 pueden necesitar distinguir una rampa de una galería (el aire no se comporta igual), pero S1-09 no debe quedar bloqueada por un campo que todavía no se usa. Al ser opcional, la mina de prueba se escribe sin él y el cargador asume galería.
- **La mina y el escenario son archivos distintos.** La mina es estructura estática; los mineros, sensores y eventos son el estado de una emergencia concreta. Separarlos permite reutilizar la misma mina en los tres escenarios del Nivel 1; mezclarlos obligaría a duplicar la mina tres veces.

**Qué valida el cargador y qué no:**

El cargador valida la **forma** del JSON, no las restricciones de seguridad del modelo:

1. `nodos` y `aristas` existen y no están vacías.
2. `id` único entre nodos y único entre aristas.
3. Todo `desde`/`hasta` apunta a un nodo existente.
4. Sin bucles (`desde == hasta`) ni aristas duplicadas (mismo par de nodos).
5. `tipo` dentro de la lista cerrada; `nivel` entero ≥ 1.
6. Al menos una `salida` y al menos un `frente`.

El error debe indicar el campo culpable, por ejemplo: `arista tunel_int_1_int_9: el nodo 'int_9' no existe`.

**La regla de los 500 m (D10) no la valida el cargador.** Es una restricción de seguridad, no de forma, y comprobarla exige recorrer el grafo con distancias: eso llega con el planificador, más tarde en el sprint. Se verifica a mano al crear la mina (S1-09) y con una prueba cuando exista el planificador. Ponerla en el cargador obligaría a escribir Dijkstra antes de tiempo y a mezclar dos responsabilidades.

**Ejemplo mínimo:**

```json
{
  "meta": { "nombre": "Mina de prueba", "version": 1, "unidad": "m", "altura_nivel_m": 30 },
  "nodos": [
    { "id": "int_1",    "x": 0,   "y": 0,  "nivel": 1, "tipo": "interseccion" },
    { "id": "int_2",    "x": 120, "y": 0,  "nivel": 1, "tipo": "interseccion" },
    { "id": "ref_1",    "x": 120, "y": 40, "nivel": 1, "tipo": "refugio" },
    { "id": "frente_1", "x": 260, "y": 0,  "nivel": 1, "tipo": "frente" },
    { "id": "sal_1",    "x": -30, "y": 0,  "nivel": 2, "tipo": "salida" }
  ],
  "aristas": [
    { "id": "tunel_int_1_int_2",    "desde": "int_1", "hasta": "int_2" },
    { "id": "tunel_int_2_ref_1",    "desde": "int_2", "hasta": "ref_1" },
    { "id": "tunel_int_2_frente_1", "desde": "int_2", "hasta": "frente_1" },
    { "id": "rampa_int_1_sal_1",    "desde": "int_1", "hasta": "sal_1", "labor": "rampa" }
  ]
}
```

Con este ejemplo, `tunel_int_1_int_2` mide 120 m, `rampa_int_1_sal_1` mide ≈ 42,4 m (30 m horizontales y 30 m de desnivel) y la arista `tunel_int_2_ref_1` es la que usa la regla de refugio.

**Alternativas consideradas:**

1. Guardar `z` en cada nodo en vez de deducirlo de `nivel`: descartada, crea dos fuentes de verdad que pueden contradecirse.
2. Guardar `longitud` en cada arista: descartada, se desincroniza si alguien mueve un nodo.
3. Escribir cada arista en los dos sentidos: descartada, duplica los datos y permite olvidar una dirección.
4. `refugio` como atributo booleano de una intersección: descartada, el planificador necesita un nodo destino al que calcular la ruta de refugio.
5. `id` numéricos (`n1`, `e1`): descartados, hacen ilegible la traza y la explicación.
6. Validar los 500 m dentro del cargador: descartada, exige el planificador antes de tiempo y mezcla forma con seguridad.

**Por qué:** un solo origen para cada dato evita inconsistencias; el grafo no dirigido y la longitud derivada hacen que las reglas (D01) y el planificador compartan una única noción de costo; y separar mina de escenario permite reutilizar la estructura en los tres escenarios del Nivel 1.

**Consecuencias:**
- S1-10 implementa `Nodo` (con `z` y `distancia_a`) y `Arista` (con `longitud` como propiedad calculada), sin guardar valores derivados.
- S1-11 valida la estructura y lanza `ValueError` con el campo culpable; no valida D10.
- S1-16 prueba una mina válida y un archivo con error (nodo inexistente o `tipo` inválido).
- La heurística euclidiana 3D del Nivel 2 usa la misma fórmula, sin cambios de esquema.

