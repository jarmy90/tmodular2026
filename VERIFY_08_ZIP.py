"""Verify ITERACION_08_DIRECT_AUT zip and report integrity."""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path("C:/Users/profesor/tm/Teoria Modular")
ZIP_PATH = ROOT / "TM_ENTREGAS_ITERACION" / "TM_ITERATION_08_REVIEW.zip"
DIR_NAME = "ITERACION_08_DIRECT_AUT_20261030_1850"
PACK_DIR = ROOT / "TM_ENTREGAS_ITERACION" / DIR_NAME


def sha(path: Path) -> str:
    _h = hashlib.sha256()
    with path.open("rb") as _fh:
        for _chunk in iter(lambda: _fh.read(1 << 20), b""):
            _h.update(_chunk)
    return _h.hexdigest()


def main() -> int:
    report = {
        "zip_exists": False,
        "zip_size": None,
        "zip_sha256": None,
        "pack_dir_exists": False,
        "pack_dir_members_on_disk": None,
        "zip_arcnames": None,
        "zip_member_count": None,
        "integrity_checks": [],
        "failures": [],
    }

    if not ZIP_PATH.is_file():
        report["failures"].append("zip missing")
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 1

    report["zip_exists"] = True
    report["zip_size"] = ZIP_PATH.stat().st_size
    report["zip_sha256"] = sha(ZIP_PATH)

    if PACK_DIR.is_dir():
        report["pack_dir_exists"] = True
        report["pack_dir_members_on_disk"] = sorted(
            p.name for p in PACK_DIR.iterdir() if p.is_file()
        )

    with zipfile.ZipFile(ZIP_PATH) as zf:
        arcnames = zf.namelist()
        report["zip_arcnames"] = arcnames
        report["zip_member_count"] = len(arcnames)
        disk_members = report["pack_dir_members_on_disk"] or []

        all_pass = True
        for name in disk_members:
            arcname = f"{DIR_NAME}/{name}"
            if arcname not in arcnames:
                report["failures"].append(f"missing arc {arcname}")
                all_pass = False
                continue
            disk_hash = sha(PACK_DIR / name)
            zip_hash = hashlib.sha256(zf.read(arcname)).hexdigest()
            if disk_hash != zip_hash:
                report["failures"].append(f"hash mismatch {name}")
                all_pass = False
            else:
                report["integrity_checks"].append(f"ok {name}")

        if sorted(disk_members) != sorted(
            a for a in arcnames if a.startswith(DIR_NAME + "/")
        ):
            report["failures"].append("zip member set differs from disk")

    report["integrity"] = "PASS" if all_pass and not report["failures"] else "FAIL"
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["integrity"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
