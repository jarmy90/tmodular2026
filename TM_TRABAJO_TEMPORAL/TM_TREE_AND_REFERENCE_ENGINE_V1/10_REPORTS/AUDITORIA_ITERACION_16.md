# AUDITORIA ITERACION 16

## FASE 1 — Que interprete ejecuta cada suite

Antes de esta iteracion el agregador deducia la autoridad del texto de consola
y no exigia un motor concreto.

Ahora `run_iteration_16_all.py` fija en el entorno de todas las suites:

```text
TM_READER_MODULE       = tm_reference_interpreter_v1_direct_aut
TM_READER_SHA256       = hash del archivo en el momento de la ejecucion
TM_READER_CORE_VERSION = TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT
TM_REFERENCE_ENGINE_DIR= 05_REFERENCE_ENGINE
```

y `tm_reader_guard.verify()` aborta la suite si:

- el modulo importado no es el candidato;
- el SHA-256 no coincide con el exigido;
- falta `CORE_VERSION` o no coincide con el exigido.

`SUITE_ENGINE_MAP.csv` registra por suite: modulo importado, ruta absoluta,
SHA-256, CORE_VERSION, estado del binding, pruebas y recuento por autoridad.
Resultado de esta ejecucion: 8/8 suites con binding OK.

## FASE 2 — T-015 sin compatibilidad silenciosa

Antes:

```python
def _gap_ok(reading, origin, direction):
    if not hasattr(reading, "new_one_status"):
        return reading.mod_size == 200   # semantica historica aceptada
    return (reading.new_one_status == "NEW_ONE_ACTIVE" and ...)
```

Ese fallback aceptaba el resultado del motor antiguo. Se elimino por completo.
La expectativa de T-015 es ahora la del patch v2.19: 0,25 exactos no son plano,
2 queda prohibido y se registra la secuencia implicita
(`GAP_IMPLICIT_SEQUENCE`, `GAP_IMPLICIT_NEW_ONE`) con origen exactamente en la
apertura. Si el interprete no tiene esos campos o eventos, T-015 falla.

## FASE 3 — Autoridad corregida

La autoridad se lee del campo `classification` de cada CSV (estructura), no de
la salida de consola.

| Bloque | Total | CANONICAL | PROVISIONAL | OPEN_RULE |
|---|---|---|---|---|
| core | 19 | 19 | 0 | 0 |
| A/B/B Grande/AUT | 32 | 29 | 3 | 0 |
| AUT directo por A | 17 | 1 | 16 | 0 |
| C / CUT | 18 | 0 | 18 | 0 |
| gap / concurrencia | 16 | 16 | 0 | 0 |
| TT | 12 | 12 | 0 | 0 |
| ciclo / FT | 18 | 16 | 2 | 0 |
| gap prioridad / plano | 14 | 11 | 0 | 3 |
| **Total** | **146** | **104** | **39** | **3** |

Motivo de las provisionales:

- las 16 de AUT directo y las 18 de C/CUT construyen su fixture con una A/B
  nacida por la autonomia provisional del retorno (`A_CONF`). La regla bajo
  prueba (AUT directo, C Grande, CUT, C usada como tendencia) es canonica, pero
  su precondicion en el banco de pruebas no lo es;
- A-01 depende de la referencia orientativa del 35 %;
- BG-15 y BG-16 dependen de la autonomia provisional del retorno;
- FT-03 y FT-06 dependen del tick exacto / del filtro de 2 puntos como
  confirmacion suficiente.

Bloqueadas (open rule): GP-04, GP-05, GP-06.
No se intenta conservar el total anterior 128/16/2.

## FASE 4 — Alcance de la comparacion humana

Metricas corregidas (`run_human_segments_16.py`):

```text
human_anchors_total                    19
human_anchors_passed                    6
trace_rows_generated                 4400
human_segments_validated                6
ticks_with_independent_human_label      0
```

La lectura humana v005 no etiqueta tick a tick: define anclas por vela y
segmentos con estado esperado, evento final y autoridad. `trace_rows_generated`
no es una metrica de fidelidad.

