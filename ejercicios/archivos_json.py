"""Práctica S1-05: lectura y escritura de datos, sin definir el esquema de mina."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory


def leer_json(ruta):
    """Lee UTF-8; propaga errores de acceso y JSON inválido al llamador."""
    with Path(ruta).open(encoding="utf-8") as archivo:
        return json.load(archivo)


def escribir_json(ruta, datos):
    """Crea un archivo UTF-8 sin sobrescribir archivos existentes."""
    contenido = json.dumps(datos, ensure_ascii=False, indent=2, allow_nan=False)
    with Path(ruta).open("x", encoding="utf-8") as archivo:
        archivo.write(contenido + "\n")


def mostrar_ejemplo():
    datos = {"nombre": "Mina de práctica", "nodos": [
        {"id": "n1", "tipo": "intersección"},
        {"id": "n2", "tipo": "refugio"},
    ]}
    with TemporaryDirectory(prefix="practica-json-") as carpeta:
        ruta = Path(carpeta) / "ejemplo.json"
        escribir_json(ruta, datos)
        recuperados = leer_json(ruta)
        print(recuperados["nombre"])
        for nodo in recuperados["nodos"]:
            print(f"{nodo['id']}: {nodo['tipo']}")


if __name__ == "__main__":
    mostrar_ejemplo()
