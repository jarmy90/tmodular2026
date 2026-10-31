# CORRECCIÓN T-001

## Discrepancia

La descripción original decía:

```text
one initial move 10000->9600 in bar 1
expected size = 200
```

La medida física de 10000→9600 sería 400, no 200.

## Auditoría

Fixture:

```text
bar 0: [10000, 9900, 9800]
bar 1: [9800, 9700, 9600]
```

La función 1 se confirma al cierre de la primera vela:

```text
origin  = 10000 (máximo, dirección bajista)
extreme = 9800  (mínimo de la primera vela)
size    = 200
```

El segundo tramo 9800→9600 pertenece a la vela siguiente, no a la medida de 1.

## Resultado

- **Tipo:** error documental de la descripción.
- **Fixture:** correcto.
- **Expectativa:** correcta (`size = 200`).
- **Descripción corregida:** `10000->9800`.
- **Expectativa:** no se cambió para conservar un PASS.

Regresión ejecutada: **19/19**.
