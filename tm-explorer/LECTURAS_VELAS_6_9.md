# LECTURAS VELAS 6–9 — USTEC 2026-10-16 (sesión 16:30)

- **Agente:** MOVEMENT_RECONSTRUCTOR (reconstrucción de ticks, sin golden, sin precios esperados)
- **Fuente:** `data/ticks_USTEC_2026-10-16_16-30.csv` (delimitador `;`, 5.658 ticks, `bar_index` 1–20)
- **Serie de precio oficial:** **Bid**
- **Anclas confirmadas (no inventadas):** módulo principal min `29760,30` / max `29838,20` / rango `77,90`; `a_grande_final 29820,80`; TT bajista `29742,90`; vela 6 min `29717,60`; vela 7 min `29712,40 @16:36:02.112` → max `29738,40 @16:36:34.774`; vela 8 max `29744,40 @16:37:10.254` → min `29683,20 @16:37:59.175` (cierre `29689,10`).
- **Reglas aplicadas:** AUT = SUPERAR `127 % + 0,25` (1 tick), no tocar; B Grande candidata = movimiento contrario a A Grande, confirmada al 100 %.
- **Anti-spoiler:** no se usa el golden; **no** se concluye C Grande ni CUT; **no** se mueve ningún evento de vela.

---

## PARTE A — CRONOLOGÍA REAL de las velas 6, 7, 8 y 9

| Vela | Apertura (1.º bid) | Cierre (último bid) | Máximo | Mínimo | Orden temporal de extremos |
|---|---|---|---|---|---|
| **6** | `29766,40` @16:35:00.160 (msc 1792168500160) | `29720,70` @16:35:59.907 (msc 1792168559907) | `29780,30` @16:35:16.001 (msc 1792168516001) | `29717,60` @16:35:57.701 (msc 1792168557701) | **MAX (16:35:16.001) → MIN (16:35:57.701)** |
| **7** | `29719,10` @16:36:00.107 (msc 1792168560107) | `29735,70` @16:36:59.837 (msc 1792168619837) | `29738,40` @16:36:34.774 (msc 1792168594774) | `29712,40` @16:36:02.112 (msc 1792168562112) | **MIN (16:36:02.112) → MAX (16:36:34.774)** |
| **8** | `29734,80` @16:37:00.038 (msc 1792168620038) | `29689,10` @16:37:59.977 (msc 1792168679977) | `29744,40` @16:37:10.254 (msc 1792168630254) | `29683,20` @16:37:59.175 (msc 1792168679175) | **MAX (16:37:10.254) → MIN (16:37:59.175)** |
| **9** | `29688,30` @16:38:00.178 (msc 1792168680178) | `29678,40` @16:38:59.914 (msc 1792168739914) | `29701,10` @16:38:25.030 (msc 1792168705030) | `29670,90` @16:38:53.502 (msc 1792168733502) | **MAX (16:38:25.030) → MIN (16:38:53.502)** |

Hechos de frontera (verificados): en 6→7, 7→8 y 8→9 el movimiento cruza la frontera de vela y **crea nuevo extremo** (6→7 nuevo mín. 29712,40; 7→8 nuevo máx. 29744,40; 8→9 nuevo mín. 29674,60 @16:38:07.993). El cambio de vela **no** interrumpe el movimiento.

---

## PARTE B — LECTURAS VÁLIDAS

### LECTURA 1 — lectura del módulo principal (R-A)

