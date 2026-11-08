# Algorithm

<style>
/* 窄屏下视图切换横向可滚，否则第五个视图会被截掉（与 Market 页同一处理） */
@media (max-width:720px){
  .doc .view-switch{display:flex;max-width:100%;overflow-x:auto;scrollbar-width:none}
  .doc .view-switch button{white-space:nowrap;padding:7px 14px;flex:none}
  .doc table{display:block;overflow-x:auto}
}
</style>

<div class="view-switch"></div>


<div class="env-view" data-view="overview" data-label="Overview">

<nav class="toc view-toc"><h2>Contents</h2><ul><li class="l2"><a href="#ov-1"><span class="num">1</span> Visual Coding Has No Unit Tests to Inherit</a></li><li class="l2"><a href="#ov-2"><span class="num">2</span> A Verified Task Is Three Parts, Not One</a></li><li class="l2"><a href="#ov-3"><span class="num">3</span> The Self-Verification Hypothesis Did Not Survive</a></li><li class="l2"><a href="#ov-4"><span class="num">4</span> Fourteen Dimensions, and Where the Gap Actually Sits</a></li><li class="l2"><a href="#ov-5"><span class="num">5</span> The Frontier Labs Published Harnesses, Not Recipes</a></li><li class="l2"><a href="#ov-6"><span class="num">6</span> Measurement Budget Decides What the Roadmap Can Claim</a></li><li class="l2"><a href="#ov-7"><span class="num">7</span> Which Numbers Are Ours and Which Are Quoted</a></li></ul></nav>

<a class="anchor" id="ov-1"></a>

## 1 Visual Coding Has No Unit Tests to Inherit

