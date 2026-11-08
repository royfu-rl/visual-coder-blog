#!/usr/bin/env python3
"""Algorithm 页引用复核：draft_*.md 里的每条链接实测一遍，并找出「带数字但没给出处」的句子。

python3 scripts/check_alg_refs.py            # 全部视图
python3 scripts/check_alg_refs.py overview   # 只查一个视图
结果写到 middle_processing/vc_data/ref_check.md
"""
import concurrent.futures as cf
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'middle_processing/vc_data'
OUT = SRC / 'ref_check.md'
VIEWS = ['overview', 'tasks', 'verifier', 'training', 'domains']
PROXY = 'http://oversea-squid2.ko.txyun:11080'
LINK = re.compile(r'\[([^\]]+)\]\((https?://[^)\s]+)\)')
LOCAL = 'kml-dtmachine'   # 本项目 /view 链接：查文件在不在盘上，不走网络


def curl(url, *extra):
    env = {**os.environ, 'https_proxy': PROXY, 'http_proxy': PROXY}
    r = subprocess.run(['curl', '-sL', '--max-time', '25', *extra, url], env=env, capture_output=True, text=True)
    return r.stdout


def check(url):
    if LOCAL in url:
        path = '/' + url.split('/view/', 1)[1].split('#')[0]
        return ('ok' if Path(path).exists() else 'missing'), path
    m = re.match(r'https?://arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})', url)
    if m:   # 读 abs 页标题；export API 一并发就限流、返回空
        for _ in range(3):
            t = re.search(r'<title>\[[^\]]+\]\s*([^<]+)', curl(f'https://arxiv.org/abs/{m.group(1)}'))
            if t:
                return 'ok', ' '.join(t.group(1).split())
            time.sleep(5)
        return 'bad', 'no title'
    code = curl(url, '-o', '/dev/null', '-w', '%{http_code}').strip()
    return ('ok' if code[:1] in '23' else 'cli' + code if code in ('401', '403', '429') else 'bad'), code


def unsourced(text):
    """含数字、却没有任何链接的句子 / 表格行（跳过标题、锚点、参考文献节）。"""
    hits, refs = [], False
    for no, line in enumerate(text.split('\n'), 1):
        if line.startswith('## '):
            refs = '参考文献' in line
            continue
        if refs or not line.strip() or line.startswith(('#', '<', '|---', '| ---')):
            continue
        units = [line] if line.startswith('|') else re.split(r'(?<=[。；！？])', line)
        for u in units:
            if re.search(r'\d', u) and not LINK.search(u) and len(u.strip()) > 12:
                hits.append((no, u.strip()[:110]))
    return hits


def main():
    views = sys.argv[1:] or VIEWS
    links, report = {}, ['# Algorithm 页引用复核', '']
    texts = {v: (SRC / f'draft_{v}.md').read_text() for v in views}
    for v, t in texts.items():
        for label, url in LINK.findall(t):
            links.setdefault(url, set()).add((v, label))
    with cf.ThreadPoolExecutor(4) as ex:
        res = dict(zip(links, ex.map(check, links)))
    bad = {u: r for u, r in res.items() if r[0] != 'ok'}
    report += [f'- 链接 {sum(len(LINK.findall(t)) for t in texts.values())} 处，不同 URL {len(links)} 个，'
               f'实测通过 {len(links) - len(bad)}，未通过 {len(bad)}', '']
    report += ['## 未通过的链接', '', '| 状态 | URL | 出现在 |', '|---|---|---|']
    report += [f'| {s} {d} | {u} | {", ".join(sorted(v for v, _ in links[u]))} |' for u, (s, d) in sorted(bad.items())]
    report += ['', '## arXiv 标题（人工核对与引用名是否同一篇）', '', '| 引用名 | 编号 | 实测标题 |', '|---|---|---|']
    for u, (s, d) in sorted(res.items()):
        if 'arxiv.org' in u and s == 'ok':
            report.append(f'| {" / ".join(sorted({l for _, l in links[u]}))[:60]} | {u.rsplit("/", 1)[1]} | {d[:90]} |')
    for v, t in texts.items():
        h = unsourced(t)
        report += ['', f'## {v}：带数字但没有链接（{len(h)} 处）', '']
        report += [f'- L{n}: {s}' for n, s in h]
    OUT.write_text('\n'.join(report) + '\n')
    print('\n'.join(report[:3]))
    print(f'未通过 {len(bad)}；未给出处：' + '，'.join(f'{v} {len(unsourced(t))}' for v, t in texts.items()))
    print(f'详见 {OUT}')


if __name__ == '__main__':
    main()

