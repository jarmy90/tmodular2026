# GOLDEN VELAS 1-8 — EXPLICADO (PROVISIONAL, EXTERNO)

> Este golden es **externo al motor y PROVISIONAL**. No es fuente de reglas.
> El nucleo productivo **NUNCA** lee `tests/golden/`. Precios, fecha, simbolo y
> numero de vela solo aparecen aqui y en los tests, jamas en codigo productivo.
> Vocabulario: 1, 2, 3, modulo, A Grande, B Grande, C Grande, AUT, TT, CUT, FT,
> movimiento contrario, retroceso, salida en plano, gap, lectura.

Artefactos:

- `golden_eventos_velas_1_8.json` — eventos por tick/vela (ordeno causal, estado).
- `golden_estados_velas_1_8.json` — fotografia por vela (modular, patrones, eventos).
- `GOLDEN_EXPLICADO.md` — este documento.

Categorias separadas en todo el golden:

| categoria | significado | se exige en tests |
|---|---|---|
| CONFIRMADO | hecho cerrado por Javier (lectura cerrada) | SI |
| POSIBILIDAD_VALIDA | lectura matematicamente valida, no confirmada | SI (como candidata) |
| PENDIENTE | clasificacion pendiente; no exigir, no aproximar | NO |
| INVALIDADO | evento descartado por los ticks | NO |

Criterio de orden: se exige **SOLO orden causal** cuando la regla lo permite.
No se exige timestamp exacto.

---

## VELA 1

- **Hecho:** `1` bajista. Regla §10.2.
- Estado: **CONFIRMADO**.
- Sin pendientes.

## VELA 2

- **Hecho:** al abrir la vela se comprueba primero gap o salida en plano (§10.2).
  El CSV registra un gap de `-0.80`; la lectura previa lo clasifica como
  **salida en plano**.
- **POSIBILIDAD_VALIDA:** `POSIBLE_2` (la salida en plano puede abrir posible 2).
- **Hecho:** `2` bajista, confirmada al alcanzar el tamano de 1 (§10.2).
  Medidas: `1 = 9.00`, `2 = 9.70`.
- **POSIBILIDAD_VALIDA:** `POSIBLE_3`.
- **PENDIENTE:** `SALIDA_EN_PLANO`. §11: la **tolerancia exacta de salida en plano
  no esta cerrada**. No se exige en tests; no se implementa por aproximacion.

## VELA 3

- **Hecho:** movimiento contrario que **supera el 50 %** → `3_FALLIDO` (§10.2).
- **Hecho:** `MODULO` formado por las velas 1 y 2 (§10.3). Expansion por High-Low
  completo: min `29760.30`, max `29838.20`, rango `77.90`.
- **Hecho:** comienza `A Grande` alcista (§10.4).
- Nota de vocabulario: se usa `MOVIMIENTO_CONTRARIO_SUPERA_50` (no "superior",
  no "giro", no "estructura").

## VELA 4

- **Hecho:** termina de extenderse `A Grande`; maximo de A Grande = `29820.80`.
- **POSIBILIDAD_VALIDA:** comienza `B Grande` bajista **candidata** (movimiento
  contrario inicial, cancelable). §10.4.

## VELA 5

- **POSIBILIDAD_VALIDA:** continua `B Grande` candidata. A Grande no crea nuevo
  extremo, por lo que la candidata **no se cancela** (§10.4).

## VELA 6

- **Hecho:** `B Grande` alcanza 100 % → **B Grande confirmada** (§10.4).
- **Hecho:** `B Grande` alcanza 127 % + 0,25 → `AUT` inmediato (§10.5).
  `AUT` **no** confirma definitivamente un nuevo 1.
- **Hecho:** `TT` confirmado. `TT` bajista = final de A Grande − rango del modulo
  = `29820.80 − 77.90 = 29742.90` (§10.6).
- **POSIBILIDAD_VALIDA:** `POSIBLE_1` (el movimiento bajista puede ser 1, §10.5).

## VELA 7

