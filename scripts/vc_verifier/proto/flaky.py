"""python3 flaky.py
取证重复性：同一份产物连续探测 K 次，看判定会不会翻面、信号值会不会变。
成稿里把「取证 flaky 率」列为必须监控的指标之一，这里把本项目自己的基线量出来。
"""
import json, collections
from pathlib import Path
import compare, verify

HERE = Path(__file__).parent
K = 3
CASES = [('snowman_mut', n) for n in ['ref', 'nose_back', 'head_up_0.3', 'segments_16', 'light_dim']] + \
        [('car_mut', n) for n in ['ref', 'wheel-three', 'lamps-one', 'wheel-seg-10', 'cam-other-side']]


def main():
    rows = []
    for task, name in CASES:
        runs = HERE / 'runs' / task
        ref = json.load(open(runs / 'ref/probe.json'))
        src = HERE / 'tasks' / task / f'{name}.html'
        if not src.exists(): print('缺', src); continue
        vs, sigs = [], []
        for k in range(K):
            c = compare.probe(src, runs / f'flaky_{name}_{k}', runs / 'ref/probe.json')
            v = verify.verify(runs / 'ref', ref, runs / f'flaky_{name}_{k}', c)
            vs.append(v['verdict'])
            sigs.append((v['signals']['mv_min'], v['signals']['blk_min'],
                         tuple(sorted(v['signals']['vox'].items()))))
        flip = len(set(vs)) > 1
        drift = len(set(sigs)) > 1
        rows.append(dict(task=task, name=name, verdicts=vs, flip=flip, drift=drift))
        print(f"  {task:12s} {name:16s} {'判定翻面' if flip else '判定一致'}  {'信号有漂移' if drift else '信号逐位相同'}")
    n = len(rows)
    print(f"\n{n} 个产物各探测 {K} 次：判定翻面 {sum(r['flip'] for r in rows)}/{n}，信号漂移 {sum(r['drift'] for r in rows)}/{n}")
    json.dump(rows, open(HERE / 'runs/flaky.json', 'w'), indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()

