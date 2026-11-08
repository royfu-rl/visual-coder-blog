<!--ANALYSIS-->
视频即代码（Code2Video）指：让 agent 写出可执行的动画代码，再由确定性渲染器把代码渲染成视频，而不是用扩散模型直接生成像素。本文用三个维度比较这类工作：

- **任务形态（Task Form）**：讲稿或论文到教学动画、静态图到矢量动画、文档到幻灯片与演讲视频、规格说明到成片。
- **渲染器（Renderer）**：Manim、SVG + CSS、Lottie、Beamer、HTML/Canvas、游戏引擎。渲染器决定表达力上限，也决定这支视频能被怎样验证。
- **验收方式（Evaluation）**：
  - 渲染成功率：代码能否无错渲染。可执行、可复现。
  - 版式几何检查：元素是否重叠、出框。可执行。
  - 知识传递：让模型先屏蔽知识再只看视频答题，答对率就是传递量（TeachQuiz、PaperQuiz）。
  - VLM 看图打分：用视觉语言模型给画面打分，与人评经常不相关，只能作参考。

四组工作的渲染器与验收方式区别如下：

| 组 | 典型渲染器 | 产物 | 典型验收 |
|---|---|---|---|
| 教学动画 | Manim（Python） | 数学 / 定理 / 物理讲解视频 | 渲染成功率、版式几何、知识传递（TeachQuiz） |
| 矢量 / 图表 / Lottie | SVG + CSS、Lottie、TikZ | 矢量动画、动态图表、图示代码 | 语义对齐、渲染成功率、紧凑度 |
| 幻灯片 / 演讲视频 | python-pptx、Beamer LaTeX | 幻灯片、海报、带讲解的演讲视频 | 看产物答题（PaperQuiz / PresentQuiz）、设计质量 |
| 全代码成片 | HTML / Canvas / 引擎 | 短片、MV、完整影片 | 可运行、可交互、时序截图审查 |

逐帧确定性是这条路线的根：每一帧是帧号与代码的纯函数，同代码同帧永远渲染出相同像素，所以可逐帧复现、可测试、可迭代——这是扩散视频没有的性质。

<!--LANDSCAPE-->

<!--EVOLUTION-->
核心发现：验收标准从「画面像不像」提高到「能不能跑、能不能学到知识」。

- **2024 年：矢量动画从设计工具起步。** Keyframer 把「静态 SVG 加自然语言 → CSS 动画代码」做成一项设计研究，归纳出用户怎样用提示词描述运动，是这条线最早、被引最多的工作。
- **2025 年上半年：教学动画进入 agent 化。** TheoremExplainAgent 用规划器加编码器写出五分钟以上的 Manim 讲解视频，并建了 TheoremExplainBench；AutoPresent、PPTAgent 把幻灯片生成变成写 python-pptx 代码或可执行编辑指令。
- **2025 年下半年：闭环成形，并扩展到演讲视频。** Code2Video 用 Planner-Coder-Critic 三段闭环把教学视频拉长、拉准，建了 MMMC 与 TeachQuiz；同一个实验室的 Paper2Video 把论文编成 Beamer 代码再编译成带讲解的演讲视频。动态图表方向出现 DCG-Bench。
- **2026 年：矢量动画走向自回归与强化学习，记忆闭环出现。** VAnim 把逐帧改成在 SVG 树上做稀疏状态更新并用渲染感知的强化学习训练，OmniLottie 用 Lottie tokenizer 自回归生成；ManimAgent 给闭环加跨任务记忆，把修复轮数砍了近一半。

数据解读：早期只看渲染出的画面像不像，新工作普遍加入了可执行检查（能否渲染、版式几何）和知识传递测试，少数开始把渲染反馈做成强化学习奖励。

<!--CHOOSE-->
按目标能力选择：

- 教学数学动画：Code2Video、TheoremExplainAgent（Manim）
- 矢量与标识动画：Keyframer、Decomate、Vector Prism（SVG + CSS）、OmniLottie（Lottie）
- 动态图表：OpusAnimation / DCG-Bench
- 幻灯片、海报与演讲视频：AutoPresent、PPTAgent、Paper2Poster、Paper2Video
- 任意 HTML 画面与成片：HyperFrames、Remotion

验收方式决定结果能否作为主指标。可执行检查（渲染成功率、版式几何）和知识传递测试（TeachQuiz、PaperQuiz）可以作为主指标；VLM 看图打分与人评经常不相关，只能作参考。

<!--PIPE_INTRO-->
下表收录把视频写成代码的公开工作，覆盖教学动画、矢量动画、幻灯片与演讲视频，以及全代码成片的开源管线。Download 列为代码或数据下载入口，影响力列填写有公开数字的项目（GitHub star 或 HF 下载量）。

