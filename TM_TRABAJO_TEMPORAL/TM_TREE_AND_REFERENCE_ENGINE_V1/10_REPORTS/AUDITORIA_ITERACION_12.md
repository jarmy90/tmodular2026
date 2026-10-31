# AUDITORÍA — ITERACIÓN 12

**Baseline:** `TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT`
**Fuente normativa:** árbol v2.19 (intacto) + decisiones expertas de la iteración 12
**Fecha:** 2026-10-30

---

## 1. Qué se implementó

| Decisión | Implementación | Clasificación |
|---|---|---|
| Reinicio del ciclo tras TT 100 % | `_on_tt_tick` marca `tt_cycle_closed`; `_rotate_cycle_after_tt` al abrir la vela siguiente | CANONICAL_PASS |
| 2 evaluada en la vela siguiente al nuevo 1 | `_eval_opening` reutilizada tras promover el nuevo 1 a `1` | CANONICAL_PASS |
| CUT ≠ C tendencia | `CUT_CONFIRMED` (C > final real de A) y `C_USED_AS_TREND` (C > base del módulo) como fronteras separadas | CANONICAL_PASS |
| FT estructural | `_on_ft_tick`: origen = extremo real del TT, confirmación con extremo propio | PROVISIONAL_POLICY_PASS |

## 2. Errores propios detectados y corregidos durante la iteración

1. **Abrir 2 con TT pendiente.** Mi primera versión rotaba el ciclo en cualquier cambio de vela,
   incluso con TT pendiente, violando v2.7 B («antes de abrir una nueva A, B, módulo o lectura
   concurrente, decidir qué frontera se alcanza primero»). Corregido: con `TT_PENDING` no se
   rota ni se abre estructura nueva.
2. **Estado sin salida `A_ABSORBED`.** No tenía handler: la lectura quedaba congelada
   17.532 de 20.335 ticks (86 %) sin actualizar nada. Corregido con
   `_on_a_absorbed_tick`: el módulo sigue extendiéndose y la pregunta contraria se reabre
   cuando el retroceso parte de un extremo distinto del que absorbió.
3. **Extremo real del TT mal inicializado.** `tt_extreme` se quedaba en el precio del AUT
   (29845,30) en lugar del extremo real alcanzado (29829,10), lo que habría situado el origen
   de FT en el lugar equivocado. Corregido con seguimiento del extremo mientras el TT está vivo.
4. **TT fallaba en el tick de activación.** Con AUT directo por A, `final_A` coincide con el
   precio de activación; el tick siguiente «tocaba» final_A y declaraba TT fallido. Corregido:
   el retorno a final_A exige cruce real desde el lado del TT.
5. **TT no registraba extensión.** El extremo se actualizaba antes de evaluar el estado, por lo
   que `TT_EXTENDED` nunca se emitía. Corregido con bandera `moved`.

## 3. Corrección de una afirmación previa (iteración 11)

Dije que «el feed no contiene ningún gap ≥ 0,25». Era **falso**. El feed sí contiene gaps
reales (14,00 / 1,50 / 1,50 / 0,80 / 3,60 puntos). La observación anterior se debía a que el
lector, atrapado en un único nuevo 1, nunca volvía a evaluar una apertura. Queda corregido en
este documento y en el checkpoint.

## 4. Alcance real de las pruebas (honesto)

```text
TOTAL 132
CANONICAL_PASS          69   reglas cerradas (núcleo, gap, TT, CUT condición, ciclo, anclas)
PROVISIONAL_POLICY_PASS 62   dependen de la autonomía del retorno (A/B/C/FT)
OPEN_RULE_BLOCK          1   AUT directo sin A confirmada
```

Las 62 provisionales **no demuestran fidelidad canónica**. En particular, FT se confirma con el
mismo criterio provisional de autonomía (extensión de extremo propio + filtro de 2 puntos como
mínimo estructural), no con una evaluación funcional de claridad/continuidad.

## 5. Concurrencia

`CompositeReader` ejecuta L1 y L2 con ticks **suministrados externamente**. Eso demuestra
aislamiento (cero fugas, estados idénticos a la ejecución aislada), **no** descubrimiento
automático: el intérprete todavía no abre una L2 por una regla TM expresa, ni la mantiene, ni
la integra o cierra por sí mismo. Queda como `Q-CONCURRENCY` y no se declara implementada.

## 6. Feed completo

```text
ticks 20.335 | deterministico | prefijo consistente | 1.596 eventos
ciclos 47 | modulos 8 | A 10 | B candidata 10 | B Grande 1 | AUT 5 (2 directos)
C 3 | CUT 2 | C tendencia 3 | TT 100 % 2 | FT 1 | gaps resueltos 38
```

El lector **ya no queda atrapado** en un único nuevo 1: 47 reinicios de ciclo y 5 AUT.
La fase dominante sigue siendo `NEW_ONE_ACTIVE` (16.194 ticks), coherente con un feed con 38
gaps reales, pero no está verificado contra las lecturas humanas bloque por bloque.

## 7. Lo que sigue abierto

- **Q-CUT**: secuencia de reset posterior a CUT (el árbol la marca `PENDIENTE_JAVIER`).
- **Q-CONCURRENCY**: regla que autoriza abrir una lectura secundaria.
- **Q-FT-VARS**: variables operativas (fuera de alcance por decisión expresa).
- Comparación bloque a bloque contra las lecturas humanas `[A]/[B]`, sin usar `[D]` como golden.

## 8. Integridad

- Árbol v2.19 sin modificar: `94A1408A…6B17`.
- Tickfeed sin modificar: `5F701BE2…C9FF`.
- Lecturas humanas sin modificar: `F5D7550C…4226`.
- Motores históricos (`v1`, `ab_candidate`, `bg_aut`, R5) sin modificar.

## 9. Valoración

Las decisiones cerradas de la iteración 12 están implementadas y probadas. El motor recorre el
feed de forma causal y ya no se bloquea. No es todavía un lector completo ni validado: falta el
reset de CUT, el descubrimiento de lecturas concurrentes y la comparación humana bloque a bloque.
