# CHECKPOINT 18 — Gate de anclas endurecido

- Validador sin True/or True/constantes: cada ancla se evalúa contra el snapshot de su vela o evento.
- 19 anclas: **13 PASS**, 3/4 bloques (16:15–16:18, 16:19–16:22, 16:22–16:24). 16:25–16:32 falla desde 16:27.
- 146/146 pruebas (104 canónicas, 39 provisionales, 3 open rule).
- L2 descubierta automáticamente (seq 1145, vela 16:19), TT 29870,5 pendiente en 16:24 y extendido a 29875,4 en 16:25.
- Nuevas identidades: generaciones PRIMARY-G1/LOCAL-G1 y registros TT con owner, módulo, final_A, objetivo y estado (ITER18_TT_OWNERS.csv).
- Políticas de Iteración 17 (corredor L2, keep_first_pending, no_invalidate, 35 %) siguen clasificadas como provisionales.

Pendiente: cierre de L2-G1 y nacimiento L2-G2 en 16:26, A→B Grande→A-tendencia en 16:27, dos TT en 16:28 y doble confirmación 16:29. Gate 18: FAILED.
