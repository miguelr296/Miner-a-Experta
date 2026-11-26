# Contexto vivo del proyecto

## Estado actual
- Sprint: 1 (semanas 1–2) · 21 nov – 5 dic 2026 · Objetivo: motor mínimo + cargador JSON
- S1-00, S1-01, S1-02, S1-03, S1-03b, S1-04, S1-05, S1-07, S1-08 y S1-09 cerradas y fusionadas (10 de 20 tarjetas); quedan 10 en Ready. Nada en In Progress ni In Review; `main` sincronizada (`59556d8`).
- Existe en src/: (nada aún)
- Semana 1: umbrales, nivelación de Python, Git/PR, JSON y motor (teoría) listos; S1-09 cerrada.
- Siguiente: A: S1-12 (diseñar `Hecho` y `Regla` en `decisiones.md`); B: S1-10 (clases `Nodo`, `Arista` y `Mina`). S1-09 desbloqueó S1-11; S1-07 desbloqueó S1-12.

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
- Al cerrar una tarjeta, comprobar el contenido de `contexto.md` después del merge, no solo que exista el commit que dice "actualizar contexto": el 2026-11-25 el commit 516f52d no dejó el estado en 10 de 20.

## Pendientes que no son del sprint actual
- (ninguno por ahora)
