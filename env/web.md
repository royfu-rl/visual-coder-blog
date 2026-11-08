<!--ANALYSIS-->
- **Input**：截图、设计稿、草图、自然语言规格说明、多轮对话、图表图像。
- **Output**：单页 HTML、多文件 Web App、绘图代码或 SVG。
- **Verifier**：
  - Reward Model：美学质量评估 / 视觉相似度（渲染结果和参考图比较）
  - Agent：Browser use agent / Computer use agent，按工作流操作页面，检查功能是否可用。
  - MLLM Checklist：用于审美和设计质量。MLLM checklist 需要先与人工评审对齐。

三个维度对应六种能力：视觉还原、交互实现、功能正确、多轮编辑、审美对齐、图表与矢量精度。

<!--LANDSCAPE-->

<!--EVOLUTION-->
核心发现：评测对象从「输出是否与参考图一致」转向「输出是否可用」。

- **2023 年至 2024 年上半年：截图转代码成为标准任务。** Design2Code 使用 484 个真实网页，按渲染相似度打分。WebCode2M 和 Web2Code 把数据规模扩大到百万级。图表方向的 ChartMimic、Plot2Code 使用同样的评测方法。StarVector 的 SVG-Bench 指出，像素指标无法衡量 SVG 质量。
- **2024 年下半年：评测加入交互。** Sketch2Code 加入多轮用户反馈。Interaction2Code 专门测试交互行为，交互部分的得分低于整页生成。WebDev Arena 由真人试用后投票，平局率为 26%。
- **2025 年：由 agent 执行测试成为主流。** WebGen-Bench 用 UI agent 执行 647 个测试用例，最好的组合为 27.8%。ArtifactsBench 由 MLLM 按逐题 checklist 打分，与 WebDev Arena 排名的一致性为 94.4%。图表方向转向编辑任务，ChartEdit 的最高分为 59.96。
- **2026 年上半年：评测端到端交付和多轮编辑。** Vibe Code Bench 要求从规格说明构建并部署应用。论文中最好的模型为 61.8%，接入外部服务后从 71% 降到 30%；v1.1 榜单上 Claude Fable 5 为 90.35%。FronTalk 发现模型在多轮对话中会覆盖已经实现的功能。Figma2Code 发现闭源模型的视觉还原度高，但响应式布局和代码可维护性差。
- **2026 年中：评测长页面和多页状态。** LongWebBench 显示页面越长，结构保真度越低。UI2App 中一半模型在跨页状态上得 0 分。

