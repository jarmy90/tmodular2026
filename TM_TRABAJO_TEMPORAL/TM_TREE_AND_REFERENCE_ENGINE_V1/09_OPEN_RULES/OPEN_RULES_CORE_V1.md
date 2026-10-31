# REGLAS ABIERTAS Y ALCANCE — NÚCLEO V1

## Implementado y probado

- función 1 (inicio, dirección, medida congelada);
- apertura plana / no plana;
- 2 candidata;
- 2 confirmada al 100 % de 1;
- 2 imposible por cierre o cola;
- módulo por descarte;
- 3 pendiente;
- 3 confirmada por superación estricta;
- 3 imposible por retroceso > 50 %;
- 50 % exacto inclusivo;
- módulo regular 1+2+3.

## Abierto

### O-AUTONOMY

La autonomía de A no se decide por porcentaje, punto medio ni umbral fijo. Requiere `CONTRARY_MOVE_PENDING` y una evaluación funcional. Bloquea A/B/C/AUT.

### O-ONE-CYCLE

El ciclo funcional completo de 1 (nacimiento, candidatura, final funcional, congelación) no está cerrado para todos los casos. El núcleo solo implementa la variante de un 1 inicial medido al cierre.

### O-CUT

CUT no tiene todavía semántica ejecutable normalizada.

### O-FT

La confirmación estructural de FT no está cerrada; no se implementa.

### O-GAP-NEW-ONE

La rama de gap está reconocida (2 prohibido con apertura no plana), pero la creación de un nuevo 1 por gap implícito no está implementada. El núcleo se detiene en `GAP_OPEN_NO_TWO` y no inventa ticks.

### O-CONCURRENCY

L1/L2 se ejecutan como procesos separados. La concurrencia dentro de un mismo proceso y la integración de módulos no están implementadas.

## Retirado como formulación

`Q-AUT-REF` (¿A se mide contra el 1 o contra el módulo 1+2?) queda **retirado como formulación** por la decisión del 13-07: no se usan porcentajes, puntos medios ni umbrales fijos para la autonomía. Se sustituye por `O-AUTONOMY`.

## Regla de bloqueo

Una rama abierta no se simula. El intérprete emite `BLOCKED_BY_OPEN_RULE` o `NOT_IMPLEMENTED_CORE` y conserva la evidencia física sin clasificar A/B/C.
