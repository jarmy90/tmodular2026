# CHECKPOINT 16 — Auditoria del sistema de validacion

**Baseline:** `TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT`
**Interprete unico de todas las suites:** `tm_reference_interpreter_v1_direct_aut.py`
**SHA-256 del motor en este checkpoint:** se registra en `TEST_AUTHORITY_SUMMARY.json`
**Fecha:** 2026-10-30

## 1. Que se ha corregido en esta iteracion

1. Todas las suites se ejecutan con `TM_READER_MODULE`,
   `TM_READER_SHA256` y `TM_READER_CORE_VERSION` fijados por el agregador.
   Si una suite importa otro archivo, otra version o un modulo sin
   `CORE_VERSION`, la suite falla (`BINDING_FAILURE`).
2. `T-015` ya no admite la semantica historica. Exige: diferencia exacta de
   0,25; no plano; 2 prohibido; `GAP_IMPLICIT_SEQUENCE`; `GAP_IMPLICIT_NEW_ONE`;
   `NEW_ONE_ACTIVE`; origen exactamente en la apertura; direccion correcta.
   Se elimino el fallback `mod_size == 200`.
3. La autoridad de cada prueba se agrega leyendo el campo estructurado
   `classification` de los CSV, no el texto de consola.
4. Se corrigio el alcance de la comparacion humana: no existe etiqueta humana
   por tick. Se usan anclas y segmentos por vela.
5. El 35 % quedo aislado como `PROVISIONAL_INTERNAL_RATIO`, documentado como
   referencia orientativa, nunca frontera canonica.
6. La cabecera del interprete declara el estado real
   (IMPLEMENTADO_CANONICO / PROVISIONAL / OPEN_RULE_BLOCK / NO_IMPLEMENTADO).

## 2. Resultado de pruebas (posterior a la correccion)

```text
suites ejecutadas        8/8 con binding OK
pruebas totales          146
PASS                     146
FAIL                     0
CANONICAL_PASS           104
PROVISIONAL_POLICY_PASS   39
OPEN_RULE_BLOCK            3
```

No se conserva el total anterior 128/16/2: la clasificacion honesta es
104/39/3. Las 39 provisionales dependen de la autonomia del retorno o de la
proporcion orientativa del 35 %. Las 3 bloqueadas son GP-04, GP-05 y GP-06.

## 3. Validacion humana 16:15-16:32

```text
human_anchors_total                 19
human_anchors_passed                 6
trace_rows_generated             4.400
human_segments_validated             6
ticks_with_independent_human_label   0
blocks_total                         4
blocks_passed                        1   (16:15-16:18)
```

Anclas que pasan: 16:15, 16:16, 16:17, 16:18, 16:24, 16:25 (secuencia
implicita del gap y nuevo 1 desde 29848,5).

La comparacion tick a tick de 6.684 filas de la iteracion 15 no era una
metrica de fidelidad: solo habia 14 anclas humanas.

## 4. Primera divergencia por bloque

| Bloque | Primera divergencia | Causa raiz |
|---|---|---|
| 16:15-16:18 | ninguna | bloque validado |
| 16:19-16:22 | 16:19 local 1 (29850,0->29842,5) | L2 no descubierta automaticamente; el motor no abre la lectura local en 16:19 |
| 16:22-16:24 | 16:22 AUT directo local | el AUT directo existe solo en L1; la lectura local 1-2-3 no se conserva |
| 16:24-16:25 | 16:25 TT alcista | referencia del TT no determinada por los archivos (Q-TT-1625) |
| 16:25-16:32 | 16:26 FT | el FT existente es el del TT bajista de 16:24, no el del TT alcista de 16:25 |

## 5. Correcciones estructurales aplicadas

- **RC-1 (aplicada):** se elimino la rotacion administrativa por `NEW_ONE`.
  Un nuevo 1 que no cerro TT ya no rota al cambiar de vela; la vela siguiente
  desarrolla FT/A/B dentro de la misma estructura. Solo rotan el TT cerrado y
  el nuevo 1 nacido de `C_USED_AS_TREND`. Esto elimino la cascada de 7 ciclos
  por gap en 16:25-16:32.
- **RC-2 (aplicada):** el TT del ciclo archivado queda congelado
  (`tt_archived`), conserva objetivo/extremo para FT y trazabilidad, pero no se
  extiende ni arbitra dentro de la estructura nueva.
- **RC-3 y RC-4 (rechazadas):** exigir el 35 % del retorno para confirmar A de
  un nuevo 1 y priorizar la extension de A sobre la reanudacion del modulo
  producian A de 115 puntos y rompian las anclas 16:23/16:24 ya validadas. Se
  revirtieron; quedan documentadas como intentos rechazados.

## 6. Estado

```text
TREE_STATUS              NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_STATUS  REFERENCE_ENGINE_INCOMPLETE
PATTERN_ENGINE_STATUS    PATTERN_ENGINE_INCOMPLETE
GATE_16                  GATE_HUMAN_1625_1632_FAILED
```

No se congela el arbol, no se toca el motor oficial, no se opera en real.

## 7. Verificacion del paquete

El ZIP se extrae en una carpeta limpia y desde su contenido se ejecutan:

```text
run_iteration_16_all.py       146/146 PASS, 8/8 suites con binding OK
run_human_segments_16.py      6/19 anclas, 1/4 bloques, 0 ticks etiquetados
```

El motor del ZIP tiene el mismo SHA-256 que el del arbol de trabajo; las 8
suites importan ese archivo y ninguna otra version. `MANIFEST.json` y
`SHA256SUMS.txt` cubren los 23 archivos; el ZIP tiene 25 miembros y no contiene
tickfeed, credenciales ni cache.
