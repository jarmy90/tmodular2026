# Adenda F1 — precisión del fallo 16:37 (v0.7.5.1)

- Emisor: TM_READER_VALIDATOR. Sin edición de motor, tests, árbol, golden ni reglas.
- Fecha: 2026-10-28. Complementa `INFORME_TRASPASO_FUNCIONAL_v0751.md`.
- Motivo: la auditoría técnica de MiMo (A1: yardstick del «2») obliga a precisar el mecanismo de F1.

## 1. Hecho físico verificado (feed crudo)

Barra 16:37 (bid): O 29734,80 · H 29744,40 · L **29683,20** · C 29689,10 · H−L **61,20**.
- Máximo en `sequence_id` 5592 (16:37:10,254).
- Mínimo en `sequence_id` **5827 (16:37:59,175)** — último segundo de la vela.

El golden v003 fija exactamente eso: «Su módulo se mide desde 29744,40 hasta 29683,20. Medida del módulo: 61,20 puntos» (16:37, [A]).

## 2. Qué hace el motor

En 16:37 el motor **no reinicia**: continúa la lectura arrastrada desde 16:36 y emite la cascada R0025 → R0026 → R0027 → R0029 → R0030 → R0031 → R0032. En particular:

- A Grande termina en 29744,40 y la superación de 127 % + 0,25 produce **AUT** (E000341, `SUPERA_127_MAS_025`) — es decir, aplica **H15/DEC-010**, regla cerrada que cita ese mismo precio como extremo de A Grande.
- El «1» posterior nace como R0029 con módulo 29725,10 → 29744,40 (19,30) y su A mide 29744,40 → 29717,60 = **26,80** (E000347); después R0030/R0031 fragmentan 20,80 y 15,10.
- **Entre `sequence_id` 5775 (16:37:48,547) y 5832 (16:38:00,178) el motor no emite ningún evento**, pese a que en 5827 el precio marca el mínimo 29683,20 (21,00 puntos por debajo de 29704,20).
- Consecuencia: el módulo de 61,20 **nunca existe** en la salida; el mínimo físico de la vela queda consumido sin evento.

## 3. Por qué no es un simple `BUG_MOTOR`

- El motor es coherente con **H15 (DEC-010, CERRADA)**, que manda extender A Grande hasta 29744,40 y confirmar AUT al superar 127 % + 0,25.
- El golden 16:37 declara «El análisis independiente comienza en esta vela» y clasifica la vela como 1 bajista con módulo H−L de 61,20.
- **No existe regla cerrada que autorice ese reinicio/lectura independiente**: `REGLAS_CERRADAS.md` no contiene ninguna regla de reinicio, dominancia ni lectura independiente (búsqueda literal sin resultados).
- Además hay tensión interna documental: **A1** mide 1 y 2 por desplazamiento direccional (no H−L), mientras **A2** fija el rango del módulo por H−L del conjunto de velas. El golden aplica A2 (61,20); el motor aplica A1 (26,80 / 20,80).
- Clasificación corregida: **`REGLA_ABIERTA`** (no `BUG_MOTOR`), con dos preguntas para Javier:
  1. ¿La lectura independiente de 16:37 es un reinicio autorizado (y con qué criterio: extremo en el último segundo, nuevo mínimo tras B fallida, otro)?
  2. ¿El tamaño del módulo es H−L del conjunto (A2, golden) o desplazamiento direccional (A1, motor)?

Mientras no se respondan, el motor no puede «corregirse» sin inventar regla: cualquier parche sería una decisión teórica encubierta.

## 4. Consecuencia para la cadena

- F1 sigue **bloqueando** el cierre funcional, pero su responsable no es DS: requiere decisión de Javier.
- La observación A1 de MiMo y F1 son **el mismo nudo**, no dos defectos independientes. Deben resolverse juntos.
- A2 (umbral plano) sí queda respaldada documentalmente: v003 §9, líneas 307-310, ya fija «< 0,25 plano; 0,25 o superior no es plano». El motor implementa lo correcto; la redacción «≤ 1 tick = plano» de H14 es la que contradice al golden. Sin decisión pendiente salvo ratificar la corrección de H14.
- No autoriza replay ciego, AFS2 ni producción. No modifica v0.7.5.1; toda corrección exige v0.7.5.2 y ZIP nuevos.
