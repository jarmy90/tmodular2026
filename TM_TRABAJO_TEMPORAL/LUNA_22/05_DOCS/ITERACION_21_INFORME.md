# ITERACIÓN 21 — MOTOR DE CANDIDATOS, PREGUNTAS TM Y ESTADO CONFIRMADO

**Estado:** `ITER21_STATUS = CANDIDATE_CONFIRMATION_ARCHITECTURE_COMPLETE`
**Motor:** `tm_reference_interpreter_v1_direct_aut` (+ `tm_candidates`, `tm_market_layer`)
**Tramo procesado:** 16:15–16:32 (causal, sin información futura)
**Tramo abierto declarado:** 16:27–16:32, con primera divergencia localizada y clasificada

---

## 1. Arquitectura implementada

```
TICK FÍSICO
→ OBSERVACIÓN            (TickLedger, MarketFacts)
→ CANDIDATO FÍSICO       (CandidateTracker: OBSERVED / PHYSICAL)
→ EVIDENCIA ESTRUCTURAL  (retención de su propio extremo)
→ PREGUNTA DEL ÁRBOL     (QuestionBook + consumes cerrado)
→ CONFIRMACIÓN FUNCIONAL (FunctionalCommit)
→ COMMIT ATÓMICO         (ConfirmedState, versionado)
```

Cuatro capas, dos de ellas compartidas y dos por rama:

| Capa | Objeto | Ámbito | Escribe estado funcional |
|---|---|---|---|
| 1 | `TickRecord` / `TickLedger` | compartida | no (inmutable) |
| 2 | `MarketFacts` | compartida | no |
| 3 | `CandidateTracker` + `QuestionBook` + `ConfirmedState` | por rama | solo vía commit |
| 4 | `BranchArbiter` | compartida | no (autoridad) |
| traza | `DecisionTracer` | compartida | no |

**Invariante constitucional verificado:** un candidato nunca modifica el estado
funcional confirmado. Los commits `ADMIT` solo escriben marcadores pendientes
(`CANDIDATE`, `CONTRARY_MOVE_PENDING`); los marcadores funcionales
(`A_CONFIRMED`, `B_GRANDE`, `C_GRANDE`, `TT_CONFIRMED`, …) solo aparecen en
commits `CONFIRM`. Métrica `admit_writes_function_state = 0`.

### Regla del umbral de 2 puntos

- `< 200` unidades (2,00 puntos) → `OBSERVED`, auditoría, nunca árbol.
- `>= 200` → `CandidateRecord` con `status = PHYSICAL`.
- `admit()` por debajo del mínimo aborta con `ADMIT_BELOW_PHYSICAL_MINIMUM`.
- Un `PHYSICAL` **no** crea A, B, C, módulo, FT, TT ni rama.

El umbral solo distingue ruido de desplazamiento mínimo: no demuestra función.

---

## 2. CandidateRecord, TreeQuestion, sombras

`CandidateRecord` separa: `owner_branch_id`, `owner_generation_id`,
`source_function_id`, `role_hypothesis`, `direction`, `origin`, `extreme`,
`status`, `evidence_flags`, `structural_time`, `knowledge_time`,
`absorption_level`, `absorbing_id`, `shadow_id`, `close_reason`,
`created_at_seq`, `closed_at_seq`.

Estados: `OBSERVED → PHYSICAL → STRUCTURAL → CONFIRMED`, con finales
`ABSORBED`, `DISCARDED`, `RECLASSIFIED`. No existe `FUNCTIONAL` como estado
permanente: la evidencia funcional es el evento que produce el commit.

`TreeQuestion` declara `question_id`, `current_node`, `roles_allowed`,
`anchor_reference_id`, `consumes` (lista cerrada), `physical_requirement`,
`structural_requirement`, condiciones de confirmación/rechazo/absorción,
`next_node_if_yes/no`, `priority` y `authority`.

Violaciones que **abortan** la ejecución en lugar de degradar en silencio:

- `CANDIDATE_STATE_WRITE_VIOLATION` — escritura directa al estado.
- `QUESTION_CONSUMES_VIOLATION` / `REFERENCE_NOT_CONSUMED` — referencia no declarada.
- `CROSS_OWNER_REFERENCE_VIOLATION` / `CROSS_GENERATION_COMMIT` — otra rama u otra generación.
- `SAME_BIRTH_AND_CONFIRMATION_EVIDENCE` — confirmar con la evidencia que creó el candidato.
- `CONFIRM_WITHOUT_RETENTION` — confirmar sin retención estructural.
- `COMMIT_ON_CLOSED_QUESTION` / `COMMIT_ON_CLOSED_CANDIDATE`.
- `ADMIT_BELOW_PHYSICAL_MINIMUM`.

