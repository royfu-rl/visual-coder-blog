#!/usr/bin/env python3
"""middle_processing/{benchmarks,pipelines}.md → env/env.md

Environment 分 Web / 3D / Game 三个视图，每个视图：
  开源榜单      Analysis Frame + 一张按时间排的总表（kat-coder 样式）+ 时间线解读
                文字在 env/{web,3d,game}.md，按 <!--ANALYSIS--> <!--LANDSCAPE--> 等标记切段，
                元数据在 middle_processing/bench_meta_*.json
  开源数据管线  一张总表 + 精选细讲
  自建数据管线  占位
"""
import os, re, json

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BENCH = os.path.join(ROOT, "middle_processing", "benchmarks.md")
PIPE  = os.path.join(ROOT, "middle_processing", "pipelines.md")
DST   = os.path.join(ROOT, "env", "env.md")
LOGOS = os.path.join(ROOT, "assets", "logos")


def load_meta():
    """name → 元数据（机构 / Download / 影响力 / 任务形态 / 能力）"""
    meta = {}
    for f in ("bench_meta_web.json", "bench_meta_3dgame.json", "bench_meta_video.json"):
        p = os.path.join(ROOT, "middle_processing", f)
        if os.path.isfile(p):
            meta.update({m["name"]: m for m in json.load(open(p, encoding="utf-8"))})
    # 编程语言：bench_lang.json（按任务确定的）+ bench_lang_verified.json（查原文核实的）
    lang = {}
    p = os.path.join(ROOT, "middle_processing", "bench_lang.json")
    if os.path.isfile(p):
        lang.update(json.load(open(p, encoding="utf-8")))
    p = os.path.join(ROOT, "middle_processing", "bench_lang_verified.json")
    if os.path.isfile(p):
        lang.update({m["name"]: m["lang"] for m in json.load(open(p, encoding="utf-8")) if m.get("lang")})
    for name, l in lang.items():
        meta.setdefault(name, {})["lang"] = l
    return meta


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def date_key(d):
    return tuple(int(x) for x in re.findall(r"\d+", d)[:3]) + (0, 0)


def link(label, url):
    return f"[{label}]({url})" if url else "—"


def _md_inline(s):
    """合并表是原始 HTML <table>，marked 不处理 <td> 内的 markdown；这里把行内的
    **粗体** 和 [文字](链接) 手动转成 HTML，否则会显示成字面星号。"""
    if not s:
        return s
    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    return s


# HuggingFace 风格的影响力徽章：下载 / likes 用 HF 图标，star 用 GitHub 星标
_HF_DL = '<svg class="hf-i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v11"/><path d="M8 11l4 4 4-4"/><path d="M4 20h16"/></svg>'
_HF_LK = '<svg class="hf-i" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21C7 17.5 3 14 3 9.5 3 7 5 5 7.5 5 9.2 5 10.7 6 12 7.6 13.3 6 14.8 5 16.5 5 19 5 21 7 21 9.5 21 14 17 17.5 12 21z"/></svg>'
_HF_ST = '<svg class="hf-i" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.5l2.9 6 6.6.6-5 4.3 1.5 6.5L12 16.9 6 20.9l1.5-6.5-5-4.3 6.6-.6z"/></svg>'
_HF_ICON = {"dl": _HF_DL, "lk": _HF_LK, "st": _HF_ST}
_HF_TITLE = {"dl": "downloads", "lk": "likes", "st": "GitHub stars"}


def impact_badges(text, url=None):
    """把 '23.0k 下载 · 89 likes' / '12.0k star' / '163 下载' 解析成 HF 风格徽章。"""
    if not text:
        return ""
    parts = []
    for key, pat in (("dl", r"([\d.]+\s*[kKmM]?)\s*下载"),
                     ("lk", r"([\d.]+\s*[kKmM]?)\s*likes?"),
                     ("st", r"([\d.]+\s*[kKmM]?)\s*stars?")):
        m = re.search(pat, text)
        if m:
            parts.append((key, m.group(1).replace(" ", "")))
    if parts:
        inner = "".join(f'<span class="hf-b hf-{k}" title="{_HF_TITLE[k]}">{_HF_ICON[k]}{v}</span>'
                        for k, v in parts)
    else:
        inner = f'<span class="hf-b">{text}</span>'          # 解析不出就原样显示
    return f'<a class="hf" href="{url}">{inner}</a>' if url else f'<span class="hf">{inner}</span>'


