#!/usr/bin/env python3
"""ITERACION 16 — guardia de identidad del interprete de referencia.

Todas las suites deben ejecutarse contra el mismo archivo:
  tm_reference_interpreter_v1_direct_aut.py

Entorno reconocido:
  TM_READER_MODULE         nombre del modulo (debe ser el candidato)
  TM_REFERENCE_ENGINE_DIR  carpeta del motor (arbol de trabajo o ZIP extraido)
  TM_READER_SHA256         hash exigido (lo fija el agregador)
  TM_READER_CORE_VERSION   version exigida (la fija el agregador)

La funcion aborta la suite si el modulo importado no es el candidato, si no
declara CORE_VERSION o si el SHA-256 no coincide con el exigido.
"""
from __future__ import annotations

import hashlib
import importlib
import os
import sys
from pathlib import Path

EXPECTED_MODULE = "tm_reference_interpreter_v1_direct_aut"
HERE = Path(__file__).resolve().parent


def engine_dir() -> Path:
    env = os.environ.get("TM_REFERENCE_ENGINE_DIR")
    if env:
        path = Path(env).resolve()
        if path.is_dir():
            return path
        raise SystemExit(f"READER_DIR_MISSING {path}")
    for candidate in (HERE.parent / "05_REFERENCE_ENGINE",
                      HERE.parent / "02_ENGINE"):
        if candidate.is_dir():
            return candidate.resolve()
    raise SystemExit("READER_DIR_UNRESOLVED")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def verify(name: str | None = None):
    name = name or os.environ.get("TM_READER_MODULE", EXPECTED_MODULE)
    if name != EXPECTED_MODULE:
        raise SystemExit(f"READER_NOT_REFERENCE_MODULE {name}")
    folder = engine_dir()
    if str(folder) not in sys.path:
        sys.path.insert(0, str(folder))
    module = importlib.import_module(name)
    path = Path(module.__file__).resolve()
    digest = sha256_file(path)
    expected_sha = (os.environ.get("TM_READER_SHA256") or "").upper()
    if expected_sha and digest != expected_sha:
        raise SystemExit(
            f"READER_SHA_MISMATCH {digest} != {expected_sha} ({path})")
    version = getattr(module, "CORE_VERSION", "")
    if not version:
        raise SystemExit(f"READER_WITHOUT_CORE_VERSION {path}")
    expected_version = os.environ.get("TM_READER_CORE_VERSION")
    if expected_version and version != expected_version:
        raise SystemExit(
            f"READER_VERSION_MISMATCH {version} != {expected_version} ({path})")
    print(f"READER module={name} path={path} sha256={digest} "
          f"core_version={version}")
    return module
