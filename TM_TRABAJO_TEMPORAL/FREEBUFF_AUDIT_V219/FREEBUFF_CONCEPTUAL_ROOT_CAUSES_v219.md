# FREEBUFF_CONCEPTUAL_ROOT_CAUSES_v219

**Diagnóstico conceptual de R5 frente al árbol TM v2.19**
**Fecha:** 2026-10-30
**Árbol:** `94A1408A6123ED66948988334E7D540C2A2692C36EEA3CB736DBFF0DA2346B17` (WORKING_CANON_NOT_FROZEN)
**Motor:** R5 `9BD1BEDB5DEC8C5A1C3A831338503E90CC04EE3CD776CF4E01D27CF8AA0EBEAE`
**Evidencia:** 21 secuencias CE reproducidas + 262 prefijos + traza adicional `probe_dual_authority`
**Versión documental:** 1.0 · **Versión del motor:** `0.7.5.2-R5`
**tree_modified = false · engine_modified = false · goldens_modified = false · observational_only = true**

---

## 0. Método

No se parte de la conclusión de OpenBot. Se parte de tres preguntas:

1. ¿Qué representa realmente el estado que el motor emite?
2. ¿Qué debería representar según el árbol?
3. ¿En qué tick exacto se separan ambas cosas?

Cada divergencia se separa en cinco niveles:

```text
SÍNTOMA        qué se ve en la salida
ERROR LOCAL    qué condición o mutación lo produce (con línea)
ERROR CONCEPTUAL qué principio TM no está representado
PRINCIPIO UNIVERSAL qué regla debe gobernar todos los casos equivalentes
PROPAGACIÓN    qué fallos posteriores son consecuencia
```

## 1. La violación constitucional que explica casi todo

El árbol es explícito:

```text
v2.5 §D: la lectura TM se realiza siempre, sin importar el tamaño.
         6,00 puntos es filtro de la capa operativa futura.
v2.5 §H: no usar el filtro de 6 puntos para alterar
         A, B, AUT, TT, C, CUT o FT.
```

R5 usa `MOVE = 600` (6,00 puntos) como **mínimo ontológico** en todos estos lugares:

| Uso | Línea | Efecto |
|---|---:|---|
| `MovementBuilder(min_move=MOVE)` | 334, 355-362 | No hay dirección ni movimiento hasta 6,00 |
| Cierre de movimiento por `max(MOVE, 25 %)` | 363 | Una vibración < 6,00 nunca cierra movimiento |
| `_maybe_aut`: `if r.a_size < MOVE: return` | 918-919 | Sin A ≥ 6,00 no hay AUT |
| `_close_candidate_bar`: `span < MOVE: return` | 2797 | El `1` local exige vela de 6,00 |
| `_local_leg`: `if size < MOVE: return` | 2742 | A, B y C locales exigen 6,00 |
| A local: `abs(ae - a0) >= MOVE` | 3142 | A Grande exige 6,00 |
| B local: `counter_size >= MOVE` | 3187 | B candidata exige 6,00 |
| C local: `begin_c(p.price, MOVE)` | 3207 | C Grande exige 6,00 |
| `_open_candidate`: `movement.size >= MOVE` | 1436 | B confirmada primaria exige 6,00 |

**Error conceptual:** el filtro de elegibilidad operativa se ha convertido en la frontera ontológica de la lectura. El árbol dice "leer siempre; filtrar después"; el motor dice "si no hay 6,00, no existe".

**Principio universal:** una función existe por la **finalidad que cumple y la referencia que rompe**, no por su tamaño. El único umbral estructural de lectura es el filtro de ruido de 2,00 puntos; el de 6,00 solo clasifica elegibilidad operativa.

Esta violación, por sí sola, explica que CE-1 (un `1` de 2,00) sea imposible y que todas las funciones pequeñas desaparezcan.

## 2. RC-1 — La unidad de decisión es el movimiento cerrado

### 2.1 Formulación

R5 no decide por tick. Decide cuando `MovementBuilder` **cierra** un movimiento, y solo cierra cuando el precio retrocede `max(6,00; 25 % del recorrido)` desde su extremo.

```text
tick → actualiza origen/extremo
     → si el retroceso >= max(6,00; 25 %) → Movement cerrado
     → _process_movement → _create_reading (MODULE, función "1")
     → _update (extiende módulo o abre A)
```

