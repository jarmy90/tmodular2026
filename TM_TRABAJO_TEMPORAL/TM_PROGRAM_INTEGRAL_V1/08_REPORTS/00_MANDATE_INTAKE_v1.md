# TM_PROGRAM_INTEGRAL_V1 — Acta de recepción del mandato

**Fecha:** 2026-10-30
**Estado:** `INTAKE_ONLY / MANDATE_TRUNCATED`
**Ejecución de fases:** no iniciada
**Originales modificados:** ninguno
**tree_modified = false · engine_modified = false · goldens_modified = false**

---

## 1. Qué se recibió

| Sección | Contenido | Estado |
|---|---|---|
| 0 | Principio de avance automático y condiciones de parada | completo |
| 1 | Fuentes, hashes y precedencia | completo |
| 2 | Protección de originales y estructura de carpetas | completo |
| 3 | Principios constitucionales y ontología | completo |
| 4 | Reglas ya cerradas | **truncado** en `PLANO`: `|Open - Close_previo| < 0,25 → plano` |
| 5–final | Fases A–H, gates, entregables, validación ciega, lector en directo | **no recibido** |

El mensaje termina literalmente en la primera regla de la sección 4. No hay definición de:

- las fases A, B, C, D, E, F, G y H;
- los gates de cada fase;
- los entregables por fase;
- el protocolo de validación ciega;
- la especificación del lector en directo;
- el criterio de cierre del programa.

## 2. Qué se ha preparado (sin ejecutar fases)

### 2.1 Estructura

```text
TM_TRABAJO_TEMPORAL/TM_PROGRAM_INTEGRAL_V1/
  00_INPUTS/
  01_TREE_VALIDATION/
  02_TREE_EXECUTABLE/
  03_TEST_SPECIFICATION/
  04_ENGINE_SOURCE/
  05_TREE_ENGINE_COMPARISON/
  06_BLIND_VALIDATION/
  07_LIVE_READER_PREPARATION/
  08_REPORTS/
  09_MANIFEST/
  10_ROLLBACK/
```

### 2.2 Verificación de fuentes

Las once fuentes existen y su SHA-256 coincide con el esperado:

| Rol | SHA-256 (16 primeros) | Estado |
|---|---|---|
| Árbol v2.19 | `94A1408A6123ED66` | verificado |
| Certificado v2.19 | `995951E54A1F20FB` | verificado |
| Lecturas v005 | `F5D7550C42C90897` | verificado |
| Tickfeed maestro | `5F701BE2307352CB` | verificado |
| R3 congelado | `71D9A97AC2C49848` | verificado |
| R5 auditado | `9BD1BEDB5DEC8C5A` | verificado |
| R5 empaquetado (copia) | `19A847C078E12461` | verificado |
| Motor activo anterior | `4A2877CC7F47E056` | verificado |
| ZIP R3 | `450379BD5F1E2238` | verificado |
| ZIP R5 lectura | `DDC6AE2FFA9854FD` | verificado |
| ZIP R5 post-cut | `4238D0E1FD6ECC9E` | verificado |

Manifiesto completo: `00_INPUTS/INPUT_MANIFEST.json`.

### 2.3 Rollback

`10_ROLLBACK/ROLLBACK_PLAN_v1.md`. No se ha modificado ningún original; el rollback consiste en eliminar únicamente `TM_PROGRAM_INTEGRAL_V1/`.

## 3. Mapa provisional de fases (NO ejecutado, NO autorizado por el mandato)

La estructura de carpetas sugiere ocho fases, pero **el mandato no las define**. Se propone el siguiente mapa solo para facilitar la respuesta; no se ha ejecutado ninguna:

| Fase | Carpeta | Objetivo probable |
|---|---|---|
| A | `01_TREE_VALIDATION` | validar el árbol: completitud, contradicciones, precedencia |
| B | `02_TREE_EXECUTABLE` | convertirlo en especificación ejecutable |
| C | `03_TEST_SPECIFICATION` | especificar pruebas por concepto |
| D | `04_ENGINE_SOURCE` | implementar el motor |
| E | `05_TREE_ENGINE_COMPARISON` | comparar árbol y motor |
| F | `06_BLIND_VALIDATION` | validación ciega |
| G | `07_LIVE_READER_PREPARATION` | preparar el lector en directo |
| H | `08_REPORTS` | consolidar y cerrar |

Este mapa es una **hipótesis de trabajo**, no una interpretación del mandato. No debe usarse para avanzar sin la definición real de fases y gates.

## 4. Qué falta exactamente

Para poder ejecutar el programa sin inventar semántica, hace falta el resto del mensaje, desde:

```text
4. REGLAS YA CERRADAS
PLANO
|Open - Close_previo| < 0,25
→ plano
```

hasta el final, incluyendo:

1. el resto de reglas cerradas (plano, gap, 2, 3, A, B, C, AUT, CUT, TT, FT);
2. la definición de las fases A–H;
3. los gates de cada fase;
4. los entregables obligatorios por fase;
5. el protocolo de validación ciega;
6. la especificación del lector en directo;
7. el criterio de cierre y las condiciones de rollback.

## 5. Decisión

No se inicia ninguna fase. Hacerlo obligaría a inventar la definición de A–H y sus gates, lo que violaría el propio mandato (`no inventar semántica`, `detenerse si una fase no está definida`).

Se reanudará en cuanto se reciba la parte faltante.
