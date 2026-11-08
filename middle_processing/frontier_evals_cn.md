# 国内前沿模型发布时报告的视觉 coding benchmark

- 调研日期：2026-09-24
- 范围：前端 / Web、3D / Blender / CAD、游戏；computer-use / GUI 只作参考，标「参考」
- 来源类型
  - **厂商自报**：公开 benchmark，厂商自己跑的分
  - **自建评测集**：厂商自建、自评的评测集
  - **第三方榜单**：arena.ai（原 LMArena）Code Arena / WebDev 等
  - **仅 demo**：只有案例展示，没有分数
- 硬规则：原文里找不到的一律写「未报告」。凡注明「读图」的分数，都是从发布页的图表图片里转录的
- 第三方「实时榜」指 2026-09-23/24 抓取的 https://arena.ai/leaderboard/code/webdev 页面。分数会漂移，所以和发布时的推文数字不同

---

## 1. Moonshot · Kimi

### Kimi K3（2026-07-16）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| Kimi Webdev Bench · Overall | 前端 | Win 58.6 / Tie 13.8 / Lose 27.6（+31.0） | K3(max) 对 Claude Opus 4.8(max)，两边都用 Claude Code harness；专家盲评，看代码质量、功能完整、视觉还原、交互；技术报告 Table 4 | 自建评测集 | https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf |
| Kimi Webdev Bench · Games | 游戏 | 55.6 / 3.7 / 40.7（+14.9） | 同上 | 自建评测集 | 同上 |
| Kimi Webdev Bench · 3D / WebGL / Shader | 3D | 72.7 / 13.7 / 13.6（+59.1） | 同上 | 自建评测集 | 同上 |
| Kimi Webdev Bench · Website / UI Clone | 前端 | 52.6 / 21.1 / 26.3（+26.3） | 同上 | 自建评测集 | 同上 |
| WebDev Arena | 前端 | Elo 1,678，#1/99 | 截至 2026-07-23；报告 Table 5，原文标注 "independent third-party evaluations" | 第三方榜单（厂商报告引用） | 同上 |
| OSWorld-Verified / OSWorld 2.0 | GUI（参考） | 84.8 / 58.3 | max effort | 厂商自报 | https://huggingface.co/moonshotai/Kimi-K3 |
| Game Dev & Digital Creation（图片/视频 → 可玩游戏）、CAD、芯片设计 | 游戏 / CAD | — | — | 仅 demo | https://www.kimi.com/blog/kimi-k3 |
| Design2Code / ArtifactsBench / SWE-bench MM / 3D 或 CAD 公开 bench | — | 未报告 | — | — | — |

### Kimi K2.7 Code（2026-06）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| 任何视觉 / 前端 benchmark | — | 未报告 | 模型卡里只有 Kimi Code Bench v2、Program Bench 等 | — | https://huggingface.co/moonshotai/Kimi-K2.7-Code |

### Kimi K2.6（2026-04-20）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| Kimi Design Bench | 前端 / 设计 | Kimi 胜 47.5 / 平 21.1 / Google 胜 31.4 | 对手 Gemini 3.1 Pro；4 类任务：Visual Input、Landing Page、Full-Stack App、General Creative Programming；读图 | 自建评测集 | https://www.kimi.com/blog/kimi-k2-6 |
| OSWorld-Verified | GUI（参考） | 73.1 | thinking | 厂商自报 | https://huggingface.co/moonshotai/Kimi-K2.6 |
| Coding-Driven Design（落地页、全栈） | 前端 | — | — | 仅 demo | https://www.kimi.com/blog/kimi-k2-6 |

### Kimi K2.5（2026-01-27）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| Visual-to-code（图像 / 视频 → 代码） | 前端 | 无数字，只写了 SOTA "in our internal evaluations" | — | 自建评测集（未公开数据） | https://arxiv.org/abs/2602.02276 |
| OSWorld-Verified / WebArena | GUI / Web agent（参考） | 63.3 / 58.9 | — | 厂商自报 | 同上 |
| 一句话生成前端、看视频重建网站、带视觉调试的前端 | 前端 | — | — | 仅 demo | https://www.kimi.com/blog/kimi-k2-5.html |

### Kimi K2 / K2-0905 / K2 Thinking（2025-07 至 2025-11）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| 任何视觉 / 前端 benchmark | — | 未报告 | 0905 版只定性提到 "Improved frontend coding experience" | — | https://huggingface.co/moonshotai/Kimi-K2-Instruct-0905 |
| 交互网页、JS 版 Minecraft（K2） | 前端 / 游戏 | — | — | 仅 demo | https://www.kimi.com/blog/kimi-k2 |
| 单 prompt 生成 HTML/React（K2 Thinking） | 前端 | — | — | 仅 demo | https://www.kimi.com/blog/kimi-k2-thinking |

