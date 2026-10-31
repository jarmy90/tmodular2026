# AUDITORÍA DE DATOS — DATA_AUDITOR (TM / ECC-OpenCode)

- **Agente:** DATA_AUDITOR (Gate Cero, primera oleada)
- **Proyecto:** `C:\Users\hp\Documents\Teoria Modular\tm-explorer`
- **Fecha de auditoría:** 2026-10-18
- **Alcance:** Auditoría de datos. NINGUNA lectura TM. No se modificó el motor ni los CSV.
- **Normativa aplicada:** `Prompt_ECC_OpenCode_TM_..._v2.txt`, §5 (DATA_AUDITOR) y §1.

## Ficheros auditados

| Rol | Ruta | Delimitador | Filas |
|---|---|---|---|
| Ticks | `data\ticks_USTEC_2026-10-16_16-30.csv` | `;` | 5658 (+1 cabecera) |
| Velas M1 | `data\velas_USTEC_2026-10-16_16-30.csv` | `;` | 20 (+1 cabecera) |
| Parser de referencia | `src\replay\csv.js` | `;` | — |

Columnas ticks: `time;time_msc;bid;ask;last;volume;flags;bar_index;bar_start`
Columnas velas: `bar_index;inicio;fin;open;high;low;close;direccion;cuerpo_pts;rango_total_pts;cola_superior_pts;cola_inferior_pts;ticks;time_open_msc;time_high_msc;time_low_msc;time_close_msc;gap_desde_cierre_anterior_pts`

---

## 1. Resumen ejecutivo

- **ESTADO: APTO (apto para replay determinista sobre la serie Bid).**
- La serie de precio del dataset es **Bid**, confirmada numéricamente: la reconstrucción OHLC M1 desde ticks con la columna `bid` reproduce **20/20 velas** con delta **0.00** en Open, High, Low y Close.
- `ask = bid + 0.90` (spread fijo, 5658/5658 ticks). `last = 0` y `volume = 0` en todos los ticks (no existe serie Last real).
- **Discrepancias totales: 0** (0 deltas OHLC, 0 mismatches de timestamp, 0 mismatches de recuento de ticks).
- **Duplicados: 0. Desorden temporal: 0.** Único hueco relevante: **5.393 s** dentro de la vela 16 (que también es la de menos ticks, 264).
- Instrumento/sesión coherentes con el nombre de fichero: USTEC, 2026-10-16, sesión continua 16:30:00.026 → 16:49:59.949 (UTC). Los CSV **no incluyen columna de símbolo ni de fecha**; la identificación depende del nombre de fichero (ver Incidencias I-5).

---

## 2. Nº de ticks por vela (ticks CSV vs velas CSV)

Recuento reconstruido desde ticks = columna `ticks` del CSV de velas en **las 20 velas** (0 discrepancias).

| Vela | Ticks | Vela | Ticks | Vela | Ticks | Vela | Ticks |
|---|---|---|---|---|---|---|---|
| 1 | 286 | 6 | 282 | 11 | 289 | 16 | 264 |
| 2 | 284 | 7 | 287 | 12 | 278 | 17 | 282 |
| 3 | 287 | 8 | 291 | 13 | 283 | 18 | 280 |
| 4 | 285 | 9 | 285 | 14 | 283 | 19 | 280 |
| 5 | 286 | 10 | 287 | 15 | 279 | 20 | 280 |

Total ticks = **5658** = suma de la columna `ticks` de velas (5658). ✔

---

## 3. Serie de precio concluida (justificación numérica)

Reconstrucción OHLC M1 por `bar_index` para cada candidata (open = primer tick, high/low = extremos, close = último tick de la vela):

| Serie | Expresión | Velas que coinciden exactamente | Error sistemático observado |
|---|---|---|---|
| **Bid** | `bid` | **20 / 20** | **0.00** en O/H/L/C |
| Ask | `ask` | 0 / 20 | **+0.90** en O/H/L/C (todas las velas) |
| Mid | `(bid+ask)/2` | 0 / 20 | **+0.45** en O/H/L/C (todas las velas) |
| Last | `last` | 0 / 20 | `last = 0.00` ⇒ reconstrucción nula, inválida |

**Conclusión:** las velas del CSV son **Bid**. El error constante `+0.90` (Ask) y `+0.45` (Mid) en las 20 velas, frente al error `0.00` de Bid, descarta Ask, Mid y Last. No hay serie Last explotable (campo a 0).

Además, los timestamps de open/high/low/close de las velas coinciden **exactamente** con el primer tick, argmax, argmin y último tick de la serie Bid (0 mismatches en 20×4 = 80 comprobaciones).

---

## 4. Tabla de reconstrucción OHLC vs CSV (serie Bid) con deltas

`Recon` = reconstrucción desde ticks por Bid. `Δ` = Recon − CSV.

