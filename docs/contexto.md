# Contexto vivo del proyecto

## Estado actual
- El fork se desarrolla individualmente con ayuda del asistente hasta nuevo aviso. No se requiere revisión de otro integrante; antes de integrar cambios se revisa el código y se ejecutan las pruebas correspondientes. Se mantienen el orden y las dependencias del plan.
- Avance técnico: Nivel 1 implementado, pendiente de aceptación del usuario e integración al grupo. No equivale a declarar semanas calendario ni aprendizaje completados.
- S1-00, S1-03 y S1-03b cerradas: repositorio en GitHub y tablero con 27 tarjetas.
- Existe en src/mina_experta/: modelo, cargador, motor, conocimiento, relaciones de humo, escenarios, línea base y Dijkstra con costos dinámicos.
- Entrega: 16 nodos, 20 túneles, 25 tipos de regla, tres escenarios Nivel 1 más cuatro ejemplos pequeños. El caso de riesgo vecino incluye control sin inferencia.
- Siguiente: revisar `docs/entregas/nivel-1.md`, aceptar la rama acumulativa `luis/nivel-1-entrega` en el fork y preparar el PR al grupo. Nivel 2 pendiente.

## Comandos
- Desde la raíz y con el entorno virtual activado: `python -m pip install -e . -r requirements-dev.txt`.
- Pruebas: `python -m pytest -q`.
- Demo: `python -m mina_experta --escenario data/escenarios/nivel1_riesgo_vecino.json --explicar tunel_10_12`.

## Convenciones de código
-

## Trampas y lecciones
- Seguir el orden del plan (kanban): no saltar a otra actividad o issue (SX-0Y), sin embargo en caso de que sea necesario, debe sugerirse y el por qué.
- Al pasar de un issue a otro, avisar y explicar el porqué de la secuencia (dependencias, aprendizaje justo a tiempo, trabajo en pareja), no solo el ID.
- El usuario autorizó al asistente a ejecutar Git y publicar ramas. La entrega se deja sin fusionar para que él la acepte y tramite el PR al grupo.

## Pendientes que no son del sprint actual
- (ninguno por ahora)
