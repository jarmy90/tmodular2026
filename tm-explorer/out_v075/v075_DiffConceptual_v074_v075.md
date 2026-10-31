# Diff conceptual v0.7.4 -> v0.7.5

## Separacion de tiempos
- v0.7.4 usaba un unico tiempo de evento y podia registrar un TT con el tiempo estructural del cruce.
- v0.7.5 separa `structural_time`, `confirmation_time` y `knowledge_time`; publica en `time` el conocimiento.

## Arquitectura
- El constructor de movimientos pasa de una pasada final a `MovementBuilder` incremental.
- El scheduler de vela/gap pasa a `TickScheduler` y ejecuta GAP antes de las ramas de lectura.
- El motor ya no ordena ni reindexa eventos al final: `event_id` es append-only y `sequence_id` es el seq real del feed en conocimiento.

## Estado y auditoria
- La auditoria por tick registra owner explicito (`C/B/A/MODULE/NOISE/NONE`), lectura propietaria, seq de conocimiento y cobertura.
- La narrativa de vela usa el snapshot de cierre, no el estado final del motor.
- La cobertura causal exige que la lectura y A fueran conocidas antes de la confirmacion del swing.

## TT y AUT
- TT solo se emite despues de B Grande conocida; conserva el tiempo estructural del cruce.
- B Grande se emite antes de AUT; AUT reclasifica el recorrido y no se borra la cronologia anterior.

## Lo que no cambia
- No se anaden reglas TM nuevas.
- No se hardcodean precios, horas ni IDs.
- La geometria funcional de v0.7.4 se conserva y se valida por tests y diff de salida.
