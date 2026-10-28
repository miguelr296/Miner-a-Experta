# Anexo C — Glosario

[← Índice](../README.md)

Todas las siglas y términos técnicos usados en el proyecto, explicados para quien no viene de minería ni de sistemas expertos.

**Regla del equipo:** cada término nuevo que aparezca en el proyecto se agrega aquí en la misma sesión en que aparece.

---

## 1. Minería subterránea

| Término | Significado |
|---|---|
| **Mina subterránea** | Mina cuyo mineral se extrae por túneles bajo tierra, no a cielo abierto. |
| **Mina metálica** | Mina de la que se extraen metales (cobre, zinc, plata, oro, plomo). Es el tipo predominante en el Perú. |
| **Mina de carbón** | Mina de carbón mineral. Su peligro típico es el metano; por eso no es nuestro caso. |
| **Labor** | Cualquier excavación subterránea donde se trabaja o por donde se circula (galería, rampa, chimenea, etc.). |
| **Labor ciega** | Labor con una sola entrada; el aire y las personas entran y salen por el mismo lugar. |
| **Frente (de trabajo)** | Extremo de un túnel que se está excavando; donde se perfora y se dispara. |
| **Galería** | Túnel aproximadamente horizontal. En el modelo, la mayoría de aristas del grafo son galerías. |
| **Socavón** | Túnel horizontal que comunica el interior de la mina con la superficie. Suele ser una salida. |
| **Crucero** | Galería que cruza transversalmente a otras o a la veta. |
| **Rampa** | Túnel inclinado por donde circulan vehículos; comunica niveles distintos. |
| **Chimenea** | Excavación vertical o muy inclinada que comunica dos niveles, construida de abajo hacia arriba. |
| **Pique** | Excavación vertical, normalmente desde superficie, con ascensor (jaula) para personal y mineral. |
| **Nivel** | Conjunto de galerías a una misma profundidad. En el modelo, la coordenada `nivel` de cada nodo. |
| **Veta** | Cuerpo de mineral en forma de capa o franja dentro de la roca. |
| **Voladura / disparo** | Detonación de explosivos para romper la roca. Genera gases tóxicos (CO, NO₂). |
| **ANFO** | *Ammonium Nitrate – Fuel Oil*. Explosivo hecho de nitrato de amonio y petróleo; muy usado en minería. |
| **Caída de rocas / derrumbe** | Desprendimiento de roca del techo o paredes de un túnel. En el modelo: evento reportado que bloquea un túnel. |
| **Geomecánica** | Rama de la ingeniería que estudia la resistencia y estabilidad de la roca. Fuera de alcance del proyecto. |
| **Sostenimiento** | Elementos que refuerzan un túnel para evitar derrumbes (pernos, mallas, cimbras, concreto lanzado). |
| **RMR** | *Rock Mass Rating*. Puntaje (0–100) de la calidad de la roca. Aparece en el Anexo 19; no se usa en el proyecto. |
| **Estación de refugio** | Cámara hermética dentro de la mina, con aire, agua y comunicación, donde los trabajadores esperan ser rescatados si no pueden salir. |
| **Brigada de emergencia** | Equipo de trabajadores entrenados para rescate y atención de emergencias en la mina. |
| **Autorrescatador** | Equipo personal de respiración de emergencia que protege contra el CO durante la evacuación. |
| **Simulacro** | Ensayo planificado de una emergencia para practicar la respuesta. |

## 2. Ventilación

| Término | Significado |
|---|---|
| **Ventilación natural** | Circulación de aire que se produce sin máquinas (por diferencias de temperatura y altura). |
| **Ventilación mecánica** | Circulación de aire forzada con ventiladores. |
| **Ventilador principal** | Ventilador grande que mueve el aire de toda la mina. |
| **Ventilador auxiliar** | Ventilador pequeño que lleva aire a una labor específica, normalmente una labor ciega. |
| **Manga de ventilación** | Ducto flexible que conduce el aire del ventilador auxiliar hasta el frente. |
| **Aire limpio / fresco** | Aire que entra desde superficie y aún no pasó por labores de trabajo. |
| **Aire usado / viciado** | Aire que ya pasó por labores y lleva gases, polvo o calor. |
| **Recirculación** | Cuando el aire usado vuelve a entrar a labores de trabajo. Está prohibida. |
| **Velocidad del aire** | Rapidez con que el aire se mueve dentro de un túnel, en m/min. Indica si la ventilación funciona. |
| **Caudal** | Volumen de aire que pasa por un punto en un tiempo dado (m³/min). |

