# MODELO DE PROPIEDAD DE LECTURAS — V1

## 1. Lectura

```text
reading_id
gid
parent
phase
```

Cada lectura posee sus propias referencias. No hay estado global de función.

## 2. Funciones y referencias

Cada función posee:

- `origin` y `origin_time`;
- `extreme` y `extreme_time`;
- `direction`;
- `status`: `PENDING`, `CONFIRMED`, `IMPOSSIBLE`;
- `structural_time` (origen real);
- `knowledge_time` (tick en que se conoce).

`1`, `2`, `3` y el módulo no comparten extremos. Un extremo solo se actualiza si su función sigue viva y conserva la misma finalidad.

## 3. Propiedad

```text
reference.owner_reading_id == active_reading.reading_id
reference.owner_generation_id == active_generation.gid
```

El intérprete core usa un `gid=1` por ejecución. L1 y L2 se ejecutan en procesos separados con `reading_id` distinto; no comparten objetos.

## 4. PENDING / CONFIRMED / IMPOSSIBLE

- `PENDING`: la pregunta está abierta y la referencia puede actualizarse.
- `CONFIRMED`: se alcanzó la condición estructural; el `knowledge_time` queda fijado.
- `IMPOSSIBLE`: la condición ya no puede cumplirse en esta rama; se invalida la función y se pasa a la siguiente pregunta.

Un estado `IMPOSSIBLE` no se reutiliza ni se convierte en `CONFIRMED`.

## 5. Tiempos

- `structural_time`: instante del origen real de la función.
- `knowledge_time`: primer tick con evidencia suficiente.
- No se presenta el tick de confirmación como origen.
- No se usa información futura.

## 6. Aislamiento

- Una lectura secundaria no inyecta referencias en la principal.
- Un nuevo 1 no hereda el `three_extreme` anterior.
- Un gap no hereda estados incompatibles.
- El intérprete core no implementa A/B/C; su estado se marca `NOT_IMPLEMENTED_CORE`, no se simula.
