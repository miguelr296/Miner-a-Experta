"""Demostración S1-10: construir una mina y consultar sus vecinos."""

from mina_experta import Arista, Mina, Nodo


def mostrar_ejemplo():
    mina = Mina("Ejemplo en memoria", [
        Nodo("n1", 0, 0, -50, "frente"),
        Nodo("n2", 100, 0, -50, "refugio"),
        Nodo("n3", 200, 0, 0, "salida"),
    ], [
        Arista("t1", "n1", "n2", 100),
        Arista("t2", "n2", "n3", 120),
    ])
    print(mina.nombre)
    for identificador in mina.nodos:
        print(f"Vecinos de {identificador}:")
        for nodo, arista in mina.vecinos(identificador):
            print(f"  {nodo.id} por {arista.id}: {arista.longitud_m} m")


if __name__ == "__main__":
    mostrar_ejemplo()