[SWE-bench](https://arxiv.org/abs/2310.06770) 的每道题都至少带一个 fail-to-pass 测试（原文数据构造一节），所以「改对了没有」是一个布尔值。视觉产出没有这个布尔值。一个页面、一段 three.js 场景、一个 Blender 渲染，对不对要靠人看。看一眼就能判的东西，恰恰是最难写成脚本的东西。

常见的替代方案有两条：把判定外包给像素指标，或者让模型看着截图自评。两条都被实测否掉了。注意这里说的是「自评」——模型判自己的产物；换成独立的视觉模型去判别人的产物，情况完全不同，后面讲 Verifier 时会单独量。

核心发现：现成的「看图打分」类信号与真值的相关性要么接近零，要么是负的。

下表四行全部出自 [WorldCoder-Bench 表 2](https://arxiv.org/abs/2606.01869)：相关性是与隐藏契约覆盖率（V-Cov）的逐对 Kendall τ_b，假阳性率是低 V-Cov 产物被判通过的比例，成本以只读 DOM 为 1。

| 判定方式 | 与真值的相关性 | 假阳性率 | 相对成本 |
|---|---|---|---|
| 隐藏运行时状态契约 | Kendall τ_b 1.000 | 0 | 约 2 倍 |
| 八步 agent 自主探查 | +0.111 | 45.6% | 约 400 倍 |
| 只读 DOM | −0.021 | 33.7% | 1 倍（基线） |
| 截图加 VLM judge | −0.068 | 3.2% | 约 50 倍 |

同一个公开评测同时给出了正反两面。[3JSBench](https://3jsbench.com/) 用 100 道 three.js 题、每题三次一次成型的尝试、695 条确定性几何检查判定（[方法论页](https://3jsbench.com/methodology)），Astra 通过 80.0%（240/300），Claude Opus 5.5 通过 49.0%（147/300），两者差 31 个百分点；而同一批尝试的 SigLIP2 相似度均值，Astra 0.1081 对 Opus 5.5 0.1067，只差约 0.001（站点页面数据），站方自己把这个信号标为不参与判定的描述性指标。

核心发现：换一套判据，同一批产物上的模型差距从约 0.001 变成 31 个百分点（[3JSBench 榜单与页面数据](https://3jsbench.com/)）。

确定性判据能把模型分开，嵌入相似度不能。这句话是整页的出发点。本文的数字读自 2026-10-15 的线上榜单，站方在 2026-10-14 做过一次改判，引用时要带日期（[本项目核验记录](../middle_processing/vc_data/91_3jsbench_verified.md)）。

开头那张表的数字出自 [WorldCoder-Bench](https://arxiv.org/abs/2606.01869)。截图加 VLM judge 的假阳率并不高，只有 3.2%，问题出在它与真值的相关性是负的——它不是「乱放行」，而是排序方向错了，而且比读运行时状态贵 25 倍（约 50 倍对约 2 倍）。只读 DOM 更糟，三分之一的坏产物被它放过（33.7%）。同向的证据还有三条：

- [3JSBench](https://3jsbench.com/) 公开的 11 个模型的 SigLIP2 相似度均值全落在 0.0774（inkling）到 0.1081（Astra）这条窄带里，区分度接近零。
- [WorldBench 表 5](https://arxiv.org/abs/2610.10622) 的变异测试把功能按构造删掉之后，只读源码的 judge 仍然给这些被删项 5.44 分（满分 7.11）。
- [UI2Code^N §4.3](https://arxiv.org/abs/2511.08195) 直接拿 CLIP 相似度当 reward，在 Design2Code 与 Flame 上都低于纯 SFT。

[本项目的 three.js 原型](../middle_processing/vc_data/04_verifier.md)也复现了同一现象：雪人任务的 6 个候选页面，单张截图相似度全落在 0.973 到 1.0 之间，完全分不开。

那么反过来问：把判定做确定了，差距会不会自己消失？不会。

核心发现：同样是完全确定的判据，同样是 three.js，一个评测量出 57 个百分点的差距，另一个只量出 2.5 个（[3JSBench](https://3jsbench.com/)、[WorldCoder-Bench 表 1](https://arxiv.org/abs/2606.01869)，见下表）。

| 评测 | 判据性质 | 最高分 | 第二梯队最好 | 差距 | 来源 |
|---|---|---|---|---|---|
| 3JSBench | 695 条确定性几何检查，不含任何模型打分 | Astra 80.0% | Kimi K3 23.0% | 57.0 个百分点 | [3JSBench 榜单](https://3jsbench.com/) |
| WorldCoder-Bench | 隐藏的运行时状态契约，确定性断言 | GPT-5.4 的隐藏契约覆盖率 27.8% | Qwen3.6-Plus 25.3% | 2.5 个百分点 | [WorldCoder-Bench 表 1](https://arxiv.org/abs/2606.01869) |
| Design2Code（对照，非确定性） | 厂商报的是 o4-mini 看图打的 0 到 100 相似分，不是像素与 DOM 四项 | GLM-5V-Turbo 94.8 | Qwen3-VL-235B-Thinking 93.4 | 1.4 个百分点 | [GLM-5V-Turbo 报告](https://arxiv.org/abs/2604.26752)、[Qwen3-VL 报告 表 2](https://arxiv.org/abs/2511.21631) |

数据解读：差异不由判定方式解释，由动态范围解释。WorldCoder-Bench 的原文明说没有任何系统在隐藏契约上超过 30%，前四名挤在 23.0% 到 27.8%（[原文 §4](https://arxiv.org/abs/2606.01869)），差距自然被压扁；Design2Code 反过来，头部模型挤在 93 以上的天花板，差距同样被压扁（而且这一行的判据本身是模型打分，只能当量程的对照）；只有 3JSBench 的最高分到了 80%，有足够的量程，差距才张得开。**我们真正要做的 three.js 复刻正好落在中段，那是差距最大的区间。**

所以这一节的结论要比直觉弱一档，也比直觉稳一档。

- **不成立的说法**：判定一确定，开源就追上来了。这句话被 [3JSBench](https://3jsbench.com/) 直接证伪。
- **成立的说法**：判定方式决定你能不能把模型分开。同一批 3000 次尝试，确定性判据量出 31 个百分点（Astra 80.0% 对 Opus 5.5 49.0%），嵌入相似度只量出约 0.001（[3JSBench](https://3jsbench.com/)）。
- **因此要先做判定的理由不是「结构不是瓶颈」**，而是更朴素的一条：没有判定，既测不出差距，也训不动。这个理由弱一些，但它不需要赌一个赌不赢的判断。

下面这张表是在这个前提下读的：在少数判定确定、分数落在中段的窄任务上，开源确实追到了。

| 子任务 | 判定方式 | 权重未公开的最好 | 权重公开的最好 | 差距 | 来源 |
|---|---|---|---|---|---|
| 多轮指令遵循（MTAC-IFBench 约束满足率） | 每条约束编成 checklist，脚本加裁判逐条验 | Claude-Opus-4.6 78.6 | GLM-5.2 80.4（全场最高） | 开源反超 1.8 点 | [MTAC-IFBench 表 2](https://arxiv.org/abs/2609.14992) |
| 短程多轮修复（SWE-bench Verified，同 harness） | 单元测试 | Claude 4.5 Opus 76.8 | MiniMax M2.5 75.8 | 1.0 点 | [SWE-bench 官方 Bash Only 榜](https://www.swebench.com/) |
| 可访问性（RealUIReq-300，违例率 IR_Axe，越低越好） | 规则引擎 | GPT-5.1 0.13 | Qwen2.5-Coder-7B 加 GRPO（A11yn）0.05 | 开源反超，但这一格要打折扣 | [A11yn 表 2](https://arxiv.org/abs/2510.13914) |

数据解读：三行里只有第一行站得住。它的分数在中段，每条约束都编成 checklist 用脚本加裁判逐条验，归类无歧义，而且**所有模型都在同一个脚手架下跑**——这正是本页反复强调的同 harness 对照。全场 11 个模型的约束满足率落在 60.6% 到 80.4% 之间，最高的那个是权重公开的（[MTAC-IFBench](https://arxiv.org/abs/2609.14992)）。

- 第二行要打折：[SWE-bench](https://arxiv.org/abs/2310.06770) 2023-10 发布，是被针对性优化最久的公开榜之一，头部分数挤在一起（[官方榜](https://www.swebench.com/)），差距小可以由「被优化过」解释。
- 第三行要打更大的折：[A11yn](https://arxiv.org/abs/2510.13914) 的训练 reward 与评测主指标是同一个量，都来自 axe-core，所以 0.05 对 0.13 是「直接优化的量」对「零样本」，不是公平比较。它真正独立的证据有两条：
  - 换一个规则引擎（AChecker）后 0.26 对 0.35（[A11yn 表 2](https://arxiv.org/abs/2510.13914) 的 IR_AChecker 列）；
  - 人工两两比较，5 名评测员共 1,330 次判定，非平局里 64.7% 偏向它（表 7）。后者按判定数算是极显著的，但按评测员聚类就不显著了（只有 5 名，4 比 1，双侧 p = 0.375，[本项目复算](../middle_processing/vc_data/18_redteam.md)），所以稳妥的说法是「人类偏好没有退化」，而不是「人类明显更喜欢它」。

一行有效证据支撑不了「结构不是瓶颈」，只能支撑「结构不是唯一瓶颈」。反方向的参照同样要给：[Vision2Web 表 3](https://arxiv.org/abs/2603.26648) 的全栈视觉建站档，开源的 Qwen3-VL-32B / 8B 全线 0 分，而那一档的判定靠 GUI agent 加 VLM，恰恰没有确定性判据，所以连「差多少」都说不清。

复刻 Astra 与 Opus 5.5 的第一件事，是先把量尺造出来。

<a class="anchor" id="ov-2"></a>

## 2 A Verified Task Is Three Parts, Not One

后面所有讨论都用同一套词。

| 术语 | 定义 | 它不是什么 |
|---|---|---|
| Verified Task | 一道可自动判定的任务，由 Problem Statement、Harness、Verifier 三件组成，缺一件就不算 | 不是「一条 prompt 加一个参考答案」 |
| Problem Statement | 交给模型的需求描述，可以带多模态参考（参考图、参考页面） | 不是评分标准，模型看得到 Problem Statement，看不到 Verifier |
| Harness | 把产物跑起来并采集证据的那层：无头浏览器、冻结时钟、固定视口、多视角渲染、运行时状态读取 | 不是中性容器，它本身就是能力的一部分 |
| Verifier | 把证据判成通过或不通过的规则 | 不是 reward 模型 |
| 程序化信号 | 由确定性规则给出的判定：执行是否成功、几何断言、DOM 盒模型、规则引擎、渲染计数器 | 不是「代码静态分析」，它读的是运行后的状态 |
| VLM judge | 用视觉语言模型看渲染结果给判定 | 不是 Verifier 的替代品 |

三件套里最容易被跳过的是 Harness。

- [MTAC-IFBench](https://arxiv.org/abs/2609.14992) 上同一个 GLM-5.2，在 Claude Code 下严格全满足率（C-ISR）12.7，换 OpenCode 掉到 6.7，腰斩。
- [Vibe Code Bench 榜单](https://www.vals.ai/benchmarks/vibe-code)（2026-10-12）上同一个 Claude Opus 4.8，OpenHands 下 82.72%、Claude Code 下 77.48%，差 5.2 点；GPT-5.5 在 OpenHands、Factory、Codex 三个脚手架上分别是 69.85%、67.39%、58.19%，极差 11.7 点。

所以任何一个数字离开 harness 版本就没有意义。

Verifier 与 Problem Statement 之间有一条硬约束：Verifier 能查的信息量必须小于等于 Problem Statement 给出的信息量。[本项目预实验](../middle_processing/vc_data/90_local_experiments.md)（§5）撞过这条线两次。需求写「杯子应使用有别于桌面木色的独立颜色」，Verifier 却要求恰好是参考里那个蓝；需求写「桌腿应位于桌面四个角落附近」，Verifier 却要求腿的位置和参考几乎重合。两次失败都不是模型能力问题，而是任务不可解。这类任务进了 RL 就是纯噪声。

程序化信号与 VLM judge 的分工也要先钉死。[本项目](../middle_processing/vc_data/90_local_experiments.md)（§3）在 48 个带标签的 case 上做过对照，4 个 judge 各判两次、温度 0，共 768 次判定：四模型多数投票单视角 44/48、多视角 46/48，而程序化信号在它自己的标注集上是 47/47。单个 VLM 重判会翻面，最差的一档两次一致只有 38/48，翻面率 20.8%。结论是 VLM judge 的价值在于告诉你该补哪一条程序化检查，不在于直接当 reward。本项目的一次翻案正是这样发生的（同一记录 §3.4）：用车床几何转出的雪人头顶没有封口，四个 VLM 都看出来了，而当时的程序化信号全部失明，修法不是调阈值，是补一个不随缺陷尺寸衰减的拓扑量。

<a class="anchor" id="ov-3"></a>

## 3 The Self-Verification Hypothesis Did Not Survive

本项目的初稿写的是「自我验证循环是前沿相对开源的主要差距」。补完证据后这个结论反转了，必须先说清楚，否则后面的投入会压错方向。

支持循环论的证据是真的：把观察权限放开之后，模型在 3D 任务上的分数确实涨得很明显（[3DHarnessBench 表 1](https://arxiv.org/abs/2609.06535)，见下表）。

但「增量大」不等于「差距大」，而且**增益倍数本身量不出能力**。

| 来源与模型 | 单步基线（单视角档） | 开循环后（主动视觉档） | 增益 | 来源 |
|---|---|---|---|---|
| 3DHarnessBench，Qwen 3.8 Max | 0.740（单视角档全场第一） | 0.809 | 加 9.3% | [3DHarnessBench 表 1](https://arxiv.org/abs/2609.06535)（UNI3D 列） |
| 3DHarnessBench，Claude Opus 5 | 0.725 | 0.871 | 加 20.1% | 同上 |

这里必须交代一处核验结果。初稿在这张表里还有三行来自某个 CAD 评测的「带工具与不带工具」对照，用来论证「增益倍数与单步基线负相关」。回去读那篇论文的原文时发现，它评测的模型与我们引的那几个对不上，也没有这样一组对照——**所以那三行被删掉了，连带那个负相关的结论一起撤回**（[核验记录](../middle_processing/vc_data/92_number_audit.md) §四）。

留下的两行只能支撑一个弱得多的说法：同一个增益幅度背后可以是完全不同的绝对水平，所以**增益倍数不能当 KPI**。把它写进考核，团队会被奖励去把单步做烂，而且连「做烂了没有」都量不出来。报分必须同时给带工具与不带工具的绝对值。

这两行的四个数已回原文表 1 逐值核对一致（[核验记录](../middle_processing/vc_data/92_number_audit.md) §二）。

四条反转证据把「前沿靠循环赢」这个说法直接否掉。

| 证据 | 数字 | 来源 |
|---|---|---|
| 同 harness 的短程多轮（SWE-bench Verified，mini-SWE-agent，Attempts=1） | 最强闭源 76.8 对最强开源 75.8，差 1.0 点 | [SWE-bench Bash Only 榜](https://www.swebench.com/) |
| 迭代 harness 的收益分布（AutoLab 的脚手架消融，相对默认的 terminus-2） | 强单轮推理者 gpt-5.4 减 0.03，而 deepseek-v4-flash 加 0.13、mimo-v2.5 加 0.20；kimi-k2.6 在三个 harness 间最多差 0.43（pi-mono 0.21 到 mini-swe-agent* 0.64） | [AutoLab 的 harness 消融](https://arxiv.org/abs/2606.05080) |
| 前沿轨迹是否真做自我验证（VISTA，18 应用，8,487 个人工标注组件） | 73.0% 完全跳过 prompt 明确要求的自审，44.5% 从没打开过设计截图，8.3% 检查失败后仍报告成功 | [VISTA §5.2](https://arxiv.org/abs/2605.26144) |
| 朴素视觉自我迭代的净效果（RubSE，15 轮） | GPT-5.2 在 Design2Code 上全部 15 轮都低于第 0 轮，终点减 2.73 | [RubSE](https://arxiv.org/abs/2608.24138) |
| 完全没有循环的代际跃升（GPT-6 Astra system card，UK AISI） | 禁用思维链的时间跨度，30.9 分钟对 GPT-5.6 Sol 的 3.6 分钟，约 8.6 倍 | [GPT-6 Astra system card](https://deploymentsafety.openai.com/gpt-6-astra) |

Anthropic 自己把这件事写成缺点。[Opus 5 的 system card](https://www.anthropic.com/claude-opus-5-system-card) 把「Unproductive self-verification」列为限制，[官方 prompting 文档](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)要求用户删掉显式验证指令，原话是这类指令「cause over-verification on Claude Opus 5」。

这里要克制一点：把这几条排成一个大小序是做不到的，因为它们的单位不同——时间跨度的倍数、Avg@3 的分数差、两个判别力榜的分数差、通过率的百分点差，彼此之间不存在「大于」关系（各条单位见上面的[反转证据表](#ov-3)与[本项目归因推断](../middle_processing/vc_data/07_capability_spec.md) §2.1）。能说的只有两件事。

- 第一，差距确实出现在这几个地方：
  - 禁用思维链时的可靠时间跨度：Astra 30.9 分钟对 GPT-5.6 Sol 3.6 分钟（[system card](https://deploymentsafety.openai.com/gpt-6-astra)）；
  - 超长程任务的完成度：0.68 对 0.46（[AutoLab 主表](https://arxiv.org/abs/2606.05080)）；
  - 判别力：[ProcessBench 表 3](https://arxiv.org/abs/2412.06559) 上 o1-mini 87.9 对开源最好的 QwQ-32B-Preview 71.5，差 16.4；但 [RewardBench 2 表 3](https://arxiv.org/abs/2506.01937) 上权重公开的专用 RM 反而领先（Skywork-Reward-V2-Llama-3.1-8B 84.1 对 gemini-2.5-pro 79.5），说明这一维高度依赖测法。两组都是 2024 到 2025 年的模型，只能说明测法敏感，不能代表当前代际。
- 第二，短程多轮这一项的差距最小，同 harness 下只有 1.0 点（[SWE-bench Bash Only 榜](https://www.swebench.com/)）。所以「多轮循环是主要差距」这个说法立不住，但「别的某一项是主要差距」同样没有证据支持。

一条必须记住的 nuance：这个结论适用于通用 agentic coding，在视觉与前端子域里差距要大一些。[FronTalk 表 4](https://arxiv.org/abs/2601.04203) 里，它提出的 AceCoder（agent 批判后重写）让 GPT-4o 文本档从 56.0 涨到 65.3（加 9.3），而 Qwen2.5-VL-72B 文本档只加 5.9、视觉档只加 0.8。

循环仍然要做，而且对低单步基线的起点绝对收益最大。它只是不再是「追平前沿」的全部答案。

<a class="anchor" id="ov-4"></a>

## 4 Fourteen Dimensions, and Where the Gap Actually Sits

能力按三条准则切成 14 项（[本项目能力规格](../middle_processing/vc_data/07_capability_spec.md) §1.1 与 §1.2）：可单独度量、可单独训练、失效模式不同。不满足任一条就不单列。其中三项是把常说的「自我验证」拆开的结果，分别是取证质量、判别力、探索纪律与停机。

拆开的理由来自 [3DHarnessBench 表 3](https://arxiv.org/abs/2609.06535) 的观察接口消融（10 个实例，UNI3D 列）：

- MiniMax M3 在主动视觉档只有 0.3722，仅仅规范化截图前的视口就回到 0.6148（[3DHarnessBench 表 3](https://arxiv.org/abs/2609.06535)）；
- Gemini 3.1 Pro 0.6776，换用 Fable 5 采集的检视图才回到 0.7605（同一篇[表 3](https://arxiv.org/abs/2609.06535)）。

两个模型被两种完全不同的干预治好，这是把「多给它看几眼」当成通用解法的反例。但这组消融只有 10 个实例，按本页后面那条采样噪声公式，这个规模下的最小可检测效应是 62.6 个百分点（[本项目复算](../middle_processing/vc_data/18_redteam.md)），两个差值都在噪声里。所以它只能当作设计上的提示，不能当作证据——真要拿它定能力分类，得先把实例数提上去重测。

核心发现：自我验证不在差距最前列。至于别的维度谁更靠前，证据不支持排一个序，下表的次序只是按投入顺序给的建议。

| 建议投入次序 | 维度 | 差距证据 | 为什么难追 |
|---|---|---|---|
| 不排第一 | 自我验证三项 | 同 harness 短程多轮差 1.0 点（[SWE-bench](https://www.swebench.com/)）；73.0% 前沿轨迹跳过自审（[VISTA](https://arxiv.org/abs/2605.26144)） | 它是全行业共同瓶颈，不是前沿的护城河 |
| 1 | 长程持久性与时间预算校准 | [AutoLab](https://arxiv.org/abs/2606.05080) 的 36 个长程任务，claude-opus-4.6 的 Avg@3 是 0.68，权重公开的最好是 kimi-k2.6 的 0.46，中间还夹着一个 0.50 的闭源模型（gemini-3.1-pro） | 不是开源闭源分界，闭源 gpt-5.4 只有 0.36，排在 kimi-k2.6、mimo-v2.5-pro、glm-5、deepseek-v4-pro 四个开源模型之后 |
| 2 | 长程多文件工程 | [Vibe Code Bench v1.1](https://www.vals.ai/benchmarks/vibe-code)，闭源最高 Claude Sonnet 5.5 92.39% 对权重公开的最高 Kimi K3 84.97%，差约 7 点 | 规模衰减是真问题：[JAMER](https://arxiv.org/abs/2606.19830) 上小项目运行通过率 80.4%，大项目掉到 5.7% |
| 3 | 调试与报错恢复 | SWE-bench Multimodal，Opus 5 自报 59.4（[system card §8.2](https://www.anthropic.com/claude-opus-5-system-card)，内部 harness）对 Qwen3.8-27B 自报 38.6（[模型卡](https://huggingface.co/Qwen/Qwen3.8-27B)，Claude Code harness），差约 21 点，两边 harness 不同 | 「不越改越坏」要轨迹级 reward |
| 4 | 3D 空间推理 | 几个 3D 与 CAD 评测集上，权重公开的模型基本没有报分 | 不是能力差距已证实，是测不出来，先建测法比先提能力重要 |
| 5 | 开放审美 | [Design Arena](https://www.designarena.ai/leaderboard)（2026-10-15 直读）Opus 5.5 1392 对权重公开最好的 kimi-k3 1363，约差 29 Elo；[Code Arena WebDev 镜像](https://www.respan.ai/models/benchmarks/lmarena-webdev-lmarena)（快照 2026-10-08）Opus 5.5 1813 对 Kimi K3 1654，约差 159 Elo | 其中可程序化的那一半（排版层级、尺度、间距节奏、色相数、对比度）本项目已实测能做成零噪声判据（[实验记录](../middle_processing/vc_data/19_aesthetics.md)）；剩下那一半才需要偏好数据与专用 RM |
| 6 | 可访问性与性能预算 | 性能预算零公开 benchmark | 不是差距，是空白，自建成本最低 |

这张表改变的是投入顺序。

- 排第一的长程持久性，reward 必须来自 agent 自己的行为轨迹而不是产物。
- 排第二的长程多文件工程需要十万量级的真实环境，[MiniMax M2.5 的公开口径](https://www.minimax.io/news/minimax-m25)是超过 20 万个真实环境。
- 排在最后、最便宜的两格恰恰最该先做：可访问性靠的是确定性规则引擎，判定本身零方差、无需 judge、无需 GPU，是全表性价比最高的 RL 信号。要注意它的覆盖面有限——[axe-core 的 105 条规则](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md)里能纯自动判定的只有 41 条，其余带人工复核标记（[本项目统计](../middle_processing/vc_data/14_web_verifier.md)），所以它是一条干净但窄的信号，不是「可访问性已经被解决了」。

判别力这一维有一条成本结论，但要带着限定词用：[CriticGPT](https://arxiv.org/abs/2407.00215) 估计，要靠纯加大模型达到 CriticGPT（RL only）的漏 bug 率，需要约 30 倍预训练算力。原文两次把这个外推称作朴素外推（naive extrapolation），而且它只在「人工植入 bug 的检出率」这一个分布上测过。可以拿它当量级参考，不能拿它当结论。

<a class="anchor" id="ov-5"></a>

## 5 The Frontier Labs Published Harnesses, Not Recipes

西方三家都没有公开 visual coding 的训练数据或 RL 环境配方。本项目对 Claude 4 到 Opus 5.5 共 9 份 system card 全文检索前端、审美、渲染、Blender、three.js 这些词，没有一条是在讲训练（[检索记录](../middle_processing/vc_data/01_frontier_labs.md) §1）。

核心发现：披露密度与地域完全倒挂，国内厂商披露最多，而且结构惊人一致。

| 来源 | 披露了什么 | 没披露什么 |
|---|---|---|
| Anthropic | 生成器与评审器分离的 harness、四维设计评分、few-shot 校准评审器、用 Playwright 实操页面再打分、每个维度设硬阈值、每次生成 5 到 15 轮迭代（[harness 设计博客](https://www.anthropic.com/engineering/harness-design-long-running-apps)）；「分布收敛」的归因与 frontend-design skill（[前端 skill 博客](https://claude.com/blog/improving-frontend-design-through-skills)） | 前端与 3D 专项数据、RL 环境、视觉 reward 模型 |
| OpenAI | 一句话级别的「专门训练过 UI 与图像使用」（[GPT-5.4 前端博客](https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4)）、「可以检查并修改渲染结果」（[GPT-5.6 发布页](https://openai.com/index/gpt-5-6/)）；游戏博客里的验证手段：特效开关的像素差分、渲染计数器、90 个帧间隔采样（[Astra 游戏博客](https://developers.openai.com/blog/how-to-build-games-with-astra)） | 数据来源、设计偏好数据、内部设计评测集的构成 |
| Google | RL 同时用可验证奖励与生成式奖励，post-training 加入端到端 web 与移动应用开发任务（[Gemini 2.5 技术报告](https://arxiv.org/abs/2507.06261)） | WebDev 数据来源、审美 reward 模型 |
| 国内各家 | 预训练把代码与渲染图配对（[Kimi K2.5](https://arxiv.org/abs/2602.02276)、[Qwen3-VL](https://arxiv.org/abs/2511.21631)），[Kimi K3](https://arxiv.org/abs/2607.24653) 扩展到 3D、游戏、CAD；数据过滤在真实沙箱里跑（[MiniMax-M2](https://arxiv.org/abs/2605.26494)、[MiMo-V2-Flash](https://arxiv.org/abs/2601.02780)）；RL 先过确定性门控再叠模型评审，构建失败或伪造实现时 reward 置 0（[Kimi K3](https://arxiv.org/abs/2607.24653)）；用录屏视频而不是静态截图做判别（[MiMo-V2-Flash](https://arxiv.org/abs/2601.02780)） | Blender 方向无人披露训练数据 |

两家都公开过能直接照抄的验收规程，而且它们和本文的设计独立撞上了。

[OpenAI 的官方前端提示文档](https://developers.openai.com/api/docs/guides/frontend-prompt)给 three.js 产出定了一套硬验收：用 Playwright 截图，再对画布做像素检查，查四件事——画面不是空白、取景正确、画面在动、资源不重叠。这四条和本文 Verifier 视图里的硬门槛与多视角剪影逐项对得上，差别只在本文把它们量化成了阈值。OpenAI 官方 [playwright-interactive skill](https://github.com/openai/skills/tree/main/skills/.curated/playwright-interactive) 还有一条值得抄的制度：把题面要求、实现声明、产物三方合并成一张检查清单，每一条声明都必须映射到可观测的检查，视觉检查与功能检查分开记（[本项目阅读笔记](../middle_processing/vc_data/16_primary_sources.md) §0.1）。

Anthropic 的[评测与爬坡方法博客](https://claude.dev/blog/automating-eval-design-and-hillclimbing/)给了 grader 的操作规程：

- rubric 写成可核验的陈述（checkable claims）而不是 1 到 5 分（[原文](https://claude.dev/blog/automating-eval-design-and-hillclimbing/)「not a 1-to-5 scale」）；
- 评判模型不能是被测模型；
- 同一份产物跑两遍 grader 看判定是否翻面；
- 噪声必须小于你关心的最小改进；
- 训练集与测试集必须切开。

其中一条的措辞和本文的结论几乎一样——grader 查的每一件事都必须写在题面里（原文「everything the grader checks is stated in the task」）。本文是从两次实测失败反推出这条的，他们是写在文档里的。

可以直接拿来用的还有两类东西。一类是 [Anthropic harness 博客](https://www.anthropic.com/engineering/harness-design-long-running-apps)里四条能写进 Verifier 的教训：

- 评审器必须独立并调成怀疑模式；
- 评分措辞会引导审美收敛，rubric 里不要写「museum quality」这种诱导词；
- 每个维度设硬阈值而不是加权求和；
- 分数整体上升但不是线性的，作者常常更喜欢中间某一轮——分数单调上升不等于质量单调上升。

另一类是国内的三层结构，它和本文的 Verified Task 三件套是同一件事的不同说法。

两家对「AI 味」的归因几乎一字不差，Anthropic 写「distributional convergence」（[前端 skill 博客](https://claude.com/blog/improving-frontend-design-through-skills)），OpenAI 写「fall back to high-frequency patterns from the training data」（[GPT-5.4 前端博客](https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4)）。双方都承认纯靠预训练分布只能得到平庸设计。审美必须靠后训练信号或推理时约束注入。这一条是本文推断，两家都没说自己怎么做。

还有一条推断值得记：Anthropic 在 [Fable 5 / Mythos 5 system card](https://www.anthropic.com/claude-fable-5-mythos-5-system-card) 里把用模型当 grader 的环境单独划成「grader hacking 高风险」一类，并说明利用性的 grader 觉察几乎只出现在这类环境里。这侧面说明这类环境在 Claude 的训练中真实存在，尽管官方从没说过把那套四维 rubric 用在训练里。

<a class="anchor" id="ov-6"></a>

## 6 Measurement Budget Decides What the Roadmap Can Claim

先给一个必须贴在墙上的数字：单维度 15 题乘 8 次采样，最小可检测效应是 18 个百分点（[本项目推导](../middle_processing/vc_data/07_capability_spec.md) §4.1 与 §4.3）。

记 M 为题数，n 为每题采样次数。采样噪声给出 SE(S) ≤ 0.5 / sqrt(M·n)。两个模型在同一题集上比较，取双侧 0.05、power 80%，得到（推导见[本项目能力规格笔记](../middle_processing/vc_data/07_capability_spec.md) §4.1）：

```
程序化信号                      MDE = 1.98 / sqrt(M·n)
VLM judge 三票多数              MDE = 2.38 / sqrt(M·n)
```

这个公式只算了采样噪声，没算题目之间的难度差，所以它给出的是**最小可检测效应的下界**，真实值更大。要钉死得先在现有任务上让两个模型各采 8 次，估出题间方差再把整张表上调（推导与限定见[能力规格](../middle_processing/vc_data/07_capability_spec.md) §4.1）。

核心发现：即便按下界算，常见的内部实验规模也读不出小于 18 个点的差异（下表即[能力规格 §4.3 的 MDE 表](../middle_processing/vc_data/07_capability_spec.md)）。

| 题数乘采样 | 总样本 | 程序化 MDE | VLM judge MDE |
|---|---|---|---|
| 15 乘 8 | 120 | 18.1 | 21.7 |
| 30 乘 8 | 240 | 12.8 | 15.4 |
| 40 乘 16 | 640 | 7.8 | 9.4 |
| 100 乘 8 | 800 | 7.0 | 8.4 |
| 150 乘 16 | 2,400 | 4.0 | 4.9 |
| 300 乘 16 | 4,800 | 2.9 | 3.4 |

单位是百分点，表中数值由上面两条公式直接算出（本轮已逐格复算一致；原表见[能力规格](../middle_processing/vc_data/07_capability_spec.md) §4.3）。这张表给出三条立刻可用的结论。

1. 很多内部实验报出的「这个改动涨了 5 个点」是在 18 点分辨率下读出来的，它是噪声（15 乘 8 一行）。
2. 要在单维度上读出 5 个百分点，需要 M 乘 n 约 1,600（程序化信号）或 2,260（VLM judge），即 40 题乘 40 次或 100 题乘 16 次（1.98/√1600 ≈ 4.95，2.38/√2260 ≈ 5.0；[能力规格](../middle_processing/vc_data/07_capability_spec.md) §4.3）。
3. 在单条 case 上比两个方案的优劣，每臂至少 63 次；n 等于 5 时单题只有 6 个可能取值，MDE 是 0.89，等于什么也没测（单题 MDE = 1.98/√n，要到 0.25 需 n ≥ 63；[能力规格](../middle_processing/vc_data/07_capability_spec.md) §4.3）。

按这个分辨率把 14 维分成三档配置（[配置推导](../middle_processing/vc_data/07_capability_spec.md) §4.4）：核心档每维 40 题乘 16 次采样，中档每维 30 题乘 8 次，硬闸档每维 20 题乘 4 次，合计 430 题、4,720 次 rollout，全集加权总分的 MDE 约 3.0 到 3.5 个百分点。硬闸档只给 4 次采样是因为那几维的 Verifier 是确定性的，作用是过与不过，不需要 3 个点的分辨率。

审美这一维不能整块推迟，它要先拆。[本项目在 Web 那套 harness 上实测过](../middle_processing/vc_data/19_aesthetics.md)（结果文件 [aes_results.json](../scripts/vc_verifier/web/out/aes_results.json)）：12 个只破坏审美不破坏功能的变异里，功能侧判据只「抓到」2 个，而那 2 个还是因为改色顺带破坏了对比度才被规则引擎抓到；新加的审美判据抓到 9 个，8 个合法改版零误杀，成本只有功能侧的六分之一。所以可程序化的那一半今天就能接进 RL，推迟的应该只是剩下那一半。

剩下那一半有两条噪声地板必须先接受。

- 其一，审美无法靠单人标注当真值：[AUV-Bench](https://arxiv.org/abs/2609.34854) 请 51 名专业设计师标 1,395 个可执行参考 UI，单人 Krippendorff α 宏平均只有 0.368，3 人平均后 ICC 才到 0.637。另一项工作 [WebDevJudge 表 1](https://arxiv.org/abs/2510.18560) 里，无 rubric 时两名标注者一致率 65.0%（100 条），有人写的 rubric 树后升到 92.0%（另 50 条，不是同一批样本上的受控对比）。审美的可度量性主要是 rubric 工程问题。
- 其二，多 judge 投票的有效独立性比想象的低：[一项 judge 共识研究](https://arxiv.org/abs/2609.22512)里，10 个 judge 的平均成对错误相关 0.21，统计信息量只相当于 3.5 个独立 judge，最多 28% 的系统对比中忽略共享错误会得出假显著结论。保守做法是把三票多数的降噪效果按两票算。

还有一条预算分配上的结论：**做系统级比较时，加题比加标注者划算。** 本项目按 AUV-Bench 的标注数据外推（[推算记录](../middle_processing/vc_data/19_aesthetics.md) §0），要让单条 UI 的判读可信（组内相关系数到 0.8）需要每条 7 个标注者，到 0.9 需要 16 个；但把标注者从 3 个加到 16 个，人力乘以 5.3，检测同样的分差所需题量只从 185 降到 130，省三成。加人只有在需要单条 UI 可信判读时才值得——做金标准、做个案分析。要的是系统级排序时，钱应该花在题量上。

三个阶段的目标按这个量尺写。

| 阶段 | 周期 | 头号可检验目标 | 验收数 |
|---|---|---|---|
| 一、先能测 | 约 3 个月 | 自建 harness 复现公开分，内部 430 题集上线，Verifier 准入全过 | 与公开数字差 ≤ 2 点；全集实测 MDE ≤ 3.5 点；变异杀死率 ≥ 95%、正确解通过率 ≥ 90%、flaky ≤ 1% |
| 二、接确定性信号进 RL | 约 6 个月 | 打可访问性、性能预算、布局响应式、交互状态逻辑、动画时间 | 可访问性 IR_Axe ≤ 0.08（[A11yn](https://arxiv.org/abs/2510.13914) 口径，现 GPT-5.1 0.13）；动画 Temporal ≥ 0.40（[Animation2Code](https://arxiv.org/abs/2606.28593) 当前全场最高 0.31）；视觉保真守住 ≥ 93 不退化 |
| 三、打自我验证与长程 | 约 12 个月 | 带工具的绝对分与多轮不塌，不是循环增益倍数 | 在自建的 3D 复刻集上，带工具与不带工具的绝对分同步抬高；三次全对与单次通过的比值 ≥ 0.90；超长程 Avg@3 ≥ 0.50（[AutoLab](https://arxiv.org/abs/2606.05080) 口径） |

阶段三那一行「不带工具同步不掉」是防「只练循环不练单步」的护栏，它对应前面那条「增益倍数量不出能力」。阶段二排除的是审美里**靠人判的那一半**，不是整个审美。众包 Elo 周期长，而且噪声大：[官方公开的 WebDev Arena 偏好数据](https://huggingface.co/datasets/lmarena-ai/webdev-arena-preference-10k)（10,501 条）里平局类合计 24.3%、其中 17.0% 的票是「两个都差」（[本项目实算](../middle_processing/vc_data/19_aesthetics.md)），不适合做短周期迭代指标；而且[官方博客](https://arena.ai/blog/webdev-arena)把「两个都差」归因到依赖解析失败、状态管理错误、编译报错——全是功能问题，所以那个 Elo 里有相当一部分信息量根本不是审美。可程序化的那一半没有这个问题，应该在阶段二就接进去。

三个阶段共用四条纪律。

- 任何维度报分，必须同时报题数、采样数、harness 版本、judge 型号、带不带工具，缺一项就不要进报告。
- 每次改 Verifier，先跑变异测试与注入测试再上线。
- 分数单调上升不等于质量单调上升，保留中间轮做人工对照。
- rubric 里不写量化阈值也不写诱导词，阈值写成代码闸。

下一步按这个顺序推进。

1. **先把 Web 这条线接进 RL 环境。** 它在三个维度上同时成立：五层程序化判据在 22 个带标签变异上零漏零误、单次取证的工具开销不到半秒（[Web verifier 实验记录](../middle_processing/vc_data/14_web_verifier.md)）、而且可访问性是目前唯一有公开验证的「确定性 reward 加 RL 就能赢闭源」的维度（[A11yn](https://arxiv.org/abs/2510.13914)）。它不需要 judge，不需要 GPU，是验证整条链路通不通的最便宜实验。
2. **补留出验证，而不是补新信号。** 三条线的判别力数字各自都带着同一个折扣：three.js 的 47 个变异里只有 18 个真正留出（[实验记录](../middle_processing/vc_data/90_local_experiments.md) §2.3），Blender 的留出集只有 7 个（[Blender 实验记录](../middle_processing/vc_data/10_blender_tasks.md)），图表与 Web 都是单任务（[图表](../middle_processing/vc_data/17_chart_verifier.md)、[Web](../middle_processing/vc_data/14_web_verifier.md)）。每条线补第二、第三个场景，阈值一个不动再跑一次，跑不过去就说明结论只在原场景成立。
3. **把三个真空白做成首发**：多视口一致性当确定性判据、性能预算当判据、动画的时间正确性当通用子分。三项在公开 benchmark 里都查不到先例（[本项目检索](../middle_processing/vc_data/14_web_verifier.md) §3.6），而前两项本项目已经有可跑的实现（[Web verifier](../scripts/vc_verifier/web/verify.js)）。
4. **拿到差距向量再决定投入。** 先用自建 Harness 跑一遍开源基座加两个前沿模型，产出按维度拆开的差距表。没有这张表，前面所有排序都是推断（同样的结论见[能力规格](../middle_processing/vc_data/07_capability_spec.md) §2.1 的「最终归因」，标为推断）。

还有一条顺序上的建议，它会改变预算分配。验证器造出来之后，第一个用途不该是 RL 的 reward，而是推理时的选择器。软件工程那边有一组干净的对照（[SWE-Master 表 3](https://arxiv.org/abs/2602.03411)）：在一个已经很强的监督微调基线（57.8）之上，RL 只加 3.6 分（61.4），而采 8 次再用验证器挑一个加了 12.4 分（70.2）；两者都做也只比单做选择多 0.6 分（70.8）。推理时选择不需要 rollout 集群，不需要训练，验证器做完当天就能用。本页的技术线不同，幅度不能照搬，但结构可以：**先扩数据，再接推理时选择，最后才考虑 RL**。

最后一条纪律，贯穿后面四个视图：**每一次改 Verifier 或改 Harness，先跑变异测试和作弊测试再上线。** 本项目在四条技术线上一共撞到六次同类事故（[事故汇总](../middle_processing/vc_data/18_redteam.md)）——开口曲面的体素填充无效、小部件上的占据指标退化成等值判断、文本记录跨帧累加、文字包围盒没过变换矩阵、测量绑死在表现型类名上、取证链路只认一种引库方式。六次全部表现为「把正确产物判挂」，六次全部不是阈值问题，六次全部是靠一个该放行的样本暴露出来的。

其中最后一次最值得记：它不在判据里，在取证链路里，症状是「模型连页面都写不对」，极容易被记成模型能力问题（[实验记录](../middle_processing/vc_data/90_local_experiments.md) §11）。而它只有在让模型自己从零写页面时才会暴露——我们自己写的参考解永远用同一种写法。

后面四个视图分别展开任务怎么构造、Verifier 怎么分层与取证、训练配方怎么配、这套方法换到别的产出形态还成不成立。

<a class="anchor" id="ov-7"></a>

## 7 Which Numbers Are Ours and Which Are Quoted

这一页混了三类数字，读的时候要分清，因为它们的可信度差一个量级。

| 类别 | 含义 | 本页举例 | 怎么复核 |
|---|---|---|---|
| 本项目实测 | 在这台机器上跑出来的，脚本与中间产物都在 | three.js 47 个变异的分层判别力、Blender 22 个、图表 16 个、Web 22 个；4 个 judge 在 48 个 case 上的 768 次判定；283 组修复运行；7 个作弊页面 | 重跑脚本，结果逐字节可复现（[three.js](../middle_processing/vc_data/90_local_experiments.md)、[Blender](../middle_processing/vc_data/10_blender_tasks.md)、[图表](../middle_processing/vc_data/17_chart_verifier.md)、[Web](../middle_processing/vc_data/14_web_verifier.md)） |
| 独立复核过的公开事实 | 引用来源之外，自己又查了一遍 | [three.js 参考截图](https://github.com/mrdoob/three.js/tree/dev/examples/screenshots) 610 张、[Babylon.js](https://github.com/BabylonJS/Babylon.js/tree/master/packages/tools/tests/test/visualization) 975 张、[Blender 渲染测试](https://github.com/blender/blender/tree/main/tests/files/render)参考图 2596 张；[3JSBench](https://3jsbench.com/) 的榜单、方法论与 695 条检查的分族；[Qwen3](https://arxiv.org/abs/2505.09388) 的算力对照（表 21）、[Design2Code](https://arxiv.org/abs/2403.03163) 的自修订掉分、[A2Z](https://arxiv.org/abs/2609.39564) 的真玩通过率、[SWE-Master](https://arxiv.org/abs/2602.03411) 的数据与推理时选择、[Infinigen](https://arxiv.org/abs/2306.09310) 的生成器计数 | 直接读仓库文件树、线上页面与论文全文（[核验记录](../middle_processing/vc_data/92_number_audit.md)） |
| 引用 | 来自论文、技术报告或官方文档，我们没有复现 | [AutoLab](https://arxiv.org/abs/2606.05080) 的脚手架消融、[3DHarnessBench](https://arxiv.org/abs/2609.06535) 的观察接口消融、各公开榜单的模型分 | 看原文，注意版本与日期 |

四条必须讲清楚的局限。

最大的一条限制不是样本量，是适用范围。本页所有判别力数字都来自「修复单处破坏」型任务。换成从零搭建重测，同一套判据 26 组全挂，而产物在人看来都是对的（[实验记录](../middle_processing/vc_data/90_local_experiments.md) §10）——它量的是与参考的绝对几何重合度，这只在「除一处外都与参考一致」时才等价于「做对了」。从零搭建要换一族判据，查的是部件计数、连接与间隙、相对比例，不是绝对位置。这条限制同时解释了为什么自动造题只造修复型，以及为什么难度分布是双峰的。

还有一条限制同样来自造法，而且直接改动了成本结论。单处破坏型任务的难度分布是双峰的：单一模型 pass@8 下 16 道题里 13 道全有或全无，0.3 到 0.7 带内一道都没有，剔除零梯度后只剩 19%（[实验记录](../middle_processing/vc_data/90_local_experiments.md) §15）。成本模型原先按 60% 外推，换成实测，造 10 万个任务要从 26.9 万候选变成 84.8 万，**成本乘 3.2**。所以扩产之前必须先换造法，单处破坏在难度维度上是封顶的。

这里还有一个口径陷阱值得单独记住：同一批题用**跨模型汇总**的通过率算，可用率是 70%；用**单一策略的 pass@k** 算是 19%（[实验记录](../middle_processing/vc_data/90_local_experiments.md) §15：跨 4 个模型汇总 70%，单模型 pass@8 为 3/16，Wilson 95% 区间 6.6% 到 43.0%）。汇总把「强模型会、弱模型不会」混成了中等通过率，凭空造出并不存在的中间难度，而且偏差方向固定是乐观。估 RL 的零梯度比例只能用将要训的那个策略自己的 pass@k。

本项目实测的样本量也很小。three.js 三个场景、Blender 一个、图表一个、Web 一个，变异全是单处改动，标签由一人标注，没有一致率数字。多处错误同时出现时各层会不会互相掩盖，没有测过。three.js 的 47 个里真正留出的只有 18 个，Blender 的留出集只有 7 个，Web 的 6 个留出变异与开发集同属一个任务，图表没有做留出（[图表记录](../middle_processing/vc_data/17_chart_verifier.md) §4.6）。

作弊测试证明的是那几条路径被堵住了，不是「不可 hack」。three.js 侧 7 条里有一条在修补之前真的骗过了 Verifier（[实验日志](../middle_processing/vc_data/STATE.md)）；Web 侧第一版只挡住 7 条里的 5 条，补判据之后 6 条，剩下一条是审计引擎本身的盲区（[Web 记录](../middle_processing/vc_data/14_web_verifier.md)，对应 axe-core issue #2680）。

引用本身要抽查，而且抽查会抓到东西。本页对十四组关键数字做了回原文核验，十三组一致，一组不通过，另有一处措辞因逐值复核而收紧——某个评测的带工具对照在原文里根本不存在，那几行连同依赖它的结论一起撤回了（[核验记录](../middle_processing/vc_data/92_number_audit.md)）。两条经验：抽查的命中率不是 100%，所以必须做；最容易出错的不是数字本身，是数字的归属——这一轮撞到的两次问题，一次是评测对象对不上，一次是把「判定方式的通过率」当成了「模型的能力」，两次都不是打字错误，只有回原文才看得出来。本次补引用时又按同样方法逐条回原文，改正了若干处（[补引审计](../middle_processing/vc_data/ref_audit_overview.md)）。

引用的数字还有版本陷阱。同一个模型换脚手架能差 11.7 点（[Vibe Code Bench](https://www.vals.ai/benchmarks/vibe-code)），所以任何单点分数离开 Harness 版本都没有意义；几个公开榜单已经停更，上面标的 2026 年数字多数是厂商自报。本页凡是用到自报数字的地方都写明了出处性质。

## 参考文献

（按首次出现顺序；本项目内部记录以 KML 网关链接给出，不列入此表。）

1. [SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://arxiv.org/abs/2310.06770) — Carlos E. Jimenez 等，Princeton，2023-10-10
2. [WorldCoder-Bench: Benchmarking Physically Grounded 3D World Synthesis](https://arxiv.org/abs/2606.01869) — Shuo Lu 等，2026-06-01
3. [3JSBench 榜单](https://3jsbench.com/) — 3JSBench 站方，读取于 2026-10-15（改判版 2026-10-14）
4. [3JSBench Methodology](https://3jsbench.com/methodology) — 3JSBench 站方，读取于 2026-10-15
5. [WorldBench: Evaluating LLMs on Three.js Voxel World Generation](https://arxiv.org/abs/2610.10622) — Krish Bakshi 等，2026-10-07
6. [UI2Code^N: UI-to-Code Generation as Interactive Visual Optimization](https://arxiv.org/abs/2511.08195) — Zhen Yang 等，智谱，2025-11-11
7. [GLM-5V-Turbo: Toward a Native Foundation Model for Multimodal Agents](https://arxiv.org/abs/2604.26752) — GLM-V Team，2026-04-29
8. [Qwen3-VL Technical Report](https://arxiv.org/abs/2511.21631) — Shuai Bai 等，阿里 Qwen，2025-11-26
9. [MTAC-IFBench: Benchmarking Instruction-Following in Multi-Turn Agentic Coding](https://arxiv.org/abs/2609.14992) — Bosi Wen 等，2026-09-14
10. [SWE-bench 官方榜单（Bash Only）](https://www.swebench.com/) — SWE-bench 团队，读取于 2026-10-15
11. [A11yn: Aligning LLMs for Web Accessibility-Aware UI Generation](https://arxiv.org/abs/2510.13914) — Janghan Yoon 等，2025-10-15（v2 2026-09-07）
12. [Vision2Web: A Hierarchical Benchmark for Visual Website Development with Agent Verification](https://arxiv.org/abs/2603.26648) — Zehai He 等，2026-03-27
13. [Vibe Code Bench 实时榜（v1.1）](https://www.vals.ai/benchmarks/vibe-code) — Vals AI，2026-10-12
14. [3DHarnessBench: Probing Agentic 3D-to-Code Capabilities of Frontier Vision-Language Models](https://arxiv.org/abs/2609.06535) — Ling Liu 等，2026-09-06
15. [AutoLab: Can Frontier Models Solve Long-Horizon Auto Research and Engineering Tasks?](https://arxiv.org/abs/2606.05080) — Zhangchen Xu 等，2026-06-03
16. [VISTA: An End-to-End Benchmark for Visual Spec-to-Web-App Coding Agents](https://arxiv.org/abs/2605.26144) — JunJia Guo 等，2026-05-22
17. [Rubrics as Visual-Repair Context for Self-Evolving UI-to-Code Generation（RubSE）](https://arxiv.org/abs/2608.24138) — Tianyi Xiong 等，2026-08-25
18. [GPT-6 Astra System Card](https://deploymentsafety.openai.com/gpt-6-astra) — OpenAI，2026-09
19. [Claude Opus 5 System Card](https://www.anthropic.com/claude-opus-5-system-card) — Anthropic，2026
20. [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5) — Anthropic 官方文档，读取于 2026-10-15
21. [ProcessBench: Identifying Process Errors in Mathematical Reasoning](https://arxiv.org/abs/2412.06559) — Chujie Zheng 等，阿里 Qwen，2024-12-09
22. [RewardBench 2: Advancing Reward Model Evaluation](https://arxiv.org/abs/2506.01937) — Saumya Malik 等，AI2，2025-06-02
23. [FronTalk: Benchmarking Front-End Development as Conversational Code Generation with Multi-Modal Feedback](https://arxiv.org/abs/2601.04203) — Xueqing Wu 等，2025-12-05
24. [JAMER: Project-Level Code Framework Dataset and Benchmark on Professional Game Engines](https://arxiv.org/abs/2606.19830) — Jianwen Sun 等，2026-06-18
25. [Qwen3.8-27B 模型卡](https://huggingface.co/Qwen/Qwen3.8-27B) — 阿里 Qwen，读取于 2026-10-15
26. [Design Arena Leaderboard](https://www.designarena.ai/leaderboard) — Design Arena，读取于 2026-10-15
27. [LMArena WebDev 榜单镜像](https://www.respan.ai/models/benchmarks/lmarena-webdev-lmarena) — Respan（镜像 LMArena），快照 2026-10-08
28. [MiniMax M2.5 发布博客](https://www.minimax.io/news/minimax-m25) — MiniMax，2026
29. [axe-core Rule Descriptions](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md) — Deque Systems，读取于 2026-10-15
30. [LLM Critics Help Catch LLM Bugs（CriticGPT）](https://arxiv.org/abs/2407.00215) — Nat McAleese 等，OpenAI，2024-06-28
31. [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Anthropic 工程博客，2026-03-24
32. [Improving frontend design through Skills](https://claude.com/blog/improving-frontend-design-through-skills) — Anthropic Claude 博客，2025-11-12
33. [Designing delightful frontends with GPT-5.4](https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4) — OpenAI 开发者博客，2026-03-20
34. [GPT-5.6 发布页](https://openai.com/index/gpt-5-6/) — OpenAI，2026
35. [How to build games with Astra](https://developers.openai.com/blog/how-to-build-games-with-astra) — OpenAI 开发者博客，2026-09-04
36. [Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities](https://arxiv.org/abs/2507.06261) — Gheorghe Comanici 等，Google DeepMind，2025-07-07
37. [Kimi K2.5: Visual Agentic Intelligence](https://arxiv.org/abs/2602.02276) — Kimi Team，月之暗面，2026-02-02
38. [Kimi K3: Open Frontier Intelligence](https://arxiv.org/abs/2607.24653) — Kimi Team，月之暗面，2026-07-27
39. [The MiniMax-M2 Series: Mini Activations Unleashing Max Real-World Intelligence](https://arxiv.org/abs/2605.26494) — Aili Chen 等，MiniMax，2026-05-26
40. [MiMo-V2-Flash Technical Report](https://arxiv.org/abs/2601.02780) — Xiaomi LLM-Core Team，2026-01-06
41. [Frontend prompt instructions](https://developers.openai.com/api/docs/guides/frontend-prompt) — OpenAI 官方文档，读取于 2026-10-15
42. [playwright-interactive skill](https://github.com/openai/skills/tree/main/skills/.curated/playwright-interactive) — OpenAI，openai/skills 仓库，读取于 2026-10-15
43. [Automating eval design and hillclimbing with Claude](https://claude.dev/blog/automating-eval-design-and-hillclimbing/) — Anthropic，2026-10-07
44. [Claude Fable 5 / Mythos 5 System Card](https://www.anthropic.com/claude-fable-5-mythos-5-system-card) — Anthropic，2026
45. [AUV-Bench: Aesthetic Understanding and Generation Evaluation for User Interfaces](https://arxiv.org/abs/2609.34854) — Zhijie Deng 等，2026-09-28
46. [WebDevJudge: Evaluating (M)LLMs as Critiques for Web Development Quality](https://arxiv.org/abs/2510.18560) — Chunyang Li 等，2025-10-21
47. [Agreement Overstates Evidence: Error Dependence in LLM Judge Consensus](https://arxiv.org/abs/2609.22512) — Elias Hossain 等，2026-09-18
48. [Animation2Code: Evaluating Temporal Visual Reasoning in Video-to-Code Generation](https://arxiv.org/abs/2606.28593) — Anya Ji 等，2026-06-26
49. [webdev-arena-preference-10k 数据集](https://huggingface.co/datasets/lmarena-ai/webdev-arena-preference-10k) — LMArena，读取于 2026-10-15
50. [WebDev Arena 博客](https://arena.ai/blog/webdev-arena) — LMArena，读取于 2026-10-15
51. [SWE-Master: Unleashing the Potential of Software Engineering Agents via Post-Training](https://arxiv.org/abs/2602.03411) — Huatong Song 等，2026-02-03
52. [three.js examples/screenshots](https://github.com/mrdoob/three.js/tree/dev/examples/screenshots) — mrdoob/three.js 仓库，读取于 2026-10-15
53. [Babylon.js visualization tests](https://github.com/BabylonJS/Babylon.js/tree/master/packages/tools/tests/test/visualization) — BabylonJS 仓库，读取于 2026-10-15
54. [Blender render tests（GitHub 镜像）](https://github.com/blender/blender/tree/main/tests/files/render) — Blender Foundation，读取于 2026-10-15
55. [Qwen3 Technical Report](https://arxiv.org/abs/2505.09388) — An Yang 等，阿里 Qwen，2025-05-14
56. [Design2Code: Benchmarking Multimodal Code Generation for Automated Front-End Engineering](https://arxiv.org/abs/2403.03163) — Chenglei Si 等，Stanford，2024-03-05
57. [A2Z GameSpec-Bench: How Faithfully Can Coding Agents Generate Games from Game Design Specifications?](https://arxiv.org/abs/2609.39564) — Seonho Lee 等，2026-09-30
58. [Infinite Photorealistic Worlds using Procedural Generation（Infinigen）](https://arxiv.org/abs/2306.09310) — Alexander Raistrick 等，Princeton，2023-06-15

</div>

<div class="env-view" data-view="tasks" data-label="Tasks">

<nav class="toc view-toc"><h2>Contents</h2><ul><li class="l2"><a href="#tk-1"><span class="num">1</span> Rendering Repos Already Ship Their Own Pixel Baselines</a></li><li class="l2"><a href="#tk-2"><span class="num">2</span> The Rest of the Supply Is Blocked by Licence or Missing a Verifier</a></li><li class="l2"><a href="#tk-3"><span class="num">3</span> Verification Lands on State, Not on Code</a></li><li class="l2"><a href="#tk-4"><span class="num">4</span> Admission Testing Is Where Tasks Come From, Not Generation</a></li><li class="l2"><a href="#tk-5"><span class="num">5</span> The Verifier Must Not Know More Than the Problem Statement</a></li><li class="l2"><a href="#tk-6"><span class="num">6</span> The Admission Test Cannot See Its Own Two Blind Spots</a></li><li class="l2"><a href="#tk-7"><span class="num">7</span> Data Quality Is a Set of Numbers, Not a Review Meeting</a></li><li class="l2"><a href="#tk-8"><span class="num">8</span> Combinatorial Space Is Not Effective Diversity</a></li><li class="l2"><a href="#tk-9"><span class="num">9</span> The Bottleneck Is Not Compute</a></li></ul></nav>

<a class="anchor" id="tk-1"></a>

## 1 Rendering Repos Already Ship Their Own Pixel Baselines

渲染库的回归测试里早就躺着一批现成的 Verified Task。three.js、Babylon.js、Blender 这类仓库把「场景代码 + 参考图」一起提交进版本库，CI 渲染后逐像素比对。关键在于提交习惯：任何改变渲染行为的 PR 必须同时更新参考图，于是每一个这样的 commit 都自带一对数据——旧代码配新参考图必然失败，新代码配新参考图必然通过。这正是 [SWE-bench](https://arxiv.org/abs/2310.06770) 的 fail-to-pass 结构，只是测试换成了像素阈值，不需要 VLM judge。

核心发现：参考图的存量是万张量级，而改动过基线的 commit 是千条量级，后者才是任务供给的真实约束。

| 仓库 | 许可 | 参考图 | 改过基线的 commit | 测试机制 |
|---|---|---|---|---|
| [three.js](https://github.com/mrdoob/three.js/tree/dev/examples/screenshots) | MIT | 610 张，对应 611 个 example | 1,143 | [无头浏览器](https://github.com/mrdoob/three.js/tree/dev/test/e2e)渲染 400×250，像素阈值 0.1，差异像素上限 0.1%，注入确定性随机数与时钟，54 个 example 在豁免名单 |
| [Babylon.js](https://github.com/BabylonJS/Babylon.js/tree/master/packages/tools/tests/test/visualization) | Apache-2.0 | 975 张，对应 901 个测试 | 397 | 分 WebGL1 / WebGL2 / WebGPU 三套，338 个测试声明了排除引擎 |
| [Blender](https://github.com/blender/blender/tree/main/tests/files/render) | GPL | 2,596 张，对应 839 个场景文件，48 个类别 | 未统计（主仓库托管在 Gitea，表中链接为 GitHub 镜像） | cycles / eevee / workbench 各一套参考图 |
| [maplibre-gl-js](https://github.com/maplibre/maplibre-gl-js/tree/main/test/integration/render) | BSD-3 | 1,950 张 | 203 | 声明式样式配参考图 |
| [pixijs](https://github.com/pixijs/pixijs/tree/dev/tests/visual) | MIT | 1,711 张 | 249 | 视觉快照 |
| [primer/react](https://github.com/primer/react/tree/main/.playwright/snapshots) | MIT | 7,766 张 | 481 | 浏览器驱动的组件截图 |
| [Chart.js](https://github.com/chartjs/Chart.js/tree/master/test/fixtures) | MIT | 约 667 张 | 315 | fixture 配参考图 |
| [p5.js](https://github.com/processing/p5.js/tree/main/test/unit/visual) | LGPL-2.1 | 604 张 | 156 | 视觉单测 |
| [openlayers](https://github.com/openlayers/openlayers/tree/main/test/rendering/cases) | BSD-2 | 235 个 case | 291 | 入口脚本配参考图 |
| [deck.gl](https://github.com/visgl/deck.gl/tree/master/test/render/golden-images) | MIT | 252 张 | 178 | golden image |
| [plotly.js](https://github.com/plotly/plotly.js/tree/master/test/image/baselines) | MIT | 1,324 张 | 未取到（目录级接口只返回 1 条） | mock 配参考图 |

表中数字均为本项目用 GitHub / Gitea 接口实测：参考图读文件树计数，commit 数读 `commits?path=` 分页（[查询方法与原始记录](../middle_processing/vc_data/02_task_sources.md)；three.js、Babylon.js、Blender 三项另做过[独立复核](../middle_processing/vc_data/92_number_audit.md)）。

数据解读：9 个 GitHub 仓库（上表除 Blender、plotly.js）合计 3,413 个改过基线的 commit，参考图约 1.9 万张（[本项目实测汇总](../middle_processing/vc_data/02_task_sources.md) §1.1：commit 数按 `GET /repos/{repo}/commits?path={基线目录}&per_page=1` 读 Link 头末页页码，参考图按 `git/trees/{branch}?recursive=1` 过滤计数）。这个 3,413 是**上界，不是可用任务数**，原因有两条。第一，一部分 commit 只是整体重新生成截图（换浏览器版本、换字体、换 GPU 驱动都会触发），代码没动，构造不出 fail-to-pass 对。第二，像素基线对环境极度敏感，必须把浏览器、字体、渲染后端全部锁进同一个 Harness 镜像，锁不住的 commit 直接作废。结论是先做这一层：环境脚本现成、Verifier 确定、许可干净，three.js 加 Babylon.js 合计约 1,500 个 commit，Blender 另有 839 个场景。

<a class="anchor" id="tk-2"></a>

## 2 The Rest of the Supply Is Blocked by Licence or Missing a Verifier

离开像素基线仓库，供给立刻分化成两类：量大但要自建 Verifier，或者技术上完美但许可过不去。

| 级别 | 来源 | 可验证性 | 规模 | 许可风险 |
|---|---|---|---|---|
| S | [渲染库像素基线仓库](../middle_processing/vc_data/02_task_sources.md) | 仓库自带像素阈值 | 参考图约 1.9 万张，改基线 commit 3,413 个 | 低（Blender 为 GPL，需单独评估） |
| S | 带截图的 issue 加修复 PR（[SWE-bench Multimodal](https://arxiv.org/abs/2410.03859) 范式） | PR 自带单测 | 候选 issue 约 30 万（[GitHub 搜索实测](../middle_processing/vc_data/02_task_sources.md)），按实测转化率折算约 1,400 个 | 低，按仓库许可过滤 |
| A | [浏览器截图比对生态的长尾仓库](../middle_processing/vc_data/02_task_sources.md) | 高，但截图会漂移 | 估几千仓库、几万 PR | 低 |
| A | 程序化生成器（[Infinigen](https://arxiv.org/abs/2306.09310) 系，[仓库](https://github.com/princeton-vl/infinigen)） | 可确定性重渲 | 论文自报 182 个生成器乘无限种子 | 低（BSD） |
| A | [CodePen](https://blog.codepen.io/2016/11/25/10000000/) | 要自己截图造目标 | 1,000 万以上作品（官方 2016 年数字） | 低，公开作品默认 MIT（[官方说明](https://blog.codepen.io/documentation/licensing/)） |
| A | [js13kGames](https://js13kgames.com/sitemap.xml) | 要自建试玩 Verifier | 2,799 个（sitemap 实测） | 中，各作者自定 |
| B | [ShaderToy](https://www.shadertoy.com/)、[shaders21k](https://arxiv.org/abs/2211.16412) | 逐帧像素，最干净 | shaders21k 约 2.1 万个程序；ShaderToy 全站总数未能核实 | 高，默认 NC-SA（二手口径，官方 [terms](https://www.shadertoy.com/terms) 未能实测） |
| B | Blender StackExchange、图形类问答标签 | 要补 Verifier | `python` 加 `scripting` 两个标签约 2 万个问题（[API 实测](https://api.stackexchange.com/2.3/tags/python;scripting/info?site=blender)） | 中，数据 dump 条款限制 LLM 训练（[heise](https://heise.de/-9823083)） |
| B | 设计稿站点 | 设计稿当目标图 | 中等 | 中，robots 点名禁 AI 爬虫（[Figma robots](https://www.figma.com/robots.txt)）或禁止再分发设计稿（[Frontend Mentor FAQ](https://www.frontendmentor.io/faqs)） |
| C | 作品展示站、付费资产站 | 没有源码 | — | 高（[逐站记录](../middle_processing/vc_data/02_task_sources.md)） |

数据解读：带截图的 issue 数量看着有 30 万，但端到端转化率是千分之几。[SWE-bench Multimodal](https://arxiv.org/abs/2410.03859) 的实测是 13.5 万 PR 筛到 1,478 个候选、最后 617 个实例，折合 0.457%；按同样的转化率，30 万候选只能出约 1,400 个任务，是千量级不是万量级。这个口径和后面讲产能时 three.js 漏斗算出的约 230 个任务（[本项目估算](../middle_processing/vc_data/13_scaling_tasks.md)）是一致的——真实素材的产出量级就是三位到四位数。ShaderToy 是全表技术上最好的 shader 源——逐帧像素就是确定性 Verifier——但默认许可是非商用，这一条单独把它踢出训练池。云端托管的视觉回归服务（[Chromatic](https://www.chromatic.com/)、[Percy](https://percy.io/) 一类）同理排除：基线存在服务商那边，仓库里根本不存在。

预训练与中训练阶段的「代码配渲染图」是另一套供给，它的上限比任务池更早见底。公开可复用的配对总量约 1,000 万条（[本项目汇总](../middle_processing/vc_data/09_pretrain_data.md)），其中真实页面且可渲染的只有 [WebCode2M](https://arxiv.org/abs/2404.06369) 一家（[HF 实测](https://huggingface.co/datasets/xcodemind/webcode2m) 317 万行，[净化版](https://huggingface.co/datasets/xcodemind/webcode2m_purified) 256 万行）。合成数据的分布缺口是硬的：[WebSight](https://arxiv.org/abs/2403.09029) 平均 647 个 token、19 个标签、DOM 深度 5，而 WebCode2M 清洗后的真实页面是 5,366 个 token、184 个标签、深度 15，[Design2Code](https://arxiv.org/abs/2403.03163) 收的原始 C4 页面更是 31,216 个 token（WebCode2M 表 2）。同架构同规模对照下，合成数据训练后在真实测试集上的 TreeBLEU 是 0.06，真实数据是 0.35（WebCode2M 表 3）。合成数据还会腐烂：[WebSight](https://huggingface.co/datasets/HuggingFaceM4/WebSight) 的图片一律引用一个随机图床域名，该域名 2026-10-15 [实测返回 503](../middle_processing/vc_data/09_pretrain_data.md)，这批数据已无法按原样重渲。3D 侧更干脆——[Objaverse-XL](https://arxiv.org/abs/2307.05663) 论文自报 1,020 万个去重对象（HF 元数据 1,085 万行），里面没有一行可执行代码，它索引的 12 种扩展名全是几何资产格式（[仓库](https://github.com/allenai/objaverse-xl)，[本项目核对](../middle_processing/vc_data/09_pretrain_data.md)），只能当逆向任务的目标图，不能当「代码到图」的正样本。

<a class="anchor" id="tk-3"></a>

## 3 Verification Lands on State, Not on Code

一个 Verified Task 的最小描述是五元组：初态、Problem Statement、对模型公开的观察接口、对模型隐藏的断言集、参考解。reward 只看任意实现能否把初态推到满足断言的状态，不看它和参考解像不像。

这不是风格偏好，是被等价实现逼出来的。多份不同的 CAD 脚本能产出几何等价的模型，SFT 学不动这件事，所以 [CAD-Coder](https://arxiv.org/abs/2505.19713) 在 RL 阶段改用几何距离（Chamfer）做奖励。把参考解当整体对照打分的做法也实测更差：[Rubrics as Rewards](https://arxiv.org/abs/2507.17746) 在 HealthBench 上，让 judge 拿参考答案做 Likert 对照是 31.7%，先用参考答案生成逐条 rubric 再打分是 35.9%（表 1）。

### 3.1 Eight Paradigms, Ranked by What They Cannot See

| 范式 | 目标来源 | 主要观察层 | 最大短板 |
|---|---|---|---|
| fail-to-pass 与 pass-to-pass | 参考解的状态 | 状态与结构 | 断言覆盖不到即漏检 |
| 逆向构造（从渲染图出发） | 已有产物的渲染 | 像素与几何 | 机制不可见，一图多解 |
| 变异扰动（破坏正确产物） | 参考解的状态 | 状态 | 变异分布偏离真实错误 |
| 需求编译为 rubric | 需求加参考解辅助 | 全部，逐条标层 | judge 幻觉 |
| 交互行为测试 | 隐藏行为契约 | 动作前后的状态差分 | 契约编写成本高 |
| 属性与不变量 | 通用性质 | 状态与几何 | 不判需求是否满足 |
| 开放偏好对比 | 组内两两比较 | 像素与录屏 | 不判功能，成本是组大小的平方 |
| 难度与质量筛选 | 当前 policy 的通过率 | — | 依赖 policy 能力，需周期重跑 |

数据解读：前六种都能落到程序化信号上，后两种只能做兜底。选哪一层不是自由选择，而是被「这个需求的信息藏在哪」决定的。截图看不到物理和状态机，DOM 看不到画在画布里的东西——[WorldCoder-Bench](https://arxiv.org/abs/2606.01869) 在 1,434 对产物上实测，DOM 打分与隐藏状态真值的 Kendall τb 是 −0.021，截图加 VLM 是 −0.068，隐藏状态契约本身就是真值（1.000）；严重缺陷的误放率，DOM 33.7%、8 步 agent 式检查 45.6%、状态契约为 0（表 2）。

### 3.2 Reference Code Has Exactly Five Jobs

开发者写死的代码不是标准答案，它可能冗余、过时、性能差。拿代码相似度当奖励会把这些缺点一起学进去。它有五个正确用途（本项目设计，整理见 [03 可验证构造](../middle_processing/vc_data/03_verifiable_construction.md) §3.1，准入实现见 [gen_tasks.py](../scripts/vc_verifier/proto/gen_tasks.py)）：

1. **证明可解**。参考解必须在 Harness 里跑通并通过全部断言，重复 3 次稳定（对应 [SWE-bench](https://arxiv.org/abs/2310.06770) 的 gold patch 规则与 [GameDevBench](https://arxiv.org/abs/2602.11103) 的已验证参考解）；做不到，问题在 Verifier 或题目，不在 policy。
2. **生成断言与 rubric**。从参考解的运行状态抽断言，把它的渲染结果交给 rubric 生成器，产出「桌面上有 4 把椅子、间距大致相等」这类可观察条目，而不是「和参考截图一样」。
3. **当可破坏的底子**。对参考解注入缺陷得到初态，修复题和 Verifier 校准集一起产出。
4. **校验 Verifier**。参考解必过、初态必挂、变异体必挂，三条任一不满足就先修 Verifier。
5. **SFT 冷启动**。它是多条合格轨迹之一，不进 RL 的 reward（同 [CAD-Coder](https://arxiv.org/abs/2505.19713) 的 SFT 再 GRPO 两阶段）。

参考解应被当作下界：reward 只要求满足断言，超过参考解不受惩罚。把它放进开放维度的组内比较池当锚，统计 policy 解对它的胜率；胜率持续很高的题说明参考已经不是好参考，用通过全部断言且胜率最高的 rollout 替换它，并重跑准入测试。

<a class="anchor" id="tk-4"></a>

## 4 Admission Testing Is Where Tasks Come From, Not Generation

让 LLM 在一个能跑的页面上提出若干语义性破坏，再附一句用户视角的需求，这一步很便宜。贵的是判断哪些破坏值得收。我们自己的流程（[gen_tasks.py](../scripts/vc_verifier/proto/gen_tasks.py)）是三条准入测试全过才收：参考解必须过 Verifier（自比自，防 Verifier 本身坏掉）、破坏版必须被判挂（否则这个破坏不可验证）、被替换的代码片段必须在源码中唯一（防止改到别处）。

核心发现：LLM 提的破坏里约有一成是 Verifier 根本看不出来的（桌子 1/10，工作台补层前 2/16），准入测试把它们挡在数据集外，比事后在 RL 里发现噪声便宜得多（[实验记录](../middle_processing/vc_data/90_local_experiments.md) §4）。

下面这个 demo 是那一轮造题的真实产物。默认停在被挡掉的那一条：模型提议把杯子整个倒过来，需求写得也合理，但杯子是一个圆台，倒过来之后占据的空间几乎没变，Verifier 判不出来，于是这道题被丢弃。

<iframe class="demo-frame" style="height:430px" src="demos/task-admission.html" loading="lazy"></iframe>

| 场景 | LLM 提 | 收 | 弃 | 弃的原因 |
|---|---|---|---|---|
| 桌子加杯子 | 10 | 9 | 1 | 杯子倒置：杯子是圆台，翻转后占据几乎不变 |
| 桌面工作台（13 个 mesh，带层级和旋转） | 16 | 14 → 16 | 2 → 0 | 立杆缺失、灯臂镜像；补上连通块统计后都能抓到 |

来源：[本项目实验记录](../middle_processing/vc_data/90_local_experiments.md) §4。

数据解读：弃掉的 case 不是损失，是 Verifier 的体检报告。它精确指出了两处盲区——轴对称部件翻转后占据不变、细长部件在全局 IoU 里权重太小。其中细长部件这一条直接催生了一个新的检查层：按颜色统计连通块数与体积比。补上之后，前面两组共 29 个带标签变异仍然全部判对，零新增误杀（[实验记录](../middle_processing/vc_data/90_local_experiments.md) §2.1，[mutate.py](../scripts/vc_verifier/proto/mutate.py)）。这说明盲区是被具体 case 逼出来的，设计阶段想不出来；先造题再补 Verifier，比先定 Verifier 再造题有效。

收下来的 16 个任务按挂在第几层分布：6 个挂在多视角剪影层，8 个挂在按颜色的体素占据层，2 个挂在部件与拓扑层（[实验记录](../middle_processing/vc_data/90_local_experiments.md) §4.1）。这个分布本身就是难度分布的粗略代理——挂在第一层的是一眼可见的粗错，挂在最后一层的是细节错。

<a class="anchor" id="tk-5"></a>

## 5 The Verifier Must Not Know More Than the Problem Statement

预实验里 opus-5.5 在 9 个桌子任务上一轮过 7 个。两个没过的，查下来都不是模型的问题（[实验记录](../middle_processing/vc_data/90_local_experiments.md) §5）。

| 任务 | 需求原文 | Verifier 实际要求 | 结果 |
|---|---|---|---|
| 杯子颜色 | 杯子应使用有别于桌面木色的独立颜色 | 必须恰好是参考里那一种蓝 | 模型换了另一种颜色，该色体素 IoU 为 0，判挂 |
| 桌腿位置 | 桌腿应位于桌面四个角落附近 | 腿的位置要和参考几乎重合 | 模型把腿放到角上但缩进量不同，剪影 0.885 差一点点，判挂 |

数据解读：两次失败的根因同一条——Verifier 能查的信息量超过了 Problem Statement 给出的信息量。这类任务不是难，是不可解；进了 RL 就是纯噪声，而且会被误读成模型能力不足。两条解法：把参考渲染图放进 Problem Statement，让它变成信息补齐后的复刻任务；或者把 Verifier 放松到与描述同精度，例如判「颜色与木色的距离大于阈值」而不是「等于某个具体值」。第一条更好做也更可扩展，正好对应 Problem Statement 带多模态参考这个设定，所以在实验矩阵里作为独立一维（纯文本需求对文本加参考视角图）来测。

同一条纪律的另一面是断言不得依赖参考解的实现细节。[SWE-bench](https://arxiv.org/abs/2310.06770) 原始规则里就排除了「测试调用了解法新建的函数或类」的实例，因为命名任意、无法从题面推出。需要的锚点必须写进对模型公开的观察接口里：交互元素的标识约定、状态结构的 schema、必须保留的对象名。锚点公开，断言隐藏。

<a class="anchor" id="tk-6"></a>

## 6 The Admission Test Cannot See Its Own Two Blind Spots

前面那三条准入闸——参考解必过、破坏版必挂、被替换的片段唯一——挡掉了 Verifier 看不见的破坏。它们挡不住另外两件事，而且结构上挡不住。

**第一件：三条闸全过的任务仍然可能无解。**

闸的逻辑摆出来就清楚了。参考解当然过，它就是答案；破坏版当然挂，它就是故意做坏的；片段唯一只管别改错地方。没有任何一条在问「只拿着题面，这道题能做出来吗」。

本项目的实测频率不低：桌子那批 9 个任务里 2 个不可解（[实验记录](../middle_processing/vc_data/90_local_experiments.md) §5），Blender 留出集 7 个里 1 个（[Blender 记录](../middle_processing/vc_data/10_blender_tasks.md) §3.3）。合计 3/16，按两成算，十万任务里就有两万道持续向 RL 注入噪声。

更糟的是它和难度筛选形成正反馈。不可解题的通过率稳定在 0 附近，看起来就像「很有挑战性」，于是难度带筛选不但不会剔掉它们，反而会优先保留（本项目在一道 0% 题上撞到过这种情况，见[实验记录](../middle_processing/vc_data/90_local_experiments.md) §6.3）。

**修法是加第四条闸，查题面的可解性，而不是查产物。** 下面四步是本项目设计、尚未实现（相关的 ceiling check 设计见 [13 规模化](../middle_processing/vc_data/13_scaling_tasks.md) §2.3.6）：

1. 让一个与 Verifier 无关的模型只看 Problem Statement，枚举「你觉得验收会查哪些点」，输出一张清单。
2. 和真实断言集做匹配，算召回：被猜到的断言数除以断言总数。
3. 召回低于某个线的任务退回，未被猜到的那几条断言要么删掉，要么把对应信息补进题面。
4. 先在已有任务上校准——三道已知不可解的题是现成的金标准，这条闸抓不出它们就说明实现有问题。

成本是每道题多一次模型调用。按[本项目成本模型](../middle_processing/vc_data/13_scaling_tasks.md) §5.6，每个候选平均约 4.5 次调用（121 万次 / 26.9 万候选），这条闸的增量约两成。

**第二件：准入测试会把训练集偏向 Verifier 已经擅长的那类错误。**

被丢掉的破坏，是 Verifier 看不见的那些。留下来的破坏，是 Verifier 看得见的那些。一轮下来数据集很干净，代价是它系统性地不含「Verifier 的盲区」这一类问题。拿它训出来的模型，学会的是修 Verifier 看得见的毛病。

这件事没有干净的解法，但有一个便宜的体检：关掉某一层信号，重跑一遍准入，看收下来的任务少了多少、少的是哪一类。少得越多，说明数据集越依赖那一层，也就越偏向那一层能看见的错误。

核心发现：两个场景上各做一次留一层消融，依赖集中在体素层与部件层，而且它们各自独占了一部分任务类型。

| 关掉哪一层 | 桌面工作台（16 个提议） | 桌子加杯子（10 个提议） |
|---|---|---|
| 不关，全部信号 | 收 16 | 收 9 |
| 多视角剪影 | 收 16 | 收 9 |
| 体素占据 | 收 14 | 收 8 |
| 自洽性 | 收 16 | 收 9 |
| 部件与拓扑 | 收 14 | 收 9 |

来源：[本项目实验记录](../middle_processing/vc_data/90_local_experiments.md) §8，脚本 [ablate.py](../scripts/vc_verifier/proto/ablate.py)。

数据解读：关掉多视角剪影和自洽性，收下来的任务一个不少——不是因为这两层没用，而是它们抓的那些粗错误，别的层也能抓到。真正不可替代的是体素占据和部件与拓扑：各自独占两道题。换句话说，**如果当初没有加部件与拓扑这一层，训练集里就会少掉「细长部件缺失」这一类问题，而模型永远学不到修它。** 这个消融应该在每次改动 Verifier 之后都跑一遍，它量的不是判别力，是数据集的偏向。

<a class="anchor" id="tk-7"></a>

## 7 Data Quality Is a Set of Numbers, Not a Review Meeting

可解率只证明「参考解能过」，判别力证明「错的过不了」。两者都要，而判别力是最常被跳过的那一项。

| 指标 | 怎么算 | 门槛 | 依据 |
|---|---|---|---|
| 可解率 | 参考解通过全部断言，3 次重复取交 | 每题 100% | [SWE-bench](https://arxiv.org/abs/2310.06770) 的 gold patch 规则；[GameDevBench](https://arxiv.org/abs/2602.11103) 每题带已验证参考解 |
| 非平凡率 | fail-to-pass 断言在初态上全部失败；空解与静态截图解也必须失败 | 每题 100% | [SWE-bench](https://arxiv.org/abs/2310.06770) 的 fail-to-pass 定义 |
| 变异杀死率 | 被断言判失败的变异体占比 | 不低于 95%，未杀死的逐个审 | [WorldCoder-Bench](https://arxiv.org/abs/2606.01869) 的契约准入 |
| 替代实现通过率 | 已知正确的不同实现通过断言的比例 | 不低于 90%，过低说明断言绑了实现细节 | [CodeContests+](https://arxiv.org/abs/2506.05817) 的 TPR / TNR 口径 |
| 单条断言区分度 | 能区分最终判对与判错 rollout 的断言占比 | 为 0 的断言删除或改写 | [R2E-Gym](https://arxiv.org/abs/2504.07164)：多数任务里有区分力的测试不到 20% |
| 难度分布 | 当前 policy 采 k 次的通过率分桶 | 训练池以通过率严格落在 0 与 1 之间为主 | [DAPO](https://arxiv.org/abs/2503.14476) 的动态采样 |
| 重测一致性 | 同一产物重复验证 3 次结果不一致的比例 | 不超过 1%，超出先修时钟、种子与软件光栅 | [本地 Harness 的确定性实测](../middle_processing/vc_data/06_harness.md) §4.1 |
| 人审缺陷率 | 抽样人审中大问题比例 | 不超过 5% | [GameDevBench](https://arxiv.org/abs/2602.11103) 首轮人审 41 题：43% 无问题、50% 小问题、7% 大问题 |
| 污染率 | 与评测集的 n-gram 与 embedding 相似度超阈值比例，外加时间切分 | 0，命中即删 | [SWE-rebench](https://arxiv.org/abs/2505.20411) 的持续更新去污染 |

数据解读：R2E-Gym 的那一行是全表最该警惕的——「有测试」和「测试能分对错」是两件事，多数任务里能区分正误补丁的测试不到 20%（[R2E-Gym](https://arxiv.org/abs/2504.07164) 图 5 与正文），这些任务在 RL 里贡献的梯度接近噪声。[GameDevBench](https://arxiv.org/abs/2602.11103) 的 43% 则给出了自动出题的现实基线（首轮人审 41 题）：agent 出的题首轮只有 43% 完全干净，一半有小问题（场景跑到镜头外、断言了指令没要求的东西）。两个数字合起来说明一件事：造题环节的产出必须当候选看，准入测试才是真正的生产线。

这些指标还要周期重算。policy 变强后，原本通过率在 0 与 1 之间的题会变成全对；新的作弊方式也会出现，变异算子集需要跟着补。没有一组固定的 reward 能随 policy 能力增长一直有效（[The Verification Horizon](https://arxiv.org/abs/2606.26300) 引言的核心结论：「no fixed reward function can remain effective as policy capability continues to grow」）。

<a class="anchor" id="tk-8"></a>

## 8 Combinatorial Space Is Not Effective Diversity

程序化生成器报出来的「规模」几乎全是组合计数。[Infinigen](https://arxiv.org/abs/2306.09310) 自报 182 个生成器、1,070 个可解释自由度，论文自己把这个计数称作总体多样性的 proxy（表 2），全文没有做任何覆盖度、最近邻距离或成对相似度度量。[ProcTHOR](https://arxiv.org/abs/2206.06994) 自报可出 1,000 亿种以上 layout，同样零多样性度量。

核心发现：组合计数不但无信息量，还和下游收益脱钩——而且脱钩的方向是反的。

| 证据 | 数字 | 说明 |
|---|---|---|
| [ProcTHOR](https://arxiv.org/abs/2206.06994) 自己的规模消融（表 3） | 房屋数 10 / 100 / 1,000 / 10,000 对应 HM3D 零样本成功率 1.60% / 10.4% / 4.65% / 9.70% | 非单调，1,000 房比 100 房更差 |
| [HSSD-200](https://arxiv.org/abs/2306.11290v1) 对照 | 122 个高保真场景的 HM3DSem 零样本成功率 19%，ProcTHOR 的 10,000 个是 17%（v1 正文；v3 表 5 修订为 19.2% 对 12.5%） | 场景数差 82 倍，方向相反 |
| ProcTHOR 自己扩产的微调收益（[HSSD v3](https://arxiv.org/abs/2306.11290) 表 6） | 122 扩到 10,000 后，微调成功率 / SPL 从 48.48 / 22.79 变 48.32 / 21.80 | 82 倍扩张零增益甚至退化 |
| 本项目 Blender 槽位表算术（[记录](../middle_processing/vc_data/13_scaling_tasks.md) §1.3.5） | 组合空间 7.0e8，渲染后能被 Verifier 分开的等价类约 1.6 万 | 折损 4.4 万倍 |

数据解读：组合空间与有效多样性有干净的定义差别，就是 Hill number 的 q=0 与 q=1（[Cousins of the Vendi Score](https://arxiv.org/abs/2310.12952)），后者即 [Vendi Score](https://arxiv.org/abs/2210.02410)。前者只数有多少种取值组合，后者按实际分布加权，等价于「有效类别数」。本项目槽位表里最极端的一个槽位是灯泡功率：采样空间有 19 档，而在 Workbench 渲染下 Verifier 一档也分不出来，有效档数是 0（[记录](../middle_processing/vc_data/13_scaling_tasks.md) §1.3.5）。这类「采样空间里有、渲染后看不见」的槽位必须禁止进入场景规格，否则它直接制造上一节那种不可解任务。4.4 万倍的折损同时给出一个工程结论：单模板做不到十万，十万量级必须靠模板数与跨模板组合，而跨模板组合的价值在于它造出的空间关系不在任何单模板的槽位域里。

度量这件事本身有个陷阱：不要用通用视觉嵌入做多样性或去重判据。[DataComp](https://arxiv.org/abs/2304.14108) 实测，copy-detection 专用描述子在精确率 0.9 时召回 0.8，而 CLIP ViT-B/32 在同样精确率下召回只有 0.02。Density 与 Coverage 这一代指标的[原作者](https://arxiv.org/abs/2002.09797v1)也给了同向结论：在远离 ImageNet 统计的域上，随机初始化的 64 维嵌入比预训练特征更合理——MNIST 上 Coverage 从 0.108 升到 0.714，音频域从 0.020 升到 0.653（v1 表 1）。程序化 3D 场景离自然图像分布很远，预训练视觉特征会把一切压成一团。这与 Verifier 一侧「别拿嵌入相似度当质量闸」是同一条纪律的两个面。可用的替代是探针已经产出的几何标量：mesh 数、顶点数分位、包围盒体积比、颜色多重集直方图、连通块数、开放边界边数、层级深度，拼成二三十维的低维特征，去重与多样性验收共用一组。

在讨论怎么分桶之前，先看一下自动生成的任务**实际上**是什么难度分布。先看一个跨模型汇总的版本（10 道题，每道题汇总 23 到 32 次首轮尝试，跨 4 个模型、两种问题描述，[实验记录](../middle_processing/vc_data/90_local_experiments.md) §9）——注意这个口径后面会被推翻：

核心发现：单处破坏型任务的难度分布是双峰的，中间是空的。

| 通过率 | 任务数 |
|---|---|
| 0 到 0.1 | 2 |
| 0.1 到 0.3 | 2 |
| 0.3 到 0.7 | **0** |
| 0.7 到 0.9 | 2 |
| 0.9 到 1.0 | 4 |

来源：[本项目实验记录](../middle_processing/vc_data/90_local_experiments.md) §9。

数据解读：十道题的通过率依次是 0、0.04、0.26、0.27、0.73、0.77、0.91、0.93、1.0、1.0。模型要么会修，要么完全不会，中间带是空的。这对课程规划有两个直接后果。第一，剔除全对与全错之后还剩七成，这个数看着健康；但如果按常见的 0.3 到 0.7 收紧，**一道题都留不下**。第二，成本模型里「难度带留存」这个最敏感的外推项，取值完全由带宽决定，不是一个可以拍的常数（逐题数据见[实验记录](../middle_processing/vc_data/90_local_experiments.md) §9）。

但上面那个口径对成本模型是错的，而且错的方向固定是乐观。零梯度是按组判的，组内全是**同一个策略**，所以要用的量是单一策略的 pass@k。跨模型汇总会把「强模型会、弱模型不会」混成一个中间通过率，**凭空制造出并不存在的中等难度**。

换成严格的 pass@8（16 道题、单一模型、温度 1.0、每题独立采 8 次，共 128 次，[实验记录](../middle_processing/vc_data/90_local_experiments.md) §15，脚本 [passk.py](../scripts/vc_verifier/proto/passk.py)）：

核心发现：13 道题是全有或全无，0.3 到 0.7 带内一道都没有（[实验记录](../middle_processing/vc_data/90_local_experiments.md) §15）。

| 通过次数 | 任务数 |
|---|---|
| 0/8 | 5 |
| 1/8 | 2 |
| 2/8 到 6/8 | 1 |
| 7/8 | 0 |
| 8/8 | 8 |

来源：[本项目实验记录](../middle_processing/vc_data/90_local_experiments.md) §15，脚本 [passk.py](../scripts/vc_verifier/proto/passk.py)。

数据解读：剔除全对与全错后只剩 3/16 = 19%，Wilson 95% 区间是 6.6% 到 43.0%（[实验记录](../middle_processing/vc_data/90_local_experiments.md) §15；区间本轮按 Wilson 公式复算一致）。**即便取上界 43%，也仍低于成本模型假设的 60%**——这个假设站不住不是因为样本少，是方向就错了。两种口径差约 3.7 倍（70% 对 19%），所以估 RL 的零梯度比例只能用**将要训的那个策略自己**的 pass@k，不能用跨模型汇总。

根因在任务的造法：只改一处的破坏，要么模型看出来了就改对，要么没看出来就全错，不存在「部分做对」的中间态。要拿到中间难度，得换造法——多处缺陷叠加、或者从零构建而不是修复。这一条在规划十万任务之前就得定下来，因为它决定的是任务形态，不是筛选参数。

需要打的折扣：这十道题的样本是跨模型汇总的，混进了模型强弱；真正的 pass@k 要逐模型算，而每个模型每题只有 7 到 8 次，不够。但「中间带是空的」这个形状在逐模型的数据里同样成立（[实验记录](../middle_processing/vc_data/90_local_experiments.md) §9 的折扣说明）。

分桶本身还有一个数学事实：硬边界的桶做不到。

| 真实通过率 | n=4 | n=8 | n=16 | n=32 | n=64 |
|---|---|---|---|---|---|
| 0.10 | 5.2% | 3.8% | 1.7% | 0.1% | 0.0% |
| 0.25 | 26.2% | 32.1% | 37.0% | 26.3% | 15.6% |
| 0.35 | 68.9% | 45.3% | 29.1% | 26.8% | 22.5% |
| 0.50 | 62.5% | 28.9% | 7.7% | 2.0% | 0.2% |
| 0.75 | 26.2% | 32.1% | 37.0% | 26.3% | 15.6% |
| 0.90 | 5.2% | 3.8% | 1.7% | 0.1% | 0.0% |

数据解读：表里是三档桶（易、中、难按 0.3 与 0.7 切）的误分率，本项目精确枚举（[记录](../middle_processing/vc_data/13_scaling_tasks.md) §2.1 表 C）。桶中心和桶外都能分准，桶边界附近分不准：真实通过率 0.35 时，n=8 的误分率 45.3%，n=64 仍有 22.5%，而且几乎不随采样次数下降。原因很直接——真值恰在边界上时本来就是 50 比 50，这部分方差不可能靠加采样消除。公开对照印证同一结论：[难度标签可靠性研究](https://arxiv.org/abs/2609.40115)实测 n=16 的难度集合在两次独立构建之间的 Jaccard 复现性只有 0.727，要到 0.90 需要 242 次采样（外推）。所以难度标定只做粗闸，两段式先 n=2 筛掉全对全错、存活者补到 n=8，之后用软权重而不是硬桶。

课程学习里真正值钱的是双边过滤。[DAPO](https://arxiv.org/abs/2503.14476) 的动态采样在累加消融路径上值 8 分（表 1，42 到 50），是单个改动里最大的一项；唯一做了完整阈值扫描的工作（[Online Difficulty Filtering](https://arxiv.org/abs/2504.03380) 表 1）给出更细的拆解：只剔除全对全错值 1.0 个点（26.3 到 27.3），再把保留区间收紧到通过率 0.3 到 0.7 多拿 2.8 个点（27.3 到 30.1），收到 0.4 到 0.6 回落到 29.9。而只切一边的五个设置（23.8 到 25.9）全部低于不过滤的 26.3；训练前一次性离线筛题（用外部模型或初始模型当难度代理）只到 26.3 到 28.4，低于在线双边过滤的 30.1。还有一个容易自相矛盾的配置：标准差归一化会给几乎全对或几乎全错的题加权（[Dr. GRPO](https://arxiv.org/abs/2503.20783)），方向与动态采样正好相反，两者同时开而不自觉，等于一边筛掉一边加权。

最后一条纪律是把「难」和「坏」分开，而且不能靠人工标注。人判「这题欠规约吗」的 Krippendorff α 只有 0.24（[SPICE](https://arxiv.org/abs/2507.09108) 重算 OpenAI 公开的 SWE-bench Verified 标注），而判「这题多难」是 Fleiss kappa 0.78（[SWE-bench Multimodal](https://arxiv.org/abs/2410.03859) 的难度标注），低了一个量级。可用的替代是响应模式统计：用难度标定已经采出的 rollout 算 item-total 相关，低或负的相关说明单维假设被违反、该题可疑；[实测](https://arxiv.org/abs/2511.16842)在九个 benchmark 上送审前 50 题的精确率最高 84%，1,000 题跑一分钟，而且复用现成 rollout，零额外采样。本项目自己撞过这条线的另一面：桌子那批任务里两道没过的题，查下来不是题难，是 Verifier 查了题干没给的字段（[实验记录](../middle_processing/vc_data/90_local_experiments.md) §5）；Blender 留出集 7 个里也有 1 个同因（[Blender 记录](../middle_processing/vc_data/10_blender_tasks.md) §3.3）。单看通过率会把它们判成「超难题」留在池里，持续注入噪声。

<a class="anchor" id="tk-9"></a>

## 9 The Bottleneck Is Not Compute

真实素材挖掘的端到端留存率是千分之几到百分之几，这个量级是文献共识，不是悲观假设。

| 管线 | 起点 | 端到端留存 | 产出 |
|---|---|---|---|
| [SWE-bench](https://arxiv.org/abs/2310.06770)（表 10） | 93,139 个 PR | 2.46% | 2,294 |
| [SWE-rebench](https://arxiv.org/abs/2505.20411) | 约 45 万个下载的 PR | 4.74% | 21,336 |
| [SWE-Gym](https://arxiv.org/abs/2412.21139) | 64,689 条候选 | 3.77% | 2,438 |
| [Design2Code](https://arxiv.org/abs/2403.03163) | 127.9k 个网页 | 0.38% | 484 |
| ShaderMatch（[Shadereval](https://huggingface.co/datasets/Vipitis/Shadereval-inputs)） | 20.2 万个未过滤函数 | 0.23% | 467 |
| [SWE-smith](https://arxiv.org/abs/2504.21798)（合成变异） | 100,074 个 bug 候选 | 50.1% | 50,137 |
| [本项目自动造题准入](../middle_processing/vc_data/90_local_experiments.md) | 26 条破坏提案 | 88% 到 96% | 25 |

数据解读：瓶颈不在筛选质量，在「能不能跑起来」。SWE-rebench 自己点名安装与执行验证这一步只有约 14% 通过，只有 31% 的仓库能装成至少一个任务。按本项目口径把这条漏斗算到 three.js 上（[记录](../middle_processing/vc_data/13_scaling_tasks.md) §4.2.5）：2,401 个仓库（GitHub 搜索 `topic:threejs stars:>10` 实测），抽自包含页面约 20%，无头浏览器能跑起来并渲出至少一个 mesh 约 60%，场景捕获成功约 95%，冻结时钟后两次渲染逐字节一致约 70%，自动造题加准入约 90%，去重与难度带约 45%，端到端约 3.2%。按每仓库平均挖出 3 个可用页面估，只能出约 230 个任务——三位数，不是五位数。除仓库数与准入率外，这条漏斗的各步留存都是估计值。

所以真实素材与合成的配比不是选择题。真实素材客观上只能占千分之几的条数，合成必然在 95% 以上。collapse 一线的理论对这件事不直接适用：最悲观的结论（[Strong Model Collapse](https://arxiv.org/abs/2410.04840)）说合成占 1% 即可触发退化，但前提是替换式自噬迭代且不做筛选；有界误差的那篇（[Is Model Collapse Inevitable?](https://arxiv.org/abs/2404.01413)）给出的决定性变量是协议而非比例——累加而不是替换，加上 Verifier 筛选（[Beyond Model Collapse](https://arxiv.org/abs/2406.07515)），两条满足时工程上约 30% 的合成占比仍不掉点（[Nemotron-CC](https://arxiv.org/abs/2412.02595)：全量 6.3T token 里 1.9T 为合成，MMLU 与 DCLM 持平）。本项目这两条天然满足：标签来自程序化信号而不是模型，模型只提供破坏提案和题干措辞；准入测试本身就是 Verifier 筛选。所以真实素材的 KPI 应该改成「在有效多样性口径下贡献至少 20%」，而不是条数占比；达不到就说明反推需求做烂了，只是把真实素材重新表述成了模板本来就能出的东西。

成本模型是推算，假设逐条写明（[记录](../middle_processing/vc_data/13_scaling_tasks.md) §5.2）。准入三条取 0.97 / 0.90 / 0.95，去重 0.85，可解性闸 0.88——这五步合计留存 62%。最后一项「难度带留存」原先按 0.60 外推，**本项目实测把它打到了 0.19**（见上，[实验记录](../middle_processing/vc_data/90_local_experiments.md) §15）。

| 项 | 按 0.60 外推 | 按实测 0.19 |
|---|---|---|
| 漏斗总留存 | 37.2% | 11.8% |
| 造 10 万任务需要的候选 | 26.9 万 | **84.8 万** |
| 探针调用 | 约 160 万次 | 约 500 万次 |

数据解读：按单处破坏这一种造法，规模化成本要乘以 3.2（37.2% / 11.8%，[实验记录](../middle_processing/vc_data/90_local_experiments.md) §15，原口径见 [13 规模化](../middle_processing/vc_data/13_scaling_tasks.md) §5.2），而多花的那部分全部花在生成最后会被丢掉的任务上。下面的资源表仍按原先的 26.9 万口径列，**要按实测口径读就把 CPU、存储、LLM 调用三行各乘 3.2**；人工那一行不乘，因为抽检量是按最终任务数定的。

| 项 | three.js 线 | Blender 线 | 口径 |
|---|---|---|---|
| CPU | 1,480 核时 | 1,064 核时 | 按复用浏览器池 14.3 任务每秒（[Harness 实测](../middle_processing/vc_data/06_harness.md) §4.1）、Blender 单任务 1.21 秒墙钟（[Blender 记录](../middle_processing/vc_data/10_blender_tasks.md) §3.5 外推）外推 |
| 折算整机 | 31 台机小时 | 22 台机小时 | 48 核机器 |
| 存储 | 约 20 GB | 约 100 GB | 单任务 0.2 MB 对 1 MB |
| LLM 调用 | 约 95 万次 | 约 95 万次 | 优化后；优化前 121 万次里难度标定占 65% |
| 人工 | 约 360 人时 | 约 360 人时 | 抽检 240、一致性标定 50、欠规格仲裁 67 |

来源：[本项目成本模型](../middle_processing/vc_data/13_scaling_tasks.md) §5.3 到 §5.8。

数据解读：两条线合计约 2,500 核时，一台 48 核机器两天跑完，算力不构成瓶颈。瓶颈是 LLM 调用和人工。LLM 调用里 65% 花在难度标定上，所以唯一值得反复优化的旋钮就是「难度要采样多少次」：一次性 n=8 要 133 万次标定调用，两段式先 n=2 筛掉 55% 再补 6 次只要 78 万次，LLM 总调用从 176 万降到 121 万，省 31%。还有一个反直觉的结论：Blender 比 three.js 便宜。Workbench 稳态渲染 0.065 秒一个视角（[Blender 记录](../middle_processing/vc_data/10_blender_tasks.md) §3.5），比软件光栅下的 WebGL 快；three.js 贵在浏览器本身。代价是扩产阶段只能渲 Workbench 剪影加算几何，不能渲 Cycles。

成本模型里最敏感的一项就是这个难度带留存，而本项目实测 0.19 与公开实测方向一致，都说明 0.60 偏乐观。[Skywork-OR1](https://arxiv.org/abs/2505.22312) 实测开训前就有 54%（7B）到 63%（32B）的数学题是零梯度（全对或全错），[GRESO](https://arxiv.org/abs/2506.02177) 实测训练后期有效 prompt 比例会掉到约 20%，而理论上界在通过率服从均匀分布时 G=16 只该丢 11.8%（[本项目推算](../middle_processing/vc_data/13_scaling_tasks.md) §2.2.2）——这个差距正是「通过率极度堆在两端」的量化体现。如果实际留存是 0.30，候选数从 26.9 万翻到 53.8 万，LLM 调用从 95 万翻到 190 万。本项目已在 16 道题上跑过一次单模型 pass@8（128 次调用，[实验记录](../middle_processing/vc_data/90_local_experiments.md) §15）；把样本扩到现有全部 47 个任务只需 376 次调用、几十分钟，是收窄区间最便宜的办法。

去重的单位是场景图，不是代码语法树。主流代码数据集普遍不用语法树等价做去重——[The Stack](https://arxiv.org/abs/2211.15533)、[StarCoder](https://arxiv.org/abs/2305.06161) 等都是 token 或字符 n-gram 的 MinHash，本项目检索到的唯一结构哈希是 LLVM 中间表示那一家（[ComPile](https://arxiv.org/abs/2309.15432)，[检索记录](../middle_processing/vc_data/13_scaling_tasks.md) §3.1.1）。本项目的实测给出了更直接的理由：换一条实现路径写出世界几何逐点相同的场景，几何信号全部放行（分部件 F-score 0.9993），只有按代码比的判据会误杀（[Blender 记录](../middle_processing/vc_data/10_blender_tasks.md) §3.2）。所以指纹分三级：场景图规范化哈希抓完全同构，低维几何特征的近邻抓「同模板换种子」，而最该自建的是第三级——断言集合的 Jaccard，它抓的是「考的点重复」。程序化生成最容易塌缩的不是场景长得一样，而是十万个任务里有三万个都在考某个部件缺失。

去重还会过头。[FineWeb](https://arxiv.org/abs/2406.17557) 实测（§3.4）对 96 个快照做全局去重后只剩 4T token，下游相比不去重几乎没有提升，最老的快照被删掉 90%；逐快照独立去重保留 20T，才与 RefinedWeb 持平并逐步受益。收益来自删掉跨全部快照的巨型重复簇，对只有几十个副本的小簇继续去重反而有害。所以只打巨型同构簇加 benchmark 去污，不要把去重率当 KPI。去污这一路只有收益没有损失，但要注意 n-gram 挡不住改写：[LMSYS 实测](https://arxiv.org/abs/2311.04850) 10-gram 对改写样本的 F1 是 0，而嵌入召回加 LLM 逐对判定能到 0.94 以上。场景图哈希在这里是结构化产物相对文本数据集的优势——它比的是产物几何，改写代码、换语言、换实现路径都不影响；而如果几何变了，那就不是同一道题。

分阶段的骨架是五步（[记录](../middle_processing/vc_data/13_scaling_tasks.md) §6）：S0 校准，3 到 10 个场景、200 个任务，只验阈值在没见过的结构类别上迁移得住；S1 模板化，8 个槽位模板、2,000 个任务，核心交付物不是任务而是 8 张过了可见性审计的槽位表；S2 多样性扩张，40 个模板、2 万个任务，第一次上两段式难度标定与三路去重；S3 真实素材注入，到 5 万，许可与污染都在这一阶段出问题；S4 满产，10 万以上，加分布漂移监控与训练侧回归。三条原则贯穿全程：每个阶段的验收必须包含一条留出指标且阈值进入前定死；规模每翻十倍就重新校准一次 Verifier，因为盲区是被具体 case 逼出来的；每个阶段只放大一个变量，否则出问题分不清是谁的锅。一条红线：任何阶段都不许用正在调阈值的那个集合做验收。本项目犯过一次——第一组 13 个变异既当调参集又当验收集，颜色容差是看到误杀后才加的（[实验记录](../middle_processing/vc_data/90_local_experiments.md) §2.4）。扩到十万量级时这个错误的代价是整个数据集在一个看不见的方向上过拟合，而且因为指标都很漂亮，不会有人发现。

## 参考文献

1. [SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://arxiv.org/abs/2310.06770) — Jimenez 等，Princeton，2023-10-10
2. [mrdoob/three.js：examples/screenshots 与 test/e2e](https://github.com/mrdoob/three.js/tree/dev/examples/screenshots) — three.js 项目，GitHub 仓库（2026-10-15 读取）
3. [BabylonJS/Babylon.js：visualization tests](https://github.com/BabylonJS/Babylon.js/tree/master/packages/tools/tests/test/visualization) — Babylon.js 项目，GitHub 仓库（2026-10-15 读取）
4. [blender/blender：tests/files/render（GitHub 镜像）](https://github.com/blender/blender/tree/main/tests/files/render) — Blender Foundation，GitHub 仓库（2026-10-15 读取）
5. [maplibre/maplibre-gl-js：test/integration/render](https://github.com/maplibre/maplibre-gl-js/tree/main/test/integration/render) — MapLibre，GitHub 仓库（2026-10-15 读取）
6. [pixijs/pixijs：tests/visual](https://github.com/pixijs/pixijs/tree/dev/tests/visual) — PixiJS，GitHub 仓库（2026-10-15 读取）
7. [primer/react：.playwright/snapshots](https://github.com/primer/react/tree/main/.playwright/snapshots) — GitHub Primer，GitHub 仓库（2026-10-15 读取）
8. [chartjs/Chart.js：test/fixtures](https://github.com/chartjs/Chart.js/tree/master/test/fixtures) — Chart.js，GitHub 仓库（2026-10-15 读取）
9. [processing/p5.js：test/unit/visual](https://github.com/processing/p5.js/tree/main/test/unit/visual) — Processing Foundation，GitHub 仓库（2026-10-15 读取）
10. [openlayers/openlayers：test/rendering/cases](https://github.com/openlayers/openlayers/tree/main/test/rendering/cases) — OpenLayers，GitHub 仓库（2026-10-15 读取）
11. [visgl/deck.gl：test/render/golden-images](https://github.com/visgl/deck.gl/tree/master/test/render/golden-images) — vis.gl，GitHub 仓库（2026-10-15 读取）
12. [plotly/plotly.js：test/image/baselines](https://github.com/plotly/plotly.js/tree/master/test/image/baselines) — Plotly，GitHub 仓库（2026-10-15 读取）
13. [SWE-bench Multimodal: Do AI Systems Generalize to Visual Software Domains?](https://arxiv.org/abs/2410.03859) — Yang 等，Princeton / Stanford，2024-10-04
14. [Infinite Photorealistic Worlds using Procedural Generation（Infinigen）](https://arxiv.org/abs/2306.09310) — Raistrick 等，Princeton，2023-06-15
15. [princeton-vl/infinigen](https://github.com/princeton-vl/infinigen) — Princeton Vision & Learning Lab，GitHub 仓库
16. [10,000,000 Pens](https://blog.codepen.io/2016/11/25/10000000/) — CodePen 官方博客，2016-11-25
17. [Licensing](https://blog.codepen.io/documentation/licensing/) — CodePen 官方文档
18. [js13kGames sitemap](https://js13kgames.com/sitemap.xml) — js13kGames（2026-10-15 读取）
19. [Shadertoy](https://www.shadertoy.com/) 与 [Terms](https://www.shadertoy.com/terms) — Shadertoy 官方站（CLI 403，未能实测）
20. [Procedural Image Programs for Representation Learning（shaders21k）](https://arxiv.org/abs/2211.16412) — Baradad 等，MIT，2022-11-29
21. [Stack Exchange API：Blender 站 python / scripting 标签计数](https://api.stackexchange.com/2.3/tags/python;scripting/info?site=blender) — Stack Exchange（2026-10-15 读取）
22. [Stack Exchange restricts data access for generative AI and the rest of the world](https://heise.de/-9823083) — heise online，2024-08-03
23. [Figma robots.txt](https://www.figma.com/robots.txt) — Figma（2026-10-15 读取）
24. [Frontend Mentor FAQs](https://www.frontendmentor.io/faqs) — Frontend Mentor（2026-10-15 读取）
25. [Chromatic](https://www.chromatic.com/) — Chromatic 产品页
26. [Percy](https://percy.io/) — BrowserStack Percy 产品页
27. [WebCode2M: A Real-World Dataset for Code Generation from Webpage Designs](https://arxiv.org/abs/2404.06369) — Gui 等，2024-04-09
28. [xcodemind/webcode2m](https://huggingface.co/datasets/xcodemind/webcode2m) 与 [webcode2m_purified](https://huggingface.co/datasets/xcodemind/webcode2m_purified) — WebCode2M 作者，HuggingFace 数据集
29. [Unlocking the conversion of Web Screenshots into HTML Code with the WebSight Dataset](https://arxiv.org/abs/2403.09029) — Laurençon 等，Hugging Face，2024-03-14
30. [Design2Code: Benchmarking Multimodal Code Generation for Automated Front-End Engineering](https://arxiv.org/abs/2403.03163) — Si 等，Stanford，2024-03-05
31. [HuggingFaceM4/WebSight](https://huggingface.co/datasets/HuggingFaceM4/WebSight) — Hugging Face，HuggingFace 数据集
32. [Objaverse-XL: A Universe of 10M+ 3D Objects](https://arxiv.org/abs/2307.05663) — Deitke 等，AI2，2023-07-11
33. [allenai/objaverse-xl](https://github.com/allenai/objaverse-xl) — AI2，GitHub 仓库
34. [CAD-Coder: Text-to-CAD Generation with Chain-of-Thought and Geometric Reward](https://arxiv.org/abs/2505.19713) — Guan 等，2025-05-26
35. [Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains](https://arxiv.org/abs/2507.17746) — Gunjal 等，Scale AI，2025-07-23
36. [WorldCoder-Bench: Benchmarking Physically Grounded 3D World Synthesis](https://arxiv.org/abs/2606.01869) — Lu 等，2026-06-01
37. [GameDevBench: Evaluating Agentic Capabilities Through Game Development](https://arxiv.org/abs/2602.11103) — Chi 等，2026-02-11
38. [CodeContests+: High-Quality Test Case Generation for Competitive Programming](https://arxiv.org/abs/2506.05817) — Wang 等，2025-06-06
39. [R2E-Gym: Procedural Environments and Hybrid Verifiers for Scaling Open-Weights SWE Agents](https://arxiv.org/abs/2504.07164) — Jain 等，UC Berkeley，2025-04-09
40. [DAPO: An Open-Source LLM Reinforcement Learning System at Scale](https://arxiv.org/abs/2503.14476) — Yu 等，ByteDance Seed / 清华 AIR，2025-03-18
41. [SWE-rebench: An Automated Pipeline for Task Collection and Decontaminated Evaluation of Software Engineering Agents](https://arxiv.org/abs/2505.20411) — Badertdinov 等，Nebius，2025-05-26
42. [ProcTHOR: Large-Scale Embodied AI Using Procedural Generation](https://arxiv.org/abs/2206.06994) — Deitke 等，AI2，2022-06-14
43. [Habitat Synthetic Scenes Dataset (HSSD-200)](https://arxiv.org/abs/2306.11290) — Khanna 等，Meta / Simon Fraser，2023-06-20
44. [Cousins Of The Vendi Score: A Family Of Similarity-Based Diversity Metrics](https://arxiv.org/abs/2310.12952) — Pasarkar、Dieng，Princeton，2023-10-19
45. [The Vendi Score: A Diversity Evaluation Metric for Machine Learning](https://arxiv.org/abs/2210.02410) — Friedman、Dieng，Princeton，2022-10-05
46. [DataComp: In search of the next generation of multimodal datasets](https://arxiv.org/abs/2304.14108) — Gadre 等，2023-04-27
47. [Reliable Fidelity and Diversity Metrics for Generative Models](https://arxiv.org/abs/2002.09797v1) — Naeem 等，2020-02-23
48. [Unlearnable, or Unmeasured? On the Reliability of Difficulty Labels in RLVR](https://arxiv.org/abs/2609.40115) — Chakma 等，2026-09-30
49. [Online Difficulty Filtering for Reasoning Oriented Reinforcement Learning](https://arxiv.org/abs/2504.03380) — Bae 等，2025-04-04
50. [Understanding R1-Zero-Like Training: A Critical Perspective（Dr. GRPO）](https://arxiv.org/abs/2503.20783) — Liu 等，Sea AI Lab，2025-03-26
51. [SPICE: An Automated SWE-Bench Labeling Pipeline for Issue Clarity, Test Coverage, and Effort Estimation](https://arxiv.org/abs/2507.09108) — Oliva 等，2025-07-12
52. [Fantastic Bugs and Where to Find Them in AI Benchmarks](https://arxiv.org/abs/2511.16842) — Truong 等，Stanford，2025-11-20
53. [Training Software Engineering Agents and Verifiers with SWE-Gym](https://arxiv.org/abs/2412.21139) — Pan 等，UC Berkeley，2024-12-30
54. [Vipitis/Shadereval-inputs](https://huggingface.co/datasets/Vipitis/Shadereval-inputs) — Vipitis，HuggingFace 数据集
55. [SWE-smith: Scaling Data for Software Engineering Agents](https://arxiv.org/abs/2504.21798) — Yang 等，Stanford，2025-04-30
56. [Strong Model Collapse](https://arxiv.org/abs/2410.04840) — Dohmatob 等，Meta，2024-10-07
57. [Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accumulating Real and Synthetic Data](https://arxiv.org/abs/2404.01413) — Gerstgrasser 等，2024-04-01
58. [Beyond Model Collapse: Scaling Up with Synthesized Data Requires Verification](https://arxiv.org/abs/2406.07515) — Feng 等，NYU / Meta，2024-06-11
59. [Nemotron-CC: Transforming Common Crawl into a Refined Long-Horizon Pretraining Dataset](https://arxiv.org/abs/2412.02595) — Su 等，NVIDIA，2024-12-03
60. [Skywork Open Reasoner 1 Technical Report](https://arxiv.org/abs/2505.22312) — He 等，Skywork AI，2025-05-28
61. [Act Only When It Pays: Efficient Reinforcement Learning for LLM Reasoning via Selective Rollouts（GRESO）](https://arxiv.org/abs/2506.02177) — Zheng 等，2025-06-02
62. [The Stack: 3 TB of permissively licensed source code](https://arxiv.org/abs/2211.15533) — Kocetkov 等，BigCode，2022-11-20
63. [StarCoder: may the source be with you!](https://arxiv.org/abs/2305.06161) — Li 等，BigCode，2023-05-09
64. [ComPile: A Large IR Dataset from Production Sources](https://arxiv.org/abs/2309.15432) — Grossman 等，2023-09-27
65. [The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale](https://arxiv.org/abs/2406.17557) — Penedo 等，Hugging Face，2024-06-25
66. [Rethinking Benchmark and Contamination for Language Models with Rephrased Samples](https://arxiv.org/abs/2311.04850) — Yang 等，LMSYS，2023-11-08

本项目内部记录（不计入上表）：[02 任务来源](../middle_processing/vc_data/02_task_sources.md)、[06 Harness](../middle_processing/vc_data/06_harness.md)、[09 预训练数据](../middle_processing/vc_data/09_pretrain_data.md)、[10 Blender 任务](../middle_processing/vc_data/10_blender_tasks.md)、[13 规模化](../middle_processing/vc_data/13_scaling_tasks.md)、[90 本地实验](../middle_processing/vc_data/90_local_experiments.md)、[92 数字复核](../middle_processing/vc_data/92_number_audit.md)，以及脚本 [gen_tasks.py](../scripts/vc_verifier/proto/gen_tasks.py)、[mutate.py](../scripts/vc_verifier/proto/mutate.py)、[ablate.py](../scripts/vc_verifier/proto/ablate.py)、[passk.py](../scripts/vc_verifier/proto/passk.py)。

</div>

<div class="env-view" data-view="verifier" data-label="Verifier">

<nav class="toc view-toc"><h2>Contents</h2><ul><li class="l2"><a href="#vf-1"><span class="num">1</span> A Screenshot Is Not a Reward Signal</a></li><li class="l2"><a href="#vf-2"><span class="num">2</span> Reliable Signal Comes From Runtime State</a></li><li class="l2"><a href="#vf-3"><span class="num">3</span> Blender Reproduces the Same Conclusion</a></li><li class="l2"><a href="#vf-4"><span class="num">4</span> A VLM Judge Finds the Check You Forgot</a></li><li class="l2"><a href="#vf-5"><span class="num">5</span> Capture the Scene Without the Model's Cooperation</a></li><li class="l2"><a href="#vf-6"><span class="num">6</span> All of This Runs on CPU</a></li><li class="l2"><a href="#vf-7"><span class="num">7</span> An Independent Benchmark Converged on the Same Design</a></li><li class="l2"><a href="#vf-8"><span class="num">8</span> How the Layers Divide the Work</a></li><li class="l2"><a href="#vf-9"><span class="num">9</span> At Scale, a Blind Spot Becomes Missing Data</a></li><li class="l2"><a href="#vf-10"><span class="num">10</span> This Verifier Only Works for Repair Tasks</a></li><li class="l2"><a href="#vf-11"><span class="num">11</span> Half of Aesthetics Is a Deterministic Check</a></li></ul></nav>

<a class="anchor" id="vf-1"></a>

## 1 A Screenshot Is Not a Reward Signal

[WorldCoder-Bench](https://arxiv.org/abs/2606.01869) 把「截图加 VLM（GPT-5.4）」当作对照判据，在 1,434 个〈模型，任务〉对上重打分，通过率只有 2.7%（[WorldCoder-Bench 表 2](https://arxiv.org/abs/2606.01869)）。这个数字不说明模型差，它说明判据坏了：原文的解释是它「不加区分地惩罚视觉差异」，等于一律判差，所以这套 reward 对策略的改进完全不敏感。换个方向偷懒同样失效：[WorldBench](https://arxiv.org/abs/2610.10622) 从一个世界里删掉或禁用 5 个功能（满分合计 7.11），只读源码的 judge 仍给出 5.44 分，因为源码里那段逻辑还在、看上去写得很完整（[WorldBench 表 5](https://arxiv.org/abs/2610.10622)）。

把几条通道放在同一个真值上比，差距是数量级的（均出自 [WorldCoder-Bench 表 2](https://arxiv.org/abs/2606.01869)）：

- 截图加 VLM 与真值的 Kendall τ_b 是 −0.068，即负相关，成本是 DOM 基线的约 50 倍。（[表 2](https://arxiv.org/abs/2606.01869)）
- 读取隐藏的运行时状态契约，τ_b 是 1.000、假阳率 0，成本约 2 倍。注意它本身就是该基准的真值，τ=1 是定义使然；有意义的是另外三条通道都复现不了它的排序。（[表 2](https://arxiv.org/abs/2606.01869)）
- 一个贵 25 倍而且方向都不对的信号，不该进 reward。（50 倍对 2 倍，[表 2](https://arxiv.org/abs/2606.01869)）

我们自己的实验给出了同一方向的数据（[本项目实验记录 §2](../middle_processing/vc_data/90_local_experiments.md)）。三个 three.js 场景、47 个带人工标签的变异，只看页面自带相机的一张截图做逐像素相似度，在前两个场景的 29 个变异上判对 12 个。它不是不够准，它是在量纲上失明：雪人的胡萝卜鼻子只占几十个像素，把它挪到后脑勺，页面截图相似度仍然是 0.999。

这一节要立住的判断只有一条：**视觉产出的 reward，不能由一张图决定。** 它不是说图没用，而是说图只能作为分项，不能作为判据。

<a class="anchor" id="vf-2"></a>

## 2 Reliable Signal Comes From Runtime State

把 Verifier 拆成互相独立的几层，每层查一个不同的量，判别力才涨得上来。我们在两个场景（雪人、桌子加杯子）上各写一组变异，人工标注「该挂」还是「不该挂」（[实验记录 §2.1](../middle_processing/vc_data/90_local_experiments.md)，变异脚本 [mutate.py](../scripts/vc_verifier/proto/mutate.py)）。该挂的是部件缺失、挪位、朝向反、比例变、颜色换、杯子悬空或陷进桌面；不该挂的是网格精细度、光照强弱、背景色、相机机位、轻微色差、尺寸正负 5%。

核心发现：判别力随信号层数单调上升，方向可信，但「上升」这件事在这个样本量下并不显著——分层组合 29/29 对按色体素 25/29，4 个不一致对全部同向，配对精确检验 p 为 0.125（[红队复核](../middle_processing/vc_data/18_redteam.md)）。

| 程序化信号 | 雪人 13 例 | 桌子 16 例 | 合计 |
|---|---|---|---|
| 页面单张截图逐像素相似度 | 5 | 7 | 12/29 |
| 几何类名多重集一致 | 6 | 8 | 14/29 |
| 多视角剪影 IoU | 9 | 10 | 19/29 |
| 按色体素 IoU | 11 | 14 | 25/29 |
| 分层组合 | 13 | 16 | 29/29 |

来源：[实验记录 §2.1](../middle_processing/vc_data/90_local_experiments.md)。

数据解读：按 API 名字断言「场景里有几个球、几个圆柱」只能到 14/29，因为它查的是实现路径而不是结果，换一种建模手法做出同一个形状就会误杀。多视角剪影补上了单视角看不见的方位错误，按色体素补上了形状对而颜色错的情况，两者叠起来仍漏 4 个，缺的是部件级拓扑。这条曲线说明一件事：加视角、加分辨率都不如加一个量纲不同的新量。（[实验记录 §2.2](../middle_processing/vc_data/90_local_experiments.md)）

前两个场景的 29/29 必须打折扣，因为阈值在它们身上看过一眼：分块 IoU 的下限在这两个变异集上扫过三档，颜色容差是看到「轻微调色被误杀」之后加的（[实验记录 §2.4](../middle_processing/vc_data/90_local_experiments.md)）。所以我们又做了一次干净的留出测试。新场景是一辆小车，9 个 mesh；18 个变异和它们的标签先写死再跑，阈值沿用前两个场景，一个没动，只跑一次。结果 18/18（[实验记录 §2.3](../middle_processing/vc_data/90_local_experiments.md)，逐例数值见 [car_mut/mutation.json](../scripts/vc_verifier/proto/runs/car_mut/mutation.json)）。

下面这个 demo 用的就是这组留出数据，图是真实渲染，数字是真实测得。点一个变异，左边五张图里第一张是页面自带相机，其余四张是 Verifier 自己摆的机位。demo 里四个该挂的变异，第一张的相似度都在 0.996 以上（[mutation.json](../scripts/vc_verifier/proto/runs/car_mut/mutation.json)），单看它分不出对错。

<iframe class="demo-frame" style="height:470px" src="demos/verifier-layers.html" loading="lazy"></iframe>

留出集同时证明了每一层都不是摆设：

| 留出变异 | 挂在哪一层 | 为什么别的层抓不到 |
|---|---|---|
| 前灯少一个 | 部件连通块数 | 剪影 0.998、分块 0.924、该色体素 0.5 全在阈值之上 |
| 风挡挪到车尾 | 按色体素 | 剪影 0.992，外轮廓几乎没变，但玻璃色体素 IoU 为 0 |
| 风挡改成车身色 | 按色体素 | 剪影和分块都是 1.0，形状完全没动 |
| 少一个轮子 | 分块体素 | 全局剪影 0.903 刚好过线，分块最差块是 0.0 |
| 轮子轴向转 90 度 | 多视角剪影 | 外轮廓直接变了 |

来源：[实验记录 §2.3](../middle_processing/vc_data/90_local_experiments.md)。

数据解读：五个变异挂在四个不同的层上，没有任何一层能独自覆盖。最接近误杀的一例是「轮子半径加 4%」，分块最差块 0.727，阈值 0.5，还留着余量。这意味着分层不是为了堆保险，而是因为错误本身分布在不同的量纲上。（[实验记录 §2.3](../middle_processing/vc_data/90_local_experiments.md)）

<a class="anchor" id="vf-3"></a>

## 3 Blender Reproduces the Same Conclusion

同样的方法换一个技术栈重做一遍（[Blender 实验记录 §3](../middle_processing/vc_data/10_blender_tasks.md)，判据代码 [blender/verify.py](../scripts/vc_verifier/blender/verify.py)）。Blender 侧的场景是一张木桌加台灯加陶瓷杯，22 个变异，11 个该挂、11 个不该挂；其中 15 个是开发集，7 个是选完判据之后才造的留出集。

核心发现：两个极端都不成立，中间那条路才对。

| 信号 | 总判对 | 检出 11 个该挂 | 保真 11 个不该挂 |
|---|---|---|---|
| 只看一张截图 | 12/22 | 2 | 10 |
| 多视角剪影 IoU | 14/22 | 3 | 11 |
| 全局 Chamfer | 13/22 | 2 | 11 |
| 全局 F-score | 11/22 | 0 | 11 |
| 分部件 F-score | 18/22 | 7 | 11 |
| 全量状态断言 | 11/22 | 11 | 0 |
| 分部件几何加四族断言 | 21/22 | 11 | 10 |

来源：[Blender 实验记录 §3.4](../middle_processing/vc_data/10_blender_tasks.md)。

数据解读：全量状态断言把 11 个真错全抓住了，代价是 11 个语义未变的改写全被误杀，净判别力等于零。误杀集中在两类写法差异：把边长 1 的立方体放大 1.2 倍，改写成边长 2 的立方体缩小 0.6 倍，世界几何逐点相同而物体自身的缩放值差一倍；圆柱从 16 段改 32 段，顶点数全变而形状不变。断言查的是代码留下的痕迹，不是结果。（[Blender 实验记录 §0、§3.4](../middle_processing/vc_data/10_blender_tasks.md)）

几何指标则栽在另一个地方：平均量会把局部错误稀释掉。杯子只占全场表面积约 2%，把它在桌面上挪 30 厘米，全局 Chamfer 只从 0 涨到 0.00018，分部件算是 0.084，差 460 倍（[Blender 实验记录 §4.3](../middle_processing/vc_data/10_blender_tasks.md)）。全局 F-score 更极端，11 个该挂的一个都没检出。

所以可迁移的规律有两条，而且在 three.js 和 Blender 两侧各自独立成立：**几何指标必须分部件算；断言只能查任务描述钉死的字段。** 第二条的证据是留出集上唯一的误杀——日光功率从 3.0 调成 3.5 被判挂，而 Problem Statement 里根本没写功率（[Blender 实验记录 §3.3](../middle_processing/vc_data/10_blender_tasks.md)）。修法不是放宽容差，是在造题时就产出被钉死的字段清单，Verifier 只查清单内的字段。Verifier 能查的信息量必须小于等于 Problem Statement 给出的信息量，否则这道题进了 RL 就是纯噪声；three.js 侧预实验里两次失败也是同一个原因（[实验记录 §5](../middle_processing/vc_data/90_local_experiments.md)）。

<a class="anchor" id="vf-4"></a>

## 4 A VLM Judge Finds the Check You Forgot

VLM judge 远强于像素指标（[实验记录 §3](../middle_processing/vc_data/90_local_experiments.md)，脚本 [vlm_judge.py](../scripts/vc_verifier/proto/vlm_judge.py)）。把参考与候选的渲染图上下拼成一张交给模型判 pass 还是 fail，48 个 case、4 个 judge、每种看图条件每例两次、温度 0，共 768 次判定，单模型判对 74 到 92 次（分母 84 到 96，少掉的是没解析出结论的）；而逐像素相似度在其中 29 个变异上只有 12/29。像素指标判不出「鼻子不见了」，VLM 一眼就说出来。

这一节的结论推翻过一次，过程值得写出来（[实验记录 §3.1](../middle_processing/vc_data/90_local_experiments.md)）。最早只跑了 18 个 case，看到多视角拼图的判对率不升反降，于是写下「多视角对 VLM 无效」。把样本扩到 48 例、并修正一处人工标注错误之后，结论反过来了。

核心发现：多视角对 VLM 有效，但它买到的不是判对率，而是稳定性。

| judge | 单视角判对 | 多视角判对 | 单视角重测翻面 | 多视角重测翻面 |
|---|---|---|---|---|
| gpt-6-astra | 84/95 | 92/96 | 16.7% | 4.2% |
| gemini-3.8-flash | 88/96 | 92/96 | 8.3% | 0.0% |
| doubao-seed-2.1-pro | 78/91 | 81/84 | 6.2% | 8.3% |
| claude-opus-5-5 | 76/96 | 74/93 | 16.7% | 20.8% |
| 4 模型 8 票多数投票 | 44/48 | 46/48 | — | — |

来源：[实验记录 §3](../middle_processing/vc_data/90_local_experiments.md)。

数据解读：逐 case 配对比较，单视角赢 11 例、多视角赢 27 例；把每个 judge 的每个 case 当成独立配对做 McNemar 得 p=0.015，但这样算高估了独立性（四个 judge 判的是同一批 case），逐模型单独看没有一个到显著（p 从 0.13 到 0.61，[实验记录 §3.1](../middle_processing/vc_data/90_local_experiments.md)）。所以这张表支持的说法是「多视角不差于单视角，对强 judge 更好」，不支持「多视角一定更好」。

真正稳的结论是第三、四列。同一个模型、同一张图、温度 0 跑两次，最差一档有 20.8% 的 case 会翻面。单次 VLM 判定不能当 reward，这和用几视角无关。而多视角把两个最强 judge 的翻面率从 16.7% 压到 4.2% 和从 8.3% 压到 0。（[实验记录 §3.2](../middle_processing/vc_data/90_local_experiments.md)）

投票也救不回全部（[实验记录 §3.3](../middle_processing/vc_data/90_local_experiments.md)）。4 个模型 8 票多数投票在 48 例上单视角 44 对、多视角 46 对。拿它和程序化信号的 47/47 直接比是不成立的——两个集合不同、组成不同，而且其中一个是程序化信号自己调过阈值的集合；按配对检验，这个差别完全不显著。能比的只有定性的那一面：投票漏掉的那几例全是同一类——**定量的几何偏差**：一条桌腿缩短到 70%，8 票全判通过；桌面厚度减到原来的三分之一，5 票判通过。这两例程序化信号都抓到了，前者靠分块体素 0.167，后者靠按色体素 0.528。

还有一个对照更能说明 VLM judge 在靠什么判。把参考图拿掉，只给候选的渲染图加一段文字需求，其余全部不变——同样两个 judge、同样的 case、同样的候选图（[实验记录 §14](../middle_processing/vc_data/90_local_experiments.md)，脚本 [judge_noref.py](../scripts/vc_verifier/proto/judge_noref.py)）。

45 个带标签的 case，两个 judge（[实验记录 §14](../middle_processing/vc_data/90_local_experiments.md)）。核心发现：拿掉参考图，判别力从九成五掉到七成上下，掉的主要是检出。

| 条件 | 总判对 | 检出 | 保真 |
|---|---|---|---|
| 有参考图，单视角 | 94% | 58/63 | 43/44 |
| 有参考图，四视角 | 97% | 61/64 | 44/44 |
| 无参考图，单视角 | 68% | 35/56 | 30/40 |
| 无参考图，四视角 | 76% | 34/56 | 39/40 |

来源：[实验记录 §14](../middle_processing/vc_data/90_local_experiments.md)。

数据解读：检出从九成二掉到六成上下，而四视角下的保真仍有 39/40——没有参考的 judge 变成了一个偏宽松的放行器，不怎么冤枉好人，但一多半的缺陷放了过去。单视角下连保真也只剩 30/40，说明没有参照时它两头都在猜。机制很直接——拿掉参考之后它只能对着那段几十个字的需求判，而需求没写桌子多高、杯子多大，于是尺寸与位置类的缺陷全都「不违反需求」。**这正是本文那条规则从 judge 这一侧看到的样子**：判据能查的信息量，不会超过题面给出的信息量；并排放上参考图，等于把题面的信息量提高到逐像素，judge 这才有东西可查。（[实验记录 §14](../middle_processing/vc_data/90_local_experiments.md)）

这和训练那一侧的实验是同一件事（[实验记录 §7](../middle_processing/vc_data/90_local_experiments.md)）。生成方在没有可比对象时，首轮挂掉后只能救回 2/37；判别方在没有可比对象时，检出从九成二掉到六成。**模型缺的不是能力，是参照。**

真正体现 VLM 价值的是那次翻案（[实验记录 §3.4](../middle_processing/vc_data/90_local_experiments.md)）。最早被记成「多视角投票判错」的那一例，是我们自己标成「正确改写」的版本：它用旋转成型几何（LatheGeometry）把三个球的轮廓一次转出来，外观和参考一致，只是建模手法不同。多视角条件下 8 票里有 7 票说它有问题，而单视角条件下投票判它通过。后来把俯视图放大看，它头顶真的有一个洞，旋转成型在极点没有封口——那个洞只在俯视图里看得见。标签改成了「该挂」，上面那张表用的是改正后的标签。

当时的程序化 Verifier 对它是结构性失明的。双面剪影把洞填上了；换成单面剪影，IoU 也只从 0.997 掉到 0.958，因为洞只占几十个像素，被全局 IoU 淹没；体素 IoU 是 0.995，同理。修法不是把阈值从 0.96 调到 0.97——那样会立刻误杀一批合法改写。修法是换一个不随尺寸衰减的量：只被一个三角面用到的边，也就是开放边界边数。闭合实体是 0，这个版本是 64，直接判挂（[实验记录 §2.2](../middle_processing/vc_data/90_local_experiments.md)）。

这里必须自曝一处方法学问题。这个信号是**在它要验证的那个 case 上造出来的**，而那个 case 就在雪人那 13 例里面。所以「加上这个信号之后两个变异集仍然是 13/13 和 16/16」不是独立验证，是在调参集上报调参集的成绩，违反了本文自己在讲任务构造时定下的红线——不许用正在调阈值的集合做验收。它唯一算得上独立的证据，是后来那个小车留出集上没有因为这个信号产生新的误杀。要真正验证它，得另造一组专门含破洞与开口面的变异，标签先写死再跑。（[实验记录 §3.4](../middle_processing/vc_data/90_local_experiments.md)；红线违反的复核见 [红队审查 §1.4–§1.5](../middle_processing/vc_data/18_redteam.md)）

这件事定义了 VLM judge 的位置。它能发现「这里不对劲」但说不清是什么；程序化信号能精确指出哪一项超了，但要先有人想到查这一项。**VLM judge 的价值是帮你找到该加哪条程序化检查，不是直接当 reward。** 它也不是人工标签的替代品：标注者和自动指标会在同一个地方同时瞎掉，这次就是 4 个 VLM 对、一个人错。（[实验记录 §3.4](../middle_processing/vc_data/90_local_experiments.md)）

<a class="anchor" id="vf-5"></a>

## 5 Capture the Scene Without the Model's Cooperation

常见做法是在任务契约里要求模型把场景对象挂到一个约定好的全局变量上，例如 [WorldCoder-Bench](https://arxiv.org/abs/2606.01869) 的 `window.__3D_STATE__`。这条路不能走，两个原因都是机制层面的：训练时模型会学会「写这一行就行」，评测换一套 Harness 立刻失效；而且那个对象是模型自己造的，它可以伪造。WorldCoder-Bench 自己就记录了有模型不按约定挂出全局引用的失败（[WorldCoder-Bench 附录 D.2](https://arxiv.org/abs/2606.01869)）。

我们改用 three.js 自带的 devtools 事件通道。场景与渲染器的构造函数本身会向这个通道派发事件（见 three.js r160 源码 [Scene.js](https://github.com/mrdoob/three.js/blob/r160/src/scenes/Scene.js)），在页面脚本执行之前预先把接收端定义好，就能拿到每一个场景和渲染器实例（实现见 [harness.js](../scripts/vc_verifier/proto/harness.js)）。它不要求模型配合，事件由库自己发出。伪造并非不可能——页面可以把接收端整个换掉——但那样我们一个场景也收不到，直接挂在硬门槛上，是向安全侧失败。实测页面无论用 CDN、importmap，还是把整个库内联打包进去、完全不发网络请求，抓到的 mesh 数和体素结果都一致（[实验记录 §1.3](../middle_processing/vc_data/90_local_experiments.md)）。

光是拿到场景还不够，Verifier 必须确认看到的画面就是页面真正交付的画面。我们手写了 7 个作弊页面做攻击测试，6 个被挡，有一个一度成功骗过 Verifier：它另起一个离屏渲染器，渲染一份正确的场景，而文档里那块可见画布画的是别的东西（[项目日志 STATE.md](../middle_processing/vc_data/STATE.md)）。

修法是两条一起上（同上；离屏计数见 [harness.js](../scripts/vc_verifier/proto/harness.js)）。第一条，只认挂在文档里、有实际尺寸、未被隐藏的那块画布，离屏的一律不计入判定。第二条，把离屏渲染的次数本身当成蜜罐信号——正常解法不需要它，一旦出现就是明确的行为标记，而不是等着某条断言恰好识破。修完之后 7 个作弊页面全挡。

手写攻击只能覆盖想得到的路径，所以又让模型自己来找（[实验记录 §13](../middle_processing/vc_data/90_local_experiments.md)，脚本 [hack_probe.py](../scripts/vc_verifier/proto/hack_probe.py)）。把判据的构成原原本本告诉它，要求写一个「能过验收但实际不满足需求」的页面，三个场景乘四个模型共 12 次请求，其中两个模型全程没有产出，实际拿到 5 份可判定的作弊页，**verifier 判过 0 份**，全部挂在多视角剪影那一层。它们试的路子是：用贴图画出看起来对的东西（3 份）、往约定好的全局变量里塞一个正确场景（1 份）、直接操作画布读写（3 份）、玩绘制顺序（1 份）；一份作弊页可以同时用几条路子。

这个零要克制地读。分母只有 5，而且模型只试了一次、没有梯度、也看不到判定反馈；RL 里的策略有成千上万次尝试和明确的分数信号。它还说明一件事：模型找的路子和我们手写的七条高度重合，两边受限于同一套直觉。**真正有价值的对抗样本只能从训练里来**，所以防 hack 的工程重点不是上线前想全，而是上线后抽检高分样本。（[实验记录 §13](../middle_processing/vc_data/90_local_experiments.md)）

这两件事合起来说明：取证通道的可信度不能依赖产物的自觉。Verifier 要从库的内部机制和可见画布这类外部事实取证，不要从模型写的约定取证。7 个作弊页面全挡，说明的是这 7 条路径被堵住了，不是「不可 hack」——其中一条在修补之前真的骗过了 Verifier，同类漏洞一定还会有。（手写攻击见 [STATE.md](../middle_processing/vc_data/STATE.md)，取证实现见 [harness.js](../scripts/vc_verifier/proto/harness.js)，攻击面分析见 [Reward hacking 防御笔记 §1.3](../middle_processing/vc_data/11_hacking_defense.md)）

<a class="anchor" id="vf-6"></a>

## 6 All of This Runs on CPU

视觉验证常被当成需要 GPU 沙箱的脏活。本机的实测结论相反：整套流程只用 CPU 就够。

核心发现：取证成本在秒级以下，塞得进 RL rollout 的每步观测。

| 环节 | 实测吞吐 | 来源 |
|---|---|---|
| 单次 three.js 探测，含启动浏览器 | 0.8 到 1.0 秒 | [实验记录 §1.5](../middle_processing/vc_data/90_local_experiments.md) |
| 复用浏览器（8 浏览器乘 8 页），每任务含重载加 8 视角加场景图 | 约 14 任务每秒 | [Harness 实测 §4.1.3](../middle_processing/vc_data/06_harness.md)，[bench_pool.js](../scripts/vc_verifier/bench_pool.js) |
| 读场景图（13 个 mesh，含世界包围盒） | 1.8 毫秒 | [Harness 实测 §4.1.1](../middle_processing/vc_data/06_harness.md) |
| Blender Workbench 渲染（32 进程并发） | 15.5 视角每秒 | [Harness 实测 §4.2](../middle_processing/vc_data/06_harness.md) |
| Blender 几何指标全套（6 万点采样加三项指标） | 约 0.4 秒每候选 | [Blender 实验记录 §4.4](../middle_processing/vc_data/10_blender_tasks.md) |

数据解读：机器无 GPU，Chrome 走无头加软件渲染。结构化观测比图像便宜一到两个数量级——读一次场景图 1.8 毫秒，单视角截图 62 到 85 毫秒，8 视角转台约 0.2 到 0.5 秒（[Harness 实测 §4.1.1](../middle_processing/vc_data/06_harness.md)），所以「先给结构、再给像素」不只是精度上的选择，也是成本上的选择。Blender 侧的几何指标比渲染便宜约 3 倍，而判别力更高（分部件 F-score 检出 7/11，多视角剪影只有 3/11，[Blender 实验记录 §4.4](../middle_processing/vc_data/10_blender_tasks.md)）。如果只能留一个视觉信号，留几何，不留渲染。

确定性要靠 Harness 主动控制，不能指望页面（[Harness 实测 §4.1.4](../middle_processing/vc_data/06_harness.md)，[bench_clock.js](../scripts/vc_verifier/bench_clock.js)）。只冻结时钟不够：对一个用动画帧回调加随机数的页面，仅安装虚拟时钟时三次截图三个结果，加上暂停与定点推进之后 20 次里仍有 2 种。能做到逐字节一致的只有「由页面钩子或 Harness 显式推进帧，并直读画布像素」（同上；Harness 接管帧调度与随机源的做法见 [实验记录 §1.1](../middle_processing/vc_data/90_local_experiments.md)）。拿不到这种控制时，Verifier 必须用感知容差比对，不能比哈希。

<a class="anchor" id="vf-7"></a>

## 7 An Independent Benchmark Converged on the Same Design

[3JSBench](https://3jsbench.com/) 是本项目检索范围内唯一把 Astra 与 Claude Opus 5.5 放进同一套确定性几何判据的公开评测：100 道题、每题三次一次成型的尝试、10 个模型（[3JSBench 榜单](https://3jsbench.com/)，2026-10-15 读取，站方注明 2026-10-14 改判；读取过程见 [核实记录](../middle_processing/vc_data/91_3jsbench_verified.md)）。它的管线是独立做出来的，结构却和本项目几乎逐项重合。

核心发现：两边在不知道对方的情况下选了同一套取证方式，连视角数都一样。

| 它的做法（[3JSBench 方法页](https://3jsbench.com/methodology)） | 本项目 | 是否一致 |
|---|---|---|
| 隔离的无头浏览器跑模型写的程序 | 无头浏览器，断网，页面从内存加载 | 一致 |
| 记录场景并渲染九个固定视角 | 捕获场景，Verifier 自己摆九个相机 | 一致 |
| 在捕获到的场景上做确定性测量 | 读场景图、体素、部件、拓扑 | 一致 |
| 全部必查项通过才算通过 | 分层，任一层否决即判失败 | 一致 |
| 咨询性诊断不参与判定 | 感知相似只作分项 | 一致 |
| 基础设施故障的尝试单独排除 | 硬门槛单列，不混进判定 | 一致 |
| 用一个绑定模型把题面点名的部件对到场景的网格上 | 按颜色分部件，没有这一层 | 不一致 |

本项目一列的依据：[实验记录 §1–§2](../middle_processing/vc_data/90_local_experiments.md)。

数据解读：唯一的结构差异是部件绑定。它让模型只做绑定、不做打分，这是一个比两边现有方案都好的折中——语言模型负责把「题面说的那个盖子」对到具体网格，判定本身仍然是确定性的。本项目按颜色分部件在颜色复用的场景上会失效，这条该抄。

它的 695 条必查项分六族，分布很说明问题（[3JSBench 方法页](https://3jsbench.com/methodology)）。部件计数 223 条、结构 160 条、空间关系 157 条，三族合计占 78%，全部是「有几个、接在哪、挨着谁」。没有一条查「像不像」。

同样值得抄的是它的失败统计（[3JSBench](https://3jsbench.com/)）。3000 次尝试里最常见的五类失败是物体互相穿插 20%、可见背面 19%、表面闪烁 17%、朝向与题面不符 16%、部件断开 16%。前三类全是渲染层面的物理不自洽，而本项目的判据里只覆盖了可见背面一项。

按这个清单补了两个信号，各用一个故意做坏的场景验证（[项目日志 STATE.md](../middle_processing/vc_data/STATE.md)，判据代码 [verify.py](../scripts/vc_verifier/proto/verify.py)）。把桌面正上方零距离再铺一块同样大的面，整体穿插比例从参考的 0.053 涨到 0.762，改变绘制顺序后有 5534 个像素发生变化，两个信号都把它判挂。三个变异集回归后仍是 13/13、16/16、18/18，没有新增误杀。

有一个信号没能做成（[STATE.md](../middle_processing/vc_data/STATE.md)，判据代码 [verify.py](../scripts/vc_verifier/proto/verify.py) 里 pair_overlap 只作诊断量）。按部件两两算穿插比例，在 48 的体素分辨率下不可用：薄部件会被量化成单层，看起来像被另一个部件完全包含，参考解自己的最大值就是 1.0。所以它只能当诊断量。这条限制本身是有用的——体素分辨率决定了能查什么，细部件的接触判定得换别的办法，比如包围层次加精确相交测试。

另外一个数字替嵌入相似度盖了棺（[3JSBench 方法页](https://3jsbench.com/methodology)）。站方把 [SigLIP 2](https://arxiv.org/abs/2502.14786) 相似度明确标注为不参与判定的描述性信号，而三个模型的均值差是 Astra 加 0.011、Opus 5.5 加 0.009、GPT-6 Sol 加 0.007，对应的通过率却是 80.0%、49.0%、27.0%。通过率差 53 个百分点，嵌入相似度只差 0.004。

<a class="anchor" id="vf-8"></a>

## 8 How the Layers Divide the Work

把上面的结论装成一套可执行的分层判据。前一层失败就截断，后层不再计算；靠前的层给出的否决，后面的分数再高也不能补回来。

核心发现：成本、噪声和可 hack 程度三者沿着层次同向上升，所以越靠后的层越不能单独定生死。

| 层 | 查什么 | 单样本成本 | 噪声 | 可被 hack 的程度 |
|---|---|---|---|---|
| 硬门槛 | 能执行、无运行时报错、渲染发生过、可见画布非空 | 1 到 5 秒，纯 CPU | 几乎为 0 | 低 |
| 程序化断言 | 运行时状态：部件存在与数量、世界包围盒、层级、拓扑量、修改器与动画通道 | 5 到 30 秒 | 低，有少量 flaky | 中：按 API 名或变量名断言可被骗（[WorldBench](https://arxiv.org/abs/2610.10622)） |
| 感知与几何相似 | 多视角剪影、按色体素 IoU、分部件 Chamfer 与 F-score | 10 到 60 秒 | 中 | 高：视口尺寸、贴图文字、特征饱和 |
| VLM rubric | 多视角拼图加关键源码片段，逐条 0/1；可测属性先由程序测好再告诉 judge | 每样本 1 到 3 次调用 | 中高，本项目重测最差一档 20.8% 翻面（[实验记录 §3](../middle_processing/vc_data/90_local_experiments.md)） | 中：图中文字注入（[AgentTypo](https://arxiv.org/abs/2510.04257)）、长度偏差（[MLLM-as-a-Judge](https://arxiv.org/abs/2402.04788)） |
| 组内 pairwise | 同一 Problem Statement 的通过者两两比较，顺序正反各判一次 | 比较次数随通过者数量平方增长 | 较低 | 中：位置偏差（[Judging the Judges](https://arxiv.org/abs/2406.07791)）、自我偏好（[Self-Preference Bias](https://arxiv.org/abs/2410.21819)） |

来源：分层结构与成本、噪声档位是调研笔记里的设计估计（[Verifier 调研 §6.1](../middle_processing/vc_data/04_verifier.md)），不是本机逐层实测；本机实测的单次探测是 0.8 到 1.0 秒（见第 6 节）。

这套判据的重复性也量过（[实验记录 §12](../middle_processing/vc_data/90_local_experiments.md)，脚本 [flaky.py](../scripts/vc_verifier/proto/flaky.py)）：9 个产物各探测 3 次，判定零翻面、信号值逐位相同。做到零靠三件事——冻结时钟让帧只在取证方推进时前进、固定随机种子、除了库本身断掉所有外部请求。限制是这只覆盖同一机器同一浏览器版本，跨版本的确定性没测过，镜像升级后要重新量。

数据解读：硬门槛和程序化断言占掉了判别力的绝大部分，而成本在秒级、噪声接近零，所以它们应该承担否决权。感知相似只能作分项，因为它的失效模式是被尺寸稀释（杯子挪 30 厘米、头顶一个洞都在这一层逃掉）。VLM rubric 和 pairwise 只适合开放设计类的排序，不能用来补偿功能失败。（判别力依据 [实验记录 §2](../middle_processing/vc_data/90_local_experiments.md)、[Blender 实验记录 §3.4](../middle_processing/vc_data/10_blender_tasks.md)；分层原则见 [Verifier 调研 §6.1](../middle_processing/vc_data/04_verifier.md)）

每次改动 Verifier，先跑变异测试和注入测试，过了才上线。被准入测试弃掉的 case 比新造的任务更值钱：它们精确指出了 Verifier 的盲区（[实验记录 §4](../middle_processing/vc_data/90_local_experiments.md)）。两个场景的造题里，被弃的「杯子倒置」暴露了圆台翻转不改变占据，被弃的「细长部件缺失」直接催生了部件连通块这一层。先造题再补 Verifier，比先定 Verifier 再造题有效，因为盲区是被具体 case 逼出来的，不是设计阶段想出来的。

还要说清楚哪些结论现在不该拿去外推。

- 三个 three.js 场景和一个 Blender 场景，变异都是我们自己造的单处改动，真实策略产出的错误分布不一定长这样。47/47 里只有 18 个是真正留出的，其余 29 个的阈值在同一批变异上看过一眼。（[实验记录 §2.3–§2.4](../middle_processing/vc_data/90_local_experiments.md)，[红队审查 §1.4](../middle_processing/vc_data/18_redteam.md)）
- 判别力是在「单处改动」上测的。多处错误同时出现时各层会不会互相掩盖，没有测过。
- VLM judge 的数字来自 48 个 case、4 个模型、两种看图条件各 2 次，合计 768 次判定。它支撑「单次判定不可用」和「多视角不差于单视角」，但支撑不了「8 票投票就够了」这种配置级结论——逐模型的配对检验没有一个到显著，合计那一次又高估了独立性。（[实验记录 §3、§3.1](../middle_processing/vc_data/90_local_experiments.md)）
- 分部件几何的阈值是按「该放行那一档的下沿」取的，这个取法在部件数更多、尺度差更大的场景上会怎么退化，未测。

还有一族信号成本近乎为零却还没接：渲染器自己的计数器。绘制调用数、三角面数、几何体与贴图的实例数，这些数字在拿到渲染器的那一刻就能直接读出来，不需要额外渲染。它对应 [3JSBench](https://3jsbench.com/methodology) 六族判据里渲染质量那一族中的网格预算，也对应 OpenAI 官方 [Frontend prompt 指南](https://developers.openai.com/api/docs/guides/frontend-prompt)里 three.js 验收的「资源渲染不重叠」那条。它能抓的那类错误很具体：同一个形状被重复加载成几百个实例、贴图没有复用、三角面数比参考高一个数量级。3JSBench 的实测给出了量级——Muse Spark 1.3 中位数用 995 个网格、177000 个三角面，而最强的两个只用 45 个和 24 个，而且堆网格的那一个有 33% 的尝试出现绘制顺序闪烁（[3JSBench](https://3jsbench.com/)）。堆实例与闪烁同时出现，指向同一个成因。

下一步的三件事都指向同一个缺口——现在的证据全部来自我们自己构造的变异，而不是策略真实的失败模式。一是把 Verifier 接到完整的 rollout 上，统计每一层在真实产物上的触发分布与假阳率；二是把被钉死字段的清单做成造题阶段的强制产物，让 Verifier 的信息量与 Problem Statement 严格对齐；三是把开放边界边数这类不随尺寸衰减的拓扑量补成一组，因为目前只验证了一个这样的量，而它一次就救回了四层信号同时失明的那一例。

<a class="anchor" id="vf-9"></a>

## 9 At Scale, a Blind Spot Becomes Missing Data

前面所有判别力数字都在回答同一个问题：Verifier 判错的概率有多大。到了十万任务的量级，这个问题问错了。

准入测试的第一条是「参考解必须通过 Verifier」（[实验记录 §4](../middle_processing/vc_data/90_local_experiments.md)）。把它和一个系统性盲区放在一起，后果不是多一点噪声。下面这条机制链是**本项目推断**，第 1、2 步有实测（下表第一行），第 3 到 5 步是外推，没有在十万量级上量过（推断过程见 [红队审查 F1](../middle_processing/vc_data/18_redteam.md)，相关的留一层消融见 [实验记录 §8](../middle_processing/vc_data/90_local_experiments.md)）：

1. Verifier 对某一类几何有系统性盲区，例如开口曲面的体素填充无效。（实测，[实验记录 §6.1](../middle_processing/vc_data/90_local_experiments.md)）
2. 这一类的**参考解自己**就过不了准入。（实测，[实验记录 §6.1](../middle_processing/vc_data/90_local_experiments.md)）
3. 整类任务被静默丢弃，一条都不进数据集。（推断，[红队审查 F1](../middle_processing/vc_data/18_redteam.md)）
4. 数据集的各项指标反而更漂亮，因为留下来的全是 Verifier 看得准的那些。（推断，[红队审查 F1](../middle_processing/vc_data/18_redteam.md)）
5. 缺失不以噪声的形式出现，而以**某个几何类别从分布里消失**的形式出现。（推断，[红队审查 F1](../middle_processing/vc_data/18_redteam.md)）

核心发现：本项目已经实测到的六个盲区，每一个都对应一整类会被成批排除的场景。

| 已实测的盲区 | 怎么发现的 | 会被静默丢掉的场景类别 | 记录 |
|---|---|---|---|
| 开口曲面的体素填充无效 | 一道任务 32 组全挂，包围盒与参考逐位接近而该色体素 IoU 只有 0.017 | 一切用旋转成型、挤出、开壳、单面片建模的场景 | [实验记录 §6.1](../middle_processing/vc_data/90_local_experiments.md) |
| 小部件上的占据类指标退化成等值判断 | 同一道题修完上一条仍然 0%：那个部件只占 20 个体素，任何可见的朝向差都让 IoU 掉到 0 附近 | 一切以小部件的朝向或位置为考点的任务 | [实验记录 §6.2](../middle_processing/vc_data/90_local_experiments.md) |
| 文本记录跨帧累加 | 图表线的参考解报出 360 个数据标签，实际只有 12 个 | 一切带动画的图表与页面 | [图表实验 §4.4](../middle_processing/vc_data/17_chart_verifier.md) |
| 文字包围盒没过变换矩阵 | 图表线的参考解报出 171 对文字重叠，实际 0 对 | 一切含旋转、含嵌套层级的场景 | [图表实验 §4.4](../middle_processing/vc_data/17_chart_verifier.md) |
| 体素分辨率下薄部件被量化成单层 | 按部件两两算穿插时，参考解自己的最大值就是 1.0 | 一切以薄壳、薄板、细杆为主的场景 | [STATE.md](../middle_processing/vc_data/STATE.md) |
| Harness 的库加载覆盖不全 | 连撞三处：只认 ES 模块、拦截规则写死了路径结构、断网把官方 addon 一起拦了 | 一切不用 ES 模块写法、换一个 CDN、或用到 addon 的产物 | [实验记录 §11](../middle_processing/vc_data/90_local_experiments.md) |

最后那一条是做对抗测试时撞出来的，性质和前五条一样但来源不同：它不在判据里，在取证链路里（[实验记录 §11](../middle_processing/vc_data/90_local_experiments.md)）。我们的 Harness 原先只拦 ES 模块那一条引入路径；放开之后又发现拦截规则把路径结构写死了，换个 CDN 就漏；再放开之后又发现断网把官方 addon 一起拦了。三处都是正常写法。结果是正常的产物在执行门上就挂了，看起来像「模型连页面都写不对」。**取证链路覆盖不全，是一类特别容易被误读成模型能力问题的假阳性。**

数据解读：六条叠起来，带动画、含旋转、薄壳、开口面、小部件、不用 ES 模块写法的场景几乎会被成批排除——而这正是真实前端与 three.js 作品的主流形态。六个盲区全部是假阳性，也就是把正确产物判挂；六个全部不是阈值问题，调阈值一个也修不掉；真因分三类——坐标系、帧、取证链路的覆盖面，没有一类是随机失效，全是整类失效。

所以 Verifier 的验收指标要多一条，而且它不是准确率：**准入拒绝率按场景特征分层之后必须是均匀的**。本项目目前的准入拒绝在两个场景上是 1/10 和 2/16（补上部件连通块层之后后者降为 0/16，[实验记录 §4](../middle_processing/vc_data/90_local_experiments.md)），但从来没有按「有没有开口面、有没有动画、有没有嵌套旋转、部件厚不厚、用哪种方式引库」分层看过。只要某一层的拒绝率显著高出，那一层就是盲区，而不是「那类任务本来就难造」。

这条检查很便宜：复用已有任务，按特征打标，做一次分布检验。它比再多造一万个任务重要，因为在它做之前，数据集的任何分布统计都是幸存者统计。

<a class="anchor" id="vf-10"></a>

## 10 This Verifier Only Works for Repair Tasks

前面九节的判别力数字全部来自「修复单处破坏」。真实需求不长这样，真实需求是「按描述搭出来」。换成从零搭建重测，结果是零（[实验记录 §10](../middle_processing/vc_data/90_local_experiments.md)，脚本 [scratch.py](../scripts/vc_verifier/proto/scratch.py)）。

做法很直接：起始页只保留渲染器、相机、灯光和材质，没有任何物体；需求用一段自然语言描述场景；另一档额外给参考解的四视角图。四个场景、四个模型、最多三轮。

核心发现：26 组全挂，23 组挂在第一层，而产物在人看来都是对的（[实验记录 §10、§10.1](../middle_processing/vc_data/90_local_experiments.md)）。

| 问题描述 | 首轮通过 | 末轮通过 |
|---|---|---|
| 纯文本需求 | 0/13 | 0/13 |
| 文本加参考图 | 0/13 | 0/13 |

来源：[实验记录 §10](../middle_processing/vc_data/90_local_experiments.md)。

数据解读：把其中一道题的四个产物和参考并排渲染，四个都是木色桌面加四条腿加桌上一个蓝色圆柱杯，差别只在比例——桌子的高宽比、腿的粗细、杯子的大小与位置各不相同。Verifier 判挂的理由是它们和参考不够重合，而不是它们不满足需求。

原因不在阈值，在这套判据量的东西。它量的是**绝对几何的重合度**。这在修复任务上成立，是因为修复任务的初始状态除了一处之外全都和参考一致，所以「和参考重合」等价于「那一处改对了」。换到从零搭建，这个等价关系就断了：需求没有钉死任何尺寸，模型凭什么搭出和参考同样高的桌子。

这是前面那条规则的又一次应用——Verifier 能查的信息量必须小于等于题面给出的信息量。只不过这次不是某一道题越界，是整套判据的适用范围被越界使用了。

从零搭建该怎么判，[3JSBench](https://3jsbench.com/methodology) 已经给了答案，因为它本来就是一个从零搭建的评测：695 条必查项分六族，**没有一条查绝对位置**。部件计数 223 条、结构 160 条、空间关系 157 条，三族占 78%，查的全是有几个、接在哪、挨着谁。

| | 修复型任务 | 从零搭建型任务 |
|---|---|---|
| 初始状态 | 除一处外与参考一致 | 空场景 |
| 可以查 | 与参考的绝对几何重合度 | 部件计数、连接与间隙、接触与支撑、相对比例、拓扑 |
| 本文现有判据 | 适用，三场景 47/47 | 不适用，0/26 |
| 放松阈值能不能救 | — | 不能。松到让这四个都过，等价于把第一层关掉 |

来源：[实验记录 §10.3](../middle_processing/vc_data/90_local_experiments.md)。

这条限制比它看起来严重，因为它同时解释了另外两件事。自动造题之所以只造「修复单处破坏」，不是因为那样方便，是因为现有判据只支持那一种；前面量到的难度分布之所以双峰、中间带是空的（[实验记录 §9、§15](../middle_processing/vc_data/90_local_experiments.md)），根源也在这里——单处破坏天然没有「部分做对」。

所以补相对关系那一族判据，是比再造一万道题更靠前的事。在补齐之前，用这套数据训出来的模型学到的是「照着参考改对一处」，不是「按描述搭出来」。

照着这张表写了一个只看相对关系的原型（[relational.py](../scripts/vc_verifier/proto/relational.py)）：先把场景整体归一化，再从体素里按颜色取连通块当部件，查部件个数、体量占比、相对尺度、上下关系、接触关系和开放边界，全部是比例或序关系。

核心发现：方向确实对，但做到可用的工作量和当初做绝对判据那一套相当。

| 测试集 | 绝对重合度判据 | 相对关系判据 |
|---|---|---|
| 从零搭建的每一次尝试（80 次） | 0/80 | 13/80 |
| 三个场景的带标签变异（47 例） | 47/47 | 35/47 |

来源：[实验记录 §10.5](../middle_processing/vc_data/90_local_experiments.md)。

数据解读：方向立住了——同一批人看都对的从零产物，从一次都过不了变成能过一部分。但代价是实打实的：变异集从 47/47 掉到 35/47，漏掉的十二个有共同点，相对结构没变，腿还连在桌面上、杯子还接触桌面、比例还在容差内。**这不是实现不好，是定义上的交换**：换来对整体尺度的不变性，就放弃了对绝对位置与绝对尺寸的敏感。部件最多的那个场景仍然是 0，因为部件一多，匹配本身就不稳。（[实验记录 §10.5](../middle_processing/vc_data/90_local_experiments.md)）

所以本文的结论要收得更紧一点：**前面九节量出来的判别力，只覆盖了两类任务里的一类。** 另一类的判据还停在原型阶段，而真实需求主要落在另一类上。

<a class="anchor" id="vf-11"></a>

## 11 Half of Aesthetics Is a Deterministic Check

审美通常被当成「只能靠人或靠模型」的那一类，于是整个推迟到最后。实测下来这个划分太粗：审美里有一半能做成零噪声的程序化判据，而且**现有的功能侧判据对这一半几乎完全瞎**。

做法（[审美调研 §6](../middle_processing/vc_data/19_aesthetics.md)，跑测脚本 [run_aes.js](../scripts/vc_verifier/web/run_aes.js)）：在 Web 那套 harness 上加一个只读计算样式与几何的探针，不比像素、不调模型，查排版层级、字号尺度、字体族数、行高、间距节奏、色相数量、对比度等十一条。阈值先在参考页上测出来再加余量冻结。然后造 20 个变异——12 个只破坏审美不破坏功能（页面照跑、不报错、不溢出、不遮挡），其中 1 个事后判为无效变异；8 个是合法改版（换品牌色、换一套自洽的等比尺度、深色主题、加留白、类名重命名、压缩 HTML）。

核心发现：11 个有效的纯审美缺陷里，功能侧判据只「抓到」2 个，而那 2 个还是因为改色顺带破坏了对比度才被规则引擎抓到的（[审美调研 §6.2](../middle_processing/vc_data/19_aesthetics.md)）。

| 口径 | 审美判据 | 功能侧判据 |
|---|---|---|
| 参考页 | 11 条全过 | 全过 |
| 纯审美缺陷（11 个有效变异） | 抓到 9 | 抓到 2，且都是顺带 |
| 合法改版（8 个） | 误杀 0 | 误杀 0 |
| 单个变异耗时 | 约 0.8 秒，两个视口 | 约 4.9 秒 |

来源：[审美调研 §6.2](../middle_processing/vc_data/19_aesthetics.md)；功能侧耗时见 [Web verifier 实测](../middle_processing/vc_data/14_web_verifier.md)。

数据解读：标题层级反了、字号变成一堆相近的随机值、四种字体混用、行高压到 1.02、间距全换成奇数、抹掉所有内外边距——这六类功能侧一个都看不见，而它们正是「这页看着不像人做的」的主要来源。审美判据把其中大部分补上了，成本还只有功能侧的六分之一。（[审美调研 §6.2](../middle_processing/vc_data/19_aesthetics.md)）

两条必须放弃当闸，这比抓到几个更值得记（[审美调研 §6.3](../middle_processing/vc_data/19_aesthetics.md)）：

- **圆角一致性**：参考页本来就有四种圆角，变异推到六种，判别余量不够。
- **栅格对齐**：该挂的那个变异对齐率是 0.707，而一个**不该挂、而且审美更好**的改版是 0.765，可分离区间只剩 0.058。更要命的是它在极端处会翻向——把所有内外边距抹掉之后，对齐率反而是 1.000。**能把好坏分开，不等于能当闸。**（[审美调研 §6.3](../middle_processing/vc_data/19_aesthetics.md)）

还有一条预设要去掉：不要假定页面按 4 像素栅格排布。参考页是手写的、规则引擎全过，但它的间距只有 57.8% 落在 4 的倍数上，最合适的基数是 2，命中 91.4%（[STATE.md](../middle_processing/vc_data/STATE.md)）。基数应该从页面自己身上测出来，不是写死。

更大的一个陷阱在经典的计算美学指标上（[审美调研](../middle_processing/vc_data/19_aesthetics.md)）。那一批指标（对称性、平衡、密度之类）**全部单调可刷**，拿它们当 reward，最优解是一张空白单列页。公开实测也不支持它们：

- 非单调：一项 72 人的偏好实验里，Ngo 那一族指标得分最高的布局反而最不受欢迎，最受偏好的是中等对称度（[Salimun 2013 博士论文](https://theses.gla.ac.uk/4256)）。
- 真实网页上失效：把 14 项指标做成工具输入完整网页，只有 1 项和审美吸引力对得上（[Purchase et al. 2011](https://eprints.gla.ac.uk/54578)）。
- 越接近好越不准：用 GPT-4 给 UI 设计稿提反馈，设计师按反馈迭代、界面变好之后，反馈被评为准确的比例从首轮的 52% 降到后续轮的 39%（[Duan et al. CHI 2024](https://arxiv.org/abs/2403.13139)）。**这类信号在接近最优时会反向。**

还有一条划了边界：「AI 味」在单页尺度上测不出来。单页能查的只是**具名特征**——Inter 字体、白底紫渐变这一类已知默认（[Anthropic 前端设计博客](https://claude.com/blog/improving-frontend-design-through-skills)点名的就是这几个）。在本项目 20 个页面里，注入了这组默认的那一页被命中、品牌蓝渐变的改版不误报（[审美调研 §6.2](../middle_processing/vc_data/19_aesthetics.md)），但它量的是「像不像那几个已知模板」，不是「平庸不平庸」。

这不是推断，是实测出来的反证（[审美调研 §4](../middle_processing/vc_data/19_aesthetics.md)）。拿本站两批页面算字体维度的集中度：一批 100% 用了那个被点名的字体，集中度 0.50；另一批一次都没用，集中度却是 1.00，也就是更坍塌。**一条「禁用某字体」的规则会让后者满分通过，而它恰恰是更单调的那一批。** 规则表只能查已知的默认值，查不到「收敛」本身。

真正的平庸度是分布量，要在一批产物上算集中度或熵，所以它天然不能当逐样本的 reward，只能当批次级诊断。顺带一提，收敛有一部分是被 prompt 规定出来的——Google 的 [Generative UI](https://arxiv.org/abs/2604.09577) 专门有一节把「跨次生成保持视觉一致」当成可选特性，公开的系统指令里点名推荐字体、鼓励渐变（§2.1 与附录）。这部分不用训练就能改回来。

凭人判的那一半有一个硬天花板（[DesignPref](https://arxiv.org/abs/2511.20513)）。20 位设计师各评同样 600 对设计，二元一致率只有 0.624，Krippendorff α 是 0.248，28.5% 的对子两两分歧率达到 96% 及以上；用 20 倍数据训练出来的偏好模型也只有 57.45%，做了个性化才到 60.16%。**超过这个数就该先怀疑数据泄漏**——Webthetics 广为引用的 r≈0.85，后续 [TOCHI 工作](https://doi.org/10.1145/3569889)（Eisbach et al.）报出自己模型的交叉验证 LCC 为 0.752，并指出前者原代码有训练集与验证集重叠（后一点转述自[审美调研笔记](../middle_processing/vc_data/19_aesthetics.md)，ACM 全文对本机访问受限，未能复核原句）。

这反过来说明程序化那一半的价值被低估了：它不受这个天花板约束，因为它测的根本不是「谁更好看」。

最后一条和前沿的做法正好拧着。Anthropic 那套四维评审器里（[Anthropic 工程博客：Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)），工艺这一维（排版层级、间距一致性、配色和谐、对比度）几乎整维可程序化，而官方把它**降权**，理由是模型默认就及格、没有区分力。这个判断在他们的生成分布下成立；但进了 RL 之后，恰恰是这一维能当硬闸而不会被刷——因为它查的是可测量的事实，不是偏好。可降权的是它在**排序**里的比重，不该降的是它在**门控**里的位置。

## 参考文献

1. [WorldCoder-Bench: Benchmarking Physically Grounded 3D World Synthesis](https://arxiv.org/abs/2606.01869) — Shuo Lu 等，arXiv 2026-06-01
2. [WorldBench: Evaluating LLMs on Three.js Voxel World Generation](https://arxiv.org/abs/2610.10622) — Krish Bakshi，arXiv 2026-10-07
3. [three.js r160 源码 src/scenes/Scene.js](https://github.com/mrdoob/three.js/blob/r160/src/scenes/Scene.js) — mrdoob/three.js，r160 版本
4. [3JSBench 榜单](https://3jsbench.com/) — 3JSBench 站方，2026-10-14 改判版（2026-10-15 读取）
5. [3JSBench Methodology](https://3jsbench.com/methodology) — 3JSBench 站方，2026-10-15 读取
6. [SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features](https://arxiv.org/abs/2502.14786) — Michael Tschannen 等（Google DeepMind），arXiv 2025-02-20
7. [AgentTypo: Adaptive Typographic Prompt Injection Attacks against Black-box Multimodal Agents](https://arxiv.org/abs/2510.04257) — Yanjie Li 等，arXiv 2025-10-05
8. [MLLM-as-a-Judge: Assessing Multimodal LLM-as-a-Judge with Vision-Language Benchmark](https://arxiv.org/abs/2402.04788) — Dongping Chen 等，arXiv 2024-02-07
9. [Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge](https://arxiv.org/abs/2406.07791) — Lin Shi 等，arXiv 2024-06-12
10. [Self-Preference Bias in LLM-as-a-Judge](https://arxiv.org/abs/2410.21819) — Koki Wataoka 等，arXiv 2024-10-29
11. [Frontend prompt instructions](https://developers.openai.com/api/docs/guides/frontend-prompt) — OpenAI 开发者文档（面向 GPT-5.5），2026-10-15 读取
12. [The relationship between visual interface aesthetics, task performance, and preference](https://theses.gla.ac.uk/4256) — Carolyn Salimun，University of Glasgow 博士论文，2013
13. [Investigating objective measures of web page aesthetics and usability](https://eprints.gla.ac.uk/54578) — Helen C. Purchase 等，AUIC 2011
14. [Generating Automatic Feedback on UI Mockups with Large Language Models](https://arxiv.org/abs/2403.13139) — Peitong Duan 等，CHI 2024，arXiv 2024-03-19
15. [Improving frontend design through Skills](https://claude.com/blog/improving-frontend-design-through-skills) — Anthropic，2025-11-12
16. [Generative UI: LLMs are Effective UI Generators](https://arxiv.org/abs/2604.09577) — Yaniv Leviathan 等（Google Research），arXiv v1 2026-02-24
17. [DesignPref: Capturing Personal Preferences in Visual Design Generation](https://arxiv.org/abs/2511.20513) — Yi-Hao Peng 等，arXiv 2025-11-25
18. [Predicting Rating Distributions of Website Aesthetics with Deep Learning for AI-Based Research](https://doi.org/10.1145/3569889) — Eisbach 等，ACM TOCHI，2023
19. [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Anthropic Engineering，2026-03-24

</div>

<div class="env-view" data-view="training" data-label="Training">

<nav class="toc view-toc"><h2>Contents</h2><ul><li class="l2"><a href="#tr-1"><span class="num">1</span> Two Gates Decide Whether RL Is Worth It</a></li><li class="l2"><a href="#tr-2"><span class="num">2</span> Sample Selection Carries the Algorithm</a></li><li class="l2"><a href="#tr-3"><span class="num">3</span> Reward Aggregation Must Be Multiplicative</a></li><li class="l2"><a href="#tr-4"><span class="num">4</span> Error Trajectories Train Recovery, Clean Ones Do Not</a></li><li class="l2"><a href="#tr-5"><span class="num">5</span> Self-Verification Is a Discriminator Problem</a></li><li class="l2"><a href="#tr-6"><span class="num">6</span> Hacking Does Not Show Up in the Reward Curve</a></li><li class="l2"><a href="#tr-7"><span class="num">7</span> A Four-Stage Recipe</a></li><li class="l2"><a href="#tr-8"><span class="num">8</span> What the Base Model Has to Have</a></li></ul></nav>

<a class="anchor" id="tr-1"></a>

## 1 Two Gates Decide Whether RL Is Worth It

[Qwen3 技术报告](https://arxiv.org/abs/2505.09388)在 8B 上给了一组很不客气的对照：强化学习花 17,920 GPU 小时，AIME24 得 67.6；换成 on-policy 蒸馏，1,800 GPU 小时得 74.4。算力十分之一，分数全面更高，而且 RL 完全没有抬高 pass@64（[Qwen3 表 21](https://arxiv.org/abs/2505.09388)，两臂从同一个 checkpoint 出发）。先问清楚有没有更强的教师，再决定要不要训 RL。

这条对照有一个硬限定必须带上：它的十倍效率依赖拿到教师的输出分布（原文把蒸馏的收益归因于 teacher logits），而前沿模型只提供接口、拿不到。所以可照搬的是「先问教师」这个顺序，不是「十倍」这个数字。只能拿到文本的情况下，蒸馏退化成在教师产出上做监督微调，效率优势会小得多（这一句是推断，没有直接对照）。

核心发现：该不该上 RL 不是算法问题，是任务族问题——判定越确定，RL 的信号越干净；判定越模糊，蒸馏越划算。

| 任务族 | 教师能不能做对 | Verifier 的确定性 | 决定 |
|---|---|---|---|
| 前端与 WebDev | 能，前沿模型很强 | 低，审美与布局靠 VLM judge | 先蒸馏，RL 放后面 |
| three.js 复刻类 | 很能，最强模型 pass@3 做到 96/100（[3JSBench 榜单](https://3jsbench.com/)，Astra） | 高，运行时状态可逐条断言（[3JSBench 方法论](https://3jsbench.com/methodology)） | **先蒸馏再 RL**，不是直接上 RL |
| Blender 与 CAD 复刻类 | 部分能 | 高 | 蒸馏够不着的那部分交给 RL |
| 3D 开放设计 | 不能，最强模型在隐藏契约上只有 27.8%，前四名挤在 23.0 到 27.8%（[WorldCoder-Bench 表 1](https://arxiv.org/abs/2606.01869)） | 最低，没有唯一正解 | 最后做 |

数据解读：two gates 的顺序不能颠倒，第一道闸问的是教师，第二道才问判据。three.js 复刻这一族两道闸都亮绿灯——判据干净，而且教师非常强，100 道题里 96 道至少有一次做对（[3JSBench 榜单](https://3jsbench.com/) Astra 的 pass@3，核验见 [91 号记录](../middle_processing/vc_data/91_3jsbench_verified.md)）。这种情况下先花算力做 RL 是把便宜的那一步跳过去了：蒸馏能把大部分能力以十分之一的代价搬过来，RL 该留给蒸馏之后仍然做不对的那一部分。

反过来，3D 开放设计这一族两道闸都亮红灯。注意这里的 27.8% 是模型在隐藏运行时契约上的覆盖率，不要和前面 Verifier 视图里那个 2.7% 混淆——那个 2.7% 是「截图加 VLM」这种**判定方式**的通过率（[WorldCoder-Bench 判定范式对照](https://arxiv.org/abs/2606.01869)，核验记录见 [92 号笔记](../middle_processing/vc_data/92_number_audit.md)），衡量的是判据坏掉了，不是模型做不出来。

RL 把 reward 的误差当成梯度方向反复放大，所以它只在误差结构最干净的那一格里值得付钱。审美类任务要先拆开再说：靠人判的那一半，reward 噪声来自人本身，用 RL 去优化等于把噪声刻进权重；而可程序化的那一半（排版层级、尺度、间距节奏、色相数、对比度）不经过人，判定本身没有方差，它和可访问性是同一类信号，该在早期就接进去。（人判有多吵：44 名职业 UI 设计师的标注者间一致性，八个维度的 Krippendorff α 宏平均只有 0.368，[AUV-Bench 表 8](https://arxiv.org/abs/2609.34854)。）

第二道闸是延迟的形状，不是延迟的大小。[ROLL Flash](https://arxiv.org/abs/2510.11345) 的模拟很直接（§5.2.1）：环境延迟服从均值 10 秒标准差 10 秒时，环境级异步加速 2.46 倍；均值同样 10 秒而标准差 1 秒，只有 1.16 倍；均值 50 秒标准差 5 秒，也只有 1.20 倍。真实任务同向（图 11），软件工程类 10.22 小时降到 8.32 小时，ALFWorld 13.37 小时降到 8.44 小时。

判据写成一个数（本文给的经验判据，不是文献值）：先量 verify 延迟的标准差与均值之比，小于 0.3 就别上异步，直接同步加多并发摊平。本项目混了约 0.4 秒的 three.js 断言、约 7 秒的 Cycles 终局渲染和 5 到 8 秒的 VLM judge（[本机实测，08 笔记 §2.4.2](../middle_processing/vc_data/08_rl_recipe.md)），按快慢两类各占一半推算这个比值约 0.9，慢任务占比越小比值越大，远高于 0.3，该上。

<a class="anchor" id="tr-2"></a>

## 2 Sample Selection Carries the Algorithm

稀疏二值 reward 的主要敌人是零梯度组，不是 loss 形式。组大小 8、题目通过率 0.1 时，一组全 0 的概率是 0.9 的 8 次方，即 43.1%；通过率落在 5% 到 10% 这一段时，组大小 8 有四成到七成的组拿不到任何梯度。把组大小加到 16 才把 0.1 那一档压到 18.5%。（以上是推算。[Reinforce-Ada §2](https://arxiv.org/abs/2510.04996) 原文把组大小 8 的这个数写成约 19%，那其实是组大小 16 的值。）同一篇给了实测：Qwen2.5-Math-1.5B 在 Open-R1 子集上 pass@1 只有 26.5% 而 pass@256 高达 81.3%——原文的结论是信号塌缩是欠采样的统计假象，不是模型上限。

核心发现：[DAPO](https://arxiv.org/abs/2503.14476) 的 20 分增量里，样本选择占 14 分，loss 形式只占 3 到 4 分。

| 配置（[DAPO 表 1](https://arxiv.org/abs/2503.14476)，Qwen2.5-32B 底座） | AIME24 avg@32 | 增量 |
|---|---|---|
| 朴素 GRPO | 30 | — |
| 加超长过滤 | 36 | +6 |
| 加 clip-higher | 38 | +2 |
| 加超长软惩罚 | 41 | +3 |
| 加 token 级 loss | 42 | +1 |
| 加动态采样 | 50 | +8 |

数据解读：动态采样加 8、超长过滤加 6，两项合计 14 分；clip-higher 和 token 级 loss 各只值 1 到 2 分（[DAPO 表 1](https://arxiv.org/abs/2503.14476)）。值钱的动作是「别把算力花在零梯度组和截断样本上」，不是调 loss 的写法。注意这是逐项累加的增量，换个加入顺序数字会变。落到工程上，优先级就是先把动态采样与超长过滤接通，再谈算法族。

组大小的选择是二阶的。固定总 batch 时，组大小 8、16、24、32 的渐近性能是 0.585、0.610、0.590、0.595，基本分不开；而 batch 从 512 到 768 再到 2048，渐近性能从 0.605 到 0.610 再到 0.645（[ScaleRL 附录表 1](https://arxiv.org/abs/2510.13786)）。一阶旋钮是 batch，不是组大小。本项目取组大小 8 到 16、把 batch 做大换 prompt 多样性，和 UI2Code^N 的 batch 64 配组大小 16 在同一区间（[UI2Code^N 附录 B](https://arxiv.org/abs/2511.08195)）。

稠密化的收益来自换参照系，不是变密。[TCPO](https://arxiv.org/abs/2608.01667) 的阶梯很清楚（表 3，MATH-500）：轨迹级 56.6，改成逐轮 verifier 分 59.0，只值 2.4；再加事后重标与反事实参照到 65.2，又值 6.2。方向也有定论，[FACTOR](https://arxiv.org/abs/2608.07118) 去掉时间维信用在三个环境上掉 2.1、1.9、3.5 分（ScienceWorld 掉得最多，平均 2.5），而去掉 token 内分配在 ALFWorld 上甚至涨 0.2 分（表 4）。先做轮级，不要先做 token 级。

朴素切分是反例。把轨迹按轮切开当独立样本，在 7 个问答集上的平均 EM 比同一 reward 结构的轨迹级 PPO 低 0.10 到 0.15（0.335 对 0.432、0.280 对 0.429、0.293 对 0.447，[2505.11821 表 3](https://arxiv.org/abs/2505.11821)）。原文的解释是切开之后模型过度优化局部的轮级信号，中间 reward 高、最终结果差。本文的推断是参照系错了：优势估计从「这条轨迹的其他走法」变成了「另一条轨迹的同一轮」。正确做法是在同 prompt、同轮序号上做组内标准化（TCPO 的做法），或者让轮级权重保持均值为一（FACTOR 的做法）。

<a class="anchor" id="tr-3"></a>

## 3 Reward Aggregation Must Be Multiplicative

判据不是「加法还是乘法」，而是「有没有一个分项能在不满足主目标的前提下刷高」。有这样的分项，必须门控或者删掉；全是互补约束，加权和没问题。

核心发现：同一个任务族（SVG 生成）上，两套加权和给出相反结果，差别只在分项能不能单独刷。

| 聚合方式 | 分项构成 | 结果 |
|---|---|---|
| [RULER 表 4](https://arxiv.org/abs/2609.25270) 对照的加权和 | CLIP 相似度、美学分、人类偏好分 | MMSVG-Icon 上美学分从 4.42 顶到 6.21，rubric 分从 0.395 崩到 0.262，输出 token 从 0.3k 爆到 6.3k，CLIP 从 0.266 掉到 0.232 |
| [RULER](https://arxiv.org/abs/2609.25270) 的实例级 rubric | 逐条设计意图 | rubric 分 0.683，CLIP、美学、人类偏好三项都不低于零样本 |
| [RLRF 表 5](https://arxiv.org/abs/2505.20793) 的纯加权和 | 像素误差、Canny 边缘、感知相似 | 没出事，全部 reward 加权和是最优配置 |
| [L1 附录 A.7](https://arxiv.org/abs/2503.04697) 的加法变体 | 正确性减长度偏差 | 预算违约率恒为 0%，但模型塌缩到极短推理链 |
| [L1](https://arxiv.org/abs/2503.04697) 的乘法形式 | 正确性乘长度项 | 长度遵从与性能兼顾，是作者的主方法 |

数据解读：RULER 对照组里的美学分与任务目标不对齐而且极易刷，于是它吸走全部优化压力，还顺手补偿掉另外两项的失败。RLRF 的分项全是互补的几何约束，谁也不能单独刷高。L1 的加法变体给出了最干净的机制证明：加法把硬约束变成可以牺牲主目标去换的可交易项，0% 违约率的实现方式是永远输出极短链（[RULER 表 4](https://arxiv.org/abs/2609.25270)、[RLRF 表 5](https://arxiv.org/abs/2505.20793)、[L1 附录 A.7](https://arxiv.org/abs/2503.04697)）。

同方向的独立证据还有三组。[CrEST](https://arxiv.org/abs/2608.13179) 允许 teacher 改优势符号（去掉方向门）后，52.00 掉到 46.75（表 4）。[VETTA](https://arxiv.org/abs/2610.08402) 的轮级与 token 级优势不归一化直接相加得 55.0，低于两个单项的 67.4 和 59.8（表 2，WebShop）。[OTC](https://arxiv.org/abs/2504.14870) 把工具效率项乘在正确性上，工具调用最多降 68.3% 而准确率基本不变，作者点明乘法保证效率项只在主目标满足时才生效。

落到本项目，聚合结构是硬闸相乘、连续分在闸后加权（本项目的设计，不是文献结论）：能执行、画布非空、无运行时报错是第一道乘法闸；核心断言（对象存在、数量、层级）是第二道乘法闸；细节断言、几何相似、rubric 分只在两道闸都过之后进加权，而且几何相似的权重压在 0.3 以内。美学分、全局 CLIP 与 DINO 相似度、任何与 token 数相关的项，一律不进 reward。这套结构的文献依据汇总在 [08 笔记 §1.5.2](../middle_processing/vc_data/08_rl_recipe.md)。

终止原因必须分四类走三条路，选错会训崩。正常提交给正常 reward。预算耗尽（超时、超轮数、超 token）强制提交并把 reward 乘 0.5（[SWE-Master 式 4](https://arxiv.org/abs/2602.03411)）——它的动因是硬数据：RL 初期约 20% 的轨迹遭截断，而离线复核发现这些轨迹里 24.3% 其实已经解决了问题。环境故障（容器崩、沙箱挂）mask 掉 loss 或整组丢弃。模型自己的错（代码报错、渲染空白、断言不过）给 0 或负分并正常进梯度，这是要学的信号。

把预算耗尽也当环境故障处理，有训崩的实录：SWE-Master 复现 DeepSWE 的「截断轨迹 reward 置零加 mask loss」，结果 reward 持续下降直至训练崩溃（[SWE-Master §6.3 图 12](https://arxiv.org/abs/2602.03411)）。另一侧的边界同样硬：格式错与不可执行不能和「执行了但很差」混成同一个 0，否则两者失去区分度。[CAD-Coder 附录 B](https://arxiv.org/abs/2505.19713) 只用几何距离作 reward，约 200 步后模型开始输出不可执行的代码，reward 管线拿不到反馈，RL 提前停摆；它的解法是另加格式分。本项目选择给负分，是同一思路的更强版本。

<a class="anchor" id="tr-4"></a>

## 4 Error Trajectories Train Recovery, Clean Ones Do Not

[Agent-R](https://arxiv.org/abs/2501.11425) 的修订能力测试给了最刺眼的一组数：只用最优轨迹训出来的 Llama-3.1-8B，三个环境平均修订能力 10.84；用 Agent-R 的纠错轨迹迭代三轮后是 46.75（表 3）。纯净数据训出的模型在干净 trace 上表现正常，一旦走错就回不来。[AgentRefine](https://arxiv.org/abs/2501.01702) 的对照同向，换成无错误无修正的干净数据后，held-in 的 Alfworld 略涨（49.3 对 48.5），held-out 四个任务全面下降（表 2）。

核心发现：试错不是删或留的二选一，四种成分各有各的处理，而且处理方式搞反会掉得比不处理更多。

| 轨迹成分 | 处理 | 证据 |
|---|---|---|
| 错误的动作与观察 | 删掉 | [WebClipper](https://arxiv.org/abs/2602.12852) 建依赖图找最小必要子图，剪枝后轮数降 21%、token 降 19.4%，准确率不掉 |
| 错误轮的推理骨架 | 留在上下文，不算 loss | [AgentRefine 表 2](https://arxiv.org/abs/2501.01702)：错误轮也算 loss 是全部变体里最差的一档 |
| 剪枝衔接处的思考 | 必须重写 | [WebClipper](https://arxiv.org/abs/2602.12852) 去掉上下文感知的选择性重写后，原文用词是灾难性塌缩（catastrophic collapse） |
| 负例 token | 降权到 0.8，不要删也不要给 1 | [Verification Horizon §4.4.1](https://arxiv.org/abs/2606.26300)：权重 0.0 得 37.2%、0.5 得 35.1%、1.0 得 41.8%、0.8 得 44.4% |

数据解读：删动作、留推理、重写衔接，三者缺一不可。衔接处必须重写的原因很具体：剪掉中间几步之后，后一步的思考里会引用一个已经不存在的观察，这种「不可能的思考」直接出现在训练数据里（WebClipper 的重写提示就是要求删掉对已剪观察的引用）。让单个模型自己看着删也不行，用 Qwen3-235B 直接删冗余轮的对照（Coarse Prune）在 xbench-deepsearch 上从 0.713 掉到 0.603（[WebClipper 表 1](https://arxiv.org/abs/2602.12852)）。

修复效果必须扣掉采样随机性基线。[Real-Time Repair](https://arxiv.org/abs/2608.02464) 在 55 个真错 episode 上测得（表 4）：回滚加纯重采样本身就有 16% 恢复率，只告诉模型哪条校验失败（不给数值）才到 45%。更反直觉的是，55 条带数值发现的提示里有 26 条直接带了正确答案，这一档恢复率 36%，反而不如只说「哪条校验失败」的 45%。恢复不靠喂答案，靠知道往哪看。[Repair or Resample](https://arxiv.org/abs/2608.25920) 把这件事推到极端：自我反思修复率 4.29%、critic 指导 3.73%，都不如无指导全量重跑的 6.90%。

对本项目的含义：造纠错数据之前先跑一遍纯重采样基线，把它当作对照减掉。错误还必须来自策略自己——手工注错与 agent 自身的执行错误分布不匹配，这是 [ReTerm](https://arxiv.org/abs/2610.18484) 点名的问题。

<a class="anchor" id="tr-5"></a>

## 5 Self-Verification Is a Discriminator Problem

前面 Overview 视图已经立过结论：自我验证不是最大的能力缺口。训练侧要补的那一条更窄——增益来自判别，不来自反思。

[BlenderAlchemy](https://arxiv.org/abs/2404.17672) 的第 4 轮精修拆得最干净（表 3，CLIP ViT-B/32 分）。视觉通道的总增益 2.5 分（25.7 到 28.2），其中只给评估器看图拿回 2.1 分（84%），再给生成器看图只多 0.4 分（16%）。两条附带曲线同样重要：生成器与评估器都看不见图时，四轮迭代的分数是 27.4、26.1、26.5、25.7，一路走低，没有一轮回到起点；只要评估器能看见图，曲线就不再下跌（27.6、27.6、27.6、27.8），哪怕改法是闭着眼猜的。多轮本身没有价值，有价值的是多轮里那个判别信号。

本项目在自己的 16 个修复任务上复现了这条规律，而且把它拆得更细（[本地实验记录 §7](../middle_processing/vc_data/90_local_experiments.md)）。283 组有效运行，四种反馈乘两种问题描述，每轮都用同一个 Verifier 判定，模型看不到判定理由。

核心发现：首轮挂掉之后能不能救回来，几乎完全由问题描述里有没有参考图决定，而不是由反馈的精确度决定。

| 问题描述（[本地实验 §7](../middle_processing/vc_data/90_local_experiments.md)） | 反馈给页面相机一张图 | 反馈给四视角拼图 | 反馈给场景图文本 |
|---|---|---|---|
| 纯文本需求 | 1/14 | 0/12 | 1/11 |
| 文本加参考渲染图 | 4/12 | 6/10 | 1/9 |

数据解读：纯文本描述下三种反馈合计救回 2/37，约 5%；给了参考图之后是 11/31，约 35%。四视角拼图那一格从 0/12 变成 6/10。每格分母只有 9 到 14，单格之间的比较要打折扣，合计那一行才站得住。模型不是不会改，是不知道该改成什么——让它看自己的产物，只有在它手里有一个可比对象时才有用（数据见 [本地实验 §7 与 §7.4](../middle_processing/vc_data/90_local_experiments.md)）。

还有一条反直觉的：场景图文本是四种反馈里信息最精确的，每个物体的几何类型、世界包围盒、颜色全是数字，而它在两种描述下都是最差的一档。问题描述给的是图，反馈给的是数字，模型要先把图翻译成数字才能比对，而这一步正是它不擅长的。**反馈必须和问题描述在同一个量纲上**，精确度不能替代可比性。

再加一个对照更能说明问题。第五臂只多给一样东西：Verifier 判出的那一层的**名字**，翻译成一句人话，不给阈值也不给数值（[本地实验记录 §7.2](../middle_processing/vc_data/90_local_experiments.md)）。

| 问题描述（[本地实验 §7.2](../middle_processing/vc_data/90_local_experiments.md)） | 反馈 | 首轮挂后救回 |
|---|---|---|
| 纯文本 | 四视角拼图 | 1/10 |
| 纯文本 | 拼图加层名 | 5/22 |
| 文本加参考图 | 四视角拼图 | 3/11 |
| 文本加参考图 | 拼图加层名 | 9/23 |

数据解读：层名不含任何「怎么改」的信息，它只说出「哪一类不对」，而两种描述下它都把救回率抬了一截。这一组用的是修过 bug 的 verifier，不能和上一张表直接相减。把三组放在一起，结论是一致的——给它一个可比对象，它能自己判断；给它一个外部判断，它不需要自己判断；两样都不给，只让它看自己的产物，救回率接近零。**缺的是判断，不是修改。**

这对数据构造的含义很直接：要训自检，Problem Statement 必须带可比对象，而且训练时给模型的观察通道要和那个对象同模态。只给文本需求再让它看自己的截图，训出来的是一个会反复截图但改不动的模型。

对 reward 设计的含义同样直接：既然「指出哪一维不对」就能把一部分失败救回来，那么把 Verifier 的层名作为过程信号喂回去是有价值的——但要控制剂量，否则模型会学会依赖它，评测时拿不到层名就退化。稳妥的做法是训练时给层名、评测时不给，并单独报不给层名那一档的分数。

核心发现：没有独立判据的自我修订，对前沿模型是零，对开源模型是灾难。

| 模型（[Design2Code 表 1](https://arxiv.org/abs/2403.03163)，Block 匹配分） | 直接生成 | 文本增强（自我修订的起点） | 自我修订 |
|---|---|---|---|
| GPT-4V | 85.8 | 87.6 | 88.8 |
| GPT-4o | 93.0 | 92.4 | 92.7 |
| DeepSeek-VL-7B | 39.7 | 66.1 | 30.1 |
| Idefics2-8B | 46.7 | 23.6 | 12.3 |

数据解读：Design2Code 的 484 个真实网页上，自我修订是在文本增强那一版的产物上改的。相对这个起点，它只对 GPT-4V 有约 1 个点的正收益，对 GPT-4o 已经转平（加 0.3），对两个开源模型是断崖（66.1 到 30.1、23.6 到 12.3，[Design2Code 表 1](https://arxiv.org/abs/2403.03163)）。[原文 §4.1](https://arxiv.org/abs/2403.03163) 给的解释正是本项目的核心难点：自我修订要求模型看出参考截图与自己产物截图的差异，并把差异映射回代码，这比利用文本增强难得多。差距不在生成，在「看出两张图哪里不一样」。

训法只有一条有 visual coding 实测：[ReLook](https://arxiv.org/abs/2510.11498) 的强制优化。一次 refinement 只在 reward 严格超过本轨迹内历史最佳时才接受，不达标就重采（每轮最多 10 次），10 次都不行就终止反思并采用历史最佳。效果是单调改进的轨迹，ArtifactsBench-Lite 三个随机种子平均 25.84 涨到 27.88（表 2），而且反思频率自然收敛到约 2 轮（图 5）。反面教训写在同一篇：作者先试过对退步给负 reward，模型学会减少反思次数来躲罚，原文直接称之为 reward hacking。罚分不是在压无效反思，是在压反思。

接受判据不能用单次 VLM 打分的差分。judge 的标准差能到 11.4 ELO，而模型档位之间（如 Claude 与 Qwen）只差约 40 ELO（[Verification Horizon 方差拆解](https://arxiv.org/abs/2606.26300)）。接受判据必须是重复 K 次的均值，而且差分超过两个标准差才允许判定（本文的规则）。

判别信号自己也要训，而且训小的比用大的强。[VL-RewardBench](https://arxiv.org/abs/2411.17451) 上，同族通用模型 Qwen2.5-VL 从 7B 到 72B 只从 48.0 走到 51.6；专训的 7B reward model 做到 73.1，超过 78B 通用模型 InternVL3 的 63.3 和 GPT-4o 的 65.8，代价约 190k 对比较数据（[Skywork-VL Reward 表 3 与 §3](https://arxiv.org/abs/2505.07263)）。换成专训的小 reward model，省下的是 judge 这一侧的推理卡，具体比例取决于 judge 在整条流水线里占多大，本文没有把那份负载表搬进来，所以这里不给数字。

给 judge 和 policy 的图像预算要分开算。在最便宜的那一档配置下，图像只占一条 40 步轨迹累计输入的 8%，文本历史才是大头；但那一档的前提是图被压得很小。**换成「文字还看得清」的配置，图像占比升到 16% 到 36%。**（三个数都是本项目推算，[20 号笔记 §3](../middle_processing/vc_data/20_base_model.md)。）所以「图像不是上下文爆炸的主因」这句话只在不要求可读性时成立。

这里藏着整节最该记住的一个陷阱。

核心发现：整页长截图在 Claude 标准档计费下**比小图还便宜**，因为它被压得谁也看不清，而账单上看不出任何异常。

| 做法（按 [Claude 视觉文档](https://platform.claude.com/docs/en/build-with-claude/vision) 的公式与上限推算，标准档） | 视觉 token | 宽度保真 |
|---|---|---|
| 1440 宽、900 高的一屏 | 约 1,550 | 高 |
| 1440 宽、8000 高的整页长图 | 约 616 | 约 20%，被压到 282 像素宽 |
| 同一张长图切成 9 片 | 约 13,950 | 约 96% |

数据解读：最自然的做法——把整页截下来丢进去——既最便宜又完全看不清，而且它不会报错、不会超限、账单还更好看。**这类失败在监控上是隐形的**，只有去看模型实际收到的那张图才能发现。要文字可读就得切片，代价是 token 涨 22 倍。算式已用官方文档给的样例校验，见 [20 号笔记 §3.1](../middle_processing/vc_data/20_base_model.md)。

所以预算优先级是：先设历史滑窗，再定分辨率与切片策略，最后才考虑换成文本。滑窗取 3 张有实测依据：[OpenCUA](https://arxiv.org/abs/2508.09123) 的消融里，从 3 张加到 5 张只有边际收益，却多约 3K token 并拖慢收敛（图 10 与正文）。

顺带纠正一个容易用错的口径：「多视角拼图比分开发图省 8 倍」不是同口径比较——那两个数字的像素量本身就差 12 倍。**同像素下拼图只省约 12%**（本项目推算，[20 号笔记](../middle_processing/vc_data/20_base_model.md)）。想真正省 token 只有降分辨率一条路，而降分辨率直接伤可读性。

<a class="anchor" id="tr-6"></a>

## 6 Hacking Does Not Show Up in the Reward Curve

看 reward 曲线找 hacking 是无效的。[ARA](https://arxiv.org/abs/2602.01750) 在 500 条真实样本与 500 条高 proxy 的 exploit 样本上测检测力（表 2）：proxy reward 自己给出 0.91 对 0.89，差 0.02，没有区分力；GPT-4 作检测器 0.78 对 0.34，差 0.44；专训的 Auditor 0.82 对 0.19，差 0.63。proxy 不可能检出自己的漏洞，这是定义决定的。

还有一条更麻烦的：通用 LLM judge 榜也验不出来。[CHERRL](https://arxiv.org/abs/2606.04923) 实测里，部分遭 hack 的模型在 Arena-Hard 上不降分，self-praise 偏置的 10.5 还高于无偏置的 8.5（表 3）——同样的 hacking 模式把通用 judge 一起骗了。

但「用程序化的 held-out 判据来验」这句话有一个前提，很容易漏掉：**held-out 判据不能和训练判据同源。** 如果 held-out 只是换了题、判据仍是同一套分层 Verifier，那么 Verifier 的盲区会让训练分和 held-out 分一起涨，第一条告警结构性失效。本项目的设计现在正好踩在这个坑上。

修法不贵：held-out 里必须至少含一路与程序化信号盲区互补的判据，并且单独报它的曲线。最便宜的选择是多模型 VLM 投票——本项目已经量过两者的盲区是互补的（[本地实验记录 §3.3 与 §3.4](../middle_processing/vc_data/90_local_experiments.md)）：VLM 擅长「有没有这个东西」，程序化信号擅长「这个东西的尺寸对不对」，4 模型 8 票投票在 48 例里漏掉的几例全是定量几何偏差，而程序化信号漏掉的那一例（车床体顶部的洞）靠 VLM 抓回来。两路曲线同时涨才算真涨。

核心发现：可用的告警信号都不在 reward 曲线上，而且每条都能写成阈值。

| 监控量 | 告警判据 | 阈值来源 |
|---|---|---|
| proxy 与 held-out 的散度 | proxy 在 100 步窗口内涨 0.05 以上（0 到 1 量纲）而 held-out 变化不为正 | [CHERRL 附录 A](https://arxiv.org/abs/2606.04923) 扫的 reward 差阈值是 0.08 到 0.12 |
| 高分桶的捷径占比 | 分数不低于 0.99 的桶（样本数不少于 20）里命中捷径模式的比例不低于 20% | [CHERRL 附录 A](https://arxiv.org/abs/2606.04923) 扫的是 15% 到 30% |
| 输出长度 | 中位输出 token 的 100 步滚动涨幅超过 1.5 倍，或超过基线加三个标准差 | 建议值；机制与量级来自 [RULER 表 4](https://arxiv.org/abs/2609.25270) 的 0.3k 到 6.3k |
| 单项 rubric 饱和 | 任一分项通过率不低于 0.95 且 100 步内增幅不低于 0.15，而 gold 总分增幅不超过 0.02 | 建议值，上线前校基线 |
| 自内化间隙 | 把 rubric 放进评测侧上下文前后的分数差见顶后连续 50 步不再上升 | 建议值；依据是 [2605.12474](https://arxiv.org/abs/2605.12474) 实测见顶点与参考 panel 共识分峰值相差不超过 75 步 |
| verifier 通过率与人工抽检 | 自动通过率落在人工抽检的 Wilson 95% 区间之外 | 建议值 |
| 有效渲染率 | 截图有效率低于 80% | [ReLook](https://arxiv.org/abs/2510.11498) 训练中把它从约 40% 提到约 80% |

数据解读：前两条是定义式判据，后面几条是便宜的前哨。所有阈值都按 100 步滚动窗口算，并先对指标做 5 步中心平滑（CHERRL 附录 A.1 的做法）。时间窗很窄：[CHERRL](https://arxiv.org/abs/2606.04923) 六个设定的 onset 分布在第 68 步到第 478 步之间，差了 7 倍，所以不能只在固定步数做一次体检；而 onset 之后 100 步内捷径行为的发生率至少再涨 40%——从告警到灾难只有约 100 步，告警必须自动化。

规划的 400 步落在 onset 分布的中段，必须全程监控：六个设定里有四个的 onset 在 400 步以内（68、91、116、301 步）；code gaming 这一类的 Goodhart 分叉点确实晚到约 1,000 步（[ARA §5.1](https://arxiv.org/abs/2602.01750)），[GLM-4.5](https://arxiv.org/abs/2508.06471) 的指令跟随 RL 在约 1,000 步内也没观察到明确 hacking（图 9），但不能拿最晚的那一类当规划依据。hacking 不是必然发生的，它和 reward 的「可主动制造」程度强相关。把硬门槛做成程序、把可测量属性交给程序、judge 只判不可测的部分，这三条做到，攻击面就小得多。

还有一条针对渲染场景的直接证据（[Verification Horizon §3 图 6](https://arxiv.org/abs/2606.26300)）：只看源码加固定截图的静态 judge 会遭长度利用，模型学会写越来越冗长的 CSS 与 JavaScript 来抬分；真跑一遍的交互式 judge 避开了这种 hacking，因为 reward 来自运行时行为，而且 RL 中测试分更高、输出长度稳定。这是 Verifier 视图那条「reward 要来自运行时状态」在训练侧的独立印证。

本场景特有的代理指标每轮都该算分布而不是均值：绝对定位占比、页面 OCR 出的文字量、画布尺寸与设备像素比、场景图对象数与三角面数、硬编码常量数、自检轮数、单条轨迹的视觉 token 消耗。自检轮数要双向看——太少是逃避反思，太多是刷观测。

<a class="anchor" id="tr-7"></a>

## 7 A Four-Stage Recipe

阶段 0 不产出模型，但跳过它后面全部白做。出闸条件：同一产物取证两次关键断言 100% 一致；变异测试判别力不低于 12/13（本项目原型多视角加体素做到 13/13，[本地实验记录](../middle_processing/vc_data/90_local_experiments.md)）；注入样本一律得 0；在 50 条已标注轨迹上量出噪声地板并写进配置；三类终止原因能自动分开且环境故障有独立计数器。

核心发现：四个阶段的量级可以从公开配方反推，而且冷启动的量级是万条级别，不是百万级别。下表是本文的规划，不是实测。

| 阶段（规划，推导见 [08 笔记 §4.1.2](../middle_processing/vc_data/08_rl_recipe.md)） | 数据量级 | 算法选择 | 监控指标 | 验收标准 |
|---|---|---|---|---|
| S1 冷启动 SFT | 8K 到 15K 条轨迹，three.js、Blender、前端各约三分之一，平均 10 到 20 步 | 纯 SFT；错误轮留上下文不算 loss，负例 token 权重 0.8 | 格式合规率、工具调用成功率、平均轮数 | 工具协议零格式错；在留出任务上能走完全流程；平均轮数不超过教师的 1.2 倍 |
| S2 拒绝采样 | 3K 到 5K 个任务各采 8 到 16 次，保留率预期 10% 到 35%，出 5K 到 20K 条 | 按分层 Verifier 筛，每题留 2 到 3 条择短 | 每题 pass@N 分布、保留率、每题留存条数 | 保留率落在 10% 到 35%；低于 5% 回去补 S1，高于 60% 说明任务太简单 |
| S3 RL | 3K 到 8K 个任务，取 S2 里 pass@N 落在 0 与 0.9 之间的那些；batch 64、组大小 8 到 16、300 到 500 步 | 单轮用 DAPO 四件套；10 到 40 步多轮用 GRPO 加轮级优势；超过 50 步换 PPO 配 VAPO 四件套 | 前一节七条告警；全对组与全错组占比；环境故障率；取证 flaky 率 | held-out 人工分与 train reward 同向；环境故障率低于 2%；高分桶捷径占比低于 20% |
| S4 迭代 | 用 S3 的 ckpt 重做 S2，再训一轮 | 迭代自蒸馏：RL 模型的输出替换冷启动数据重做 SFT | 每轮重算 pass@N 与 Verifier 校准 | 新一轮的 held-out 人工分超过上一轮两个标准差 |

数据解读：UI2Code^N 的真实配置是 400 步、batch 64、组大小 16（[UI2Code^N 附录 B](https://arxiv.org/abs/2511.08195)），和这里的 S3 规划几乎重合，可以直接当规划基线。

但 S1 那一行的量级要重新想。SFT 的饱和点有实测：[SWE-Master](https://arxiv.org/abs/2602.03411) 从 0 扩到 60K 条轨迹，解决率从 6.2% 涨到 57.8%，48K 之后才趋平（§6.1 图 11）。S1 规划的 8K 到 15K 只走到饱和点的两成到三成，也就是说**曲线最陡的那一段被跳过了**，然后用 RL 去追本来加数据就能拿到的分——而同一篇的 RL 增益只有 3.6 个点（32B）到 5.8 个点（4B），和 SFT 扩数据的 51.6 个点差一个数量级。

同一篇工作还给了第三个选项，而且它的收益比 RL 大得多。

核心发现：在一个已经很强的 SFT 基线之上，RL 只加 3.6 分，而用验证器做推理时选择加了 12.4 分（[SWE-Master 主表与 §5](https://arxiv.org/abs/2602.03411)）。

| 做法（[SWE-Master 主表与 §6.1](https://arxiv.org/abs/2602.03411)，SWE-bench Verified） | 分数 | 相对 SFT 基线 |
|---|---|---|
| 零 SFT 数据（扩数据曲线的起点） | 6.2 | — |
| SFT 到约 60K 条轨迹 | 57.8 | 基线 |
| 再加 RL | 61.4 | 加 3.6 |
| 不加 RL，改成采 8 次再用验证器选 | 70.2 | 加 12.4 |
| 既加 RL 又做推理时选择 | 70.8 | 加 13.0 |

数据解读：最后两行只差 0.6 分，也就是说在这个设定下，RL 的那点增益几乎被推理时选择吃掉了。而推理时选择要的东西，恰恰是本文前面四个视图一直在造的那个——一个能把多个候选解排序的验证器。它不需要训练策略模型，不需要 rollout 集群，做完就能用（[SWE-Master](https://arxiv.org/abs/2602.03411) 的验证器本身是一个模拟执行反馈的 LLM）。

这给出一个顺序上的建议：**先扩数据，再接推理时选择，最后才考虑 RL**。前两步共用同一套验证器，而且都不依赖训练基础设施。

所以正确的做法不是直接把 S1 加到 48K，而是先用一次多臂实验把这三件事的边际增益量出来：15K 加 RL、48K 不加 RL、48K 加推理时选择、48K 加 RL 加推理时选择。在它出结果之前，S3 的预算都是拍的。这个四臂设计来自 [18 号红队记录 §3](../middle_processing/vc_data/18_redteam.md)。

需要注意口径：上面这组数字来自软件工程任务，不是 visual coding。可迁移的是结构——有一个靠谱的验证器时，推理时选择是比 RL 便宜得多的杠杆；不可直接迁移的是具体幅度。零 SFT 直接上 RL 在本场景不可行（本文判断）——要学的是工具调用协议加多轮自检行为，基座完全没有这个格式，绝大多数 rollout 会卡在格式错得 0 分，组内无方差。每题留几条也有实测（[SWE-Gym 表 6](https://arxiv.org/abs/2412.21139)，7B，SWE-bench Lite）：留 1 条 9.0%、留 2 条 9.7%、留 3 条 7.7%、不设上限 9.3%，同题内优先留轮数少的。

停训与回滚规则只有四条，但要写死在流程里（本文规则，推导见 [08 笔记 §4.3.4](../middle_processing/vc_data/08_rl_recipe.md)）。held-out 人工分连续两个评测点不涨而 train reward 还在涨，立即停并回滚到人工分最高的 ckpt，先修 Verifier。任一代理指标的分布出现双峰，或 95 分位数相对 S2 基线涨 3 倍以上，停下抽 20 条人工看。环境故障率超过 5%，暂停修基础设施，不要在高故障率下继续训，因为组基线遭污染之后差答案也能拿到正优势。取证 flaky 率相对校准时翻倍，停下给 Verifier 加确定性约束。

成本要先算清，再决定 rollout 形态。下面一组全部是推算，不是实测，假设写在表后，算式见 [08 笔记 §2.2](../middle_processing/vc_data/08_rl_recipe.md)。

| 形态（推算，[08 笔记 §2.2.2](../middle_processing/vc_data/08_rl_recipe.md)） | 1024 并发 rollout 的渲染 CPU | 折 48 核机器 |
|---|---|---|
| 多轮 three.js | 43 核 | 0.9 台 |
| 多轮 Blender（自检走 Workbench，终局走 Cycles） | 365 核 | 7.6 台 |
| 单轮 three.js | 129 核 | 2.7 台 |
| 单轮 Blender | 1,670 核 | 34.9 台 |

数据解读：多轮形态下渲染池几乎免费，因为轨迹墙钟遭解码占满，渲染只占百分之几；单轮形态把墙钟从 1200 秒压到 80 秒而取证成本不变，单位成本涨 15 倍，这时才需要独立渲染集群（推算见 [08 笔记 §2.2.2](../middle_processing/vc_data/08_rl_recipe.md)）。假设有五条：每条轨迹 40 个模型步、其中 12 步带渲染自检、终局取证重复 3 次测 flaky、轨迹墙钟 1200 秒（单序列约 25 token 每秒）、单位成本取本机 48 核配额下的实测吞吐（three.js 一次完整取证 3.35 核秒，Blender Workbench 一个视角 3.09 核秒，Cycles 一个视角 7.04 核秒）。常驻 worker 能省掉每进程约 1 秒的启动与加载，这里不扣，算保守。

一轮 RL 的总量同样是推算，而且这里有一个容易漏掉的放大项：动态采样会把「全对或全错」的组丢掉重采，通过率落在 5% 到 10% 这一段时，组大小 8 下实际要采的轨迹是名义值的 1.76 到 2.97 倍（即 1 除以非零梯度组的比例）。先给名义值：400 个优化步乘 64 个 prompt 乘组大小 8，等于 204,800 条轨迹；乘上重采放大之后是 36 万到 61 万条，对应 2.2 万到 3.8 万 GPU 小时——**比它自己引作参照的 Qwen3 纯 RL 的 17,920 小时还高**（[Qwen3 表 21](https://arxiv.org/abs/2505.09388)）。规划预算时要按放大后的数算。渲染 CPU 折 2.5 机日（多轮 three.js）到 21 机日（多轮 Blender）；GPU 按 64 张做 rollout 加 64 张做训练算，名义上约 12,800 GPU 小时，计入重采放大后是 2.2 万到 3.8 万。渲染型 Verifier 不改变成本量级，改变的是工程复杂度。这里的 GPU 假设是一个 30B 量级的 MoE 在 8 卡上服务约 128 条并发序列，本机未实测。

异步解耦的参数也要定死。staleness 取 1 到 2 代，不要贪：[AReaL](https://arxiv.org/abs/2505.24298) 实测吞吐从 27.1k 涨到 47.8k token 每秒，76% 的提升在第一代就拿到了，再加到 16 代只多 9%（表 7）；而精度风险是超线性的——不开解耦 PPO 时，staleness 4 把 AIME24 从 42.0 砍到 23.3，近乎腰斩（表 2）。各家默认值独立印证这个区间：[ROLL Flash](https://arxiv.org/abs/2510.11345) 取 2（Takeaway 3），[NeMo-RL](https://github.com/NVIDIA-NeMo/RL/blob/main/docs/guides/async-grpo.md) 默认 1，[verl](https://github.com/verl-project/verl/blob/main/docs/advance/fully_async.md) 建议小于 1（它的口径是陈旧样本比例，不是代数）。

配方之外，还有四件事要按顺序做。一是把前端、复刻、开放设计三族分开立项，前端那族先只做蒸馏对照，用它量出「判定模糊的任务族上 RL 到底亏多少」，目前这个判断只有 Qwen3 一组跨域数字支撑。二是在真实 rollout 上量每一层 Verifier 的触发分布与假阳率，现在的判别力全部来自我们自己构造的单处改动变异。三是把前一节的七条告警接成自动化，阈值先在 S2 的拒绝采样数据上校一遍基线，因为 [CHERRL](https://arxiv.org/abs/2606.04923) 里 onset 之后的窗口只有约 100 步，靠人看曲线来不及。四是先训一个专用的小 reward model 再开 S3，它既省 judge 侧的推理卡，也是压低 judge 噪声的直接手段（单次 judge 的标准差可到 11.4 ELO，[Verification Horizon](https://arxiv.org/abs/2606.26300)）。

<a class="anchor" id="tr-8"></a>

## 8 What the Base Model Has to Have

前面七节都在讲数据和训法，但有一件事没定：用什么底座。visual coding 对底座的要求和纯文本编码不一样，而且公开证据足够把几个旋钮的优先级排出来。各条的原始表号汇总在 [20 号笔记](../middle_processing/vc_data/20_base_model.md)。

**视觉输入不可替代，但「让模型自己把图描述成文字」是负收益。**

核心发现：视觉输入的价值取决于那条文本通道对任务是否信息完备，而这个价值跨越一个数量级。

| 形态 | 视觉输入的净价值 | 代表数字 |
|---|---|---|
| 让模型先把截图描述成文字再决策 | 约等于零或负 | 两篇独立复现：先描述再行动 17.6 低于不描述 18.5（[OpenCUA 表 6](https://arxiv.org/abs/2508.09123)）；先写图注再写码 81.1 约等于直接写 81.2（[ChartMimic 表 5](https://arxiv.org/abs/2406.09961)） |
| 用图注替代图 | 恢复一半 | 只给代码 79.06，加图注 81.74，给真图 90.95（[ArtifactsBench](https://arxiv.org/abs/2507.04952) 判别消融） |
| 用精确的结构化文本替代图 | 经常反超图 | 结构化候选 39.1 对截图标注 20.3（[SeeAct 表 3](https://arxiv.org/abs/2401.01614)）；图表转表格后回答 38.2 到 67.6（[DePlot](https://arxiv.org/abs/2212.10505)，ChartQA 人写题） |
| 图作为结构化文本之外的补充 | 弱正，常在噪声内 | 三个交互基准上分别是减 0.9、加 0.5、加 1.6，都在标准误量级（[WorkArena 表 2](https://arxiv.org/abs/2403.07718)） |
| 图是唯一信息源 | 强正 | 两个真实站点任务从 2.3 到 43.2、从 7.1 到 59.5（[WebVoyager 表 1](https://arxiv.org/abs/2401.13919)） |

数据解读：本文要训的任务——判断自己写的代码渲染出来对不对——落在最后一档，而它的辅助通道（场景图、DOM）落在第三档。两者都要，而第一档必须避开。这解释了前面那个反直觉的实验结果：给模型场景图文本当反馈是四种里最差的一档。场景图的价值在于它**由程序从运行时状态直接读出**，不经过模型；一旦让模型自己去做这个转译，价值就没了。

还有一条佐证：[Plot2Code](https://arxiv.org/abs/2405.07990) 让纯文本 GPT-4 拿着从标准答案里抽出的精确描述去写码，评分 7.36，到了多模态 GPT-4V 7.68 的 95.8%。精确文本化极其有价值，模型自己文本化毫无价值——区别只在谁来做这件事。

这里有一条容易踩错的分叉，必须钉死：**规划「要写成什么结构」有用，描述「图里有什么」没用。** 让模型先识别布局分区、规划层级再写码，涨 3.1 分（[UI2Code^N 表 12](https://arxiv.org/abs/2511.08195)，88.6 对 85.5）；让模型先把截图描述一遍再写码，是减 0.1 到减 0.9（上表第一行的两例）。前者在做抽象，后者在做转译，而转译这一步正是会引入幻觉的地方——[ChartMimic](https://arxiv.org/abs/2406.09961) 直接把原因写出来了：先生成图注可能引入幻觉，导致后续代码出错。

还有一条和推理时选择连得上：[Flame](https://arxiv.org/abs/2503.01619) 测「先解释再写码」，三种风格里 pass@1 两种变差，而 pass@3 与 pass@5 两种变好。**它提高的不是单次质量，是多样性。** 所以这种提示放进 best-of-N 里有价值，放进单次生成里是负收益——和前面那条「先扩数据、再接推理时选择、最后才考虑 RL」是同一个方向。

但场景图单独用会欠载：只给结构图 13.6%、只给视觉 45.7%、两者一起 63.5%（[GraphEQA 表 2](https://arxiv.org/abs/2412.14480)）。颜色这类属性在转译中会丢（[DePlot](https://arxiv.org/abs/2212.10505)）。**两路必须交叉核对**，这和本文量到的「按几何类名断言，29 个变异只判对 14 个」是同一个病（[本地实验记录 §2.1](../middle_processing/vc_data/90_local_experiments.md)）。

**分辨率是第一旋钮，编码器规模不是。**

核心发现：在算力配平的对照里，提分辨率比加 LLM 参数值 8 倍以上（DocVQA 加 33.7 对加 4.0，[PaliGemma 2 表 13](https://arxiv.org/abs/2412.03555)）。

| 对照 | 算力变化 | 分数变化 |
|---|---|---|
| 分辨率 224 到 336（[MM1](https://arxiv.org/abs/2403.09611)） | — | 约加 3% |
| 编码器参数翻倍（[MM1](https://arxiv.org/abs/2403.09611)，ViT-L 到 ViT-H） | — | 不到 1% |
| 3B 上分辨率 224 到 448（[PaliGemma 2 表 13](https://arxiv.org/abs/2412.03555)） | 4.6 倍 | 文档问答加 33.7 |
| 224 分辨率上 3B 到 10B（[PaliGemma 2 表 13](https://arxiv.org/abs/2412.03555)） | 3.7 倍 | 加 4.0 |

数据解读：但分辨率的饱和点由**源图的原生分辨率**决定，不由模型决定。前端整页截图长边常在 3000 到 10000 像素（本文估计），属于高分辨率文档那一侧，不能按小图基准外推。一个具体的反例：TextVQA 的原图平均只有约 950 乘 811 像素，[Monkey](https://arxiv.org/abs/2311.06607) 把输入放到 1344 乘 896 后这一项反而略掉，原文的解释正是源图本身不够大。

顺带纠正一个常见的方向错误：「文字看不清」不是瓶颈。文字是最早饱和、最不可训的那一维，同一批模型在 Design2Code 文字项上的极差只有 2.7 个点（[UI2Code^N 表 2](https://arxiv.org/abs/2511.08195)），而 SFT 加 RL 带来的位置项增益是文字项的十倍（0.129 对 0.013，[ScreenCoder 表 2](https://arxiv.org/abs/2507.22827)，ScreenBench）。真正的瓶颈是大图上的**元素召回**与**布局层级**——[DCGen](https://arxiv.org/abs/2406.16386) 统计到 85% 的错误是漏掉元素。

最后，堆分辨率必须配结构信号与压缩。[TextMonkey](https://arxiv.org/abs/2403.04473) 把分辨率从 896 提到 1344 而不压 token，DocVQA 反而从 64.1 掉到 54.9（表 IX）；同文统计的冗余 token 占比随分辨率从 448 档的 26.6% 涨到 1334 档的 59.5%。

规模这一维有一个值得注意的反例：在图到码这类任务上，一个 9B 的原生分辨率多模态模型 GLM-4.1V 在 Design2Code 拿到 64.7，而 72B 的通用多模态模型 Qwen2.5-VL 只有 41.9（[GLM-4.5V/4.1V 报告](https://arxiv.org/abs/2507.01006)，对照项是 GLM 团队自测）——参数差 8 倍，分数反过来。这说明在这个任务族里，底座的**视觉处理方式**比参数量更决定上限。

**一个可执行的起点配置**（推断，不是实测，推导见 [20 笔记 §6.2](../middle_processing/vc_data/20_base_model.md)）：9B 量级的原生分辨率多模态稠密底座，像素面积预算放到八百万以上，文本上下文 64K；当前视口给一张 1440 宽的截图，历史只留三张低分辨率；单条轨迹的视觉 token 设上限；场景图走摘要而不是转储，并与视觉通道交叉核对。

还要提防一个假象：有的评测里文字类子分看着很高（Design2Code 文字项 GPT-4o 到 98.6），那是因为它是条件型指标——只在已匹配上的区块里算，漏掉的区块根本不进分母（[Design2Code](https://arxiv.org/abs/2403.03163) 的指标定义）。**用它判断「文字够不够清楚」会得到完全错误的结论。**

三个该先做的实验，都是半天到一天：渲染图上的多图崩溃点（现有多图结论全部来自自然图基准，没有一条在渲染图上测过）、长截图的有效宽度、以及文字识别分数与 image-to-code 分数的相关性——最后一条零成本，本次调研没有找到做过的公开工作。

## 参考文献

1. [Qwen3 Technical Report](https://arxiv.org/abs/2505.09388) — Qwen Team（An Yang 等），2025-05-14
2. [3JSBench 榜单](https://3jsbench.com/) — 3JSBench 站方，2026-10-14 改判版
3. [3JSBench Methodology](https://3jsbench.com/methodology) — 3JSBench 站方，2026-10-14 改判版
4. [WorldCoder-Bench: Benchmarking Physically Grounded 3D World Synthesis](https://arxiv.org/abs/2606.01869) — Shuo Lu 等，2026-06-01
5. [AUV-Bench: Aesthetic Understanding and Generation Evaluation for User Interfaces](https://arxiv.org/abs/2609.34854) — Zhijie Deng 等，2026-09-28
6. [Part II: ROLL Flash – Accelerating RLVR and Agentic Training with Asynchrony](https://arxiv.org/abs/2510.11345) — Han Lu 等，2025-10-13
7. [Reinforce-Ada: An Adaptive Sampling Framework under Non-linear RL Objectives](https://arxiv.org/abs/2510.04996) — Wei Xiong 等，2025-10-06
8. [DAPO: An Open-Source LLM Reinforcement Learning System at Scale](https://arxiv.org/abs/2503.14476) — Qiying Yu 等（ByteDance Seed），2025-03-18
9. [The Art of Scaling Reinforcement Learning Compute for LLMs](https://arxiv.org/abs/2510.13786) — Devvrit Khatri 等（Meta），2025-10-15
10. [UI2Code^N: UI-to-Code Generation as Interactive Visual Optimization](https://arxiv.org/abs/2511.08195) — Zhen Yang 等，2025-11-11
11. [TCPO: Turn-Level Credit Policy Optimization](https://arxiv.org/abs/2608.01667) — Sicong Liao 等，2026-08-03
12. [How Much, Then Where: Credit-Conserving Action-to-Token Allocation for Multi-Turn Agent RL（FACTOR）](https://arxiv.org/abs/2608.07118) — Lichao Ma 等，2026-08-07
13. [Reinforcing Multi-Turn Reasoning in LLM Agents via Fine-Grained Reward Structure and Credit Assignment](https://arxiv.org/abs/2505.11821) — Quan Wei 等，2025-05-17
14. [RULER: Instance-aware Rubric Rewards for SVG Generation](https://arxiv.org/abs/2609.25270) — Hangyu Ran 等，2026-09-21
15. [Rendering-Aware Reinforcement Learning for Vector Graphics Generation（RLRF）](https://arxiv.org/abs/2505.20793) — Juan A. Rodriguez 等，2025-05-27
16. [L1: Controlling How Long A Reasoning Model Thinks With Reinforcement Learning](https://arxiv.org/abs/2503.04697) — Pranjal Aggarwal 等，2025-03-06
17. [Teach the Magnitude, Not the Direction: Verifier-Bounded Credit Assignment for Multi-Turn Multi-step LLM Agents（CrEST）](https://arxiv.org/abs/2608.13179) — Zechuan Wang 等，2026-08-13
18. [VETTA: Coordinating Turn- and Token-Level Credit Assignment for Multi-Turn LLM Agents](https://arxiv.org/abs/2610.08402) — Jiaju Chen 等，2026-10-06
19. [Acting Less is Reasoning More! Teaching Model to Act Efficiently（OTC）](https://arxiv.org/abs/2504.14870) — Hongru Wang 等，2025-04-21
20. [SWE-Master: Unleashing the Potential of Software Engineering Agents via Post-Training](https://arxiv.org/abs/2602.03411) — Huatong Song 等，2026-02-03
21. [CAD-Coder: Text-to-CAD Generation with Chain-of-Thought and Geometric Reward](https://arxiv.org/abs/2505.19713) — Yandong Guan 等，2025-05-26
22. [Agent-R: Training Language Model Agents to Reflect via Iterative Self-Training](https://arxiv.org/abs/2501.11425) — Siyu Yuan 等，2025-01-20
23. [AgentRefine: Enhancing Agent Generalization through Refinement Tuning](https://arxiv.org/abs/2501.01702) — Dayuan Fu 等，2025-01-03
24. [WebClipper: Efficient Evolution of Web Agents with Graph-based Trajectory Pruning](https://arxiv.org/abs/2602.12852) — Junjie Wang 等，2026-02-13
25. [The Verification Horizon: No Silver Bullet for Coding Agent Rewards](https://arxiv.org/abs/2606.26300) — Binghai Wang 等，2026-06-24
26. [Real-Time Detection and Repair of LLM Agent Failures](https://arxiv.org/abs/2608.02464) — Sunny Dubey，2026-08-03
27. [Repair or Resample? Rethinking Failure Debugging in LLM Multi-Agent Systems](https://arxiv.org/abs/2608.25920) — Zhongwen Luan 等，2026-08-26
28. [ReTerm: Recovery Training for Self-Improving Terminal Agents](https://arxiv.org/abs/2610.18484) — Wei Xie 等，2026-10-13
29. [BlenderAlchemy: Editing 3D Graphics with Vision-Language Models](https://arxiv.org/abs/2404.17672) — Ian Huang 等，2024-04-26
30. [Design2Code: Benchmarking Multimodal Code Generation for Automated Front-End Engineering](https://arxiv.org/abs/2403.03163) — Chenglei Si 等，2024-03-05
31. [ReLook: Vision-Grounded RL with a Multimodal LLM Critic for Agentic Web Coding](https://arxiv.org/abs/2510.11498) — Yuhang Li 等，2025-10-13
32. [VL-RewardBench: A Challenging Benchmark for Vision-Language Generative Reward Models](https://arxiv.org/abs/2411.17451) — Lei Li 等，2024-11-26
33. [Skywork-VL Reward: An Effective Reward Model for Multimodal Understanding and Reasoning](https://arxiv.org/abs/2505.07263) — Xiaokun Wang 等（Skywork），2025-05-12
34. [Claude 视觉文档（Vision）](https://platform.claude.com/docs/en/build-with-claude/vision) — Anthropic，访问于 2026-10-15
35. [OpenCUA: Open Foundations for Computer-Use Agents](https://arxiv.org/abs/2508.09123) — Xinyuan Wang 等，2025-08-12
36. [Adversarial Reward Auditing for Active Detection and Mitigation of Reward Hacking（ARA）](https://arxiv.org/abs/2602.01750) — Mohammad Beigi 等，2026-02-02
37. [Reproducing, Analyzing, and Detecting Reward Hacking in Rubric-Based Reinforcement Learning（CHERRL）](https://arxiv.org/abs/2606.04923) — Xuekang Wang 等，2026-06-03
38. [Reward Hacking in Rubric-Based Reinforcement Learning](https://arxiv.org/abs/2605.12474) — Anas Mahmoud 等，2026-05-12
39. [GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models](https://arxiv.org/abs/2508.06471) — GLM-4.5 Team（智谱），2025-08-08
40. [Training Software Engineering Agents and Verifiers with SWE-Gym](https://arxiv.org/abs/2412.21139) — Jiayi Pan 等，2024-12-30
41. [AReaL: A Large-Scale Asynchronous Reinforcement Learning System for Language Reasoning](https://arxiv.org/abs/2505.24298) — Wei Fu 等，2025-05-30
42. [NeMo-RL 文档：Async GRPO](https://github.com/NVIDIA-NeMo/RL/blob/main/docs/guides/async-grpo.md) — NVIDIA，访问于 2026-10-15
43. [verl 文档：Fully Async Policy](https://github.com/verl-project/verl/blob/main/docs/advance/fully_async.md) — verl 项目，访问于 2026-10-15
44. [ChartMimic: Evaluating LMM's Cross-Modal Reasoning Capability via Chart-to-Code Generation](https://arxiv.org/abs/2406.09961) — Cheng Yang 等，2024-06-14
45. [ArtifactsBench: Bridging the Visual-Interactive Gap in LLM Code Generation Evaluation](https://arxiv.org/abs/2507.04952) — Chenchen Zhang 等（腾讯混元），2025-07-07
46. [GPT-4V(ision) is a Generalist Web Agent, if Grounded（SeeAct）](https://arxiv.org/abs/2401.01614) — Boyuan Zheng 等，2024-01-03
47. [DePlot: One-shot visual language reasoning by plot-to-table translation](https://arxiv.org/abs/2212.10505) — Fangyu Liu 等（Google），2022-12-20
48. [WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks?](https://arxiv.org/abs/2403.07718) — Alexandre Drouin 等（ServiceNow），2024-03-12
49. [WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models](https://arxiv.org/abs/2401.13919) — Hongliang He 等，2024-01-25
50. [Plot2Code: A Comprehensive Benchmark for Evaluating MLLMs in Code Generation from Scientific Plots](https://arxiv.org/abs/2405.07990) — Chengyue Wu 等，2024-05-13
51. [Advancing vision-language models in front-end development via data synthesis（Flame）](https://arxiv.org/abs/2503.01619) — Tong Ge 等，2025-03-03
52. [GraphEQA: Using 3D Semantic Scene Graphs for Real-time Embodied Question Answering](https://arxiv.org/abs/2412.14480) — Saumya Saxena 等，2024-12-19
53. [MM1: Methods, Analysis & Insights from Multimodal LLM Pre-training](https://arxiv.org/abs/2403.09611) — Brandon McKinzie 等（Apple），2024-03-14
54. [PaliGemma 2: A Family of Versatile VLMs for Transfer](https://arxiv.org/abs/2412.03555) — Andreas Steiner 等（Google DeepMind），2024-12-04
55. [Monkey: Image Resolution and Text Label Are Important Things for Large Multi-modal Models](https://arxiv.org/abs/2311.06607) — Zhang Li 等，2023-11-11
56. [ScreenCoder: Advancing Visual-to-Code Generation for Front-End Automation via Modular Multimodal Agents](https://arxiv.org/abs/2507.22827) — Yilei Jiang 等，2025-07-30
57. [Automatically Generating UI Code from Screenshot: A Divide-and-Conquer-Based Approach（DCGen）](https://arxiv.org/abs/2406.16386) — Yuxuan Wan 等，2024-06-24
58. [TextMonkey: An OCR-Free Large Multimodal Model for Understanding Document](https://arxiv.org/abs/2403.04473) — Yuliang Liu 等，2024-03-07
59. [GLM-4.5V and GLM-4.1V-Thinking: Towards Versatile Multimodal Reasoning with Scalable Reinforcement Learning](https://arxiv.org/abs/2507.01006) — GLM-V Team（智谱），2025-07-01

本项目内部记录（KML 网关 /view 链接，非公开）：[90 本地实验记录](../middle_processing/vc_data/90_local_experiments.md)、[92 数字核验记录](../middle_processing/vc_data/92_number_audit.md)、[08 RL 配方笔记](../middle_processing/vc_data/08_rl_recipe.md)、[20 基座笔记](../middle_processing/vc_data/20_base_model.md)、[91 3JSBench 核验](../middle_processing/vc_data/91_3jsbench_verified.md)、[18 红队记录](../middle_processing/vc_data/18_redteam.md)。

</div>

<div class="env-view" data-view="domains" data-label="Domains">

<nav class="toc view-toc"><h2>Contents</h2><ul><li class="l2"><a href="#dm-1"><span class="num">1</span> Charts Are the Output Where Tolerance Disappears</a></li><li class="l2"><a href="#dm-2"><span class="num">2</span> Read the Drawn Geometry, Not the Configuration Object</a></li><li class="l2"><a href="#dm-3"><span class="num">3</span> The Mutation Set Audits the Verifier Before It Rates the Model</a></li><li class="l2"><a href="#dm-4"><span class="num">4</span> On the Web the Errors Are Not Visual Errors</a></li><li class="l2"><a href="#dm-5"><span class="num">5</span> Playability Fails on Coverage, Not on Accuracy</a></li><li class="l2"><a href="#dm-6"><span class="num">6</span> The State Interface Cannot Depend on the Model's Cooperation</a></li><li class="l2"><a href="#dm-7"><span class="num">7</span> Web First, Charts Second, Games Third</a></li></ul></nav>

<a class="anchor" id="dm-1"></a>

## 1 Charts Are the Output Where Tolerance Disappears

前面讲 3D Verifier 时，每一条判据都带着容差：剪影 IoU 要大于 0.9，体素 IoU 要大于 0.5，颜色距离要小于 60（[3D 本机实验记录 第 2 节](../middle_processing/vc_data/90_local_experiments.md)）。容差是被迫的，因为「画得对不对」没有数值真值可比。换到图表和矢量图，这个前提消失了：输入数据已知，产物能被还原成数值再逐个比对。判定可以不带容差。

本机实测给出了这条路的噪声地板（下文本节数字均出自[图表 Verifier 实验记录](../middle_processing/vc_data/17_chart_verifier.md)第 4 节，Chart.js 4.4.6 单任务）。同一个参考页面重复渲染 5 次，几何回读的柱子坐标与坐标轴刻度像素位置逐位完全相同，截图的摘要值只有 1 种。这不是「噪声很小」，是这一环确实为零。参考解自己跟自己比，逐值回读的最大相对误差是 0.15%，而这 0.15% 每次都一样，来自图表库把柱子底边画在零线下方约半个像素的固定偏置，不是随机抖动。判据的容差定在 1%，对它有 6 倍余量。

核心发现：三类程序化信号在同一批变异上的判别力差了一个档，而像素比对的失败不在阈值。

| 信号 | 判对 | 漏判 | 误杀 |
|---|---|---|---|
| 逐值回读 | 13/16 | 3 | 0 |
| 像素比对 | 9/16 | 3 | 4 |
| 结构断言 | 14/16 | 2 | 0 |
| 逐值回读或结构断言 | 16/16 | 0 | 0 |

来源：[图表 Verifier 实验记录 §4](../middle_processing/vc_data/17_chart_verifier.md)，16 个带标签变异，无留出。

数据解读：逐值回读漏掉的三个变异全部不是数据错，分别是轴截断、图表类型画错、轴标题连单位一起丢掉。轴截断那一个尤其说明职责边界：y 轴从 500 起画，柱子的几何仍然精确编码着原数值，线性拟合外推到零线之下读出 0.00% 误差，这是正确行为而不是失灵。轴范围归结构断言管。结构断言漏掉的两个全部是纯数据错，整列缩放 1.3 倍和单点把 1510 画成 1150，结构完全合法。两边盲区精确互补，所以取或就是 16/16（[图表 Verifier 实验记录 §4.3 逐变异表](../middle_processing/vc_data/17_chart_verifier.md)）。

像素比对不是不够准，是在这件事上不存在可用的工作点。它漏掉的单点画错只让 0.75% 的像素发生变化，图例与数据错位只让 0.01% 的像素变化；而它误杀的四个全是纯外观改动，换配色让 30.51% 的像素变化，柱子变窄 14.13%，图例挪到底部 11.32%（[实验记录 逐变异表](../middle_processing/vc_data/17_chart_verifier.md)）。要抓住 0.01% 就得把阈值压到千分之一以下，那时 30.51% 会被误杀得更彻底。信号与噪声在量纲上直接重叠，中间没有空隙。

成本也站在回读这边。17 个页面各起一次浏览器，单页全流程中位 840 毫秒，其中渲染约 470 毫秒、截图约 110 毫秒，而回读只要 1 到 4 毫秒，是渲染耗时的千分之四（[实验记录 耗时表](../middle_processing/vc_data/17_chart_verifier.md)）。这个比例决定了回读可以放进 RL 的每一步，而截图不行。

这一节要立住的判断只有一条：图表与矢量图是目前唯一能把 Verifier 这一环的噪声压到零的产出形态。零噪声是质量上的优势，不等于它该排第一——入场顺序还要看工程成本和供给规模，后面那一节会给出完整排序。它不是「像素比对的更严格版本」，而是换了一个被测量——像素比对量的是两张图有多像，逐值回读量的是屏幕上那根柱子到底有多高。

<a class="anchor" id="dm-2"></a>

## 2 Read the Drawn Geometry, Not the Configuration Object

零容差的前提是回读读的是真东西。读图表库的配置对象做不到这一点：那里的数值是模型自己写进去的，模型画错了，读回来的还是那份对的数字。同样的道理在 Tasks 视图里已经出现过一次——判据必须落在状态上而不是落在代码上——换成图表，落点从场景图变成绘制几何。

正确的通道是从绘制结果反推。先由两个坐标轴刻度的像素位置拟合出数值与像素的线性映射，再取柱子顶边和底边两个像素反算它代表的数值。矢量图这边更直接，读图元自身的高度属性，配合两个刻度文本的位置换算。两条路都不读任何源码常量（判据定义见[图表 Verifier 实验记录 §1.1](../middle_processing/vc_data/17_chart_verifier.md)）。

核心发现：注入一个已知倍率的错误，回读报出来的偏差与理论值对得上。

| 被测页面 | 逐值回读最大相对误差 | 注入的错误 |
|---|---|---|
| 矢量图参考版 | 0.02% | 无 |
| 矢量图问题版 | 24.99% | 柱高统一乘 0.75，理论偏差 25% |
| 画布参考版 | 0.15% | 无，残差来自底边半像素偏置 |

来源：[图表 Verifier 实验记录 §4.5](../middle_processing/vc_data/17_chart_verifier.md)。

数据解读：24.99% 对上理论值 25%，说明回读量到的是真实绘制几何，而不是任何中间变量。矢量图路线的残差比画布路线低一个档，因为它没有底边偏置。0.02% 的残差意味着这条通道几乎没有系统误差可言（[图表 Verifier 实验记录 §4.5](../middle_processing/vc_data/17_chart_verifier.md)）。

抗伪造同样靠这个落点。把正确数据写进配置、再用自定义绘制画出错误的柱子，配置回读会放行，几何回读不会。把数值用文字写对、柱子画错，交叉检查会抓住：数据标签的文本必须与同位置柱子的几何回读值自洽。在离屏画布上另画一张正确的图，也骗不过「只认挂在文档里、有尺寸、未隐藏的那块画布」这条规则，这条规则是从 3D 线原样搬过来的（[3D 本机实验记录](../middle_processing/vc_data/90_local_experiments.md)）。

Harness 不要求模型配合暴露任何东西，理由和 3D 线相同：训练时模型只会学会写那一行，换一套 Harness 就失效。图表这边有两条不需要页面配合的替代路径。第一条是图表库由环境提供，Harness 自己起本地服务下发，页面不许访问外网，库在谁手里实例注册表就在谁手里。第二条是在页面脚本之前接管画布文字绘制接口——所有画布文字都必须经过它，拦住就拿到全部文字，与用哪个图表库无关。本机参考解抓到 33 段文字，包括轴标题、图例、刻度、主标题和 12 个数据标签，一段不漏（[图表 Verifier 实验记录 §2.2](../middle_processing/vc_data/17_chart_verifier.md)）。

位图回读是另一条路，但它不够格。公开工作的天花板是 [DePlot](https://arxiv.org/abs/2212.10505) 在 PlotQA 合成图上 94.2 的 RMS_F1（[论文 表 4](https://arxiv.org/abs/2212.10505)），在分布外的 TaTa 真实图上掉到平均约 78%（[论文 §6.2](https://arxiv.org/abs/2212.10505)，只标注了 10 张图）。拿这个当 reward，噪声地板比要测的效应还大。做 RLVR 只能走文档对象或运行时通道。

<a class="anchor" id="dm-3"></a>

## 3 The Mutation Set Audits the Verifier Before It Rates the Model

本机实测跑出 16/16 之前，Verifier 自己出了三个 bug（[图表 Verifier 实验记录 §4.4](../middle_processing/vc_data/17_chart_verifier.md)）。三个都制造假阳性，也就是把正确的产物判挂；三个都不是阈值问题，调阈值一个也修不掉。

核心发现：假阳性的真因全部在坐标系和帧，不在判据的松紧。

| 症状 | 真因 | 修法 |
|---|---|---|
| 参考解报告数据标签 360 个而不是 12 个，动画变异被误杀 | 每帧重绘都把所有文字重画一遍，文字钩子把 240 帧的记录全存了下来 | 给每条记录打帧号，只取最后一个画了字的帧 |
| 动画变异的逐值回读误差 2.70%，超过 1% 判据 | 只推了 30 帧虚拟时间 480 毫秒，而动画时长 800 毫秒，读到的是中间态 | 推到 240 帧，虚拟时间 3.84 秒 |
| 参考解报告 171 对文字重叠，实际 0 对 | 图表库普遍先平移旋转再在局部坐标里写字，钩子记的是局部坐标，旋转文本全堆在原点 | 文字包围盒四角过一遍当前变换矩阵；矢量图侧改用页面坐标接口 |

来源：[图表 Verifier 实验记录 §4.4](../middle_processing/vc_data/17_chart_verifier.md)。

数据解读：修掉这三个 bug 之后，逐值回读从 12/16 变 13/16，结构断言从 13/16 变 14/16。两个提升全部来自消除假阳性，而判据里的四个阈值从写下到最终结果一个没动（[图表 Verifier 实验记录 §4.4](../middle_processing/vc_data/17_chart_verifier.md)）。

三条推论。第一，假阳性比假阴性难发现得多。前两个 bug 的表现都是「某个不该挂的变异挂了」，如果变异集里没有「不该挂」的那一半，它们会一直潜伏到 RL 里变成纯噪声。该挂与该放行各占一半的变异集，第一价值是体检 Verifier，不是评模型。第二，坐标系是这类 Verifier 的头号坑：表里两个 bug 出在帧，一个出在坐标系，而矢量图的值回读又踩了第二次坐标系的坑。凡是位置参与判定的检查，都要先问这个坐标在哪个系里。矢量图的值回读还要再分一层：刻度位置必须用图形自身坐标系，页面坐标只能给重叠和溢出用，混用会凭空多出一个缩放因子，本机实测把 25% 的偏差读成了 75%（[实验记录 §4.4](../middle_processing/vc_data/17_chart_verifier.md)）。第三，修的是 Harness，不是阈值。

这条推论反过来约束了准入测试的设计。Tasks 视图讲过，准入测试决定任务从哪来；这里补一句：准入测试的第一个被测对象是 Verifier 自己。

<a class="anchor" id="dm-4"></a>

## 4 On the Web the Errors Are Not Visual Errors

Web 侧没有「像素噪声淹没信号」这个问题。参考页自己跟自己比，截图的平均绝对差是 0.000，相同像素占比 1.0000，噪声地板为零（下文本节本机数字均出自 [Web Verifier 实验记录](../middle_processing/vc_data/14_web_verifier.md) 第 4 节）。问题出在另一头：11 个该挂的变异里有 7 个在桌面宽度的首屏截图上与参考完全相同，相似度 1.0。零噪声加四成检出，说明截图这个观测口就是看不到这些错误。

状态本来就可读，所以确定性信号比 3D 侧更强。本机参考页是一个带地标结构、导航、卡片网格、标签页、表单校验、模态框、哈希路由和主题持久化的单页，判据分五层：正确性、布局与响应式、可访问性、交互状态机、性能预算，门控是乘法的，任一层挂即判挂（[Web Verifier 实验记录 §1、§4.1](../middle_processing/vc_data/14_web_verifier.md)）。

核心发现：五层组合在 22 个带标签变异上零漏零误，而单一观测口无论怎么选阈值都到不了（[Web Verifier 实验记录 §4.4~4.5](../middle_processing/vc_data/14_web_verifier.md)）。

| 信号 | 判对 | 检出 11 个该挂 | 误杀 11 个不该挂 |
|---|---|---|---|
| 单张截图逐像素，阈值取最优 | 14/22 | 4 | 1 |
| DOM 标签序列一致 | 11/22 | 2 | 2 |
| 类名序列一致 | 8/22 | 0 | 3 |
| 可见文本一致 | 11/22 | 0 | 0 |
| 正确性层 | 13/22 | 2 | 0 |
| 布局与响应式层，三视口 | 13/22 | 2 | 0 |
| 可访问性层 | 15/22 | 4 | 0 |
| 交互状态机层 | 14/22 | 3 | 0 |
| 性能预算层 | 12/22 | 1 | 0 |
| 五层组合 | 22/22 | 11 | 0 |

来源：[Web Verifier 实验记录 §4.5 判别力表](../middle_processing/vc_data/14_web_verifier.md)。

数据解读：22 个变异里 16 个是开发集、6 个是留出集，标签先写死，阈值只在参考页的 5 次重复上校准、在任何变异体上一次都没调（[Web Verifier 实验记录 §4.3](../middle_processing/vc_data/14_web_verifier.md)）。11 条该挂的全部挂在设计时预期的那一层（[同上 §4.5](../middle_processing/vc_data/14_web_verifier.md)）。类名序列这个朴素判据检出 0/11、误杀 3/11，比随机还差——它只能抓到「换了类名」这件事本身，而换类名正是最常见的等价重写。可见文本一致同样检出 0/11。朴素结构判据失效的原因是它们绑在实现手法上，而类名、标签名、CSS 写法、事件绑定方式、单位、字体栈、是否压缩这七样都可以在视觉与功能完全等价的前提下任意更换（[同上 §5.3](../middle_processing/vc_data/14_web_verifier.md)）。

像素信号的阈值无处可放。要抓住对比度降级那一条，阈值必须设在 0.9883 以上；但换配色这个合法重写的像素差是 0.9002，内联图标那条是 0.9999（[实验记录 逐变异表](../middle_processing/vc_data/14_web_verifier.md)）。合法重写的像素差比大多数真缺陷都大。这与 3D 侧的情况不同：3D 侧是逐像素 12/29，而单个 VLM judge 在 48 例上的判对率是 79% 到 96%（[3D 本机实验记录 §2.1、§3](../middle_processing/vc_data/90_local_experiments.md)），VLM 比像素强得多；Web 侧那 7 个该挂的变异在视觉上和参考完全一样——删掉替代文本、按钮换成普通容器、摘掉表单校验、启动时同步忙等、脚本尾部未定义变量、主题不落存储，图上都没有任何痕迹。VLM 在这里的替代空间比 3D 侧更小，不是因为 VLM 弱，是因为这些错误压根不是视觉错误。

核心发现：五层各有不可替代的贡献，没有一层是摆设。

| 层 | 只有它抓到的真缺陷 | 是哪几条 |
|---|---|---|
| 可访问性 | 4 | 对比度降级、缺替代文本、按钮换成普通容器、标题跳级加地标丢失 |
| 正确性 | 2 | 资源 404、运行时未捕获异常 |
| 交互状态机 | 2 | 表单校验被摘掉、主题不持久化 |
| 布局与响应式 | 1 | 窄视口横向溢出 |
| 性能预算 | 1 | 启动时的长任务 |

来源：[Web Verifier 实验记录 §4.5 唯一贡献表](../middle_processing/vc_data/14_web_verifier.md)。

数据解读：多视口是必需的一维而不是锦上添花。只看桌面单视口是 12/22、检出 1/11，加上手机与平板两档后是 13/22、检出 2/11（[实验记录 §4.7](../middle_processing/vc_data/14_web_verifier.md)）。差的那一条是卡片写死固定宽度：它在桌面宽度下一切正常，三列、无溢出、无越界，到手机宽度才暴露出 65 像素的横向溢出和 10 个越界元素。检索到的公开 benchmark 里没有一家把多视口一致性做成确定性判据：[Vision2Web](https://arxiv.org/abs/2603.26648) 对桌面、平板、手机三套原型用 VLM judge 打分，[WebGen-Bench](https://arxiv.org/abs/2505.03733) 的响应式用例由 UI agent 判是非，[MV-Bench](https://arxiv.org/abs/2607.19910) 只用固定 1920×1080 单视口（检索过程见 [Web Verifier 实验记录 §3.6](../middle_processing/vc_data/14_web_verifier.md)）；而本机实测里它贡献了 11 个真缺陷中其它四层都抓不到的那一个。

可访问性是整张能力表里唯一「确定性 reward 加 RL 就能赢闭源」已被公开验证的维度。[A11yn](https://arxiv.org/abs/2510.13914) 用规则引擎 axe-core 的严重度加权违例做 GRPO 的 reward，把 Qwen2.5-Coder-7B 的违例率 IR_Axe 从 0.40 压到 0.05，低于 GPT-5.1 的 0.13、Gemini 3 Pro 的 0.24 和 Claude Sonnet 4.6 的 0.45（[论文 v2 表 2](https://arxiv.org/abs/2510.13914)）。这个数要打折：reward 与评测主指标是同一个量，所以 0.05 对 0.13 是「直接优化的量对零样本」而不是公平比较；它真正的独立证据是换一个规则引擎后的 IR_AChecker 0.26 对 0.35（同表），以及人工两两比较的胜 39.3%、平 39.3%、负 21.4%（[论文 附录 E 表 7](https://arxiv.org/abs/2510.13914)）。规则引擎本身也没有大家以为的那么自动：[axe-core 4.14.0 规则表](https://github.com/dequelabs/axe-core/blob/v4.14.0/doc/rule-descriptions.md)共 105 条规则，64 条的问题类型带 needs review，纯自动判定的只有 41 条，占 39%（本次按该表逐行重数）。

作弊是真能作弊的。手写 7 个作弊页，第一版判据挡住 5 个（[实验记录 §4.9](../middle_processing/vc_data/14_web_verifier.md)）。漏掉的两个分别是「加载时无条件把主题写成深色、切换按钮其实什么都不做」和「把不合格文字的字号设为 0、再用伪元素把同样的字画回屏幕」。第一个靠补判据修掉：每条状态机断言必须带前置态、终态和往返三段，清空存储后的初始态、操作后的终态、刷新后仍然保持、再操作一次能回去，硬编码的页面在第一条和第四条上同时挂掉。第二个修不掉——审计引擎对这个页面的输出是零违例、零需要复核、45 条通过，伪元素承载的文字它根本不检查，字号为 0 的真元素又被当成无文本跳过，两头都落空。这条对应的上游问题 [axe-core issue #2680](https://github.com/dequelabs/axe-core/issues/2680) 自 2020-12 提出至今仍是 open。纯 DOM 侧的确定性信号在这里到顶了，只能靠静态代码闸或者看屏幕上实际显示了什么。补完两条判据后做了全量回归，仍然 22/22，零新增误杀；改的全是判据，不是阈值。

第一遍跑出来的其实是 21/22，唯一误判拆开是两个性质完全不同的问题（[实验记录 §4.10](../middle_processing/vc_data/14_web_verifier.md)）。一个是 Verifier 的真 bug：列数测量用了表现型类名做选择器，类名一换就读成 0 列，修法是改成结构化定位，取主内容里第一个有两个以上子项的列表。另一个是人工标签错了：重命名脚本用全文正则，把 ARIA 角色名一起改掉了，那不是等价重写而是真的破坏了无障碍结构，审计引擎判对了。这和 3D 侧那次标注翻案是同一类事（[3D 本机实验记录 §3.4](../middle_processing/vc_data/90_local_experiments.md)）——判据判错之前，先怀疑标签。

成本可以忽略。单次完整探针 4.9 秒，但其中工具开销不到 0.5 秒：浏览器启动 181 毫秒、新开页加载 61 毫秒、注入审计引擎 72 毫秒、跑一次审计 30 到 71 毫秒、复用浏览器开页约 50 毫秒（[实验记录 §4.11](../middle_processing/vc_data/14_web_verifier.md)）。剩下全是固定的稳定等待和 40 帧采样，去掉帧采样、把等待改成事件驱动、状态机复用同一个页面上下文，可以压到 1 秒以内（推算，未实测）。22 个变异全量两遍跑完 114 到 117 秒，平均 5.2 秒一个。两遍全量重跑的判定翻面 0 条，层级列表与明细逐字节一致——确定性信号不需要多次投票，这直接省掉乘在成本上的那个系数；对照是 3D 侧的 VLM judge，最差一档温度 0 重判有 20.8% 的 case 翻面（[3D 本机实验记录 §3](../middle_processing/vc_data/90_local_experiments.md)）。

<a class="anchor" id="dm-5"></a>

## 5 Playability Fails on Coverage, Not on Accuracy

网页游戏这边，判据准不准已经不是瓶颈。[PlaytestArena](https://arxiv.org/abs/2605.28258) 的 GUI judge 与人的条目级一致率是 87.9%，而人与人之间是 91.4%，差 3.5 个百分点（[论文「Is the GUI Evaluator Reliable?」一节](https://arxiv.org/abs/2605.28258)）；[PlaySuite](https://arxiv.org/abs/2610.07127) 的里程碑式 judge 与人的「相差一级以内」一致率 90.4%，人与人 93.0%，人自己的 Krippendorff α 只有 0.624（[论文 §3](https://arxiv.org/abs/2610.07127)）。继续优化 judge 的收益已经很小。

真正卡住的是验得到验不到。

核心发现：同样的 playtest 预算，花在「再玩一遍」上几乎没有回报，花在「把状态摆到规则的前置条件上」才有。

| playtest 策略 | 能给出结论的规则占比 |
|---|---|
| 第一遍正常玩 | 40.5% |
| 再加一遍正常玩 | 41.0% |
| 把状态直接注入到规则的前置条件 | 48.5% |

来源：[A2Z GameSpec-Bench 表 4(c)](https://arxiv.org/abs/2609.39564)，50 个游戏的 86 条依赖规则，预算对齐。

数据解读：加一遍正常玩只涨 0.5 个百分点，换成状态注入涨 8.0 个百分点。逐 agent 看差距更大：正常玩的覆盖率在 13.1% 到 29.0% 之间，加状态注入后是 53.3% 到 88.0%（[A2Z 附录 F.3](https://arxiv.org/abs/2609.39564)）。碰不到的规则就是 0 信号，判据再准也没用。所以钱该花在「状态能摆到任意位置」上，而不是「训一个会玩的 agent」上——同一批十个游戏上，一个在线游戏 agent 的里程碑达成率只有 0.0% 到 42.2%，而加上对抗式注入后的判定覆盖率合计是 73.4%（[A2Z 附录 G.4 表 S20](https://arxiv.org/abs/2609.39564)；两者分母不同，论文注明不能直接相比）。

只读源码会被骗，骗的量级是可测的。源码判满分的规则，真玩时只有 76.8% 成立；反过来，源码判零分的规则里有 25.7% 真玩是对的（[A2Z §4.3](https://arxiv.org/abs/2609.39564)）。同一来源还给了一条更狠的：规则的局部通过率是 72.4%，但要求它的所有上游规则也通过，就只剩 22.7%，差 49.7 个百分点（[A2Z 附录 B.7](https://arxiv.org/abs/2609.39564)）。能跑和能玩是两个几乎正交的量，另一组消融给出了同样的方向——[Code2Games](https://arxiv.org/abs/2610.05033) 只给编译与运行诊断，构建成功率从 78.5 涨到 88.7，交互符合度只从 58.0 挪到 59.0；加了玩法断言反馈才从 59.0 涨到 75.8（[论文 表 3](https://arxiv.org/abs/2610.05033)）。

录屏加 VLM judge 这条路更直接地证伪了自己。[V-GameGym](https://arxiv.org/abs/2509.20136) 把交互代码改写成 10 秒自动演示再录屏打分，而录屏评分表里仍然留着「用户输入响应性」这一项（[论文 附录 R](https://arxiv.org/abs/2509.20136)）——全程没有发过任何一次输入。这不是实现瑕疵，是「用录屏当可玩性证据」本身的归谬。

可玩性并不是只能靠人。把「能玩」拆成 6 族 33 条子命题之后，24 条能做成纯程序判据，6 条需要 agent 真玩，3 条只能靠人（本项目的拆解设计，见[游戏 Verifier 调研记录 §1](../middle_processing/vc_data/15_game_verifier.md)，未实测）。只能靠人的那三条是好不好玩、审美和创意，而人与人在逐条 rubric 上的整体一致性本来就只有 κ=0.68（[PlaytestArena 评测可靠性一节](https://arxiv.org/abs/2605.28258)）。所以「可玩性只能靠真玩」是错的，对的说法是「可玩性不能只靠看源码和看截图」。

<a class="anchor" id="dm-6"></a>

## 6 The State Interface Cannot Depend on the Model's Cooperation

代表性的公开游戏 playtest 系统都要求游戏自己暴露状态接口：[A2Z](https://arxiv.org/abs/2609.39564) 要求每个构建提供状态设置入口与场景变更器，而且这个注入面被显式排除在不变量检查之外（[论文 附录 D.1.2](https://arxiv.org/abs/2609.39564)）；[UI-TARS-2](https://arxiv.org/abs/2509.02544) 的合成游戏同样被要求暴露显式状态接口供验证脚本读取（[技术报告 §2.5.1](https://arxiv.org/abs/2509.02544)）。训练时照搬，模型学到的就是「写那一行」。这和 3D 线不要求页面暴露场景变量是同一条原则，换了领域没有变。

核心发现：五条拿状态的路线按抗欺骗强度排序，最强的那条反而不需要知道游戏内部任何东西。

| 路线 | 怎么拿 | 骗得过吗 | 覆盖面 |
|---|---|---|---|
| 输入重放加状态差分 | 固定种子固定时钟跑多条输入轨迹，比较产物或帧哈希序列 | 最难骗，要骗必须真的实现一个会按规则响应输入的系统 | 全部 |
| 绘制调用拦截 | 预加载时接管渲染循环与绘制接口 | 几乎骗不过，这就是玩家看到的东西 | 全部画布游戏 |
| 引擎自带钩子 | 引擎自己派发的全局事件或实例注册表 | 难骗，事件由引擎发不是作者写的 | 取决于引擎 |
| 像素与音频弱监督 | 帧差与音效事件探测 | 容易骗，背景动画会让每帧都不同 | 全部 |
| 要求模型暴露接口 | 脚手架规定必须写 | 骗得过，训练时一定会被骗 | 强制 100% |

来源：本项目的路线设计，见[游戏 Verifier 调研记录 §3.1~3.2](../middle_processing/vc_data/15_game_verifier.md)，属分析结论，未实测。

数据解读：排序的依据不是强度而是性质。输入重放加状态差分把「可玩性」转成了一个不需要语义的差分问题——一条空输入轨迹、一条有输入轨迹、几条不同强度的策略轨迹，剩下的全是序列比较。3D 线的冻结时钟部分可以原样复用（[3D 本机实验记录](../middle_processing/vc_data/90_local_experiments.md)），要新建的只有输入重放。

引擎钩子这一层的现实比文档描述的糟。逐引擎读发行包源码的结果是（[游戏 Verifier 调研记录 §3.3](../middle_processing/vc_data/15_game_verifier.md)）：[three.js](https://github.com/mrdoob/three.js)、[PixiJS](https://github.com/pixijs/pixijs) v8、[Babylon.js](https://github.com/BabylonJS/Babylon.js) 的钩子由引擎自己创建，只要在页面脚本之前注入就能用；[p5.js](https://github.com/processing/p5.js) 在全局模式下连作者自己的分数变量都挂在全局对象上，但实例模式下拿不到。网页小游戏常用的 [Phaser](https://github.com/phaserjs/phaser) 3（A2Z 的 100 个任务全部基于 Phaser）恰好是最不可用的那个——它的调试全局在 3.60 到 3.90 的八个发行文件里一次都没有出现，唯一通用路子是在页面脚本前劫持它的游戏构造函数。Unity 的网页导出只给单向的 [SendMessage 消息发送接口](https://docs.unity3d.com/Manual/web-interacting-browser-js-to-unity.html)，没有返回值；Godot 的网页桥接 [JavaScriptBridge](https://docs.godotengine.org/en/stable/classes/class_javascriptbridge.html) 官方文档写明可以在构建时关掉。

还有一条比可用性更要命的限制：没有一个引擎钩子给得出游戏逻辑状态（[游戏 Verifier 调研记录 §3.3](../middle_processing/vc_data/15_game_verifier.md)）。它们给的是渲染图与场景图，分数和生命仍然在作者的闭包里。性价比最高的补法不在引擎层——拦截画布的文字绘制接口，直接从参数里读出屏幕上的分数、生命和关卡文本，完全不需要 OCR。这条路在图表线上已经实测可行（33 段文字一段不漏，[图表 Verifier 实验记录](../middle_processing/vc_data/17_chart_verifier.md)），在游戏线上尚未实测；画布游戏的 HUD 文字多半走这个接口，但这一点没有做过统计。它能把「分数会涨」从需要 agent 真玩降级成纯程序判据。

确定性回放是这一切的地基，而地基有两个硬漏点。第一个是 Web Worker 里的时钟拦截不住：[PlaySuite](https://arxiv.org/abs/2610.07127) 为此排除了 225 个 Construct 3 游戏，这是它技术性排除里最大的一类，多于「只支持拖拽」的 72 个和「多人」的 25 个（[论文 表 5](https://arxiv.org/abs/2610.07127)）。第二个是超越函数跨引擎版本会分叉：[ECMAScript 规范](https://tc39.es/ecma262/#sec-math.sin)把 Math.sin 等定为 implementation-approximated，不规定精度；调研时记录到一个物理库的现存 issue，同一份刚体仿真在两个不同版本的 V8 下结果不同（[游戏 Verifier 调研记录 §4.2](../middle_processing/vc_data/15_game_verifier.md)；原 issue 链接本次实测被对方站点拒绝访问，未能复核）。这两条决定了准入测试必须加一条硬闸：同一份代码双跑，产物不一致就不进数据集。不确定的任务进了 RL 就是纯噪声。

<a class="anchor" id="dm-7"></a>

## 7 Web First, Charts Second, Games Third

三个维度决定入场顺序：判定的确定性、工程成本、供给规模。三个领域在这三个维度上的位置并不一致，所以排序不是按「哪个最干净」排的。

核心发现：Web 在三个维度上同时占优，而且它是唯一已有公开验证的那一个。

| 领域 | 判定确定性 | 工程成本 | 供给规模 | 顺序 |
|---|---|---|---|---|
| Web 前端 | 五层组合 22/22，检出 11/11、误杀 0/11；两遍全量重跑判定翻面 0、明细逐字节一致（[Web 实验记录](../middle_processing/vc_data/14_web_verifier.md)） | 单次探针 4.9 秒，其中工具开销不到 0.5 秒，推算可压到 1 秒以内；读数全是浏览器原生接口 | 开源仓库自带大量视觉回归基线（[任务来源记录 §1](../middle_processing/vc_data/02_task_sources.md)）；可访问性这一维已有公开的确定性 reward 加 RL 结果（[A11yn](https://arxiv.org/abs/2510.13914)） | 第一 |
| 图表与矢量图 | 零容差，噪声地板实测为 0；逐值回读或结构断言 16/16（[图表实验记录](../middle_processing/vc_data/17_chart_verifier.md)） | 回读 1 到 4 毫秒；无需多视角渲染；判据只有四个阈值；与 Web 共用同一套浏览器 Harness | 渲染库自带的像素基线有 [Chart.js](https://github.com/chartjs/Chart.js/tree/master/test/fixtures) 约 667 张、[plotly.js](https://github.com/plotly/plotly.js/tree/master/test/image/baselines) 1,324 张、[p5.js](https://github.com/processing/p5.js/tree/main/test/unit/visual) 604 张、[deck.gl](https://github.com/visgl/deck.gl/tree/master/test/render/golden-images) 252 张、[OpenLayers](https://github.com/openlayers/openlayers/tree/main/test/rendering/cases) 235 个用例（GitHub API 计数，见[任务来源记录 §1](../middle_processing/vc_data/02_task_sources.md)） | 第二 |
| 网页游戏 | 24 条子命题设计上可做确定性判据，方差未测，6 条要 agent，3 条靠人（[游戏调研记录 §1](../middle_processing/vc_data/15_game_verifier.md)） | 要新建输入重放、绘制调用拦截、难度判据三件；Phaser 3 还要自己劫持构造函数 | [js13kGames](https://js13kgames.com/sitemap.xml) 2,799 个自包含作品（sitemap 实测，见[任务来源记录](../middle_processing/vc_data/02_task_sources.md)）；[PlaySuite](https://arxiv.org/abs/2610.07127) 从约 170 万个 itch.io 游戏加 1,460 个 PyWeek 游戏里筛出约 1.75 万个可执行环境，评测用其中 5,734 个；[V-GameGym](https://arxiv.org/abs/2509.20136) 收了 2,219 个 Pygame 样本 | 第三 |

数据解读：Web 排第一的理由不是它的判据最干净——图表才是唯一能把容差去掉的形态。Web 排第一是因为三件事同时成立：判别力在 22 个带标签变异上零漏零误；Verifier 的成本低到可以忽略；可访问性这一维已经有人用确定性 reward 把一个 7B 模型训到违例率低于闭源模型（[A11yn 表 2](https://arxiv.org/abs/2510.13914)）。

还有第四件，是做完上面三件之后才发现的：**审美里可程序化的那一半也挂在同一套 Web Harness 上。** 构造了 12 个只破坏审美不破坏功能的变异，其中 1 个判为无效，剩下 11 个里功能侧判据只顺带抓到 2 个，而新加的审美判据抓到 9 个、8 个合法改版零误杀，单页约 0.8 秒，是功能侧 4.9 秒的六分之一左右（[审美调研记录 §6.2](../middle_processing/vc_data/19_aesthetics.md)）。这意味着 Web 这条线一次性覆盖了两个维度——功能正确性和工艺质量——而其它两条线目前都只覆盖前者。

这四件各有折扣。零漏零误是第二遍的结果，第一遍 21/22，而且只有单参考页、6 个留出（[Web 实验记录](../middle_processing/vc_data/14_web_verifier.md)）。那项可访问性工作的训练 reward 与评测主指标是同一个量，所以它证明的是「这条链路能跑通」，不是「开源因此超过了闭源」；它的人工两两比较只有 5 名评测员、共 1,330 次判断，论文没有给显著性检验（[A11yn 附录 E](https://arxiv.org/abs/2510.13914)），稳妥的说法是人类偏好没有退化。即便都打完折，Web 仍然是目前唯一三件都有现成证据的领域，所以它是整条链路最便宜的验证实验。

图表排第二而不是第一，是因为它的优势在质不在量。零噪声意味着 reward 的方差全部来自题面歧义和模型自己，不来自判据，这正是乘法门控能够成立的前提；但它的供给面比 Web 窄，本机证据也只有单任务。把它放在 Web 之后还有一条工程理由：两者共用同一套浏览器 Harness，Web 先落地之后图表的边际成本接近零。

游戏排第三，不是因为它的判据差。24 条确定性判据同样不需要容差，但要先补三件新基础设施，而覆盖率这个瓶颈没有便宜的解法——同样的预算花在「再玩一遍」上只涨 0.5 个百分点，花在「把状态摆到前置条件上」才涨 8.0 个百分点（[A2Z 表 4(c)](https://arxiv.org/abs/2609.39564)），而后者本身就是一套要逐游戏投入的工程。

四个要打折扣的地方必须先说清楚。Web 侧是单参考页、22 个变异、其中 6 个留出，而且 22/22 是第二遍的结果，第一遍是 21/22；阈值一个没动，改的是一条测量实现和一条变异生成实现。Web 侧的作弊集补判据发生在作弊测试之后，「补完 6/7」这个数要和「第一版 5/7」一起看，剩下那一个是审计引擎的结构性盲区（[axe-core issue #2680](https://github.com/dequelabs/axe-core/issues/2680)），不是阈值能修的。图表侧的 16/16 只有 1 个任务、16 个变异，没有做留出验证，而且只测了一个图表库。游戏侧的全部数字来自公开文献，本机一行代码都没跑过，拆出来的 33 条子命题是设计而不是结论。

下一步三件事，按顺序做。第一，跑可访问性的确定性 reward 复现实验，这是整条链路最便宜也是唯一有公开背书的入口；但要把最佳实践规则和无障碍标准规则分开记账，并换第二个规则引擎做独立验证，避免 reward 和评测主指标是同一个量。第二，把 Web 的 Harness 扩成跨领域公共件，补上画布文字绘制拦截和输入重放两样——前者同时服务图表的数据标签自洽检查和游戏的分数读数，后者是游戏线唯一无法从现有组件复用的核心新件。第三，给三个领域各补一个留出被试：Web 换第二个参考页，图表补折线和饼图两个任务，游戏做第一个本机变异集；三处的阈值都一个不动，验证判别力能不能迁移。

## 参考文献

外部来源（按首次出现顺序）

1. [DePlot: One-shot visual language reasoning by plot-to-table translation](https://arxiv.org/abs/2212.10505) — Google Research，Fangyu Liu 等，2022-12-20
2. [Vision2Web: A Hierarchical Benchmark for Visual Website Development with Agent Verification](https://arxiv.org/abs/2603.26648) — Zehai He 等（智谱），2026-03-27
3. [WebGen-Bench: Evaluating LLMs on Generating Interactive and Functional Websites from Scratch](https://arxiv.org/abs/2505.03733) — Zimu Lu 等，2025-05-06
4. [MV-Bench: Benchmarking Multimodal Large Language Models for Coordinated Multi-View Interface Construction](https://arxiv.org/abs/2607.19910) — Yue Zhao 等，2026-07-22
5. [A11yn: Aligning LLMs for Web Accessibility-Aware UI Generation](https://arxiv.org/abs/2510.13914) — Janghan Yoon 等（延世大学、首尔大学），2025-10-15（引用数字取 v2，2026-09-07）
6. [axe-core 4.14.0 Rule Descriptions](https://github.com/dequelabs/axe-core/blob/v4.14.0/doc/rule-descriptions.md) — Deque Systems，v4.14.0
7. [axe-core issue #2680: Pseudo elements without position:absolute not picked up by color contrast](https://github.com/dequelabs/axe-core/issues/2680) — Deque Systems GitHub，2020-12-07 提出，仍 open
8. [GUI Agents for Continual Game Generation（PlaytestArena / Play2Code）](https://arxiv.org/abs/2605.28258) — Yixu Huang 等，2026-05-27
9. [PlaySuite: A Large-Scale Benchmark for Interactive Visual Intelligence](https://arxiv.org/abs/2610.07127) — Dheeraj Varghese 等，2026-10-05
10. [A2Z GameSpec-Bench: How Faithfully Can Coding Agents Generate Games from Game Design Specifications?](https://arxiv.org/abs/2609.39564) — Seonho Lee 等，2026-09-30
11. [Code2Games: Enabling Coding Agents for Gaming World Generation](https://arxiv.org/abs/2610.05033) — Wei Wu 等，2026-10-04
12. [V-GameGym: Visual Game Generation for Code Large Language Models](https://arxiv.org/abs/2509.20136) — Wei Zhang 等，2025-09-24
13. [UI-TARS-2 Technical Report: Advancing GUI Agent with Multi-Turn Reinforcement Learning](https://arxiv.org/abs/2509.02544) — ByteDance Seed，Haoming Wang 等，2025-09-02
14. [three.js](https://github.com/mrdoob/three.js) — mrdoob 等，GitHub 仓库
15. [PixiJS](https://github.com/pixijs/pixijs) — PixiJS 团队，GitHub 仓库
16. [Babylon.js](https://github.com/BabylonJS/Babylon.js) — Babylon.js 团队，GitHub 仓库
17. [p5.js](https://github.com/processing/p5.js) — Processing Foundation，GitHub 仓库
18. [Phaser](https://github.com/phaserjs/phaser) — Phaser Studio，GitHub 仓库
19. [Unity Manual: Call Unity C# script functions from JavaScript](https://docs.unity3d.com/Manual/web-interacting-browser-js-to-unity.html) — Unity Technologies，官方文档
20. [Godot Docs: JavaScriptBridge](https://docs.godotengine.org/en/stable/classes/class_javascriptbridge.html) — Godot Engine，官方文档（stable）
21. [ECMAScript Language Specification: Math.sin](https://tc39.es/ecma262/#sec-math.sin) — Ecma TC39，现行草案
22. [Chart.js test/fixtures](https://github.com/chartjs/Chart.js/tree/master/test/fixtures) — Chart.js 团队，GitHub 仓库目录
23. [plotly.js test/image/baselines](https://github.com/plotly/plotly.js/tree/master/test/image/baselines) — Plotly，GitHub 仓库目录
24. [p5.js test/unit/visual](https://github.com/processing/p5.js/tree/main/test/unit/visual) — Processing Foundation，GitHub 仓库目录
25. [deck.gl test/render/golden-images](https://github.com/visgl/deck.gl/tree/master/test/render/golden-images) — vis.gl，GitHub 仓库目录
26. [OpenLayers test/rendering/cases](https://github.com/openlayers/openlayers/tree/main/test/rendering/cases) — OpenLayers，GitHub 仓库目录
27. [js13kGames sitemap](https://js13kgames.com/sitemap.xml) — js13kGames，站点地图

本项目实验与调研记录

- [3D 本机实验记录（90_local_experiments）](../middle_processing/vc_data/90_local_experiments.md)
- [图表 Verifier 实验记录（17_chart_verifier）](../middle_processing/vc_data/17_chart_verifier.md)
- [Web Verifier 实验记录（14_web_verifier）](../middle_processing/vc_data/14_web_verifier.md)
- [游戏 Verifier 调研记录（15_game_verifier）](../middle_processing/vc_data/15_game_verifier.md)
- [审美调研与实验记录（19_aesthetics）](../middle_processing/vc_data/19_aesthetics.md)
- [任务来源调研记录（02_task_sources）](../middle_processing/vc_data/02_task_sources.md)

</div>