**第三方（Kimi）**
| 模型 | 榜单 | 分数 | 出处 |
|---|---|---|---|
| K3 | Frontend Code Arena | 1679，#1（只在搜索摘要里看到，推文页打不开） | https://x.com/arena/status/2077824029126504525 |
| K2.6 | Code Arena WebDev | Elo 1,529，#6/67（2026-04-26，The Batch 转述） | https://www.deeplearning.ai/the-batch/kimi-k2-6-matches-open-qwen3-6-max-anddeepseek-v4-falls-just-behind-top-closed-models |
| K2.5-thinking | Code Arena WebDev | 已上榜，没找到分数 | https://arena.ai/blog/leaderboard-changelog |

---

## 2. 智谱 · GLM

### GLM-5.3（2026-08-14，最新旗舰）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| Z.ai Code Bench v1.0 | 通用 agentic coding（不专门考前端） | Max 34.5% / High 31.4% | Claude Code 2.1.207 | 自建评测集 | https://z.ai/blog/glm-5.3 |
| 前端 / 视觉 / 3D / 游戏类 | — | 未报告 | — | — | https://huggingface.co/zai-org/GLM-5.3 |

### GLM-5.3-Flash（2026-08-26，原生多模态）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| Vision2Web | 视觉转网页 | 77.8 | 放在博客表格的 Vision 组；没有评测设置脚注 | 厂商自报 | https://z.ai/blog/glm-5.3-flash |
| OSWorld 2.0 | GUI（参考） | 59.1 | — | 厂商自报 | 同上 |
| 截图 / URL 复刻 Next.js、Blender 3D 场景、Godot 游戏、build123d CAD | 前端 / 3D / 游戏 / CAD | — | — | 仅 demo | https://docs.z.ai/guides/vlm/glm-5.3-flash |

### GLM-5.2（2026-06-16）/ GLM-5.1（2026-04-07）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| 前端 / 视觉类 | — | 未报告 | — | — | https://z.ai/blog/glm-5.2 |
| 8 小时自主构建网页版 Linux 桌面（5.1） | 前端 | — | — | 仅 demo | https://z.ai/blog/glm-5.1 |

### GLM-5V-Turbo（API 模型）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| Design2Code | 设计稿转代码 | 94.8 | 文档图表 | 厂商自报 | https://docs.z.ai/guides/vlm/glm-5v-turbo |
| Flame-VLM-Code | 视觉转 React | 93.8 | 同上 | 厂商自报 | 同上 |
| Vision2Web | 视觉转网页 | 31.0 | 和 5.3-Flash 的 77.8 差距很大，文档没说两处设置是否一致 | 厂商自报 | 同上 |
| CC-Frontend（CC-Bench-V2） | 前端 | 68.4 | — | 自建评测集 | 同上 |
| OSWorld / AndroidWorld / WebVoyager | GUI（参考） | 62.3 / 75.7 / 88.5 | — | 厂商自报 | 同上 |

### GLM-5（2026-02-12）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| CC-Bench-V2 前端（博客） | 前端 | Build Success 98.0% / E2E Correctness 74.8% | 构建后由 Agent-as-a-Judge 判 | 自建评测集 | https://z.ai/blog/glm-5 |
| CC-Bench-V2 前端（论文 Table 8，220 题，含 Web Games、SVG/Canvas） | 前端 / 游戏 | HTML ISR 38.9 / CSR 76.3；React 34.6 / 71.0；Vue 32.7 / 77.1 | 评审 = Claude Code + Sonnet 4.5 + Playwright；逐项与人工一致 94% | 自建评测集 | https://arxiv.org/abs/2602.15763 |
| 幻灯片生成人评（对 GLM-4.5） | 视觉设计 | 总胜率 67.5% | 人评 | 自建评测集 | 同上 |
| Code Arena / Agentic WebDev | 前端 | 1449（±16），总榜 #6，开源 #1 | 报告 Figure 3 贴的截图 | 第三方榜单（厂商引用） | 同上 |

### GLM-4.7（2025-12-22）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| LMArena WebDev | 前端 | 1449（Preliminary），总榜 #6，开源 #1 | 厂商文档贴的截图 | 第三方榜单（厂商引用） | https://docs.z.ai/guides/llm/glm-4.7 |
| Three.js、体素宝塔、3D 粒子星系、3D 魔方、海报、幻灯片 | 前端 / 3D | — | — | 仅 demo | https://z.ai/blog/glm-4.7 |

