# ESTADO ACTUAL -- TM Core v0.7.5.2-R5

**Fecha:** 2026-10-29
**Estado:** LECTURA_AUTONOMA_1615_1629_CANDIDATA_VALIDACION
**Motor unico:** `python/TM_CORE_PYTHON_v0752_CANONICAL_R5.py`
SHA-256 `19A847C078E124616495E85A832F9D2FA12A371413046CBAEB7E9644D47C6A36`
**R3 congelado:** `450379BD5F1E22380614E6112E3FB52C2A653EE8358BF7E5238995AF99D3B7DB` (no modificar).

---

## 1. Versiones

| Componente | Version | Estado |
|---|---|---|
| Motor | `0.7.5.2-R5` | Candidato; traza de estado PASS; 28 tests verdes |
| Golden historico | `v003` | HISTORICO_SUPERADO_EN_16_23_Y_16_24 |
| Golden propuesta | `v004` | TRANSICION_DOCUMENTAL |
| Lecturas humanas | `v005` | AUTORIDAD_HUMANA_CANDIDATA_MAS_RECIENTE |

## 2. Traza por tick

3538 ticks, max 2 lecturas activas, 0 ticks sin dominante, 0 violaciones de
ancla congelada, 42 cambios de funcion, 0 errores. Archivos:
`out/STATE_TRACE.jsonl`, `out/STATE_TRACE_VALIDATION.json`,
`out/STATE_TIMELINE_1615_1629.csv`.

## 3. Comparacion v005 (16:15-16:29)

9 MATCH (5 concurrente + 4 core), 2 RULE_OPEN (16:24, 16:27), 4 MOTOR_DIVERGENT
(16:25, 16:26, 16:28, 16:29).

- 16:24 AUT por B demostrado: 960 > 952 (131,51 %), seq estructural 2165,
  conocimiento 2226, sustituye R0001.
- v005 16:24 contradictorio (seccion 10 vs adenda 11) -> RULE_OPEN sin inventar.
- Confirmacion: R5 en el tick del cruce; legacy/v005 al completarse el
  movimiento -> pregunta abierta de granularidad.
- TT/FT locales no emitidos (reglas cerradas) -> gap declarado, primer tick
  secuencia 1639 (16:22); objetivo de R6.
- Entrada 16:30: v005 espera 1 bajista; R5 cierra en B_CAND +1 -> divergencia
  documentada.

## 4. Gate legacy

`NOT_COMPARABLE`: legacy 86 lecturas fragmentadas, R5 12 consolidadas. El gate
por nombre R0062/R0064 queda retirado (DEC-017) y sustituido por firmas de hitos
B100/AUT/CUT/TT/FT.

## 5. Gates verdes

pytest 28; selftest 8/8 R5; gate 16:23 PASS; gate post-CUT PASS; 12 prefijos con
0 fallos; raw `6594783A...B1776F` inalterado por el comparador; legacy tests 20
(exit 0).

## 6. Pendiente con Javier

1. 16:24: referencia de A (730 local vs 800 modulo) y validez de AUT con TT
   previo pendiente.
2. Granularidad de confirmacion (tick de cruce vs fin de movimiento).
3. Semantica TT/FT en lecturas locales para R6.

## 7. Restricciones

No replay ciego. No AFS2. No produccion. No autonomia completa. R3 congelado.
v005 no se sobrescribe; v004 no se elimina.
