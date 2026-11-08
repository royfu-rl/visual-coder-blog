"""python3 passk.py [--model M] [--k 8]

单模型 pass@k：同一道题独立采 k 次，统计每题通过几次。
用来钉死成本模型里最敏感的那一项——「难度带筛选留存率」。
前面那次难度分布是跨模型汇总的，混了模型强弱；这里是严格的 pass@k。
"""
import argparse, json, re, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests
import compare, verify

HERE = Path(__file__).parent
URL, KEY = 'http://klink.internal/v1/chat/completions', 'sk-klink-MJFlh5vNbu2Rnujem807KsvGhk7lhJ6O'
SYS = """你在修复一个 three.js 页面。页面能跑、不报错，但渲染出的 3D 场景在语义上是错的。
按需求把场景改对。只改必要的地方，不要重写整个页面，也不要改背景、光照、相机机位和网格精细度。
回复必须输出完整的、可直接运行的 HTML，放在 ```html 代码块里。"""


def call(model, msgs, temp):
    body = {'model': model, 'max_tokens': 20000, 'temperature': temp, 'messages': msgs}
    for k in range(3):
        try:
            r = requests.post(URL, json=body, headers={'Authorization': 'Bearer ' + KEY}, timeout=300,
                              proxies={'http': None, 'https': None})
            t = r.json()['choices'][0]['message']['content'] or ''
            m = re.search(r'```html\s*(.*?)```', t, re.S)
            if m: return m.group(1).strip()
        except Exception:
            pass
        time.sleep(4 * (k + 1))
    return None


def run(job):
    task, i, model, refd, ref, outroot = job
    work = outroot / task['id'] / f's{i}'
    work.mkdir(parents=True, exist_ok=True)
    src = Path(task['start']).read_text()
    msgs = [{'role': 'system', 'content': SYS},
            {'role': 'user', 'content': f"需求：{task['request']}\n\n当前页面源码：\n```html\n{src}\n```"}]
    code = call(model, msgs, 1.0)                 # 采样温度 1.0，k 次之间要有差异
    if not code: return dict(task=task['id'], i=i, verdict=None, err='no-output')
    f = work / 'try.html'; f.write_text(code)
    try:
        v = verify.probe_and_verify(refd, ref, f, work / 'probe')
    except Exception as e:
        return dict(task=task['id'], i=i, verdict=None, err=repr(e)[:90])
    return dict(task=task['id'], i=i, verdict=v['verdict'], layer=v['layer'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', default='gemini-3.8-flash')
    ap.add_argument('--k', type=int, default=8)
    ap.add_argument('--workers', type=int, default=16)
    a = ap.parse_args()
    spec = json.load(open(HERE / 'tasks/desk_gen/tasks.json'))
    refd = HERE / 'runs/desk_gen/ref'
    ref = json.load(open(refd / 'probe.json'))
    outroot = HERE / 'runs/passk'; outroot.mkdir(parents=True, exist_ok=True)
    out = outroot / 'results.jsonl'
    done = {(j['task'], j['i']) for j in map(json.loads, open(out))} if out.exists() else set()
    jobs = [(t, i, a.model, refd, ref, outroot) for t in spec['tasks'] for i in range(a.k)
            if (t['id'], i) not in done]
    print(f'{len(jobs)} jobs ({a.model}, k={a.k})')
    with ThreadPoolExecutor(a.workers) as ex, open(out, 'a') as f:
        for r in ex.map(run, jobs):
            f.write(json.dumps(r, ensure_ascii=False) + '\n'); f.flush()
            print(f"  {r['task']:24s} s{r['i']} {r.get('verdict') or r.get('err')}", flush=True)
    report()


def report():
    import collections
    rows = [json.loads(l) for l in open(HERE / 'runs/passk/results.jsonl')]
    rows = {(r['task'], r['i']): r for r in rows}.values()
    ok = collections.Counter(); tot = collections.Counter()
    for r in rows:
        if r['verdict'] is None: continue      # 基础设施故障剔除
        tot[r['task']] += 1; ok[r['task']] += r['verdict'] == 'pass'
    print(f"\n{'任务':24s} 通过/采样")
    band = collections.Counter()
    for t in sorted(tot, key=lambda t: ok[t] / tot[t]):
        p = ok[t] / tot[t]
        print(f'  {t:24s} {ok[t]}/{tot[t]} = {p:.2f}')
        band['全错' if p == 0 else ('全对' if p == 1 else '中间')] += 1
        band['带内 0.3~0.7'] += 1 if 0.3 <= p <= 0.7 else 0
    n = len(tot)
    print(f"\n剔除全对与全错后留存 {band['中间']}/{n} = {band['中间'] / n:.0%}")
    print(f"只留 0.3 到 0.7 带内 {band['带内 0.3~0.7']}/{n} = {band['带内 0.3~0.7'] / n:.0%}")


if __name__ == '__main__':
    main()

