# TM — FASE A — POLÍTICAS EXPERIMENTALES DEL LECTOR

- **Instrumento:** `blind_reader.py`
- **Versión:** FASE_A_v1
- **SHA-256 actual:** `5453936409204D742D74E6F51D73B09DC3E1185E23F633261B5179C7E392F458`
- **Árbol:** v2.19 `94A1408A6123ED66948988334E7D540C2A2692C36EEA3CB736DBFF0DA2346B17`
- **Estado:** `WORKING_CANON_NOT_FROZEN`
- **tree_modified = false · engine_modified = false · goldens_modified = false · observational_only = true**

> **Limitación de integridad:** las políticas se aplicaron editando el lector
> en el mismo archivo, sin snapshots inmutables por versión. Por eso
> `HASH_ANTERIOR` figura como `NO_ARCHIVADO` en todas. No se inventan hashes
> intermedios. La evidencia de antes/después son las salidas existentes
> (`ev_200.csv`, `ev_600.csv`, `ev_1200.csv`, `ev_2000.csv`, `gen_*.csv`) y los
> eventos del bloque. Esta es una carencia del proceso de Fase A, no del
> análisis.

---

## 0. RESUMEN

| Estado | Políticas |
|---|---|
| **TREE_SUPPORTED** | P05, P09, P14 |
| **EXPERIMENTAL_ASSUMPTION** | P01, P02, P03, P04, P06, P08, P10, P12, P13, P15, P16 |
| **OPEN_RULE_DEPENDENCY** | P07, P11, P17 |
| **Total** | 17 |

Dos políticas son la causa directa de la fragmentación:

- **P13 / E-DIR:** el 1 se orienta por `close − open`, no por la transición.
- **P08 / E-ORIG:** el 1 nace en la vela siguiente, no en el extremo de la
  transición.

Ninguna de las dos es `TREE_SUPPORTED`. Las dos son `EXPERIMENTAL_ASSUMPTION` y
están en conflicto con v2.17/v2.18 y con 4.5.

---

## P01 — ONE_BAR_RANGE (H1)

| Campo | Valor |
|---|---|
| POLICY_ID | P01 |
| Versión | FASE_A_v1 |
| Hash anterior | `NO_ARCHIVADO` |
| Hash posterior | `54539364…` |
| Problema observado | El lector necesitaba una unidad para 1; R5 usaba el primer tramo físico y producía 29 lecturas. |
| Regla del árbol | 4.2 mide 2 contra el 100 % de 1; v005 16:15 fija 1 = 16,2 (rango de la vela) y 16:16 = 12,6. |
| Resultado anterior | 1 = primer tramo (R5): 29 lecturas en el bloque. |
| Resultado posterior | 1 = rango direccional de la vela: 16 generaciones. |
| Ticks afectados | 11.414; primera divergencia en gen 12. |
| Estado | **EXPERIMENTAL_ASSUMPTION** |
| Evidencia | Gen 12: 1 = 33,5 alcista; el tramo bajista 14,4 queda como origen. |

**Consecuencia:** la vela 16:49 es alcista por cierre, pero su primer tramo es
bajista. P01 elige el rango total y convierte el rebote en 1. En una vela no
monótona, P01 no distingue 1 de A. Es la primera causa de la inversión.

---

## P02 — A_MIN_6 (H2)

| Campo | Valor |
|---|---|
| POLICY_ID | P02 |
| Versión | FASE_A_v1 |
| Hash anterior | `NO_ARCHIVADO` |
| Hash posterior | `54539364…` |
| Problema observado | 2 puntos no deben crear A; hacía falta un mínimo. |
| Regla del árbol | v2.5 fija un mínimo teórico de 6 puntos; v2.16 dice que no hay umbral universal. |
| Resultado anterior | Con A = 2,00: 16 generaciones en el bloque (28 en total con warm-up). |
| Resultado posterior | Con A = 6,00: 16 generaciones en el bloque. |
| Variantes | A = 12,00 → 9 generaciones; A = 20,00 → 11. |
| Ticks afectados | Todas las transiciones A_TREND/AUT. |
| Estado | **EXPERIMENTAL_ASSUMPTION** (rechazada por Javier) |
| Evidencia | `gen_200.csv` (`6ced42ba…`), `gen_600.csv` (`bc203568…`), `gen_1200.csv` (`b8708f89…`), `gen_2000.csv` (`ed023815…`) |

