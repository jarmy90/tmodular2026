# CRONOLOGÍA DE MOVIMIENTOS — USTEC 2026-10-16 (sesión 16:30)

- **Agente:** MOVEMENT_RECONSTRUCTOR (Gate Cero, primera oleada — §5 y §6 del prompt v2)
- **Fuente de datos:** `data/ticks_USTEC_2026-10-16_16-30.csv`
- **Serie de precio empleada:** **Bid** (coherente al 100 % con `data/velas_USTEC_2026-10-16_16-30.csv`; ver §0)
- **Parser:** `src/replay/csv.js` (`loadTicks` / `loadBars`)
- **Alcance:** reconstrucción objetiva de ticks en orden estricto. Foco en **velas 7 y 8** (§12). Contexto velas 6 y 9 para continuidad.
- **Regla de método (§8, §13):** primero se describe el **recorrido real** (hechos de tick); la **clasificación TM** solo se propone como *posibilidad* y nunca se impone. Ninguna escena se ha movido de vela.

> Anti-spoiler: la cronología se construye **solo** desde los ticks. Los datos ancla del encargo se usaron únicamente como **verificación**, no como origen. No se ha usado el golden para generar ningún evento.

---

## 0. Serie de precio y verificación de coherencia

- Delimitador `;`, 5.658 ticks, 20 velas (`bar_index` 1–20).
- `last = 0.00` en todos los ticks ⇒ no hay serie Last. `ask` presente; **bid** es la serie continua usable.
- Verificación: para las **20 velas**, `open/high/low/close` reconstruidos desde **bid** coinciden **exactamente** con el CSV de velas (`match = true` en todas).
- `time_msc` (epoch) imprimible como UTC = campo `time` del propio CSV → sellos horarios internamente coherentes. Los timestamps de este documento son los del CSV (hora del bróker), con fecha 2026.10.16.

Verificación de anclas del encargo (hechos de tick, confirmados):

| Vela | Open | High (ts) | Low (ts) | Close | Ancla encargo |
|---|---|---|---|---|---|
| 7 | 29719.10 | 29738.40 @16:36:34.774 | 29712.40 @16:36:02.112 | 29735.70 | coincide |
| 8 | 29734.80 | 29744.40 @16:37:10.254 | 29683.20 @16:37:59.175 | 29689.10 | coincide |

- "Sin retorno alcista a ≥29738.40 tras el máximo de la vela 8": **confirmado**. Primer tick ≥29738.40 posterior es en la **vela 16** (high 29742.30 @16:45:31.684). En velas 9–15 todos los máximos < 29738.40 (vela 15 high 29736.70 es el más alto).

---

## 1. ¿Máximo o mínimo primero? (vela por vela, con timestamps)

