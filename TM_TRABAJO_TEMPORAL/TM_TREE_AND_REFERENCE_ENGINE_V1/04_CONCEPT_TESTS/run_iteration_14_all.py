#!/usr/bin/env python3
"""ITERACION 14 — ejecuta todas las suites y agrega resultados."""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

SUITES = [
    ("core", "run_core_tests.py"),
    ("A/B/B Grande/AUT", "run_ab_candidate_tests.py"),
    ("AUT directo por A", "run_direct_aut_tests.py"),
    ("C / CUT", "run_iteration_09_tests.py"),
    ("gap / concurrencia", "run_iteration_10_tests.py"),
    ("TT", "run_iteration_11_tests.py"),
    ("ciclo / FT", "run_iteration_12_tests.py"),
    ("gap prioridad / plano", "run_iteration_13_tests.py"),
]

LINE = re.compile(r"^(PASS|FAIL)\s+(\S+)\s*(.*)$")


def main() -> int:
    rows, totals = [], {"PASS": 0, "FAIL": 0}
    for suite, script in SUITES:
        out = subprocess.run([sys.executable, str(HERE / script)],
                             capture_output=True, text=True, encoding="utf-8")
        for line in out.stdout.splitlines():
            m = LINE.match(line.strip())
            if not m:
                continue
            status, test_id, rest = m.groups()
            authority = "CANONICAL"
            if "PROVISIONAL_POLICY_PASS" in rest:
                authority = "PROVISIONAL"
            if "OPEN_RULE_BLOCK" in rest:
                authority = "OPEN_RULE"
            rows.append({"suite": suite, "test_id": test_id,
                         "status": status, "authority": authority,
                         "detail": rest[:200]})
            totals[status] += 1
        if out.returncode != 0:
            rows.append({"suite": suite, "test_id": "SUITE", "status": "FAIL",
                         "authority": "CANONICAL",
                         "detail": out.stderr[-200:]})
            totals["FAIL"] += 1

    with (HERE / "ITER14_TEST_RESULTS.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["suite", "test_id", "status",
                                           "authority", "detail"])
        w.writeheader()
        w.writerows(rows)
    provisional = sum(1 for r in rows if r["authority"] == "PROVISIONAL")
    canonical = sum(1 for r in rows if r["authority"] == "CANONICAL")
    blocked = sum(1 for r in rows if r["authority"] == "OPEN_RULE")
    summary = {"total": len(rows), "pass": totals["PASS"], "fail": totals["FAIL"],
               "canonical": canonical, "provisional": provisional,
               "open_rule": blocked}
    (HERE / "ITER14_TEST_RESULTS.json").write_text(json.dumps(summary, indent=2),
                                                   encoding="utf-8")
    print(json.dumps(summary, indent=2))
    for r in rows:
        if r["status"] == "FAIL":
            print("FAIL", r["suite"], r["test_id"], r["detail"])
    return 0 if totals["FAIL"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
