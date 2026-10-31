# TM Core 0.7.5.2-R3: B Grande universal y dos vias AUT

Estado: candidato pendiente de auditoria Reader Validator y MiMo. No es version aprobada por Javier; v2.12 sigue como arbol aprobado. La propuesta v2.13 R2 se entrega separada.

## Reproducir desde la raiz del paquete

Requisitos: Python 3.12 y `pip install -r requirements.txt`.

Comando unico:

```powershell
python repro/run_all.py
```

`run_all.py` ejecuta la autoprueba, 16 pruebas nuevas, los 20 tests legacy con su feed incluido, transformaciones, replay completo del feed maestro, prefijos fisicos en procesos nuevos, comparacion posterior contra v003, y genera resumenes en `out/`. El codigo de salida esperado es 2 mientras exista una divergencia humana documentada; un codigo 2 no equivale a todos los tests aprobados.

## Pruebas individuales

```powershell
python -m pytest -q tests/legacy_v075/TM_CORE_PYTHON_v075_TESTS.py
python tests/test_big_b_aut.py
python tests/test_transformations.py
python repro/run_transition_prefixes.py
python python/TM_CORE_PYTHON_v075_CANONICAL.py --selftest
```

## Artefactos

- `python/TM_CORE_PYTHON_v0752_CANONICAL.py`: motor R3. No lee golden ni informes.
- `authority/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA_R2.md`: propuesta, no sustituye v2.12.
- `data/TM_TICKFEED_1615_1730.csv`: feed maestro.
- `data/TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v003.txt`: golden humano, inalterado.
- `data/TM_TICKFEED_v010_LEGACY.csv`: fixture congelada para la suite legacy.
- `out/CORE_RAW_OUTPUT.json`: salida original del motor.
- `out/GOLDEN_COMPARISON.json`: comparacion de solo lectura; no escribe en raw ni modifica motor/golden.
- `out/TRANSITION_PREFIXES.json`: cortes fisicos alrededor de transiciones, proceso nuevo en cada corte.

## Divergencia conocida

v003 afirma AUT alcista en 16:23 al superar el inicio de A. La regla universal ahora requiere que B supere estrictamente 127% de A + 0,25. El primer cruce real del nivel de inicio ocurre antes del maximo, pero no alcanza el umbral AUT. Golden Comparison conserva ese conflicto como `LECTURA_NO_REPRODUCIDA`; el golden no se adapta.

R0062/R0064 se comparan contra la referencia legacy incluida. La implementacion no declara autonomia perfecta, replay ciego, AFS2 ni produccion.
