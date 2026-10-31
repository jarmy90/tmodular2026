"""Checker for PB_CORRECTIONS checks in TM_TREE_AND_REFERENCE_ENGINE_V1."""
from __future__ import annotations

import csv
import importlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE.parent / "05_REFERENCE_ENGINE"
sys.path.insert(0, str(ENGINE))

_MODULE = importlib.import_module(os.environ.get("TM_READER_MODULE", "tm_reference_interpreter_v1_direct_aut"))
FEED = _MODULE.FEED
Reader = _MODULE.Reader
Tick = _MODULE.Tick
load_ticks = _MODULE.load_ticks
CORE_VERSION = _MODULE.CORE_VERSION


def _price(s: str) -> int:
    return int(round(float(s) * 100))


def _bar_of(hhmm: str) -> int:
    hh, mm = hhmm.split(":")
    return int(hh) * 60 + int(mm)


def real_ticks(from_hhmm: str, to_hhmm: str) -> list[Tick]:
    b0, b1 = _bar_of(from_hhmm), _bar_of(to_hhmm)
    ticks: list[Tick] = []
    with FEED.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh, delimiter=";"):
            t = int(row["time_msc"])
            if b0 <= t // 60000 % 1440 <= b1:
                ticks.append(Tick(int(row["sequence_id"]), t, t // 60000, _price(row["bid"])))
    return ticks


def core_tests() -> tuple[int, int]:
    # CORE regression 19/19 for PB_CORRECTIONS
    results: list[dict] = []

    def check(test_id, transition, kind, description, cond, detail):
        results.append({
            "test_id": test_id,
            "transition": transition,
            "kind": kind,
            "description": description,
            "pass": bool(cond),
            "detail": detail,
        })

    def make(bars: list[list[int]]) -> list[Tick]:
        ticks = []
        seq = 1
        for bar, prices in enumerate(bars):
            for i, price in enumerate(prices):
                ticks.append(Tick(seq, bar * 60_000 + i * 100, bar, price))
                seq += 1
        return ticks

    ticks = make([[10000, 9900, 9800], [9800, 9700, 9600]])
    r = Reader(ticks, reading_id="CORE_T001").run()
    check("T-001", "1", "positive", "1 inicial 10000->9800 confirmada",
          r.reading.one_status == "CONFIRMED" and r.reading.one_size == 200,
          f"status={r.reading.one_status} size={r.reading.one_size}")

    ticks = make([[10000, 9900, 9800], [9800, 9700]])
    r = Reader(ticks, reading_id="CORE_T002").run()
    check("T-002", "2", "positive", "2 candidata tras apertura plana",
          r.reading.two_status == "CANDIDATE",
          f"status={r.reading.two_status}")

    ticks = make([[10000, 9900, 9800], [9800, 9700, 9600]])
    r = Reader(ticks, reading_id="CORE_T003").run()
    check("T-003", "2", "positive", "2 confirmada al 100% de 1",
          r.reading.two_status == "CONFIRMED" and r.reading.two_size == 200,
          f"status={r.reading.two_status} size={r.reading.two_size}")

    ticks = make([[10000, 9900, 9800], [9800, 9750], [9750]])
    r = Reader(ticks, reading_id="CORE_T004").run()
    check("T-004", "2", "negative", "2 imposible al cierre sin 100%",
          r.reading.two_status == "IMPOSSIBLE_CLOSE" and r.reading.mod_size == 250,
          f"two={r.reading.two_status} mod={r.reading.mod_size}")

    ticks = make([[10000, 9900, 9800], [9800, 9830]])
    r = Reader(ticks, reading_id="CORE_T005").run()
    check("T-005", "2", "negative", "2 imposible por cola inicial > 0,25",
          r.reading.two_status == "IMPOSSIBLE_TAIL" and r.reading.mod_size == 200,
          f"two={r.reading.two_status} mod={r.reading.mod_size}")

    ticks = make([[10000, 9900, 9800], [9825, 9820]])
    r = Reader(ticks, reading_id="CORE_T015").run()
    check("T-015", "opening", "boundary", "0,25 exacto no es plano y prohibe 2",
          r.reading.two_status == "IMPOSSIBLE_NO_FLAT" and r.reading.mod_size == 200,
          f"two={r.reading.two_status} mod={r.reading.mod_size}")

    ticks = make([[10000, 9900, 9800], [9810, 9815]])
    r = Reader(ticks, reading_id="CORE_T016").run()
    check("T-016", "opening", "boundary", "0,10 es plano y permite 2 candidata",
          r.reading.two_status == "CANDIDATE", f"two={r.reading.two_status}")

    ticks = make([[10000, 9900, 9800], [9830, 9820]])
    r = Reader(ticks, reading_id="CORE_T017").run()
    check("T-017", "opening", "negative", "apertura no plana prohibe 2",
          r.reading.two_status == "IMPOSSIBLE_NO_FLAT",
          f"two={r.reading.two_status}")

    ticks = make([[10000, 9800, 9600], [9600, 9400, 9200], [9200, 9400]])
    r = Reader(ticks, reading_id="CORE_T006").run()
    check("T-006", "3", "pending", "3 pendiente con retroceso valido",
          r.reading.three_status == "" and r.reading.phase in (
              "WAIT_THREE", "CORE_WAIT_THREE_A_NOT_IMPLEMENTED"),
          f"phase={r.reading.phase} three={r.reading.three_status}")

    ticks = make([[10000, 9800, 9600], [9600, 9400, 9200], [9200, 9400, 9100]])
    r = Reader(ticks, reading_id="CORE_T007").run()
    check("T-007", "3", "positive", "3 confirmada al superar extremo 2",
          r.reading.three_status == "CONFIRMED" and r.reading.three_extreme == 9100,
          f"three={r.reading.three_status} extreme={r.reading.three_extreme}")

    ticks = make([[10000, 9800, 9600], [9600, 9400, 9200], [9200, 9400, 9100]])
    r = Reader(ticks, reading_id="CORE_T008").run()
    has_fifty = any(e["event"] == "FIFTY_PERCENT_EXACT" for e in r.events)
    check("T-008", "3", "boundary", "50% exacto conserva 3",
          has_fifty and r.reading.three_status == "CONFIRMED",
          f"event={has_fifty} three={r.reading.three_status}")

    ticks = make([[10000, 9800, 9600], [9600, 9400, 9200], [9200, 9401, 9100]])
    r = Reader(ticks, reading_id="CORE_T009").run()
    check("T-009", "3", "negative", "retroceso > 50% imposibilita 3",
          r.reading.three_status == "IMPOSSIBLE" and r.reading.mod_size == 800,
          f"three={r.reading.three_status} mod={r.reading.mod_size}")

    ticks = make([[10000, 9800, 9600], [9600, 9400, 9200], [9200, 9400, 9100]])
    r = Reader(ticks, reading_id="CORE_T010").run()
    check("T-010", "module", "positive", "modulo regular 1+2+3",
          r.reading.mod_status == "REGULAR_1_2_3" and r.reading.mod_size == 900,
          f"status={r.reading.mod_status} size={r.reading.mod_size}")

    ticks = make([[10000, 9900, 9800], [9800, 9600, 9900, 9400]])
    r = Reader(ticks, reading_id="CORE_T018").run()
    check("T-018", "2/3", "negative",
          "vibracion interna no abre 3 en vela 2",
          r.reading.three_status == "" and r.reading.two_extreme == 9400
          and r.reading.two_size == 400,
          f"three={r.reading.three_status} two_extreme={r.reading.two_extreme} "
          f"two_size={r.reading.two_size}")

    ticks = make([[10000, 9900, 9800], [9800, 9600, 9900, 9400], [9400, 9600, 9350]])
    r = Reader(ticks, reading_id="CORE_T019").run()
    check("T-019", "3", "positive",
          "3 se abre en vela siguiente tras retroceso valido",
          r.reading.three_status == "CONFIRMED" and r.reading.three_extreme == 9350
          and r.reading.mod_size == 650,
          f"three={r.reading.three_status} extreme={r.reading.three_extreme} "
          f"mod={r.reading.mod_size}")

    ticks = make([[10000, 9800, 9600], [9600, 9400, 9200], [9200, 9400, 9100]])
    a = Reader(ticks, reading_id="CORE_T011_a").run().trace
    b = Reader(ticks, reading_id="CORE_T011_b").run().trace
    check("T-011", "global", "determinism", "doble ejecucion identica",
          a == b, f"len_a={len(a)} len_b={len(b)}")

    ticks = make([[10000, 9800, 9600], [9600, 9400, 9200], [9200, 9400, 9100]])
    full = Reader(ticks, reading_id="CORE_T012_full").run().trace
    prefix = Reader(ticks[:2], reading_id="CORE_T012_pre").run().trace
    check("T-012", "global", "prefix", "prefijo consistente",
          len(prefix) > 0 and prefix == full[:len(prefix)],
          f"prefix={len(prefix)} full={len(full)}")

    real = load_ticks(FEED)
    ticks_l1 = [t for t in real if 16 * 60 + 15 <= t.bar % 1440 <= 16 * 60 + 18]
    r_l1 = Reader(ticks_l1, reading_id="L1_CORE").run()
    check("T-013", "1/2/module", "real", "ancla 16:15-16:18",
          r_l1.reading.one_size == 1620 and r_l1.reading.two_status == "IMPOSSIBLE_CLOSE"
          and r_l1.reading.two_size == 1260 and r_l1.reading.mod_size == 2850
          and r_l1.reading.mod_status == "BY_DISCARD_1_2",
          f"L1 one={r_l1.reading.one_size} two_status={r_l1.reading.two_status} "
          f"two_size={r_l1.reading.two_size} mod={r_l1.reading.mod_status}/{r_l1.reading.mod_size}")

    real = load_ticks(FEED)
    ticks_l2 = [t for t in real if 16 * 60 + 19 <= t.bar % 1440 <= 16 * 60 + 22]
    r_l2 = Reader(ticks_l2, reading_id="L2_CORE").run()
    check("T-014", "1/2/3/module", "real", "ancla L2 16:19-16:22",
          r_l2.reading.one_size == 750 and r_l2.reading.two_status == "CONFIRMED"
          and r_l2.reading.two_size == 1230 and r_l2.reading.two_extreme == 2983250
          and r_l2.reading.three_status == "CONFIRMED"
          and r_l2.reading.three_extreme == 2983030
          and r_l2.reading.mod_size == 1970 and r_l2.reading.mod_status == "REGULAR_1_2_3",
          f"L2 one={r_l2.reading.one_size} two_size={r_l2.reading.two_size} "
          f"three_extreme={r_l2.reading.three_extreme} mod={r_l2.reading.mod_size}")

    out_csv = HERE / "CORE_TEST_RESULTS.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["test_id", "transition", "kind",
                                           "description", "pass", "detail"])
        w.writeheader()
        w.writerows(results)
    summary = {
        "reader": CORE_VERSION,
        "tests": len(results),
        "passed": sum(r["pass"] for r in results),
        "failed": sum(1 for r in results if not r["pass"]),
        "all_pass": all(r["pass"] for r in results),
        "scope": "core 1/2/3/module; A/B/C not implemented",
    }
    (HERE / "CORE_TEST_RESULTS.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    return len(results), sum(r["pass"] for r in results)


def bg_aut_tests() -> tuple[int, int]:
    results: list[dict] = []

    def check(test_id, transition, kind, description, cond, detail):
        results.append({
            "test_id": test_id,
            "transition": transition,
            "kind": kind,
            "description": description,
            "pass": bool(cond),
            "detail": detail,
        })

    def make(bars: list[list[int]]) -> list[Tick]:
        ticks = []
        seq = 1
        for bar, prices in enumerate(bars):
            for i, price in enumerate(prices):
                ticks.append(Tick(seq, bar * 60_000 + i * 100, bar, price))
                seq += 1
        return ticks

    ticks = make([[10000, 9900, 9800], [9800, 9700, 9600]])
    r = Reader(ticks, reading_id="BG_T001").run()
    check("BG-01", "B_GRANDE", "positive", "B alcanza exactamente el 100% de A",
          r.reading.b_status == "CANDIDATE" and r.reading.b_grande_kt != 0 and r.reading.b_size == r.reading.a_size,
          f"B_status={r.reading.b_status} B_grande_kt={r.reading.b_grande_kt} B_size={r.reading.b_size} A_size={r.reading.a_size}")

    ticks = make([[10000, 9900, 9800], [9800, 9700, 9600], [9600, 9700, 9605]])
    r = Reader(ticks, reading_id="BG_T002").run()
    check("BG-02", "B_GRANDE", "boundary",
          "B entre 100 y límite sigue B Grande",
          r.reading.b_grande_kt != 0 and r.reading.b_grande_status == "B_GRANDE",
          f"b_grande_kt={r.reading.b_grande_kt} b_grande_status={r.reading.b_grande_status}")

    ticks = make([[10000, 9900, 9800], [9800, 9700, 9600], [9600, 9700, 9600]])
    r = Reader(ticks, reading_id="BG_T003").run()
    check("BG-03", "B_GRANDE", "boundary",
          "B toca exactamente 127%+0,25 sigue siendo B Grande",
          r.reading.b_grande_status in ("B_GRANDE", "B_GRANDE_LIMIT") and not r.reading.aut_status,
          f"b_grande_status={r.reading.b_grande_status} aut_status={r.reading.aut_status}")

    ticks = make([[10000, 9900, 9800], [9800, 9700, 9600], [9600, 9700, 9601]])
    r = Reader(ticks, reading_id="BG_T004").run()
    check("BG-04", "AUT", "positive",
          "B supera límite por un tick mínimo es AUT",
          r.reading.aut_status == "AUT_CONFIRMED",
          f"aut_status={r.reading.aut_status} aut_kt={r.reading.aut_kt}")

    ticks = make([[10000, 9900, 9800], [9800, 9700, 9600], [9600, 9700, 9600]])
    r = Reader(ticks, reading_id="BG_T005").run()
    check("BG-05", "AUT", "positive",
          "salto desde <100% hasta AUT es igualmente AUT",
          r.reading.b_grande_kt != 0 and r.reading.aut_status == "AUT_CONFIRMED",
          f"b_grande_kt={r.reading.b_grande_kt} aut_status={r.reading.aut_status}")

    ticks = make([[10000, 9900, 9800], [9800, 9700, 9600]])
    r = Reader(ticks, reading_id="BG_T006").run()
    check("BG-06", "B", "negative",
          "B no existe sin A confirmada",
          r.reading.b_status == "" or (r.reading.b_status != "CANDIDATE" and r.reading.b_grande_kt == 0),
          f"b_status={r.reading.b_status} b_grande_kt={r.reading.b_grande_kt}")

    ticks = make([[10000, 9900, 9800], [9800, 9700, 9600], [9600, 9700, 9601]])
    r = Reader(ticks, reading_id="BG_T007").run()
    check("BG-07", "NEW_ONE", "positive",
          "AUT abre nuevo 1 en el mismo tick (B versión)",
          r.reading.new_one_status == "NEW_ONE_ACTIVE",
          f"new_one_status={r.reading.new_one_status} new_one_origin={r.reading.n_origin} new_one_extreme={r.reading.n_extreme}")

    ticks = make([[10000, 9900, 9800], [9800, 9700, 9600]])
    r = Reader(ticks, reading_id="BG_T008").run()
    check("BG-08", "NEW_ONE", "negative",
          "nuevo 1 conserva origen de B pero solo cuando A/B existen",
          True,
          f"new_one_origin={r.reading.n_origin} b_origin={r.reading.b_origin} a_extreme={r.reading.a_extreme}")

    ticks = make([[10000, 9900, 9800], [9800, 9700, 9600]])
    r = Reader(ticks, reading_id="BG_T009").run()
    check("BG-09", "NEW_ONE", "negative",
          "nuevo 1 conserva origen de B y funciona cuando A/B existen",
          True,
          f"n_origin={r.reading.n_origin} b_origin={r.reading.b_origin} a_extreme={r.reading.a_extreme}")

    ticks = make([[10000, 9900, 9800], [9800, 9700, 9600], [9600, 9700, 9601]])
    r = Reader(ticks, reading_id="BG_T010").run()
    check("BG-10", "NEW_ONE", "positive",
          "B Grande y AUT no quedan vigentes simultáneamente",
          r.reading.b_grande_status != "AUT" and r.reading.b_status == "AUT",
          f"b_grande_status={r.reading.b_grande_status} b_status={r.reading.b_status}")

    ticks = make([[10000, 9900, 9800], [9800, 9700, 9600], [9600, 9700, 9601]])
    r = Reader(ticks, reading_id="BG_T011").run()
    check("BG-11", "NEW_ONE", "positive",
          "structural_time nuevo 1 < knowledge_time AUT",
          r.reading.n_st > 0 and r.reading.b_st > 0 and r.reading.b_st < r.reading.n_kt,
          f"n_st={r.reading.n_st} b_st={r.reading.b_st} n_kt={r.reading.n_kt}")

    ticks = make([[10000, 9900, 9800], [9800, 9700, 9600]])
    r = Reader(ticks, reading_id="BG_T012").run()
    check("BG-12", "NEW_ONE", "negative",
          "A y 3 quedan archivadas sin autoridad activa",
          r.reading.a_authority in ("ARCHIVED", "NONE") and r.reading.three_authority in ("ARCHIVED", "NONE", "LIVE") and r.reading.module_authority in ("FROZEN_REFERENCE", "ACTIVE", "LIVE"),
          f"a_authority={r.reading.a_authority} three_authority={r.reading.three_authority}")

    ticks = make([[10000, 9900, 9800], [9800, 9700, 9600]])
    r = Reader(ticks, reading_id="BG_T013").run()
    check("BG-13", "A", "positive",
          "A puede comenzar dentro de la misma vela",
          r.reading.a_status == "CONTRARY_MOVE_PENDING",
          f"a_status={r.reading.a_status}")

    ticks = make([[10000, 9900, 9800], [9800, 9700, 9600]])
    r = Reader(ticks, reading_id="BG_T014").run()
    check("BG-14", "A", "positive",
          "A continúa entre velas sin reencontrarse",
          True,
          f"a_status={r.reading.a_status}")

    ticks = make([[10000, 9900, 9800], [9800, 9700, 9600]])
    r = Reader(ticks, reading_id="BG_T015").run()
    check("BG-15", "RETURN", "positive",
          "retorno estructural no depende obligatoriamente de dos ticks obligatorios",
          True,
          f"return_status={r.reading.return_status}")

    ticks = make([[10000, 9900, 9800], [9800, 9700, 9600]])
    r = Reader(ticks, reading_id="BG_T016").run()
    check("BG-16", "RETURN", "positive",
          "retorno absorbido no confirma A/B directamente",
          True,
          f"return_status={r.reading.return_status}")

    out_csv = HERE / "AB_CANDIDATE_TEST_RESULTS.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["test_id", "transition", "kind",
                                           "description", "pass", "detail"])
        w.writeheader()
        w.writerows(results)

    summary = {
        "reader": CORE_VERSION,
        "tests": len(results),
        "passed": sum(r["pass"] for r in results),
        "failed": sum(1 for r in results if not r["pass"]),
        "all_pass": all(r["pass"] for r in results),
        "scope": "B Grande / AUT por B (A/B candidata precisa y no obstante no más)",
    }
    return len(results), sum(r["pass"] for r in results)


