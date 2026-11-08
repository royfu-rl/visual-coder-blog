# Visual Coding 可验证任务 · 任务来源调研

- 日期：2026-10-15
- 范围：Web 前端、three.js / WebGL / shader、Blender / bpy、网页游戏
- 与已有文件的关系：benchmarks.md、pipelines.md、deep_*.md 已覆盖的 benchmark 与数据管线不再展开，本文只补三块
  - GitHub 上「自带像素基线」的仓库（这是全文最重要的增量）
  - 开发者社区网站
  - 按「可验证性 × 规模 × 许可」分级
- 数字口径
  - 「实测」：本次用 GitHub / Gitea / HF / StackExchange / Discourse API 直接数出来的，附查询 URL
  - 「估算」：明确标注，并写出估算依据
  - 「官方自述」：只引用平台自己的公告，日期较旧的会标出

---

## 1. GitHub 来源

### 1.1 核心发现：渲染库的「像素基线测试」是天然的 F2P 来源

- 原理
  - 这类仓库在 repo 里放 `场景代码 + 参考图(png)`，CI 渲染后逐像素比对
  - 修改渲染行为的 PR 会同时更新参考图，于是每个这样的 commit 都天然构成一对数据
    - 旧代码 + 新参考图 → fail
    - 新代码 + 新参考图 → pass
  - verifier 是确定性的像素阈值，不需要 VLM judge
- 粗略可挖量：下表中 9 个 GitHub 仓库（不含 plotly 和 Blender）改过基线的 commit 合计 3,413 个（实测），参考图合计约 1.9 万张。这是 F2P 候选的上界，因为其中有一部分只是重新生成截图，并没有改代码

