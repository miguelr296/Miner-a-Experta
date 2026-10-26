"""Demostración ejecutable: python -m ejercicios.clases desde la raíz."""

from ejercicios.modelo_aprendizaje import Minero, PuntoControl


def mostrar_ejemplos():
    frente = PuntoControl("n1", "frente")
    refugio = PuntoControl("n3", "refugio")
    ana = Minero("Ana", frente)
    luis = Minero("Luis", frente)

    print("Estado inicial:")
    print(ana.describir())
    print(luis.describir())

    ana.cambiar_ubicacion(refugio)
    print("Tras actualizar solo a Ana:")
    print(ana.describir())
    print(luis.describir())


if __name__ == "__main__":
    mostrar_ejemplos()
