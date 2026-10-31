# AUDITORÍA INDEPENDIENTE 19B — TT, EXTREMO FUNCIONAL, FT Y ARCHIVO DE LOCAL-G1

Alcance: cadena 16:25 TT alcista → extremo → FT → A principal → archivo de
LOCAL-G1 → decisión sobre LOCAL-G2. No se toca 16:27–16:32.

Lectura humana tratada como HUMAN_EXPERT_HYPOTHESIS. Jerarquía aplicada:
reglas TM cerradas > causalidad tick a tick > coherencia funcional > propiedad
de referencias > lectura humana > políticas provisionales.

---

## 1. Defecto encontrado en el checkpoint 19A

`LOCAL-G1-TT-2987050` guardaba como extremo el **precio de confirmación**
(29870,6) y no el extremo real del patrón. Consecuencias en cadena:

1. `physical_extreme` inexistente: no había campo distinto de `confirmed_price`.
2. El FT nacía del precio de confirmación (29870,6), 4,8 puntos por debajo del
   máximo real, y por tanto **antes** de que el TT terminase de extenderse.
3. El archivo de LOCAL-G1 se decidía con el precio de confirmación, no con el
   conocimiento del extremo funcional.
4. El registro legacy (`ITER18_TT_OWNERS.csv`, `ITER18_GENERATIONS.csv`) se
   creaba una sola vez y quedaba congelado en `closed_at=0` / `TT_EXTENDED`,
   contradiciendo al checkpoint.

Ninguna de estas piezas usaba precios literales en el motor: el error era de
**modelo** (un solo campo para tres conceptos), no de umbral.

---

## 2. Escenas evaluadas

| scene | tesis | tt_objective | confirmed_price/seq | physical_extreme/seq | functional_extreme | FT_origin | A_origin | resultado |
|---|---|---|---|---|---|---|---|---|
| A | el TT termina al alcanzar el objetivo | 2987050 | 2987060 / 2519 | 2987060 / 2519 | 2987060 | 2987060 | 2987060 | RECHAZADA |
| B | el TT se extiende; el extremo funcional se confirma al aparecer autonomía contraria | 2987050 | 2987060 / 2519 | 2987540 / 2532 | 2987540 (kt 2535) | 2987540 | 2987540 | **ACEPTADA** |
| C | parte de la "extensión" pertenece a otra función/lectura | — | — | — | — | — | — | RECHAZADA para 16:25; PARCIAL en 16:26 |

Rechazo de A: entre 2519 y 2532 el precio sigue subiendo hasta 29875,4 sin que
exista ningún recorrido contrario con autonomía; etiquetar el extremo en 2519
exigiría información futura (saber que después sube) o negar el máximo físico.
Además obligaría a que el FT naciera en 29870,6, contradiciendo el retroceso
real de 600 que arranca en 29875,4 y el origen que la lectura principal
registra de forma independiente para A.

Rechazo de C en 16:25: mientras LOCAL-G1 es la única generación local viva, no
hay segundo propietario al que asignar la extensión; el TT principal está en
29829,1 (bajista, otro propietario) y no puede reclamarla. C se conserva solo
para 16:26, donde A principal (PRIMARY-G1) y FT (LOCAL-G1) comparten origen
físico con propietarios distintos.

---

## 3. Evidencia tick a tick (BID, seq → hecho)

