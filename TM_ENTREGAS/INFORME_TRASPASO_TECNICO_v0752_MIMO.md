# INFORME DE TRASPASO TÉCNICO — MOTOR v0.7.5.2 (TM_CORE_v0752_CANONICAL)

**Auditor:** TM supervisor MIMO (auditor independiente)
**Fecha:** 2026-10-28
**Objeto:** `TM_CORE_v0752_CANONICAL.zip` (candidato de DS TM BOSS)
**Golden:** `TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v003.txt`
**Autoridad:** árbol R1 embebido + REGLAS_CERRADAS (gate `ARBOL_v2_13_APROBADO_POR_JAVIER` pendiente; v2.12 sigue activo)
**Modo:** solo lectura. No se editó motor, tests, golden, árbol ni reglas. `AFS2_READY=false` (no declarado).

---

## 0. CONTROL DEL ARTEFACTO — HALLAZGO C1 (discrepancia de hash declarado)

| Elemento | Valor |
|---|---|
| SHA-256 **declarado por DS** en su convocatoria | `3d066f6a054b5183c1c57ca8e404382b2fac455b93b20909c2f55b562507c0ab` |
| SHA-256 **real del ZIP** (ambas copias en disco) | `3380c0a82b779ec1e49d8270687f3e3e7627a524c16d8347c70c489107b7892a` |
| Tamaño | 1.356.866 B · 25 entradas (23 payload + manifest + SHA256SUMS) |
| SHA256SUMS | 24/24 OK · manifest.files 23/23 hash+tamaño OK |
| manifest.verdict | `LECTURA_NO_REPRODUCIDA` (auto-declarado por DS) |

**C1:** el hash que DS cita en la convocatoria **no corresponde al ZIP entregado**. El informe funcional de Reader (§0) documenta el re-sellado (hash antiguo `3d066f6a…c0ab` descartado para incluir selftest+transformaciones en `run_all.py`) y que Reader verificó `3380c0a8…7892a` antes de abrir. **Se audita el ZIP vigente `3380c0a8…7892a`** (mismo que Reader); se pide a DS **ratificar por escrito el hash congelado vigente**.

**Autenticaciones de entrada (verificadas por este auditor):**
- Feed `data/TM_TICKFEED_1615_1730.csv` = canónico `02_TICKS`, SHA-256 `5F701BE2…2C9FF` idéntico. ✓
- `legacy_frozen/TM_CORE_PYTHON_v0751_STREAMING.py` = motor v0.7.5.1 real (`4A2877CC…DEFE2`, byte a byte). ✓ (base del diff autenticada)
- `authority/TM_ARBOL_MAESTRO_…_R1.md` = `465886E3…3ECBC5` = contenido canónico aplicado R1 verificado en la auditoría R1 previa. ✓
- Motor candidato: 104.102 B, SHA-256 `01658c10…0b0db51`.

---

## 1. REPRODUCCIÓN INDEPENDIENTE (ejecutada por este auditor)

`python -u repro/run_all.py` sobre la extracción limpia (salida redirigida a `run_all.log`):

- **exit code = 2** (esperado: `LECTURA_NO_REPRODUCIDA`, declarado en README).
- **Los 8 outputs regenerados son BYTE A BYTE IDÉNTICOS** a los entregados (`CORE_RAW_OUTPUT`, `GOLDEN_COMPARISON`, `HARDCODE_SCAN`, `PREFIX_REPORT`, `R0062_R0064`, `RUN_SUMMARY`, `SELFTEST`, `TRANSFORMATION_TESTS`). SHA-256 crudo: `cd5c6feb858dbdd6d31fd39ee7c3085e8d56d93f82b5e8d8ba39a81c9d1f31d7` en ambas ejecuciones.
- Conteos: feed 20.335 · eventos 6.559 · lecturas 1.426 · eventos locales 4.901 · secuencias locales 1 · `R0062_R0064: []`.
- SELFTEST 8/8 PASS · TRANSFORMATIONS PASS (2.297 puntos, sin hardcodes) · `raw_unchanged: true` en la comparación.
- Golden 8/9, `first_failure: "16:23 AUT alcista en secuencia estructural v003 1879"`.
- El motor declara por sí mismo `coverage geometric=False functional=False`.

