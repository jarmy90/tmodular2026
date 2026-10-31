"""Fresh-process physical cut replay around live B/C/AUT transitions."""
from __future__ import annotations
import csv, hashlib, json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FEED=ROOT/"data"/"TM_TICKFEED_1615_1730.csv"
CORE=ROOT/"python"/"TM_CORE_PYTHON_v0752_CANONICAL.py"
FULL=json.loads((ROOT/"out"/"CORE_RAW_OUTPUT.json").read_text(encoding="utf-8"))
ROWS=list(csv.DictReader(FEED.open(encoding="utf-8-sig",newline=""),delimiter=";"))
OUT=ROOT/"out"/"transition_prefixes";OUT.mkdir(parents=True,exist_ok=True)

def signature(e):
    return (e.get("kind"),e.get("function"),e.get("reading_id"),e.get("parent_reading_id"),
            e.get("sequence_id"),e.get("structural_sequence_id"),e.get("confirmation_sequence_id"),
            e.get("knowledge_sequence_id"),e.get("aut_source"),e.get("price"),e.get("reason"))

def run_cut(seq:int)->dict:
    cutfile=OUT/f"feed_through_{seq}.csv";od=OUT/f"out_{seq}";od.mkdir(exist_ok=True)
    with cutfile.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=ROWS[0].keys(),delimiter=";");w.writeheader()
        w.writerows(row for row in ROWS if int(row["sequence_id"])<=seq)
    subprocess.run([sys.executable,str(CORE),"--feed",str(cutfile),"--out",str(od)],check=True,stdout=subprocess.DEVNULL)
    observed=json.loads((od/"CORE_RAW_OUTPUT.json").read_text(encoding="utf-8"))
    expected=[signature(e) for e in FULL["events"] if e.get("knowledge_sequence_id",0)<=seq and e.get("kind")!="FIN_FEED"]
    actual=[signature(e) for e in observed["events"] if e.get("kind")!="FIN_FEED"]
    return {"cut_sequence_id":seq,"ticks":sum(int(row["sequence_id"])<=seq for row in ROWS),
            "physical_feed_sha256":hashlib.sha256(cutfile.read_bytes()).hexdigest(),
            "expected_events":len(expected),"observed_events":len(actual),"passed":expected==actual}

def main()->int:
    seeds=[]
    for event in FULL["events"]:
        if event.get("kind")=="AUT" and event.get("aut_source")=="B_EXCEEDS_127_PLUS_0_25":
            seeds.append(int(event["knowledge_sequence_id"]));break
    for function in ("AUT","B","C"):
        event=next((e for e in FULL["events"] if e.get("kind")=="LOCAL_FUNCTION" and e.get("function")==function),None)
        if event:seeds.append(int(event["knowledge_sequence_id"]))
    last=int(ROWS[-1]["sequence_id"])
    cuts=sorted({n for seq in seeds for n in (max(1,seq-1),seq,min(last,seq+1))})
    results=[run_cut(seq) for seq in cuts]
    report={"method":"physical CSV truncation; fresh Python subprocess per cut; compare emitted knowledge prefix only",
            "transition_seeds":seeds,"cuts":len(results),"prefix_failures":sum(not x["passed"] for x in results),"results":results}
    (ROOT/"out"/"TRANSITION_PREFIXES.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k!="results"},indent=2))
    return 0 if report["prefix_failures"]==0 else 2

if __name__=="__main__":raise SystemExit(main())
