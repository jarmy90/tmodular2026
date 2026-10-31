# -*- coding: utf-8 -*-
"""Tree -> engine map for the v2.19 audit (CSV)."""
from __future__ import annotations

import csv
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "02_TREE_MAPPING" / "TREE_TO_ENGINE_MAP_v219.csv"

ROWS = [
    ("TREE-001", "N-001 / N-040", "1 nace con el primer desplazamiento direccional, sin mínimo teórico; su medida es desplazamiento, no High-Low",
     "MovementBuilder.feed", "333-390", "MISSING",
     "Exige 6,00 antes de tener dirección; CE-1/CE-3 sin lectura"),
    ("TREE-002", "N-013 / N-038", "A Grande y el propio 1 se extienden hasta su extremo real y atraviesan velas",
     "_update (MODULE)", "1072-1112", "WRONG",
     "Extiende module_extreme con cada movimiento de la misma dirección: absorbe 2 y 3"),
    ("TREE-003", "Ciclo de vida de 1 (implícito)", "1 debe tener candidatura, confirmación y congelación de medida",
     "_create_reading", "857-897", "MISSING",
     "No hay ONE_CANDIDATE ni ONE_CONFIRMED; la lectura nace ya MODULE y ya cerrada"),
    ("TREE-004", "N-006 / N-007 / N-008", "2 exige plano, sin gap, cola <= 0,25, misma dirección y 100 % de 1; imposible solo si se niega una condición",
     "local_two_gate / _process_local_sequence WAIT_TWO", "555 / 3005-3090", "PARTIAL",
     "Solo existe en LOCAL; LOCAL exige AUT primario previo; one_size = rango de vela"),
    ("TREE-005", "N-009 / N-010", "3 exige retroceso 0-50 % del rango de 2 y superación estricta del extremo de 2",
     "_process_local_sequence WAIT_THREE", "3025-3045", "WRONG",
     "Solo exige nuevo extremo >= 2,00; no evalúa retroceso"),
    ("TREE-006", "N-011", "Si falla 3, 1+2 forman módulo y el contrario es A Grande",
     "_two_impossible", "2988-3004", "PARTIAL",
     "Solo cubre gap/cola/ruptura; no hay rama de fallo de 3"),
    ("TREE-007", "N-012", "Módulo = rango de expansión (max high - min low) del conjunto de velas",
     "Reading.module_size / _create_reading", "254 / 879-884", "WRONG",
     "Módulo = |extremo - origen| del movimiento; CE-2 0->16 en vez de 0->10"),
    ("TREE-008", "N-013 / N-014 / N-015", "A Grande es el movimiento contrario al módulo y termina en su extremo real",
     "_update (MODULE->A)", "1072-1112", "PARTIAL",
     "Solo nace cuando un movimiento contrario de 6,00 se cierra; llega tarde"),
    ("TREE-009", "H12", "B candidata antes del 100 % de A; B Grande al alcanzar el 100 %",
     "BigBTracker.feed / _b_grande", "464-482 / 995-1025", "PARTIAL",
     "Condición 100 % correcta, pero A y B solo existen sobre movimientos cerrados de 6,00"),
    ("TREE-010", "N-016 / N-017 / H9", "AUT solo al superar estrictamente 127 % + 0,25; tocar mantiene B Grande",
     "BigBTracker.limit / _maybe_aut", "457 / 918-940", "CORRECT",
     "Matemática correcta; hereda a_size >= 6,00 y puede emitir B_GRANDE y AUT en el mismo tick"),
    ("TREE-011", "N-022", "C Grande solo después de B Grande confirmada",
     "begin_c / _legacy_tick_decision", "483-496 / 3330-3417", "INCONSISTENT",
     "LOCAL exige 6,00 de excursión; PRIMARY abre C con cualquier tick contrario"),
    ("TREE-012", "N-023", "Un nuevo extremo de B cancela C sin borrar historial",
     "_update (TT_PENDING)", "1236-1260", "PARTIAL",
     "Emite C_CANCELADA y borra c_origin; no conserva la C como historial consultable"),
    ("TREE-013", "N-024 / v1.2", "CUT contra el final de A o contra la base del módulo, según la rama",
     "_check_cut / _process_local_sequence C_ACTIVE", "942-970 / 3205-3220", "INCONSISTENT",
     "PRIMARY usa a_end +/- 2,00; LOCAL usa a_end congelado; no usa la base del módulo"),
    ("TREE-014", "N-018 / N-019 / N-039", "TT se confirma en el primer tick que alcanza el 100 % del objetivo",
     "_check_tt", "1027-1058", "WRONG",
     "Solo se evalúa al cerrar un movimiento y barre el rango; TT perdido con precio 12 puntos por encima"),
    ("TREE-015", "N-020", "TT fallido al tocar el final de A; recorrido anterior = módulo y retorno = A Grande",
     "_update TT_PENDING CUT", "1260-1300", "WRONG",
     "Exige a_end +/- 2,00 y emite CUT en lugar de la reclasificación canónica"),
    ("TREE-016", "N-026", "FT solo tras TT confirmado y pérdida de estructura del TT",
     "_update TT_EXT", "1312-1347", "WRONG",
     "Primer movimiento contrario cierra FT; no hay condición estructural ni variables"),
    ("TREE-017", "v2.19 §A-C", "Gap = A Grande, B Grande y A usada como tendencia implícitas; nuevo 1 en la apertura",
     "_schedule_gap", "1540-1558", "MISSING",
     "Solo emite GAP; no registra funciones implícitas ni nuevo 1"),
    ("TREE-018", "v2.3 §B / v2.19 §E", "Con gap no hay 2; la rama de gap se resuelve con los ticks siguientes",
     "_process_local_sequence gap guard", "3005-3013", "GATED",
     "Retorno temprano sin decisión; además LOCAL nunca está armado sin AUT previo"),
    ("TREE-019", "N-028 / N-029 / N-030", "Concurrencia regulada, referencias independientes, dominancia por estructura",
     "_owner / _make_local_reading", "1560-1583 / 2705-2728", "PARTIAL",
     "Dueño por module_size; sin regla de apertura L2/L3; máximo 3 por capacidad"),
    ("TREE-020", "N-039", "structural_time <= confirmation_time <= knowledge_time; conocimiento en el primer tick válido",
     "_emit / _check_tt", "752-827 / 1027-1058", "PARTIAL",
     "Campos correctos; la decisión se toma al cerrar movimiento y se backfillea el knowledge_time"),
    ("TREE-021", "v1.2 §13.6", "Función, patrón y evento son capas distintas y coexisten",
     "Reading.state / fail_reason", "162-252 / 899-914", "WRONG",
     "TT/FT/CUT se escriben en state; C sobre TT_EXT y FT como DONE"),
    ("TREE-022", "v2.5 §D y §H", "6,00 es filtro operativo; no puede alterar A, B, AUT, TT, C, CUT ni FT",
     "MOVE=600", "22, 334-362, 918, 2797, 3142, 3187, 3207", "CONSTITUTIONAL_VIOLATION",
     "MOVE se usa como mínimo estructural de 1, A, B, C y AUT"),
    ("TREE-023", "v2.13 / v2.16 / v2.17 / v2.19", "A y C usadas como tendencia son transformaciones con genealogía, no lecturas nuevas",
     "_new_local_reading_after_aut / _reclassify_c_as_new_1", "2837-2885 / 2925-2987", "PARTIAL",
     "Crea lectura nueva y cierra la anterior; no emite transition_reason canónico A_USED_AS_TREND"),
    ("TREE-024", "v2.7 §B", "Antes de abrir A/B/módulo se resuelve qué frontera se alcanza primero: TT 100 % o final de A",
     "no existe", "-", "MISSING",
     "No hay árbitro cronológico TT/final de A; CE-5 no puede evaluarlo"),
]

with OUT.open("w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["map_id", "tree_reference", "canonical_expectation", "engine_symbols", "engine_lines", "status", "evidence"])
    w.writerows(ROWS)
print("wrote", OUT, len(ROWS), "rows")
