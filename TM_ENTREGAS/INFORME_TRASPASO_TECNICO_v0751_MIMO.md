# Informe de traspaso técnico — auditoría v0.7.5.1 (ZIP corregido)

- Emisor: TM SUPERVISOR MIMO (auditoría técnica; sin permisos de edición sobre motor, tests, árbol, golden ni reglas).
- Fecha: 2026-10-28.
- Destinatarios: Copilot/Javier (decisión), copia a DS TM BOSS y TM_READER_VALIDATOR.
- Artefacto auditado: `deliverables_v0751_corrected_COMPLETE.zip`, SHA-256 `9ECF30117FF878EEE970F95096DA0337E0E026BA74EC1529A9B0D3FBC4473418` — **mismo ZIP** que el congelado por TM_READER_VALIDATOR (identidad verificada por hash).
- Coordinación: creado `C:\Users\profesor\tm\Teoria Modular\AGENT_COORDINATION.md` (no existía en ninguna parte).

## VEREDICTO: APROBADO (auditoría técnica), con observaciones no bloqueantes

Alcance: integridad del paquete, reproducción desde cero, hardcodes, generalidad, R0062↔R0064, golden solo-compara, causalidad y disponibilidad local. No autoriza replay ciego, AFS2 ni producción (`AFS2_READY=false`). No sustituye al veredicto funcional **CON RESERVAS** de Reader ni la decisión de Javier sobre F1/F2/F4.

## 1. Integridad (ítems 1 y 12)

- Extraído y verificado: 48 archivos = 46 manifestados + `manifest.json` + `SHA256SUMS.txt`.
- `SHA256SUMS.txt`: 47/47 hashes correctos. `manifest.json`: 46/46 correctos. 0 discrepancias, 0 archivos extra no justificados.

## 2. Ejecución desde cero (ítem 2)

`python repro/run_all.py` completo, `checks` 10/10 en `repro/REPORT.json`, `pass: true`:

| Check | Resultado |
|---|---|
| legacy_tests | **20/20 passed** (88 s) |
| corrected_tests | **7/7 passed** (5 s) |
| engine_counts | 86 lecturas / 1399 eventos / 62 gap / 1 secuencia local / 71 local_events |
| golden_22 | **22/22** |
| sample_prefix | 11 casos, 0 fallos |
| full_prefix (matriz) | **733 cortes, 0 fallos** (por clase: bar_close 75, random_500 500, local_before_availability 44, local_before_confirmation 46, local_after_confirmation 46, local_after_availability 44, R0062/R0064 114) |
| comparison | readings idénticos; 1411→1399 = **12 GAP <0,25 eliminados**; resto idéntico |
| r0062_r0064 | module/a/b/tt/ft + correspondencia: todos true |
| generality | 2 casos (mirror+precio+tiempo), pass |
| hardcodes | pass, 0 hits (ahora también escanea `repro/build_manifest.py`) |

Determinismo: regenerado el paquete y diff contra el ZIP original — `prefix_matrix_v0751.json` **idéntico byte a byte**; `v0751_Informe.json` solo cambia `generated_at`; `REPORT.json` solo duraciones de pytest; `hardcodes.json` solo la lista de archivos escaneados. Tras la ejecución, **fuentes intactas**: solo cambiaron logs y salidas regeneradas (`python/`, `tests/`, `data/`, scripts de auditoría = mismos hashes que `SHA256SUMS.txt`).

Nota de entorno: el primer intento agotó 15 min durante `pip install`+arranque (timeout mío, no del paquete); relanzado con log sin búfer completó todo sin incidencias.

## 3. Hardcodes (ítem 6)

Motor `python/TM_CORE_PYTHON_v0751_STREAMING.py`, barrido propio + `audit_v0751_hardcodes.py`:

- 0 precios golden (296xx/298xx), 0 horas 16:15–16:24, 0 IDs R00xx, 0 sequence_id fijos, 0 referencias a golden/lecturas_confirmadas, 0 rutas absolutas.
- Únicas constantes de hora: `WINDOW_START/END = 16:52:00/17:01:00` — son **parámetros CLI** (`--window-start/--end`) que solo filtran el CSV de comparación de lecturas; no son la ventana golden (16:15–16:24) ni alteran la lógica del motor.
- Constantes de dominio (`MOVE`, `PLANO_TICK=25`, `MIN_MODULE`, `MAX_ACTIVE`, …) expuestas en el `Informe.json`, no derivadas del CSV.

## 4. Generalidad (ítem 7)

`audit_v0751_generality.py`: transforma el feed real con espejo de precio (`2*mirror − p + shift`), desplazamiento de precio y de tiempo; **reconstruye barras y reejecuta `core.run_engine`**; aserta inversión de dirección, conservación de orígenes/extremos y desplazamiento temporal de confirmaciones. 2 casos → pass. No hay atajo ni salida prefabricada.

## 5. R0062 → R0064 (ítem 8)

`R0062_R0064.json`: `checks = {module, a, b, tt, ft}` todos `true`; `correspondence: true` entre ventana base (feed legacy `TM_TICKFEED_v010_LEGACY.csv`) y ventana completa (feed maestro). Corresponde a `audit_v0751_r0062.py`, que ejecuta el motor sobre ambos feeds.

## 6. Golden solo compara (ítem 10)

`audit_v0751_golden.py`: hace `core.load_feed` + `core.run_engine` y **compara** el resultado con `EXPECTED_LOCAL` y hitos de `lecturas_confirmadas_v003.txt` (presencia de texto). Los valores esperados viven en el script de auditoría y **no se inyectan al motor** (el motor no importa ni lee el golden: 0 referencias).

## 7. Causalidad y disponibilidad local (ítems 9 y 11)

