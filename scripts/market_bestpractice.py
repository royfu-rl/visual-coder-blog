#!/usr/bin/env python3
"""Market 页 Overview 第 6 节：按技术路线、每个场景一张最佳实践卡片。

  python3 scripts/market_bestpractice.py fetch    # 给没有现成封面的条目拉封面，落 market/posters/bp-<route>-<i>.jpg
  python3 scripts/market_bestpractice.py render   # 渲染成卡片，写进 market.md 的 <!--BP:route--> 标记之间

数据：middle_processing/market/best_practice.json，{route: [{title, maker, url, caption, heat, commercial, tech, poster | image}]}
poster 填已有封面的 key（如 ad-00）直接复用；image 填封面图地址，fetch 时下载。
卡片模板与下载逻辑沿用 market_demos.py，不碰它的 demos_*.json 与 demos_verify.json。
"""
import html
import json
import os
import re
import sys

from market_demos import CARD, MD, MID, POSTERS, fetch_image

DATA = os.path.join(MID, "best_practice.json")


def key(route, i, d):
    return d.get("poster") or f"bp-{route}-{i:02d}"


def fetch():
    for route, items in json.load(open(DATA)).items():
        for i, d in enumerate(items):
            if d.get("poster"):
                continue
            k = key(route, i, d)
            print(k, fetch_image(d["image"], os.path.join(POSTERS, k + ".jpg")), d["title"])


def render():
    md = open(MD).read()
    e = lambda s: html.escape(str(s or ""), quote=True)
    for route, items in json.load(open(DATA)).items():
        cards = [CARD.format(url=e(d["url"]), key=key(route, i, d), title=e(d["title"]), maker=e(d["maker"]),
                             caption=e(d["caption"]), heat=e(d["heat"]), biz=e(d["commercial"]), tech=e(d["tech"]))
                 for i, d in enumerate(items)
                 if os.path.exists(os.path.join(POSTERS, key(route, i, d) + ".jpg"))]
        block = f"<!--BP:{route}-->\n\n<div class=\"gal-grid\">\n" + "\n".join(cards) + "\n</div>\n\n<!--/BP-->"
        md, n = re.subn(rf"<!--BP:{route}-->.*?<!--/BP-->", lambda m: block, md, flags=re.S)
        print(f"{route}: {len(cards)}/{len(items)} cards" + ("" if n else "  (marker missing!)"))
    open(MD, "w").write(md)


if __name__ == "__main__":
    {"fetch": fetch, "render": render}[sys.argv[1]]()

