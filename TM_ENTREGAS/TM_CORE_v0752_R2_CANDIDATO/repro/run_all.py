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
print("TRANSFORMATION_TESTS:", flush=True)
subprocess.run([sys.executable,str(ROOT/"tests"/"test_transformations.py")],check=True)
cmd = [sys.executable, str(CORE), "--feed", str(FEED), "--out", str(OUT)]
print("CORE:", " ".join(cmd), flush=True)
subprocess.run(cmd, check=True)
print("COMPARISON:", flush=True)
comparison = subprocess.run([sys.executable, str(ROOT / "repro" / "compare_golden.py")])
raw = json.loads((OUT / "CORE_RAW_OUTPUT.json").read_text(encoding="utf-8"))
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
}
(OUT / "RUN_SUMMARY.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=2))
raise SystemExit(comparison.returncode)
