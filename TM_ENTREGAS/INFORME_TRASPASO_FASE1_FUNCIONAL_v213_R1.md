# Informe de traspaso — auditoría funcional R1 (v2.13)

- Emisor: TM_READER_VALIDATOR. Solo lectura; sin edición de motor, tests, árbol, golden ni reglas.
- Fecha: 2026-10-28.
- Artefacto: `TM_CANON_v2_13_PROPUESTA_R1.zip`.
- Hash verificado **antes de abrir**: `C79E6D49D039A8F78A436013DF71673B9150EE342CF68D303849B65C32D79C90` — 316.146 bytes, 27 entradas. Coincide con el declarado.
- Estado declarado: `CANDIDATO_PENDIENTE_AUDITORIA_MIMO_Y_APROBACION_JAVIER`.

## 1. Integridad

| Comprobación | Resultado |
|---|---|
| SHA-256 del ZIP | `C79E6D49…9C90` ✓ |
| Entradas físicas | 27 = 25 payload + `manifest.json` + `SHA256SUMS.txt` ✓ |
| `SHA256SUMS.txt` | 26/26 OK, 0 ausentes, 0 alterados ✓ |
| `manifest.json` | 25/25 hashes correctos; `file_count=25`, `archive_physical_count_expected=27` ✓ |
| `source_zip_sha256` | `A4227493…01E3F` = ZIP R0 auditado ✓ |

## 2. Los cinco puntos solicitados

| # | Requisito | Resultado |
|---|---|---|
| 1 | PLANO-01 retira 16:23 de ejemplos y lo registra como contraejemplo NO PLANO | **Cumple**. `golden_minutes` = «16:16 (+0,1), 16:20 (-0,2)»; `case_type` = «16:23 = contraejemplo / caso de NO PLANO»; `observed_difference` = «+0,3»; `applied_boundary` = «\|apertura-cierre anterior\| >= 0,25»; `case_result` = «no abre en plano». El árbol R1 §9 línea 130 lo repite como contraejemplo. |
| 2 | Decisión de autoridad anexa | **Cumple**. `DECISION_AUTORIDAD_PLANO_GAP_JAVIER.md` (464 B), referenciada en `manifest.authority_decision`, en el árbol §0.1 línea 8 y §3 línea 62. |
| 3 | 16:38/16:39 conservan `source_state` literal `[A/B]` y estado canónico parcial | **Cumple**. Registro: `source_state=[A/B]`, `canonical_status=CONFIRMADA_PARCIAL`, `note` explica que la parcialidad se conserva por instrucción expresa. Recuento: `source_state` A=14 / B=11 / `[A/B]`=2 / D=48; `canonical_status` 14 completa / 13 parcial / 48 pendiente. |
| 4 | Conflicto de 2 puntos sigue pendiente | **Cumple**. `CONTRADICCIONES_…md` sin cambios (P-RUIDO-01 sigue pendiente); árbol §4 línea 78 declara «La aplicación general de un umbral de 2 puntos queda **PENDIENTE** de reconciliación expresa con DEC-015»; `rules_pending_changed=False`. |
| 5 | Diff LF aplicable con el comando del README | **Cumple**. `DIFF_v2_13_inicial_a_R1.diff` con 0 CRLF. Ejecutado el procedimiento del README tal cual (`git -c core.autocrlf=false apply --ignore-space-change --ignore-whitespace`, exit 0): resultado `465886E3671E21A4B7C962A61CB4AA54C8AC8D4359C10FCE6B20E89D13C3EBC5`, 13.008 B — idéntico al árbol R1 y al hash declarado en el manifiesto. |

## 3. Golden y fuentes exactos (no inferidos, no alterados)

