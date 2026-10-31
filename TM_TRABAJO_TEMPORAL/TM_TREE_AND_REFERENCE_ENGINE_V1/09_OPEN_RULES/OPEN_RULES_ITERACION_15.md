# REGLAS ABIERTAS — ITERACIÓN 15

## Cerradas

### Q-ONE-AT-CLOSE
El 1 se confirma al cierre de su propia vela. `knowledge_time` = último tick de
esa vela; la apertura siguiente solo evalúa plano/gap/cola/2.

### Q-TWO-OWN-BAR (v2.13/v2.14)
La 2 confirmada pertenece a su vela. Al cerrar se congela su extremo final
(`TWO_FROZEN_AT_CLOSE`). La vela siguiente desarrolla 3; el mínimo real de 3
actualiza el módulo.

### Q-STATE-LEAK
Cada A nace con su propio retorno y su propio AUT directo. No se heredan
`return_*` ni `aut_direct_status` de la A anterior.

### Q-RESUMPTION-VS-ABSORPTION
La reanudación del módulo sobre una A estructural la completa como B; la
absorción queda reservada a la oscilación interna que no alcanza la proporción
del movimiento dominante.

## Provisionales

### P-PROP-35
La proporción del 35 % del movimiento dominante separa desarrollo interno de A
estructural. v2.16 la declara **orientativa**, no frontera matemática aprobada.
Se usa como criterio ejecutable provisional en la lectura local.

Efecto verificado:
- 16:21 → A 4,7 / módulo 19,7 = 24 % → absorbida; 3 extiende a 29830,3.
- 16:23 → A 8,0 / nuevo 1 20,5 = 39 % → A estructural; B y AUT local.

### P-L2-BIRTH
La lectura local nace en la primera vela del nuevo 1 dominante y adquiere
autoridad cuando su AUT directo confirma. Verificada en 16:19–16:23; no probada
en otros bloques.

### P-L2-AUT-3
En la lectura local, un nuevo recorrido que supera la base del módulo integrado
por el AUT confirma AUT (nivel 3 de la jerarquía local). El nuevo 1 conserva el
origen de la A que lo produce (29852,6), no la base del módulo.

## Abiertas

- **Q-L2-GENERAL**: regla general de nacimiento/cierre de lecturas locales más
  allá del caso 16:19–16:23.
- **Q-TT-LOCAL**: TT y FT de estructuras locales encadenadas tras varios AUT.
- **Q-1624-DOC**: la adenda de 16:24 dice "TT alcista no alcanzado" y el golden
  v003 registra el TT principal bajista 29829,1 alcanzado a las 16:24:44.990.
  Son TT distintos; falta nombrarlos en la ficha.
- **Q-CUT-FT-L2**: CUT y FT dentro de lecturas locales.

## Prohibiciones vigentes

- No usar la política de cuatro puntos.
- No convertir el 35 % en frontera canónica sin decisión expresa.
- No congelar el árbol ni tocar motores oficiales.
- No operar en real.
