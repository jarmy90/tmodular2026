"""Physical-prefix replay in a fresh subprocess for every cut.

The full matrix is intentionally a separate, opt-in run. It uses the raw master
CSV, truncates the file physically, starts a new interpreter, then compares only
the knowledge prefix available at that cut.
"""
from __future__ import annotations
import csv, hashlib, json, random, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FEED=ROOT/"data"/"TM_TICKFEED_1615_1730.csv"
CORE=ROOT/"python"/"TM_CORE_PYTHON_v0752_CANONICAL.py"
FULL=json.loads((ROOT/"out"/"CORE_RAW_OUTPUT.json").read_text(encoding="utf-8"))
ROWS=list(csv.DictReader(FEED.open(encoding="utf-8-sig",newline=""),delimiter=";"))
OUT=ROOT/"out"/"prefix_checks";OUT.mkdir(parents=True,exist_ok=True)

def digest(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def signature(e):
    return (e.get("kind"),e.get("function"),e.get("reading_id"),e.get("parent_reading_id"),
            e.get("sequence_id"),e.get("structural_sequence_id"),e.get("confirmation_sequence_id"),
            e.get("knowledge_sequence_id"),e.get("structural_time_ms"),e.get("confirmation_time_ms"),
            e.get("knowledge_time_ms"),e.get("price"),e.get("reason"))

def run_cut(seq:int,label:str)->dict:
    cutfile=OUT/f"{label}_{seq}.csv";od=OUT/f"out_{label}_{seq}";od.mkdir(exist_ok=True)
    with cutfile.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=ROWS[0].keys(),delimiter=";");w.writeheader()
        w.writerows(row for row in ROWS if int(row["sequence_id"])<=seq)
    subprocess.run([sys.executable,str(CORE),"--feed",str(cutfile),"--out",str(od)],check=True,stdout=subprocess.DEVNULL)
    observed=json.loads((od/"CORE_RAW_OUTPUT.json").read_text(encoding="utf-8"))
    expected=[signature(e) for e in FULL["events"] if e.get("knowledge_sequence_id",0)<=seq and e.get("kind")!="FIN_FEED"]
    actual=[signature(e) for e in observed["events"] if e.get("kind")!="FIN_FEED"]
    return {"label":label,"cut_sequence_id":seq,"physical_file_sha256":digest(cutfile),
            "prefix_events_expected":len(expected),"prefix_events_observed":len(actual),
            "passed":expected==actual}

def main():
    # Candle close sequences are derived from the master CSV, never typed by hand.
    closes={}
    for row in ROWS:closes[row["bar_time_m1"]]=int(row["sequence_id"])
    cuts=[(seq,"bar_close") for seq in closes.values()]
    rng=random.Random(7552)
    seqs=[int(r["sequence_id"]) for r in ROWS]
    cuts += [(rng.choice(seqs),"random") for _ in range(500)]
    # Include one tick before/at/after first local confirmation of each function kind.
    local=[e for e in FULL["events"] if e.get("kind")=="LOCAL_FUNCTION" and e.get("function") in {"1","2","3","AUT"}]
    chosen={}
    for e in local:
        key=(e.get("bar_time"),e.get("function"))
        chosen.setdefault(key,int(e["knowledge_sequence_id"]))
    for (bar,fn),seq in chosen.items():
        for n in (max(1,seq-1),seq,min(seqs[-1],seq+1)):cuts.append((n,f"{bar}_{fn}"))
    results=[]
    for i,(seq,label) in enumerate(cuts,1):
        results.append(run_cut(seq,label))
        if i%25==0:print(f"prefixes {i}/{len(cuts)}",flush=True)
    report={"seed":7552,"cuts":len(results),"prefix_failures":sum(not r["passed"] for r in results),"results":results}
    (ROOT/"out"/"PREFIX_MATRIX.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k!="results"},indent=2))
    return 0 if report["prefix_failures"]==0 else 2
if __name__=="__main__":raise SystemExit(main())