| Archivo | SHA-256 | Estado |
|---|---|---|
| `source/…v003.txt` | `1E634EBB…104E5B` | idéntico al golden vigente y al del ZIP de motor ✓ |
| `historical/…v2_12.md` | `07880B12…F997A8` | idéntico al v2.12 activo ✓ |
| `source/…PROPUESTA_INICIAL.md` | `D385FFDF…87B7` | idéntico al árbol R0 auditado ✓ |
| `source/AGENTS.md` | `83309F96…B2D6` | idéntico al del proyecto ✓ |
| `source/DECISIONES_EXPERTO.md` | `A3B3B053…D6EC` | idéntico al activo ✓ |
| `source/REGLAS_CERRADAS.md` | `B5FDBB3E…C1F2` | idéntico al activo ✓ |
| `source/REGLAS_PROVISIONALES.md` | `BB992BDD…D536` | idéntico al activo ✓ |
| `source/PREGUNTAS_PENDIENTES.md` | `62FFE3D1…EF2F` | idéntico al activo ✓ |
| `source/00_LEEME_…txt` | `AF82AE96…9F23` | idéntico al del proyecto ✓ |

Comparación R0 → R1: solo cambian `manifest.json`, `README_REPRODUCCION.md`, `SHA256SUMS.txt`, el árbol (renombrado a `_R1`), el registro golden y la matriz PLANO-01; se añaden el anexo, el informe de cambios, el diff y `source/…_INICIAL.md`. `CONTRADICCIONES`, `REGLAS_SUPERADAS` (17 filas), `CLASIFICACION_CONTENIDO`, `historical/` y todas las fuentes quedan **byte a byte sin cambios**.

## 4. Verificación de no-regresión documental

- Registro: 75 filas consecutivas 16:15–17:29, sin huecos ni duplicados; 0 lecturas vacías.
- El árbol conserva el bloque 16:15–16:24 con 16:16 plano (+0,1), 16:19–16:21 = 1-2-3, 16:22 AUT, 16:23 NO PLANO.
- §3 fija `PLANO ⇔ |Δ| < 0,25` y `GAP ⇔ |Δ| ≥ 0,25` y declara la sustitución global de `≤ 0,25`.
- §4 mantiene el umbral de 2 puntos como diferencia documental no resuelta; no se amplían reglas ni se toca `REGLAS_PROVISIONALES.md`.
- Manifiesto: `engine_tests_golden_feed_legacy_deliverables_modified=False`, `phase2_or_afs2_executed=False`.

## 5. Observaciones menores (no bloqueantes)

1. **Naturaleza del anexo de autoridad.** `DECISION_AUTORIDAD_PLANO_GAP_JAVIER.md` es una reproducción redactada por DS («recibida el 2026-10-28»), no un artefacto original de Javier (mensaje, captura o firma). Documenta la instrucción, pero la trazabilidad sigue siendo declarativa. No es defecto del entregable; sí conviene que Javier lo ratifique al aprobar.
2. **Enlace desde la matriz.** La columna `authority` de `PLANO-01` sigue citando «Instrucción v2.13; DEC-013» sin nombrar el anexo; el árbol sí lo cita (§0.1 y §3). Enlace incompleto, sin efecto funcional.
3. **Redacción residual del umbral.** El árbol §4 sigue describiendo «2 puntos exactos como umbral de confirmación retroactiva» al citar la instrucción de fase, aunque acto seguido lo declara PENDIENTE. Riesgo de lectura como regla cerrada si se cita fuera de contexto.
4. **Etiqueta del manifiesto.** `manifest.golden.states` informa B=13, que en el registro corresponde a 11 `B` + 2 `[A/B]` bajo `canonical_status=CONFIRMADA_PARCIAL`. Es coherente, pero el nombre `states` no distingue etiqueta literal de estado canónico.

## 6. Límites

- El ZIP sigue **sin motor ni salida bruta**: no se acredita causalidad, prefijos, generalidad ni regresión de motor.
- Auditoría exclusivamente documental; no se ejecutaron tests de motor.
- No se infirió ninguna regla desde el golden: la frontera 0,25 se toma de la regla expresa y del anexo, y el golden solo aporta 16:16, 16:20 y el contraejemplo 16:23.

## 7. Veredicto funcional

**CONFORME en los cinco puntos solicitados** — 0 defectos funcionales, 4 observaciones menores no bloqueantes. **Apto para auditoría técnica de MiMo**, con la aprobación de Javier aún pendiente. No autoriza replay ciego, AFS2, producción ni Fase 2, y no modifica la base activa v2.12.
