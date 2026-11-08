#!/usr/bin/env python3
"""小红书按关键词爬笔记，给 Market 页「按领域」一节做素材。

  python3 scripts/xhs_crawl.py login  --state <state 文件>     # 扫码登录：二维码落 xhs/login_qr.png，扫完存登录态
  python3 scripts/xhs_crawl.py search --state <state 文件>     # 登录态浏览器逐个关键词搜，截获 search/notes 接口结果
  python3 scripts/xhs_crawl.py table                           # 搜索结果汇总成 notes.tsv（标题 / 作者 / 赞藏评），供筛选
  python3 scripts/xhs_crawl.py notes <note_id> ...             # 只给入围的补详情（正文 / 标签 / 全部图片），串行慢抓
  python3 scripts/xhs_crawl.py cover <note_id> ...             # 首图落 market/posters/xhs-<id>.jpg

数据：middle_processing/market/xhs/
  keywords.json          {领域: [关键词]}
  search/<关键词>.json    接口原始 items
  notes/<note_id>.json   标题 / 正文 / 标签 / 作者 / 时间 / 赞藏评转 / 图片 URL / xsec_token

两条路：
  搜索必须登录（不登录弹扫码框、不发 search/notes 请求）→ Playwright 带 cookie，签名交给页面自己
  详情不用登录：手机 UA + 搜索结果里的 xsec_token（xhs-fetcher 的路子）；
               爬虫 UA（facebookexternalhit）只对搜索引擎收录过的老笔记直出，作兜底
"""
import argparse, io, json, os, random, re, sys, time

import requests
from PIL import Image

from market_demos import MID, POSTERS

sys.path.insert(0, "/mmu_mllm_hdd_4/infra/skills/xhs-fetcher/scripts")
from xhs_fetch import image_candidates, is_image  # noqa: E402  图片回退链沿用 xhs-fetcher skill

XHS = os.path.join(MID, "xhs")
SEARCH, NOTES = os.path.join(XHS, "search"), os.path.join(XHS, "notes")
PROXY = "http://10.68.24.18:11080"           # 国内代理
BOT_UA = "facebookexternalhit/1.1"
from xhs_fetch import UA as MOBILE_UA  # noqa: E402
DESK_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
API = "/search/notes"                        # 2026-11 起是 so.xiaohongshu.com/api/sns/web/v2/search/notes


def load(p):
    return json.load(open(p))


def dump(obj, p):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p + ".tmp", "w") as f:              # 先写临时文件再改名，并发读不会读到半截
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(p + ".tmp", p)


def state(html):
    m = re.search(r"window\.__INITIAL_STATE__\s*=\s*(.*?)</script>", html, re.S)
    return json.loads(re.sub(r"\bundefined\b", "null", m.group(1))) if m else {}


# ---------- login：扫码，登录态存成 storage_state ----------

def login(state_file, minutes=10):
    """二维码截图落 xhs/login_qr.png（约 1 分半刷新一次），扫码成功后存 state_file 并删掉二维码。"""
    from playwright.sync_api import sync_playwright
    qr = os.path.join(XHS, "login_qr.png")
    with sync_playwright() as p:
        b = p.chromium.launch(proxy={"server": PROXY})
        ctx = b.new_context(user_agent=DESK_UA, viewport={"width": 1400, "height": 900}, locale="zh-CN")
        pg = ctx.new_page()
        me = []
        pg.on("response", lambda r: me.append(r) if "/api/sns/web/v2/user/me" in r.url else None)
        end = time.time() + minutes * 60
        while time.time() < end:
            pg.goto("https://www.xiaohongshu.com/explore", timeout=60000)
            pg.wait_for_timeout(4000)
            el = pg.query_selector(".qrcode-img") or pg.query_selector(".login-container")
            (el.screenshot(path=qr) if el else pg.screenshot(path=qr))
            print("二维码已更新", time.strftime("%H:%M:%S"), flush=True)
            for _ in range(45):                      # 90 秒后二维码过期，重开页面
                pg.wait_for_timeout(2000)
                if not pg.query_selector(".login-container"):
                    pg.wait_for_timeout(3000)
                    ctx.storage_state(path=state_file)
                    os.remove(qr)
                    print("登录成功，state →", state_file, flush=True)
                    return b.close()
        print("超时未扫码", flush=True)
        b.close()


