import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "05_REFERENCE_ENGINE"))

from tm_reference_interpreter_v1_direct_aut import FEED, load_ticks  # noqa: E402
from tm_reading_manager import TMReadingManager  # noqa: E402


def main() -> int:
    ticks = [t for t in load_ticks(FEED)
             if 16 * 60 + 15 <= t.bar % 1440 <= 16 * 60 + 32]
    mgr = TMReadingManager(ticks).run()
    last = {}
    for row in mgr.rows:
        last[row["bar"]] = row
    for bar in sorted(last):
        row = last[bar]
        hh = f"{bar // 60}:{bar % 60:02d}"
        print(f"== {hh} phase={row['l1_phase']} one={row['l1_one_dir']}@"
              f"{row['l1_one_size']} two={row['l1_two']} "
              f"mod={row['l1_mod']} a={row['l1_a']} b={row['l1_b']} "
              f"tt={row['l1_tt']}@{row['l1_tt_objective']} "
              f"n={row['l1_n_origin']}->{row['l1_n_extreme']} "
              f"cyc={row['l1_cycle']}")
    summ = mgr.summaries()
    for p in summ["pattern_records"]:
        print("PATTERN", p["pattern_id"], p["pattern_type"], p["status"],
              p.get("objective"), p.get("confirmed_price"),
              p.get("functional_extreme"), p.get("owner_generation_id"),
              p.get("opened_at_seq"), p.get("confirmed_at_seq"))
    for g in summ["generation_records"]:
        print("GEN", g["generation_id"], g["status"], g.get("opened_at_seq"),
              g.get("closed_at_seq"), g.get("close_reason"))
    print({k: v for k, v in summ.items()
           if k not in ("pattern_records", "generation_records")})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
