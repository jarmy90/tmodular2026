from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "python" / "TM_CORE_PYTHON_v0752_CANONICAL.py"
FEED = ROOT / "data" / "TM_TICKFEED_1615_1730.csv"
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)
print("SELFTEST:", flush=True)
subprocess.run([sys.executable,str(CORE),"--selftest"],check=True)
print("UNIVERSAL_B_AUT_TESTS:", flush=True)
subprocess.run([sys.executable,str(ROOT/"tests"/"test_big_b_aut.py")],check=True)
print("LEGACY_20_TESTS:", flush=True)
subprocess.run([sys.executable,"-m","pytest","-q",str(ROOT/"tests"/"legacy_v075"/"TM_CORE_PYTHON_v075_TESTS.py")],check=True)
print("TRANSFORMATION_TESTS:", flush=True)
subprocess.run([sys.executable,str(ROOT/"tests"/"test_transformations.py")],check=True)
cmd = [sys.executable, str(CORE), "--feed", str(FEED), "--out", str(OUT)]
print("CORE:", " ".join(cmd), flush=True)
subprocess.run(cmd, check=True)
print("PHYSICAL_TRANSITION_PREFIXES:", flush=True)
prefixes=subprocess.run([sys.executable,str(ROOT/"repro"/"run_transition_prefixes.py")])
if prefixes.returncode: raise SystemExit(prefixes.returncode)
print("COMPARISON:", flush=True)
comparison = subprocess.run([sys.executable, str(ROOT / "repro" / "compare_golden.py")])
raw = json.loads((OUT / "CORE_RAW_OUTPUT.json").read_text(encoding="utf-8"))
prefix_report=json.loads((OUT/"TRANSITION_PREFIXES.json").read_text(encoding="utf-8"))
summary = {
    "core_raw_sha256": hashlib.sha256((OUT / "CORE_RAW_OUTPUT.json").read_bytes()).hexdigest(),
    "feed_points": raw["feed_points"], "events": len(raw["events"]),
    "readings": len(raw["readings"]), "local_sequences": len(raw["local_sequences"]),
    "local_events": len(raw["local_events"]),
    "R0062_R0064": [
        {k:r.get(k) for k in ("reading_id","state","module_origin","module_extreme","tt_target","tt_hit","ft","ft_price")}
        for r in raw["readings"] if r.get("reading_id") in ("R0062","R0064")
    ],
    "comparison_exit": comparison.returncode,
    "transition_prefixes": prefix_report["cuts"],
    "prefix_failures": prefix_report["prefix_failures"],
    "aut_causes": sorted({e.get("aut_source") for e in raw["events"] if e.get("function")=="AUT" and e.get("aut_source")}),
}
(OUT / "RUN_SUMMARY.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=2))
subprocess.run([sys.executable,str(ROOT/"repro"/"build_diffs.py")],check=True)
print("BUILD_FROZEN_PACKAGE:", flush=True)
subprocess.run([sys.executable,str(ROOT/"repro"/"build_package.py")],check=True)
raise SystemExit(comparison.returncode)
