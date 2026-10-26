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

### 2026-10-26 · Pulido y preparación de entrega Nivel 1 · duración no registrada
- Hice: sincronizé la rama acumulativa luis/nivel-1-entrega con main del fork (PR #1–#5 ya integrados), corregí rutas vacías que activaban predeterminados silenciosamente, actualicé las instrucciones desfasadas de AGENTS/contexto y preparé inicio rápido multiplataforma y guía con texto de PR. Añadí CI para Python 3.12 en Linux y Windows. En una copia limpia del commit y entorno nuevo pasaron 334 pruebas; se ejecutaron los siete escenarios desde fuera del checkout. Una distribución instalada sin dependencias externas de ejecución también ejecutó los tres escenarios Nivel 1.
- Falló / dudas: ninguna falla local. La API de GitHub sigue devolviendo Forbidden; no se puede confirmar la ejecución de CI ni abrir PR mediante esa API. Windows queda configurado en CI, no validado localmente. Los supuestos académicos y el alcance pendiente de Nivel 2 están expresos en la guía.
- Siguiente paso exacto: aceptar el PR de luis/nivel-1-entrega hacia main del fork tras revisar diff y CI; después el usuario abrirá el PR del fork/main al repositorio grupal con el texto de docs/entregas/nivel-1.md. No fusionar ni enviar al grupo automáticamente.

### 2026-10-26 · Punto de control técnico de Nivel 1 · duración no registrada
- Hice: añadí mina_nivel1.json con 16 nodos, 20 túneles, dos cotas subterráneas, dos salidas y tres refugios. Los cuatro frentes tienen refugio a 150, 220, 60 y 100 m. Implementé relaciones dirigidas de humo, condiciones con entidades explícitas, R24/R25 y explicación por consola. Tres escenarios nuevos corren de punta a punta. En el control de riesgo vecino, la base cruza el vecino en una ruta de 420 m; el motor lo evita en una de 500 m, y desactivar solo vecindad recupera la ruta de la base. Pasaron 322 pruebas.
- Falló / dudas: ninguna falla en los casos ejecutados. La relación de humo es un supuesto de un salto, no simulación física ni prueba de seguridad real. La mina de práctica se conserva. No se han integrado ramas a main ni creado tags; la revisión académica, horas y cierre semanal no se acreditan automáticamente.
- Siguiente paso exacto: revisar el punto de control funcional documentado, integrar el avance acumulado cuando el usuario cierre la sesión y preparar Nivel 2 según el plan: certeza, conflictos, decisiones y A*. Mantener explícita la diferencia entre validación técnica y evaluación real del modelo.

### 2026-10-26 · Gases y ventilación configurables · duración no registrada
- Hice: añadí NO₂, CO₂, H₂S, O₂ y velocidad del aire con uso explícito de ANFO, configuración ambiente.json, R08–R23 y D26. Amplié la línea base con los mismos sensores y añadí un cuarto escenario reproducible de ventilación con ANFO. Las 23 reglas coinciden con el catálogo y sus referencias a pruebas. Pasaron 307 pruebas y la comprobación de dependencias.
- Falló / dudas: ninguna falla en los casos ejecutados. No se hizo una nueva verificación normativa; se reutilizan las fuentes del catálogo y se distinguen los supuestos de emergencia. La ventilación y el exceso de O₂ penalizan sin inventar umbrales de cierre; el filtro directo conserva su política distinta. La mina sigue teniendo ocho nodos y aún no hay evidencia de riesgos vecinos detectados por encadenamiento.
- Siguiente paso exacto: ampliar la mina a 15–20 nodos manteniendo D10, preparar el conocimiento explícito de relaciones entre túneles y probar un escenario donde el motor deduzca un riesgo vecino que el filtro local no capture. Mantener pendiente el cierre real de Nivel 1 y las capacidades de Nivel 2.

### 2026-10-26 · Escenarios JSON y línea base · duración no registrada
- Hice: implementé escenarios portables con mineros identificados y hechos originales, tres casos (CO moderado, incendio con desvío y derrumbe con aislamiento), y Dijkstra con filtro directo por CO/eventos independiente del motor. Añadí comparación manual y automática en escenarios, D25 y documentación de políticas y límites. Pasaron 262 pruebas, incluidas ejecuciones de los tres casos desde fuera del checkout.
- Falló / dudas: ninguna falla en los casos ejecutados. La diferencia en CO moderado refleja políticas distintas, no una superioridad demostrada por encadenamiento. Siguen siete reglas y ocho nodos; aún faltan cobertura de gases/ventilación, al menos 15 reglas, mina ampliada y el caso de riesgos vecinos. Las métricas de exposición y tiempo no se han implementado ni se infieren de los costos.
- Siguiente paso exacto: ampliar la cobertura del conocimiento y sus pruebas sin cambiar la independencia de la línea base; después preparar una mina mayor y un escenario donde la cadena de reglas detecte un riesgo que el filtro local no capture.

### 2026-10-25 · Integración de costos y rutas · duración no registrada
- Hice: conecté los hechos del motor con un mapa de costos de solo lectura y Dijkstra propio. Añadí R06/R07 con factores JSON, D24 y opciones de consola para orígenes y destinos. En la mina real, cerrar tunel_3_4 cambia la ruta desde n5 de 470 m a una alternativa de 710 m; aislar n5 devuelve SIN RUTA. Pasaron las 225 pruebas.
- Falló / dudas: ninguna falla en los casos ejecutados. Las siete reglas actuales no completan Nivel 1; aún faltan la línea base con filtro por umbral, los escenarios JSON, otros gases, ventilación y la mina ampliada. No se afirma seguridad por ausencia de mediciones ni se elige automáticamente refugio frente a salida.
- Siguiente paso exacto: implementar la línea base con filtro por umbral y los escenarios JSON reproducibles, manteniendo la revisión del alcance completo del sprint 2. Horas y aprendizaje no medidos; no se crean cierres semanales ni tags automáticamente.

### 2026-10-25 · Entregable mínimo: cargador y motor · duración no registrada
- Hice: completé el núcleo técnico de S1-11 a S1-16, con carga estricta, comprobación global de D10, hechos y reglas por entidad, selección por prioridad, refracción y traza. Añadí cinco reglas documentadas (cadena de CO más incendio y derrumbe reportados), umbrales JSON y consola; el borrador de S1-17 queda cubierto con implementación y pruebas. Registré D22/D23 y la modalidad individual en el flujo. Pasaron 195 pruebas, la comprobación de dependencias y una instalación limpia del paquete con ejecución fuera del checkout.
- Falló / dudas: no falló la suite del proyecto. La práctica aislada S1-06 produjo deliberadamente 1 prueba aprobada y 1 fallida, verificando el código 1; se eliminó el archivo temporal. La consola no calcula rutas ni demuestra uso operativo; los niveles de emergencia siguen siendo supuestos. No se actualizaron main, tarjetas ni tags semanales. Aprendizaje, horas reales y cierre semanal de S1-18 siguen sin acreditarse automáticamente.
- Siguiente paso exacto: revisar este punto de control del sprint 1 y preparar el siguiente bloque del plan: ampliar el conocimiento, aplicar costos y cierres al planificador propio y completar escenarios. Mantener pendientes explícitos el resto de gases, ventilación, 15 reglas de Nivel 1, tres escenarios, rutas por minero y comparación con la línea base.

### 2026-10-25 · S1-10: modelo de la mina · duración no registrada
- Hice: implementé `Nodo`, `Arista` y `Mina` en `src/mina_experta/`, con datos de solo lectura y vecinos bidireccionales. Añadí instalación del paquete, demostración en memoria, documentación y D21. La demostración funcionó, pasaron las 113 pruebas y no se detectaron dependencias incompatibles.
- Falló / dudas: ninguna falla en los casos ejecutados. El modelo valida coherencia local; todavía no carga archivos ni exige conectividad global o recorridos de refugio a 500 m para toda mina construida en código.
- Siguiente paso exacto: S1-11, cargar `data/mina_prueba.json`, crear los objetos del modelo y validar los requisitos globales y errores de archivo. S1-12 sigue pendiente para el diseño del motor.

### 2026-10-25 · S1-09: mina de prueba · duración no registrada
- Hice: creé `data/mina_prueba.json` con ocho nodos, ocho túneles, dos cotas subterráneas, una salida, un refugio y dos frentes. Documenté y comprobé recorridos de 150 m y 220 m hasta el refugio. Pasaron las 69 pruebas, incluidas las ocho del entregable: formato, referencias, geometría, conectividad y recorridos.
- Falló / dudas: ninguna falla en los casos ejecutados. Las comprobaciones corresponden al archivo concreto; aún no hay cargador general ni planificador.
- Siguiente paso exacto: S1-10, clases `Nodo`, `Arista` y `Mina` con consulta de vecinos, para después cargar este JSON en S1-11. La línea de diseño del motor (S1-12) se conserva como pendiente del sprint.

### 2026-10-25 · S1-08: esquema JSON de la mina · duración no registrada
- Hice: definí el contrato de la mina estática en `data/esquemas/mina.schema.json`, documenté D20, los campos y las restricciones del futuro cargador, y añadí términos al glosario. El formato usa coordenadas en metros y túneles bidireccionales con longitud física. Pasaron las 61 pruebas y la comprobación de dependencias.
- Falló / dudas: ninguna falla en la validación estructural. Todavía no hay cargador ni comprobación ejecutable de referencias, geometría, conectividad y recorridos de hasta 500 m; esos requisitos se registraron para S1-11. No se creó aún la mina de prueba.
- Siguiente paso exacto: S1-09, crear `data/mina_prueba.json` con 6–8 nodos y documentar los recorridos desde cada frente a un refugio, conforme a D10 y D20.

### 2026-10-25 · S1-07: ciclo del motor · duración no registrada
- Hice: preparé una guía de encadenamiento hacia adelante, prioridad, refracción y traza, con un recorrido manual de tres reglas abstractas y preguntas de comprensión. No se añadieron reglas de minería ni código del motor.
- Falló / dudas: la comprensión individual queda por comprobar; una guía no la acredita automáticamente. El desempate de reglas y la identificación de disparos siguen pendientes de S1-12.
- Siguiente paso exacto: revisar el recorrido y continuar con S1-08, diseño del esquema JSON de la mina, antes de crear los datos de S1-09.

### 2026-10-25 · S1-05: lectura y escritura de JSON · duración no registrada
- Hice: registré la modalidad individual aprobada por el usuario en el contexto. Añadí un ejemplo de escritura y lectura JSON con archivos temporales, guía y pruebas de errores y protección contra sobrescritura.
- Falló / dudas: la revisión de compañero deja de ser requisito por decisión del usuario. La API de GitHub sigue sin acceso confirmado; publicar ramas por Git funciona. No se ha integrado a main ni se han cerrado tarjetas automáticamente.
- Siguiente paso exacto: ejecutar las comprobaciones de S1-05 y publicar la rama; después abordar S1-07 (ciclo del motor y refracción) antes del diseño del esquema JSON de S1-08.

### 2026-10-25 · S1-02: clases y módulos · duración no registrada
- Hice: confirmé la publicación previa de S1-04 (`b744ad0`) y preparé S1-02 en `luis/s1-02-clases-modulos`, basada en esa rama. Añadí una clase con `__init__`, una `dataclass` y una demostración que las importa desde otro módulo, con guía y pruebas.
- Falló / dudas: la consulta de PR sigue bloqueada; se diagnosticó rechazo del proxy a `api.github.com` (conexión HTTPS, 403). No se abrió ni fusionó un PR ni se sustituyó la revisión del compañero. El aprendizaje individual sigue pendiente de revisión.
- Siguiente paso exacto: verificar y publicar las comprobaciones de S1-02; resolver la apertura y revisión de los PR cuando haya acceso a la API o desde el navegador. Después continuar con S1-05 (leer y escribir JSON), sin dar por cerradas las tarjetas de aprendizaje.

### 2026-10-25 · Preparación de S1-04 · duración no registrada
- Hice: añadí `requirements-dev.txt` y la guía multiplataforma de instalación, comprobación de rama y revisión por PR; preparé la rama `luis/s1-04-nivelacion`. La instalación, la comprobación de dependencias y las 14 pruebas pasaron.
- Falló / dudas: la API de GitHub devolvió `Forbidden`; no se pudo consultar la tarjeta ni abrir el PR automáticamente. La publicación de la rama se comprueba por separado; no se considera completada S1-04 sin revisión del compañero.
- Siguiente paso exacto: abrir el PR de esta rama en el fork, vincular la issue correcta y obtener revisión; después continuar con S1-02 (clases y módulos).

### 2026-10-25 · Soluciones verificadas de S1-01 · duración no registrada
- Hice: por petición del usuario, implementé los tres ejercicios en `ejercicios/nivelacion.py` y sus comprobaciones en `tests/test_nivelacion.py`; la ejecución de consola produjo los resultados esperados y pasaron 14 casos con pytest.
- Falló / dudas: ninguna falla en los casos ejecutados. Falta que el integrante revise y explique las soluciones para acreditar el aprendizaje; no se cerraron tarjetas ni se publicó en GitHub.
- Siguiente paso exacto: revisar las soluciones de S1-01 y después practicar S1-04 (rama y PR), antes de S1-02 según el orden sugerido. La aplicación sigue sin implementar.

### 2026-10-25 · Inicio de S1-01 en el fork · duración no registrada
- Hice: revisamos el plan y preparamos una guía de nivelación de Python con tres ejercicios del dominio, casos de comprobación y ejecución en el entorno virtual existente.
- Falló / dudas: no hay soluciones del integrante que revisar todavía; S1-01 continúa pendiente. No se implementó código de la aplicación ni se modificó el tablero del equipo.
- Siguiente paso exacto: resolver el ejercicio 1 de `docs/plan/nivelacion-python.md`, ejecutarlo con sus tres entradas y revisar el resultado antes de continuar con los ejercicios 2 y 3.

### 2026-10-24 · Tablero del sprint 1 · 2 h
- Hice: cerramos S1-00, S1-03 y S1-03b; configuramos GitHub Projects (columnas, campos, etiquetas, workflows) y cargamos las 27 tarjetas del sprint 1 con dueño, estimación, prioridad e iteración.
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
