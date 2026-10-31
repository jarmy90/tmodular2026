# ITERACION 23A — AUDITORIA GEOMETRICA DE LOCAL-G2 (16:26–16:29)

Estado: **ITER23_STATUS = LOCAL_GEOMETRY_VALIDATED**

Baseline: `TM_ITERATION_22_REVIEW.zip` (extraido en `LUNA_22`, suites reproducidas
antes de tocar codigo). No se toca 16:30, ni MODULE_ORIGIN_RESOLUTION, ni 16:31,
ni 16:32. La arquitectura autoritativa de 22 se conserva.

---

## 1. Baseline reproducido

| Suite | Antes de la auditoria | Despues |
|---|---|---|
| 169 regresiones canonicas | 169/169 | 169/169 |
| 19B tests | 23/23 | 23/23 |
| 19B anclas de transicion | 12/12 | 12/12 |
| 20A anclas | 10/10 | 10/10 |
| Iteracion 21 | 50/50 | 50/50 |
| Iteracion 22 | 39/39 | 39/39 |
| Iteracion 23A | — | 42/42 |
| gate 22 / gate 23A | OK | OK |

## 2. Convencion de direccion (contradiccion 1)

`dir = signo(extremo − origen)`: **+1 = alcista, −1 = bajista**. El modulo
29873,80 → 29867,00 con `dir = +1` era **un error de campo**, no documental:
tras la reclasificacion "A deviene modulo" el motor seguia re-bloqueando el
modulo contra `_dir_lock` (la direccion vieja) y extendia el extremo por el lado
contrario. Resultado: origen 29 873,80 con extremo por debajo → geometria
imposible en 920 de los 991 ticks de la ventana.

Correccion (general, sin precios ni horas): la reclasificacion re-bloquea
`_dir_lock` en la direccion de A y el extremo solo puede extenderse en esa
direccion; cualquier incoherencia se contabiliza como
`module_direction_invalid`. Tras el arreglo: **0 rupturas** en 16:26–16:28 y en
16:27–16:28 (`module_direction_breaks_16_26/27 = 0`).

## 3. Genealogia del modulo (contradiccion 2)

La A **no** comparte origen con el modulo "por accidente". Secuencia real
(rama 16:26):

| seq | hecho |
|---|---|
| 2553 | semilla local |
| 2557 | excursion dominante provisional: 29 869,30 → 29 871,80, **2,50**, dir +1 (`mod_extreme=2987180`, `mod_size=250`) |
| 2562 | extremo del modulo extendido a 29 873,80: 29 869,30 → 29 873,80, **4,50**, dir +1 (`mod_extreme=2987380`, `mod_size=450`) |
| 2567 | A candidata: origen 29 873,80 (= extremo del modulo provisional), dir −1 |
| 2623 | A confirmada (11,20). 11,20 > 4,50 → **reclasificacion explicita**: `MODULE:001` (4,50 alcista) queda en historial y el modulo pasa a `MODULE:002` = A (origen 29 873,80, extremo 29 862,60, 11,20, dir −1, `source_function = A:001`) |

Escena: **`SCENE_1_MODULE_EXTENSION_ABSORBS_A`** — el tramo medido inicialmente
como modulo (4,50) era interno al movimiento dominante; la A mayor deviene
modulo (opcion A del pliego) con **reclasificacion trazada** (opcion E). No es
"C: A con origen incorrecto" (`A.origin == birth_module_extreme` = 29 873,80) y
la direccion invertida era el bug F, ya corregido.

El modulo derivado de A **sigue extendiendose**: 53 ticks por debajo del extremo
de A hasta 29 822,10 (51,70). Eso no reescribe nada: se registra
`LOCAL_MODULE_EXTENDS_BEYOND_A` y la A conserva su delimitacion y su
`knowledge_time`. Es exactamente el fenomeno que abre
`MODULE_ORIGIN_RESOLUTION` (16:30) y por eso **no se resuelve aqui**.

## 4. Genealogia de A

| campo | valor |
|---|---|
| funcion | `LOCAL-G2:A:001` |
| origen / extremo | 29 873,80 → 29 862,60 |
| tamano / direccion | 11,20 / −1 |
| modulo de nacimiento | `MODULE:001`, extremo de nacimiento 29 873,80 |
| evidencia de nacimiento | seq 2567 (`LOCAL_A_CANDIDATE`) |
| evidencia de confirmacion | seq 2623 (`LOCAL_A_DEVELOPMENT` → `A_CONFIRMED`) |
| structural_time / knowledge_time | 1792167961885 / 1792167976866 (kt > st) |

A continua entre velas: cero cierres forzados por `bar_close` en la ventana.

## 5. Genealogia de B y ratio (contradiccion 3)

| campo | valor |
|---|---|
| funcion | `LOCAL-G2:B:001` |
| source_function | `LOCAL-G2:A:001` |
| origen (= extremo de A) | 29 862,60 |
| extremo | 29 867,00 |
| tamano / direccion | 4,40 / +1 |
| 100 % / 127 %+0,25 | 11,20 / 14,47 |
| **ratio** | 440 / 1120 = **0,3929** |
| estado | `B_CANDIDATE_CONFIRMED` (seq 2627) |

