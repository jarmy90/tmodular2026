from __future__ import annotations
import hashlib, json, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUTZIP=ROOT.parent/"TM_CORE_v0752_R3_B_AUT.zip"
MANIFEST=ROOT/"manifest.json"
SUMS=ROOT/"SHA256SUMS.txt"

entries=[]
for p in sorted(p for p in ROOT.rglob("*") if p.is_file()
                and p.name not in {"manifest.json","SHA256SUMS.txt"}
                and "__pycache__" not in p.parts and ".pytest_cache" not in p.parts
                and p.suffix!=".pyc"):
    rel=p.relative_to(ROOT).as_posix()
    entries.append({"path":rel,"size_bytes":p.stat().st_size,
                    "sha256":hashlib.sha256(p.read_bytes()).hexdigest()})

run_summary=json.loads((ROOT/"out"/"RUN_SUMMARY.json").read_text(encoding="utf-8"))
comparison=json.loads((ROOT/"out"/"GOLDEN_COMPARISON.json").read_text(encoding="utf-8"))
prefix=json.loads((ROOT/"out"/"TRANSITION_PREFIXES.json").read_text(encoding="utf-8"))
manifest={
  "package":"TM_CORE_v0752_R3_B_AUT",
  "version":"0.7.5.2-R3",
  "status":"CANDIDATO_PENDIENTE_READER_VALIDATOR_Y_MIMO",
  "tree_status":"CANDIDATO_PENDIENTE_APROBACION_JAVIER",
  "file_count":len(entries)+2,"payload_file_count":len(entries),"files":entries,
  "authorities":{"tree":"authority/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA_R2.md",
    "approved_tree_base":"authority/TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_12.md",
    "feed":"data/TM_TICKFEED_1615_1730.csv",
    "golden":"data/TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v003.txt"},
  "source_versions":{"frozen_base":"0.7.5.2-R2","legacy":"0.7.5.1"},
  "results":{"core_raw_sha256":run_summary["core_raw_sha256"],
    "feed_points":run_summary["feed_points"],"events":run_summary["events"],
    "readings":run_summary["readings"],"golden_passed":comparison["passed"],
    "golden_total":comparison["total"],"transition_prefixes":prefix["cuts"],
    "prefix_failures":prefix["prefix_failures"],"R0062_R0064":run_summary["R0062_R0064"]},
  "reproduction":"python repro/run_all.py",
  "known_failures":["Golden v003 16:23 AUT claim conflicts with the universal B interval; golden is unchanged",
    "16:23 AUT opposite-direction and 16:24 chain remain unreproduced",
    "A passing synthetic suite and 12 physical transition prefixes do not establish autonomous reading accuracy"],
  "not_authorized":["replay ciego","AFS2","produccion"]
}
MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")

sum_lines=[]
for p in sorted(p for p in ROOT.rglob("*") if p.is_file() and p.name!="SHA256SUMS.txt"
                and "__pycache__" not in p.parts and ".pytest_cache" not in p.parts and p.suffix!=".pyc"):
    sum_lines.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT).as_posix()}")
SUMS.write_text("\n".join(sum_lines)+"\n",encoding="utf-8")

with zipfile.ZipFile(OUTZIP,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(p for p in ROOT.rglob("*") if p.is_file() and "__pycache__" not in p.parts
                    and ".pytest_cache" not in p.parts and p.suffix!=".pyc"):
        z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(OUTZIP) as z:
    names=z.namelist();bad=[n for n in names if "\\" in n or n.startswith("/") or ":" in n]
    missing=[e["path"] for e in entries if e["path"] not in names]
    if bad or missing or len(names)!=manifest["file_count"]:
        raise SystemExit({"bad":bad,"missing":missing,"zip_count":len(names),"manifest_count":manifest["file_count"]})
print(json.dumps({"zip":str(OUTZIP),"size_bytes":OUTZIP.stat().st_size,
  "sha256":hashlib.sha256(OUTZIP.read_bytes()).hexdigest(),"file_count":len(names),
  "payload_files":len(entries),"manifest_files_missing":len(missing),"invalid_paths":len(bad)},indent=2))
