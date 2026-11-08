#!/usr/bin/env python3
"""把 arXiv HTML 全文抓下来转纯文本，供本地精读。

用法: python fetch_arxiv.py 2503.13377 2504.06958 ...
输出: middle_processing/papers/<id>.txt
"""
import os, re, sys, html, urllib.request, concurrent.futures

OUT = "/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/papers"
PROXY = "http://oversea-squid1.jp.txyun:11080"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"

opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
)
opener.addheaders = [("User-Agent", UA)]


def to_text(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style|svg)\b.*?</\1>", " ", raw)
    raw = re.sub(r"(?is)<math\b[^>]*alttext=\"(.*?)\".*?</math>", r" $\1$ ", raw)
    raw = re.sub(r"(?is)<math\b.*?</math>", " ", raw)
    raw = re.sub(r"(?i)</(p|div|tr|li|h[1-6]|section|table)>", "\n", raw)
    raw = re.sub(r"(?i)</t[dh]>", " | ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    raw = re.sub(r"[ \t\xa0]+", " ", raw)
    raw = re.sub(r"\n\s*\n+", "\n", raw)
    return raw.strip()


def grab(pid: str) -> str:
    last = None
    for ver in ("v3", "v2", "v1", ""):
        url = f"https://arxiv.org/html/{pid}{ver}"
        try:
            with opener.open(url, timeout=90) as r:
                if r.status != 200:
                    continue
                body = r.read().decode("utf-8", "ignore")
            if len(body) < 20000:  # 多半是占位/无 HTML 版
                continue
            txt = to_text(body)
            with open(os.path.join(OUT, f"{pid}.txt"), "w") as f:
                f.write(txt)
            return f"OK   {pid} {ver or 'latest':>6}  {len(txt)//1000}k chars"
        except Exception as e:
            last = e
    return f"FAIL {pid}  {type(last).__name__}: {last}"


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for line in ex.map(grab, sys.argv[1:]):
            print(line)

