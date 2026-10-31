# -*- coding: utf-8 -*-
"""Input manifest for TM_PROGRAM_INTEGRAL_V1. Reads originals; writes only in 00_INPUTS/09_MANIFEST."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROGRAM = HERE.parent
PROJECT = PROGRAM.parents[1]
DELIV = Path(r"C:\Users\profesor\OpenBot\Agents\agent-ece275c8-821a-43f3-b05f-6cdf123b7ade")
AUDIT = PROJECT / "TM_TRABAJO_TEMPORAL/FREEBUFF_AUDIT_V219"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest().upper()


INPUTS = [
    ("tree_v219", PROJECT / "TM_CANON_ACTIVO/01_ARBOL/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_19_ACUMULADO.md",
     "94A1408A6123ED66948988334E7D540C2A2692C36EEA3CB736DBFF0DA2346B17", "WORKING_CANON_NOT_FROZEN"),
    ("tree_certificate", PROJECT / "TM_CANON_ACTIVO/01_ARBOL/TM_ARBOL_v2_19_CERTIFICADO.json",
     "995951E54A1F20FB41479569FD320B45C74A22DB400DBDECA6877337F5697168", "WORKING_CANON_NOT_FROZEN"),
    ("human_readings_v005", PROJECT / "TM_CANON_ACTIVO/03_LECTURAS_HUMANAS/TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v005.txt",
     "F5D7550C42C90897D833E6C2A3FAF772753A129640FD4411DE4190CB2CF94226", "PARTIAL"),
    ("master_tickfeed", PROJECT / "TM_CANON_ACTIVO/02_TICKS/TM_TICKFEED_1615_1730.csv",
     "5F701BE2307352CB559ABBD7BB856A6FD2A1F91E5D269A93DCC9AE2992E2C9FF", "VERIFIED"),
    ("engine_R3_frozen", PROJECT / "TM_CANON_ACTIVO/04_MOTOR_PYTHON/CANDIDATO_v0752_R3/TM_CORE_PYTHON_v0752_CANONICAL_R3.py",
     "71D9A97AC2C49848D152A790DB0C70D20B30643782BFEE0AC030D19110330B08", "FROZEN"),
    ("engine_R5_audited", DELIV / "deliverables_R5/python/TM_CORE_PYTHON_v0752_CANONICAL_R5.py",
     "9BD1BEDB5DEC8C5A1C3A831338503E90CC04EE3CD776CF4E01D27CF8AA0EBEAE", "AUDIT_BASELINE_NOT_FROZEN"),
    ("engine_R5_packaged_copy", AUDIT / "00_INPUTS_REFERENCE/variants/R5_PACKAGED_19A847C0.py",
     "19A847C078E124616495E85A832F9D2FA12A371413046CBAEB7E9644D47C6A36", "HISTORICAL_PACKAGED"),
    ("engine_active_previous", PROJECT / "TM_CANON_ACTIVO/04_MOTOR_PYTHON/TM_MOTOR_ACTIVO.py",
     "4A2877CC7F47E0565D6D788BA20D198486CDDEBA718F6A8F8498222B38DDEFE2", "ACTIVE_PREVIOUS"),
    ("R3_zip_frozen", PROJECT / "TM_ENTREGAS/TM_CORE_v0752_R3_B_AUT.zip",
     "450379BD5F1E22380614E6112E3FB52C2A653EE8358BF7E5238995AF99D3B7DB", "FROZEN"),
    ("R5_zip_lectura", DELIV / "TM_CORE_v0752_R5_LECTURA_1615_1629.zip",
     "DDC6AE2FFA9854FD6DE1B9B058BB12DF19E8542F309BD9C8693B823A60785A9F", "HISTORICAL_PACKAGED"),
    ("R5_zip_post_cut", DELIV / "TM_CORE_v0752_R5_POST_CUT.zip",
     "4238D0E1FD6ECC9E136856ED49E03958C3151F628318444077ECA7440494A72C", "HISTORICAL_PACKAGED"),
]


def main():
    rows = []
    for role, path, expected, state in INPUTS:
        if not path.exists():
            rows.append({"role": role, "absolute_path": str(path), "exists": False,
                         "expected_sha256": expected, "verified": False, "state": state})
            continue
        st = path.stat()
        actual = sha256(path)
        rows.append({
            "role": role, "absolute_path": str(path), "exists": True,
            "size_bytes": st.st_size,
            "mtime_utc": datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat(),
            "expected_sha256": expected, "sha256": actual,
            "verified": actual == expected, "state": state,
            "read_only": True,
        })
    manifest = {
        "artifact": "TM_PROGRAM_INTEGRAL_V1_INPUT_MANIFEST",
        "document_version": "1.0",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "program_root": str(PROGRAM),
        "project_root": str(PROJECT),
        "outside_workspace_reads": str(DELIV),
        "mandate_status": "TRUNCATED_AT_SECTION_4",
        "mandate_received_through": "4. REGLAS YA CERRADAS — PLANO (incomplete)",
        "phases_A_H_defined": False,
        "tree_modified": False, "engine_modified": False, "goldens_modified": False,
        "observational_only": True,
        "all_verified": all(r["verified"] for r in rows),
        "inputs": rows,
    }
    out = PROGRAM / "00_INPUTS/INPUT_MANIFEST.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"manifest -> {out}")
    print("all_verified:", manifest["all_verified"])
    for r in rows:
        print(f'  {r["role"]:28s} exists={r["exists"]} verified={r["verified"]} {r.get("sha256","")[:16]}')


if __name__ == "__main__":
    main()
