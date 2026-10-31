"""Sonda: reconstruccion tick a tick 16:24-16:27 sin archivar LOCAL-G1."""
import os
from pathlib import Path

import tm_reading_manager as mm
from tm_reference_interpreter_v1_direct_aut import load_ticks, FEED, _hhmm

ticks = load_ticks(FEED)
print("ticks", len(ticks), "feed", FEED)


def bar_of(t):
    return (t.time_ms // 60000) % 1440


def hhmm(bar):
    return f"{bar // 60:02d}:{bar % 60:02d}"


# 1. OHLC por vela 16:24..16:27 y seq de extremos
for b in range(16 * 60 + 24, 16 * 60 + 28):
    ts = [t for t in ticks if t.bar == b]
    if not ts:
        continue
    hi = max(ts, key=lambda t: t.price)
    lo = min(ts, key=lambda t: t.price)
    print(f"\nVELA {hhmm(b)} n={len(ts)} open={ts[0].price} close={ts[-1].price} "
          f"high={hi.price}@{hi.seq} low={lo.price}@{lo.seq}")
    print("  seq", ts[0].seq, "..", ts[-1].seq)

# 2. manager sin archivo
mgr = mm.TMReadingManager(ticks)
mgr._maybe_archive_local = lambda t: None
mgr.run()
l2 = mgr.l2
r = l2.reading
print("\nL2 final phase", r.phase, "a", r.a_status, r.a_size, "b", r.b_status,
      r.b_size, "mod", r.mod_size, "tt", r.tt_status, "ext", r.tt_extreme,
      "ft", r.ft_status, r.ft_origin, r.ft_extreme, r.ft_size,
      "n", r.n_origin, r.n_extreme, "cycle", r.cycle_id)

print("\nEVENTOS L2 16:24-16:27")
seen = set()
for e in r.events:
    bar = (e["time_ms"] // 60000) % 1440
    if 16 * 60 + 24 <= bar <= 16 * 60 + 27:
        key = (e["seq"], e["event"], e["detail"][:60])
        if key in seen:
            continue
        seen.add(key)
        print(f'{e["seq"]:5d} {hhmm(bar)} {_hhmm(e["time_ms"])} {e["event"]:<32} {e["detail"][:150]}')
