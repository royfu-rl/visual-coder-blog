#!/usr/bin/env python3
"""Generate the "Basic" teaching page: basic/basic.md + basic/demos/*.html.

一个给纯小白的入门页：用「代码在左 / 浏览器实时渲染在右」的方式，最小成本看懂
本项目里出现的那一堆语言。每个 live demo 的「展示代码」和「右边运行的文件」出自
同一份源串，所以两边永远不会对不上。

工作流：改本文件 → `python3 scripts/gen_basic_page.py` → 回项目根 `python3 build.py`。

几个硬约束（和 build.py / template.html 对齐）：
  * 每个 demo 块是一段 raw HTML，marked 在浏览器里会重新解析。CommonMark 规定
    块级 HTML 到第一行空行就结束，所以 demo 块内部**不能有空行**；<pre> 里的换行
    一律写成 &#10;，整段代码压成一行。
  * <pre> 的文本里若出现裸 ` 或 $，会被 renderDoc 的 code-span / math 正则吞掉，
    所以 esc() 把 ` $ ~ | 也转成数字实体。
  * 右边的 <iframe src="demos/x.html"> 由 build.py 的 inline_iframes 自动内联成
    srcdoc，页面因此保持单文件自包含。
"""
from __future__ import annotations

import os

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASIC = os.path.join(ROOT, "basic")
DEMOS = os.path.join(BASIC, "demos")


# --------------------------------------------------------------------------- #
# 转义：把展示代码塞进 raw-HTML <pre> 里而不被 marked / renderDoc 破坏
# --------------------------------------------------------------------------- #
def esc(s: str) -> str:
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = (s.replace("$", "&#36;").replace("`", "&#96;")
          .replace("~", "&#126;").replace("|", "&#124;"))
    return s.replace("\n", "&#10;")


