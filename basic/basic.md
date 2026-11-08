# Basic

## Contents

- [三家「厨房」：先把语言归类](#三家厨房先把语言归类)
- [网页系：HTML / CSS / JS 的分工](#网页系html-css-js-的分工)
  - [React 和 CSS 是什么关系](#react-和-css-是什么关系)
  - [SVG 与 Lottie：画图与数据化的动画](#svg-与-lottie画图与数据化的动画)
  - [三者嵌套：HTML 装 SVG，一套 CSS 修饰两者](#三者嵌套html-装-svg一套-css-修饰两者)
- [3D 系：three.js 与 Blender](#3d-系threejs-与-blender)
  - [three.js：浏览器里的实时 3D](#threejs浏览器里的实时-3d)
  - [Blender：用软件建模，离线渲染](#blender用软件建模离线渲染)
- [AI 怎么生成 3D：原生 3D 模型](#ai-怎么生成-3d原生-3d-模型)
  - [输出的是什么：和视频生成对比](#输出的是什么和视频生成对比)
  - [从「场」到网格：三步看懂](#从场到网格三步看懂)
  - [是 diffusion 还是 LLM](#是-diffusion-还是-llm)
  - [为什么说它「可编辑」](#为什么说它可编辑)
  - [三代路线与各家模型](#三代路线与各家模型)
- [数学动画系：Python + Manim](#数学动画系python-manim)
- [幻灯片系：pptx / LaTeX-Beamer](#幻灯片系pptx-latex-beamer)
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

<div class="demo">
<div class="demo-top"><span class="demo-lang lang-html">HTML</span><span class="demo-title">只有结构，不化妆</span></div>
<div class="demo-split">
<pre class="demo-code"><code>&lt;h2&gt;我的第一个网页&lt;/h2&gt;&#10;&lt;p&gt;这是一个段落。下面是一个列表：&lt;/p&gt;&#10;&lt;ul&gt;&#10;  &lt;li&gt;苹果&lt;/li&gt;&#10;  &lt;li&gt;香蕉&lt;/li&gt;&#10;&lt;/ul&gt;&#10;&lt;a href="#"&gt;一个链接&lt;/a&gt;</code></pre>
<iframe class="demo-frame" style="height:210px" src="demos/html-bare.html"></iframe>
</div>
<p class="demo-note">只有 HTML、没写任何样式时，浏览器用<b>默认外观</b>——这就是网页的「结构 / 骨架」。标题、段落、列表、链接都用一对尖括号标签框起来。</p>
</div>

同一段骨架，加上 CSS 之后：

<div class="demo">
<div class="demo-top"><span class="demo-lang lang-css">CSS</span><span class="demo-title">同一段结构，CSS 负责外观</span></div>
<div class="demo-split">
<pre class="demo-code"><code>&lt;!-- HTML：还是那套结构 --&gt;&#10;&lt;div class="card"&gt;&#10;  &lt;h3&gt;Visual Coder&lt;/h3&gt;&#10;  &lt;p&gt;把鼠标移上来试试&lt;/p&gt;&#10;&lt;/div&gt;&#10;&#10;/* CSS：负责「长什么样」 */&#10;.card {&#10;  width: 220px;&#10;  padding: 22px;&#10;  border-radius: 16px;&#10;  color: #fff;&#10;  background: linear-gradient(135deg, #2f6bff, #8b5cf6);&#10;  box-shadow: 0 12px 30px rgba(47,107,255,.35);&#10;  transition: transform .2s ease;&#10;}&#10;.card:hover { transform: translateY(-6px); }&#10;.card h3 { margin: 0 0 6px; font-size: 18px; }&#10;.card p  { margin: 0; opacity: .85; font-size: 13px; }</code></pre>
<iframe class="demo-frame" style="height:260px" src="demos/css-box.html"></iframe>
</div>
<p class="demo-note">同样一段 HTML，<b>CSS 决定「长什么样」</b>：颜色、圆角、阴影、渐变，还有鼠标悬停时的动画。把光标移到右边的卡片上看看。这就是前端最常改的东西。</p>
</div>

再加上 JavaScript，它就能响应你的操作：

<div class="demo">
<div class="demo-top"><span class="demo-lang lang-js">JavaScript</span><span class="demo-title">点击后页面会变</span></div>
<div class="demo-split">
<pre class="demo-code"><code>&lt;!-- HTML 先画出按钮 --&gt;&#10;&lt;button id="btn"&gt;点我 +1&lt;/button&gt; &lt;span class="n" id="n"&gt;0&lt;/span&gt;&#10;&#10;// JavaScript 负责「交互 / 行为」&#10;let count = 0;&#10;const btn = document.getElementById('btn');&#10;btn.onclick = () =&gt; {&#10;  count = count + 1;&#10;  document.getElementById('n').textContent = count;&#10;};</code></pre>
<iframe class="demo-frame" style="height:200px" src="demos/js-counter.html"></iframe>
</div>
<p class="demo-note">HTML 把按钮画出来，<b>JavaScript 负责「交互 / 行为」</b>：点一下就改变页面。到这里网页三件套就齐了——<b>结构(HTML) / 样式(CSS) / 行为(JS)</b>，各管一摊。</p>
</div>

### React 和 CSS 是什么关系

初学最容易糊涂的就是这俩。一句话：**它们根本不在一个维度上，不是竞争关系。**

- **CSS** 回答「这块长什么样」——颜色、间距、动画。
- **React** 回答「页面由哪些块组成、数据变了界面怎么跟着变」。它<b>不是新语言</b>，
  就是 JavaScript 加一套写法，把界面拆成可复用的**组件**。

所以真实项目里是<b>一起用</b>的：React 搭出结构和交互逻辑，CSS 负责这些结构的外观。

<div class="demo">
<div class="demo-top"><span class="demo-lang lang-react">React</span><span class="demo-title">把界面拆成「组件」</span></div>
<div class="demo-split">
<pre class="demo-code"><code>function Counter() {&#10;  // useState：记住一个会变的数字 n&#10;  const [n, setN] = React.useState(0);&#10;  return (&#10;    &lt;button onClick={() =&gt; setN(n + 1)}&gt;&#10;      你点了 {n} 次&#10;    &lt;/button&gt;&#10;  );&#10;}</code></pre>
<iframe class="demo-frame" style="height:200px" src="demos/react-counter.html"></iframe>
</div>
<p class="demo-note"><b>React 不是第四种语言，而是用 JavaScript 写界面的框架</b>：把页面拆成一个个可复用的「组件」，数据(n)一变，界面自动重画，不用自己手动改 DOM。<b>和 CSS 的关系</b>：React 管「结构和数据怎么变」，CSS 管「长什么样」，两者正交、配合用。右边是这个组件渲染后的实际效果（为便于离线查看用等价原生 JS 驱动，交互一致）。</p>
</div>

> 为什么本项目里网页系的开源项目最多？因为「浏览器能打开」= 天然跨平台、天然能截图，
> 很多 Code2Video 工具就是让模型写一段网页，再逐帧截图拼成视频（比如 Remotion 用的就是 React）。

### SVG 与 Lottie：画图与数据化的动画

<div class="demo">
<div class="demo-top"><span class="demo-lang lang-svg">SVG</span><span class="demo-title">像写标签一样画图，还能动</span></div>
<div class="demo-split">
<pre class="demo-code"><code>&lt;svg width="240" height="150" viewBox="0 0 240 150"&gt;&#10;  &lt;rect x="10" y="10" width="220" height="130" rx="16" fill="#eaf0ff"/&gt;&#10;  &lt;circle cx="60" cy="70" r="26" fill="#2f6bff"&gt;&#10;    &lt;animate attributeName="cx" values="60;180;60"&#10;             dur="2s" repeatCount="indefinite"/&gt;&#10;  &lt;/circle&gt;&#10;  &lt;text x="120" y="135" text-anchor="middle"&#10;        font-size="12" fill="#5b636e"&gt;SVG 用标签画图形&lt;/text&gt;&#10;&lt;/svg&gt;</code></pre>
<iframe class="demo-frame" style="height:230px" src="demos/svg-draw.html"></iframe>
</div>
<p class="demo-note"><b>SVG 是「用标签画出来的矢量图」</b>——写法和 HTML 一样，但画的是圆、矩形、路径，而且能内置动画。图表、图标、插画常用它。下一个要讲的 Lottie，就是把这类动画导成一段数据。</p>
</div>

<div class="demo">
<div class="demo-top"><span class="demo-lang lang-json">JSON</span><span class="demo-title">动画也能是「数据」</span></div>
<div class="demo-split">
<pre class="demo-code"><code>{&#10;  "v": "5.7",              // 版本&#10;  "fr": 30,                // 帧率&#10;  "w": 120, "h": 120,      // 画布尺寸&#10;  "layers": [&#10;    { "ty": 4, "nm": "圆",&#10;      "ks": {              // 用关键帧描述「从小变大」&#10;        "s": { "k": [ { "t": 0,  "s": [20] },&#10;                      { "t": 30, "s": [100] } ] }&#10;      } }&#10;  ]&#10;}</code></pre>
<iframe class="demo-frame" style="height:230px" src="demos/lottie-json.html"></iframe>
</div>
<p class="demo-note"><b>Lottie 本质是一段 JSON（数据，不是代码）</b>：设计师在 After Effects 里做好动画，导出成这样一份文件，网页 / App 用一个小播放器按帧播放它，体积小又清晰。右边是这段数据所描述效果的<b>浏览器示意</b>。</p>
</div>

### 三者嵌套：HTML 装 SVG，一套 CSS 修饰两者

前面几轮我们反复说「HTML/SVG 负责造元素、CSS 负责修饰」。下面这个 demo 把三者捏在一起,
一眼看清它们怎么分工、怎么嵌套——这是真实网站里最常见的组合。

<div class="demo">
<div class="demo-top"><span class="demo-lang lang-html">HTML + CSS + SVG</span><span class="demo-title">一张卡片同时用上三者</span></div>
<div class="demo-split">
<pre class="demo-code"><code>&lt;!-- HTML：一张卡片，里面嵌一个 SVG 太阳 --&gt;&#10;&lt;div class="card"&gt;&#10;  &lt;h3&gt;Sunny&lt;/h3&gt;&#10;  &lt;svg viewBox="0 0 120 120" width="112" height="112"&gt;&#10;    &lt;g class="rays"&gt;                        &lt;!-- 一组光芒 --&gt;&#10;      &lt;line x1="60" y1="6"  x2="60" y2="22"/&gt;&#10;      &lt;line x1="60" y1="98" x2="60" y2="114"/&gt;&#10;      &lt;line x1="6"  y1="60" x2="22" y2="60"/&gt;&#10;      &lt;line x1="98" y1="60" x2="114" y2="60"/&gt;&#10;    &lt;/g&gt;&#10;    &lt;circle class="sun" cx="60" cy="60" r="24"/&gt;&#10;  &lt;/svg&gt;&#10;&lt;/div&gt;&#10;&#10;&lt;style&gt;&#10;/* CSS 修饰 HTML 元素 */&#10;.card {&#10;  width: 180px; padding: 20px; text-align: center;&#10;  border-radius: 18px; color: #fff;&#10;  background: linear-gradient(135deg, #f6b73c, #e0566a);&#10;}&#10;.card h3 { margin: 0 0 8px; }&#10;&#10;/* 同一套 CSS，也在修饰 SVG 元素 */&#10;.sun { fill: #fff; }                   /* 注意：是 fill 不是 background */&#10;.rays line { stroke: #fff; stroke-width: 5; stroke-linecap: round; }&#10;.rays {                                /* CSS 让 SVG 的光芒转起来 */&#10;  transform-box: view-box;&#10;  transform-origin: 60px 60px;&#10;  animation: spin 6s linear infinite;&#10;}&#10;@keyframes spin { to { transform: rotate(360deg); } }&#10;&lt;/style&gt;</code></pre>
<iframe class="demo-frame" style="height:300px" src="demos/combo-card.html"></iframe>
</div>
<p class="demo-note">看清楚三层:<b>HTML</b> 的 <b>&lt;div class="card"&gt;</b> 里<b>嵌着一个 &lt;svg&gt;</b>(HTML 装 SVG);<b>同一套 CSS</b> 既修饰了 HTML 的 <b>.card</b>(渐变背景),也修饰了 SVG 的 <b>.sun / .rays</b>(填充白色、并让光芒转起来)。注意给圆上色用的是 <b>fill</b> 不是 background——这就是「HTML/SVG 造元素、CSS 修饰元素」的真实样子。</p>
</div>

## 3D 系：three.js 与 Blender

做「立体」有两条路，正好是本项目和 Gallery 里那些 3D 场景的来源——一条在<b>浏览器里用代码实时转</b>，
一条用<b>专业软件建模、再离线渲染</b>。

### three.js：浏览器里的实时 3D

还是网页那一套（写 JS、浏览器直接打开），只是从「画 2D」升级成「摆一个真三维场景」：
<b>场景 / 相机 / 光源 / 网格</b>四件事，每帧渲染一次。它基于 <b>WebGL</b>，是网页做 3D 最主流的库。

<div class="demo">
<div class="demo-top"><span class="demo-lang lang-js">JavaScript · three.js</span><span class="demo-title">浏览器里摆一个真三维场景</span></div>
<div class="demo-split">
<pre class="demo-code"><code>import * as THREE from 'three';&#10;&#10;// three.js 的「四件事」：场景 / 相机 / 渲染器 / 网格&#10;const scene    = new THREE.Scene();&#10;const camera   = new THREE.PerspectiveCamera(50, w / h, 0.1, 100);&#10;camera.position.set(2.4, 1.8, 2.8);&#10;const renderer = new THREE.WebGLRenderer({ antialias: true });&#10;&#10;// 放一个立方体，给它材质，再打一盏灯&#10;const cube = new THREE.Mesh(&#10;  new THREE.BoxGeometry(1.4, 1.4, 1.4),&#10;  new THREE.MeshStandardMaterial({ color: 0x2f6bff })&#10;);&#10;scene.add(cube);&#10;scene.add(new THREE.DirectionalLight(0xffffff, 1.3));&#10;&#10;// 每帧转一点、重新渲染（动画就是这么来的）&#10;function loop() {&#10;  requestAnimationFrame(loop);&#10;  cube.rotation.y += 0.006;&#10;  renderer.render(scene, camera);&#10;}&#10;loop();</code></pre>
<iframe class="demo-frame" style="height:300px" src="demos/threejs-cube.html"></iframe>
</div>
<p class="demo-note"><b>three.js 是 JavaScript 的 3D 库</b>（基于 <b>WebGL</b>）：还是写 JS、还是浏览器直接打开，只是从「画 2D」升级成「摆一个真三维场景」——<b>场景 / 相机 / 光源 / 网格</b>，每帧渲染一次。它是网页做 3D 最主流的库。右边可以<b>拖动旋转</b>；本站 <b>Gallery</b> 整面墙都是它写的。</p>
</div>

> 本站的 <b>Gallery</b> 整面墙——小星球、雪球、黄铜天象仪——全部是 three.js 写的单文件场景。

### Blender：用软件建模，离线渲染

另一条路不在浏览器里：Blender 是一款<b>专业 3D 软件</b>，建模、打光、渲染都在它里面完成；
代码（Python）只是用来「遥控」它。产物是<b>离线文件</b>，不像 three.js 那样实时。

<div class="demo">
<div class="demo-top"><span class="demo-lang lang-py">Python · bpy (Blender)</span><span class="demo-title">软件建模，离线渲染成文件</span></div>
<div class="demo-split">
<pre class="demo-code"><code>import bpy   # Blender 的 Python 接口&#10;&#10;# 1) 建模：往场景里加一个立方体&#10;bpy.ops.mesh.primitive_cube_add(size=2)&#10;cube = bpy.context.active_object&#10;&#10;# 2) 给它一个蓝色材质&#10;mat = bpy.data.materials.new("Blue")&#10;mat.diffuse_color = (0.18, 0.42, 1.0, 1.0)&#10;cube.data.materials.append(mat)&#10;&#10;# 3) 渲染成一张图片（离线，不在浏览器里）&#10;bpy.context.scene.render.filepath = "//cube.png"&#10;bpy.ops.render.render(write_still=True)</code></pre>
<iframe class="demo-frame" style="height:260px" src="demos/blender-cube.html"></iframe>
</div>
<p class="demo-note"><b>Blender 不是网页技术，是一款专业 3D 软件</b>（建模 / 动画 / 渲染都在它里面做）。你写的其实是 <b>Python(bpy)</b> 去「遥控」它：加物体、给材质、按下渲染。<b>产物是离线文件</b>——一张图、一段 mp4，或一个 <b>.glb 3D 模型</b>。那个 .glb 还能反过来丢给 <b>three.js</b> 在网页里加载：<b>Blender 建好模型 → three.js 在浏览器里展示</b>，这就是两者的接力。右边是 CSS 示意。</p>
</div>

## AI 怎么生成 3D：原生 3D 模型

上面两条路都是「人写代码或人在软件里建模」。Market 页里的 Meshy、混元 3D、Tripo 是第三条路：**模型直接生成一个 3D 文件**。
业内叫它「原生 3D」，意思是模型直接在 3D 数据上训练和生成，不是先画几张 2D 图再拼成 3D。

先给结论：**主干是 diffusion，交付物是网格文件。**

### 输出的是什么：和视频生成对比

| | 视频生成 | 原生 3D 生成 |
|---|---|---|
| 模型直接输出 | latent，解码后就是像素帧 | latent，解码后是一个 **SDF 场**（空间里每个点离表面多远） |
| 最终交付物 | 像素：帧数 × 高 × 宽 × RGB | **网格**：顶点 + 面 + UV + 贴图 |
| 中间有没有额外一步 | 没有，解码即成品 | 有：用 marching cubes 把场转成网格，这是固定算法，不是学出来的 |
| 视角 | 固定，镜头怎么走就是什么画面 | 任意角度都能渲染 |
| 拿去干什么 | 直接看 | 进引擎、3D 打印、绑骨、继续加工 |

一个网格文件（例如 .glb）里装的是：

- **顶点**：几万到几十万个 (x, y, z) 坐标。
- **面**：哪 3 到 4 个顶点连成一个面，决定表面怎么连。
- **UV**：每个顶点对应贴图上的哪个位置。
- **贴图**：几张 2D 图片，包括颜色、法线，以及 PBR 的粗糙度和金属度。所以 3D 生成的「上色」部分，其实还是 2D 图像生成。

视频生成交付「看到的结果」，3D 生成交付「可以从任意角度看的东西本身」。这就是它能接上 3D 打印、游戏引擎这些下游流程的原因。

### 从「场」到网格：三步看懂

<div class="demo">
<div class="demo-top"><span class="demo-lang lang-js">原生 3D 管线</span><span class="demo-title">场 → 网格 → 重拓扑（点上方按钮切换）</span></div>
<div class="demo-split">
<pre class="demo-code"><code># 以开源的混元 3D 2.0 为例&#10;&#10;# 1) 生成：diffusion 在 3D latent 上去噪&#10;latent = shape_dit.sample(cond=dinov2(image))&#10;&#10;# 2) 解码：VAE 把 latent 变成场&#10;#    问任意一点 (x,y,z)，回答它离表面多远&#10;sdf = shape_vae.decode(latent)&#10;&#10;# 3) 抽面：固定算法，不是模型&#10;mesh = marching_cubes(sdf, level=0)   # 几万到几十万个碎三角面&#10;&#10;# 4) 上色：几何作条件，多视角生成贴图再烘焙&#10;mesh.texture = paint_model(mesh, image)&#10;&#10;# 5) 后处理：各家真正拉开差距的地方&#10;mesh = retopo(mesh)      # 四边面低模&#10;parts = segment(mesh)    # 拆件&#10;rig = auto_rig(mesh)     # 绑骨</code></pre>
<iframe class="demo-frame" style="height:440px" src="demos/sdf-to-mesh.html"></iframe>
</div>
<p class="demo-note">右边是同一个胶囊的三个阶段，可以拖动旋转。<b>1 场</b>：模型真正输出的东西，蓝点在内部、灰点在外部。<b>2 网格</b>：marching cubes 抽出约 3000 个碎三角面，能打印，但布线乱，美术没法改。<b>3 重拓扑</b>：同一个形状只用 208 个整齐的四边面，能细分、能绑骨。真实模型的面数比这里多一到两个数量级，差距更大。</p>
</div>

管线里各步对应的公开工作：

1. **几何 VAE**：从网格表面采样点云，压成一组 latent token；解码时预测任意一点的 SDF。做法来自 [3DShape2VecSet](https://arxiv.org/abs/2301.11445)。
2. **几何生成**：一个 DiT，用 diffusion 或 flow matching 训练，条件是输入图片的特征。例如 [混元 3D 2.0](https://arxiv.org/abs/2501.12202)、Rodin 背后约 15 亿参数的 [CLAY](https://arxiv.org/abs/2406.13897)。
3. **贴图**：把几何的法线图、位置图作为条件，做多视角图像扩散，再烘焙到 UV 上。CLAY 直接出 2K 的 PBR 贴图。
4. **后处理**：
   - 重拓扑：自回归模型逐个生成面，产出人工建模风格的低模，例如 [MeshGPT](https://arxiv.org/abs/2311.15475)、NVIDIA [Meshtron](https://arxiv.org/abs/2412.09548)（最多 6.4 万个面）。
   - 拆件和绑骨：把整体拆成能单独打印或单独动的部件，再自动加骨骼。

### 是 diffusion 还是 LLM

主干是 diffusion，但三种技术各有位置：

| 路线 | 训练目标 | 用在哪 | 代表 |
|---|---|---|---|
| diffusion / flow matching | 在 3D latent 上去噪 | **主干**：生成形状和贴图 | 混元 3D、Rodin（CLAY）、TripoSG、TRELLIS |
| 自回归（LLM 式） | 把 3D 切成 token，逐个预测下一个 | 重拓扑；少数整体生成 | MeshGPT、Meshtron；Roblox [Cube](https://arxiv.org/abs/2503.15475) |
| LLM 写代码 | 生成 CAD 或 Blender 代码 | 参数化零件、程序化建模 | Zoo、Adam、BlenderMCP |

两点容易混：

- **用了 Transformer 不等于是 LLM。** DiT 的结构是 Transformer，但它学的是「给一团带噪声的 latent，预测怎么去噪」，一次生成整个物体；LLM 学的是「预测下一个 token」。判断路线看训练目标，不看网络结构。
- **主干不用自回归，是因为序列太长。** 一个精细物体要 1 万个面以上，逐面生成又慢、误差还会一路累积；扩散一次生成整个连续的场，分辨率更容易做高。所以自回归只用在面数少的低模上。

### 为什么说它「可编辑」

既然主干是 diffusion，「可编辑」从哪来？答案是：**可编辑由输出的表示决定，和生成方法无关。** marching cubes 之后，文件里已经没有任何 diffusion 的痕迹，只是一堆顶点和面。所以要分三层看：

| 层次 | 能做什么 | 原生 3D 能不能 | 靠什么 |
|---|---|---|---|
| 文件级 | 在 Blender 里拖顶点、雕刻、改贴图 | 名义上能，实际难：碎三角面没有边线循环，美术基本只能重做 | 标准网格格式 |
| 结构级 | 移动或替换部件、绑骨做动画 | 靠后处理才能 | 重拓扑、拆件模型 |
| 参数级 | 「杯子加高 2mm」「孔径改成 5mm」 | **不能** | 只有 CAD 代码、程序化建模 |

diffusion 自己能做的「编辑」都是**重新生成**：几何不动重做贴图、遮住一块重新采样、换参考图重来。它没法精确地「改多少」，因为 latent 里没有「高度」「孔径」这种有名字的参数，只有一团向量。

参数级可编辑长这样：

<div class="demo">
<div class="demo-top"><span class="demo-lang lang-py">CAD-as-code</span><span class="demo-title">改一个数字，模型精确重建</span></div>
<div class="demo-split">
<pre class="demo-code"><code># 一个杯子 = 一条截面轮廓绕中轴转一圈&#10;def cup(height, radius, wall=3):        # 单位 mm&#10;    profile = [(0, 0), (radius, 0),&#10;               (radius, height),&#10;               (radius - wall, height),&#10;               (radius - wall, wall), (0, wall)]&#10;    return revolve(profile)&#10;&#10;cup(height=60, radius=30)   # 拖右边滑杆试试</code></pre>
<iframe class="demo-frame" style="height:300px" src="demos/cad-param.html"></iframe>
</div>
<p class="demo-note">交付物是<b>代码加参数</b>，不是一团网格：改 height 从 60 到 62，杯子精确加高 2mm，其余尺寸一点不变，每一步还能审查。原生 3D 模型要做同样的修改，只能重新生成，而且无法保证只变高度。所以零件、支架这类<b>尺寸必须对</b>的东西适合交给 LLM 写代码，手办、游戏道具这类<b>看着对就行</b>的东西适合原生 3D。</p>
</div>

### 三代路线与各家模型

| 代 | 时间 | 做法 | 代表 | 卡在哪 |
|---|---|---|---|---|
| 2D 蒸馏 | 2022 到 2023 | 用 2D 扩散模型给 3D 表示打分，逐个物体优化 | [DreamFusion](https://arxiv.org/abs/2209.14988) | 一个物体几十分钟到几小时；常出现多张脸 |
| 多视图 + 重建 | 2023 到 2024 | 先生成 4 到 6 张多视角图，再用重建网络拼成 3D | Zero123、MVDream、[LRM](https://arxiv.org/abs/2311.04400) | 快，但几何发糊，各视角对不齐 |
| 原生 3D | 2024 至今 | 直接在 3D latent 上做 diffusion | CLAY、混元 3D 2.x、TripoSG、TRELLIS | 依赖 3D 数据，而 3D 数据很少 |

| 公司 / 模型 | 公开程度 | 已知结构 |
|---|---|---|
| 影眸 Rodin | 有论文 | [CLAY](https://arxiv.org/abs/2406.13897)：多分辨率 3D VAE + latent DiT，几何部分 15 亿参数 |
| 腾讯混元 3D 2.x | 开源 + 技术报告 | [ShapeVAE + flow matching DiT](https://arxiv.org/abs/2501.12202)，外加独立的贴图模型 |
| VAST Tripo | 部分开源 | [TripoSG](https://arxiv.org/abs/2502.06608)：SDF VAE + rectified flow |
| 微软 TRELLIS / TRELLIS.2 | 开源 | 稀疏体素上的[结构化 latent](https://arxiv.org/abs/2412.01506)，同一个 latent 可解码成网格或 3D 高斯点；[TRELLIS.2](https://arxiv.org/abs/2512.14692) 40 亿参数 |
| Roblox Cube | 有论文 | 把形状切成离散 token，再像 LLM 一样生成，少数走自回归主干的 |
| Meshy | **闭源，无论文** | 官方没公开结构。从产品表现推断，Meshy-4 起已转向原生 3D latent diffusion；差异化在重拓扑、绑骨、打印分色等后处理 |

**真正的瓶颈是数据。** 公开的 [Objaverse-XL](https://arxiv.org/abs/2307.05663) 有 1000 万个以上的 3D 物体，但噪声大，清洗后能用的通常只剩几十万量级；图像模型的训练数据是 10 亿到 100 亿张，相差 3 到 4 个数量级。大家用的基本是同一批数据，所以大厂开源后模型层很快拉平，竞争转向后处理和分发，这正是 Market 里 3D Assets 页的结论。

## 数学动画系：Python + Manim

和网页系完全不同的一条路：这里不靠浏览器截图，而是<b>引擎自己把每一帧画出来</b>。

- **Python** 是一门通用编程语言（也是 AI 圈最常用的）。
- **Manim** 是一个 Python **库**：提供 `Circle`、`Square`、`Transform` 这些现成的数学对象和动作，
  你用 Python 把它们拼起来，它负责算出动画的每一帧并渲成 mp4。

<div class="demo">
<div class="demo-top"><span class="demo-lang lang-py">Python · Manim</span><span class="demo-title">用 Python 描述数学动画</span></div>
<div class="demo-split">
<pre class="demo-code"><code>from manim import *&#10;&#10;class Demo(Scene):&#10;    def construct(self):&#10;        c = Circle(color=BLUE)&#10;        self.play(Create(c))                 # 先画出一个圆&#10;        self.play(Transform(c, Square(color=GREEN)))  # 圆变成方&#10;        self.wait()</code></pre>
<iframe class="demo-frame" style="height:260px" src="demos/manim-morph.html"></iframe>
</div>
<p class="demo-note"><b>Manim 是 Python 的「数学动画引擎」</b>（3Blue1Brown 发明）：你用 Python 描述有哪些对象、要「播放」什么动作，引擎自己算出每一帧并渲成视频。右边是<b>浏览器示意</b>——真正的 Manim 产物是一个 mp4 文件，不在网页里跑。</p>
</div>

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
\documentclass{beamer}
\begin{document}
\begin{frame}{Visual Coder}   % 一页 = 一个 frame
  \begin{itemize}
    \item 结构化的讲稿
    \item 导出就是 PDF
  \end{itemize}
\end{frame}
\end{document}
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
| **.glb 网格** | 3D 模型的通用文件：顶点 + 面 + 贴图 | 3D 系 | three.js / Blender 加载后渲染 | 原生 3D 模型的交付物；Blender 与 three.js 的接力格式 |
| **Python** | 通用编程语言 | 数学/幻灯片系 | 看调用的库 | 粘合一切、调度各类引擎 |
| **Manim** | Python 的数学动画引擎 | 数学动画系 | 引擎逐帧渲成 mp4 | 教学/数学动画（Code2Video 等） |
| **python-pptx / Beamer** | 生成 PPT / PDF 讲义 | 幻灯片系 | 导出文件、再转视频 | 演讲视频、论文讲解 |

> **两种「出视频」的方式**，正好对应前两家：网页系多是<b>把画面一帧帧截图再拼起来</b>；
> 数学动画系是<b>引擎自己把每一帧画出来</b>。认到这一层，就足够看懂本项目所有源文件了。