<!--PIPE_NOTE-->
- **紧凑表示是制胜招，不是写代码本身。** 直接让模型吐裸 Lottie JSON，成功率接近零；OmniLottie 加一个 Lottie tokenizer 后升到 88.3%，VAnim 把逐帧改成稀疏状态更新，token 效率提升 9.86 倍。模型学不动的是长串低层代码，不是代码这个媒介。
- **验收分成两半，可靠的那半是可执行检查。** 渲染成功率、版式几何、答题正确率可复现；VLM 看图打分不可靠——ManimAgent 实测它的 VLM 判官与人评相关系数为 −0.17，并明确把 VLM 排除在头部评测证据之外。
- **渲染器基础设施已成熟，但面向 agent 的只有一个。** Manim、Remotion、Motion Canvas 都稳定可用，HyperFrames 是唯一一个把「给 agent 自动化用」写进设计的渲染器（命令行默认非交互、逐帧定位可复现）。
- **最缺的是失败后如何修复的轨迹数据。** 公开数据几乎全是一次成功的配对；ManimAgent 用双通道记忆存成功与失败经验，是少数带迭代过程的工作。

<!--PICK-->
细讲按采用度（下载量或 star 数）排序，重点说明代码如何自动合成并验收。采用度较低、但带可验证奖励或多轮修复轨迹的工作放在最后。

| 候选 | 代码/数据开源 | 规模 | 可验证信号 | 多轮修复轨迹 | 采用度 | 结论 |
|---|---|---|---|---|---|---|
| Code2Video | ✓ | MMMC 456 单元 | TeachQuiz 知识传递 | ✓ 评审器迭代 | 细讲 | **细讲** |
| TheoremExplainAgent | ✓ | 240 定理 | 渲染成功率 + 5 指标 | ✓ 自纠 5 次 | 细讲 | **细讲** |
| Paper2Video | ✓ | 101 篇论文 | PresentQuiz 超过人类 | ✓ 编译反馈修复 | 细讲 | **细讲** |
| ManimAgent | 承诺开源 | 记忆库 200 条 | 渲染 + VLM 关键帧 | ✓ 记忆闭环 | 细讲（靠后） | 细讲（靠后） |
| Keyframer | ✓ | 设计研究 13 人 | 编译 + 人工 | ✗ | 细讲（靠后） | 细讲（靠后） |
| Vector Prism | 未放出 | 保真 76.1 | GPT-T2V 打分 | ✗ | 细讲（靠后） | 细讲（靠后） |
| VAnim | ✓ | SVGAnim-134k | 渲染感知 RL 奖励 | ✓ GRPO | 细讲（靠后） | 细讲（靠后） |

<!--FRONTIER-->
<table class="frontier"><thead><tr><th>信号</th><th>厂商 / 模型</th><th>形态</th><th>来源</th></tr></thead><tbody><tr><td class="bench" rowspan="3">全代码成片技能潮<span class="self-tag">社区</span></td><td>{{lab:Anthropic}} Claude Opus 5.5</td><td>编码时长跨过门槛，社区用它写 HTML/Canvas/Three.js 动画代码逐帧渲染出片，无视频模型</td><td><a href="https://www.anthropic.com/news/claude-opus-5-5">Blog</a></td></tr><tr><td>{{lab:Google}} Gemini 3.8 Flash</td><td>一句提示生成 Three.js 动画与可交互 3D 场景（发布页 demo）</td><td><a href="https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/">Blog</a></td></tr><tr><td>{{lab:OpenAI}} GPT-6 Astra</td><td>Three.js + WebGPU 动画与游戏（发布页 demo）</td><td><a href="https://developers.openai.com/blog/how-to-build-games-with-astra">Blog</a></td></tr><tr><td class="bench" rowspan="1">自建动画子类<span class="self-tag">自建</span></td><td>{{lab:Moonshot}} Kimi K3</td><td>Kimi Webdev Bench 的 SVG / 动画子类，题目不公开</td><td><a href="https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf">Blog</a></td></tr><tr><td class="bench" rowspan="1">未报告相关分数</td><td>{{lab:ByteDance Seed}} {{lab:MiniMax}} {{lab:DeepSeek}} 等</td><td>未报告 code-video 分数</td><td>—</td></tr></tbody></table>

数据解读：

- **没有厂商报告公开的 code-video benchmark。** MMMC、TeachQuiz、TheoremExplainBench 等都没有出现在任何厂商的发布材料里。这是一个和游戏方向一样的空白：可执行验收条件具备，但还没进入厂商的对比表。
- **厂商的信号只有两种，都不是在测做视频。** 一种是全代码成片的社区技能潮，由 Claude Opus 5.5 的编码能力触发，而非某个新视频功能；另一种是发布页的动画 demo（Gemini、GPT-6 Astra）。
- **这是一个开源与学术主导的方向。** 和 Web、3D、Game 不同，code-video 的前沿目前在开源仓库和论文里，不在厂商榜单上。

