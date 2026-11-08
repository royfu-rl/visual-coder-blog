"""几何指标：Chamfer / F-score / 按色体素 IoU。输入是 probe.py 存的带色表面采样点。

约定
  尺度统一除以参考解包围盒对角线 diag，所有阈值都是相对量，换场景不用重调
  F-score 的容差 tau 默认 1% diag（本例 diag 约 2.9 m → tau 约 2.9 cm）
  体素 IoU 走表面占据（不要求 watertight），N=32 网格固定在参考解的 bbox 上
"""
import numpy as np
from scipy.spatial import cKDTree

N_VOX = 32


def chamfer(A, B, diag):
    """双向 Chamfer（均值）与 Hausdorff95，均已按 diag 归一化"""
    if not len(A) or not len(B):
        return dict(chamfer=1.0, hd95=1.0)
    da = cKDTree(B).query(A)[0] / diag
    db = cKDTree(A).query(B)[0] / diag
    return dict(chamfer=round(float(da.mean() + db.mean()) / 2, 5),
                hd95=round(float(max(np.percentile(da, 95), np.percentile(db, 95))), 5))


def fscore(A, B, diag, tau=0.01):
    """A=候选, B=参考。precision=候选点落在参考表面 tau 内的比例，recall 反之"""
    if not len(A) or not len(B):
        return dict(prec=0.0, rec=0.0, f=0.0)
    p = float((cKDTree(B).query(A)[0] / diag < tau).mean())
    r = float((cKDTree(A).query(B)[0] / diag < tau).mean())
    return dict(prec=round(p, 4), rec=round(r, 4), f=round(2 * p * r / max(p + r, 1e-9), 4))


def snap(cols, palette, tol=28):
    """候选颜色就近归到参考调色板。轻微调色不算错，换成另一个色族仍算错"""
    rgb = lambda h: np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=float)
    pal = {p: rgb(p) for p in palette}
    out = {}
    for h in set(cols.tolist()):
        if h in pal:
            out[h] = h; continue
        k, d = min(((k, np.linalg.norm(v - rgb(h))) for k, v in pal.items()), key=lambda x: x[1])
        out[h] = k if d < tol else h
    return np.array([out[h] for h in cols])


def voxelize(P, C, grid, n=N_VOX):
    lo, hi = np.array(grid[0]), np.array(grid[1])
    idx = np.floor((P - lo) / np.maximum(hi - lo, 1e-9) * n).astype(int)
    ok = ((idx >= 0) & (idx < n)).all(1)
    key = idx[ok] @ np.array([n * n, n, 1])
    return key, C[ok]


def vox_iou(ref, cand, grid, n=N_VOX):
    """按颜色分别算表面体素 IoU，外加一个忽略颜色的整体 IoU"""
    rk, rc = voxelize(ref[0], ref[1], grid, n)
    ck, cc = voxelize(cand[0], snap(cand[1], set(rc.tolist())), grid, n)
    iou = lambda a, b: len(a & b) / max(len(a | b), 1)
    per = {c: round(iou(set(rk[rc == c].tolist()), set(ck[cc == c].tolist())), 4)
           for c in sorted(set(rc.tolist()))}
    return dict(per_color=per, min_color=round(min(per.values()) if per else 0.0, 4),
                shape=round(iou(set(rk.tolist()), set(ck.tolist())), 4))


def per_color(ref, cand, diag, tau=0.005):
    """分部件（按材质色分组）各算一遍 Chamfer / F-score，取最差的那组。
    全局平均量对「小部件错了」天生不敏感——杯子只占全场 2% 的面积，挪走 30cm 全局 Chamfer 只动 0.0002"""
    RP, RC = ref; CP, CC = cand
    CC = snap(CC, set(RC.tolist()))
    out = {}
    for c in sorted(set(RC.tolist())):
        a, b = CP[CC == c], RP[RC == c]
        out[c] = dict(**chamfer(a, b, diag), **fscore(a, b, diag, tau), n=int(len(b)))
    return dict(per_color=out,
                worst_f=round(min((v["f"] for v in out.values()), default=0.0), 4),
                worst_chamfer=round(max((v["chamfer"] for v in out.values()), default=1.0), 5))


def load(d):
    z = np.load(d / "points.npz")
    return z["P"].astype(np.float64), z["C"].astype(str)


def all_metrics(ref_dir, cand_dir, grid, tau=0.01):
    RP, RC = load(ref_dir); CP, CC = load(cand_dir)
    diag = float(np.linalg.norm(np.array(grid[1]) - np.array(grid[0]))) or 1.0
    out = dict(diag=round(diag, 4))
    out.update(chamfer(CP, RP, diag))
    out.update(fscore(CP, RP, diag, tau))
    out.update(vox_iou((RP, RC), (CP, CC), grid))
    pc = per_color((RP, RC), (CP, CC), diag, tau=0.005)
    out.update(worst_f=pc["worst_f"], worst_chamfer=pc["worst_chamfer"])
    return out