# --------------------------------------------------------------------------- #
# demo 右侧可运行文件的壳
# --------------------------------------------------------------------------- #
_SHELL = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{{box-sizing:border-box}}
html,body{{margin:0;min-height:100%}}
body{{{layout}font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",system-ui,sans-serif;
 color:#111418;padding:18px;background:#fff;line-height:1.6}}
button{{font:inherit;font-size:14px;padding:8px 15px;border:1px solid #e4e7ec;border-radius:10px;
 background:#f6f7f9;color:#111418;cursor:pointer;transition:.15s}}
button:hover{{border-color:#2f6bff;color:#2f6bff}}
.n{{font-size:20px;font-weight:700;color:#2f6bff}}
.hint{{position:fixed;left:8px;bottom:6px;font-size:11px;color:#b6bcc6}}
{css}
</style></head><body>
{body}
{script}
</body></html>"""

_CENTER = ("display:flex;align-items:center;justify-content:center;"
           "gap:14px;flex-wrap:wrap;text-align:center;")


def shell(body: str, *, css: str = "", script: str = "", center: bool = True,
          hint: str = "") -> str:
    layout = _CENTER if center else ""
    if hint:
        body = body + f'\n<div class="hint">{hint}</div>'
    return _SHELL.format(layout=layout, css=css, body=body,
                         script=script).strip()


# --------------------------------------------------------------------------- #
# demo 块（写进 basic.md 的那段 raw HTML —— 内部严禁空行）
# --------------------------------------------------------------------------- #
def demo_block(slug: str, lang: str, lang_cls: str, title: str,
               shown: str, note: str, height: int) -> str:
    return (
        '<div class="demo">\n'
        f'<div class="demo-top"><span class="demo-lang {lang_cls}">{lang}</span>'
        f'<span class="demo-title">{title}</span></div>\n'
        '<div class="demo-split">\n'
        f'<pre class="demo-code"><code>{esc(shown)}</code></pre>\n'
        f'<iframe class="demo-frame" style="height:{height}px" '
        f'src="demos/{slug}.html"></iframe>\n'
        '</div>\n'
        f'<p class="demo-note">{note}</p>\n'
        '</div>'
    )


# =========================================================================== #
# 1. HTML —— 裸骨架
# =========================================================================== #
html_markup = """<h2>我的第一个网页</h2>
<p>这是一个段落。下面是一个列表：</p>
<ul>
  <li>苹果</li>
  <li>香蕉</li>
</ul>
<a href="#">一个链接</a>"""

d_html = (
    demo_block(
        "html-bare", "HTML", "lang-html", "只有结构，不化妆",
        html_markup,
        "只有 HTML、没写任何样式时，浏览器用<b>默认外观</b>——这就是网页的"
        "「结构 / 骨架」。标题、段落、列表、链接都用一对尖括号标签框起来。",
        210),
    shell(html_markup, center=False, hint="纯 HTML · 浏览器默认样式"),
)


# =========================================================================== #
# 2. CSS —— 给同一段结构化妆（用户点名要的例子）
# =========================================================================== #
css_rules = """.card {
  width: 220px;
  padding: 22px;
  border-radius: 16px;
  color: #fff;
  background: linear-gradient(135deg, #2f6bff, #8b5cf6);
  box-shadow: 0 12px 30px rgba(47,107,255,.35);
  transition: transform .2s ease;
}
.card:hover { transform: translateY(-6px); }
.card h3 { margin: 0 0 6px; font-size: 18px; }
.card p  { margin: 0; opacity: .85; font-size: 13px; }"""

css_markup = """<div class="card">
  <h3>Visual Coder</h3>
  <p>把鼠标移上来试试</p>
</div>"""

css_shown = f"""<!-- HTML：还是那套结构 -->
{css_markup}

/* CSS：负责「长什么样」 */
{css_rules}"""

d_css = (
    demo_block(
        "css-box", "CSS", "lang-css", "同一段结构，CSS 负责外观",
        css_shown,
        "同样一段 HTML，<b>CSS 决定「长什么样」</b>：颜色、圆角、阴影、渐变，"
        "还有鼠标悬停时的动画。把光标移到右边的卡片上看看。这就是前端最常改的东西。",
        260),
    shell(css_markup, css=css_rules, hint="HTML + CSS"),
)


# =========================================================================== #
# 3. JavaScript —— 行为
# =========================================================================== #
js_markup = '<button id="btn">点我 +1</button> <span class="n" id="n">0</span>'
js_code = """let count = 0;
const btn = document.getElementById('btn');
btn.onclick = () => {
  count = count + 1;
  document.getElementById('n').textContent = count;
};"""
js_shown = f"""<!-- HTML 先画出按钮 -->
{js_markup}

// JavaScript 负责「交互 / 行为」
{js_code}"""

d_js = (
    demo_block(
        "js-counter", "JavaScript", "lang-js", "点击后页面会变",
        js_shown,
        "HTML 把按钮画出来，<b>JavaScript 负责「交互 / 行为」</b>：点一下就改变页面。"
        "到这里网页三件套就齐了——<b>结构(HTML) / 样式(CSS) / 行为(JS)</b>，各管一摊。",
        200),
    shell(js_markup, script=f"<script>{js_code}</script>",
          hint="HTML + JavaScript · 可点击"),
)


# =========================================================================== #
# 4. SVG —— 用标签画矢量图（内置动画）
# =========================================================================== #
svg_code = """<svg width="240" height="150" viewBox="0 0 240 150">
  <rect x="10" y="10" width="220" height="130" rx="16" fill="#eaf0ff"/>
  <circle cx="60" cy="70" r="26" fill="#2f6bff">
    <animate attributeName="cx" values="60;180;60"
             dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="120" y="135" text-anchor="middle"
        font-size="12" fill="#5b636e">SVG 用标签画图形</text>
</svg>"""

d_svg = (
    demo_block(
        "svg-draw", "SVG", "lang-svg", "像写标签一样画图，还能动",
        svg_code,
        "<b>SVG 是「用标签画出来的矢量图」</b>——写法和 HTML 一样，但画的是圆、"
        "矩形、路径，而且能内置动画。图表、图标、插画常用它。下一个要讲的 Lottie，"
        "就是把这类动画导成一段数据。",
        230),
    shell(svg_code, hint="SVG · 矢量图 + 动画"),
)


# =========================================================================== #
# 5. React —— 不是新语言，是用 JS 写界面的框架
# =========================================================================== #
react_shown = """function Counter() {
  // useState：记住一个会变的数字 n
  const [n, setN] = React.useState(0);
  return (
    <button onClick={() => setN(n + 1)}>
      你点了 {n} 次
    </button>
  );
}"""
react_body = '<button id="b">你点了 <span id="k">0</span> 次</button>'
react_script = ("<script>let n=0;const k=document.getElementById('k');"
                "document.getElementById('b').onclick=()=>{n++;k.textContent=n;};</script>")

d_react = (
    demo_block(
        "react-counter", "React", "lang-react", "把界面拆成「组件」",
        react_shown,
        "<b>React 不是第四种语言，而是用 JavaScript 写界面的框架</b>：把页面拆成一个个"
        "可复用的「组件」，数据(n)一变，界面自动重画，不用自己手动改 DOM。"
        "<b>和 CSS 的关系</b>：React 管「结构和数据怎么变」，CSS 管「长什么样」，两者"
        "正交、配合用。右边是这个组件渲染后的实际效果（为便于离线查看用等价原生 JS 驱动，交互一致）。",
        200),
    shell(react_body, script=react_script,
          hint="React 组件的渲染效果 · 可点击"),
)


# =========================================================================== #
# 6. Lottie —— 本质是一段 JSON 数据，不是代码
# =========================================================================== #
lottie_shown = """{
  "v": "5.7",              // 版本
  "fr": 30,                // 帧率
  "w": 120, "h": 120,      // 画布尺寸
  "layers": [
    { "ty": 4, "nm": "圆",
      "ks": {              // 用关键帧描述「从小变大」
        "s": { "k": [ { "t": 0,  "s": [20] },
                      { "t": 30, "s": [100] } ] }
      } }
  ]
}"""
lottie_body = '<div id="dot"></div>'
lottie_css = ("#dot{width:70px;height:70px;border-radius:50%;background:#9333a8;"
              "animation:pp 1.6s ease-in-out infinite}"
              "@keyframes pp{0%,100%{transform:scale(.3)}50%{transform:scale(1)}}")

d_lottie = (
    demo_block(
        "lottie-json", "JSON", "lang-json", "动画也能是「数据」",
        lottie_shown,
        "<b>Lottie 本质是一段 JSON（数据，不是代码）</b>：设计师在 After Effects 里做好"
        "动画，导出成这样一份文件，网页 / App 用一个小播放器按帧播放它，体积小又清晰。"
        "右边是这段数据所描述效果的<b>浏览器示意</b>。",
        230),
    shell(lottie_body, css=lottie_css, hint="Lottie 数据的效果示意"),
)


# =========================================================================== #
# 7. Python + Manim —— 数学动画引擎
# =========================================================================== #
manim_shown = """from manim import *

class Demo(Scene):
    def construct(self):
        c = Circle(color=BLUE)
        self.play(Create(c))                 # 先画出一个圆
        self.play(Transform(c, Square(color=GREEN)))  # 圆变成方
        self.wait()"""
manim_body = '<div id="sh"></div>'
manim_css = ("#sh{width:92px;height:92px;background:#2f6bff;"
             "animation:mm 3s ease-in-out infinite}"
             "@keyframes mm{0%,20%{border-radius:50%;background:#2f6bff;transform:rotate(0)}"
             "60%,100%{border-radius:8px;background:#16a34a;transform:rotate(90deg)}}")

d_manim = (
    demo_block(
        "manim-morph", "Python · Manim", "lang-py", "用 Python 描述数学动画",
        manim_shown,
        "<b>Manim 是 Python 的「数学动画引擎」</b>（3Blue1Brown 发明）：你用 Python "
        "描述有哪些对象、要「播放」什么动作，引擎自己算出每一帧并渲成视频。右边是"
        "<b>浏览器示意</b>——真正的 Manim 产物是一个 mp4 文件，不在网页里跑。",
        260),
    shell(manim_body, css=manim_css, hint="Manim 效果示意（真实产物是 mp4）"),
)


# =========================================================================== #
# 8. 三者嵌套：HTML 装 SVG，一套 CSS 同时修饰两者
# =========================================================================== #
combo_markup = """<!-- HTML：一张卡片，里面嵌一个 SVG 太阳 -->
<div class="card">
  <h3>Sunny</h3>
  <svg viewBox="0 0 120 120" width="112" height="112">
    <g class="rays">                        <!-- 一组光芒 -->
      <line x1="60" y1="6"  x2="60" y2="22"/>
      <line x1="60" y1="98" x2="60" y2="114"/>
      <line x1="6"  y1="60" x2="22" y2="60"/>
      <line x1="98" y1="60" x2="114" y2="60"/>
    </g>
    <circle class="sun" cx="60" cy="60" r="24"/>
  </svg>
</div>"""

combo_css = """/* CSS 修饰 HTML 元素 */
.card {
  width: 180px; padding: 20px; text-align: center;
  border-radius: 18px; color: #fff;
  background: linear-gradient(135deg, #f6b73c, #e0566a);
}
.card h3 { margin: 0 0 8px; }

/* 同一套 CSS，也在修饰 SVG 元素 */
.sun { fill: #fff; }                   /* 注意：是 fill 不是 background */
.rays line { stroke: #fff; stroke-width: 5; stroke-linecap: round; }
.rays {                                /* CSS 让 SVG 的光芒转起来 */
  transform-box: view-box;
  transform-origin: 60px 60px;
  animation: spin 6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }"""

combo_shown = f"{combo_markup}\n\n<style>\n{combo_css}\n</style>"

d_combo = (
    demo_block(
        "combo-card", "HTML + CSS + SVG", "lang-html", "一张卡片同时用上三者",
        combo_shown,
        "看清楚三层:<b>HTML</b> 的 <b>&lt;div class=\"card\"&gt;</b> 里<b>嵌着一个 &lt;svg&gt;</b>"
        "(HTML 装 SVG);<b>同一套 CSS</b> 既修饰了 HTML 的 <b>.card</b>(渐变背景),也修饰了 SVG 的 "
        "<b>.sun / .rays</b>(填充白色、并让光芒转起来)。注意给圆上色用的是 <b>fill</b> 不是 background"
        "——这就是「HTML/SVG 造元素、CSS 修饰元素」的真实样子。",
        300),
    shell(combo_markup, css=combo_css, hint="HTML 嵌 SVG · 一套 CSS 修饰两者"),
)


# =========================================================================== #
# 9. three.js —— 浏览器里的实时 3D（JS 的 3D 库，基于 WebGL）
# =========================================================================== #
three_shown = """import * as THREE from 'three';

// three.js 的「四件事」：场景 / 相机 / 渲染器 / 网格
const scene    = new THREE.Scene();
const camera   = new THREE.PerspectiveCamera(50, w / h, 0.1, 100);
camera.position.set(2.4, 1.8, 2.8);
const renderer = new THREE.WebGLRenderer({ antialias: true });

// 放一个立方体，给它材质，再打一盏灯
const cube = new THREE.Mesh(
  new THREE.BoxGeometry(1.4, 1.4, 1.4),
  new THREE.MeshStandardMaterial({ color: 0x2f6bff })
);
scene.add(cube);
scene.add(new THREE.DirectionalLight(0xffffff, 1.3));

// 每帧转一点、重新渲染（动画就是这么来的）
function loop() {
  requestAnimationFrame(loop);
  cube.rotation.y += 0.006;
  renderer.render(scene, camera);
}
loop();"""

three_run = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>*{margin:0;box-sizing:border-box}html,body{height:100%;overflow:hidden;background:#0f1115}
canvas{display:block}.hint{position:fixed;left:9px;bottom:7px;font:11px -apple-system,system-ui,sans-serif;color:#7a828e}</style>
<script type="importmap">{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js"}}</script>
</head><body>
<div class="hint">three.js · 浏览器实时 3D（可拖动旋转）</div>
<script type="module">
import * as THREE from 'three';
const scene = new THREE.Scene();
const cam = new THREE.PerspectiveCamera(50, innerWidth/innerHeight, 0.1, 100);
cam.position.set(2.4, 1.8, 2.8); cam.lookAt(0, 0, 0);
const r = new THREE.WebGLRenderer({ antialias: true });
r.setPixelRatio(Math.min(devicePixelRatio, 2)); r.setSize(innerWidth, innerHeight);
document.body.appendChild(r.domElement);
const cube = new THREE.Mesh(
  new THREE.BoxGeometry(1.4, 1.4, 1.4),
  new THREE.MeshStandardMaterial({ color: 0x2f6bff, roughness: .35, metalness: .1 }));
scene.add(cube);
scene.add(new THREE.HemisphereLight(0xffffff, 0x334155, 1.1));
const dir = new THREE.DirectionalLight(0xffffff, 1.3); dir.position.set(3, 5, 2); scene.add(dir);
let px = 0, py = 0, down = false;
r.domElement.addEventListener('pointerdown', e => { down = true; px = e.clientX; py = e.clientY; });
addEventListener('pointerup', () => down = false);
addEventListener('pointermove', e => { if (!down) return;
  cube.rotation.y += (e.clientX - px) * 0.01; cube.rotation.x += (e.clientY - py) * 0.01;
  px = e.clientX; py = e.clientY; });
addEventListener('resize', () => { cam.aspect = innerWidth/innerHeight; cam.updateProjectionMatrix();
  r.setSize(innerWidth, innerHeight); });
(function loop(){ requestAnimationFrame(loop);
  if (!down) { cube.rotation.y += 0.006; cube.rotation.x += 0.003; }
  r.render(scene, cam); })();
</script>
</body></html>"""

d_three = (
    demo_block(
        "threejs-cube", "JavaScript · three.js", "lang-js", "浏览器里摆一个真三维场景",
        three_shown,
        "<b>three.js 是 JavaScript 的 3D 库</b>（基于 <b>WebGL</b>）：还是写 JS、还是浏览器直接打开，"
        "只是从「画 2D」升级成「摆一个真三维场景」——<b>场景 / 相机 / 光源 / 网格</b>，每帧渲染一次。"
        "它是网页做 3D 最主流的库。右边可以<b>拖动旋转</b>；本站 <b>Gallery</b> 整面墙都是它写的。",
        300),
    three_run,
)


# =========================================================================== #
# 10. Blender —— 专业 3D 软件，用 Python(bpy) 脚本控制，离线渲染
# =========================================================================== #
blender_shown = """import bpy   # Blender 的 Python 接口

# 1) 建模：往场景里加一个立方体
bpy.ops.mesh.primitive_cube_add(size=2)
cube = bpy.context.active_object

# 2) 给它一个蓝色材质
mat = bpy.data.materials.new("Blue")
mat.diffuse_color = (0.18, 0.42, 1.0, 1.0)
cube.data.materials.append(mat)

# 3) 渲染成一张图片（离线，不在浏览器里）
bpy.context.scene.render.filepath = "//cube.png"
bpy.ops.render.render(write_still=True)"""

blender_body = '<div class="scene"><div class="cube"><span></span><span></span><span></span><span></span><span></span><span></span></div></div>\n<div class="tag">离线渲染 → 图 / mp4 / .glb 模型</div>'
blender_css = """.scene{perspective:620px;width:120px;height:120px;display:grid;place-items:center}
.cube{position:relative;width:78px;height:78px;transform-style:preserve-3d;animation:bspin 9s linear infinite}
.cube span{position:absolute;width:78px;height:78px;border:1px solid rgba(255,255,255,.55);
 background:linear-gradient(135deg,rgba(47,107,255,.78),rgba(99,102,241,.78))}
.cube span:nth-child(1){transform:translateZ(39px)}
.cube span:nth-child(2){transform:rotateY(180deg) translateZ(39px)}
.cube span:nth-child(3){transform:rotateY(90deg) translateZ(39px)}
.cube span:nth-child(4){transform:rotateY(-90deg) translateZ(39px)}
.cube span:nth-child(5){transform:rotateX(90deg) translateZ(39px)}
.cube span:nth-child(6){transform:rotateX(-90deg) translateZ(39px)}
@keyframes bspin{to{transform:rotateX(360deg) rotateY(360deg)}}
.tag{margin-top:14px;font-size:12px;color:#5b636e}"""

d_blender = (
    demo_block(
        "blender-cube", "Python · bpy (Blender)", "lang-py", "软件建模，离线渲染成文件",
        blender_shown,
        "<b>Blender 不是网页技术，是一款专业 3D 软件</b>（建模 / 动画 / 渲染都在它里面做）。"
        "你写的其实是 <b>Python(bpy)</b> 去「遥控」它：加物体、给材质、按下渲染。<b>产物是离线文件</b>"
        "——一张图、一段 mp4，或一个 <b>.glb 3D 模型</b>。那个 .glb 还能反过来丢给 <b>three.js</b> 在"
        "网页里加载：<b>Blender 建好模型 → three.js 在浏览器里展示</b>，这就是两者的接力。右边是 CSS 示意。",
        260),
    shell(blender_body, css=blender_css, hint="Blender 示意（真实产物是离线文件）"),
)


DEMO_FILES = {
    "html-bare": d_html[1], "css-box": d_css[1], "js-counter": d_js[1],
    "svg-draw": d_svg[1], "react-counter": d_react[1],
    "lottie-json": d_lottie[1], "manim-morph": d_manim[1],
    "combo-card": d_combo[1], "threejs-cube": d_three[1], "blender-cube": d_blender[1],
}


# =========================================================================== #
# basic.md 正文
# =========================================================================== #
MD = f"""# Basic

## Contents

- [三家「厨房」：先把语言归类](#三家厨房先把语言归类)
- [网页系：HTML / CSS / JS 的分工](#网页系html--css--js-的分工)
  - [React 和 CSS 是什么关系](#react-和-css-是什么关系)
  - [SVG 与 Lottie：画图与数据化的动画](#svg-与-lottie画图与数据化的动画)
  - [三者嵌套：HTML 装 SVG，一套 CSS 修饰两者](#三者嵌套html-装-svg一套-css-修饰两者)
- [3D 系：three.js 与 Blender](#3d-系threejs-与-blender)
  - [three.js：浏览器里的实时 3D](#threejs浏览器里的实时-3d)
  - [Blender：用软件建模，离线渲染](#blender用软件建模离线渲染)
- [数学动画系：Python + Manim](#数学动画系python--manim)
- [幻灯片系：pptx / LaTeX-Beamer](#幻灯片系pptx--latex-beamer)
- [一张总表：全部语言的地位](#一张总表全部语言的地位)

本页面向纯小白：**这些语言你一个都不用学会**，只要能认出它们属于哪一类、各管什么。
左边是代码、右边是浏览器<b>实时渲染</b>的结果，移动鼠标、点击都能试。

## 三家「厨房」：先把语言归类

做视频 / 做界面，就像下馆子点菜：**你（点菜的）不用会做菜**，只要知道有几家不同的
厨房。本项目里那一长串语言，其实只分三家——

<div class="fam-map">
<div class="fam"><div class="fam-tag">① 最通用</div><h4>网页系</h4><p>浏览器能直接打开的那一套。做界面、做动画、做图表都靠它，开源项目也最多。</p><div class="chips"><span class="chip">HTML</span><span class="chip">CSS</span><span class="chip">JavaScript</span><span class="chip">React</span><span class="chip">SVG</span><span class="chip">Lottie</span></div></div>
<div class="fam"><div class="fam-tag">② 做立体</div><h4>3D 系</h4><p>做三维场景：一条在浏览器里用代码实时转（three.js），一条用专业软件建模再离线渲染（Blender）。</p><div class="chips"><span class="chip">three.js</span><span class="chip">WebGL</span><span class="chip">Blender</span><span class="chip">Python · bpy</span></div></div>
<div class="fam"><div class="fam-tag">③ 专做数学</div><h4>数学动画系</h4><p>3Blue1Brown 那种数学讲解动画。用 Python 描述、引擎自己算出每一帧。</p><div class="chips"><span class="chip">Python</span><span class="chip">Manim</span></div></div>
<div class="fam"><div class="fam-tag">④ 专做讲稿</div><h4>幻灯片系</h4><p>说白了就是生成 PPT / 讲义。拼版式、放文字图片。</p><div class="chips"><span class="chip">python-pptx</span><span class="chip">LaTeX · Beamer</span></div></div>
</div>

记住一句话就够：**它们都只是「一份让某个工具照着画出画面的脚本」，区别只在于交给哪家厨房。**

## 网页系：HTML / CSS / JS 的分工

网页「三件套」，可以用盖房子来记：

- **HTML = 砖墙骨架**：决定页面上<b>有什么</b>（标题、段落、按钮、图片）。
- **CSS = 装修刷漆**：决定这些东西<b>长什么样</b>（颜色、大小、排版、动画）。
- **JavaScript = 水电开关**：决定<b>点了会发生什么</b>（交互、数据变化）。

先看只有骨架、不化妆的样子：

{d_html[0]}

同一段骨架，加上 CSS 之后：

{d_css[0]}

再加上 JavaScript，它就能响应你的操作：

{d_js[0]}

### React 和 CSS 是什么关系

初学最容易糊涂的就是这俩。一句话：**它们根本不在一个维度上，不是竞争关系。**

- **CSS** 回答「这块长什么样」——颜色、间距、动画。
- **React** 回答「页面由哪些块组成、数据变了界面怎么跟着变」。它<b>不是新语言</b>，
  就是 JavaScript 加一套写法，把界面拆成可复用的**组件**。

所以真实项目里是<b>一起用</b>的：React 搭出结构和交互逻辑，CSS 负责这些结构的外观。

{d_react[0]}

> 为什么本项目里网页系的开源项目最多？因为「浏览器能打开」= 天然跨平台、天然能截图，
> 很多 Code2Video 工具就是让模型写一段网页，再逐帧截图拼成视频（比如 Remotion 用的就是 React）。

### SVG 与 Lottie：画图与数据化的动画

{d_svg[0]}

{d_lottie[0]}

### 三者嵌套：HTML 装 SVG，一套 CSS 修饰两者

前面几轮我们反复说「HTML/SVG 负责造元素、CSS 负责修饰」。下面这个 demo 把三者捏在一起,
一眼看清它们怎么分工、怎么嵌套——这是真实网站里最常见的组合。

{d_combo[0]}

## 3D 系：three.js 与 Blender

做「立体」有两条路，正好是本项目和 Gallery 里那些 3D 场景的来源——一条在<b>浏览器里用代码实时转</b>，
一条用<b>专业软件建模、再离线渲染</b>。

### three.js：浏览器里的实时 3D

还是网页那一套（写 JS、浏览器直接打开），只是从「画 2D」升级成「摆一个真三维场景」：
<b>场景 / 相机 / 光源 / 网格</b>四件事，每帧渲染一次。它基于 <b>WebGL</b>，是网页做 3D 最主流的库。

{d_three[0]}

> 本站的 <b>Gallery</b> 整面墙——小星球、雪球、黄铜天象仪——全部是 three.js 写的单文件场景。

### Blender：用软件建模，离线渲染

另一条路不在浏览器里：Blender 是一款<b>专业 3D 软件</b>，建模、打光、渲染都在它里面完成；
代码（Python）只是用来「遥控」它。产物是<b>离线文件</b>，不像 three.js 那样实时。

{d_blender[0]}

## 数学动画系：Python + Manim

和网页系完全不同的一条路：这里不靠浏览器截图，而是<b>引擎自己把每一帧画出来</b>。

- **Python** 是一门通用编程语言（也是 AI 圈最常用的）。
- **Manim** 是一个 Python **库**：提供 `Circle`、`Square`、`Transform` 这些现成的数学对象和动作，
  你用 Python 把它们拼起来，它负责算出动画的每一帧并渲成 mp4。

{d_manim[0]}

## 幻灯片系：pptx / LaTeX-Beamer

这一家最好理解——产物就是**一份 PPT 或 PDF 讲义**，常被进一步转成讲解视频。
它们一般不在浏览器里跑，这里只看一眼长相，知道「哦，这是在拼幻灯片」即可。

用 Python 拼一页 PPT（`python-pptx`）：

```python
from pptx import Presentation
prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[0])   # 新建一页
slide.shapes.title.text = "Visual Coder"             # 标题
slide.placeholders[1].text = "一页自动生成的幻灯片"    # 副标题
prs.save("deck.pptx")
```

用 LaTeX 的 Beamer 模式写一页（学术讲稿常用）：

```latex
\\documentclass{{beamer}}
\\begin{{document}}
\\begin{{frame}}{{Visual Coder}}   % 一页 = 一个 frame
  \\begin{{itemize}}
    \\item 结构化的讲稿
    \\item 导出就是 PDF
  \\end{{itemize}}
\\end{{frame}}
\\end{{document}}
```

两段代码的意思都是「第一页标题写什么、列几个要点」，只是语法不同。

## 一张总表：全部语言的地位

把上面全收进一张表。**看懂这张表，源文件里的语言就不再吓人了。**

| 语言 | 一句话地位 | 属于哪家 | 怎么出画面 | 本项目里的角色 |
|---|---|---|---|---|
| **HTML** | 网页的骨架/结构 | 网页系 | 浏览器直接渲染 | 一切网页类生成的地基 |
| **CSS** | 网页的样式/外观 | 网页系 | 浏览器直接渲染 | 决定生成页面好不好看 |
| **JavaScript** | 网页的行为/交互 | 网页系 | 浏览器直接渲染 | 驱动动画与逐帧变化 |
| **React** | 用 JS 写界面的框架（非新语言） | 网页系 | 编译成 HTML 后由浏览器渲染 | Remotion 等「写代码出视频」的底座 |
| **SVG** | 用标签画的矢量图 | 网页系 | 浏览器直接渲染 | 图标、图表、矢量动画 |
| **Lottie (JSON)** | 数据化的动画 | 网页系 | 播放器按帧播放数据 | 轻量动画资产（OmniLottie 等） |
| **three.js** | 浏览器里的 3D 库（基于 WebGL） | 网页系 / 3D | 浏览器实时渲染 | 本站 Gallery 全部 3D 场景 |
| **Blender** | 专业 3D 建模 / 渲染软件（Python 脚本控制） | 3D 系 | 软件离线渲成 图 / mp4 / 模型 | 高质量 3D 资产与离线动画 |
| **Python** | 通用编程语言 | 数学/幻灯片系 | 看调用的库 | 粘合一切、调度各类引擎 |
| **Manim** | Python 的数学动画引擎 | 数学动画系 | 引擎逐帧渲成 mp4 | 教学/数学动画（Code2Video 等） |
| **python-pptx / Beamer** | 生成 PPT / PDF 讲义 | 幻灯片系 | 导出文件、再转视频 | 演讲视频、论文讲解 |

> **两种「出视频」的方式**，正好对应前两家：网页系多是<b>把画面一帧帧截图再拼起来</b>；
> 数学动画系是<b>引擎自己把每一帧画出来</b>。认到这一层，就足够看懂本项目所有源文件了。
"""


# --------------------------------------------------------------------------- #
# 落盘
# --------------------------------------------------------------------------- #
def main() -> None:
    os.makedirs(DEMOS, exist_ok=True)
    for slug, html in DEMO_FILES.items():
        with open(os.path.join(DEMOS, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(html)
    with open(os.path.join(BASIC, "basic.md"), "w", encoding="utf-8") as f:
        f.write(MD)
    print(f"  wrote {os.path.relpath(os.path.join(BASIC, 'basic.md'), ROOT)}")
    print(f"  wrote {len(DEMO_FILES)} demo files -> {os.path.relpath(DEMOS, ROOT)}/")
    for slug in DEMO_FILES:
        print(f"    - demos/{slug}.html")


if __name__ == "__main__":
    main()

