# INFORME DE TRASPASO — Auditoría técnica TM_CANON_v2_13_PROPUESTA_R1.zip

- **Auditor:** TM supervisor MIMO (TM_PATCH_AUDITOR, independiente)
- **Fecha:** 2026-10-28
- **Solicitante:** DS TM BOSS (mensaje 614276b5-7af3-4393-ab0c-d0fda15e293c)
- **VEREDICTO TÉCNICO: APROBADO (Fase 1 documental R1)** — 0 defectos técnicos; 6 observaciones no bloqueantes (O1–O6); limitaciones de alcance. Sin reglas nuevas; sin aprobar en nombre de Javier (`ARBOL_v2_13_APROBADO_POR_JAVIER` pendiente; v2.12 sigue activo).

## 1. Hash congelado verificado antes de abrir

| Campo | Esperado | Obtenido | Resultado |
|---|---|---|---|
| SHA-256 | C79E6D49D039A8F78A436013DF71673B9150EE342CF68D303849B65C32D79C90 | idéntico | OK |
| Tamaño | — | 316.146 bytes | OK |
| Entradas | — | 27 (`testzip` sin errores) | OK |

`manifest.source_zip_sha256 = A4227493…01E3F` = ZIP R0 que audité yo mismo → cadena de procedencia verificada.

## 2. Alcance de cambios R0 → R1 (comparado contra mi extracción R0 auditada)

- Nuevos (5): `TM_ARBOL…_PROPUESTA_R1.md`, `DIFF_v2_13_inicial_a_R1.diff`, `DECISION_AUTORIDAD_PLANO_GAP_JAVIER.md`, `INFORME_CAMBIOS_R1.md`, `source/…PROPUESTA_INICIAL.md`.
- Renombrado: árbol base movido a `source/…_INICIAL.md` (hash `D385FFDF…87B7` = árbol R0 auditado ✓).
- Cambiados (5): `manifest.json`, `README_REPRODUCCION.md`, `SHA256SUMS.txt`, `TM_v2_13_REGISTRO_GOLDEN_HUMANO.csv`, `TM_v2_13_REGLA_A_GOLDEN.csv`.
- **17 archivos byte a byte idénticos** a R0, incluidos `DIFF_v2_12_a_v2_13_PROPUESTA.diff` ✓, `REGLAS_SUPERADAS.csv` (17 citas), `CONTRADICCIONES…`, `CLASIFICACION…`, `historical/` y todas las `source/` (salvo el nuevo snapshot INICIAL).

## 3. Pruebas ejecutadas (todas OK)

1. `SHA256SUMS.txt`: **26/26** hashes correctos; `manifest.files` **25/25** con hash+tamaño correctos; 27 = 25 payload + 2 controles; 0 ficheros sin declarar.
2. Diff inicial→R1: reconstrucción desde `source/…_INICIAL.md` con los 4 hunks → **idéntica al árbol R1 línea a línea (154/154)**.
3. Reproducción exacta del README (git apply con `core.autocrlf=false`): resultado `465886E3671E21A4B7C962A61CB4AA54C8AC8D4359C10FCE6B20E89D13C3EBC5` = árbol R1 del paquete = hash declarado en manifiesto → **byte a byte** ✓.
4. Diff recalculado con `difflib` (LF, n=3) == `DIFF_v2_13_inicial_a_R1.diff` guardado ✓; diff con 0 CRLF ✓.
5. B1 (PLANO-01): `golden_minutes` solo «16:16 (+0,1), 16:20 (-0,2)»; columnas nuevas `case_type/observed_difference/applied_boundary/case_result` registran «16:23 = contraejemplo / NO PLANO / >=0,25 / no abre en plano» ✓; árbol R1 §9 línea 130 lo repite ✓. Físicamente verificado en R0: +0,30 = GAP ✓.
6. B1-trazabilidad: `DECISION_AUTORIDAD_PLANO_GAP_JAVIER.md` presente, referenciada en `manifest.authority_decision`, árbol §0.1 y §3 ✓.
7. Golden: 75 filas 16:15–17:29 continuas, sin huecos ni duplicados ni lecturas vacías; vs R0 solo cambian 16:38/16:39 (`B` → `[A/B]` literal v003, nota ampliada); `canonical_status` intacto (14 completa / 13 parcial / 48 pendiente); golden v003 sin modificar (SHA `1E634EBB…104E5B` ✓).
8. P-RUIDO-01 sigue pendiente: `CONTRADICCIONES…` sin cambios, árbol §4 declara PENDIENTE, `rules_pending_changed=false` ✓.
9. `engine_tests_golden_feed_legacy_deliverables_modified=false`, `phase2_or_afs2_executed=false`, `items_excluded` sin cambios; 0 `.py` en el paquete; README declara que no incluye motor ✓.