### GLM-4.6（2025-09-30）/ GLM-4.5（2025-07-28）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| CC-Bench-V1.1（4.6，含前端） | agentic coding 人评对战 | 对 Claude Sonnet 4：胜 48.6 / 平 9.5 / 负 41.9 | Docker 环境，多轮人机协作 | 自建评测集 | https://z.ai/blog/glm-4.6 |
| CC-Bench（4.5，52 题，含前端） | agentic coding 人评对战 | 对 Claude 4 Sonnet：胜 40.4 / 平 9.6 / 负 50.0 | Claude Code 环境；没有前端单项分 | 自建评测集 | https://z.ai/blog/glm-4.5 ；https://arxiv.org/abs/2508.06471 |
| Flappy Bird、3D 第一人称迷宫、SVG 动画、全栈建站（4.5） | 游戏 / 3D / 前端 | — | — | 仅 demo | https://z.ai/blog/glm-4.5 |

### GLM-4.6V（2025-12-08）/ GLM-4.5V（2025-08-11）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| Design2Code | 设计稿转代码 | 4.6V：88.6（4.6V-Flash：69.8）；4.5V：82.2 | o4-mini 做视觉判分，相似度 ≥80 算通过 | 厂商自报 | https://huggingface.co/zai-org/GLM-4.6V ；https://arxiv.org/abs/2507.01006 |
| Flame-React-Eval | 视觉转 React | 4.6V：86.3；4.5V：82.5 | 同上 | 厂商自报 | 同上 |
| OSWorld / AndroidWorld / WebVoyager | GUI（参考） | 4.6V：37.2 / 57.0 / 81.0；4.5V：35.8 / 57.0 / 84.4 | — | 厂商自报 | 同上 |

**第三方（GLM，实时榜 2026-09-23）**
| 模型 | 名次 | 分数 |
|---|---|---|
| glm-5.3-max | #15 | 1619.2 |
| glm-5.3-flash | #19 | 1611.2 |
| glm-5.2-max | #20 | 1599.3 |
| glm-5.1 | #45 | 1508.2 |
| glm-5 | #67 | 1435.8 |
| glm-4.7 | #68 | 1434.7 |
| glm-5v-turbo | #77 | 1400.6 |
| glm-4.6 | #102 | 1340.6 |

出处：https://arena.ai/leaderboard/code

---

## 3. 阿里 · Qwen

### Qwen3.8-Max（2026-08-03，最新旗舰）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| QwenReactBench | 前端 / React | 1724 | Claude Code 构建 React 项目；中英双语，7 类；渲染后多模态模型判分；BT/Elo | 自建评测集 | https://qwen.ai/blog?id=qwen3.8 |
| QwenSVGBench | SVG | 1713 | 渲染后多模态判分；BT/Elo | 自建评测集 | 同上 |
| Vision2Web | 视觉网页开发 | 69.0 | 取 frontend / webpage / website 三类平均；Claude Code harness；gpt-5.4 判分 | 厂商自报 | 同上 |
| QwenBlenderBench | 3D / Blender | 69.9 | 原文只说 "internal benchmark" | 自建评测集 | 同上 |
| Parametric CAD Bench | CAD | 91.5 | 原文没写口径 | 厂商自报（无法判断是否自建） | 同上 |
| RecreationBench | 应用复刻（5 个平台，含 Web） | 51.7 | 内部长程 benchmark：把运行中的应用当黑盒观察，然后从零重建 | 自建评测集 | 同上 |
| PresentBench | 幻灯片 | 79.6 | 原文没写口径 | 厂商自报 | 同上 |
| WebArena-Verified | Web agent（参考） | 66.8 | 官方 grader，跑在 OSWorld scaffold 里 | 厂商自报 | 同上 |
| OSWorld-Verified / ScreenSpot Pro / AndroidWorld | GUI（参考） | 86.1 / 84.5 / 85.3 | — | 厂商自报 | 同上 |
| 截图重建前端、户型图 → Blender 3D、一句话生成游戏、2D 表 → 3D 演示 | 前端 / 3D / 游戏 | — | — | 仅 demo | 同上 |
| WebDev Arena / Design2Code / ArtifactsBench / SWE-bench MM | — | 未报告 | — | — | — |

### Qwen3.8-Max-0902（后训练更新）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| 视觉 / 前端 / 3D 类 | — | 未报告 | 发布长图里只有 Coding / Agent / Multimodal 三块，没有这类 benchmark | — | https://x.com/Alibaba_Qwen/status/2094968708288680276 |

