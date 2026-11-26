# Contexto vivo del proyecto

## Estado actual
- Sprint: 1 (semanas 1–2) · 21 nov – 5 dic 2026 · Objetivo: motor mínimo + cargador JSON
- S1-00, S1-01, S1-02, S1-03, S1-03b, S1-04, S1-05, S1-06, S1-07, S1-08, S1-09 y S1-12 cerradas y fusionadas (12 de 20 tarjetas); 7 en Ready y S1-17 en In Progress (A, borrador de 5 reglas); nada en In Review; `main` sincronizada (`03d2874`).
- Existe en src/: (nada aún)
- Semana 1: umbrales, nivelación de Python, Git/PR, JSON y motor (teoría) listos; S1-09 cerrada.
- Siguiente: A: S1-17 (borrador de 5 reglas) → S1-13; B: S1-10 (clases `Nodo`, `Arista` y `Mina`, #12) → S1-11. S1-12 desbloqueó S1-13; S1-10 desbloquea S1-11.

## Comandos
- (se agregan cuando existan)

## Convenciones de código
-

## Trampas y lecciones
- Seguir el orden del plan (kanban): no saltar a otra actividad o issue (SX-0Y), sin embargo en caso de que sea necesario, debe sugerirse y el por qué.
- Al pasar de un issue a otro, avisar y explicar el porqué de la secuencia (dependencias, aprendizaje justo a tiempo, trabajo en pareja), no solo el ID.
- El asistente no ejecuta comandos de Git ni lee el tablero: guía al equipo, que los escribe y entiende; al inicio de cada sesión el equipo le pega la salida de `git status -sb`, `git branch -a` y `git log --oneline -5`, más el estado de In Progress, In Review y Done.
- En Python `False` vale 0: un hecho `(tunel, cerrado, False)` significa que el túnel NO está cerrado. Filtrar por atributo antes de comparar o sumar valores.
- No usar nombres de funciones incorporadas (`max`, `sum`, `list`, `dict`) como variables; se pierde la función.
- Los ejercicios de nivelación se escriben en una carpeta local fuera del repositorio; `src/` se reserva para el código del proyecto.
- Las tarjetas de aprendizaje con ejercicios (S1-01, S1-02, S1-05, S1-06) se cierran con un PR que solo toca documentación (bitácora/capítulo), porque el ejercicio vive en una carpeta local fuera del repositorio.
- La automatización "PR con `Closes #N` → Done" funciona: S1-02 (PR #27) pasó sola a Done. S1-01 y S1-04 se habían cerrado a mano; no hace falta repetirlo.
- Los enlaces de dependencia se crean en la tarjeta que espera ("Blocked by"). Un enlace invertido en una tarjeta de cierre (S1-18) bloquea en silencio a media columna: al revisar el tablero, comprobar que ninguna tarjeta de cierre bloquee a otras.
- Cuando una decisión mueve una tarea de sprint, actualizar los cuatro lugares: tabla de `sprints.md`, cronograma, tabla del sprint en `kanban.md` y títulos del Backlog. "Varios mineros" estaba en Nivel 1 en `alcance.md` y en el Sprint 3 en `sprints.md` a la vez.
- Al cerrar una tarjeta, comprobar el contenido de `contexto.md` en `main` después del merge (`git show origin/main:docs/contexto.md`), no solo que exista el commit que dice "actualizar contexto". Ya falló dos veces: 516f52d (2026-11-25) y el PR #35 (2026-11-26), que dejó el estado en 10 de 20 al cerrar S1-12.

## Pendientes que no son del sprint actual
- Ramas remotas `luis/motor-python`, `luis/pulir-prototipo-web` y `revert-23-luis/nivel-1-entrega`: **ignorar por ahora**. No estorban, no bloquean el sprint 1 y no se revisan, fusionan ni borran hasta que el equipo lo mencione.
