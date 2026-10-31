# AUDITORÍA — ITERACIÓN 14

## 1. Objetivo de la iteración

Cerrar las tres respuestas expertas (Q-ONE-AT-CLOSE, Q-GAP-TT, Q-CONCURRENCY 16:23)
y repetir la comparación humana de los cuatro bloques **tick a tick**, sin añadir
heurísticas nuevas.

## 2. Cambios realizados en el intérprete

Archivo: `05_REFERENCE_ENGINE/tm_reference_interpreter_v1_direct_aut.py`

| Cambio | Estado | Verificado |
|---|---|---|
| 1 confirmado al cierre de su propia vela (`_confirm_one_at_close`), con `knowledge_time` = último tick de la vela | implementado | sí (B1/B2) |
| `feed()` público + `run()` como bucle de ticks (permite lectura en streaming) | implementado | sí (146 pruebas) |
| Módulo integrado del AUT en campos propios (`aut_mod_*`), sin reescribir el módulo del ciclo | implementado | sí |
| `local_mode` con AUT local al 100 % del origen de A | implementado, **sonda apagada** | no verificado |
| Sonda de lectura local (`local_probe`, apagada por defecto) | experimental | declarada y divergente |

No se modificó ninguna regla TM. No se cambió el umbral 127 % + 0,25 de la vía
principal. No se congeló el árbol ni se tocó el motor oficial.

## 3. Pruebas

```
total 146 | pass 146 | fail 0
canónicas 128 | provisionales 16 | open_rule 2
```

Suites: núcleo 19, A/B/B Grande/AUT 32, AUT directo 17, C/CUT 18,
gap/concurrencia 16, TT 12, ciclo/FT 18, gap-prioridad/plano 14.

Regresión nueva añadida en Iteración 14:
`GP-12 doble pertenencia: TT heredado confirmado + nuevo 1 desde el OPEN`.

## 4. Comparación humana tick a tick (v005)

Convención causal: el estado de cierre de vela se conoce con el primer tick de la
vela siguiente; `knowledge_time` conserva el último tick de la vela cerrada.
No es un adelanto de información: es el instante en que la vela existe cerrada.

| Bloque | Anclas | Primera divergencia |
|---|---|---|
| B1 16:15–16:18 | 4/4 | ninguna |
| B2 16:19–16:22 | 4/4 | ninguna |
| B3 16:22–16:24 | 2/3 | **16:23:02.021, seq 1846** |
| B4 16:24–16:25 | 3/3 | ninguna |

### Primera divergencia exacta

```
sequence_id : 1846
hora        : 16:23:02.021
precio      : 29842,8
humano      : A Grande bajista de la lectura LOCAL, nacida en 29850,8,
              con extremo 29842,8 (A = 8,0 puntos sobre el nuevo 1 local
              alcista 29830,3 -> 29850,8).
python (L1) : A = 9,1 desde 29848,5; nuevo 1 bajista 29857,6 -> 29830,3;
              TT principal 29829,1 pendiente.
```

La lectura principal es correcta: en 16:23 continúa el AUT bajista de 16:18 y su
TT principal. Lo que falta es la **lectura local anidada** que el humano declara
en 16:22 (A 20,5 desde 29830,3; AUT directo alcista; nuevo 1 con extremo 29850,8).

## 5. Sonda de lectura local (experimental, apagada)

Se probó una lectura secundaria que nace en la primera vela del nuevo 1 dominante
y se declara cuando su AUT directo confirma. Resultado:

- 16:22: AUT directo y nuevo 1 con `origin` 29830,3 y extremo 29850,8 → coincide
  con el humano.
- 16:23: la A contraria nace correctamente en 29850,8 con extremo 29842,8, pero
  la transición posterior (B que recupera el origen de A → AUT local) queda
  absorbida por la extensión del módulo y el estado se degrada.

Conclusión: la sonda **no se declara implementada**. Queda apagada
(`local_probe = False`) y se registra como regla abierta.

## 6. Qué es provisional

- La autonomía del retorno (16 pruebas `PROVISIONAL_POLICY_PASS`).
- El umbral local de AUT al 100 % (implementado solo en la sonda apagada).
- FT: tick exacto de confirmación y suficiencia del filtro de 2 puntos.

## 7. Qué queda abierto

Ver `09_OPEN_RULES/OPEN_RULES_ITERACION_14.md`:

- Q-L2-BIRTH: regla de nacimiento y declaración de la lectura local.
- Q-L2-ABSORB: precedencia entre absorción por módulo y B estructural en la
  lectura local.
- Q-TT-ALCISTA-1624: el texto humano de 16:24 dice "TT alcista no alcanzado" y
  el golden v003 dice que el TT principal bajista 29829,1 se alcanza a las
  16:24:44.990. No son el mismo TT; falta fijar cuál manda en la ficha de 16:24.

## 8. Estado

```
GATE_AUT_DIRECT_BY_A_PASS          (sin cambios)
GATE_C_GRANDE_TREND_PASS           (sin cambios)
GATE_TICK_COMPARISON_3_OF_4        FAILED_EN_B3
TREE_STATUS                        NOT_READY_TO_FREEZE_TREE
REFERENCE_ENGINE_STATUS            REFERENCE_ENGINE_INCONSISTENT_IN_LOCAL_READING
PATTERN_ENGINE_STATUS              PATTERN_ENGINE_INCOMPLETE
```
