from __future__ import annotations
import hashlib, importlib.util, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("core", ROOT / "python" / "TM_CORE_PYTHON_v0752_CANONICAL.py")
core = importlib.util.module_from_spec(spec); sys.modules["core"] = core; spec.loader.exec_module(core)
FEED = ROOT / "data" / "TM_TICKFEED_1615_1730.csv"

def sig(engine):
    return [(e.get("kind"),e.get("function"),e.get("direction"),e.get("structural_sequence_id"),e.get("confirmation_sequence_id"))
            for e in engine.events]

def run(points):
    e=core.Engine([],{})
    e.feed_chunk(points)
    return e.finalize_stream()

def main():
    points,_=core.load_feed(FEED)
    start=core.parse_hms("16:15:00",points[0].time_ms);end=core.parse_hms("16:25:00",points[0].time_ms)
    points=core.filter_points(points,start,end)
    baseline=run(points)
    # Chunk boundary plus a serialized fresh-process checkpoint.
    cut=len(points)//2
    first=core.Engine([],{});first.feed_chunk(points[:cut]);restored=core.Engine.restore_state(first.serialize_state())
    restored.feed_chunk(points[cut:]);chunked=restored.finalize_stream()
    assert sig(baseline)==sig(chunked), "chunk/checkpoint event stream differs"
    # Translation and timestamp offset must preserve structure.
    shifted=[core.Pt(p.price+12_345,p.seq,p.time_ms+7_200_000,p.bar+120) for p in points]
    shifted_engine=run(shifted)
    norm=lambda e:[(x.get("kind"),x.get("function"),x.get("direction")) for x in e.events]
    assert norm(baseline)==norm(shifted_engine), "price/time translation changed event genealogy"
    # Price inversion must preserve function genealogy and invert direction.
    inverted=[core.Pt(-p.price,p.seq,p.time_ms,p.bar) for p in points]
    inv_engine=run(inverted)
    inv_dir={-1:1,0:0,1:-1}
    assert [(k,f,inv_dir.get(d,d)) for k,f,d in norm(baseline)]==norm(inv_engine), "direction inversion changed function genealogy"
    # Forbidden golden literals are checked in the engine source only.
    source=(ROOT/"python"/"TM_CORE_PYTHON_v0752_CANONICAL.py").read_text(encoding="utf-8")
    forbidden=["29850.8","29850.0","29842.5","29844.8","29832.5","29830.3","29852.6","29837.3","29833.3","29840.6","29828.1","1809","1846","1879","2062","2078","2107","2165","2259","16:19","16:20","16:21","16:22","16:23","16:24"]
    hits=[x for x in forbidden if x in source]
    assert not hits, f"golden hardcodes in engine: {hits}"
    result={"status":"PASS","chunk_serialize_restore":"PASS","shifted_prices_timestamps":"PASS","inverted_direction":"PASS","engine_hardcodes":hits,"feed_points":len(points)}
    out=ROOT/"out"/"TRANSFORMATION_TESTS.json";out.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