`CandidateShadow` impide recrear un candidato absorbido sin evidencia nueva:
bloquea mientras `(extremo_nuevo − extremo_sombra) · dirección <= 0` y libera la
sombra cuando el propietario supera el extremo. El bloqueo se cuenta
(`shadow_recreations_blocked`) y el intento queda como `DISCARDED` con
`close_reason = SHADOW_BLOCKED`.

---

## 3. Preguntas migradas

`AFTER_ONE_OPENING`, `TWO_DEVELOPMENT`, `AFTER_MODULE`,
`IMPLICIT_MODULE_ORIGIN`, `B_DEVELOPMENT`, `TT_ARBITRATION`.

`IMPLICIT_MODULE_ORIGIN` conserva la alternativa rechazada
(`MODULE_ORIGIN_AT_PROHIBITED_EXCURSION`) en `rejected_hypotheses`: el origen
elegido y el descartado quedan auditables, no silenciados.

---

## 4. Trazador y clasificación de divergencias

Una fila por tick (4 400 en el tramo) con: `sequence_id`, `timestamp`, `price`,
`branch_id`, `generation_id`, `confirmed_node_before/after`, candidatos antes y
después, `current_question`, `references_used`, evidencia física / estructural /
funcional, `decision`, `events`, `structural_time`, `knowledge_time`,
`explanation`.

Clasificador (`DecisionTracer.classify`) con nueve categorías y banco de pruebas
propio (9/9): `QUESTION_ERROR`, `REFERENCE_ERROR`, `OWNER_ERROR`,
`EARLY_CONFIRMATION`, `LATE_CONFIRMATION`, `NOISE_FRAGMENTATION`,
`WRONG_ABSORPTION`, `LOST_STATE`, `MISSING_RULE` (+ `NO_DIVERGENCE` cuando el
estado llega en el tick esperado).

---

## 5. Gate

| Métrica | Valor |
|---|---|
| regresiones 169 | **169/169** |
| pruebas 19B | **23/23** |
| anclas de transición 19B | **12/12** |
| anclas 20A/20B | **10/10** |
| pruebas de iteración 21 | **50/50** |
| anclas humanas | **13/19** (6 abiertas, con divergencia clasificada) |
| `candidate_state_writes` | 0 |
| `cross_owner_reference_reads` | 0 |
| `consumes_violations` | 0 |
| `unowned_candidates` | 0 |
| `unowned_functions` | 0 |
| `recreated_absorbed_candidates` | 0 |
| `same_birth_and_confirmation_evidence` | 0 |
| `admit_writes_function_state` | 0 |
| `third_branch_attempts` | 0 |
| `archived_generation_writes` | 0 |
| `active_branches` | 1 (MAIN activa, LOCAL archivada) |
| `active_slots` | 1 |
| `hardcoded_market_values` | 0 |
| `movement_without_function_changes_node` | false |
| `determinism` | true |
| `prefix_consistency` | true |

`LOCAL-G1` permanece `ARCHIVED` (seq 2553), slot local libre, patrones TT/FT
históricos conservados con propietario.

---

## 6. Primera divergencia (16:27)

| Campo | Lectura humana | Motor |
|---|---|---|
| `b_grande_status` | `B_GRANDE` (lectura local) | `CANDIDATE` / 170 |
| A usada para medir B | A local propia | A principal 2630 |
| 100 % exigido | el de la A local | 2630 |

**Clasificación: `OWNER_ERROR`.**
La B del tramo local se está midiendo contra la A de `PRIMARY-G1`. La lectura
humana exige una A local propia; no es un fallo del umbral del 100 % ni del
límite `127 % + 0,25`, sino de propiedad de la referencia.

Pregunta técnica abierta: **`AB_DELIMITATION_IN_NOISY_BAR`**. Un `Reader` limpio
iniciado en 16:26 (rama aislada, sin herencia) muestra el mecanismo: el módulo se
extiende (`MODULE_EXTENDED_AFTER_ABSORPTION` repetido de 25,00 a 33,80) mientras
la excursión contraria se absorbe una y otra vez, y la A solo se confirma en
7,50 desde 29840,0. Eso es fragmentación de ruido, no una regla ausente
demostrada.

## 7. Segunda divergencia (16:30) — `MODULE_ORIGIN_RESOLUTION`

| Medida | Humano | Motor |
|---|---|---|
| origen del módulo | extremo prohibido 29838,2 | apertura 29820,6 |
| tamaño | 53,6 (29838,2 − 29784,6) | 36,0 (29820,6 − 29784,6) |

**Clasificación: `QUESTION_ERROR`** sobre `IMPLICIT_MODULE_ORIGIN`. Tras el gap
de 1,50 la excursión contraria inicial (apertura → máximo) se absorbe y el módulo
implícito nace en la apertura; la lectura humana mide el tramo dominante desde el
extremo de la excursión prohibida. Ambas lecturas son geométricamente
consistentes con los ticks (el rango de la vela es exactamente 53,60); la
diferencia es de **origen**, no de medición. No se introduce ninguna excepción.

## 8. Tercera divergencia (16:31) — consecuencia

