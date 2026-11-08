#!/usr/bin/env python3
"""把 env/{web,3d,game}.md 里 <!--FRONTIER--> 段的 markdown 表转成 HTML 表

- 按 Benchmark 分组，Benchmark 列 rowspan 合并；「—」归到最后的「未报告（仅 demo）」组
- 机构与模型合成一列
- 来源只分两类：厂商自己写的（自报 / system card / 自建 / 厂商引用第三方 / demo）→ Blog；第三方榜单 → Benchmark
每次都从 middle_processing/frontier_md_backup/ 的 markdown 原稿重新生成（原稿 + EDITS → HTML），可重复运行
"""
import html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
SELF = ("Internal Design Tasks", "Kimi Webdev Bench", "CC-Frontend", "QwenReactBench", "QwenBlenderBench",
        "Parametric CAD Bench", "Trae Web Bench", "VIBE-V2")
UNCLEAR = ("Parametric CAD Bench",)   # 原文未说明是否自建，排在自建组但标「来源不明」


def md2html(t):
    """行内 markdown 链接 → <a>；其余转义（{{lab:}} 占位符保留给生成器展开）"""
    out, pos = [], 0
    for m in LINK.finditer(t):
        out.append(html.escape(t[pos:m.start()], quote=False))
        out.append(f'<a href="{m.group(2)}">{html.escape(m.group(1), quote=False)}</a>')
        pos = m.end()
    out.append(html.escape(t[pos:], quote=False))
    return "".join(out)


def source_cell(t):
    links = LINK.findall(t)
    if not links:
        return html.escape(t.replace("仅 demo", "Blog").strip(), quote=False) if "未找到官方页" not in t else "—（媒体转述，未找到官方页）"
    if len(links) == 1:
        label, url = links[0]
        kind = "Benchmark" if label.startswith("第三方榜单") else "Blog"
        return f'<a href="{url}">{kind}</a>'
    return "Blog：" + " · ".join(f'<a href="{u}">{html.escape(l)}</a>' for l, u in links)


def convert(table_md):
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in table_md.strip().splitlines()[2:]]
    groups, order = {}, []
    for org, model, bench, score, note, src in rows:
        key = "未报告相关分数" if bench in ("—", "") else bench
        if key not in groups:
            groups[key] = []; order.append(key)
        groups[key].append((f"{org} {model}", score, note, src))
    # 排序：公开 benchmark（按报告的模型数降序）→ 自建 / 来源不明 → 未报告（仅 demo）
    plain = lambda k: LINK.sub(lambda m: m.group(1), k)
    is_self = lambda k: any(plain(k).startswith(x) for x in SELF)
    pub = sorted([k for k in order if not k.startswith("未报告") and not is_self(k)], key=lambda k: -len(groups[k]))
    own = [k for k in order if not k.startswith("未报告") and is_self(k)]
    order = pub + own + [k for k in order if k.startswith("未报告")]
    h = ['<table class="frontier"><thead><tr><th>Benchmark</th><th>模型</th><th>分数</th><th>口径</th><th>来源</th></tr></thead><tbody>']
    for k in order:
        g = groups[k]
        for i, (om, score, note, src) in enumerate(g):
            tag = (f'<span class="self-tag">{"来源不明" if any(plain(k).startswith(x) for x in UNCLEAR) else "自建"}</span>'
                   if is_self(k) else "")
            first = f'<td rowspan="{len(g)}" class="bench">{md2html(k)}{tag}</td>' if i == 0 else ""
            h.append(f"<tr>{first}<td>{md2html(om)}</td><td>{md2html(score)}</td><td>{md2html(note)}</td><td>{source_cell(src)}</td></tr>")
    h.append("</tbody></table>")
    return "".join(h)


