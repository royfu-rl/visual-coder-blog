"""分块 IoU：把体素网格切成 B^3 块，只看参考里有内容的块，取最差的一块。
全局 IoU 对「一条腿短了」这种局部缺陷不敏感，分块能把它放大。"""
import json, sys
from pathlib import Path
import numpy as np
from compare import snap

HERE = Path(__file__).parent


def blocks(ref_vox, cand_vox, B=6, min_fill=15):
    N = round(len(ref_vox) ** (1 / 3))
    pal = set(ref_vox) - {''}
    r = (np.array(ref_vox) != '').reshape(N, N, N)
    c = (np.array(snap(cand_vox, pal)) != '').reshape(N, N, N)
    e = N // B
    out = []
    for i in range(B):
        for j in range(B):
            for k in range(B):
                sl = (slice(i * e, (i + 1) * e), slice(j * e, (j + 1) * e), slice(k * e, (k + 1) * e))
                a, b = r[sl], c[sl]
                if a.sum() < min_fill: continue
                out.append((a & b).sum() / max((a | b).sum(), 1))
    return out


def main(task):
    runs = HERE / 'runs' / f'{task}_mut'
    ref = json.load(open(runs / 'ref/probe.json'))
    rows = json.load(open(runs / 'mutation.json'))
    print(f'--- {task} (B=6)')
    for r in rows:
        c = json.load(open(runs / r['name'] / 'probe.json'))
        bl = blocks(ref['vox'], c['vox'])
        r['blk_min'] = round(float(min(bl)), 3); r['blk_p10'] = round(float(np.percentile(bl, 10)), 3)
        print(f"{r['name']:14s} {r['should']:4s} blk_min={r['blk_min']:.3f} p10={r['blk_p10']:.3f}  (mv+vox={r['mv+vox']})")
    for th in [0.5, 0.6, 0.7]:
        ok = sum((('pass' if r['blk_min'] >= th else 'fail') == r['should']) for r in rows)
        okc = sum((('pass' if (r['blk_min'] >= th and r['mv+vox'] == 'pass') else 'fail') == r['should']) for r in rows)
        print(f'  blk_min>={th}: 单独 {ok}/{len(rows)}   与 mv+vox 组合 {okc}/{len(rows)}')
    json.dump(rows, open(runs / 'mutation.json', 'w'), indent=1, ensure_ascii=False)


if __name__ == '__main__':
    for t in (sys.argv[1:] or ['snowman', 'table']): main(t)

