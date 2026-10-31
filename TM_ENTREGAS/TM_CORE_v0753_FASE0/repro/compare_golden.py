"""Read-only comparison. It consumes CORE_RAW_OUTPUT and never mutates it."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "out" / "CORE_RAW_OUTPUT.json"
OUT = ROOT / "out" / "GOLDEN_COMPARISON.json"

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    raw_hash_before = sha(RAW)
    data = json.loads(RAW.read_text(encoding="utf-8"))
    events = data["local_events"]
    def has(bar: str, function: str, direction: str | None = None) -> bool:
        return any(e.get("bar_time") == bar and e.get("function") == function and
                   (direction is None or e.get("direction") == direction) for e in events)
    checks = [
        ("16:19 local 1 bajista", has("16:19", "1", "DOWN")),
        ("16:20 2 bajista", has("16:20", "2", "DOWN")),
        ("16:21 3 bajista", has("16:21", "3", "DOWN")),
        ("16:22 A alcista", has("16:22", "A", "UP")),
        ("16:22 AUT alcista", has("16:22", "AUT", "UP")),
        ("16:23 A bajista", has("16:23", "A", "DOWN")),
        ("16:23 AUT alcista según v003", has("16:23", "AUT", "UP")),
        ("16:23 AUT bajista", has("16:23", "AUT", "DOWN")),
        ("16:24 A alcista y B/AUT bajistas", has("16:24", "A", "UP") and has("16:24", "B", "DOWN") and has("16:24", "AUT", "DOWN")),
    ]
    expected = [name for name, ok in checks if not ok]
    seq_events = [e for e in data["events"] if e.get("kind") == "LOCAL_FUNCTION"]
    first_23_aut = next((e for e in seq_events if e.get("bar_time") == "16:23" and e.get("function") == "AUT"), None)
    upward_auts = [e for e in events if e.get("bar_time") == "16:23" and e.get("function") == "AUT" and e.get("direction") == "UP"]
    divergence = None
    if not upward_auts:
        a_leg = next((e for e in events if e.get("bar_time") == "16:23" and e.get("function") == "A" and e.get("direction") == "DOWN"), None)
        b_leg = next((e for e in events if e.get("bar_time") == "16:23" and e.get("function") == "B" and e.get("direction") == "UP"), None)
        a_size = abs(a_leg["extreme"] - a_leg["origin"]) if a_leg else None
        b_size = abs(b_leg["extreme"] - b_leg["origin"]) if b_leg else None
        limit = ((127 * a_size) // 100 + 25) if a_size is not None else None
        divergence = {
            "classification": "REGLA_VIGENTE_VS_GOLDEN_INCOMPATIBLE",
            "golden_reference_sequence_id": 1879,
            "golden_reference_is": "máximo B, no primer cruce",
            "first_causal_crossing_feed_sequence_id": 1876,
            "prior_state": "A bajista confirmada; B alcista supera 100% de A, pero no 127% + 0,25",
            "output_obtained": {"A_size_price_units": a_size, "B_size_price_units": b_size,
                                "required_AUT_excess_price_units": limit, "aut_emitted": False},
            "rule_status": "La regla universal B Grande exige superar 127% + 0,25; v003 afirma AUT al superar solo el inicio de A. No se modifica el golden.",
        }
    result = {
        "artifact": "GOLDEN_COMPARISON", "input": "out/CORE_RAW_OUTPUT.json",
        "raw_sha256_before": raw_hash_before,
        "checks": [{"expectation": n, "passed": ok} for n, ok in checks],
        "passed": sum(ok for _, ok in checks), "total": len(checks),
        "first_failure": expected[0] if expected else None,
        "first_16_23_aut_core_event": first_23_aut,
        "rule_conflict": divergence,
        "raw_sha256_after": sha(RAW), "raw_unchanged": raw_hash_before == sha(RAW),
        "status": "LECTURA_NO_REPRODUCIDA" if expected or divergence else "COMPARACION_COMPLETA",
        "note": "Comparación posterior de solo lectura; no escribe ni adapta el núcleo ni el golden.",
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not expected and not divergence and result["raw_unchanged"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
