# S1-05 — Leer y escribir JSON

[← Índice](../../README.md)

Tras S1-02 practicamos archivos JSON con la biblioteca estándar, sin dependencias nuevas. Ejecuta desde la raíz, con el entorno virtual activado:

```bash
python -m ejercicios.archivos_json
python -m pytest -q
```

El ejemplo escribe en una carpeta temporal, lee el archivo e imprime:

```text
Mina de práctica
n1: intersección
n2: refugio
```

La carpeta temporal se elimina al terminar. El ejemplo todavía no es `mina_prueba.json` ni define su esquema; eso corresponde a S1-08 y S1-09.

En [archivos_json.py](../../ejercicios/archivos_json.py), `json.load` transforma el contenido del archivo en diccionarios y listas. `json.dumps` hace la conversión inversa a texto. Los booleanos JSON `true` y `false` se convierten en `True` y `False`; `null` se convierte en `None`. Las tuplas no son un tipo JSON.

`with` cierra el archivo incluso si ocurre un error. UTF-8 permite conservar acentos. El modo `x` crea un archivo nuevo y rechaza sobrescribir uno existente. La conversión se realiza antes de abrirlo para evitar crear archivos cuando los datos no se pueden convertir; no es una garantía de escritura atómica ante errores de disco.

Las pruebas comprueban lectura de un archivo independiente, ida y vuelta con tipos JSON, acentos, archivo ausente, JSON mal formado y protección de archivos existentes. También verifican que datos no serializables no creen archivos. Leer JSON válido no valida el esquema de una mina.

El criterio técnico de S1-05 queda cubierto por un script que lee JSON y muestra sus datos. La comprensión individual sigue pendiente de revisión con el usuario. El siguiente paso del orden sugerido es S1-07: ciclo del motor, encadenamiento hacia adelante y refracción, antes de diseñar el esquema en S1-08.
