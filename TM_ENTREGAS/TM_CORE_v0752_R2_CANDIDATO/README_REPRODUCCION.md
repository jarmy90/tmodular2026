# TM Core v0.7.5.2 R2 — candidato no conforme

Requiere Python 3.12; usa solo la biblioteca estándar. El motor procesa el feed secuencial. `GOLDEN_COMPARISON.json` se genera después y solo lee `CORE_RAW_OUTPUT.json`.

## Reproducción

Desde la raíz extraída:

```powershell
python repro/run_all.py
```

El comando termina con código 2 porque el motor devuelve `LECTURA_NO_REPRODUCIDA`. Ese resultado es intencional y está documentado, no es un pase de aceptación.

Para repetir por separado:

```powershell
python python/TM_CORE_PYTHON_v0752_CANONICAL.py --selftest
python tests/test_transformations.py
python -m pytest -q tests/legacy_v075/TM_CORE_PYTHON_v075_TESTS.py
```

La matriz física extensa está disponible con `python repro/run_prefix_matrix.py`; no se ejecutó en esta entrega y no debe interpretarse como aprobada.

## Resultado de esta iteración

- Legacy: 20/20.
- Autoprueba: 8/8.
- Transformaciones y búsqueda de hardcodes: PASS, 0 hits en el motor.
- Golden Comparison: 6/9. El primer desacuerdo está en 16:23: el golden declara AUT alcista al superar el inicio de A, mientras la decisión experta vigente exige que B supere 127% de A + 0,25. El motor no emite ese AUT y no altera el golden.
- R0062/R0064 aparecen, pero no reproducen exactamente la geometría y referencias TT/FT legacy.
- Concurrencia total máxima medida: 4; requisito global máximo 3 incumplido.
- Prefijos completos: pendientes.

La tabla completa del primer desacuerdo está en `out/GOLDEN_COMPARISON.json`; detalle y estado de las lecturas en `out/R0062_R0064.json` y `HANDOFF_DS_TO_AUDITORS.md`.

No usar para replay ciego, AFS2 ni producción.
