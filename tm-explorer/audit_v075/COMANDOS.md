# Comandos de verificacion

## Entorno

```powershell
python --version
python -m pytest --version
```

Referencia usada: Python 3.12.10, pytest 9.1.1.

## Paquete

```powershell
python -m pytest motor\TM_CORE_PYTHON_v075_TESTS.py -q
python motor\TM_CORE_PYTHON_v075_STREAMING.py --selftest
python audit_v075\audit_v075_build.py
python audit_v075\audit_v075_prefix_finalize.py --shards 4
python audit_v075\audit_v075_finalize.py
python -m pytest tests\audit_v075_tests.py -q
```

`audit_v075_build.py` regenera A00-A22 y las salidas `v075a2_*`.
`audit_v075_prefix_finalize.py` usa los `P_shard_*.jsonl` existentes y solo calcula los cortes
pendientes; si se borran, recalcula los 3327 cortes fisicos (puede tardar ~20 minutos en 4 nucleos).
`audit_v075_finalize.py` regenera `R00_Readiness.json` a partir de los artefactos.

## Evidencia ya ejecutada

- `out_v075_audit2/pytest_salida.txt`: 20 tests originales, 20 passed.
- `out_v075_audit2/pytest_auditoria_salida.txt`: 10 tests de auditoria, 10 passed.
- `out_v075_audit2/selftest_salida.txt`: 8 comprobaciones.
- `out_v075_audit2/build_salida.txt`: resumen del build.
- `out_v075_audit2/P02_PrefijosMatriz.csv`: 3327 cortes, 0 fallos.
- `out_v075_audit2/A13_Invariantes.json`: invariantes y hallazgos.
