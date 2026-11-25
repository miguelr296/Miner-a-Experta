# 3. Cronograma y reparto de trabajo

[← Índice](../../README.md)

## 3.1 Roles

| Integrante | Responsabilidad principal |
|---|---|
| **Integrante A** | Conocimiento (reglas, umbrales, fuentes) y motor de inferencia |
| **Integrante B** | Modelo del grafo, cargador JSON, escenarios y planificador |

El **motor mínimo se programa en pareja** (semana 2), para que ambos lo entiendan y puedan defenderlo.

Ambos tienen 10 h/semana.

## 3.2 Cronograma

Las semanas se agrupan en 4 sprints de 2 semanas (ver [Sprints](sprints.md)); las tareas se gestionan en el [tablero Kanban](kanban.md).

| Sem. | Integrante A | Integrante B | Sesión conjunta | Entregable |
|---|---|---|---|---|
| 1 | Nivelación Python; umbrales de la normativa; mina de prueba en JSON | Nivelación Python; apoyo en el esquema JSON | Esquema JSON, repositorio, acuerdo de trabajo | Mina de prueba en JSON + umbrales con fuente |
| 2 | **Motor mínimo (en pareja)**; borrador de 5 reglas en el catálogo; pytest básico | **Motor mínimo (en pareja)**; clases del grafo; cargador JSON + pruebas | Integrar motor y cargador | Motor que dispara 2–3 reglas con traza |
| 3 | 15 reglas + explicación "¿por qué?" | Dijkstra + línea base con filtro | Revisión cruzada | Reglas probadas; rutas calculadas |
| 4 | Conectar motor → costos de aristas | Conectar planificador → varios mineros y salida en consola | **3 escenarios de punta a punta** | **Punto de control** |
| 5 | Factores de certeza | A\* | Revisión cruzada | Certeza propagada; A\* operativo |
| 6 | Reglas de decisión + conflictos | Escenarios de conflicto + métricas | **Decisión sobre Nivel 3** | Nivel 2 completo |
| 7 | Pulido / Nivel 3 | Pulido / Nivel 3 | Documentación final | Sistema final |
| 8 | Corregir errores; ensayar explicación del motor | Corregir errores; ensayar escenarios | Ensayo de la demo; tag `final` | Demo lista |

Hay **un capítulo por semana para todo el equipo**, escrito en la sesión conjunta.

## 3.3 Puntos de decisión

- **Fin de semana 4:** ¿corre de punta a punta? Si no → aplicar la regla de recorte del [alcance](alcance.md).
- **Semana 6:** ¿Nivel 2 completo? Si sí → elegir un elemento del Nivel 3.

## 3.4 Riesgos

| Riesgo | Mitigación |
|---|---|
| Aprendizaje de Python más lento de lo previsto | Nivelación en semana 1; recalibrar horas cada viernes |
| Conflictos de Git entre principiantes | Un archivo, un dueño por semana; Pull Requests revisados |
| Un integrante entiende el motor y el otro no | Motor programado en pareja; revisión cruzada semanal |
| Reglas superficiales | Cada regla con fuente, justificación y prueba |
| Valores normativos mal citados | Verificación contra el texto vigente en la semana 1 |
| Interfaz que se come el tiempo | Tope de 4 h; la consola ya es un resultado válido |
