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
        ("16:23 AUT alcista en secuencia estructural v003 1879", any(
            e.get("kind") == "LOCAL_FUNCTION" and e.get("function") == "AUT" and
            e.get("bar_time") == "16:23" and e.get("sequence_id") == 1879 for e in data["events"])),
        ("16:23 AUT bajista", has("16:23", "AUT", "DOWN")),
        ("16:24 A/B/AUT bajista", has("16:24", "A", "DOWN") and has("16:24", "B", "DOWN") and has("16:24", "AUT", "DOWN")),
    ]
    expected = [name for name, ok in checks if not ok]
    seq_events = [e for e in data["events"] if e.get("kind") == "LOCAL_FUNCTION"]
    first_23_aut = next((e for e in seq_events if e.get("bar_time") == "16:23" and e.get("function") == "AUT"), None)
    actual_auts_16_23 = [e for e in seq_events if e.get("bar_time") == "16:23" and e.get("function") == "AUT" and e.get("direction") == 1]
    first_tick_divergence = None
    if actual_auts_16_23 and not any(e.get("sequence_id") == 1879 for e in actual_auts_16_23):
        first_tick_divergence = {
            "expected_sequence_id": 1879,
            "actual_first_aut_sequence_id": actual_auts_16_23[0].get("sequence_id"),
            "prior_state_expected": "A bajista sigue desarrollándose hasta el B alcista que alcanza 29852,6",
            "output_obtained": actual_auts_16_23[0],
            "rule_status": "criterio causal exacto de confirmación local AUT pendiente de formalización; no se ajusta el golden"
        }
    result = {
        "artifact": "GOLDEN_COMPARISON",
        "input": "out/CORE_RAW_OUTPUT.json",
        "raw_sha256_before": raw_hash_before,
        "checks": [{"expectation": n, "passed": ok} for n, ok in checks],
        "passed": sum(ok for _, ok in checks), "total": len(checks),
        "first_failure": expected[0] if expected else None,
        "first_16_23_aut_core_event": first_23_aut,
        "first_tick_divergence": first_tick_divergence,
        "raw_sha256_after": sha(RAW),
        "raw_unchanged": raw_hash_before == sha(RAW),
        "status": "LECTURA_NO_REPRODUCIDA" if expected or first_tick_divergence else "COMPARACION_COMPLETA",
        "note": "Comparación posterior de solo lectura; no escribe ni adapta el núcleo."
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not expected and not first_tick_divergence and result["raw_unchanged"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
