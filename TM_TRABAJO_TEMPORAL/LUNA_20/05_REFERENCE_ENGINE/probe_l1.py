"""Sonda L1: apertura del movimiento contrario desde 29875.4 y estado 16:25-16:27."""
import tm_reading_manager as mm
from tm_reference_interpreter_v1_direct_aut import load_ticks, FEED, _hhmm

ticks = load_ticks(FEED)
mgr = mm.TMReadingManager(ticks)
mgr._maybe_archive_local = lambda t: None
mgr.run()
r = mgr.l1.reading
print("L1 final phase", r.phase, "a", r.a_status, r.a_origin, r.a_extreme, r.a_size,
      "| tt", r.tt_status, r.tt_extreme, "| ft", r.ft_status, r.ft_origin,
      r.ft_extreme, r.ft_size, "| n", r.n_origin, r.n_extreme, "| mod", r.mod_size,
      "| cycle", r.cycle_id)

print("\nEVENTOS L1 16:25:40-16:27:10")
for e in r.events:
    bar = (e["time_ms"] // 60000) % 1440
    hh = _hhmm(e["time_ms"])
    if "16:25:40" <= hh <= "16:27:10":
        print(f'{e["seq"]:5d} {hh} {e["event"]:<34} {e["detail"][:170]}')