| 仓库 | 许可 | 参考图（实测） | 改过基线的 commit（实测） | 测试机制 | 备注 |
|---|---|---|---|---|---|
| [mrdoob/three.js](https://github.com/mrdoob/three.js/tree/dev/test/e2e) | MIT | 610 张 `examples/screenshots/*.jpg`，对应 611 个 example html | 1,143 | puppeteer 渲染 400×250；`pixelThreshold=0.1`，`maxDifferentPixels=0.1%`；注入确定性随机数与时钟；54 个 example 在豁免名单 | README 自称覆盖 97% 的 example；同一批截图也用作缩略图 |
| [BabylonJS/Babylon.js](https://github.com/BabylonJS/Babylon.js/tree/master/packages/tools/tests/test/visualization) | Apache-2.0 | `config.json` 共 901 个测试，其中 883 个用 playgroundId；975 张 ReferenceImages png | 397 | Playwright，分 WebGL1 / WebGL2 / WebGPU 三套；338 个测试带 `excludedEngines` | 场景代码在 playground snippet 服务器上，按 `#ID#rev` 取 |
| [Blender](https://projects.blender.org/blender/blender/src/branch/main/tests) | GPL | `tests/files/render/` 下 839 个 .blend、2,596 张参考 png（cycles / eevee / workbench 各一套），共 48 个类别 | 未统计（在 Gitea 上） | `tests/python/*_render_tests.py`；`tests/python/` 共 142 个条目，含 bmesh / geometry nodes / 修改器 / IO 等 Python 测试 | 测试数据已并入主仓库（LFS）；`tests/files` 全目录 7,240 个文件 |
| [maplibre/maplibre-gl-js](https://github.com/maplibre/maplibre-gl-js) | BSD-3 | 1,950 张，在 `test/integration/render` | 203 | style.json 加 expected.png | 输入是声明式 style，不是命令式代码 |
| [plotly/plotly.js](https://github.com/plotly/plotly.js) | MIT | 1,324 张，在 `test/image/baselines` | 目录级 API 只返回 1；抽查单张基线有 5 个 commit | mock json 加 baseline png | 基线可能被整体重生成过，未细查 |
| [pixijs/pixijs](https://github.com/pixijs/pixijs) | MIT | 1,711 张，在 `tests/visual/snapshots` | 249 | 视觉快照测试 | 2D WebGL / WebGPU |
| [primer/react](https://github.com/primer/react) | MIT | 7,766 张，在 `.playwright/snapshots` | 481 | Playwright `toHaveScreenshot` | UI 组件库的典型代表 |
| [chartjs/Chart.js](https://github.com/chartjs/Chart.js) | MIT | 约 667 张，在 `test/fixtures` | 315 | fixture js 加 png | 也是 SWE-bench M 的来源仓库之一 |
| [processing/p5.js](https://github.com/processing/p5.js) | LGPL-2.1 | 604 张，在 `test/unit/visual` | 156 | 视觉单测 | 也是 SWE-bench M 的来源仓库之一 |
| [openlayers/openlayers](https://github.com/openlayers/openlayers) | BSD-2 | 235 个 case，在 `test/rendering/cases` | 291 | main.js 加 expected.png | 也是 SWE-bench M 的来源仓库之一 |
| [visgl/deck.gl](https://github.com/visgl/deck.gl) | MIT | 252 张，在 `test/render/golden-images` | 178 | golden image | 3D 数据可视化 |

- 数据怎么数的
  - 参考图：`GET api.github.com/repos/{repo}/git/trees/{branch}?recursive=1`，按路径和扩展名过滤
  - commit 数：`GET /repos/{repo}/commits?path={基线目录}&per_page=1`，读 Link 头里 `rel="last"` 的页码
  - Blender：用 projects.blender.org 的 Gitea API 分页拉 `tests/files` 子树
- 没有像素基线的仓库（只能走 issue / PR 或自建 verifier）
  - pmndrs/react-three-fiber：测试图片 0 张
  - playcanvas/engine：有 296 个 `*.example.mjs`，配 592 张缩略图（webp），但没有比对测试
  - godotengine/godot：`tests/` 下 238 个文件，只有 1 张 png，全是 C++ doctest
  - mermaid、ant-design：视觉回归托管在外部服务（Argos 等），仓库里没有基线
  - apache/echarts：视觉测试的基线不在仓库里

### 1.2 通用前端的视觉回归生态（规模估算）

- 依赖方仓库数：抓 GitHub 的 network/dependents 页面（实测）
  - 只说明有多少仓库装了这个工具，不代表都有可用的基线

| 工具 | 依赖方仓库 | 说明 |
|---|---|---|
| `@playwright/test` | 458,596 | 只有一部分用了 `toHaveScreenshot` |
| `storybook` | 127,816 | 要配 Chromatic、Loki 或 test-runner 才有截图比对 |
| `chromatic` | 57,166 | 基线存在 Chromatic 云端，仓库里拿不到 |
| `jest-image-snapshot` | 15,400 | 基线在仓库的 `__image_snapshots__/` 里 |
| `@storybook/test-runner` | 13,236 | — |
| `@percy/cli` | 6,023 | 基线在 Percy 云端，仓库里拿不到 |
| `backstopjs` | 5,300 | 基线通常在仓库里 |
| `loki` | 3,942 | 基线在仓库的 `.loki/reference` 里 |
| `reg-suit` | 611 | — |
| `lost-pixel` | 187 | — |

- PR 规模：用 GitHub issue / PR 搜索的 total_count（实测；匹配的是 PR 标题和正文，不搜代码）
  - 正文提到 `toHaveScreenshot` 的已合并 PR：14,656
  - 提到 `toMatchScreenshot` 或 `toMatchImageSnapshot` 的已合并 PR：32,634
  - 同时出现 `chromatic` 和 `visual changes` 的已合并 PR：8,364
- 估算：仓库里真正带截图基线、能跑出 F2P 的
  - 量级在几千个仓库、几万个 PR
  - 依据：jest-image-snapshot 加 backstop 加 loki 合计约 2.5 万个依赖仓库，假设其中 10~20% 活跃且有基线
  - 只算这三个工具，是因为 Chromatic 和 Percy 的基线在云端，仓库里不存在，直接排除
- 主要坑
  - 字体和 GPU 不同会让截图漂移，必须锁定 docker、字体和浏览器版本
  - 不少 PR 只是「更新基线」，代码没改，需要过滤

### 1.3 Issue / PR 对（SWE-bench Multimodal 范式）

- SWE-bench M（[2410.03859](https://arxiv.org/abs/2410.03859)）
  - 论文：617 个实例，来自 17 个 JS 库；每个实例的题面或测试里至少有一张图；人工核验 83.5% 的实例必须看图才能解
  - HF 数据集实测共 612 行（论文写 617，相差 5 行），分两部分
    - dev 102 行：wp-calypso 37 / Chart.js 24 / p5.js 16 / marked 14 / react-pdf 11
    - test 510 行：carbon 133 / openlayers 79 / lighthouse 54 / bpmn-js 54 / highlight.js 39 / alibaba-fusion next 39 / PrismJS 38 / quarto-cli 24 / grommet 20 / prettier 13 / eslint 11 / scratch-gui 6
  - [HF 数据集](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Multimodal)
- OmniGIRL（[2505.04606](https://arxiv.org/abs/2505.04606)）
  - 959 个实例，覆盖 Python / JS / TS / Java 四种语言、15 个仓库，其中一部分 issue 带图
  - 最好成绩：只看带图 issue，Claude-3.5-Sonnet 解出 10.5%
- 「已关闭且关联了 PR、正文带截图」的 issue 数（search/issues 实测；这是关键词匹配，按上界看）

| 查询条件 | 数量 |
|---|---|
| 新图床 `user-attachments/assets`，language:TypeScript | 192,818 |
| 新图床，language:JavaScript | 51,136 |
| 新图床，language:CSS | 3,488 |
| 旧图床 `user-images.githubusercontent.com`，TypeScript | 76,009 |
| 旧图床，JavaScript | 40,801 |
| 旧图床，TypeScript 且带 bug 标签 | 20,978 |
| three.js：已关闭且关联 PR 的 issue | 1,982 |
| Babylon.js：同上 | 361 |
| godot：同上，且标签 topic:rendering | 2,068 |

- 估算：能构造成「issue 截图 + 修复 PR + 可执行测试」的实例
  - 量级在 1 万左右
  - 依据：带图 issue 约 30 万；SWE-bench 类管线在「PR 带测试改动 + 环境能装起来」这两步，通常各只留下 5% 以下
  - 1.1 节里自带像素基线的仓库，转化率会明显更高

### 1.4 Blender / 3D 相关仓库

- Blender 官方 Extensions 平台（[API](https://extensions.blender.org/api/v1/extensions/)，实测）
  - 共 1,533 个扩展：add-on 1,256 个、主题 276 个
  - 许可：GPL-3.0+ 1,341 个、GPL-2.0+ 185 个，MIT 只有 4 个
  - 价值：bpy 代码量大，但大多是 UI 或工具，「输入 → 渲染结果」型的任务很少
- Infinigen（[princeton-vl/infinigen](https://github.com/princeton-vl/infinigen)，BSD）
  - 测试清单里列出的生成器（实测）：室内网格 89、自然网格 82、材质 53、散布 22
  - `src/infinigen/assets` 下有 568 个 py 文件
  - 价值：每个生成器都是带参数的 bpy 代码，随机种子可控、渲染可复现，可以批量造「参数 / 代码 → 图」的逆向任务
- GitHub topic 规模（实测，按 topic 页上的公开仓库数）

| topic | 仓库数 |
|---|---|
| threejs | 24,356 |
| webgl | 15,107 |
| godot | 12,512 |
| frontend-mentor | 7,155 |
| blender | 6,762 |
| storybook | 6,444 |
| creative-coding | 6,078 |
| p5js | 5,150 |
| procedural-generation | 5,024 |
| glsl | 4,278 |
| react-three-fiber | 3,136 |
| js13k | 3,010 |
| blender-addon | 2,323 |
| phaser | 2,321 |
| pixijs | 1,641 |
| babylonjs | 754 |
| blender-python | 575 |
| visual-regression | 363 |
| shadertoy | 312 |
| visual-regression-testing | 250 |
| bpy | 126 |

---

## 2. 开发者社区网站

- 抓取一列的说明
  - 「CF 拦截」：日本和国内两个代理都返回 403，WebFetch 也是 403，说明有反爬，批量抓取需要额外打通
  - 「对 AI 爬虫有限制」：robots.txt 里点名禁止了 GPTBot 等 AI 爬虫

| 站点 | 规模 | 内容形态 | 许可 | 批量抓取 | 作为任务的价值 |
|---|---|---|---|---|---|
| CodePen | 1,000 万+ pen（官方 2016 年数字，[blog](https://blog.codepen.io/2016/11/25/10000000/)） | HTML / CSS / JS 加实时预览，有缩略图 | 公开 pen 默认 MIT（[官方](https://blog.codepen.io/documentation/licensing/)）；私有 pen 无许可 | CF 拦截，robots.txt 也是 403；没有公开 API，只能逐个抓 `/pen/{id}` | 高：自包含、可直接渲染，许可干净；适合做「图 → 代码」和「代码改动 → 截图对比」 |
| JSFiddle | 未公开 | 代码加运行，无截图 | 没有默认许可 | robots.txt 不禁止；没有列表 API | 低：许可不清 |
| ShaderToy | 公开作品 5.2 万+（Wikipedia，2021 年中）；shaders21k 收了约 2 万个 | GLSL fragment shader，可以确定性渲染（给定 iTime） | 默认 CC BY-NC-SA 3.0（非商用，未在官方 terms 页核实）；作者可单独授权 | CF 拦截；API 需要 key，且只能取到作者勾了 `public+api` 的作品 | verifier 很好（逐帧像素），但 NC 许可是硬伤；参考数据集 [Shadereval-inputs](https://huggingface.co/datasets/Vipitis/Shadereval-inputs) 467 条 |
| Sketchfab | CC 可下载模型 50 万+（官方 2020 年，[blog](https://sketchfab.com/blogs/community/over-half-a-million-free-3d-models-on-sketchfab)） | 3D 资产，没有生成代码 | 各种 CC BY 变体 | 有 Data API 和 Download API（要 token） | 中：只能当「目标图 / 目标网格」，要和代码 verifier 搭配（Objaverse 已收） |
| Blender StackExchange | 123,167 问、115,066 答；`python` 标签 13,632、`scripting` 6,738、`geometry-nodes` 5,967（[API 实测](https://api.stackexchange.com/2.3/info?site=blender)） | 问答文本，常带截图和 bpy 片段 | 内容是 CC BY-SA 4.0；但 2024 年起官方数据 dump 要勾选「不用于训练 LLM」（[heise](https://heise.de/-9823083)） | API 免 key，每天 300 次；网页被 CF 拦截 | 中：bpy 报错修复、带截图的「做不出某效果」类问题可以改造成任务；许可有灰色地带 |
| StackOverflow 相关标签 | three.js 20,863 / glsl 8,207 / webgl 6,731 / p5.js 3,162 / blender 3,147 / phaser 2,228 / babylonjs 465（实测） | 同上 | 同上 | 同上 | 同上 |
| BlenderArtists | 602,128 帖、581 万回复（[about.json](https://blenderartists.org/about.json) 实测） | 论坛，作品图和 .blend 附件 | 帖子版权归作者 | Discourse API 可用；robots.txt 对 GPTBot 是 `Disallow: /` | 低到中：对 AI 爬虫有限制，内容偏作品展示 |
| three.js forum（Discourse） | 26,314 帖、225,536 回复（实测） | 问答，大量附 codepen / jsfiddle 链接 | 版权归作者 | Discourse JSON API 可用；robots 只禁 `/search` 等 | 中：适合当 bug 描述 + 外链 demo 的线索源 |
| Blender Market（已更名 Superhive） | 商品数未查 | 付费 add-on 和资产 | 商业许可 | robots 不禁止 | 低：付费内容，不能用 |
| Poly Haven | 2,387 个资产：HDRI 997 / 纹理 869 / 模型 521（[API](https://api.polyhaven.com/assets) 实测） | 资产加预览图 | CC0 | 有公开 API | 高（作为原料）：给 Blender / three.js 任务提供零风险的贴图、HDRI 和模型 |
| Awwwards | 未查 | 获奖网站截图和视频 | 网站版权归属主 | robots 禁止 `/vote` 等 | 低：只有图没有代码，可以当「设计参考图」 |
| Dribbble | 未查 | 设计稿图片 | 版权归作者 | robots 有大量 Disallow | 低：同上，而且版权风险高 |
| Figma Community | 未查 | Figma 设计文件（结构化图层） | 免费文件是 CC BY 4.0（[官方](https://help.figma.com/hc/en-us/articles/360042296374)） | robots 点名禁止 GPTBot / ClaudeBot / CCBot 等，社区搜索页也禁止 | 中：设计稿 → 代码的输入许可干净，但抓取受限 |
| Frontend Mentor | 免费挑战若干，另有 50+ 个付费挑战；GitHub topic frontend-mentor 有 7,155 个解答仓库 | 设计稿（JPG，付费用户有 Figma）+ 用户解答（GitHub + 线上站点） | 设计稿禁止再分发（[FAQ](https://www.frontendmentor.io/faq)）；解答仓库各自的许可 | robots 禁 `/api/` | 中：同一题有成千上万个解答，可以挖「设计稿 → 多个参考实现」，但设计稿本身不能分发 |
| itch.io | 浏览器游戏无官方数字；第三方估 10 万+，不可靠 | 打包好的 HTML5 游戏，通常没有源码 | 各作者自定，商店条款 | CF 拦截 | 低：没有源码 |
| js13kGames | 2,799 个参赛作品（2012–2026，[sitemap](https://js13kgames.com/sitemap.xml) 实测；2026 年 317 个） | 完整的 JS 小游戏，比赛规则要求 GitHub 上有可读源码 | 各作者自定，多为 MIT | robots `Allow: /` | 高：自包含、体积小（≤13KB zip），适合做「游戏规格 → 实现 + 试玩验证」 |
| OpenProcessing | 官方自称「100 万+ 开源项目」 | p5.js / Processing sketch，可在线运行 | 每个 sketch 各自选 CC 许可，常见 BY-SA 和 BY-NC-SA | robots 要求 `Crawl-delay: 6`；没找到官方 API 文档 | 中：creative coding 的主要来源，按许可过滤后可用 |
| Observable | 未查（实测时返回 429） | 交互式 JS 和 D3 notebook | 默认无许可（只在 Observable 内可 fork）；作者可选 MIT / ISC 等 | 被限流 | 中低：要先按许可筛 |
| Kaggle | DistilKaggle 收了 54 万个 notebook | Python notebook，几乎没有前端或 3D 内容 | 每个 notebook 各自许可 | 有 Meta Kaggle 元数据 | 低：和本课题关系弱 |
| HF Spaces | static SDK 的 Space 共 331,654 个（[API](https://huggingface.co/api/spaces?filter=static) 实测分页计数） | 静态 HTML / JS，含大量 AI 生成的单页应用 | 每个仓库各自许可，很多没写 | API 开放，robots `Allow: /` | 中：量大，但质量参差，许可要逐个看；能直接部署和渲染 |

---

## 3. 已有公开数据集 / Benchmark：来源与构造

- 只写数据从哪来、怎么造，不评 verifier
- 已在 benchmarks.md / pipelines.md 里详细写过的条目，这里压缩成一行

| 名称 | arXiv / 链接 | 数据来源 | 规模 | 能否改造成 RL 任务 |
|---|---|---|---|---|
| WebSight | [2403.09029](https://arxiv.org/abs/2403.09029) | 纯合成：LLM 编网站主题 → 代码 LLM 写 Tailwind HTML → Playwright 截图 | v0.2 共 2M | 能：截图 → HTML，渲染后比相似度；但分布偏简单 |
| Design2Code | [2403.03163](https://arxiv.org/abs/2403.03163) | C4 里的真实网页，清洗后人工筛选 | 484 | 能，但规模太小，只适合做评测 |
| Vision2UI → WebCode2M | [2404.06369](https://arxiv.org/abs/2404.06369) | Common Crawl 真实网页渲染后，用打分模型过滤 | v1 2K；v2 2.56M | 能：量大，自带布局信息 |
| Web2Code | [2406.20098](https://arxiv.org/abs/2406.20098) | GPT-3.5 新生成 + GPT-4 精修 WebSight / pix2code | 1,179.7K | 能（同 WebSight） |
| Sketch2Code | [2410.16232](https://arxiv.org/abs/2410.16232) | 人工照着 Design2Code 网页手绘草图 | 731 张草图 / 484 个网页 | 能：草图 → HTML，规模小 |
| Interaction2Code | [2411.03292](https://arxiv.org/abs/2411.03292) | 人工整理真实网页的交互，记录交互前后截图 | 127 个网页 / 374 个交互 | 能：交互后截图可以当目标 |
| WebGen-Bench | [2505.03733](https://arxiv.org/abs/2505.03733) | 人工加 GPT-4o 写指令和功能用例，人工筛选 | 测试 101 条指令 / 647 条用例；训练指令 6,667 条 | 能：GUI agent 跑用例当 reward |
| Web-Bench | [2505.07473](https://arxiv.org/abs/2505.07473) | 资深工程师按 Web 标准和主流框架设计的项目 | 50 个项目 × 20 个顺序依赖任务 = 1,000 | 能：自带 E2E 测试，适合多步 RL |
| FullFront | [2505.17399](https://arxiv.org/abs/2505.17399) | 真实网页经 MLLM 两阶段重建成干净 HTML；QA 部分用 625 张真实截图 | 三类子任务（真实 QA 1,250 对） | 部分能：代码生成子任务可以 |
| FrontendBench | [2506.13832](https://arxiv.org/abs/2506.13832) | 人和 LLM 共同编写 prompt 和测试用例 | 148 对，5 个层级 | 能：自带交互测试 |
| DesignBench | [2506.06251](https://arxiv.org/abs/2506.06251) | GitHub 上的框架项目 + Moz Top 500 网站；修复任务的真值由开发者手写 | 900 例；React / Vue / Angular / 原生 | 能：编辑 / 修复任务天然是改代码 → 对比截图 |
| ArtifactsBench | [2507.04952](https://arxiv.org/abs/2507.04952) · [HF](https://huggingface.co/datasets/tencent/ArtifactsBenchmark) | 人工加 LLM 构造的题目，每题配 checklist | 1,825（HF 实测 1,825 行） | 能：checklist 加时序截图 |
| WebDev Arena | [blog](https://arena.ai/blog/webdev-arena) · [HF](https://huggingface.co/datasets/lmarena-ai/webdev-arena-preference-10k) | 线上真实用户 prompt 加两两投票 | 公开偏好数据 10,501 条（HF 实测） | 能：prompt 池加偏好 RM 训练数据 |
| SWE-bench M | [2410.03859](https://arxiv.org/abs/2410.03859) | 17 个 JS 库里带图的 issue + 修复 PR + 单测 | 617（HF 实测 612） | 能：F2P 单测，见 1.3 节 |
| BlenderGym | [2504.01786](https://arxiv.org/abs/2504.01786) | 手工搭建的起始场景和目标场景 | 245 | 能：按目标图编辑 bpy |
| BlenderLLM / BlendNet / CADBench | [2412.14203](https://arxiv.org/abs/2412.14203) | BlendNet 是 2K 人工加 10K GPT-4o 标注；CADBench-Sim 合成，CADBench-Wild 取自 CAD 论坛真实问题 | BlendNet 12,059；CADBench-Sim 500 / Wild 200 | 能：文本 → bpy，渲染后判分 |
| 3D-PreMise | [2401.06437](https://arxiv.org/abs/2401.06437) | 人工编写的工业零件 prompt 加标准建模程序 | 57 | 能，但太小 |
| SceneCraft | [2403.01248](https://arxiv.org/abs/2403.01248) | 自建带空间约束真值的数据集 + Sintel 电影场景重建 | 未公开具体条数 | 部分能：约束满足可以直接当 reward |
| Infinigen / Indoors | [2306.09310](https://arxiv.org/abs/2306.09310) / [2406.11824](https://arxiv.org/abs/2406.11824) | 程序化生成器 | 生成器约 246 个（见 1.4 节），样本数无上限 | 能：参数 / 代码逆向，渲染可复现 |
| shaders21k | [2211.16412](https://arxiv.org/abs/2211.16412) | 爬取 Shadertoy 等来源的 OpenGL 程序 | 约 21K 个程序 | 能（逐帧像素），但许可继承 NC |
| Shadereval | [GitHub](https://github.com/Vipitis/shadertoys-dataset) · [HF](https://huggingface.co/datasets/Vipitis/Shadereval-inputs) | Shadertoy API 取的公开作品，用 scancode 检测许可后过滤 | 467（HF 实测） | 能：函数补全后比对渲染结果 |
| GameBench | [2406.06613](https://arxiv.org/abs/2406.06613) | 9 个策略游戏环境，评 agent 的推理，不评写代码 | 9 个环境 | 不适合：不是代码生成。真正的游戏代码类见 benchmarks.md §7 和 pipelines.md 游戏表（V-GameGym、GameDevBench、PlaytestArena 等） |

---

## 4. 结论：来源分级

- 评分维度
  - 可验证性：有没有确定性 verifier（像素基线、单测），或者容易补一个
  - 规模：能直接拿到的任务数
  - 许可风险：低 = MIT / BSD / Apache / CC0 / CC BY；高 = NC、ToS 限制训练、无许可

| 级别 | 来源 | 可验证性 | 规模 | 许可风险 | 一句话 |
|---|---|---|---|---|---|
| S | 渲染库像素基线仓库：three.js、Babylon、Blender render tests、maplibre、pixi、plotly、Chart.js、p5、OL、deck.gl、primer/react | 极高：仓库自带像素阈值 | 参考图约 1.9 万张；改基线的 commit 3,413 个（9 个仓库） | 低（Blender 是 GPL，要评估） | 最接近「SWE-bench for pixels」，先做这一块 |
| S | 带截图的 issue + 修复 PR（SWE-bench M 范式，JS / TS 前端） | 高：PR 自带单测 | 候选 issue 约 30 万；能成型的估计在 1 万量级 | 低：按仓库许可过滤 | 要搭环境，管线可以复用 SWE-bench 系 |
| A | Playwright / jest-image-snapshot / Loki / Backstop 生态的长尾仓库 | 高，但截图会漂移 | 估计几千个仓库、几万个 PR | 低 | 要锁死字体和浏览器；Chromatic、Percy 的基线在云端，拿不到 |
| A | Infinigen 及其他程序化生成器 | 高：可以确定性重渲染 | 约 246 个生成器 × 无限种子 | 低（BSD） | 适合造「代码 / 参数逆向」任务 |
| A | CodePen | 中：要自己截图生成目标 | 1,000 万+ pen | 低（公开 pen 是 MIT） | 价值最高的社区源，难点在反爬 |
| A | js13kGames | 中：要自建试玩 verifier | 2,799 个 | 中：各作者自定 | 小而全的网页游戏 |
| A | three.js examples、Babylon playground（当作「生成任务」用） | 高：已有截图 | 611 + 883 | 低 | 可以转成「描述 / 截图 → 复现 example」 |
| B | ShaderToy、shaders21k | 极高：逐帧像素 | 5 万+ | 高（NC-SA） | 技术上最好的 shader 源，被许可卡住 |
| B | Blender SE、StackOverflow 图形类标签 | 中：要补 verifier | 约 2 万个 bpy 和图形类问题 | 中：dump 条款限制 LLM 训练 | 适合做 bug 修复题干 |
| B | Figma Community、Frontend Mentor | 中：设计稿当目标 | 中等 | 中：Figma 是 CC BY 但 robots 禁 AI；FEM 禁止再分发设计稿 | 设计稿 → 代码 |
| B | HF static Spaces、OpenProcessing、Observable | 中 | 33 万 / 100 万+ / 未知 | 中：许可逐个不同 | 先按许可过滤，再按质量过滤 |
| B | Sketchfab、Poly Haven、Blender Extensions | 只能当原料或目标 | 50 万+ / 2,387 / 1,533 | 低到中 | 给 3D 任务提供资产；本身不是任务 |
| C | Awwwards、Dribbble、itch.io、JSFiddle、Kaggle、Blender Market、BlenderArtists | 低：没有代码，或许可不清 | — | 高 | 最多当灵感图或 prompt 种子 |

- 优先级建议
  1. 先把 S 级的像素基线仓库做成 F2P 任务：three.js 与 Babylon 合计约 1,500 个 commit、Blender 有 839 个场景，环境都已经有现成的 CI 脚本
  2. 再按 SWE-bench M 的方式扩到 issue / PR，但只挑带像素或 DOM 测试的仓库，避免环境成本失控
  3. CodePen 和 Infinigen 作为可以规模化的生成类任务池：CodePen 许可干净，Infinigen 可复现

---

## 未能核实 / 局限

- GitHub 代码搜索需要登录，`toHaveScreenshot` 出现在多少个仓库的代码里无法直接计数，1.2 节改用依赖方数量和 PR 正文命中数近似
- 1.3 节的 issue 数是关键词匹配，会有噪声，只能当上界
- plotly 用目录级 commits API 只返回 1 条，原因不明，所以表里没有填 commit 数
- CodePen、ShaderToy、itch.io、Blender SE 的网页和 robots.txt 都被 CF 拦截；ShaderToy 的默认许可来自第三方转述
- 1.1 节的 commit 数不等于 F2P 数，里面包含纯粹重新生成截图的 commit，需要再过滤

