# HANDOFF DS -> auditores — TM Core v0.7.5.2-R3

Fecha: 2026-10-28
Implementador: DS TM BOSS

## Artefacto congelado

- ZIP: `TM_CORE_v0752_R3_B_AUT.zip`
- Ruta: `C:\Users\profesor\tm\Teoria Modular\TM_ENTREGAS\TM_CORE_v0752_R3_B_AUT.zip`
- SHA-256: `450379BD5F1E22380614E6112E3FB52C2A653EE8358BF7E5238995AF99D3B7DB`
- Tamaño: 1.677.900 bytes
- Entradas ZIP: 69 (67 payload + manifest.json + SHA256SUMS.txt)
- Manifiesto: 67/67 archivos presentes; SHA256SUMS 68 lineas verificadas; rutas internas POSIX; cero checksum errors.
- No modificar este ZIP durante auditoria. Cualquier correccion genera R4 y otro ZIP.

## Versiones y autoridad

- Motor candidato: `0.7.5.2-R3`; SHA-256 `71D9A97AC2C49848D152A790DB0C70D20B30643782BFEE0AC030D19110330B08`.
- Arbol: `TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA_R2.md`; SHA-256 `9C6F30D826CBA6135F53A4CDB780266C29102ADEA5022616F528A1E8CE223F64`.
- v2.12 permanece como arbol aprobado. v2.13 R2 es propuesta pendiente de auditoria y aprobacion de Javier.
- Golden humano v003 y feed maestro van fisicamente incluidos y sin cambios.
- v0.7.5.1/0.7.5.2 R2 y sus ZIP anteriores permanecen intactos.

## Archivos principales

- `python/TM_CORE_PYTHON_v0752_CANONICAL.py`
- `authority/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA_R2.md`
- `authority/DECISION_AUT_B_GRANDE_Y_DOS_VIAS_AUT_JAVIER.md`
- `tests/test_big_b_aut.py`
- `tests/legacy_v075/TM_CORE_PYTHON_v075_TESTS.py` y fixture v0.10 incluida
- `repro/run_all.py`, `run_transition_prefixes.py`, `build_diffs.py`, `build_package.py`
- `out/CORE_RAW_OUTPUT.json`, `GOLDEN_COMPARISON.json`, `TRANSITION_PREFIXES.json`, `RUN_SUMMARY.json`
- diffs de arbol v2.12->v2.13 R2, R1->R2 y motor R2->R3

## Resultados ejecutados

- Pruebas nuevas: 16/16.
- Suite legacy original: 20/20, feed original v0.10 incluido en el ZIP; las aserciones no se modificaron.
- Autoprueba: 8/8.
- Transformaciones: PASS para chunks, serializacion/restauracion, traslacion de precios/timestamps e inversion direccional.
- Busqueda de hardcodes golden en el motor: 0 hits.
- Replay del feed maestro: 20.335 ticks, 88 lecturas, 1.266 eventos, 41 eventos locales.
- Prefijos fisicos de transicion: 12 cortes, procesos nuevos y CSV truncados, 0 fallos.
- R0062/R0064: geometry/module, TT y FT coinciden con referencias legacy congeladas.
- Golden Comparison: 6/9. CORE_RAW_OUTPUT hash `32DAA8B1AA56946B3BDDE6267CBE677AE3D57A8C2C05505A6B89BBA07DE05129`, raw sin cambio tras comparar.

## Divergencia y limites

La primera divergencia queda en 16:23: v003 afirma AUT alcista al superar el inicio de A, pero la regla universal exige superar estrictamente 127% de A + 0,25. El primer cruce real del nivel de inicio es sequence 1876; sequence 1879 es el maximo de B, no el primer cruce. El motor no emite ese AUT porque el tamaño observado de B no llega al limite. No se adapto el golden. Por ello AUT bajista 16:23 y cadena 16:24 tampoco se reproducen.

La matriz completa de 75 cierres + 500 cortes aleatorios no se ejecuto; se ejecutaron 12 prefijos de transicion. Pruebas aprobadas no equivalen a exactitud autonoma completa. No se declara replay ciego, AFS2 ni produccion.

## Orden de auditoria

Reader Validator debe revisar primero la salida bruta y determinar la primera divergencia. MiMo recibe despues exactamente este ZIP congelado y verifica manifiesto, reproduccion, tests, prefijos, generalidad, hardcodes, R0062/R0064 y causalidad. Veredicto de implementador: candidato funcionalmente parcial, pendiente de ambos auditores y Javier.

Comando unico desde la raiz extraida: `python repro/run_all.py`. Termina con estado no-cero por la divergencia golden conocida; tests y prefijos estan reportados por separado.