Consecuencia: **no existe un movimiento en curso**. Existe un movimiento ya cerrado, y la función se le asigna retrospectivamente.

El árbol exige lo contrario: la función nace con el primer desplazamiento y **vive** mientras el movimiento se desarrolla (`ONE_CANDIDATE`), con origen inmutable y extremo móvil. El cierre no crea la función: la confirma o la descarta.

### 2.2 Las cuatro causas independientes

RC-1 no es un solo `if`. Es una premisa compartida con cuatro causas técnicamente separables. Cada una puede arreglarse sin las otras, y cada una produce un fallo distinto.

#### RC-1.1 — No hay bootstrap de `1`

- **SÍNTOMA:** CE-1, CE-3, CE-4, CE-5, CE-6-NEG, CE-7 no tienen lectura en el tick 2.
- **ERROR LOCAL:** `MovementBuilder.feed` (351-362) no asigna `direction` hasta `p.price - origin >= 600`; `_open_candidate` (1383-1415) solo crea `FIRST` cuando ya existe un `Movement` cerrado.
- **ERROR CONCEPTUAL:** el motor no representa la **candidatura** de `1`. Solo representa su consolidación.
- **PROPAGACIÓN:** sin `1` no hay `2`; sin `2` no hay `3`; sin `3` no hay módulo regular ni A; sin A no hay B, AUT, C, CUT, TT.
- **PRUEBA QUE LO AÍSLA:** una secuencia de 2,00 puntos debe producir `1` candidata con origen y extremo; hoy produce cero eventos.

#### RC-1.2 — La escalera PRIMARY no contiene `2` ni `3`

- **SÍNTOMA:** en las 21 secuencias no se emite nunca `2` ni `3`; la única pregunta primaria es `DONDE_NACE_A`.
- **ERROR LOCAL:** `_advance_primary_question` (3282-3313) asigna a `MODULE` la pregunta `expected_function="A"` (3290-3297). `2` y `3` solo existen en `_process_local_sequence` (3005-3281).
- **ERROR CONCEPTUAL:** la escalera `1→2→3→A` está partida en dos máquinas. La primaria empieza en `A`; la local empieza en `1`, pero **solo se arma tras un AUT primario** (`_observe_core_aut`, 2784-2790).
- **PROPAGACIÓN:** aunque RC-1.1 se corrigiera, la lectura primaria seguiría sin preguntar por `2`. Y la local seguiría sin poder arrancar sin un AUT que, a su vez, exige toda la escalera primaria.
- **PRUEBA QUE LO AÍSLA:** con un `1` ya inyectado, la siguiente pregunta primaria debe ser `2`, no `A`.

Esta es la razón de fondo del bloqueo circular:

```text
para tener LOCAL necesito AUT
para tener AUT necesito A, B, B Grande y 127 %
para tener A necesito un movimiento contrario cerrado
para tener lectura necesito un movimiento de 6,00 cerrado
```

#### RC-1.3 — El módulo absorbe `2` y `3`

- **SÍNTOMA:** CE-2 mide módulo 0→16 cuando el `1` canónico es 0→10; CE-7-C mide 25→−0,25 cuando el `1` canónico es 25→0.
- **ERROR LOCAL:** `_create_reading` fija `module_origin = movement.origin` y `module_extreme = movement.extreme` (879-884); `_update` extiende `module_extreme` con **cada** movimiento de la misma dirección (1074-1093). `module_size` es `|extremo − origen|` (254).
- **ERROR CONCEPTUAL:** el módulo se identifica con el **recorrido total de la pata**, no con la función `1`. Al no existir `2` ni `3`, sus recorridos se suman al módulo.
- **MATIZ IMPORTANTE:** el módulo **no siempre** está inflado. En CE-4-NEG la pata 0→20 es monótona y el módulo 0→20 es correcto. El error aparece cuando la pata contiene oscilaciones internas que no alcanzan el retroceso de 6,00: entonces el movimiento las absorbe y el módulo las incluye. Por eso CE-2 (0→16) falla y CE-4-NEG (0→20) acierta.
- **PROPAGACIÓN:** TT se proyecta con un módulo mayor; CUT y porcentajes 100/127 se calculan sobre una base distinta; la comparación entre lecturas de distinta volatilidad deja de ser válida.
- **PRUEBA QUE LO AÍSLA:** una pata con retrocesos internos de 3,00 debe producir módulo 10,00 y funciones separadas; no un módulo 16,00.