### Qwen3.8-27B / 3.8-Flash-Next / 3.8-Omni-Flash
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| SWE-bench Multimodal（27B） | 多模态 SWE | 38.6 | 公开 dev split；Claude Code harness | 厂商自报 | https://huggingface.co/Qwen/Qwen3.8-27B |
| Vision2Web（27B / Flash-Next / Omni-Flash） | 视觉网页 | 62.9 / 64.0 / 62.9 | 与 3.8-Max 同口径 | 厂商自报 | 同上；https://qwen.ai/blog?id=qwen3.8-flash-next ；https://qwen.ai/blog?id=qwen3.8-omni-flash |
| RecreationBench（27B / Flash-Next） | 应用复刻 | 47.1 / 49.9 | — | 自建评测集 | 同上 |
| Audio-Visual Vibe Coding：Snake Game（Omni-Flash） | 游戏 | — | — | 仅 demo | https://qwen.ai/blog?id=qwen3.8-omni-flash |

### Qwen3.7-Max / Qwen3.7-Plus（2026-05 / 06）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| QwenWebDev | 前端 | Max 1568 / Plus 1536 | 中英双语，7 类；渲染后多模态判分；BT/Elo | 自建评测集 | https://qwen.ai/blog?id=qwen3.7 |
| QwenSVG | SVG | Max 1608 / Plus 1588 | Elo | 自建评测集 | 同上 |
| QwenVision2Code（Plus） | 图像 / 视频 → 代码 | 1772.0 | 没有口径脚注 | 自建评测集 | https://qwen.ai/blog?id=qwen3.7-plus |
| ScreenSpot Pro / OSWorld-Verified（Plus） | GUI（参考） | 79.0 / 73.3 | — | 厂商自报 | 同上 |
| Three.js 手势粒子、3D 赛车游戏、WebGL instancing（Max） | 3D / 游戏 | — | — | 仅 demo | https://qwen.ai/blog?id=qwen3.7 |

### Qwen3.6 系列（2026-04）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| QwenWebBench | 前端（7 类：Web Design / Web Apps / Games / SVG / Data Vis / Animation / 3D） | Plus 1501.7；Max-Preview 1532；27B 1487；35B-A3B 1397 | BT/Elo。Plus 的分数在 Max-Preview 图里写成 1495，两处不一致 | 自建评测集 | https://qwen.ai/blog?id=qwen3.6 ；https://qwen.ai/blog?id=qwen3.6-max-preview |
| ScreenSpot Pro / OSWorld-Verified（Plus） | GUI（参考） | 68.2 / 62.5 | — | 厂商自报 | https://qwen.ai/blog?id=qwen3.6 |
| 3D 水族箱、塞尔达风雪山 3D、第一人称飞行游戏、UI 截图转前端 | 3D / 游戏 / 前端 | — | — | 仅 demo | 同上 |

### Qwen3.5（2026-02-16）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| FullStackBench en / zh | 全栈 | 27B：60.1 / 57.4；122B：62.6 / 58.7 | — | 厂商自报 | https://huggingface.co/Qwen/Qwen3.5-27B |
| ScreenSpot Pro / OSWorld-Verified（397B） | GUI（参考） | 65.6 / 62.2 | — | 厂商自报 | https://qwen.ai/blog?id=qwen3.5 |
| 赛车游戏、视频转游戏 HTML、手绘草图转前端 | 游戏 / 前端 | — | — | 仅 demo | 同上 |

### Qwen3-VL-235B-A22B（2025）
| Benchmark | 类别 | 分数（Thinking / Instruct） | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| Design2Code | 截图 → HTML | 93.4 / 92.0 | 技术报告 Table 2 | 厂商自报 | https://arxiv.org/abs/2511.21631 |
| ChartMimic | 图表 → 代码 | 78.4 / 80.5 | 同上 | 厂商自报 | 同上 |
| UniSVG | SVG | 65.8 / 69.8 | 同上 | 厂商自报 | 同上 |
| ScreenSpot Pro / OSWorld | GUI（参考） | 61.8 / 62.0；38.1 / 31.6 | 同上 | 厂商自报 | 同上 |

### Qwen-Coder
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| FullStackBench en / zh（Coder-Next） | 全栈 | 60.58 / 57.38 | 技术报告 Table 7；报告自己承认 "frontend and UI-related capability remains an area for improvement" | 厂商自报 | https://github.com/QwenLM/Qwen3-Coder/blob/main/qwen3_coder_next_tech_report.pdf |
| WebArena / Mind2Web（Coder-480B） | Web agent（参考） | 49.9 / 55.8 | 博客主图 | 厂商自报 | https://qwen.ai/blog?id=qwen3-coder |
| 物理模拟、太阳系、DUET 游戏、植物大战僵尸类网页游戏 | 游戏 / 前端 | — | — | 仅 demo | 同上；https://qwen.ai/blog?id=qwen3-coder-next |

