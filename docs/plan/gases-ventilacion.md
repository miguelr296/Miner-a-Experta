# Sprint 2 — Gases y ventilación

[← Índice](../../README.md)

Se añadieron R08–R23: NO₂, CO₂, H₂S, deficiencia y exceso de O₂, y aire con contexto de ANFO. Hay **23 reglas** en el [catálogo](../reglas.md), con sus referencias a pruebas. Superar las 15 reglas no acredita por sí solo todo el Nivel 1.

**Avance posterior:** la [verificación de Nivel 1](nivel1-verificacion.md) añade la mina de 16 nodos y R24/R25 de exposición vecina. Los 23 tipos y 307 resultados de esta guía corresponden a la sesión de gases y ventilación.

## Umbrales y fuentes

[ambiente.json](../../data/configuracion/ambiente.json) contiene los nuevos umbrales, límites y factores; CO conserva sus archivos anteriores. No se escriben umbrales numéricos dentro del motor.

| Variable | Alerta | Riesgo alto | Peligro inmediato |
|---|---|---|---|
| NO₂, ppm | > 3 | > 5 | > 10 |
| CO₂, ppm | > 5000 | > 30000 | > 60000 |
| H₂S, ppm | > 10 | > 15 | > 30 |
| Deficiencia de O₂, % | < 19,5 | < 18 | < 16 |

Cada gas encadena lectura → alerta → riesgo alto → cierre. Alerta y riesgo alto también concluyen factores configurables, inicialmente 2 y 3. Se combinan por máximo, no por producto; el cierre domina siempre. El exceso de O₂ (> 22,5 %) solo genera alerta y factor de penalización: no se inventa un umbral de cierre por exceso.

Los niveles de peligro inmediato, las clasificaciones instantáneas y los factores son **supuestos de simulación**, aunque algunos valores procedan de límites ocupacionales ya citados. Se reutilizan las referencias del catálogo; no se afirma una nueva verificación normativa.

## Aire y ANFO

Se penaliza aire por debajo de 20 m/min, por encima de 250 m/min o por debajo de 25 m/min con ANFO. El factor inicial es 3. No se inventa un umbral de cierre por ventilación para el sistema experto. El filtro de la línea base sí cierra al salir del rango, según su política simple.

Toda lectura de aire_m_min requiere un hecho booleano uso_anfo en el mismo túnel. No se interpreta la ausencia como False. Las dos condiciones de aire bajo pueden coexistir con ANFO; el máximo de factores evita contar dos veces esa penalización.

## Ejecutar

Con el entorno virtual activado, desde la raíz:

```bash
python -m mina_experta --desde n5 --no2 tunel_3_4=11 --comparar
python -m mina_experta --desde n5 --o2 tunel_3_4=15 --comparar
python -m mina_experta --desde n5 --aire tunel_2_3=22 --anfo tunel_2_3 --comparar
python -m mina_experta --desde n5 --aire tunel_2_3=22 --sin-anfo tunel_2_3 --comparar
python -m mina_experta --escenario data/escenarios/ventilacion_anfo.json
python -m pytest -q
```

También existen --co2 y --h2s. Los gases salvo O₂ se expresan en ppm; O₂ en porcentaje; aire en m/min. Los valores deben ser finitos y no negativos; O₂ no puede superar 100 %. Se rechazan lecturas repetidas y declaraciones contradictorias de uso de ANFO.

## Escenarios y comparación

El campo opcional ambiente es una ruta relativa al escenario. Los cuatro ejemplos del repositorio lo indican. Los archivos versión 1 anteriores siguen aceptándose para CO y eventos; los sensores nuevos sin configuración de ambiente generan error, en vez de ignorarse.

El filtro independiente se amplió a los mismos sensores: cierra al exceder los primeros límites de NO₂/CO₂/H₂S, salir del rango de O₂ o incumplir los límites de aire con ANFO. No usa conclusiones del motor.

En el nuevo escenario con aire a 22 m/min y ANFO, Ana tiene un recorrido penalizado de 470 m con costo 670 en el sistema, mientras el filtro directo deja ese origen sin salida. Esto muestra políticas distintas, no superioridad ni seguridad demostradas.

## Validación y pendientes

Las pruebas cubren cada regla, todas las fronteras de gases, límites de O₂, aire con y sin ANFO, datos/configuraciones inválidos y combinación de riesgos. También ejecutan cada gas por consola y el escenario ANFO desde fuera del checkout.

Resultado de la sesión: **307 pruebas aprobadas**, dependencias sin incompatibilidades y correspondencia comprobada de las 23 reglas con el catálogo y sus referencias de pruebas.

Falta ampliar la mina a 15–20 nodos y demostrar un caso donde el encadenamiento detecte riesgo en un túnel vecino que el filtro local no capture. A*, certeza y decisiones de Nivel 2 siguen pendientes.
