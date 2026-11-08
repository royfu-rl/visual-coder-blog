#!/usr/bin/env python3
r"""Generate the "Gallery" showcase page: gallery/gallery.md + gallery/demos/*.html.

一面陈列墙：把 /mmu_mllm_hdd_4/infra/visual-coding/three-js 下那组手写的交互式
three.js 场景，做成一组优雅的卡片。点卡片 → 全屏 lightbox 里实时运行该 demo
（懒加载：iframe 点开才创建、关闭即销毁，任何时刻最多一个 WebGL 上下文，绕开浏览器
对并发 WebGL 上下文数量的限制）。

工作流：`python3 scripts/gen_gallery_page.py` → 回项目根 `python3 build.py`。

和 build.py / template.html 对齐的硬约束：
  * 卡片网格是一段 raw HTML，marked 在浏览器里重新解析。CommonMark 规定块级 HTML
    到第一行空行就结束，所以整段网格**不能有空行**。
  * 卡片不写字面量 <iframe src="...">，而是把目标路径放在 data-src 上、点击时由
    template.html 的 galOpen() 动态建 iframe —— 这样 build.py 的 inline_iframes
    不会把 11 个 demo（每个 ~50–85KB）全内联进 index.html，页面保持精简；demo 文件
    留作独立 .html，运行时经 /view 网关按相对路径取用。
  * data-src 用「data-」前缀，正好落在 build.py _SRC_RE 的 (?<![-\w]) 负向前视外，
    不会被当成图片 src 改写。
"""
from __future__ import annotations

import os
import shutil

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GALLERY = os.path.join(ROOT, "gallery")
DEMOS   = os.path.join(GALLERY, "demos")
SRC_DIR = "/mmu_mllm_hdd_4/infra/visual-coding/three-js"


# --------------------------------------------------------------------------- #
# demo 清单：(slug, 中文名, 英文名（沿用 demo 自己的 <title>）, 一句话简介, 主题渐变)
# 顺序是策展过的——冷暖、明暗交错，让整墙看起来有节奏。
# --------------------------------------------------------------------------- #
DEMOS_LIST = [
    ("tiny-planet",    "小星球",     "Tiny Planet.",
     "弯曲地平线的迷你星球，风车、木屋、湖泊一应俱全。",
     "linear-gradient(145deg,#4fa16a,#15213f)"),
    ("sky-island",     "浮空岛",     "Cloud Harbor.",
     "倒锥形浮空岛，岛上港口小镇，岛底垂下树根与藤蔓。",
     "linear-gradient(145deg,#8fd0f4,#3a74b0)"),
    ("snow-globe",     "雪球小镇",   "Snow Globe.",
     "玻璃雪球里的尖顶小镇，窗透暖黄，雪落其中。",
     "linear-gradient(145deg,#35508a,#e9b24e)"),
    ("bonsai-seasons", "四季盆景",   "Four Seasons.",
     "递归生成的虬曲老树盆景，一键在春夏秋冬间切换。",
     "linear-gradient(145deg,#4e7a4a,#c56a35)"),
    ("brass-orrery",   "黄铜天象仪", "The Orrery.",
     "胡桃木底座上的八大行星，由黄铜悬臂支撑转动。",
     "linear-gradient(145deg,#241a10,#c39a4e)"),
    ("lava-lamp",      "熔岩灯",     "Lava Lamp.",
     "70 年代熔岩灯，蜡团在瓶中融合、分裂、拉丝。",
     "linear-gradient(145deg,#e8512f,#6a2d86)"),
    ("marble-run",     "弹珠轨道",   "Marble Run.",
     "枫木轨道塔，弹珠滚过亚克力管道与之字斜槽。",
     "linear-gradient(145deg,#cdb389,#4a6b8a)"),
    ("claw-machine",   "复古娃娃机", "Claw Club.",
     "糖果色娃娃机，霓虹灯牌加一屋毛绒玩具，可抓。",
     "linear-gradient(145deg,#ff9ec4,#74dcc0)"),
    ("popup-book",     "立体书",     "Pop-Up City.",
     "翻开的精装书里立起一座纸艺城市。",
     "linear-gradient(145deg,#e7dcc4,#2b3a67)"),
    ("ramen-bowl",     "深夜拉面",   "Midnight Ramen.",
     "粗陶碗里的琥珀汤拉面，配料齐全，热气升腾。",
     "linear-gradient(145deg,#1b2a5c,#d2922f)"),
    ("pirate-jelly",   "海盗果冻岛", "Pirate Jelly.",
     "果冻海水沙盘，椰林、宝箱、篝火与骷髅礁石。",
     "linear-gradient(145deg,#15b39e,#d8b86a)"),
]


