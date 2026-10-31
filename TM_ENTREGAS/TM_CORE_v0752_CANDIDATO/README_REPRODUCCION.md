# TM Core v0.7.5.2 — candidato pendiente de auditoría

Este paquete es autocontenido y se ejecuta con Python 3.12 (solo biblioteca estándar). El motor lee únicamente `data/TM_TICKFEED_1615_1730.csv`. La comparación golden se ejecuta después y lee `out/CORE_RAW_OUTPUT.json`; no importa el motor ni modifica la salida bruta.

La regla documental de referencia está adjunta en `authority/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA_R1.md`. Su ZIP de origen conserva SHA-256 `C79E6D49D039A8F78A436013DF71673B9150EE342CF68D303849B65C32D79C90`; el árbol sigue como candidato sin aprobación final.

## Reproducción completa

Desde la raíz extraída del ZIP:

```powershell
python repro/run_all.py
```

El comando ejecuta el núcleo sobre el feed completo, escribe `out/CORE_RAW_OUTPUT.json`, genera `out/GOLDEN_COMPARISON.json` y `out/RUN_SUMMARY.json`. El proceso termina con código 2 cuando la comparación detecta `LECTURA_NO_REPRODUCIDA`; ese es el resultado esperado de esta entrega candidata.

Pruebas de transformación:

```powershell
python tests/test_transformations.py
```

Autoprueba del núcleo:

```powershell
python python/TM_CORE_PYTHON_v0752_CANONICAL.py --selftest
```

## Estado de esta ejecución

- El núcleo procesó 20.335 ticks y escribió la salida bruta antes de comparar.
- La comparación básica de funciones previstas en 16:19–16:24 es 8/9: falla el hito causal del AUT alcista de 16:23. El primer evento emitido es sequence_id 1876; v003 identifica 1879.
- El flujo local contiene emisiones repetidas después de esos hitos; no se considera una reproducción completa.
- R0062/R0064 no aparecen en la salida del candidato con sus IDs esperados.
- La autoprueba pasa 8/8; transformación de precios/tiempos, inversión de dirección y serialización por chunks pasan en la prueba independiente.
- La matriz completa de 75 cierres más 500 prefijos aleatorios no se declara aprobada. Está pendiente de la corrección del primer desacuerdo y de auditoría.

No usar esta versión para replay ciego, AFS2 ni producción. El estado final solicitado es `MOTOR_v0752_CANDIDATO_PENDIENTE_READER_VALIDATOR_Y_MIMO`.