**Consecuencia:** H2 no se adopta. La autonomía de A queda como
`CONTRARY_MOVE_PENDING` en el diseño conceptual. La cifra 6,00 no es canónica.

---

## P03 — RETRACE_2 (H3)

| Campo | Valor |
|---|---|
| POLICY_ID | P03 |
| Versión | FASE_A_v1 |
| Hash anterior | `NO_ARCHIVADO` |
| Hash posterior | `54539364…` |
| Problema observado | 3 exige un retroceso funcional válido de 2. |
| Regla del árbol | 4.3; el mandato manda investigar el 50 % exacto. |
| Resultado anterior | Sin retroceso definido, 3 no se podía evaluar. |
| Resultado posterior | Retroceso ≥ 2,00 puntos y ≤ 50 % de 2; 50 % exacto queda pendiente. |
| Ticks afectados | Gen 23 (cola 8,2), gen 25 (2 = 0,1); no hubo 50 % exacto. |
| Estado | **EXPERIMENTAL_ASSUMPTION / OPEN_RULE_DEPENDENCY** |
| Evidencia | `TWO_IMPOSSIBLE_TAIL` 17:17:59.962; `TWO_IMPOSSIBLE_CLOSE` 17:23:59.618 |

**Consecuencia:** no se confirmó ningún 3 en el bloque. La política no se
valida con evidencia; queda abierta.

---

## P04 — A_EXTENDS_AFTER_B_GRANDE (H4)

| Campo | Valor |
|---|---|
| POLICY_ID | P04 |
| Versión | FASE_A_v1 |
| Hash anterior | `NO_ARCHIVADO` |
| Hash posterior | `54539364…` |
| Problema observado | A podía extenderse después de B Grande y B se cancelaba. |
| Regla del árbol | v2.18: A conserva su origen y actualiza su extremo; B se mide desde el final real de A. |
| Resultado anterior | B se cancelaba al primer retroceso; A se fragmentaba. |
| Resultado posterior | A se extiende; B se reinicia desde el nuevo extremo de A. |
| Ticks afectados | Gen 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27. |
| Estado | **EXPERIMENTAL_ASSUMPTION** |
| Evidencia | Eventos `A_EXTENDED … (B reiniciada)` en 16:50:02, 16:52:06, 16:54:04, 16:56:00, etc. |

**Consecuencia:** el lector conserva una sola B mientras A se extiende, pero
reinicia su medida. Es coherente con v2.18; el “reinicio” de B es una decisión
de implementación, no una regla literal.

---

## P05 — TT_TICK (H5)

| Campo | Valor |
|---|---|
| POLICY_ID | P05 |
| Versión | FASE_A_v1 |
| Hash anterior | `NO_ARCHIVADO` |
| Hash posterior | `54539364…` |
| Problema observado | R5 evaluaba el TT al cerrar un movimiento y perdía confirmaciones. |
| Regla del árbol | 4.8: TT se confirma en el primer tick que alcanza el objetivo. |
| Resultado anterior | TT sólo al cierre. |
| Resultado posterior | TT evaluado en cada tick. |
| Ticks afectados | 6 TT confirmados; 5 después del AUT de su generación. |
| Estado | **TREE_SUPPORTED** |
| Evidencia | Gen 14 (16:54:29.847), 15 (16:56:32.746), 16 (17:01:11.951), 21 (17:13:19.308), 26 (17:28:42.077). |

---

## P06 — TT_SURVIVES_AUT (H6)