| Vela | Primero | Timestamp 1.º | Segundo | Timestamp 2.º | Nuevos extremos vs vela anterior |
|---|---|---|---|---|---|
| 1 | **MÁXIMO** 29838.20 | 16:30:04.448 | MÍNIMO 29784.60 | 16:30:24.677 | — |
| 2 | MÁXIMO 29810.80 | 16:31:00.169 | **MÍNIMO 29760.30** | 16:31:33.648 | sí (nuevo mín.) |
| 3 | **MÍNIMO 29794.10** | 16:32:02.517 | MÁXIMO 29820.80 | 16:32:38.002 | sí (nuevo mín.) |
| 4 | MÁXIMO 29819.20 | 16:33:26.522 | MÍNIMO 29782.10 | 16:33:58.601 | sí (nuevo mín.) |
| 5 | MÁXIMO 29792.80 | 16:34:13.040 | **MÍNIMO 29765.70** | 16:34:56.951 | sí (nuevo mín.) |
| 6 | MÁXIMO 29780.30 | 16:35:16.001 | **MÍNIMO 29717.60** | 16:35:57.701 | sí (nuevo mín.) |
| **7** | **MÍNIMO 29712.40** | **16:36:02.112** | **MÁXIMO 29738.40** | **16:36:34.774** | sí (nuevo mín.) |
| **8** | **MÁXIMO 29744.40** | **16:37:10.254** | **MÍNIMO 29683.20** | **16:37:59.175** | sí (nuevo máx.) |
| 9 | MÁXIMO 29701.10 | 16:38:25.030 | **MÍNIMO 29670.90** | 16:38:53.502 | sí (nuevo mín.) |
| 10 | MÍNIMO 29669.20 | 16:39:03.523 | MÁXIMO 29708.10 | 16:39:49.025 | sí (nuevo mín.) |
| 11 | MÍNIMO 29665.60 | 16:40:12.680 | MÁXIMO 29698.90 | 16:40:32.727 | sí (nuevo mín.) |
| 12 | MÁXIMO 29683.60 | 16:41:00.185 | MÍNIMO 29656.10 | 16:41:34.079 | sí (nuevo mín.) |
| 13 | MÍNIMO 29651.20 | 16:42:09.361 | MÁXIMO 29685.60 | 16:42:55.279 | sí (nuevo mín.) |
| 14 | MÍNIMO 29679.80 | 16:43:01.691 | MÁXIMO 29706.20 | 16:43:27.754 | no |
| 15 | MÍNIMO 29683.40 | 16:44:21.312 | MÁXIMO 29736.70 | 16:44:59.014 | no |
| 16 | MÍNIMO 29720.60 | 16:45:16.847 | MÁXIMO 29742.30 | 16:45:31.684 | no (pero 1.er ≥29738.40) |
| 17 | MÁXIMO 29745.10 | 16:46:36.462 | MÍNIMO 29719.80 | 16:46:59.915 | sí (nuevo máx. de la secuencia) |
| 18 | MÁXIMO 29731.80 | 16:47:02.921 | MÍNIMO 29709.80 | 16:47:54.246 | no |
| 19 | MÁXIMO 29714.60 | 16:48:02.069 | MÍNIMO 29674.60 | 16:48:54.201 | no |
| 20 | MÍNIMO 29666.40 | 16:49:04.018 | MÁXIMO 29699.90 | 16:49:57.945 | sí (nuevo mín.) |

Nota vela 9: el máximo 29701.10 se imprime **dos veces** (16:38:25.030 y 16:38:26.833); el primero es el temporalmente válido.

**Respuestas directas:**
- **Vela 7 → alcanzó primero el MÍNIMO** (29712.40 @16:36:02.112) y después el MÁXIMO (29738.40 @16:36:34.774).
- **Vela 8 → alcanzó primero el MÁXIMO** (29744.40 @16:37:10.254) y después el MÍNIMO (29683.20 @16:37:59.175, último tick de la vela).

---

## 2. Continuidad entre velas (¿empezó antes / se interrumpió?)

| Frontera | Último tick vela N | Primer tick vela N+1 | Delta | ¿Se interrumpió el movimiento? |
|---|---|---|---|---|
| 6 → 7 | 29720.70 @16:35:59.907 | 29719.10 @16:36:00.107 | −1.60 | **NO.** El movimiento **bajista** continúa e **imprime nuevo mínimo** (29712.40 @16:36:02.112 < 29717.60 de vela 6). |
| 7 → 8 | 29735.70 @16:36:59.837 | 29734.80 @16:37:00.038 | −0.90 | **NO.** El movimiento **alcista** continúa e **imprime nuevo máximo** (29744.40 @16:37:10.254 > 29738.40 de vela 7). |
| 8 → 9 | 29689.10 @16:37:59.977 | 29688.30 @16:38:00.178 | −0.80 | **NO.** El movimiento **bajista** continúa e **imprime nuevo mínimo** (29674.60 @16:38:07.993 < 29683.20 de vela 8). |

**Respuestas directas:**
- **¿El movimiento comenzó en la vela anterior?** — **Sí** en vela 7 (el bajista viene de la vela 6) y **sí** en vela 8 (el alcista viene de la vela 7). En vela 9 también (el bajista viene de la vela 8).
- **¿El cambio de vela interrumpió realmente el movimiento?** — **No** en ninguna de las tres fronteras 6→7, 7→8, 8→9: en cada una el movimiento cruzó la frontera y produjo un nuevo extremo.

---

## 3. CRONOLOGÍA DE MOVIMIENTOS (tabla principal)

Léase con §8: `R-A…R-E` son **lecturas candidatas** (posibilidades), no clasificaciones confirmadas.
Movimientos reconstruidos con pivotes de amplitud ≥ ~4 pts (ruido de micromovimiento < 4 pts descartado; los micromovimientos no ocupan lectura — §10.8).