## 3. Gases y unidades

| Término | Significado |
|---|---|
| **O₂** | Oxígeno. Normal en el aire: ~20,9 %. Por debajo de 19,5 % hay deficiencia de oxígeno. |
| **CO** | Monóxido de carbono. Gas incoloro e inodoro, muy tóxico. Lo producen voladuras, motores diésel e incendios. |
| **NO₂** | Dióxido de nitrógeno. Gas tóxico producido por voladuras y motores diésel. |
| **NO** | Monóxido de nitrógeno. Otro gas de voladura (Anexo 15, ítem 34). |
| **Gases nitrosos** | Nombre conjunto del NO y el NO₂. |
| **CO₂** | Dióxido de carbono. En exceso desplaza al oxígeno. |
| **H₂S** | Ácido sulfhídrico (sulfuro de hidrógeno). Gas tóxico con olor a huevo podrido; aparece en algunos yacimientos. |
| **CH₄** | Metano. Gas inflamable típico de minas de carbón. Excluido del proyecto. |
| **ppm** | Partes por millón. 25 ppm de CO = 25 moléculas de CO por cada millón de moléculas de aire. |
| **%** (en gases) | Porcentaje del volumen del aire. Se usa para el O₂. |
| **m/min** | Metros por minuto. Unidad de velocidad del aire. |
| **m³/min** | Metros cúbicos por minuto. Unidad de caudal de aire. |
| **msnm** | Metros sobre el nivel del mar. Influye en el aire necesario por trabajador (Art. 247). |

## 4. Límites de exposición

| Término | Significado |
|---|---|
| **Límite de exposición ocupacional** | Concentración máxima de un agente químico a la que un trabajador puede exponerse sin daño a su salud, según la norma. |
| **TWA** | *Time Weighted Average* (media ponderada en el tiempo). Concentración promedio permitida durante una jornada de 8 h. |
| **STEL** | *Short Term Exposure Limit* (límite de corta duración). Concentración permitida durante un máximo de 15 min seguidos. |
| **Techo (C)** | *Ceiling*. Concentración que no debe superarse en ningún momento. |
| **IDLH** | *Immediately Dangerous to Life or Health*. Nivel de peligro inmediato para la vida (estándar de NIOSH). Considerado y **no** usado (ver D12). |
| **NIOSH** | Instituto Nacional de Seguridad y Salud Ocupacional de EE. UU. Publica los valores IDLH. |
| **ACGIH** | Conferencia Americana de Higienistas Industriales Gubernamentales. Fuente original de los valores del Anexo 15. |
| **Peligro inmediato** | En este proyecto: nivel de gas a partir del cual se cierra el túnel. Es un `SUPUESTO` del equipo (ver D12). |

## 5. Normativa

| Término | Significado |
|---|---|
| **DS** | Decreto Supremo. Norma dictada por el Poder Ejecutivo del Perú. |
| **EM** | Sufijo de las normas del sector Energía y Minas. |
| **MINEM** | Ministerio de Energía y Minas del Perú. |
| **DS 024-2016-EM** | Reglamento de Seguridad y Salud Ocupacional en Minería. Fuente de nuestros umbrales. |
| **DS 023-2017-EM** | Decreto que modificó varios artículos del DS 024-2016-EM. |
| **Modificatoria** | Norma que cambia el texto de otra. Siempre se usa el texto modificado vigente. |
| **Art.** | Artículo de la norma. |
| **Anexo** | Documento complementario de la norma con tablas y formatos. Anexo 15: límites de gases. Anexo 19: refugios. |
| **SSO** | Seguridad y Salud Ocupacional. |
| **OSINERGMIN** | Organismo Supervisor de la Inversión en Energía y Minería. Publica la norma en gob.pe. |

## 6. Sistemas expertos

