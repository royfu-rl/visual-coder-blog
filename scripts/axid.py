#!/usr/bin/env python3
"""给 arXiv id 列表，打印 标题 / 提交日期。用法: axid.py 2412.21139 ..."""
import sys, re, html, requests, concurrent.futures
P={"http":"http://oversea-squid1.jp.txyun:11080","https":"http://oversea-squid1.jp.txyun:11080"}
def one(pid):
    s=requests.Session(); s.trust_env=False
    try:
        t=s.get(f"https://arxiv.org/abs/{pid}",proxies=P,timeout=60,
                headers={"User-Agent":"Mozilla/5.0"}).text
    except Exception as e: return f"{pid} ERR {e}"
    ti=re.search(r'(?s)<meta name="citation_title" content="(.*?)"',t)
    dt=re.search(r'(?s)<meta name="citation_date" content="(.*?)"',t)
    sub=re.search(r'(?s)Submitted on\s*([^<(]+)',t)
    return f"{pid:16s} {(dt.group(1) if dt else '?'):12s} {(sub.group(1).strip() if sub else '')[:24]:24s} {html.unescape(ti.group(1)) if ti else 'NOT FOUND'}"
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
    for l in ex.map(one, sys.argv[1:]): print(l)

