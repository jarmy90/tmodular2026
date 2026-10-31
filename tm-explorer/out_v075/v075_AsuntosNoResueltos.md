# Asuntos no resueltos v0.7.5

## Reglas o semantica abierta
- `post_tt_fallido_no_definido`
- `ft_expiracion_no_definida`
- `entrada_tardia_ft_no_definida`
- `a_mayor_que_modulo_guardia_provisional`
- `aut_extra_tick_unidad_cerrada_0_25`
- `cobertura_estructural_definicion_por_confirmar`
- `functional_coverage_causal_parcial`
- `geometric_coverage_causal_parcial`
- `lectura_abierta_al_final:R0063`
- `AUT`: se evalua al confirmar un movimiento, no en cada tick intermedio; verificar si la regla exige tick exacto.

## Cobertura
- Causal geometrica: `1314/1335`.
- Causal funcional: `1263/1335`.
- Ticks sin owner: `334`.
- La cobertura parcial es informativa; no se fuerza con lecturas futuras.

## Proceso
- La aprobacion de Javier sobre los cuatro tests v0.7.4 corregidos sigue sin registrarse.
- Faltan los documentos de prioridad/dossier indicados en `AGENTS.md`.
- `AFS2_READY=true` no implica cobertura funcional total ni cierre de reglas pendientes.
