# PREGUNTAS EXPERTAS — CHECKPOINT 3

**Q-B3 cerrada:** el 3 de 16:23 en v2 no era legal (pertenecía a una generación con 2 IMPOSIBLE). v3 lo invalida; la ruta legal es B Grande → C. No se pregunta.

**Preguntas activas: Q-AUT y Q-3-50.** Q-INIT sigue abierta, no preguntada.

---

## Q-AUT — autonomía de A con recorridos pequeños

**MOVIMIENTO**

Estábamos en el 3 legal 29850,0 → 29833,3 (módulo 16,7), con 2 confirmado en 29832,5.

El precio subió 4,1 puntos (A = 29833,3 → 29837,4).

Después bajó 4,9 puntos (B = 119,5 % de A) y luego 6,4 puntos (156 % de A).

El lector confirma A y B Grande; el v005 sigue el 3 hasta 29830,3 (módulo 19,7) y lee A = 20,5.

**PREGUNTA**

¿A se confirma con un B que alcanza el 100 % de A aunque A sea un recorrido pequeño, o requiere autonomía funcional (posición, continuidad, independencia, finalidad) antes de confirmarse?

**SI se confirma con B = 100 %**

- Se mantienen las 51 generaciones L1.
- El 3 se congela en 29833,3.
- Los ciclos A/B de 4–6 puntos producen transiciones.
- El conteo incluye posibles fragmentaciones por ruido estructural.

**SI requiere autonomía funcional**

- El 3 sigue hasta 29830,3; el módulo es 19,7.
- A es 20,5.
- Desaparecen las transiciones de 4–6 puntos.
- El conteo baja y se acerca a la lectura humana local.

**CASOS DESBLOQUEADOS**

16:20–16:22, el módulo local 19,7, las 51 generaciones y la clasificación primaria/secundaria.

**NO SE PROPONE UMBRAL.** No 2, 6, 12, 20 puntos ni 35 %. La respuesta debe ser una condición funcional, no un número.

---

## Q-3-50 — 50 % exacto de 2

**MOVIMIENTO**

En un 3, el retroceso de 2 toca exactamente el 50 % del recorrido de 2.

El árbol exige “retroceso funcional válido”, pero no cierra si el 50 % exacto lo conserva o lo invalida.

**PREGUNTA**

¿Tocar exactamente el 50 % de 2 conserva la posibilidad de 3 o la invalida?

**SI conserva**

- 3 puede confirmarse en el siguiente tick válido.
- El módulo sigue regular 1+2+3.
- v3 ya la admite (`FIFTY_PERCENT_EXACT`).

**SI invalida**

- 3 pasa a IMPOSSIBLE.
- El módulo se resuelve por descarte.
- Cambia el origen de A.

**CASOS DESBLOQUEADOS**

Todos los 3 con retroceso exacto del 50 %, el módulo regular y la matriz de pruebas de 3.

---

## Q-INIT — abierta, no preguntada

El primer 1 del feed sigue sin regla cerrada. No bloquea las 53 generaciones únicas; se resolverá después de Q-AUT.