#### RC-1.4 — Cada función exige 6,00 para existir

- **SÍNTOMA:** A no nace de un giro de 2,00; B no nace de 2,00; C no nace de 2,00.
- **ERROR LOCAL:** umbrales `MOVE` en A (3142), B (3187), C (3207) y AUT (918).
- **ERROR CONCEPTUAL:** se aplica el filtro operativo a las funciones, en contra de v2.5 §H.
- **PROPAGACIÓN:** una secuencia real con giros de 2–5 puntos nunca produce funciones, aunque el árbol las exija.
- **PRUEBA QUE LO AÍSLA:** A de 2,00 exactos debe existir (filtro de ruido); hoy no existe.

### 2.3 ¿RC-1 es una causa o varias?

**Una premisa, cuatro causas.** La premisa es: *"una función solo existe cuando un movimiento se ha cerrado"*. Las cuatro causas son independientes en el código:

| Causa | Puede corregirse sola | Efecto si solo se corrige ella |
|---|---|---|
| RC-1.1 bootstrap | sí | habría `1`, pero la pregunta primaria seguiría siendo `A` |
| RC-1.2 escalera | sí | habría `2/3`, pero solo tras un AUT que aún no puede existir |
| RC-1.3 módulo | sí | el módulo mediría bien, pero seguiría naciendo tarde |
| RC-1.4 umbrales | sí | A/B/C pequeñas existirían, pero sobre un `1` inexistente |

Por eso **no basta con un parche**: corregir solo RC-1.1 produce un `1` que nunca se convierte en `2`; corregir solo RC-1.2 produce una escalera que nunca arranca. La arquitectura debe sustituir la unidad de decisión, no añadir etiquetas.

## 3. RC-2 — El gap se detecta pero no se resuelve

- **SÍNTOMA:** CE-6-POS y CE-6-FRON emiten `GAP` y nada más; CE-6-NEG no emite nada.
- **ERROR LOCAL:** `_schedule_gap` (1540-1558) programa un evento informativo con `gap` y hora; no guarda estado, no crea referencias, no llama a ninguna resolución. `_process_local_sequence` (3005-3013) retorna sin decidir si hay gap en fase `AFTER_3`/`A_CANDIDATE`/`A_ACTIVE`. En `WAIT_TWO` el gap sí produce `_two_impossible` (correcto: no hay `2`), pero la fase resultante es `AFTER_3` → `A`, no un nuevo `1` desde la apertura.
- **ERROR CONCEPTUAL:** el motor modela **precios**, no **estructura**. Sin ticks no hay movimiento, y sin movimiento no hay función. El árbol dice lo contrario: el tramo no negociado **es** una resolución funcional (`A Grande` → `B Grande` → `A usada como tendencia`) y la apertura es el origen operativo del nuevo `1`.
- **PROPAGACIÓN:** tras un gap, la lectura continúa desde una referencia anterior a la apertura, o no continúa en absoluto. Se pierde el nuevo `1`, y con él todo el ciclo siguiente.
- **¿Depende de RC-1?** **Parcialmente.**
  - La detección y el `NO_TWO` son independientes: ya funcionan.
  - El registro de funciones implícitas podría emitirse sin resolver RC-1 (son eventos sin precios internos).
  - Pero el **nuevo `1` desde la apertura** necesita el ciclo de vida de `1` (RC-1.1). Sin él no hay dónde alojarlo.
  - Además, la rama local de gap es inalcanzable hoy porque LOCAL nunca se arma sin AUT (RC-1.2).

## 4. RC-3 — Función, patrón y evento comparten un solo campo

- **SÍNTOMA:** una `C` se emite sobre una lectura en `TT_EXT`; el `FT` la pasa a `DONE`; el `CUT` se guarda como `fail_reason`; el TT se escribe como `state`.
- **ERROR LOCAL:** `Reading.state` (162-252) contiene a la vez `MODULE`, `A`, `B_CAND`, `TT_PENDING`, `C`, `TT_EXT`, `DONE`; `_done` (899-914) usa `fail_reason` como sustituto de evento.
- **ERROR CONCEPTUAL:** no se distingue **qué es** la estructura (función), **qué patrón la recorre** (TT/FT) y **qué evento la cierra** (AUT/CUT/invalidación). El árbol exige tres capas que coexisten sin borrarse.
- **PROPAGACIÓN:** al confirmar un patrón se sobrescribe la función; al cerrar la lectura se pierde la función que debía seguir viva; el historial no es consultable por capa.
- **ESTADO:** no se puede ejercitar plenamente en las 21 CE porque el motor no llega a TT/FT/CUT. La evidencia es de código y de la traza adicional (C emitida sobre `TT_EXT`).

