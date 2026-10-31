from __future__ import annotations
import difflib, hashlib, json, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUTZIP=ROOT.parent/"TM_CORE_v0752_CANONICAL.zip"
LEGACY=ROOT/"legacy_frozen"/"TM_CORE_PYTHON_v0751_STREAMING.py"
CORE=ROOT/"python"/"TM_CORE_PYTHON_v0752_CANONICAL.py"
diff="".join(difflib.unified_diff(LEGACY.read_text(encoding="utf-8").splitlines(True),
    CORE.read_text(encoding="utf-8").splitlines(True),fromfile="v0751/TM_CORE_PYTHON_v0751_STREAMING.py",
    tofile="v0752/TM_CORE_PYTHON_v0752_CANONICAL.py"))
(ROOT/"diff_v0751_to_v0752.diff").write_text(diff,encoding="utf-8",newline="\n")
files=sorted(p for p in ROOT.rglob("*") if p.is_file() and p.name not in {"manifest.json","SHA256SUMS.txt"} and "__pycache__" not in p.parts and ".pyc" not in p.suffix)
entries=[]
for p in files:
    rel=p.relative_to(ROOT).as_posix()
    entries.append({"path":rel,"size_bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
manifest={"package":"TM_CORE_v0752_CANONICAL","version":"0.7.5.2","status":"CANDIDATO_PENDIENTE_READER_VALIDATOR_Y_MIMO",
          "file_count":len(entries)+2,"payload_file_count":len(entries),"files":entries,
          "authorities":{"tree":"TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_13_PROPUESTA_R1.md (candidate; not Javier-approved)",
                          "feed":"data/TM_TICKFEED_1615_1730.csv","golden":"data/TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v003.txt"},
          "reproduction":"python repro/run_all.py","verdict":"LECTURA_NO_REPRODUCIDA"}
(ROOT/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
sum_lines=[]
for p in sorted([p for p in ROOT.rglob("*") if p.is_file() and p.name!="SHA256SUMS.txt" and "__pycache__" not in p.parts and ".pyc" not in p.suffix]):
    sum_lines.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT).as_posix()}")
(ROOT/"SHA256SUMS.txt").write_text("\n".join(sum_lines)+"\n",encoding="utf-8")
with zipfile.ZipFile(OUTZIP,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(p for p in ROOT.rglob("*") if p.is_file() and "__pycache__" not in p.parts and ".pyc" not in p.suffix):
        z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(OUTZIP) as z:
    names=z.namelist();bad=[n for n in names if "\\" in n or n.startswith("/") or ":" in n]
    missing=[e["path"] for e in entries if e["path"] not in names]
    if bad or missing or len(names)!=manifest["file_count"]:raise SystemExit({"bad":bad,"missing":missing,"actual":len(names),"manifest":manifest["file_count"]})
print(json.dumps({"zip":str(OUTZIP),"size_bytes":OUTZIP.stat().st_size,"sha256":hashlib.sha256(OUTZIP.read_bytes()).hexdigest(),"files":len(names),"payload":len(entries),"manifest_missing":len(missing),"invalid_paths":len(bad)},indent=2))
