# Informe de cambios — v2.13 R1

Version de origen: `TM_CANON_v2_13_PROPUESTA.zip`
SHA-256 de origen: `A42274932680493CFEA99F0D8587258B11C61E7B7EC8C9FDB49322403FC01E3F`
Estado nuevo: `CANDIDATO_PENDIENTE_AUDITORIA_MIMO_Y_APROBACION_JAVIER`.

## Cambios de trazabilidad autorizados

1. `PLANO-01` ya solo cita 16:16 (+0,1) y 16:20 (-0,2) como ejemplos de plano. 16:23 (+0,3) queda registrado como contraejemplo NO PLANO; se anota `|apertura-cierre anterior| >= 0,25` y `no abre en plano`.
2. Se incorpora `DECISION_AUTORIDAD_PLANO_GAP_JAVIER.md` con la frontera expresa autorizada. No se modifican el golden ni la regla.
3. 16:38 y 16:39 conservan `[A/B]` en `source_state`; `canonical_status` permanece `CONFIRMADA_PARCIAL`.
4. Se conserva abierta la discrepancia documental del umbral de 2 puntos; no se amplian reglas.
5. El diff es UTF-8 con finales LF. El comando exacto para normalizar cualquier entrada CRLF y aplicarlo est? en `README_REPRODUCCION.md`; se valid? con Git usando `core.autocrlf=false` y el resultado coincide byte a byte con el ?rbol R1.

## No cambiaron

- Regla plano/gap: solo se documenta la autoridad ya indicada por Javier.
- Golden v003, feed, reglas pendientes y reglas expertas.
- Motor, tests y entregables legacy.
