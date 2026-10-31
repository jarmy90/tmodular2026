# CHECKPOINT 19B

Iteración: 19B · Motor: `tm_reference_interpreter_v1_direct_aut.py`
SHA-256 motor: `E12692A409973FC3F72FCCEC830ECF7E9E7136A0CAD439BC4DD3B0F246676350`
SHA-256 gestor: `B463C4F824DA833E020E1D7FCB94AC7524F1B46A5E14A2397C5FC4111B275176`

## Resultado

| métrica | valor |
|---|---|
| pruebas | **169/169** (146 previas + 23 nuevas) |
| suites enlazadas al mismo intérprete | 9/9 |
| canónicas / provisionales / abiertas | 122 / 44 / 3 |
| anclas 16:15–16:32 | 13/19 (sin cambios; 16:27–16:32 no se tocan) |
| bloques | 3/4 |
| anclas de la transición 16:25–16:26 | **11/11** |
| `archived_generation_writes` | 0 |
| `cross_generation_reference_leaks` | 0 |
| determinismo | true |
| consistencia de prefijo | true |
| slots activos | 1 (solo PRIMARY) |

## Transición corregida

| campo | valor |
|---|---|
| TT objetivo | 29870,5 |
| TT precio de confirmación | 29870,6 (seq 2519, 16:25:52.041) |
| extremo físico | 29875,4 (seq 2532) |
| extremo funcional | 29875,4 · CONFIRMED · st 2532 · kt 2535 |
| candidatos FT absorbidos | 2 (29871,8 · 29874,1) |
| origen FT | 29875,4 |
| FT al cierre de 16:26 | 29849,1 (26,3 puntos) |
| origen A principal | 29875,4 (conocimiento 16:26:13.444) |
| LOCAL-G1 cierre funcional | seq 2535 |
| LOCAL-G1 archivo | seq 2553 · `close_reason=TT_FUNCTIONAL_EXTREME_CONFIRMED` |
| slot LOCAL | libre |
| patrones históricos | `LOCAL-G1-TT-2987050`, `LOCAL-G1-FT-2987540` |
| LOCAL-G2 | **NOT_OPENED** (`FUNCTION_AND_FT_EXPLAIN_16_26`, CANONICAL) |
| CLOSING | funciones congeladas (2535–2552); TT y FT siguen vivos |
| ARCHIVED | solo `PATTERN_LAYER_ONLY`; cero funciones desde 2553 |

## Diferencias contra el baseline 19A

1. `PatternRecord` separa `confirmed_price`, `physical_extreme` y
   `functional_extreme` (+ `_status`, `_knowledge_seq`, `_seq`).
2. El FT nace del extremo funcional y absorbe candidatos superados por el TT.
3. El archivo de la generación depende del evento
   `TT_FUNCTIONAL_EXTREME_CONFIRMED` sobre su propietario, no del objetivo.
4. Generación con ciclo OPEN → ACTIVE → CLOSING → ARCHIVED; reapertura si el TT
   extiende de nuevo.
5. Los registros exportados (`ITER18_GENERATIONS.csv`, `ITER18_TT_OWNERS.csv`)
   se sincronizan con `GenerationRecord`/`PatternRecord`; antes quedaban
   congelados con `closed_at=0`.
6. `CLOSING` congela la capa de funciones (`freeze_functions`) sin apagar el
   patrón: el TT puede extenderse y el FT seguir trazando. La sonda de
   continuidad usa `freeze_on_closure=False` para medir qué habría hecho el
   lector local; el motor real nunca descongela una generación archivada.

## Estado

`ITER19B_STATUS = GENERATIONAL_HANDOFF_AND_FT_ORIGIN_COMPLETE`

No se declara `REFERENCE_ENGINE_COMPLETE`. Reglas abiertas intactas:
módulo por descarte local, doble TT de 16:28, resolución 16:27, fallo de TT por
`final_A` en 16:32.
