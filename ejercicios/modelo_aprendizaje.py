"""Clases didácticas de S1-02; no definen el modelo definitivo de la mina."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PuntoControl:
    """Datos de una ubicación de ejemplo, sin grafo ni reglas de seguridad."""

    identificador: str
    tipo: str


class Minero:
    """Ejemplo de inicialización explícita y estado propio de cada instancia."""

    def __init__(self, nombre: str, ubicacion: PuntoControl):
        self.nombre = nombre
        self.ubicacion = ubicacion

    def cambiar_ubicacion(self, destino: PuntoControl) -> None:
        """Actualiza el ejemplo; no calcula ni autoriza rutas de evacuación."""
        self.ubicacion = destino

    def describir(self) -> str:
        return f"{self.nombre}: {self.ubicacion.identificador} ({self.ubicacion.tipo})"
