# INFORME DE TRASPASO — Auditoría técnica TM_CANON_v2_13_PROPUESTA.zip (Fase 1 documental)

- **Auditor:** TM supervisor MIMO (TM_PATCH_AUDITOR, independiente)
- **Fecha:** 2026-10-28
- **Solicitante:** DS TM BOSS (mensaje 09d21eb4-5413-4466-8d83-d661446d8617)
- **VEREDICTO TÉCNICO: APROBADO (Fase 1 documental)** con 2 observaciones no bloqueantes (B1, B2) y 1 limitación de verificación (L2). Sin reglas nuevas declaradas. Sin aprobación de Javier (queda en `ARBOL_v2_13_APROBADO_POR_JAVIER`).

## 1. Versión y hash verificados antes de abrir

| Campo | Esperado | Obtenido | Resultado |
|---|---|---|---|
| SHA-256 | A42274932680493CFEA99F0D8587258B11C61E7B7EC8C9FDB49322403FC01E3F | idéntico | OK |
| Tamaño | 306.875 bytes | 306.875 | OK |
| Entradas ZIP | 23 | 23 (`testzip` sin errores) | OK |

Paquete extraído en `audit_work\v213_pkg\` sin modificar ningún artefacto original.

## 2. Archivos revisados (23/23)

- Propuesta: `TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA.md` (153 líneas), `README_REPRODUCCION.md`, `DIFF_v2_12_a_v2_13_PROPUESTA.diff`.
- Evidencia: `TM_v2_13_REGISTRO_GOLDEN_HUMANO.csv` (75 filas), `TM_v2_13_REGLA_A_GOLDEN.csv`, `REGLAS_SUPERADAS.csv` (17 citas), `CONTRADICCIONES_RESUELTAS_Y_PENDIENTES.md`, `CLASIFICACION_CONTENIDO_v2_12.csv.md`.
- Controles: `manifest.json`, `SHA256SUMS.txt`.
- `source/` (10 archivos) y `historical/` (3 archivos): v2.12, dossiers v3/v4, golden v003, REGLAS_CERRADAS, REGLAS_PROVISIONALES, DECISIONES_EXPERTO, AGENTS.md, PREGUNTAS_PENDIENTES, LEEME, A00, A06, MANIFEST_ACTIVO_FASE0.

## 3. Comandos y pruebas ejecutadas

1. `Get-FileHash -Algorithm SHA256` del ZIP → hash/size/entradas (previo a abrir).
2. Verificación `SHA256SUMS.txt`: **22/22** archivos coinciden; 0 fallos.
3. Verificación `manifest.json`: 21/21 `files` con hash correcto; 23 = 21 payload + 2 controles (coherente con README y con la nota C-ZIP-01).
4. Snapshots `source/`+`historical/` vs autoridades vivas en disco (SHA-256): REGLAS_CERRADAS ✓, DECISIONES_EXPERTO ✓ (la única copia no idéntica es un snapshot histórico gubernamental antiguo, no la autoridad), AGENTS.md ✓, REGLAS_PROVISIONALES ✓, golden v003 ✓ (6/6, incluye `TM_CANON_ACTIVO\03_LECTURAS_HUMANAS`), árbol v2.12 ✓ (6/6), dossiers v3/v4 ✓ (3/3 y 3/3), A00 ✓, LEEME ✓, PREGUNTAS_PENDIENTES ✓ (8/8).
5. `REGLAS_SUPERADAS.csv`: **17/17** citas verificadas línea a línea contra los snapshots del paquete (archivo, número de línea y texto coinciden).
6. Diferencia: reconstrucción byte a línea desde `DIFF…diff`: lado antiguo = `historical/…v2_12.md` exacto (13.727 líneas); lado nuevo = propuesta exacta (153 líneas). 1 hunk; 13.621 borrados / 106 añadidos. 0 ficheros `.py` en el paquete; sin ejecución de motor/GOLDEN/tests declarada ni implícita.
7. Golden: 75 filas cubren 16:15–17:29 sin huecos; `source_state` A=14, B=13, C=0, D=48 = manifiesto = v003. Único desajuste de mi extracción automática: 16:38 (CSV=B); el v003 contiene etiquetas enfrentadas ([A] en resumen línea 65; [A/B] parcial en líneas 80/191). Es la contradicción documentada **C-GOLDEN-38**, resuelta a B por instrucción de fase: resolución correcta y trazable.
8. Verificación física PLANO-01 desde el feed canónico `TM_CANON_ACTIVO\02_TICKS\TM_TICKFEED_1615_1730.csv` (agregado 1 min, primer/último bid):
   - 16:16: +0,10 → PLANO ✓ (matriz: +0,1)
   - 16:20: −0,20 → PLANO ✓ (matriz: −0,2)
   - 16:23: +0,30 → **GAP** (≥0,25) ✓ (matriz: +0,3); estado A de 16:23 ✓ (v003 línea 509)
9. Coherencia de gobernanza: estado `CANDIDATO_PENDIENTE_APROBACION`; v2.12 permanece activo; gate `ARBOL_v2_13_APROBADO_POR_JAVIER`; Fase 2 no autorizada; `rules_pending_changed=false` (snapshot REGLAS_PROVISIONALES idéntico a la autoridad viva, es decir, sin editar); `items_excluded` (motor v0.7.5.2, AFS2, FT nuevas, REGLAS_PROVISIONALES) coherente con el contenido.
10. Entrega física: `TM_ENTREGAS\TM_CANON_v2_13_PROPUESTA\` es idéntica al ZIP (0 archivos de más, 0 de menos, 0 hashes distintos).

## 4. Resultados de la evaluación independiente frente a la revisión funcional

| Afirmación funcional | Verificación independiente MIMO |
|---|---|
| 17/17 citas de reglas superadas | Confirmado 17/17 (línea y texto) |
| Golden v003 idéntico a su autoridad | Confirmado (6 copias idénticas, incl. activa) |
| Árbol v2.12 idéntico a su autoridad | Confirmado (6 copias idénticas) |
| Discrepancia matriz PLANO-01 16:23 (+0,3) | Confirmada como **etiquetado**, no numérico: el gap +0,30 es correcto y es GAP (no plano); la fila `PLANO-01` lista 16:23 en `golden_minutes` con `golden_state=A` sin marcarlo como contraejemplo. El árbol §3 sí cita solo 16:16 y 16:20 como plano → coherente con la regla. |

## 5. Observaciones no bloqueantes

- **B1 (documental):** `TM_v2_13_REGLA_A_GOLDEN.csv`, fila `PLANO-01`: 16:23 (+0,3) es gap por ≥0,25 y debería etiquetarse expresamente como caso no-plano/contraejemplo; valores y estados son correctos.
- **B2 (codificación):** `?` literal reemplazando tildes en `manifest.json` («dem?s», «n?») y en el árbol §3 («direcci?n»). UTF-8 válido; solo cosmético.

## 6. Limitaciones

- **L2:** `source/MANIFEST_ACTIVO_FASE0.json` y `source/A06_Readiness_v0751.json` no tienen copia independiente localizable fuera del paquete (y sus entregas espejo): solo se pudo verificar su Integridad interna y su hash de manifiesto, no igualdad con una autoridad viva externa.
- **Alcance Fase 1:** paquete documental sin motor ni salida bruta — no se afirman ni evalúan pruebas de motor, prefijos, generalidad, causalidad, regresión ni AFS2. `AFS2_READY=false` sigue en pie; replay ciego y producción no autorizados.

## 7. Reglas abiertas afectadas

Ninguna nueva. P-DUDA-009, P-RUIDO-01, P-TT-FT-01, P-FT-02, P-CUT-03, P-CONC-04, P-GOLDEN-33 se preservan sin cambios en `REGLAS_PROVISIONALES.md`/`PREGUNTAS_PENDIENTES.md` (verificado por hash idéntico a las autoridades).

## 8. Recomendación

1. Enviar a Javier como candidato v2.13 con gate `ARBOL_v2_13_APROBADO_POR_JAVIER`; mientras no se apruebe, v2.12 sigue activo.
2. Corregir B1 (etiqueta de contraejemplo en PLANO-01) y B2 (mojibake) en la siguiente revisión del candidato — no requiere ZIP nuevo para auditar de nuevo si solo cambian esos dos ficheros.
3. Si se pretende traspasar L2, aportar la ruta viva de `MANIFEST_ACTIVO_FASE0.json` y `A06_Readiness_v0751.json` para cotejo de hash.
4. Este informe no sustituye la revisión funcional ni la aprobación de Javier.

*Archivos de apoyo: `audit_work\v213_pkg\` (extracción íntegra), `audit_work\check_v213.py`, `audit_work\check_plano01.py`.*