| Campo | Valor |
|---|---|
| POLICY_ID | P06 |
| Versión | FASE_A_v1 |
| Hash anterior | `NO_ARCHIVADO` |
| Hash posterior | `54539364…` |
| Problema observado | El TT de una generación se perdía al abrir la siguiente. |
| Regla del árbol | 4.8 y 4.9: el TT es patrón concurrente; puede extenderse. |
| Resultado anterior | TT archivado al cerrar la generación. |
| Resultado posterior | TT conservado como `POSSIBLE`/`EXTENDED` y evaluado después. |
| Ticks afectados | Gen 14, 15, 16, 21, 26 (confirmaciones post-AUT). |
| Estado | **EXPERIMENTAL_ASSUMPTION** |
| Evidencia | `TT_CONFIRMED` con `gen=14` en 16:54:29, `gen=15` en 16:56:32, `gen=16` en 17:01:11. |

**Consecuencia:** cinco de seis TT se confirman después de que su generación
haya terminado. Es una lectura concurrente; el árbol no fija cuánto sobrevive
un TT. Queda para Fase B.

---

## P07 — GAP_SKETCH (H7)

| Campo | Valor |
|---|---|
| POLICY_ID | P07 |
| Versión | FASE_A_v1 |
| Hash anterior | `NO_ARCHIVADO` |
| Hash posterior | `54539364…` |
| Problema observado | v2.19 exige A/B/A implícitas en el gap; el lector no las desarrolla. |
| Regla del árbol | v2.19, 4.6: no inventar ticks; nuevo 1 desde la apertura. |
| Resultado anterior | Gap no registrado. |
| Resultado posterior | `GAP_SIGNIFICANT_UNDEFINED` + esbozo `SKETCH_ONLY`; sin extremos internos. |
| Ticks afectados | 14 aperturas no planas; 9 con gap ≥ 1,00. |
| Estado | **OPEN_RULE_DEPENDENCY** |
| Evidencia | Gen 12 (−3,10), 14 (−1,40), 15 (−3,50), 16 (−1,20), 17 (+2,10), 18 (−3,00), 19 (−2,30), 20 (−1,10), 21 (+1,90). |

**Consecuencia:** el tramo del gap queda sin resolución funcional completa. Es
una carencia del instrumento, no una decisión del árbol.

---

## P08 — NEW_ONE_NEXT_BAR (E-ORIG)

| Campo | Valor |
|---|---|
| POLICY_ID | P08 |
| Versión | FASE_A_v1 |
| Hash anterior | `NO_ARCHIVADO` |
| Hash posterior | `54539364…` |
| Problema observado | Después de AUT/C_TREND/A_TREND, el lector espera la vela siguiente para abrir el 1. |
| Regla del árbol | 4.5: AUT confirma **inmediatamente** el nuevo 1; v2.17/v2.18: el movimiento de la transición se convierte en nuevo 1. |
| Resultado anterior | El nuevo 1 nacía en el tick de la transición. |
| Resultado posterior | El nuevo 1 nace en la apertura de la vela siguiente; el resto de la vela de transición queda sin 1. |
| Ticks afectados | 15 transiciones; **551,515 s = 9,19 min = 22,4 %** del bloque sin 1 generacional. |
| Estado | **EXPERIMENTAL_ASSUMPTION** (en conflicto con 4.5) |
| Evidencia | 16:50:32.234 → 16:51:00.099; 16:52:17.291 → 16:53:00.189; 17:07:02.847 → 17:08:00.199; etc. |

**Consecuencia:** es la causa del segundo error, E-ORIG. Las 16 generaciones
tienen su origen en el extremo de la vela siguiente, no en el extremo de la
transición. Afecta incluso a las 5 candidatas principales.

---

## P09 — MODULE_FARTHEST