Columnas: `TIMESTAMP | PRECIO | DIRECCIÓN | NUEVO EXTREMO | RETROCESO | LECTURAS AFECTADAS | FUNCIÓN TM POSIBLE`.

### Vela 6 — tramo relevante previo (contexto de las lecturas activas)

| TIMESTAMP | PRECIO | DIRECCIÓN | NUEVO EXTREMO | RETROCESO | LECTURAS AFECTADAS | FUNCIÓN TM POSIBLE |
|---|---|---|---|---|---|---|
| 16:35:16.001 | 29780.30 | alcista | no | máximo intermedio | R-A | retroceso dentro de B Grande |
| 16:35:33.046 | 29758.30 | bajista | no | — | R-A | cruza 29760.30 (100 % de A Grande) |
| 16:35:35.448 | **29742.80** | bajista | **sí (nuevo mín.)** | — | R-A | **AUT + TT en el mismo tick** (29743.715 / 29742.90) |
| 16:35:57.701 | **29717.60** | bajista | **sí (nuevo mín. de vela 6)** | — | R-A, R-B | mínimo de vela 6; abre posible 1 bajista |
| 16:35:59.306 | 29722.20 | alcista | no | retroceso +4.6 | R-B | rebote final de la vela |

### Vela 7

| TIMESTAMP | PRECIO | DIRECCIÓN | NUEVO EXTREMO | RETROCESO | LECTURAS AFECTADAS | FUNCIÓN TM POSIBLE |
|---|---|---|---|---|---|---|
| 16:36:00.107 | 29719.10 | bajista | — (apertura) | desde 29720.70 | R-B | salida en plano (−1.60) |
| 16:36:02.112 | **29712.40** | bajista | **sí (nuevo mín. vela 6-7)** | — | R-B (fin), R-C (inicio) | **final del posible 1 bajista** (R-B) |
| 16:36:02.712 | 29719.40 | alcista | — | — | R-C | inicio A Grande alcista candidata |
| 16:36:03.714 | 29713.80 | bajista | no | −5.6 | R-C | retroceso |
| 16:36:05.115 | 29720.90 | alcista | no | — | R-C | extensión |
| 16:36:06.317 | 29714.30 | bajista | no | −6.6 | R-C | retroceso |
| 16:36:11.527 | 29728.10 | alcista | no | — | R-C | extensión |
| 16:36:19.341 | 29721.60 | bajista | no | −6.5 | R-C | retroceso |
| 16:36:27.355 | 29734.70 | alcista | no | — | R-C | extensión |
| 16:36:29.961 | 29726.60 | bajista | no | −8.1 | R-C | retroceso |
| 16:36:34.774 | **29738.40** | alcista | **sí (máx. de vela 7)** | — | R-C | A Grande (máximo de la vela) |
| 16:36:38.385 | 29727.60 | bajista | no | −10.8 | R-C | retroceso (no cancela) |
| 16:36:40.588 | 29735.10 | alcista | no | — | R-C | extensión |
| 16:36:41.392 | 29730.60 | bajista | no | −4.5 | R-C | retroceso |
| 16:36:42.793 | 29735.30 | alcista | no | — | R-C | extensión |
| 16:36:44.801 | 29728.30 | bajista | no | −7.0 | R-C | retroceso |
| 16:36:46.405 | 29734.10 | alcista | no | — | R-C | extensión |
| 16:36:47.208 | 29728.10 | bajista | no | −6.0 | R-C | retroceso |
| 16:36:48.808 | 29738.30 | alcista | no (retoque, −0.1) | — | R-C | retest del máximo |
| 16:36:52.420 | 29731.30 | bajista | no | −7.0 | R-C | retroceso |
| 16:36:53.221 | 29737.30 | alcista | no | — | R-C | extensión |
| 16:36:55.226 | 29730.10 | bajista | no | −7.2 | R-C | retroceso |
| 16:36:57.632 | 29737.20 | alcista | no | — | R-C | extensión |
| 16:36:59.837 | 29735.70 | — | cierre de vela | — | R-C | cierre (movimiento vivo) |

### Vela 8

