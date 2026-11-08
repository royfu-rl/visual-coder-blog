"""python3 solve.py <task_dir> [--models m1,m2] [--rounds 3] [--conds none,page,multi,graph]

让模型修复自动生成的「坏掉的」three.js 页面，比较四种反馈条件下的通过率：
  none   只给需求和源码，一次成型，无任何反馈
  page   每轮回传页面自带相机的一张渲染图
  multi  每轮回传 verifier 的 4 个视角（正面/侧面/背面/俯视）拼图
  graph  每轮回传场景图文本（物体列表 + 包围盒 + 颜色），不给图
  oracle 每轮回传多视角拼图，外加 verifier 判出的那一层的名字（只给层名，不给阈值也不给数值）
         用来区分「模型改不动」和「模型看不出」：如果只要有人指出哪一类不对它就能修好，
         那瓶颈在判别而不在生成
每轮都用同一个 verifier 判定；通过即停。统计首轮通过率与 K 轮后的通过率。
reward 只来自 verifier，模型看不到 verifier 的判定理由（避免它照着指标改）。
"""
import argparse, base64, io, json, re, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests
from PIL import Image
import compare, verify

HERE = Path(__file__).parent
URL, KEY = 'http://klink.internal/v1/chat/completions', 'sk-klink-MJFlh5vNbu2Rnujem807KsvGhk7lhJ6O'
VIEWS = [1, 3, 5, 9]

SYS = """你在修复一个 three.js 页面。页面能跑、不报错，但渲染出的 3D 场景在语义上是错的。
按需求把场景改对。只改必要的地方，不要重写整个页面，也不要改背景、光照、相机机位和网格精细度。
每次回复都必须输出完整的、可直接运行的 HTML，放在 ```html 代码块里。"""


def shot(run_dir, cond):
    idx = [0] if cond == 'page' else VIEWS
    S = 320
    im = Image.new('RGB', (S * len(idx), S), 'white')
    for c, i in enumerate(idx):
        im.paste(Image.open(run_dir / f'rgb_{i}.png').resize((S, S)), (c * S, 0))
    b = io.BytesIO(); im.save(b, 'PNG')
    return base64.b64encode(b.getvalue()).decode()


def graph_text(p):
    L = [f"渲染调用 {p['renders']} 次，灯光 {p['lights']}，网格 {len(p['meshes'])} 个："]
    for m in p['meshes']:
        mn, mx = [round(v, 3) for v in m['min']], [round(v, 3) for v in m['max']]
        L.append(f"  {m['geo']:18s} 颜色 {m['color']}  包围盒 min={mn} max={mx}")
    return '\n'.join(L)


def call(model, msgs):
    body = {'model': model, 'max_tokens': 20000, 'temperature': 0.3, 'messages': msgs}
    for k in range(4):
        try:
            # 超时砍短比放长管用：网关偶发挂死时长超时会把整批拖住，短超时重试反而更快收敛
            r = requests.post(URL, json=body, headers={'Authorization': 'Bearer ' + KEY}, timeout=300,
                              proxies={'http': None, 'https': None})
            t = r.json()['choices'][0]['message']['content'] or ''
            m = re.search(r'```html\s*(.*?)```', t, re.S)
            if m: return m.group(1).strip(), t
        except Exception as e:
            t = repr(e)
        time.sleep(5 * (k + 1))
    return None, t[-300:]