Con el módulo de 36,0 el motor abre A 26,10 (29784,6 → 29810,7), B 28,40 y
C Grande; no arma el TT humano. Con el módulo de 53,6 la geometría humana se
reproduce exactamente desde los ticks:

- final_A = máximo de 16:31 = **29810,8** (motor: 29810,7)
- objetivo TT = 29810,8 − 53,6 = **29757,2**
- mínimo de 16:31 = **29760,3**
- distancia al objetivo = **3,1 puntos** → TT pendiente

Es decir: la lectura humana de 16:31 **no necesita corrección**; queda bloqueada
por la divergencia de origen de 16:30, no por su propia aritmética.

`16:32` no se arbitra mientras `MODULE_ORIGIN_RESOLUTION` siga abierta: la
secuencia humano «TT no alcanza objetivo → supera final_A → TT falla → módulo
conjunto → nueva A» no puede evaluarse sin el origen del módulo.

---

## 9. Reglas, políticas y heurísticas

| id | forma general | autoridad |
|---|---|---|
| `R21-CANDIDATE-ISOLATION` | un candidato no escribe estado confirmado; solo un commit lo hace | `CANONICAL_DERIVATION` |
| `R21-PHYSICAL-THRESHOLD` | el umbral físico solo crea `PHYSICAL`; no crea función | `CANONICAL_DERIVATION` |
| `R21-CONSUMES` | una pregunta solo lee referencias declaradas de su rama y generación | `CANONICAL_DERIVATION` |
| `R21-SHADOW` | un candidato absorbido no se recrea sin superar su extremo | `CANONICAL_DERIVATION` |
| `R21-RETENTION` | confirmar exige tick posterior al alta y retención del extremo | `CANONICAL_DERIVATION` |
| `R21-NO-BIRTH-CONFIRMATION` | la evidencia que crea el candidato no puede confirmarlo | `CANONICAL_DERIVATION` |
| `R20-1-A_DELIMITED_AT_CLOSE` | A delimitada al cierre de su vela | `PROVISIONAL_CONTEXTUAL_POLICY` (no universal) |
| `P21-MODULE-ORIGIN` | origen del módulo implícito tras gap = apertura | `PROVISIONAL_POLICY`, en revisión (`MODULE_ORIGIN_RESOLUTION`) |

Rechazadas como universales: porcentaje fijo, número de ticks, cambio de vela
como cierre de función, «B al 100 % para confirmar A», salto fijo de 4 puntos.

---

## 10. Pruebas (50)

Sección A (15): estados, prohibición de escritura directa, veto de nacimiento,
retención, `consumes`, referencias ajenas, commit cruzado, rol no permitido,
sombra, niveles de absorción, pregunta cerrada.

Sección B (10): tramo real — cero violaciones, commits `ADMIT`/`CONFIRM`,
propietarios, archivo de LOCAL-G1, `IMPLICIT_MODULE_ORIGIN`, dos ramas,
determinismo, prefijo, espejo estado/lector, sombras.

Sección C (25): absorbido vs A; >2 puntos absorbido; `<2` nunca `PHYSICAL`;
extensión y no-extensión; retención sin función; extensión sin función;
plano/gap; cola inicial; primer toque; ledger inmutable; marcas de vela; dos
ramas en el mismo tick; TT que confirma y TT que falla; tercera rama; lectura
cruzada; **traslado de precios**; **inversión vertical**; **cambio de escala**;
**cambio de timestamps y `sequence_id`**; determinismo del trazador; prefijo de
la traza; clasificador de nueve categorías; auditoría de valores incrustados;
propietarios de patrones y generaciones.

La invariancia es fuerte: trasladar el precio +1000 puntos, invertirlo
verticalmente o duplicar la escala deja el estado idéntico (los tamaños se
duplican exactamente). No hay precios ni horas en el código ejecutable.

---

## 11. Dudas residuales

1. `AB_DELIMITATION_IN_NOISY_BAR`: en una vela con absorciones repetidas, ¿qué
   evidencia cierra la A sin fragmentarla? Requiere una pregunta propia.
2. `MODULE_ORIGIN_RESOLUTION`: ¿el origen del módulo implícito es la apertura del
   gap o el extremo de la excursión contraria que el propio gap prohibió?
3. `LOCAL-G2` no se ha abierto. El slot está libre y la rama `LOCAL-G1` está
   archivada; abrirla exige resolver (1) para que su A no herede la principal.
4. Las anclas 16:27–16:32 quedan como `OPEN` con evidencia tick a tick; no se
   han «arreglado» con excepciones.

---

## 12. Estado máximo alcanzado

`CANDIDATE_CONFIRMATION_ARCHITECTURE_COMPLETE` — la arquitectura que impide que
el ruido contamine el árbol está implementada y probada. No es un motor
completo: falta la resolución funcional de A/B en velas ruidosas y el arbitraje
de origen de módulo.
