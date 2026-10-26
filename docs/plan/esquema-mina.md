# S1-08 — Esquema JSON de la mina

[← Índice](../../README.md)

El [esquema comprobable](../../data/esquemas/mina.schema.json) y D20 del [registro de decisiones](../decisiones.md) definen la versión 1. Este archivo contiene la estructura fija de una mina. Los sensores, las posiciones de mineros, los eventos y los umbrales tendrán archivos separados; no se incorporan todavía a este contrato.

## Campos obligatorios

| Elemento | Campos | Significado |
|---|---|---|
| Mina | `version`, `nombre`, `nodos`, `aristas` | Versión entera 1, nombre no vacío, listas no vacías |
| Nodo | `id`, `x`, `y`, `nivel`, `tipo` | Identificador, coordenadas en metros y función del lugar |
| Arista | `id`, `origen`, `destino`, `longitud_m` | Identificador del túnel, extremos y longitud física positiva |

Los identificadores empiezan por una letra minúscula y continúan con letras minúsculas sin acentos, dígitos o guiones bajos. Por ejemplo, `n1` y `tunel_1_2`. Cada identificador es único en su colección. Los tipos son exactamente `interseccion`, `salida`, `refugio` y `frente`; los valores de máquina no llevan acentos. Se rechazan campos desconocidos para detectar errores al escribirlos.

`nivel` es la tercera coordenada espacial en metros, no el número de piso. Adoptamos superficie en 0 y cotas subterráneas negativas. Dos lugares pueden compartir coordenadas, pero conservan identificadores distintos.

Cada túnel se registra una sola vez y permite tránsito en ambos sentidos en esta versión. `origen` y `destino` no imponen una dirección. No se admiten túneles de un nodo a sí mismo ni dos túneles entre el mismo par de nodos. Un cierre posterior afectará ambos sentidos. La ventilación no se modela como dirección de circulación de personas.

`longitud_m` es la distancia real del recorrido, que puede superar la distancia en línea recta entre sus extremos. Es el costo base por distancia. Los multiplicadores de riesgo y cierres se aplicarán después (D01); no se guardan como estado mutable en este archivo.

## Dos niveles de comprobación

El esquema comprueba campos, tipos, listas, identificadores, tipos de nodo y longitudes positivas. No tiene referencias externas que deban descargarse al validar.

El cargador de S1-11 deberá comprobar además:

1. Identificadores únicos en cada colección y extremos que existan.
2. Ausencia de túneles hacia sí mismos y pares repetidos, incluso con los extremos invertidos.
3. Números finitos; rechazo de extensiones no estándar como `NaN` e `Infinity` y claves JSON repetidas.
4. Longitud de cada túnel al menos igual a la distancia euclidiana 3D entre sus extremos. Así la futura heurística no sobreestima la distancia (D01).
5. Al menos un frente, un refugio y una salida. Todos los nodos deben pertenecer a una misma mina conectada en su estado base.
6. Para cada frente, existencia de un recorrido hacia algún refugio de longitud total **menor o igual a 500 m**, sumando `longitud_m` (D10). La distancia en línea recta no basta. El algoritmo para comprobarlo será propio, sin NetworkX.

La comprobación de 500 m describe la mina base; no garantiza que una emergencia mantenga transitables esos túneles. Los recuentos de 6–8 nodos para S1-09 y de 15–20 nodos con dos niveles para Nivel 1 son criterios de los entregables, no límites rígidos del formato.

## Cómo comprobar el esquema

Con el entorno virtual activado, desde la raíz:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest tests/test_esquema_mina.py -q
python -m pytest -q
```

La dependencia `jsonschema` se usa solo para verificar el contrato durante el desarrollo. No implementa el motor ni algoritmos de rutas. Las pruebas usan una muestra mínima dentro de la suite, comprueban el propio esquema y rechazan variantes mal formadas. No validan aún las relaciones del grafo ni sustituyen al futuro cargador.

El siguiente paso es S1-09: crear `data/mina_prueba.json` con 6–8 nodos, respetando este contrato y mostrando un recorrido de hasta 500 m desde cada frente hasta un refugio.
