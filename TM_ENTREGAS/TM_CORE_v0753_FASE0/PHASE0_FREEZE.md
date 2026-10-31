# FASE 0 - CONGELACION Y LINEA BASE (v0753)

Fecha: 2026-10-29
Autoridad: Javier (TM BOSS), fase autorizada en el mensaje de mision integral.
Ejecutor: TM_READER_VALIDATOR.

## 1. Objeto congelado

| Elemento | Ruta | SHA-256 | Estado |
|---|---|---|---|
| ZIP R3 congelado | `TM_ENTREGAS\TM_CORE_v0752_R3_B_AUT.zip` | `450379bd5f1e22380614e6112e3fb52c2a653ee8358bf7e5238995af99d3b7db` | restaurado, solo lectura |
| Copia inmutable del ZIP | `TM_ENTREGAS\ROLLBACK\TM_CORE_v0752_R3_B_AUT_450379bd.zip` | idem | solo lectura |
| Carpeta R3 extraida | `TM_ENTREGAS\TM_CORE_v0752_R3_B_AUT` | 67/67 ficheros contra `manifest.json`, 0 desviaciones | solo lectura |
| Copia inmutable extraida | `TM_ENTREGAS\ROLLBACK\v0752_R3_450379bd` | 69 ficheros, solo lectura | punto de rollback |
| Motor R3 | `python\TM_CORE_PYTHON_v0752_CANONICAL.py` | `71d9a97ac2c49848d152a790db0c70d20b30643782bfee0ac030d19110330b08` | inmutable |
| Feed maestro | `data\TM_TICKFEED_1615_1730.csv` | `5f701be2307352cb559abbd7bb856a6fd2a1f91e5d269a93dcc9ae2992e2c9ff` | inmutable |
| Salida R3 | `out\CORE_RAW_OUTPUT.json` | `32daa8b1aa56946b3bdde6267cbe677ae3d57a8c2c05505a6b89bba07de05129` | inmutable |

## 2. Version de trabajo

`TM_ENTREGAS\TM_CORE_v0753_FASE0` - copia de R3 (69 ficheros, sin caches).
Verificacion: 67/67 ficheros de payload coinciden con `manifest.json` (0 desviaciones).
No se toca ningun archivo canonico. R3 no se sobrescribe en ninguna fase.

## 3. Incidente INFRA-001 (resuelto)

`repro/run_all.py` termina llamando a `repro/build_package.py`, que resuelve el nombre
del paquete desde `manifest.json` y escribe el ZIP en el directorio padre. Al ejecutarse
desde la copia, reconstruyo `TM_ENTREGAS\TM_CORE_v0752_R3_B_AUT.zip` con otra marca de
tiempo y otro SHA (`53606da1...`).

Impacto: solo el contenedor ZIP. La carpeta extraida y los 67 ficheros de payload
nunca se modificaron (verificado contra el manifest).

Restauracion: se localizaron tres copias independientes con el SHA original
(`Shared\Transfers\209722d3...`, `Shared\Transfers\d46a119a...` y
`agent-ece275c8\deliverables_R3`), se restauro el ZIP y se verifico
`450379bd5f1e...`. El ZIP queda en solo lectura.

Prevencion: nuevo `repro/run_all_safe.py` con guarda de congelacion que aborta si el
SHA del ZIP cambia antes o despues de la ejecucion. A partir de ahora los gates se
ejecutan con este lanzador. `run_all.py` no se vuelve a usar desde copias.

## 4. Linea base reproducible

Ejecutada en `TM_CORE_v0753_FASE0` el 2026-10-29. Tiempo total 111,6 s.

| Gate | Comando | Resultado |
|---|---|---|
| Autoprueba | `python python/TM_CORE_PYTHON_v0752_CANONICAL.py --selftest` | OK, 8 comprobaciones |
| B/AUT universal | `python tests/test_big_b_aut.py` | 16/16 OK (3,3 s) |
| Legacy 20 | `pytest -q tests/legacy_v075/TM_CORE_PYTHON_v075_TESTS.py` | 20/20 (95,1 s) |
| Transformaciones | `python tests/test_transformations.py` | PASS, hardcodes `[]`, feed_points 2297 |
| Motor sobre feed | `--feed data/TM_TICKFEED_1615_1730.csv --out out` | readings 88, events 1266, movements 439, cobertura geometrica y funcional True |
| Prefijos fisicos | `python repro/run_transition_prefixes.py` | 12 cortes, `prefix_failures = 0` |
| Comparacion golden | `python repro/compare_golden.py` | 6/9, `LECTURA_NO_REPRODUCIDA`, primera fallo 16:23 AUT alcista |
| Salida bruta | `out/CORE_RAW_OUTPUT.json` | SHA `32daa8b1...` identico a R3 |
| T3 canonica | `pytest t3_validation/test_t3_canonical.py` | 3 pass / 9 fail |
| Replay 16:21 | `python t3_validation/replay_1621.py` | canonico seq 1446 (29832,3); motor seq 1590 (29830,5) |

