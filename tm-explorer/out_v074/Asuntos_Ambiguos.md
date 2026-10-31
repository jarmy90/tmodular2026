# Asuntos ambiguos de v0.7.4

Estos puntos no bloquean la entrega técnica, pero sí una declaración de cierre conceptual.

## A1. Límite de A respecto al módulo

La regla canónica provisional dice que A Grande termina cuando supera el módulo. El caso validado contradice esa lectura: `A=78.30` sobre `x=65.20` debe seguir produciendo TT `29615.20` y FT.

Decisión actual: permitir A mayor que el módulo y cerrar solo si `A > 2 * x` con `A_SIGNIFICATIVA` abierta.

Pendiente: confirmar si 2x es el límite correcto, si depende de escala o si A nunca invalida por tamaño.

## A2. TT 100: primer cruce o extremo del movimiento

El motor registra `tt_100_price=29614.20` (primer tick que cruza `29615.20`) y `tt_real_extreme=29600.20` (extremo posterior de B).

Pendiente: decidir si el “100%” debe reportarse con el primer cruce o con el extremo real del movimiento. El TT y el FT no cambian; cambia el valor de auditoría.

## A3. Mínimo de B

La hipótesis humana usa `29600.70`. El feed produce `29600.20` como mínimo posterior dentro de B. El TT `29615.20` y el FT se mantienen.

Pendiente: confirmar que el mínimo estructural es el mínimo real del feed y no un nivel intermedio de la hipótesis.

## A4. FT: expiración y entrada tardía

El motor confirma FT con el primer contrario posterior al TT. No hay regla cerrada para:

- cuánto tiempo puede esperar el FT;
- si un FT tardío sigue siendo válido;
- si debe existir una ventana máxima después del TT;
- qué pasa si el precio vuelve al TT antes del FT.

## A5. `post_tt_fallido`

No está definido si un TT que falla después de confirmarse debe:

- abrir una nueva lectura;
- cerrar la lectura con una función específica;
- conservar el TT como referencia histórica;
- generar un CUT;
- o quedar como asunto pendiente sin función inventada.

## A6. CUT con buffer

El buffer de `2.00` puntos resolvió el caso de `29624.80 -> 29626.70` (1.90 puntos), que no debía cortar. Falta confirmar:

- si el buffer es fijo o proporcional al módulo;
- si se mide contra `a_end` o contra el origen de B;
- si aplica a todos los TT o solo a TT confirmados.

## A7. Máximo de lecturas activas

Se aplica `MAX_ACTIVE=3` con archivo por capacidad. Falta confirmar:

- si el límite es universal;
- si la prioridad debe ser por `x`, por antigüedad o por función;
- si una lectura archivada puede reabrirse.

## A8. Granularidad del módulo de 16:45

Hay dos lecturas posibles: `11.00` y `25.30`. La diferencia afecta la genealogía y la cobertura, no el caso clave de `65.20`.

Pendiente: decisión experta sobre el origen y el extremo válidos.

## A9. Cobertura: módulo o módulo + A/B/C

La cobertura actual considera módulo, A, B y C. Con esa definición, los 1,335 swings quedan cubiertos. Si se exige solo el módulo, quedan 22 uncovered.

Pendiente: confirmar la definición canónica de cobertura funcional.

## A10. Escala macro

El motor no mantiene un stream macro separado de 40 puntos. La macro se reconstruye desde los módulos locales. Falta confirmar si eso es suficiente para todos los casos o si se requiere una lectura macro explícita.

## A11. Numeración de lecturas

`proto10.py` llama `R0063` a la lectura clave. v0.7.4 la llama `R0062` porque arranca desde el feed completo. La geometría es equivalente; la diferencia es de asignación de IDs.

## A12. Documentos y versión

No están disponibles físicamente:

- `00_LEEME_PRIMERO_PRIORIDAD_DOCUMENTOS_TM.txt`
- `Dossier_TM_v3_Lectura_Obligatoria.txt`
- adenda `Dossier_TM_v4_Concurrencia_Reclasificacion.txt`
- `CASOS_VALIDADOS.md`
- `v2.13.3`

La autoridad usada es `v2.14` y el árbol canónico disponible. Cualquier cierre definitivo debe contrastarse con esos documentos.