- **PENDIENTE:** `POSIBLE_1_FIN`. El movimiento bajista continua hasta el minimo
  (`29712.40`) y termina el posible 1. §11: la **permanencia de una lectura** a
  traves de nuevos movimientos no esta cerrada. No se exige en tests.
- **Hecho:** dentro de la misma vela comienza movimiento alcista → `A Grande`
  alcista. **Orden verificado en la vela 7:** primero el minimo (`29712.40`),
  despues el maximo (`29738.40`). No se impone la lectura previa (§12); el orden
  procede de los ticks.

## VELA 8 — CONTRADICCION VERIFICADA (foco)

La lectura previa exigia: `B Grande` bajista → `AUT` inmediato → `C Grande`
alcista → `C Grande` alcanza el final de A Grande → `CUT`.

Los ticks **si** permiten:

- **Hecho:** desde el maximo de A Grande comienza `B Grande` bajista. Orden
  verificado en la vela 8: primero el maximo `29744.40` (extension de A Grande,
  ~10.2 s), despues el minimo `29683.20` (~59 s).
- **Hecho:** `B Grande` alcanza 127 % + 0,25 → `AUT` inmediato (§10.5).

Los ticks **NO** permiten:

- **PENDIENTE:** `C_CANDIDATA`. §11: el momento exacto en que un movimiento
  contrario queda confirmado como C Grande no esta cerrado.
- **PENDIENTE:** `CUT`. `C Grande` deberia alcanzar el final de A Grande
  (~`29738.40`), pero dentro de la vela 8 no hay retorno alcista posterior: el
  precio sube a `29744.40`, cae a `29683.20` y cierra en `29689.10`. El nivel
  ~`29738.40` **no vuelve a tocarse hasta la vela 16**.
- **INVALIDADO:** el sub-evento "C Grande alcanza el final de A Grande **dentro
  de la vela 8**" queda descartado por los ticks.

Decisiones del curador sobre la vela 8:

1. `C Grande` y `CUT` quedan **PENDIENTE** (posibilidad valida, no hecho).
2. **NO** se mueve el evento a otra vela (aunque el nivel reaparezca en la vela 16).
3. **NO** se exige `C Grande`/`CUT` en tests de aceptacion.
4. **NO** se implementa por aproximacion.
5. `B Grande`, `AUT` y el inicio confirmado de la lectura nueva son hechos.

---

## RESUMEN

- **CONFIRMADO (17):** 1; 2; posible2->2; modulo; A Grande; maximo A; B Grande
  confirmada; 127 %+0,25; AUT; TT; A Grande nueva (vela 7); B Grande (vela 8);
  127 %+0,25 (vela 8); AUT (vela 8); B candidata (velas 4-5, como candidata).
- **POSIBILIDAD_VALIDA (5):** posible 2; posible 3; TT pendiente; posible 1;
  B Grande candidata (contada como candidata).
- **PENDIENTE (3):** salida en plano (vela 2, §11); posible 1 fin (vela 7, §11);
  C Grande candidata y CUT (vela 8).
- **INVALIDADO (1):** retorno de C Grande hasta el final de A Grande dentro de
  la vela 8.

## PENDIENTES QUE AFECTAN AL GOLDEN (§11)

- Tolerancia exacta de salida en plano → `SALIDA_EN_PLANO`.
- Serie de precio exacta (Bid/Ask/Last/punto medio) → `meta.serie_precio` PENDIENTE.
- Momento de confirmacion de movimiento contrario como A/B/C Grande →
  `C_CANDIDATA` (vela 8).
- Permanencia de una lectura → `POSIBLE_1_FIN` (vela 7).
- Reglas completas de FT → no aparece FT en la lectura cerrada de velas 1-8
  (solo TT); no se anade ningun evento FT.

## ANTI-SPOILER

- El golden no ensena la respuesta al nucleo: el nucleo no lo lee.
- Prohibido en codigo productivo: precios, fecha, simbolo, indice de vela,
  condiciones para esta muestra, acceso a golden, ticks futuros, nombres que
  anticipen el resultado.
- Aqui (golden/tests) si se permiten precios concretos.
