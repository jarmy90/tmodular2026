# Informe de causalidad v0.7.5

## Resolucion del hallazgo

- Lectura: `R0062`.
- `TT` objetivo: `29615.20`; primer cruce estructural: `29614.20` a `2026-10-16 16:56:32.145`.
- `B Grande` confirmada: `2026-10-16 16:57:16.859`.
- `TT` conocimiento: `2026-10-16 16:57:16.859`.
- El evento `TT` conserva el tiempo estructural del cruce, pero se emite con el `knowledge_time` de B Grande. Un prefijo fisico anterior a B Grande no puede contenerlo.

## Invariantes medidos

- Eventos: `873`; lecturas: `67`; movimientos: `264`.
- `knowledge_time >= structural_time`: `True`.
- `event_id` append-only: `True`.
- `sequence_id` real del feed: `True`.
- TT solo despues de B Grande: `True`.
- Formula TT: `True`.
- GAP antes de otras ramas: `True`.
- Geometria generica preservada: `True`.

## Matriz de prefijos

- Cortes ejecutados: `201`.
- Fallos: `0`.

## Cobertura causal

- Geometrica causal: `1314/1335` (98.43%).
- Funcional causal: `1263/1335` (94.61%).
- Movimientos con cobertura funcional causal: `261/264`.
- Ticks con owner explicito: `10786/11120`; sin owner: `334`.

La cobertura parcial no se rellena con lecturas posteriores. Se reporta como cobertura no disponible en ese tick, no como cobertura causal.

## Conclusion

- `AFS2_READY=true`.
- Alcance: integridad causal y prefijos; no implica cobertura funcional total.
