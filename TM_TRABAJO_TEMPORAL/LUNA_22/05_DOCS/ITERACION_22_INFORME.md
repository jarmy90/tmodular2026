# ITERACION 22 — DELIMITACION FUNCIONAL A/B Y LOCAL-G2 AUTORITATIVA

Estado: **ITER22_STATUS = AB_DELIMITATION_AND_LOCAL_BRANCH_COMPLETE**

Baseline: `TM_ITERATION_21_REVIEW.zip` (extraido y verificado; motor
`D77DCDDE…D75D00C` sin cambios conceptuales en esta iteracion).

No se resuelve `MODULE_ORIGIN_RESOLUTION` de 16:30. No hay reglas por vela.
`A_DELIMITED_AT_CLOSE` no se recupera como norma universal.

---

## 1. Arquitectura observadora frente a autoritativa

En 21 el `CandidateTracker` + `TreeQuestion` convivian con el Reader heredado y
podian limitarse a registrar a posteriori lo que el Reader ya habia decidido.
En 22 existe una unica via de escritura para las preguntas migradas:

```
CandidateTracker -> TreeQuestion.evaluate() -> FunctionalCommit -> ConfirmedState
                 -> adaptacion a campos legacy
```

Campos nuevos en el motor:

- `decision_authority` por pregunta: `LEGACY | TREE_QUESTION | PHYSICAL_FACT | PATTERN_ARBITRATION`.
- `_authorize(question_id, role, tick, fields)` devuelve `True` solo si existe
  `FunctionalCommit` de tipo `CONFIRM` para esa pregunta y ese tick. Sin commit,
  la escritura legacy **no ocurre** (no se escribe y luego se revierte).
- `legacy_preempted` cuenta intentos de escribir estado confirmado sin commit
  previo. Gate: `legacy_preemptions = 0`.

Toda la escritura pasa por `_arch_confirm` / `_arch_apply`, que ademas
rechazan cualquier intento de escribir en una generacion `ARCHIVED`
(`archived_generation_writes = 0`).

## 2. Preguntas migradas

| Pregunta | Autoridad | Commits admit | Commits confirm |
|---|---|---|---|
| `AFTER_MODULE` (nace A) | TREE_QUESTION | 2 | — |
| `A_DEVELOPMENT` | TREE_QUESTION | — | 6 |
| `B_DEVELOPMENT` | TREE_QUESTION | — | (incluido) |
| `B_GRANDE_CONFIRMATION` | TREE_QUESTION | — | — |
| `B_LIMIT` | TREE_QUESTION | — | — |
| `LOCAL_A_DEVELOPMENT` | TREE_QUESTION | — | 1 (seq 2623) |
| `LOCAL_B_DEVELOPMENT` | TREE_QUESTION | — | 1 (seq 2627) |

`consumes` es cerrado: una pregunta solo puede leer las referencias declaradas.
Un acceso a otra rama, otra generacion o una referencia archivada produce
`QUESTION_CONSUMES_VIOLATION` / `CROSS_OWNER_REFERENCE_VIOLATION`
(`consumes_violations = 0`, `cross_owner_reference_reads = 0`).

## 3. FunctionalCommits reales

Run 16:15–16:29 con trazador activo:

- `ADMIT` : 2 (apertura del candidato A y apertura del candidato B; ninguno
  escribe estado confirmado).
- `CONFIRM`: 6 en MAIN, 2 en LOCAL-G2.
- `decision_authority = TREE_QUESTION` en `after_module`, `a_development`,
  `b_development`, `b_grande`, `b_limit`.

## 4. Delimitacion funcional de A

`A_DEVELOPMENT` mantiene A abierta mientras el propietario no cambie:

- el cierre de vela no termina A: A continua entre 16:26 y 16:27 y entre
  16:27 y 16:28 sin ninguna escritura forzada por `bar_close`
  (`bar_close_forced_a_closures = 0`);
- A se congela en su extremo funcional **solo** cuando `B_DEVELOPMENT` emite
  `CONFIRM` para B (`functional_b_commits_a_close = true`,
  `candidate_b_writes_a = 0`: B no escribe A directamente, es el commit de la
  pregunta B el que cierra A);