**第三方（Qwen）**
| 模型 | 发布时 | 实时榜（09-24） | 出处 |
|---|---|---|---|
| qwen3.8-max | #4，1,668 | #5，1671 ±12 | https://x.com/arena/status/2084108703729615026 |
| qwen3.8-max-0902 | #1，1691 | #7，1660 ±9 | https://x.com/arena/status/2094974637704913198 |
| qwen3.8-flash-next | 约 #8，1617（AutoEval） | #10，1636 | https://x.com/arena/status/2092634189048971440 |
| qwen3.8-27b | #9，1595 | #22，1591 | https://x.com/arena/status/2091920512796725272 |
| qwen3.7-max | — | #41，1517 | https://arena.ai/leaderboard/code/webdev |
| qwen3.6-plus / 3.6-max-preview | — | #57，1460 / #51，1479 | 同上 |
| qwen3.5-397b-a17b | — | #78，1399 | 同上 |
| qwen3-coder-480b | — | #112，1274 | 同上 |

---

## 4. DeepSeek

### DeepSeek-V4.1-Flash（2026-09-10，原生多模态）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| 前端开发 | 前端 | 无分数，只在技术报告里定性说明它能 "utilize rendered screen captures for visual inspection and self-correction" | — | 厂商自报（定性） | https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash |
| 视觉 coding benchmark | — | 未报告（只有 Chartography、BabyVision、ZeroBench 这类理解题） | — | — | 同上 |

### DeepSeek-V4-Pro-0813 / V4-Flash-0731（正式版）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| DSBench-FullStack | 全栈（不专考视觉） | Pro-0813 71.1 / Flash-0731 68.7 | "internal full-stack development test set"；DeepSeek Harness，max effort | 自建评测集 | https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813 ；https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731 |
| 其余视觉 / 前端 / 3D / 游戏 | — | 未报告 | — | — | 同上 |

### DeepSeek-V4-Flash-Vision-Exp（2026-08-21）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| 前端 / 设计 benchmark | — | 未报告 | — | — | https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp |
| 西藏自驾 PPT、重构 DeepSeek Harness 官网、黏土怪物动效前端 Mini Demo | PPT / 前端 | — | — | 仅 demo | https://api-docs.deepseek.com/zh-cn/news/news260821 |

### DeepSeek-V4-Pro / Flash preview（2026-04-24）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| WebDev Arena / Design2Code / ArtifactsBench / SWE-bench MM / 3D / 游戏 / OSWorld | — | 未报告 | 模型卡和 58 页报告都已检索 | — | https://arxiv.org/abs/2606.19348 |
| White-Collar Task · Formatting Aesthetics | 办公产物视觉（非前端） | V4-Pro-Max 76.68 | 30 个中文专业任务，人工盲评；报告 §5.4.3 | 自建评测集 | 同上 |
| Agent 框架下生成的 PPT 内页 | PPT | — | — | 仅 demo | https://api-docs.deepseek.com/zh-cn/news/news260424 |

### DeepSeek-V3.1 / V3.2（2025）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| 所有目标类别 | — | 未报告 | — | — | https://huggingface.co/deepseek-ai/DeepSeek-V3.2 ；https://huggingface.co/deepseek-ai/DeepSeek-V3.1 |

**第三方（DeepSeek，均来自 Arena 官方推文）**
| 模型 | 榜单 | 分数 | 出处 |
|---|---|---|---|
| V4.1-Flash | Code Arena WebDev | 1620，约 #14（early AutoEval） | https://x.com/arena/status/2098088993367949337 |
| V4-Pro-0813 (Max) | Code Arena WebDev | 1607，约 #8（early AutoEval） | https://x.com/arena/status/2087767198974533648 |
| V4-Flash-High | Frontend Code Arena | 1,586，#7；分类排名：Gaming #6、Reference-based Design #6 | https://x.com/arena/status/2083351033993142605 |
| V4 Pro preview (thinking) | Code Arena | #14 overall、开源 #3，只有排名没有分数 | https://x.com/arena/status/2047518354903359697 |
| V3.1 / V3.2 | WebDev / Code Arena | 已上榜，没找到分数 | https://arena.ai/company/leaderboard-changelog |

---

## 5. 字节 · Seed