| TIMESTAMP | PRECIO | DIRECCIÓN | NUEVO EXTREMO | RETROCESO | LECTURAS AFECTADAS | FUNCIÓN TM POSIBLE |
|---|---|---|---|---|---|---|
| 16:37:00.038 | 29734.80 | bajista | — (apertura) | desde 29735.70 | R-C | salida en plano (−0.90) |
| 16:37:00.839 | 29735.80 | alcista | no | — | R-C | micromovimiento |
| 16:37:04.042 | 29725.10 | bajista | no | desde 29738.40 | R-C | retroceso (no nuevo extremo) |
| 16:37:10.254 | **29744.40** | alcista | **sí (máx. vela 8 y de la secuencia 7-8)** | — | R-C (máx.), R-D (inicio) | **máximo de A Grande candidata (R-C) / inicio B Grande candidata (R-D)** |
| 16:37:17.875 | 29717.60 | bajista | no (nuevo mín. interno de vela 8) | — | R-D | B Grande bajista en curso |
| 16:37:18.678 | 29730.10 | alcista | no | +12.5 | R-D, R-E | contrario (C Grande candidata, no confirmada) |
| 16:37:20.483 | 29724.20 | bajista | no | — | R-D, R-E | C candidata cancelada por retroceso |
| 16:37:22.085 | 29731.60 | alcista | no | +13.2 | R-D, R-E | contrario (C candidata) |
| 16:37:22.687 | 29724.70 | bajista | no | — | R-D, R-E | cancelación |
| 16:37:23.687 | 29729.10 | alcista | no | +9.3 | R-D, R-E | contrario (C candidata) |
| 16:37:24.088 | 29724.80 | bajista | no | — | R-D, R-E | cancelación |
| 16:37:26.090 | 29733.10 | alcista | no | +21.0 | R-D, R-E | contrario máximo de la vela 8 (C candidata) |
| 16:37:35.310 | **29712.30** | bajista | **sí (nuevo mín.)** | — | R-D, R-E | **B Grande alcanza ~100 %** (nivel 29712.40) / **cancela C candidata** |
| 16:37:37.514 | 29719.30 | alcista | no | +7.0 | R-D, R-E | contrario (C candidata) |
| 16:37:42.123 | **29704.20** | bajista | **sí (nuevo mín.)** | — | R-D, R-E | cancela C candidata |
| 16:37:45.935 | 29718.60 | alcista | no | +14.4 | R-D, R-E | contrario (C candidata) |
| 16:37:49.148 | 29710.80 | bajista | no | — | R-D | retroceso interno |
| 16:37:51.358 | 29715.30 | alcista | no | +4.5 | R-D | contrario pequeño |
| 16:37:55.363 | **29702.80** | bajista | **sí (nuevo mín.)** | — | R-D | **B Grande alcanza el nivel AUT candidato** (29703.51) |
| 16:37:59.175 | **29683.20** | bajista | **sí (mín. de vela 8)** | — | R-D | mínimo de vela 8 (último tick) |
| 16:37:59.977 | 29689.10 | — | cierre de vela | rebote +5.9 | R-D | cierre (movimiento vivo) |

### Vela 9 — cabecera (continuidad)

| TIMESTAMP | PRECIO | DIRECCIÓN | NUEVO EXTREMO | RETROCESO | LECTURAS AFECTADAS | FUNCIÓN TM POSIBLE |
|---|---|---|---|---|---|---|
| 16:38:00.178 | 29688.30 | bajista | — (apertura) | desde 29689.10 | R-D | salida en plano (−0.80) |
| 16:38:07.993 | **29674.60** | bajista | **sí (nuevo mín.)** | — | R-D | B Grande continúa (no interrumpida por cambio de vela) |
| 16:38:16.212 | 29698.90 | alcista | no | +24.3 | R-D, R-E | contrario (C candidata) |
| 16:38:53.502 | 29670.90 | bajista | sí (nuevo mín.) | — | R-D | nuevo extremo cancela el contrario |

---

## 4. PROTOCOLO REFORZADO — VELA 7 (§12)

