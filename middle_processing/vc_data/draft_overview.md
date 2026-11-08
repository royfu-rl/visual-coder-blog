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