def load_orgs():
    """name → [工业机构, 学术机构]（orgs_*.json，查全部作者单位后各取最有名的一个）"""
    orgs = {}
    for f in ("orgs_bench_web.json", "orgs_bench_3dgame.json", "orgs_pipe_web.json", "orgs_pipe_3dgame.json",
              "orgs_bench_video.json", "orgs_pipe_video.json"):
        p = os.path.join(ROOT, "middle_processing", f)
        if os.path.isfile(p):
            for m in json.load(open(p, encoding="utf-8")):
                orgs[m["name"]] = [o for o in (m.get("industry"), m.get("academic")) if o and o.get("org")]
    return orgs


ORGS = load_orgs()


def org_mark(m, name):
    """机构标识：工业在前、学术在后，各一个 logo（没有 favicon 用首字母方块）；名称后跟灰色机构名。
    orgs_*.json 没覆盖到的，回落到元数据里的单个 org。"""
    orgs = ORGS.get(name) or ([{"org": m["org"]}] if (m or {}).get("org") else [])
    if not orgs:                                   # 核实过无单位（如单人 gmail 作者）
        return "", ' <span class="org">独立作者</span>'
    marks = ""
    for o in orgs:
        f = os.path.join(LOGOS, slug(o["org"]) + ".png")
        if os.path.isfile(f):
            marks += f'<img height="14" src="../assets/logos/{slug(o["org"])}.png" align="center" alt="" title="{o["org"]}"> '
        else:
            marks += f'<span class="org-mark" title="{o["org"]}">{o["org"][0].upper()}</span> '
    return marks, ' <span class="org">' + " · ".join(o["org"] for o in orgs) + "</span>"


# 细讲 → 数据样例组件（middle_processing/samples/<slug>.html，规范见 DEMO_SPEC.md）
SAMPLES = {"ChartGalaxy": "chartgalaxy", "WebSight": "websight", "pix2code": "pix2code", "CoSyn-400K": "cosyn-400k",
           "ScreenCoder": "screencoder", "Vision2UI": "webcode2m", "VinciCoder": "vincicoder", "WebGen-Agent": "webgen-agent",
           "VisCoder2": "viscoder2", "Objaverse": "objaverse", "Cap3D": "cap3d", "CAD-Recode": "cad-recode",
           "MeshCoder": "meshcoder", "Code2Logic": "gameqa", "MarioGPT": "mariogpt",
           "Code2Video": "code2video", "TheoremExplainAgent": "theoremexplainagent", "OmniLottie": "omnilottie",
           "Paper2Video": "paper2video", "Keyframer": "keyframer", "Vector Prism": "vectorprism"}


def with_sample(p, lines):
    """把样例组件插到细讲的最后一张图之后；没有图就插在第一行（定位）之后"""
    f = os.path.join(ROOT, "middle_processing", "samples", f"{SAMPLES.get(p, '-')}.html")
    if not os.path.isfile(f):
        return lines
    demo = open(f, encoding="utf-8").read().strip()
    idx = max([i for i, l in enumerate(lines) if "</figure>" in l], default=None)
    if idx is None:
        idx = next((i for i, l in enumerate(lines) if l.strip()), 0)
    return lines[:idx + 1] + ["", demo, ""] + lines[idx + 1:]


# 细讲标题的「核心机构」：牵头团队，不按名气（表格里的工业 + 学术双机构是按名气选的）
PICK_CORE = {
    "WebGen-Agent": [("CUHK MMLab", "cuhk.edu.hk")],
    "VinciCoder":   [("Meituan", "meituan.com"), ("CASIA", "ia.cas.cn")],
    "VisCoder2":    [("Waterloo TIGER-Lab", "uwaterloo.ca"), ("CMU", "cmu.edu")],
    "CAD-Recode":   [("Artec3D", "artec3d.com"), ("Univ. Luxembourg", "uni.lu"), ("AIRI", "airi.net")],
    "MeshCoder":    [("Shanghai AI Lab", "shlab.org.cn"), ("Tsinghua", "tsinghua.edu.cn")],
}


for _f in ("deep_web_orgs.json", "deep_3d_orgs.json", "deep_game_orgs.json", "deep_video_orgs.json"):
    _p = os.path.join(ROOT, "middle_processing", _f)
    if os.path.isfile(_p):
        for _name, _lst in json.load(open(_p, encoding="utf-8")).items():
            PICK_CORE.setdefault(_name, [tuple(x) for x in _lst])

# 细讲 → pipe_meta 里的名称（取采用度）
PICK_META = {"Vision2UI": "Vision2UI → WebCode2M", "VisCoder2": "VisCoder2 / VisCode-Multi-679K",
             "Objaverse": "Objaverse", "Cap3D": "Cap3D", "Infinigen": "Infinigen",
             "Code2Logic": "Game-RL / Code2Logic / GameQA", "OpenGame": "OpenGame / GameCoder-27B"}