| seq | hora | precio | evento | lectura |
|---|---|---|---|---|
| 2519 | 16:25:52.041 | 29870,6 | TT_100_REACHED → TT_CONFIRMED | objetivo 29870,5 superado |
| 2520-2522 | 16:25:52.237-.641 | 29871,3 → 29871,8 | TT_EXTENDED ×3 | extensión, no cierre |
| 2523 | 16:25:52.842 | 29871,6 | FT_POSSIBLE (origen 29871,8) | candidato 1 |
| 2525 | 16:25:53.241 | 29873,4 | TT_EXTENDED + FT_ABSORBED_BY_TT_EXTENSION | retroceso interno |
| 2526-2527 | 16:25:53.6-.8 | 29874,0 → 29874,1 | TT_EXTENDED ×2 | nuevo extremo |
| 2528 | 16:25:54.043 | 29873,8 | FT_POSSIBLE (origen 29874,1) | candidato 2 |
| 2531 | 16:25:54.648 | 29875,1 | TT_EXTENDED + FT_ABSORBED | retroceso interno |
| 2532 | 16:25:55.050 | 29875,4 | TT_EXTENDED | **extremo físico** |
| 2533 | 16:25:55.250 | 29875,3 | FT_POSSIBLE (origen 29875,4) | candidato 3 |
| 2535 | 16:25:55.655 | 29870,0 | FT_STRUCTURAL_CONFIRMED + TT_FUNCTIONAL_EXTREME_CONFIRMED | extremo funcional conocido; 600 puntos = 6,00 |
| 2548 | 16:25:59.075 | 29869,3 | FT_EXTENDED | FT sigue |
| 2553 | 16:26:00.081 | 29869,3 | LOCAL_G1_ARCHIVED (close_reason=TT_FUNCTIONAL_EXTREME_CONFIRMED) | archivo administrativo, slot libre |
| 2609 | 16:26:13.444 | 29865,8 | CONTRARY_MOVE_PENDING origin=29875,4 | A principal nace del mismo extremo |
| 2623 | 16:26:16.866 | 29865,3 | RETURN_MOVE_PENDING | retroceso dentro de A |

Candidatos FT absorbidos: 2 (29871,8 y 29874,1). Ningún FT nace del nivel del
100 % (29870,5) ni del primer retroceso.

---

## 4. Extremo físico vs extremo funcional

- `physical_extreme` = 29875,4 (seq 2532). Máximo bruto del tramo.
- `functional_extreme` = 29875,4, `status=CONFIRMED`, `structural_time`=2532,
  `knowledge_time`=2535. En este tramo coinciden porque tras el máximo no hubo
  ninguna extensión posterior: el primer recorrido contrario autónomo (6,00
  puntos) ya no fue superado. El modelo los mantiene separados: si el TT vuelve
  a extenderse, `tt_extreme_status` pasa a `REOPENED` y la generación recupera
  ACTIVE (probado en FT-19B-11).
- Antes de 2535 el extremo es PROVISIONAL y no se archiva nada con él.

## 5. Regla general obtenida

```
TT alcanza objetivo → TT_CONFIRMED
mientras siga batiendo su extremo → physical_extreme se actualiza, TT_EXTENDED
si el precio supera el origen de un FT candidato → candidato ABSORBIDO (retroceso interno)
si aparece recorrido contrario con autonomía física (>= NOISE) desde el extremo
    → functional_extreme CONFIRMED (structural_time = tick del extremo,
                                    knowledge_time = tick actual)
    → FT nace del extremo funcional, no del nivel 100 %
    → generación propietaria pasa a CLOSING (no crea funciones nuevas)
    → al fijarse el conocimiento, archivo administrativo al abrir la vela
      siguiente, salvo que la apertura supere el extremo (entonces REOPENED)
    → patrones TT/FT conservados como históricos, slot liberado
```

Sin hora, sin precio y sin `sequence_id` concretos: la condición es el evento
`TT_FUNCTIONAL_EXTREME_CONFIRMED` sobre el propietario.

## 6. Ciclo de vida resultante de LOCAL-G1

| fase | seq | hora | hecho |
|---|---|---|---|
| OPEN/ACTIVE | 1792167600145 (16:19) | descubrimiento causal | 1 local 7,5 |
| ACTIVE | … | 16:19–16:25 | 1-2-3, módulo 19,7, A, AUT, TT 29870,5 |
| CLOSING (closure funcional) | 2535 | 16:25:55.655 | extremo funcional confirmado; `freeze_functions=True` |
| ARCHIVED (archivo administrativo) | 2553 | 16:26:00.081 | slot LOCAL libre; TT y FT históricos |

En CLOSING la capa de funciones queda congelada (`FUNCTION_LAYER_FROZEN`) pero
el patrón sigue vivo: `_on_tt_tick` puede extender el extremo y `_on_ft_tick`
sigue trazando el FT. Tras el archivo solo se emite `PATTERN_LAYER_ONLY`.

