"""python3 mutate.py
变异测试：对参考解做一处改动，看 verifier 的各类信号能否区分「该判错」和「不该判错」。
  should=fail  语义变了（部件挪位、缩放、缺失、变色）
  should=pass  语义没变（面数、光照强度、写法），判错就是误杀
verifier 判别力 = 该挂的挂了多少（检出率）+ 不该挂的放过多少（保真率）。
"""
import json, sys
from pathlib import Path
import compare

HERE = Path(__file__).parent
TASK = sys.argv[1] if sys.argv[1:] and sys.argv[1] != 'report' else 'snowman'
REF = HERE / f'tasks/{TASK}/ref.html'
OUT = HERE / f'tasks/{TASK}_mut'

# (名字, 原文片段, 替换片段, should)
MUTANTS = json.load(open(HERE / f'tasks/{TASK}/mutants.json')) if (HERE / f'tasks/{TASK}/mutants.json').exists() else [
    ('nose_z_half',     '0, 3.2, 0.62).rotation', '0, 3.2, 0.3).rotation',   'fail'),
    ('nose_missing',    "add(new THREE.ConeGeometry(0.08, 0.45, 24), carrot, 0, 3.2, 0.62).rotation.x = Math.PI/2;", '', 'fail'),
    ('nose_green',      '0xff7a1a', '0x22aa44',                               'fail'),
    ('head_up_0.3',     'snow, 0, 3.2, 0)', 'snow, 0, 3.5, 0)',               'fail'),
    ('head_x_0.3',      'snow, 0, 3.2, 0)', 'snow, 0.3, 3.2, 0)',             'fail'),
    ('body_r_+20%',     'SphereGeometry(0.9,', 'SphereGeometry(1.08,',        'fail'),
    ('mid_r_-20%',      'SphereGeometry(0.62,', 'SphereGeometry(0.5,',        'fail'),
    ('head_r_+5%',      'SphereGeometry(0.42,', 'SphereGeometry(0.44,',       'pass'),
    ('segments_16',     '48, 32)', '16, 12)',                                 'pass'),
    ('light_dim',       'DirectionalLight(0xffffff, 1.5)', 'DirectionalLight(0xffffff, 0.6)', 'pass'),
    ('snow_tint',       '0xf4f6fa', '0xeef0f4',                               'pass'),
    ('bg_color',        '0x87a8d0', '0xd0b087',                               'pass'),
    ('cam_moved',       'cam.position.set(0, 1.4, 6)', 'cam.position.set(1.5, 2, 5)', 'pass'),
]


def verdicts(s, ref_cols, main=None):
    """把连续分数变成 pass/fail；阈值在 snowman 正解上定，变异集上不调"""
    return {
        'page':  s['page'] >= 0.99,
        'mv':    s['mv_min'] >= 0.9,
        'vox':   all(s['vox'].get(c, 0) >= (0.9 if c == main else 0.5) for c in ref_cols),
        'naive': s['naive_pass'],
    } | {'mv+vox': s['mv_min'] >= 0.9 and all(s['vox'].get(c, 0) >= (0.9 if c == main else 0.5) for c in ref_cols)}


def main():
    OUT.mkdir(exist_ok=True)
    src = REF.read_text()
    for name, a, b, _ in MUTANTS:
        assert a in src, name
        (OUT / f'{name}.html').write_text(src.replace(a, b, 1))
    (OUT / 'ref.html').write_text(src)
    runs = HERE / 'runs' / OUT.name
    ref = compare.probe(OUT / 'ref.html', runs / 'ref')
    cols = sorted(set(ref['vox']) - {''})
    import collections
    main = collections.Counter(c for c in ref['vox'] if c).most_common(1)[0][0]
    table = []
    for name, _, _, should in MUTANTS:
        c = compare.probe(OUT / f'{name}.html', runs / name, runs / 'ref/probe.json')
        s = compare.score(runs / 'ref', ref, runs / name, c)
        v = verdicts(s, cols, main)
        table.append(dict(name=name, should=should, **{k: ('pass' if x else 'fail') for k, x in v.items()}, raw=s))
        print(name, should, v, s['page'], s['mv_min'], s['vox'])
    for k in ['page', 'mv', 'vox', 'naive', 'mv+vox']:
        right = sum(r[k] == r['should'] for r in table)
        print(f'{k:6s} 判对 {right}/{len(table)}')
    json.dump(table, open(runs / 'mutation.json', 'w'), indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()