def _pick_org_list(p):
    lst = next((v for k, v in PICK_CORE.items() if k.startswith(p)), [])
    return [{"org": o, "domain": d} for o, d in lst]


def pick_impact(p, pmeta):
    m = pmeta.get(PICK_META.get(p, p), {})
    return (" " + impact_badges(m["impact"], m.get("impact_url"))) if m.get("impact") else ""


def pick_logos(p):
    html = ""
    for o in _pick_org_list(p):
        f = os.path.join(LOGOS, slug(o["org"]) + ".png")
        if os.path.isfile(f):
            html += f'<img class="h-logo" height="20" src="../assets/logos/{slug(o["org"])}.png" alt="" title="{o["org"]}">'
        else:
            html += f'<span class="org-mark h-logo" title="{o["org"]}">{o["org"][0].upper()}</span>'
    return html + " " if html else ""


def pick_orgs(p):
    orgs = _pick_org_list(p)
    return ' <span class="org">' + " · ".join(o["org"] for o in orgs) + "</span>" if orgs else ""


def load_pipe_meta():
    meta = {}
    for f in ("pipe_meta_web.json", "pipe_meta_3dgame.json", "pipe_meta_video.json"):
        p = os.path.join(ROOT, "middle_processing", f)
        if os.path.isfile(p):
            meta.update({m["name"]: m for m in json.load(open(p, encoding="utf-8"))})
    return meta


def pipe_table(prow, meta):
    """发布日期 | 名称(logo) | Download | 数据形态 | 规模 | 影响力 | 特性 / 训练用途"""
    out = ["| 发布日期 | 数据集 / 工作 | Download | 数据形态 | 规模 | 影响力 | 特性 / 训练用途 |",
           "|---|---|---|---|---|---|---|"]
    items = []
    for scene, c in prow:
        nm = re.match(r"\[([^\]]+)\]\(([^)]+)\)(.*)", c[1])
        name, url = nm.group(1), nm.group(2)
        m = meta.get(name, {})
        date = m.get("date") or c[0].replace("-", "/").replace("/0", "/")
        mark, org = org_mark(m, name)
        dl = link(m.get("download_label"), m.get("download_url"))
        if dl == "—":                                    # 元数据没给：回落到原表「开源」列
            first = re.search(r"\[[^\]]+\]\([^)]+\)", c[-1])
            dl = first.group(0) if first else (c[-1] if not c[-1].startswith("是") else "—")
        cells = [date, f"{mark}[{name}]({url}){org}", dl,
                 m.get("form") or c[2], m.get("size") or c[3],
                 impact_badges(m.get("impact"), m.get("impact_url")) or "—",
                 m.get("feature") or c[4]]
        items.append((date_key(date), "| " + " | ".join(x.replace("|", "/") for x in cells) + " |"))
    return out + [row for _, row in sorted(items, key=lambda x: x[0])]


def bench_table(rows, meta):
    """kat-coder 样式：发布日期 | Benchmark(logo) | Download | 任务形态 | 编程语言 | 题目数量 | 影响力 | 考察能力"""
    out = ["| 发布日期 | Benchmark | Download | 任务形态 | 编程语言 | 题目数量 | 影响力 | 考察能力 / 可补强方向 |",
           "|---|---|---|---|---|---|---|---|"]
    items = []
    for r in rows:
        m = meta.get(r["name"], {})
        date = m.get("date") or r["date"].replace("-", "/").replace("/0", "/")
        mark, org = org_mark(m, r["name"])
        cells = [date,
                 f'{mark}[{r["name"]}]({r["url"]}){org}',
                 link(m.get("download_label"), m.get("download_url")),
                 m.get("task_form") or "—",
                 m.get("lang") or "—",
                 m.get("size") or r["cells"][2],
                 impact_badges(m.get("impact"), m.get("impact_url")) or "—",
                 m.get("capability") or r["cells"][4]]
        items.append((date_key(date), "| " + " | ".join(c.replace("|", "/") for c in cells) + " |"))
    return out + [row for _, row in sorted(items, key=lambda x: x[0])]