Determinismo: la salida bruta de la copia coincide bit a bit con la de R3
(`32daa8b1...`). La linea base es reproducible.

Causa preexistente aceptada: `comparison_exit = 2` por la divergencia 16:23 v003 vs
regla 127 % + 0,25. No es regresion.

## 5. Autoridades y rutas de decision (auditoria de componentes)

| Componente | Linea | Clasificacion | Autoridad |
|---|---|---|---|
| `_process_local_sequence` | 2508-2610 | OFFICIAL + MIGRATE | unica emisora de 2 y 3 |
| `WAIT_THREE` | 2565-2574 | OFFICIAL, CONTRADICTORY con el canon | decide 3 con `STRUCTURAL_MOVE` |
| `WAIT_A_BAR` / `MODULO_EXT` | 2575-2603 | OFFICIAL, DUPLICATED | recalcula extremo del modulo aparte de la pata |
| Transicion al cierre de vela | 2780-2790 | OFFICIAL, MIGRATE | fija el final de 2 y abre `WAIT_THREE` |
| `_local_123` | 498-537 | DEAD + DUPLICATED + non-causal | sin autoridad; 1 aparicion |
| `local_two_gate` | 478-480 | PURE_HELPER, OFFICIAL | compuerta de 2; `abs(gap) < 25` correcto |
| `BigBTracker` | 423-471 | OFFICIAL, MIGRATE | B / AUT / C |
| `_check_tt` / `_maybe_aut` | 808-889 | OFFICIAL, MIGRATE | TT y AUT |
| `t3_validation/` | - | SHADOW de validacion | no emite salida oficial |

Nota de correccion sobre mi informe anterior: `local_two_gate` usa `< 0,25`, que
coincide con la aclaracion de Javier (`0,25` exactos **no** es plano). El canon
antiguo `|delta| <= 0,25` queda SUPERSEDED. No hay bug de frontera.

## 6. Fuentes canonicas localizadas

- `TM_CANON_ACTIVO\01_ARBOL\TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_12.md` (N-001, N-005..N-011, §3.2, TM-3-001/002/003, Q-005/Q-006).
- `TM_CANON_ACTIVO\06_REGLAS_CONTROL\REGLAS_CERRADAS.md` (A1, A2) y `PREGUNTAS_PENDIENTES.md`.
- Dossier TM v3 §4.3, Dossier TM v4 §4.3, Prompt v2 §10.2.
- `TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v003.txt` (golden humano).
- `TM_ENTREGAS\AUDITORIA_FUNCIONAL_DEFINICION_3_v0752_R3.md` y
  `INFORME_VALIDACION_FUNCION_3_v0752_R3.md` (diagnostico aceptado).
- `TM_CORE_v0752_R3_B_AUT\authority\...PROPUESTA_R2.md` (propuesta, no canon).

## 7. Rollback

1. Restaurar el ZIP congelado desde `ROLLBACK\TM_CORE_v0752_R3_B_AUT_450379bd.zip`.
2. Sustituir `TM_CORE_v0752_R3_B_AUT` por `ROLLBACK\v0752_R3_450379bd`.
3. Verificar `450379bd...` y los 67 hashes del manifest.
4. La version de trabajo puede descartarse sin afectar a R3.

## 8. Reglas abiertas vigentes

| ID | Estado | Efecto |
|---|---|---|
| Q-005 | OPEN | minimo de retroceso funcional y forma exacta del intervalo |
| TM-3-004 | OPEN | fin de 3 |
| Q-006 | CLOSED por Javier en esta mision | superacion estricta |
| Yardstick 50 % | CLOSED por Javier | `abs(extremo_2 - origen_2)` |
| Intravela | CLOSED por Javier | solo con secuencia completa demostrable |
| Plano 0,25 | CLOSED por Javier | `< 0,25`; 0,25 exactos no es plano |

## 9. Siguiente fase

Fase 1: infraestructura de preguntas sin cambio semantico.
Nuevo modulo `python/tm_question_state.py` (enums, dataclasses, invariantes, traza
`question`) e instrumentacion del motor con salida identica salvo el bloque nuevo.
Gate de fase: `run_all_safe.py` con `core_raw_sha256` sin cambios y 3/12 en T3.
