# R5_VARIANT_COMPARISON — R5 auditado vs R5 empaquetado

**Documento:** `R5_VARIANT_COMPARISON.md`
**Fecha:** 2026-10-30
**Fuente primaria:** árbol `94A1408A…` (WORKING_CANON_NOT_FROZEN)
**Motor analizado:** R5 `9BD1BEDB…` (auditado) y R5 `19A847C0…` (empaquetado)
**Versión documental:** 1.0 · **Versión del motor:** `0.7.5.2-R5` (ambas variantes)
**tree_modified = false · engine_modified = false · goldens_modified = false · observational_only = true**

---

## 1. Rutas

| Variante | Ruta absoluta | Origen |
|---|---|---|
| **A — R5 auditado** | `C:\Users\profesor\OpenBot\Agents\agent-ece275c8-821a-43f3-b05f-6cdf123b7ade\deliverables_R5\python\TM_CORE_PYTHON_v0752_CANONICAL_R5.py` | Motor vivo del paquete de trabajo y de la auditoría CE |
| **B — R5 empaquetado** | `TM_CORE_v0752_R5_LECTURA_1615_1629.zip → python/TM_CORE_PYTHON_v0752_CANONICAL_R5.py` | ZIP de entrega; idéntico en `TM_CORE_v0752_R5_POST_CUT.zip` |
| Copia de trabajo A | `TM_TRABAJO_TEMPORAL/FREEBUFF_AUDIT_V219/00_INPUTS_REFERENCE/variants/R5_AUDITED_9BD1BEDB.py` | Copia byte a byte, sin modificar |
| Copia de trabajo B | `TM_TRABAJO_TEMPORAL/FREEBUFF_AUDIT_V219/00_INPUTS_REFERENCE/variants/R5_PACKAGED_19A847C0.py` | Extraída del ZIP, sin modificar |
| Diff completo | `TM_TRABAJO_TEMPORAL/FREEBUFF_AUDIT_V219/01_INTEGRITY/R5_variant_unified_diff.txt` | 422 líneas de diff unificado |

## 2. Tamaños

| Métrica | A — auditado | B — empaquetado | Δ |
|---|---:|---:|---:|
| Bytes | 158.090 | 144.357 | +13.733 |
| Líneas físicas | 3.580 | 3.368 | +212 |
| Clases + funciones (AST) | 105 | 101 | +4 |
| Constantes estructurales | idénticas | idénticas | 0 |

## 3. Hashes

| Variante | SHA-256 |
|---|---|
| **A — auditado** | `9BD1BEDB5DEC8C5A1C3A831338503E90CC04EE3CD776CF4E01D27CF8AA0EBEAE` |
| **B — empaquetado** | `19A847C078E124616495E85A832F9D2FA12A371413046CBAEB7E9644D47C6A36` |
| ZIP `TM_CORE_v0752_R5_LECTURA_1615_1629.zip` | `DDC6AE2FFA9854FD6DE1B9B058BB12DF19E8542F309BD9C8693B823A60785A9F` (1.910.921 B) |
| ZIP `TM_CORE_v0752_R5_POST_CUT.zip` | `4238D0E1FD6ECC9E136856ED49E03958C3151F628318444077ECA7440494A72C` (1.909.791 B) |

`manifest.json` del paquete declara `version: 0.7.5.2-R5.1`; **ambos** archivos declaran `VERSION = "0.7.5.2-R5"`. El `SHA256SUMS.txt` del paquete registra B, no A.

## 4. Fecha de modificación

| Archivo | mtime (local) |
|---|---|
| A — auditado | 2026-10-30 09:16:14 |
| B — empaquetado (dentro del ZIP) | 2026-10-29 11:40:52 |
| Informes CE | 2026-10-30 10:08–10:26 |

A es posterior a B. La auditoría CE se ejecutó el 2026-10-30 contra A.

## 5. Diferencias estructurales

`difflib` sobre líneas: **223 líneas insertadas en A, 11 líneas eliminadas de B, 32 bloques cambiados**. No es un reformateo: los bloques cambiados se concentran en la máquina local y en el nuevo bloque PRIMARY.

| Bloque | A | B |
|---|---|---|
| Autoridad de pregunta por tick | `_advance_primary_question` (nueva) | no existe |
| Decisión PRIMARY B/AUT/C por tick | `_legacy_tick_decision` (nueva) | `_track_primary_b_aut` (solo B/AUT) |
| Registro de pregunta | `_q` (nueva) | no existe |
| Comparación local vs legacy | `_shadow_compare` (nueva) | no existe |
| 2 imposible → módulo por descarte | `_two_impossible` (nueva) | solo `_local_gate_event` |
| Cola/ruptura en `WAIT_THREE` | usa `_two_impossible` | emite gate sin cambio de fase |

## 6. Símbolos añadidos o eliminados

**Solo en A (5):**