| Campo | Valor |
|---|---|
| POLICY_ID | P09 |
| Versión | FASE_A_v1 |
| Hash anterior | `NO_ARCHIVADO` |
| Hash posterior | `54539364…` |
| Problema observado | Un 2 que retrocede encogía el módulo (17:22: 30,8 en vez de 44,7). |
| Regla del árbol | 4.2; el módulo se mide por extremos estructurales, no por rangos brutos ni por el último extremo de 2. |
| Resultado anterior | Módulo = extremo de 2: 30,8. |
| Resultado posterior | Módulo = extremo más lejano de 1/2: 44,7. |
| Ticks afectados | Gen 14, 15, 20, 21, 23, 25, 26. |
| Estado | **TREE_SUPPORTED** |
| Evidencia | 17:22: 1 high 29678,3 (seq 18304), 2 high 29664,4 (seq 18394); 44,7. |

**Consecuencia:** correcto. La medida 30,8 no es un módulo: es la distancia al
extremo de un 2 fallido. Se documenta en `PHASE_A_EXTREME_OWNERSHIP.csv`.

---

## P10 — C_ABSORPTION

| Campo | Valor |
|---|---|
| POLICY_ID | P10 |
| Versión | FASE_A_v1 |
| Hash anterior | `NO_ARCHIVADO` |
| Hash posterior | `54539364…` |
| Problema observado | C rompía su origen y el lector la seguía como C. |
| Regla del árbol | No explícita; el ciclo de vida de C. |
| Resultado anterior | C continuaba tras romper su origen. |
| Resultado posterior | `C_ABSORBED`; C se anula y B se reanuda. |
| Ticks afectados | 11 eventos `C_ABSORBED`. |
| Estado | **EXPERIMENTAL_ASSUMPTION** |
| Evidencia | Gen 12 (16:50:07.968, 16:50:17.595), 13 (16:52:16.490), 14 (16:54:22.226, 16:54:26.436), etc. |

---

## P11 — C_TREND_BASE

| Campo | Valor |
|---|---|
| POLICY_ID | P11 |
| Versión | FASE_A_v1 |
| Hash anterior | `NO_ARCHIVADO` |
| Hash posterior | `54539364…` |
| Problema observado | C usada como tendencia se dispara contra la base del módulo o contra el final de A. |
| Regla del árbol | v2.17: base del módulo; v1.2/CUT: final de A. |
| Resultado anterior | C_TREND contra el final de A. |
| Resultado posterior | CUT contra el final de A; C_TREND contra la base del módulo. |
| Ticks afectados | Gen 12: CUT 16:50:24.206, C_TREND 16:50:32.234 (margen 0,30). Gen 18: CUT 17:05:41.048, C_TREND 17:07:02.847 (margen 2,00). |
| Estado | **OPEN_RULE_DEPENDENCY** |
| Evidencia | `CUT` y `C_USED_AS_TREND` en el mismo C, con referencias distintas. |

---

## P12 — TT_FAIL_BASE

| Campo | Valor |
|---|---|
| POLICY_ID | P12 |
| Versión | FASE_A_v1 |
| Hash anterior | `NO_ARCHIVADO` |
| Hash posterior | `54539364…` |
| Problema observado | El árbol no fija cuándo falla un TT. |
| Regla del árbol | 4.8 no define la condición de fallo. |
| Resultado anterior | TT quedaba `POSSIBLE` indefinidamente. |
| Resultado posterior | TT falla si el precio retorna a la base del módulo antes del objetivo. |
| Ticks afectados | 9 TT `FAILED`. |
| Estado | **EXPERIMENTAL_ASSUMPTION** |
| Evidencia | Gen 12, 13, 17, 18, 19, 20, 22, 23, 25. |

---

## P13 — ONE_DIRECTION_BAR (E-DIR)