# 视图 → (benchmark 类别号, 管线场景名, 精选细讲标题前缀)
VIEWS = [
    # 细讲：按采用度排序；"|" 之后是采用度低、但训练信号更丰富的
    ("web",  "Web",  ["1", "2", "3"], ["Web / UI 代码", "图表 / SVG / TikZ 代码"],
     ["ChartGalaxy", "WebSight", "pix2code", "CoSyn-400K", "ScreenCoder", "Vision2UI", "|", "VinciCoder", "WebGen-Agent", "VisCoder2"]),
    ("3d",   "3D",   ["4", "5", "6", "8"], ["3D / Blender / CAD 代码", "3D 资产原料与标注"],
     ["Objaverse", "Cap3D", "Infinigen", "CAD-Recode", "|", "MeshCoder"]),
    ("game", "Game", ["7"], ["游戏"], ["Code2Logic", "OpenGame", "MarioGPT"]),
    ("video", "Video", ["9", "10", "11", "12"], ["视频即代码"],
     ["Code2Video", "TheoremExplainAgent", "Paper2Video", "OmniLottie", "|", "Keyframer", "Vector Prism", "VAnim", "ManimAgent"]),
]
# 前沿厂商 logo：正文里写 {{lab:OpenAI}}，生成时换成 logo + 名字
LAB = {"OpenAI": "openai.com", "Anthropic": "anthropic.com", "Google": "deepmind.google", "Moonshot": "moonshot.cn",
       "Zhipu": "zhipuai.cn", "Qwen": "tongyi.aliyun.com", "DeepSeek": "deepseek.com", "ByteDance Seed": "seed.bytedance.com",
       "Tencent Hunyuan": "hunyuan.tencent.com", "MiniMax": "minimax.io"}


def lab_marks(text):
    def repl(m):
        name = m.group(1)
        f = os.path.join(LOGOS, slug(name) + ".png")
        # 只放 logo（模型名本身已经够辨识），悬停显示机构名；没有 logo 图才退回写名字
        if os.path.isfile(f):
            return f'<img height="14" src="../assets/logos/{slug(name)}.png" align="center" alt="{name}" title="{name}">'
        return name
    return re.sub(r"\{\{lab:([^}]+)\}\}", repl, text)


# 开源榜单的分组表：(按钮名, 一句说明, 类别号, 额外并入的条目, 排除的条目)
GUI_CAD = ["VideoCAD", "CADWorld"]
BENCH_GROUPS = {
    "web": [
        ("Screenshot → Code", "输入截图 / 设计稿 / 草图，输出网页代码，渲染后和参考图比。", ["1"], [], []),
        ("Web App", "从规格或对话生成可交互的 Web App，由浏览器 agent 实测功能。", ["2"], [], []),
        ("Chart / SVG", "图表还原与编辑、SVG 生成，输出绘图代码或矢量代码。", ["3"], [], []),
    ],
    "3d": [
        ("Blender", "写 Blender Python / Three.js 代码来建模和编辑场景。", ["4"], [], []),
        ("Diffusion", "评 text / image-to-3D 生成模型（SDS 优化、前馈重建、3D latent diffusion），直接输出 mesh / NeRF / Gaussian，不写代码；只评外观质量与文本一致性。", ["6"], [], []),
        ("GUI", "不写代码，直接在 Blender / CAD / Photoshop 等专业软件里长程点击操作。", ["8"], GUI_CAD, []),
        ("CAD", "写 CadQuery 等参数化 CAD 代码，目标是工程零件，按尺寸、约束、可制造性验收。列在这里是因为它的确定性验收和程序化合成方法值得借鉴。", ["5"], [], GUI_CAD),
    ],
    "video": [
        ("Manim", "Python + Manim 等数学动画引擎：把讲稿 / 论文 / 定理写成 Manim 代码，引擎逐帧渲成 mp4。",
         ["9"], [], []),
        ("PPT", "生成幻灯片 / 海报 / 演讲视频：python-pptx、Beamer 等，产物是 .pptx / PDF，再转视频。",
         ["11"], [], []),
        ("HTML · 网页", "浏览器渲染一类：HTML / CSS / SVG / Canvas / Lottie 代码，逐帧截图合成视频（含 OpenCV 逐帧直出的 SimuScene）。",
         ["10", "12"], [], []),
        ("渲染器", "把动画代码渲染成视频的确定性引擎，以及面向 agent 的视频框架 / DSL —— 本身不是内容，是底座。",
         [], [], []),
    ],
}
VIDEO_MANIM = ["TheoremExplainAgent", "manimator", "Code2Video", "ManimAgent"]
VIDEO_PPT   = ["AutoPresent", "PPTAgent", "Paper2Poster", "PresentAgent", "Paper2Video"]
VIDEO_RENDERERS = ["3b1b/manim", "Manim Community", "Remotion", "Motion Canvas",
                   "ranim", "HyperFrames", "Hypit"]


