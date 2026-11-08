"""python3 ablate.py
留一层消融：关掉某一层信号，重跑准入，看还能收下多少任务。
收得越少，说明数据集越依赖那一层，也就越偏向那一层能看见的错误类型。
"""
import json
from pathlib import Path
import compare, verify, parts, blockiou, collections
import numpy as np

HERE = Path(__file__).parent


def verdict(ref, cand, off, main):
    """off 是要关掉的层名；返回这个破坏版还会不会被判挂"""
    sig = {}
    if cand['errors'] or not cand.get('meshes'):
        return 'fail'
    if off != 'L1':
        if cand['_mv'] < 0.9 or cand['_face'] < 0.9: return 'fail'
    if off != 'L2b':
        if (cand.get('overlap') or 0) > (ref.get('overlap') or 0) + 0.10 or (cand.get('flicker') or 0) > 64:
            return 'fail'
    if off != 'L2':
        if any(v < (0.9 if c == main else 0.5) for c, v in cand['_vox'].items()): return 'fail'
        if cand['_blk'] < 0.5: return 'fail'
    if off != 'L3':
        ok, _ = parts.compare_parts(ref['vox'], cand['vox'])
        oe, _ = parts.open_edges_ok(ref, cand)
        if not ok or not oe: return 'fail'
    return 'pass'


def main():
    out = {}
    for task, pat in [('desk_gen', 'b4_'), ('table_gen', 'b_')]:
        runs = HERE / 'runs' / task
        ref = json.load(open(runs / 'ref/probe.json'))
        main_col = collections.Counter(c for c in ref['vox'] if c).most_common(1)[0][0]
        broken = sorted((HERE / 'tasks' / task / 'broken').glob('*.html'))
        cands = []
        for b in broken:
            d = runs / f'ab_{b.stem}'
            c = compare.probe(b, d, runs / 'ref/probe.json')
            s = compare.score(runs / 'ref', ref, d, c)
            c['_mv'], c['_face'], c['_vox'] = s['mv_min'], s['face_min'], s['vox']
            c['_blk'] = round(float(min(blockiou.blocks(ref['vox'], c['vox']))), 3)
            cands.append((b.stem, c))
        row = {}
        for off in ['-', 'L1', 'L2', 'L2b', 'L3']:
            kept = [n for n, c in cands if verdict(ref, c, off, main_col) == 'fail']
            row[off] = (len(kept), len(cands))
        out[task] = row
        print(f'{task}：共 {len(cands)} 个提议的破坏')
        for off, (k, n) in row.items():
            tag = '全部信号' if off == '-' else f'关掉 {off}'
            print(f'  {tag:10s} 收 {k}/{n}')
    json.dump(out, open(HERE / 'runs/ablation.json', 'w'), indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()