- `detect_local_sequences(engine)` (motor L495): deriva solo de `engine.points`, `engine.bars` y `engine.movements`; imports del motor = stdlib únicamente; sin datos embebidos. Se ejecuta al final del streaming filtrando `confirmation_time <= known_time` (L1543+): en prefijos no se filtra ningún evento futuro.
- `v0751_LocalEventos.csv` (71 filas): `confirmation_time_ms <= knowledge_time_ms` en 71/71; todos los precios origin/extreme/module son ticks reales del feed (0 ausentes).
- `local_availability.json`: 71/71 con `availability >= confirmation` y `lag >= 0` (máx 69,3 s); `availability_index` monótono. Coherente con las clases `local_before_*` de la matriz (0 fallos en 180 cortes).
- Separación de tiempos del motor: `causality` del `Informe.json` → `all_knowledge_after_structural/confirmation = true`, `event_ids_append_only`, `sequence_ids_real_feed`.

## 8. Reproducción física independiente (sin motor)

Script propio sobre el CSV crudo (`audit_work/verify_phys.py`):

- Barra 16:15 desde ticks: high 29877,00 / low 29860,80 / rango 16,20 → **coincide** con las constantes golden.
- Barra 16:16: gap = +0,10 y open == high, rango 12,60 < 16,20 → **coincide** con «plano, no 2».
- Los 15 pares origen/extreme de `EXPECTED_LOCAL` existen como precios de tick reales.
- Los 12 gaps con 0 < |gap| < 0,25 del feed (10, −20, 20, 20, 10, 10, −20, −10, −10, 20, −10, 20) son **exactamente** los 12 eventos eliminados en la comparación. **0 gaps de exactamente 0,25** en el feed.
- Hitos del golden (`v0.03`, `16:19 = 1 bajista`, `16:22 = AUT alcista confirmado`, `16:24:49.819`) presentes en `lecturas_confirmadas_v003.txt`.

## 9. Diff revisado (v075 → v0751)

`diff/v075_to_v0751.diff` leído completo (524 líneas). Cambios: `VERSION` + `PLANO_TICK`; capa local (`LocalLeg/LocalSequence/_local_123/detect_local_sequences`); frontera de gap en `_schedule_gap` (`not bar.gap` → `abs(bar.gap) < PLANO_TICK`, coincide con «0,25 exactos o más NO son plano»); emisión de `local_events` con filtro de conocimiento; salidas CSV/Informe. Legacy `TM_CORE_PYTHON_v075_STREAMING.py` y `tests/legacy` sin tocar (hash idénticos al manifiesto).

## 10. Regresiones y fallos críticos

- **Ninguna regresión técnica**: 20/20 legacy intactos, readings idénticos, eventos restantes idénticos, matriz 733/0, golden 22/22.
- Sin fallos críticos técnicos. Los fallos funcionales F1–F4 (16:37, 16:31, 16:32, tope de lecturas) los clasificó TM_READER_VALIDATOR y quedan **pendientes de Javier**; no son defectos del parche GAP/local auditado aquí.

## 11. Reglas abiertas afectadas / observaciones (para Javier)

1. **A1 — yardstick del «2» local.** `_local_123` exige rango del 2 ≥ `span` (High−Low completo de la vela 1). REGLAS_CERRADAS A1 mide «desplazamiento direccional, no High−Low» para 1 y 2 en la capa de módulo; la capa local no tiene regla cerrada explícita. El golden local (15/15) y la matriz validan el comportamiento actual. Aclarar la regla de la capa local.
2. **A2 — redacción del umbral plano.** Implementado y brief de MiMo: plano si `|gap| < 0,25` (0,25 exacto = gap). H14 en REGLAS_CERRADAS dice `≤ 1 tick` = plano. Sin efecto práctico en este feed (0 gaps de 0,25 exacto), pero conviene unificar la redacción.
3. **Docstring local.** Dice «tamano >= 1»; el código exige `>= span`. El código sigue A1(b) «rango de 2 ≥ rango de 1»; corregir el docstring.
4. **`knowledge_time` local = `confirmation_time`.** La disponibilidad real se analiza aparte (`local_availability`, lag ≤ 69,3 s, monótono). Diseño documentado y causal; sin acción.
5. Pendientes declarados por el propio motor en el `Informe.json` (`post_tt_fallido_no_definido`, `ft_expiracion_no_definida`, `aut_extra_tick_unidad_cerrada_0_25`, …) — coherentes con «no inventar reglas abiertas».

## 12. Casos mínimos reproducibles

1. Frontera plano: barras con gap ∈ {10, −20, 20, …} → sin evento gap; gap ≥ 25 → evento. (Feed: 12 casos <0,25, 0 casos =0,25.)
2. Prefijo sin fugas: corte en `availability_index` anterior al cierre de barra → la clase `local_before_availability` no contiene eventos locales (44/44 cortes).
3. Generalidad: `mirror=3_000_000, price_shift=12_345, time_shift=7_200_000 ms` → direcciones invertidas, roundtrip de precios correcto (caso 1 de `generalidad_sintetica.json`).
4. Físico: recomputar 16:15/16:16 solo con el CSV crudo → mismos valores golden (script `audit_work/verify_phys.py`).

## 13. Recomendación concreta

1. **Aceptar en el carril técnico** el parche v0.7.5.1 (`9ECF3011…3418`): reproducible, sin hardcodes, causal, con tests previos intactos.
2. Elevar a Javier las decisiones F1, F2, F4 (Reader) y las observaciones A1/A2 (MiMo); toda corrección exige versión v0.7.5.2 y ZIP nuevos.
3. No promover a replay ciego, AFS2 ni producción hasta el cierre de F1/F2/F4 y nueva auditoría.
4. Publicado `AGENT_COORDINATION.md` en la raíz del proyecto para las siguientes cadenas.