def grouped_tables(key, caps, bench, meta):
    """一类一张表 + 顶部切换按钮（template 里的 .tbl-tabs 组件）"""
    groups = BENCH_GROUPS.get(key)
    if not groups:
        return bench_table([r for no in caps for r in bench[no]], meta)
    allrows = {r["name"]: r for no in caps for r in bench[no]}
    out = ['<div class="tbl-tabs">', ""]
    for label, desc, cats, extra, exclude in groups:
        rows = [r for no in cats for r in bench[no] if r["name"] not in exclude] + [allrows[n] for n in extra]
        out += [f'<div class="tbl-pane" data-label="{label}" data-count="{len(rows)}">', "",
                f'<p class="tbl-desc">{desc}</p>', ""] + bench_table(rows, meta) + ["", "</div>", ""]
    return out + ["</div>"]


CAP = {"1": "截图 → 网页", "2": "交互式 Web App", "3": "图表 / SVG", "4": "程序化 3D / Blender",
       "5": "CAD", "6": "3D 资产质量", "7": "游戏开发", "8": "专业软件 GUI"}
PIPE_SHORT = {"Web / UI 代码": "Web / UI", "图表 / SVG / TikZ 代码": "图表 / SVG",
              "3D / Blender / CAD 代码": "Blender / CAD", "3D 资产原料与标注": "资产原料", "游戏": "游戏"}



def rows_of(lines):
    """markdown 表格数据行 → cell 列表"""
    for l in lines:
        if l.startswith("|") and re.match(r"\|\s*\d{4}-\d{2}", l):
            yield [c.strip() for c in l.strip().strip("|").split("|")]


def split_sections(path, pat):
    """按标题正则切块：{标题: [行]}"""
    out, cur = {}, None
    for l in open(path, encoding="utf-8").read().splitlines():
        m = re.match(pat, l)
        if m:
            cur = m.group(1).strip(); out[cur] = []; continue
        if l.startswith("### ") or l.startswith("---"):
            cur = None; continue
        if cur is not None:
            out[cur].append(l)
    return out


# 数据管线的分组表：视图 → [(按钮名, 一句说明, 条目名列表)]；名称取原表「名称」列
PIPE_GROUPS = {
    "web": [
        ("Screenshot → Code", "截图、设计稿或草图到网页代码的配对数据。",
         ["pix2code", "WebSight", "Design2Code", "Vision2UI → WebCode2M", "Web2Code", "Sketch2Code", "ScreenCoder",
          "WebRenderBench / ALISA", "UI2Code^N", "AnyDoc / DocHTML", "MT-Web2Code"]),
        ("Web App", "带交互、多文件或 agent 轨迹的 Web App 数据。",
         ["UICoder", "Interaction2Code", "WebGen-Bench / WebGen-Instruct", "ArtifactsBench", "WebGen-Agent", "ReLook", "WebVIA"]),
        ("Chart / SVG", "图表绘图代码、SVG 与 TikZ 数据。", None),       # None = 该视图的默认场景全部
    ],
    "3d": [
        ("Blender", "Blender 代码、Blender 场景生成器与 Blender agent 数据。",
         ["Infinigen", "SceneCraft", "Infinigen Indoors", "BlenderLLM / BlendNet", "BlenderGym", "LL3M", "MeshCoder", "BlenderRAG"]),
        ("Diffusion", "训练神经 3D 生成模型用的资产原料与标注，不含建模代码。", None),
        ("CAD", "参数化 CAD 代码与 CAD 构造序列数据。",
         ["DeepCAD", "Text2CAD", "CAD-MLLM / Omni-CAD", "CAD-Recode", "CADFusion", "CAD-Coder（VLM 版）/ GenCAD-Code",
          "CAD-Coder（文本版）", "cadrille"]),
    ],
    "video": [
        ("Manim", "", VIDEO_MANIM),
        ("PPT", "", VIDEO_PPT),
        ("HTML · 网页", "", "__rest__"),     # 其余网页/Canvas/SVG/Lottie 类 + SimuScene
        ("渲染器", "", VIDEO_RENDERERS),
    ],
}
PIPE_GROUP_DEFAULT = {"web": "图表 / SVG / TikZ 代码", "3d": "3D 资产原料与标注"}