结论：单页截图转代码已接近饱和，新的 benchmark 集中在交互、多轮编辑和端到端交付上。

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
<table class="frontier"><thead><tr><th>Benchmark</th><th>模型</th><th>分数</th><th>来源</th></tr></thead><tbody><tr><td class="bench" rowspan="5"><a href="https://arena.ai/leaderboard/code/webdev">Code Arena · WebDev</a></td><td>{{lab:OpenAI}} GPT-6 Astra</td><td>1793（1st）</td><td><a href="https://arena.ai/leaderboard/code/webdev">Benchmark</a></td></tr><tr><td>{{lab:Anthropic}} Claude Opus 5</td><td>1691（3rd）</td><td><a href="https://arena.ai/leaderboard/code/webdev">Benchmark</a></td></tr><tr><td>{{lab:Google}} Gemini 3.7 Flash</td><td>1588</td><td><a href="https://deepmind.google/models/model-cards/gemini-3-7-flash/">Blog</a></td></tr><tr><td>{{lab:Moonshot}} Kimi K3</td><td>1678（1st，2026-07-23）</td><td><a href="https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf">Blog</a></td></tr><tr><td>{{lab:ByteDance Seed}} Seed2.1 Pro</td><td>1539（8th）</td><td><a href="https://lf3-static.bytednsdoc.com/obj/eden-cn/lapzild-tss/ljhwZthlaukjlkulzlp/seed2.1/Seed2_1_Model_Card.pdf">Blog</a></td></tr><tr><td class="bench" rowspan="2"><a href="https://www.vals.ai/benchmarks/vibe-code">Vibe Code Bench v1.1</a></td><td>{{lab:OpenAI}} GPT-6 Astra</td><td>89.59%</td><td><a href="https://www.vals.ai/benchmarks/vibe-code">Benchmark</a></td></tr><tr><td>{{lab:Anthropic}} Claude Fable 5</td><td>90.35%（1st）</td><td><a href="https://www.vals.ai/benchmarks/vibe-code">Benchmark</a></td></tr><tr><td class="bench" rowspan="2"><a href="https://arxiv.org/abs/2603.26648">Vision2Web</a></td><td>{{lab:Zhipu}} GLM-5.3-Flash</td><td>77.8</td><td><a href="https://z.ai/blog/glm-5.3-flash">Blog</a></td></tr><tr><td>{{lab:Qwen}} Qwen3.8-Max</td><td>69.0</td><td><a href="https://qwen.ai/blog?id=qwen3.8">Blog</a></td></tr><tr><td class="bench" rowspan="1"><a href="https://arxiv.org/abs/2410.03859">SWE-bench Multimodal</a></td><td>{{lab:Anthropic}} Claude Opus 5</td><td>59.4%</td><td><a href="https://www.anthropic.com/claude-opus-5-system-card">Blog</a></td></tr><tr><td class="bench" rowspan="1"><a href="https://arxiv.org/abs/2403.03163">Design2Code</a> / Flame-VLM-Code</td><td>{{lab:Zhipu}} GLM-5V-Turbo</td><td>94.8 / 93.8</td><td><a href="https://docs.z.ai/guides/vlm/glm-5v-turbo">Blog</a></td></tr><tr><td class="bench" rowspan="1"><a href="https://artifactsbenchmark.github.io/leaderboard.html">ArtifactsBench</a></td><td>{{lab:ByteDance Seed}} Seed2.0 Pro</td><td>66.6</td><td><a href="https://arxiv.org/abs/2607.00248">Blog</a></td></tr><tr><td class="bench" rowspan="1">Internal Design Tasks<span class="self-tag">自建</span></td><td>{{lab:OpenAI}} GPT-6 Astra</td><td>50.0%</td><td><a href="https://openai.com/index/gpt-6-astra/">Blog</a></td></tr><tr><td class="bench" rowspan="1">Kimi Webdev Bench<span class="self-tag">自建</span></td><td>{{lab:Moonshot}} Kimi K3</td><td>胜 58.6 / 平 13.8 / 负 27.6</td><td><a href="https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf">Blog</a></td></tr><tr><td class="bench" rowspan="1">CC-Frontend（CC-Bench-V2）<span class="self-tag">自建</span></td><td>{{lab:Zhipu}} GLM-5V-Turbo</td><td>68.4</td><td><a href="https://docs.z.ai/guides/vlm/glm-5v-turbo">Blog</a></td></tr><tr><td class="bench" rowspan="1">QwenReactBench / QwenSVGBench<span class="self-tag">自建</span></td><td>{{lab:Qwen}} Qwen3.8-Max</td><td>1724 / 1713</td><td><a href="https://qwen.ai/blog?id=qwen3.8">Blog</a></td></tr><tr><td class="bench" rowspan="1">Trae Web Bench / Trae Artifacts<span class="self-tag">自建</span></td><td>{{lab:ByteDance Seed}} Seed2.1 Pro</td><td>78.4 / 51.0</td><td><a href="https://lf3-static.bytednsdoc.com/obj/eden-cn/lapzild-tss/ljhwZthlaukjlkulzlp/seed2.1/Seed2_1_Model_Card.pdf">Blog</a></td></tr><tr><td class="bench" rowspan="1">VIBE-V2 / SVG-Bench<span class="self-tag">自建</span></td><td>{{lab:MiniMax}} MiniMax-M3</td><td>50.1 / 63.7</td><td><a href="https://www.minimax.io/blog/minimax-m3">Blog</a></td></tr><tr><td class="bench" rowspan="2">未报告相关分数</td><td>{{lab:DeepSeek}} DeepSeek-V4.1-Flash</td><td>未报告</td><td><a href="https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash">Blog</a></td></tr><tr><td>{{lab:Tencent Hunyuan}} Hy4 preview</td><td>未报告</td><td><a href="https://huggingface.co/tencent/Hy4-preview">Blog</a></td></tr></tbody></table>