| Término | Significado |
|---|---|
| **Sistema experto** | Programa que resuelve problemas de un dominio imitando el razonamiento de un experto humano, separando el conocimiento del mecanismo que lo usa. |
| **Base de conocimiento** | Todo el conocimiento del sistema: reglas y datos del dominio. |
| **Base de reglas** | Conjunto de reglas SI–ENTONCES. |
| **Regla (SI–ENTONCES)** | Unidad de conocimiento: si se cumplen ciertas condiciones, entonces se concluye algo. |
| **Antecedente** | La parte "SI" de una regla (las condiciones). |
| **Consecuente** | La parte "ENTONCES" de una regla (la conclusión o acción). |
| **Hecho** | Dato conocido en un momento. En el proyecto: tupla `(entidad, atributo, valor)`, p. ej. `(tunel_4_7, co_ppm, 30)`. |
| **Hecho derivado** | Hecho que no venía de los sensores, sino que fue concluido por una regla. |
| **Memoria de trabajo** | Conjunto de hechos conocidos en el momento actual. |
| **Motor de inferencia** | Programa genérico que aplica las reglas a los hechos para obtener conclusiones. |
| **Inferencia** | Obtener una conclusión nueva a partir de hechos y reglas. |
| **Encadenamiento hacia adelante (forward chaining)** | Razonar desde los hechos hacia las conclusiones, disparando reglas hasta que no se pueda concluir nada nuevo. Es el que usamos. |
| **Encadenamiento hacia atrás (backward chaining)** | Razonar desde una hipótesis hacia los hechos que la confirmarían. No se usa. |
| **Disparar una regla** | Ejecutar su consecuente porque su antecedente se cumple. |
| **Conjunto de conflicto (agenda)** | Lista de reglas que podrían dispararse en un mismo momento. |
| **Resolución de conflictos** | Criterio para elegir qué regla se dispara primero cuando varias aplican. |
| **Prioridad** | Número asignado a cada regla; a mayor prioridad, se dispara antes. |
| **Especificidad** | Criterio de resolución: gana la regla con más condiciones, porque describe un caso más concreto. |
| **Refracción** | Evitar que una regla se dispare dos veces con los mismos hechos (evita bucles infinitos). |
| **Traza** | Registro de qué reglas se dispararon, en qué orden y con qué hechos. Base de la explicación. |
| **Explicación "¿por qué?"** | El sistema justifica una conclusión mostrando la regla y los hechos que la produjeron. |
| **Explicación "¿cómo?"** | El sistema muestra la cadena completa de reglas que llevó a una conclusión. |
| **Factor de certeza** | Número (por ejemplo de –1 a 1) que expresa cuánta confianza se tiene en un hecho o regla. |
| **MYCIN** | Sistema experto médico de los años 70 (Stanford) que introdujo los factores de certeza. Referente clásico del curso. |
| **Rete** | Algoritmo que acelera la búsqueda de reglas aplicables. Fuera de alcance. |
| **Adquisición de conocimiento** | Proceso de obtener el conocimiento del experto. En el proyecto la fuente es la norma más los supuestos del equipo. |
| **Ingeniero del conocimiento** | Persona que traduce el conocimiento experto en reglas. En este proyecto, el integrante A. |
| **`NORMA` / `SUPUESTO`** | Tipo de fuente de cada regla: valor citado de la norma o criterio razonado del equipo. |

## 7. Grafos y búsqueda de rutas

| Término | Significado |
|---|---|
| **Grafo** | Estructura de nodos conectados por aristas. Representa la mina. |
| **Nodo** | Punto del grafo: intersección de túneles, salida, refugio o frente. |
| **Arista** | Conexión entre dos nodos: un tramo de túnel. |
| **Peso / costo** | Valor de recorrer una arista. Parte de la longitud física y las reglas lo aumentan según el riesgo. |
| **Multiplicador de costo** | Factor (≥ 1) por el que una regla multiplica el costo de una arista. |
| **Ruta** | Secuencia de aristas desde un origen hasta un destino. |
| **Dijkstra** | Algoritmo que encuentra la ruta de menor costo en un grafo. |
| **A\* (A estrella)** | Variante de Dijkstra que usa una heurística para explorar menos nodos. |
| **Heurística** | Estimación del costo que falta para llegar al destino. |
| **Admisible** | Heurística que nunca sobreestima el costo real. Garantiza que A\* encuentre la ruta óptima. |
| **Distancia euclidiana** | Distancia en línea recta entre dos puntos. Nuestra heurística para A\*. |
| **BFS** | *Breadth-First Search* (búsqueda en anchura). Búsqueda simple que ignora los costos. No se usa. |
| **Línea base** | Solución simple de referencia contra la que se compara el sistema (Dijkstra con filtro por umbral). |
| **Filtro por umbral** | Bloquear un túnel solo si un sensor supera su límite, sin razonamiento encadenado. |

