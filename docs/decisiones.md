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
**Decisión:** tablero con columnas Backlog / Por hacer / En curso / En revisión / Hecho; tarjetas de 1–3 h; WIP de 1 tarea en curso por persona; 15–20 tareas por sprint; solo se detalla el sprint actual.
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

## D20 — Contrato JSON de la mina estática, versión 1
**Fecha:** 2026-10-25
**Decisión:** usar `version`, `nombre`, `nodos` y `aristas`. Los nodos tienen `id`, `x`, `y`, `nivel` (coordenadas en metros) y `tipo`; las aristas tienen `id`, `origen`, `destino` y `longitud_m`. Los tipos son `interseccion`, `salida`, `refugio` y `frente`. Los túneles son bidireccionales, sin bucles ni pares repetidos; sus longitudes físicas son positivas y al menos la distancia recta 3D. Superficie en cota 0, subsuelo en cotas negativas. Sensores, mineros, emergencias y umbrales quedan separados de la estructura fija.
**Alternativas:** derivar siempre la longitud de las coordenadas; permitir túneles dirigidos desde el primer entregable; mezclar estado de emergencia y geometría en un archivo.
**Por qué:** permite túneles cuyo recorrido supera la línea recta, conserva la futura heurística admisible y evita mezclar datos permanentes con inferencias. El esquema valida la estructura; S1-11 validará referencias, unicidad, geometría, conectividad y la restricción D10 de 500 m por recorrido. Detalles en [S1-08](plan/esquema-mina.md) y contrato en [mina.schema.json](../data/esquemas/mina.schema.json).

## D21 — Modelo estático inmutable y vecinos bidireccionales
**Fecha:** 2026-10-25
**Decisión:** `Nodo` y `Arista` son clases de datos inmutables; `Mina` copia las colecciones de entrada y ofrece consultas de solo lectura por identificador. `vecinos(id)` devuelve pares `(Nodo, Arista)` en ambos sentidos, conservando el orden de entrada. El constructor valida la coherencia local; S1-11 verificará los requisitos globales de una mina completa.
**Alternativas:** diccionarios modificables accesibles al llamador; reconstruir las conexiones recorriendo todos los túneles en cada consulta.
**Por qué:** evita que cambios externos invaliden las conexiones ya construidas y permite consultar vecinos y longitudes sin mezclar la geometría con el futuro estado de emergencia.

## D22 — Carga estricta y comprobación global de la mina
**Fecha:** 2026-10-25
**Decisión:** cargar UTF-8 con biblioteca estándar, rechazando claves JSON repetidas y constantes no estándar. Validar campos antes de construir el modelo; exigir conectividad, frente, salida, refugio y D10. Comprobar D10 mediante búsqueda propia por distancia desde todos los refugios, limitada a 500 m.
**Alternativas:** depender de JSON Schema durante la ejecución; comprobar D10 solo por distancia recta.
**Por qué:** evita archivos ambiguos y dependencias de ejecución adicionales; el límite se refiere al recorrido real. El esquema de desarrollo sigue siendo una comprobación independiente del formato.

## D23 — Motor mínimo por entidad con traza y refracción
**Fecha:** 2026-10-25
**Decisión:** conservar hechos como tuplas escalares inmutables, reglas con condiciones y conclusiones declarativas y memoria nueva por ejecución. Un disparo reúne condiciones de la misma entidad; su identidad incluye regla, entidad y antecedentes. Ordenar por prioridad descendente y desempatar por identificador de regla y entidad. Solo añadir hechos; no ejecutar efectos externos. Registrar antecedentes, conclusiones y hechos nuevos; el límite de disparos genera error si queda trabajo pendiente.
**Alternativas:** bloquear una regla para todas las entidades tras su primer disparo; permitir funciones arbitrarias como acciones; mezclar mediciones de distintas entidades.
**Por qué:** hace reproducible y explicable la cadena mínima sin omitir el segundo túnel ni introducir efectos difíciles de comprobar. Uniones entre vecinos, retractación y explicación recursiva quedan fuera de esta primera implementación. Detalles y pseudocódigo en [el entregable mínimo](plan/entregable-minimo.md).