- **Apertura:** 29719.10 @16:36:00.107 (bid). Gap/salida en plano vs cierre vela 6 (29720.70): **−1.60**.
- **Primer extremo relevante:** **MÍNIMO 29712.40 @16:36:02.112** (a 2.0 s de la apertura). Es **nuevo mínimo** respecto a la vela 6 (29717.60) ⇒ el tramo bajista precedente continúa cruzando la frontera de vela.
- **Segundo extremo relevante:** **MÁXIMO 29738.40 @16:36:34.774** (a 34.7 s).
- **Orden exacto entre mínimo y máximo:** **MÍNIMO primero (16:36:02.112) → MÁXIMO después (16:36:34.774)**. Ningún tick posterior supera 29738.40 dentro de la vela 7 (máximos posteriores 29738.30 @16:36:48.808 y 29737.20 @16:36:57.632 son retoques).
- **Movimientos entre los extremos (mín → máx):** ascenso 29712.40 → 29738.40 (**+26.0 pts**) con **tres retrocesos** intermedios significativos: 29713.80 (−5.6), 29714.30 (−6.6), 29721.60 (−6.5), 29726.60 (−8.1). Tramo final acelerado: 29734.90→29737.70→29738.40 en ~0.6 s (16:36:34.172→.774).
- **Lecturas activas procedentes de la vela 6:**
  - **R-A** — bloque *módulo(1+2) → A Grande (vela 3) → B Grande (velas 4-6)*, con **AUT y TT confirmados en vela 6** (16:35:35.448).
  - **R-B** — *posible 1 bajista* abierto en el mínimo de la vela 6 (29717.60) tras AUT/TT.
- **Niveles AUT / TT reconstruibles por hechos:**
  - **R-A:** rango del conjunto vela 1+2 = `29838.20 − 29760.30 = 77.90`. Final de A Grande = 29820.80.
    - **TT bajista = 29820.80 − 77.90 = 29742.90** → alcanzado en vela 6 @16:35:35.448 (29742.80).
    - Nivel AUT de su B Grande (`final A − 1.27·A − 0.25`, A = 60.50) = **29743.715** → alcanzado en vela 6 @16:35:35.448.
  - **R-B (posible 1 bajista):** no hay módulo asociado reconstruible por hechos ⇒ **AUT/TT de R-B no determinables** (ambigüedad objetiva, ver §8).
- **Hecho de cierre:** el movimiento bajista R-B **finaliza** en 29712.40 @16:36:02.112; dentro de la propia vela 7 comienza el alcista. Clasificar ese alcista como **A Grande** es una **posibilidad** (R-C), no un hecho de tick.

## 5. PROTOCOLO REFORZADO — VELA 8 (§12)

- **Apertura:** 29734.80 @16:37:00.038 (bid). Salida en plano vs cierre vela 7 (29735.70): **−0.90**.
- **Orden exacto entre máximo y mínimo:** **MÁXIMO primero → MÍNIMO después.**
- **Timestamp del MÁXIMO:** **29744.40 @16:37:10.254** (a 10.2 s de la apertura). Es nuevo máximo respecto a la vela 7 (29738.40) ⇒ el movimiento alcista cruzó la frontera de vela y se extendió.
- **Timestamp del MÍNIMO:** **29683.20 @16:37:59.175** (último tick de la vela).
- **Movimientos entre apertura / máximo / mínimo:**
  1. Apertura 29734.80 → pequeño retroceso a **29725.10 @16:37:04.042** (−9.7 desde máx. previo; **no** nuevo extremo).
  2. Ascenso 29725.10 → **29744.40 @16:37:10.254** (`+19.3` desde el retroceso; aceleración 29736.1→29744.4 entre 16:37:06.045 y 16:37:10.254).
  3. Descenso 29744.40 → **29683.20 @16:37:59.175** (`−61.2 pts`) gobernado por **mínimos decrecientes** (ver §7).
- **¿Qué lectura alcanza B Grande / AUT / TT?**
  - **Hecho (recorrido):** desde el máximo 29744.40, el precio recorrió **−32.00 pts** (nivel 29712.40) @**16:37:35.310** y **−40.89 pts** (nivel ~29703.51) @**16:37:55.363**.
  - **Posible (R-D):** si el alcista vela 7-mín (29712.40) → vela 8-máx (29744.40), tamaño **32.00**, es **A Grande**:
    - **B Grande 100 %** = 29744.40 − 32.00 = **29712.40** → alcanzado @16:37:35.310 (29712.30).
    - **AUT** = 29744.40 − 1.27·32.00 − 0.25 = **29703.51** → alcanzado @16:37:55.363 (29702.80). B Grande continúa hasta 29683.20 (por debajo del nivel AUT).
  - **TT:** no hay módulo reconstruible asociado a R-D ⇒ **no se puede fijar un TT nuevo por hechos**. El único TT reconstruible (29742.90) pertenece a R-A y ya quedó confirmado en vela 6.