Segmentos validados: 16:15 (1 inicial), 16:16 (2 no confirma, modulo 28,5),
16:17 (A 9,1), 16:18 (AUT + TT pendiente 29829,1), 16:24 (TT bajista
confirmado/extendido con nuevo 1 a 29828,1), 16:25 (gap +14, sin 2, secuencia
implicita, nuevo 1 desde 29848,5).

Segmentos que fallan: 16:19 (1 local), 16:20 (2 local), 16:21 (3 local), 16:22
(AUT local), 16:23 (AUT local y nuevo 1 29852,6->29837,3), 16:25 TT alcista,
16:26 FT del TT de 16:25, 16:27 A/B/A-tendencia con TT pendiente, 16:28 dos TT
coexistentes, 16:29 dos TT culminados, 16:30 modulo 53,6, 16:31 TT pendiente
3,10 puntos, 16:32 TT fallido por cruce de FINAL_A.

## FASE 5 — Superar el 35 %

`PROVISIONAL_INTERNAL_RATIO = 35` queda aislado como constante configurable con
comentario explicito. Ya no hay literales `35` en el motor. Ninguna prueba que
dependa de esa frontera es CANONICAL_PASS.

## FASE 6 — Identidad del interprete

La cabecera del motor ya no dice que C, CUT, TT, FT, gap-new-1 y concurrencia no
estan implementados. Declara el estado real por capas:

```text
IMPLEMENTADO_CANONICO
IMPLEMENTADO_PROVISIONAL
OPEN_RULE_BLOCK
NO_IMPLEMENTADO
```

## FASE 7 — Validacion 16:25-16:32

Resultado: **5 anclas de 16:15-16:24 validadas (16:15, 16:16, 16:17, 16:18, 16:24); 16:25-16:32 NO validado.**

Correcciones estructurales aplicadas:

- **RC-1:** la rotacion administrativa por `NEW_ONE` se elimino del motor. Un
  nuevo 1 que no cerro TT no rota al cambiar de vela. Solo rotan el TT cerrado y
  el nuevo 1 de `C_USED_AS_TREND`. Antes de esta correccion cada vela de
  16:25-16:32 abria un ciclo nuevo por gap y el lector quedaba atrapado
  extendiendo un unico nuevo 1.
- **RC-2:** el TT del ciclo archivado queda congelado (`tt_archived`): conserva
  objetivo y extremo para FT y trazabilidad, pero no sigue extendiendose ni
  arbitrando dentro de la estructura nueva.

Intentos rechazados (documentados y revertidos):

- **RC-3:** exigir el 35 % del retorno para confirmar A de un nuevo 1. Resultado:
  A de 115 puntos que se comia 16:26-16:31 y rompia 16:23/16:24.
- **RC-4:** priorizar la extension de A sobre la reanudacion del modulo. Mismo
  efecto; revertido.

Divergencias que siguen abiertas en 16:25-16:32:

1. 16:25 carece de TT alcista. Los archivos no determinan su referencia
   (Q-TT-1625).
2. El motor mantiene un unico TT. 16:28 exige dos TT pendientes simultaneos de
   escalas distintas (Q-MULTI-TT).
3. En 16:26-16:27 la lectura principal debe desarrollar A -> B -> A usada como
   tendencia sin fragmentarse ni extenderse 115 puntos. La autonomia provisional
   del retorno no distingue esas escalas; no se promueve a canon.
4. La lectura local (L2) no se descubre en 16:19 ni en 16:22: el motor solo la
   crea por el disparador canonico de AUT directo cuando se activa la sonda
   local. Sin L2 no existen 2/3 locales ni el AUT local de 16:22-16:23.

## FASE 8 — Autoaprendizaje

Cada divergencia se itero con: ultimo segmento coincidente, reconstruccion de
lecturas vivas, tres hipotesis, rechazo de las que rompen bloques ya validados
(RC-3/RC-4), causa minima y reejecucion desde 16:15. No se inventaron precios
internos en el gap ni se uso informacion futura.
