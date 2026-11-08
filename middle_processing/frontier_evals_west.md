# 海外前沿模型发布时报告的「视觉 / 前端 / 3D / 游戏」类 coding 评测

> 查证日期：2026-09-23。只收录原文里看得到的内容；原文没有的写「未报告」。
> 来源类型分四种
> - **厂商自报**：发布页 / system card / model card 里厂商自己跑的数
> - **厂商引用第三方**：厂商页面里写的，但数字来自第三方（Surge / Andon Labs / LMArena 等）
> - **第三方榜单**：榜单网站上直接读到的数，不在厂商发布页里
> - **仅 demo**：发布页只有视频 / 案例，没有分数
>
> 类别标记：`Web` 前端/网页；`3D/CAD`；`Game`；`GUI*` computer-use / GUI grounding（只作参考）；`Vis-ref` 其他视觉推理（参考）

## 读取说明（先看这里）

- **GPT-6 Astra / GPT-5.6 发布页直连返回 403**，表格内容是通过 `r.jina.ai` 渲染后读到的（仍是 openai.com 原页）。表格数字是逐行读出来的；但有一条脚注（[5]，BenchCAD 的脚注）没读到正文
- **「Claude Opus 5」页面是存在的**（2026-07-24），跟 Fable 5 页面不是同一篇：
  - Fable 5 页面：https://www.anthropic.com/news/claude-fable-5-mythos-5 （2026-06-09），发的是 Fable 5 + Mythos 5，对照的是 Opus 4.8
  - Opus 5 页面：https://www.anthropic.com/news/claude-opus-5
- **Google 目前没有 3.x 的新 Pro**：Pro 线最新的还是 Gemini 3.1 Pro（2026-02）；此后发的都是 Flash（3.5 / 3.6 / 3.7 / 3.8，其中 3.8 Flash 是 2026-09-02）。所以本文 Google 部分覆盖 3.1 Pro（Pro 旗舰）和 3.8 Flash（最新发布），另附 3.7 Flash、上一代 3 Pro
- 超出指定范围、但已经存在的新版本：Claude Fable 5.1、Claude Opus 5.5（2026-09-22）、GPT-6 Sol / Luna。本文只在别家的对比列或第三方榜单里提到它们，不单独展开

---

## 1. OpenAI · GPT-6 Astra

出处
- O1 发布页：https://openai.com/index/gpt-6-astra/ （页面上有 2026-09-22 的更新记录）
- O3 开发者博客（Blender）：https://developers.openai.com/blog/architectural-visualization-with-astra
- O4 开发者博客（游戏）：https://developers.openai.com/blog/how-to-build-games-with-astra
- O5 System Card：https://deploymentsafety.openai.com/gpt-6-astra （只有安全类评测，没有视觉 coding 评测）

| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| BenchCAD | 3D/CAD | **95.9%**（对照：GPT-5.6 Sol 83.3%、Fable 5.1 84.3%、Fable 5 67.5%、Opus 5 82.1%） | 原文："With tools … 95.9% geometric-overlap score"。其他厂商的数字都标了脚注 [5]（脚注正文没读到） | 厂商自报（工具增强） | O1 |
| Internal Design Tasks | Web/设计（推测） | **50.0%**（Sol 47.4%、Fable 5 35.8%） | 放在 Professional 表里；原页没写这项测什么、怎么判分 | 厂商自报（内部评测） | O1 |
| ScreenSpot-Pro | GUI* | **92.7%**（Sol 76.9%、Fable 5 87.3%） | no tools；Fable 的数实际取自 Mythos（脚注 17） | 厂商自报 | O1 |
| OSWorld 2.0 | GUI* | **72.6%**（Sol 65.7%、Opus 5 70.2%） | v2026.08.08，offline set，partial score；Claude 分数取自官方榜单（脚注 3） | 厂商自报 | O1 |
| Agents' Last Exam | GUI* | **59.3%**（Sol 53.6%、Fable 5 48.7%、Opus 5 55.5%） | "complex professional tasks in real software" | 厂商自报 | O1 |
| SWE-bench Multimodal / WebDev Arena / Design2Code / 其他前端 benchmark | Web | 未报告 | — | — | O1 |
| Blender 建模 → UE5 可漫游场景 | 3D/CAD | 仅 demo | "models a house in Blender and turns it into a walkable scene in Unreal Engine 5"；开发者博客里写的是用 bpy 建模、Cycles 渲染 | 仅 demo | O1、O3 |
| KiCad PCB 布板 | 3D/CAD（EDA） | 仅 demo | 15 秒快放视频 | 仅 demo | O1 |
| 游戏生成 | Game | 仅 demo | "bring games to life through vivid graphics, engaging gameplay and accurate motion"；开发者博客案例 Void Explorer 用的是 Three.js + WebGPU | 仅 demo | O1、O4 |
| 网站 / Sites / 前端 QA | Web | 仅 demo | "create, host, and share websites, web apps, and games directly from a prompt"；"run frontend QA checks" | 仅 demo | O1 |
| **Code Arena · WebDev** | Web | **1793**（gpt-6-astra-max，排第 1，±12，4,323 票） | Arena Elo | 第三方榜单 | https://arena.ai/leaderboard/code/webdev （2026-09-23） |
| **Vibe Code Bench v1.1** | Web | **89.59%** | accuracy | 第三方榜单 | https://www.vals.ai/benchmarks/vibe-code （2026-09-22） |
| BenchCAD 官方榜 | 3D/CAD | 0.959 voxel IoU（with tools） | 榜单标注为 "vendor self-reported, not re-graded" | 第三方榜单（转录厂商自报） | https://benchcad.com/leaderboard |