# ---------- search：登录态浏览器 ----------

def search(state_file, pages):
    from playwright.sync_api import sync_playwright
    todo = [(d, k) for d, ks in load(os.path.join(XHS, "keywords.json")).items() for k in ks
            if not os.path.exists(os.path.join(SEARCH, k + ".json"))]
    with sync_playwright() as p:
        b = p.chromium.launch(proxy={"server": PROXY})
        ctx = b.new_context(user_agent=DESK_UA, viewport={"width": 1400, "height": 900}, locale="zh-CN",
                            storage_state=state_file)
        pg = ctx.new_page()
        got = []
        pg.on("response", lambda r: got.append(r) if API in r.url else None)
        for domain, kw in todo:
            got.clear()
            pg.goto(f"https://www.xiaohongshu.com/search_result?keyword={kw}&source=web_search_result_notes", timeout=60000)
            pg.wait_for_timeout(5000)
            for _ in range(pages - 1):
                pg.mouse.wheel(0, 6000)
                pg.wait_for_timeout(random.uniform(2500, 4000))
            items = []
            for r in got:
                try:
                    items += (r.json().get("data") or {}).get("items") or []
                except Exception:
                    pass
            items = [x for x in items if x.get("model_type") == "note"]
            if not items:
                print(f"✗ {kw}: 0 条，停（cookie 失效 / 验证码？）当前页 {pg.url[:80]}")
                break
            dump({"domain": domain, "keyword": kw, "items": items}, os.path.join(SEARCH, kw + ".json"))
            print(f"{domain} | {kw}: {len(items)} 条")
            time.sleep(random.uniform(5, 9))
        b.close()


# ---------- notes：不登录抓详情 ----------

def fetch_note(nid, token):
    """手机 UA + 搜索给的 xsec_token（xhs-fetcher 的路子）：先直连（出口在海外，会跳 rednote.com），
    再走国内代理（2026-11-03 跑过一批后该 IP 被风控，跳 sec 404）；最后爬虫 UA（只对搜索引擎收录过的老笔记有效）。"""
    out = os.path.join(NOTES, nid + ".json")
    if os.path.exists(out):
        return "skip"
    px = {"https": PROXY, "http": PROXY}
    n = None
    for proxies in ([{}, px] if token else []):
        try:
            r = requests.get(f"https://www.xiaohongshu.com/discovery/item/{nid}?xsec_token={token}&xsec_source=pc_search",
                             headers={"User-Agent": MOBILE_UA, "Referer": "https://www.xiaohongshu.com/"},
                             proxies=proxies, timeout=40)
        except requests.RequestException:
            continue
        n = (((state(r.text).get("noteData") or {}).get("data") or {}).get("noteData"))
        if n:
            break
    if not n:
        r = requests.get(f"https://www.xiaohongshu.com/explore/{nid}", headers={"User-Agent": BOT_UA}, proxies=px, timeout=40)
        n = (((state(r.text).get("note") or {}).get("noteDetailMap") or {}).get(nid) or {}).get("note")
    if not n:
        return "fail"
    info = n.get("interactInfo") or {}
    dump({
        "note_id": nid, "xsec_token": token or n.get("xsecToken"),
        "type": n.get("type"), "title": n.get("title"), "desc": n.get("desc"),
        "tags": [t.get("name") for t in n.get("tagList") or []],
        "author": (n.get("user") or {}).get("nickname") or (n.get("user") or {}).get("nickName"),
        "user_id": (n.get("user") or {}).get("userId"),
        "time": n.get("time"), "ip_location": n.get("ipLocation"),
        "likes": info.get("likedCount"), "collects": info.get("collectedCount"),
        "comments": info.get("commentCount"), "shares": info.get("shareCount"),
        "images": [im.get("urlDefault") or im.get("url") for im in n.get("imageList") or []],
    }, out)
    return "ok"


