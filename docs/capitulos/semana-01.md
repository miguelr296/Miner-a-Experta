# Semana 1 — Nivelación, modelo de la mina y fuentes

[← Índice](../../README.md) · Código de esta semana: tag [`semana-01`](../../../../tree/semana-01)

**Fechas:** dd/mm – dd/mm · **Horas reales:** A: __ h · B: __ h · **Entregable:** Sí / Parcial / No

## 1. Objetivo de la semana

- Nivelación en Python (clases, diccionarios, lectura de JSON) y Git.
- Diseñar el esquema JSON de la mina y una mina de prueba.
- Extraer y verificar los umbrales normativos que usarán las reglas.
- Acordar las reglas de trabajo del equipo.

## 2. Conceptos aprendidos

- **Límites de exposición ocupacional:** TWA (promedio de 8 h), STEL (15 min) y techo (nunca se supera). No son niveles de emergencia.
- **Adquisición de conocimiento:** sin experto disponible, una norma técnica puede cumplir el rol de fuente experta, pero no cubre todo; lo faltante se declara como supuesto.

## 3. Decisiones tomadas y por qué

- D09: gases en niveles (normal / alerta / riesgo alto) según TWA y STEL.
- D10: refugio a ≤ 500 m de cada frente como restricción del modelo de mina.
- D11: cada regla declara si su fuente es `NORMA` o `SUPUESTO`.
- D12: el nivel de peligro inmediato (cierre del túnel) es un supuesto del equipo.
- D13: umbrales en un JSON de configuración.
- D14: glosario obligatorio.

## 4. Qué se implementó

- Tabla de umbrales del [catálogo de reglas](../reglas.md), con artículo o anexo de origen: O₂, CO, NO₂, CO₂, H₂S, velocidad del aire y refugios.
- Tabla de niveles de riesgo por gas (normal / alerta / riesgo alto / peligro inmediato).
- [Glosario](../glosario.md) con todas las siglas y términos usados hasta ahora.
- Repositorio en GitHub y tablero del sprint 1 con 27 tarjetas (S1-03 y S1-03b).
- *(pendiente: esquema JSON y mina de prueba; nivelación en Python)*

## 5. Pruebas

- Avance individual del fork: modelo de la mina, cargador estricto y motor mínimo con tres reglas de CO. Guía y alcance real en [el entregable mínimo](../plan/entregable-minimo.md).
- La suite ejecuta casos de formato, geometría, conectividad, distancia a refugios, prioridad, refracción, separación entre entidades, umbrales y consola. Resultados de la sesión en la bitácora; esto no cierra la semana ni acredita el aprendizaje individual.

## 6. Problemas encontrados

- La norma no define niveles de gas de peligro inmediato; sin ellos no hay base citable para cerrar un túnel por gases. Se resolvió con un supuesto declarado (D12).

## 7. Lecciones aprendidas

## 8. Siguiente semana

Motor de inferencia mínimo, programado en pareja.
