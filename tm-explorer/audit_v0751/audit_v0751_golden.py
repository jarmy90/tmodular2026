from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

import TM_CORE_PYTHON_v0751_STREAMING as core


FEED = Path(
    r"C:\Users\profesor\OpenBot\Shared\Transfers\fb8c2a5d-d62c-48d0-8120-bae2016283c4\TM_TICKFEED_1615_1730.csv"
)
GOLDEN = ROOT / "data" / "lecturas_confirmadas_v003.txt"


EXPECTED_LOCAL = [
    ("16:19", "1", -1, 29850.0, 29842.5),
    ("16:20", "2", -1, 29844.8, 29832.5),
    ("16:21", "3", -1, 29835.0, 29830.3),
    ("16:22", "A", 1, 29830.3, 29850.8),
    ("16:22", "AUT", 1, 29850.0, 29850.8),
    ("16:22", "1", 1, 29830.3, 29850.8),
    ("16:23", "A", -1, 29850.8, 29842.8),
    ("16:23", "B", 1, 29842.8, 29852.6),
    ("16:23", "AUT", 1, 29850.8, 29852.6),
    ("16:23", "AUT", -1, 29852.6, 29837.3),
    ("16:23", "1", -1, 29852.6, 29837.3),
    ("16:24", "1", -1, 29852.6, 29833.3),
    ("16:24", "A", 1, 29833.3, 29840.6),
    ("16:24", "B", -1, 29840.6, 29828.1),
    ("16:24", "AUT", -1, 29833.3, 29828.1),
]


def _bar(engine: core.Engine, name: str) -> core.Bar:
    for bar in engine.bars.values():
        if bar.name == name:
            return bar
    raise AssertionError(f"barra ausente: {name}")


def _price(engine: core.Engine, value: int) -> float:
    return value / 100.0


def _record(checks: list[dict], name: str, ok: bool, detail: str) -> None:
    checks.append({"check": name, "ok": bool(ok), "detail": detail})


def evaluate(engine: core.Engine) -> list[dict]:
    checks: list[dict] = []
    if not GOLDEN.exists():
        raise AssertionError(f"golden ausente: {GOLDEN}")
    text = GOLDEN.read_text(encoding="cp1252", errors="replace")
    _record(
        checks,
        "v003_presente",
        "v0.03" in text
        and "16:19 = 1 bajista" in text
        and "16:22 = AUT alcista confirmado" in text
        and "16:24:49.819" in text,
        "golden v003 leido y contiene los hitos locales",
    )

    b1515 = _bar(engine, "16:15")
    b1516 = _bar(engine, "16:16")
    _record(
        checks,
        "16:15_modulo",
        b1515.high.price == 2987700
        and b1515.low.price == 2986080
        and b1515.high.price - b1515.low.price == 1620,
        f"OHLC 16:15 {core.price_s(b1515.open.price)}/{core.price_s(b1515.high.price)}/"
        f"{core.price_s(b1515.low.price)}/{core.price_s(b1515.last.price)}",
    )
    _record(
        checks,
        "16:16_plano_no_2",
        b1516.gap == 10
        and b1516.open.price == b1516.high.price
        and (b1516.high.price - b1516.low.price) < 1620,
        f"gap={b1516.gap} rango={b1516.high.price - b1516.low.price}",
    )

    r1 = next((r for r in engine.readings if r.reading_id == "R0001"), None)
    _record(
        checks,
        "16:15_16:18_estructura",
        r1 is not None
        and r1.module_origin == 2987700
        and r1.module_extreme == 2984850
        and r1.a_origin == 2984850
        and r1.a_end == 2985760
        and r1.tt_target == 2982910
        and r1.direction < 0,
        "R0001 modulo 29877.0->29848.5; A 29848.5->29857.6; TT 29829.1",
    )
    aut_1618 = [
        e
        for e in engine.events
        if e["function"] == "AUT"
        and e["direction"] < 0
        and e["bar_time"] == "16:18"
        and e["reading_id"] == "R0001"
    ]
    _record(
        checks,
        "16:18_AUT_bajista",
        bool(aut_1618),
        f"AUT bajista 16:18: {len(aut_1618)} evento(s)",
    )
    b1518 = _bar(engine, "16:18")
    _record(
        checks,
        "16:18_TT_pendiente",
        r1 is not None
        and r1.tt_target == 2982910
        and r1.tt_time > 0
        and r1.tt_time > b1518.last.time_ms,
        f"TT 29829.1 alcanzado despues de 16:18: {core.ms_to_text(r1.tt_time) if r1 and r1.tt_time else 'pendiente'}",
    )

    actual = [
        (
            e["bar_time"],
            e["function"],
            -1 if e["direction"] == "DOWN" else 1,
            _price(engine, e["origin"]),
            _price(engine, e["extreme"]),
        )
        for e in engine.local_events[: len(EXPECTED_LOCAL)]
    ]
    for index, (expected, got) in enumerate(zip(EXPECTED_LOCAL, actual), 1):
        _record(
            checks,
            f"local_{index:02d}_{expected[1]}_{expected[0]}",
            expected == got,
            f"esperado={expected} obtenido={got}",
        )
    _record(
        checks,
        "local_sin_faltantes",
        len(engine.local_events) >= len(EXPECTED_LOCAL),
        f"eventos locales={len(engine.local_events)} esperados>={len(EXPECTED_LOCAL)}",
    )
    return checks


def main() -> int:
    points, bars = core.load_feed(FEED)
    engine = core.run_engine(points, bars)
    checks = evaluate(engine)
    passed = sum(1 for check in checks if check["ok"])
    total = len(checks)
    out = ROOT / "out_v0751" / "golden_v003.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(
            {"passed": passed, "total": total, "checks": checks},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    for check in checks:
        print(f"{'PASS' if check['ok'] else 'FAIL'} {check['check']}: {check['detail']}")
    print(f"GOLDEN v003: {passed}/{total}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())


