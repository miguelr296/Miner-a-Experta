"""Soluciones de referencia de S1-01; independientes del futuro motor."""


def distancia_total(tramos):
    """Suma las distancias no negativas de un recorrido, en metros."""
    total = 0
    for tramo in tramos:
        total += tramo
    return total


def buscar_por_tipo(nodos, tipo):
    """Filtra identificadores conservando el orden del diccionario."""
    encontrados = []
    for identificador, tipo_nodo in nodos.items():
        if tipo_nodo == tipo:
            encontrados.append(identificador)
    return encontrados


def buscar_por_tipo_comprension(nodos, tipo):
    """Expresa el mismo filtro mediante una comprensión de lista."""
    return [identificador for identificador, tipo_nodo in nodos.items()
            if tipo_nodo == tipo]


def entidades_con_derrumbe(eventos):
    """Recoge entidades con reportes verdaderos, sin duplicados."""
    entidades = set()
    for entidad, atributo, valor in eventos:
        if atributo == "derrumbe_reportado" and valor is True:
            entidades.add(entidad)
    return entidades


def mostrar_ejemplos():
    """Ejecuta un ejemplo de cada ejercicio por consola."""
    print("Distancia total:", distancia_total([120, 80, 150]))
    nodos = {"n1": "frente", "n2": "intersección", "n3": "refugio",
             "n4": "salida", "n5": "refugio"}
    print("Refugios (bucle):", buscar_por_tipo(nodos, "refugio"))
    print("Refugios (comprensión):",
          buscar_por_tipo_comprension(nodos, "refugio"))
    eventos = [("tunel_1_2", "derrumbe_reportado", True),
               ("tunel_2_3", "derrumbe_reportado", False),
               ("tunel_1_2", "derrumbe_reportado", True),
               ("tunel_3_4", "derrumbe_reportado", True)]
    print("Entidades con derrumbe:", sorted(entidades_con_derrumbe(eventos)))


if __name__ == "__main__":
    mostrar_ejemplos()