- **Movimientos contrarios posteriores a B Grande:** contrarios alcistas a 29730.10, 29731.60, 29729.10, **29733.10 @16:37:26.090** (el mayor), 29719.30, 29718.60, 29715.30. **Todos** fueron seguidos por un nuevo mínimo.
- **¿B Grande vuelve a crear extremo y cancelaría una C Grande candidata?** **Sí.** Cada contrario (B→C candidata) es cancelado por un nuevo mínimo de B Grande (29712.30, 29704.20, 29702.80, 29683.20). **Ninguna C Grande se confirma dentro de la vela 8**; las candidatas quedan **canceladas por nuevo extremo** (§10.7). No se pregunta "¿hay CUT?": ver §7.

---

## 6. Respuestas explícitas al encargo (las cinco preguntas)

1. **¿Cada vela alcanzó primero el máximo o el mínimo?** — Ver tabla §1. Síntesis: **velas 3, 7, 10, 11, 13, 14, 15, 16, 20 → mínimo primero**; **velas 1, 2, 4, 5, 6, 8, 9, 12, 17, 18, 19 → máximo primero**. En particular **vela 7 = mínimo→máximo** y **vela 8 = máximo→mínimo**.
2. **¿El movimiento comenzó en la vela anterior?** — **Sí.** Vela 7: el bajista viene de la vela 6 (nuevo mínimo). Vela 8: el alcista viene de la vela 7 (nuevo máximo). Vela 9: el bajista viene de la vela 8 (nuevo mínimo).
3. **¿El cambio de vela interrumpió el movimiento?** — **No** en 6→7, 7→8 ni 8→9. En las tres el movimiento cruzó la frontera e impuso nuevo extremo (§2).
4. **¿Un movimiento contrario fue cancelado por un nuevo extremo?** — **Sí, en la vela 8** (y en la 9). Los contrarios alcistas de R-D (máximo 29733.10 @16:37:26.090) fueron cancelados por nuevos mínimos sucesivos; igualmente sus **C Grande candidatas** (§5).
5. **¿Qué lecturas continúan siendo válidas?** — Ver §7 y §8.

---

## 7. Lecturas: hechos vs posibilidades

| ID | Descripción (posible) | Hecho objetivo que la sostiene | Estado |
|---|---|---|---|
| **R-A** | módulo(1+2) → A Grande (v.3) → B Grande (v.4-6) + **AUT** + **TT** | rango 77.90 (29838.20−29760.30); AUT/TT alcanzados 16:35:35.448 | **TT confirmado en vela 6**; lectura que "contiene módulo" conserva su historia. No se invalida por cambio de vela (§10.1). |
| **R-B** | **posible 1 bajista** tras AUT/TT (abierto v.6) | mínimo 29717.60 (v.6) → 29712.40 (v.7) | **Finaliza en vela 7** @16:36:02.112 (fin del posible 1). AUT/TT de R-B no determinables por hechos. |
| **R-C** | **A Grande** alcista iniciada en vela 7 | mínimo 29712.40 (v.7) → máximo 29744.40 (v.8), +32.0 pts | **Válida como candidata**; su máximo cruza la frontera de vela 7→8 (no interrumpida). |
| **R-D** | **B Grande** bajista desde 29744.40 | 100 % (29712.40) @16:37:35.310; nivel AUT (29703.51) @16:37:55.363 | **Candidata**; si R-C es A Grande, R-D alcanza **AUT** por hechos de tick. |
| **R-E** | **C Grande** candidata(s) tras B Grande | contrarios alcistas de vela 8 (máx. 29733.10) | **CANCELADA(S)** por nuevos mínimos de B Grande. |

---

## 8. Bloqueos y ambigüedades objetivas

1. **[BLOQUEANTE — CUT vela 8]** El golden/`REGLAS_CERRADAS §E/F` atribuyen a la vela 8 el evento **CUT**. Por hechos de tick, **CUT no puede confirmarse en la vela 8**:
   - CUT exige que **C Grande** alcance el **final de A Grande**.
   - Tras el máximo de la vela 8 (29744.40 @16:37:10.254) **no existe ningún tick ≥ 29738.40** hasta la **vela 16** (29742.30 @16:45:31.684) — verificado.
   - Por tanto, ninguna C Grande puede completarse en la vela 8; las candidatas son **canceladas** por nuevos mínimos (§5).
   - **Consecuencia:** el CUT de la vela 8 contradice el recorrido de ticks. No se mueve el evento a otra vela (§13). → duda para Javier (RULES_ANALYST/SCENE_QUESTIONER).
