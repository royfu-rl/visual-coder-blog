"""三类信号的打分与判定。

信号族
  view0     只看场景自带相机的一张图（最常见的 2D verifier）
  mv_mask   verifier 自己摆 9 个相机的剪影 IoU（多视角）
  mv_rgb    同一组相机的平光彩色图相似度
  geom      Chamfer / F-score / 按色体素 IoU（见 geom.py）
  stateA1~A9 bpy 状态断言，按属性族分开记，便于看每族各自抓住什么

用法：python verify.py <ref_dir> <cand_dir>
"""
import json, math, sys
from pathlib import Path
import numpy as np
from PIL import Image
import geom

TOL = dict(loc=0.005, rot=0.5, scale=0.01, color=0.03, scalar=0.02, energy=0.02)


# ------------------------------------------------------------------ 图像信号
def rgba(d, i):
    a = np.asarray(Image.open(Path(d) / f"view_{i}.png").convert("RGBA"), dtype=np.float32)
    return a[..., :3] * (a[..., 3:] / 255.0), a[..., 3] > 127      # 合成到黑底 + 剪影


def image_signals(ref_dir, cand_dir, nview=9):
    r0, _ = rgba(ref_dir, 0); c0, _ = rgba(cand_dir, 0)
    ious, rgbs = [], []
    for i in range(1, nview + 1):
        r, rm = rgba(ref_dir, i); c, cm = rgba(cand_dir, i)
        ious.append((rm & cm).sum() / max((rm | cm).sum(), 1))
        rgbs.append(1 - np.abs(r - c).mean() / 255)
    return dict(view0=round(float(1 - np.abs(r0 - c0).mean() / 255), 4),
                mv_mask_min=round(float(min(ious)), 4), mv_mask_mean=round(float(np.mean(ious)), 4),
                mv_rgb_min=round(float(min(rgbs)), 4), mv_rgb_mean=round(float(np.mean(rgbs)), 4))


# ------------------------------------------------------------- 状态断言（九族）
def near(a, b, t):
    return abs(float(a) - float(b)) <= t


def vnear(a, b, t):
    return len(a) == len(b) and all(near(x, y, t) for x, y in zip(a, b))


def angnear(a, b, t):
    return all(min(abs(x - y) % 360, 360 - abs(x - y) % 360) <= t for x, y in zip(a, b))


def families(R, C):
    """返回 {族名: [失败说明...]}。空列表 = 该族通过"""
    f = {k: [] for k in "A1 A2 A3 A4 A5 A6 A7 A8 A9".split()}
    ro, co = R["objects"], C["objects"]

    # A1 物体层级与命名：名字集合、父子、所属集合
    if set(ro) != set(co):
        f["A1"].append(f"objects differ: missing={sorted(set(ro)-set(co))} extra={sorted(set(co)-set(ro))}")
    for n in set(ro) & set(co):
        if ro[n]["parent"] != co[n]["parent"]:
            f["A1"].append(f"{n}.parent")
        if ro[n]["collections"] != co[n]["collections"]:
            f["A1"].append(f"{n}.collection")
    if {k: v for k, v in R["collections"].items()} != C["collections"]:
        f["A1"].append("collection membership")

    for n in sorted(set(ro) & set(co)):
        a, b = ro[n], co[n]
        # A2 变换：世界位置 / 欧拉角 / 缩放 + 世界包围盒（对「换建模路径」更稳）
        if not vnear(a["loc"], b["loc"], TOL["loc"]):
            f["A2"].append(f"{n}.loc {a['loc']}≠{b['loc']}")
        if not angnear(a["rot_deg"], b["rot_deg"], TOL["rot"]):
            f["A2"].append(f"{n}.rot {a['rot_deg']}≠{b['rot_deg']}")
        if not vnear(a["scale"], b["scale"], TOL["scale"]):
            f["A2"].append(f"{n}.scale {a['scale']}≠{b['scale']}")
        # A3 网格统计：求值后的拓扑计数、流形性、带符号体积（负=法线翻了）
        if "mesh" in a and "mesh" in b:
            x, y = a["mesh"]["eval"], b["mesh"]["eval"]
            for k in ("verts", "faces", "tris"):
                if x[k] != y[k]:
                    f["A3"].append(f"{n}.{k} {x[k]}≠{y[k]}")
            if y["non_manifold_edges"] or y["loose_verts"]:
                f["A3"].append(f"{n} non-manifold={y['non_manifold_edges']} loose={y['loose_verts']}")
            if math.copysign(1, x["volume"]) != math.copysign(1, y["volume"]):
                f["A3"].append(f"{n} normals flipped")
            if not near(x["volume"], y["volume"], abs(x["volume"]) * 0.02 + 1e-6):
                f["A3"].append(f"{n}.volume {x['volume']}≠{y['volume']}")
        # A4 修改器栈：类型顺序 + 关键参数
        if [m["type"] for m in a["modifiers"]] != [m["type"] for m in b["modifiers"]]:
            f["A4"].append(f"{n} modifier stack {[m['type'] for m in a['modifiers']]}≠{[m['type'] for m in b['modifiers']]}")
        else:
            for m, k in zip(a["modifiers"], b["modifiers"]):
                for key in set(m) & set(k) - {"name"}:
                    if isinstance(m[key], float) and not near(m[key], k[key], TOL["scalar"]):
                        f["A4"].append(f"{n}.{m['type']}.{key} {m[key]}≠{k[key]}")
                    elif not isinstance(m[key], float) and m[key] != k[key]:
                        f["A4"].append(f"{n}.{m['type']}.{key} {m[key]}≠{k[key]}")
        # A6 灯光与相机
        for kind, tol in (("light", TOL["energy"]), ("camera", TOL["scalar"])):
            if kind in a and kind in b:
                for key, va in a[kind].items():
                    vb = b[kind].get(key)
                    ok = (vnear(va, vb, TOL["color"]) if isinstance(va, list) else
                          near(va, vb, abs(va) * tol + 1e-6) if isinstance(va, float) else va == vb)
                    if not ok:
                        f["A6"].append(f"{n}.{kind}.{key} {va}≠{vb}")
            elif (kind in a) != (kind in b):
                f["A6"].append(f"{n}.{kind} missing")
        # A7 动画 F-curve：通道、关键帧（帧号 + 值）、插值
        fa, fb = a.get("fcurves", {}), b.get("fcurves", {})
        if set(fa) != set(fb):
            f["A7"].append(f"{n} fcurve channels {sorted(fa)}≠{sorted(fb)}")
        for ch in set(fa) & set(fb):
            ka, kb = fa[ch]["keys"], fb[ch]["keys"]
            if len(ka) != len(kb) or not all(near(p[0], q[0], 0.01) and near(p[1], q[1], 0.01)
                                             for p, q in zip(ka, kb)):
                f["A7"].append(f"{n}.{ch} keys {ka}≠{kb}")
            if fa[ch]["interp"] != fb[ch]["interp"]:
                f["A7"].append(f"{n}.{ch} interp")
        # A8 约束与刚体
        if a["constraints"] != b["constraints"]:
            f["A8"].append(f"{n}.constraints")
        if a["rigid_body"] != b["rigid_body"]:
            f["A8"].append(f"{n}.rigid_body")

    # A5 材质节点树：节点类型集合 + 连线 + 关键 socket 默认值
    for m in set(R["materials"]) | set(C["materials"]):
        x, y = R["materials"].get(m), C["materials"].get(m)
        if x is None or y is None:
            f["A5"].append(f"material {m} missing"); continue
        if x["nodes"] != y["nodes"] or x["links"] != y["links"]:
            f["A5"].append(f"{m} node graph")
        for k, va in x["defaults"].items():
            vb = y["defaults"].get(k)
            if vb is None:
                f["A5"].append(f"{m}.{k} missing"); continue
            t = TOL["color"] if isinstance(va, list) else TOL["scalar"]
            if not (vnear(va, vb, t) if isinstance(va, list) else near(va, vb, t)):
                f["A5"].append(f"{m}.{k} {va}≠{vb}")
    if R["world"] != C["world"]:
        f["A5"].append("world node tree")

    # A9 场景渲染设置
    for k, va in R["render"].items():
        vb = C["render"].get(k)
        if va != vb:
            f["A9"].append(f"render.{k} {va}≠{vb}")
    return f


