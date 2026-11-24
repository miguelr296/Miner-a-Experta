# Mina Experta · Prototipo web

Interfaz sencilla para visualizar las decisiones de un sistema experto de evacuación en minería subterránea. Todo el cálculo ocurre en el navegador: no hay backend ni paso de compilación.

Consulta el [registro de cambios y motivos](CAMBIOS.md) para revisar esta rama.

## Cómo abrir

Abre `index.html` con doble clic o arrástralo a un navegador moderno.

Opcionalmente, desde esta carpeta:

```bash
# con Python instalado
python -m http.server 8000
```

Luego visita `http://localhost:8000`.

## Qué puedes hacer

- **Elegir un escenario:** voladura (ESC-01), incendio (ESC-02) derrumbe con falla de ventilación (ESC-03), inundación (ESC-04) o corte eléctrico (ESC-05).
- **Revisar el plano:** los túneles se colorean según su nivel de riesgo; el túnel seleccionado muestra una ruta azul.
- **Filtrar por nivel:** botones *Todo el plano*, *Nivel 1* y *Nivel 2*.
- **Comparar con la línea base:** activa el interruptor *Línea base* para ver la ruta sin costos de riesgo.
- **Ver decisiones:** cada tarjeta indica si la persona debe evacuar, refugiarse o esperar.
- **Abrir explicaciones:** haz clic en una tarjeta o usa *Ver detalle*; también puedes hacer clic en un túnel del plano y pulsar *¿Por qué?*.
- **Consultar la base de reglas:** botón *Catálogo de reglas* en la barra superior.
- **Cambiar de pestaña:** Decisiones, Reglas, Registro y Comparar.

## Probar datos y cambiar el tema

Selecciona un túnel en **Probar datos**, modifica lecturas o eventos y pulsa **Aplicar y recalcular**. El aviso del plano permite volver al escenario original. El formulario incluye los cinco gases del motor y permite ensayar valores por encima de los umbrales de peligro del modelo.

El botón **Modo oscuro** alterna entre los dos temas. Al abrir la aplicación por primera vez se usa la preferencia del sistema. Si el navegador permite el almacenamiento local, se recuerda el tema elegido.

## Cómo seguir el razonamiento

En **Decisiones → Ver razonamiento**, la vista detallada muestra la regla, el recorrido, el costo y la comparación con la línea base. Pulsa **Ver secuencia interactiva en el plano** para resaltar los pasos de la decisión. Desde el panel del plano puedes volver a la **Vista detallada** y retomar el paso seleccionado.

En el escenario de incendio (ESC-02), selecciona la Galería Principal y abre **¿Por qué?**. Lee el evento simulado, las reglas de la traza y el resultado sobre el túnel. Luego abre la decisión de un minero para ver la ruta elegida después del cierre.

- `assets/js/data.js` reúne los hechos iniciales, los umbrales y el catálogo de reglas con su fuente.
- `assets/js/engine.js` aplica las reglas por prioridad, registra la traza y entrega los túneles transitables y sus costos al planificador Dijkstra.
- Cuando un gas alcanza el nivel simulado de peligro, su diagnóstico activa `R-RIESGO-07`. Esta regla eleva el riesgo del túnel, `R-RIESGO-01` lo cierra y `R-RUTA-01` registra el bloqueo para el planificador.

## Guardar escenarios propios

Selecciona un escenario de partida y usa **Probar datos** para cambiar las lecturas o los eventos de uno o varios túneles. Aplica los cambios de cada túnel antes de pasar al siguiente. **Volver al escenario original** descarta todos los cambios sin guardar.

En el panel **Escenarios**, pulsa **Guardar como** y escribe un nombre y, si quieres, una descripción. La copia conserva los mineros y sus ubicaciones, y aparece en el selector. Se guarda en el navegador si el almacenamiento local está disponible. Las reglas de simulación activas se aplican al abrir cualquier escenario y se gestionan por separado desde el catálogo.

Para borrar una copia guardada, pulsa **Eliminar** debajo de su tarjeta y confirma el nombre en el diálogo. Si la copia está activa, la aplicación vuelve a **Voladura**. Los escenarios originales siempre siguen disponibles.

## Compartir un caso en JSON

En el panel **Escenarios**, abre **Importar o exportar**. Puedes descargar el escenario activo, incluidas las lecturas personalizadas que todavía no hayas guardado. Marca **Incluir reglas de simulación activas** para compartir también las condiciones y los efectos de esas reglas. El JSON contiene datos y parámetros de reglas.

Al importar, la app valida el formato y guarda una copia con nombre propio. El caso importado usa sus propias reglas de simulación, incluso al abrirlo de nuevo. Si el archivo omite las reglas, el caso se ejecuta con el catálogo original. Editar reglas en ese caso solo afecta a esa copia. Los otros escenarios conservan las reglas de su sesión. El archivo está pensado para la topología incluida en esta versión del prototipo.

