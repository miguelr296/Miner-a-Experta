# Bitácora de sesiones

[← Índice](README.md)

Una entrada por sesión, la más reciente arriba. Tres líneas bastan.

## 2026-11-24 · Prototipo web

- Hice: incorporé el ZIP de la presentación a la rama local y conecté el diagnóstico de peligro por gases con el cierre del túnel.
- Falló: el diagnóstico de gas en peligro podía coexistir con un túnel transitable.
- Siguiente paso: presentar en el plano la secuencia de lectura, reglas activadas y efecto sobre la ruta del minero.

## 2026-11-24 · Demo interactiva

- Hice: separé la inferencia, las rutas y las explicaciones. Integré el formulario de simulación y el selector de tema.
- Falló: el ZIP nuevo no permitía editar H₂S ni superar el umbral de CO₂ desde el formulario. Amplié los controles.
- Siguiente paso: ensayar la presentación con un cambio de lectura y seguir su efecto desde la traza hasta la ruta.

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

### 2026-11-23 · S1-05: leer y escribir JSON en Python (sesión 3) · 1 h
- Hice: comparamos el módulo `json` con Gson/`System.Text.Json` y escribimos `leer_json.py` (carga el archivo, cuenta nodos y maneja `JSONDecodeError` con línea y columna) y `escribir_json.py` (lee, agrega `meta` y guarda con `indent=2` y `ensure_ascii=False`), en la carpeta local de nivelación fuera del repositorio. En documentación: `contexto.md` al día con el cierre de S1-02 y la automatización de PR validada con #27; corregimos el capítulo de la semana 1, que decía que las tarjetas de aprendizaje no requieren PR.
- Falló / dudas: `escribir_json.py` sobrescribía `mina_demo.json` y borraba los nodos; se corrigió leyendo antes de escribir. En `leer_json.py` las impresiones quedaban fuera del `try`, así que con un JSON inválido se usaba `datos` sin definir; se movieron a un `else`. Falta ejecutar la prueba con un JSON roto (quitar una coma): el manejo de `JSONDecodeError` está escrito, pero no verificado.
- Siguiente paso exacto: commit `docs: cerrar S1-05, JSON en Python`, push, PR con `Closes #7`, review del compañero y merge; luego S1-07 (forward chaining y refracción), que desbloquea S1-12.

### 2026-11-23 · S1-02: clases y módulos (sesión 2) · 1,5 h
- Hice: explicamos `__init__`/`self`, `@dataclass`, métodos especiales y módulos. Escribí `modelo.py` (`Nodo` con `distancia_a` en 3D vía `math.dist`; `Tunel` con `longitud`, `__len__` y `__repr__`) y `demo.py` en la carpeta local de nivelación, fuera del repositorio: `python demo.py` imprime `Tunel(tunel_ref_1_frente_4, 144.2255... m)` y `2`. Además corregimos la entrada del 2026-10-25 (los 17 en Backlog ya estaban en Ready) y registramos en `contexto.md` que las tarjetas de aprendizaje se cierran con un PR de solo documentación.
- Falló / dudas: pegué los dos archivos en un mismo bloque y hubo que separarlos en `modelo.py` y `demo.py` para que el import funcionara. S1-04 se movió a Done a mano, así que la automatización "PR con `Closes #N` → Done" sigue sin probarse. Horas estimadas, sin medir: ~1,5 h.
- Siguiente paso exacto: rama `<nombre>/s1-02`, PR con `Closes #3`, review del compañero, merge y comprobar que la tarjeta pasa sola a Done; luego S1-05, leer y escribir JSON en Python.

### 2026-11-23 · Nivelación de Python (S1-01) y cierre de S1-04 · 3 h
- Hice: completamos E1–E7 con datos de la mina (variables, f-strings, listas, diccionarios, tuplas, conjuntos, funciones, control y comprensiones); agregamos cinco términos al glosario; S1-01 y S1-04 quedaron cerradas.
- Falló / dudas: confundimos `("tunel_1_2", "cerrado", False)` con un túnel cerrado y promediamos valores de hechos en vez de costos; `False` vale 0 en Python. También usamos `max` como nombre de variable. Se corrigió filtrando por atributo y usando `costos.values()`. El `TypeError` al modificar una tupla fue intencional.
- Siguiente paso exacto: S1-02, clases y módulos en Python.

### 2026-10-25 · Corrección de documentación del tablero
- Hice: actualicé el plan, las decisiones, el glosario, el capítulo de la semana 1 y la bitácora: 20 tarjetas en total, columnas en inglés y una tarjeta compartida cuando el dueño es A y B.
- Falló / dudas: las 17 tarjetas pendientes del sprint 1 estaban en Backlog; según el plan corresponden a Ready. **Resuelto:** se movieron a Ready y hoy quedan 15 (S1-01 y S1-04 ya se cerraron).
- Siguiente paso exacto: (cumplido) mover las tareas pendientes del sprint 1 a Ready y comenzar S1-01, nivelación de Python.

### 2026-10-24 · Tablero del sprint 1 · 2 h
- Hice: cerramos S1-00, S1-03 y S1-03b; configuramos GitHub Projects (columnas, campos, etiquetas, workflows) y cargamos las 20 tarjetas del sprint 1, una por tarea, con dueño, estimación, prioridad e iteración.
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
