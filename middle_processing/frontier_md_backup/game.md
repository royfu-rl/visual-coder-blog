<!--ANALYSIS-->
游戏类 benchmark 数量不多。本文用三个维度比较它们：

- **任务形态（Task Form）**：从零生成可玩的游戏、在已有工程上修改、查找 bug。
- **引擎（Engine）**：Pygame、浏览器 JavaScript、Godot、UE5 C++。越靠后越接近商业工程。
- **验收方式（Evaluation）**：
  - 沙箱运行加视觉检查：只能证明游戏可以运行。
  - 单元测试或行为测试：证明逻辑正确。
  - Agent 试玩加 rubric：证明游戏可以玩。

三个维度对应五种能力：可运行、可玩、资产与着色器、工程架构、查找 bug。

<!--LANDSCAPE-->
下表按发布时间排序。名称前为参与机构的 logo，工业界和学术界各取一个；名称链接到论文。Download 列为数据下载入口。影响力列只填写有公开数字的项目（GitHub star 或 HF 下载量）。

<!--EVOLUTION-->
核心发现：验收标准从「能编译」提高到「能玩、能维护」。

- **2025 年：第一批游戏生成 benchmark。** V-GameGym 包含 2,219 个 Pygame 样本，评测了 70 个模型，最好的约为 45%。
- **2026 年上半年：使用真实引擎，并由 agent 试玩。** GameDevBench 包含 333 个 Godot 任务，最佳 agent 约为 54%，其中 2D 图形类只有 31.6%；加入图像和视频反馈后，Sonnet 4.5 从 33.3% 提高到 47.7%。PlayEval 中各基线的编译通过率高，但 Play@3 接近 0。PlaytestArena 中边写边试玩的 Play2Code 通过率为 66.8%，比单次生成高 37.1 个百分点。GBQA 中找 bug 最好的模型为 48.39%。
- **2026 年中：评测工程规模。** GameCraft-Bench（Godot）中最强的 agent 为 41.46%。JamBench 中运行通过率从小项目的 80.4% 降到大项目的 5.7%，主要失败原因是架构设计，不是语法。GameEngineBench（UE5 C++）最强配置的 pass@1 为 55.5%，有 31 题所有配置都没有解出。

数据解读：编译通过率会高估模型的游戏开发能力，评测必须加入试玩或行为测试。

<!--CHOOSE-->
按目标能力选择：

- 从零生成可玩游戏：PlaytestArena、V-GameGym
- 真实引擎工程：GameDevBench（Godot）、GameEngineBench（UE5）
- 大项目架构：JamBench
- 逻辑正确性与查找 bug：PlayEval、GBQA

只看编译结果或截图的评测会高估模型，必须有 agent 试玩或行为测试。

<!--PIPE_INTRO-->
下表按发布时间排序。Download 列为数据下载入口，数据未公开的写明状态。影响力列只填写有公开数字的项目。

<!--PIPE_NOTE-->
- **没有规模化的开源「游戏代码加执行轨迹」训练集。** 10 条中只有 GameQA 的数据可以下载，它是由游戏代码生成的视觉问答数据，不是代码生成数据。
- **最接近的工作**：V-GameGym（2.2K 条，偏评测）、OpenGame（只公开了框架）、PlayTrain（把游戏用作强化学习环境）。
- **游戏可以自动验证。** 单元测试和试玩 agent 都能给出可验证的奖励，适合构建自动化数据管线。

<!--PICK-->
游戏方向没有同时满足「数据开源、规模化、可验证」的工作。细讲按采用度挑选了影响最大的三条，说明它们的数据如何自动合成。

| 候选 | 数据开源 | 规模 | 可验证信号 | 多轮修复轨迹 | 采用度 | 结论 |
|---|---|---|---|---|---|---|
| GameQA | ✓ | 140K | 游戏代码生成真值 | ✗ | 3.7k 下载 | **细讲** |
| OpenGame / GameCoder | 仅框架 | 未披露 | 单测 + 无头浏览器 | ✗ | 3.0k star | **细讲** |
| MarioGPT | 仅代码 | — | 可玩性 | ✗ | 1.2k star | **细讲** |
| V-GameGym | ✓ | 2,219 | 沙箱运行 | ✗ | 103 下载 | 未选：规模太小，偏评测 |

<!--FRONTIER-->
核心发现：没有任何厂商报告公开的游戏生成 benchmark。游戏方向的分数只来自自建评测集的子类，其余都是 demo。

| 机构 | 模型 | Benchmark | 分数 | 口径 | 来源 |
|---|---|---|---|---|---|
| {{lab:OpenAI}} | GPT-6 Astra | — | 未报告 | Three.js + WebGPU 太空游戏 | [仅 demo](https://developers.openai.com/blog/how-to-build-games-with-astra) |
| {{lab:Anthropic}} | Claude Fable 5 | — | 未报告 | 玩宝可梦、Slay the Spire（玩游戏，不是做游戏） | [仅 demo](https://www.anthropic.com/news/claude-fable-5-mythos-5) |
| {{lab:Anthropic}} | Claude Opus 5 | ARC-AGI-3 | 30.2% | 交互式环境推理，不是做游戏 | [厂商引用第三方](https://www.anthropic.com/news/claude-opus-5) |
| {{lab:Google}} | Gemini 3.8 Flash | — | 未报告 | 一句提示生成 3D 城堡解谜游戏 | [仅 demo](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/) |
| {{lab:Moonshot}} | Kimi K3 | Kimi Webdev Bench · Games | 胜 55.6 / 平 3.7 / 负 40.7 | 对 Claude Opus 4.8，专家盲评 | [自建评测集（技术报告）](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf) |
| {{lab:Zhipu}} | GLM-5.3-Flash | — | 未报告 | Godot 游戏 | [仅 demo](https://docs.z.ai/guides/vlm/glm-5.3-flash) |
| {{lab:Qwen}} | Qwen3.8-Max | — | 未报告 | 一句话生成游戏 | [仅 demo](https://qwen.ai/blog?id=qwen3.8) |
| {{lab:ByteDance Seed}} | Seed2.1 Pro | GameWorld | 31.2 | 玩浏览器游戏，不是做游戏 | [厂商自报（model card）](https://lf3-static.bytednsdoc.com/obj/eden-cn/lapzild-tss/ljhwZthlaukjlkulzlp/seed2.1/Seed2_1_Model_Card.pdf) |
| {{lab:Tencent Hunyuan}} | Hy4 preview | — | 未报告 | 单个 prompt 生成可玩原型（文字描述） | [仅 demo](https://huggingface.co/tencent/Hy4-preview) |

数据解读：

- **游戏生成没有公开 benchmark 进入厂商的发布材料。** Benchmark Timeline by Capability 总表中的 GameDevBench、PlaytestArena、GameEngineBench 等都没有厂商报告。
- **现有的游戏类分数有两种，都不是在测做游戏。** 一种是自建评测集的子类（Kimi Webdev Bench 的 Games、GLM CC-Bench-V2 的 Web Games、QwenWebBench 的 Games），题目不公开；另一种是玩游戏的能力（GameWorld、ARC-AGI-3、宝可梦）。
- **这是一个空白。** 游戏生成可以用单元测试和 agent 试玩自动验收，具备建立公开 benchmark 的条件。

