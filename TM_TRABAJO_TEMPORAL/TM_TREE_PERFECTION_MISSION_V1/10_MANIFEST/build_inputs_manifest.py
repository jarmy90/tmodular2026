#!/usr/bin/env python3
"""Build the input manifest for TM_TREE_PERFECTION_MISSION_V1.

Read-only over the originals. Writes INPUTS_MANIFEST.json and SHA256SUMS.txt
inside 10_MANIFEST/. Fails if an expected hash does not match.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parents[1]
MANIFEST_DIR = BASE / "10_MANIFEST"
MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

INPUTS = [
    {
        "id": "TREE_V219",
        "role": "arbol_de_trabajo",
        "path": ROOT / "TM_CANON_ACTIVO/01_ARBOL/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md",
        "expected_sha256": "94a1408a6123ed66948988334e7d540c2a2692c36eea3cb736dbff0da2346b17",
        "authority": "WORKING_CANON_NOT_FROZEN",
    },
    {
        "id": "TICKFEED_MASTER",
        "role": "tickfeed_maestro",
        "path": ROOT / "TM_TICKFEED_1615_1730.csv",
        "expected_sha256": "5f701be2307352cb559abbd7bb856a6fd2a1f91e5d269a93dcc9ae2992e2c9ff",
        "authority": "EVIDENCIA_FISICA_CAUSAL",
    },
    {
        "id": "LECTURAS_V005",
        "role": "lecturas_humanas",
        "path": ROOT / "TM_CANON_ACTIVO/03_LECTURAS_HUMANAS/TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v005.txt",
        "expected_sha256": "f5d7550c42c90897d833e6c2a3faf772753a129640fd4411de4190cb2cf94226",
        "authority": "VERIFICA_APLICACION_NO_CREA_REGLA",
    },
    {
        "id": "R3_FROZEN",
        "role": "motor_estable_congelado",
        "path": ROOT / "TM_CANON_ACTIVO/04_MOTOR_PYTHON/CANDIDATO_v0752_R3/TM_CORE_PYTHON_v0752_CANONICAL_R3.py",
        "expected_sha256": "71d9a97ac2c49848d152a790db0c70d20b30643782bfee0ac030d19110330b08",
        "authority": "EVIDENCIA_NO_AUTORIDAD",
    },
    {
        "id": "R5_AUDITED",
        "role": "motor_r5_auditado",
        "path": ROOT.parents[1] / "OpenBot/Agents/agent-ece275c8-821a-43f3-b05f-6cdf123b7ade/deliverables_R5/python/TM_CORE_PYTHON_v0752_CANONICAL_R5.py",
        "expected_sha256": "9bd1bedb5dec8c5a1c3a831338503e90cc04ee3cd776cf4e01d27cf8aa0ebeae",
        "authority": "EVIDENCIA_NO_AUTORIDAD",
    },
    {
        "id": "R5_PACKAGED",
        "role": "motor_r5_empaquetado",
        "path": ROOT / "TM_TRABAJO_TEMPORAL/FREEBUFF_AUDIT_V219/00_INPUTS_REFERENCE/variants/R5_PACKAGED_19A847C0.py",
        "expected_sha256": "19a847c078e124616495e85a832f9d2fa12a371413046cbaeb7e9644d47c6a36",
        "authority": "EVIDENCIA_NO_AUTORIDAD",
    },
    {
        "id": "MANDATE",
        "role": "mandato_vigente",
        "path": BASE / "00_INPUTS/PROMPT_FREEBUFF_PERFECCION_FINAL_ARBOL_TM.txt",
        "expected_sha256": "993a597d24f16e39a1b2424e0c51003fdff7e9c1269969047c9f81f562d06408",
        "authority": "MANDATO_VIGENTE",
    },
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def count_lines(path: Path) -> int:
    total = 0
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            total += chunk.count(b"\n")
    return total


def main() -> int:
    rows = []
    all_ok = True
    for item in INPUTS:
        path: Path = item["path"]
        exists = path.is_file()
        row = {
            "id": item["id"],
            "role": item["role"],
            "path": str(path),
            "exists": exists,
            "authority": item["authority"],
        }
        if exists:
            size = path.stat().st_size
            digest = sha256(path)
            row.update(
                {
                    "size_bytes": size,
                    "lines": count_lines(path),
                    "sha256": digest,
                    "modified_utc": datetime.fromtimestamp(
                        path.stat().st_mtime, tz=timezone.utc
                    ).isoformat(),
                    "expected_sha256": item["expected_sha256"],
                    "hash_matches": digest == item["expected_sha256"],
                }
            )
            all_ok = all_ok and row["hash_matches"]
        else:
            row.update(
                {
                    "size_bytes": None,
                    "lines": None,
                    "sha256": None,
                    "modified_utc": None,
                    "expected_sha256": item["expected_sha256"],
                    "hash_matches": False,
                }
            )
            all_ok = False
        rows.append(row)

    payload = {
        "mission": "TM_TREE_PERFECTION_MISSION_V1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "workspace": str(BASE),
        "project_root": str(ROOT),
        "originals_modified": False,
        "tree_status": "WORKING_CANON_NOT_FROZEN",
        "tree_authority": True,
        "engine_authority": False,
        "all_expected_hashes_match": all_ok,
        "inputs": rows,
    }
    (MANIFEST_DIR / "INPUTS_MANIFEST.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    sums = "".join(f"{r['sha256']} *{r['path']}\n" for r in rows if r["sha256"])
    with (MANIFEST_DIR / "SHA256SUMS.txt").open(
        "w", encoding="utf-8", newline="\n"
    ) as fh:
        fh.write(sums)

    print(f"all_expected_hashes_match={all_ok}")
    for r in rows:
        print(
            f"{r['id']:16s} {str(r['size_bytes']):>9s} "
            f"{str(r['lines']):>5s} {r['sha256']} "
            f"{'OK' if r['hash_matches'] else 'MISMATCH'}"
        )
    return 0 if all_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