## 5. RC-4 — Tres autoridades para el mismo tick

- **SÍNTOMA:** el mismo tick puede producir una decisión de `_update` (movimiento), otra de `_process_local_sequence` (fase local) y otra de `_legacy_tick_decision` (tick primario). En la traza adicional, `B_GRANDE` y `AUT` se emiten en el mismo tick y el TT se pierde.
- **ERROR LOCAL:** `feed_chunk` (3418-3460) ejecuta, en este orden: `_process_movement`, `_advance_primary_question` (que llama a `_legacy_tick_decision`), cierre de vela y `_close_candidate_bar`, `_observe_core_aut`, `_process_local_sequence`. Cada una puede crear, extender o cerrar lecturas.
- **ERROR CONCEPTUAL:** no existe **una** autoridad que responda "qué función viene ahora" por lectura y por tick. Hay tres, con nociones distintas de módulo, B Grande y cierre.
- **PROPAGACIÓN:** genealogías duplicadas, estados contradictorios y TT perdido. `_shadow_compare` solo registra divergencias; no arbitra.
- **EVIDENCIA:** `03_CONCEPTUAL_DIAGNOSIS/probe_dual_authority.out`, caso B: tick 17 emite `B_GRANDE` y `AUT` con el mismo timestamp; el objetivo TT 28,00 se supera hasta 40,00 y el TT no se confirma.

## 6. Correspondencia con los siete conceptos CE

| Concepto CE | Fallos | Confirmado en código | Causa raíz |
|---|---|---|---|
| CE-1 tamaño vs finalidad | F-01..F-05 | sí | RC-1.1, RC-1.3, RC-1.4 + violación de v2.5 §H |
| CE-2 función/patrón/estado | F-06 | sí | RC-3 |
| CE-3 autoridad única | F-07, F-08 | sí | RC-1.2, RC-4 |
| CE-4 escalas concurrentes | F-09 | sí | RC-4 + `module_size` único |
| CE-5 tiempo de conocimiento | F-10 | sí | RC-1 (decisión al cierre) |
| CE-6 gap | F-11 | sí | RC-2 |
| CE-7 transformación funcional | F-12 | sí | RC-3 + genealogía |

**Matices de esta auditoría frente a OpenBot:**

- **F-01:** se confirma, pero con dos formas distintas. En PRIMARY el `1` es un **movimiento** (origen→extremo); en LOCAL es el **rango de una vela** (`bar.low`→`bar.high`, 2796-2800). Ambas son "contenedor", no "contenido".
- **F-02:** se confirma, pero el umbral dominante es **6,00**, no 2,00. El umbral de 2,00 aparece en otra ruta: `_open_candidate` puede crear una lectura nueva `A_SIGNIFICATIVA` cuando A ≥ 75 % del módulo (1462-1475), y `A_DESPROPORCIONADA_MODULO` cuando A > 2× módulo (1533). Son dos patologías distintas: funciones por tamaño y lecturas nuevas por proporción.
- **F-04:** se confirma con el matiz de CE-4-NEG: el módulo no siempre está inflado; solo cuando la pata absorbe oscilaciones < 6,00.
- **F-08:** se confirma, pero la herramienta principal es `_two_impossible` (2988-3004), que en la variante auditada sustituye al simple `_local_gate_event` de la variante empaquetada.
- **F-10:** se confirma y se agrava: el TT puede perderse por completo, no solo llegar tarde (traza adicional).

## 7. Tabla síntoma / error local / conceptual / propagación

