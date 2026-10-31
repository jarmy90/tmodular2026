# INFORME DE TRASPASO FUNCIONAL — MOTOR v0.7.5.2 (TM_CORE_v0752_CANONICAL)

**Auditor:** TM_READER_VALIDATOR (Reader Validator)
**Fecha:** 2026-10-28
**Objeto:** `TM_CORE_v0752_CANONICAL.zip` (candidato de DS TM BOSS)
**Golden de referencia:** `TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v003.txt`
**Autoridad documental:** `TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA_R1.md` + `REGLAS_CERRADAS.md` (CERRADAS) + `DECISIONES_EXPERTO.md` (DEC-015)
**Modo:** solo lectura. No se editó motor, tests, árbol, golden ni reglas.

---

## 0. CONTROL DEL ARTEFACTO

| Elemento | Valor |
|---|---|
| ZIP | `TM_CORE_v0752_CANONICAL.zip` — 1.356.866 B (re-sellado por DS el 28-10-2026) |
| SHA-256 ZIP | `3380c0a82b779ec1e49d8270687f3e3e7627a524c16d8347c70c489107b7892a` |
| Entradas | 25 (23 payload + `manifest.json` + `SHA256SUMS.txt`) |
| SHA256SUMS | 24/24 OK |
| Manifest | `verdict: LECTURA_NO_REPRODUCIDA` |
| Motor | `python/TM_CORE_PYTHON_v0752_CANONICAL.py` — 104.102 B |
| Raw | `out/CORE_RAW_OUTPUT.json` — 20.964.900 B, SHA-256 `cd5c6feb858dbdd6d31fd39ee7c3085e8d56d93f82b5e8d8ba39a81c9d1f31d7` |
| Conteos | feed_points 20.335 · events 6.559 · readings 1.426 · local_events 4.901 · local_sequences 1 |

El hash se verificó **antes** de abrir el ZIP. La extracción se hizo en directorio temporal ajeno al árbol canónico.

**Re-sellado:** DS reemplazó el contenedor ZIP (hash anterior `3d066f6a…c0ab`, descartado) por `3380c0a8…7892a` para incluir selftest y transformaciones en `repro/run_all.py`. Comparación byte a byte de ambas extracciones: **25/25 archivos idénticos** (motor, datos, `out/*.json`, manifest, SHA256SUMS, tests, repro, diff). El contenido funcional auditado **no cambió**; este informe se ancla al hash vigente `3380c0a8…7892a`.

---

## 1. INTEGRIDAD Y REPRODUCIBILIDAD DEL PAQUETE

1. **El raw no fue alterado por la comparación.** `GOLDEN_COMPARISON.json` declara `raw_sha256_before` = `raw_sha256_after` = `cd5c6feb…1f31d7`, idéntico al hash recalculado por el auditor. La comparación es posterior (13:35:02) al raw (13:35:00) y es de solo lectura. **VERIFICADO.**
2. `SELFTEST.json`: PASS, 8 checks.
3. `TRANSFORMATION_TESTS.json`: PASS (chunk serialize/restore, desplazamiento de precios y timestamps, inversión de dirección, sin hardcodes en el motor; 2.297 puntos).
4. `HARDCODE_SCAN.json`: PASS, 26 literales del golden comprobados, 0 coincidencias.
5. `PREFIX_REPORT.json`: **`NOT_RUN_FULL_MATRIX`** — no hay matriz de prefijos (75 cierres físicos, 500 cortes aleatorios, proceso nuevo por corte). **No hay evidencia de generalidad ni de causalidad por prefijo.**
6. `GOLDEN_COMPARISON.json`: 8/9, `comparison_exit: 2`, `status: LECTURA_NO_REPRODUCIDA`, `first_failure: "16:23 AUT alcista en secuencia estructural v003 1879"`.
7. **Reproducción ejecutada por el auditor:** `python repro/run_all.py` sobre la extracción limpia del ZIP `3380c0a8…7892a` (selftest + transformaciones + motor + comparación). Resultado: raw `cd5c6feb…1f31d7`, 20.335 / 6.559 / 1.426 / 4.901, `R0062_R0064: []`, `comparison_exit: 2`. **Idéntico al raw entregado: el pipeline es reproducible y determinista.**

Los puntos 2–4 son pruebas de autoconsistencia del candidato: **no acreditan exactitud tick a tick.**

---

## 2. RESULTADO TICK A TICK (16:15 → 16:24)

El golden solo aporta detalle fino (precio + `sequence_id` + hora) en 16:22–16:24; en 16:15–16:21 aporta módulo/A/B/AUT/TT a nivel de vela. Contraste con `sequence_id` del feed maestro:

