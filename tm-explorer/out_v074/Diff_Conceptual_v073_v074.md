# Diff conceptual v0.7.3 -> v0.7.4

## 1. Cambio de unidad de lectura

| Dimensión | v0.7.3 | v0.7.6 | v0.7.4 |
|---|---|---|---|
| Unidad | Ciclo/lectura dominante | Multi-escala con warmup causal | Movimiento confirmado y lectura funcional |
| Inicio de lectura | Semilla dominante | Semilla + continuación | `FIRST`, `B_CONFIRMADA_NEW1`, `A_SIGNIFICATIVA`, `CUT_NEW1` |
| Escala | Dominante | `scale=1` efectivo | Una escala funcional; macro se reconstruye desde módulos |
| Movimiento | Legs fijos y extensión dominante | Multi-escala | Builder único 25% / mínimo 6.00 |
| Prioridad | Absorción por dominante | Prioridad y absorción | Máximo 3 activas; archivo explícito |
| TT | Extiende la lectura dueña | Extiende TT y absorbe locales | TT local con objetivo `a_end + dirección * x` |
| A > módulo | Invalida o absorbe | Regla heredada | Permitida; guardia provisional 2x |
| B | B de la lectura dominante | B con absorción | `B_CAND`, B Grande, oscilación y B fallida |
| CUT | Sin buffer explícito | Corte por reversión | Buffer de 2.00 puntos |
| Doble pertenencia | No resuelta | `coexisting_function` parcial | FT y nuevo `1` pueden coexistir |
| Cobertura | Geométrica/dominante | `TM_COVERAGE_OK` geométrico | Geométrica y funcional, módulo/A/B/C |
| Auditoría | Eventos | Eventos + lecturas | Tick a tick + narrativa por vela |
| Causalidad | No probada por prefijo | Warmup causal | Prueba de prefijo de eventos y lecturas |

## 2. Cambios que explican el caso 16:52–17:00

### v0.7.3

- `R0007` absorbe el recorrido.
- El TT se extiende hasta `29600.70`.
- No nace el módulo `29667.30 -> 29602.10`.
- No nace el TT `29615.20`.

### v0.7.4

- El movimiento `29667.30 -> 29602.10` se confirma a las `16:52:48.559`.
- Se crea `R0062` como `B_CONFIRMADA_NEW1` de `R0061`.
- El módulo es `65.20`.
- A sube a `29680.40` (`78.30`), superando el módulo sin invalidarlo.
- B baja a `29600.20` (`80.20`).
- El TT `29615.20` se alcanza en `29614.20`.
- El FT se confirma a las `16:57:34.937`.
- La lectura anterior conserva su FT; la nueva lectura conserva su propio TT/FT.

## 3. Reglas de decisión incorporadas

1. El módulo se forma con el movimiento confirmado, no con el máximo/mínimo dominante.
2. Un movimiento contrario que alcanza el 75% del módulo puede abrir una lectura nueva (`A_SIGNIFICATIVA`).
3. Un A que supera el módulo no invalida automáticamente la lectura; el límite provisional es 2x.
4. B puede oscilar dentro de su rango; no se convierte en C mientras no exista B confirmada.
5. El TT solo existe al 100%; antes es objetivo.
6. El TT confirmado puede extenderse; el FT requiere un contrario posterior.
7. Un CUT solo se confirma si el contrario supera `a_end` por al menos 2.00 puntos.
8. Una lectura local puede nacer dentro de una lectura anterior; la herencia no bloquea la nueva estructura.
9. La cobertura funcional se mide sobre módulo, A, B y C, no solo sobre el módulo.
10. La narración y la auditoría son parte del resultado, no un subproducto opcional.

## 4. Lo que no cambió

- Fase 1: solo lectura estructural; nada de operativa, sentimiento ni rentabilidad.
- Vocabulario TM permitido.
- Prohibición de inventar funciones sin precondiciones.
- TT al 100% como requisito.
- C solo después de B confirmada.
- No modificar reglas, tests canónicos, golden, v0.7.1 ni v0.7.3 sin autorización.

## 5. Diferencia de numeración

El prototipo `proto10.py` llama `R0063` a la lectura clave. El motor v0.7.4 la llama `R0062`, porque arranca desde el feed completo y asigna IDs desde la primera lectura. La geometría, el TT y el FT son equivalentes. En informes y tests se usa el ID del motor: `R0062`.
