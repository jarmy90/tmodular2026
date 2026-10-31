# MATRIZ REGLA → GOLDEN

Cada regla cerrada se enlaza con el caso físico que la valida y el gate que la
comprueba. Los valores son oráculos de validación; nunca se inyectan en el motor.

| Regla | DEC | Caso físico / golden | Evidencia | Gate |
|---|---|---|---|---|
| Plano si \|apertura − cierre anterior\| < 0,25 | DEC-001 | 16:23 abre +0,3 → no plano; 16:24 abre −1,4 → no plano | GATE_1623_EVENTS.csv | `test_transformations.py` |
| B Grande al 100 % de A | DEC-005/H16 | 16:23: B 980 / A 800 = 122,5 % (seq 1876) | GATE_1623_ANCHORS.json | `test_big_b_aut.py` |
| AUT solo al superar 127 % + 0,25 | DEC-002/DEC-003 | 16:23: límite 1041 > 980 → sin AUT | GATE_1623_ANCHORS.json | `test_big_b_aut.py` |
| C solo tras B Grande confirmada | H16 | 16:23: C 29852,60 → 29841,80 | GATE_1623_EVENTS.csv | `test_anchor_gates.py` |
| CUT contra a_end congelado | DEC-011 | 16:23: primer cruce seq 2015 | GATE_1623_ANCHORS.json | `gate_1623_anchors.py` |
| Post-CUT: C Grande que confirma CUT = nuevo 1 dominante | DEC-016 | 16:23 → 16:24: nuevo 1 bajista desde 29852,60, confirmación 2015 | GATE_POST_CUT.json | `gate_post_cut.py`, `test_post_cut_gates.py` |
| Lectura previa sin genealogía común se archiva sin borrar | DEC-016 | R0001 → DOMINANCE_REPLACED_BY_CUT | GATE_POST_CUT_EVENTS.csv | `test_post_cut_gates.py` |
| Máximo 3 lecturas activas, ninguna huérfana | §11.3 | 16:23: 2 activas; 16:24: 1 activa | GATE_POST_CUT.json | `gate_post_cut.py` |
| Con gap no hay 2 | DEC-005 | 16:24 apertura −1,4 | GATE_POST_CUT_EVENTS.csv | `test_transformations.py` |
| TT solo al 100 %, nunca por aproximación | §19 | 16:24: TT alcista pendiente/no alcanzado | CORE_RAW_OUTPUT.json | `gate_post_cut.py` |
| Extension de A cuando B falla sin 100 % | DEC-017 | 16:17: A 29848,50 -> 29857,60; TT 29829,10 (v005) | STATE_TIMELINE_1615_1629.csv | `state_trace.py` |
| Estado funcional correcto en cada tick | DEC-017 | 3538 ticks, 0 sin dominante, 0 violaciones | STATE_TRACE_VALIDATION.json | `state_trace.py`, `test_state_trace.py` |
| Gate legacy por firma de hitos, no por nombre | DEC-017 | Legacy 86 lecturas vs R5 12 -> NOT_COMPARABLE | LEGACY_STRUCTURAL_EQUIVALENCE.json | `compare_v005.py` |
| TT/FT en lecturas locales | ABIERTA | Pendiente de definicion; primer tick afectado seq 1639 | COMPARACION_v005_1615_1629.json | pendiente R6 |
