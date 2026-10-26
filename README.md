# Sistema Experto para Emergencias y Evacuación en Minería Subterránea

Proyecto del curso **Sistemas Expertos**. Proyecto original de 2 integrantes; este fork se desarrolla individualmente con ayuda del asistente. Lenguaje: Python.

Sistema que, ante una emergencia simulada en una mina metálica subterránea, **infiere el estado de riesgo** con un motor de reglas propio (forward chaining), **calcula rutas de evacuación** para varios mineros y **explica cada decisión**.

## Inicio rápido — Nivel 1

Requiere **Python 3.12**. Ejecuta desde la raíz del checkout de esta entrega. Para descargar la rama candidata y revisar antes de integrar, consulta la [guía de entrega](docs/entregas/nivel-1.md).

| Sistema / terminal | Crear entorno | Activar entorno |
|---|---|---|
| Windows, PowerShell | `py -3.12 -m venv .venv` | `.\.venv\Scripts\Activate.ps1` |
| Windows, CMD | `py -3.12 -m venv .venv` | `.venv\Scripts\activate.bat` |
| macOS / Linux | `python3.12 -m venv .venv` | `source .venv/bin/activate` |

Después de activarlo:

```bash
python -m pip install -e . -r requirements-dev.txt
python -m mina_experta --escenario data/escenarios/nivel1_gases.json
python -m mina_experta --escenario data/escenarios/nivel1_derrumbe.json
python -m mina_experta --escenario data/escenarios/nivel1_riesgo_vecino.json --explicar tunel_10_12
python -m pytest -q
```

Si PowerShell impide activar el entorno, sustituye `python` por `.\.venv\Scripts\python.exe` en esos comandos. No necesitas cambiar políticas del equipo. Guarda las minas, escenarios y configuración del checkout: sus archivos JSON no se instalan dentro del paquete Python.

El ejemplo vecino muestra una ruta de 500 m para el sistema y de 420 m para el filtro local: la segunda cruza el túnel expuesto según el supuesto de humo. El caso de derrumbe devuelve SIN RUTA para Luis. SIN RUTA es un resultado válido (código 0); un archivo o argumento inválido termina con código 2.

La entrega tiene 16 nodos, 20 túneles y 25 tipos de regla. Es una **simulación académica**, con límites ocupacionales y supuestos de emergencia identificados en el catálogo. No es una herramienta validada para uso operativo. Nivel 2 sigue pendiente.

## Cómo leer este repositorio

Este README es la portada. La documentación se lee como un informe, en orden:

### Parte I — Plan
1. [Enfoque](docs/plan/enfoque.md)
2. [Alcance](docs/plan/alcance.md)
3. [Cronograma y reparto de trabajo](docs/plan/cronograma-y-reparto.md)
4. [Flujo de trabajo](docs/plan/flujo-de-trabajo.md)
5. [Sprints](docs/plan/sprints.md)
6. [Tablero Kanban](docs/plan/kanban.md)
7. [S1-01: nivelación de Python](docs/plan/nivelacion-python.md)
8. [S1-04: práctica de rama y revisión](docs/plan/practica-git.md)
9. [S1-02: clases y módulos](docs/plan/clases-y-modulos.md)
10. [S1-05: lectura y escritura de JSON](docs/plan/lectura-json.md)
11. [S1-07: ciclo del motor y refracción](docs/plan/ciclo-motor.md)
12. [S1-08: esquema JSON de la mina](docs/plan/esquema-mina.md)
13. [S1-09: mina académica de prueba](docs/plan/mina-prueba.md)
14. [S1-10: modelo de la mina en Python](docs/plan/modelo-mina.md)
15. [Sprint 1: cargador y motor mínimo](docs/plan/entregable-minimo.md)
16. [Sprint 2: costos y rutas con Dijkstra](docs/plan/rutas-costos.md)
17. [Sprint 2: escenarios y línea base](docs/plan/escenarios-comparacion.md)
18. [Sprint 2: gases y ventilación](docs/plan/gases-ventilacion.md)
19. [Nivel 1: mina ampliada y verificación](docs/plan/nivel1-verificacion.md)

### Parte II — Desarrollo (un capítulo por semana)
- [Semana 1](docs/capitulos/semana-01.md)
- *(se agrega un capítulo cada semana a partir de la [plantilla](docs/capitulos/_plantilla.md))*

### Anexos
- [Entrega Nivel 1: revisión y texto para PR](docs/entregas/nivel-1.md)
- [Catálogo de reglas](docs/reglas.md)
- [Registro de decisiones](docs/decisiones.md)
- [Glosario de siglas y términos](docs/glosario.md)
- [Bitácora de sesiones](BITACORA.md)
- [Contexto vivo del proyecto](docs/contexto.md) *(interno)*

## Cronología del código

Cada semana cerrada se marca con un tag (`semana-01`, `semana-02`, …). Cada capítulo enlaza al tag de su semana, para ver el código exacto de ese momento.

## Estructura

```
mina-experta/
├── README.md            # portada e índice
├── BITACORA.md          # diario de sesiones
├── docs/
│   ├── plan/            # enfoque, alcance, cronograma, flujo, sprints, kanban
│   ├── capitulos/       # un capítulo por semana
│   ├── reglas.md        # catálogo de reglas con fuente y prueba
│   ├── decisiones.md    # decisiones de diseño y su porqué
│   └── glosario.md      # siglas y términos técnicos
├── data/                # minas, esquemas, configuración y escenarios JSON
├── src/mina_experta/    # modelo, inferencia, costos, Dijkstra y consola
├── tests/               # pruebas pytest
├── pyproject.toml       # instalación del paquete
└── requirements-dev.txt # herramientas de desarrollo
```

## Ejecución

La consola dispone de 25 tipos de regla, traza, explicación directa y rutas con Dijkstra y costos dinámicos. El punto de control técnico de Nivel 1 incluye una mina de 16 nodos y tres escenarios completos, además de cuatro ejemplos de práctica. Un caso controlado muestra cómo el motor evita un vecino expuesto a humo que el filtro local no identifica. Las capacidades de Nivel 2 siguen pendientes. Desde la raíz del repositorio, con el entorno virtual preparado:

```bash
python -m pip install -e . -r requirements-dev.txt
python -m mina_experta --escenario data/escenarios/nivel1_riesgo_vecino.json --explicar tunel_10_12
python -m mina_experta --desde n5 --co tunel_3_4=120
python -m mina_experta --escenario data/escenarios/co_moderado.json
python ejercicios/nivelacion.py
python -m ejercicios.clases
python -m ejercicios.mina_en_memoria
python -m pytest -q
```

Consulta la [guía de nivelación](docs/plan/nivelacion-python.md) para los objetivos y los casos esperados.
