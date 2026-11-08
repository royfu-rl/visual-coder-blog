#!/usr/bin/env python3
"""Market 页的 demo 卡片墙：验证 → 生成。

  python3 scripts/market_demos.py verify   # 逐条验原站可达、封面是真图，落 market/posters/ 与 demos_verify.json
  python3 scripts/market_demos.py render   # 把通过验证的条目渲染成卡片，写进 market.md 的 <!--DEMOS:tab--> 标记之间

数据：middle_processing/market/demos_<tab>.json（title, maker, url, image, caption, heat, heat_src, commercial, tech）
无封面或原站拒绝脚本访问的，由 scripts/market_shot.js 用无头浏览器补截图 / 补验证。
"""
import html
import io
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor

import requests
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MID = os.path.join(ROOT, "middle_processing", "market")
POSTERS = os.path.join(ROOT, "market", "posters")
MD = os.path.join(ROOT, "market", "market.md")
STATUS = os.path.join(MID, "demos_verify.json")
TABS = ["asset", "game", "ad", "web", "industry"]

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/148.0 Safari/537.36")
PROXIES = [  # 海外 squid → 国内代理 → 直连，逐个试
    {"http": "http://oversea-squid1.jp.txyun:11080", "https": "http://oversea-squid1.jp.txyun:11080"},
    {"http": "http://10.68.24.18:11080", "https": "http://10.68.24.18:11080"},
    None,
]


def get(url, timeout=25):
    last = None
    for px in PROXIES:
        s = requests.Session()
        s.trust_env = False
        try:
            r = s.get(url, headers={"User-Agent": UA}, proxies=px, timeout=timeout, allow_redirects=True)
            if r.status_code < 400:
                return r
            last = r
        except requests.RequestException as e:
            last = e
    return last


def check_page(url):
    r = get(url)
    if isinstance(r, requests.Response):
        return r.status_code, r.status_code < 400
    return str(r)[:80], False


def fetch_image(src, dest):
    r = get(src)
    if not isinstance(r, requests.Response) or r.status_code >= 400:
        return f"img-fail {getattr(r, 'status_code', r)}"
    try:
        im = Image.open(io.BytesIO(r.content)).convert("RGB")
    except Exception as e:
        return f"not-image {type(e).__name__}"
    if im.width < 400 or im.height < 200:
        return f"too-small {im.width}x{im.height}"
    # YouTube 无 maxres 时返回 120x90 灰图，上面已被 too-small 拦掉
    im.thumbnail((960, 960))
    im.save(dest, "JPEG", quality=82)
    return "ok"


def verify():
    os.makedirs(POSTERS, exist_ok=True)
    old = json.load(open(STATUS)) if os.path.exists(STATUS) else {}
    jobs = []
    for tab in TABS:
        p = os.path.join(MID, f"demos_{tab}.json")
        if not os.path.exists(p):
            continue
        for i, d in enumerate(json.load(open(p))):
            jobs.append((tab, i, d))

    def one(job):
        tab, i, d = job
        key = f"{tab}-{i:02d}"
        dest = os.path.join(POSTERS, key + ".jpg")
        page_code, page_ok = check_page(d["url"])
        img = fetch_image(d["image"], dest) if d.get("image") else "no-image"
        prev = old.get(key, {})
        # 浏览器补验 / 补截图的结论保留，除非 url 变了
        if prev.get("url") == d["url"]:
            page_ok = page_ok or prev.get("browser_ok", False)
            if img != "ok" and prev.get("shot_ok"):
                img = "shot"
        return key, {"tab": tab, "title": d["title"], "url": d["url"], "page": page_code,
                     "page_ok": page_ok, "img": img,
                     "browser_ok": prev.get("browser_ok", False) if prev.get("url") == d["url"] else False,
                     "shot_ok": prev.get("shot_ok", False) if prev.get("url") == d["url"] else False}

    with ThreadPoolExecutor(12) as ex:
        res = dict(ex.map(one, jobs))
    json.dump(res, open(STATUS, "w"), ensure_ascii=False, indent=1)
    bad = {k: v for k, v in res.items() if not (v["page_ok"] and v["img"] in ("ok", "shot"))}
    print(f"{len(res)} items, {len(res) - len(bad)} pass, {len(bad)} need work")
    for k, v in bad.items():
        print(f"  {k}  page={v['page']}  img={v['img']}  {v['title']}  {v['url']}")


CARD = ('<a class="gal-card mk-card" href="{url}" target="_blank" rel="noopener">'
        '<div class="gal-poster" style="background:url(\'market/posters/{key}.jpg\') center/cover no-repeat,#1b1f27">'
        '<span class="gal-play">↗ 打开原站</span></div>'
        '<div class="gal-meta"><div class="gal-cn">{title}</div>'
        '<div class="mk-by">{maker}</div>'
        '<div class="gal-cap">{caption}</div>'
        '<div class="mk-tags"><span class="mk-tech">{tech}</span><span class="mk-heat">{heat}</span><span class="mk-biz">{biz}</span></div>'
        '</div></a>')


def render():
    st = json.load(open(STATUS))
    md = open(MD).read()
    for tab in TABS:
        p = os.path.join(MID, f"demos_{tab}.json")
        if not os.path.exists(p):
            continue
        cards = []
        items = sorted(enumerate(json.load(open(p))), key=lambda x: x[1].get("rank", x[0]))  # rank 只管展示顺序，key 跟数据下标走
        for i, d in items:
            key = f"{tab}-{i:02d}"
            v = st.get(key, {})
            if not (v.get("page_ok") and v.get("img") in ("ok", "shot")):
                continue
            e = lambda s: html.escape(str(s or ""), quote=True)
            cards.append(CARD.format(url=e(d["url"]), key=key, title=e(d["title"]), maker=e(d["maker"]),
                                     caption=e(d["caption"]), heat=e(d["heat"]), biz=e(d.get("commercial")),
                                     tech=e(d.get("tech"))))
        block = f"<!--DEMOS:{tab}-->\n\n<div class=\"gal-grid\">\n" + "\n".join(cards) + "\n</div>\n\n<!--/DEMOS-->"
        md, n = re.subn(rf"<!--DEMOS:{tab}-->.*?<!--/DEMOS-->", lambda m: block, md, flags=re.S)
        print(f"{tab}: {len(cards)} cards" + ("" if n else "  (marker missing!)"))
    open(MD, "w").write(md)


if __name__ == "__main__":
    {"verify": verify, "render": render}[sys.argv[1]]()

