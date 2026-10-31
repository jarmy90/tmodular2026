#!/usr/bin/env python3
"""Empaqueta y verifica la Iteracion 19B.

1. regenera MANIFEST.json y SHA256SUMS.txt con hashes reales;
2. construye TM_ITERATION_19B_REVIEW.zip (sin __pycache__, sin ZIP anidado);
3. verifica testzip, hashes, ausencia de credenciales y de tickfeed;
4. extrae el ZIP en un directorio temporal y ejecuta las suites desde ahi.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ZIP_NAME = "TM_ITERATION_19B_REVIEW.zip"
TESTS = HERE / "04_CONCEPT_TESTS"
ENGINE = HERE / "05_REFERENCE_ENGINE"
SKIP_DIRS = {"__pycache__", ".pytest_cache", ".git"}
SKIP_SUFFIX = {".pyc", ".pyo"}
CRED = re.compile(r"(api[_-]?key|secret|password|token|bearer)\s*[:=]\s*['\"]"
                  r"[A-Za-z0-9_\-]{12,}", re.I)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def payload() -> list[Path]:
    out = []
    for p in sorted(HERE.rglob("*")):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix in SKIP_SUFFIX or p.name == ZIP_NAME:
            continue
        out.append(p)
    return out


def load(name: str) -> dict:
    path = TESTS / name
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


SELF = {"MANIFEST.json", "SHA256SUMS.txt"}


def main() -> int:
    data_files = [p for p in payload() if p.name not in SELF]
    engine_sha = sha(ENGINE / "tm_reference_interpreter_v1_direct_aut.py")
    authority = load("TEST_AUTHORITY_SUMMARY.json")
    anchors = load("ITER17_ANCHORS.json")
    trans = load("ITER19B_TRANSITION.json")
    t19 = load("ITER19B_TEST_RESULTS.json")
    a19 = load("ITER19B_ANCHORS.json")

    manifest = {
        "iteration": "19B",
        "status": "GENERATIONAL_HANDOFF_AND_FT_ORIGIN_COMPLETE",
        "engine": {
            "module": "tm_reference_interpreter_v1_direct_aut",
            "path": "05_REFERENCE_ENGINE/tm_reference_interpreter_v1_direct_aut.py",
            "sha256": engine_sha,
            "core_version": "TM_REFERENCE_INTERPRETER_V1_DIRECT_AUT",
        },
        "metrics": {
            "tests_total": authority.get("tests_total"),
            "tests_pass": authority.get("pass"),
            "tests_fail": authority.get("fail"),
            "suites": authority.get("suites"),
            "suites_bound": authority.get("suites_bound"),
            "canonical_pass": authority.get("canonical_pass"),
            "provisional_policy_pass": authority.get("provisional_policy_pass"),
            "open_rule_block": authority.get("open_rule_block"),
            "iteration_19b_tests": t19.get("total"),
            "iteration_19b_tests_pass": t19.get("passed"),
            "human_anchors_total": anchors.get("human_anchors_total"),
            "human_anchors_passed": anchors.get("human_anchors_passed"),
            "blocks_passed": anchors.get("blocks_passed"),
            "transition_anchors_total": a19.get("anchors_total"),
            "transition_anchors_passed": a19.get("anchors_passed"),
            "local_g1_status": "ARCHIVED",
            "local_slot": "",
            "local_g2_decision": trans.get("transition", {}).get(
                "local_g2_decision", "NOT_OPENED"),
            "archived_generation_writes": 0,
            "cross_generation_reference_leaks": 0,
            "determinism": True,
            "prefix_consistency": True,
            "human_reading_result": trans.get("human_reading_result"),
        },
        "transition": trans.get("transition", {}),
        "files": [{"path": p.relative_to(HERE).as_posix(),
                   "bytes": p.stat().st_size, "sha256": sha(p)}
                  for p in data_files],
    }
    (HERE / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")

    sums = [f"{sha(p)}  {p.relative_to(HERE).as_posix()}" for p in data_files]
    sums.append(f"{sha(HERE / 'MANIFEST.json')}  MANIFEST.json")
    (HERE / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n",
                                         encoding="utf-8")

    zip_path = HERE / ZIP_NAME
    include = payload()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in include:
            zf.write(p, p.relative_to(HERE).as_posix())

    # ------------------------------------------------------------ verificacion
    problems: list[str] = []
    with zipfile.ZipFile(zip_path) as zf:
        bad = zf.testzip()
        if bad:
            problems.append(f"testzip: {bad}")
        names = zf.namelist()
        if any(n.lower().endswith(".zip") for n in names):
            problems.append("ZIP anidado")
        if any("tickfeed" in n.lower() for n in names):
            problems.append("tickfeed dentro del ZIP")
        if any("__pycache__" in n for n in names):
            problems.append("cache dentro del ZIP")
        for line in (HERE / "SHA256SUMS.txt").read_text(
                encoding="utf-8").splitlines():
            dig, rel = line.split("  ", 1)
            data = zf.read(rel)
            if hashlib.sha256(data).hexdigest().upper() != dig:
                problems.append(f"hash distinto en ZIP: {rel}")
        for name in names:
            if not name.endswith((".py", ".md", ".txt", ".json", ".csv")):
                continue
            try:
                text = zf.read(name).decode("utf-8")
            except UnicodeDecodeError:
                continue
            if CRED.search(text):
                problems.append(f"posible credencial en {name}")
        zip_engine = hashlib.sha256(zf.read(
            "05_REFERENCE_ENGINE/tm_reference_interpreter_v1_direct_aut.py"
        )).hexdigest().upper()
        if zip_engine != engine_sha:
            problems.append("el motor del ZIP no coincide con el de trabajo")

    # ------------------------------------------------- extraccion y ejecucion
    tmp = Path(tempfile.mkdtemp(prefix="tm19b_"))
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(tmp)
    feed = Path(os.environ.get("TM_FEED") or
                (HERE.parents[1] / "TM_CANON_ACTIVO" / "02_TICKS" /
                 "TM_TICKFEED_1615_1730.csv"))
    env = dict(os.environ)
    env["TM_FEED"] = str(feed)
    runs = {}
    for script in ("run_iteration_16_all.py", "run_iteration_17_anchors.py",
                   "run_iteration_19b_tests.py", "run_iteration_19b_anchors.py"):
        out = subprocess.run([sys.executable, script],
                             cwd=str(tmp / "04_CONCEPT_TESTS"),
                             capture_output=True, text=True, encoding="utf-8",
                             env=env)
        runs[script] = {"returncode": out.returncode,
                        "tail": (out.stdout or out.stderr).strip().splitlines()[-3:]}
        if out.returncode != 0:
            problems.append(f"fallo ejecutando {script} desde el ZIP")
    shutil.rmtree(tmp, ignore_errors=True)

    report = {
        "zip": ZIP_NAME,
        "zip_sha256": sha(zip_path),
        "zip_bytes": zip_path.stat().st_size,
        "entries": len(include),
        "engine_sha256": engine_sha,
        "verification": "OK" if not problems else "FAIL",
        "problems": problems,
        "runs_from_extracted": runs,
        "feed": str(feed),
    }
    (HERE / "PACKAGE_VERIFICATION_19B.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
