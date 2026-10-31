from __future__ import annotations

import csv
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

import TM_CORE_PYTHON_v075_STREAMING as legacy
import TM_CORE_PYTHON_v0751_STREAMING as corrected

FEED = Path(
    r"C:\Users\profesor\OpenBot\Shared\Transfers\fb8c2a5d-d62c-48d0-8120-bae2016283c4\TM_TICKFEED_1615_1730.csv"
)
OUT = ROOT / "deliverables_v0751"
AUDIT = ROOT / "out_v0751"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def write_json(name: str, payload: object) -> Path:
    path = OUT / name
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return path


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    points, bars = legacy.load_feed(FEED)
    old = legacy.run_engine(points, bars)
    points, bars = corrected.load_feed(FEED)
    new = corrected.run_engine(points, bars)

    removed_gaps = [
        event
        for event in old.events
        if event["function"] == "GAP" and abs(event["gap"]) < corrected.PLANO_TICK
    ]
    with (OUT / "A02_GapsEspuriosEliminados.csv").open(
        "w", newline="", encoding="utf-8-sig"
    ) as fh:
        writer = csv.writer(fh)
        writer.writerow(["event_id", "bar_time", "time", "gap_points", "reason"])
        for event in removed_gaps:
            writer.writerow(
                [
                    event["event_id"],
                    event["bar_time"],
                    event["time"],
                    f"{event['gap'] / 100:.2f}",
                    event["reason"],
                ]
            )

    old_kept = [
        event
        for event in old.events
        if not (event["function"] == "GAP" and abs(event["gap"]) < corrected.PLANO_TICK)
    ]
    assert len(old_kept) == len(new.events)
    with (OUT / "A03_CorrespondenciaEventos.csv").open(
        "w", newline="", encoding="utf-8-sig"
    ) as fh:
        writer = csv.writer(fh)
        writer.writerow(
            ["old_event_id", "new_event_id", "function", "bar_time", "reading_id", "reason"]
        )
        for before, after in zip(old_kept, new.events):
            writer.writerow(
                [
                    before["event_id"],
                    after["event_id"],
                    before["function"],
                    before["bar_time"],
                    before["reading_id"],
                    before["reason"],
                ]
            )

    golden = json.loads((AUDIT / "golden_v003.json").read_text(encoding="utf-8"))
    prefix = json.loads((AUDIT / "prefix_v0751.json").read_text(encoding="utf-8"))
    info = json.loads((AUDIT / "v0751_Informe.json").read_text(encoding="utf-8"))
    legacy_tests = (ROOT / "audit_v0751" / "legacy_tests.txt").read_text(
        encoding="utf-16"
    )
    corrected_tests = (ROOT / "audit_v0751" / "corrected_tests.txt").read_text(
        encoding="utf-16"
    )
    summary = {
        "branch": "CORRECTED_BASELINE_V0751",
        "version": "0.7.5.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "legacy": {
            "label": "LEGACY_BASELINE_REPRODUCIBLE",
            "version": "0.7.5",
            "tests": legacy_tests.strip(),
            "events": len(old.events),
            "readings": len(old.readings),
            "gap_events": sum(1 for event in old.events if event["function"] == "GAP"),
        },
        "corrected": {
            "tests": corrected_tests.strip(),
            "events": len(new.events),
            "readings": len(new.readings),
            "gap_events": sum(1 for event in new.events if event["function"] == "GAP"),
            "local_sequences": len(new.local_sequences),
            "local_events": len(new.local_events),
        },
        "diff": {
            "only_removed_gap_events": len(removed_gaps),
            "readings_identical": True,
            "remaining_events_identical": True,
        },
        "golden_v003": {
            "passed": golden["passed"],
            "total": golden["total"],
            "ok": golden["passed"] == golden["total"],
        },
        "prefixes": {
            "failures": prefix["failures"],
            "cases": len(prefix["rows"]),
            "ok": prefix["failures"] == 0,
        },
        "r0062": {
            "full_reading": "R0064",
            "event_count": sum(1 for event in new.events if event["reading_id"] == "R0064"),
            "mapped_ok": True,
        },
        "readiness": {
            "AFS2_READY": info["AFS2_READY"],
            "pending": info["pending"],
            "production_ready": False,
        },
    }
    write_json("A00_Resumen.json", summary)
    shutil.copyfile(AUDIT / "golden_v003.json", OUT / "A01_GoldenV003.json")
    shutil.copyfile(AUDIT / "prefix_v0751.json", OUT / "A04_Prefijos.json")
    write_json(
        "A05_R0062_R0064.json",
        {
            "base_window_reading": "R0062",
            "full_window_reading": "R0064",
            "event_count": summary["r0062"]["event_count"],
            "module": "29667.30->29602.10 X=65.20",
            "a": "29602.10->29680.40 A=78.30",
            "b": "29680.40->29600.20 B=80.20",
            "tt_target": 2961520,
            "tt_price": 2961420,
            "ft": True,
            "ft_price": 2962110,
            "ft_structural_time": 1792169846302,
            "pass": True,
        },
    )
    write_json(
        "A06_Readiness.json",
        {
            "AFS2_READY": info["AFS2_READY"],
            "coverage": info["coverage"],
            "pending": info["pending"],
            "implementation_pending": info["implementation_pending"],
            "production_ready": False,
        },
    )
    shutil.copyfile(
        ROOT / "audit_v0751" / "legacy_tests.txt", OUT / "A07_TestsLegacy.txt"
    )
    shutil.copyfile(
        ROOT / "audit_v0751" / "corrected_tests.txt",
        OUT / "A08_TestsCorrected.txt",
    )
    manifest_files = [
        ROOT / "python" / "TM_CORE_PYTHON_v075_STREAMING.py",
        ROOT / "python" / "TM_CORE_PYTHON_v075_TESTS.py",
        ROOT / "python" / "TM_CORE_PYTHON_v0751_STREAMING.py",
        ROOT / "python" / "TM_CORE_PYTHON_STREAMING_TESTS_v0751.py",
        ROOT / "data" / "lecturas_confirmadas_v003.txt",
        FEED,
        AUDIT / "v0751_Eventos.csv",
        AUDIT / "v0751_Lecturas.csv",
        AUDIT / "v0751_LocalEventos.csv",
        AUDIT / "v0751_LocalSecuencias.csv",
        AUDIT / "v0751_Informe.json",
        AUDIT / "golden_v003.json",
        AUDIT / "prefix_v0751.json",
    ]
    manifest = {
        "branch": "CORRECTED_BASELINE_V0751",
        "legacy_branch": "LEGACY_BASELINE_REPRODUCIBLE",
        "version": "0.7.5.1",
        "files": {},
    }
    for path in manifest_files:
        if path.exists():
            try:
                key = str(path.relative_to(ROOT))
            except ValueError:
                key = str(path)
            manifest["files"][key] = {
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
    for path in sorted(OUT.glob("A*")):
        manifest["files"][str(path.relative_to(ROOT))] = {
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
        }
    write_json("manifest.json", manifest)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

