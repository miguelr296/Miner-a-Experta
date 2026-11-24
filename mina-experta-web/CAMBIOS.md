# Cambios del prototipo web y motivos

Esta revisión incorpora la demo de Mina Experta al repositorio y reúne los ajustes realizados para explicar el razonamiento en una presentación. El prototipo se ejecuta en el navegador con JavaScript y datos simulados. El plan del curso describe la implementación prevista en Python. Para ejecutar la demo, abre [index.html](index.html).

## Cambios por iteración

| Commit | Qué cambió | Por qué |
| --- | --- | --- |
| `23b99eb` | Se incorporó el ZIP inicial con el plano, los escenarios, el catálogo, el motor y la interfaz. Se añadió `R-RIESGO-07` para elevar el riesgo del túnel cuando un gas llega a peligro. | La demo quedaba fuera del repositorio y el motor podía diagnosticar peligro por gas sin cerrar el túnel. La nueva regla conecta el diagnóstico con el cierre y deja visible esa transición en la traza. |
| `6e8106c` | Se integró **Probar datos** del segundo ZIP. Se separaron inferencia, planificación y explicaciones. Se añadieron un selector de tema, una explicación del túnel en tres partes y una comparación con cobertura equivalente. | Queríamos probar una lectura en vivo y ver su efecto, conservar el motor fácil de revisar y comparar el puntaje solo entre mineros con salida en ambos métodos. |
| `d8c2a5a` | Se ajustaron fondos, textos, colores de riesgo, etiquetas del SVG, bordes, foco y estados de botones en modo oscuro. Los tooltips reutilizan las clases de riesgo y decisión. | El tema oscuro todavía usaba fondos y colores fijos del claro. Compartir estilos reduce las diferencias entre etiquetas que representan el mismo estado. |
| `6126f0d` | Se reorganizó la explicación por minero en ubicación, cierres, rutas evaluadas y decisión. Se añadió una referencia por distancia para identificar cierres. Se corrigieron motivos de las tarjetas que atribuían el aislamiento a un derrumbe o daban por despejada una ruta. | La tarjeta debía explicar el motivo que se desprende de los hechos de cada escenario. Para explicar un desvío por cierre hacía falta una referencia que mostrara por dónde iría el camino más corto. |
| `5f59c9d` | Se explica el desempate cuando dos rutas tienen el mismo costo ajustado y el planificador prefiere la de menor puntaje de riesgo. | Las distancias y el costo por sí solos dejaban sin explicar casos como el de Jorge en el incendio. |
| `a3ee036` | Se añadió una secuencia junto al plano. Cada paso puede resaltar ubicación, tramo cerrado o riesgoso, alternativa y ruta elegida. La leyenda refleja los trazos visibles. | El público puede relacionar cada explicación con el lugar donde ocurre. Durante la secuencia se muestra el plano completo para que se vean recorridos entre niveles. |
| `20be463` | Se recuperó la vista detallada con decisión, regla, recorrido, costo y comparación. Se puede pasar de esa vista a la secuencia y volver al mismo paso. | La vista detallada sirve para consultar los valores y la secuencia para seguir la decisión sobre el plano. |
| `a38b827` | La traza del túnel registra los hechos leídos por la condición, su origen y los valores antes y después de cada escritura. **Ver motor paso a paso** permite inspeccionar una activación. | El detalle se produce durante la inferencia y permite auditar una decisión con las lecturas recién introducidas. |

## Ampliación del prototipo para la revisión

| Qué cambió | Por qué y cómo comprobarlo |
| --- | --- |
| **Reglas de simulación desde el catálogo.** Se puede añadir o retirar una condición de sensor con umbral y efecto de riesgo. | Permite comparar resultados sin cambiar código. En Voladura, añade CO > 80 ppm → peligro y busca la regla SIM en la traza de la Galería 340-N. |
| **Escenarios propios.** Se acumulan cambios de varios túneles, se guarda una copia con nombre y se puede eliminar. | Permite repetir una variante sin tocar los casos originales. Al borrar la copia activa, la app vuelve a Voladura. |
| **ESC-04 e inundación.** Una regla de diagnóstico traduce el reporte en peligro y reutiliza la cadena de cierre. | Demuestra un bloqueo físico con gases en referencia. Ambas estrategias excluyen la Rampa de Escape cerrada. |
| **ESC-05 y corte eléctrico.** La regla distingue si la ventilación de respaldo está operativa. | Demuestra un desvío por costo sin cierre. Jorge recorre 480 m frente a 470 m por el trayecto de la línea base. |
| **Importación y exportación JSON.** Se exporta el escenario activo con reglas opcionales y se importa como copia. | Permite compartir un caso reproducible. Las reglas de una copia importada se guardan y se aplican solo a esa copia. |
| **Pruebas y resultados de referencia.** Se fijaron las entradas, cierres, costos, decisiones y rutas de los cinco casos. | Permite comprobar regresiones y comparar la implementación futura. Se corrigió el desempate entre destinos de igual costo para preferir la de menor puntaje de riesgo. |
| **Antes y después del recálculo.** Lista túneles y mineros afectados, muestra ambas lecturas del resultado y enlaza sus explicaciones. | Permite identificar los efectos de una regla o un cambio de datos sin recorrer todos los paneles. |
| **Modo presentación.** Agranda etiquetas y permite plegar los laterales. El panel de decisiones vuelve al abrir la secuencia interactiva. | Da más espacio al plano durante la demo y permite seguir el razonamiento junto al mapa. |