EDITS = {
    "web": [
        ("| {{lab:DeepSeek}} | DeepSeek-V4-Pro-0813 | DSBench-FullStack | 71.1 | 内部全栈测试集，不专测视觉 | [自建评测集（model card）](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813) |",
         "| {{lab:DeepSeek}} | DeepSeek-V4.1-Flash | — | 未报告 | 技术报告只定性提到用渲染截图做视觉自检，没有视觉 coding 分数；V4-Pro 另报的 DSBench-FullStack 是内部全栈集，不测视觉 | [Blog](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) |"),
        ("| GPT-6 Astra | [Code Arena · WebDev](https://arena.ai/leaderboard/code/webdev) | 1793（第 1） | Arena Elo，2026-09-23 |", "| GPT-6 Astra | [Code Arena · WebDev](https://arena.ai/leaderboard/code/webdev) | 1793（第 1） | Overall 总榜，Arena Elo，2026-09-23 |"),
        ("| Claude Opus 5 | [Code Arena · WebDev](https://arena.ai/leaderboard/code/webdev) | 1691（第 3） | Arena Elo |", "| Claude Opus 5 | [Code Arena · WebDev](https://arena.ai/leaderboard/code/webdev) | 1691（第 3） | Overall 总榜，Arena Elo，2026-09-23 |"),
        ("| Gemini 3.7 Flash | [Code Arena · WebDev](https://arena.ai/leaderboard/code/webdev) | 1588 | 引用公开榜单；3.8 Flash 的表里去掉了这一项 |", "| Gemini 3.7 Flash | [Code Arena · WebDev](https://arena.ai/leaderboard/code/webdev) | 1588 | 厂商引用，分类未注明；3.8 Flash 的表里去掉了这一项 |"),
        ("| Kimi K3 | [WebDev Arena](https://arena.ai/leaderboard/code/webdev) | 1678（第 1，2026-07-23） | 写入技术报告 |", "| Kimi K3 | [Code Arena · WebDev](https://arena.ai/leaderboard/code/webdev) | 1678（第 1，2026-07-23） | 厂商引用，分类未注明；报告中用旧名 WebDev Arena |"),
        ("| GLM-5.3-Flash | Vision2Web | 77.8 | 未给评测设置 |", "| GLM-5.3-Flash | [Vision2Web](https://arxiv.org/abs/2603.26648) | 77.8 | 未给评测设置；Vision2Web 由智谱与清华发布 |"),
        ("| Qwen3.8-Max | Vision2Web | 69.0 |", "| Qwen3.8-Max | [Vision2Web](https://arxiv.org/abs/2603.26648) | 69.0 |"),
        ("| Seed2.1 Pro | [Code Arena · Frontend](https://arena.ai/leaderboard/code) | 1539（第 8） | 发布时快照 |", "| Seed2.1 Pro | [Code Arena · WebDev](https://arena.ai/leaderboard/code/webdev) | 1539（第 8） | Frontend 分类，发布时快照 |"),
    ],
    "3d": [
        ("| {{lab:DeepSeek}} · {{lab:Tencent Hunyuan}} · {{lab:MiniMax}} | 最新旗舰 |", "| {{lab:DeepSeek}} {{lab:Tencent Hunyuan}} {{lab:MiniMax}} | DeepSeek-V4-Pro-0813 / Hy4 preview / MiniMax-M3 |"),
        ("| GPT-6 Astra | Blender 建模并导入 UE5 | — | 发布页视频与开发者博客 |", "| GPT-6 Astra | — | 未报告 | Blender 建模并导入 UE5（发布页视频与开发者博客） |"),
        ("| Claude Opus 5 | FreeCAD 按图纸重建零件 | — | Frontier-Bench 中的一题，无单独分数 |", "| Claude Opus 5 | — | 未报告 | FreeCAD 按图纸重建零件（Frontier-Bench 中的一题，无单独分数） |"),
        ("| Claude Opus 5 | [BenchCAD Vision2Code](https://benchcad.com/leaderboard) | 0.366 / 0.821 | voxel IoU，", "| Claude Opus 5 | [BenchCAD](https://benchcad.com/leaderboard) | 0.366 / 0.821 | Vision2Code 子任务，voxel IoU，"),
        ("| Claude Mythos 5 | [BenchCAD Vision2Code](https://benchcad.com/leaderboard) | 0.384 | voxel IoU，", "| Claude Mythos 5 | [BenchCAD](https://benchcad.com/leaderboard) | 0.384 | Vision2Code 子任务，voxel IoU，"),
    ],
    "game": [
        ("| Claude Opus 5 | ARC-AGI-3 | 30.2% | 交互式环境推理，不是做游戏 |", "| Claude Opus 5 | — | 未报告 | 只报了 ARC-AGI-3（30.2%），测交互式环境推理，是玩游戏不是做游戏 |"),
        ("| Seed2.1 Pro | GameWorld | 31.2 | 玩浏览器游戏，不是做游戏 |", "| Seed2.1 Pro | — | 未报告 | 只报了 GameWorld（31.2），测玩浏览器游戏，不是做游戏 |"),
    ],
}
SRC = os.path.join(ROOT, "middle_processing", "frontier_md_backup")   # 转换前的 markdown 原稿

for key in ("web", "3d", "game"):
    p = os.path.join(ROOT, "env", f"{key}.md")
    s = open(os.path.join(SRC, f"{key}.md"), encoding="utf-8").read()
    for a, b in EDITS[key]:
        if a in s:
            s = s.replace(a, b)
    a = s.index("<!--FRONTIER-->")
    seg = s[a:]
    t0 = seg.index("| 机构 | 模型 |")
    lines = seg[t0:].split("\n")
    n = 0
    while n < len(lines) and lines[n].startswith("|"):
        n += 1
    old = "\n".join(lines[:n])
    s = s[:a] + seg.replace(old, convert(old), 1)
    open(p, "w", encoding="utf-8").write(s)
    print(key, "converted")

