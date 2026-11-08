"""python3 gen_tasks.py <ref.html> <out_task_dir> [n]

自动把一个能跑的 three.js 页面变成一批「修复型」可验证任务：
  1. 让 LLM 读源码，提出 n 个**语义性破坏**（SEARCH/REPLACE），并写出用户视角的需求描述
  2. 应用破坏 → 生成 broken.html
  3. 准入测试（三条都要过，否则丢弃）：
       a. 参考解必须过 verifier
       b. broken 必须被 verifier 判挂（否则这个破坏不可验证，等于没破坏）
       c. 把 broken 改回参考解必须过（反向可解性，天然成立，用于回归自检）
  4. 落盘 task.json：需求描述 + 起始代码 + 参考解 + verifier 配置
产出的每个任务都带「初始态必挂、参考解必过」的证据，这就是 Verified Task 的准入。
"""
import json, re, sys
from pathlib import Path
import requests
import compare, verify

HERE = Path(__file__).parent
URL, KEY = 'http://klink.internal/v1/chat/completions', 'sk-klink-MJFlh5vNbu2Rnujem807KsvGhk7lhJ6O'
MODEL = 'claude-opus-5-5'

PROMPT = """下面是一个能正常运行的 three.js 页面源码。请提出 {n} 个互不相同的**语义性破坏**，
每个破坏后的页面仍然能运行、不报错，但渲染出的 3D 场景在语义上错了（部件缺失、位置错、朝向错、
比例错、颜色错、层级错等）。不要改成一眼就崩的东西，也不要只改背景、光照强度、网格精细度、
相机机位这类不影响场景语义的属性。

对每个破坏输出一个对象：
  id      短横线小写英文名
  search  源码中要被替换的片段，必须和源码逐字符一致，且在源码中唯一
  replace 替换成的片段
  defect  一句话说明破坏后场景错在哪（给出题用，不给模型看）
  request 用户视角的修复需求，只描述期望的正确状态，**不要提到具体代码、数值或 API 名**

只输出一个 JSON 数组，不要别的内容。

源码：
```html
{src}
```"""


def ask(src, n):
    body = {'model': MODEL, 'max_tokens': 16000, 'temperature': 0.7,
            'messages': [{'role': 'user', 'content': PROMPT.format(n=n, src=src)}]}
    r = requests.post(URL, json=body, headers={'Authorization': 'Bearer ' + KEY}, timeout=600,
                      proxies={'http': None, 'https': None})
    txt = r.json()['choices'][0]['message']['content']
    m = re.search(r'\[.*\]', txt, re.S)
    return json.loads(m.group(0))


def main(ref_path, out_dir, n=10):
    ref_path, out = Path(ref_path), Path(out_dir)
    (out / 'broken').mkdir(parents=True, exist_ok=True)
    src = ref_path.read_text()
    (out / 'ref.html').write_text(src)

    runs = HERE / 'runs' / out.name
    ref = compare.probe(out / 'ref.html', runs / 'ref')
    self_check = verify.verify(runs / 'ref', ref, runs / 'ref', ref)
    assert self_check['verdict'] == 'pass', '参考解自比都不过，verifier 坏了'

    props = ask(src, n)
    print(f'LLM 提了 {len(props)} 个破坏')
    tasks, rejected = [], []
    for p in props:
        if p['search'] not in src or src.count(p['search']) != 1:
            rejected.append((p['id'], 'search 片段不唯一或不存在')); continue
        broken = src.replace(p['search'], p['replace'], 1)
        bp = out / 'broken' / f"{p['id']}.html"; bp.write_text(broken)
        v = verify.probe_and_verify(runs / 'ref', ref, bp, runs / f"b_{p['id']}")
        if v['verdict'] != 'fail':
            rejected.append((p['id'], f"verifier 没判挂（{v['signals']}）")); continue
        tasks.append(dict(id=p['id'], request=p['request'], defect=p['defect'],
                          start=str(bp), ref=str(out / 'ref.html'),
                          admit=dict(ref_pass=True, broken_fail_at=v['layer'], signals=v['signals'])))
        print(f"  收 {p['id']:22s} 挂在 {v['layer']}  mv={v['signals']['mv_min']} blk={v['signals'].get('blk_min')}")
    for i, why in rejected:
        print(f"  弃 {i:22s} {why}")
    json.dump(dict(ref=str(out / 'ref.html'), tasks=tasks, rejected=rejected),
              open(out / 'tasks.json', 'w'), indent=1, ensure_ascii=False)
    print(f'收 {len(tasks)} / 提 {len(props)}')


if __name__ == '__main__':
    a = sys.argv[1:]
    main(a[0], a[1], int(a[2]) if len(a) > 2 else 10)