| Vela | Golden | Motor v0.7.5.2 | Estado |
|---|---|---|---|
| 16:16 | módulo 28,5 (29877,0 → 29848,5) | E000001 16:16:33.762 módulo 28,50 | ✔ exacto |
| 16:17 | A Grande 9,1 (29848,5 → 29857,6) | A extiende a 29857,60 (tick 502, 16:17) | ✔ exacto |
| 16:18 | B Grande 14,6; AUT bajista; TT 29829,1 | E000007/9 seq 935 16:18:59.420; TT 29829,10 | ✔ exacto (H9: nivel 29845,79, B 29843,00) |
| 16:19 | nuevo 1 bajista local 7,5 (29850,0 → 29842,5) | E000014 16:20:00.145, módulo 7,50 | ⚠ valor correcto, **registro 29,4 s tardío** (mínimo real seq 1042, 16:19:30.741) |
| 16:20 | 2 confirmado (12,3 ≥ 7,5) | E000015 seq 1202 16:20:14.218, extremo 29837,30 (12,70) | ✔ causal |
| 16:21 | 3 confirmado, nuevo mínimo 29830,3 | E000028 seq 1446 16:21:14.734, nuevo extremo 29832,30; extiende a 29830,30 | ✔ causal |
| 16:22 | A 29830,3 → 29850,8 (20,5); AUT alcista al superar 29850,0 | E000042 seq 1809 16:22:52.576 (primer tick > 29850,00 del feed) | ✔ exacto |
| 16:23 | A 29850,8 → 29842,8 (seq 1846); B → 29852,6 (seq 1879); AUT alcista; luego AUT bajista | E000048 seq 1842; E000054 seq **1876** (29851,40); E000061 seq 2015 (primer cruce < 29842,80); 2062 = extremo | ✔/⚠ ver §3 y §4 |
| 16:24 | 29833,3 (2078) · 29838,0 (2107) · 29840,6 (2165) · 29828,1 (2259); A→B→AUT bajista | los 4 ticks coinciden; R0003 queda en B_GRANDE + TT_100 y se archiva; **el AUT bajista no aparece en la lectura primaria** | ✘ ver §4.3 |

Todos los `sequence_id` citados por el golden en 16:22–16:24 corresponden a ticks reales del feed (verificado uno a uno).

---

## 3. EL «PRIMER TICK DIVERGENTE» DECLARADO POR DS NO ES UNA DIVERGENCIA

DS declara primera divergencia en 16:23: motor AUT en seq **1876** (29851,40) frente a seq **1879** (29852,60) del golden.

Feed maestro:

```
seq 1875   16:23:10.376   29850,60
seq 1876   16:23:10.943   29851,40   <-- primer tick > 29850,80
seq 1879   16:23:12.154   29852,60   <-- máximo de la vela
```

- El umbral citado por el golden es «supera el inicio de A, 29850,8».
- El **primer** tick que lo supera es 1876; 1879 es el **extremo**, no el cruce.
- El motor fija `confirmation_sequence_id`/`knowledge_sequence_id` = 1876, `structural_sequence_id` = 1846 (nacimiento de A) y `confirmation_time` = 16:23:10.943. **Es causalmente exacto y tick-exacto.**

**Clasificación: `GOLDEN_INCOMPLETO`.** El golden no aporta el tick de cruce, solo el tick del máximo; la comprobación de DS compara contra el máximo y produce un falso negativo. La afirmación «el candidato falla el primer AUT exacto» **no se sostiene**.

Consecuencia práctica: el 8/9 y el `verdict: LECTURA_NO_REPRODUCIDA` **no pueden apoyarse en la comprobación 1879**. El veredicto de este informe se sostiene en otros hallazgos (§4, §5).

---

## 4. HALLAZGO PRINCIPAL: LA CAPA LOCAL VIOLA H16 (REGLA CERRADA)

### 4.1 Magnitud

| Métrica | v0.7.5.1 (base) | v0.7.5.2 (candidato) |
|---|---|---|
| Lecturas | 86 | **1.426** |
| Eventos | 1.399 | **6.559** |
| Eventos locales | 71 | **4.901** |
| AUT locales | 0 | **1.413** |
| Lecturas locales (LR) | — | **1.414 (LR0001 … LR1414) sin un solo evento de cierre/archivo** |

AUT locales por minuto (extracto): 16:23 → 5 · 16:24 → 11 · 16:26 → 13 · 16:29 → 17 · **16:30 → 41** · 16:33 → 33 · 16:40 → 32. Promedio ≈ 21/min.

### 4.2 Prueba de micromovimiento convertido en lectura

