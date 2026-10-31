#!/usr/bin/env python3
"""Genera ITER19B_TIMELINE.csv: evidencia tick a tick de 16:25:50-16:26:15."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "05_REFERENCE_ENGINE"))
from tm_reader_guard import verify as _verify_reader  # noqa: E402
_verify_reader()

from tm_reference_interpreter_v1_direct_aut import load_ticks, FEED, _hhmm  # noqa: E402
from tm_reading_manager import TMReadingManager  # noqa: E402


def main() -> int:
    ticks = [t for t in load_ticks(FEED)
             if 16 * 60 + 15 <= t.bar % 1440 <= 16 * 60 + 32]
    mgr = TMReadingManager(ticks).run()
    by_seq = {t.seq: t for t in ticks}
    l2_events = [e for e in mgr.l2.reading.events if e["seq"] > 0]
    l1_events = [e for e in mgr.l1.reading.events if e["seq"] > 0]

    # Estado real en cada tick (no el estado final del lector).
    m2 = TMReadingManager(ticks)
    states = {}
    for t in ticks:
        m2.feed(t)
        if 2500 <= t.seq <= 2625:
            r2 = m2.l2.reading
            states[t.seq] = (r2.tt_status, r2.tt_extreme, r2.tt_extreme_status,
                             r2.ft_status, r2.ft_origin, r2.ft_extreme,
                             r2.ft_absorbed)

    rows = []
    for seq in range(2500, 2625):
        t = by_seq.get(seq)
        if t is None or seq not in states:
            continue
        hh = _hhmm(t.time_ms)
        if not ("16:25:40" <= hh <= "16:26:20"):
            continue
        ev2 = [f'{e["event"]}: {e["detail"]}' for e in l2_events if e["seq"] == seq]
        ev1 = [f'{e["event"]}: {e["detail"]}' for e in l1_events if e["seq"] == seq]
        (tt_status, tt_extreme, tt_status_x, ft_status, ft_origin,
         ft_extreme, ft_absorbed) = states[seq]
        r2 = type("S", (), {"tt_status": tt_status, "tt_extreme": tt_extreme,
                           "tt_extreme_status": tt_status_x, "ft_status": ft_status,
                           "ft_origin": ft_origin, "ft_extreme": ft_extreme,
                           "ft_absorbed": ft_absorbed})()
        rows.append({
            "sequence_id": seq, "time": hh, "price": t.price,
            "l2_events": " | ".join(ev2),
            "l1_events": " | ".join(ev1),
            "tt_status": r2.tt_status, "tt_extreme": r2.tt_extreme,
            "tt_extreme_status": r2.tt_extreme_status,
            "ft_status": r2.ft_status, "ft_origin": r2.ft_origin,
            "ft_extreme": r2.ft_extreme, "ft_absorbed": r2.ft_absorbed,
        })
    # Solo ticks con evento o cambio de estado relevante, mas los extremos.
    keep = []
    prev = None
    for r in rows:
        sig = (r["tt_status"], r["tt_extreme"], r["ft_status"],
               r["ft_origin"], r["ft_absorbed"])
        if r["l2_events"] or r["l1_events"] or sig != prev or \
                r["price"] in (2987060, 2987540):
            keep.append(r)
        prev = sig

    with (HERE / "ITER19B_TIMELINE.csv").open("w", newline="",
                                              encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(keep[0].keys()))
        w.writeheader()
        w.writerows(keep)
    for r in keep:
        print(f'{r["sequence_id"]:5d} {r["time"]} {r["price"]} '
              f'tt={r["tt_status"]}/{r["tt_extreme"]} '
              f'ft={r["ft_status"]}/{r["ft_origin"]}->{r["ft_extreme"]} '
              f'| {r["l2_events"][:90]} | L1 {r["l1_events"][:90]}')
    print(f"filas={len(keep)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
