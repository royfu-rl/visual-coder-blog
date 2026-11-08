"""python3 vlm_judge.py
VLM judge 对照：同一批候选（snowman 5 个 + 13 个变异），两种看图条件
  single  参考 vs 候选，各一张页面相机视角（最常见的「截图 + VLM 打分」）
  multi   参考 vs 候选，各 4 个 verifier 视角（正面 / 侧面 / 背面 / 俯视）拼图
每个 judge × 条件 × 重复 2 次，统计判对率与两次一致率。should 标签与 mutate.py 相同。
"""
import base64, io, json, re, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests
from PIL import Image, ImageDraw

HERE = Path(__file__).parent
RUNS = HERE / 'runs'
URL, KEY = 'http://klink.internal/v1/chat/completions', 'sk-klink-MJFlh5vNbu2Rnujem807KsvGhk7lhJ6O'
JUDGES = ['gpt-6-astra', 'claude-opus-5-5', 'gemini-3.8-flash', 'doubao-seed-2.1-pro']
VIEWS = [1, 3, 5, 9]          # harness 里的视角编号：方位 0°、90°、180°、俯视
PROMPT = """你是 3D 场景复现任务的验收员。任务：候选场景要复现参考场景里的 3D 物体。
算对：物体形状、各部件的相对位置和大小、部件颜色一致。
不算错：光照强弱、背景、相机取景角度、网格精细度、颜色的轻微色差、代码写法。
图中上半部分是参考，下半部分是候选。{extra}
只输出一行 JSON：{{"verdict": "pass" 或 "fail", "reason": "一句话"}}"""

# ok_lathe 最初标成 pass（以为只是换了建模手法），后来放大俯视图确认 LatheGeometry 在极点没封口，
# 头顶真有一个洞。标签改成 fail；程序化 verifier 补了开放边界边数之后也判挂。
SHOULD = {'ref': 'pass', 'ok_restyled': 'pass', 'ok_lathe': 'fail',
          'flat_cutout': 'fail', 'nose_back': 'fail', 'wrong_layout': 'fail'}


def cases():
    out = [('snowman', k, v) for k, v in SHOULD.items() if k != 'ref']
    for t in ['snowman_mut', 'table_mut']:
        for r in json.load(open(RUNS / t / 'mutation.json')):
            out.append((t, r['name'], r['should']))
    # desk 自动生成的 16 个缺陷，全部 should=fail（已通过准入测试）
    for t in json.load(open(HERE / 'tasks/desk_gen/tasks.json'))['tasks']:
        out.append(('desk_gen', 'b2_' + t['id'], 'fail'))
    return out


def sheet(task, name, cond):
    ref_dir = 'ref'
    idx = [0] if cond == 'single' else VIEWS
    S = 256; im = Image.new('RGB', (S * len(idx), 2 * S + 40), 'white'); d = ImageDraw.Draw(im)
    for row, who in enumerate(['ref', name]):
        for c, i in enumerate(idx):
            im.paste(Image.open(RUNS / task / who / f'rgb_{i}.png').resize((S, S)), (c * S, 20 + row * (S + 20)))
    d.text((4, 4), 'REFERENCE', fill='black'); d.text((4, S + 24), 'CANDIDATE', fill='black')
    buf = io.BytesIO(); im.save(buf, 'PNG'); return base64.b64encode(buf.getvalue()).decode()


def ask(model, img, cond):
    extra = '每行四张分别是：正面、侧面(90°)、背面、俯视。' if cond == 'multi' else '每部分是同一个页面相机的一张截图。'
    body = {'model': model, 'max_tokens': 4000, 'temperature': 0,
            'messages': [{'role': 'user', 'content': [
                {'type': 'text', 'text': PROMPT.format(extra=extra)},
                {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,' + img}}]}]}
    for k in range(4):
        try:
            r = requests.post(URL, json=body, headers={'Authorization': 'Bearer ' + KEY}, timeout=180,
                              proxies={'http': None, 'https': None})
            txt = r.json()['choices'][0]['message']['content'] or ''
            m = re.search(r'"verdict"\s*:\s*"(pass|fail)"', txt)
            if m: return m.group(1), txt[-200:]
        except Exception as e:
            txt = repr(e)
        time.sleep(3 * (k + 1))
    return None, txt[-200:]


def main():
    jobs = []
    for task, name, should in cases():
        for cond in ['single', 'multi']:
            img = sheet(task, name, cond)
            for model in JUDGES:
                for rep in range(2):
                    jobs.append((task, name, should, cond, model, rep, img))
    out = HERE / 'runs/vlm_judge.jsonl'
    done = set()
    if out.exists():
        for l in open(out):
            j = json.loads(l); done.add((j['name'], j['cond'], j['model'], j['rep']))
    todo = [j for j in jobs if (j[1], j[3], j[4], j[5]) not in done]
    print(len(jobs), 'jobs,', len(todo), 'todo')

    def go(j):
        task, name, should, cond, model, rep, img = j
        v, txt = ask(model, img, cond)
        return dict(task=task, name=name, should=should, cond=cond, model=model, rep=rep, verdict=v, raw=txt)

    with ThreadPoolExecutor(12) as ex, open(out, 'a') as f:
        for r in ex.map(go, todo):
            f.write(json.dumps(r, ensure_ascii=False) + '\n'); f.flush()
    report()


def report():
    rows = [json.loads(l) for l in open(HERE / 'runs/vlm_judge.jsonl')]
    for model in JUDGES:
        for cond in ['single', 'multi']:
            rs = [r for r in rows if r['model'] == model and r['cond'] == cond]
            ok = sum(r['verdict'] == r['should'] for r in rs); none = sum(r['verdict'] is None for r in rs)
            pairs = {}
            for r in rs: pairs.setdefault(r['name'], []).append(r['verdict'])
            agree = sum(len(set(v)) == 1 for v in pairs.values())
            print(f'{model:18s} {cond:6s} 判对 {ok}/{len(rs)}  未解析 {none}  两次一致 {agree}/{len(pairs)}')


if __name__ == '__main__':
    report() if sys.argv[1:] == ['report'] else main()

