"""python3 scratch.py [--rounds 3] [--models ...]

从零搭建而不是修复：起始页只有渲染器、相机、灯光和材质，没有任何物体。
每道题的参考解就是对应那个场景，判定沿用同一套分层 verifier。
问题描述分两档：纯文本需求 / 文本加参考解的 4 视角图。

要回答的问题：修复型任务上立住的 verifier，换到「从零」任务上是不是过严。
"""
import argparse, json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import compare, verify, solve

HERE = Path(__file__).parent
REFMAP = {'snowman': 'snowman', 'table': 'table', 'desk': 'desk', 'car': 'car'}


def ensure_refs():
    """每道题用自己的参考场景，各自探一次"""
    out = {}
    for k, name in REFMAP.items():
        d = HERE / 'runs/scratch_ref' / k
        ref = compare.probe(HERE / f'tasks/{name}/ref.html', d)
        json.dump(ref, open(d / 'probe.json', 'w'))
        out[k] = (d, ref)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--models', default='claude-opus-5-5,gpt-6-astra,gemini-3.8-flash,qwen3.8-max')
    ap.add_argument('--rounds', type=int, default=3)
    ap.add_argument('--specs', default='text,img')
    ap.add_argument('--workers', type=int, default=12)
    a = ap.parse_args()

    refs = ensure_refs()
    spec = json.load(open(HERE / 'tasks/scratch/tasks.json'))
    outroot = HERE / 'runs/scratch_solve'
    out = outroot / 'results.jsonl'; outroot.mkdir(parents=True, exist_ok=True)
    done = {(j['task'], j['model'], j['cond'], j.get('spec')) for j in map(json.loads, open(out))} if out.exists() else set()

    jobs = []
    for t in spec['tasks']:
        rd, ref = refs[t['id']]
        for m in a.models.split(','):
            for sp in a.specs.split(','):
                for c in ['multi']:
                    if (t['id'], m, c, sp) not in done:
                        jobs.append((t, m, c, a.rounds, rd, ref, outroot, sp))
    print(f'{len(jobs)} jobs')
    with ThreadPoolExecutor(a.workers) as ex, open(out, 'a') as f:
        for r in ex.map(solve.run_one, jobs):
            f.write(json.dumps(r, ensure_ascii=False) + '\n'); f.flush()

    rows = [json.loads(l) for l in open(out)]
    rows = {(r['task'], r['model'], r['cond'], r.get('spec')): r for r in rows}.values()
    rows = [r for r in rows if not any('error' in h for h in r['hist'])]
    print(f'\n有效 {len(rows)} 组')
    for sp in ['text', 'img']:
        rs = [r for r in rows if r.get('spec') == sp]
        if not rs: continue
        print(f"  描述={sp:5s} 首轮 {sum(r['first'] == 'pass' for r in rs)}/{len(rs)}  末轮 {sum(r['final'] == 'pass' for r in rs)}/{len(rs)}")
    print('\n按题目：')
    for t in sorted({r['task'] for r in rows}):
        rs = [r for r in rows if r['task'] == t]
        lay = [h.get('layer') for r in rs for h in r['hist'][-1:] if h.get('verdict') == 'fail']
        import collections
        print(f"  {t:10s} 通过 {sum(r['final'] == 'pass' for r in rs)}/{len(rs)}  末轮挂在 {dict(collections.Counter(lay))}")


if __name__ == '__main__':
    main()