def hits():
    """{note_id: (搜索 item, 分组, 关键词)}，同一笔记多次命中取第一次。"""
    seen = {}
    for f in sorted(os.listdir(SEARCH)):
        s = load(os.path.join(SEARCH, f))
        for x in s["items"]:
            seen.setdefault(x["id"], (x, s["domain"], s["keyword"]))
    return seen


def notes(ids):
    """只给入围的补详情：串行、每条间隔 2-4 秒，连续 5 条失败（多半被风控）就停。"""
    seen, bad = hits(), 0
    for nid in ids:
        r = fetch_note(nid, seen[nid][0].get("xsec_token"))
        print(nid, r, flush=True)
        bad = bad + 1 if r == "fail" else 0
        if bad >= 5:
            sys.exit("连续 5 条失败，停（代理 IP 被风控？过一阵再跑）")
        if r != "skip":
            time.sleep(random.uniform(2, 4))


def num(s):
    """'1.2万' / '11.1K' / '6,302' / '10+' → int。"""
    s = str(s or 0).replace(",", "").rstrip("+")
    unit = {"万": 10000, "K": 1000, "k": 1000}.get(s[-1:], 1)
    return int(float(s[:-1] if unit > 1 else s or 0) * unit)


def table():
    """以搜索结果为准（标题 / 作者 / 赞藏评都在里面），有详情的补正文。"""
    rows = []
    for nid, (x, domain, kw) in hits().items():
        c = x.get("note_card") or {}
        i = c.get("interact_info") or {}
        p = os.path.join(NOTES, nid + ".json")
        desc = load(p)["desc"] if os.path.exists(p) else ""
        rows.append([domain, kw, nid, c.get("type"), num(i.get("liked_count")), num(i.get("collected_count")),
                     num(i.get("comment_count")), (c.get("user") or {}).get("nickname") or "",
                     (c.get("display_title") or "").replace("\t", " "), re.sub(r"\s+", " ", desc or "")[:160]])
    rows.sort(key=lambda r: (r[0], -r[4]))
    with open(os.path.join(XHS, "notes.tsv"), "w") as f:
        f.write("分组\t关键词\tid\t类型\t赞\t藏\t评\t作者\t标题\t正文前160字\n")
        f.writelines("\t".join(map(str, r)) + "\n" for r in rows)
    print(len(rows), "行 →", os.path.join(XHS, "notes.tsv"))


def cover(ids):
    seen = hits()
    for nid in ids:
        p = os.path.join(NOTES, nid + ".json")
        url = load(p)["images"][0] if os.path.exists(p) else seen[nid][0]["note_card"]["cover"]["url_default"]
        for u in image_candidates(url):
            try:
                b = requests.get(u, headers={"User-Agent": DESK_UA, "Referer": "https://www.xiaohongshu.com/"},
                                 proxies={"https": PROXY, "http": PROXY}, timeout=60).content
            except Exception:
                continue
            if len(b) >= 1024 and is_image(b):
                im = Image.open(io.BytesIO(b)).convert("RGB")
                im.thumbnail((960, 960))
                im.save(os.path.join(POSTERS, f"xhs-{nid}.jpg"), "JPEG", quality=82)
                print(nid, "ok", im.size)
                break
        else:
            print(nid, "FAIL")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["login", "search", "notes", "table", "cover"])
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--state", help="登录态文件（含 session，别放进项目目录）")
    ap.add_argument("--pages", type=int, default=2)
    a = ap.parse_args()
    {"login": lambda: login(a.state), "search": lambda: search(a.state, a.pages), "notes": lambda: notes(a.ids),
     "table": table, "cover": lambda: cover(a.ids)}[a.cmd]()