## 2. OpenAI · GPT-5.6 Sol（上一代旗舰）

出处：O2 发布页 https://openai.com/index/gpt-5-6/ （有 2026-07-30 / 08-21 的更新记录）

| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| BenchCAD | 3D/CAD | **70.6%**（Terra 62.3%、Luna 63.1%、GPT-5.5 44.4%、Mythos 5 38.4%、Opus 4.8 27.3%） | 不带工具；放在 "Computer use" 表里 | 厂商自报 | O2 |
| BenchCAD (python tool) | 3D/CAD | **83.4%**（GPT-5.5 55.8%、Mythos 5 65%、Opus 4.8 51.8%） | 带 Python 工具。注意 Astra 页面引用的 Sol 分数是 83.3% | 厂商自报（工具增强） | O2 |
| OSWorld 2.0 | GUI* | **62.6%**（Opus 4.8 54.8%） | — | 厂商自报 | O2 |
| MMMU Pro / gdp.pdf | Vis-ref | 83% / 30.7% | no tools / — | 厂商自报 | O2 |
| 前端 / 设计 | Web | 没有 benchmark，只有文字描述 | "step change in design judgment … tasteful, ergonomic, and functional interfaces"；会在渲染结果上检查、修改 | 仅 demo | O2 |
| SWE-bench Multimodal / WebDev Arena / 游戏 | — | 未报告 | — | — | O2 |
| **Code Arena · WebDev** | Web | **1617**（gpt-5.6-sol-xhigh, codex-harness，排第 17） | Arena Elo | 第三方榜单 | https://arena.ai/leaderboard/code/webdev |

---

## 3. Anthropic · Claude Fable 5（/ Mythos 5）

出处
- A1 发布页：https://www.anthropic.com/news/claude-fable-5-mythos-5 （2026-06-09）
- A2 System Card（PDF）：https://anthropic.com/claude-fable-5-mythos-5-system-card （§8.1 汇总表、§8.2、§8.16 Multimodal）

| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| SWE-bench Multimodal | Web | **Mythos 5：54.9%**（Fable 5 在自己的 card 里没单列；Opus 5 card 给的 Fable 5 是 54.1%） | 5 次平均；内部 harness（见 Opus 4.7 card §9.3） | 厂商自报 | A2 §8.2 |
| BenchCAD Vision2Code（全集） | 3D/CAD | Mythos 5 **0.384 voxel IoU**（Mythos Preview 0.355、Opus 4.8 0.273） | 17,874 个文件，不带工具，5 次平均 | 厂商自报 | A2 §8.16.4 |
| BenchCAD Vision2Code（1000 个文件的子集） | 3D/CAD | Mythos 5 **0.379（不带工具）/ 0.650（带工具）**（Preview 0.356 / 0.610） | 带工具 = Python 容器 + 裁图工具 | 厂商自报（工具增强） | A2 §8.16.4 |
| OSWorld-Verified | GUI* | **85.0%**（Fable 5 和 Mythos 5 都是 85.0；Opus 4.8 83.4、GPT-5.5 78.7、Gemini 3.1 Pro 76.2） | 首次尝试成功率，5 次平均；361 题，100 步 | 厂商自报 | A1 表格、A2 §8.16.3 |
| ScreenSpot-Pro | GUI* | Mythos 5 **87.3%（不带工具）/ 90.7%（带工具）**（Preview 79.3 / 93.0） | 5 次平均 | 厂商自报 | A2 §8.16.9 |
| Blueprint-Bench 2 | Vis-ref（照片 → 2D 户型图） | **38.6%**（GPT-5.5 36.2、Gemini 3.5 Flash 33.6、Gemini 3.1 Pro 26.5） | 分数由 Andon Labs 跑、Andon Labs 报 | 厂商引用第三方 | A1 表格、A2 §8.16.2 |
| GDP.pdf | Vis-ref | 29.8% | strict pass，no tools，由 Surge 跑 | 厂商引用第三方 | A1、A2 §8.16.1 |
| WebDev Arena / Design2Code / 游戏生成 | — | 未报告 | — | — | A1、A2 |
| 截图重建 Web App 源码 | Web | 仅 demo（文字描述） | "rebuilding a web app's source code from screenshots alone" | 仅 demo | A1 |
| VibeCAD：浏览器里的 CAD 编辑器 + 3D 可打印模型 | 3D/CAD | 仅 demo | 编辑器本身也是 Fable 5 写的 | 仅 demo | A1 |
| 太阳系 / 日食模拟、配合音乐的流体模拟 | Web/可视化 | 仅 demo | — | 仅 demo | A1 |
| 玩宝可梦火红（只看截图）、Slay the Spire、Factorio | Game（玩游戏，不是做游戏） | 仅 demo；Slay the Spire 的结果只有定性描述（"三倍"） | — | 仅 demo | A1 |
| ViBench（Replit 的端到端 vibe-coding 评测） | Web | 没给数字，客户证言说是 "highest-performing" | — | 厂商引用第三方（仅定性） | A1 客户证言 |
| **Code Arena · WebDev** | Web | **1626**（claude-fable-5-high，排第 12）；Fable 5.1-max 是 1753（排第 2） | Arena Elo | 第三方榜单 | https://arena.ai/leaderboard/code/webdev |
| **Vibe Code Bench v1.1** | Web | **90.35%**（排第 1；Fable 5.1 90.26%） | accuracy | 第三方榜单 | https://www.vals.ai/benchmarks/vibe-code |
| BenchCAD 官方榜 | 3D/CAD | Mythos 5 0.650、Fable 5.1 0.843（with tools） | vendor self-reported，没有重判 | 第三方榜单（转录厂商自报） | https://benchcad.com/leaderboard |

## 4. Anthropic · Claude Opus 5

出处
- A3 发布页：https://www.anthropic.com/news/claude-opus-5 （2026-07-24）
- A4 System Card：https://www.anthropic.com/claude-opus-5-system-card （§8.1、§8.2、§8.12 Multimodal、§9.3）

| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| SWE-bench Multimodal | Web | **59.4%**（Opus 4.8 38.4、Fable 5 54.1） | 5 次平均；公开 dev split，内部 harness，剔除 1 题（§9.3） | 厂商自报 | A4 §8.1 / §8.2 |
| BenchCAD Vision2Code（1000 个文件的子集） | 3D/CAD | **0.366（不带工具）/ 0.821（带工具）**（Opus 4.8 0.277 / 0.521；Mythos 5 0.378 / 0.678） | voxel IoU，5 次平均；图注说 GPT-5.6 Sol 的数是 OpenAI 公布的全集分数 | 厂商自报（工具增强） | A4 §8.12.2 |
| OSWorld 2.0 | GUI* | **70.6%**（Fable 5 66.1、Opus 4.8 55.7、GPT-5.6 Sol 62.6） | 首次尝试成功率，5 次平均；最多 500 步 | 厂商自报 | A3 表格、A4 §8.12.3 |
| ARC-AGI-3 | Vis-ref（交互式游戏环境推理，不是做游戏） | 30.2%（high） | ARC Prize 验证 | 厂商引用第三方 | A3、A4 §8.14.2 |
| FrontierBench v0.1 | 含 CAD 类任务的终端任务集 | 43.3%（Harbor 跑的）/ 44.4%（内部跑的） | 74 题，其中包括 CAD 任务，但没有单独拆出分数 | 厂商自报 + 第三方 | A3、A4 §8.5 |
| WebDev Arena / Design2Code / 游戏生成 | — | 未报告 | — | — | A3、A4 |
| FreeCAD：从图纸重建机械零件 | 3D/CAD | 仅案例（是 Frontier-Bench 里的一道题，没有单独分数） | 模型看不到图，自己写了一条 CV 管线从像素里取几何信息 | 仅 demo | A3 |
| 风洞 / 细胞交互可视化 | Web/可视化 | 仅 demo | "much stronger visual outputs" | 仅 demo | A3 |
| 前端 / 游戏 / 3D（客户证言） | Web/Game | 仅定性 | "the best animations, games, and 3D work we have seen from an Opus model"；另一条证言说它会在桌面宽度和手机宽度下自己检查页面 | 仅 demo（客户证言） | A3 |
| **Code Arena · WebDev** | Web | **1691**（claude-opus-5-max，排第 3）/ 1661（-high，排第 6） | Arena Elo | 第三方榜单 | https://arena.ai/leaderboard/code/webdev |
| **Vibe Code Bench v1.1** | Web | **88.40%**（Opus 5.5 是 90.29%） | accuracy | 第三方榜单 | https://www.vals.ai/benchmarks/vibe-code |