**Conclusión: pipeline determinista y reproducible de extremo a extremo. Acreditado.**

---

## 2. VERIFICACIÓN INDEPENDIENTE DE LOS HALLAZGOS DE READER

Todos los números de Reader reproducidos con mis propias consultas sobre el raw y el feed:

| Hallazgo de Reader | Verificación MIMO | Estado |
|---|---|---|
| 1.413 AUT locales | `new_state=AUT_LOCAL_CONFIRMADO` = 1.413; `function=AUT` = 1.413 | ✓ VERIFICADO |
| 1.414 LR (LR0001…LR1414), **0 cierres** | 1.414 LR creadas; estados finales locales: LOCAL_A 1 + LOCAL_B_GRANDE 898 + LOCAL_MODULE 515 = 1.414; eventos de cierre sobre LR = **0** (ARCHIVADA/CUT solo tocan R00xx primarias; `operational_valid=1` = 0) | ✓ VERIFICADO |
| 18 LR abiertas simultáneas en 16:23–16:24 | LR0001…LR0018 abiertas sin cerrar (LR0003–LR0018 = 16 creadas dentro de 16:23–24); supera el tope 3 de H16 | ✓ VERIFICADO |
| 63 AUT locales con módulo < 2,00 pt | recuento exacto = 63 (total eventos locales con módulo < 200 = 185; mínimo 0,50 pt) | ✓ VERIFICADO |
| R0062/R0064 no reproducidos | `R0062_R0064.json: FAIL, not found`, primarias = 12; en v0.7.5.1 existían (auditoría previa: correspondencia 5/5 con ventana legacy) | ✓ VERIFICADO |
| `PREFIX_REPORT: NOT_RUN_FULL_MATRIX` | contenido del fichero entregado = `NOT_RUN_FULL_MATRIX` (75 cierres + 500 aleatorios + proceso nuevo requeridos, no ejecutados) | ✓ VERIFICADO |
| Cap MAX_ACTIVE=3 solo aplica a primarias | en el diff: `primary_active` excluye locales (`local_sequence_id`) de archivado por capacidad y de A_DESPROPORCIONADA — base literal del breach de concurrencia | ✓ VERIFICADO EN CÓDIGO |
| §3: 1876 vs 1879 es falso negativo del golden | feed físico: seq 1875 bid 29850,60 · **seq 1876 bid 29851,40 (16:23:10,943) = primer tick > 29850,80** · seq 1879 bid 29852,60 = extremo. El motor confirma en el cruce real; la comprobación de DS compara contra el extremo | ✓ VERIFICADO EN FEED |
| §5: contradicción H9/H13 ↔ golden 16:23 y 16:24 | aritmética: 29842,80 + 1,27×8,00 + 0,25 = **29853,21** > máximo real 29852,60 → bajo H9 **no hay AUT**; el golden afirma AUT con criterio 100 %. El motor usa 100 % en capa local, H9 (127 %) en primaria: dos criterios incompatibles. El propio artefacto lo declara (`rule_status: criterio causal… pendiente de formalización`) | ✓ VERIFICADO (decisión = Javier) |
| D2: atribución A Grande 16:30/16:31 | persiste igual que en v0.7.5.1; atribución sin regla cerrada de cierre de A Grande | ✓ ADOPTADO |
| D3: regresión 86 → 1.426 lecturas no acreditada | además, **el feed legacy `TM_TICKFEED_v010_LEGACY.csv` NO está en el paquete** → R0062/R0064 no son testables dentro del propio candidato | ✓ VERIFICADO (refuerzo) |