- **Movimiento anterior:** módulo formado por las velas 1 y 2 (movimiento previo contrario a A Grande).
- **Módulo usado:** velas 1+2, min `29760,30`, max `29838,20`, **rango 77,90**.
- **Dirección del módulo:** bajista.
- **Inicio de A Grande:** `29760,30` @16:31:33.648 (msc 1792168293648), mínimo del módulo (vela 2).
- **Extremos de A Grande en orden temporal:** mínimo `29760,30` @16:31:33.648 (bar2) → máximo `29820,80` @16:32:38.002 (msc 1792168358002, bar3). **MIN primero → MAX después.** (A Grande = movimiento contrario al módulo = alcista; tamaño = `29820,80 − 29760,30` = **60,50**).
- **Inicio de B Grande candidata:** `29820,80` @16:32:38.002 (msc 1792168358002, bar3).
- **Nivel del 100 %:** `29760,30` (= `29820,80 − 60,50`).
- **Nivel del 127 %:** `29743,965` (= `29820,80 − 1,27·60,50`).
- **Nivel del 127 % + 0,25:** `29743,715` (= `29743,965 − 0,25`).
- **Máximo o mínimo alcanzado por B Grande:** mínimo del tramo bajista desde `29820,80` = `29651,20` @16:42:09.361 (msc 1792168929361, bar13); dentro de las velas 6–9 el mínimo del tramo es `29670,90` @16:38:53.502 (bar9). (El fin de B Grande no está cerrado → se reporta el mínimo del descenso observado.)
- **¿Superó AUT?:** **SÍ** (`29742,80 < 29743,715`).
- **Movimiento contrario posterior:** ascenso desde `29712,40` (bar7 min) hasta `29738,40` @16:36:34.774 (bar7 max) y después `29744,40` @16:37:10.254 (bar8 max).
- **¿B Grande creó después otro extremo?:** **SÍ** (nuevos mínimos sucesivos tras el AUT y tras los rebotes: `29712,40` bar7, `29683,20` bar8, `29674,60`/`29670,90` bar9, hasta `29651,20` bar13).
- **Cálculo / módulo (una línea):** tomé como módulo las **velas 1+2** (rango 77,90) porque son el 1 y 2 cuyo 3 falló y por descarte forman el módulo; el movimiento contrario alcista `29760,30 → 29820,80` es A Grande y su contrario bajista desde `29820,80` es B Grande candidata.

### LECTURA 2 — lectura desde el mínimo de la vela 7 (R-D)

- **Movimiento anterior:** tramo bajista de la LECTURA 1 (desde `29820,80` hasta `29712,40`), movimiento previo / contrario al ascenso siguiente.
- **Módulo usado:** **no reconstruible por hechos** (tras AUT/TT de la LECTURA 1 no hay un 1–2 determinable por ticks; pendiente regla de referencia del ciclo posterior).
- **Dirección del módulo:** no determinable.
- **Inicio de A Grande:** `29712,40` @16:36:02.112 (msc 1792168562112), mínimo de la vela 7.
- **Extremos de A Grande en orden temporal:** mínimo `29712,40` @16:36:02.112 (bar7) → máximo `29744,40` @16:37:10.254 (msc 1792168630254, bar8). **MIN primero → MAX después.** (Tamaño = `29744,40 − 29712,40` = **32,00**; cruza la frontera de vela 7→8 sin interrupción.)
- **Inicio de B Grande candidata:** `29744,40` @16:37:10.254 (msc 1792168630254, bar8).
- **Nivel del 100 %:** `29712,40` (= `29744,40 − 32,00`).
- **Nivel del 127 %:** `29703,76` (= `29744,40 − 1,27·32,00`).
- **Nivel del 127 % + 0,25:** `29703,51` (= `29703,76 − 0,25`).
- **Máximo o mínimo alcanzado por B Grande:** mínimo del tramo bajista desde `29744,40` = `29651,20` @16:42:09.361 (bar13); dentro de la vela 8 = `29683,20` @16:37:59.175 (msc 1792168679175); en la vela 9 = `29670,90` @16:38:53.502.
- **¿Superó AUT?:** **SÍ** (`29702,80 < 29703,51`).
- **Movimiento contrario posterior:** contrarios alcistas dentro de la vela 8 — `29730,10 @16:37:18.678`, `29731,60 @16:37:22.085`, `29729,10 @16:37:23.687`, `29733,10 @16:37:26.090` (el mayor), `29719,30`, `29718,60`, `29715,30` — y en la vela 9 `29701,10 @16:38:25.030` y `29698,90 @16:38:16.212`. Todos seguidos de un nuevo mínimo.
- **¿B Grande creó después otro extremo?:** **SÍ** (cada contrario alcista quedó seguido de un nuevo mínimo: `29712,30`, `29704,20`, `29702,80`, `29683,20`, `29670,90`…).
- **Cálculo / módulo (una línea):** tomé como A Grande el ascenso `29712,40 (mín. vela 7) → 29744,40 (máx. vela 8)` porque es el movimiento contrario al descenso previo y su tamaño (32,00) define los niveles de su B Grande; no hay módulo reconstruible asociado por hechos.

### LECTURA 3 — variante por inicio alternativo de A Grande (ambigüedad no cerrada)