- Primer AUT local espurio: **E000066, seq 2033, 16:23:51.058**, LR0004, `B_LOCAL_SUPERA_ORIGEN_A`, módulo nuevo LR0005 = **2,30 puntos**.
- Primer módulo por debajo del umbral de ruido de fase (2,00): **E000082, seq 2066, 16:24:00.299**, LR0007 = **1,90 puntos**.
- En la sesión: **63 AUT locales con módulo < 2,00 puntos** (1,20 · 1,50 · 1,60 · 1,70 · 1,80 · 1,90).
- En 16:23–16:24 se abren **18 lecturas locales simultáneas** (LR0001…LR0018) sin cerrar ninguna.

### 4.3 Regla infringida (CERRADA, no provisional)

`REGLAS_CERRADAS.md` §C (líneas 169–179) y §H16 (líneas 368–373), DEC-011/DEC-015, **estado CERRADA**:

> «No se calculan ruido ni micromovimientos: no se clasifican, no se convierten en A, B, C, **AUT**, TT ni **nuevo 1** y **no ocupan lectura**; se descartan. La permanencia se decide por coherencia de movimiento, no por cada oscilación.»
> «La concurrencia es habitual: normalmente dos lecturas; excepcionalmente tres, **máximo operativo 3**.»
> «Una oscilación intravela **no** ocupa automáticamente una lectura.»

El candidato convierte cada oscilación en `A → B → AUT → nuevo 1 → lectura nueva`, sin filtro, sin cierre y sin tope de concurrencia. Es exactamente el contraejemplo que H16 prohíbe.

**Clasificación: `BUG_MOTOR` (bloqueante).** El umbral numérico ruido/movimiento (PR-g) está abierto; la prohibición de *clasificar* el micromovimiento **no** lo está.

### 4.4 Efecto sobre la comparación

La comprobación «16:24 A/B/AUT bajista» figura como **passed**, pero la lectura primaria R0003 **no emite AUT**: llega a B_GRANDE (24,50 / 22,30 = 109,9 %), TT_100 y se **archiva por MAX_3_ACTIVAS** (E000143, seq 2290). El AUT bajista solo existe en la capa local (11 en esa vela). Es decir: **la comprobación pasa por el ruido, no por la lectura.** El 8/9 no mide fidelidad funcional.

### 4.5 Terminología

El motor usa `LOCAL_MODULE` / `LOCAL_FUNCTION` / `AUT_LOCAL_CONFIRMADO` / `LRxxxx`. H10 (DEC-004, CERRADA) sustituye «local»/«superior» por **lectura 1 / lectura 2 / lectura 3**. No conformidad documental (no bloqueante por sí sola).

---

## 5. SEGUNDO HALLAZGO: CONTRADICCIÓN ABIERTA H9 ↔ GOLDEN (16:23 y 16:24)

### 5.1 16:23

- A Grande bajista = 29850,80 → 29842,80 = **8,00**.
- Nivel AUT cerrado (H9, DEC-003): 29842,80 + 1,27 × 8,00 + 0,25 = **29853,21**.
- Máximo real del feed: **29852,60** (seq 1879). Motor: 29851,40 (seq 1876).
- **Ninguno alcanza 29853,21.** Bajo H9 **no hay AUT**; el recorrido es B Grande sin AUT (H13(a)).
- El golden afirma AUT al «superar el inicio de A, 29850,8» = **100 %**, no 127 % + 0,25.

### 5.2 16:24

- R0003: A = 22,30; nivel AUT = 29852,60 − (1,27 × 22,30 + 0,25) = **29824,03**.
- Mínimo real: **29828,10** (seq 2259). **No se alcanza.** El motor aplica H13(a): B_GRANDE + TT_100, sin AUT.
- El golden afirma «A→B→AUT bajista» apoyándose en la base del módulo (100 %), no en 127 % + 0,25.

### 5.3 Lectura del hallazgo

El motor contiene **dos criterios de AUT incompatibles entre sí**:

- capa primaria: H9/H13 (127 % + 0,25) — correcta según regla cerrada;
- capa local: «B supera el origen de A» (100 %) — el criterio que usa el golden.

Y el golden usa el 100 % en 16:23 y 16:24, en contradicción con H9. DS reconoce la laguna en su propio artefacto: `rule_status: "criterio causal exacto de confirmación local AUT pendiente de formalización; no se ajusta el golden"`.

**Clasificación: `REGLA_ABIERTA` + `CONTRADICCIÓN` (H9/H13 ↔ golden, velas 16:23 y 16:24).** No es corregible por el motor ni por el auditor: requiere decisión de Javier. No se ajusta el golden.

---

## 6. OBSERVACIONES ADICIONALES

