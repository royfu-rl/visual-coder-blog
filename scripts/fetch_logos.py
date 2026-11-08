#!/usr/bin/env python3
"""bench_meta_*.json / pipe_meta_*.json 里的 org_domain → assets/logos/<org>.png（favicon，走海外代理）

已存在且是合法图片的跳过；拉到 HTML 错误页（魔数不对）的丢弃。
"""
import hashlib, json, os, re, subprocess

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGOS = os.path.join(ROOT, "assets", "logos")
PROXY = "http://oversea-squid1.jp.txyun:11080"
MAGIC = (b"\x89PNG", b"\xff\xd8\xff", b"\x00\x00\x01\x00", b"RIFF")
GLOBE = "b8a0bf372c762e966cc99ede8682bc71"   # Google 查不到时返回的默认地球图标


def sources(domain):
    """依次尝试：Google 主域 → Google www. 子域 → DuckDuckGo"""
    www = domain if domain.startswith("www.") else "www." + domain
    yield f"https://www.google.com/s2/favicons?domain={domain}&sz=128"
    yield f"https://www.google.com/s2/favicons?domain={www}&sz=128"
    yield f"https://icons.duckduckgo.com/ip3/{domain}.ico"
    yield f"https://icons.duckduckgo.com/ip3/{www}.ico"


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def ok(path):
    if not (os.path.isfile(path) and os.path.getsize(path) > 100):
        return False
    data = open(path, "rb").read()
    return data[:4].startswith(MAGIC) and hashlib.md5(data).hexdigest() != GLOBE


def main():
    os.makedirs(LOGOS, exist_ok=True)
    orgs = {}
    for f in ("bench_meta_web.json", "bench_meta_3dgame.json", "pipe_meta_web.json", "pipe_meta_3dgame.json"):
        p = os.path.join(ROOT, "middle_processing", f)
        if os.path.isfile(p):
            for m in json.load(open(p, encoding="utf-8")):
                if m.get("org") and m.get("org_domain"):
                    orgs[slug(m["org"])] = m["org_domain"]
    # 工业 + 学术双机构
    for f in ("orgs_bench_web.json", "orgs_bench_3dgame.json", "orgs_pipe_web.json", "orgs_pipe_3dgame.json"):
        p = os.path.join(ROOT, "middle_processing", f)
        if os.path.isfile(p):
            for m in json.load(open(p, encoding="utf-8")):
                for o in (m.get("industry"), m.get("academic")):
                    if o and o.get("org") and o.get("domain"):
                        orgs[slug(o["org"])] = o["domain"]
    # 细讲标题的核心机构
    import importlib.util
    spec = importlib.util.spec_from_file_location("gen", os.path.join(ROOT, "scripts", "gen_env_page.py"))
    gen = importlib.util.module_from_spec(spec); spec.loader.exec_module(gen)
    for name, d in gen.LAB.items():
        orgs.setdefault(slug(name), d)
    for lst in gen.PICK_CORE.values():
        for o, d in lst:
            orgs.setdefault(slug(o), d)
    got = fail = 0
    for name, domain in sorted(orgs.items()):
        dst = os.path.join(LOGOS, name + ".png")
        if ok(dst):
            got += 1; continue
        for url in sources(domain):
            subprocess.run(["curl", "-sSL", "--max-time", "30", "-x", PROXY, "-o", dst, url])
            if ok(dst):
                break
        if ok(dst):
            got += 1
        else:
            fail += 1; print(f"  失败 {name} <- {domain}")
            if os.path.exists(dst): os.remove(dst)
    print(f"logos: {got} ok, {fail} failed, {len(orgs)} orgs")


if __name__ == "__main__":
    main()