Sin B Grande no hay **A usada como tendencia** por esa via y no se arma TT: la
rama 16:26 termina en `tt.id = ""`. La contradiccion documental de 22
("A/B/A-tendencia = CONFIRMED_BY_TICKS" junto a "ratio 39,3 % → no B Grande")
queda **corregida**: la reclamacion es `PARTIALLY_CONFIRMED` (modulo y A
confirmados; B Grande y A-tendencia no existen).

Ademas, como el dominante continua mas alla del extremo de A, la B es un **rebote
interno** del modulo; el motor lo registra y no la promociona.

## 6. Genealogia del TT (contradiccion 4)

El TT de 28,70 no salia de un modulo de 28,70: salia de la **sonda de
sensibilidad sembrada en 16:27**, y el modulo crecio despues del armado. Ahora
la genealogia se congela al armar:

| campo | valor |
|---|---|
| tt_id | `LOCAL-G2:TT:001` |
| owner_generation | LOCAL-G2 (sonda 16:27) |
| owner_module_id | `LOCAL-G2:MODULE:001` (29 850,80 → 29 847,10 declarado 3,70) |
| module_size **al armar** | **7,00** (modulo extendido hasta 29 843,80) |
| source_function_id | `LOCAL-G2:B:001` |
| opened_at_seq | 2842 |
| final_A | 29 850,60 (= extremo de A) |
| direction | −1 |
| objective | 29 843,60 = final_A − 7,00 |
| invalidation | **FINAL_A** 29 850,60 |
| status | `TT_CONFIRMED` |
| first_boundary | `OBJECTIVE@2857` |
| st / kt | 1792168029912 (extremo de A) / 1792168030513 |

Dos correcciones de fondo:

1. **Referencia de invalidacion.** Un TT nacido de un AUT invalida en `final_A`;
   solo la A usada como tendencia invalida en el origen de A. La rama local
   aplicaba `a_origin` a un TT de AUT, lo que producia un `TT_FAILED` falso en
   16:27 (`INVALIDATION@2849`). Corregido a `FINAL_A` con cruce real (no toque):
   el TT alcanza su objetivo en seq 2857.
2. **Objetivo congelado.** `objective == final_A + dir * tt_module_size`, con
   `tt_module_size` registrado. El modulo final (28,70) no reescribe el patron:
   la medida 7,00 y la 28,70 pertenecen a momentos distintos y ambas son
   trazables.

## 7. Escenarios

| Escena | Resultado |
|---|---|
| `SCENE_1` modulo inicial extendido; la supuesta A era parte del modulo | **seleccionada** (reclasificacion + 53 extensiones posteriores) |
| `SCENE_2` modulo termina y A nace de su extremo | valida para tramos sin extension posterior (probada en sintetico G4) |
| `SCENE_3` dos estructuras locales sucesivas | rechazada: una sola semilla, un solo propietario, sin segunda escala |

## 8. Clasificacion de las reclamaciones humanas

| Reclamacion | Clasificacion | Base tick a tick |
|---|---|---|
| B Grande en la lectura local (16:27) | `PARTIALLY_CONFIRMED` | A local 11,20 y modulo confirmados; B 4,40 = 39,3 % del 100 %; rebote interno del dominante |
| Dos TT pendientes con propietarios distintos al cierre 16:28 | `CORRECTED_BY_TICKS` | TT activos = 1 (mayor `TT_PENDING` 29 822,80; local ninguno) |
| Ambos TT confirman en 16:29 | `CORRECTED_BY_TICKS` | solo el TT mayor confirma en 16:29; la rama propietaria no arma TT |

Sonda 16:27 (no propietaria, se conserva como sensibilidad): produce A 3,50,
B 6,80 (194 %), AUT con cruce causal y TT propio que **confirma**. Demuestra que
la semilla decide la geometria: `LOCAL_SEED_POLICY` queda abierta y **no se
fuerza** ninguna de las dos.

## 9. Autoridad de las preguntas

| funcion | nacimiento | confirmacion | autoridad |
|---|---|---|---|
| A local | `LOCAL_A_CANDIDATE` seq 2567 | commit `CONFIRM` `LOCAL_A_DEVELOPMENT` seq 2623 | TREE_QUESTION |
| B local | `LOCAL_B_OPENED` seq 2623 | commit `CONFIRM` `LOCAL_B_DEVELOPMENT` seq 2627 | TREE_QUESTION |
| B Grande / AUT (sonda) | commit `LOCAL_B_GRANDE_CONFIRMATION` / `LOCAL_B_LIMIT` | seq 2841 / 2842 | TREE_QUESTION |

`birth_evidence != confirmation_evidence` en las tres. Cero preempciones legacy,
cero escrituras de candidato, cero consumos fuera de `consumes`.

## 10. Inventario de medidas locales (ninguna sin explicacion)

