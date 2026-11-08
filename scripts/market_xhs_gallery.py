#!/usr/bin/env python3
"""Market 页 webdev / 3D 两条线的「场景 → 项目」gallery，案例来自小红书。

  python3 scripts/market_xhs_gallery.py logo     # 拉项目 logo，落 market/posters/logo-<slug>.png
  python3 scripts/market_xhs_gallery.py cover    # 拉示例首图，落 market/posters/xhs-<note_id>.jpg
  python3 scripts/market_xhs_gallery.py render   # 写进 market.md 的 <!--XG:route--> 标记之间

数据：middle_processing/market/xhs/gallery.json
  {route: [{scene, desc, cards: [{project, project_url, logo, field, used, example, note | poster, url, heat}]}]}
  note 填小红书笔记 id：封面取首图、链接带 xsec_token、heat 默认取赞藏；poster / url 用于非小红书示例。
卡片：封面链示例，项目名链官网，下面是 示例 / 谁在用 / 领域。
"""
import html, io, json, os, re, sys

import requests
from PIL import Image

from market_demos import MD, POSTERS
from xhs_crawl import XHS, cover as xhs_cover, hits, load, num

DATA = os.path.join(XHS, "gallery.json")
OVERSEA = "http://oversea-squid1.jp.txyun:11080"
e = lambda s: html.escape(str(s or ""), quote=True)

CARD = ('<div class="gal-card mk-card xg-card">'
        '<a href="{url}" target="_blank" rel="noopener"><div class="gal-poster" style="background:url(\'market/posters/{poster}.jpg\') center/cover no-repeat,#1b1f27">'
        '<span class="gal-play">↗ 看示例</span></div></a>'
        '<div class="gal-meta">{proj}'
        '<div class="gal-cap"><b>示例</b>{example}</div>'
        '<div class="xg-row"><b>谁在用</b>{used}</div>'
        '<div class="mk-tags"><span class="mk-biz">{field}</span><span class="mk-heat">{heat}</span></div>'
        '</div></div>')


def cards():
    for route, scenes in load(DATA).items():
        for s in scenes:
            for c in s["cards"]:
                yield route, s, c


def logo():
    """Google favicon 服务（实际多为 64px）；拿不到就不显示 logo。"""
    for slug, url in {c["logo"]: c["project_url"] for _, _, c in cards() if c.get("logo")}.items():
        dest = os.path.join(POSTERS, f"logo-{slug}.png")
        if os.path.exists(dest):
            continue
        dom = re.sub(r"^https?://([^/]+).*", r"\1", url)
        try:
            b = requests.get(f"https://www.google.com/s2/favicons?domain={dom}&sz=128",
                             proxies={"https": OVERSEA, "http": OVERSEA}, timeout=30).content
            im = Image.open(io.BytesIO(b)).convert("RGBA")
            im.save(dest)
            print(slug, "ok", im.size)
        except Exception as ex:
            print(slug, "FAIL", type(ex).__name__)


def cover():
    xhs_cover([c["note"] for _, _, c in cards()
               if c.get("note") and not os.path.exists(os.path.join(POSTERS, f"xhs-{c['note']}.jpg"))])


def card(c, seen):
    """链接 token 和赞藏数取搜索结果（所有卡片同一口径）；没有官网链接的项目只显示名字。"""
    if c.get("note"):
        x = seen[c["note"]][0]
        i = x["note_card"].get("interact_info") or {}
        poster = f"xhs-{c['note']}"
        url = f"https://www.xiaohongshu.com/explore/{c['note']}?xsec_token={x.get('xsec_token') or ''}&xsec_source=pc_search"
        heat = c.get("heat") or f"小红书 赞 {num(i.get('liked_count')):,} · 藏 {num(i.get('collected_count')):,}"
    else:
        poster, url, heat = c["poster"], c["url"], c.get("heat")
    lg = c.get("logo")
    # <img> 的 src 会被按 md 所在目录（market/）改写，背景图 url() 不会，所以这里写相对 market.md 的路径
    img = f'<img src="posters/logo-{lg}.png" alt="">' if lg and os.path.exists(os.path.join(POSTERS, f"logo-{lg}.png")) else ""
    proj = (f'<a class="xg-proj" href="{e(c["project_url"])}" target="_blank" rel="noopener">{img}{e(c["project"])}</a>'
            if c.get("project_url") else f'<div class="xg-proj">{img}{e(c["project"])}</div>')
    return CARD.format(url=e(url), poster=poster, proj=proj, example=e(c["example"]), used=e(c["used"]),
                       field=e(c["field"]), heat=e(heat))


ANCHOR = {"webdev": "xw", "3d": "x3"}   # 场景锚点 <前缀>-s<序号>，与 market.md 里手写的目录对应


def render():
    md, seen = open(MD).read(), hits()
    for route, scenes in load(DATA).items():
        out = []
        for i, s in enumerate(scenes, 1):
            ok = [c for c in s["cards"] if os.path.exists(os.path.join(POSTERS, (f"xhs-{c['note']}" if c.get("note") else c["poster"]) + ".jpg"))]
            out.append(f"<a class=\"anchor\" id=\"{ANCHOR[route]}-s{i}\"></a>\n\n### {s['scene']}\n\n{s['desc']}\n\n<div class=\"gal-grid\">\n"
                       + "\n".join(card(c, seen) for c in ok) + "\n</div>\n")
            print(f"{route} | {s['scene']}: {len(ok)}/{len(s['cards'])}")
        block = f"<!--XG:{route}-->\n\n" + "\n".join(out) + "\n<!--/XG-->"
        md, n = re.subn(rf"<!--XG:{route}-->.*?<!--/XG-->", lambda m: block, md, flags=re.S)
        if not n:
            print(f"{route}: marker missing!")
    open(MD, "w").write(md)


if __name__ == "__main__":
    {"logo": logo, "cover": cover, "render": render}[sys.argv[1]]()

