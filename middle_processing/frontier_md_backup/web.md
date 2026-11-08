<!--ANALYSIS-->
比较 Web 类 benchmark 时，本文固定使用三个维度：

- **输入形态（Input）**：截图、设计稿、草图、自然语言规格说明、多轮对话、图表图像。
- **产物形态（Output）**：单页 HTML、多文件 Web App、绘图代码或 SVG。
- **验收方式（Evaluation）**：
  - 视觉相似度：把渲染结果和参考图逐项比较。结果可复现，但只衡量外观是否一致。
  - Agent 实测：浏览器 agent 按工作流操作页面，检查功能是否可用。
  - MLLM checklist 或人工评审：用于审美和设计质量。MLLM checklist 需要先与人工评审对齐。

三个维度对应六种能力：视觉还原、交互实现、功能正确、多轮编辑、审美对齐、图表与矢量精度。

<!--LANDSCAPE-->
下表按类别分为 3 组，点击表格上方的按钮切换，每组按发布时间排序。名称前为参与机构的 logo，工业界和学术界各取一个；名称链接到论文。Download 列为数据下载入口。影响力列只填写有公开数字的项目（GitHub star 或 HF 下载量）。

<!--EVOLUTION-->
核心发现：评测对象从「输出是否与参考图一致」转向「输出是否可用」。

- **2023 年至 2024 年上半年：截图转代码成为标准任务。** Design2Code 使用 484 个真实网页，按渲染相似度打分。WebCode2M 和 Web2Code 把数据规模扩大到百万级。图表方向的 ChartMimic、Plot2Code 使用同样的评测方法。StarVector 的 SVG-Bench 指出，像素指标无法衡量 SVG 质量。
- **2024 年下半年：评测加入交互。** Sketch2Code 加入多轮用户反馈。Interaction2Code 专门测试交互行为，交互部分的得分低于整页生成。WebDev Arena 由真人试用后投票，平局率为 26%。
- **2025 年：由 agent 执行测试成为主流。** WebGen-Bench 用 UI agent 执行 647 个测试用例，最好的组合为 27.8%。ArtifactsBench 由 MLLM 按逐题 checklist 打分，与 WebDev Arena 排名的一致性为 94.4%。图表方向转向编辑任务，ChartEdit 的最高分为 59.96。
- **2026 年上半年：评测端到端交付和多轮编辑。** Vibe Code Bench 要求从规格说明构建并部署应用。论文中最好的模型为 61.8%，接入外部服务后从 71% 降到 30%；v1.1 榜单上 Claude Fable 5 为 90.35%。FronTalk 发现模型在多轮对话中会覆盖已经实现的功能。Figma2Code 发现闭源模型的视觉还原度高，但响应式布局和代码可维护性差。
- **2026 年中：评测长页面和多页状态。** LongWebBench 显示页面越长，结构保真度越低。UI2App 中一半模型在跨页状态上得 0 分。

数据解读：单页截图转代码已接近饱和，新的 benchmark 集中在交互、多轮编辑和端到端交付上。

<!--CHOOSE-->
单页还原类 benchmark（如 Design2Code）只适合做回归测试。按目标能力选择：

- 交互实现：Interaction2Code、WebIGBench、UI2App
- 功能正确与端到端交付：WebGen-Bench、Vibe Code Bench
- 审美与设计质量：ArtifactsBench（自动评审），UI-Bench 与 WebDev Arena（人工评审）
- 多轮编辑：FronTalk、1D-Bench、ChartEditBench
- 图表与 SVG 精度：ChartMimic、Chart2Code、SVGenius

评测方式决定结果能否作为主指标。执行类和 agent 实测类可以作为主指标；MLLM checklist 需要先与人工评审对齐；纯视觉相似度只作参考。

<!--PIPE_INTRO-->
下表收录为训练模型生成「代码与视觉结果」配对数据的公开工作，分为 3 组，每组按发布时间排序。Download 列为数据下载入口，数据未公开的写明状态。影响力列只填写有公开数字的项目。

