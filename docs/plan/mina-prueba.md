# S1-09 — Mina académica de prueba

[← Índice](../../README.md)

[mina_prueba.json](../../data/mina_prueba.json) contiene ocho nodos y ocho túneles bidireccionales conforme a D20 y al [esquema](esquema-mina.md). Es un escenario geométrico ficticio, todavía sin sensores, emergencias ni mineros. No representa una instalación real.

## Lugares y conexiones

| Nodo | Tipo | Coordenadas `(x, y, nivel)` en metros |
|---|---|---|
| n1 | Salida | (0, 0, 0) |
| n2 | Intersección | (100, 0, -50) |
| n3 | Intersección | (200, 0, -50) |
| n4 | Refugio | (300, 0, -50) |
| n5 | Frente | (450, 0, -50) |
| n6 | Intersección | (200, 100, -100) |
| n7 | Frente | (400, 100, -100) |
| n8 | Intersección | (300, 100, -100) |

La salida está en superficie y los nodos subterráneos se distribuyen en cotas de −50 y −100 m. Los túneles conectan n1–n2 (120 m), n2–n3 (100 m), n3–n4 (100 m), n4–n5 (150 m), n3–n6 (120 m), n6–n8 (100 m), n8–n7 (100 m) y n8–n4 (120 m).

El circuito n3–n4–n8–n6–n3 permite practicar más adelante rutas alternativas. No garantiza alternativas ante cualquier cierre: por ejemplo, n5 tiene una sola conexión. Todos los nodos son alcanzables en el estado base.

## Evidencia de D10

| Frente | Recorrido hasta el refugio n4 | Longitud |
|---|---|---|
| n5 | n5 → n4 | 150 m |
| n7 | n7 → n8 → n4 | 100 + 120 = 220 m |

Ambos recorridos existen y suman menos de 500 m. Son pruebas de existencia de una ruta válida; no afirmamos que ya haya un planificador calculando rutas mínimas. Las longitudes de todos los túneles son al menos la distancia recta 3D de sus extremos.

## Comprobación

Desde la raíz del repositorio, con el entorno virtual activado:

```bash
python -m pytest tests/test_mina_prueba.py -q
python -m pytest -q
```

Las pruebas leen el archivo real y comprueban esquema, tamaño, tipos, identificadores, extremos, pares de nodos, geometría, conectividad y los dos recorridos documentados. Estas comprobaciones protegen este entregable concreto; el validador general y los errores de carga corresponden a S1-11.

Después corresponde S1-10: implementar las clases `Nodo`, `Arista` y `Mina`, con consulta de vecinos. La lectura del JSON para construir esos objetos vendrá en S1-11.