| Campo | Valor |
|---|---|
| POLICY_ID | P13 |
| Versión | FASE_A_v1 |
| Hash anterior | `NO_ARCHIVADO` |
| Hash posterior | `54539364…` |
| Problema observado | El 1 se orienta por `close − open`, no por la transición que lo creó. |
| Regla del árbol | v2.17: C → nuevo 1 en su propia dirección; v2.18: A usada como tendencia → nuevo 1. |
| Resultado anterior | El 1 se orientaba por la transición (`origin_reason`). |
| Resultado posterior | El 1 se orienta por la vela; `origin_reason` no se usa. |
| Ticks afectados | 16 generaciones; **10 inversiones**. |
| Estado | **EXPERIMENTAL_ASSUMPTION** (en conflicto con v2.17) |
| Evidencia | Gen 12: C_TREND −1, 1 +1. Gen 18: A_TREND −1, 1 +1. Gen 19: C_TREND −1, 1 +1. |

**Consecuencia:** es la causa del primer error, E-DIR. En 10 de 16 casos el 1
es el movimiento contrario (A) del nuevo 1 del padre.

---

## P14 — THREE_STRICT_EXTREME

| Campo | Valor |
|---|---|
| POLICY_ID | P14 |
| Versión | FASE_A_v1 |
| Hash anterior | `NO_ARCHIVADO` |
| Hash posterior | `54539364…` |
| Problema observado | 3 nunca se confirmaba porque el extremo de 2 se actualizaba antes de comprobar la superación estricta. |
| Regla del árbol | 4.3: recuperar la dirección de 2 y superar estrictamente su extremo. |
| Resultado anterior | 3 imposible por orden de actualización. |
| Resultado posterior | Se comprueba la superación antes de actualizar 2. |
| Ticks afectados | 0 módulos regulares en el bloque; warm-up 16:21. |
| Estado | **TREE_SUPPORTED** |
| Evidencia | Warm-up 16:19–16:21; bloque sin 1-2-3. |

---

## P15 — A_TREND_FIRST_TICK

| Campo | Valor |
|---|---|
| POLICY_ID | P15 |
| Versión | FASE_A_v1 |
| Hash anterior | `NO_ARCHIVADO` |
| Hash posterior | `54539364…` |
| Problema observado | A podía crecer indefinidamente (175 puntos) sin transición. |
| Regla del árbol | v2.18: A usada como tendencia; v2.16: sin umbral universal. |
| Resultado anterior | A se extendía sin límite. |
| Resultado posterior | A_TREND en el primer tick que supera la base; A se congela en ese tick. |
| Ticks afectados | Gen 17 (margen 0,40), gen 20 (1,30), gen 22 (0,50), gen 25 (1,50). |
| Estado | **EXPERIMENTAL_ASSUMPTION** |
| Evidencia | Gen 17: A 29623,2 → el precio sigue a 29617,6 (5,6 más). Gen 25: A 29632,1 → el precio sigue a 29611,9 (20,2 más). |

**Consecuencia:** la transición es formalmente válida (A > base), pero el
extremo real de A sigue después. El nuevo 1 nace antes del extremo real. Es la
materia de Q_A_MARGIN.

---

## P16 — A_ABSORBS_MODULE_EXTREME

| Campo | Valor |
|---|---|
| POLICY_ID | P16 |
| Versión | FASE_A_v1 |
| Hash anterior | `NO_ARCHIVADO` |
| Hash posterior | `54539364…` |
| Problema observado | Un nuevo extremo del módulo mientras A/B estaban abiertos perdía el mínimo/máximo de 16:21. |
| Regla del árbol | v2.16: el retroceso posterior a AUT/nuevo 1 no se clasifica automáticamente como A Grande. |
| Resultado anterior | A/B conservaban referencias antiguas; el extremo se perdía. |
| Resultado posterior | `MODULE_EXTENDED`; A se reinicia y B se recalcula. |
| Ticks afectados | Gen 14 (16:54:01), 15 (16:56:00), 20 (17:11:01), 21 (17:13:00), 26 (17:27:00). |
| Estado | **EXPERIMENTAL_ASSUMPTION** |
| Evidencia | `MODULE_EXTENDED` con “A se reinicia”. |

---

## P17 — C_GRANDE_NOT_IMPLEMENTED

