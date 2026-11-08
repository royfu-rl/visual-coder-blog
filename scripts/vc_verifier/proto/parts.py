"""按颜色的部件统计：体积比 + 连通块数。
体素/剪影 IoU 对细长部件（显示器立杆、灯臂）不敏感，因为它们占的体素极少；
但「这一色的总体积少了 30%」或「连通块从 2 个变 1 个」是能看出来的。
和几何类名断言不同，这个信号不关心用什么 API 建模，换写法不会误杀。
"""
import numpy as np
from scipy import ndimage
from compare import snap


def stats(vox, pal):
    N = round(len(vox) ** (1 / 3))
    a = np.array(vox).reshape(N, N, N)
    out = {}
    for c in pal:
        m = a == c
        out[c] = (int(m.sum()), int(ndimage.label(m)[1]))
    return out


def open_edges_ok(ref, cand):
    """候选的开放边界不能明显多于参考：闭合实体被做成破壳 / 开口面片时会暴涨"""
    r = sum(m.get('open', 0) for m in ref['meshes'])
    c = sum(m.get('open', 0) for m in cand['meshes'])
    return c <= r * 1.1 + 16, dict(ref_open=r, cand_open=c)


def compare_parts(ref_vox, cand_vox, vol_tol=0.25):
    pal = sorted(set(ref_vox) - {''})
    r, c = stats(ref_vox, pal), stats(snap(cand_vox, set(pal)), pal)
    rows = {}
    for col in pal:
        rv, rn = r[col]; cv, cn = c[col]
        rows[col] = dict(vol_ratio=round(cv / max(rv, 1), 3), ref_n=rn, cand_n=cn)
    worst = min((abs(1 - v['vol_ratio']) for v in rows.values()), default=0)
    ok = all(abs(1 - v['vol_ratio']) <= vol_tol and v['ref_n'] == v['cand_n'] for v in rows.values())
    return ok, rows