<!--PIPE_NOTE-->
- **真值多由程序合成，真实网页多用于测试。** WebSight（2M）由 LLM 生成网页代码后渲染截图；WebCode2M（2.56M）从 Common Crawl 爬取后过滤。Design2Code 的训练集取自 WebSight 的子集。
- **奖励信号逐步细化。** ScreenCoder 使用像素级 −MSE，WebRenderBench 使用布局与样式一致性，WebGen-Agent 使用 VLM 截图分加 GUI-agent 测试分，UI2Code^N 使用相对排序。
- **交互与修复数据公开得最少。** WebVIA、UI2Code^N 只公开了模型；ReLook、MT-Web2Code 只承诺开源。
- **图表与 SVG 数据最成熟。** 19 条中 16 条可以下载，规模达到百万级（SAgoge 16M、MMSVG-2M、VisCode-Multi-679K），执行并渲染验证是通用做法。

<!--PICK-->
细讲按采用度（下载量或 star 数）排序，重点说明数据如何自动合成。采用度较低、但带可验证奖励或多轮修复轨迹的工作放在最后。

| 候选 | 数据开源 | 规模 | 可验证信号 | 多轮修复轨迹 | 采用度 | 结论 |
|---|---|---|---|---|---|---|
| ChartGalaxy | ✓ | 1.7M | 模板程序化，真值确定 | ✗ | 23.0k 下载 | **细讲** |
| WebSight | ✓ | 2M | 渲染截图配对 | ✗ | 18.1k 下载 | **细讲** |
| pix2code | ✓ | 3 平台合成 GUI | DSL 渲染，真值确定 | ✗ | 12.0k star | **细讲** |
| CoSyn-400K | ✓ | 400K 图 | 代码渲染 | ✗ | 11.0k 下载 | **细讲** |
| ScreenCoder | 部分 | 10K | 像素 −MSE 奖励 | ✗ | 3.0k star | **细讲** |
| WebCode2M | ✓ | 2.56M | 审美打分过滤 | ✗ | 2.4k 下载 | **细讲** |
| VinciCoder | ✓ | 1.6M | DINOv2 渲染相似度 | ✓ 看图修代码 300K | 829 下载 | 细讲（靠后） |
| WebGen-Agent | ✓ | 700 轨迹 + 500 指令 | 截图分 + GUI-agent 测试 | ✓ | 163 下载 | 细讲（靠后） |
| VisCoder2 | ✓ | 679K | Jupyter 执行 + 出图校验 | ✓ 纠错对话 66K | 49 下载 | 细讲（靠后） |
| WebVIA / UI2Code^N | ✗ | 11K / 80K | ✓ | ✓ | 39 / 87 star | 未选：数据没放出 |

<!--FRONTIER-->
核心发现：前沿厂商在 Web 方向没有共同采用的公开 benchmark。能横向比较各家模型的只有两个第三方榜单。

