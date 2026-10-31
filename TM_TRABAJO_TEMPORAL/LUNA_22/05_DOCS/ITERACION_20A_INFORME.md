# ITERACIÓN 20A — DELIMITACIÓN DE A AL CIERRE Y PROPIEDAD DEL TT

Fecha: 2026-10-31
Baseline: `TM_ITERATION_19B_REVIEW.zip`
Estado: `ITER20A_STATUS = A_DELIMITATION_AND_TREND_OWNERSHIP_COMPLETE`
Tramo abierto declarado: **16:30–16:32** (no se finge cerrado).

---

## 1. Resumen ejecutivo

Esta iteración no reconstruye el baseline: parte de él (169/169 pruebas, 13/19
anclas humanas, 12/12 anclas de transición 19B) y ataca el primer eslabón que
impedía avanzar: **la A de 16:26 nunca se delimitaba**, por lo que crecía durante
16:27–16:31 hasta 115,1 puntos y el TT asociado nacía con referencias absurdas
(objetivo 29645,2 en lugar de 29822,8).

Se han introducido **dos reglas generales** (ninguna depende de hora ni precio) y
se ha medido su efecto:

| Regla | Forma general | Estado |
|---|---|---|
| **R20-1** `A_DELIMITED_AT_CLOSE` | Una A pendiente cuyo extremo se alcanzó en la vela que cierra y que no ha producido un retorno autónomo (≥ NOISE) **desde su propio extremo** queda delimitada por el cierre estructural de esa vela. No aplica si existe módulo regular en la misma dirección. | CANONICAL_DERIVATION (hermana de Q-ONE-AT-CLOSE) |
| **R20-2** `PATTERN_OWNERSHIP` | La A que devino módulo por descarte y armó un TT con invalidación en su **origen** es propietaria de la tendencia: ni el AUT directo ni la absorción de B pueden reescribir sus referencias. | CANONICAL_RULE |

Efecto medido sobre el tickfeed real (16:15–16:32):

* A principal 16:26 = 29875,4 → 29849,1 (**26,3**), no 38,6 ni 115,1.
* Módulo por descarte = 26,3 (`BY_DISCARD_A`).
* TT resultante = 29849,1 − 26,3 = **29822,8** (invalidación en el origen de A,
  29875,4).
* El TT permanece `TT_PENDING` en 16:27 y 16:28 **sin reescritura**.
* El TT **confirma durante 16:29** y se extiende después (29784,6 en 16:30;
  29760,3 en 16:31, que coincide con el mínimo humano documentado).

El tramo 16:30–16:32 sigue abierto: la rotación del ciclo posterior a un TT
confirmado por la vía de tendencia no está cableada (la rotación solo existe para
`phase == NEW_ONE_ACTIVE`). Ver §9.

---

## 2. Escenas de 16:26

Se evaluaron tres escenas antes de tocar código:

| Escena | Contenido | Veredicto |
|---|---|---|
| **A** | A principal + FT explican todo el recorrido; no hay lectura local. | **ACEPTADA** (dominante) |
| **B** | A principal + FT coexisten con un módulo local candidato propio de una nueva generación. | Rechazada: el lector local, con el slot todavía ocupado por LOCAL-G1, arrastra el `one` 29850,0 de LOCAL-G1 y su módulo 19,7; no forma módulo por descarte de 16:26 sin heredar referencias. |
| **C** | El módulo local existe pero solo se confirma retroactivamente en 16:27. | Conservada como **OPEN_RULE Q-L2-1627** (evidencia nueva en §6). |

Decisión registrada por el gestor: `LOCAL_G2_NOT_SUPPORTED` en 16:26, con la
decisión reevaluable en 16:27 (`ITER19B_ANCHORS` C12 = OPEN_RULE).

Evidencia dura: el movimiento de 16:26 (29873,8 → 29849,1) **no crea módulo por
descarte local** porque el módulo local exige 1-2-3 propios y el `one` local
pertenece a la generación anterior; y la A principal nace simultáneamente desde
el extremo real del TT (29875,4), que es el mismo origen del FT. Es **doble
pertenencia causal**, no transferencia de referencias.

---

## 3. Geometría real de 16:27 (corrección de la lectura humana)

Con R20-1 activa, la reconstrucción tick a tick da:

| Magnitud | Valor derivado de ticks |
|---|---|
| A_origin | 29875,4 (extremo real del TT alcista, cola final de 16:25) |
| A_extreme | 29849,1 (mínimo de 16:26, confirmado al cierre de esa vela) |
| A_size | 26,3 |
| A_structural_seq | 2797 (16:26:59,673) |
| A_knowledge_seq | 16:26:59,874 (cierre estructural de su vela) |
| B_origin | 29849,1 |
| B_extreme | 29850,8 (máximo de 16:27) |
| B_size | **1,7** |
| B_100_level | 29875,4 (origen de A) |
| B_127_25_level | 29849,1 + 33,65 = 29882,75 |
| B_status | `CANDIDATE` (nunca B Grande, nunca AUT) |
| Módulo propietario | `BY_DISCARD_A`, 26,3 |
| TT_objective | **29822,8** |
| TT_direction | −1 |
| TT_status al cierre de 16:27 | `TT_PENDING` |

