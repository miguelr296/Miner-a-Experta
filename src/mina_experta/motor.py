"""Motor propio: hechos inmutables, reglas por entidad, prioridad y refracción."""

from dataclasses import dataclass
from itertools import product
import math


type Valor = str | int | float | bool | None
type Hecho = tuple[str, str, Valor]


def _validar_valor(valor):
    if type(valor) not in (str, int, float, bool, type(None)):
        raise ValueError("El valor de un hecho debe ser un escalar JSON")
    if type(valor) in (int, float):
        try:
            finito = math.isfinite(valor)
        except OverflowError:
            finito = False
        if not finito:
            raise ValueError("El valor numérico debe ser finito")


def _clave(hecho):
    if not isinstance(hecho, tuple) or len(hecho) != 3:
        raise ValueError("Un hecho debe ser una tupla (entidad, atributo, valor)")
    entidad, atributo, valor = hecho
    if not all(isinstance(texto, str) and texto.strip() for texto in (entidad, atributo)):
        raise ValueError("Entidad y atributo deben ser textos no vacíos")
    _validar_valor(valor)
    # Python considera True == 1. Aquí un evento booleano no es una medición.
    tipo = "numero" if type(valor) in (int, float) else type(valor).__name__
    return entidad, atributo, tipo, valor


@dataclass(frozen=True)
class Condicion:
    atributo: str
    operador: str
    valor: Valor
    entidad: str | None = None

    def __post_init__(self):
        _clave(("ejemplo", self.atributo, self.valor))
        if self.entidad is not None:
            _clave((self.entidad, self.atributo, self.valor))
        if self.operador not in ("eq", "gt", "ge", "lt", "le"):
            raise ValueError(f"Operador desconocido: {self.operador}")
        if self.operador != "eq" and type(self.valor) not in (int, float):
            raise ValueError("Las comparaciones ordenadas requieren números")

    def cumple(self, hecho: Hecho) -> bool:
        if self.entidad is not None and hecho[0] != self.entidad:
            return False
        if hecho[1] != self.atributo:
            return False
        valor = hecho[2]
        if self.operador == "eq":
            return _clave(("e", "a", valor)) == _clave(("e", "a", self.valor))
        if type(valor) not in (int, float):
            return False
        if self.operador == "gt":
            return valor > self.valor
        if self.operador == "ge":
            return valor >= self.valor
        if self.operador == "lt":
            return valor < self.valor
        return valor <= self.valor


@dataclass(frozen=True)
class Regla:
    id: str
    condiciones: tuple[Condicion, ...]
    conclusiones: tuple[tuple[str, Valor], ...]
    prioridad: int = 0
    entidad: str | None = None

    def __post_init__(self):
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValueError("La regla requiere identificador")
        if type(self.prioridad) is not int:
            raise ValueError("La prioridad debe ser entera")
        if self.entidad is not None:
            _clave((self.entidad, "destino_regla", True))
        object.__setattr__(self, "condiciones", tuple(self.condiciones))
        object.__setattr__(self, "conclusiones", tuple(tuple(c) for c in self.conclusiones))
        if not self.condiciones or not self.conclusiones:
            raise ValueError("La regla requiere condiciones y conclusiones")
        if not all(isinstance(c, Condicion) for c in self.condiciones):
            raise ValueError("Condiciones inválidas")
        for conclusion in self.conclusiones:
            if len(conclusion) != 2:
                raise ValueError("Conclusión inválida")
            _clave(("ejemplo", *conclusion))


@dataclass(frozen=True)
class Activacion:
    regla: Regla
    entidad: str
    antecedentes: tuple[Hecho, ...]

    @property
    def clave(self):
        return self.regla.id, self.entidad, tuple(_clave(h) for h in self.antecedentes)


@dataclass(frozen=True)
class Paso:
    regla_id: str
    entidad: str
    antecedentes: tuple[Hecho, ...]
    conclusiones: tuple[Hecho, ...]
    hechos_nuevos: tuple[Hecho, ...]


@dataclass(frozen=True)
class Resultado:
    hechos: tuple[Hecho, ...]
    traza: tuple[Paso, ...]

    def por_que(self, hecho: Hecho) -> tuple[Paso, ...]:
        clave = _clave(hecho)
        return tuple(paso for paso in self.traza
                     if any(_clave(conclusion) == clave for conclusion in paso.conclusiones))


class Motor:
    """Una ejecución nueva reconstruye memoria, disparos y traza desde cero.

    Las condiciones son locales salvo que declaren una entidad explícita.
    Solo se añaden hechos; no hay retractación ni efectos externos.
    """

    def __init__(self, reglas):
        self.reglas = tuple(reglas)
        if len({regla.id for regla in self.reglas}) != len(self.reglas):
            raise ValueError("Identificadores de regla duplicados")

    def aplicables(self, hechos) -> tuple[Activacion, ...]:
        memoria = {}
        for hecho in hechos:
            memoria[_clave(hecho)] = hecho
        activaciones = []
        for regla in sorted(self.reglas, key=lambda r: (-r.prioridad, r.id)):
            entidades = sorted({h[0] for h in memoria.values()})
            for entidad in ((regla.entidad,) if regla.entidad is not None else entidades):
                opciones = [tuple(h for h in memoria.values()
                                  if h[0] == (condicion.entidad or entidad) and condicion.cumple(h))
                            for condicion in regla.condiciones]
                for antecedentes in product(*opciones):
                    activaciones.append(Activacion(regla, entidad, antecedentes))
        return tuple(activaciones)

    def ejecutar(self, hechos, *, max_disparos: int = 10000) -> Resultado:
        if type(max_disparos) is not int or max_disparos < 1:
            raise ValueError("max_disparos debe ser un entero positivo")
        memoria = {}
        for hecho in hechos:
            memoria[_clave(hecho)] = hecho
        disparados = set()
        traza = []
        while True:
            activacion = next((a for a in self.aplicables(memoria.values())
                               if a.clave not in disparados), None)
            if activacion is None:
                return Resultado(tuple(memoria.values()), tuple(traza))
            if len(traza) >= max_disparos:
                raise RuntimeError("Se alcanzó el límite de disparos; ejecución incompleta")
            conclusiones = tuple((activacion.entidad, atributo, valor)
                                 for atributo, valor in activacion.regla.conclusiones)
            nuevos = []
            for conclusion in conclusiones:
                clave = _clave(conclusion)
                if clave not in memoria:
                    memoria[clave] = conclusion
                    nuevos.append(conclusion)
            disparados.add(activacion.clave)
            traza.append(Paso(activacion.regla.id, activacion.entidad,
                              activacion.antecedentes, conclusiones, tuple(nuevos)))