| Vela | CSV O/H/L/C | Recon O/H/L/C (Bid) | ΔO | ΔH | ΔL | ΔC | Ticks | Estado |
|---|---|---|---|---|---|---|---|---|
| 1 | 29820.60 / 29838.20 / 29784.60 / 29811.60 | 29820.60 / 29838.20 / 29784.60 / 29811.60 | 0.00 | 0.00 | 0.00 | 0.00 | 286 | OK |
| 2 | 29810.80 / 29810.80 / 29760.30 / 29793.10 | 29810.80 / 29810.80 / 29760.30 / 29793.10 | 0.00 | 0.00 | 0.00 | 0.00 | 284 | OK |
| 3 | 29796.70 / 29820.80 / 29794.10 / 29809.80 | 29796.70 / 29820.80 / 29794.10 / 29809.80 | 0.00 | 0.00 | 0.00 | 0.00 | 287 | OK |
| 4 | 29808.30 / 29819.20 / 29782.10 / 29785.90 | 29808.30 / 29819.20 / 29782.10 / 29785.90 | 0.00 | 0.00 | 0.00 | 0.00 | 285 | OK |
| 5 | 29784.90 / 29792.80 / 29765.70 / 29766.90 | 29784.90 / 29792.80 / 29765.70 / 29766.90 | 0.00 | 0.00 | 0.00 | 0.00 | 286 | OK |
| 6 | 29766.40 / 29780.30 / 29717.60 / 29720.70 | 29766.40 / 29780.30 / 29717.60 / 29720.70 | 0.00 | 0.00 | 0.00 | 0.00 | 282 | OK |
| 7 | 29719.10 / 29738.40 / 29712.40 / 29735.70 | 29719.10 / 29738.40 / 29712.40 / 29735.70 | 0.00 | 0.00 | 0.00 | 0.00 | 287 | OK |
| 8 | 29734.80 / 29744.40 / 29683.20 / 29689.10 | 29734.80 / 29744.40 / 29683.20 / 29689.10 | 0.00 | 0.00 | 0.00 | 0.00 | 291 | OK |
| 9 | 29688.30 / 29701.10 / 29670.90 / 29678.40 | 29688.30 / 29701.10 / 29670.90 / 29678.40 | 0.00 | 0.00 | 0.00 | 0.00 | 285 | OK |
| 10 | 29678.60 / 29708.10 / 29669.20 / 29693.30 | 29678.60 / 29708.10 / 29669.20 / 29693.30 | 0.00 | 0.00 | 0.00 | 0.00 | 287 | OK |
| 11 | 29694.90 / 29698.90 / 29665.60 / 29682.90 | 29694.90 / 29698.90 / 29665.60 / 29682.90 | 0.00 | 0.00 | 0.00 | 0.00 | 289 | OK |
| 12 | 29683.60 / 29683.60 / 29656.10 / 29670.80 | 29683.60 / 29683.60 / 29656.10 / 29670.80 | 0.00 | 0.00 | 0.00 | 0.00 | 278 | OK |
| 13 | 29668.40 / 29685.60 / 29651.20 / 29684.30 | 29668.40 / 29685.60 / 29651.20 / 29684.30 | 0.00 | 0.00 | 0.00 | 0.00 | 283 | OK |
| 14 | 29686.80 / 29706.20 / 29679.80 / 29693.10 | 29686.80 / 29706.20 / 29679.80 / 29693.10 | 0.00 | 0.00 | 0.00 | 0.00 | 283 | OK |
| 15 | 29691.60 / 29736.70 / 29683.40 / 29733.20 | 29691.60 / 29736.70 / 29683.40 / 29733.20 | 0.00 | 0.00 | 0.00 | 0.00 | 279 | OK |
| 16 | 29733.30 / 29742.30 / 29720.60 / 29726.80 | 29733.30 / 29742.30 / 29720.60 / 29726.80 | 0.00 | 0.00 | 0.00 | 0.00 | 264 | OK |
| 17 | 29725.60 / 29745.10 / 29719.80 / 29719.80 | 29725.60 / 29745.10 / 29719.80 / 29719.80 | 0.00 | 0.00 | 0.00 | 0.00 | 282 | OK |
| 18 | 29721.90 / 29731.80 / 29709.80 / 29713.10 | 29721.90 / 29731.80 / 29709.80 / 29713.10 | 0.00 | 0.00 | 0.00 | 0.00 | 280 | OK |
| 19 | 29712.30 / 29714.60 / 29674.60 / 29680.10 | 29712.30 / 29714.60 / 29674.60 / 29680.10 | 0.00 | 0.00 | 0.00 | 0.00 | 280 | OK |
| 20 | 29680.80 / 29699.90 / 29666.40 / 29689.90 | 29680.80 / 29699.90 / 29666.40 / 29689.90 | 0.00 | 0.00 | 0.00 | 0.00 | 280 | OK |