# ------------------------------------------------------------------- 组装
def score(ref_dir, cand_dir):
    ref_dir, cand_dir = Path(ref_dir), Path(cand_dir)
    R = json.load(open(ref_dir / "state.json")); C = json.load(open(cand_dir / "state.json"))
    s = dict(error=C["error"] is not None)
    s.update(image_signals(ref_dir, cand_dir, len(R["views"]["pos"])))
    s.update(geom.all_metrics(ref_dir, cand_dir, R["grid"]))
    fam = families(R["state"], C["state"])
    s["state"] = {k: (v[:3] if v else None) for k, v in fam.items()}
    s["state_pass"] = {k: not v for k, v in fam.items()}
    return s


# 阈值在「参考解自己跑两遍」的噪声上定，不在变异集上调（见 THRESHOLDS.md）
TH = dict(view0=0.995, mv_mask=0.97, mv_rgb=0.995, chamfer=0.004, f=0.97, vox=0.80, shape=0.90,
          worst_f=0.99)     # 分部件 F-score 的阈值取「不该挂那一档」的下沿 0.9989


def verdicts(s):
    g = {
        "view0":    s["view0"] >= TH["view0"],
        "mv_mask":  s["mv_mask_min"] >= TH["mv_mask"],
        "mv_rgb":   s["mv_rgb_min"] >= TH["mv_rgb"],
        "chamfer":  s["chamfer"] <= TH["chamfer"],
        "fscore":   s["f"] >= TH["f"],
        "vox":      s["min_color"] >= TH["vox"] and s["shape"] >= TH["shape"],
        "geom_pc":  s["worst_f"] >= TH["worst_f"],      # 分部件 F-score，取最差那组
    }
    g.update({f"state_{k}": v for k, v in s["state_pass"].items()})
    g["state_all"] = all(s["state_pass"].values())
    g["geom_all"] = g["chamfer"] and g["fscore"] and g["vox"]
    g["mv+vox"] = g["mv_mask"] and g["vox"]
    # 组合判据：形状/位置/颜色交给渲染和几何，断言只留「图里根本看不见」的那几族
    # 刻意不收 A2(变换) / A3(网格统计) / view0(单图)——它们在变异集上保真率最差
    g["combo"] = all(g[k] for k in ("mv_mask", "geom_all", "state_A1", "state_A4",
                                    "state_A6", "state_A7", "state_A8", "state_A9"))
    g["combo+A5"] = g["combo"] and g["state_A5"]
    # 推荐判据：几何只用分部件 F-score，断言只留「渲染里看不见」的四族
    g["combo_pc"] = all(g[k] for k in ("geom_pc", "state_A4", "state_A6", "state_A7", "state_A9"))
    return {k: (v and not s["error"]) for k, v in g.items()}


if __name__ == "__main__":
    s = score(sys.argv[1], sys.argv[2])
    print(json.dumps(s, ensure_ascii=False, indent=1))
    print(json.dumps(verdicts(s), ensure_ascii=False))

