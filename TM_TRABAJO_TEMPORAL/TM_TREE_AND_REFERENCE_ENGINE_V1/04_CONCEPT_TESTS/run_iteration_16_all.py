#!/usr/bin/env python3
"""ITERACION 16 — auditoria del sistema de validacion.

Fase 1: cada suite se ejecuta con TM_READER_MODULE fijado al candidato y con
        el SHA-256 y el CORE_VERSION exigidos. La suite falla si importa otro
        archivo, otra version o un modulo sin CORE_VERSION.
Fase 3: la autoridad se agrega leyendo el campo estructurado `classification`
        de cada CSV, nunca del texto de consola.

Salidas:
  SUITE_ENGINE_MAP.csv        suite -> modulo -> ruta -> sha256 -> version
  TEST_AUTHORITY_SUMMARY.json recuento real por clasificacion
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE.parent / "05_REFERENCE_ENGINE"
MODULE = "tm_reference_interpreter_v1_direct_aut"
EXPECTED_VERSION = "TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT"

SUITES = [
    ("core", "run_core_tests.py", "CORE_TEST_RESULTS.csv"),
    ("A/B/B Grande/AUT", "run_ab_candidate_tests.py", "AB_CANDIDATE_TEST_RESULTS.csv"),
    ("AUT directo por A", "run_direct_aut_tests.py", "DIRECT_AUT_TEST_RESULTS.csv"),
    ("C / CUT", "run_iteration_09_tests.py", "C_TEST_RESULTS.csv"),
    ("gap / concurrencia", "run_iteration_10_tests.py",
     "GAP_CONCURRENCY_TEST_RESULTS.csv"),
    ("TT", "run_iteration_11_tests.py", "TT_TEST_RESULTS.csv"),
    ("ciclo / FT", "run_iteration_12_tests.py", "ITER12_TEST_RESULTS.csv"),
    ("gap prioridad / plano", "run_iteration_13_tests.py", "ITER13_TEST_RESULTS.csv"),
]

READER_LINE = re.compile(
    r"^READER module=(\S+) path=(.+?) sha256=([0-9A-F]+) core_version=(\S+)$")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def main() -> int:
    engine = (ENGINE / f"{MODULE}.py").resolve()
    sha = sha256_file(engine)
    env = dict(os.environ)
    env["TM_READER_MODULE"] = MODULE
    env["TM_READER_SHA256"] = sha
    env["TM_READER_CORE_VERSION"] = EXPECTED_VERSION
    env["TM_REFERENCE_ENGINE_DIR"] = str(ENGINE)

    map_rows, authority_rows = [], []
    totals = {"PASS": 0, "FAIL": 0}
    for suite, script, csv_name in SUITES:
        out = subprocess.run([sys.executable, str(HERE / script)], cwd=str(HERE),
                             capture_output=True, text=True, encoding="utf-8",
                             env=env)
        reader = None
        for line in out.stdout.splitlines():
            m = READER_LINE.match(line.strip())
            if m:
                reader = m.groups()
        status = "OK" if out.returncode == 0 and reader else "BINDING_FAILURE"
        if reader:
            mod, path, got_sha, version = reader
            binding_ok = (mod == MODULE and Path(path).resolve() == engine
                          and got_sha == sha and version == EXPECTED_VERSION)
        else:
            mod, path, got_sha, version, binding_ok = "", "", "", "", False
        if not binding_ok:
            status = "BINDING_FAILURE"

        rows = []
        csv_path = HERE / csv_name
        if csv_path.exists():
            with csv_path.open(encoding="utf-8", newline="") as fh:
                rows = list(csv.DictReader(fh))
        counts = {"CANONICAL_PASS": 0, "PROVISIONAL_POLICY_PASS": 0,
                  "OPEN_RULE_BLOCK": 0, "FAIL": 0}
        for row in rows:
            passed = str(row.get("pass", "")).lower() == "true"
            cls = (row.get("classification") or "").strip()
            if not cls:
                cls = "CANONICAL_PASS" if passed else "FAIL"
            counts[cls] = counts.get(cls, 0) + 1
            totals["PASS" if passed else "FAIL"] += 1
            authority_rows.append({
                "suite": suite, "test_id": row.get("test_id", ""),
                "status": "PASS" if passed else "FAIL",
                "classification": cls,
                "description": (row.get("description") or "")[:160],
            })
        map_rows.append({
            "suite": suite, "script": script, "env_TM_READER_MODULE": MODULE,
            "module_imported": mod, "path": path, "sha256": got_sha,
            "core_version": version, "expected_sha256": sha,
            "expected_version": EXPECTED_VERSION,
            "binding": "OK" if binding_ok else "BINDING_FAILURE",
            "suite_status": status, "tests": len(rows),
            "canonical": counts["CANONICAL_PASS"],
            "provisional": counts["PROVISIONAL_POLICY_PASS"],
            "open_rule": counts["OPEN_RULE_BLOCK"],
            "fail": counts["FAIL"] + (0 if status == "OK" else 1),
        })
        if status != "OK":
            print(f"BINDING_FAILURE {suite}: {out.stderr[-300:]}")

    with (HERE / "SUITE_ENGINE_MAP.csv").open("w", newline="",
                                              encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(map_rows[0].keys()))
        w.writeheader()
        w.writerows(map_rows)
    with (HERE / "TEST_AUTHORITY_ROWS.csv").open("w", newline="",
                                                 encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["suite", "test_id", "status",
                                           "classification", "description"])
        w.writeheader()
        w.writerows(authority_rows)

    agg = {k: sum(1 for r in authority_rows if r["classification"] == k)
           for k in ("CANONICAL_PASS", "PROVISIONAL_POLICY_PASS",
                     "OPEN_RULE_BLOCK", "FAIL")}
    summary = {
        "reader_module": MODULE,
        "reader_path": str(engine),
        "reader_sha256": sha,
        "core_version": EXPECTED_VERSION,
        "suites": len(SUITES),
        "suites_bound": sum(1 for r in map_rows if r["binding"] == "OK"),
        "tests_total": len(authority_rows),
        "pass": totals["PASS"],
        "fail": totals["FAIL"],
        "canonical_pass": agg["CANONICAL_PASS"],
        "provisional_policy_pass": agg["PROVISIONAL_POLICY_PASS"],
        "open_rule_block": agg["OPEN_RULE_BLOCK"],
        "failed": agg["FAIL"],
        "authority_source": "CSV classification column (structured)",
    }
    (HERE / "TEST_AUTHORITY_SUMMARY.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["suites_bound"] == len(SUITES) and totals["FAIL"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