**Discrepancias: 0 / 20 velas** (80 deltas OHLC, todos 0.00).
**Mismatches de timestamp open/high/low/close vs CSV: 0 / 80.**
**Mismatches de recuento de ticks: 0 / 20.**

---

## 5. Incidencias

### 5.1 Duplicados
- `time_msc` duplicados: **0** (5658 valores distintos sobre 5658 filas).
- Filas completas duplicadas (`time|time_msc|bid|ask`): **0**.
- `time` (segundo) repetido dentro del mismo segundo: normal (máx. 6 ticks/segundo); no es duplicado de tick.

### 5.2 Orden temporal
- Filas con `time_msc` menor que la anterior: **0**.
- `time_msc` adyacentes iguales: **0**.
- Orden estrictamente creciente por `time_msc`. ✔

### 5.3 Huecos
- Intervalo entre ticks: min 135 ms, p50 200 ms, p90 202 ms, p99 402 ms, **máx 5393 ms**.
- Un único hueco > 5 s: entre `16:45:07.921` (msc 1792169107921) y `16:45:13.314` (msc 1792169113314), **dentro de la vela 16** (coincide con el mínimo de actividad: 264 ticks). No hay saltos de minuto ni de vela.

### 5.4 Delimitador, decimales y formato
- Delimitador `;` uniforme: 9 columnas en ticks, 18 en velas, sin variación.
- Sin BOM; finales de línea CRLF.
- `bid`: siempre 1 decimal. `ask`: 0 o 1 decimal (consecuencia de `bid + 0.90`). `last`, `volume`: 0.00 fijo. `flags`: 134 constante (`0x86`).
- Spread `ask − bid`: **0.90** en 5658/5658 ticks (spread fijo).

### 5.5 Zona horaria (`time` vs `time_msc`)
- Primer tick: `time=2026.10.16 16:30:00`, `time_msc=1792168200026` ⇒ UTC `2026-10-16T16:30:00.026Z`.
- Último tick: `time=2026.10.16 16:49:59`, `time_msc=1792169399949` ⇒ UTC `2026-10-16T16:49:59.949Z`.
- La parte horaria de `time` coincide con la hora **UTC** de `time_msc` (hora de servidor del bróker = UTC en esta muestra). `time` es granularidad de segundo; `time_msc` de milisegundo. **Coherentes**; usar `time_msc` para el orden/replay.

### 5.6 Coherencia instrumento / sesión / serie
- Símbolo, fecha y sesión solo constan en el **nombre de fichero** (USTEC / 2026-10-16 / 16:30). Los CSV no tienen columna de símbolo ni de fecha.
- Sesión continua 16:30–16:50 sin cortes de minuto; `bar_index` 1..20 continuo y alineado con `bar_start` (0 filas con desalineación minuto↔`bar_start`). ✔

### 5.7 Hallazgos por ID

| ID | Gravedad | Hallazgo |
|---|---|---|
| I-1 | Info | Serie de precio = **Bid** (spread fijo 0.90; `last`/`volume` a 0). |
| I-2 | Baja | Un hueco de 5.393 s dentro de la vela 16 (única vela con < 270 ticks). |
| I-3 | Ninguna | Sin duplicados ni desorden; `time_msc` estrictamente creciente. |
| I-4 | Info | `time` = hora UTC de `time_msc`; usar `time_msc` como clave temporal. |
| I-5 | Baja | CSV sin columna de símbolo/fecha; identificación depende del nombre de fichero. Verificar contra el gráfico/export origen. |
| I-6 | Info | Sin serie Last real (`last=0`): cualquier lógica que asuma "Last" o "trades" no es aplicable; el replay debe usar Bid. |

---

## 6. Conclusión sobre aptitud del dataset para replay determinista

- **APTO.** Orden estricto por `time_msc`, sin duplicados ni desorden, delimitador y decimales consistentes, sesión e instrumento coherentes con el nombre de fichero.
- El **replay debe construirse sobre la serie Bid**, que reproduce exactamente las velas M1 del CSV (20/20, delta 0.00).
- Único punto a tener en cuenta: el hueco de 5.393 s en la vela 16 (no introduce ambigüedad de orden, pero es la vela de menor densidad).
- No hay bloqueos duros de datos.

### Pregunta abierta para el experto (no bloqueante para la auditoría)
La normativa (§11) reserva a Javier la confirmación de la **serie de precio exacta para el replay** cuando los datos mezclan Bid/Ask/Last/mid. En esta muestra **no hay mezcla**: la evidencia numérica fija Bid de forma inequívoca. Se deja constancia para validación del experto, sin que ello bloquee la auditoría de datos.

---

*Generado por DATA_AUDITOR. No contiene lectura TM. No se modificaron el motor ni los CSV.*