> 补充：Opus 5.5（2026-09-22）发布页上视觉相关的只有 OSWorld 2.0 81.8%（partial）和 Chartography 89.0%（with tools），没有前端 / 3D / 游戏类 benchmark。出处：https://www.anthropic.com/claude-opus-5-5

---

## 5. Google · Gemini 3.1 Pro（目前的 Pro 旗舰，2026-02）

出处
- G1 Model Card：https://deepmind.google/models/model-cards/gemini-3-1-pro/
- G2 发布博客：https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/

| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| MMMU-Pro | Vis-ref | 80.5% | no tools | 厂商自报 | G1 |
| WebDev Arena / SWE-bench Multimodal / ScreenSpot-Pro / OSWorld / 3D / 游戏 | — | 未报告（model card 表里都没有） | — | — | G1 |
| 动画 SVG、国际空间站遥测仪表盘、3D 椋鸟群飞（手势追踪 + 生成式配乐）、文学主题的个人网站 | Web / 3D | 仅 demo | — | 仅 demo | G2 |
| **Code Arena · WebDev** | Web | **1447**（gemini-3.1-pro-preview，排第 60） | Arena Elo | 第三方榜单 | https://arena.ai/leaderboard/code/webdev |
| OSWorld-Verified | GUI* | 76.2% | 出现在 Gemini 3.6 Flash model card 的对比列里 | 厂商自报（写在后续 card 里） | https://deepmind.google/models/model-cards/gemini-3-6-flash/ |

## 6. Google · Gemini 3.8 Flash（最新发布，2026-09-02）

出处
- G3 Model Card：https://deepmind.google/models/model-cards/gemini-3-8-flash/
- G4 发布博客：https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/

| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| OSWorld-2.0 | GUI* | **59.0%**（3.7 Flash 50.6、Opus 5 75.4、GPT-5.6 Sol 62.6） | partial score，启用 batch tool；Gemini 和 Sonnet 5 是自己算的 | 厂商自报 | G3、G4 表格 |
| CharXiv Reasoning / LVBench / GDP.PDF | Vis-ref | 86.2% / 87.8%（agentic）/ 35.0% | — | 厂商自报 | G3 |
| WebDev / Code Arena / SWE-bench Multimodal / 3D / 游戏 | — | 未报告（3.8 的表里去掉了 3.7 表里的 Code Arena 那一行） | — | — | G3 |
| Antigravity 里一句提示做出的 3D 巫师城堡解谜游戏 | Game / 3D | 仅 demo | 纹理用 Nano Banana 生成 | 仅 demo | G4 |
| DOS 版 Google Maps（可玩）、USGS 地形剖面图、Hardware Anatomy（Three.js 爆炸视图） | Web / 3D | 仅 demo | — | 仅 demo | G4 |
| **Code Arena · WebDev** | Web | **1584**（gemini-3.8-flash-high，排第 23，Preliminary） | Arena Elo | 第三方榜单 | https://arena.ai/leaderboard/code/webdev |

## 7. Google · 对照：Gemini 3.7 Flash（2026-08）与 Gemini 3 Pro（2025-11，上一代 Pro）