### D1 — Registro tardío del 1 local de 16:19 (`REGLA_ABIERTA`)
Mínimo 29842,50 en seq 1042/1044 (16:19:30.741); la lectura local se crea en E000014 a las **16:20:00.145** (primer tick de la vela siguiente). Valor correcto (7,50), instante no formalizado. No hay regla cerrada que fije el instante de confirmación de la lectura local.

### D2 — Atribución de la A Grande de 16:30/16:31 (`GOLDEN_INCOMPLETO` / `REGLA_ABIERTA`, persiste desde v0.7.5.1)
Motor: R0011, A = 29784,60 → **29812,90** (tick real seq 3827, 16:30:59.568). Golden: `FINAL_A = 29810,80` (apertura/máximo de 16:31) y sitúa el cruce «≈16:32:23 con tick 29811,80». Ambos usan ticks reales; la diferencia es de **atribución** (qué extremo cierra A Grande) y sigue sin resolverse. No se clasifica como BUG: falta la regla de cierre de A Grande más allá de DEC-010.

### D3 — Regresión R0062/R0064 no acreditable
En v0.7.5.1 existía la lectura **R0062 → R0064** (26 eventos, `mapped_ok`). En v0.7.5.2: `status: FAIL`, «not found in candidate output», `actual_primary_readings: 12`. Con 86 → 1.426 lecturas, el candidato **no reproduce la base v0.7.5.1**; la regresión no está demostrada y el salto de escala es, por sí mismo, incompatible con una evolución conservadora.

### D4 — Sin evidencia de generalidad
`PREFIX_REPORT: NOT_RUN_FULL_MATRIX`. No hay cierres físicos 75, ni cortes aleatorios 500, ni proceso nuevo por corte. `repro/run_prefix_matrix.py` existe pero no se ejecutó.

### D5 — Comparación no funcional
Las 9 comprobaciones son cadenas de texto («16:21 3 bajista») resueltas por presencia de eventos; una es falso negativo (§3) y otra es falso positivo por ruido (§4.4). No verifican `reading_id`, genealogía ni `sequence_id`.

---

## 7. VEREDICTO

**NO CONFORME — `LECTURA_NO_REPRODUCIDA`.**

- **Bloqueante:** `BUG_MOTOR` — la capa local convierte micromovimientos en A/B/AUT/nuevo 1 y lecturas (1.414 lecturas, 1.413 AUT, 0 cierres, 18 concurrentes en 16:24), contra H16/DEC-015 (CERRADA) y el tope de 3 lecturas.
- **Abierto:** `REGLA_ABIERTA` + contradicción H9/H13 ↔ golden en 16:23 y 16:24 (127 % + 0,25 frente a 100 %). Decisión de Javier.
- **No acreditado:** regresión v0.7.5.1 (R0062/R0064) y generalidad/prefijos (no ejecutados).
- **Descartado:** el «primer tick divergente» 1876 vs 1879 es un falso negativo del golden (§3).

El candidato **no puede aprobarse** ni sustituir a v2.12. No se modifica el golden ni las reglas.

---

## 8. LÍMITES DE ESTA AUDITORÍA

1. Contraste tick a tick **completo** solo en 16:15–16:24 (único tramo con detalle `sequence_id` en el golden). De 16:25 a 17:29 se verificaron agregados y coherencia interna del raw, no la exactitud de cada lectura primaria.
2. El umbral numérico ruido/movimiento (PR-g) sigue abierto: la infracción de H16 se acredita por el principio («no se convierten en AUT ni nuevo 1»), no por un corte de 2,00 puntos.
3. No se dispone de los enunciados originales de Javier, solo del árbol R1 y de las reglas cerradas.
4. Se **ejecutó** `repro/run_all.py` sobre la extracción limpia del ZIP vigente: raw idéntico (`cd5c6feb…`) y mismos conteos, lo que acredita determinismo del pipeline; no se editó ningún archivo del paquete.

---

## 9. RECOMENDACIONES A DS (sin autoridad sobre el contenido)

1. No publicar v0.7.5.2 como reproducción válida. Retirar la afirmación de «primer tick divergente en 1876».
2. Aplicar H16 con umbral cerrado por Javier, emitir cierre/archivo de lecturas y tope de 3 concurrentes.
3. No unificar el criterio de AUT local hasta que Javier resuelva H9 ↔ golden (16:23 y 16:24).
4. Reponer la comprobación R0062/R0064 contra la base v0.7.5.1 y ejecutar la matriz de prefijos completa antes de cualquier nueva entrega.
5. Sustituir `LOCAL_*` por la numeración `lectura 1/2/3` de H10.