def grouped_pipe_tables(key, prow, pmeta):
    groups = PIPE_GROUPS.get(key)
    if not groups:
        return pipe_table(prow, pmeta)
    name_of = lambda c: re.match(r"\[([^\]]+)\]", c[1]).group(1)
    out, used = ['<div class="tbl-tabs">', ""], set()
    for label, desc, names in groups:
        if names is None:
            rows = [(sc, c) for sc, c in prow if sc == PIPE_GROUP_DEFAULT[key]]
        else:
            rows = [(sc, c) for sc, c in prow if name_of(c) in names]
        used |= {name_of(c) for _, c in rows}
        out += [f'<div class="tbl-pane" data-label="{label}" data-count="{len(rows)}">', "",
                f'<p class="tbl-desc">{desc}</p>', ""] + pipe_table(rows, pmeta) + ["", "</div>", ""]
    missed = [name_of(c) for _, c in prow if name_of(c) not in used]
    if missed:
        print(f"  [warn] {key} 管线未分组：{missed}")
    return out + ["</div>"]


# ---- 合并表：benchmark + 数据集 并入一张表（统一超集列 + 类型标签 + top5 加权高亮）----
def _to_num(tok):
    tok = tok.strip().lower().replace(",", "")
    mult = 1.0
    if tok.endswith("k"): mult, tok = 1e3, tok[:-1]
    elif tok.endswith("m"): mult, tok = 1e6, tok[:-1]
    try:
        return float(tok) * mult
    except ValueError:
        return 0.0


def impact_score(text):
    """影响力加权：下载量 + 3×GitHub star + 20×HF like（star/like 更稀缺，权重更高）"""
    if not text:
        return 0.0
    s = 0.0
    m = re.search(r"([\d.]+\s*[kKmM]?)\s*下载", text);  s += (_to_num(m.group(1)) if m else 0)
    m = re.search(r"([\d.]+\s*[kKmM]?)\s*stars?", text); s += 3 * (_to_num(m.group(1)) if m else 0)
    m = re.search(r"([\d.]+\s*[kKmM]?)\s*likes?", text); s += 20 * (_to_num(m.group(1)) if m else 0)
    return s


def source_cell(m):
    """来源：HF / GitHub / 论文，带链接"""
    lab = m.get("download_label") or ""
    u = m.get("download_url") or ""
    blob = (lab + " " + u).lower()
    if "huggingface" in blob or lab.lower() == "hf":
        name, cls = "HF", "src-hf"
    elif "github" in blob:
        name, cls = "GitHub", "src-gh"
    elif u:
        name, cls = (lab or "链接"), "src-link"
    else:
        return '<span class="src src-paper">论文</span>'
    return f'<a class="src {cls}" href="{u}">{name}</a>'


def _unify_bench(r, meta):
    m = meta.get(r["name"], {}); c = r["cells"]
    mark, org = org_mark(m, r["name"])
    date = m.get("date") or r["date"].replace("-", "/").replace("/0", "/")
    imp = m.get("impact")
    return {"dk": date_key(date), "date": date, "typ": "Benchmark",
            "name": f'{mark}<a href="{r["url"]}">{r["name"]}</a>{org}',
            "src": source_cell(m), "form": m.get("task_form") or "—",
            "size": m.get("size") or c[2],
            "impact": impact_badges(imp, m.get("impact_url")) or "—",
            "note": _md_inline(m.get("capability") or c[4]), "score": impact_score(imp),
            "lang": "—", "art": "—"}


def _unify_pipe(c, pmeta):
    nm = re.match(r"\[([^\]]+)\]\(([^)]+)\)", c[1]); name, url = nm.group(1), nm.group(2)
    m = pmeta.get(name, {})
    mark, org = org_mark(m, name)
    date = m.get("date") or c[0].replace("-", "/").replace("/0", "/")
    imp = m.get("impact")
    return {"dk": date_key(date), "date": date, "typ": m.get("typ", "数据集"),
            "name": f'{mark}<a href="{url}">{name}</a>{org}',
            "src": source_cell(m), "form": m.get("form") or c[2],
            "size": m.get("size") or c[3],
            "impact": impact_badges(imp, m.get("impact_url")) or "—",
            "note": _md_inline(m.get("feature") or c[4]), "score": impact_score(imp),
            "lang": m.get("lang") or "—", "art": m.get("art") or "—"}


def _merged_th(extra):
    cols = ["发布日期", "名称", "类型"]
    if extra:                       # Video 视图：额外给出语言与最终产物
        cols += ["语言", "产物"]
    cols += ["来源", "形态", "规模/题量", "影响力", "说明"]
    return "<thead><tr>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr></thead>"


