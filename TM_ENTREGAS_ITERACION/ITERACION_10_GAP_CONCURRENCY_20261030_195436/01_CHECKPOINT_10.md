# CHECKPOINT 10 — GAP EXPLÍCITO Y CONCURRENCIA L1/L2 (ITERACIÓN 10)

Fecha: 2026-10-30
Intérprete: `tm_reference_interpreter_v1_direct_aut.py` (revisión 10)
Concurrencia: `tm_concurrent_readings.py`

## 1. Gap separado en cuatro estados

```text
NON_FLAT_OPEN_OBSERVED      |Open − Close_previo| >= 0,25
NO_TWO_BY_NON_FLAT_OPEN     solo cuando la lectura esperaba 2
GAP_IMPLICIT_TRANSITION     2 imposible → módulo por descarte → A implícita
CONTINUATION_ACROSS_BAR     función viva no se divide al cambiar de vela
```

Reglas aplicadas:

- toda apertura no plana prohíbe 2 si la pregunta activa es TWO;
- una función viva (A/B/C/AUT/nuevo 1/2/3) **no** se reinicia por cambio de vela;
- la rama gap abre A implícita desde el extremo observable del módulo;
- no se inventan precios internos ni ticks: `len(trace) == len(ticks)`.

## 2. Concurrencia L1/L2

`CompositeReader` ejecuta como máximo **dos** escalas activas:

- `reading_id`, `parent_reading_id`, ticks, funciones y genealogía propios;
- un tick puede afectar a ambas lecturas;
- una lectura local **no** sustituye a L1;
- tercera escala prohibida sin regla expresa (`ValueError`).

Auditoría de propiedad: cada referencia (`one/two/mod/a/c/n`) debe caer dentro
del rango de precios de **sus propios** ticks. Fugas → `CROSS_READING_REFERENCE_LEAK`.

## 3. Resultados

```text
GAP + CONCURRENCIA .... 11 / 11 PASS
  GAP-01..05 ...........  5 / 5
  CONC-01..06 ..........  6 / 6   (cero fugas)
REGRESIÓN 09 .......... 82 / 82 PASS
```

Propiedad fuerte verificada: `L1` ejecutada sola produce exactamente el mismo
estado que `L1` dentro de la composición; idem `L2`. No hay interferencia.

## 4. Recorrido completo 16:15–17:29

```text
ticks ................. 20335
determinista .......... true  (doble ejecución idéntica)
prefijo ............... true
eventos ............... 335
fase final ............ NEW_ONE_ACTIVE
```

Hallazgo real: en todo el feed se produce **un solo** ciclo completo
(1 → 2 → 3 → módulo → A → B Grande → AUT → nuevo 1). A partir de ahí el nuevo 1
se extiende (248 `NEW_ONE_EXTENDED`) y la lectura no vuelve a abrir 2, 3 ni A.
La causa es de árbol, no de implementación: **el ciclo universal de 1 está en
`OPEN_RULE_BLOCK`**. El intérprete no inventa ese reinicio.

Consecuencia: el feed completo se recorre causalmente, pero solo el primer
ciclo es comparable. Los bloques posteriores quedan bloqueados por esa regla.

## 5. Bloques no implementados

```text
CUT  → OPEN_RULE_BLOCK (sin referencia única)
TT   → OPEN_RULE_BLOCK (no hay regla cerrada del objetivo; el ancla 29829,1
       no basta para definirlo sin inventar)
FT   → OPEN_RULE_BLOCK (falta condición estructural cerrada)
```

## 6. Gates

```text
GATE_GAP_PASS
GATE_CONCURRENCY_PASS
```

- gap no divide funciones vivas: sí (GAP-05)
- gap no inventa ticks: sí (GAP-04)
- cero fugas: sí
- doble replay: sí
- prefijos: sí
- determinismo: sí

## 7. Preguntas expertas (tres)

1. **Q-CYCLE-1** — ¿qué regla cierra el reinicio del ciclo de 1 tras un nuevo 1
   (AUT por B, AUT directo por A o C usada como tendencia)? Es la que bloquea
   el resto del feed.
2. **Q-CUT** — referencia única canónica de CUT y su diferencia con
   C-usada-como-tendencia y con la superación del final de A.
3. **Q-TT** — ¿de qué función confirmada se deriva el objetivo de TT, y con qué
   condición estructural se confirma sin usar variables operativas?

## 8. Estado

```text
TREE_STATUS: NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_STATUS: REFERENCE_ENGINE_INCOMPLETE
PATTERN_ENGINE_STATUS: PATTERN_ENGINE_BLOCKED
```

No se modificó el motor oficial. No se ejecutaron órdenes reales.