## D24 — Costos por máximo factor y cierres dominantes
**Fecha:** 2026-10-25
**Decisión:** construir un mapa de costos independiente de la mina y nuevo por ejecución. El costo es longitud física por el mayor multiplicador inferido (todos ≥ 1). El cierre domina a los factores y excluye el túnel en ambos sentidos. R06/R07 usan factores externos configurables para alerta y riesgo alto de CO. Dijkstra propio devuelve nodos, aristas, distancia y costo; por defecto busca la salida de menor costo y devuelve ausencia de ruta si ninguna es alcanzable.
**Alternativas:** multiplicar todos los escalones acumulativos de riesgo; modificar permanentemente las longitudes; elegir siempre la salida más próxima en línea recta.
**Por qué:** evita contar repetidamente el mismo fenómeno y conservar efectos de una ejecución anterior. Mantiene D01 y separa el costo ponderado de la distancia física. Elegir automáticamente entre salida y refugio sigue pendiente de las decisiones de Nivel 2.

## D25 — Escenarios portables y comparación sobre datos originales
**Fecha:** 2026-10-26
**Decisión:** escenario JSON versión 1 con nombre, rutas de mina/umbrales/costos, mineros identificados, destinos y hechos originales. Resolver rutas respecto al archivo, rechazar lecturas repetidas, atributos derivados y mezclas con entradas manuales. Comparar con Dijkstra filtrado directamente por CO sobre el límite ocupacional configurado (inicialmente 25 ppm), incendio y derrumbe reportados. Ambos enfoques comparten mina, ubicaciones, hechos y destinos; la línea base no invoca el motor.
**Alternativas:** depender del directorio de ejecución; mezclar silenciosamente archivos y opciones; comparar contra Dijkstra sin filtro; usar las conclusiones del motor en la línea base.
**Por qué:** hace reproducible el experimento y conserva la independencia del comparador. El cierre directo por límite ocupacional es una política académica explícita, no una orden normativa de emergencia. Diferencias por políticas no acreditan por sí solas superioridad del sistema; falta demostrar el aporte del encadenamiento sobre riesgos vecinos.

## D26 — Ambiente configurable y contexto explícito de ANFO
**Fecha:** 2026-10-26
**Decisión:** añadir NO₂, CO₂, H₂S, O₂ y aire, con umbrales y factores en ambiente.json. Conservar tres escalones para gases; solo el último cierra. Exceso de O₂ y aire fuera de rango penalizan sin inventar umbrales de cierre. Exigir uso_anfo booleano por túnel para evaluar aire. Ampliar el filtro de la línea base a los mismos sensores. Aceptar ambiente como ruta opcional en escenarios versión 1; sin ella solo se admiten las entradas previas de CO y eventos.
**Alternativas:** asumir ANFO=False si falta; usar siempre el mínimo general; ignorar sensores nuevos en la línea base; cerrar por cualquier desviación en ambos enfoques.
**Por qué:** conserva los límites documentados y evita decisiones silenciosas ante falta de contexto. Se distinguen los valores ocupacionales de las políticas académicas de clasificación, penalización y cierre. Los factores se combinan por máximo sin modificar las longitudes.

## D27 — Exposición vecina mediante relaciones explícitas de un salto
**Fecha:** 2026-10-26
**Decisión:** mantener la mina pequeña y añadir una mina de Nivel 1 de 16 nodos. Definir relaciones dirigidas de exposición a humo en un JSON independiente, con túneles existentes que compartan un nodo. Extender las condiciones y reglas con entidades fijas opcionales. R04 deriva foco_incendio; R24 une el foco de origen con recibe_humo_de en el destino; R25 cierra el vecino expuesto. Instanciar R24 por par, con identificadores únicos y antecedentes completos en la traza. La exposición no crea un foco nuevo. La línea base recibe las relaciones pero sigue siendo un filtro local.
**Alternativas:** cerrar todos los túneles que compartan un nodo; propagar humo fuera del motor sin registrar antecedentes; tratar exposición como un foco que se propaga indefinidamente.
**Por qué:** permite verificar el aporte del encadenamiento sin confundir adyacencia geométrica con ventilación física. Es un supuesto explícito, no simulación de fluidos. El control sin reglas vecinas conserva los datos y recupera la ruta de la línea base. Detalles en [el punto de control Nivel 1](plan/nivel1-verificacion.md).