`archived_generation_writes = 0`: tras 2553 la capa de funciones no recibe
escrituras; solo la capa de patrones (FT) sigue trazando su extremo. La sonda
de continuidad (`freeze_on_closure=False`) confirma qué habría ocurrido sin
congelar: rotación del lector local, `n_origin=29828,1` heredado y `mod_size=0`;
por eso abrir LOCAL-G2 con ese estado sería heredar referencias.

## 7. Decisión sobre LOCAL-G2 — NOT_OPENED

Escenas contrastadas para 16:26:

- **MODULE**: exigiría un módulo por descarte propio de 16:26. El sondeo da
  `mod_size = 0` en 16:26–16:29: la caída no forma 1-2-3 (no hay 2 medible), y
  la continuación del lector local arrastra el `one` de LOCAL-G1 (29828,1).
  Abrir con eso sería heredar referencias.
- **FUNCTION**: A principal (PRIMARY-G1) + FT (LOCAL-G1) explican el tramo
  completo con propietarios distintos y origen común 29875,4.
- **ABSORBED**: compatible con lo anterior; el movimiento queda absorbido en A
  principal, que sigue creciendo hasta 29849,1.

Decisión: `NOT_OPENED`, escena `FUNCTION_AND_FT_EXPLAIN_16_26`, autoridad
CANONICAL, con 3 evidencias registradas. La lectura humana habla de "módulo
bajista por descarte"; el motor **no** lo materializa porque el módulo por
descarte sigue siendo OPEN_RULE (no hay regla cerrada que lo mida). Se registra
como duda residual, no como excepción codificada.

## 8. Resultado sobre la lectura humana

**HUMAN_READING_CONFIRMED_BY_TICKS** en la cadena 16:25–16:26:

- TT alcista confirmado y extendido hasta el máximo 29875,4: confirmado.
- FT del TT de 16:25 con origen en el máximo: confirmado.
- Inicio de A Grande bajista en la cola final de 16:25: confirmado
  (origen 29875,4; conocimiento 16:26:13.444).
- "Módulo bajista por descarte activo": **no verificado** por los ticks; queda
  como OPEN_RULE, sin corrección de la lectura (no se puede refutar ni afirmar
  sin la regla).

Corrección aplicada al **motor** (no a la lectura): el origen del FT pasó de
29871,8 (extremo provisional) a 29875,4; diferencia 3,60 puntos; efecto: FT y A
comparten origen y el archivo de LOCAL-G1 se decide por conocimiento del
extremo.

## 9. Políticas provisionales usadas

| política | uso | autoridad |
|---|---|---|
| NOISE = 2,00 puntos (autonomía física del recorrido contrario) | confirma FT | PROVISIONAL_POLICY_PASS |
| corredor del TT para descubrir L2 | sin cambios en 19B | PROVISIONAL |
| congelación de funciones en CLOSING | evita rotaciones y referencias heredadas; el patrón no se apaga | CANONICAL (estado del ciclo de vida) |
| 35 % de módulo | **no** decide el FT: 6,00/19,70 = 30,5 % → con el 35 % el FT no se habría confirmado | PROVISIONAL, no canónica |
| `tt_keep_first_pending` / `tt_no_invalidate` | no usadas para archivar (el archivo depende de identidad y vigencia) | PROVISIONAL |

## 10. Dudas residuales

1. Instante exacto de conocimiento del extremo funcional: el motor usa el
   primer recorrido contrario ≥ 2,00 puntos (2535). Un criterio estructural
   (proporción del módulo) daría 2536-2540. Afecta solo al `knowledge_time`,
   no al origen ni al propietario.
2. Módulo por descarte: sin regla cerrada, LOCAL-G2 no puede abrirse sin
   heredar referencias. Bloquea 16:26–16:29 en la lectura local, no en la
   principal.
3. El FT confirma por autonomía física (2,00 puntos) y no por proporción del
   módulo; se mantiene provisional y así se clasifica en la matriz.