- `a_closures_at_structural_end = 1` (la unica A cerrada en la ventana lo hace
  en su extremo estructural, no en un cierre de vela).

Una B fisica (2 puntos) o estructural no modifica A: solo la confirmacion
funcional de B delimita A.

## 5. Desarrollo de B

- `B_PHYSICAL` / `B_STRUCTURAL` no escriben estado.
- `B_CANDIDATE_CONFIRMED`: B existe con propietario, origen y medida propios;
  los retrocesos internos no la dividen.
- `B_ratio = B_size / A_size` se calcula **solo** con referencias del mismo
  `branch_id` y `generation_id`. Cualquier intento de medir `LOCAL.B` contra
  `PRIMARY.A` lanza `CROSS_OWNER_REFERENCE_VIOLATION`
  (`cross_owner_ratios = 0`, `main_b_uses_main_a = true`,
  `local_b_uses_local_a = true`).
- `B_GRANDE` si `ratio >= 1.00`; sigue si `ratio <= 1.27` (+0.25 tolerancia);
  `AUT` si lo supera estrictamente. AUT no es C.

## 6. LOCAL-G2 desde cero

LOCAL-G2 se crea con `ConfirmedState`, `CandidateTracker`, `QuestionBook` y
referencias propias; no hereda `one`, modulo, A/B, TT ni `local_mode` de
LOCAL-G1 (`local_g2_inherited_references = 0`). `parent_context_id` es
descriptivo y no concede autoridad sobre referencias MAIN.

Semilla: `CandidateRecord` propio, `owner = LOCAL-G2`, origin/extreme propios,
`structural_time` del extremo fisico y `knowledge_time` del primer commit
funcional (confirmacion retroactiva, sin spoiler: antes de `kt` la rama esta
`LOCAL_CANDIDATE`).

Geometria derivada (16:26–16:27):

| Campo | Valor |
|---|---|
| modulo local | 2987380 -> 2986700, 680, dir +1, `LOCAL_MODULE_BY_DISCARD_A` |
| A local | 2987380 -> 2986260, 1120, dir -1, `A_CONFIRMED` (seq 2623) |
| B local | 2986260 -> 2986700, 440, dir +1, `B_CANDIDATE_CONFIRMED` (seq 2627) |
| B ratio | 0.3929 (100 % = 1120, 127 % = 1447) |
| TT local | no armado en esta ventana |

## 7. Escenas ensayadas

| Escena | Resultado | Motivo |
|---|---|---|
| `SCENE_LOCAL_A` (no existe local) | rechazada | MAIN no explica la autonomia del tramo: el modulo local extiende su propio extremo y responde una pregunta propia |
| `SCENE_LOCAL_B` (nace en 16:26) | **seleccionada** | semilla en 16:26, primera pregunta funcional A en 16:26, conocimiento en la misma ventana |
| `SCENE_LOCAL_C` (solo retroactiva) | compatible, no dominante | la semilla ya tiene evidencia estructural suficiente antes de 16:27; la confirmacion es retroactiva pero el `structural_time` no cambia |

No se selecciona por coincidencia humana. Criterio: cero reglas canonicas
rotas, cero fugas, propietarios correctos, menor fragmentacion.

## 8. Clasificacion de la lectura humana

| Reclamacion | Clasificacion | Evidencia |
|---|---|---|
| B Grande en la lectura local (16:27) | `CORRECTED_BY_TICKS` | medida contra su propia A local: 440 / 1120 = 39.3 % del 100 % exigido; no hay B Grande local en ese tramo |
| Dos TT pendientes con propietarios distintos (16:28) | `PARTIALLY_CONFIRMED` | existen dos estructuras con propietario distinto, pero la local no arma TT en 16:26–16:29 |
| Ambos TT confirman en 16:29 | `CORRECTED_BY_TICKS` | solo el TT mayor alcanza su objetivo (2982280); el TT local nace en 16:27 y su primera frontera es la invalidacion |
| A/B/A-tendencia con B medida contra A propia | `CONFIRMED_BY_TICKS` | geometria local reconstruida con referencias exclusivas |