| # | SÍNTOMA | ERROR LOCAL | ERROR CONCEPTUAL | PROPAGACIÓN |
|---|---|---|---|---|
| 1 | CE-1 sin lectura | `MovementBuilder` exige 6,00 (355-362) | no hay `1` candidata | no hay 2/3/A/B/C |
| 2 | CE-3 sin `2` | `_advance_primary_question` espera `A` (3297) | escalera partida en dos máquinas | `2/3` inalcanzables |
| 3 | CE-2 módulo 16 | `module_extreme` se extiende con cada movimiento (1074-1093) | módulo = pata completa, no `1` | TT/CUT sobre base falsa |
| 4 | CE-7 módulo 25,25 | ídem | ídem | ídem |
| 5 | A no nace de 2,00 | `>= MOVE` (3142) | filtro operativo usado como ontología | funciones pequeñas inexistentes |
| 6 | B no nace de 2,00 | `counter_size >= MOVE` (3187) | ídem | ídem |
| 7 | C no nace de 2,00 | `begin_c(..., MOVE)` (3207) | ídem | ídem |
| 8 | CE-6 solo `GAP` | `_schedule_gap` (1540-1558) | el gap no es estructura | nuevo `1` perdido |
| 9 | `TT` nunca confirmado | `_check_tt` solo al cerrar movimiento (1027) | decisión al cierre, no al tick | TT perdido con precio 12 puntos arriba |
| 10 | `B_GRANDE` + `AUT` mismo tick | `_b_grande` llama a `_maybe_aut` (1021) | sin árbitro de secuencia | N-037 violado |
| 11 | `C` sobre `TT_EXT` | `state` único (162) | capas mezcladas | función borrada por patrón |
| 12 | lectura local tras AUT | `_observe_core_aut` (2784) | `1` local no hereda el `1` del ciclo | genealogía duplicada |

## 8. Qué hace bien R5 (no desechar)

| Concepto | Evidencia |
|---|---|
| Precios en centésimas, sin floats | `price_i`, `PRICE_SCALE` |
| Plano/gap con comparación entera | `PLANO_TICK = 25`, `local_two_gate` |
| AUT estricto `> 127 % + 0,25` | `BigBTracker.limit`, tests 28/28 |
| B Grande exactamente al 100 % | `b_size >= a_size` |
| TT por `>=` objetivo | `_check_tt` |
| C solo tras B Grande | `begin_c` exige `confirmed` |
| A se extiende entre velas | `_update` estado A |
| Sin color ni OHLC para clasificar | todo el motor sobre ticks |
| Historial al cerrar | `_done` + `ARCHIVADA` |
| Tiempos estructural/confirmación/conocimiento | campos `*_time` |
| Determinismo y causalidad de prefijos | 21/21 y 262/262 |
| Límite de 3 lecturas | `MAX_ACTIVE` |
| Ingesta y orden de ticks | `load_feed`, `feed_chunk` |
| Serialización y comparadores | `serialize_state`, `write_outputs` |

## 9. Lo que no puede decidirse sin Javier

1. **Confirmación y congelación de `1`.** El árbol no fija el tick exacto. Sin ello, la medida del módulo y la puerta de `2` quedan indefinidas (ver `FREEBUFF_EXPERT_QUESTIONS_v219.md`, Q1).
2. **0,25: plano o gap.** H14 dice `≤ 0,25`; v2.13 y CE-6 dicen `< 0,25`. R5 aplica `< 0,25`. Es una contradicción documental, no un fallo de código (Q2).
3. **CUT contra `a_end` o contra la base del módulo.** N-024 y v1.2/v2.17 no coinciden (Q3).
4. **Nuevo `1` en AUT o en TT** cuando el AUT no cruza la base del módulo (Q4).
5. **Medida del módulo `1-2-3`: desplazamiento direccional o expansión high-low** (N-012 vs N-040) (Q5).
6. **FT: tick y condición estructural** (R-02) (Q6).
7. **Apertura/prioridad L2/L3** (R-04) (Q7).

## 10. Orden conceptual de corrección (sin código)

1. **Sustituir la unidad de decisión**: de "movimiento cerrado" a "estado funcional por tick".
2. **Ciclo de vida de `1`**: `ONE_CANDIDATE → ONE_CONFIRMED` con origen inmutable y medida congelada.
3. **Escalera única**: `1 → 2 → 3 → A → B → AUT → C → CUT → TT → FT` en una sola autoridad.
4. **Módulo como función**, no como pata: el módulo se deriva de `1` (y de `2/3` cuando corresponda), nunca del recorrido total.
5. **Eliminar `MOVE` de la lectura**: solo `2,00` (ruido) y `0,25` (tick/plano); `6,00` queda para la capa operativa.
6. **Gap como resolución funcional** con funciones implícitas sin precios y nuevo `1` en la apertura.
7. **Separar función / patrón / evento** antes de tocar TT, FT o CUT.
8. **Un árbitro cronológico** (v2.7) antes de abrir A/B/módulo.

Nada de esto se implementa en esta fase.
