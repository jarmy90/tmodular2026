"""Sonda: estado L2 al cierre de cada vela 16:24-16:29 (una sola pasada)."""
import tm_reading_manager as mm
from tm_reference_interpreter_v1_direct_aut import load_ticks, FEED

ticks = load_ticks(FEED)
mgr = mm.TMReadingManager(ticks)
mgr._maybe_archive_local = lambda t: None

snaps = []
prev_bar = None
for t in ticks:
    b = t.bar % 1440
    if prev_bar is not None and b != prev_bar:
        r = mgr.l2.reading if mgr.l2 else None
        if r is not None:
            snaps.append((prev_bar, last_price, r.phase, r.mod_size, r.mod_status,
                          r.a_status, r.a_size, r.a_origin, r.b_status, r.b_size,
                          r.n_origin, r.n_extreme, r.n_dir, r.tt_status,
                          r.tt_objective, r.tt_extreme, r.ft_status, r.ft_origin,
                          r.ft_extreme, r.cycle_id, r.one_size, r.one_origin))
    prev_bar = b
    last_price = t.price
    mgr.feed(t)

print("cierre de vela: phase mod a b n tt ft cycle")
for s in snaps:
    (b, px, phase, mod, mst, ast, asz, aor, bst, bsz, no, ne, nd, tts, tto,
     tte, fts, fto, fte, cyc, osz, oor) = s
    if not (16 * 60 + 23 <= b <= 16 * 60 + 29):
        continue
    print(f"{b//60:02d}:{b%60:02d} px={px} {phase} mod={mod}/{mst} "
          f"a={ast}/{asz}@{aor} b={bst}/{bsz} n={no}->{ne}/{nd} "
          f"tt={tts}/{tto}/{tte} ft={fts}/{fto}->{fte} cyc={cyc} one={osz}@{oor}")