def _merged_html(rows, topset, extra=False):
    trs = []
    for r in rows:
        cls = ' class="top5"' if id(r) in topset else ""
        typ = ('<span class="type type-bench">Benchmark</span>' if r["typ"] == "Benchmark"
               else f'<span class="type type-data">{r["typ"]}</span>')
        xtd = f'<td>{r.get("lang", "—")}</td><td>{r.get("art", "—")}</td>' if extra else ""
        trs.append(f'<tr{cls}><td>{r["date"]}</td><td>{r["name"]}</td><td>{typ}</td>{xtd}'
                   f'<td>{r["src"]}</td><td>{r["form"]}</td><td>{r["size"]}</td>'
                   f'<td>{r["impact"]}</td><td>{r["note"]}</td></tr>')
    return f'<table class="merged">{_merged_th(extra)}<tbody>' + "".join(trs) + "</tbody></table>"


def merged_tables(key, caps, bench, meta, prow, pmeta):
    """1.2 总表：benchmark 分组表与数据管线分组表按标签合并；全视图 top5 影响力标绿底。"""
    bgroups = BENCH_GROUPS.get(key)
    pgroups = PIPE_GROUPS.get(key)
    allbench = {r["name"]: r for no in caps for r in bench[no]}
    blabels = []
    if bgroups:
        for label, desc, cats, extra, exclude in bgroups:
            rows = [r for no in cats for r in bench[no] if r["name"] not in exclude] + [allbench[n] for n in extra]
            blabels.append((label, desc, [_unify_bench(r, meta) for r in rows]))
    else:
        blabels.append(("全部", "", [_unify_bench(r, meta) for no in caps for r in bench[no]]))
    name_of = lambda c: re.match(r"\[([^\]]+)\]", c[1]).group(1)
    plabels, porder = {}, []
    if pgroups:
        claimed = {n for _, _, names in pgroups if isinstance(names, list) for n in names}
        for label, desc, names in pgroups:
            if names is None:                       # 该视图主场景的全部管线
                rows = [c for sc, c in prow if sc == PIPE_GROUP_DEFAULT[key]]
            elif names == "__rest__":               # 未被其它组点名的其余管线
                rows = [c for sc, c in prow if name_of(c) not in claimed]
            else:
                rows = [c for sc, c in prow if name_of(c) in names]
            plabels[label] = [_unify_pipe(c, pmeta) for c in rows]; porder.append(label)
    else:
        plabels["全部"] = [_unify_pipe(c, pmeta) for _, c in prow]; porder.append("全部")
    blabel_set = {l for l, _, _ in blabels}
    order = [l for l, _, _ in blabels] + [l for l in porder if l not in blabel_set]
    allrows = [rr for _, _, rows in blabels for rr in rows] + [rr for rows in plabels.values() for rr in rows]
    topset = {id(rr) for rr in sorted(allrows, key=lambda x: x["score"], reverse=True)[:5] if rr["score"] > 0}
    bmap = {l: (desc, rows) for l, desc, rows in blabels}
    extra = (key == "video")

    def pane_rows(label):
        desc, brows = bmap.get(label, ("", []))
        rows = sorted(list(brows) + list(plabels.get(label, [])), key=lambda x: x["dk"])
        return desc, rows

    # 单组：不要标签条，直接出一张平表
    if len(order) == 1:
        desc, rows = pane_rows(order[0])
        out = [f'<p class="tbl-desc">{desc}</p>', ""] if desc else []
        return out + [_merged_html(rows, topset, extra=extra)]

    out = ['<div class="tbl-tabs">', ""]
    for label in order:
        desc, rows = pane_rows(label)
        out += [f'<div class="tbl-pane" data-label="{label}" data-count="{len(rows)}">', ""]
        if desc:
            out += [f'<p class="tbl-desc">{desc}</p>', ""]
        out += [_merged_html(rows, topset, extra=extra), "", "</div>", ""]
    return out + ["</div>"]


def sections(key):
    """env/<key>.md 按 <!--NAME--> 标记切段"""
    text = open(os.path.join(ROOT, "env", f"{key}.md"), encoding="utf-8").read()
    parts = re.split(r"<!--([A-Z_]+)-->", text)
    return {parts[i]: parts[i + 1].strip() for i in range(1, len(parts), 2)}