# --------------------------------------------------------------------------- #
# 复制 demo 本体到 gallery/demos/<slug>.html（这些场景是纯程序化生成，无本地素材依赖）
# --------------------------------------------------------------------------- #
def copy_demos() -> list[str]:
    os.makedirs(DEMOS, exist_ok=True)
    copied = []
    for slug, *_ in DEMOS_LIST:
        src = os.path.join(SRC_DIR, slug, "index.html")
        if not os.path.isfile(src):
            print(f"  [skip] {slug} (源缺失: {src})")
            continue
        shutil.copy2(src, os.path.join(DEMOS, f"{slug}.html"))
        copied.append(slug)
    return copied


# --------------------------------------------------------------------------- #
# 一张卡片（无字面量 iframe src；点击交给 galOpen）
# --------------------------------------------------------------------------- #
def card(i: int, slug: str, cn: str, en: str, cap: str, grad: str) -> str:
    return (
        f'<div class="gal-card" role="button" tabindex="0" '
        f'data-src="gallery/demos/{slug}.html" data-title="{cn}" data-en="{en}" '
        f'onclick="galOpen(this)" onkeydown="if(event.key===\'Enter\'||event.key===\' \'){{event.preventDefault();galOpen(this)}}">'
        f'<div class="gal-poster" style="background:url(\'gallery/posters/{slug}.jpg\') center/cover no-repeat,{grad}">'
        f'<span class="gal-play">⤢ 点击全屏互动</span>'
        f'</div>'
        f'<div class="gal-meta">'
        f'<div class="gal-cn">{cn}</div>'
        f'<div class="gal-cap">{cap}</div>'
        f'<code class="gal-slug">{slug}</code>'
        f'</div>'
        f'</div>'
    )


# --------------------------------------------------------------------------- #
# 组装 gallery.md
# --------------------------------------------------------------------------- #
def build_md(slugs: set[str]) -> str:
    cards = "\n".join(
        card(i, slug, cn, en, cap, grad)
        for i, (slug, cn, en, cap, grad) in enumerate(DEMOS_LIST, 1)
        if slug in slugs
    )
    grid = f'<div class="gal-grid">\n{cards}\n</div>'
    return f"""# 画廊 · Gallery

一组用 **three.js** 手写的交互式 3D 场景——全部是*单文件、纯程序化生成*的：没有外部
模型、没有贴图，整幕画面都由代码当场算出来，在浏览器里实时渲染。

下面每张卡片是该场景的**实拍画面**。点任意一张，进入**全屏实时运行**——可以拖拽旋转、
滚轮缩放，多数场景还能点击交互（种树、摇雪球、开宝箱、转动天象仪……）。

{grid}

> 每个场景都是一份独立的 `index.html`，只在运行时从 CDN 取 three.js 本体——卡片放大后
> 右上角「**在新标签打开 ↗**」，打开的就是该 demo 本体。
"""


def main() -> None:
    slugs = copy_demos()
    md = build_md(set(slugs))
    os.makedirs(GALLERY, exist_ok=True)
    with open(os.path.join(GALLERY, "gallery.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(f"  wrote {os.path.relpath(os.path.join(GALLERY, 'gallery.md'), ROOT)}")
    print(f"  copied {len(slugs)} demos -> {os.path.relpath(DEMOS, ROOT)}/")
    for slug in slugs:
        print(f"    - demos/{slug}.html")


if __name__ == "__main__":
    main()

