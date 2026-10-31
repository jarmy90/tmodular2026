# CHECKPOINT 5 — NÚCLEO DEL INTÉRPRETE DE REFERENCIA

## 1. Trabajo completado

Se creó `TM_TREE_AND_REFERENCE_ENGINE_V1` y un intérprete limpio, sin partir de `blind_reader_v4`.

Alcance implementado:

- propiedad de lectura;
- función 1;
- apertura plana / no plana;
- 2 candidata / confirmada / imposible;
- módulo por descarte;
- 3 pendiente / confirmada / imposible;
- 50 % inclusivo;
- módulo regular 1+2+3.

No implementado: A, B, C, AUT, CUT, TT, FT, gap con nuevo 1 y concurrencia interna.

## 2. Hallazgo y corrección

La primera versión congelaba el extremo de 2 al confirmarse y trataba la continuación como 3. El ancla L2 producía 2 = 10,8 y un 3 prematuro en 29833,3.

Contra v005, el 2 real es:

```text
2 = 29844,8 -> 29832,5 = 12,3
```

Corrección aplicada:

- 2 confirmada sigue actualizando su extremo mientras conserva su finalidad;
- las vibraciones internas de la vela de 2 no abren 3;
- 3 se evalúa desde la vela siguiente;
- 3 confirma en el primer tick que supera estrictamente el extremo final de 2;
- 3 sigue actualizando su extremo final.

Resultado L2:

```text
1 = 7,5
2 = 12,3 (extremo 29832,5)
3 primer cruce = 29832,3 a las 16:21:14.734
3 extremo final = 29830,3
módulo = 19,7
```

`three.kt` es el primer cruce; el extremo final es 29830,3. No se confunden.

## 3. Pruebas

```text
tests = 19
passed = 19
failed = 0
determinism = identical
prefix = consistent
replay checks = 5/5 PASS
L2 trace sha256 = 1e62eb2dad69ecdda2b4c10af47c76deec63377b0ef6abc02b0eca9beb3ed13f
```

Anclas reales:

- 16:15–16:18: 1=16,2; 2=12,6 imposible; módulo=28,5 por descarte.
- L2 16:19–16:22: 1=7,5; 2=12,3; 3 final=29830,3; módulo=19,7.

## 4. Comparación árbol-Python

15 comparaciones registradas:

- 13 `MATCH`;
- 2 `BLOCKED_BY_SCOPE` (A/B/AUT de 16:18 y A posterior 20,5).

No hay divergencia de implementación dentro del alcance del núcleo.

## 5. Gate

```text
GATE CORE = PASS
```

El gate del árbol completo no se emite: A/B/C/AUT/CUT/TT/FT no están implementados y varias reglas siguen abiertas.

## 6. Reglas abiertas

- autonomía funcional de A (`CONTRARY_MOVE_PENDING`);
- ciclo inicial y final funcional de 1;
- CUT;
- confirmación estructural de FT;
- gap con nuevo 1;
- concurrencia e integración de módulos.

`Q-AUT-REF` queda retirado como formulación: no se usan porcentajes, puntos medios ni umbrales fijos.

## 7. Recomendación

```text
NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_INCOMPLETE
```

El núcleo es determinista, causal y consistente. El motor oficial no existe y no debe declararse. El siguiente trabajo es especificar y probar `CONTRARY_MOVE_PENDING` y la transición A sin umbral fijo, antes de B/C/AUT.

No se modificaron árbol, tickfeed, v005, R3, R5, motor activo ni goldens.
