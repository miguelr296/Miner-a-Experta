# Mina Experta · Prototipo web

Interfaz sencilla para visualizar las decisiones de un sistema experto de evacuación en minería subterránea. Todo el cálculo ocurre en el navegador: no hay backend ni paso de compilación.

## Cómo abrir

Abre `index.html` con doble clic o arrástralo a un navegador moderno.

Opcionalmente, desde esta carpeta:

```bash
# con Python instalado
python -m http.server 8000
```

Luego visita `http://localhost:8000`.

## Qué puedes hacer

- **Elegir un escenario:** voladura (ESC-01), incendio (ESC-02) o derrumbe con falla de ventilación (ESC-03).
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

En **Decisiones → Ver razonamiento**, selecciona un paso para ubicar al minero, señalar un cierre o comparar las rutas sobre el plano. La leyenda del paso identifica los trazos visibles. Usa **Volver a decisiones** o **Esc** para cerrar la secuencia.

En el escenario de incendio (ESC-02), selecciona la Galería Principal y abre **¿Por qué?**. Lee el evento simulado, las reglas de la traza y el resultado sobre el túnel. Luego abre la decisión de un minero para ver la ruta elegida después del cierre.

- `assets/js/data.js` reúne los hechos iniciales, los umbrales y el catálogo de reglas con su fuente.
- `assets/js/engine.js` aplica las reglas por prioridad, registra la traza y entrega los túneles transitables y sus costos al planificador Dijkstra.
- Cuando un gas alcanza el nivel simulado de peligro, su diagnóstico activa `R-RIESGO-07`. Esta regla eleva el riesgo del túnel, `R-RIESGO-01` lo cierra y `R-RUTA-01` registra el bloqueo para el planificador.

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