**Resultado humano:** `HUMAN_READING_CORRECTED_BY_TICKS` en un punto concreto:

| human_value | tick_derived_value | diferencia | evidencia | regla | efecto posterior |
|---|---|---|---|---|---|
| «A Grande → B Grande → A Grande usada como tendencia» (B Grande en 16:27) | B = 1,7 puntos (1,7 % de A), nunca alcanza el 100 % | 24,6 puntos de B faltantes | ticks 2807–3046 de 16:27: máximo 29850,8 contra origen de A 29875,4 | R20-1 + módulo por descarte de A | El TT no necesita B Grande: nace del módulo por descarte de la propia A y confirma en 16:29 |

No se rebajó el 100 % de B Grande: simplemente **la estructura de 16:27 no
contiene una B Grande**, y el TT no la requiere porque su módulo propietario es
la A por descarte (v2.2 del árbol).

Hipótesis geométricas ensayadas y motivo de rechazo:

| # | Hipótesis | Resultado |
|---|---|---|
| H1 | A empieza demasiado pronto (hereda 16:25) | Rechazada: el origen 29875,4 es el extremo real del TT y está en la cola de 16:25, como exige la lectura humana. |
| H2 | A termina demasiado tarde (absorbe 16:27) | **Causa raíz encontrada**: sin R20-1 la A se extendía a 29836,8 (38,6) y luego a 29760,3 (115,1). |
| H3 | A pertenece al propietario equivocado | Rechazada: A ∈ PRIMARY-G1, FT ∈ LOCAL-G1, mismo origen, capas distintas (ancla FT-19B-10). |
| H4 | B se abre tarde | Rechazada: B se abre al cierre de 16:26 con tamaño 0 y solo alcanza 1,7. |
| H5 | Referencia de LOCAL-G1 contaminando el tramo | Rechazada: cero fugas medidas (`cross_generation_reference_leaks = 0`). |
| H6 | Módulo propietario incorrecto | Rechazada: `mod_owner = A`, `mod_status = BY_DISCARD_A`, tamaño 26,3. |
| H7 | «A usada como tendencia» confundida con AUT directo | **Confirmada como riesgo real**: el AUT directo reescribía el TT. Corregido con R20-2. |
| H8 | Gap/plano retiene una función anterior | Rechazada: 16:26 no es plano (−1,5). |

---

## 4. Regla R20-1 — formulación y justificación

```
SI  phase == A_PENDING
    y a_status == CONTRARY_MOVE_PENDING
    y el extremo de A se alcanzó en la vela que ahora cierra
    y NO existe retorno ≥ NOISE cuyo origen sea ese mismo extremo
    y NO existe módulo regular en la dirección de A
    y 3 no conserva autoridad en esa vela
ENTONCES
    A queda delimitada por el cierre estructural de su vela
    (structural_time = tick del extremo, knowledge_time = cierre)
    módulo por descarte = |A|
    TT armado con invalidación en el ORIGEN de A
```

Justificación: es la hermana exacta de `Q-ONE-AT-CLOSE` (el 1 se confirma al
cierre de su vela) y del descarte de 1-2 que «se conoce al cierre». Sin ella, la
A de una vela sigue creciendo con la vela siguiente y el módulo por descarte se
calcula sobre un recorrido ajeno: exactamente el error H2.

Condición de retorno **desde el propio extremo**: se detectó que `return_size`
podía contener un retroceso interno antiguo (2,0 puntos medidos desde 29851,4
durante el descenso), lo que bloqueaba la delimitación. La condición correcta es
`return_origin == a_extreme`.

---

## 5. Regla R20-2 — propiedad del patrón

```
SI  A devino módulo por descarte y armó un TT con invalidación en su origen
ENTONCES a_trend_owner = True
        el AUT directo queda BLOCKED_BY_TT_OWNER
        la absorción de B no reabre A (no reescribe a_extreme)
```

Justificación: un TT con invalidación en el origen de la tendencia pertenece a esa
tendencia. Reutilizar la misma A como AUT directo (o reabrirla por absorción)
transfiere la propiedad del patrón sin evento explícito: es la fuga que producía
el segundo TT espurio 29821,3 y su fallo inmediato en 16:27.

---

## 6. Estado de 16:28 y 16:29

**16:28** — Existe **un** TT pendiente (29822,8, propietario PRIMARY-G1, módulo
26,3). La lectura humana propone dos TT (local de 16:27 + mayor de 16:26). Los
ticks no sostienen dos propietarios: el slot LOCAL quedó libre tras archivarse
LOCAL-G1 y la vela de 16:27 queda absorbida por la tendencia de la A principal.
Queda registrado como `OPEN_RULE Q-L2-1627`: la sonda local con el slot sin
archivar **sí** forma un módulo local propio (450) en 16:26–16:29, por lo que una
generación local nueva podría justificarse en 16:27 con evidencia adicional.
No se abre por invención.