## Añadir reglas de simulación

Abre **Catálogo de reglas → Reglas de simulación**. Selecciona el sensor, la comparación, el umbral y el efecto. **Añadir y recalcular** muestra cuántas activaciones hubo y cuántos túneles cambiaron. Las reglas simuladas aparecen con un identificador `SIM-xx` en la pestaña **Reglas** y en la traza del túnel cuando se activan.

Para probarlo, en **Voladura (ESC-01)** añade **CO mayor que 80 ppm → Peligro inmediato**. La Galería 340-N, con 88 ppm en el escenario, queda cerrada y Jorge pasa a esperar a la brigada. Cambia de escenario para usar la misma regla con otros datos o retírala para comparar con el resultado original. Las reglas de sesión se descartan al recargar. Las reglas propias de un caso importado se guardan con ese caso.

## Escenarios con nuevos factores

- **ESC-04 · Inundación.** El tramo final de la Rampa de Escape se cierra con gases en valores de referencia. En **Decisiones**, Elmer pasa de la salida sur al Socavón Principal.
- **ESC-05 · Corte eléctrico.** El Crucero Norte sube a riesgo alto porque pierde la ventilación y su respaldo. La Rampa Central conserva el respaldo y la regla no se activa allí. Para Jorge, la ruta pasa de 470 m en la línea base a 480 m por el desvío del sistema.

Puedes cambiar estos eventos desde **Probar datos** y compararlos en **¿Por qué?**. El [catálogo](../docs/reglas.md#reglas-del-prototipo-web-para-esc-04-y-esc-05) incluye las condiciones, prioridades y motivos de las reglas.

## Demostración del motor

En **Voladura (ESC-01)**, abre **Probar datos**, selecciona **Galería 340-N** y cambia solo el CO de 88 a 101 ppm. Aplica los datos y abre **¿Por qué? → Ver motor paso a paso** en ese túnel. Busca las activaciones `R-CO-03`, `R-RIESGO-07`, `R-RIESGO-01` y `R-RUTA-01`. Cada una muestra qué consultó el motor y qué escribió en la memoria de hechos. El selector incluye las demás reglas disparadas en el túnel.

En **Decisiones → Jorge Salazar → Ver razonamiento** puedes comprobar el efecto del cierre. En el código, abre `inferirTuneles` en `assets/js/engine.js` para mostrar el bucle de reglas, y `construirGrafo` en `assets/js/planner.js` para mostrar dónde se excluye el tramo cerrado.

## Comparar un recálculo

Después de aplicar lecturas, añadir o retirar una regla, restaurar los datos o pulsar **Ejecutar inferencia**, el plano muestra un resumen. **Ver antes y después** abre los túneles y mineros afectados con sus valores anteriores y nuevos, y permite abrir la traza del túnel o el razonamiento del minero para el resultado actual. La cuenta de rutas distintas refleja cambios en el recorrido. Si solo varía el costo o el puntaje de riesgo, el detalle también lo muestra.

## Pruebas y resultados de referencia

Desde la raíz del repositorio, ejecuta `python -m pytest tests/test_escenarios_web.py` con pytest y Node.js instalados. Las pruebas ejecutan el motor JavaScript y comprueban umbrales, prioridades, cierres, refugios, empates e intercambio JSON.

El [archivo de referencia](../tests/fixtures/escenarios_web.json) fija las entradas y los resultados esperados de los cinco escenarios. Incluye el estado y costo de los túneles afectados y, por minero, la regla de decisión y las rutas con su secuencia de nodos, distancia, costo y puntaje de riesgo. Cada túnel afectado se representa como `[id, nivel, cerrado, costo]`. Un cierre tiene costo `null` y una ruta ausente se representa con `null`.

Ante dos destinos con el mismo costo ajustado, el planificador experto elige el de menor puntaje de riesgo. La línea base conserva su criterio por distancia. La referencia registra decisiones de la simulación académica y puede reutilizarse para comparar la futura implementación en Python.

## Enlaces directos útiles

- `index.html?esc=ESC-02`
- `index.html?esc=ESC-03&tab=reglas`
- `index.html?ver=catalogo`
- `index.html?ver=tunel:t_i2_r1`
- `index.html?ver=minero:m3`

## Estructura

```
index.html
assets/
  css/styles.css
  js/data.js      # escenarios, mina, mineros y reglas
  js/engine.js        # memoria de hechos e inferencia
  js/planner.js       # Dijkstra y decisiones por minero
  js/explanations.js  # explicaciones a partir de la traza
  js/theme.js         # preferencia de tema
  css/theme.css       # paleta oscura
  js/app.js       # dibujo del plano e interacción
```

> Prototipo académico. Los umbrales normativos se basan en el DS 024-2016-EM; los niveles de emergencia y multiplicadores son supuestos declarados del equipo.
