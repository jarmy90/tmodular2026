# CORRECCIONES DE FASE B — RESUMEN EJECUTIVO

Las anclas aceptadas en Fase B se conservan con una corrección mínima y
documentada.

## 1. A puede nacer dentro de la vela

`P_AB_01_A_NEXT_BAR` queda `SUPERSEDED_EXPERIMENTAL_POLICY`.

A puede nacer en la misma vela del módulo o de 3. Si 3 vuelve a extenderse,
A se absorbe. Si A adquiere autonomía, 3 se archiva en su extremo estructural
real.

## 2. Retorno sin contador de ticks

`P_AB_03_RETURN_TWO_TICKS` queda `READER_EXPERIMENTAL_POLICY_NOT_CANON`.

`RETURN_JUMP = 4,0` queda `REJECTED_EXPERIMENTAL_ASSUMPTION`.

El retorno se confirma por:

- extensión de su propio extremo; o
- salto estructural único de al menos 4,0 puntos, cuando el salto aporta la
  evidencia funcional.

El mínimo de 2,0 puntos solo separa ruido.

## 3. T-001

La descripción decía `10000->9600` con `size=200`. El fixture correcto es
`10000->9800` (size 200); el segundo tramo pertenece a la vela siguiente.
Se corrigió la descripción, no la expectativa.

## 4. B Grande y AUT por B

Se conservan las reglas aprobadas:

```text
B < 100 % de A -> B_CANDIDATE
B >= 100 % de A -> B_GRANDE
B <= 127 % de A + 0,25 -> B_GRANDE
B > 127 % de A + 0,25 -> AUT en el mismo tick
```

Ancla L1:

- B Grande: 16:18:34.125, B = 9,1
- AUT: 16:18:34.926, B = 12,3
- nuevo 1: origin 29857,6, st 16:17:05.425, kt 16:18:34.926, extensión 29843,0

B no se informa con 14,6. 12,3 es el movimiento B/AUT; 14,6 es la extensión
del nuevo 1.

## 5. AUT directo por A

Vía separada:

```text
A_CONFIRMED
-> si A supera estrictamente la base del módulo
-> AUT_DIRECT_BY_A
-> NEW_ONE_ACTIVE
```

Ancla L2:

- módulo base = 29850,0
- A = 29830,3 -> 29850,8 = 20,5
- A cruza base estricta en 16:20:59.125
- AUT directo nace en 16:20:59.125
- nuevo 1 origin = 29830,3, st = nacimiento de A, kt = 16:20:59.125
- extensión posterior = 29857,3

No hay B en esta vía.