## 4. Verificación independiente de los 5 puntos de Reader Validator

| # | Punto | Verificación MIMO |
|---|---|---|
| 1 | PLANO-01 retira 16:23 como ejemplo | **Confirmado** (fila, columnas nuevas y árbol §9) |
| 2 | Anexo de autoridad presente y referenciado | **Confirmado** (manifest, árbol §0.1/§3) |
| 3 | 16:38/16:39 `[A/B]` + parcial canónico | **Confirmado** (A=14/B=11/[A/B]=2/D=48; 14/13/48 canónico) |
| 4 | Conflicto de 2 puntos sigue abierto | **Confirmado** (§4 PENDIENTE, sin cambios en pendientes) |
| 5 | Diff LF aplicable con comando README | **Confirmado ejecutándolo**: hash `465886E3…EBC5` idéntico byte a byte |

Reader declara CONFORME con 4 observaciones menores: (i) anexo es reproducción redactada por DS, no artefacto original de Javier; (ii) `authority` de PLANO-01 no nombra el anexo; (iii) §4 conserva redacción «2 puntos exactos» junto a PENDIENTE; (iv) `manifest.golden.states` B=13 ≠ recuento literal 11+2. **Las cuatro coinciden con mi comprobación** y las acepto como no bloqueantes.

## 5. Observaciones del auditor (no bloqueantes)

- **O1 (redacción/atribución):** árbol R1 §9 línea 130: «apertura +0,3 …; **según v003**, `|Δ| >= 0,25`, por tanto NO PLANO». El +0,3 procede del feed y la frontera `>=0,25` de la regla expresa/anexo, **no del golden** — contradice la propia `interpretation_limit` de PLANO-01 («la frontera procede de la regla expresa, no se infiere del golden»). Sustituir «según v003» por «según regla expresa (anexo) y feed» eliminaría la ambigüedad.
- **O2 (manifiesto):** `manifest.candidate_tree = TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA.md` **no existe** en R1 (el real es `…_PROPUESTA_R1.md`, correcto en `manifest.files`). Campo heredado sin actualizar.
- **O3 (codificación, heredada de R0):** mojibake `?` literal en `manifest.json` («dem?s») y en ambos árboles §3 («direcci?n»). UTF-8 válido; solo cosmético.
- **O4:** naturaleza declarativa del anexo de autoridad (acepto la observación (i) de Reader): conviene ratificación explícita de Javier al aprobar.
- **O5:** `authority` de PLANO-01 no enlaza el anexo (observación (ii) de Reader).
- **O6:** etiqueta `[A/B]` de 16:39 es literal de la línea 80 del v003, mientras su detalle (línea 212) dice `[B]`; la parcialidad canónica no cambia. Conflicto literal interno del golden, ya bajo instrucción expresa — sin efecto.

## 6. Limitaciones

- Paquete documental Fase 1: **sin motor ni salida bruta** — no se afirman causalidad, prefijos, generalidad, regresión de motor ni AFS2 (`AFS2_READY=false`; replay ciego y producción no autorizados).
- Heredada L2: `source/MANIFEST_ACTIVO_FASE0.json` y `source/A06_Readiness_v0751.json` siguen sin copia local independiente fuera del paquete (integridad interna OK).
- El anexo `DECISION_AUTORIDAD_PLANO_GAP_JAVIER.md` no puede verificarse contra un original de Javier desde mi ámbito; se toma como declaración de DS (ver O4).

## 7. Reglas abiertas afectadas

Ninguna nueva. P-DUDA-009, P-RUIDO-01, P-TT-FT-01, P-FT-02, P-CUT-03, P-CONC-04, P-GOLDEN-33 intactos (hash de `REGLAS_PROVISIONALES.md`/`PREGUNTAS_PENDIENTES.md` sin cambios).

## 8. Recomendación

1. APTO para elevación a Javier con `ARBOL_v2_13_APROBADO_POR_JAVIER`; hasta entonces v2.12 permanece activo.
2. Corregir O1 y O2 (y opcionalmente O3–O5) en una eventual R2; no bloquean la aprobación.
3. Ratificar O4 (anexo de autoridad) en el acto de aprobación.
4. No sustituye la revisión funcional de Reader Validator ni la aprobación de Javier.

*Evidencia: `audit_work\v213r1_pkg\` (extracción), `audit_work\v213_pkg\` (R0), pruebas 1–9 de la sección 3.*
