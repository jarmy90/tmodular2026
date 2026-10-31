#!/usr/bin/env python3
"""Auditoria funcional de las 16 generaciones de Fase A.

Lee la salida ya bloqueada (BLIND_TREE_GENERATIONS_1649_1729.csv y
BLIND_TREE_EVENTS_1649_1729.csv) y produce:

  - PHASE_A_GENERATION_CLASSIFICATION.csv
  - PHASE_A_EXTREME_OWNERSHIP.csv
  - PHASE_A_GENERATION_AUDIT.json

No re-ejecuta el lector, no modifica originales y no usa informacion futura:
solo compara la direccion de cada 1 con la direccion de la transicion que la
creo, y la propiedad de cada extremo con los datos ya registrados.

La unica referencia externa es la transicion heredada de 16:48:15.900, tomada
del estado inicial documentado en BLIND_TREE_READINGS_1649_1729.md. No es una
regla del motor: es evidencia del bloque.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
GEN_PATH = BASE / "BLIND_TREE_GENERATIONS_1649_1729.csv"
EV_PATH = BASE / "BLIND_TREE_EVENTS_1649_1729.csv"
READER_PATH = BASE / "blind_reader.py"

# Transicion heredada del bloque anterior (estado a 16:48:59.811).
# C_USED_AS_TREND: C = 29666.1, base del modulo = 29666.4, direccion bajista.
WARMUP = {
    "generation": 12,
    "ended_by": "C_USED_AS_TREND",
    "transition_time": "16:48:15.900",
    "transition_price": 2966610,
    "transition_base": 2966640,
    "transition_dir": -1,
    "source": "BLIND_TREE_READINGS_1649_1729.md seccion 0 (estado heredado)",
}


def sign(x: int) -> int:
    return 1 if x > 0 else (-1 if x < 0 else 0)


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def transition_for(prev: dict) -> tuple[str, int, str]:
    """Devuelve (tipo, direccion, detalle) de la transicion que abre la gen."""
    kind = prev["ended_by"]
    if kind == "AUT":
        d = -sign(int(prev["a_extreme"]) - int(prev["a_origin"]))
        return kind, d, f"AUT en direccion de B (B={prev['b_extreme']})"
    if kind == "A_USED_AS_TREND":
        d = sign(int(prev["a_extreme"]) - int(prev["a_origin"]))
        return kind, d, f"A usada como tendencia (A={prev['a_size']})"
    if kind == "C_USED_AS_TREND":
        d = sign(int(prev["c_extreme"]) - int(prev["c_origin"]))
        return kind, d, f"C usada como tendencia (C={prev['c_extreme']})"
    raise ValueError(f"transicion no reconocida: {kind}")


def main() -> int:
    gens = read_csv(GEN_PATH)
    events = read_csv(EV_PATH)
    by_gen = {int(g["generation"]): g for g in gens}

    # Evento de transicion por generacion (el evento vive en la generacion
    # anterior; la primera transicion del bloque es la heredada de 16:48).
    trans_event: dict[int, dict] = {}
    one_event: dict[int, dict] = {}
    for ev in events:
        if ev["event"] in ("AUT", "A_USED_AS_TREND", "C_USED_AS_TREND"):
            g = int(ev["generation"])
            trans_event[g + 1] = ev
        elif ev["event"] == "ONE_CONFIRMED":
            one_event[int(ev["generation"])] = ev

    classification: list[dict] = []
    ownership: list[dict] = []
    summary = {
        "generations": len(gens),
        "counts": {},
        "first_divergence": None,
        "direction_inversions": [],
    }

    for i, g in enumerate(gens):
        gen = int(g["generation"])
        one_origin = int(g["one_origin"])
        one_extreme = int(g["one_extreme"])
        mod_origin = int(g["module_origin"])
        mod_extreme = int(g["module_extreme"])
        one_dir = sign(one_extreme - one_origin)
        one_size = int(g["one_size"])

        if i == 0:
            kind, tdir, tdetail = (
                WARMUP["ended_by"], WARMUP["transition_dir"], WARMUP["source"]
            )
            ttime = WARMUP["transition_time"]
        else:
            prev = gens[i - 1]
            kind, tdir, tdetail = transition_for(prev)
            ev = trans_event.get(gen, {})
            ttime = ev.get("time", "")

        match = "YES" if one_dir == tdir else "NO"

        # Margen de la transicion anterior (solo A_TREND / C_TREND).
        margin = ""
        if i > 0:
            prev = gens[i - 1]
            if kind == "A_USED_AS_TREND":
                margin = f"{int(prev['a_size']) - int(prev['module_size'])}"
            elif kind == "C_USED_AS_TREND":
                margin = f"{abs(int(prev['c_extreme']) - int(prev['module_origin']))}"

        if gen == 27:
            cls, cause = "VALID_PRIMARY_OPEN", "OPEN_AT_FEED_END"
        elif match == "YES" and kind == "AUT":
            cls, cause = "VALID_PRIMARY", "AUT_DIRECTION_OK"
        elif match == "YES" and kind == "C_USED_AS_TREND":
            cls, cause = "VALID_PRIMARY", "C_TREND_DIRECTION_OK"
        elif match == "YES" and kind == "A_USED_AS_TREND":
            prev = gens[i - 1]
            a_dir = sign(int(prev["a_extreme"]) - int(prev["a_origin"]))
            exceeds = (one_extreme - int(prev["a_extreme"])) * a_dir > 0
            if not exceeds:
                cls, cause = "VALID_SECONDARY", "RETEST_DOES_NOT_EXCEED_A_EXTREME"
            elif int(margin) <= 50:
                cls, cause = "PENDING_EXPERT_DECISION", "A_TREND_MARGIN_LE_0_50"
            else:
                cls, cause = "VALID_PRIMARY", "A_TREND_DIRECTION_OK"
        elif match == "NO" and kind in ("C_USED_AS_TREND", "A_USED_AS_TREND"):
            cls = "INTEGRATED_IN_LARGER_MODULE"
            cause = "C_TREND_DIRECTION" if kind == "C_USED_AS_TREND" else "A_TREND_DIRECTION"
        elif match == "NO" and kind == "AUT":
            cls, cause = "PENDING_EXPERT_DECISION", "AUT_DIRECTION_OPEN"
        else:
            cls, cause = "PENDING_EXPERT_DECISION", "UNCLASSIFIED"

        if match == "NO" and kind == "C_USED_AS_TREND":
            rule_strength = "EXPLICIT"
        elif match == "NO" and kind == "A_USED_AS_TREND":
            rule_strength = "STRONG_INFERENCE"
        elif match == "NO" and kind == "AUT":
            rule_strength = "OPEN"
        else:
            rule_strength = "N/A"

        row = {
            "generation": gen,
            "transition_in": kind,
            "rule_strength": rule_strength,
            "transition_time": ttime,
            "transition_dir": tdir,
            "one_dir": one_dir,
            "direction_match": match,
            "one_origin": one_origin,
            "one_extreme": one_extreme,
            "one_size": one_size,
            "one_kt": g["one_kt"],
            "one_confirmation_time": one_event.get(gen, {}).get("time", ""),
            "module_size": g["module_size"],
            "a_size": g["a_size"],
            "b_measure": g["b_measure"],
            "ended_by": g["ended_by"],
            "transition_margin_centipoints": margin,
            "classification": cls,
            "cause": cause,
            "transition_detail": tdetail,
        }
        classification.append(row)

        if match == "NO":
            summary["direction_inversions"].append({
                "generation": gen,
                "transition_in": kind,
                "transition_time": ttime,
                "transition_dir": tdir,
                "one_dir": one_dir,
                "one_size": one_size,
                "classification": cls,
            })
            if summary["first_divergence"] is None:
                summary["first_divergence"] = {
                    **row,
                    "structural_time": g["one_kt"],
                    "knowledge_time": one_event.get(gen, {}).get("time", ""),
                }

        # ---------------------------------------------------------- ownership
        # Origen y extremo de 1: el lector los toma del rango de la vela (H1).
        # El propietario funcional se decide por la direccion y por quien
        # alcanzo el extremo, no por la etiqueta del lector.
        one_origin_owner = "1 (extremo de la vela de 1, H1)"
        # El extremo de 1 pertenece a 1. A nace en ese extremo y se aleja;
        # eso no transfiere la propiedad del extremo de 1 a A.
        one_extreme_owner = "1"
        # Extremo del modulo: el mas lejano entre 1 y 2.
        two_extreme = int(g["two_extreme"]) if g["two_extreme"] else 0
        candidates = [one_extreme] + ([two_extreme] if two_extreme else [])
        farthest = max(candidates, key=lambda p: abs(p - mod_origin))
        if mod_extreme != farthest:
            mod_extreme_owner = "modulo (nuevo extremo posterior; A se reinicia)"
        elif two_extreme and abs(two_extreme - mod_origin) > abs(one_extreme - mod_origin):
            mod_extreme_owner = "2 (extremo mas lejano del modulo)"
        else:
            mod_extreme_owner = "1 (extremo mas lejano del modulo; 2 no lo supera)"

        ownership.append({
            "generation": gen,
            "one_origin": one_origin,
            "one_origin_owner": one_origin_owner,
            "one_extreme": one_extreme,
            "one_extreme_owner": one_extreme_owner,
            "two_origin": g["two_origin"],
            "two_extreme": g["two_extreme"],
            "module_origin": mod_origin,
            "module_origin_owner": "1 (origen del modulo)" if mod_origin == one_origin else "2/extension",
            "module_extreme": mod_extreme,
            "module_extreme_owner": mod_extreme_owner,
            "a_origin": g["a_origin"],
            "a_origin_owner": ("1 (extremo final)" if int(g["a_origin"]) == one_extreme
                               else "modulo (extremo posterior)"),
            "a_extreme": g["a_extreme"],
            "a_extreme_owner": "A",
            "b_origin": g["a_extreme"],
            "b_origin_owner": "A (extremo final)",
            "b_extreme": g["b_extreme"],
            "b_extreme_owner": "B" if g["b_extreme"] not in ("", "0") else "N/A (sin B)",
            "c_origin": g["c_origin"],
            "c_origin_owner": ("B (extremo final)" if g["c_origin"] not in ("", "0")
                               else "N/A (sin C)"),
            "c_extreme": g["c_extreme"],
            "c_extreme_owner": "C" if g["c_extreme"] not in ("", "0") else "N/A (sin C)",
            "note": (
                "17:22 low 29633.6 seq18125; high 29678.3 seq18304; "
                "2 high 29664.4 seq18394 inside 1; module 44.7"
                if gen == 25 else
                ("module extreme beyond 1 and 2; A reset"
                 if mod_extreme_owner.startswith("modulo") else
                 ("2 owns module extreme"
                  if mod_extreme_owner.startswith("2") else ""))
            ),
        })

    counts: dict[str, int] = {}
    for r in classification:
        counts[r["classification"]] = counts.get(r["classification"], 0) + 1
    summary["counts"] = counts
    summary["reader_sha256"] = sha256(READER_PATH)
    summary["generations_sha256"] = sha256(GEN_PATH)
    summary["events_sha256"] = sha256(EV_PATH)

    with (BASE / "PHASE_A_GENERATION_CLASSIFICATION.csv").open(
        "w", encoding="utf-8", newline=""
    ) as fh:
        w = csv.DictWriter(fh, fieldnames=list(classification[0].keys()))
        w.writeheader()
        w.writerows(classification)

    with (BASE / "PHASE_A_EXTREME_OWNERSHIP.csv").open(
        "w", encoding="utf-8", newline=""
    ) as fh:
        w = csv.DictWriter(fh, fieldnames=list(ownership[0].keys()))
        w.writeheader()
        w.writerows(ownership)

    with (BASE / "PHASE_A_GENERATION_AUDIT.json").open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)

    print(json.dumps(summary["counts"], ensure_ascii=False, indent=2))
    print("first divergence:", summary["first_divergence"]["generation"],
          summary["first_divergence"]["transition_in"],
          summary["first_divergence"]["transition_time"])
    print("inversions:", len(summary["direction_inversions"]))
    print("reader sha256:", summary["reader_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