- `_advance_primary_question`
- `_legacy_tick_decision`
- `_q`
- `_shadow_compare`
- `_two_impossible`

**Solo en B (1):**

- `_track_primary_b_aut`

## 7. Diferencias semánticas

1. **B tenía una sola máquina operativa.** `_track_primary_b_aut` avanzaba B y AUT en la lectura primaria, pero no evaluaba C, no emitía preguntas y no tenía rama de descarte. La escalera `2/3` vivía únicamente en `_process_local_sequence`.
2. **A añade una segunda autoridad tick a tick.** `_advance_primary_question` decide, para cada lectura, si la máquina es `PRIMARY` o `LOCAL`; para `PRIMARY` ejecuta `_legacy_tick_decision`; para `LOCAL` ejecuta una copia en sombra y registra divergencias. En A conviven, por tanto, **tres** caminos de decisión: `_update` (por movimiento), `_process_local_sequence` (por fase local) y `_legacy_tick_decision` (por tick primario).
3. **A formaliza el módulo por descarte** cuando `2` es imposible (`_two_impossible`: fase `AFTER_3`, `module_kind=POR_DESCARTE`). B solo dejaba un evento de gate.
4. **A introduce el registro `QUESTION`** con `current_function`, `expected_function`, `active_question`, `candidate_status`, condiciones y `transition_reason`. Es la única salida que permite auditar "qué pregunta estaba activa". B no la tiene.
5. **Ambas conservan el mismo arranque.** Las dos usan `MovementBuilder(min_move=600, retrace=25 %)`, el mismo `_close_candidate_bar` (vela cerrada con `span>=6,00`) y los mismos umbrales `MOVE=600` para A, B y C. **La diferencia A/B no toca RC-1 ni RC-2**: añade superficie de decisión encima del mismo bootstrap roto.
6. **Riesgo específico de A:** al ejecutar `_legacy_tick_decision` sobre lecturas PRIMARY y `_process_local_sequence` sobre las LOCAL en el mismo tick, el mismo precio puede producir dos genealogías. La salvaguarda `_shadow_compare` solo compara y registra; no arbitra.

## 8. Tests asociados

La suite del paquete importa `python/TM_CORE_PYTHON_v0752_CANONICAL_R5.py`, es decir, **A**. Resultado reproducido: **28 passed** en 6,17 s (`pytest tests -q`). Los tests cubren:

- `BigBTracker`: 100 %, 127 % + 0,25, AUT estricto, `begin_c`, persistencia.
- `local_two_gate`: gap 0,24/0,25, cola 25/26.
- Anclas de A congeladas y violación de invariante.
- Post-CUT: genealogía, límite de 3 lecturas, fase `AFTER_3`.
- Transformaciones: chunk/checkpoint, traslación de precio/tiempo, inversión de dirección, ausencia de hardcodes de golden.

**Ningún test construye la escalera `1→2→3→A→B→C` desde ticks.** La suite está en verde y el concepto sigue ausente: verde no equivale a cobertura funcional.

## 9. Informes producidos por cada variante

| Informe | Motor citado | Variante |
|---|---|---|
| `INPUTS_MANIFEST.json` | `9BD1BEDB…` | A |
| `CE_TESTS_v219.md` | árbol + expectativas | — |
| `CE_OBSERVATION_RESULTS_v219.md` | `9BD1BEDB…` | A |
| `CONCEPTUAL_MOVEMENT_ERRORS_v219.md` | `9BD1BEDB…` | A |
| `RC_BOOTSTRAP_ONE_DESIGN_v219.md` | `9BD1BEDB…` | A |
| `manifest.json`, `SHA256SUMS.txt`, ZIP | `19A847C0…` | B |

No existe informe CE producido con B. Por tanto, **los hallazgos CE no son reproducibles desde el paquete entregado**.

## 10. Recomendación de línea base

**Línea base provisional: A (`9BD1BEDB…`)**, porque:

1. es el motor que citan los informes CE y `INPUTS_MANIFEST.json`;
2. es el que la suite de tests importa y con el que se obtiene 28/28;
3. es el único con registro `QUESTION` y `_two_impossible`, sin los cuales no puede auditarse la pregunta activa ni el módulo por descarte.

Condiciones:

- **No declarar A motor oficial ni congelado.** Su propio paquete lo contradice.
- **No sustituir B por A** ni reempaquetar en esta fase.
- **No usar B para reproducir CE**: daría resultados distintos y no comparables.
- Antes de cualquier implementación, el propietario debe decidir qué hash es autoritativo y reconstruir el paquete desde ese único hash. Esa decisión no corresponde a esta auditoría.

**Consecuencia operativa:** toda corrección futura debe aplicarse sobre A y verificarse contra los 21 CE, pero el entregable oficial seguirá siendo ambiguo hasta que se resuelva la discrepancia A/B.
