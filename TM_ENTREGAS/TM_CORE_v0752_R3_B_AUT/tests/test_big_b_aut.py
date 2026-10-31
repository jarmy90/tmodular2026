from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("core", ROOT / "python" / "TM_CORE_PYTHON_v0752_CANONICAL.py")
core = importlib.util.module_from_spec(spec)
sys.modules["core"] = core
spec.loader.exec_module(core)


class UniversalBigBTests(unittest.TestCase):
    def tracker(self, a_size=10_000, direction=1):
        anchor = 20_000_000
        return core.BigBTracker(direction, anchor, a_size, anchor)

    def test_01_9999_percent_is_candidate_only(self):
        t = self.tracker()
        self.assertEqual(t.feed(t.anchor + 9_999), [])
        self.assertFalse(t.confirmed)

    def test_02_exact_100_confirms_on_that_tick(self):
        t = self.tracker()
        self.assertEqual(t.feed(t.anchor + 10_000), ["B_GRANDE"])
        self.assertTrue(t.confirmed)

    def test_03_120_percent_remains_big_b(self):
        t = self.tracker()
        self.assertEqual(t.feed(t.anchor + 12_000), ["B_GRANDE"])
        self.assertFalse(t.aut)

    def test_04_exact_127_percent_plus_025_is_still_big_b(self):
        t = self.tracker()
        self.assertEqual(t.feed(t.anchor + 12_725), ["B_GRANDE"])
        self.assertFalse(t.aut)

    def test_05_first_increment_above_limit_is_immediate_aut(self):
        t = self.tracker()
        self.assertEqual(t.feed(t.anchor + 12_725), ["B_GRANDE"])
        self.assertEqual(t.feed(t.anchor + 12_726), ["AUT_B"])
        self.assertTrue(t.aut)

    def test_06_first_contrary_tick_after_big_b_starts_c_directly(self):
        t = self.tracker()
        t.feed(t.anchor + 10_000)
        self.assertTrue(t.begin_c(t.anchor + 9_999))
        self.assertFalse(t.begin_c(t.anchor + 9_998))

    def test_07_touching_a_base_is_not_crossing(self):
        self.assertFalse(core.strict_crosses(1, 10_000, 10_000))
        self.assertFalse(core.strict_crosses(-1, 10_000, 10_000))

    def test_08_crossing_a_base_confirms_direct_aut_route(self):
        self.assertTrue(core.strict_crosses(1, 10_001, 10_000))
        self.assertTrue(core.strict_crosses(-1, 9_999, 10_000))

    def test_09_internal_retraces_do_not_reset_b_extreme(self):
        t = self.tracker()
        t.feed(t.anchor + 5_000)
        t.feed(t.anchor + 2_500)
        t.feed(t.anchor + 4_500)
        self.assertEqual(t.extreme, t.anchor + 5_000)
        self.assertEqual(t.feed(t.anchor + 10_000), ["B_GRANDE"])

    def test_10_state_survives_bar_boundary_and_serialization(self):
        t = self.tracker()
        t.feed(t.anchor + 7_000)
        restored = core.pickle.loads(core.pickle.dumps(t))
        self.assertEqual(restored.feed(restored.anchor + 10_000), ["B_GRANDE"])
        self.assertTrue(restored.confirmed)

    def test_11_gap_blocks_two_before_other_two_conditions(self):
        self.assertFalse(core.local_two_gate(gap=25, tail=0, direction_ok=True, size_ok=True))

    def test_12_flat_no_tail_direction_and_size_allow_two(self):
        self.assertTrue(core.local_two_gate(gap=24, tail=25, direction_ok=True, size_ok=True))
        self.assertFalse(core.local_two_gate(gap=24, tail=26, direction_ok=True, size_ok=True))
        self.assertFalse(core.local_two_gate(gap=24, tail=0, direction_ok=False, size_ok=True))
        self.assertFalse(core.local_two_gate(gap=24, tail=0, direction_ok=True, size_ok=False))

    def test_13_live_engine_emits_b100_and_b_aut_on_exact_ticks_across_bars(self):
        e = core.Engine([])
        p0 = core.Pt(9_000_000, 1, 1_000, 0)
        seq = core.LocalSequence("LS0001", 1, "", 8_000_000, 9_000_000, 1_000, 1_000, 1, 1)
        r = core.Reading("LR0001", 1, "LOCAL_A", 1_000, 1, 0, "fixture", 8_000_000,
                         9_000_000, 1_000, 1_000, 1, 1)
        r.a_origin = 9_000_000
        r.a_end = 9_000_000 - 1_000_000
        r.a_origin_time = r.a_end_time = 1_000
        r.a_origin_seq = r.a_end_seq = 1
        r.dominant = True
        r.local_sequence_id = seq.sequence_id
        e.readings.append(r); e.active.append(r); e.by_id[r.reading_id] = r
        e.local_sequences.append(seq)
        e._local["state"] = {"sequence": seq, "reading": r, "direction": 1,
            "module_origin": p0, "module_extreme": p0, "one_size": 1_000_000,
            "bar1": 0, "bar2": None, "two_open": None, "two_confirmed": False,
            "requires_base": False, "aut_base": p0, "aut_count": 0}
        e._local.update({"phase": "B_ACTIVE", "b_origin": core.Pt(r.a_end, 1, 1_000, 0),
                         "b_extreme": core.Pt(r.a_end, 1, 1_000, 0), "a_origin": p0,
                         "a_extreme": core.Pt(r.a_end, 1, 1_000, 0)})
        a_end = r.a_end
        feed = [core.Pt(a_end, 10, 2_000, 0), core.Pt(a_end + 1_000_000, 11, 3_000, 1),
                core.Pt(a_end + 1_270_025, 12, 4_000, 2), core.Pt(a_end + 1_270_026, 13, 5_000, 2)]
        for point in feed:
            e.feed_chunk([point])
        b_events = [x for x in e.events if x.get("function") == "B" and x.get("new_state") == "LOCAL_B_GRANDE"]
        aut_events = [x for x in e.events if x.get("function") == "AUT"]
        self.assertEqual(len(b_events), 1)
        self.assertEqual(b_events[0]["confirmation_sequence_id"], 11)
        self.assertEqual(len(aut_events), 1)
        self.assertEqual(aut_events[0]["confirmation_sequence_id"], 13)
        self.assertEqual(aut_events[0]["aut_source"], core.AUT_CAUSE_B)
        self.assertEqual(aut_events[0]["active_function"], "AUT")

    def test_14_live_engine_a_direct_aut_has_no_fictitious_b(self):
        e = core.Engine([])
        base = core.Pt(10_000, 1, 1_000, 0)
        top = core.Pt(20_000, 2, 2_000, 0)
        seq = core.LocalSequence("LS0001", 1, "", base.price, top.price, 1_000, 2_000, 1, 2)
        r = core.Reading("LR0001", 1, "LOCAL_A", 2_000, 2, 0, "fixture", base.price,
                         top.price, 1_000, 2_000, 1, 2)
        r.dominant = True
        r.local_sequence_id = seq.sequence_id
        e.readings.append(r); e.active.append(r); e.by_id[r.reading_id] = r
        e.local_sequences.append(seq)
        state = {"sequence": seq, "reading": r, "direction": 1, "module_origin": base,
                 "module_extreme": top, "one_size": 10_000, "bar1": 0, "requires_base": False,
                 "aut_base": base, "aut_count": 0, "a_emitted": True}
        e._local["state"] = state
        e._local.update({"phase": "A_ACTIVE", "a_origin": top, "a_extreme": base})
        e.feed_chunk([core.Pt(base.price, 3, 3_000, 0)])
        self.assertFalse(any(x.get("function") == "AUT" for x in e.events))
        e.feed_chunk([core.Pt(base.price - 1, 4, 4_000, 0)])
        aut = [x for x in e.events if x.get("function") == "AUT"]
        self.assertEqual(len(aut), 1)
        self.assertEqual(aut[0]["aut_source"], core.AUT_CAUSE_A)
        self.assertEqual(aut[0]["active_function"], "AUT")
        self.assertFalse(any(x.get("function") == "B" for x in e.events))
        self.assertEqual(e.active[-1].direction, -1)

    def test_15_real_feed_emits_both_aut_causes_with_tick_knowledge(self):
        points, bars = core.load_feed(ROOT / "data" / "TM_TICKFEED_1615_1730.csv")
        engine = core.run_engine(points, bars)
        sources = {event.get("aut_source") for event in engine.events if event.get("function") == "AUT"}
        sources.update(event.get("aut_source") for event in engine.local_events if event.get("function") == "AUT")
        self.assertIn(core.AUT_CAUSE_B, sources)
        self.assertIn(core.AUT_CAUSE_A, sources)
        for event in engine.events:
            if event.get("function") == "AUT" and event.get("aut_source"):
                self.assertLessEqual(event["confirmation_sequence_id"], event["knowledge_sequence_id"])

    def test_16_post_aut_contrary_move_remains_c_grande(self):
        t = self.tracker()
        t.feed(t.anchor + 12_725)
        t.feed(t.anchor + 12_726)
        self.assertTrue(t.aut)
        self.assertTrue(t.begin_c(t.anchor + 12_725))


if __name__ == "__main__":
    unittest.main(verbosity=2)
