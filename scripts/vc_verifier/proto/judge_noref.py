"""python3 judge_noref.py

VLM judge 在**没有参考图**时还剩多少判别力。
前面量过的是「参考与候选并排」这一档；这里加一档「只看候选 + 一段文字需求」。
两档用同一批带标签的 case、同一批 judge、同样跑两次。

要回答的问题和求解实验那边是同一个：判别靠的是可比对象，还是靠模型自己的知识。
"""
import base64, io, json, re, sys, time, collections
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests
from PIL import Image

HERE = Path(__file__).parent
RUNS = HERE / 'runs'
URL, KEY = 'http://klink.internal/v1/chat/completions', 'sk-klink-MJFlh5vNbu2Rnujem807KsvGhk7lhJ6O'
JUDGES = ['gpt-6-astra', 'gemini-3.8-flash']   # 网关慢，收窄到两个最强的 judge
VIEWS = [1, 3, 5, 9]

DESC = {
 'snowman': '一个雪人：三个白色的球由大到小叠起来，最上面那个是头，头的正前方有一个橙色的胡萝卜鼻子横着伸出来。',
 'table': '一张木色的桌子：一块桌面加四条圆柱形的桌腿，分布在四角；桌面上放一个蓝色的圆柱形杯子。',
 'car': '一辆红色的小车：下面是扁长的底盘，上面偏后是车厢；车厢前端有一块浅蓝色的斜置风挡；左右各两个黑色轮子；车头前端有两个浅黄色的圆形前灯。',
}
PROMPT = """你是 3D 场景的验收员。下面的图是一个场景的 {nv}，需求是：

{desc}

算对：需求里点名的部件都在、形状和相对位置合理、点名的颜色对得上。
不算错：光照强弱、背景、相机取景角度、网格精细度、颜色的轻微色差、需求里没写的尺寸细节。

只输出一行 JSON：{{"verdict": "pass" 或 "fail", "reason": "一句话"}}"""


def cases():
    out = []
    for task, scene in [('snowman_mut', 'snowman'), ('table_mut', 'table'), ('car_mut', 'car')]:
        for r in json.load(open(RUNS / task / 'mutation.json')):
            out.append((task, scene, r['name'], r['should']))
    return out


def sheet(task, name, cond):
    idx = [0] if cond == 'single' else VIEWS
    S = 300
    im = Image.new('RGB', (S * len(idx), S), 'white')
    for c, i in enumerate(idx):
        im.paste(Image.open(RUNS / task / name / f'rgb_{i}.png').resize((S, S)), (c * S, 0))
    b = io.BytesIO(); im.save(b, 'PNG')
    return base64.b64encode(b.getvalue()).decode()


def ask(model, img, cond, desc):
    nv = '一张渲染图' if cond == 'single' else '四个视角的渲染图（正面、侧面、背面、俯视）'
    body = {'model': model, 'max_tokens': 4000, 'temperature': 0,
            'messages': [{'role': 'user', 'content': [
                {'type': 'text', 'text': PROMPT.format(nv=nv, desc=desc)},
                {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,' + img}}]}]}
    for k in range(3):
        try:
            r = requests.post(URL, json=body, headers={'Authorization': 'Bearer ' + KEY}, timeout=200,
                              proxies={'http': None, 'https': None})
            t = r.json()['choices'][0]['message']['content'] or ''
            m = re.search(r'"verdict"\s*:\s*"(pass|fail)"', t)
            if m: return m.group(1), t[-180:]
        except Exception as e:
            t = repr(e)
        time.sleep(4 * (k + 1))
    return None, t[-180:]


def main():
    out = RUNS / 'judge_noref.jsonl'
    done = set()
    if out.exists():
        for l in open(out):
            j = json.loads(l); done.add((j['task'], j['name'], j['cond'], j['model'], j['rep']))
    jobs = []
    for task, scene, name, should in cases():
        for cond in ['single', 'multi']:
            img = sheet(task, name, cond)
            for m in JUDGES:
                for rep in range(1):
                    if (task, name, cond, m, rep) in done: continue
                    jobs.append((task, scene, name, should, cond, m, rep, img))
    print(f'{len(jobs)} jobs')

    def go(j):
        task, scene, name, should, cond, m, rep, img = j
        v, raw = ask(m, img, cond, DESC[scene])
        return dict(task=task, name=name, should=should, cond=cond, model=m, rep=rep, verdict=v, raw=raw)

    with ThreadPoolExecutor(16) as ex, open(out, 'a') as f:
        for r in ex.map(go, jobs):
            f.write(json.dumps(r, ensure_ascii=False) + '\n'); f.flush()
    report()


def report():
    rows = [json.loads(l) for l in open(RUNS / 'judge_noref.jsonl')]
    print(f"\n{'judge':20s} {'单视角':>10s} {'多视角':>10s}")
    for m in JUDGES:
        cells = []
        for c in ['single', 'multi']:
            rs = [r for r in rows if r['model'] == m and r['cond'] == c and r['verdict']]
            cells.append(f"{sum(r['verdict'] == r['should'] for r in rs)}/{len(rs)}".rjust(10))
        print(f'{m:20s} ' + ' '.join(cells))
    for c in ['single', 'multi']:
        ok = tot = 0
        for name in sorted({r['name'] for r in rows}):
            vs = [r['verdict'] for r in rows if r['name'] == name and r['cond'] == c and r['verdict']]
            if not vs: continue
            sh = next(r['should'] for r in rows if r['name'] == name)
            ok += ('pass' if vs.count('pass') > vs.count('fail') else 'fail') == sh; tot += 1
        print(f'  8 票多数投票 {c}: {ok}/{tot}')


if __name__ == '__main__':
    report() if sys.argv[1:] == ['report'] else main()

