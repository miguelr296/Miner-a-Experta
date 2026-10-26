# S1-02 — Clases y módulos

[← Índice](../../README.md)

Continuamos tras las soluciones de S1-01. S1-04 tiene una rama publicada, pero su PR y revisión siguen pendientes por el bloqueo de la API de GitHub. Esa revisión no es una dependencia técnica de este ejercicio.

## Objetivo y ejecución

Crear una clase propia en un módulo e importarla y utilizarla desde otro. Este ejemplo es material de aprendizaje: no define el esquema JSON, no modela los túneles ni calcula rutas.

Desde la raíz del repositorio y con el entorno virtual activado:

```bash
python -m ejercicios.clases
python -m pytest -q
```

La demostración muestra a Ana y Luis en `n1`; después cambia solo a Ana a `n3`. Luis debe permanecer en `n1`. La suite completa incluye tanto S1-01 como S1-02.

## Qué observar en el código

- En [modelo_aprendizaje.py](../../ejercicios/modelo_aprendizaje.py), `Minero` es una clase con `__init__` explícito. Al escribir `Minero("Ana", frente)`, Python inicializa los atributos de esa instancia mediante `self`.
- `self` cumple un papel parecido a `this` en Java/C#, pero se declara como primer parámetro del método. Al llamar `ana.describir()`, no se pasa `self` manualmente.
- `PuntoControl` usa `@dataclass`: Python genera, entre otros métodos, la inicialización y la comparación por campos. `frozen=True` evita reasignar esos campos. Por eso podemos compartir un punto entre dos mineros y cambiar la ubicación de uno sin alterar el punto del otro.
- Las anotaciones `str` y `PuntoControl` describen los tipos esperados; no validan automáticamente los argumentos durante la ejecución.
- En [clases.py](../../ejercicios/clases.py), el `import` obtiene las clases de otro módulo. Un módulo es un archivo Python; `ejercicios/` es un paquete, con su archivo `__init__.py`.
- El bloque `if __name__ == "__main__":` ejecuta la demostración cuando se invoca como programa. Importar el módulo no debe iniciar la demostración.
- Usa `python -m ejercicios.clases` desde la raíz para que Python encuentre el paquete. No ejecutes directamente el archivo `ejercicios/clases.py`.

## Comprobaciones

Las pruebas verifican la inicialización, la descripción, la independencia de dos mineros que comparten un punto, la comparación de datos y la protección del punto frente a cambios. También ejecutan la demostración en un proceso separado y comparan su salida completa.

Queda pendiente que el integrante explique estas diferencias y pruebe a crear otro minero. No damos por acreditado el aprendizaje solo por tener pruebas aprobadas. Después corresponde S1-05, lectura y escritura de JSON, requisito para diseñar los datos de la mina.
