# TM — CHECKPOINT 3
## Corrección de propiedad de estados, invalidación de 3 y relectura completa

**Fecha:** 2026-10-30
**Lector:** `blind_reader_v3_owned_states.py`
**SHA-256 lector:** `AE559A31AAB3222A6F04029999102DCA6347D83201F2009888557CED60C1029F`
**Estado:** `STATE_OWNERSHIP_CORRECTED` · `GENERATIONS_NOT_APPROVED` · `TREE_NOT_FROZEN`
**Originales:** árbol `94A1408A…`, tickfeed `5F701BE2…`, v005 `F5D7550C…`: intactos. `originals_modified=false`, `engine_modified=false`, `goldens_modified=false`.

---

## 1. HALLAZGO Y CORRECCIÓN

La traza v2 permitía:

```text
TWO_IMPOSSIBLE
→ MODULE_BY_DISCARD
→ THREE_EXTENDED
→ THREE_EXTENDED_ABSORBS_AB
```

Eso viola el invariante **3 exige 2 confirmado**. La causa estaba en tres puntos:

1. `module_by_discard` no invalidaba el 3 ni limpiaba `three_extreme`.
2. `on_a_tick` y `on_b_tick` extendían 3 sin comprobar `three_legal`.
3. El nuevo 1 de AUT_B heredaba `a_extreme_st` en lugar del origen estructural de B.

v3 aplica:

- `three_legal = True` solo desde `module_1_2_3`, con 2 CONFIRMED;
- al pasar a módulo por descarte o módulo 1+2: `three_status=IMPOSSIBLE`, `three_extreme=0`, `three_kt=0`, `three_invalidation=TWO_*`, `three_legal=False`;
- extensión de 3 solo si `three_legal`; si no, el módulo extiende y A vuelve a `CONTRARY_MOVE_PENDING`;
- B Grande tiene precedencia sobre la extensión del módulo; una vez Grande, B no falla: el contrario es C;
- el nuevo 1 de AUT_B usa `b_origin` y `b_st`;
- cada referencia tiene `reading_id`, `branch_id`, `refs_owner`, `three_owner`, `mod_owner_reading`, `mod_owner_generation`.

Además, Q2 se corrige en el estado: **A candidata no congela 3**. Un retroceso de 2 puntos abre `A_CANDIDATE_AFTER_3`, pero el 3 sigue siendo dueño de su extremo; si el precio hace un nuevo extremo de 3, el 3 se extiende y A vuelve a pending. El 3 se congela solo cuando A se confirma o se usa como tendencia.

---

## 2. EJECUCIÓN

| Bloques | Ticks | Generaciones | Invalid | 3 sin 2 |
|---|---:|---:|---:|---:|
| 16:15–16:24 | 2.297 | 6 | 0 | 0 |
| 16:25–16:48 | 4.777 | 21 | 0 | 0 |
| 16:49–17:29 | 13.261 | 24 | 0 | 0 |
| **Feed completo** | **20.335** | **51** | **0** | **0** |
| L2 16:19–16:24 | 1.360 | 4 | 0 | 0 |

Los segmentos son ejecuciones de estado fresco, no continuaciones del feed completo; sus conteos no son aditivos. La cadena autorizada es la del feed completo.

Feed completo:

```text
AUT_B             20
A_USED_AS_TREND   18
C_USED_AS_TREND    3
GAP                9
OPEN               1
TOTAL             51
```

Determinismo:

- doble ejecución: 20.335 líneas idénticas, SHA-256 `23800D07EB356CF3…7B93`;
- prefijos 16:30, 17:00, 17:15: 3.829, 12.265 y 16.454 líneas, coincidencia línea a línea;
- evidencia: `06_REGRESSION/PHASE_3_DETERMINISM.json`.

---

## 3. AUDITORÍA DE PROPIEDAD

`06_REGRESSION/PHASE_3_GENERATION_AUDIT.csv` contiene las 55 filas (51 L1 + 4 L2) con:

`two_confirmed`, `three_legal`, `three_owner`, `mod_owner`, `mod_owner_reading`, `invalidation_reason`, `inherited_refs`, `next_function`, `classification`, `errors`.

Resultado:

```text
INVALID_THREE_WITHOUT_CONFIRMED_TWO   0
CROSS_READING_REFERENCE_LEAK          0
CROSS_GENERATION_REFERENCE_LEAK       0
STALE_FUNCTION_STATE                  0
INVALID_MODULE_EXTENSION              0
INVALID_ABSORPTION                    0
INVALID_NEW_ONE_ORIGIN                0
ERRORES TOTALES                       0
```

Clasificación:

| Capa | Clase | Filas |
|---|---|---:|
| L1 | `VALID_PRIMARY` | 41 |
| L1 | `INTEGRATED_IN_LARGER_MODULE` (gap) | 9 |
| L1 | `VALID_PRIMARY_PENDING` | 1 |
| L2 | `VALID_PRIMARY` única | 2 |
| L2 | `INTEGRATED_IN_LARGER_MODULE` (duplicado de L1) | 2 |

**Generaciones únicas: 53** = 51 L1 + 2 L2. Las otras 2 L2 coinciden estructuralmente con L1.