| 机构 | 模型 | Benchmark | 分数 | 口径 | 来源 |
|---|---|---|---|---|---|
| {{lab:OpenAI}} | GPT-6 Astra | Internal Design Tasks | 50.0% | 发布页未说明测试内容 | [厂商自报（内部）](https://openai.com/index/gpt-6-astra/) |
| {{lab:OpenAI}} | GPT-6 Astra | [Code Arena · WebDev](https://arena.ai/leaderboard/code/webdev) | 1793（第 1） | Arena Elo，2026-09-23 | [第三方榜单](https://arena.ai/leaderboard/code/webdev) |
| {{lab:OpenAI}} | GPT-6 Astra | [Vibe Code Bench v1.1](https://www.vals.ai/benchmarks/vibe-code) | 89.59% | accuracy | [第三方榜单](https://www.vals.ai/benchmarks/vibe-code) |
| {{lab:Anthropic}} | Claude Opus 5 | [SWE-bench Multimodal](https://arxiv.org/abs/2410.03859) | 59.4% | 5 次平均，内部 harness | [厂商自报（system card）](https://www.anthropic.com/claude-opus-5-system-card) |
| {{lab:Anthropic}} | Claude Opus 5 | [Code Arena · WebDev](https://arena.ai/leaderboard/code/webdev) | 1691（第 3） | Arena Elo | [第三方榜单](https://arena.ai/leaderboard/code/webdev) |
| {{lab:Anthropic}} | Claude Fable 5 | [Vibe Code Bench v1.1](https://www.vals.ai/benchmarks/vibe-code) | 90.35%（第 1） | accuracy | [第三方榜单](https://www.vals.ai/benchmarks/vibe-code) |
| {{lab:Google}} | Gemini 3.7 Flash | [Code Arena · WebDev](https://arena.ai/leaderboard/code/webdev) | 1588 | 引用公开榜单；3.8 Flash 的表里去掉了这一项 | [厂商引用第三方（model card）](https://deepmind.google/models/model-cards/gemini-3-7-flash/) |
| {{lab:Moonshot}} | Kimi K3 | Kimi Webdev Bench | 胜 58.6 / 平 13.8 / 负 27.6 | 对 Claude Opus 4.8，专家盲评 | [自建评测集（技术报告）](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf) |
| {{lab:Moonshot}} | Kimi K3 | [WebDev Arena](https://arena.ai/leaderboard/code/webdev) | 1678（第 1，2026-07-23） | 写入技术报告 | [厂商引用第三方](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf) |
| {{lab:Zhipu}} | GLM-5.3-Flash | Vision2Web | 77.8 | 未给评测设置 | [厂商自报](https://z.ai/blog/glm-5.3-flash) |
| {{lab:Zhipu}} | GLM-5V-Turbo | [Design2Code](https://arxiv.org/abs/2403.03163) / Flame-VLM-Code | 94.8 / 93.8 | — | [厂商自报](https://docs.z.ai/guides/vlm/glm-5v-turbo) |
| {{lab:Zhipu}} | GLM-5V-Turbo | CC-Frontend（CC-Bench-V2） | 68.4 | — | [自建评测集](https://docs.z.ai/guides/vlm/glm-5v-turbo) |
| {{lab:Qwen}} | Qwen3.8-Max | QwenReactBench / QwenSVGBench | 1724 / 1713 | 渲染后由多模态模型判分，BT/Elo | [自建评测集](https://qwen.ai/blog?id=qwen3.8) |
| {{lab:Qwen}} | Qwen3.8-Max | Vision2Web | 69.0 | 三类平均，gpt-5.4 判分 | [厂商自报](https://qwen.ai/blog?id=qwen3.8) |
| {{lab:DeepSeek}} | DeepSeek-V4-Pro-0813 | DSBench-FullStack | 71.1 | 内部全栈测试集，不专测视觉 | [自建评测集（model card）](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813) |
| {{lab:ByteDance Seed}} | Seed2.1 Pro | Trae Web Bench / Trae Artifacts | 78.4 / 51.0 | model card Table 5 | [自建评测集（model card）](https://lf3-static.bytednsdoc.com/obj/eden-cn/lapzild-tss/ljhwZthlaukjlkulzlp/seed2.1/Seed2_1_Model_Card.pdf) |
| {{lab:ByteDance Seed}} | Seed2.1 Pro | [Code Arena · Frontend](https://arena.ai/leaderboard/code) | 1539（第 8） | 发布时快照 | [厂商引用第三方（model card）](https://lf3-static.bytednsdoc.com/obj/eden-cn/lapzild-tss/ljhwZthlaukjlkulzlp/seed2.1/Seed2_1_Model_Card.pdf) |
| {{lab:ByteDance Seed}} | Seed2.0 Pro | [ArtifactsBench](https://artifactsbenchmark.github.io/leaderboard.html) | 66.6 | model card | [厂商自报](https://arxiv.org/abs/2607.00248) |
| {{lab:Tencent Hunyuan}} | Hy4 preview | — | 未报告 | 发布表无前端项；WebCraftBench 分数只出现在[团队论文](https://arxiv.org/abs/2609.15387)中 | [发布页](https://huggingface.co/tencent/Hy4-preview) |
| {{lab:MiniMax}} | MiniMax-M3 | VIBE-V2 / SVG-Bench | 50.1 / 63.7 | agent 验证交互与渲染，3 次平均 | [自建评测集](https://www.minimax.io/blog/minimax-m3) |

数据解读：

- **没有一个公开 Web benchmark 被多数厂商采用。** Vision2Web 只有 GLM 和 Qwen 在用；SWE-bench Multimodal 只有 Anthropic 在用；ArtifactsBench 在 Seed2.0、Hunyuan-A13B、MiniMax-M2 上各报过一次，之后都不再报告。
- **国内 7 家中 6 家以自建评测集为主。** 自建集的题目和判分方式各不相同，分数不能跨厂商比较，Qwen 几乎每一代都换一个自建集的名字。
- **可以横向比较的只有第三方榜单**：Code Arena · WebDev（人工偏好 Elo）和 Vibe Code Bench v1.1（agent 实测）。
- **Benchmark Timeline by Capability 总表中的学术 benchmark 基本没有被厂商采用。** WebGen-Bench、Interaction2Code 等都没有出现在厂商的发布材料里；Design2Code 只在 GLM 的视觉模型上报告过。

