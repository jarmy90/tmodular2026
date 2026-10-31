#!/usr/bin/env python3
"""Final attempt for ITERACION_08_DIRECT_AUT package build."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("C:/Users/profesor/tm/Teoria Modular")
PKG = ROOT / "TM_TRABAJO_TEMPORAL" / "TM_TREE_AND_REFERENCE_ENGINE_V1" / "13_ITERATION_PACKAGES"
BUILD_SCRIPT = PKG / "build_iteration_08.py"
OUT_DIR = ROOT / "TM_ENTREGAS_ITERACION" / "ITERACION_08_DIRECT_AUT_20261030_1826"
ZIP_PATH = ROOT / "TM_ENTREGAS_ITERACION" / "TM_ITERATION_08_REVIEW.zip"
RUNNING_MARKER = PKG / "build_08_running_indicator.txt"
REPORT_MARKER = PKG / "build_08_final_run_marker.txt"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def log(msg: str) -> None:
    sys.stderr.write(msg + "\n")
    sys.stderr.flush()


def listed_files(root: Path) -> list[str]:
    try:
        return sorted(p.name for p in root.iterdir() if p.is_file())
    except OSError as e:
        return ["ERR:" + str(e)]


def main() -> int:
    log("BEGIN " + now_iso())
    status = {
        "started_at": now_iso(),
        "python": sys.executable,
        "cwd": os.getcwd(),
        "pkg_exists": BUILD_SCRIPT.is_file(),
        "pkg_dir_files_before": listed_files(PKG),
        "out_dir_exists_before": OUT_DIR.exists(),
        "zip_exists_before": ZIP_PATH.exists(),
        "marker_found": False,
        "rule_of_three_waiting": True,
        "command": None,
        "returncode": None,
        "stdout": None,
        "stderr": None,
        "after_marker": None,
        "out_dir_files_after": None,
        "zip_exists_after": None,
        "finished_at": None,
    }

    try:
        if not BUILD_SCRIPT.is_file():
            log("build script missing")
            status["error"] = "build script missing"
            return 1

        log("RUN " + now_iso())
        proc = subprocess.run(
            [sys.executable, str(BUILD_SCRIPT)],
            cwd=str(PKG),
            capture_output=True,
            text=True,
            timeout=120,
        )
        status["command"] = "python " + str(BUILD_SCRIPT)
        status["returncode"] = proc.returncode
        status["stdout"] = proc.stdout
        status["stderr"] = proc.stderr
        log("RUN_DONE rc=" + str(proc.returncode) + " " + now_iso())

        # rule of three wait
        for _ in range(60):
            if RUNNING_MARKER.is_file():
                status["marker_found"] = True
                break
            time.sleep(1)

        if RUNNING_MARKER.is_file():
            try:
                status["after_marker"] = RUNNING_MARKER.read_text(encoding="utf-8")
            except OSError as e:
                status["after_marker_error"] = str(e)

    except subprocess.TimeoutExpired:
        status["error"] = "timeout"
        status["command"] = "python " + str(BUILD_SCRIPT) + " (timeout)"
    except Exception as e:
        status["error"] = repr(e)

    status["out_dir_files_after"] = listed_files(OUT_DIR) if OUT_DIR.exists() else None
    status["zip_exists_after"] = ZIP_PATH.exists() if ZIP_PATH.exists() else False
    status["finished_at"] = now_iso()

    REPORT_MARKER.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MARKER.write_text(json.dumps(status, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if status.get("zip_exists_after"):
        log("ZIP_READY")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
