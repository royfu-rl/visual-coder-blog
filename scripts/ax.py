#!/usr/bin/env python3
"""arXiv API 搜题名 -> id/date。用法: ax.py "title words" ..."""
import sys, re, html, urllib.parse, requests
P={"http":"http://oversea-squid1.jp.txyun:11080","https":"http://oversea-squid1.jp.txyun:11080"}
S=requests.Session(); S.trust_env=False
for q in sys.argv[1:]:
    u="http://export.arxiv.org/api/query?"+urllib.parse.urlencode(
        {"search_query":f'all:"{q}"',"start":0,"max_results":4})
    try:
        r=S.get(u,proxies=P,timeout=60).text
    except Exception as e:
        print("ERR",q,e); continue
    print("### Q:",q)
    for e in re.findall(r"(?s)<entry>(.*?)</entry>",r):
        t=re.sub(r"\s+"," ",html.unescape(re.search(r"(?s)<title>(.*?)</title>",e).group(1))).strip()
        i=re.search(r"<id>http://arxiv.org/abs/([^<]+)</id>",e).group(1)
        d=re.search(r"<published>([^<]+)</published>",e).group(1)[:10]
        print(f"  {i:22s} {d}  {t[:95]}")

