# -*- coding: utf-8 -*-
"""Builds FREEBUFF_FIRST_DIVERGENCES_v219.csv from the raw reproduction."""
from __future__ import annotations

import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
RAW = json.loads((HERE / "ce_out" / "CE_REPRODUCTION_RAW.json").read_text(encoding="utf-8"))
BY = {c["id"]: c for c in RAW}

EXPECT = {
    "CE1-POS": (2, "1 abierta (origen 100,00; extremo 102,00; medida 2,00) y 2 candidata al abrir 102,00 en plano"),
    "CE1-NEG": (2, "1 abierta (100,00→102,00); 2 imposible al girar en 102,00; 1 = módulo por descarte y A Grande bajista"),
    "CE1-FRON": (2, "1 abierta (100,00→102,00); 2 candidata; 2 confirmada en 104,00 exactos"),
    "CE2-POS": (2, "1 abierta desde 0,00; módulo 10,00 al cerrar la pata (no 16,00)"),
    "CE2-NEG": (2, "1 abierta desde 0,00; módulo 10,00; A/B/C/TT hasta 3,90"),
    "CE2-FRON": (2, "1 abierta desde 0,00; módulo 10,00; CUT en 0,00 exactos"),
    "CE3-POS": (2, "1 abierta (0,00→6,00); 2 candidata desde 6,00; 2 confirmada en 12,25"),
    "CE3-NEG": (2, "1 abierta (0,00→6,00); 2 imposible por apertura 6,25"),
    "CE3-FRON": (2, "1 abierta (0,00→6,00); 2 confirmada en 12,00 exactos"),
    "CE4-POS": (2, "1 principal y 1 local abiertas; TT local y principal con referencias separadas"),
    "CE4-NEG": (2, "1 principal abierta; módulo 20,00; TT principal pendiente"),
    "CE4-FRON": (2, "1 principal abierta; B candidata desde 20,00"),
    "CE5-POS": (2, "1 abierta (0,00→10,00); A = 10,00→6,00; TT confirmado en 16,00 con knowledge del tick"),
    "CE5-NEG": (2, "1 abierta; TT pendiente (15,75 no alcanza)"),
    "CE5-FRON": (2, "1 abierta; TT confirmado en 16,00 exactos"),
    "CE6-POS": (5, "A Grande, B Grande y A usada como tendencia implícitas; nuevo 1 en 110,00; 2 prohibida"),
    "CE6-NEG": (5, "sin gap: continúa la lectura; no hay funciones implícitas"),
    "CE6-FRON": (5, "gap de 0,25: A/B/A-tendencia implícitas y nuevo 1 en 100,25"),
    "CE7-AUT": (2, "1 abierta (0,00→20,00); A Grande bajista desde 20,00; AUT y nuevo 1 al cruzar la base 0,00"),
    "CE7-C-NEG": (2, "1 bajista 25,00→0,00; A 0,00→4,00; B Grande; C 25,00 al alza sin CUT"),
    "CE7-C-FRON": (2, "1 bajista 25,00→0,00; A 0,00→4,00; B Grande; C hasta 26,00 con CUT en 0,00 exactos"),
}

CLASS = {
    "CE1-POS": "RC-1.1 bootstrap", "CE1-NEG": "RC-1.1 bootstrap", "CE1-FRON": "RC-1.1 bootstrap",
    "CE2-POS": "RC-1.1 bootstrap + RC-1.3 módulo", "CE2-NEG": "RC-1.1 bootstrap + RC-1.3 módulo",
    "CE2-FRON": "RC-1.1 bootstrap + RC-1.3 módulo",
    "CE3-POS": "RC-1.1 bootstrap", "CE3-NEG": "RC-1.1 bootstrap + RC-2 umbral 0,25",
    "CE3-FRON": "RC-1.1 bootstrap",
    "CE4-POS": "RC-1.1 bootstrap + RC-1.2 escalera", "CE4-NEG": "RC-1.1 bootstrap + RC-1.2 escalera",
    "CE4-FRON": "RC-1.1 bootstrap + RC-1.2 escalera",
    "CE5-POS": "RC-1.1 bootstrap", "CE5-NEG": "RC-1.1 bootstrap", "CE5-FRON": "RC-1.1 bootstrap",
    "CE6-POS": "RC-2 gap", "CE6-NEG": "RC-1.1 bootstrap", "CE6-FRON": "RC-2 gap + umbral 0,25",
    "CE7-AUT": "RC-1.1 bootstrap + RC-1.2 AUT", "CE7-C-NEG": "RC-1.1 bootstrap + RC-1.3 módulo",
    "CE7-C-FRON": "RC-1.1 bootstrap + RC-1.3 módulo",
}


def main():
    out = AUDIT / "FREEBUFF_FIRST_DIVERGENCES_v219.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow([
            "case_id", "ce", "variant", "ticks", "first_divergence_tick", "price",
            "expected_at_first_tick", "observed_at_first_tick", "primary_error",
            "first_reading_tick", "first_module_origin", "first_module_extreme",
            "first_module_size", "propagation",
        ])
        for cid, (tick, expected) in EXPECT.items():
            c = BY[cid]
            st = next(s for s in c["states"] if s["tick"] == tick)
            observed = ("sin lectura" if not st["readings"] else f'{len(st["readings"])} lectura(s)')
            if st["events"]:
                observed += "; eventos=" + ",".join(e["kind"] for e in st["events"])
            first = next((s["tick"] for s in c["states"] if s["readings"]), "")
            if first:
                r = next(r for s in c["states"] if s["tick"] == first for r in s["readings"])
                mo, me, ms = r["module_origin"] / 100, r["module_extreme"] / 100, r["module_size"] / 100
            else:
                mo = me = ms = ""
            propagation = {
                "RC-1.1 bootstrap": "sin 1 no hay pregunta por 2, ni 3, ni A, ni B, ni C",
                "RC-1.1 bootstrap + RC-1.3 módulo": "sin 1 no hay A; el módulo nace tardío y absorbe la pata completa",
                "RC-1.1 bootstrap + RC-2 umbral 0,25": "sin 1 no hay 2; además el umbral 0,25 se aplica como gap estricto",
                "RC-1.1 bootstrap + RC-1.2 escalera": "sin 1 no hay lecturas concurrentes ni autoridad de pregunta",
                "RC-1.1 bootstrap + RC-1.2 AUT": "sin 1 no hay A; AUT no se dispara y no nace nuevo 1",
                "RC-2 gap": "gap detectado pero sin A/B/A-tendencia ni nuevo 1 desde la apertura",
                "RC-2 gap + umbral 0,25": "gap de 0,25 detectado; sin resolución funcional",
            }[CLASS[cid]]
            w.writerow([cid, c["ce"], c["variant"], c["ticks"], tick, st["price"] / 100,
                        expected, observed, CLASS[cid], first, mo, me, ms, propagation])
    print("wrote", out, "rows", len(EXPECT))


if __name__ == "__main__":
    main()
