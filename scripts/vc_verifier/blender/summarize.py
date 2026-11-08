"""从 runs/ 里已有的探针输出重算所有信号并出表（不重跑 bpy）。
  python summarize.py            # 开发集 + 留出集
"""
import json, sys
from pathlib import Path
import verify, mutate

R = Path(__file__).parent / "runs/desk_lamp"
SIG = ["combo_pc", "combo", "view0", "mv_mask", "mv_rgb", "chamfer", "fscore", "vox", "geom_pc",
       "geom_all", "state_A1", "state_A2", "state_A3", "state_A4", "state_A5",
       "state_A6", "state_A7", "state_A8", "state_A9", "state_all"]


def batch(tag, cases):
    rows = []
    for name, _, _, should in cases:
        s = verify.score(R / "ref", R / name)
        rows.append(dict(name=name, should=should, raw=s, v=verify.verdicts(s)))
    nf = sum(r["should"] == "fail" for r in rows)
    print(f"\n=== {tag}（{nf} 该挂 / {len(rows)-nf} 不该挂）")
    print(f"{'信号':12s} {'总判对':>8s} {'检出':>8s} {'保真':>8s}   误判的 case")
    for k in SIG:
        hit = [r["name"] for r in rows if r["should"] == "fail" and not r["v"][k]]
        keep = [r["name"] for r in rows if r["should"] == "pass" and r["v"][k]]
        bad = [r["name"] for r in rows if (r["should"] == "fail") == r["v"][k]]
        print(f"{k:12s} {len(hit)+len(keep):4d}/{len(rows):<3d} {len(hit):4d}/{nf:<3d} "
              f"{len(keep):4d}/{len(rows)-nf:<3d}   {' '.join(bad)[:80]}")
    json.dump(rows, open(R / f"{tag}_full.json", "w"), indent=1, ensure_ascii=False)
    return rows


if __name__ == "__main__":
    a = batch("mutation", mutate.MUTANTS)
    b = batch("holdout", mutate.HOLDOUT)
    print("\n=== 两批合并")
    rows = a + b
    nf = sum(r["should"] == "fail" for r in rows)
    for k in SIG:
        hit = sum(1 for r in rows if r["should"] == "fail" and not r["v"][k])
        keep = sum(1 for r in rows if r["should"] == "pass" and r["v"][k])
        print(f"{k:12s} {hit+keep:4d}/{len(rows):<3d}  检出 {hit}/{nf}  保真 {keep}/{len(rows)-nf}")

