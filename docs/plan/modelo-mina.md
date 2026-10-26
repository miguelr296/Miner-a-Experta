# S1-10 — Modelo de la mina en Python

[← Índice](../../README.md)

El paquete `mina_experta`, ubicado en `src/mina_experta/`, contiene las clases `Nodo`, `Arista` y `Mina`. Instálalo desde la raíz con el entorno virtual activado:

```bash
python -m pip install -e . -r requirements-dev.txt
python -m ejercicios.mina_en_memoria
python -m pytest -q
```

`-e .` instala el proyecto de forma que los cambios en `src/` se puedan usar sin reinstalarlo. `pyproject.toml` describe ese paquete y la versión mínima de Python. No hay dependencias de ejecución externas para el modelo.

## Uso público

```python
from mina_experta import Arista, Mina, Nodo

frente = Nodo("n1", 0, 0, -50, "frente")
refugio = Nodo("n2", 100, 0, -50, "refugio")
tunel = Arista("t1", "n1", "n2", 100)
mina = Mina("Ejemplo", [frente, refugio], [tunel])

for vecino, arista in mina.vecinos("n1"):
    print(vecino.id, arista.longitud_m)
```

El ejemplo imprime `n2 100`. Consultar los vecinos de `n2` devuelve el mismo túnel hacia `n1`. La demostración ejecutable añade una salida y muestra todas las conexiones.

Los nodos y las aristas no se pueden modificar una vez creados. Las colecciones `mina.nodos` y `mina.aristas` permiten consulta por identificador, pero no inserción o eliminación. `vecinos(id)` devuelve pares `(Nodo, Arista)` en una tupla y conserva el orden de entrada de los túneles. Un nodo aislado devuelve una tupla vacía; uno inexistente genera `KeyError`.

El constructor rechaza nombres vacíos, identificadores inválidos o repetidos, coordenadas no finitas, tipos de nodo desconocidos, longitudes no positivas, extremos ausentes, túneles hacia sí mismos, pares repetidos y longitudes inferiores a la distancia recta 3D. Estos datos incoherentes generan `ValueError`.

Todavía se permiten minas parciales o desconectadas para construir y probar el modelo. El cargador de S1-11 exigirá además una mina completa y conectada, los tipos requeridos y el recorrido de hasta 500 m a un refugio. No se han implementado aún la lectura del JSON, los costos de riesgo ni las rutas.

El siguiente paso es S1-11: cargar `data/mina_prueba.json` y comprobar los requisitos globales. El diseño del motor de S1-12 sigue pendiente dentro del sprint.
