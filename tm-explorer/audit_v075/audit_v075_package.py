from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DEST = Path(
    r"C:\Users\profesor\OpenBot\Agents\agent-ece275c8-821a-43f3-b05f-6cdf123b7ade\deliverables_v075_audit2"
)
DATOS = ROOT / "datos"

FILES = {
    "motor/TM_CORE_PYTHON_v075_STREAMING.py": ROOT / "python" / "TM_CORE_PYTHON_v075_STREAMING.py",
    "motor/TM_CORE_PYTHON_v075_TESTS.py": ROOT / "python" / "TM_CORE_PYTHON_v075_TESTS.py",
    "motor/TM_CORE_PYTHON_v075_REPORTS.py": ROOT / "python" / "TM_CORE_PYTHON_v075_REPORTS.py",
    "tests/audit_v075_tests.py": ROOT / "audit_v075" / "audit_v075_tests.py",
    "datos/feed_maestro_1615_1730.csv": Path(
        r"C:\Users\profesor\OpenBot\Shared\Transfers\fb8c2a5d-d62c-48d0-8120-bae2016283c4\TM_TICKFEED_1615_1730.csv"
    ),
    "datos/feed_anterior_1620_1700.csv": Path(
        r"C:\Users\profesor\OpenBot\Shared\Transfers\9c9276ac-5e0f-4c1a-8edb-22e5466079b0\TM_TICKFEED_20261016_v010_USTEC_12345_USTEC_DAY16.csv"
    ),
    "datos/lecturas_confirmadas_v002.txt": Path(
        r"C:\Users\profesor\OpenBot\Shared\Transfers\fb8c2a5d-d62c-48d0-8120-bae2016283c4\TM_LECTURAS_CONFIRMADAS_16OCT_1615_1730_v002.txt"
    ),
    "datos/arbol_canonico_v2_14.md": Path(
        r"C:\Users\profesor\OpenBot\Shared\Transfers\fb8c2a5d-d62c-48d0-8120-bae2016283c4\TM_ARBOL_MAESTRO_CANONICO_COMPLETO_v2_14.md"
    ),
    "README.md": ROOT / "audit_v075" / "README.md",
    "AUDITORIA.md": ROOT / "audit_v075" / "AUDITORIA.md",
    "COMANDOS.md": ROOT / "audit_v075" / "COMANDOS.md",
}

AUDIT_SCRIPTS = [
    "audit_v075_common.py",
    "audit_v075_build.py",
    "audit_v075_prefix_run.py",
    "audit_v075_prefix_shard.py",
    "audit_v075_prefix_matrix.py",
    "audit_v075_prefix_finalize.py",
    "audit_v075_finalize.py",
    "audit_v075_tests.py",
    "audit_v075_package.py",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_file(source: Path, destination: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def build_package(dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    for relative, source in FILES.items():
        copy_file(source, dest / relative)
    for name in AUDIT_SCRIPTS:
        source = ROOT / "audit_v075" / name
        if source.exists():
            copy_file(source, dest / "audit_v075" / name)
    reports_source = ROOT / "out_v075_audit2"
    reports_dest = dest / "out_v075_audit2"
    reports_dest.mkdir(parents=True, exist_ok=True)
    for source in sorted(reports_source.iterdir()):
        if source.is_file() and source.name != "__pycache__":
            shutil.copy2(source, reports_dest / source.name)
    (dest / "requirements.txt").write_text("pytest==9.1.1\n", encoding="utf-8")
    (dest / "VERSION.txt").write_text(
        "TM_CORE_PYTHON v0.7.5\naudit=v075_audit2\n"
        "python=3.12.10\npytest=9.1.1\n",
        encoding="utf-8",
    )

    manifest = []
    hashes = []
    for path in sorted(dest.rglob("*")):
        if not path.is_file() or path.name in {"HASHES.sha256", "MANIFEST.json"}:
            continue
        relative = path.relative_to(dest).as_posix()
        digest = sha256(path)
        manifest.append({"path": relative, "bytes": path.stat().st_size, "sha256": digest})
        hashes.append(f"{digest}  {relative}")
    (dest / "HASHES.sha256").write_text("\n".join(hashes) + "\n", encoding="utf-8")
    (dest / "MANIFEST.json").write_text(
        json.dumps(
            {
                "audit": "v075_audit2",
                "motor_version": "0.7.5",
                "files": manifest,
                "file_count": len(manifest),
                "total_bytes": sum(item["bytes"] for item in manifest),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def build_zip(dest: Path, zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(dest.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(dest).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(2026, 10, 27, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100644 & 0xFFFF) << 16
            with path.open("rb") as handle:
                archive.writestr(info, handle.read())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dest", type=Path, default=DEFAULT_DEST)
    args = parser.parse_args()
    dest = args.dest.resolve()
    build_package(dest)
    zip_path = dest.parent / f"{dest.name}.zip"
    build_zip(dest, zip_path)
    print(f"package={dest}")
    print(f"zip={zip_path} bytes={zip_path.stat().st_size}")
    print(f"files={sum(1 for p in dest.rglob('*') if p.is_file())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
