"""从零搭建型任务的判据：只看相对关系，不看绝对位置。

现有的分层 verifier 量的是与参考的绝对几何重合度，只在「除一处外都与参考一致」的修复任务上成立；
从零搭建时它 16 组全挂，而产物在人看来都对。

这里换一族量：先把场景整体归一化（平移到包围盒中心、按对角线缩放），再查
  R1 部件构成   每种颜色的部件个数（连通块）
  R2 体量占比   每种颜色的体积占全场的比例
  R3 相对尺度   每个部件的尺寸相对全场对角线
  R4 上下关系   部件之间谁在谁上方（归一化后的中心高度序）
  R5 接触关系   部件对之间是否接触（归一化后的包围盒间隙）
  R6 拓扑       开放边界边数
判据全部是比例或序关系，和整体尺度、整体位置无关。

python3 relational.py <ref_probe.json> <cand_probe.json> [...]
"""
import json, sys
from pathlib import Path
import numpy as np
from scipy import ndimage
from compare import snap

TOL = dict(count=0, vol_ratio=0.35, size_ratio=0.40, gap=0.06, order=0)


def voxel_parts(p):
    """从体素网格里按颜色取连通块，每块给归一化中心、尺寸、体积占比。
    按颜色分组会把桌面和四条腿合成一块（同色），于是少一条腿看不出来；按连通块分就看得出。"""
    vox = p.get('vox')
    if not vox: return None
    N = round(len(vox) ** (1 / 3))
    a = np.array(vox).reshape(N, N, N)
    occ = a != ''
    if not occ.any(): return []
    idx = np.argwhere(occ)
    lo, hi = idx.min(0), idx.max(0) + 1
    d = float(np.linalg.norm(hi - lo))
    out = []
    for col in sorted(set(vox) - {''}):
        lab, n = ndimage.label(a == col)
        for k in range(1, n + 1):
            cells = np.argwhere(lab == k)
            if len(cells) < 4: continue          # 太小的块是量化噪声
            c = (cells.mean(0) - (lo + hi) / 2) / d
            sz = (cells.max(0) - cells.min(0) + 1) / d
            out.append(dict(color=col, c=c, s=sz, vol=len(cells) / max(occ.sum(), 1), open=0))
    return out


def norm_parts(p):
    """按整体包围盒归一化，返回每个 mesh 的归一化中心、尺寸、颜色"""
    mn = np.min([m['min'] for m in p['meshes']], axis=0)
    mx = np.max([m['max'] for m in p['meshes']], axis=0)
    c0, d = (mn + mx) / 2, float(np.linalg.norm(mx - mn))
    out = []
    for m in p['meshes']:
        a, b = np.array(m['min']), np.array(m['max'])
        out.append(dict(color=(m['color'] or '')[1:].lower(),
                        c=((a + b) / 2 - c0) / d, s=(b - a) / d,
                        vol=float(np.prod(np.maximum(b - a, 1e-6))) / d ** 3,
                        open=m.get('open', 0)))
    return out, d


def group(parts):
    """同色部件合成一组：个数、总体量、最大尺寸、中心高度"""
    g = {}
    for p in parts:
        q = g.setdefault(p['color'], dict(n=0, vol=0.0, smax=np.zeros(3), ys=[]))
        q['n'] += 1; q['vol'] += p['vol']
        q['smax'] = np.maximum(q['smax'], p['s']); q['ys'].append(float(p['c'][1]))
    for q in g.values(): q['y'] = float(np.mean(q['ys']))
    return g


def contacts(parts, tol):
    """归一化后包围盒间隙小于 tol 的同色组对"""
    out = set()
    for i, a in enumerate(parts):
        for b in parts[i + 1:]:
            if a['color'] == b['color']: continue
            gap = np.maximum(np.abs(a['c'] - b['c']) - (a['s'] + b['s']) / 2, 0)
            if float(np.linalg.norm(gap)) < tol: out.add(tuple(sorted((a['color'], b['color']))))
    return out


def check(ref, cand, tol=TOL, mode='voxel'):
    rp = voxel_parts(ref) if mode == 'voxel' else None
    cp = voxel_parts(cand) if mode == 'voxel' else None
    if rp is None or cp is None:            # 没存体素就退回 mesh 包围盒
        rp, _ = norm_parts(ref); cp, _ = norm_parts(cand)
    pal = {p['color'] for p in rp}
    for p in cp:                       # 颜色就近归并，轻微调色不算换色
        if p['color'] not in pal and p['color']:
            p['color'] = snap([p['color']], pal)[0]
    rg, cg = group(rp), group(cp)
    fails = []

    # R1 部件构成：每种颜色必须有，连通块数用体素统计（更稳），这里用 mesh 组内个数做近似
    for col in pal:
        if col not in cg: fails.append(('R1 缺少颜色', col)); continue
        if cg[col]['n'] != rg[col]['n']:
            fails.append(('R1 部件个数', col, rg[col]['n'], cg[col]['n']))
    if fails: return fails

    for col in pal:
        r, c = rg[col], cg[col]
        # R2 体量占比
        if r['vol'] > 1e-4 and abs(c['vol'] - r['vol']) / r['vol'] > tol['vol_ratio']:
            fails.append(('R2 体量占比', col, round(r['vol'], 4), round(c['vol'], 4)))
        # R3 相对尺度：取最大边
        a, b = float(max(r['smax'])), float(max(c['smax']))
        if a > 1e-3 and abs(b - a) / a > tol['size_ratio']:
            fails.append(('R3 相对尺度', col, round(a, 3), round(b, 3)))

    # R4 上下关系：同色组按归一化中心高度排序，序必须一致
    ro = [k for k, _ in sorted(rg.items(), key=lambda kv: kv[1]['y'])]
    co = [k for k, _ in sorted(cg.items(), key=lambda kv: kv[1]['y']) if k in pal]
    if ro != co: fails.append(('R4 上下关系', ro, co))

    # R5 接触关系
    rc, cc = contacts(rp, tol['gap']), contacts(cp, tol['gap'])
    miss, extra = rc - cc, cc - rc
    if miss: fails.append(('R5 该接触却没接触', sorted(miss)))
    if extra: fails.append(('R5 不该接触却接触', sorted(extra)))

    # R6 拓扑
    ro_ = sum(m.get('open', 0) for m in ref['meshes']); co_ = sum(m.get('open', 0) for m in cand['meshes'])
    if co_ > ro_ * 1.1 + 16: fails.append(('R6 开放边界', ro_, co_))
    return fails


if __name__ == '__main__':
    ref = json.load(open(sys.argv[1]))
    for f in sys.argv[2:]:
        c = json.load(open(f))
        bad = check(ref, c)
        tag = Path(f).parts[-4] if len(Path(f).parts) >= 4 else f
        print(f"{tag:22s} {'通过' if not bad else '挂'}  {bad if bad else ''}")

