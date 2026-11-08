# 索引

这批材料回答一个问题：**要复刻 GPT-6 Astra 与 Claude Opus 5.5 的 visual coding 能力，训练数据该怎么造。**
成稿是站点的 Algorithm 页（五个视图），正文源在本目录的 `draft_*.md`，由 `scripts/gen_alg_page.py` 组装。

## 成稿

| 文件 | 视图 | 回答什么 |
|---|---|---|
| `draft_overview.md` | Overview | 为什么瓶颈在判定、能力差距在哪、路线与测量预算 |
| `draft_tasks.md` | Tasks | 任务从哪来、怎么变可验证、准入测试、多样性与产能 |
| `draft_verifier.md` | Verifier | 分层判据、取证、攻击测试、规模化之后的盲区 |
| `draft_training.md` | Training | 该不该上 RL、算法、轨迹修复、自检、监控、配方 |
| `draft_domains.md` | Domains | 同一套方法换到 Web、图表、游戏还成不成立，入场顺序 |

## 本地实验与核验

| 文件 | 内容 |
|---|---|
| `90_local_experiments.md` | three.js 线的全部实测：harness、分层判别力、留出测试、VLM judge 对照、自动造题、一道 0% 的题查出两个问题、实验矩阵、留一层消融、难度分布 |
| `91_3jsbench_verified.md` | 实地核实 3JSBench 的榜单与方法论，它的管线与本项目高度重合 |
| `92_number_audit.md` | 九组关键数字的独立核验记录，以及已更正的八处错 |
| `18_redteam.md` | 对成稿的红队审查：论证漏洞、八个失败模式、替代方案、待核数字 |

## 调研笔记

| 文件 | 主题 |
|---|---|
| `01_frontier_labs.md` | 前沿实验室公开了什么（结论：西方三家几乎不披露训练配方） |
| `02_task_sources.md` | GitHub 像素基线仓库、社区站点、已有 benchmark，按可验证性分级 |
| `03_verifiable_construction.md` | 八种把任务变可验证的范式、参考代码的五个用途、数据质量指标 |
| `04_verifier.md` | 感知指标、VLM judge、3D 专题、游戏、hack 实例、分层与校准 |
| `05_trajectory_repair.md` | 长程轨迹剪枝与纠错数据，保留什么删什么 |
| `06_harness.md` | 无头渲染、确定性、吞吐实测、agent 的视觉工具 |
| `07_capability_spec.md` | 十四个能力维度、差距归因、评测方案与测量预算 |
| `08_rl_recipe.md` | RL 算法、异步基础设施、视觉 reward、分阶段配方 |
| `09_pretrain_data.md` | 预训练与中训的「代码配渲染图」数据，规模与挖掘管线 |
| `10_blender_tasks.md` | Blender 侧的状态断言、任务合成、判别力实测 |
| `11_hacking_defense.md` | 攻击面穷举、verifier 校准协议、在线监控、人工抽检 |
| `12_self_verification.md` | 自检能力：增益来自判别不来自反思 |
| `13_scaling_tasks.md` | 从几十个场景扩到十万：多样性、难度、去重、成本模型 |
| `14_web_verifier.md` | Web/DOM 侧的确定性信号与本机实测 |
| `15_game_verifier.md` | 可玩性拆解、覆盖率瓶颈、状态接口、确定性回放 |
| `16_primary_sources.md` | 两家一手材料的逐篇精读与可照抄机制 |
| `17_chart_verifier.md` | 图表与矢量图的逐值回读，噪声地板为零 |
| `19_aesthetics.md` | 审美能不能做成可用信号 |
| `20_base_model.md` | 底座选型：视觉编码器、分辨率、图像 token、上下文 |

## 代码

`scripts/vc_verifier/`，四条技术线各一套 harness 与分层 verifier，外加自动造题、变异测试、消融、
VLM judge 对照、求解实验。见该目录的 README。

## 进度

`STATE.md` 按时间记录了全过程，包括改错与翻案。读结论看成稿，读过程看它。

