# PATCH CANÓNICO v2.20 — FRONTERA DE PLANO Y CIERRE DE Q-CUT

**Estado:** `CONFIRMADO_JAVIER`
**Precedencia:** posterior a `TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md`.
Se añade como patch independiente para no alterar el árbol acumulado ya auditado
(SHA-256 `94A1408A…6B17`). En caso de discrepancia con el árbol v2.19, prevalece este patch.

---

## A. Frontera de plano (fija, sin ambigüedad)

```text
|Open - Close_anterior| <  0,25  -> PLANO
|Open - Close_anterior| >= 0,25  -> NO PLANO -> 2 PROHIBIDO
```

Consecuencias obligatorias:

1. `0,24` es plano.
2. `0,25` exactos **no** es plano; prohibe 2.
3. `0,26` no es plano; prohibe 2.
4. El texto histórico que describa «diferencias de 0,1 o 0,2 como plano» se conserva como
   trazabilidad, pero esta frontera es la vigente.
5. La comprobación de cola inicial y de tamaño exigido sólo se aplica **después** de
   confirmar plano.

## B. Cierre de Q-CUT

```text
C supera ESTRICTAMENTE el final real de A
-> CUT CONFIRMADO
-> CUT no crea nuevo 1
-> CUT no resetea el ciclo
-> C sigue activa y conserva su extremo vivo
```

```text
si posteriormente C supera ESTRICTAMENTE la base del módulo
-> C_USED_AS_TREND
-> nuevo 1 en la dirección de C
-> se aplica la rotación general del ciclo
```

Reglas:

1. El final real de A y la base del módulo son **referencias distintas**; no se sustituye una
   por otra.
2. CUT no consume la candidatura de C ni la archiva.
3. La trazabilidad obligatoria es `B Grande -> C Grande -> CUT (si procede) -> C usada como
   tendencia (si procede) -> nuevo 1`.
4. Tocar exactamente el final real de A no confirma CUT; se exige superación estricta.
5. Tocar exactamente la base del módulo no convierte C en tendencia; se exige superación estricta.

`Q-CUT` deja de ser `OPEN_RULE_BLOCK` y pasa a regla cerrada.

## C. Separación entre cierre causal y rotación administrativa

```text
TICK QUE CONFIRMA TT:
  cycle_closed_at_tt = ese tick
  ciclo anterior cerrado; referencias antiguas sin autoridad activa
  el mismo movimiento = nuevo 1
  TT conserva objetivo y extremo real
  NO se abre 2 dentro de esa vela

APERTURA SIGUIENTE:
  cycle_rotation_committed_at = primer tick de la vela nueva
  el nuevo 1 acumulado se promueve a one_*
  se evalúa plano / gap
  se evalúa cola inicial
  se abre o se prohibe 2
```

Ninguno de los dos instantes puede presentarse como el otro: el cierre es causal y ocurre en el
tick del TT; la rotación es administrativa y ocurre en la apertura siguiente.

## D. Terminología de métricas

No se denomina «ciclos» al contador de rotaciones. Se informa por separado:

```text
cycle_rotations
cycles_closed_by_tt
cycles_started_by_gap
cycles_started_by_c_trend
initial_cycles
incomplete_or_archived_cycles
```