## 8. Programación y herramientas

| Término | Significado |
|---|---|
| **Python** | Lenguaje de programación del proyecto. |
| **JSON** | Formato de texto para datos estructurados. Ahí se describe la mina y los escenarios. |
| **Clase** | Plantilla de Python para crear objetos con datos y comportamiento (p. ej. `Nodo`, `Regla`). |
| **Diccionario** | Estructura de Python de pares clave–valor. |
| **Tupla** | Secuencia inmutable de Python, p. ej. `(entidad, atributo, valor)`. |
| **Módulo** | Archivo `.py` con código reutilizable. |
| **`__init__` / `self`** | Constructor de una clase en Python / referencia al propio objeto (equivale a `this` en Java/C#). |
| **`@dataclass`** | Decorador de Python que genera automáticamente el constructor de clases que solo guardan datos. |
| **Comprensión de listas** | Forma compacta de crear listas en Python: `[x * 2 for x in numeros]`. |
| **Tipado dinámico** | El tipo de una variable se decide al ejecutar, no se declara (a diferencia de Java/C#). |
| **Git** | Sistema de control de versiones: guarda el historial de cambios del código. |
| **GitHub** | Sitio web que aloja repositorios Git y permite colaborar. |
| **Repositorio** | Carpeta del proyecto con todo su historial. |
| **Commit** | Punto guardado del historial, con un mensaje que describe el cambio. |
| **Rama (branch)** | Línea de trabajo paralela para hacer cambios sin afectar `main`. |
| **`main`** | Rama principal; siempre debe funcionar. |
| **Merge** | Unir los cambios de una rama en otra. |
| **Pull Request (PR)** | Solicitud en GitHub para unir una rama a `main`, que el compañero revisa antes de aceptar. |
| **Conflicto de Git** | Cuando dos personas cambian la misma parte de un archivo y Git no sabe cuál conservar. |
| **Tag** | Marcador con nombre sobre un commit. Usamos `semana-01`, `semana-02`… y `final`. |
| **pytest** | Herramienta de Python para escribir y correr pruebas automáticas. |
| **Prueba unitaria** | Prueba que verifica una pieza pequeña del código (una regla, una función). |
| **`assert`** | Instrucción que verifica que algo sea verdadero; si no lo es, la prueba falla. |
| **Markdown (`.md`)** | Formato de texto simple con títulos, listas y tablas. Toda la documentación está en Markdown. |
| **README** | Archivo de portada del repositorio. |
| **MkDocs / GitHub Pages** | Herramienta que convierte los `.md` en un sitio web / servicio que lo publica gratis. Opcional. |
| **Streamlit** | Librería de Python para crear interfaces web simples. Nivel 3. |
| **NetworkX / matplotlib** | Librerías de Python para manejar y dibujar grafos / gráficos. |

## 9. Gestión del proyecto

| Término | Significado |
|---|---|
| **Scrum** | Marco ágil de trabajo en ciclos cortos (sprints). Usamos solo algunas de sus prácticas. |
| **Sprint** | Ciclo de trabajo de duración fija (2 semanas en este proyecto) con un objetivo concreto. |
| **Objetivo del sprint** | Resultado que debe existir al terminar el sprint. |
| **Planning** | Reunión al inicio del sprint para elegir y repartir tareas. |
| **Review** | Reunión al final del sprint para mostrar lo que funciona. |
| **Retrospectiva (retro)** | Reunión al final del sprint para decidir qué mejorar en la forma de trabajar. |
| **Daily** | Breve reporte diario de avance (en este proyecto, asíncrono). |
| **Sync** | Sesión conjunta a mitad del sprint para integrar y revisar el tablero. |
| **Ceremonias** | Nombre conjunto de planning, review, retro y daily. |
| **Backlog** | Historias de sprints futuros que aún no se han detallado como tareas. |
| **Ready** | Tareas detalladas del sprint actual que todavía no se empiezan. |
| **In Progress** | Tareas en las que alguien está trabajando ahora. |
| **In Review** | Tareas con un PR abierto que esperan revisión. |
| **Done** | Tareas que cumplen la definición de terminado. |
| **Historia** | Funcionalidad del sistema, más grande que una tarea (p. ej. "Dijkstra con costos dinámicos"). |
| **Tarea / tarjeta** | Trabajo de 1–3 h con criterio de aceptación; se registra en una tarjeta. Si A y B son co-dueños, ambos se asignan a la misma tarjeta. |
| **Criterio de aceptación** | Condición verificable que indica que una tarea está terminada. |
| **Definición de terminado (DoD)** | *Definition of Done*. Lista de condiciones que toda tarea debe cumplir para pasar a **Done**. |
| **Velocidad** | Horas (o tareas) que el equipo realmente completa por sprint. Se usa para planificar el siguiente. |
| **Capacidad** | Horas disponibles para tareas en un sprint (≈ 18 h por persona). |
| **Kanban** | Método de gestión visual con un tablero de columnas por estado de las tareas. |
| **Tablero** | Panel con columnas (Backlog, Ready, In Progress, In Review, Done) donde se mueven las tarjetas. |
| **WIP** | *Work In Progress*. Trabajo en curso. El **límite WIP** es el máximo de tarjetas permitidas en una columna. |
| **GitHub Projects** | Herramienta de GitHub para tableros Kanban vinculados al repositorio. |
| **Issue** | Ficha de GitHub que describe una tarea o problema. Cada tarjeta del tablero es un Issue. |
| **Milestone** | Agrupación de Issues en GitHub con fecha límite. No se usa: los sprints se manejan con el campo Iteración. |
| **Iteración (Iteration)** | Tipo de campo de GitHub Projects que representa ciclos de duración fija. Cada sprint es una iteración. |
| **Campo `Status`** | Campo de GitHub Projects cuyas opciones son las columnas del tablero. |
| **Borrador (draft item)** | Tarjeta creada directamente en el tablero, aún no convertida en Issue. |
| **Workflows (automatizaciones)** | Reglas de GitHub Projects que mueven tarjetas solas (p. ej. a *Done* al cerrar un Issue). |
| **Assignee** | Persona asignada a un Issue; una tarjeta compartida puede tener asignados a A y B. |
| **Etiqueta (label)** | Marca de color en un Issue para clasificarlo (aprendizaje, código, pruebas, docs). |
| **Núcleo / Si alcanza** | Prioridad de una tarea: imprescindible para el objetivo del sprint / se hace solo si sobra tiempo. |
| **Programación en pareja** | Dos personas escriben el mismo código juntas: una escribe y la otra revisa, alternándose. |
| **Nivel 1 / 2 / 3** | Capas del alcance: obligatorio, meta firme, extra. |
| **Entregable** | Resultado concreto y verificable que debe existir al final de una semana. |
| **Punto de control** | Momento de revisión que decide si se recorta alcance (semanas 4 y 6). |
| **Colchón** | Tiempo reservado para absorber atrasos (semana 8, fines de semana). |
| **Escenario** | Archivo JSON con una emergencia concreta para probar el sistema. |
| **Simulación por turnos** | El estado de la mina cambia paso a paso (p. ej. el gas se propaga). Nivel 3. |
| **Métrica** | Medida numérica para comparar el sistema con la línea base (exposición al riesgo, longitud de ruta). |
| **Scope creep** | Crecimiento descontrolado del alcance por agregar "una cosa más". |
| **Deuda técnica** | Atajos en el código que habrá que corregir después. |
| **Bitácora** | Diario de sesiones: qué se hizo, qué falló y el siguiente paso. |