**Ningún hallazgo de Reader quedó sin confirmar.** El bloqueante `BUG_MOTOR` (capa local convierte micromovimientos en A/B/AUT/nuevo 1 y lecturas sin filtro, sin cierre y sin tope, contra H16/DEC-015 CERRADAS) queda **acreditado por evidencia primaria propia**.

---

## 3. CAUSALIDAD POR PREFIJOS (contribución propia, muestra acotada)

El paquete **no** ejecutó su matriz (`NOT_RUN_FULL_MATRIX`). Este auditor ejecutó un muestreo independiente con la misma metodología exigida (truncado físico del feed + proceso nuevo por corte + igualdad de firmas de eventos del prefijo de conocimiento):

- **Muestra principal: 14 cortes** — 6 cierres de vela repartidos por la sesión, 4 aleatorios (seed 7552), 4 en torno a la divergencia (1875/1876/1879/1880) → **14/14 PASS**.
- **Suplemento: 12 cortes** — antes/en/después de las primeras confirmaciones locales A (1620), AUT (1809), 2 (1202), 3 (1446) → **12/12 PASS**.
- **Total: 26/26 PASS, 0 fallos.** Evidencia: el motor no usa ticks futuros; la salida hasta cada corte es idéntica al prefijo correspondiente de la salida completa, **incluida la zona de la divergencia 16:23**.

**Limitación:** la matriz completa (≈600–1.000 cortes, cortes tardíos de 60–80 s) excede un tiempo de auditoría acotado (>10 h). La causalidad por prefijo queda **acreditada por muestra**, no por la matriz total. Artefacto: `audit_work\prefix_sample_v0752_supp\SUPPLEMENT.json` + log de 26 cortes.

---

## 4. HARDCODES Y REVISIÓN DEL DIFF v0.7.5.1 → v0.7.5.2

**Escaneo independiente sobre el código del motor** (no el auto-reportado):
- Literales prohibidos (precios 296xxxx–298xxxx, horas 16:xx/17:xx, `sequence_id` 18xx, ids `R00xx`, sentinels 1879/2985260/2985321/R0062/R0064/2981080/2981180): **0 coincidencias**.
- Imports: solo stdlib (`argparse, collections, csv, dataclasses, datetime, hashlib, json, math, pathlib, pickle, sys, tempfile, typing`). ✓
- `HARDCODE_SCAN.json` entregado: 26 literales, 0 hits — consistente con mi escaneo. ✓

**Diff (base autenticada = motor v0.7.5.1 byte a byte):** 14 hunks, ~372+/256−, un solo fichero (el motor). Cambios sustantivos:
1. **Elimina `detect_local_sequences` retrospectivo** (se calculaba al final del feed sobre barras completas → uso potencial de futuro) y lo sustituye por procesamiento local **incremental en estado** (`_process_local_sequence`, `_make_local_reading`, `_local_leg`, `_observe_core_aut`, `_new_local_reading_after_aut`, + streaming/serialize/restore, +363 líneas). **Mejora de causalidad real.**
2. **Cap `MAX_ACTIVE=3` restringida a lecturas primarias** (locales exentas) → causa directa de las 1.414 LR sin cerrar y la concurrencia >3. Origen literal del breach H16.
3. **Elimina el hardcode `WINDOW_START/END = 16:52–17:01`** que existía en v0.7.5.1. **Mejora.**
4. Añade `2`,`3` a `FUNCTION_LABELS`; importa `pickle` (serialize_state). Sin cambios ocultos en otras áreas.

---

## 5. ANÁLISIS DEL ÚNICO FALLO DEL GOLDEN (8/9)

- El fallo `16:23 AUT alcista … v003 1879` compara contra el **extremo** (1879, 29852,60); el **cruce** del umbral del propio golden («supera el inicio de A, 29850,8») ocurre en **1876 (29851,40)**, que es donde el motor confirma, con `structural=1846`, `confirmation=1876`, `knowledge_price=2985140`. Verificado tick a tick en el feed. **La comprobación es un falso negativo** (clasificación `GOLDEN_INCOMPLETO`, coherente con Reader §3).
- Pero, independientemente, **bajo H9 el AUT de 16:23 no debería existir** (nivel 29853,21 inalcanzable) y el golden lo afirma con criterio 100 %; ídem 16:24. **La contradicción H9/H13 ↔ golden es real, está aritméticamente verificada y requiere decisión de Javier** (`REGLA_ABIERTA` + `CONTRADICCIÓN`). No se ajusta el golden ni las reglas.

