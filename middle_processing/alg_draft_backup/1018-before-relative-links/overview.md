# Visual Coder

## Contents

- [Scope](#scope)
- [Environment](#environment)
- [Algorithm](#algorithm)
- [Evaluation](#evaluation)

## Scope

模型写出的代码能运行，不等于结果可用。在视觉交互场景中，代码要被渲染、被操作，最后交付为网页、3D 资产或游戏；交付质量要靠渲染结果、交互行为和运行时状态来判断。本文覆盖三个场景：

| 场景 | 产物 | 验收依据 |
|---|---|---|
| Web | HTML、多文件 Web App、图表与 SVG 代码 | 渲染结果、浏览器 agent 实测 |
| 3D | Blender 代码、CAD 代码、神经 3D 资产 | 多视图渲染、几何检查、运行时状态 |
| Game | Pygame、JavaScript、Godot、UE5 工程 | 单元测试、agent 试玩 |

## Environment

[Environment](env/env.md) 按场景分为 Web、3D、Game 三个视图。每个视图包含三部分：Open Benchmarks、Open Data Pipelines、In-House Data Pipeline。

| 视图 | Benchmark | 数据管线 | 数据可下载 |
|---|---|---|---|
| Web | 42 | 37 | 25 |
| 3D | 28 | 23 | 17 |
| Game | 8 | 10 | 1 |

数据解读：

- **评测从「输出是否与参考一致」转向「输出是否可用」。** 新的 benchmark 由 agent 操作页面、试玩游戏，或对几何做确定性检查。
- **越接近真实工程，得分越低。** 端到端 Web App 为 61.8%（论文口径），UE5 C++ 为 55.5%，Godot 游戏为 41.46%，CAD 桌面软件为 17.5%（人类专家为 87.0%）。
- **公开数据中，图表与 SVG 最成熟。** 3D 与 CAD 依靠程序化合成获得无标注成本的真值。游戏方向没有规模化的开源训练数据，10 条工作中只有 1 条可以下载。

## Algorithm

[Algorithm](alg/alg.md) 回答一个问题：要复刻 GPT-6 Astra 与 Claude Opus 5.5 的 visual coding 能力，训练数据该怎么造。分五个视图，每个视图文末附参考文献，正文每个数字都链到原文。

| 视图 | 回答什么 |
|---|---|
| Overview | 瓶颈为什么在判定、差距在哪、测量预算 |
| Tasks | 任务从哪来、怎么变成可验证、准入测试与产能 |
| Verifier | 分层判据、取证、攻击测试、规模化后的盲区 |
| Training | 该不该上 RL、轨迹修复、自检、监控、配方 |
| Domains | 同一套方法换到 Web、图表、游戏还成不成立 |

数据解读：

- **判定方式决定能不能把模型分开。** [3JSBench](https://3jsbench.com/) 用 695 条确定性几何检查（[方法论](https://3jsbench.com/methodology)），Astra 通过 80.0%（240/300），Opus 5.5 通过 49.0%（147/300）；同一批尝试的 SigLIP2 相似度两者只差约 0.001。
- **截图加 VLM 不能当 reward。** [WorldCoder-Bench 表 2](https://arxiv.org/abs/2606.01869)：截图加 VLM judge 与真值的 Kendall τ_b 是 −0.068，成本约为只读 DOM 的 50 倍。
- **前沿实验室公开的是 harness，不是配方。** Anthropic 披露了生成器与评审器分离的设计 harness（[博客](https://www.anthropic.com/engineering/harness-design-long-running-apps)），OpenAI 披露了游戏验证手段（[Astra 游戏博客](https://developers.openai.com/blog/how-to-build-games-with-astra)），训练数据与视觉 reward 都未披露。
- **本项目实测：分层程序化判据 47/47，单张截图逐像素 12/29**（[实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。

## Evaluation

[Evaluation](eval/eval.md) 包含四部分：

- **Why Auto-Eval**：为什么需要自动评测
- **Introduce Visual Critic**：Omini Reward Model 与 Visual Analysis Platform
- **Failure-Mode Analysis**：与前沿模型的对比
- **TMM**：环境侧、服务侧、行为侧的过程指标，以及如何回流到训练迭代