def run_one(args):
    task, model, cond, rounds, ref_dir, ref, outroot, spec = args
    tag = f"{task['id']}|{model}|{cond}|{spec}"
    work = outroot / model.replace('/', '_') / f'{spec}-{cond}' / task['id']
    work.mkdir(parents=True, exist_ok=True)
    src = Path(task['start']).read_text()
    ask = f"需求：{task['request']}\n\n当前页面源码：\n```html\n{src}\n```"
    if spec == 'img':
        content = [{'type': 'text', 'text': '下图是**正确**场景应该长的样子（正面、侧面、背面、俯视四个视角）。'
                                            '请让页面渲染出与图一致的场景。'},
                   {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,' + shot(ref_dir, 'multi')}},
                   {'type': 'text', 'text': ask}]
    else:
        content = ask
    msgs = [{'role': 'system', 'content': SYS}, {'role': 'user', 'content': content}]
    hist = []
    for rd in range(rounds if cond != 'none' else 1):
        code, raw = call(model, msgs)
        if code is None:
            hist.append(dict(round=rd, error=raw)); break
        f = work / f'try{rd}.html'; f.write_text(code)
        try:
            cand = compare.probe(f, work / f'r{rd}', ref_dir / 'probe.json')
            v = verify.verify(ref_dir, ref, work / f'r{rd}', cand)
        except Exception as e:
            hist.append(dict(round=rd, error=repr(e)[:200])); break
        hist.append(dict(round=rd, verdict=v['verdict'], layer=v['layer'], signals=v['signals']))
        print(f"  {tag} r{rd} -> {v['verdict']} ({v['layer']})", flush=True)
        if v['verdict'] == 'pass' or rd == rounds - 1 or cond == 'none':
            break
        msgs.append({'role': 'assistant', 'content': f'```html\n{code}\n```'})
        if cond == 'oracle':
            LAY = {'L0': '页面报错或没渲染出东西', 'L1': '物体的外形轮廓不对',
                   'L2': '物体的占位或颜色不对', 'L2b': '物体互相穿插或共面闪烁',
                   'L3': '部件的数量、体积或连通关系不对'}
            fb = [{'type': 'text', 'text': '你刚才那版没有通过验收。验收只告诉你一句话：'
                   + LAY.get(v['layer'], v['layer'])
                   + '。下面是它的渲染结果（正面、侧面、背面、俯视）。请据此给出修正后的完整 HTML：'},
                  {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,' + shot(work / f'r{rd}', 'multi')}}]
        elif cond == 'graph':
            fb = [{'type': 'text', 'text': '这是你刚才那版渲染出来的场景结构，请自己判断哪里还不对，然后给出修正后的完整 HTML：\n' + graph_text(cand)}]
        else:
            note = '这是你刚才那版的渲染结果（正面、侧面、背面、俯视）。' if cond == 'multi' else '这是你刚才那版的渲染结果（页面自带相机）。'
            fb = [{'type': 'text', 'text': note + '请自己判断哪里还不对，然后给出修正后的完整 HTML：'},
                  {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,' + shot(work / f'r{rd}', cond)}}]
        msgs.append({'role': 'user', 'content': fb})
    return dict(task=task['id'], model=model, cond=cond, spec=spec, rounds=len(hist),
                first=hist[0].get('verdict') if hist else None,
                final=hist[-1].get('verdict') if hist else None, hist=hist)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('task_dir'); ap.add_argument('--models', default='claude-opus-5-5,gpt-6-astra,gemini-3.8-flash,qwen3.8-max')
    ap.add_argument('--rounds', type=int, default=3)
    ap.add_argument('--conds', default='none,page,multi,graph')
    ap.add_argument('--workers', type=int, default=10)
    ap.add_argument('--specs', default='text,img')
    a = ap.parse_args()

    td = Path(a.task_dir); spec = json.load(open(td / 'tasks.json'))
    runs = HERE / 'runs' / td.name
    ref = json.load(open(runs / 'ref/probe.json'))
    outroot = HERE / 'runs' / f'{td.name}_solve'
    out = outroot / 'results.jsonl'; outroot.mkdir(parents=True, exist_ok=True)
    done = {(j['task'], j['model'], j['cond'], j.get('spec', 'text')) for j in map(json.loads, open(out))} if out.exists() else set()

    jobs = [(t, m, c, a.rounds, runs / 'ref', ref, outroot, sp)
            for t in spec['tasks'] for m in a.models.split(',') for c in a.conds.split(',') for sp in a.specs.split(',')
            if (t['id'], m, c, sp) not in done]
    print(f'{len(jobs)} jobs')
    with ThreadPoolExecutor(a.workers) as ex, open(out, 'a') as f:
        for r in ex.map(run_one, jobs):
            f.write(json.dumps(r, ensure_ascii=False) + '\n'); f.flush()
    report(outroot)


def report(outroot):
    rows = [json.loads(l) for l in open(outroot / 'results.jsonl')]
    models = sorted({r['model'] for r in rows}); conds = ['none', 'page', 'multi', 'graph']
    print(f"\n{'模型':20s} {'spec':5s} " + ' '.join(f'{c:>14s}' for c in conds))
    for m in models:
      for sp in ['text', 'img']:
        cells = []
        for c in conds:
            rs = [r for r in rows if r['model'] == m and r['cond'] == c and r.get('spec', 'text') == sp]
            if not rs: cells.append(f'{"-":>14s}'); continue
            fin = sum(r['final'] == 'pass' for r in rs); fir = sum(r['first'] == 'pass' for r in rs)
            cells.append(f'{fir}->{fin}/{len(rs):<9d}'[:14].rjust(14))
        if any('-' != x.strip() for x in cells): print(f'{m:20s} {sp:5s} ' + ' '.join(cells))
    print('\n格式：首轮通过 -> 末轮通过 / 任务数')


if __name__ == '__main__':
    main()