| medida | que es | explicacion |
|---|---|---|
| 4,50 | modulo dominante provisional | `module_reclassifications.previous` |
| 11,20 | A local | `a.size`, 29 873,80 → 29 862,60 |
| 4,40 | B local | `b.size` = 39,29 % de A |
| 51,70 | modulo final (16:26) | extension posterior a A (53 ticks), registrada |
| 7,00 | modulo del TT (sonda) | `tt.module_size` congelado al armar |
| 28,70 | modulo final (sonda) | extension posterior al armado; el TT conserva 7,00 |

`unexplained_local_measurements = 0`.

## 11. Cambios de codigo

`05_REFERENCE_ENGINE/tm_local_generation.py`

1. Re-bloqueo de direccion en la reclasificacion A→modulo + invariante
   `signo(extremo−origen) == dir` (contador `module_direction_invalid`).
2. Evento explicito `LOCAL_MODULE_RECLASSIFIED` con geometria anterior completa
   (`module_reclassifications`).
3. Identificadores causales (`MODULE:nnn`, `A:nnn`, `B:nnn`, `TT:nnn`) y
   genealogia: `a_source_module_id`, `birth_module_extreme`, `b_source_function_id`,
   `tt_module_id/origin/extreme/size/source_function/opened_at_seq/invalidation_kind`.
4. `structural_time` real por extremo (modulo, A, B) y `knowledge_time` en el
   commit.
5. Invalidation del TT por genesis (`FINAL_A` / `A_ORIGIN`) y cruce real de
   frontera con precio previo.
6. Cruce causal B→B Grande→AUT (`CAUSAL_CROSS_IN_AUT_TICK`), espejo de MAIN.
7. `geometry()`: 14 invariantes derivables, usadas por pruebas y gate.
8. Diagnostico `LOCAL_MODULE_EXTENDS_BEYOND_A` (sin reescritura de estado).

`run_iteration_22_gate.py`: las tres reclamaciones se **derivan** de los ticks
(antes tenian veredicto y prosa fijos y evaluaban el TT local con la referencia
de invalidacion erronea). Ninguna prueba usa `False`/`True` fijos ni el estado
final para validar un instante anterior.

## 12. Pruebas nuevas

`run_iteration_23a_tests.py`: **42/42**. Cubre los 36 supuestos exigidos:
direccion, modulo extendido sin A prematura, A desde el extremo del modulo,
origen compartido solo con reclasificacion, reclasificacion trazada, A entre
velas, B fisica/estructural sin commit, B funcional delimita A, B desde el
extremo de A, ratio exacto, 39,3 % no es B Grande, sin B Grande no hay
A-tendencia, 100 % exacto, intervalo superior, AUT por un tick, C posterior,
TT con modulo/final_A/objetivo/ruta trazables, TT sin modulo rechazado, TT
confirmado, TT fallido, TT MAIN y LOCAL independientes, dos ramas en el mismo
tick, evidencia de nacimiento ≠ confirmacion, direccion invertida detectada,
traslado, inversion, escalado, timestamps, sequence_id, prefijo, determinismo y
los tres abortos de arquitectura (legacy, propietario, consumes).

## 13. Gate 23A

```
local_module_direction_valid          = true
local_module_size_valid               = true
local_module_genealogy_complete       = true
local_A_origin_valid                  = true
local_A_source_module_valid           = true
local_A_direction_valid               = true
local_B_origin_equals_A_extreme       = true
local_B_source_function_valid         = true
local_B_ratio_traceable               = true
local_B_grande_requires_100_percent   = true
local_A_trend_requires_valid_B_grande = true
local_TT_module_traceable             = true
local_TT_final_A_traceable            = true
local_TT_objective_derivable          = true
local_TT_activation_path_traceable    = true
module_direction_breaks_16_26/27      = 0 / 0
unexplained_local_measurements        = 0
contradictory_human_classifications   = 0
hardcoded_market_values               = 0
active_branches                       = 2
cross_owner_ratios                    = 0
legacy_preemptions                    = 0
determinism / prefix_consistency      = true / true
```

## 14. Divergencias residuales (fuera de 23A)

1. `MODULE_ORIGIN_RESOLUTION` (16:30): el dominante continua mas alla del
   extremo de la A confirmada. Resolver qué movimiento abre el modulo exige
   protocolo MISSING_RULE; no se inventa regla aqui.
2. `LOCAL_SEED_POLICY`: semilla 16:26 (propietaria, sin TT) frente a semilla
   16:27 (AUT + TT confirmado). La semilla no puede decidirse por coincidencia
   humana.

## 15. Entregables

- Tabla tick a tick: `04_CONCEPT_TESTS/ITER23A_LOCAL_TRACE_1626.csv` (991 ticks)
  y `ITER23A_LOCAL_TRACE_1627.csv` (745 ticks), 28 columnas por tick.
- Gate: `ITER23A_GATE.json`; pruebas: `ITER23A_TEST_RESULTS.{json,csv}`.
- ZIP: `TM_ITERATION_23A_REVIEW.zip` con `MANIFEST.json`, `SHA256SUMS.txt` y
  verificacion desde extraccion limpia (todas las suites en `rc=0`).