Las condiciones, prioridades y justificaciones de `R-INU-01` y `R-VEN-04` figuran en el [catálogo](../docs/reglas.md#reglas-del-prototipo-web-para-esc-04-y-esc-05). El [archivo de referencia](../tests/fixtures/escenarios_web.json) contiene los cinco casos.

## Datos, reglas y rutas

- **Simulación.** El formulario modifica las lecturas y eventos de un túnel a la vez y acumula los cambios en una copia del escenario. Se pueden editar los cinco gases, incluida la incorporación de H₂S. El máximo del control de CO₂ permite superar el umbral de peligro del modelo. Las ayudas de los gases se derivan de la configuración y los preajustes agilizan la demostración. El aviso del plano permite restaurar el escenario original.
- **Cierre por gas.** `R-RIESGO-07` pertenece a la categoría RIESGO, tiene prioridad 79 y se registra como SUPUESTO (D09/D12). Si un gas está en peligro inmediato, escribe `nivel_riesgo = peligro`. Después `R-RIESGO-01` escribe `cerrado = true` y `R-RUTA-01` registra `transitable = false`. El planificador omite el túnel cerrado al construir el grafo.
- **Comparación.** La línea base usa distancia y bloquea tramos críticos. El sistema aplica los costos ajustados por riesgo. El puntaje suma niveles simulados por tramo y los totales se calculan para los mismos mineros en ambos métodos. La referencia por distancia sin restricciones se consulta únicamente para explicar cierres en el camino hipotético más corto.
- **Traza.** Las lecturas reflejan los atributos consultados por la condición al evaluarse. Una condición con cortocircuito puede omitir otros atributos. Las escrituras incluyen el valor anterior y la conclusión registrada. La vista presenta las reglas disparadas. Los conflictos registrados se muestran en su propia sección.

## Dónde revisar el código

| Archivo | Responsabilidad |
| --- | --- |
| [data.js](assets/js/data.js) | Plano, lecturas iniciales, escenarios, umbrales y catálogo de reglas con fuente. |
| [engine.js](assets/js/engine.js) | Memoria de hechos, condiciones de las reglas, prioridad, refracción, traza y ejecución del escenario. |
| [planner.js](assets/js/planner.js) | Construcción de grafos, Dijkstra y decisión de evacuar, refugiarse o esperar. |
| [explanations.js](assets/js/explanations.js) | Explicaciones por túnel y minero, con referencias a los elementos que se resaltan. |
| [app.js](assets/js/app.js) e [index.html](index.html) | Interacción, formulario, plano, vistas de razonamiento y selector del paso del motor. |
| [styles.css](assets/css/styles.css), [theme.css](assets/css/theme.css) y [theme.js](assets/js/theme.js) | Estilos, contrastes y preferencia de tema. La primera apertura sigue el sistema y la selección se recuerda cuando el navegador permite el almacenamiento local. |

## Verificación y revisión

- Se ejecutaron los cinco escenarios en Node.js. Las nueve pruebas de regresión cubren resultados de referencia, umbrales, empates, cierres, intercambio y recálculo. En el escenario de derrumbe se verificaron las tres recomendaciones: evacuar, refugiarse y esperar a la brigada.
- Se probó el cierre por cada gas de forma aislada y se verificó la cadena de reglas y su efecto en la ruta.
- Se verificaron con DOM simulado las vistas de razonamiento, la navegación entre pasos, el retorno al mismo punto del plano y la persistencia del tema.
- Se calcularon relaciones de contraste para 15 pares de colores del tema oscuro. El mínimo de los pares de texto evaluados fue 5,84:1.
- Para revisar en navegador, seguir el [guion de demostración](README.md#demostración-del-motor), comprobar los resaltados en ambos temas y restaurar el escenario. La revisión visual completa y al 125 % de zoom queda pendiente. El comportamiento de los paneles se comprobó con un DOM simulado.

Los datos, umbrales de emergencia y multiplicadores describen una simulación académica.
