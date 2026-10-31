# TM — INFORME BREVE DEL ÁRBOL CANÓNICO v1

- **Fecha:** 2026-10-19
- **Estado:** borrador completo para revisión de Javier.
- **Alcance:** documentación y especificación; sin programación.
- **Fuente principal:** `PROMPT_OPENBOT_TM_ARBOL_CANONICO.txt`.
- **Árbol:** `control/TM_ARBOL_CANONICO_COMPLETO_v1.md`.

## 1. Entregables creados

| Entregable | Ruta | Estado |
|---|---|---|
| Árbol canónico | `control/TM_ARBOL_CANONICO_COMPLETO_v1.md` | Creado; 40 nodos `N-001`–`N-040` |
| Dudas para Javier | `control/TM_DUDAS_PENDIENTES_JAVIER.md` | Creado; 5 preguntas bloqueantes |
| Matriz de transiciones | `control/TM_MATRIZ_TRANSICIONES_v1.csv` | Creado; 40 filas × 16 columnas |
| Tests requeridos | `control/TM_TESTS_REQUERIDOS_v1.md` | Creado; 45 tests |
| Informe breve | `control/TM_INFORME_ARBOL_CANONICO_v1.md` | Este documento |

## 2. Contenido cerrado

- Arquitectura A: controlador de concurrencia L1–L3.
- Arquitectura B: máquina de estados por lectura.
- Arquitectura C: árbol completo de transiciones.
- Arquitectura D: precondiciones y prohibiciones globales.
- Arquitectura E: fórmulas y fronteras exactas.
- Arquitectura F: historial sin borrado.
- Arquitectura G: caso validado de vela 1–4.
- Arquitectura H: catálogo de 45 tests.
- Arquitectura I: registro de 5 dudas bloqueantes.

## 3. Caso validado

- Vela 1: `1` alcista, rango `9,80`.
- Vela 2: `A`, `B`, `AUT`; final de A `29179,20`; TT `29189,00`.
- Vela 3: máximo `29189,30`; TT confirmado; `nuevo 1` de L1.
- L1 cerrada correctamente.
- Segunda lectura observada en vela 3: módulo `5,40`; TT `29187,40`; nuevo 1 hasta `29189,30`.
- Esa segunda lectura **no se abre** por falta de regla expresa: `DUDA-J01`.
- No se afirma que la vela 3 contenga A/B/AUT propios de L1.

## 4. Dudas bloqueantes

1. `DUDA-J01`: apertura de L2/L3.
2. `DUDA-J02`: composición general del módulo.
3. `DUDA-J03`: prioridad cuando dos o tres lecturas alcanzan nivel en el mismo tick.
4. `DUDA-J04`: condición exacta de `C = nuevo 1`.
5. `DUDA-J05`: regla matemática completa de FT.

## 5. Incidencia de control

Antes de recibir el prompt de crear archivos nuevos, se registraron cambios en documentos vigentes para documentar `DEC-015` y la concurrencia 2/3:

- `control/DECISIONES_EXPERTO.md`
- `control/REGLAS_CERRADAS.md`
- `control/DICCIONARIO_TM.md`
- `Dossier_TM_v3_Lectura_Obligatoria.txt`
- `Dossier_TM_v4_Concurrencia_Reclasificacion.txt`
- `00_LEEME_PRIMERO_PRIORIDAD_DOCUMENTOS_TM.txt`

El prompt nuevo prohíbe modificar documentos vigentes. Estos cambios no se han revertido. Javier confirmó que se conservan como `DEC-015`; no se editarán más documentos vigentes en esta fase.

No se modificó código, golden ni tests. No se ejecutaron tests. No se creó `CASOS_VALIDADOS.md` porque no existe.

## 6. Verificación realizada

- `TM_MATRIZ_TRANSICIONES_v1.csv`: 40 filas, 16 columnas, `N-001`–`N-040`.
- `TM_TESTS_REQUERIDOS_v1.md`: 45 tests, 15 positivos, 12 negativos, 8 frontera, 5 cronología, 5 concurrencia.
- Todos los IDs de test citados por el árbol existen en el catálogo.
- `TM_ARBOL_CANONICO_COMPLETO_v1.md`: 1191 líneas, sin caracteres de reemplazo.
- `TM_DUDAS_PENDIENTES_JAVIER.md`: 5 preguntas bloqueantes, cada una con opciones A/B/C.

## 7. Siguiente paso

1. Javier responde el bloque de 5 dudas.
2. Se cierran o reclasifican las ramas `PENDIENTE_JAVIER`.
3. Se actualiza el árbol y la matriz con las decisiones.
4. Solo después se implementan los tests.