- **Movimiento anterior:** el mismo descenso previo de la LECTURA 1 (desde `29820,80`).
- **Módulo usado:** **no reconstruible por hechos** (igual que LECTURA 2).
- **Dirección del módulo:** no determinable.
- **Inicio de A Grande:** `29717,60` @16:35:57.701 (msc 1792168557701), mínimo de la vela 6.
- **Extremos de A Grande en orden temporal:** mínimo `29717,60` @16:35:57.701 (bar6) → máximo `29744,40` @16:37:10.254 (msc 1792168630254, bar8). **MIN primero → MAX después.** (Tamaño = `29744,40 − 29717,60` = **26,80**.)
- **Inicio de B Grande candidata:** `29744,40` @16:37:10.254 (msc 1792168630254, bar8).
- **Nivel del 100 %:** `29717,60` (= `29744,40 − 26,80`).
- **Nivel del 127 %:** `29710,364` (= `29744,40 − 1,27·26,80`).
- **Nivel del 127 % + 0,25:** `29710,114` (= `29710,364 − 0,25`).
- **Máximo o mínimo alcanzado por B Grande:** mínimo del tramo bajista desde `29744,40` = `29651,20` @16:42:09.361 (bar13); dentro de la vela 8 = `29683,20` @16:37:59.175.
- **¿Superó AUT?:** **SÍ** (`29708,70 < 29710,114`).
- **Movimiento contrario posterior:** los mismos contrarios alcistas de la vela 8 y 9 (ver LECTURA 2).
- **¿B Grande creó después otro extremo?:** **SÍ**.
- **Cálculo / módulo (una línea):** es la misma A Grande de la LECTURA 2 tomada con el **otro inicio candidato** (`29717,60`, mín. vela 6, tamaño 26,80) porque el inicio de A Grande **no está fijado** por hechos (bloqueo 3 de `CRONOLOGIA_MOVIMIENTOS.md`); cambia el nivel del 100 % (29717,60) y el AUT (29710,114).

---

## PARTE C — TICK EXACTO DE CADA NIVEL DE B GRANDE (100 %, 127 %, 127 % + 0,25)

Formato: primer tick que **iguala** (bid = nivel) y primer tick que **supera** estrictamente (bid < nivel, bajista). Si no hay igualdad exacta se indica `—` (el nivel no cae en la malla de 0,1).

### LECTURA 1 (B Grande desde 29820,80; tamaño 60,50)

| Nivel | Valor | Primer tick que IGUALA | Primer tick que SUPERA | ¿Solo toca y no supera? |
|---|---|---|---|---|
| 100 % | `29760,30` | — (nunca; tick previo 29762,40 @16:35:32.846) | `29758,30` @16:35:33.046, msc 1792168533046, bar6 | **NO** (supera) |
| 127 % | `29743,965` | — (nunca) | `29742,80` @16:35:35.448, msc 1792168535448, bar6 | **NO** (supera) |
| 127 % + 0,25 | `29743,715` | — (nunca) | `29742,80` @16:35:35.448, msc 1792168535448, bar6 | **NO** (supera; AUT en el mismo tick) |

### LECTURA 2 (B Grande desde 29744,40; tamaño 32,00)

| Nivel | Valor | Primer tick que IGUALA | Primer tick que SUPERA | ¿Solo toca y no supera? |
|---|---|---|---|---|
| 100 % | `29712,40` | — (nunca; tick previo 29716,20 @16:37:35.109) | `29712,30` @16:37:35.310, msc 1792168655310, bar8 | **NO** (supera) |
| 127 % | `29703,76` | — (nunca) | `29702,80` @16:37:55.363, msc 1792168675363, bar8 | **NO** (supera) |
| 127 % + 0,25 | `29703,51` | — (nunca) | `29702,80` @16:37:55.363, msc 1792168675363, bar8 | **NO** (supera; AUT en el mismo tick) |

### LECTURA 3 (B Grande desde 29744,40; tamaño 26,80)

| Nivel | Valor | Primer tick que IGUALA | Primer tick que SUPERA | ¿Solo toca y no supera? |
|---|---|---|---|---|
| 100 % | `29717,60` | `29717,60` @16:37:17.875, msc 1792168637875, bar8 (repite en `29717,60` @16:37:32.906) | `29717,30` @16:37:33.707, msc 1792168653707, bar8 | **NO** (toca y luego supera) |
| 127 % | `29710,364` | — (nunca) | `29708,70` @16:37:40.718, msc 1792168660718, bar8 | **NO** (supera) |
| 127 % + 0,25 | `29710,114` | — (nunca) | `29708,70` @16:37:40.718, msc 1792168660718, bar8 | **NO** (supera; AUT en el mismo tick) |