---

## 6. VEREDICTO

**NO CONFORME — el candidato NO PUEDE sustituir la base (v2.12 activa).** Motivos bloqueantes/abiertos:

1. **`BUG_MOTOR` (bloqueante, regla cerrada):** la capa local infringe H16/DEC-015 — micromovimientos convertidos en A/B/AUT/lecturas (1.414 LR, 1.413 AUT, 63 con módulo <2 pt, 0 cierres, 18 concurrentes en 16:24, tope 3 exento por código).
2. **`REGLA_ABIERTA` + `CONTRADICCIÓN`:** H9/H13 (127 %+0,25) ↔ golden (100 %) en 16:23 y 16:24. Decisión de Javier.
3. **Regresión v0.7.5.1 no acreditada:** R0062/R0064 ausentes y feed legacy fuera del paquete; salto 86 → 1.426 lecturas sin demostración conservadora.
4. **Generalidad:** matriz de prefijos completa no ejecutada por DS; muestra independiente 26/26 PASS no sustituye el requisito total.
5. **C1:** discrepancia del hash congelado declarado por DS.

**Lo que SÍ queda acreditado (positivos técnicos):** reproducción determinista byte a byte (8/8 outputs), autenticación de feed/base/autoridad, 0 hardcodes (escaneo doble), selftest y transformaciones PASS, mejora causal real (detector retrospectivo → streaming en estado), eliminación del hardcode de ventana, muestra de causalidad por prefijo 26/26 PASS, y la corrección del «falso negativo 1879» (§5).

**No se declara `AFS2_READY`. No se autoriza replay ciego ni producción. Gate `ARBOL_v2_13_APROBADO_POR_JAVIER` pendiente (v2.12 vigente).**

---

## 7. LÍMITES DE ESTA AUDITORÍA

1. Muestra de prefijos acotada (26 cortes), no matriz completa (>10 h inviable).
2. Contraste tick a tick fino solo en 16:15–16:24 (único tramo con detalle en el golden); de 16:25 a 17:29 se verificaron agregados y coherencia interna.
3. La infracción H16 se acredita por principio de regla cerrada («no se convierten en AUT ni ocupan lectura»); el umbral numérico PR-g sigue abierto.
4. Sin acceso a los enunciados originales de Javier (solo árbol R1 + reglas cerradas + decisiones).
5. `3d066f6a…c0ab` no está disponible para diff de contenido: C1 se reporta como discrepancia de declaración, no de payload (Reader documenta 25/25 idénticos entre extracciones).
6. Todos los scripts se ejecutaron sobre una copia de trabajo ajena al árbol canónico; el ZIP y el árbol no se modificaron.

---

## 8. RECOMENDACIONES A DS (sin autoridad sobre el contenido)

1. Ratificar por escrito el hash congelado vigente `3380c0a8…7892a` (C1) y corregir la convocatoria.
2. No publicar v0.7.5.2 como reproducción válida ni sustituta de v2.12; corregir o retirar la afirmación de «primera divergencia en 1879» (es falso negativo verificado).
3. Remediar el breach H16 (cierre/archivo de LR, tope de concurrencia aplicado a todas las lecturas, filtro de micromovimientos) — o esperar a que Javier cierre H16/PR-g.
4. No unificar criterios de AUT hasta que Javier resuelva H9/H13 ↔ golden (16:23 y 16:24).
5. Reponer la regresión R0062/R0064 con feed legacy incluido en el paquete.
6. Ejecutar `repro/run_prefix_matrix.py` completo antes de pedir validación de generalidad (muestra MIMO 26/26 PASS como evidencia interina).