### Seed2.1 Pro / Turbo（2026-06；0915 更新）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| Trae / Web Bench | 前端 | Pro 78.4 / Turbo 73.6 | Model card Table 5 | 自建评测集 | https://lf3-static.bytednsdoc.com/obj/eden-cn/lapzild-tss/ljhwZthlaukjlkulzlp/seed2.1/Seed2_1_Model_Card.pdf |
| Trae / Artifacts | 前端 artifact（React + Tailwind） | Pro 51.0 / Turbo 47.0 | 同上 | 自建评测集 | 同上 |
| Code Arena: Frontend | 前端 | Pro #8，1539 | Model card Figure 9，发布时的快照 | 第三方榜单（厂商引用） | 同上 |
| CreativeWork（Notion / Canva / Figma） | GUI + 设计操作 | Pro 42.5 / Turbo 34.5 | Table 4 | 自建评测集 | 同上 |
| GameWorld | 玩浏览器游戏（不是生成游戏） | Pro 31.2 / Turbo 25.9 | Table 4 | 厂商自报 | 同上 |
| OSWorld / MobileWorld | GUI（参考） | Pro 78.8 / 73.1 | Table 4 | 厂商自报 | 同上 |
| 户型图 / 设计稿 / 视频 → 前端，草图 → 网页，WebGL 流体 | 前端 | — | — | 仅 demo | https://seed.bytedance.com/en/seed2_1 |
| 0915：4 张设计图 → 3D 四季庭院，"Web3D 开发和游戏场景呈现" | 3D / 游戏 | — | 媒体转述火山引擎的说法，没找到官方分数 | 仅 demo | https://ai.codefather.cn/news/2100251252460953605 |

### Seed2.0 Pro / Lite（2026-02；Lite 0428）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| ArtifactsBench | 前端 / 可视交互 | Pro 66.6 / Lite 62.6 | Model card Table 11/12 | 厂商自报 | https://arxiv.org/abs/2607.00248 |
| Vibe Coding 人工评估 | vibe coding | Lite(0428) 49.4% / Pro(0215) 48.4% | 人评 | 自建评测集 | https://seed.bytedance.com/en/seed2 |
| OSWorld-Verified | GUI（参考） | Lite(0428) 64.4% | — | 厂商自报 | 同上 |
| 图 → 代码网页（3D tilt）、matplotlib 3D、FreeCAD 操作 | 前端 / 3D / CAD | — | — | 仅 demo | https://arxiv.org/abs/2607.00248 |

### Doubao-Seed-Code（2025-11）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| 视觉 / 前端 benchmark | — | 未报告 | — | — | https://developer.volcengine.com/articles/7577301460712030258 |
| UI 设计稿 / 截图 / 手绘 → 代码，视觉比对后修样式 | 前端 | — | — | 仅 demo | 同上 |

### Seed1.8（2025-12）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| U-Artifacts | 前端 artifact | 49.2 | 199 例，13 个主题；GUI agent 模拟用户来判分；Table 4 | 自建评测集 | https://arxiv.org/abs/2603.20633 |
| ScreenSpot-Pro / OSWorld | GUI（参考） | 64.3（crop 工具 73.1）/ 61.9 | — | 厂商自报 | 同上 |

### Seed1.6 / Seed1.5-VL（2025）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| 前端 / 视觉 coding（Seed1.6） | — | 未报告 | — | — | https://seed.bytedance.com/en/blog/introduction-to-techniques-used-in-seed1-6 |
| 14 款 Poki 游戏（1.5-VL） | 玩游戏（不是生成游戏） | 例：2048 870.6 | Table 9 | 自建评测集 | https://arxiv.org/abs/2505.07062 |
| ScreenSpot-Pro / OSWorld（1.5-VL） | GUI（参考） | 60.9 / 36.7 | Table 8 | 厂商自报 | 同上 |

**第三方（Seed）**
| 模型 | 榜单 | 分数 | 出处 |
|---|---|---|---|
| seed-2.1-pro-preview | arena.ai WebDev 实时榜 | #39/131，1518.89 | https://arena.ai/leaderboard/code/webdev |

---

## 6. 腾讯 · 混元（Hy）

结论先说：**在混元自家的模型发布表里，ArtifactsBench 只出现过一次，就是 Hunyuan-A13B。** 后来的 Hy3 / Hy4 不再报它，改用新的自建集 WebCraftBench 和内部评测。

### Hy4 preview（2026-08-27，最新旗舰，770B-A49B）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| 发布表中的视觉 / 前端类 | — | 未报告 | — | — | https://huggingface.co/tencent/Hy4-preview |
| "front-end visual taste"、游戏开发（单 prompt → 可玩原型） | 前端 / 游戏 | — | 只有文字描述 | 仅 demo | 同上 |
| WebCraftBench | 前端 Web 应用生成 | Total +0.911，5/17 | 在 17 个模型内做 z-score；Claude Code harness；Claude-Opus-4.8 判分 | 自建评测集（混元团队的论文，不是发布材料） | https://arxiv.org/abs/2609.15387 |

