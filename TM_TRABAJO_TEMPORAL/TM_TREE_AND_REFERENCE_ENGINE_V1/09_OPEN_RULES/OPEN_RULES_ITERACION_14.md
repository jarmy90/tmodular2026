# REGLAS ABIERTAS — ITERACIÓN 14

## Cerradas en esta iteración

### Q-ONE-AT-CLOSE — CERRADA

El 1 queda delimitado, medido y confirmado al cierre de su propia vela.

```
STRUCTURAL_TIME_1        inicio del movimiento
EXTREME_TIME_1           tick en que alcanza su extremo
KNOWLEDGE_TIME_1         último tick de su vela (cierre efectivo)
OPENING_EVALUATION_TIME  primer tick de la vela siguiente
```

Verificado: 16:15 (1 = 16,2; kt 16:15:59.862) y 16:19 (1 local = 7,5;
kt dentro de 16:19). El primer tick de la vela siguiente no confirma el 1:
solo evalúa apertura.

### Q-GAP-TT 16:24–16:25 — CERRADA

Antes de abrir 16:25 se conservan congelados módulo, final real de A, dirección,
objetivo TT y nivel de invalidación. El gap no inventa precios internos; la
apertura fija el origen del nuevo 1. Un mismo tick puede confirmar el TT
heredado y abrir el nuevo 1 (`DOUBLE_BELONGING_TT_AND_GAP`, prueba GP-12).

## Abiertas

### Q-L2-BIRTH — nacimiento y declaración de la lectura local

La lectura local del bloque 16:19–16:23 no se abre con el gap de +0,3 ni con el
gap de 16:25. Su genealogía empieza en el 1 local de 16:19 (7,5) y queda
declarada por el AUT directo de 16:22.

Falta una regla expresa que fije **cuándo nace**:

1. ¿En la primera vela del nuevo 1 dominante (16:19), aunque su apertura no sea
   plana (-0,4)?
2. ¿Solo cuando su propio AUT directo confirma (16:22), reconstruyendo 1/2/3 y
   módulo con datos ya pasados?
3. ¿En ambas: sombra desde 16:19 y autoridad desde 16:22?

Efecto observable: en (1) el 3 local se mide hasta 29830,3 (módulo 19,7);
con la sonda actual se midió 29832,3 (módulo 17,7).

### Q-L2-ABSORB — absorción frente a B estructural en la lectura local

En 16:23 el precio sube de 29842,8 a 29852,6 y recupera el origen de A (29850,8).
El humano lo clasifica como B que confirma AUT local. El motor lo absorbe como
extensión del módulo.

Pregunta: cuando el recorrido contrario recupera el extremo del módulo con
extensión propia ≥ 2 puntos, ¿prevalece B estructural sobre la absorción?
La sonda implementada así degradó el estado; no se declara canónica.

### Q-TT-ALCISTA-1624 — contradicción documental en 16:24

- Lectura humana v005 (adenda 16:24–16:29): "el avance no alcanza el 100 % del
  TT correspondiente; TT pendiente".
- Golden v003: "TT 29829.1 alcanzado después de 16:18: 2026-10-16 16:24:44.990".

No son el mismo TT: 29829,1 es el TT principal bajista; el "TT alcista" de la
adenda pertenece a la estructura local/alcista posterior. Falta que la ficha de
16:24 nombre explícitamente ambos.

## Prohibiciones vigentes

- No resolver CUT ni FT por invención.
- No usar la política de cuatro puntos.
- No activar la sonda local como canónica.
- No congelar el árbol.
- No tocar motores oficiales.