2. **[BLOQUEANTE — fin de R-C / inicio de R-D]** El "final de A Grande" (nivel que debe alcanzar C Grande) no es determinable de forma única por hechos: candidatos 29738.40 (máx. vela 7) o 29744.40 (máx. vela 8). La elección cambia si un eventual C Grande confirma CUT o no.
3. **[NO BLOQUEANTE — base de medida de R-C/R-D]** El tamaño de la A Grande candidata depende de dónde se fije su inicio (mín. vela 6 = 29717.60 → 26.80; mín. vela 7 = 29712.40 → 32.00). Con inicio en 29712.40 el AUT de R-D = 29703.51 y se alcanza (@16:37:55.363); con inicio en 29717.60 el AUT = 29710.11 y también se alcanza, pero en otro tick. Falta la regla exacta de referencia de inicio.
4. **[NO BLOQUEANTE — TT de R-D]** Sin módulo reconstruible asociado a R-C/R-D, no hay **TT** nuevo posible por hechos; solo existe el TT ya confirmado de R-A (29742.90, vela 6). Falta criterio para saber si R-D genera módulo.
5. **[NO BLOQUEANTE — R-B]** El *posible 1 bajista* (R-B) no tiene módulo reconstruible ⇒ sus niveles AUT/TT no son calculables; falta regla de referencia del ciclo posterior a TT/AUT.
6. **[NO BLOQUEANTE — pivotes]** La tabla §3 usa pivotes ≥ ~4 pts. El umbral de micromovimiento no está cerrado (§11): con umbral 2 pts aparecen más pivotes intravela, pero **no alteran** el orden de extremos mayor de las velas 7 y 8 ni la continuidad entre velas.

---

## 9. Anti-spoiler

- Ningún precio, timestamp ni número de vela de este documento proviene del golden.
- Los datos ancla del encargo se usaron **solo** para verificar (§0); la reconstrucción se hizo tick a tick.
- No se ha reclasificado ni trasladado ningún evento TM entre velas.
- Clasificaciones TM marcadas como **posibles** (R-A…R-E); hechos de tick marcados como **hechos**.

---
*Artefacto del agente MOVEMENT_RECONSTRUCTOR. Alimenta a SCENE_QUESTIONER (§6, segunda oleada) y a TM_VOCABULARY_REVIEWER. No se programa núcleo TM antes del gate de comprensión.*

---

## 10. ANEXO — Cronología 6–9 con apertura/cierre y time_msc (segunda oleada)

> Añadido sin borrar lo existente. Aporta los **bordes** (apertura/cierre con `time_msc`), que §1 no incluía. Serie **Bid**. Detalle completo en `LECTURAS_VELAS_6_9.md`.

| Vela | Apertura (1.º bid) | Cierre (último bid) | Máximo | Mínimo | Orden de extremos |
|---|---|---|---|---|---|
| 6 | `29766,40` @16:35:00.160 (1792168500160) | `29720,70` @16:35:59.907 (1792168559907) | `29780,30` @16:35:16.001 (1792168516001) | `29717,60` @16:35:57.701 (1792168557701) | MAX → MIN |
| 7 | `29719,10` @16:36:00.107 (1792168560107) | `29735,70` @16:36:59.837 (1792168619837) | `29738,40` @16:36:34.774 (1792168594774) | `29712,40` @16:36:02.112 (1792168562112) | MIN → MAX |
| 8 | `29734,80` @16:37:00.038 (1792168620038) | `29689,10` @16:37:59.977 (1792168679977) | `29744,40` @16:37:10.254 (1792168630254) | `29683,20` @16:37:59.175 (1792168679175) | MAX → MIN |
| 9 | `29688,30` @16:38:00.178 (1792168680178) | `29678,40` @16:38:59.914 (1792168739914) | `29701,10` @16:38:25.030 (1792168705030) | `29670,90` @16:38:53.502 (1792168733502) | MAX → MIN |
