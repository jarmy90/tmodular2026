"""Build the flat ITERACION_04 delivery and its verified review ZIP."""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MISSION = Path(__file__).resolve().parents[1]
READ = MISSION / "01_BLIND_READINGS"
REG = MISSION / "06_REGRESSION"
MOV = MISSION / "02_MOVEMENT_ANALYSIS"
DELIVERY_ROOT = ROOT / "TM_ENTREGAS_ITERACION"

STAMP = datetime.now().strftime("%Y%m%d_%H%M")
ITER_NAME = f"ITERACION_04_{STAMP}"
ITER_DIR = DELIVERY_ROOT / ITER_NAME
ZIP_PATH = DELIVERY_ROOT / "TM_ITERATION_04_REVIEW.zip"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def add(src: Path, name: str, reason: str) -> dict:
    dst = ITER_DIR / name
    shutil.copy2(src, dst)
    return {
        "zip_path": f"{ITER_NAME}/{name}",
        "original_path": str(src.relative_to(ROOT)),
        "size": dst.stat().st_size,
        "sha256": sha256(dst),
        "reason": reason,
    }


def main() -> int:
    DELIVERY_ROOT.mkdir(parents=True, exist_ok=True)
    ITER_DIR.mkdir(parents=True, exist_ok=False)

    files: list[dict] = []
    files.append(add(MISSION / "09_REPORTS/CHECKPOINT_4_REPORT.md",
                     "01_CHECKPOINT_4_REPORT.md", "checkpoint y decisiones aplicadas"))
    files.append(add(MISSION / "04_EXPERT_QUESTIONS/PHASE_4_QUESTIONS.md",
                     "02_PHASE_4_QUESTIONS.md", "preguntas expertas"))
    files.append(add(READ / "blind_reader_v4_functional_autonomy.py",
                     "03_blind_reader_v4_functional_autonomy.py", "lector v4"))
    files.append(add(READ / "V4_FULL_GENERATIONS.csv",
                     "04_PHASE_4_GENERATIONS_L1.csv", "generaciones L1 finales"))
    files.append(add(READ / "V4_L2_1619_1624_GENERATIONS.csv",
                     "05_PHASE_4_GENERATIONS_L2.csv", "generaciones L2"))
    files.append(add(READ / "V4_CLASSIC_GENERATIONS.csv",
                     "06_PHASE_4_GENERATIONS_CLASSIC.csv", "v4 classic para aislar A"))
    files.append(add(MOV / "V4_ABSORPTIONS.csv",
                     "08_PHASE_4_ABSORPTIONS.csv", "absorciones y confirmaciones de A"))
    files.append(add(REG / "PHASE_4_L1_L2_MAP.csv",
                     "09_PHASE_4_L1_L2_MAP.csv", "mapa L1/L2"))
    files.append(add(MOV / "PHASE_4_DIVERGENCES.csv",
                     "10_PHASE_4_DIVERGENCES.csv", "divergencias"))
    files.append(add(MISSION / "05_TREE_REVISIONS/TREE_REVISION_v2_20_DRAFT_R2.md",
                     "11_TREE_REVISION_v2_20_DRAFT_R2.md", "borrador v2.20 R2"))
    files.append(add(REG / "PHASE_4_DETERMINISM.json",
                     "12_PHASE_4_DETERMINISM.json", "determinismo"))
    files.append(add(REG / "PHASE_4_SUMMARY.json",
                     "13_PHASE_4_SUMMARY.json", "resumen de auditoría"))
    files.append(add(REG / "PHASE_4_GENERATION_AUDIT.csv",
                     "14_PHASE_4_GENERATION_AUDIT.csv", "auditoría por generación"))
    files.append(add(MOV / "V4_BEFORE_AFTER.csv",
                     "16_V4_BEFORE_AFTER.csv", "antes/después 51/4/44"))
    files.append(add(MISSION / "05_TREE_REVISIONS/EXPERIMENTAL_POLICIES_V4.md",
                     "17_EXPERIMENTAL_POLICIES_V4.md", "políticas experimentales v4"))

    # focal event sample 16:15-16:25
    events_src = READ / "V4_FULL_EVENTS.csv"
    focal = ITER_DIR / "07_PHASE_4_EVENTS_FOCAL.csv"
    kept = 0
    with events_src.open(encoding="utf-8", newline="") as src, focal.open(
            "w", encoding="utf-8", newline="") as dst:
        reader = csv.reader(src)
        writer = csv.writer(dst)
        writer.writerow(next(reader))
        for row in reader:
            if len(row) > 1 and "16:15:00.000" <= row[1] <= "16:25:00.000":
                writer.writerow(row)
                kept += 1
    files.append({
        "zip_path": f"{ITER_NAME}/07_PHASE_4_EVENTS_FOCAL.csv",
        "original_path": str(events_src.relative_to(ROOT)),
        "size": focal.stat().st_size,
        "sha256": sha256(focal),
        "reason": f"muestra focal 16:15-16:25 ({kept} eventos); log completo en el proyecto",
    })
    note = ITER_DIR / "07b_EVENTS_NOTE.txt"
    note.write_text(
        "Muestra focal 16:15-16:25. El log completo no se copia por tamaño.\n"
        f"Ruta completa: {events_src.relative_to(ROOT)}\n"
        f"Líneas completas: {sum(1 for _ in events_src.open(encoding='utf-8'))}\n"
        f"SHA-256 completo: {sha256(events_src)}\n"
        f"Eventos en la muestra: {kept}\n",
        encoding="utf-8")
    files.append({
        "zip_path": f"{ITER_NAME}/07b_EVENTS_NOTE.txt",
        "original_path": str(events_src.relative_to(ROOT)),
        "size": note.stat().st_size,
        "sha256": sha256(note),
        "reason": "índice y hash del log completo",
    })

    full = json.loads((READ / "V4_FULL_SUMMARY.json").read_text(encoding="utf-8"))
    classic = json.loads((READ / "V4_CLASSIC_SUMMARY.json").read_text(encoding="utf-8"))
    audit = json.loads((REG / "PHASE_4_SUMMARY.json").read_text(encoding="utf-8"))
    det = json.loads((REG / "PHASE_4_DETERMINISM.json").read_text(encoding="utf-8"))

    iteration_manifest = {
        "iteration_id": ITER_NAME,
        "date": datetime.now().isoformat(timespec="seconds"),
        "objective": (
            "Aplicar Q-AUT funcional, Q-3-50 inclusivo y GAP sin zona muerta; "
            "releer 16:15-17:29 y auditar las generaciones"
        ),
        "reader": "blind_reader_v4_functional_autonomy.py",
        "reader_sha256": sha256(READ / "blind_reader_v4_functional_autonomy.py"),
        "decisions": {
            "Q_AUT": "B solo después de A_CONFIRMED",
            "Q_3_50": "retroceso <= 50% conserva 3; 50% exacto válido",
            "GAP": "toda apertura no plana prohíbe 2 y entra en gap",
        },
        "counts": {
            "v3_full": 51,
            "v4_classic": classic["generations"],
            "v4_full": full["generations"],
            "v4_invalid": full["invalid_generations"],
            "v4_three_without_two": full["three_without_two"],
            "v4_primary": audit["counts"].get("L1:VALID_PRIMARY", 0),
            "v4_gap": audit["counts"].get("L1:INTEGRATED_IN_LARGER_MODULE", 0),
            "v4_pending": audit["counts"].get("L1:VALID_PRIMARY_PENDING", 0),
            "l2_generations": audit["L2_generations"],
            "l2_unique": audit["counts"].get("L2:VALID_PRIMARY", 0)
            + audit["counts"].get("L2:VALID_PRIMARY_PENDING", 0),
            "l2_duplicates": audit["counts"].get("L2:INTEGRATED_IN_LARGER_MODULE", 0),
            "unique_total": full["generations"]
            + audit["counts"].get("L2:VALID_PRIMARY", 0)
            + audit["counts"].get("L2:VALID_PRIMARY_PENDING", 0),
            "ownership_errors": audit["errors_total"],
            "removed_by_A": 51 - classic["generations"],
            "added_by_gap": full["generations"] - classic["generations"],
        },
        "end_reasons": full["end_reasons"],
        "determinism": det,
        "full_trace": {
            "path": str((READ / "V4_FULL_TRACE.jsonl").relative_to(ROOT)),
            "sha256": sha256(READ / "V4_FULL_TRACE.jsonl"),
            "lines": sum(1 for _ in (READ / "V4_FULL_TRACE.jsonl").open(encoding="utf-8")),
        },
        "open_question": "Q-AUT-REF (1 vs módulo 1+2)",
        "originals_modified": False,
        "tree_modified": False,
        "engine_modified": False,
        "golden_modified": False,
        "tree_frozen": False,
        "generations_approved": False,
        "recommendation": "NEEDS_EXPERT_DECISION",
    }
    man_path = ITER_DIR / "15_ITERATION_MANIFEST.json"
    man_path.write_text(json.dumps(iteration_manifest, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
    files.append({
        "zip_path": f"{ITER_NAME}/15_ITERATION_MANIFEST.json",
        "original_path": str(man_path.relative_to(ROOT)),
        "size": man_path.stat().st_size,
        "sha256": sha256(man_path),
        "reason": "manifiesto de la iteración",
    })

    package_manifest = {
        "iteration_id": ITER_NAME,
        "date": datetime.now().isoformat(timespec="seconds"),
        "objective": iteration_manifest["objective"],
        "files": files,
        "originals_modified": False,
        "tree_modified": False,
        "engine_modified": False,
        "golden_modified": False,
        "note": "PACKAGE_MANIFEST.json no se lista a sí mismo; su hash está en SHA256SUMS.txt.",
    }
    (ITER_DIR / "PACKAGE_MANIFEST.json").write_text(
        json.dumps(package_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    sums = []
    for p in sorted(ITER_DIR.iterdir(), key=lambda x: x.name):
        if p.name == "SHA256SUMS.txt":
            continue
        sums.append(f"{sha256(p)}  {p.name}")
    (ITER_DIR / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(ITER_DIR.iterdir(), key=lambda x: x.name):
            zf.write(p, arcname=f"{ITER_NAME}/{p.name}")

    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        names = zf.namelist()
        with zf.open(f"{ITER_NAME}/SHA256SUMS.txt") as fh:
            index = {}
            for line in fh.read().decode().splitlines():
                h, name = line.split("  ", 1)
                index[name] = h
        checked = 0
        failures = []
        for name in names:
            base = name.split("/")[-1]
            if base == "SHA256SUMS.txt":
                continue
            got = hashlib.sha256(zf.read(name)).hexdigest().upper()
            if index.get(base) != got:
                failures.append(base)
            checked += 1

    result = {
        "iteration_id": ITER_NAME,
        "flat_folder": str(ITER_DIR.relative_to(ROOT)),
        "zip_path": str(ZIP_PATH.relative_to(ROOT)),
        "zip_size_bytes": ZIP_PATH.stat().st_size,
        "zip_sha256": sha256(ZIP_PATH),
        "zip_members": len(names),
        "checked_members": checked,
        "hash_failures": failures,
        "integrity_ok": not failures,
    }
    (DELIVERY_ROOT / "ITERATION_04_DELIVERY.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
