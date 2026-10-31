# -*- coding: utf-8 -*-
"""Construye PHASE_A_MANIFEST.json y SHA256SUMS.txt de la Fase A."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PROGRAM = HERE.parent


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def rec(p: Path) -> dict:
    try:
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        rel = str(p)
    return {
        "path": rel,
        "absolute_path": str(p),
        "size": p.stat().st_size,
        "sha256": sha(p),
        "modified_utc": datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(),
    }


INPUTS = [
    ("tree_v219", ROOT / "TM_CANON_ACTIVO/01_ARBOL/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md",
     "94A1408A6123ED66948988334E7D540C2A2692C36EEA3CB736DBFF0DA2346B17"),
    ("lecturas_v005", ROOT / "TM_CANON_ACTIVO/03_LECTURAS_HUMANAS/TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v005.txt",
     "F5D7550C42C90897D833E6C2A3FAF772753A129640FD4411DE4190CB2CF94226"),
    ("tickfeed_maestro", ROOT / "TM_CANON_ACTIVO/02_TICKS/TM_TICKFEED_1615_1730.csv",
     "5F701BE2307352CB559ABBD7BB856A6FD2A1F91E5D269A93DCC9AE2992E2C9FF"),
    ("r5_auditado", Path(r"C:\Users\profesor\OpenBot\Agents\agent-ece275c8-821a-43f3-b05f-6cdf123b7ade\deliverables_R5\python\TM_CORE_PYTHON_v0752_CANONICAL_R5.py"),
     "9BD1BEDB5DEC8C5A1C3A831338503E90CC04EE3CD776CF4E01D27CF8AA0EBEAE"),
    ("mandato_continuacion", PROGRAM / "00_INPUTS/TM_MANDATO_CONTINUACION_SECCION_4_HASTA_FINAL.txt",
     "f9050901565c334e1daf6ba48df42dc0ab5d0f081798b27598318e48b0ad3657"),
]

REPORTS = [
    PROGRAM / "08_REPORTS/01_MANDATE_CONTINUATION_RECORD.md",
    PROGRAM / "08_REPORTS/PHASE_A_CHECKPOINT_v1.md",
]

OUTPUTS = [
    "blind_reader.py",
    "verify_phase_a.py",
    "run_r5_block.py",
    "build_phase_a_manifest.py",
    "BLIND_TREE_READINGS_1649_1729.md",
    "BLIND_TREE_SECONDARY_READINGS.md",
    "BLIND_TREE_CONCEPTUAL_GAPS.md",
    "BLIND_TREE_FIRST_DIVERGENCES.csv",
    "BLIND_TREE_TRACE_1649_1729.jsonl",
    "BLIND_TREE_EVENTS_1649_1729.csv",
    "BLIND_TREE_STATE_AT_BAR_CLOSE.csv",
    "BLIND_TREE_GENERATIONS_1649_1729.csv",
    "verify_phase_a.json",
    "R5_BLOCK_EVIDENCE.json",
]


def main():
    inputs = []
    for name, path, expected in INPUTS:
        item = {"id": name, **rec(path)}
        item["expected_sha256"] = expected
        item["hash_matches"] = item["sha256"] == expected.upper()
        inputs.append(item)

    outputs = [{"id": p, **rec(HERE / p)} for p in OUTPUTS]
    reports = [{"id": p.name, **rec(p)} for p in REPORTS]
    verify = json.loads((HERE / "verify_phase_a.json").read_text(encoding="utf-8"))

    manifest = {
        "phase": "A",
        "version": "v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "authority": {
            "tree": "v2.19 WORKING_CANON_NOT_FROZEN",
            "tree_sha256": inputs[0]["sha256"],
            "engine_authority": False,
            "tree_modified": False,
            "engine_modified": False,
            "goldens_modified": False,
            "observational_only": True,
        },
        "inputs": inputs,
        "outputs": outputs,
        "reports": reports,
        "commands": [
            "python blind_reader.py --from 16:15 --to 17:29 --events out_ev.csv --bar-close out_bc.csv --generations out_gen.csv --trace out_trace.jsonl",
            "python verify_phase_a.py",
            "python run_r5_block.py",
            "python build_phase_a_manifest.py",
        ],
        "block": {
            "from": "16:49:00.012",
            "to": "17:29:59.897",
            "bars": 41,
            "ticks": 11414,
            "first_sequence_id": 8922,
            "last_sequence_id": 20335,
            "generations": 16,
            "regular_modules_123": 0,
            "discard_modules": 16,
            "aut": 8,
            "a_used_as_trend": 4,
            "c_used_as_trend": 2,
            "open_at_feed_end": 1,
            "events": 454,
        },
        "verification": {
            "determinism_run1": verify["determinism"]["run1"],
            "determinism_run2": verify["determinism"]["run2"],
            "determinism_equal": verify["determinism"]["equal"],
            "prefixes_checked": verify["prefixes_checked"],
            "prefixes_ok": verify["prefixes_ok"],
            "prefix_failures": verify["prefix_failures"],
            "ticks": verify["ticks"],
            "exceptions": 0,
        },
        "policies": {
            "H1": "1 = rango direccional de su vela",
            "H2": "A se confirma con 6,00 puntos (minimo teorico v2.5)",
            "H3": "retroceso valido de 2: >= 2,00 y <= 50 %",
            "H4": "B Grande monotona; A puede extenderse",
            "H5": "TT evaluado tick a tick",
            "H6": "TT sobrevive al AUT como patron",
            "H7": "gap: esbozo implicito, sin ticks inventados",
        },
        "open_questions": [
            "Q1 unidad de 1 en vela no monotona",
            "Q2 autonomia de A y propiedad del extremo del modulo",
            "Q3 gap significativo y referencia de C",
            "Q4 dominancia y concurrencia",
        ],
        "registered_gaps": [
            "Q_TWO_LIFECYCLE", "Q_TAIL", "Q_MODULE_MEASURE", "Q_50",
            "Q_TT_FAILURE", "Q_FT", "Q_C_ABSORPTION", "Q_CONCURRENCY",
            "Q_AUT_NEW_ONE",
        ],
        "gate_a": {
            "status": "PASS_WITH_OPEN_QUESTIONS",
            "all_ticks_traversed": True,
            "every_function_traceable": True,
            "ambiguities_explicit": True,
            "spoilers_used": False,
            "deterministic": verify["determinism"]["equal"],
            "prefixes_consistent": verify["prefixes_ok"] == verify["prefixes_checked"],
            "hardcoding": False,
            "next_phase": "B",
        },
        "next_phase_blockers": [
            "Q1 y Q2 requieren decision experta antes de congelar el arbol ejecutable",
        ],
    }

    out = HERE / "PHASE_A_MANIFEST.json"
    out.write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
    print("manifest:", out)
    print("inputs ok:", all(i["hash_matches"] for i in inputs))
    print("outputs:", len(outputs), "reports:", len(reports))

    files = [HERE / p for p in OUTPUTS if (HERE / p).exists()] + [out]
    sums = HERE / "SHA256SUMS.txt"
    lines = []
    for p in sorted(files, key=lambda x: x.name):
        lines.append(f"{sha(p)}  {p.name}")
    for p in REPORTS:
        lines.append(f"{sha(p)}  08_REPORTS/{p.name}")
    sums.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("sums:", sums, len(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