def main():
    # benchmark：类别号 → 行
    bsec = split_sections(BENCH, r"### (\d+)\. ")
    bench = {}
    for no, lines in bsec.items():
        bench[no] = []
        for c in rows_of(lines):
            m = re.match(r"\[([^\]]+)\]\(([^)]+)\)", c[1])
            bench[no].append({"date": c[0], "name": m.group(1), "url": m.group(2), "cells": c})
    # 管线：场景 → 行；精选细讲：标题 → 行
    meta = load_meta()
    pmeta = load_pipe_meta()
    psec = split_sections(PIPE, r"### 总表 · (.+)")
    deep = split_sections(PIPE, r"#### (.+)")
    for f in ("deep_web.md", "deep_3d.md", "deep_game.md", "deep_video.md"):
        p = os.path.join(ROOT, "middle_processing", f)
        if os.path.isfile(p):
            deep.update(split_sections(p, r"#### (.+)"))

    out = ["# Environment", "", '<div class="view-switch"></div>', ""]

    for key, label, caps, scenes, picks in VIEWS:
        sec = sections(key)
        nb = sum(len(bench[c]) for c in caps)
        prow = [(sc, c) for sc in scenes for c in rows_of(psec[sc])]
        nopen = sum(c[-1].startswith("是") for _, c in prow)
        toc, body = [], []

        def head(level, num, title):
            """带锚点的编号标题，同时登记进目录"""
            aid = f"{key}-" + num.replace(".", "-")
            toc.append((level, num, title, aid))
            body.extend([f'<a class="anchor" id="{aid}"></a>', "", f'{"#" * level} {num} {title}', ""])

        # 1 Open Benchmarks
        head(2, "1", "Open Benchmarks")
        head(3, "1.1", "Benchmark")
        body.extend([lab_marks(sec["FRONTIER"]), ""])
        head(3, "1.2", "Benchmark Timeline")       # 比较维度（原 Analysis Frame）放在总表前
        parts = [sec["ANALYSIS"], ""]
        if sec["LANDSCAPE"].strip():                # 有说明文字才渲染引用块，空则跳过
            parts += ["\n".join("> " + l if l.strip() else ">" for l in sec["LANDSCAPE"].splitlines()), ""]
        body.extend(parts + merged_tables(key, caps, bench, meta, prow, pmeta) + [""])
        head(3, "1.3", "Evolution")
        body.extend([sec["EVOLUTION"], ""])
        head(3, "1.4", "Use")
        body.extend([sec["CHOOSE"], ""])

        # 2 Open Data Pipelines（全部工作已并入 §1.2 总表，这里只保留观察与细讲）
        head(2, "2", "Open Data Pipelines")
        head(3, "2.1", "Observations")
        body.extend([sec["PIPE_NOTE"], ""])
        head(3, "2.2", "Deep Dives")               # 原 2.3 Selection Criteria + 2.4 Deep Dives 合并后再上移
        body.extend([sec["PICK"], ""])
        k = 0
        for p in picks:
            if p == "|":
                body.extend(["以下工作的采用度较低（下载量或 star 数为几十到几百），但带有可验证奖励或多轮修复轨迹。", ""])
                continue
            title = next((t for t in deep if t.startswith(p)), None)
            if title is None:
                print(f"  [skip] 细讲缺失：{p}")
                continue
            k += 1
            num = f"2.2.{k}"
            aid = f"{key}-" + num.replace(".", "-")
            toc.append((4, num, title, aid))
            body.extend([f'<a class="anchor" id="{aid}"></a>', "",
                         # 每条细讲是一个可折叠组件：summary 是标题行，展开后是正文
                         f'<details class="deep"><summary><span class="deep-title">{pick_logos(p)}{num} {title}{pick_orgs(p)}{pick_impact(p, pmeta)}</span></summary>',
                         ""] + with_sample(p, deep[title]) + ["", "</details>", ""])

        # 3 In-House Data Pipeline
        head(2, "3", "In-House Data Pipeline")
        body.extend(["待补充。", ""])

        # 目录卡片
        nav = ['<nav class="toc view-toc"><h2>Contents</h2><ul>']
        for level, num, title, aid in toc:
            if level == 2:                         # 目录只列一级章节
                nav.append(f'<li class="l{level}"><a href="#{aid}"><span class="num">{num}</span> {title}</a></li>')
        nav.append("</ul></nav>")

        out += [f'<div class="env-view" data-view="{key}" data-label="{label}">', "", "".join(nav), ""] + body + ["</div>", ""]

    os.makedirs(os.path.dirname(DST), exist_ok=True)
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out))
    # marked 把成对的 ~ 当删除线（「93~96%」会吞成「9396%」）：数字区间换成 –，其余换全角 ～
    text = re.sub(r"(?<=\d)\s*~\s*(?=\d)", "–", text)
    text = re.sub(r"(?<!\()~(?![^\s(]*\))", "～", text)
    open(DST, "w", encoding="utf-8").write(text)
    for key, label, caps, scenes, _ in VIEWS:
        print(f"  {label:5s} bench {sum(len(bench[c]) for c in caps):3d}  pipe {sum(1 for s in scenes for _ in rows_of(psec[s])):3d}")
    print("→", DST)


if __name__ == "__main__":
    main()

