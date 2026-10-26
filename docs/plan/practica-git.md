# S1-04 — Rama y revisión de avances

[← Índice](../../README.md)

Esta práctica sigue a S1-01 y precede a S1-02 en el orden sugerido. Publicar una rama no completa la tarea: falta abrir un PR vinculado a la tarjeta correcta, recibir la revisión del otro integrante y comprobar la automatización al fusionarlo.

## Preparar un equipo

Clona tu fork con Git y entra en su carpeta. Usa Python 3.12, la versión validada para estos ejercicios.

```bash
git clone https://github.com/LuisInfinito/Miner-a-Experta.git
cd Miner-a-Experta
```

En Windows crea el entorno con `py -3.12 -m venv .venv`; en macOS o Linux usa `python3.12 -m venv .venv`.

Actívalo según tu terminal:

| Terminal | Comando |
|---|---|
| PowerShell | `.\.venv\Scripts\Activate.ps1` |
| CMD | `.venv\Scripts\activate.bat` |
| Bash o Zsh | `source .venv/bin/activate` |

Si tu equipo restringe la activación en PowerShell, puedes usar directamente `.\.venv\Scripts\python.exe` en lugar de `python` en los comandos siguientes, sin cambiar políticas del equipo.

## Comprobar una rama publicada

Para revisar los avances de esta sesión:

```bash
git fetch origin
git switch luis/s1-04-nivelacion
python -m pip install -r requirements-dev.txt
python -m pip check
python ejercicios/nivelacion.py
python -m pytest tests/test_nivelacion.py -q
```

La demostración debe mostrar distancia 350, refugios `n3` y `n5`, y entidades `tunel_1_2` y `tunel_3_4`. La suite debe terminar con 14 pruebas aprobadas. Ejecuta todo desde la raíz del checkout. Cada equipo crea su propio `.venv`; no se copia ni se versiona.

Ese comando comprueba solo S1-01. En ramas posteriores, `python -m pytest -q` ejecuta además los nuevos ejercicios y puede mostrar un total mayor.

## Abrir y revisar el PR

1. En GitHub, abre el fork `LuisInfinito/Miner-a-Experta` y crea un PR con base `main` y comparación `luis/s1-04-nivelacion`. Verifica que la base sea este fork, salvo que el equipo decida enviar el avance al repositorio grupal.
2. Usa el título `test: añadir ejercicios de nivelación verificados` y describe los tres ejercicios, la guía de ejecución y las 14 pruebas aprobadas.
3. Vincula la tarjeta real de S1-04. Añade `Closes #N` solo sustituyendo `N` por el número comprobado de una issue de este repositorio. No uses el identificador S1-04 como número ni cierres una tarjeta del repositorio grupal por suposición.
4. Pide al otro integrante que compruebe la rama y revise el código. Las pruebas locales no sustituyen esa revisión.
5. Tras la aprobación, fusiona siguiendo las reglas del equipo y verifica si la tarjeta pasó a Hecho. No supongas que el fork heredó las automatizaciones del tablero grupal.

## Estado de esta sesión

La consulta de issues por la API devolvió `Forbidden`; no se pudo verificar su número ni abrir un PR automáticamente. Las pruebas locales sí pasaron. El resultado del envío de la rama queda registrado en la bitácora. La comprensión de S1-01 y la revisión por el compañero siguen siendo actividades del integrante.

Se confirmó por Git que la rama `luis/s1-04-nivelacion` está publicada con el commit `b744ad0`. Al retomar S1-04, la consulta de PR también falló: el proxy rechazó la conexión HTTPS a `api.github.com` con `403 Forbidden`. Existe una variable de autenticación, pero no se pudo verificar el acceso a la API; no hace falta pedir otro token sin resolver antes ese bloqueo. Se puede abrir el PR desde GitHub en el navegador. No se ha fusionado la rama ni confirmado la automatización del tablero.
