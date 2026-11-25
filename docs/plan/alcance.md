# 2. Alcance

[← Índice](../../README.md)

## 2.1 Supuestos de capacidad

| Dato | Valor |
|---|---|
| Duración | 8 semanas |
| Horas por persona | 10 h/semana → 80 h |
| Total del equipo | 160 h |
| Descuento por aprendizaje (Python nuevo pero con base en Java/C#; pytest y GitHub Projects nuevos) y coordinación | 20–25 % |
| **Horas productivas estimadas** | **≈ 120–128 h** |

Es una estimación con incertidumbre alta. Se recalibra con las horas reales registradas en la bitácora al final de cada semana.

## 2.2 Nivel 1 — Obligatorio (semanas 1–4)

- Mina en JSON: 15–20 nodos, 2 niveles, con coordenadas (x, y, nivel) y tipo (intersección, salida, refugio y frente).
- Motor forward chaining con **prioridad** y **refracción**.
- **15 reglas** en tres categorías: diagnóstico, riesgo encadenado y efecto sobre la ruta.
  - Cobertura: gases, ventilación, incendio y caída de rocas.
  - Al menos una cadena de 3–4 pasos.
- Explicación **"¿por qué?"**: por qué se llegó a cada conclusión (traza de reglas).
- **Dijkstra** con costos dinámicos.
- Varios mineros (un cálculo de ruta por minero).
- 3 escenarios de emergencia.
- Línea base: **Dijkstra con filtro por umbral de sensor**.
- Salida por consola, ejecutable con un solo comando.

**Criterio de éxito:** al final de la semana 4, el sistema corre de punta a punta en los 3 escenarios.

## 2.3 Nivel 2 — Meta firme (semanas 5–6)

- **Factores de certeza** (estilo MYCIN): los sensores tienen confianza y las reglas la propagan.
- Explicación **"¿cómo?"**: reconstrucción paso a paso de una conclusión.
- Reglas de decisión: evacuar, refugiarse o esperar brigada.
- 2–3 pares de **reglas en conflicto deliberado**, resueltos por prioridad o especificidad.
- **A\*** con heurística euclidiana 3D (extensión de Dijkstra).
- Ampliación a **≈ 25 reglas**.
- Métricas contra la línea base: exposición al riesgo, longitud de ruta.

## 2.4 Nivel 3 — Solo si van adelantados en la semana 6

- Interfaz simple en Streamlit + NetworkX (**tope: 4 horas**).
- Simulación temporal por turnos (la memoria de hechos se reconstruye desde cero cada turno).
- Detección de sensor defectuoso.

## 2.5 Fuera de alcance

Bases de datos, interfaz web elaborada, datos reales de minas, aprendizaje automático, entrevistas a expertos, modelado completo del reglamento.

## 2.6 Regla de recorte

| Situación | Acción |
|---|---|
| Semana 4 sin sistema de punta a punta | Se eliminan los factores de certeza; se cierra el Nivel 1 bien hecho |
| Semana 6 con Nivel 2 incompleto | No se toca el Nivel 3; se pulen escenarios y documentación |
| Semana 6 con Nivel 2 completo | Se elige **un** elemento del Nivel 3 |

Se recorta siempre desde arriba, nunca la base.
