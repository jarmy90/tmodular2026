#!/usr/bin/env python3
"""Manifiesto de la auditoria funcional de las 16 generaciones (Fase A)."""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]  # .../Teoria Modular


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def entry(path: Path, role: str, expected: str | None = None) -> dict:
    d = {
        "role": role,
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "absolute_path": str(path),
        "size": path.stat().st_size,
        "sha256": sha256(path),
        "modified_utc": datetime.fromtimestamp(
            path.stat().st_mtime, tz=timezone.utc
        ).isoformat(),
    }
    if expected:
        d["expected_sha256"] = expected
        d["hash_matches"] = d["sha256"].upper() == expected.upper()
    return d


def main() -> int:
    tree = ROOT / "TM_CANON_ACTIVO/01_ARBOL/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md"
    tick = ROOT / "TM_CANON_ACTIVO/02_TICKS/TM_TICKFEED_1615_1730.csv"
    v005 = ROOT / "TM_CANON_ACTIVO/03_LECTURAS_HUMANAS/TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v005.txt"
    reader = BASE / "blind_reader.py"
    gens = BASE / "BLIND_TREE_GENERATIONS_1649_1729.csv"
    events = BASE / "BLIND_TREE_EVENTS_1649_1729.csv"
    trace = BASE / "BLIND_TREE_TRACE_1649_1729.jsonl"
    verify = BASE / "verify_phase_a.json"
    phase_a = BASE / "BLIND_TREE_READINGS_1649_1729.md"
    checkpoint = BASE.parents[0] / "08_REPORTS/PHASE_A_CHECKPOINT_v1.md"

    inputs = [
        entry(tree, "tree_v219", "94A1408A6123ED66948988334E7D540C2A2692C36EEA3CB736DBFF0DA2346B17"),
        entry(tick, "tickfeed_maestro", "5F701BE2307352CB559ABBD7BB856A6FD2A1F91E5D269A93DCC9AE2992E2C9FF"),
        entry(v005, "lecturas_v005", "F5D7550C42C90897D833E6C2A3FAF772753A129640FD4411DE4190CB2CF94226"),
        entry(reader, "reader_fase_a"),
        entry(gens, "generaciones_bloqueadas"),
        entry(events, "eventos_bloqueados"),
        entry(trace, "traza_por_tick"),
        entry(verify, "verificacion_determinismo"),
        entry(phase_a, "acta_fase_a"),
        entry(checkpoint, "checkpoint_fase_a"),
    ]

    outputs = [
        entry(BASE / "PHASE_A_GENERATION_AUDIT.md", "auditoria_generaciones"),
        entry(BASE / "PHASE_A_GENERATION_CLASSIFICATION.csv", "clasificacion_16"),
        entry(BASE / "PHASE_A_EXPERIMENTAL_POLICIES.md", "politicas_experimentales"),
        entry(BASE / "PHASE_A_EXTREME_OWNERSHIP.csv", "propiedad_extremos"),
        entry(BASE / "PHASE_A_PRIMARY_SECONDARY_MAP.md", "mapa_primaria_secundaria"),
        entry(BASE / "PHASE_A_GENERATION_AUDIT.json", "resumen_auditoria"),
        entry(BASE / "audit_generations.py", "script_auditoria"),
        entry(BASE / "verify_generation_audit.py", "script_verificacion"),
        entry(BASE / "PHASE_A_AUDIT_VERIFICATION.json", "verificacion_auditoria"),
    ]

    audit = json.loads((BASE / "PHASE_A_GENERATION_AUDIT.json").read_text(encoding="utf-8"))

    manifest = {
        "phase": "A",
        "subphase": "generation_audit",
        "version": "v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "authority": {
            "tree": "v2.19 WORKING_CANON_NOT_FROZEN",
            "tree_frozen": False,
            "engine_authority": False,
            "observational_only": True,
            "originals_modified": False,
        },
        "inputs": inputs,
        "outputs": outputs,
        "audit_counts": audit.get("counts", {}),
        "first_divergence": audit.get("first_divergence", {}),
        "direction_inversions": audit.get("direction_inversions", []),
        "status": "NEEDS_EXPERT_DECISION",
        "gate": "GATE_A_EVIDENCE_AUDITED__16_GENERATIONS_NOT_APPROVED",
        "open_questions": [
            "Q_AUT_DIRECTION",
            "Q_C_GRANDE",
            "Q_A_MARGIN",
        ],
        "limitations": [
            "No se re-ejecuto el lector; se audito la salida bloqueada.",
            "No hay golden humano del bloque 16:49-17:29 (v005 lo marca [D]).",
            "Las 5 primarias locales tienen direccion valida pero origen en la vela siguiente.",
            "Los hashes intermedios de las politicas P01-P17 no se archivaron.",
        ],
        "commands": [
            "python audit_generations.py",
            "python verify_generation_audit.py",
            "python build_audit_manifest.py",
        ],
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
    }

    out = BASE / "PHASE_A_AUDIT_MANIFEST.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    sums = BASE / "SHA256SUMS_AUDIT.txt"
    lines = []
    for item in outputs:
        lines.append(f"{item['sha256'].upper()}  {item['path']}")
    lines.append(f"{sha256(out).upper()}  {str(out.relative_to(ROOT)).replace(chr(92), '/')}")
    sums.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"manifest: {out}")
    print(f"sums: {sums}")
    for item in outputs:
        print(f"{item['sha256'][:16]}  {item['path']}")
    print("all inputs match:", all(i.get("hash_matches", True) for i in inputs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