| 模型 | Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|---|
| 3.7 Flash | **Code Arena（Web development）** | Web | **1588 Elo**（3.6 Flash 1538、Sonnet 5 1541、GPT-5.6 Terra 1523） | 方法页原文："sourced from the official public Web Dev leaderboard" | 厂商引用第三方 | https://deepmind.google/models/model-cards/gemini-3-7-flash/ ；方法页 https://deepmind.google/models/evals-methodology/gemini-3-7-flash |
| 3.7 Flash | OSWorld-2.0 / Agent's Last Exam | GUI* | 47.9% / 26.3% | — | 厂商自报 | 同上 |
| 3 Pro | **WebDev Arena** | Web | **1487 Elo**（原文："tops the WebDev Arena leaderboard"） | 写在正文里，不在表格里 | 厂商引用第三方 | https://blog.google/products/gemini/gemini-3/ |
| 3 Pro | ScreenSpot-Pro | GUI* | **72.7%**（2.5 Pro 11.4、Sonnet 4.5 36.2、GPT-5.1 3.5） | 带 "capture screenshot" 工具，media_resolution=extra_high；设成 high 时是 60.5 | 厂商自报（工具增强） | 同上表格；方法页 https://deepmind.google/models/evals-methodology/gemini-3-pro |
| 3 Pro | 复古 3D 飞船游戏、3D 体素艺术、生成式 UI | Game / 3D / Web | 仅 demo | — | 仅 demo | https://blog.google/products/gemini/gemini-3/ |
| 3 Pro | Code Arena · WebDev（当前榜） | Web | 1439（排第 63） | Arena Elo | 第三方榜单 | https://arena.ai/leaderboard/code/webdev |

---

## 结论

1. **前端 / Web 方向，三家报的东西完全不一样**
   - Anthropic：唯一一家长期报 **SWE-bench Multimodal** 的（Mythos 5 54.9%，Opus 5 59.4%）
   - Google：报的是 **WebDev Arena / Code Arena Elo**（3 Pro 1487、3.7 Flash 1588），但 3.1 Pro 和 3.8 Flash 的表里都没有这一项
   - OpenAI：GPT-6 Astra 只报了一个说明不清的 "Internal Design Tasks"（50.0%）
   - 真正能横向比三家的只有第三方榜单：**Code Arena WebDev**（Astra 1793 第 1、Fable 5.1 1753、Opus 5 1691）和 **Vals Vibe Code Bench v1.1**（Fable 5 90.35%、Astra 89.59%、Opus 5 88.40%）
   - Design2Code、ArtifactsBench、WebArena、VisualWebArena、Screenshot2Code、FrontendBench：三家的发布材料里都**没有出现**
2. **BenchCAD 是今年唯一一个三家里有两家同时跟进的 3D / CAD benchmark**
   - OpenAI 和 Anthropic 都报了 Vision2Code，但口径不一样，不能直接比
     - OpenAI：写成百分比，"geometric overlap"，带工具（Astra 95.9%）
     - Anthropic：voxel IoU，分成全集和 1000 个文件的子集，带工具和不带工具分开报（Opus 5 带工具 0.821）
   - BenchCAD 官方榜把两家的数都标成「vendor self-reported，没有重判」
   - Google 完全没报
3. **Blender / 3D 场景 / 游戏生成：三家都没有公开 benchmark，只有 demo**
   - Astra：Blender → UE5 建房子、Three.js 太空游戏
   - Fable 5：VibeCAD
   - Gemini 3.8 Flash：3D 城堡游戏、Three.js 爆炸视图
   - 跟「游戏」沾边的数字只有两类，但都不是「做游戏」
     - 玩游戏：ARC-AGI-3、宝可梦、Slay the Spire
     - 第三方 Code Arena 里的 Gaming 分类
4. **GUI / computer-use 是三家都报的**，但版本在变
   - 上半年报 OSWorld-Verified，下半年已经全部换成 OSWorld 2.0
   - ScreenSpot-Pro 仍然是 GUI grounding 的通用尺子（Astra 92.7%、Mythos 5 87.3%、Gemini 3 Pro 72.7%）
   - 这一类只能当「会不会看界面」的参考，不代表视觉 coding 能力
5. **写博客时要注意口径**
   - 同一个模型在不同厂商页面上的分数经常对不上：GPT-5.6 Sol 的 BenchCAD 在自家页面是 83.4%，在 Astra 页面是 83.3%；Fable 5 的 SWE-bench Multimodal 在 Anthropic 两份 card 里分别是 54.9（Mythos 5）和 54.1
   - OpenAI 在对比表里常用 Mythos 的数来代替 Fable
   - 引用时要写清楚：是哪个页面给的、带没带工具、是全集还是子集

