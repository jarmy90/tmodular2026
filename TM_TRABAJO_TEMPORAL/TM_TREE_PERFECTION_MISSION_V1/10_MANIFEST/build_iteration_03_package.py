"""Build the flat ITERACION_03 delivery and its verified review ZIP."""
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
DELIVERY_ROOT = ROOT / "TM_ENTREGAS_ITERACION"

STAMP = datetime.now().strftime("%Y%m%d_%H%M")
ITER_NAME = f"ITERACION_03_{STAMP}"
ITER_DIR = DELIVERY_ROOT / ITER_NAME
ZIP_PATH = DELIVERY_ROOT / "TM_ITERATION_03_REVIEW.zip"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def copy(src: Path, name: str, reason: str) -> dict:
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
    files.append(copy(MISSION / "09_REPORTS/CHECKPOINT_3_REPORT.md",
                      "01_CHECKPOINT_3_REPORT.md", "checkpoint y resumen"))
    files.append(copy(MISSION / "04_EXPERT_QUESTIONS/PHASE_3_QUESTIONS.md",
                      "02_PHASE_3_QUESTIONS.md", "preguntas expertas"))
    files.append(copy(READ / "blind_reader_v3_owned_states.py",
                      "03_blind_reader_v3_owned_states.py", "lector experimental"))
    files.append(copy(READ / "V3_FULL_GENERATIONS.csv",
                      "04_PHASE_3_GENERATIONS_L1.csv", "generaciones L1"))
    files.append(copy(READ / "V3_L2_1619_1624_GENERATIONS.csv",
                      "05_PHASE_3_GENERATIONS_L2.csv", "generaciones L2"))
    files.append(copy(REG / "PHASE_3_L1_L2_MAP.csv",
                      "07_PHASE_3_L1_L2_MAP.csv", "mapa L1/L2"))
    files.append(copy(MISSION / "02_MOVEMENT_ANALYSIS/PHASE_3_DIVERGENCES.csv",
                      "08_PHASE_3_DIVERGENCES.csv", "divergencias"))
    files.append(copy(MISSION / "05_TREE_REVISIONS/EXPERIMENTAL_POLICIES_V3.md",
                      "09_EXPERIMENTAL_POLICIES_V3.md", "políticas experimentales"))
    files.append(copy(REG / "PHASE_3_DETERMINISM.json",
                      "10_PHASE_3_DETERMINISM.json", "regresión y determinismo"))
    files.append(copy(REG / "PHASE_3_SUMMARY.json",
                      "11_PHASE_3_SUMMARY.json", "resumen de auditoría"))
    files.append(copy(REG / "PHASE_3_GENERATION_AUDIT.csv",
                      "12_PHASE_3_GENERATION_AUDIT.csv", "auditoría por generación"))

    # focal event sample (16:19-16:25), not the full event log
    events_src = READ / "V3_FULL_EVENTS.csv"
    focal = ITER_DIR / "06_PHASE_3_EVENTS_FOCAL.csv"
    kept = 0
    with events_src.open(encoding="utf-8", newline="") as src, focal.open(
            "w", encoding="utf-8", newline="") as dst:
        reader = csv.reader(src)
        writer = csv.writer(dst)
        header = next(reader)
        writer.writerow(header)
        for row in reader:
            if len(row) > 3 and "16:19:00.000" <= row[1] <= "16:25:00.000":
                writer.writerow(row)
                kept += 1
    files.append({
        "zip_path": f"{ITER_NAME}/06_PHASE_3_EVENTS_FOCAL.csv",
        "original_path": str(events_src.relative_to(ROOT)),
        "size": focal.stat().st_size,
        "sha256": sha256(focal),
        "reason": f"muestra focal 16:19-16:25 ({kept} eventos); el log completo queda en el proyecto",
    })
    note = ITER_DIR / "06b_EVENTS_NOTE.txt"
    note.write_text(
        "Muestra focal 16:19-16:25. El log completo no se copia por tamaño.\n"
        f"Ruta completa: {events_src.relative_to(ROOT)}\n"
        f"Líneas completas: {sum(1 for _ in events_src.open(encoding='utf-8'))}\n"
        f"SHA-256 completo: {sha256(events_src)}\n"
        f"Eventos en la muestra: {kept}\n",
        encoding="utf-8")
    files.append({
        "zip_path": f"{ITER_NAME}/06b_EVENTS_NOTE.txt",
        "original_path": str(events_src.relative_to(ROOT)),
        "size": note.stat().st_size,
        "sha256": sha256(note),
        "reason": "índice y hash del log completo de eventos",
    })

    full_summary = json.loads((READ / "V3_FULL_SUMMARY.json").read_text(encoding="utf-8"))
    audit = json.loads((REG / "PHASE_3_SUMMARY.json").read_text(encoding="utf-8"))
    determinism = json.loads((REG / "PHASE_3_DETERMINISM.json").read_text(encoding="utf-8"))

    iteration_manifest = {
        "iteration_id": ITER_NAME,
        "date": datetime.now().isoformat(timespec="seconds"),
        "objective": "Corregir propiedad de estados, invalidar 3 sin 2 y releer 16:15-17:29",
        "reader": "blind_reader_v3_owned_states.py",
        "reader_sha256": sha256(READ / "blind_reader_v3_owned_states.py"),
        "counts": {
            "L1_full_generations": full_summary["generations"],
            "L1_invalid": full_summary["invalid_generations"],
            "L1_three_without_two": full_summary["three_without_two"],
            "L1_primary": audit["counts"].get("L1:VALID_PRIMARY", 0),
            "L1_gap_integrated": audit["counts"].get("L1:INTEGRATED_IN_LARGER_MODULE", 0),
            "L1_pending": audit["counts"].get("L1:VALID_PRIMARY_PENDING", 0),
            "L2_generations": audit["L2_generations"],
            "L2_unique": audit["counts"].get("L2:VALID_PRIMARY", 0),
            "L2_duplicates": audit["counts"].get("L2:INTEGRATED_IN_LARGER_MODULE", 0),
            "unique_total": full_summary["generations"] + audit["counts"].get("L2:VALID_PRIMARY", 0),
            "ownership_errors": audit["errors_total"],
        },
        "determinism": determinism,
        "full_trace": {
            "path": str((READ / "V3_FULL_TRACE.jsonl").relative_to(ROOT)),
            "sha256": sha256(READ / "V3_FULL_TRACE.jsonl"),
            "lines": sum(1 for _ in (READ / "V3_FULL_TRACE.jsonl").open(encoding="utf-8")),
        },
        "originals_modified": False,
        "tree_modified": False,
        "engine_modified": False,
        "golden_modified": False,
        "tree_frozen": False,
        "generations_approved": False,
        "recommendation": "NEEDS_EXPERT_DECISION",
    }
    man_path = ITER_DIR / "13_ITERATION_MANIFEST.json"
    man_path.write_text(json.dumps(iteration_manifest, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
    files.append({
        "zip_path": f"{ITER_NAME}/13_ITERATION_MANIFEST.json",
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
    pkg_path = ITER_DIR / "PACKAGE_MANIFEST.json"
    pkg_path.write_text(json.dumps(package_manifest, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")

    # SHA256SUMS of every flat file except itself
    sums = []
    for p in sorted(ITER_DIR.iterdir(), key=lambda x: x.name):
        if p.name == "SHA256SUMS.txt":
            continue
        sums.append(f"{sha256(p)}  {p.name}")
    (ITER_DIR / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")

    # ZIP with the flat folder
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(ITER_DIR.iterdir(), key=lambda x: x.name):
            zf.write(p, arcname=f"{ITER_NAME}/{p.name}")

    # verify all members against SHA256SUMS inside the ZIP
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
            data = zf.read(name)
            got = hashlib.sha256(data).hexdigest().upper()
            expected = index.get(base)
            if expected is None or got != expected:
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
    (DELIVERY_ROOT / "ITERATION_03_DELIVERY.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