| Campo | Valor |
|---|---|
| POLICY_ID | P17 |
| Versión | FASE_A_v1 |
| Hash anterior | `NO_ARCHIVADO` |
| Hash posterior | `54539364…` |
| Problema observado | C nunca se confirma como C Grande al 100 % de A. |
| Regla del árbol | 4.4: después de B Grande, el movimiento contrario es C Grande. |
| Resultado anterior | C sólo candidata. |
| Resultado posterior | Sigue sólo candidata; `CUT` y `C_TREND` son transiciones, no un estado C Grande. |
| Ticks afectados | Gen 12 (C = 34,7 > A = 16,2); gen 18 (C = 61,5 > A = 33,4). |
| Estado | **OPEN_RULE_DEPENDENCY / estado ausente** |
| Evidencia | No existe evento `C_GRANDE` en el bloque. |

**Consecuencia:** no es una política, es un hueco de ontología. Q_C_GRANDE lo
cubre.

---

## 1. CRONOLOGÍA DE CAMBIOS DEL LECTOR

| # | Cambio | Problema que corrigió | Política | Estado |
|---:|---|---|---|---|
| 1 | Comprobar 3 antes de actualizar el extremo de 2 | 3 nunca confirmaba | P14 | TREE_SUPPORTED |
| 2 | Reiniciar la lectura tras AUT como nueva generación | El AUT reseteaba a un 1 de vela sin continuidad | P08 | EXPERIMENTAL |
| 3 | Absorber A/B ante un nuevo extremo del módulo | Se perdía el mínimo de 16:21 | P16 | EXPERIMENTAL |
| 4 | Invalidar C al romper su origen | C seguía tras romper su origen | P10 | EXPERIMENTAL |
| 5 | Módulo sin 2 = extremo de 1, no apertura siguiente | El módulo se medía desde la apertura equivocada | P09 | TREE_SUPPORTED |
| 6 | A usada como tendencia al superar la base | A crecía 175 puntos sin transición | P15 | EXPERIMENTAL |
| 7 | Módulo por descarte = extremo más lejano de 1/2 | 17:22 medía 30,8 en vez de 44,7 | P09 | TREE_SUPPORTED |
| 8 | Conservar TT por generación | El TT se perdía al abrir la siguiente | P06 | EXPERIMENTAL |

**Hashes:** no se conservaron snapshots por cambio. El hash actual es
`54539364…`; los anteriores son `NO_ARCHIVADO`. Para la Fase B, cada política
debe tener su copia inmutable y su hash antes/después.

---

## 2. EFECTO SOBRE LAS 16 GENERACIONES

| Política | Generaciones afectadas | Efecto observable |
|---|---|---|
| P01 | 16/16 | 1 = rango de vela; gen 12 invierte la dirección |
| P02 | 16/16 | A se confirma a 6,00; sensibilidad 9–16 generaciones |
| P08 | 16/16 | 22,4 % del tiempo sin 1; origen en la vela siguiente |
| P13 | 10/16 | Inversiones de dirección |
| P09 | 7/16 | Módulo por extremo más lejano |
| P15 | 4/16 | A_TREND con margen 0,40–1,50 |
| P16 | 5/16 | A se reinicia por nuevo extremo |
| P10 | 7/16 | C absorbida |
| P06 | 5/16 | TT confirmado después del AUT |
| P17 | 2/16 | C Grande ausente |

---

## 3. CLASIFICACIÓN FINAL

```text
TREE_SUPPORTED ............ P05, P09, P14
EXPERIMENTAL_ASSUMPTION ... P01, P02, P03, P04, P06, P08, P10, P12, P13, P15, P16
OPEN_RULE_DEPENDENCY ...... P07, P11, P17
```

Ninguna política `EXPERIMENTAL_ASSUMPTION` puede usarse para validar el árbol
ni para congelarlo. P01, P08 y P13 son las que sostienen la lectura de 16
generaciones; mientras no se corrijan, esa lectura es una hipótesis de trabajo,
no una salida canónica.