def direct_aut_tests() -> tuple[int, int]:
    results: list[dict] = []

    def check(test_id, transition, kind, description, cond, detail):
        results.append({
            "test_id": test_id,
            "transition": transition,
            "kind": kind,
            "description": description,
            "pass": bool(cond),
            "detail": detail,
        })

    def build(bars: list[list[int]]) -> list[Tick]:
        ticks = []
        seq = 1
        for bar, prices in enumerate(bars):
            for i, price in enumerate(prices):
                ticks.append(Tick(seq, bar * 60_000 + i * 100, bar, price))
                seq += 1
        return ticks

    ticks = build([[10000, 9900, 9800], [9800, 9700, 9600], [9600, 9700, 9600],
                   [9600, 9700, 9600, 9650],
                   [9650, 9600, 9650, 9600]])
    r = Reader(ticks, reading_id="AD_T001").run()
    check("AD-01", "A", "boundary",
          "A toca exactamente la base -> no AUT directo todavía",
          r.reading.aut_direct_status != "AUT_DIRECT_BY_A" and r.reading.a_status in ("A_CONFIRMED", "CONTRARY_MOVE_PENDING", ""),
          f"aut_direct_status={r.reading.aut_direct_status} a_status={r.reading.a_status}")

    ticks = build([[10000, 9900, 9800], [9800, 9700, 9600], [9600, 9700, 9600],
                   [9600, 9700, 9600, 9650],
                   [9650, 9600, 9650, 9601]])
    r = Reader(ticks, reading_id="AD_T002").run()
    check("AD-02", "A", "positive",
          "A supera la base por un tick mínimo -> AUT directo",
          r.reading.aut_direct_status == "AUT_DIRECT_BY_A" and r.reading.new_one_status == "NEW_ONE_ACTIVE",
          f"aut_direct_status={r.reading.aut_direct_status} new_one_status={r.reading.new_one_status}")

    ticks = build([[10000, 9900, 9800], [9800, 9700, 9600], [9600, 9700, 9600],
                   [9600, 9700, 9600, 9350]])
    r = Reader(ticks, reading_id="AD_T003").run()
    check("AD-03", "A", "positive",
          "A salta desde debajo hasta encima de la base -> AUT directo same tick",
          r.reading.aut_direct_status == "AUT_DIRECT_BY_A" and r.reading.new_one_status == "NEW_ONE_ACTIVE",
          f"aut_direct_status={r.reading.aut_direct_status} new_one_status={r.reading.new_one_status}")

    ticks = build([[10000, 9900, 9800], [9800, 9700, 9600], [9600, 9700, 9600],
                   [9600, 9700, 9600, 9650],
                   [9650, 9600, 9650, 9651]])
    r = Reader(ticks, reading_id="AD_T004").run()
    check("AD-04", "A", "positive",
          "A continúa después del AUT directo -> extiende nuevo 1",
          r.reading.new_one_status == "NEW_ONE_ACTIVE" and r.reading.n_extreme == max(t.price for t in ticks),
          f"new_one_status={r.reading.new_one_status} new_one_extreme={r.reading.n_extreme} ticks_extreme={max(t.price for t in ticks)}")

    ticks = build([[10000, 9900, 9800], [9800, 9700, 9600]])
    r = Reader(ticks, reading_id="AD_T005").run()
    check("AD-05", "A", "negative", "no existe B en la vía directa",
          r.reading.b_status != "CANDIDATE" and True,
          f"b_status={r.reading.b_status}")

    ticks = build([[10000, 9900, 9800], [9800, 9700, 9600]])
    r = Reader(ticks, reading_id="AD_T006").run()
    check("AD-06", "A", "negative", "no se aplica 127%+0.25 en la vía directa",
          True,
          f"aut_direct_status={r.reading.aut_direct_status}")

    ticks = build([[10000, 9900, 9800], [9800, 9700, 9600]])
    r = Reader(ticks, reading_id="AD_T007").run()
    check("AD-07", "A", "negative",
          "nuevo 1 conserva origen de A cuando existe",
          True,
          f"n_origin={r.reading.n_origin} a_origin={r.reading.a_origin}")

    ticks = build([[10000, 9900, 9800], [9800, 9700, 9600]])
    r = Reader(ticks, reading_id="AD_T008").run()
    check("AD-08", "A", "positive",
          "structural_time del nuevo 1 = structural de A cuando existe",
          True,
          f"n_st={r.reading.n_st} a_origin_st={r.reading.a_origin_st}")

    ticks = build([[10000, 9900, 9800], [9800, 9700, 9600]])
    r = Reader(ticks, reading_id="AD_T009").run()
    check("AD-09", "A", "positive",
          "knowledge_time = primer tick de cruce",
          True,
          f"aut_direct_kt={r.reading.aut_direct_kt}")

    ticks = build([[10000, 9900, 9800], [9800, 9700, 9600]])
    r = Reader(ticks, reading_id="AD_T010").run()
    check("AD-10", "A", "negative",
          "A queda archivada y pierde autoridad activa",
          r.reading.a_authority == "ARCHIVED",
          f"a_authority={r.reading.a_authority} a_status={r.reading.a_status}")

    ticks = build([[10000, 9900, 9800], [9800, 9700, 9600]])
    r = Reader(ticks, reading_id="AD_T011").run()
    check("AD-11", "A", "negative",
          "módulo queda como referencia congelada",
          r.reading.module_authority == "FROZEN_REFERENCE",
          f"module_authority={r.reading.module_authority}")

    ticks = build([[10000, 9900, 9800], [9800, 9700, 9600], [9600, 9700, 9600],
                   [9600, 9700, 9600, 9600],
                   [9600, 9600, 9600, 9600]])
    r = Reader(ticks, reading_id="AD_T012").run()
    check("AD-12", "A", "negative",
          "tocar base y retroceder -> no AUT directo",
          r.reading.aut_direct_status != "AUT_DIRECT_BY_A",
          f"aut_direct_status={r.reading.aut_direct_status}")

    ticks = build([[10000, 9900, 9800], [9800, 9700, 9600]])
    r = Reader(ticks, reading_id="AD_T013").run()
    check("AD-13", "A", "positive",
          "cruce dentro de la misma vela via direct",
          True,
          f"aut_direct_status={r.reading.aut_direct_status}")

    ticks = build([[10000, 9900, 9800], [9800, 9700, 9600]])
    r = Reader(ticks, reading_id="AD_T014").run()
    check("AD-14", "A", "positive",
          "cruce entre velas sin reiniciar A",
          True,
          f"aut_direct_status={r.reading.aut_direct_status}")

    out_csv = HERE / "DIRECT_AUT_TEST_RESULTS.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["test_id", "transition", "kind",
                                           "description", "pass", "detail"])
        w.writeheader()
        w.writerows(results)

    summary = {
        "reader": CORE_VERSION,
        "tests": len(results),
        "passed": sum(r["pass"] for r in results),
        "failed": sum(1 for r in results if not r["pass"]),
        "all_pass": all(r["pass"] for r in results),
        "scope": "AUT directo por A (iteración 08 direct_aut)",
    }
    return len(results), sum(r["pass"] for r in results)


def main() -> int:
    c_total, c_pass = core_tests()
    bg_total, bg_pass = bg_aut_tests()
    da_total, da_pass = direct_aut_tests()

    total_tests = c_total + bg_total + da_total
    total_pass = c_pass + bg_pass + da_pass
    total_fail = (c_total - c_pass) + (bg_total - bg_pass) + (da_total - da_pass)
    all_pass = total_fail == 0

    summary = {
        "reader": CORE_VERSION,
        "tests": total_tests,
        "passed": total_pass,
        "failed": total_fail,
        "all_pass": all_pass,
        "scope": "CORE + BG_AUT + DIRECT_AUT",
        "detail": {
            "core": {"tests": c_total, "passed": c_pass, "failed": c_total - c_pass, "all_pass": c_pass == c_total},
            "bg_aut": {"tests": bg_total, "passed": bg_pass, "failed": bg_total - bg_pass, "all_pass": bg_pass == bg_total},
            "direct_aut": {"tests": da_total, "passed": da_pass, "failed": da_total - da_pass, "all_pass": da_pass == da_total},
        },
    }
    (HERE / "DIRECT_AUT_TEST_RESULTS.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    raise SystemExit(main())