**16:29** — El TT confirma por cruce real del objetivo 29822,8 (mínimo de la vela
29822,1) durante la vela, no por cierre. Después se extiende:

| Vela | Extremo físico del TT |
|---|---|
| 16:29 | 29822,1 (confirmación) |
| 16:30 | 29784,6 |
| 16:31 | **29760,3** (mínimo humano documentado) |

El extremo físico coincide con el mínimo humano de 16:31, lo que es evidencia
independiente de que la geometría A → módulo → TT es la correcta.

---

## 7. Reglas provisionales y su estado

| Política | Estado tras 20A |
|---|---|
| Filtro de autonomía física 2,0 puntos (`NOISE`) | PROVISIONAL_PHYSICAL_AUTONOMY_FILTER (sin cambios) |
| 35 % para confirmar A de un nuevo 1 | PROVISIONAL_POLICY, **no aplicada** en la vía de cierre de vela (R20-1 usa otro criterio: extremo en la vela + ausencia de retorno desde el extremo) |
| `REOPENED` para extremo funcional | Aislada: solo aplica a generación CLOSING, extremo PROVISIONAL y continuación del patrón propietario; una generación ARCHIVED no vuelve a ACTIVE |
| `tt_no_invalidate`, `tt_keep_first_pending` | Sin uso en la vía de tendencia (la propiedad la da R20-2) |
| Corredor de descubrimiento L2 | Sin cambios; no se usa en 16:26 |

---

## 8. Métricas verificadas

| Métrica | Valor |
|---|---|
| Pruebas canónicas (9 suites) | **169 / 169**, 0 fallos |
| Anclas de transición 19B | **12 / 12** |
| Anclas nuevas 20A | **10 / 10** |
| Anclas humanas 16:15–16:32 | **13 / 19** (B4-1..B4-3 siguen pasando; B4-4..B4-9 dependen de 16:27–16:32) |
| Fugas entre generaciones | 0 |
| Escrituras en generación archivada | 0 |
| Slots activos | 1 (PRIMARY) |
| Determinismo | true |
| Consistencia de prefijo | true |
| Reglas por hora/precio en el motor | 0 |
| `or True` / PASS fijos en anclas | 0 |

Adversariales ejecutadas sobre R20-1/R20-2:

* traslación +1.000 puntos → mismo módulo, mismo `final_A` relativo, mismo objetivo relativo;
* inversión vertical → mismo tamaño, dirección invertida;
* cambio de `sequence_id`/timestamps → misma clasificación;
* prefijo antes/después de la confirmación → sin spoiler;
* dos ejecuciones completas → idénticas.

---

## 9. Tramo abierto 16:30–16:32 (bloqueo exacto)

Estado: **NO RESUELTO**, declarado en el ancla D10.

Causa exacta: cuando el TT confirma en la vía de tendencia, la fase queda en
`B_LIVE`; `_on_bar_open` solo rota el ciclo si `phase == NEW_ONE_ACTIVE`
(`_rotate_cycle_after_tt` exige esa fase). Falta:

1. al confirmar el TT en la vía de tendencia, abrir el nuevo 1 canónico
   (`NEW_ONE_ACTIVE` con `n_origin = tt_final_a`, `n_extreme = extremo del TT`,
   `n_dir = tt_dir`), que es el movimiento que confirmó y extendió el TT;
2. dejar que la apertura siguiente ejecute `_rotate_cycle_after_tt` con
   `via = TT`;
3. procesar 16:30 (2 imposible al cierre → módulo por descarte) y 16:31
   (A + AUT sobre el módulo conjunto) hasta reproducir `final_A` 29810,8 y
   objetivo 29757,2, y el fallo de 16:32 por `final_A` antes que objetivo.

Ese es el siguiente cambio concreto, con una sola regla general y sin precios.

---

## 10. Cambios de código de esta iteración

`05_REFERENCE_ENGINE/tm_reference_interpreter_v1_direct_aut.py`

1. `_finalize_a(t, time_ms)`: extrae la finalización de A (compartida por la vía
   de retorno y la vía de cierre); marca `a_trend_owner` cuando la A deviene
   módulo por descarte y arma TT con invalidación en su origen.
2. `_confirm_a_at_close(bar, price, time_ms)`: R20-1.
3. `_on_bar_close`: nueva rama `A_PENDING` → `_confirm_a_at_close`.
4. `_confirm_aut_direct`: guarda `BLOCKED_BY_TT_OWNER` (R20-2).
5. `_on_b_candidate_tick`: la absorción de B no reabre una A propietaria de TT.
6. `Reading.a_trend_owner` (campo nuevo, por lectura).

Pruebas:

* `04_CONCEPT_TESTS/run_iteration_20_anchors.py` (10 anclas nuevas, incluye
  traslación, inversión, determinismo y prefijo).
* `04_CONCEPT_TESTS/probe_l1.py` (sonda de estado por vela).

Anclas de 19B: C10 reespecificada a lo que el motor sostiene (LOCAL-G2 no
abierta, slot libre, generación archivada) y C12 nueva que **registra** la
evidencia local en 16:26–16:29 como regla abierta. No se borró ninguna prueba.