### Hy3（2026-07）/ Hy3 preview（2026-04）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| 专家盲测（270 人） | 综合，原文说 "advantage most substantial in frontend development" | 2.67/4 | 不是前端单项分 | 自建评测集（人评） | https://huggingface.co/tencent/Hy3 |
| Hy-Vibe Bench | vibe coding（原文没说是否涉及视觉） | Hy3 preview 50.5 | 读图 | 自建评测集 | https://huggingface.co/tencent/Hy3-preview |
| WebCraftBench | 前端 | Hy3 Total −0.592，12/17 | 同 Hy4 | 自建评测集 | https://arxiv.org/abs/2609.15387 |
| WorkBuddy Bench · Web 子集（70 题） | 前端 / GUI | HY-3 67.71（CodeBuddy Code）/ 66.43（Claude Code） | 3 次平均 | 自建评测集（腾讯优图 / WorkBuddy 团队的论文） | https://arxiv.org/abs/2607.20911 |

### Hunyuan-A13B（2025-06）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| ArtifactsBench | 前端 / SVG / 小游戏 | 43 | 技术报告 Table 3，慢思考模式 | 厂商自报 + 自建评测集 | https://huggingface.co/tencent/Hunyuan-A13B-Instruct |
| FullStackBench | 全栈 | 慢思考 67.8 / 快思考 58.3 | 技术报告 | 厂商自报 | https://github.com/Tencent-Hunyuan/Hunyuan-A13B/blob/main/report/Hunyuan_A13B_Technical_Report.pdf |

### HY 2.0 / Hunyuan-T1 / TurboS / Hunyuan-Large
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| 视觉 / 前端类（发布材料） | — | 未报告 | TurboS 报的是 Chatbot Arena overall 1356，不是 WebDev | — | https://arxiv.org/abs/2505.15431 ；https://www.ithome.com/0/902/856.htm |

### ArtifactsBench 官方榜上的混元（自建评测集）
| 模型 | 分数 | 口径 | 出处 |
|---|---|---|---|
| Hunyuan-Turbos-Preview | 50.97（GAME 51.61 / SVG 51.37 / WEB 52.31） | v1.0，Gemini-2.5-Pro 判分 | https://github.com/Tencent-Hunyuan/ArtifactsBenchmark |
| Hunyuan-A13B | 42.95（v1.0）/ 40.95（v1.1） | 同上 | https://artifactsbenchmark.github.io/leaderboard.html |

**第三方（混元，都是腾讯论文引用的，不是直接从榜单读到的）**
| 模型 | 榜单 | 分数 | 出处 |
|---|---|---|---|
| Hy4 preview | Code Arena | 1641，#11 | https://arxiv.org/abs/2609.15387 （Fig. 1，没写快照日期） |
| Hy3 | Code Arena | 1515，#39 | 同上 |

---

## 7. MiniMax

### MiniMax-M3（2026-06-01，最新）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| VIBE-V2 | 前端 / 全栈（Web / Android / iOS） | 50.1 | Claude Code 脚手架；Agent-as-a-Verifier 验交互和视觉；3 次平均；读图 | 自建评测集 | https://huggingface.co/MiniMaxAI/MiniMax-M3 ；https://www.minimax.io/blog/minimax-m3 |
| SVG-Bench | SVG 生成 / 编辑 | 63.7 | VLM 验渲染结果；3 次平均 | 自建评测集 | 同上 |
| OSWorld-Verified | GUI（参考） | 75.2 | 361 个样本 | 厂商自报 | 同上 |

### MiniMax-M2.7（2026-03）/ M2.5（2026-02）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| VIBE-Pro | repo 级 Web / Android / iOS / Simulation | M2.7：55.6%；M2.5：54.2（Web 36.9 / Sim 81.4 / Android 50.6 / iOS 47.9） | Claude Code 脚手架，3 次平均；M2.5 的分数读图 | 自建评测集 | https://www.minimax.io/news/minimax-m27-en ；https://huggingface.co/MiniMaxAI/MiniMax-M2.5 |
| OpenRoom 等 Web GUI demo（M2.7） | 前端 | — | — | 仅 demo | https://www.minimax.io/news/minimax-m27-en |

### MiniMax-M2.1（2025-12）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| VIBE（Visual & Interactive Benchmark for Execution in Application Development） | Web / 仿真 / App 从零构建 | Avg 88.6（Web 91.5 / Sim 87.1 / Android 89.7 / iOS 88.0 / Backend 86.7） | Agent-as-a-Verifier，3 次平均；开源 200 题 | 自建评测集 | https://huggingface.co/MiniMaxAI/MiniMax-M2.1 ；https://huggingface.co/datasets/MiniMaxAI/VIBE |
| 3D 圣诞树（R3F）、Three.js 乐高沙盒、等距 SVG 岛屿地图 | 3D / SVG | — | — | 仅 demo | https://www.minimax.io/news/minimax-m21 |

