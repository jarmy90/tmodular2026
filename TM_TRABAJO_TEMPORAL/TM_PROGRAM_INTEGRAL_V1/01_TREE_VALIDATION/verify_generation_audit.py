#!/usr/bin/env python3
"""Verificacion independiente de la auditoria de las 16 generaciones."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def sign(x: int) -> int:
    return 1 if x > 0 else (-1 if x < 0 else 0)


def main() -> int:
    gens = {int(r["generation"]): r for r in rows(BASE / "BLIND_TREE_GENERATIONS_1649_1729.csv")}
    cls = {int(r["generation"]): r for r in rows(BASE / "PHASE_A_GENERATION_CLASSIFICATION.csv")}
    own = {int(r["generation"]): r for r in rows(BASE / "PHASE_A_EXTREME_OWNERSHIP.csv")}

    assert len(gens) == 16, len(gens)
    assert len(cls) == 16, len(cls)
    assert len(own) == 16, len(own)

    # Direcciones
    inversions = [g for g, r in cls.items() if r["direction_match"] == "NO"]
    explicit = [g for g in inversions if cls[g]["rule_strength"] == "EXPLICIT"]
    strong = [g for g in inversions if cls[g]["rule_strength"] == "STRONG_INFERENCE"]
    open_ = [g for g in inversions if cls[g]["rule_strength"] == "OPEN"]
    assert len(inversions) == 10, inversions
    assert explicit == [12, 19], explicit
    assert strong == [18, 23], strong
    assert open_ == [14, 15, 16, 20, 24, 25], open_

    # Clasificacion
    primary = [g for g, r in cls.items() if r["classification"].startswith("VALID_PRIMARY")]
    secondary = [g for g, r in cls.items() if r["classification"] == "VALID_SECONDARY"]
    integrated = [g for g, r in cls.items() if r["classification"] == "INTEGRATED_IN_LARGER_MODULE"]
    pending = [g for g, r in cls.items() if r["classification"] == "PENDING_EXPERT_DECISION"]
    assert sorted(primary) == [13, 17, 22, 26, 27], primary
    assert secondary == [21], secondary
    assert sorted(integrated) == [12, 18, 19, 23], integrated
    assert sorted(pending) == [14, 15, 16, 20, 24, 25], pending

    # Primera divergencia
    first = cls[12]
    assert first["direction_match"] == "NO"
    assert first["transition_in"] == "C_USED_AS_TREND"
    assert first["one_kt"] == "16:49:59.949"
    assert first["one_confirmation_time"] == "16:50:00.152"
    assert first["one_dir"] == "1" and first["transition_dir"] == "-1"

    # 17:22: propiedad del extremo del modulo
    g25 = gens[25]
    o = int(g25["one_origin"])
    x = int(g25["one_extreme"])
    t = int(g25["two_extreme"])
    m = int(g25["module_extreme"])
    assert o == 2963360, o
    assert x == 2967830, x
    assert t == 2966440, t
    assert m == 2967830, m
    assert x - o == 4470, x - o
    assert t - o == 3080, t - o
    assert own[25]["module_extreme_owner"].startswith("1"), own[25]["module_extreme_owner"]

    # Tiempo no asignado
    events = rows(BASE / "BLIND_TREE_EVENTS_1649_1729.csv")
    def sec(hms: str) -> float:
        h, m, s = hms.split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)
    trans = []
    nxt = {}
    for r in events:
        if r["event"] in ("AUT", "A_USED_AS_TREND", "C_USED_AS_TREND"):
            trans.append((int(r["generation"]), r["time"]))
        elif r["event"] == "ONE_CANDIDATE":
            nxt[int(r["generation"])] = r["time"]
    total = sum(sec(nxt[g + 1]) - sec(t) for g, t in trans if g + 1 in nxt)
    assert abs(total - 551.515) < 0.01, total
    assert abs(total / 2459.885 * 100 - 22.4) < 0.1, total / 2459.885 * 100

    # Originales intactos
    tree = ROOT / "TM_CANON_ACTIVO/01_ARBOL/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md"
    tick = ROOT / "TM_CANON_ACTIVO/02_TICKS/TM_TICKFEED_1615_1730.csv"
    v005 = ROOT / "TM_CANON_ACTIVO/03_LECTURAS_HUMANAS/TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v005.txt"
    assert sha256(tree).upper() == "94A1408A6123ED66948988334E7D540C2A2692C36EEA3CB736DBFF0DA2346B17"
    assert sha256(tick).upper() == "5F701BE2307352CB559ABBD7BB856A6FD2A1F91E5D269A93DCC9AE2992E2C9FF"
    assert sha256(v005).upper() == "F5D7550C42C90897D833E6C2A3FAF772753A129640FD4411DE4190CB2CF94226"

    result = {
        "generations": 16,
        "inversions": inversions,
        "explicit": explicit,
        "strong_inference": strong,
        "open": open_,
        "primary": primary,
        "secondary": secondary,
        "integrated": integrated,
        "pending": pending,
        "first_divergence": {
            "generation": 12,
            "structural_time": first["one_kt"],
            "knowledge_time": first["one_confirmation_time"],
        },
        "case_17_22": {
            "one_origin": o,
            "one_extreme": x,
            "two_extreme": t,
            "module_44_7": x - o,
            "wrong_30_8": t - o,
        },
        "unassigned_seconds": round(total, 3),
        "unassigned_percent": round(total / 2459.885 * 100, 1),
        "originals_ok": True,
        "status": "PASS",
    }
    (BASE / "PHASE_A_AUDIT_VERIFICATION.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
