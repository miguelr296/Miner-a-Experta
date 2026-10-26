# Entrega candidata — Nivel 1

[← Índice](../../README.md) · [Verificación funcional](../plan/nivel1-verificacion.md)

Rama acumulativa: **luis/nivel-1-entrega**, en LuisInfinito/Miner-a-Experta. Contiene el trabajo previo y se sincronizó con main del fork, incluidos los PR #1–#5 ya aceptados. La rama se deja sin fusionar para la revisión y aceptación del usuario.

## Descargar y revisar

```bash
git clone --branch luis/nivel-1-entrega --single-branch https://github.com/LuisInfinito/Miner-a-Experta.git
cd Miner-a-Experta
```

Si ya tienes el repositorio, guarda tus cambios locales antes de cambiar de rama y usa:

```bash
git fetch origin
git switch luis/nivel-1-entrega
```

Sigue el [inicio rápido del README](../../README.md#inicio-rápido--nivel-1) para crear el entorno, instalar y ejecutar. No copies una carpeta .venv de otra máquina. Esta entrega usa los archivos JSON del checkout y Python 3.12.

## Qué revisar

| Comprobación | Resultado esperado |
|---|---|
| Suite completa | 334 pruebas aprobadas |
| Escenario nivel1_gases | Desvío de Ana: n13 → n15 → n6 → n10 → n9 → n11; 500 m |
| Escenario nivel1_derrumbe | Luis en n16 queda sin ruta; no es un fallo del programa |
| Escenario nivel1_riesgo_vecino | Sistema: 500 m sin cruzar el vecino; filtro: 420 m cruzándolo |
| --explicar tunel_10_12 en riesgo vecino | R25 justifica el cierre por expuesto_humo; la traza previa conserva el foco y la relación |
| Archivo o ruta vacía | Error con código 2, sin sustituir silenciosamente un dato predeterminado |

La inferencia vecina tiene un control: al retirar solo R24/R25, el sistema recupera la misma ruta que la línea base. No se mide una mejora real de seguridad: el riesgo de humo está definido como supuesto explícito de un salto.

## Contenido

- Modelo inmutable, cargador estricto y validación de distancia a refugios.
- Motor propio con prioridad, refracción, traza y explicación directa.
- Gases CO, NO₂, CO₂, H₂S, O₂; ventilación con ANFO y eventos de incendio/derrumbe.
- Umbrales y factores JSON, separados del motor y de las longitudes físicas.
- Dijkstra propio con costos dinámicos, cierres y rutas por ubicación de minero.
- Comparador independiente: Dijkstra con filtro directo sobre los mismos datos originales.
- Mina de 16 nodos, 20 túneles, dos niveles subterráneos, dos salidas, tres refugios y cuatro frentes.
- Tres escenarios Nivel 1 y cuatro ejemplos pequeños conservados.

## Validación y límites

La comprobación local se hace en Linux con Python 3.12. La CI de `.github/workflows/pruebas.yml` ejecutará instalación, suite y tres escenarios en Linux y Windows con Python 3.12. Configurar esa CI no acredita que ya haya terminado una ejecución remota; revisa sus resultados en GitHub antes de integrar.

La revisión se ejecutó en una copia limpia de los archivos versionados, con entorno virtual nuevo e instalación del proyecto: 334 pruebas aprobadas y los siete escenarios ejecutados desde fuera del checkout. También se construyó e instaló la distribución Python sin dependencias externas de ejecución y se ejecutaron allí los tres escenarios de Nivel 1, con sus datos proporcionados desde el checkout. Los resultados se registran en BITACORA.md. La ejecución de CI remota, incluido Windows, no está confirmada desde este entorno.

No se incluyen factores de certeza, A*, decisiones automáticas de refugio/brigada ni explicación recursiva de Nivel 2. Los umbrales de emergencia y la exposición vecina son supuestos académicos. No se validó el modelo en una mina real ni se volvió a verificar la normativa durante esta preparación de entrega. Los capítulos y registros históricos conservan sus resultados de sesiones anteriores; el estado actual está en esta guía y en el contexto actualizado.

## Texto propuesto para el PR

**Título:** feat: completar Nivel 1 con inferencia explicable y rutas de evacuación

**Descripción:**

El repositorio pasa de los fundamentos iniciales a una entrega ejecutable por consola: carga una mina de 16 nodos y 20 túneles, evalúa 25 tipos de regla y calcula rutas con Dijkstra y costos dinámicos para varios mineros. Incluye gases, ventilación con ANFO, incendio, derrumbe, explicación directa y tres escenarios completos comparados con una línea base filtrada.

El escenario de riesgo vecino registra incendio → foco → exposición del vecino → cierre. El sistema evita el túnel expuesto con un recorrido de 500 m; el filtro local toma uno de 420 m que lo atraviesa. Un control sin la inferencia vecina recupera la ruta del filtro. Las relaciones de humo y los niveles de emergencia se declaran como supuestos de simulación.

Validación: 334 pruebas locales aprobadas; instalación limpia y tres escenarios por consola. Se añade CI para Python 3.12 en Linux y Windows; su resultado remoto queda por revisar. Nivel 2 está fuera de este PR.

## Integración en el fork y el grupo

1. Abre un PR en el fork, base main y comparación luis/nivel-1-entrega. Revisa las pruebas de GitHub y el diff; luego acepta y fusiona si el resultado es el esperado.
2. Para el grupo, crea otro PR con el repositorio grupal como base y tu fork/main como comparación, después de aceptar la entrega en el fork. Verifica explícitamente esos repositorios en la pantalla de comparación.
3. Usa el texto anterior y enlaza la tarjeta real del grupo si corresponde. No se inventó un número de issue ni se cerraron tarjetas o semanas automáticamente.

El asistente publica esta rama, pero no fusiona en main ni envía el PR al grupo en nombre del usuario. La aceptación e integración siguen bajo control del usuario.