`human_anchors_passed = 13/19` (sin cambios: esta iteracion no persigue 19/19;
resuelve las reclamaciones del tramo 16:26–16:29 con evidencia tick a tick).

## 9. TT activos

| TT | Propietario | Estado | Objetivo | Primera frontera |
|---|---|---|---|---|
| TT mayor 16:26 (modulo 26.3) | PRIMARY-G1 | `TT_CONFIRMED` en 16:29 | 2982280 | objetivo |
| TT local 16:27 (modulo 2870) | LOCAL-G2 | `TT_FAILED` | 2984360 | `INVALIDATION@2849` (2984710) |

Maximo un TT activo por generacion; dos generaciones activas; historicos
separados. No se fuerza el segundo TT.

## 10. Pruebas

`run_iteration_22_tests.py`: **39 / 39**

Cubre, entre otras: `AFTER_MODULE` autoritativo, Reader legacy no puede
confirmar A antes del commit, A continua entre velas, cierre de vela no termina
A, B fisica no delimita A, B estructural no la modifica, B confirmada congela A,
B con retrocesos internos, 100 % exacto, limite 127 % + 0.25, `AUT` por un tick,
C posterior a B Grande, LOCAL-G2 limpia, cero herencia de LOCAL-G1, cero ratios
cruzados, LOCAL candidata sin spoiler, confirmacion retroactiva, absorcion,
integracion, sombras, MAIN+LOCAL en el mismo tick, TT independientes, traslacion,
inversion, escalado, prefijo, determinismo, `DecisionAuthority`, abortos por
preemption legacy / escritura de candidato / consumes / propietario.

## 11. Regresiones

| Suite | Resultado |
|---|---|
| 169 regresiones canonicas | 169/169 |
| 19B tests | 23/23 |
| 19B anclas de transicion | 12/12 |
| 20A anclas | 10/10 |
| Iteracion 21 | 50/50 |
| Iteracion 22 | 39/39 |
| determinismo / prefijo | true / true |
| fugas entre generaciones | 0 |
| escrituras en generaciones archivadas | 0 |

## 12. Gate

```
legacy_preemptions               = 0
local_g2_inherited_references    = 0
local_b_uses_local_a             = true
main_b_uses_main_a               = true
cross_owner_ratios               = 0
bar_close_forced_a_closures      = 0
a_closures_at_structural_end     = 1
candidate_b_writes_a             = 0
functional_b_commits_a_close     = true
candidate_state_writes           = 0
cross_owner_reference_reads      = 0
consumes_violations              = 0
archived_generation_writes       = 0
active_branches                  = 2
third_branch_attempts            = 0
hardcoded_market_values          = 0
after_module_authority           = TREE_QUESTION
a_development_authority          = TREE_QUESTION
b_development_authority          = TREE_QUESTION
b_grande_authority               = TREE_QUESTION
b_limit_authority                = TREE_QUESTION
```

## 13. Primera divergencia restante

`MODULE_ORIGIN_RESOLUTION` (16:30). Con la arquitectura autoritativa el motor ya
no puede confirmar A/B antes de tiempo, de modo que el bloqueo de 16:30 ya no
es de estado: es de **origen del modulo** (que movimiento fisico abre el modulo
del que nace A). No se ha tocado en esta iteracion por instruccion explicita.

## 14. Preguntas tecnicas abiertas

1. `MODULE_ORIGIN_RESOLUTION`: como seleccionar el origen del modulo cuando dos
   lecturas miden desde extremos contrarios sin introducir una regla por vela.
2. `LOCAL_SEED_POLICY`: la semilla local se ha resuelto con evidencia
   estructural; falta formalizar la condicion exacta de "autonomia respecto de
   MAIN" como contrato de `TreeQuestion` (hoy es `structural_requirement`
   declarado por la pregunta concreta).
3. Politica provisional vigente que sigue en pie: `A_DELIMITED_AT_CLOSE`
   (contextual, no universal) y `PROVISIONAL_PHYSICAL_AUTONOMY_FILTER` (2 puntos
   como filtro de desplazamiento fisico minimo, no como definicion de A/B/C).
