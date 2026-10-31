# Auditoria canonica v0.7.5

## Alcance

- Motor auditado: v0.7.5, inmutable.
- Feed maestro: 20.335 ticks, 16:15:00.016-17:29:59.897, 75 velas.
- Feed anterior: 11.120 ticks, 16:20:00.145-17:00:59.931, 41 velas.
- Tramo comun exacto tick a tick; IDs nuevos con offset fijo `+1145`.
- Golden humano: `TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v002.txt`.
- Arbol: `TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_14.md` con parches v2.13/v2.14.

## Resultados

### PASS

- Carga del feed y monotonia temporal.
- Tramo comun: 11.120/11.120 ticks identicos; 873/873 eventos; 67/67 lecturas.
- R0062 base -> R0064 ampliado: 26/26 eventos, geometria, tiempos, TT y FT exactos.
- Prefijos fisicos: 3327 cortes, 0 fallos.
- R0062: 1782 cortes, 0 fallos.
- Invariantes causales: event_id append-only, sequence_id real, knowledge_time valido, TT despues de B Grande, target TT correcto.
- `plano_gap` solo aparece como hallazgo, no como PASS.

### HALLAZGOS BLOQUEANTES

1. **GAP espurio**: 74 GAP observados frente a 62 esperados; 12 falsos positivos con `|gap| < 0.25`.
   Casos iniciales 16:16 (`+0.10`) y 16:20 (`-0.20`). El motor lanza GAP con cualquier `bar.gap != 0`.
2. **Golden humano 1/8**: fallan 16:15, 16:16, 16:17, 16:19, 16:20, 16:21 y 16:22.
   - 16:16: GAP en lugar de plano/modulo por descarte.
   - 16:17: A se emite inicialmente hasta 29856.30; se extiende a 29857.60 solo al confirmar B_FALLIDA en 16:18.
   - 16:19: emite C/A alcistas; el humano pide continuacion bajista y lectura local en revision.
   - 16:20: GAP por -0.20 y no reconoce el posible 2.
   - 16:21: solo GAP; no reconoce el posible 3.
   - 16:22: no forma A Grande alcista 29830.30->29850.80 en la vela; emite AUT/TT sobre una lectura bajista distinta.
3. **Fin de feed**: 72 movimientos estructurales no explicados y 0 `PENDIENTE_POR_REGLA`.
   No se puede declarar cobertura completa ni `pending=[]`.
4. **Estados FT**: 37 patrones FT, 0 canonicos. Todos usan `CONFIRMADO`; faltan los estados finales v2.13/v2.14.
5. **Cobertura**: 2166/2238 swings funcionales causales; 434/20335 ticks sin owner.
   Razones: `PRECIO_FUERA_RANGO_ACTIVO` 421, `PRE_LECTURA` 6, `SIN_LECTURA_ACTIVA` 7.
6. **CLI con barras completas**: `--start` reconstruye las 75 velas y produce 874 eventos;
   aparece GAP espurio en 16:20. La regresion estricta del tramo comun es 873/873.

### NO BLOQUEANTE PARA CAUSALIDAD

- Prefijos fisicos: el motor no usa futuro; todos los cortes reproducen eventos y lecturas conocidas.
- R0062: la correspondencia por geometria/tiempo es exacta; no usar IDs entre feeds.
- R0001 anterior no tiene equivalente exacto en el feed ampliado; queda sin mapeo y documentado en `A03`.

## Veredictos

Ver `out_v075_audit2/R00_Readiness.json`.

- `CAUSAL_ENGINE_READY=true`
- `PREFIX_INVARIANCE_READY=true`
- `GEOMETRY_REGRESSION_READY=true`
- `CANONICAL_GOLDEN_READY=false`
- `PLANO_GAP_READY=false`
- `FT_FINAL_STATE_READY=false`
- `END_FEED_INTEGRITY_READY=false`
- `FUNCTIONAL_COVERAGE_COMPLETE=false`
- `OWNER_COVERAGE_COMPLETE=false`
- `OPEN_RULES_PRESENT=true`
- `AFS2_EXPERIMENTAL_READY=false`
- `AFS2_PRODUCTION_READY=false`

## Invariantes de la auditoria

- No se modifico el motor ni sus tests.
- No se creo una version nueva.
- No se desarrollo AFS2.
- Las reglas abiertas no se cerraron por inferencia.
- Los informes conservan hashes y evidencia de ejecucion.
