# -*- coding: utf-8 -*-
"""Probe: same R5, same ticks -> two authorities, late/retroactive TT, local boot after AUT."""
import importlib.util, sys
from pathlib import Path

CORE = Path(__file__).resolve().parents[1] / "00_INPUTS_REFERENCE" / "variants" / "R5_AUDITED_9BD1BEDB.py"
spec = importlib.util.spec_from_file_location("r5_probe", CORE)
m = importlib.util.module_from_spec(spec); sys.modules["r5_probe"] = m; spec.loader.exec_module(m)

CASES = {
 "A_two_authorities": [[0,4,8,10,12],[14,16,18,20,14],[14,12,10,8,16],[18,20,22,24,26],[28,30,32,34,35],[34,32,30,29]],
 "B_same_tick_b_aut_tt": [[0,4,8,10,12],[14,16,18,20,14],[14,12,10,8,16],[18,24,30,36,40],[38,36,34]],
}
for name, bars in CASES.items():
    pts=[]; seq=0
    for bi,b in enumerate(bars,1):
        for ti,pr in enumerate(b):
            seq+=1; pts.append(m.Pt(m.price_i(pr),seq,bi*60000+ti*1000,bi))
    e=m.CanonicalEngine(pts,{}); e.trace_states=True
    print("="*100); print("CASE", name, "ticks", len(pts)); print("="*100)
    for pt in pts:
        n=len(e.events); e.feed_chunk([pt])
        for ev in e.events[n:]:
            if ev["kind"] in ("FIN_FEED",): continue
            print(f'tick {pt.seq:2d} p={pt.price/100:7.2f} {ev["kind"]:17s} f={ev["function"]:7s} '
                  f'st={ev["new_state"]:12s} structural_p={ev["price"]/100:7.2f} '
                  f'knowledge_p={ev["knowledge_price"]/100:7.2f} tt_100={ev["tt_100"]/100:7.2f}')
    for r in e.readings:
        print(f'READ {r.reading_id} dir={r.direction} state={r.state} module={r.module_origin/100}->{r.module_extreme/100} '
              f'A={r.a_origin/100}->{r.a_end/100} B={r.b_origin/100}->{r.b_extreme/100} '
              f'tt_target={r.tt_target/100} tt_hit={r.tt_hit} tt_price={r.tt_price/100} '
              f'b_grande_t={r.b_grande_time} aut_t={r.aut_time} local={getattr(r,"local_sequence_id","")}')