**Resumen Parte C:** ningún nivel queda en «solo se toca y no se supera». El único contacto exacto es el 100 % de la LECTURA 3 (`29717,60` @16:37:17.875), y va seguido de superación (`29717,30` @16:37:33.707). En las tres lecturas, `127 % + 0,25` se **supera** en el mismo tick que `127 %` (malla de 0,1 salta el nivel decimal).

---

## PARTE D — HECHOS EN ORDEN TEMPORAL

1. **Vela 6, desde 29820,80** el movimiento bajista (B Grande candidata de la LECTURA 1) cae: **100 % `29760,30` superado** (`29758,30` @16:35:33.046); **127 % `29743,965` y `127 %+0,25` `29743,715` superados** (`29742,80` @16:35:35.448) → **AUT** en ese tick. En ese mismo tick queda alcanzado el TT bajista `29742,90` (ancla confirmada).
2. El descenso **continúa creando nuevos mínimos**: `29717,60` (bar6), `29712,40` (bar7), `29683,20` (bar8), `29674,60`/`29670,90` (bar9)… hasta `29651,20` @16:42:09.361 (bar13).
3. **Vela 7:** tras el mínimo `29712,40` @16:36:02.112 comienza un **movimiento contrario (ascenso)**: máx `29738,40` @16:36:34.774; **vela 8** lo extiende a `29744,40` @16:37:10.254 (nuevo máximo).
4. **Vela 8, desde 29744,40** cae un movimiento contrario bajista: **100 % `29712,40` superado** (`29712,30` @16:37:35.310); **127 % `29703,76` y `127 %+0,25` `29703,51` superados** (`29702,80` @16:37:55.363) → **AUT**. El descenso prosigue hasta `29683,20` @16:37:59.175.
5. Tras ese AUT, los **contrarios alcistas** de la vela 8 y 9 (`29733,10` el mayor, `29701,10`, …) fueron **cancelados por nuevos mínimos**; el descenso siguió a `29670,90` (bar9) y `29651,20` (bar13).

**Respuestas directas Parte D**
- **¿B Grande alcanzó el 100 %?** — **SÍ** en las tres lecturas (superado, no solo tocado, salvo el contacto exacto del 100 % de la LECTURA 3, que también fue superado).
- **¿Superó 127 %+0,25?** — **SÍ** en las tres lecturas → **AUT** en L1 (`29742,80` @16:35:35.448), L2 y L3 (`29702,80` @16:37:55.363 / `29708,70` @16:37:40.718 respectivamente).
- **¿Hubo después movimiento contrario?** — **SÍ** en las tres: en L1 el ascenso de la vela 7–8; en L2/L3 los contrarios alcistas de las velas 8–9 (todos seguidos de nuevo mínimo).
- **¿B Grande creó después otro extremo?** — **SÍ** en las tres (nuevos mínimos tras cada contrario).

*(No se nombra C Grande ni CUT como conclusión: solo se describen los hechos de tick.)*

---

## PARTE E — UNA SOLA PREGUNTA CONCEPTUAL TM

Con la lectura de las velas 7–8: el movimiento alcista comienza en **P0 = `29712,40`** (mínimo de la vela 7) y alcanza primero **P1 = `29738,40`** (máximo de la vela 7); en la vela siguiente crea un nuevo extremo **P2 = `29744,40`** (máximo de la vela 8) antes de que comience el descenso contrario.

**¿P2 continúa siendo el extremo de A Grande (A Grande = `29712,40 → 29744,40`), o existe alguna regla TM que cierre A Grande en P1 = `29738,40` aunque después se cree P2 — y, en ese caso, qué movimiento es el tramo P1→P2?**

---

## BLOQUEOS Y RUTAS

- **Bloqueos (registrados, no resueltos aquí):** (1) fin de A Grande no único — candidatos `29738,40` (máx. vela 7) o `29744,40` (máx. vela 8); (2) inicio de A Grande no fijado — candidatos `29717,60` (mín. vela 6) o `29712,40` (mín. vela 7); (3) no hay módulo reconstruible para la LECTURA 2/3; (4) contradicción C1 (C Grande/CUT vela 8) sigue **BLOQUEANTE** y **no** se toca aquí.
- **Rutas:** `LECTURAS_VELAS_6_9.md` (este archivo, raíz del proyecto). No se modifica `DECISIONES_EXPERTO.md`, `REGLAS_CERRADAS.md` ni el golden.