Las 51 no se aprueban. Que sean legalmente posibles no significa que sean semánticamente primarias. La clasificación `VALID_PRIMARY` es provisional y no autoriza congelación.

---

## 4. Q-B3 — CERRADA COMO ERROR DEL LECTOR

El 3 de 16:23 en v2 pertenecía a una generación con **2 IMPOSIBLE**. No era un 3 legal y no competía con B Grande. v3 lo invalida.

Lectura legal de 16:23 en L2:

```text
1 up: 29830.3 → 29850.8 (20.5)
2: IMPOSIBLE (gap de 3.0)
3: IMPOSIBLE
módulo por descarte: 29830.3 → 29852.6 = 22.3
A: 29852.6 → 29842.8 = 8.0
B: 29842.8 → 29852.6 = 9.8 = 122.5 % de A  → B GRANDE
C: 29852.6 → 29829.9 = 22.7            → C_GRANDE
C supera la base del módulo 29830.3     → C_USED_AS_TREND
nuevo 1 bajista en 16:24:44.788, origen 29852.6
```

Coincide con la ruta A del protocolo: **solo queda B Grande → C**. No hay competencia en la misma lectura. Q-B3 no se formula como pregunta experta.

---

## 5. PRIMERA DIVERGENCIA REAL: 16:20, AUTONOMÍA DE A

El 3 legal de L2 se confirma en 29833.3 (extremo final 29833.3, módulo 16.7). El v005 lee 29830.3, módulo 19.7, A 20.5.

Secuencia v3:

```text
3:        29850.0 → 29833.3 (16.7)
A:        29833.3 → 29837.4 = 4.1
B:        29837.4 → 29832.5 = 4.9  → B_GRANDE (119.5 %)
B:        29832.5 → 29830.3 = 6.4  → AUT_B (156 % de A)
nuevo 1:  29837.4 → 29830.3
```

La diferencia no es de propiedad: el 3 es legal y su extremo se actualiza. El problema es que un A de 4.1 y un B de 4.9 confirman A y B Grande antes de que el 3 alcance 29830.3. El v005 absorbe ese ciclo como vibración interna. Esto es **Q-AUT**, no un error de estados.

Consecuencia: el módulo local 19.7 / A 20.5 no se reproduce en una sola generación. La lectura v3 lo reparte en dos generaciones (3 16.7 + nuevo 1 7.1). No se corrige con un umbral provisional.

---

## 6. PREGUNTAS RESTANTES

### Q-AUT — autonomía de A con recorridos pequeños

**MOVIMIENTO**
Estábamos en el 3 legal 29850.0 → 29833.3 (módulo 16.7). El precio subió 4.1 (A) y bajó 4.9 (B = 119.5 % de A), luego 6.4 (156 % de A). El lector confirma A y B Grande; el v005 sigue el 3 hasta 29830.3 (módulo 19.7) y lee A 20.5.

**PREGUNTA**
¿A se confirma con un B que alcanza el 100 % de A aunque A sea un recorrido pequeño, o requiere autonomía funcional (posición, continuidad, independencia, finalidad) antes de confirmarse?

**SI se confirma con B = 100 %**
Se mantienen las 51 generaciones; el 3 se congela en 29833.3; el ciclo A/B de 4–6 puntos produce transiciones.

**SI requiere autonomía funcional**
El 3 sigue hasta 29830.3; el módulo es 19.7; A es 20.5; desaparecen las transiciones de 4–6 puntos y el conteo baja.

**CASOS DESBLOQUEADOS**
16:20–16:22, el módulo local 19.7, las 51 generaciones y la clasificación primaria/secundaria.

### Q-3-50 — 50 % exacto de 2

¿Tocar exactamente el 50 % de 2 conserva la posibilidad de 3 o la invalida? v3 la admite (`FIFTY_PERCENT_EXACT`, `retr_valid` si el retroceso ≥ 2 puntos); el árbol no lo cierra. Afecta a la matriz de 3 y al módulo regular.

Q-INIT —primer 1 del feed— sigue abierta, no preguntada. Q-B3 cerrada.

---

## 7. RECOMENDACIÓN

```text
NEEDS_EXPERT_DECISION
```

La propiedad de estados está corregida y auditada con 0 errores. No se aprueban las 51 generaciones ni se congela el árbol. Q-AUT decide si las transiciones de 4–6 puntos son estructura o fragmentación; Q-3-50 decide la frontera de 3. Sin esas dos respuestas, el conteo y la matriz de pruebas no son canónicos.

Si Javier responde Q-AUT y Q-3-50:

1. incorporar a v2.20;
2. reejecutar el feed completo;
3. auditar las generaciones resultantes;
4. comparar L1/L2;
5. preparar la matriz de pruebas.

---

## 8. LIMITACIONES

- Los segmentos 16:25–16:48 y 16:49–17:29 arrancan con estado INITIAL; no son continuaciones y no deben sumarse.
- L2 es una ejecución separada con `reading_id=L2`; no comparte estado con L1. Es la separación más estricta, no una co-simulación.
- La auditoría verifica propiedad, no validez semántica de cada transición.
- 51 generaciones no equivalen a 51 primarias: 41 primarias provisionales, 9 integradas por gap y 1 abierta.
- La diferencia 16:20 es Q-AUT, no un error de propiedad.