### MiniMax-M2（2025-10）/ M1（2025-06）
| Benchmark | 类别 | 分数 | 口径 | 来源类型 | 出处 |
|---|---|---|---|---|---|
| ArtifactsBench（M2） | 前端 / 可视化 | 66.8 | 3 次平均；用腾讯官方实现，Gemini-2.5-Pro 判分 | 厂商自报 | https://huggingface.co/MiniMaxAI/MiniMax-M2 |
| FullStackBench（M1） | 全栈 | M1-80K 68.3 / M1-40K 67.6 | — | 厂商自报 | https://huggingface.co/MiniMaxAI/MiniMax-M1-80k |

**第三方（MiniMax，实时榜 2026-09-23）**
| 模型 | 名次 | 分数 |
|---|---|---|
| minimax-m3 | #50 | 1486 |
| minimax-m2.7 | #79 | 1398 |
| minimax-m2.1-preview | #85 | 1387 |
| minimax-m2.5 | #87 | 1384 |
| minimax-m2 | #110 | 1298 |

出处：https://arena.ai/leaderboard/code

---

## 结论

1. **主流做法是「自建集 + 引用 Arena」，公开 benchmark 用得很少。**
   - 7 家里有 6 家的主力前端评测是自建集：
     - Kimi：Webdev Bench / Design Bench
     - 智谱：CC-Bench-V2 / Z.ai Code Bench
     - Qwen：QwenWebBench → QwenWebDev → QwenReactBench / QwenSVGBench / QwenVision2Code
     - Seed：Trae Web Bench / Artifacts / U-Artifacts
     - MiniMax：VIBE → VIBE-Pro → VIBE-V2 / SVG-Bench
     - 混元：WebCraftBench / Hy-Vibe
   - 这些自建集的评法几乎都是「渲染后让 VLM / agent 判分」或「人评对战」，分数跨版本不可比。Qwen 的集甚至每一代都换名字。
   - 唯一的公开人类偏好口径是 arena.ai Code Arena / WebDev。Kimi K3、GLM-4.7 / 5、Seed2.1 都在发布材料里引用了它，但它本质上是第三方榜单。
2. **公开前端 benchmark 用得零散，而且在变。**
   - ArtifactsBench 只有 MiniMax-M2、Seed2.0、Hunyuan-A13B 报过。之后三家都不再报，腾讯自家新模型也换成了 WebCraftBench。
   - Design2Code 只在视觉模型上报：GLM-4.5V / 4.6V / 5V-Turbo、Qwen3-VL。
   - 2026 年下半年的新热点是 **Vision2Web**：GLM-5.3-Flash、GLM-5V-Turbo、Qwen3.8 全系都报了。
   - 各有一家报过的公开集：
     - SWE-bench Multimodal：只有 Qwen3.8-27B
     - FullStackBench：只有 MiniMax-M1、Hunyuan-A13B、Qwen3.5 和 Qwen3-Coder-Next
   - 各家都没有报：WebDev Arena（作为自报分）、Vibe Code Bench、VisualWebArena。
3. **3D、Blender、CAD 方向的量化分数几乎只有 Qwen 在报，而且基本是自建集。**
   - Qwen3.8-Max 报了 QwenBlenderBench 69.9（原文明写 internal）和 Parametric CAD Bench 91.5（原文没写来源）。
   - Kimi K3 的 Webdev Bench 里有「3D / WebGL / Shader」子项，给的是胜率。
   - 其他家的 3D 内容全是 demo：GLM-5.3-Flash 的 Blender / CAD、MiniMax-M2.1 的 Three.js、Seed2.1 的 3D 庭院等。
   - 没有任何一家报过 BenchCAD、BlenderGym、3DCodeBench 这类公开集。
4. **游戏方向没有公开的「生成游戏」benchmark。**
   - 有分数的只有自建集的子类：Kimi Webdev Bench 的 Games 子项、GLM CC-Bench-V2 的 Web Games 场景、QwenWebBench 的 Games 类、ArtifactsBench 的 GAME 维度。
   - 另外，Arena 的 Gaming 分类排名是第三方数据。
   - Seed 的 GameWorld / Poki 考的是「玩游戏」，不是「写游戏」。
   - 其余全是「一句话生成小游戏」的 demo。
5. **DeepSeek 是例外。** 从 V3.1 到 V4.1，官方没报过任何视觉或前端 coding benchmark。
   - 只有内部的 DSBench-FullStack（全栈，不专门考视觉），加上 PPT 和官网复刻 demo。
   - 前端能力只能看 Arena 推文里的第三方分数。
   - GUI 类（OSWorld、ScreenSpot-Pro）在其他各家基本都作为多模态 agent 参考项报了，DeepSeek 没报。

