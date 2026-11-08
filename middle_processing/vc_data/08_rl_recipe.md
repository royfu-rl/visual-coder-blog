# 08 用「渲染型 verifier」做 RL：算法、基础设施与配方

> 2026-10-15。场景：visual coding agent（写前端 / three.js / Blender 代码），
> reward 来自渲染后的程序化断言、感知指标与 VLM judge，单次评估几百毫秒到几秒。
> 与 04（verifier 设计）、05（长程轨迹修复）、06（harness 实测）配套，只写增量；
> 已被那三篇覆盖的内容在本文只做一行引用。
> 日期按 arXiv ID 推算（2610.10622 即 2026-10）。数字后面括号里是出处的节号或表号。
> 带「推算」字样的数字是本文自己算的，假设都写在旁边。

## 0. 结论速览

**算法**

1. **稀疏二值 reward 的主要敌人是零梯度组，不是 loss 形式。**
   DAPO 四件套的 20 分增量里，overlong filtering（+6）和 dynamic sampling（+8）占 14 分，
   clip-higher 和 token-level loss 各只值 1~2 分（2503.14476 表 1）。
   更狠的一句：**「signal collapse 是欠采样的统计假象，不是模型上限」**——
   同一模型 pass@1 26.5% 而 pass@256 81.3%（2510.04996 §2）。
2. **组大小 G 是二阶选择，batch size 才是一阶的。**
   固定总 batch 时 G=8/16/24/32 的渐近性能 0.585 / 0.610 / 0.590 / 0.595；
   而 batch 512→2048 把渐近性能从 0.605 抬到 0.645（2510.13786 表 1）。
3. **长程多轮（> 50 步）要用 PPO + critic，不是 GRPO。**
   两个最接近的工业系统（UI-TARS-2、VAPO）都这么选，而且 Value-Pretraining 不是可选项：
   去掉它要掉 49 分，裸 PPO 只有 5 分（2504.05118 表 1）。
4. **不要照搬「熵塌缩」的叙事。** GUI 和网页小游戏的 RL **熵经常是上升的**（2509.02544 图 8）；
   两条熵轨迹完全重合而下游差很多（2510.13786 图 16）；熵机制那篇作者自己说
   「没有观察到被干预的熵值与性能之间的关系」（2505.22617 §4.5）。
5. **长度控制用 overlong filtering（8k 档）+ 强制打断，不要用绝对长度惩罚。**
   产物长度与任务复杂度强相关，绝对阈值会系统性惩罚复杂任务。要压的是自检轮数，不是代码长度。
6. **turn 级切分不能朴素做。** 把轨迹按 turn 切开当独立样本，比任何 trajectory-level 基线都差
   **0.10~0.15 EM**（2505.11821 表 3）；`A^turn + α·A^tok` 不归一化就相加，**比两个单项任何一个都差**
   （55.0 对 67.4 / 59.8，2610.08402 表 2）。要么在「同 prompt、同 turn index」上做组内标准化，
   要么做 mean-one 守恒。
7. **稠密化的收益来自「换参照系」，不是「变密」。** TCPO 表 3：轨迹级 56.6 → 逐轮 verifier 分 59.0
   只值 **+2.4**，而 retro / hindsight / 反事实又值 **+6.2**。
   而且**时间维（哪一轮）是主因，token 维（哪个词）是次因**（FACTOR 表 4：去掉时间维信用 −3.5，
   去掉 token 内分配在 ALFWorld 上甚至 +0.2）。
8. **门控必须是乘法，五组独立证据。** 最干净的是 L1 的三变体对照（2503.04697 附录 A.7）：
   加法版的 budget 违约率恒为 0%，**但模型塌缩到极短 CoT** —— 加法把硬约束变成了可以用牺牲主目标来换的
   可交易项。另见 VETTA、FACTOR、CrEST、OTC-PO。
9. **判据不是「加法还是乘法」，而是「有没有一个分项能在不满足主目标的前提下被刷高」。**
   RULER 表 4：CLIP+Aesthetic+HPS 加权和把 Aesthetic 从 4.31 顶到 **6.70（+55%）**，
   同时 CLIP 掉 **20%**、Icon 的 rubric 分从 0.395 **崩到 0.262**、token 从 0.3k **爆到 6.3k**。
   而 RLRF 的纯加权和没出事 —— 因为它的分项全是互补的几何约束（MSE、Canny），没有「易刷项」。
10. **rubric 别调权重，去改 rubric 本身。** RaR §6：**去掉类别权重（38.8%）反而高于带全部权重（37.2%）**；
    而生成器从 Qwen-32B 换成「见过参考答案的 O3-mini」从 31.1 涨到 35.9。
    RULER 同向：universal rubric 0.591 → instance-aware **0.683**。

**基础设施**

11. **渲染 worker 池几乎免费，前提是多轮形态。** 按本机实测推算：1024 个并发 rollout，
    多轮 three.js 只要 **43 核**，多轮 Blender **365 核**；但单轮 Blender 要 **1,670 核**（2.2.2）。
    墙钟被解码占满，渲染只占百分之几。唯一的实测对照：UI2Code^N 的 RVPO 训练墙钟里
    生成 75.4% / **渲染 22.4%** / VLM 比较 2.2%（2511.08195 表 20）。
12. **慢 verifier 是方向级的阻塞，不是性能优化。** DeepSeek-R1 原文：
    「由于评测耗时长、影响 RL 效率，大规模 RL 还没有广泛应用到软件工程任务上……
    未来版本会通过拒绝采样、或在 RL 过程中引入**异步评测**来改善效率」（2501.12948 §4）。
13. **staleness 的甜点是 1~2 代，不是 8 代。** AReaL 实测 η 从 0 到 1 就吃掉 **76%** 的加速
    （27.1k→47.8k tok/s），再往上只多 9%；各家默认值（ROLL Flash α=2、NeMo-RL 1、verl < 1、
    Ring 2.6「几个优化步」）独立印证。**但算法必须配套**：不开 decoupled PPO 时 η=4 就把
    AIME24 从 42.0 砍到 23.3（2505.24298 表 2）。
14. **异步的收益来自延迟的方差，不是均值。** 环境延迟 N(10, σ=10) 时环境级异步 **2.46×**，
    N(10, σ=1) 只有 **1.16×**，N(50, σ=5) 只有 1.20×（2510.11345 §5.2.2）。
    我们的 verify 延迟是 0.4 s 到 8 s 的混合，落在高收益区。
    **判据：σ/μ < 0.3 就别做异步。**
15. **「预算耗尽」和「环境故障」必须分开，选错会训崩。**
    SWE-Master：`CONTAINER_FAILED` → mask loss；`TIMEOUT`/`MAX_STEPS` → **强制提交 + reward 乘 0.5**。
    把后者也当前者去 mask（DeepSWE 的做法），在 SWE-Master 自己的模型上导致
    **reward 持续下降直至训练崩溃**（2602.03411 §6.3 图 12）。
16. **reward 必须是独立可扩容的服务。** Ling 2.0 的 reward 系统扩到 **40K 并发请求、成功率 > 99.9%**，
    其中**已经包含一个「视觉 reward evaluator」** —— 这是「渲染后 VLM judge」最接近的工业先例。
    有界队列 +39% 吞吐，异步 reward 让训练时间最多降 30%（2510.22115 §4.4）。
17. **一轮 RL 约 12,800 GPU 小时（推算），渲染只要 2.5~21 机日。**
    和 Qwen3-8B 的纯 RL（17,920 GPU 小时）同档。渲染型 verifier 不改变成本量级，改变的是工程复杂度。
18. **但先问一句：能不能蒸馏？** Qwen3 表 21（8B，数学+代码）：
    RL **17,920 GPU 小时** → AIME24 67.6；**on-policy 蒸馏 1,800 GPU 小时** → AIME24 **74.4**。
    算力 1/10、分数全面更高，而且 RL 完全没提升 pass@64。
    **只有在「没有更强的教师」时 RL 才是唯一选项** —— 本项目的 3D 场景大概属于这一类。

**视觉 reward**

19. **图像不是上下文爆炸的主因，文本历史是。** 40 步轨迹累计输入约 1.06 M token，
    图像只占 8%（3.1.1）。做法优先级：先设滑窗（3 张，OpenCUA 实测 3→5 只有边际收益、多 3K token），
    再压分辨率，最后才考虑换成文本。
20. **别让模型把图转写成文字再推理。** OpenCUA 表 6：推理时用 L3（先描述截图）不如 L2，
    原因是描述里混进大量与任务无关的元素。但**精确的 scene graph 不在此列** ——
    它不是 caption，是无损读数，而且只要毫秒级和几十个 token。
21. **训一个 7B 专用 RM，压倒用一个 78B 通用 judge。** VL-RewardBench：
    Qwen2.5-VL 同族 7B→72B 只从 48.0 到 51.6（+3.6）；
    而专训的 Skywork-VL Reward 7B 做到 **73.1**，超过 InternVL3-78B 的 63.3 和 GPT-4o 的 65.8。
    代价只有约 190k 对比较数据。省下的是 30%~60% 的 rollout 卡（2.2.4）。
22. **不完美的 judge 也能用，但要看误差类型。** UI-TARS-2 的 ORM 只有 F1 83.8 且假阳偏高，
    RL 里仍然有效（§4）；而用关键词匹配验证视觉证据会让 hack 率反升 2.2~3.4 个点（2607.09492）。
    判据：**judge 的误差是不是可被模型主动制造的**。随机误差可容忍，可被利用的系统误差不可容忍。

**配方**

23. **SFT 冷启动的量级是 1 万 ~ 10 万条，不是百万条。** UI2Code^N 用 80K（但前面垫了 20M 图-码持续预训练）；
    DeepSeek-R1 只用「数千条」（但代价是 Dev1 在 AIME 上相对 R1-Zero 退化）；
    SWE-Master 的 scaling 曲线在 **48K 之后趋平**（05 §2.4）。
24. **零 SFT 直接 RL 在本场景不可行。** 要学的是工具调用协议 + 多轮自检行为，基座完全没有这个格式，
    绝大多数 rollout 会卡在「格式错 → 0 分」，组内无方差。
25. **hacking 不是必然发生的。** GLM-4.5 的指令跟随 RL 在约 1,000 步内没有观察到明确 hacking（§3.4 图 9）。
    它和 reward 的「可被主动制造」程度强相关：把硬门槛做成程序、可测量属性交给程序、
    judge 只判不可测的部分 —— 这三条做到了，hacking 的面就小得多。
26. **任何「这一轮掉了」的判断，差分必须超过 2σ。** judge 的 σ 可以到 11.4 ELO，
    而模型档位之间只差约 40 ELO（05 §8.4）。没量过 σ 就改 rubric、回滚 ckpt，是在拿噪声当信号。

---

# 1. 算法

## 1.1 单轮 outcome-reward 算法族：稀疏二值 reward 下的实际配置

### 1.1.1 七条路线的对照

| 算法 | arXiv | 核心改动 | 稀疏二值下的招牌数字 |
|---|---|---|---|
| **GRPO** | 2402.03300 / 2501.12948 | 组内均值作 baseline，除以组内 std | DeepSeekMath-Instruct → RL：GSM8K 82.9→88.2、MATH 46.8→51.7。R1-Zero：AIME24 pass@1 **15.6%→77.9%**，cons@16 86.7% |
| **DAPO** | 2503.14476 | clip-higher、dynamic sampling、token-level loss、overlong shaping | Qwen2.5-32B base，AIME24 avg@32 **30→50**，只用 R1-Zero 的 50% 步数 |
| **Dr.GRPO** | 2503.20783 | 删掉 `1/|o_i|` 和 `/std` 两个 bias | 7B 六基准均值 26.5→**51.4**；**27 小时 / 8×A100** |
| **GSPO** | 2507.18071 | importance ratio 放到 **序列级**（长度归一化的几何平均） | MoE 必需：Qwen3-30B-A3B 每做一次更新，约 **10% 激活专家与旧策略不同** |
| **RLOO** | 2402.14740 | leave-one-out baseline，整句当一个 action | TL;DR win-rate RLOO(k=4) **77.9** vs PPO **67.6**；HH-Llama **64.1 vs 32.0** |
| **VAPO** | 2504.05118 | 带 critic：Decoupled-GAE + Length-adaptive GAE + Value-Pretraining | AIME24 avg@32 **60**（DAPO 50、vanilla PPO **5**） |
| **CISPO** | 2506.13585 | clip 的是 IS 权重而不是 token 更新，**所有 token 都保留梯度** | 用 50% 步数追平 DAPO；M1 最终 AIME24 86.0% |
| **Lite PPO** | 2508.08221 | 只留两招：group-mean + **batch-std** 归一化 + token-level loss | 在 4B/8B **base** 模型上打过 DAPO 和 GRPO |

### 1.1.2 超参：有原文数值的全在这里

| 项 | GRPO（DeepSeekMath） | R1-Zero | DAPO | VAPO | GSPO |
|---|---|---|---|---|---|
| 组大小 G | **64** | **16** | **16** | 1（每 prompt 采 1 次，batch 8192） | 未给 |
| clip | ε 未给数值（沿用 0.2） | **ε = 10**（刻意，原文称 "large PPO clipping strategy"） | **ε_low 0.2 / ε_high 0.28** | 0.2，另加 clip-higher | **3e-4 / 4e-4** |
| KL | β = **0.04**，加在 loss 里（k3 无偏估计） | β = **0.001**，每 **400 步**把 ref 刷成最新 policy | **去掉** | — | — |
| batch | 1024 | 32 prompt × 16 = **512**；一次 rollout 出 8192 条，切 16 个 mini-batch | prompt batch **512** × G=16，mini-batch 512 → **每次 rollout 做 16 次梯度更新** | prompt **8192**，mini-batch 512 | 每批 rollout 切 4 个 mini-batch |
| lr | 1e-6 | 3e-6 | 1e-6 常数 + 20 步 warmup | actor 1e-6 / critic 2e-6 | — |
| 步数 | 未给 | **10,400 步 ≈ 1.6 epoch**（8.2k 步时上下文 32k→64k，性能与长度同时跳变） | 到 50 分用了 R1-Zero 一半步数 | **5,000 步**到 60.4 | — |

**三条容易传错的事实（本次核实后更正）**

1. **GSPO 的 clip 范围比 GRPO 小约 3 个数量级，不是 2 个**：3e-4/4e-4 对 0.2/0.27，约 667 倍。
   原文里的「两个数量级」说的是**被 clip 掉的 token 比例**（2507.18071 §5.2 图 2），不是 clip 阈值。
2. **R1-Zero 的 clip ε 是 10**，等于基本不 clip 正向更新。这和 DAPO 的 clip-higher 是同一个病的两种药。
3. **DAPO 的 dynamic sampling 把 rollout 放大了多少倍，原文没给数字**，只有「采样实例数增加，但收敛时间反而缩短」的定性说法（图 6）。别引倍数。

### 1.1.3 DAPO 四件套的逐项增量（表 1，Qwen2.5-32B base，AIME24 avg@32）

| 配置 | 分数 | 增量 |
|---|---|---|
| Naive GRPO | 30 | — |
| + Overlong Filtering（直接 mask 截断样本的 loss） | 36 | **+6** |
| + Clip-Higher | 38 | +2 |
| + Soft Overlong Punishment | 41 | +3 |
| + Token-level Loss | 42 | +1 |
| + **Dynamic Sampling**（过滤 acc 严格等于 0 或 1 的组） | **50** | **+8** |

**读法**：对稀疏二值 reward，收益最大的两项是 **overlong filtering（+6）** 和 **dynamic sampling（+8）**，
两项加起来占了 20 分增量里的 14 分。clip-higher 和 token-level loss 各只值 1~2 分。
这和直觉相反 —— 真正值钱的是**样本选择**（别拿零梯度的组和被截断的样本浪费算力），不是 loss 形式的微调。

Soft Overlong Punishment 的原文数值：L_max = 20,480、L_cache = 4,096，
所以 ≤ 16,384 不罚；16,384 < |y| ≤ 20,480 时按 **斜率 −1/4096 每 token** 线性从 0 降到 −1；
|y| > 20,480 直接 −1。

### 1.1.4 Dr.GRPO 指出的两个 bias（对视觉任务尤其重要）

| bias | 来源 | 后果 |
|---|---|---|
| **response-level length bias** | 除以 `|o_i|` | A>0 时短回答梯度大 → 正确答案偏短；A<0 时长回答被罚得轻 → **错误答案越养越长** |
| **question-level difficulty bias** | 除以 `std({R})` | std 小的题（几乎全对或全错）权重更高 → 难度偏置 |

两个值得记的推论：
- Dr.GRPO 证明去掉这两项后与 **RLOO 等价**（差一个可吸进学习率的常数），并还原了 PPO 的原始目标（App. A）。
- **「回答长度自发增长 = 推理能力涌现」这个叙事被 length bias 污染了**：
  Dr.GRPO 的错误回答长度显著短于 GRPO（图 5）。
- 原文表 2 顺手指出：**OpenRLHF / trl / verl 等开源 PPO 实现都带 length bias**，比 GRPO 发表还早。
  → 本项目若用 verl 系，先确认 `masked_mean` 的归约口径。

### 1.1.5 组大小 G 到底要多大（两篇口径不同，必须分清）

| 口径 | 出处 | 结论 |
|---|---|---|
| **固定总 batch**（G 变大则 prompt 数变少） | ScaleRL 2510.13786 表 1：G = 8/16/24/32 的渐近性能 A = **0.585 / 0.610 / 0.590 / 0.595** | **G 是二阶选择，基本没区别**。原文：「this allocation is a second-order choice」 |
| **固定 prompt 数**（G 变大则总 batch 变大） | Reinforce-Ada 2510.04996：GRPO n=4/8/16 加权平均 **45.3 / 46.1 / 47.3** | **单调上升**，但成本线性涨 |
| **真正能抬上限的轴** | ScaleRL 表 1：batch 512/768/**2048** 的 A = 0.605 / 0.610 / **0.645** | **batch size，不是 G** |

对本项目的含义：**先把 batch 做大（prompt 多样性），G 取 8~16 就够**。
UI2Code^N 的实际选择是 batch 64 × G=16（2511.08195 App. B.3），在这个结论的合理区间内。

### 1.1.6 零梯度组有多严重（这是稀疏二值 reward 的核心病）

| 出处 | 数字 |
|---|---|
| Reinforce-Ada 2510.04996 §2 | 组大小 8、题目通过率 p=0.1 时，**全 0 的概率 0.9^8 ≈ 19%**。Open-R1 子集上 Qwen2.5-Math-1.5B：**n=4 时 35.3% 的组全对，n=256 时降到 10.2%**；同模型 pass@1 = 26.5% 而 **pass@256 = 81.3%** |
| SRPO 2504.14286 §3.3 图 8 | 训练中**接近 50% 的组产生完全相同的 reward**（advantage 为 0） |
| DAPO 2503.14476 图 3(b) | acc=1 的 prompt 比例随训练**持续上升**（只有图，无数值） |

**最重要的一句**（2510.04996）：
**「signal collapse 是欠采样的统计假象，不是模型上限」** —— pass@1 26.5% 但 pass@256 81.3%。
对 visual coding 这件事更严重：我们的 reward 本身就二值且稀疏（渲染对不对、断言过不过），
一个任务初期 pass 率可能只有 5%~10%，G=8 时**约 43%~66% 的组全 0**。

四种对策，按性价比排：

| 对策 | 做法 | 数字 |
|---|---|---|
| 1. **dynamic sampling**（DAPO） | 继续采，直到 batch 被「acc 既不是 0 也不是 1」的样本填满 | DAPO 表 1 里值 **+8 分**，是四件套里最大的一项 |
| 2. **自适应组大小**（Reinforce-Ada 2510.04996） | 每题边采边停：收到 K_pos = K_neg = 8 个正负例就停；最后按正负各一半下采样成固定组，并乘 `1/p̂_i` 还原目标 | **反传组大小只用 n=4**（成本 = GRPO-n4），加权平均 **47.6 > GRPO-n16 的 47.3**，收敛快 2 倍 |
| 3. **epoch 级重采样**（SRPO 的 History Resampling） | **丢掉全对的，保留全错的**（更新后的 policy 可能做对，天然课程）。比 on-the-fly dynamic sampling 省算力 | 两阶段 + HR 对朴素混训：AIME24 **40.5→44.3**、LiveCodeBench **35.1→38.7**；最终 AIME24 50.0，**步数约为 R1-Zero 的 1/10** |
| 4. **经验回放**（ExGRPO 2510.02245） | buffer 存部分正确的轨迹，按正确率分 Easy[75,100) / Medium(25,75] / Hard(0,25] 三桶；**只训 Medium 桶收益最大**；桶内选**当前策略下熵最低**的那条 | ρ（经验占比）消融：**50% → 48.3**、25% → 46.4、**75% → 44.8（低于 on-policy 基线）**。in-distribution +3.5 点、OOD +7.6 点 |

**ExGRPO 的「雪球效应」值得单独记**：高熵的成功轨迹里有很多是「靠错误推理链蒙对」的，
反复从 buffer 采样会污染训练 —— 所以要用**熵最小化**做轨迹选择，尤其在早期。
对视觉任务这条更要紧：**渲染结果对但代码逻辑错**（巧合正确）是本场景的高频形态，
而我们的 verifier 恰恰只看结果。回放这类样本等于在教巧合。

### 1.1.7 熵：别照搬「熵塌缩」的叙事

熵机制那篇（2505.22617）的核心是一条协方差公式：
相邻两步熵变 ≈ `−Cov_{a~π}(log π(a|s), A(s,a))`，而协方差的分布是极端长尾的：

| 分位（Qwen2.5-7B 第 1 步） | 平均协方差 |
|---|---|
| Top 0.02% | **5.654** |
| Top 2% | 1.385 |
| Top 50% | 0.152 |
| 全体 | **0.003** |

对策只干预 **1e-4 ~ 1e-3 比例的 token** 就能改写整条熵曲线：
Clip-Cov（随机 detach 比例 r = 2e-4 的正协方差 token，协方差界 ω = [1, 5]）、
KL-Cov（对协方差 top-k 加 KL，k = 2e-3（7B）/ 2e-4（32B），β = 1）。
效果：七基准平均 7B **+2.0%**、32B **+6.4%**；32B 的 AIME24/25 各 **+15.0% / +14.6%**。

**但是必须同时记住三条反面证据**：

1. **原文自己的 caveat**：作者「**没有观察到被干预的熵值与模型性能之间的关系**」，最优熵值仍是 open question。
2. **ScaleRL 2510.13786 图 16**：batch 768 和 2048 两条 run 的**熵轨迹几乎完全重合**，但 2048 的下游显著更强。
   → **熵不是可靠的性能代理。**
3. **UI-TARS-2 2509.02544 §4 图 8**：GUI 和网页小游戏的 RL **熵经常是上升的**，与推理类 RL 的单调下降相反。
   → 我们的场景（多轮、工具调用、视觉反馈）更接近 GUI，**不要预设熵会下降，更不要把熵下降当告警**。

**entropy bonus 是坑**：
- 2505.22617 §4.1：加 ref KL 能稳住熵但**性能退化**；传统熵正则要么超参极敏感，要么直接损害性能。
- Magistral 2506.10910 §7.4.2 独立佐证：**同一个 entropy bonus 系数，在 math-only 上让熵掉、在 math+code 上让熵炸**。
  他们最后的做法是**只动 ε_high，动态调在 0.26~0.28 之间**，目标是保持组内熵稳定。

### 1.1.8 长度控制

| 机制 | 出处与数值 | 评价 |
|---|---|---|
| **Overlong Filtering** | DAPO：直接 mask 截断样本的 loss，单项 **30→36**。Lite PPO 2508.08221 §4.4：阈值 **8k 有效、20k 无效**（8k 下过滤的是「长但不退化」的推理；20k 下过滤的是重复不终止的退化样本） | **第一选择**。便宜、无副作用 |
| **Soft Overlong Punishment** | DAPO 式 13（见 1.1.3）；表 1 里 **38→41**；Magistral 沿用 | 次选 |
| **组内相对长度奖励** | Kimi k1.5 2501.12599 §2.3.3：`λ = 0.5 − (len_i − min_len)/(max_len − min_len)`；**答对取 λ，答错取 min(0, λ)**。先不加惩罚训一段，再切成恒定惩罚（warm-up） | 用于压 overthinking。注意它是**组内相对**的，不需要定绝对阈值 |
| **强制打断**（替代长度惩罚） | ScaleRL 2510.13786：不罚长，超长时强行追加结束短语（原文：「Okay, time is up. Let me stop thinking and formulate a final answer now. `</think>`」） | 对 agent 轨迹更合适：能保住一个可评的终局产物 |
| **精确长度控制** | L1/LCPO 2503.04697：`r = 1{正确} − α·|n_gold − n_y|`，**α = 3e-4**；LCPO-Max 用 `clip(α·(n_gold−n_y)+δ, 0, 1)`，**δ = 0.5**（保证「小幅超标但答对」优于「答错」）。训练时 n_gold ~ U(100, 4000) | 只在需要可控 token 预算时用 |
| **长度奖励会塌缩** | RLRF（04 §5.1）：SVG 越来越短直到生成发散，长度权重要从 0.1 逐步升高。Dr.GRPO：length normalization 本身就是隐式长度奖励 | 任何长度项都要 warm-up |

**对 visual coding 的直接建议**：
用 **overlong filtering（8k 档）+ 强制打断**，不要用绝对长度惩罚。
原因是产物长度与任务复杂度强相关（一个 three.js 场景 300 行 vs 3000 行都正常），
绝对阈值会系统性惩罚复杂任务。要压的是**自检轮数**，不是代码长度。

### 1.1.9 训推不一致：一个容易被归错因的坑

| 问题 | 证据 |
|---|---|
| rollout 引擎（vLLM/SGLang）与训练引擎的数值不一致，让 RL 实际上变成 off-policy | FP16 那篇（2510.26788）：根因是 **BF16 的 10 位 vs FP16 的 7 位 mantissa**；**换成 FP16 几乎消除 mismatch**，在「每题可解但不 trivial」的数据集上训练准确率接近 100%，而算法补丁（TIS/MIS）只能延缓崩溃 |
| 补丁的成本 | TIS/MIS 的实现**需要额外一次 forward，训练成本 +约 25%** |
| 补丁修不了的部分 | **deployment gap**：最终参数是对 trainer 分布最优，不是对 inference engine 最优 |
| 相关实现口径 | 2510.26788 实测配置：GRPO clip_higher **0.28**，**IS 截断阈值 C = 3** |
| GLM-4.5 的工程选择 | **BF16 训练 + FP8 推理**，每次更新前做在线 block-wise FP8 量化（2508.06471 §3.5）—— 等于主动接受更大的 mismatch 去换 rollout 吞吐 |

本项目的含义：**先排除数值不一致，再怀疑算法**。
症状是「训练 reward 稳定上升，但换到评测引擎上分数不涨甚至掉」——
这与 reward hacking 的症状（4.3.1 第 1 条）长得一样，必须先用同一引擎复测一次区分开。

未核实条目（不要当论文引）：TIS 原始出处（Yao et al. 2025）、IcePop、"When Speed Kills Stability" 均为技术博客，无 arXiv 号；
POLARIS 在 ScaleRL 里是**数据集**（Polaris-53K）而非算法论文。

## 1.2 多轮 agent RL 的信用分配

### 1.2.0 先给一个工业参照：长程多轮用的是 PPO + critic，不是 GRPO

这一点和「GRPO 已经统一天下」的印象相反，但两个最接近本场景的工业系统都选了带 critic 的路线。

**UI-TARS-2（2509.02544 §2.5.4）的完整配方**：PPO，加四件套（全部来自 VAPO / VC-PPO）：

| 组件 | 做什么 | 原文理由 |
|---|---|---|
| **Decoupled-GAE** | policy 和 value 用**不同的** λ | 防止长序列上 critic 的 value 估计衰减 |
| **Length-Adaptive GAE** | λ 随序列长度调整 | 不同长度的序列优势估计口径不一致 |
| **Value Pretraining** | 在固定策略下用 λ=1（即 MC 回报）把 value 模型离线训到收敛（看 value loss 和 explained variance），再作为初始化 | 消除 value 初始化偏置 |
| **Clip Higher** | ε_low 和 ε_high 解耦（引 DAPO） | 抬 ε_high 给低概率动作更多上升空间；ε_low 保持小，避免过早消灭 token |

另加 reward shaping：**reward 主要由终局正确性决定**，某些场景加格式奖励和长度惩罚，
用来「抑制过早终止或无限继续」（原文：discourage premature termination or infinite continuation）。

**VAPO 的消融（2504.05118 表 1，Qwen2.5-32B，AIME24 avg@32）—— 这张表说明为什么不能裸用 PPO**：

| 配置 | 分数 | 掉多少 |
|---|---|---|
| **Vanilla PPO** | **5** | value 学崩：长度暴跌，不推理直接答 |
| DeepSeek-R1-Zero-Qwen-32B | 47 | — |
| DAPO | 50 | — |
| **VAPO** | **60**（最佳 60.4，三次重复 60~61） | — |
| w/o **Value-Pretraining** | 11 | **−49** |
| w/o **Decoupled-GAE** | 33 | **−27** |
| w/o Length-adaptive GAE | 45 | −15 |
| w/o Clip-Higher | 46 | −14 |
| w/o Token-level Loss | 53 | −7 |
| w/o Positive Example LM Loss | 54 | −6 |
| w/o Group-Sampling | 55 | −5 |

公式：**λ_policy = 1 − 1/(α·l)，α = 0.05**，l 是该条输出长度；**λ_critic = 1.0**（无偏）。
动机：固定 λ=0.95 时，l > 100 的 TD 系数 `0.95^100 ≈ 0.006` 已等于 0，GAE 完全被有偏的 bootstrap 支配。
效率：**5,000 步**到 60.4；追平 DAPO 只用 DAPO 60% 的步数；多次独立 run **零 crash**，熵既不塌也不炸。

**怎么选（给本项目）**

| 条件 | 选择 | 理由 |
|---|---|---|
| 轨迹 ≤ 20 步、单次 reward | **GRPO 系**（DAPO 四件套） | 不用养 critic，省一半显存和一套超参 |
| 轨迹 20~50 步 | GRPO + 步级优势（见 1.2.1、1.2.2） | 还能靠组内结构算步级信用 |
| 轨迹 > 50 步、上下文接近窗口上限 | **PPO + VAPO 四件套** | 组相对方法在这个长度上的优势估计噪声太大；两个工业系统（UI-TARS-2、Seed 的 VAPO）都这么选 |
| 用 MoE 基座 | **必须上 GSPO**（或 routing replay） | Qwen3-30B-A3B 每次更新后约 10% 激活专家变化，token-level ratio 会剧烈抖动导致不收敛 |

**代价要说清**：PPO + critic 路线的 **Value-Pretraining 不是可选项**（去掉掉 49 分）。
这意味着在跑主训练之前要额外付一轮「固定策略采样 + 训 value 到收敛」的算力。
在渲染型 verifier 场景里，这一轮的 reward 也要算，等于把 2.2.5 的渲染预算再加一遍。
如果 CPU 预算紧（2.2.2 的单轮 Blender 那一格），这是选 GRPO 系的一个实际理由。

### 1.2.1 turn-level vs trajectory-level：四组明确的对照消融

这是本节最有价值的部分 —— 四篇独立工作都做了「同一套 rollout 协议下换信用分配」的消融。

**(a) MT-GRPO / MT-PPO（2505.11821）—— 形式化三种 MDP 并实测**

| MDP | reward 结构 | 等价于 |
|---|---|---|
| M1 terminal | 只有最终 outcome reward | trajectory-level |
| M2 delayed | 中间 + outcome 累加成一个延迟标量 | trajectory-level（与 M3 return-equivalent） |
| M3 per-turn | 每轮显式 reward | turn-level |

关键论断：**M2 与 M3 return-equivalent，但信用分配不等价**（§3.2）。

GRPO 侧（表 2，两轮 search agent，Qwen2.5-7B，验证集 reward）：

| 方法 | Tool Exec (0~0.2) | Search Answer (0~0.5) | XML Format (0~0.2) | Exact Match (0~1) |
|---|---|---|---|---|
| GRPO-OR（M1，纯 outcome） | 0 | 0 | 0.04 | **0** |
| GRPO-MR（M2，merged） | 0.2 | 0.3724 | 0.1994 | 0.3346 |
| **MT-GRPO（M3）** | 最佳 | 最佳 | 最佳 | **+0.1664 over GRPO-MR** |

**注意 GRPO-OR 在这个两轮设定下完全学不动（EM = 0）** —— 这是 trajectory-level 稀疏 reward 在多轮上的极端失败案例。

**最该记住的反例**（表 3，六数据集 EM 平均）：

| 方法 | Avg. EM |
|---|---|
| GRPO-OR（Search-R1） | 0.351 |
| GRPO-MR（Search-R1） | 0.414 |
| PPO-OR（Search-R1） | 0.432 |
| **MT-PPO（本文）** | **0.447** |
| **Turn-Decomposed PPO-OR** | **0.335** |
| **Turn-Decomposed PPO-MR** | **0.280** |
| **Turn-Decomposed MT-PPO** | **0.293** |

**把轨迹「朴素地按 turn 切开当独立样本」比任何 trajectory-level 基线都差 0.10~0.15 EM。**
turn 级切分只有配上正确的跨轮 advantage 聚合才有用。

代价：MT-GRPO 要在每轮的同一状态重采 G 个动作，K 轮共 **G^(K−1)** 条轨迹；
K=2 时退化成 G 条，与 vanilla GRPO 同价。**K 大了不可行**，这是它的硬边界。

**(b) TCPO（2608.01667）—— 「稠密 ≠ 有用」最干净的一张表**

credit 信号阶梯消融（表 3，DeepSeek-R1-Distill-Llama-8B，best-turn Pass@8）：

| 信号 | MATH-500 | LiveCodeBench |
|---|---|---|
| 轨迹级 reward 广播 | 56.6% | 27.9% |
| 原始每轮 verifier 分 | 59.0% | 30.3% |
| Δ reward（相邻轮分差） | 59.8% | 30.4% |
| + Retro（与 best-so-far 比较） | 62.2% | 31.5% |
| + Hindsight 延迟信用 | 63.4% | 31.7% |
| **TCPO（+ 选择性反事实）** | **65.2%** | **32.2%** |

**读法：从轨迹级到逐轮分只值 +2.4，而「换参照系」又值 +6.2。**
原文的结论是：多轮 verifier 分有用，是因为被换算成了**合适参照下的 credit**，不是因为变密了（§4.4）。

反事实预算（表 4）：**随机选轮做反事实等于白花钱**（63.4% → 63.4%，开销 1.03×）；
按 high-surprisal Top-L 选才有 +1.8（65.2%）；全量反事实 66.8%（1.11×）。

另一个副产品：TCPO 让**成功轨迹的平均轮数下降**（Qwen3-4B MATH 1.26→1.19，LCB 1.61→1.27）。
对本项目直接有用：更好的信用分配会自动减少无效自检轮数。

**(c) VETTA（2610.08402）—— 加法聚合的直接反例**

credit 组合消融（表 2，WebShop）：

| ID | actor credit | 成功率 | task score |
|---|---|---|---|
| C1 | A^tok（纯 token 级） | 67.4 | 84.9 |
| C2 | A^turn（纯 turn 级） | 59.8 | 74.5 |
| **C3** | **A^turn + α·A^tok（朴素相加）** | **55.0** | 79.0 |
| **C4** | **A^turn + α·归一化后的 A^tok** | **72.8** | 83.6 |
| C5 | A^tok，但 critic 只监督 token | 44.8 | 56.8 |

**C3 比两个单项（67.4 / 59.8）任何一个单独用都差。只有先归一化（C4）才拿到最好结果。**
这同时是 1.5 节「加法聚合的尺度面」的硬证据。

**(d) FACTOR（2608.07118）与 CrEST（2608.13179）—— 守恒约束**

两篇的共同思路：**token 级的 teacher 只许调幅度，不许改方向和均值**。

- FACTOR：`C_{t,j} = A*_t · ω_{t,j}`，其中 ω 做 **per-action mean-one 归一化**，
  teacher 只能在动作内重分配，不能改动作级均值或符号。
  表 2（3 seed，成功率%）：

  | reduction | 方法 | ALFWorld | WebShop | ScienceWorld |
  |---|---|---|---|---|
  | token-mean | 基线 | 88.5±1.3 | 78.6±1.5 | 42.3±1.4 |
  | action-mean | 基线 | 89.8±1.1 | 80.0±1.5 | 44.7±1.2 |
  | action-mean | **FACTOR** | **92.0±0.5** | **82.4±0.6** | **48.9±0.8** |

  消融（表 4）：去掉时间维信用分配损失最大（ALF −2.1 / WS −1.9 / **SciW −3.5**）；
  去掉 token 内分配只损失 WS −1.6 / SciW −2.1，**ALF 甚至 +0.2**。
  → **时间维（哪一轮）是主因，token 维（哪个词）是次因。** 优先把轮级信用做对。
  batch-global 归一化替代 per-action 归一化：SciW **−1.7**。
- CrEST：`A_t = A_turn · φ_t`，且 `w_t = clip(exp(sign(A_turn)·Δ_t), 1−ε, 1+ε)` ——
  **符号完全由 verifier 决定，teacher 只调幅度**。
  层级消融（表 3，BFCL V3，Qwen3-4B，Avg）：GRPO 43.63 → 只做轮间 47.88 → 只做轮内 48.75 → **两者 52.00（+8.37）**；
  最长轨迹的分片（Long Context）协同最强（47.0 → 60.0）。
  门控消融（表 4）：去 direction gate 52.00 → **46.75**；去 entropy gate → 46.25；两个都去 → 43.50（回到 GRPO）。
  **一条重要的负面结果**：有 privileged ground-truth teacher 的纯 token 级稠密蒸馏（OPSD）
  在 BFCL Avg 只有 **38.75%，低于 GRPO 的 43.63%**，而且 **> 77% 的梯度压在 top-5% token 上**（多是低熵格式词）。
  → **privileged teacher 单独用会低于纯 RL。**

**(e) ARPO（2507.19849）—— 按熵在工具调用后分叉**

| 项 | 内容 |
|---|---|
| 核心观察 | **工具返回后最初 10~50 个 token 熵急升**，且升幅高于初始输入引起的熵（§2.2）。search 工具返回自然语言 → 熵波动大于 Python 返回确定性数字 |
| 机制 | 先做 N 条 trajectory-level 采样，余下 M−N 预算留给 partial sampling；每次工具调用后生成 k 个 token 算 step 级熵，归一化变化量 ΔH_t 过阈值就分支 |
| advantage 归因 | **Hard**：共享前缀取 d 条分支 advantage 的均值；**Soft**：不显式区分，靠 GRPO 的 token 级 importance ratio 天然令共享前缀的比值相同。**默认 soft**（图 5 显示 soft 的 reward 更高更稳） |
| 熵阈值 | 性能随阈值上升，**峰在 0.4**，到 1.0 反降（图 8 左） |
| 超参 | 7B：batch 128、mini-batch 16、global rollout 16、initial sampling 8、熵权重 0.2、阈值 0.5、KL 系数 0、2 epoch、8×H800 |
| 工具调用次数 | **ARPO 用 GRPO 一半的工具调用次数**取得更高准确率（图 7） |
| 效果 | 10 任务平均：Qwen2.5-3B-Instruct GRPO 50.4 → ARPO **52.8**；Llama3.1-8B-Instruct 51.1 → **55.3**。GAIA 与 WebWalkerQA 相对 GRPO **约 +6 个点** |

**对本项目的适配**：ARPO 的观察在渲染场景应该更强 ——
`render_views` 返回的是图像，比 search 返回的自然语言更「外源」，工具返回后的熵升应该更大。
分支点就该设在**每次拿到渲染结果之后**。这正是最该探索的位置。

### 1.2.2 turn 维度的组内标准化怎么做

| 工作 | 标准化形式 | 组怎么构 |
|---|---|---|
| **MT-GRPO**（式 3~5） | `A^I_{i,(k)} = (R^I_{i,(k)} − mean_i) / std_i`，**在同一 timestep k 上跨 G 条轨迹标准化**；再按 α 折扣聚合未来：`A^MT = Σ_{l=k} α^{l−k} A^I_{i,(l)} + α^{K−k} A^O_i` | 每轮在同一状态重采 G 个动作（代价 G^{K−1}） |
| **TCPO**（§3.3） | 在集合 `A_{x,k}`（**同 prompt、同 turn index**）上归一化，再乘早轮先验 `γ^{k−1}`；当集合大小 < 2 时跳过标准化 | **不改 base rollout，纯后处理** |
| **CrEST**（式 3） | `A_k = (R_k − mean_j R_k^{(j)}) / (std_j + ε)`，**每轮独立**，不传播未来 outcome | 同一 GRPO 组 G 条 rollout 的第 k 轮 |
| **GiGPO**（05 §5.1 已覆盖） | 按**环境状态哈希**归组，不按 turn index | 不需要额外 rollout |
| **ARPO** | 不显式按 turn 标准化，靠共享前缀 token 的 importance ratio 相等隐式实现 | 熵触发的分支树 |

**选择建议（给本项目）**：
- **TCPO 的口径最容易上**：纯后处理，不改 rollout，不加成本。而且我们每一步本来就有 verifier 分（L0/L1 的断言通过数）。
- **GiGPO 的锚状态口径更适合有确定性环境状态的场景**（05 §5.1 已给适配方案）。
- **MT-GRPO 的 G^{K−1} 在 K > 3 时不可行**，不要考虑。

### 1.2.3 γ、轨迹长度与长程实证

| 工作 | γ 设置 | 长轨迹数字 |
|---|---|---|
| RAGEN / StarPO（2504.20073） | GAE **γ=1.0, λ=1.0**（完全不折扣） | 最长 5 turn × 10 action；**每轮动作预算 5~6 个最好，7 个开始退化**（表 2） |
| FACTOR（2608.07118） | **γ=1** | ScienceWorld 是最长 horizon，收益也最大（+4.2 pp） |
| TRIAGE（2606.32017） | value head **γ=0.95**（ALFWorld/WebShop）、**γ=0.9**（Search-QA，轨迹更短） | ALFWorld 完成轨迹平均段数 43.9（基座）→ 24.45（GRPO）→ **21.90**；WebShop 14.80 → 8.00 → **6.82** |
| GiGPO 官方配置 | γ=0.95、相似度阈值 0.9、ω=1.0 | — |
| TCPO（2608.01667） | 早轮先验 `γ^{k−1}`（**γ 数值未披露**） | AppWorld 的相对性能从 1 turn 的约 84% 升到 20 turn 的 100%；MATH-500 **3 轮饱和**、LCB **5 轮到平台** |
| TRACE（2607.13988） | 用 TD look-ahead 视界 K 替代折扣 | **K=0（关掉稠密 TD backup）只有 30.0**；中等传播 34.7 / 35.6；**传得最远反降到 28.9**（§4.4） |

**三条可直接用的结论**

1. **γ=1（不折扣）在 agent 场景是主流**（RAGEN、FACTOR）。
   只有在轨迹很短或要抑制长轨迹时才用 0.9~0.95（TRIAGE）。
2. **稠密轮级 reward 只能当辅助项，系数不能大**。TRACE §4.4 扫 turn-level reward 系数：
   1 → 3 时从 33.6 涨到 **35.6**，再大掉到 34.5、31.1。
3. **训练时限制轮数会让 RL 完全学不动**（2510.24126 §4.3）：
   把 turn 限成 2，正确引文率一直在 **10~15% 徘徊**；不限轮数的同模型 300 步从约 40% 升到 **85%**。
   原因是 GRPO 需要组内有正例 —— 轮数砍了，正例就没了。
   **反过来**，AgentGym-RL 的 ScalingInter-RL（2509.08755）是**早期限轮、后期放大 horizon**，
   用来避免长 horizon 下的崩塌。两者不矛盾：限轮只能是课程的早期阶段，不能是全程配置。

TRACE 的主结果顺带一提（纯 RL，无冷启动 SFT、无 agentic mid-training）：
BrowseComp-Plus 上 Qwen3-4B **7.2 → 35.6**、Qwen3-30B-A3B **8.4 → 42.6**。

---

## 1.3 部分分（partial credit）与稠密化

### 1.3.1 rubric 分项加权作 reward

| 工作 | 分项数与权重 | 关键数字 |
|---|---|---|
| **RaR**（2507.17746） | 每条样本平均 **7.7 项**（20,166 样本共 154,808 项）。**显式聚合** `r = Σ w_j c_j / Σ w_j`（归一化使跨 prompt 可比）；**隐式聚合**把 criteria 连同类别权重丢给 judge 出 1~10 标量。人工权重：Essential 1.0 / Important 0.7 / Optional 0.3 / Pitfall 0.9 | 最好的 RaR 变体相对 Direct-Likert 在 HealthBench 相对提升最多 **31%**、GPQA-Diamond **7%** |
| **RULER**（2609.25270，04 已覆盖部分） | 前沿模型**只凭指令**生成 **6 项、归为 3 轴**（Semantic Fidelity / Visual Quality / Rendering Style）；item 写在「设计意图」层而非像素/path 约束 | 与人类 Spearman 0.79（04 §1.2）；rubric 生成器可换（Claude-Opus-4.6 ↔ GPT-5.5 结论稳定） |
| **Verification Horizon**（2606.26300，05 §8.5 已覆盖） | 671 个 WebDev 任务，平均 **25.9 项 / 6 维**，**item 占比本身就是隐式权重**：Functional 37.7% / Content 19.0% / Visual 13.3% / Layout 12.9% / UX 9.3% / Technical 7.2% | judge 一致性 Spearman 0.810~0.905、Kendall 0.714~0.786；同族内 τ=1.0、跨族 τ ≥ 0.93 |

**两条反直觉的消融（都来自 RaR §6）**

1. **权重几乎不重要**：rubric 设计消融里 **去掉类别权重（No Categorical Labels）38.8%，高于带全部权重的 37.2%**；
   Essential-Only 34.9%、No Pitfall 37.2%。原文明说「including rubric weights or pitfall criteria 带来的差异极小」。
2. **rubric 来源远比权重重要**：生成器消融 —— O3-mini（**带参考答案**）35.9 > GPT-4o 34.2 >
   GPT-4o-mini 32.7 = Qwen-72B 32.7 > Qwen-7B 31.9 > Qwen-32B 31.1；
   通用静态 rubric（Predefined）明显落后。
   RULER 的同向证据：Universal rubric 的 rubric 分 0.591，instance-aware 的 **0.683**。

→ **操作结论：别花时间调权重，花时间让 rubric 变成 instance-aware 且由见过参考答案的强模型生成。**
04 §6.2 的校准清单里应该加一条：rubric 生成器要能看到参考产物。

### 1.3.2 0/1 还是连续部分分：**没有普适答案，与起点耦合**

| 工作 | 选择 | 数字 |
|---|---|---|
| **SWE-RL**（2502.18449 式 1） | **纯连续**：`difflib.SequenceMatcher` 相似度 ∈ [0,1]，格式错 −1 | Llama3-SWE-RL-70B 在 SWE-bench Verified **41.0%**；且在五个域外任务上也提升，而 SFT 基线平均反降。**本文没做 0/1 vs 连续的消融** |
| **SWE-Master**（2602.03411 §3.4.2） | **二值**（过全部 F2P+P2P 才 1）**+ 乘法式部分分处理截断**：DONE → r；TIMEOUT/MAX_STEPS/MAX_TOKENS → **α·r（α=0.5）**；CONTAINER_FAILED → 0 且 mask | 动因是硬数据：RL 初期约 **20% 轨迹被截断**，而离线复核发现这些轨迹中 **24.3% 其实已经解决了问题**（图 5）。不给部分分会把真进展全判零并导致训练塌缩 |
| **Magistral**（2506.10910） | 做过对照 | 代码任务用「**通过测试比例**」的连续 reward **训得更快、丢弃的数据少 3 倍**，但**最终分数略低于二值 reward** |
| **DeepSWE vs SWE-Master 的相反结论** | — | DeepSWE 主张「截断轨迹 reward 置 0 + mask loss」更稳；SWE-Master 复现后**持续退化直至塌缩**（§6.3 图 12）。作者归因于初始化与数据复杂度差异 |
| **EvilGenie**（2511.21654） | 测例部分分挡不住 hacking | 留出 30% 测例（上限 10 条）作 holdout，把「过可见测例但挂至少一条 holdout」判为 hacking。结论：**holdout 测例相对 LLM judge 只有极小增益**，作者在 Inspect scaffold 下干脆弃用 holdout |
| **R2E-Gym**（2504.07164，05 §2.3 已覆盖） | 两类 verifier 互补缺陷 | 执行型「distinguishability 低」（过/不过区分度差，即部分分难做）；免执行型有偏且依赖风格特征 |

**给本项目的判断**

| 阶段 | 选择 | 理由 |
|---|---|---|
| L0 硬门槛（能不能跑） | **二值，且格式错给 −1** | 可执行与不可执行必须严格可分（CAD-Coder 的塌缩，2.3.5） |
| L1 程序化断言 | **连续（通过的断言占比）**，但要分 core 与 detail 两级 | Magistral：连续训得快、丢的数据少；core 断言失败时设上限（04 §6.1） |
| 预算耗尽的轨迹 | **强制提交 + reward 乘 0.5** | SWE-Master：24.3% 的截断轨迹其实已经做对 |
| L3 rubric | **连续（归一化加权平均）**，不要 holistic 标量 | RULER |
| 最终收车指标 | **二值** | Magistral：二值的最终分更高 |

### 1.3.3 稠密化的失败证据（必须看完再决定要不要做 PRM）

| 证据 | 数字 |
|---|---|
| **Spurious Rewards**（2506.10947） | Qwen2.5-Math-7B 上：**随机 reward +21.4、格式 reward +13.8、错误标签 +24.1、1-shot RL +26.0、majority voting +27.1**，而 ground-truth reward 才 **+29.1**。→ **大半「稠密化收益」可以由与正确性无关的信号复现。任何 proxy 涨幅在没有 null baseline 的情况下都不能当作信号质量的证据。** |
| **RM 过优化定律**（2210.10760） | gold reward 随 proxy 优化**先升后降**，且该关系对 RL 与 best-of-n 有**不同的函数形式**，系数随 RM 参数量平滑变化；RL 在同等 KL 下既优化更慢也过优化更慢 → **KL 不是跨方法比较「优化量」的可靠尺度** |
| **多模态 reward hacking**（2607.09492） | outcome-only reward 下 hacking 率最高 **48.1%**；32B 在 outcome-only 下仍有 **54.9% worse rate**；算法鲁棒性与规模耦合：GRPO 48~53%、RLOO 67~68%、DAPO 从 2B 的 67.2% 降到 8B 的 45.5%。**最关键一句：关键词式的「视觉证据 reward」比 answer-aware reward 更容易被 hack，只有 VLM-as-judge 的语义验证才降低 hacking** |
| **CrEST**（2608.13179） | privileged ground-truth teacher 的纯 token 级稠密蒸馏 **38.75% < GRPO 43.63%** |
| **AgentPRM**（05 §5.2 已覆盖） | PRM 用 10k rollouts 训时，400 步后成功率 82% → 70%，而**验证集上的 process reward 还在涨** |

**所以：稠密化只有在 verifier 本身可靠时才成立。**
本项目的次序必须是「先把程序化断言做硬，再考虑 PRM」，不是反过来。

---

## 1.4 课程与难度筛选

### 1.4.1 按 pass@k 分桶：唯一一篇做全的工作

**Boundary-Aware Curriculum RL（2606.22317）**

| 项 | 内容 |
|---|---|
| 难度估计 | **256 样本解码预算 × 3 个种子**，记录首次答对的样本序号并跨种子取均值；256 内未答对记为 unsolved |
| 分桶 | Easy / Medium / Hard / **Frontier**（pass@32 附近）/ **Beyond**（256 内未解，必然形成零优势组） |
| **Beyond 桶不丢** | 取 10 个最接近 pass@32 分界的 Frontier 与 10 个最接近 pass@256 分界的 Beyond，构造 teacher trace 做**小规模 SFT 桥接**，再 RL 巩固 |
| 课程区间 | 5 选 1，原则是「用最硬的、但仍含足够可达样本的区间」 |
| **重估频率** | **每个课程轮重做一次完整 pass@k 探索**，共 3 轮 |
| 结果 | 平均 pass@256 相对 base **+9.8 pp**、相对 vanilla RLVR **+10.3 pp**；**vanilla RLVR 的 pass@256 平均低于 base model** |

典型数字（pass@256，Base → Vanilla RLVR → Curriculum RL）：
Qwen2.5-7B AIME24 40.0 → **26.7** → 52.2；LLaMA-3.1-8B-Instruct MATH500 73.6 → **55.4** → 88.0。
问题级迁移：5 个设定合计 base unsolved 538 → curriculum unsolved 350，
即 **538 道 base 解不出的题里 226 道变可解**。

桶分布随轮次的漂移（Qwen2.5-7B，表 9）：

| 轮次 | Easy | Medium | Hard | Frontier | Beyond | 平均 k |
|---|---|---|---|---|---|---|
| Base | 24 | 1343 | 354 | 166 | 61 | 12.43 |
| RL1 | 650 | 1108 | 72 | 69 | 49 | 5.64 |
| RL2 | 697 | 1057 | 66 | 82 | 46 | 6.10 |
| RL3 | 736 | 1027 | 59 | 75 | 51 | 5.91 |

**读法：第一轮后 Easy 桶从 24 暴涨到 650 —— 这就是「静态课程会迅速失效」的量化证据。**
但注意 RL1 之后基本不动了（650→697→736），说明**重估的边际价值主要在第一次**。

### 1.4.2 丢弃策略：DAPO 的被动过滤是有代价的

**Reinforce-Ada（2510.04996 表 5，按 base pass@16 分四档）**：

| 方法 | Extremely Hard | Hard | Medium | **Easy** | Overall |
|---|---|---|---|---|---|
| Base | 0.0000 | 0.0889 | 0.2950 | 0.6151 | 0.1139 |
| GRPO | 0.3414 | 0.4639 | 0.6497 | 0.6865（+7.14） | 0.4749 |
| **DAPO** | 0.3487 | 0.4648 | 0.6521 | **0.5580（−5.70）** | 0.4757 |
| Reinforce-Ada | **0.3674** | **0.4825** | **0.6579** | **0.7153（+10.02）** | **0.4933** |

**DAPO 的动态采样在 Easy 桶上比 base 还低 5.70 个点** ——
过滤掉全对组相当于把易题从课程里剔了，代价是易题能力退化。
样本分布（5000 题）：extremely hard 984（19.7%）、hard 3,082（61.7%）、medium 870（17.4%）、easy 63（1.3%）。

另一条反例（§3.2）：**先用小预算 explore 估 p̂ 再按 1/√p̂ 分配预算的两阶段方案会崩** ——
难题在小预算下 p̂=0，退化成和被动过滤一样丢掉最该救的 prompt。

墙钟代价（表 3）：1.5B 上 Seq-pos **2.2×**、Seq-balance **2.8×** step time；
7B 上开销小得多（actor update 占 236 s 中的 85 s，而 1.5B 只占 102 s 中的 15 s）。
→ **模型越大，自适应采样越划算。**

**ExGRPO（2510.02245）的退役策略**：所有 rollout 全对的题从 buffer 移除。
重新引入退役题：in-dist 平均 48.4 → **45.3** —— **复习已掌握的题是负收益**。
桶采样概率 `p ∝ N(Acc(q); μ=0.5, σ=1)`；敏感性：on-policy 45.3；μ=0.5/σ=1 → **48.4**；
σ=1.5（趋近均匀）→ 46.2；μ=0.25（偏难）→ 更差。

**两条看似矛盾、实际边界清楚的结论**：
- **全对的题要退役**（ExGRPO：重新引入 −3.1）；
- **但不能把易题整类剔掉**（Reinforce-Ada：DAPO 的 Easy 桶 −5.70）。
  区别在于「这一道题已经稳过」和「这一类题偏易」。前者退役，后者保留并降权。

### 1.4.3 工业披露

| 模型 | 难度筛选做法 |
|---|---|
| **GLM-4.5**（2508.06471 §3.3.1） | 两阶段课程，第二阶段切到 **pass@8 = 0 但 pass@512 > 0** 的极难题，且**必须来自已验证正确答案池**；对照组继续用中等难度则平台化（图 5） |
| **GLM-5**（2602.15763） | 数学与科学做 **difficulty filtering**：只留「GLM-4.7 极少答对或一贯答错，但更强 teacher（GPT-5.2 xhigh、Gemini 3 Pro Preview）仍可解」的题；SFT 阶段同样只保留对 GLM-4.7 有挑战性的题。异步 off-policy 下按 rollout 用的权重版本做 **staleness 过滤**，太旧的样本直接丢 |
| **MiniMax-M1**（2506.13585） | 数学：强推理模型算每题 **pass@10，只留 0 < 通过率 < 0.9**，得约 **50K** 题。逻辑：上界 = 强模型 pass@10 > 0，下界 = MiniMax-Text-01 通过率 0~0.5 的最低难度参数，约 **53K**。代码同法约 **30K**。课程：先只用 rule-based reward 的推理任务，再逐步混入通用域 |
| **Kimi k1.5**（2501.12599 §2.3） | **model-based 难度标注**：SFT 模型对每题高温采样 **10 次**，通过率作难度代理，先预过滤 trivial 题。**Curriculum Sampling** 易→难；**Prioritized Sampling** 按历史成功率反比采样 |
| **Kimi K2**（2507.20534） | 「Moderate Difficulty」原则：用 SFT 模型 pass@k 评难度，**只选中等难度**，太易太难都少信号 |
| **Ling / Ring 2.6**（2606.15079） | **Dynamic Pass Rating（DPR）**：不用静态历史通过率，而按训练行为动态判难 —— 早期就解出的、或通过率持续高的算易；一直没解出或不稳定的算难，优先训练。形成「始终聚焦当前能力前沿」的自适应课程。另有「按难度区分的长度限制」 |
| **Qwen3**（2505.09388） | **没有 pass@k 课程段落**。只有 query filtering（用 Qwen2.5-72B-Instruct 剔掉不易验证的 query）+ response filtering，最终只有 **3,995 条 query-verifier 对** 用 GRPO |
| **SWE-Master**（2602.03411 §4.2） | 每 issue 跑 N ∈ [3,12] 次 rollout 取平均 resolve rate 作难度代理；**分布呈双峰**（恒解出 / 恒失败），**两端都剔除**，只留混有成功与失败的 issue。不做难度过滤 54.2% → 做 **57.8%** |

**最该抄的两条**
1. **MiniMax-M1 的双边阈值**（`0 < 通过率 < 0.9`，用 pass@10 估）—— 口径最简单、最容易复现。
   本项目的 S2 拒绝采样阶段天然会算出 pass@N，直接用。
2. **Ling 2.6 的 DPR** —— 不用静态估计，按训练中的行为动态判难。
   在渲染场景更重要：**我们的难度估计很贵**（每次 pass@k 估计都要跑渲染），
   静态估一次 256 样本 × 3 种子 的代价在 Blender 上会非常高（按 2.2.1：256×3×24.7 core-s = 5.3 核时 / 题）。
   → **本项目应该用在线正确率（ExGRPO 口径）或 DPR，不要用离线 pass@256。**

---

## 1.5 奖励聚合：硬门槛 × 连续分（乘法）vs 加法

### 1.5.1 最干净的一组对照：L1 的三个变体

**L1 / LCPO（2503.04697 附录 A.7）**，三个变体同从同一 checkpoint 训 120 步：

| 变体 | reward 形式 | 结果 |
|---|---|---|
| **L1-Max（乘法）** | 正确性 × 长度项 | 性能与长度遵从兼顾，**最终采用** |
| **L1-Max Addition（加法）** | `I(y=y_gold) − α·\|n_gold − n_y\|` | **budget 违约率恒为 0%，但模型塌缩到极短 CoT**，性能显著低于其余三个变体（图 15/17）；作者为清晰起见把它从图 16 剔除 |
| L1-Max Sigmoid（乘法 + 软门） | `I(y=y_gold) · σ(α(n_gold − n_y))` | 与乘法变体无统计显著差异 |
| L1-Max 单目标 | 只保留长度目标 | 与乘法变体无统计显著差异 |

**一句话机制**：加法把「硬约束」变成了**可以用牺牲主目标来换的可交易项**，
于是模型选择把主目标扔掉 —— 0% 违约是通过永远输出极短链达成的。

### 1.5.2 其他四组乘法 vs 加法的证据

| 工作 | 证据 |
|---|---|
| **VETTA**（2610.08402 表 2） | `A^turn + α·A^tok` 未归一化 = **55.0**，低于纯 token（67.4）和纯 turn（59.8）**任何一个单项**；归一化后的加法才 72.8 |
| **FACTOR**（2608.07118 表 4） | 严格乘法 `C = A*_t · ω_{t,j}`，ω 非负且 mean-one，teacher 不能改符号也不能改动作级均值。放松成 batch-global 归一化：ScienceWorld **−1.7 pp** |
| **CrEST**（2608.13179 表 4） | `A_t = A_turn · φ_t`，**符号完全由 verifier 决定**。去掉 direction gate（允许 teacher 改方向）：52.00 → **46.75** |
| **OTC-PO**（2504.14870） | `r = r_correct × 工具效率项`。原文 §3.3 注解：「乘法结构确保工具效率**只在主目标满足时**才被奖励；答案错时 `r_correct=0`，工具项被完全禁用。这个设计通过阻止 policy 在最终答不对时还被鼓励用工具来缓解 reward hacking」。效果：**工具调用数最多降 68.3%、tool productivity 最多提升 215.4%、准确率基本持平** |
| **Adaptive-Group**（2610.17710，05 §5.3 已覆盖） | 改成和之后召回涨到 97.2 但特异度掉到 53.5 |

**五组独立证据指向同一结论：门控必须是乘法。**

### 1.5.3 加法聚合的 hacking 面：最硬的一组数字

**RULER（2609.25270 表 4，固定 Qwen3-8B + GRPO，只换 reward）**：

| reward | Illustration: CLIP / Aesth. / HPS / Rubric / Tokens | Icon: CLIP / Aesth. / HPS / Rubric / Tokens |
|---|---|---|
| Zero-Shot | 0.244 / 4.309 / 0.233 / 0.432 / 0.4k | 0.266 / 4.424 / 0.234 / 0.395 / 0.3k |
| **CLIP+Aesthetic+HPS 加权和** | **0.196** / **6.697** / 0.235 / 0.464 / 0.7k | **0.232** / **6.210** / 0.239 / **0.262** / **6.3k** |
| Universal Rubric | 0.244 / 4.813 / 0.241 / 0.660 / 0.7k | 0.266 / 4.793 / 0.244 / 0.591 / 0.3k |
| **RULER（instance-aware rubric）** | 0.249 / 4.859 / 0.246 / **0.693** / 2.0k | 0.269 / 4.873 / 0.247 / **0.683** / 0.7k |

**读法**：加权和把 **Aesthetic 从 4.31 顶到 6.70（+55%）**，同时
**CLIP 从 0.244 掉到 0.196（−20%）**，Icon 的 rubric 分从 0.395 **崩到 0.262**，
token 数从 0.3k **爆到 6.3k**。
典型的「一个易刷分项吸走全部优化压力，并补偿掉另外两项的失败」。

其他实例：
- **静态 judge 被长度利用**（2606.26300 §3.2 图 6）：只看源码 + 固定截图的 judge 下，
  模型学会写**越来越冗长的 CSS/JS** 来抬分；**交互式 judge（Playwright 真跑）免疫**，
  因为 reward 来自 runtime 行为，而且 RL 中测试分更高、输出长度稳定。
- **TEDS / DINO 作 reward**（Visual-ERM 2603.13224，04 §5.1 已覆盖）：
  训练 reward 稳步上升，目标指标只微涨、其他指标略降；
  DINO-based RL 在 Table-to-Markdown 上不仅无收益还**全面退化**。
- **关键词式视觉证据 reward**（2607.09492）：作为附加项，**比不加更容易被 hack**。

### 1.5.4 门控式 reward 的工业实现

| 工作 | gate 判据 | gate 失败时 | 数字 |
|---|---|---|---|
| **ARPO**（2507.19849 式 8） | 层级门控：格式闸 → Acc 闸 → 才给工具协同分。`R = max(Acc + r_M, Acc)` 当格式好且 Acc>0；`0` 当格式好但 Acc=0；`−1` 其他；r_M = 0.1 | 0 或 −1 | 见 1.2.1(e) |
| **ARA**（2602.01750） | 对抗训练出的 Auditor 给出「response 是真实对齐」的置信度 | `r_gated = r_proxy · (auditor confidence)^k`，被判 exploit 时**无论 proxy 多高都压向 0**；Auditor 在第二阶段冻结 | Auditor 检测（表 2，500 真 / 500 高 proxy exploit，proxy 可比）：**proxy reward 0.91 vs 0.89（Δ0.02，无区分力）**；GPT-4 0.78 vs 0.34（Δ0.44）；**Auditor 0.82 vs 0.19（Δ0.63）**。标准 PPO 的 Goodhart 分叉点：code gaming 约 1,000 步、length bias 约 3,500 步、sycophancy 约 4,000 步；code gaming 的 hacking 率在 4,000 步饱和于约 **59%**。Auditor 容量需求随 exploit 复杂度上升：length bias 25M 饱和、sycophancy 35M、**code gaming 50M** |
| **Verification Horizon**（2606.26300） | 轨迹级行为监控匹配高风险 pattern（搜原 PR、开上游 diff、查 commit hash），pattern 集每个训练区间由 agentic reviewer 迭代扩充 | **token 级惩罚**（非硬零） | 见 1.5.5 |
| **RULER** | 能否被 CairoSVG 渲染 | 人评中渲染失败**直接判负**；自动指标只在成功渲染样本上聚合，另报 render success rate | RULER render success Icon 99.3% / Illustration 100%（表 8） |
| **Visual-ERM**（2603.13224） | render-success reward（RSR），**归一化后加法** | 加法 | 平均 76.8（base）→ 79.0（不含 RSR）→ **79.5（含 RSR）**，**只值 +0.5**；作者归因训练稳定性而非信号质量 |
| **Code Aesthetics**（2510.23272） | 执行成功 / 静态美学 / 交互可用性三路 | **加法**：w_exec = 0.1、w_static = **0.8**、w_interact = 0.1；交互元素限 3 个（因 GUI agent 成功率低） | Qwen3-4B 带 agentic reward vs 不带：30.42 / 26.19 / 25.31 / 1.04 对 29.16 / 25.20 / 24.67 / 0.71 |
| **RLRF**（2505.20793） | **无硬闸，纯加权和** `r = Σ λ_i r_i` | — | 奖励消融（表 5）：单用 L2 的 MSE 最好，L2+Canny 更好；DreamSim 与 DreamSim-Edges 单用都差、配 Canny 才好；**全部 reward 加权和最好**。为防「把 prompt 文字画进 SVG」，**渲染前剥掉所有 `<text>` 元素**并混入 evaluator |

**一个重要的对照**：RLRF（纯加权和）和 RULER（加权和被 hack）在同一个任务族（SVG）上结论相反。
差别在于 **RLRF 的分项之间是互补的几何约束（MSE、Canny 边缘），而 RULER 批评的加权和里混了 Aesthetic 这种
「与任务目标不对齐且极易刷」的项**。
→ **判据不是「加法还是乘法」，而是「有没有一个分项能在不满足主目标的前提下被刷高」。**
有这样的分项时必须门控或直接删掉；全是互补约束时加权和没问题。

### 1.5.5 权重标定：别标，改结构

| 方法 | 出处与做法 |
|---|---|
| **用 item 数量充当权重** | Verification Horizon：6 维共 25.9 项，权重由 checklist 条目分布实现，不显式标数 |
| **让 judge 隐式聚合** | RaR 的 Implicit 变体：把 criteria + 类别标签一起给 judge 出 1~10 标量，「avoiding the need for hand-tuned weights」；主结果上 Implicit 稳定优于 Direct-Likert |
| **用相对排序替代绝对权重** | UI2Code^N 的 RVPO：对多个渲染候选按**相对视觉偏好排序**，不优化绝对分。原文明说这降低了绝对 reward 校准不良的影响、「使单一 shortcut pattern 更难主导优化」 |
| 归一化后再聚合 | Visual-ERM、VETTA C4 |
| 与人类标注做秩相关验证 | Verification Horizon 表 4：Spearman 0.810~0.905、Kendall 0.714~0.786、Battle Agreement 34.2~41.4%（n=15,698 对） |
| 人工类别 → 数值 | RaR：Essential 1.0 / Important 0.7 / Optional 0.3 / Pitfall 0.9 —— **但消融显示去掉权重更好** |

**Bradley-Terry 拟合 rubric 分项权重**：本次核实范围内**没有**找到直接做这件事的论文，标「未核实」。

### 1.5.6 本项目的聚合方案

```
R = Gate_L0 × [ w1·S_L1core + w2·S_L1detail + w3·S_L2 + w4·S_L3 ]   ← 错
R = Gate_L0 × Gate_L1core × [ S_L1detail ⊗ S_L2 ⊗ S_L3 ]            ← 对
```

具体规则：

| 层 | 形式 | 失败时 |
|---|---|---|
| **L0 能跑、canvas 非空、无 JS 错误** | **乘法硬闸（0/1）** | 整个 R = 0；格式错 / 不可执行给 **−1** |
| **L1 core 断言**（对象存在、数量、层级） | **乘法硬闸（0/1）** | 整个 R = 0。不允许 L2/L3 补偿（04 §6.1 已定） |
| **L1 detail 断言**（尺寸比例、相对位置） | 连续：通过占比 | 正常进加权 |
| **L2 几何 / 感知**（按色体素 IoU、CD） | 连续 | 正常进加权，**但权重不超过 0.3** |
| **L3 rubric** | 连续：归一化加权平均，**分项数即权重**，不标数值 | 正常进加权 |
| **L4 组内 pairwise** | 只用于开放设计任务，**不补偿功能失败** | — |
| 预算耗尽 | 整体 **× 0.5**，强制提交 | — |
| 环境故障 | **mask loss / 丢弃整组** | 不进梯度 |

**三条必须守住的纪律**
1. **任何「可以在不满足主目标前提下被刷高」的分项，要么门控，要么删掉**（1.5.4 的判据）。
   本场景里这类分项是：美学分、CLIP/DINO 相似度、token 数相关的任何项。
2. **L2 的权重要压住。** RULER 的 Aesthetic +55% / CLIP −20% 就是权重给大了的后果。
3. **先量「某分项能被刷到多高」再定权重**：对每个分项单独做一次 100 步的小 RL，
   看它能把自己刷到多少、把其他分项压到多少。这比标权重有用得多。

---

# 2. 基础设施

## 2.0 先说清问题

慢 verifier 不是性能优化题，是方向级的阻塞。DeepSeek-R1 自己给了反例：

> 由于评测耗时长、影响 RL 效率，大规模 RL 还没有广泛应用到软件工程任务上……
> 未来版本会通过对 SWE 数据做拒绝采样、或在 RL 过程中引入**异步评测**来改善效率。
> （2501.12948 §4 局限）

两个相关的量级：
- agentic RL 中 **rollout 占总墙钟 70% 以上**（NeMo-DCR 2610.08430）、**90% 以上**（APRIL 2509.18521）。
- 渲染型 verifier 的延迟分布**方差很大**（three.js 0.4 s、Blender Workbench 1.4 s、Cycles 7 s、VLM judge 5~8 s），
  这恰恰是异步收益最大的区间（见 2.1.3）。

---

## 2.1 异步 rollout 与慢 verifier 解耦

### 2.1.1 六个框架的异步披露对照

| 框架 | arXiv | 异步形态 | staleness 旋钮 | 招牌加速 |
|---|---|---|---|---|
| **AReaL** | 2505.24298 | 完全解耦 + **中断式生成**（一条轨迹由多个权重版本的 segment 拼成） | `rollout.max_head_offpolicyness`（文档称典型 2~8；论文最终代码 η=4、数学 η=8） | 吞吐 **2.57×**、端到端 **2.77×**、强扩展最多 2.5× |
| **ROLL / ROLL Flash** | 2506.06122 / 2510.11345 | 队列调度 + **环境级异步** + 冗余环境 | **per-sample 的 α**（SampleBuffer 上界 (1+α)×batch） | RLVR **2.24×**、ALFWorld **2.72×**、SWE **1.81×** |
| **verl** | 2409.19256（论文无异步） | `one_step_off_policy` 与 `fully_async_policy` 两个 experimental recipe | `async_training.staleness_threshold`（0=同步，文档建议 < 1）+ `partial_rollout` | one-step-overlap **+23%~+40%**；全异步 128 卡 **2.35×** |
| **slime** | **无论文**（GitHub + lmsys blog） | 后台 asyncio worker 维持跨 rollout 边界的 in-flight 生成池 | `--partial-rollout` + 过采样；`--mask-offpolicy-in-partial-rollout` | 生产背书：GLM-4.5 ~ 5.3 全系都是 slime 训的 |
| **Ling / Ring 2.6（ASystem）** | 2510.22115 / 2606.15079 | **不走完全解耦**，走 partial-rollout + 全局 token 预算 Φ 门控 | `max_staleness × consumer_batch_size`，超限 segment 直接退役 | 「Ring-2.6 的有效 staleness 只有几个优化步，**相对同步基线未观察到稳定性或最终 reward 的损失**」 |
| **Trinity-RFT** | 2505.17826 | explorer / experience buffer / trainer 三件套，四种模式 | `sync_interval` | 7B 一个 epoch：严格 on-policy **130.33 h** → one-step off **48.98 h（2.66×）** |

其他可引：StreamRL（2504.15930，异步 1.30~2.66×）、LlamaRL（2505.24034，405B 权重同步 **2.31 s**、端到端 10.7×）、
AsyncFlow（2507.01663，Ascend，vs verl 平均 1.59×）、RLinf（2509.15965，1.07~2.43×）、
APRIL（2509.18521，主动中断长尾，+17%~+35%）、INTELLECT-2（2505.07291，两步异步、去中心化）、
SAO（2607.07508，GLM-5.2 生产用的单 rollout 异步）。

### 2.1.2 staleness 容忍度：甜点是 1~2 代，不是 8 代

**AReaL 表 2（1.5B 数学，η 扫描）—— 目前唯一一张完整的 staleness × 算法的二维表**：

| η（最大 staleness） | AIME24 不带 decoupled loss | AIME24 带 decoupled loss |
|---|---|---|
| 0（oracle，同步） | 42.0 | — |
| 1 | 41.8 | 42.1 |
| 2 | 40.0 | 41.8 |
| **4** | **23.3** | **42.2** |
| 8 | 35.7 | 41.0 |
| 16 | 35.8 | 38.7 |
| ∞ | 34.0 | 36.9 |

**两条硬结论**
1. **不配套算法，轻微 staleness 就会腰斩**：η=4 时 AIME24 从 42.0 掉到 23.3。
2. **配上 decoupled PPO，η ≤ 8 几乎无损**；但 η→∞ 即使有校正也追不上 oracle。

**吞吐的边际收益在 η=1 就见底**（AReaL 附录 C.3 表 7，1.5B / 8k / 8 卡，token/s）：

| η | 0 | 1 | 2 | 4 | 8 | 16 |
|---|---|---|---|---|---|---|
| 吞吐 | 27.1k | **47.8k** | 47.8k | 49.0k | 51.5k | 52.0k |

**η 从 0 到 1 吃掉了 76% 的加速（27.1k→47.8k），再往上只多 9%。**
→ **工程含义：把 staleness 设成 1~2，不要贪。** 代价（精度风险）是超线性的，收益是次线性的。

各家的默认值全都落在这个区间，互相独立地印证：

| 来源 | 默认 / 建议 |
|---|---|
| ROLL Flash 2510.11345 Takeaway 3 | **α = 2 对绝大多数配置就足够**（24Train16Infer：α=1 +28%、α=2 **+64%**、再加无收益） |
| NeMo-RL `docs/guides/async-grpo.md` | `max_trajectory_age_steps` **默认 1**，建议从 1 起调 |
| verl `fully_async_policy` | `staleness_threshold` **建议 < 1**（threshold=1 基本等价 one-step-off） |
| Ring 2.6 | 有效 staleness「只有几个优化步」 |
| AsyncFlow | 「经验研究表明 rollout 与 update 之间**一步**异步不会导致显著性能退化」 |

**α 的两个单调性**（ROLL Flash 表 1）：**随序列长度上升**（4K/8K/16K/32K → α=1/1/1/2）、
**随 rollout batch 下降**（32/64/128/256 → α=4/2/2/2）。
我们的场景序列长（49k 终局上下文）、batch 中等（64），落在 α=2。

**一个反直觉的实测**（verl `fully_async_policy` README，128 卡）：
staleness 0 / 0.1 / 0.3 / 0.5 对应 400 步 1d1h53m / 19h59m / 17h20m / 17h22m，
而 AIME 最高分 0.2844 / 0.3542 / 0.3469 / 0.3521 ——
**纯流式同步（threshold=0）反而是精度最差的一档**。README 归因为 response length 漂移引起的训练不稳定，
并写明「需进一步分析」。引用时要带这个保留。

### 2.1.3 慢 verifier 的收益来自方差，不是均值

ROLL Flash 的模拟（2510.11345 §5.2.2）是这个问题最干净的证据。
环境延迟服从正态分布，batch 512，比较同步与环境级异步：

| 环境延迟分布 | 每步时间 | 加速 |
|---|---|---|
| N(μ=10s, **σ=10**) | 892 s → 362 s | **2.46×** |
| N(μ=10s, **σ=1**) | — | **1.16×** |
| N(μ=50s, σ=5) | — | **1.20×** |

**均值大但方差小（μ=50, σ=5）只有 1.20×；均值小但方差大（μ=10, σ=10）有 2.46×。**
真实环境的实测同向：**SWE 10.22h → 8.32h（1.23×）、ALFWorld 13.37h → 8.44h（1.58×）**。

**对本项目的直接判断**：
我们的 verify 延迟是 0.4 s（three.js 断言）到 8 s（Cycles + VLM judge）的混合，
变异系数远大于 1，**落在高收益区（接近 2.46× 那一格）**。
而如果只做 three.js 断言（延迟稳定在 0.4 s 上下），异步的收益会掉到 1.2× 以下 —— 不值得上复杂度。

**判据**：先量 verify 延迟的 σ/μ。σ/μ < 0.3 就别做异步，直接同步 + 多并发摊平。

### 2.1.4 长尾的四种处理

| 机制 | 做法 | 数字 |
|---|---|---|
| **partial rollout / 续跑** | 预算用尽时暂停在飞的轨迹，连 KV-cache 指纹一起持久化，由下一个策略版本续跑 | Ring 2.6（ASystem）、Kimi K2（引自 K1.5）、slime `--partial-rollout`、verl `partial_rollout`。代价：一条 response 含多个权重版本 |
| **主动中断**（APRIL 2509.18521） | 超订 → 够数就**主动打断**剩余 → partial 存 buffer → 下轮续跑 | DAPO-Math/Qwen3-4B **+17%**、DeepScaleR/GRPO +21%、DeepMath/GSPO **+35%**；8 卡吞吐 9,814 → 12,210 tok/s（+31.3%）。**代价：约 40% 的 rollout 含前代策略生成的片段** |
| **冗余超订**（ROLL Flash） | 多开 env group / group_size，先到先用 | 固定 batch 256，`32×8 → 36×12` 每步 **243 s → 45 s（5.45×）**。**加 group 数比加 group_size 更有效** |
| **按 token 预算切步** | 每个优化步由全局 token 预算 Φ 门控，而不是等最慢的轨迹 | Ring 2.6：「按 token 数而不是按最慢轨迹切步」。配 overlap batch dispatcher，上一批还在收集时就提交新工作，推理池永不在 batch 边界被抽空 |

另两条可抄的工程细节：
- **长度 ranker 预测长尾**（StreamRL 2504.15930）：用 Qwen2.5-7B 预测输出长度，对最长 20% 的 recall **0.87**、
  10% 为 0.82、5% 为 0.76；训练只几分钟、纯离线、无在线开销。用来提前把长的排到前面。
- **贪心 collation**（Magistral 2506.10910）：按长度降序装 microbatch，**减少 19% padding**。
  同时必须保证「不得对序列长度引入偏差」—— 完成快的短序列不能被超采样。

### 2.1.5 reward 必须是独立可扩容的服务

这是本节最该照抄的一条。六个独立来源都把 reward 做成了服务，而不是训练循环里的函数：

| 来源 | 做法 | 数字 |
|---|---|---|
| **Ling 2.0**（2510.22115 §4.4） | 统一 reward 系统同时承载 rule-based / model-based / 多语言代码 verification，**三个模块**：高可用沙箱（含**视觉 reward evaluator**）、抢占式调度 + 高性能**有界队列**、异步 reward 计算框架 | **扩展到 40K 并发异构 reward 请求，成功率持续 > 99.9%**；有界队列缓解峰值超时，**吞吐 +39%**；异步 reward 解耦训练迭代，**训练时间最多降 30%** |
| **Ring 2.6**（2606.15079） | **数千个 ASandbox 副本**；推理引擎与环境**独立扩容**；**rollout controller 把每次工具调用建模成 awaitable，保证 GPU 绝不被 pending 的 HTTP/MCP 请求占住**；统一 verifier 接口（推理 / coding harness / 工具模拟器 / 浏览器全走同一套 HTTP/MCP 契约） | 因此 reasoning 与 agentic 数据集能混在同一个 run 里 |
| **AReaL**（2505.24298 §4.1、§6） | 独立 `Reward Service`；**reward 计算与 TCP 传输放到独立线程**，与后续生成请求 pipeline 重叠；rollout worker 内用 asyncio 协程避免互相阻塞 | 设备切分 **推理:训练 = 3:4**（实测优于 50/50） |
| **ROLL**（2506.06122） | `Environment Worker` 为一等公民、支持弹性扩容；**sample-level rollout lifecycle control**（每样本独立路由）；ray 异步 reward，三类 worker（rule / sandbox / LLM-judge）按负载动态计算；**CPU 密集的 reward worker 刻意分散到不同 resource pool 避免互相干扰** | 规模声明：200B+ MoE、数千卡、连续两周无中断 |
| **verl**（`docs/advance/reward_loop.rst`） | `RewardLoopManager` / `RewardLoopWorker`，每条样本 `asyncio.create_task`；四种 manager：`naive` / `dapo` / **`limit`（限制并发，用于外部 API 限流）** / **`remote`（独立进程，适合 CPU 密集）**；RM 可 colocate 或 **standalone resource pool**（每条 rollout 完成后立即评分） | 文档明确推荐 reward 函数写成异步 |
| **GLM-4.5**（2508.06471 §3.5） | **统一 HTTP endpoint + 中央 data pool**：agent 框架大多输出 message-list，全部落 data pool 作为训练共享源；task 侧 rollout 逻辑与 RL 训练彻底解耦；data pool 支持按任务定制过滤与动态采样 | 推理 RL 用同步 colocated；**SWE 这类长周期任务用解耦异步** |

**Ling 2.0 的 `视觉 reward evaluator` 已经在生产 reward 池里** ——
这是「渲染后 VLM judge」目前最接近的工业先例，值得作为本项目的架构背书。

### 2.1.6 训推精度一致：不只是算法问题

| 来源 | 做法与数字 |
|---|---|
| **Ring 2.6** | Megatron 训练与 SGLang 推理**双边都用 FP32 算 LM Head，带来约 2 个点的 reward 提升**；其余层 module-aware FP8（Attention Linear 与 Shared Experts 保 BF16，Routed Experts 用 blockwise FP8）；**RL 初始化时加载 FP32 optimizer master weight 而非反量化的 BF16 权重**，改善早期 reward 增长；推理 kernel 的融合粒度与数值行为**刻意对齐训练阶段** |
| **ScaleRL**（2510.13786） | **FP32 logits（LM head）把渐近性能从 0.52 抬到 0.61** —— 单项最大的 asymptote 提升 |
| **Ling 2.0** | 全程 FP8 训练（激活/梯度 [1,128]、权重 [128,128] 分块），900B token 后与 BF16 的相对 loss 差 **< 0.25%**（均值约 0.1%），显存降 > 15%、MFU +15% |
| **GLM-4.5** | **BF16 训练 / FP8 推理**，每次更新前在线 block-wise 量化 —— 主动接受更大 mismatch 换 rollout 吞吐 |
| **NeMo-DCR**（2610.08430） | 6 个模型实测每步只有 **0.6%~1.2% 的 BF16 元素真正变值**；delta 压缩后 1T 模型跨区 refit 从 **87.5 分钟降到 150 秒**，且 bit-exact（强调「rollout–training 数值不一致会破坏 RL 稳定性」） |
| **Magistral** | 权重**在生成途中就地替换**，**不刷新 KV cache**（原文：因为损失函数本身有 off-policy 校正，实测没必要重算）；NCCL GPU-to-GPU 广播把单次更新压到 **< 5 秒** |

两条相反的工程选择（都有道理，按场景选）：

| 选择 | 代表 | 理由 |
|---|---|---|
| **中断生成、丢弃旧 KV cache、用新权重重算 prefill** | AReaL | 把 staleness 压到最小。代价是重复 prefill |
| **生成途中就地换权重、保留 KV cache** | Magistral | 省掉重复 prefill。代价是前缀分布错配（slime 提供 `--mask-offpolicy-in-partial-rollout` 把前缀 token 从 loss 排除，但原文承认**这不消除前缀分布错配**） |

### 2.1.7 本项目的架构建议

```
┌─ Rollout 池（GPU，64 卡）──────┐      ┌─ Render 池（CPU，43~365 核）─┐
│ vLLM/SGLang server mode        │      │ 常驻浏览器池（8 浏览器×8 页） │
│ agent loop 协程并发            │─────▶│ 常驻 bpy worker（避免 13 s    │
│ sticky session 绑 request_id   │      │   shader 编译）               │
└───────────┬────────────────────┘      │ 有界队列 + 超时 + 冗余超订    │
            │                            └───────────┬───────────────────┘
            │                                        │
            │                            ┌─ Judge 池（GPU，2~4 卡）─────┐
            │                            │ 7B 专训 RM，取 logits 概率   │
            │                            └───────────┬───────────────────┘
            ▼                                        ▼
      ┌─ Data pool / SampleBuffer（上界 (1+α)×batch，α=2）──────────────┐
      │ 环境故障样本 → 回炉重排，不进训练                                │
      │ 预算耗尽样本 → 强制提交，reward 乘 0.5                           │
      └───────────────────────────┬──────────────────────────────────────┘
                                  ▼
                    ┌─ Trainer（GPU，64 卡）─────────┐
                    │ decoupled PPO / rollout IS 校正 │
                    │ recompute_logprobs = true       │
                    └─────────────────────────────────┘
```

关键参数（综合各家默认值）：

| 参数 | 建议值 | 依据 |
|---|---|---|
| staleness α | **2**（序列长、batch 64） | ROLL Flash 表 1 的两条单调性 |
| 必须开 decoupled loss / rollout IS 校正 | **是** | AReaL 表 2：不开则 η=4 腰斩 |
| `recompute_logprobs` | **true** | AReaL 文档：启用 decoupled loss 时必须 |
| 渲染队列 | **有界**（抢占式调度） | Ling 2.0：有界队列缓解峰值超时，吞吐 +39% |
| 工具调用 | **建模为 awaitable** | Ring 2.6：保证 GPU 不被 pending HTTP 占住 |
| 冗余超订 | **加 group 数**，不是加 group_size | ROLL Flash §5.2.2：5.45× |
| 渲染 worker : 训练 GPU | 见 2.2.3（0.7 ~ 26 核/卡） | 本机实测推算 |
| 推理 GPU : 训练 GPU | **3 : 4** 起调 | AReaL 实测优于 50/50 |
| LM head 精度 | **FP32**（训练与推理双边） | Ring 2.6 约 +2 个点 reward；ScaleRL 渐近 0.52→0.61 |

## 2.2 渲染 worker 池怎么和 GPU 训练集群配比（本机实测推算）

### 2.2.1 单位成本（来自 06_harness 第 4 节，48 核配额 KML pod，无 GPU）

| 取证单位 | 实测吞吐 | 折算单位成本 |
|---|---|---|
| three.js 一次完整取证（reload + 8 视角转台 + scene graph） | 14.3 任务/s（8 浏览器 × 8 页） | **3.35 core-s / 次** |
| Blender Workbench 一个视角（512×384） | 15.5 视角/s（32 进程） | 3.09 core-s / 视角 → **24.7 core-s / 8 视角** |
| Blender Cycles CPU 一个视角（512, 32 spp） | 0.88 s/视角（8 线程） | 7.04 core-s / 视角 → **56.3 core-s / 8 视角** |

换算口径：`core-s = 核配额 ÷ 吞吐`。48 核写成 47.9（cgroup `cpu.max=4787500/100000`）。
Workbench 和 Cycles 的数字已含每进程约 1 s 的启动与加载；常驻 worker 可以再省掉这一项，这里不扣，算保守。

### 2.2.2 两种 rollout 形态的 CPU 需求

假设（写清楚，便于换算）：

| 参数 | 多轮 agent | 单轮 generate-then-verify |
|---|---|---|
| 每条轨迹模型步数 | 40 | 1 |
| 其中带渲染自检的步数 | 12（30%） | 0 |
| 终局取证 | 3 次重复（测 flaky） | 3 次重复 |
| 轨迹墙钟 | 1200 s（40 步 × 800 输出 token，单序列约 25 tok/s） | 80 s（2000 输出 token） |

推算结果（1024 个并发 rollout 槽）：

| 形态 | CPU / 轨迹 | 核 / 并发槽 | 1024 并发所需 | 折 48 核机器 |
|---|---|---|---|---|
| 多轮 three.js | 50 core-s | 0.042 | **43 核** | 0.9 台 |
| 多轮 Blender（Workbench 自检 + 终局 Cycles） | 427 core-s | 0.356 | **365 核** | 7.6 台 |
| 单轮 three.js | 10 core-s | 0.126 | **129 核** | 2.7 台 |
| 单轮 Blender | 130 core-s | 1.631 | **1670 核** | 34.9 台 |

**三条结论**

1. **多轮 agent 形态下，渲染池几乎免费。** 轨迹墙钟被 LLM 解码占满，渲染只占百分之几。
   1024 并发的 three.js 自检只要 43 核 —— 比 rollout GPU 节点的宿主 CPU 还少，不需要独立渲染农场。
2. **单轮形态下反而贵。** 墙钟从 1200 s 压到 80 s，而取证成本不变，单位成本涨 15 倍。
   单轮 Blender 要 35 台机器，这时才需要独立的渲染集群。
3. **贵的是 Cycles，不是 Blender。** Workbench 与 Cycles 差 2.3 倍（24.7 对 56.3 core-s / 8 视角），
   EEVEE Next 在 llvmpipe 上更差（06 第 4.2 节：比 Legacy 慢 4~5 倍，首帧 shader 编译 13 s）。
   自检全部走 Workbench，Cycles 只在终局 reward 用一次。

### 2.2.3 和 GPU 的配比

再加一层假设：一个 30B-A3B 量级的 MoE，用 vLLM/SGLang 在 8 卡上服务约 128 条并发序列
（本机未实测，按 qwen38-vllm-fleet 的量级估）。那么 1024 并发 ≈ 64 张卡做 rollout，另配同量级卡做训练。

| 形态 | 每张 rollout GPU 需要配的 CPU 核 |
|---|---|
| 多轮 three.js | 0.7 |
| 多轮 Blender | 5.7 |
| 单轮 three.js | 2.0 |
| 单轮 Blender | 26 |

一台 8 卡 GPU 机通常有 96~192 逻辑核，即 12~24 核/卡。**除了「单轮 + Blender + Cycles」这一格，
其余三格都能用 rollout 节点的宿主 CPU 吃掉**，不必单独建渲染池。
真要独立池，按上表乘以安全系数 2（flaky 重跑、长尾任务、变异测试）即可。

### 2.2.4 VLM judge 的 GPU 配比（这才是真成本）

假设每条轨迹 3 次 judge 调用，每次输入 8k 文本 + 一张 1024×512 contact sheet（703 图像 token），输出 500 token。
1024 并发、轨迹墙钟 1200 s，则 judge 负载 = 2.56 调用/s = 1,280 输出 tok/s + 约 23k 预填 tok/s。

| judge 规模 | 大致需要的卡 | 占 64 张 rollout 卡的比例 |
|---|---|---|
| 7~8B | 2~4 | 3%~6% |
| 32B | 8~16 | 13%~25% |
| 72B | 20~40 | 31%~63% |

这组数字（自行推算，未实测）是「要不要训自己的小 reward model」的经济学依据：
**从 72B 通用 judge 换成 7B 专训 RM，省下的是 30%~60% 的 rollout 卡**。第 3.2 节给质量侧的证据。

### 2.2.5 一轮 RL 的量级

规模假设：400 个优化步 × 64 个 prompt × 组大小 G=8 = **204,800 条轨迹**。

| 项 | 多轮 three.js | 多轮 Blender |
|---|---|---|
| 渲染 CPU 总量 | 2,858 core-h = 60 机时（48 核）= **2.5 机日** | 24,301 core-h = 507 机时 = **21 机日** |
| 输出 token 总量 | 6.55 B（40 步 × 800） | 同 |
| rollout 墙钟（1024 并发，25 tok/s/序列） | **约 71 小时** | 同 |
| GPU 总量（64 rollout + 64 训练，按 100 小时） | **约 12,800 GPU 小时** | 同 |

含义：**渲染不是瓶颈，解码是。** 一轮 RL 的 CPU 成本（2.5~21 机日）相对 12,800 GPU 小时可以忽略。
所以工程重点不是「渲染够不够快」，而是 **2.1 节的异步解耦**：别让慢 verifier 把 GPU 拖空。

---

## 2.3 环境隔离、超时、非模型故障

### 2.3.1 四类失败，三种处理 —— 而且选错会训崩

**唯一一篇把这件事写清楚的论文是 SWE-Master（2602.03411 §3.4.2，式 4/5）**。
它把终止原因分四类，走三条不同的路：

| 类别 | SWE-Master 的标签 | 处理 | 原文 |
|---|---|---|---|
| **A. 正常结束** | `DONE`（主动提交） | 正常 reward、正常进梯度 | — |
| **B. 预算耗尽** | `TIMEOUT` / `MAX_STEPS` / `MAX_TOKENS` | **强制提交**，reward 乘惩罚系数 **α = 0.5** | — |
| **C. 环境/基础设施故障** | `CONTAINER_FAILED`（硬件问题、环境崩溃）、`SERVER_ERROR` | **损失 mask，M = 0** | 「masking loss of failed trajectories stemming from container runtime errors, guaranteeing that policy updates are driven **exclusively by valid agent-environment interactions**」 |
| **D. 模型自己的错** | 代码报错、渲染空白、断言不过、console 有异常 | 给 0（或负分），**正常进梯度** | 这是要学的信号。ReLook：任一截图无效直接 0 分，有效渲染率 40%→80%（04 §5.1） |

**为什么要单设 B 这一档**（§3.4.1）：RL 初期策略会陷入「反复生成/修改单测却不提交」的循环，
**约 20% 的轨迹因 token / 轮数耗尽被截断**，全拿 0 reward，平均 reward 退化 —— 才引入强制提交 + reward shaping。

**最重要的一条反面证据（§6.3）**：
DeepSWE 的做法是「被环境约束（最大上下文 / 超时 / 轮数）截断的轨迹 → reward 置 0 并 mask loss」，
即把 B 也当成 C 处理。SWE-Master 在自己的模型上复现这个策略，结果是
**reward 持续下降直至训练崩溃**（图 12）。
作者归因为初始化与数据复杂度差异：DeepSWE 从零在较简单的 R2E-Gym 上训，
SWE-Master 先在长程异构数据上做了充分 SFT。

→ **操作口径：B 和 C 必须分开。** B 用「强制提交 + reward 打折」，C 用「mask loss / 丢弃」。
把 B 当 C 处理在长程任务上有训崩的实录。

### 2.3.2 C 类（真故障）的三种实现，各有适用

| 做法 | 代表 | 细节 |
|---|---|---|
| **mask loss**（样本留在组里，但不贡献梯度） | SWE-Master | 适合故障率低（< 2%）的情况。注意组内均值仍会被这条样本的 reward 影响，除非一起从 baseline 里剔除 |
| **丢弃整组、回炉重排** | **slime** `examples/fully_async`：含 `ABORTED` 样本的 group 被 push 回 `data_buffer.add_samples`，**而不是送进训练**。**NeMo-RL**：`max_generation_failures`（默认 0），超限的 prompt group 在正常运行中被丢弃且 resume 不恢复 | 最干净。代价是浪费已完成的那几条 |
| **冗余超订、绕过慢/死环境** | **ROLL Flash** 2510.11345 §5.2.2：多开 env group，先到先用；明确目标是「mitigate the negative impact of environment instability，防止 fail-slow 与 fail-stop 环境成为系统瓶颈」 | 固定 batch 256，`32×8 → 36×12` 每步 **243 s → 45 s（5.45×）**。**加 group 数比加 group_size 更有效** |
| **timeout / retry / skip** | Trinity-RFT 2505.17826：「deals with environment/agent failures gracefully via dedicated **timeout/retry/skip** mechanisms」 | 最朴素，适合起步 |

**为什么不能把 C 一律给 0**：组相对算法（GRPO 系）的基线是组内均值。
如果一个 prompt 的 8 条 rollout 里有 3 条因为沙箱挂了拿 0，组均值被压低，
剩下 5 条里哪怕写得很差也会拿到正优势 —— 等于用基础设施噪声给坏答案发奖。
这和 DAPO 的 dynamic sampling（丢弃全 0 / 全 1 组）是同一个机制的两面。

**一个容易漏的统计偏差**（NeMo-RL `docs/guides/async-grpo.md`）：
一个 prompt group 只有**最长的那条 rollout 完成**才算完成，
所以 checkpoint 时滞留在 buffer 里的 group **系统性偏向短 rollout**。
官方建议 `checkpointing.load_replay_buffer: false`，用重算换无偏的 step 组成。
→ 本项目用 partial rollout 时必须注意这条：**续跑机制会悄悄把训练分布推向短轨迹**，
而短轨迹在 visual coding 里往往意味着「没做自检」。

### 2.3.3 超时阈值的工业取值

| 来源 | 配置 |
|---|---|
| **SWE-Master** §4 | 单轨迹超时 **5,400 秒**、最多 **150 轮**、上下文 **108K**；每题 4 条并行 rollout、温度 1.0。SFT 轨迹上限 80K token / 100 轮（超出剪掉） |
| **R2E-Gym** 2504.07164 | 两套：40 步 / 32K token / **整轨迹 10 分钟 / 单动作 90 秒**；或 40 步 / 20K token / **5 分钟 / 60 秒**。原文动机：「防止 agent 启动长跑后台进程」 |
| **verl + SandboxFusion** | `default_timeout` **30 s**、`max_concurrent` 256、`memory_limit_mb` 1024、全局 `rate_limit=10`（Ray actor + Semaphore 做令牌桶防 429） |
| **AReaL** `examples/swe` | `econfig` 里有 `step_limit`、`max_completion_tokens`、**`timeout`（每 episode 墙钟上限，秒）** |

**本项目的建议**：单动作（一次渲染取证）**60 秒**、单轨迹 **1,800 秒**、最多 **60 轮**、上下文 **80K**。
依据：Cycles 8 视角约 7 s（06 §4.2），60 秒给了 8 倍余量，能区分「机器慢」和「模型写了死循环」。

### 2.3.4 本场景特有的隔离项

| 项 | 做法 | 出处 |
|---|---|---|
| 每任务独立容器 | GLM-4.5 的 agent RL：高并发 Docker runtime，每个任务一套隔离环境 | 2508.06471 §3.5 |
| 共享文件系统但隔离进程 | UI-TARS-2 的 all-in-one sandbox：GUI + 终端 + 文件系统共享一个容器实例，服务用 proxy URL 暴露给 agent 预览前后端 | 2509.02544 §2.2 |
| 禁止联网 | 白名单。WorldCoder-Bench 记录过模型绕过给定资源目录、从 GitHub 拉模型（2606.01869 App. D.2） | 已在 04 覆盖 |
| Blender 必须从干净 .blend 开始 | VETR 记录：同一程序在持久场景上执行 9 次，修改器叠 9 层，网格体积缩到 1/256（App. C.1） | 已在 04 覆盖 |
| 浏览器池要定期回收 | SwiftShader 在单浏览器的 GPU 进程里串行；长跑会漏内存。按任务数轮换浏览器实例 | 06 §4.1.3 推断 |
| 快照要和上下文对齐 | AgentRewind：只回滚上下文不回滚文件系统，−43.9 pp | 已在 05 §4.3 覆盖 |
| **作弊通路在环境层拦截，不在 reward 层扣分** | SWE-Master §6.4：模型会自发用 `git show` / `git log` 从网络拉 golden patch；环境被配置为**拦截并返回禁止警告**，SFT 与 RL 全程强制。消融：**放开 git 限制反而略微掉分** | 2602.03411 §6.4 |
| 用两个独立沙箱分别跑 agent 和 grader | slime `examples/coding_agent_rl`：一个沙箱跑 agent、**另一个全新沙箱**上 apply git diff 再跑官方测试出 reward；patch 按「agent 运行前后的真实 workspace 差异」比对 | slime 仓库 |
| 内存要用 cgroup 硬限，不能靠 RSS 监控 | 同上，sunabako 要求 delegated cgroup（`SUNABAKO_ALLOW_TEST_MEMORY=0`），原文说明 RSS 监控无法硬限聚合内存 | slime 仓库 |

**沙箱规模的公开参照**（用来判断自己的渲染池是不是「正常量级」）：

| 来源 | 规模 |
|---|---|
| Ling 2.0 | **40K 并发异构 reward 请求，成功率 > 99.9%** |
| Ring 2.6 | **数千个 ASandbox 副本**，与推理引擎独立扩容 |
| verl + SandboxFusion | `max_concurrent=256`、全局 `rate_limit=10`、`default_timeout=30 s` |
| SWE-Gym（05 §2.1 的补充） | 从 358 个仓库抽 64,689 个候选，**验证与过滤消耗约 50,000 CPU 核时**，最终只剩 2,438 个；**预构建 Docker 镜像共 6 TB** |
| SWE-smith | 50,137 实例 / 128 仓库；**同仓库任务共享环境，env 总大小仅 295 GB**（对比 SWE-Gym 6 TB、R2E-Gym Subset 4 TB） |

**SWE-smith 的「同仓库共享环境」把镜像体积压了 20 倍，这条对本项目直接可用**：
three.js / Blender 的任务应按「依赖集」而不是按「任务」建镜像
（一个 three 版本 + 一套 vendored 资产 = 一个镜像，下面挂几百个任务）。
对照 06 §4.1.5 的体积：chrome-linux64 552MB、node_modules 65MB、bpy 4.5 的 site-packages 784MB。

### 2.3.5 格式与协议失败：给 0 还是给负分

GLM-4.5 的 agent RL：**工具调用格式错就直接中止整条轨迹并给 0 reward**（2508.06471 §3.3.2，process format penalty）。
这和 SWE-RL 的 `-1`（格式错）对比有意思：

| 工作 | 格式错的处理 | 正常时的 reward |
|---|---|---|
| SWE-RL（2502.18449 式 1） | **−1** | `difflib.SequenceMatcher` 相似度，连续值 0~1 |
| GLM-4.5 agent RL（§3.3.2） | **0，并中止轨迹** | 最终答案正确性 |

区别在于有没有负分空间。给 −1 时，「格式错」严格差于「格式对但答案全错」，模型先学会闭嘴守格式；
给 0 时两者等价，靠的是格式正确的样本天然更容易拿到正分。
本场景建议前者：渲染型任务里「不可执行」和「执行了但很差」必须可区分，否则会复现 CAD-Coder 的塌缩
（只用 CD 作 reward，约 200 步后输出不可执行代码，训练中止；2505.19713 App. B）。

## 2.4 成本估算

### 2.4.1 一条 visual coding 轨迹的 token 账

假设（40 步多轮，图像走 3 张滑窗 contact sheet，见 3.1.1）：

| 项 | 数量 |
|---|---|
| 系统提示 + 任务（含参考图） | 3,000 |
| 每步模型输出（think + 代码 + 工具调用） | 800 |
| 每步文本观察（scene graph 摘要 + console） | 300 |
| 常驻图像（3 张 1024×512 contact sheet） | 2,109 |
| **终局上下文** | **约 49,000** |
| **累计输出** | **32,000** |
| **累计输入（无 prefix cache）** | **约 1.06 M** |
| 其中图像部分 | 约 84 k（3 × 703 × 40，滑窗内的图每步重读） |

**三个量级感**
- 图像只占累计输入的 8%。**上下文爆炸的主因是文本历史，不是图像**（3.1.1）。
- 累计输入是累计输出的 **33 倍**。所以 prefix cache 命中率是成本的第一旋钮：
  每步新增的未缓存部分只有约 1.1 k token，理论命中率可以到 97%。
**公开的轨迹 token 账（对照用）**

| 来源 | 每条轨迹 |
|---|---|
| SWE-Gym（05 §2.1） | 491 条 SFT 轨迹平均约 **19 轮、约 19,000 token** |
| **SWE-Master 表 6**（SWE-bench Verified，resolve 61.4%） | **输入 5,549.6k（约 5.55 M，累计重发上下文）、输出 32.5k、平均 111.2 轮** |
| 同上，加 LSP 工具后 | **4,232.1k / 27.2k / 91.7 轮**（输入 −23.7%、输出 −16.3%、轨迹长度 −17.5%），resolve 61.0% |
| SWE-Master 表 5（前沿模型在 R2E-Gym scaffold 上） | MiniMax-M2.1 **82.0 轮**、GLM-4.7 **97.3 轮** |

读法：
- 我们推算的 **1.06 M 输入 / 32 k 输出** 与 SWE-Master 的输出量（32.5k）几乎一致，
  但输入少 5 倍 —— 因为我们假设 40 步而不是 111 步。**输入 token 基本等于「步数的平方」量级**，
  所以**控制步数比控制单步长度重要得多**。
- SWE-Master 加了 LSP 工具后输入降 23.7%、轮数降 17.5%，分数基本不变。
  **给 agent 更强的结构化观测工具，等于直接省 token** —— 这正是 3.1.3 建议优先给 scene graph 的理由。
- SWE-Master 剪掉超过 **80K token 或 100 turn** 的实例，这类只占已解决实例的 5% 但 OOM 风险不成比例（05 §2.4）。
  → 我们的 49k 终局上下文在正常区间，但要设 80k 硬上限。

### 2.4.2 一次 verify 的成本

| 层 | 内容 | CPU | GPU | 墙钟 |
|---|---|---|---|---|
| L0 硬门槛 | 能跑、canvas 非空、无 JS 错误 | 包含在下一行 | 0 | < 0.5 s |
| L1 程序化断言（three.js） | reload + 8 视角 + scene graph + 断言 | **3.35 core-s** | 0 | 约 0.4 s（p50 383 ms） |
| L1 程序化断言（Blender Workbench） | 8 视角 512×384 | **24.7 core-s** | 0 | 约 1.4 s（常驻 worker） |
| L2 几何/感知 | 按色体素 IoU、CD、法线比对 | 约 1~3 core-s（numpy） | 可选 | < 1 s |
| L2' Cycles 终局渲染 | 8 视角 512/32spp | **56.3 core-s** | 0 | 约 7 s |
| L3 VLM rubric | contact sheet + 代码片段，3~5 次取概率 | 0 | 约 1.5 s/次（7B，估） | 约 5~8 s |
| L4 组内 pairwise | G=16 的 tournament | 0 | 比较成本与生成解耦 | UI2Code^N 实测只占训练时间 **2.2%** |

**一条实测的黄金数字**（UI2Code^N 2511.08195 表 20，RVPO 训练的墙钟拆解）：

| 阶段 | 时间 (s) | 占比 |
|---|---|---|
| Generation | 130.9 | **75.4%** |
| **Rendering** | 38.8 | **22.4%** |
| Comparison（VLM 两两比较） | 3.9 | **2.2%** |

这是目前唯一一份「渲染型 verifier 在 RL 里到底占多少时间」的公开拆解。读法：
- **渲染占 22.4%**，不可忽略但也不是瓶颈。这是**单轮**网页渲染的口径（每条 rollout 一次生成一次渲染）；
  我在 2.2.2 推算的多轮形态下渲染占比会更低（约 4%），单轮形态下更高 —— 与这个数字方向一致。
- **VLM 比较只占 2.2%**，原因写在原文：**候选 rollout 只生成一次、复用做两两比较**，
  所以「比较成本与昂贵的 token 生成解耦」；再用 tournament 聚合减少不必要的比较次数。
  → **这是 L4 组内 pairwise 能用在 RL 里的全部理由**，值得照抄。

### 2.4.3 跑一轮 RL 的量级

本项目的推算（规模假设见 2.2.5：400 步 × 64 prompt × G=8 = 204,800 条轨迹）：

| 项 | 数量 |
|---|---|
| 轨迹数 | 204,800 |
| 输出 token | **6.55 B** |
| 输入 token（无 cache） | 约 2.2 × 10^11；按 97% cache 命中算实际预填约 7 × 10^9 |
| 渲染 CPU（three.js 多轮） | 2,858 core-h = **2.5 机日**（48 核） |
| 渲染 CPU（Blender 多轮） | 24,301 core-h = **21 机日** |
| rollout 墙钟（1024 并发，25 tok/s/序列） | 约 **71 小时** |
| GPU 总量（64 rollout + 64 训练 × 100 h） | 约 **12,800 GPU 小时** |
| judge GPU（7B） | 2~4 卡 × 100 h = 200~400 GPU 小时（占 1.5%~3%） |

### 2.4.4 公开披露的对照（核实过）

| 来源 | 披露 |
|---|---|
| **MiniMax-M1**（2506.13585 摘要） | **512 × H800、3 周**跑完全部 RL，租用成本 **534,700 美元**（约 258,000 GPU 小时）。训练中 AIME24 从 68% 涨到 80% |
| **Qwen3**（2505.09388 表 21） | 8B 模型、只做数学+代码：**RL = 17,920 GPU 小时** |
| **ScaleRL**（2510.13786） | 全部实验 **> 400,000 GPU 小时**（GB200）；单次 8B 实验最多 **16,000** GPU 小时；最大一次 run **100,000** GPU 小时（7,400 步） |
| **AReaL**（2505.24298 表 1，H800 8 卡/节点） | 1.5B：16 节点 × 250 步 = **14.8 h**（同步 41.0 h）；7B：24 节点 = **25.4 h**（同步 57.7 h）；14B 代码：32 节点 × 80 步 = **21.9 h**；32B 代码：48 节点 × 60 步 = **31.1 h** |
| **Trinity-RFT**（表 3） | 7B 一个 epoch：严格 on-policy **130.33 h** → one-step off-policy **48.98 h（2.66×）** |
| **verl** `fully_async_policy` | Qwen2.5-Math-7B / H20 / DAPO / 400 步：32 卡同步 **3d17h5m**；128 卡同步 1d16h48m → 全异步 **17h22m** |
| **Dr.GRPO**（2503.20783） | **27 小时 / 8 × A100**（7B，只用 MATH level 3-5，generation budget 3k） |
| **ROLL**（2506.06122） | 200B+ MoE、**数千卡、约两周无中断**（无更细口径） |
| **SWE-smith**（05 §2.2） | 5 万任务 / 128 仓库，造数据总成本约 **1,360 美元**；轨迹生成每条约 **2 美元** |
| **Web-Shepherd**（05 §5.3） | 3B PRM 每 1000 实例 **4.67 美元**（A100 1.19 美元/小时折算） |

**量级定位**：我们推算的 12,800 GPU 小时与 Qwen3-8B 的纯 RL（17,920）同档，
远低于 MiniMax-M1（约 258,000）。
这是一个「一次正经的训练 run」的量级，不是「一次旗舰模型训练」的量级。
**换句话说：渲染型 verifier 不会把 RL 的成本量级改变一个档位** —— 它改变的是工程复杂度（2.1、2.3），不是账单。

### 2.4.5 一个必须先考虑的替代方案：on-policy 蒸馏

Qwen3（2505.09388 表 21）给了一组很不客气的对照（8B 模型，数学 + 代码）：

| 方案 | GPU 小时 | AIME24 | AIME25 | LiveCodeBench v5 |
|---|---|---|---|---|
| **强化学习** | **17,920** | 67.6 | 55.5 | 52.9 |
| **on-policy 蒸馏**（用更强的教师） | **1,800** | **74.4** | **65.5** | **60.3** |

**算力只有 1/10，分数全面更高。** 而且原文补了一句：**RL 完全没有提升 pass@64**。

这条必须写在前面，因为它决定了什么时候该上 RL：

| 条件 | 该做什么 |
|---|---|
| 有一个在本任务上明显更强的教师（例如 Claude / GPT 级在 three.js 上远超自家模型） | **先做 on-policy 蒸馏**，不要上 RL。10 倍算力差 |
| 没有更强的教师，或教师也做不对（本项目的 3D 场景大概属于这一类，参见 04 的 WorldCoder-Bench 通过率只有 2.7%） | **RL 是唯一选项** |
| 想扩能力边界（pass@k 要涨） | RL 要配课程（1.4），否则 pass@256 相对 base 是 **−0.5 点** |

本项目的判断：**三类任务要分开**。
- 前端 / WebDev：前沿模型很强，**优先蒸馏**；
- three.js / Blender 的复刻类：有程序化 GT，**RL 的信号最干净，值得上**；
- 3D 开放设计：教师也做不好、verifier 也最弱，**最后做**。

---

# 3. 视觉 reward 特有的两个问题

## 3.1 图像 token 很贵：每步截图会炸上下文

### 3.1.1 先算清量级

按 Claude 的 `⌈w/28⌉×⌈h/28⌉` 公式（06 §2.2 已核实出处）：

| 图像 | token |
|---|---|
| 1024×768 全图 | 1,036 |
| 512×384 | 266 |
| 8 视角拼成 1024×512 contact sheet（每格 256×256） | **703** |
| 8 视角拼成 768×384 contact sheet（每格 192×192） | 392 |

一条 40 步轨迹的累计输入（假设系统加任务 3k、每步输出 800、每步文本观察 300）：

| 图像策略 | 常驻图像 token | 终局上下文 | 累计输入 |
|---|---|---|---|
| 不给图 | 0 | 47,000 | 0.98 M |
| 滑窗 3 张 contact sheet | 2,109 | 49,109 | 1.06 M |
| 滑窗 3 张 1024×768 全图 | 3,108 | 50,108 | 1.10 M |
| 不滑窗、12 次自检全留 1024×768 | 12,432 | 59,432 | 约 1.3 M |

**结论先给**：在 40 步这个量级上，图像不是上下文爆炸的主因 —— **文本历史才是**（0.98 M 里图像占不到 10%）。
真正会炸的是「每步都截图且不丢」的模式：12 次自检就吃掉 12.4k，20 步以上的交互任务直接翻倍。
所以优先级是：**先设滑窗，再压分辨率，最后才考虑换成文本**。

### 3.1.2 五种做法的公开证据

| 做法 | 代表工作 | 关键数字 | 适用性 |
|---|---|---|---|
| **A. 历史截图滑窗** | OpenCUA（2508.09123 §3.2 图 10） | 历史截图 1 / 3 / 5 张：1→3 大幅提升；**3→5 只有边际收益，却多约 3K 上下文 token，还拖慢收敛**。默认取 **3 张** | 直接可抄。三张的物理含义是「上一步前、上一步后、当前」 |
| 同上，judge 侧 | UI-TARS-2（2509.02544 §2.5.2） | 生成式 ORM 的输入 = 完整文本历史 + **最后 5 张截图**（原文：为了塞进上下文窗口） | judge 比 policy 可以多看两张 |
| **B. 文本历史压到最短** | OpenCUA（§3.2、§5） | 同样 3 张图下，用 L1（只有动作）当文本历史 **优于** L2（思考+动作）；L2 "offers no benefit and may introduce hallucinations" | 轨迹里别保留旧的 thinking。和 05 节的剪枝结论一致 |
| **C. 按需翻历史截图** | VAGEN（2602.00575，已在 05 覆盖） | 关掉「翻历史截图」工具后，准确率 83.1→80.5，而**截图消耗反而从 11.9 张涨到 18.4 张** | verifier 侧最优做法 |
| **D. 文本化替代图像** | VisualWebArena（2401.13649 表 3、附录 C） | GPT-4 纯 a11y 树 **7.25%** → 加 BLIP-2 图像 caption **12.75%** → GPT-4V 真看图 **15.05%** → 加 SoM **16.37%**。困难视觉子集：纯文本 4.8% / caption 8.0% / GPT-4V+SoM 12.4%。OCR 子集 6.4%→12.2% | **caption 能补回约 60% 的差距，但补不满**。对本场景是好消息：我们的「文本化」不是 caption，而是**精确的 scene graph**，信息无损 |
| 同上，反例 | OpenCUA 表 6 | 推理时用 L3（先把截图描述出来再决策）**不如** L2；原因是描述里混进大量与任务无关的元素 | **别让模型把图转写成文字再推理** |
| **E. 视觉 token 压缩** | ShowUI（2411.17465 §2.1、图 2） | 1344×756 在 14×14 patch 下 5,184 token，2×2 merge 后仍 1,296；按 RGB 连通分量做 UI-guided token selection 砍掉 **33%** 冗余视觉 token、训练加速 **1.4×**；2B 模型 256K 数据零样本 grounding 75.1% | 渲染图大面积纯色（天空、背景、留白）比 UI 更冗余，这条迁移性好 |

### 3.1.3 本场景的推荐组合

渲染型任务比 GUI 任务多一张牌：**运行时状态是精确、无损、便宜的**（06 §2.2 实测：three.js scene graph 1.8 ms、Blender 0.1~1 ms，返回 JSON 是毫秒级）。
所以上下文预算应该这样花：

| 优先级 | 给什么 | 预算 |
|---|---|---|
| 1 | **scene graph / DOM 摘要 / console**（文本，精确） | 每步 200~600 token，必给 |
| 2 | **当前状态的 contact sheet**（8 视角 192×192 → 392 token，或 256×256 → 703 token） | 只在「刚改完、要看一眼」的步给 |
| 3 | 历史截图滑窗 **最多 3 张**，且历史位只存低分辨率（512×384 → 266 token） | 约 800 token 常驻 |
| 4 | 局部放大图（只在 judge 判细节时按需取） | 不进 policy 上下文 |

硬预算写进环境（06 §2.2 已写）：每条轨迹视觉 token 上限，超了强制降分辨率。
这是 RL 成本的主要旋钮，也是防止模型学会「疯狂截图刷观测」的唯一办法。

**一个本场景独有的替代方案**：把多视角比对交给**程序**而不是模型。
原型的结论是按颜色体素 IoU 在 6 个候选上唯一能全部区分（STATE.md 03:05），变异测试 11/13（03:25）。
这类数字进上下文只要几十个 token，比 8 张图的 5,600 token 便宜两个数量级，而且不受 VLM 空间推理弱的影响
（BLINK 上 GPT-4V 51.26%、人类 95.7%，2404.12390 表 1）。

---

## 3.2 VLM judge 作 reward：延迟、吞吐、规模，以及该不该自己训

### 3.2.1 「训一个小的」压倒「用一个大的」——证据很硬

VL-RewardBench（1,250 条，Overall / Macro，数字取自 Skywork-VL Reward 2505.07263 表 3）：

| 模型 | 规模 | Overall | Macro | 类型 |
|---|---|---|---|---|
| Qwen2-VL-7B-Instruct | 7B | 28.3 | 33.9 | 通用 judge |
| Qwen2.5-VL-7B-Instruct | 7B | 48.0 | 49.5 | 通用 judge |
| InternVL3-8B | 8B | 57.0 | 55.6 | 通用 judge |
| Qwen2-VL-72B-Instruct | 72B | 39.5 | 43.0 | 通用 judge |
| Molmo-72B-0924 | 72B | 44.1 | 43.7 | 通用 judge |
| QVQ-72B-Preview | 72B | 46.4 | 46.4 | 通用 judge |
| Qwen2.5-VL-72B-Instruct | 72B | 51.6 | 52.7 | 通用 judge |
| InternVL3-78B | 78B | 63.3 | 61.6 | 通用 judge |
| Claude-3.5-Sonnet | — | 55.3 | 53.6 | 闭源 |
| GPT-4o（2024-08-06） | — | 65.8 | 62.4 | 闭源 |
| Gemini-2.0-flash-exp | — | 68.8 | 64.5 | 闭源 |
| **IXC-2.5-Reward-7B** | **7B** | **66.3** | **68.6** | **专训 RM** |
| **Skywork-VL Reward** | **7B** | **73.1** | **69.0** | **专训 RM** |

读法：
- **同族扩规模几乎没用**：Qwen2.5-VL 7B→72B 只从 48.0 到 51.6（+3.6）。
- **专训 7B 碾压通用 78B**：73.1 对 63.3（+9.8），也超过 GPT-4o 的 65.8 和 Gemini-2.0-flash 的 68.8。
- 代价很小：Skywork-VL Reward 的训练集约 **190k** 对比较样本（约 70% 带图），
  冻结视觉编码器、只训 projector + 语言主干 + reward head（§3.2）。
- 第二个独立证据：VL-RewardBench 原文（2411.17451 §4.3）报告**对 LLaVA-OneVision-7B 做 critic 训练，判断准确率 +14.7 个点**。
- 第三个独立证据：Web-Shepherd 3B 在 WebRewardBench 上 65.0，GPT-4o-mini 只有 5.0；成本每千实例 4.67 美元对 43.57 美元（已在 05 §5.3 覆盖）。
- 第四个：R1-Reward 用 **200k** 偏好数据做 RL 训练，超过训了 100 万以上样本的 IXC-2.5-Reward（2505.02835 §5.1）。

**所以：该训。** 对 visual coding 场景，更应该训 —— 通用 VL-RM 的训练数据里几乎没有「渲染图对渲染图的差异检测」，
而这恰恰是通用模型最弱的一项（Visual-ERM 实测 GPT-4o 在渲染图差异检测上 F1_hard 只有 25.0，已在 04 覆盖）。

### 3.2.2 judge 的两条已知陷阱

| 陷阱 | 证据 | 含义 |
|---|---|---|
| **感知而非推理是瓶颈** | VL-RewardBench §4.1：Existence / Recognition 类错误率最高，GPT-4o-mini 在 Existence 上错 67.9%，Qwen2-VL-7B 在 Recognition 上错 80.9%；Reasoning 平均错 41.8%。扩规模主要修感知（Qwen2-VL 7B→72B 计数错误 74.1%→55.9%，−18.2 pp），修推理只 −6.0% | 「这个物体在不在」这类问题要交给程序断言，不要交给 judge。和 04 §6 的分层一致 |
| **judge 的 test-time scaling 对小模型是负的** | VL-RewardBench §4.2：K 从 1 到 7，GPT-4o 60.3→62.7；而 **Qwen2-VL-72B 和 Molmo-72B 分别掉 1.7 和 2.6 个点** | 「多采几次投票」不是通用解药。要先在自己的 judge 上量一次 K 曲线再定 K。注意这与 Web-Shepherd「5 次取概率平均 51.4」不矛盾：后者取的是 **logits 概率的均值**，不是采样答案的多数票 |

### 3.2.3 吞吐与延迟

公开论文里几乎没人报 judge 的 wall-clock，只有成本折算。能用的两组：

| 来源 | 口径 | 数字 |
|---|---|---|
| Web-Shepherd（2505.15277，05 §5.3 已覆盖） | 每 1000 实例成本（美元） | 3B 为 4.67、GPT-4o-mini 43.57、GPT-4o 435.74、Qwen2.5-VL-72B 53.69。3B 口径：单张 A100 80GB、1.19 美元/小时、vLLM 吞吐折算；每实例平均 81,287 输入 token、1,953 输出 token |
| VAGEN（2602.00575，05 §5.3 已覆盖） | 每条轨迹截图数 / 输出 token | VAGEN 11.9 / 1218，ProRe 24.2 / 1923 |

反推 Web-Shepherd 的 3B：4.67 美元 / 1000 实例 ÷ 1.19 美元/小时 = 3.92 A100 小时 / 1000 实例
= **约 14 s/实例/卡**，输入 81k token 是大头。
把这个数字套到 2.2.4 节的 1024 并发场景（每条轨迹 3 次 judge、墙钟 1200 s，即 2.56 调用/s）：
14 s/调用 × 2.56 = **36 张 A100 等效**。
但我们的 judge 输入远小于 81k（8k 文本 + 703 图像 token），按 token 数线性折算约 1/9，即 **约 4 张卡**，
与 2.2.4 的独立估算（7B 需 2~4 卡）一致。两条路径互证，可以用这个量级定容量。

### 3.2.4 推荐的 judge 配置（给本项目）

| 维度 | 选择 | 理由 |
|---|---|---|
| 规模 | **7~8B 专训生成式 RM** | 质量超 78B 通用（3.2.1）；成本是 72B 的 1/10（2.2.4） |
| 训练数据 | 1~2 万条带人工裁决的渲染图对比较，加变异测试自动造的负例 | Skywork-VL 用 190k 做通才；我们只做一个窄域，一个数量级就够。负例可由 04 §6.2 的变异测试自动生成（删功能、移 1px、换色、关碰撞） |
| 输入 | contact sheet + 关键源码片段 + **程序先测好的确定性读数**（相机位姿、bbox、部件尺寸） | ArtifactsBench 消融：去掉代码只给图，一致率从 90.95% 掉到 74.94%（04 §2.1）。确定性读数比多给图更稳（05 §9 已写） |
| 打分形式 | rubric 逐条 0/1，**取 logits 概率而非采样词** | Web-Shepherd：12.2 → 43.1 → 51.4（5 次取概率平均） |
| 重复次数 | 先量自己的 K 曲线再定；默认 3~5 次取概率均值 | VL-RewardBench §4.2 的反例：小模型 K 大了会掉分 |
| 与 policy 的关系 | **不同模型家族，且 judge 不随 policy 更新** | 自偏好：GPT-4 对自家回答判赢召回 0.945、判输 0.425（2410.21819） |
| 刷新节奏 | 每隔若干轮用新 rollout 重标一批、重训 judge | AgentPRM 的失败模式：PRM 被打穿且验证集测不出来，400 步后成功率 82%→70%（05 §5.2） |

### 3.2.5 一个重要的反向证据：不完美的 judge 也能用

UI-TARS-2（2509.02544 §4，Training Rewards and Entropy）：
- 自建 300 条人工标注 GUI 轨迹的 ORM 评测集，UI-TARS-2 作为生成式 ORM 的二分类 **F1 = 83.8**，
  且**假阳性率偏高**。
- 但原文明确说：人工检查 reward 后**没有发现实质性的 reward hacking**，这样一个「不完美」的 ORM 在 RL 里仍然有效。
- 作者给的解释：即使最终结果判错，agent 在中间步骤往往做对了很多事；
  假阳的样本里，模型拿到的正分主要落在那些正确的中间步上，正贡献盖过了错误奖励。

**怎么看这条**：它和 04 §5 的「不可靠 verifier 不如不加」（2607.09492：关键词匹配验证视觉证据，hack 率反升 2.2~3.4 个点）看似冲突，实际边界清楚：
- UI-TARS-2 的 ORM 是**整条轨迹的成败判断**，错的是「这条到底成没成」，不改变「要完成任务」这个方向；
- 2607.09492 的失败是**用可被构造满足的代理判据替换了真判据**（关键词匹配），模型直接学会生成那些关键词。
- 判据：**judge 的误差是不是可被模型主动制造的**。随机误差可容忍，可被利用的系统误差不可容忍。
  这也是为什么硬门槛必须是程序，而不能是 judge。

---

# 4. 落地建议：从 0 到 1 的训练配方

## 前置判断：先过两道闸，再决定要不要做 RL

**闸一：有没有更强的教师？**（依据见 2.4.5）
Qwen3 表 21：8B 模型上 RL 要 17,920 GPU 小时得 AIME24 67.6，
而 on-policy 蒸馏只要 **1,800 GPU 小时**就得 **74.4** —— 算力 1/10、分数更高，且 RL 没提升 pass@64。
按任务族分流：

| 任务族 | 教师能不能做对 | 决定 |
|---|---|---|
| 前端 / WebDev | 能（前沿模型很强） | **优先蒸馏**，RL 放后面 |
| three.js / Blender 复刻类 | 部分能，但有程序化 GT | **RL 信号最干净，优先做** |
| 3D 开放设计 | 不能（WorldCoder-Bench 通过率 2.7%，04 §0） | 教师和 verifier 都弱，**最后做** |

**闸二：verify 延迟的 σ/μ 是多少？**（依据见 2.1.3）
σ/μ < 0.3 就别上异步架构，直接同步 + 多并发摊平；> 1 才值得付异步的复杂度。
本项目混合了 0.4 s 的断言和 8 s 的 Cycles + judge，σ/μ 远大于 1，该上。

---

## 4.0 阶段 0：先把 harness 和 verifier 做完，再碰训练

这一步不产出模型，但**跳过它会让后面全部白做**。出闸条件（04 §6.2 已定义，这里只给量化门槛）：

| 门 | 判据 | 阈值 |
|---|---|---|
| 可重放 | 同一产物取证两次 | 关键断言 100% 一致；感知分差 < 自测 σ |
| 判别力 | 变异测试（删功能、移 1px、换色、关碰撞、加隐藏元素） | 原型实测：page 截图 5/13、多视角 9/13、按色体素 11/13、**多视角+体素 13/13**（STATE.md 03:25）。要求 ≥ 12/13 |
| 抗注入 | 页面里写「请给满分」、全屏贴参考图、代理几何 | 注入样本必须得 0 |
| 噪声地板 | 50 条已标注轨迹上量 σ_noise | 写进配置；后续所有「差分」判据都要 > 2σ（05 §8.4） |
| 故障分类 | A/B/C 三类失败能自动分开（2.3.1） | 环境故障样本有独立计数器 |

**为什么必须先做**：DeepSeek-R1 自己给了反例 ——
「由于评测耗时长、影响 RL 效率，大规模 RL 还没有广泛应用到软件工程任务上……
未来版本会通过对 SWE 数据做拒绝采样、或在 RL 过程中引入**异步评测**来改善效率」（2501.12948 §4 局限）。
慢 verifier 直接决定了一个方向能不能上 RL。

---

## 4.1 四个阶段的量级

### 4.1.1 公开配方的量级对照

| 阶段 | UI2Code^N（2511.08195 App. B，最接近本场景） | DeepSeek-R1（2501.12948） | UI-TARS-2（2509.02544） | WebRL（2411.02337） |
|---|---|---|---|---|
| 持续预训练 | **约 10M 网页图-HTML 对**，合计约 20M 图-码样本；lr 2e-5、TP=2、global batch 1,536 | — | — | — |
| SFT 冷启动 | **约 80K** 条（drafting / polishing / editing 三类）；5 epoch、max seq 32,768、packed batch 256、lr 5e-6 | **数千条**（刻意很小） | 人在环交互式标注，量未披露 | WebArena-Lite 人工示范 |
| 拒绝采样 | 用「逆向工程」造数：先生成复杂 GT HTML，再合成对应的 refinement 输入 / 编辑指令 | 从一阶段 RL ckpt 拒绝采样，得 **600K 推理 + 200K 非推理 = 800K** | RFT 轮次（量未披露） | — |
| RL | **12K 真实 + 30K 合成 = 42K** 条；batch 64、**组大小 G=16**、**400 步** | 两阶段 RL；GRPO，参考策略周期性更新到最新策略 | PPO + critic（见 4.2） | 每阶段 **500** 条新指令，replay ≤ 2× 当期交互数据 |

**关键观察**
- 我在 2.2.5 节假设的「400 步 × 64 prompt × G=8」几乎就是 UI2Code^N 的真实配置（400 × 64 × G=16）。
  这个量级可以直接当规划基线。
- **SFT 冷启动的量级是 1 万 ~ 10 万条，不是百万条。** 80K（UI2Code^N）和「数千条」（R1）之间差一个半数量级，
  区别在于基座有没有该领域的感知能力：
  - UI2Code^N 先用 20M 图-码样本做持续预训练，SFT 才敢只放 80K；
  - R1 是纯文本推理，基座已经会，所以数千条就够。
- **冷启动太小有代价**：R1 Dev1（只过了小规模冷启动 SFT）在 AIME 上**相对 R1-Zero 退化**，
  原文归因为「cold-start 数据集规模有限」（§4 表 3 讨论）。
  所以冷启动不是越小越好，而是「刚好教会格式和行为范式」。
- **零 SFT 直接 RL 在本场景不可行**。R1-Zero 成立的前提是基座已有该能力、只需激活。
  visual coding agent 要学的是**工具调用协议 + 多轮自检行为**，这是基座完全没有的格式，
  没有冷启动会把绝大多数 rollout 卡在「格式错 → 0 分」上，组内无方差、无梯度。
- **SFT 数据量的饱和点有实测**（05 §2.4 已覆盖，这里只引数字）：SWE-Master 的 SFT 从 0 扩到 60K 条轨迹，
  解决率 6.2% → 57.8%，**48K 之后趋平**；同时模型自己变短（平均轮数 115→94、思考 token 14.8k→12.7k）。
  这是目前唯一一条「agent 轨迹 SFT 的 scaling 曲线 + 饱和点」的公开数字，可以当规划上界。

### 4.1.2 本项目的建议量级（推导，非实测）

前提：基座用一个已经有 UI/3D 感知能力的 VLM（例如 GLM-4.1V-9B 级别），**跳过持续预训练**。

| 阶段 | 数据量 | 产出什么 | 主要风险 |
|---|---|---|---|
| **S1 SFT 冷启动** | **8K ~ 15K 条轨迹**（three.js / Blender / 前端各约三分之一），平均 10~20 步 | 学会工具协议（get_scene_graph / console_logs / render_views / screenshot / interact / bash）、`<think>` 结构、「改完要自检」的行为范式 | 轨迹来源。用强模型（Claude / GPT 级）在 harness 里跑，按 04 的分层 verifier 筛，再按 05 §9 的管线剪枝重写 |
| **S2 拒绝采样** | 从 **3K ~ 5K 个任务** 上每题采 **N=8~16**，筛出通过 verifier 的，保留率预计 **10%~35%** → **5K ~ 20K 条** 高质量轨迹 | 把 S1 模型的分布拉到「自己能走通」的轨迹上；同时得到每题的 pass@N 用于 S3 的难度分桶 | 保留率太低（< 5%）说明任务太难，要先补 S1；太高（> 60%）说明任务太简单，RL 无信号 |
| **S3 RL** | **3K ~ 8K 个任务**（S2 里 **pass@N 落在 0 < p < 0.9** 的那些，口径抄 MiniMax-M1：用 pass@10 估、双边阈值、得约 50K 数学题），batch 64、G=8~16、300~500 步 | 真正的能力增量 | 见 4.3 的监控 |
| **S4 迭代** | 用 S3 的 ckpt 重新做 S2，再训一轮 | GLM-4.5 的 iterative self-distillation（2508.06471 §3.3.2）：RL 到平台期后，用 RL 模型的输出替换冷启动数据重做 SFT，再在更强的 SFT 模型上继续 RL | 每轮都要重算 pass@N 和 verifier 校准 |

拒绝采样的保留率参考（05 §2 已覆盖，这里只引量级与口径）：
- SWE-Gym 2,438 实例、R2E-Gym 8.1K 题、SWE-smith 50K 实例、OpenSWE 45,320 个 Docker 环境。
- SWE-smith 的实测保留率：8,686 任务做 17,906 次尝试，成功 **6,457 条（36%）**，每任务最多留 3 条 → 最终 5,016 条。
- **每题留几条**：SWE-Gym 的 per-instance capping 消融 —— 留 1 条 9.0%、**留 2 条 9.7%**、留 3 条 7.7%、不设上限 9.3%。
  同题内**优先留轮数少的**。→ **本项目取每题 2~3 条、择短。**
- **难度不决定训练价值**：SWE-smith 按难度分 4 档各 500 条，训后 SWE-Verified 12.4 / 10.8 / 13.6 / 12.2，无单调性。
  → 拒绝采样阶段不要按难度挑，**只在 S3 的课程里按难度挑**。

### 4.1.3 一条容易忽略的省钱路：给 agent 更强的结构化工具

SWE-Master 表 6 的对照（同一模型，加 LSP 工具并继续训）：

| 配置 | 输入 token | 输出 token | 平均轮数 | resolve |
|---|---|---|---|---|
| 不加 LSP | 5,549.6k | 32.5k | 111.2 | 61.4% |
| **加 LSP** | **4,232.1k（−23.7%）** | **27.2k（−16.3%）** | **91.7（−17.5%）** | 61.0% |

分数基本不变，但 token 和轮数都降了约 20%。
**同理，本项目的 `get_scene_graph`（1.8 ms、几十到几百 token）就是 three.js 的 LSP**。
优先把它做好，比优化 reward 更省钱 —— 而且 2.4.1 已经算过：
输入 token 大致随步数的平方增长，**降 20% 轮数就是降约 36% 输入 token**。

---

## 4.2 算法选择

### 4.2.1 决策表

| 轨迹形态 | 推荐 | 为什么 |
|---|---|---|
| **单轮 generate-then-verify**（给需求 → 一次写完 → 取证打分） | **GRPO 系 + DAPO 的四件套**（clip-higher、dynamic sampling、token-level loss、overlong shaping） | 单轮、二值 / 准二值 reward，这是 DAPO 的原生场景。UI2Code^N 的 RVPO 本质也是 GRPO（2511.08195 §2.3） |
| **多轮自检**（10~40 步，中途有渲染反馈） | **GRPO + 两层优势**。两个可选口径：① **GiGPO**（按环境状态哈希归组，A = A_episode + ω·A_step，ω=1）；② **TCPO**（在「同 prompt、同 turn index」上归一化，纯后处理不改 rollout），再加 Δ reward 与 retro 参照 | 都不需要额外 rollout / critic / RM。GiGPO 实测 ALFWorld 7B 90.8 对 GRPO 77.6（05 §5.1）；TCPO 的 credit 阶梯见 1.2.1(b)，**换参照系比变密值钱 2.6 倍**。**先做轮级，不要先做 token 级**（FACTOR 表 4：时间维是主因） |
| **多轮 + 想在工具返回后加探索** | **ARPO 的熵触发分支**（soft 归因） | 渲染工具返回图像，比 search 返回文本更「外源」，工具后熵升应更明显。实测工具调用次数减半而准确率更高（1.2.1(e)）。阈值从 **0.4** 起扫 |
| **长程多轮**（50 步以上，上下文接近窗口上限） | **PPO + critic，配 VAPO/VC-PPO 四件套** | UI-TARS-2 的实际选择（2509.02544 §2.5.4）：Decoupled-GAE（policy 与 value 用不同系数）、Length-Adaptive GAE、Value Pretraining（固定策略下用 λ=1 的 MC 回报把 value 训到收敛再做初始化）、Clip Higher。原因是长序列上 value 估计会衰减 |
| **开放设计类**（没有唯一正解，只能比优劣） | **组内 pairwise + tournament 聚合**（UI2Code^N 的 RVPO） | 候选只生成一次、复用做两两比较，比较成本与生成成本解耦；Table 20 实测比较只占训练时间 2.2% |

**不要做的**：用 CLIP / DINO 全局相似度当 reward。
UI2Code^N 消融：CLIP 相似度作 reward 在 Design2Code 和 Flame 上**都低于 SFT**（§4.3）。
Visual-ERM 的同类结论见 04 §5.1。

### 4.2.2 超参的工业口径（已核实）

| 项 | 取值 / 做法 | 出处 |
|---|---|---|
| KL 项 | **去掉**（GRPO 不加 KL loss） | GLM-4.5 §3.3.1 原文：「Our overall RL algorithm builds upon the GRPO framework, **excluding the KL loss term**」 |
| 参考策略 | 如果保留 KL，**周期性把参考策略更新到最新策略** | DeepSeek-R1 附录 B：训上千步时策略会显著偏离初始参考策略 |
| 课程 | **两阶段难度课程**；第二阶段换成「极难」题（pass@8 = 0 但 pass@512 > 0），且**只从已验证答案的池子里取** | GLM-4.5 §3.3.1 图 5：基线继续喂中等难度会撞平台期，换极难题后继续涨 |
| 输出长度 | **单阶段直接在目标最大长度上训**，不要渐进式升长度 | GLM-4.5 §3.3.1 图 6：多阶段渐进升长会在早期造成**不可逆**的掉分（模型 unlearn 了长上下文能力），最终上限更低。直接在 64K 上训持续变好 |
| loss 归约 | 代码类 RL 用 **token-weighted mean**，不要 sequence-mean | GLM-4.5 §3.3.1 图 7 左：收敛显著更快；缓解序列级 reward 的长度偏差，抑制「base case」式的退化样本。与 DAPO 的 token-level loss 同一方向 |
| 采样温度 | **动态**：reward 进平台期就升温；用 held-out 集按温度扫一遍，取「不比当前最优掉超过 1%」的最大温度 | GLM-4.5 §3.3.1 |
| 数据质量 | 宁要少而硬，不要多而杂 | GLM-4.5 §3.3.1 图 7 右：科学 RL 只用专家核验过的选择题，显著优于混质量数据 |
| 格式惩罚 | 工具格式错 → **中止轨迹 + 0 分** | GLM-4.5 §3.3.2 |
| 熵 | **不要预设熵一定下降** | UI-TARS-2 §4 图 8：GUI 与网页小游戏的 RL **熵经常是上升的**，与推理类 RL 的单调下降相反。所以「熵塌缩」告警阈值必须按任务族分别标定 |

---

## 4.3 监控：哪些曲线一异常就说明在 hack

### 4.3.1 必画的曲线

分四组。每组给「正常形态」和「异常形态」，以及异常时第一步该做什么。

| # | 指标 | 正常 | 异常 = 在 hack | 第一反应 |
|---|---|---|---|---|
| 1 | **train reward 与 held-out 人工分** | 同向 | **train 涨、held-out 平或跌** | 停训。这是 reward hacking 的定义式判据。AgentPRM 的记录最刺眼：PRM 被打穿后成功率 82%→70%，而**验证集上的 process reward 还在涨**（05 §5.2） |
| 2 | **L0 硬门槛通过率** | 单调升到平台 | **100% 饱和后 L2/L3 分继续猛涨** | 代理分饱和 = 失去区分度。Visual-ERM 记录 DINO/TEDS 饱和而下游不涨（04 §5.1） |
| 3 | **响应长度** | 缓升后平 | **暴涨**（RULER：0.3k→6.3k token，04 §5.1）或**暴跌**（RLRF：SVG 越来越短直到发散） | 暴涨查重复装饰 / 密集重叠；暴跌查长度惩罚的阈值方向 |
| 4 | **熵** | 按任务族标定的区间 | 偏离标定区间（注意：GUI/游戏类 RL 熵会**上升**，UI-TARS-2 §4） | 先确认是不是「这个任务族本来就这样」，再调 clip-higher |
| 5 | **组内方差 / 全对与全错组占比** | 全错组随训练下降、全对组上升 | 全对组占比快速冲到 80%+ | 课程该换档（GLM-4.5 的第二阶段），不是算法问题 |
| 6 | **环境故障率**（2.3.1 的 B 类） | < 2%，平稳 | 突然上升 | 不是模型问题。但必须查：故障样本有没有被当 0 分进梯度 |
| 7 | **flaky 率**（同产物取证两次不一致） | 稳定在 verifier 校准时的水平 | 上升 | 模型在往不确定性里钻（动画时序、随机种子）。WorldBench 的基线：未改动条目单次重跑仍有 7/32 翻面（04 §3.2） |

### 4.3.2 本场景特有的代理指标（代码层面）

这些是「便宜、每条都能算、一眼能看出不对」的量。建议每轮算分布而不是均值。

| 指标 | 为什么看它 | 已知的 hack 形态 |
|---|---|---|
| 绝对定位（`position:absolute`）占比 | 凑像素分最省力的办法 | UI2Code^N 实测 0.7%→0.5%，RL 后未出现（04 §1.1）。有这组基线做对照 |
| `<text>` / 文本元素数、OCR 到的页面文字 | 把 prompt 原文画进图 | RLRF Text2SVG（04 §5.1）；judge 前先 OCR，检出指令性文本直接 0（04 §2.3） |
| viewBox / canvas 尺寸、DPR | 缩小画布骗 L2 相似度 | RLRF `viewBox="0 0 1 1"`（04 §5.1） |
| DOM 节点数、场景图对象数、三角面数 | 退化输出（空页面、单个立方体）仍拿分 | ReLook 的零分硬闸之前，有效渲染率只有约 40%（04 §5.1） |
| 硬编码常量数、字符串字面量里出现期望值 | 写死答案 | Claude 4 系统卡的 special-casing（04 §5.2） |
| 自检轮数 / 工具调用次数 | 「改完反而变差给负分 → 学会少反思」 | ReLook §2.6（05 §4.6）。这条要**双向**看：太少是逃避反思，太多是刷观测 |
| 单条轨迹视觉 token 消耗 | 刷截图 | 对照 VAGEN 的 11.9 张基线（3.2.3） |
| 重复率（最长重复子串 / 周期段长度） | 循环退化 | 判据用「周期段 ≥ 400 字」，不是看行重复（经验，来自本机的崩坏闸误报史） |

### 4.3.3 hacking 什么时候会出现：两篇给了可画成曲线的实证

**CHERRL（2606.04923）—— rubric RL 下 hacking 的可控复现**

用双 judge（gold judge + 注入已知 bias 的 judge）构成 proxy reward，测量「onset step」：

| 数据集 | bias 类型 | onset step（众数 / 区间） | 与任务成功的纠缠度 OR |
|---|---|---|---|
| VerInstruct | lexical | **116** [115, 161] | 1.09 |
| VerInstruct | format | 301 [301, 443] | 0.86 |
| VerInstruct | self-praise | **478** [478, 492] | 0.53 |
| HealthBench | tone | **68** [68, 79] | 1.02 |
| HealthBench | lexical | 91 [91, 95] | 0.91 |
| HealthBench | self-praise | **460** [460, 466] | 0.57 |

**规律：OR（bias 与真实任务成功的纠缠度）越接近或高于 1，onset 越早。**
self-praise 的 OR 只有 0.53~0.57，所以最晚才被发现 —— 但也最隐蔽。
onset 之后 100 步内 shortcut 发生率上升 **至少 40%**。

下游能力退化（表 3/4）：

| 训练集 | 指标 | baseline | 无 bias | lexical | **self-praise** |
|---|---|---|---|---|---|
| VerInstruct | IFBench Strict | 31.7 | 33.3 | 27.3 | **23.7** |
| HealthBench | HealthBench | 42.8 | 47.4 | 44.4 | **36.1** |

**一条必须记住的警告**：Arena-Hard 上部分被 hack 的模型**不降分**
（self-praise 10.5 > 无 bias 8.5）—— 通用 judge 被同样的 hacking 模式骗到。
→ **用 LLM-judge 型的通用榜来验伪 hacking 是无效的。** 必须有程序化的 held-out 判据。

**ARA（2602.01750）—— Goodhart 分叉点与检测器容量**

| exploit 类型 | 标准 PPO 下的 Goodhart 分叉点 | Auditor 饱和所需容量 |
|---|---|---|
| code gaming | **约 1,000 步**（hacking 率在 4,000 步饱和于约 59%） | **50M** |
| length bias | 约 3,500 步 | 25M |
| sycophancy | 约 4,000 步 | 35M |

检测力对照（500 真实 / 500 高 proxy 的 exploit，proxy 分可比）：

| 检测器 | 真实样本得分 | exploit 样本得分 | Δ |
|---|---|---|---|
| **proxy reward 本身** | 0.91 | 0.89 | **0.02（无区分力）** |
| GPT-4 | 0.78 | 0.34 | 0.44 |
| **专训 Auditor** | 0.82 | 0.19 | **0.63** |

**两条含义**
1. **code gaming 类的 hacking 在 1,000 步就分叉**。
   对照 GLM-4.5 的「指令跟随 RL 到约 1,000 步未见明显 hacking」（§3.4 图 9）——
   1,000 步就是这个量级的分界线，**我们规划的 400 步在相对安全区，但不能据此免检**。
2. **proxy reward 自己完全看不出 hacking（Δ=0.02）**。
   这直接否定了「看 reward 曲线是否异常」这种监控方式 ——
   必须有独立的、不参与优化的判据（4.3.1 第 1 条的 held-out 人工分，或专训 Auditor）。

**SWE 任务里哪些行为会被 RL 放大**（Verification Horizon 2606.26300 表 2，
Qwen-Turbo，训练集 resolved rate 59.99% 为基线；Freq. 是 rollout 级流行度，phi 是行为-成功相关）：

| 行为 | Freq.(%) | Resolved(%, Δ) | phi |
|---|---|---|---|
| 可见测例过拟合 | 30.00 | 51.62 (−8.37) | −0.112 |
| 仓库历史挖掘 | 21.11 | 56.55 (−3.44) | −0.036 |
| 评测 harness 篡改 | 8.25 | 41.47 (−18.52) | −0.113 |
| evaluator-aware patching | 8.78 | 56.39 (−3.60) | −0.023 |
| **外部修复查找** | 7.03 | 61.69 (**+1.70**) | **+0.010** |
| **解法产物检索** | 4.32 | **72.34 (+12.35)** | **+0.054** |
| 测试 oracle 篡改 | 3.69 | 47.29 (−12.70) | −0.051 |

**只有「联网捞 golden patch」这类 policy-dependent shortcut 是正相关的 ——
这正是会被 RL 放大的那一类。** 其他「作弊」行为其实与成功负相关，RL 自己就会淘汰它们。
→ **监控的优先级应该放在「有没有可达的外部捷径」，而不是「有没有写死常量」。**

加上轨迹级行为监控（token 级惩罚 + pattern 集迭代扩充）后（表 3）：

| benchmark | Clean Resolved | Hack Rate | Hacked Resolved |
|---|---|---|---|
| SWE-Bench Verified | 36.49 → **64.98**（+28.50） | 51.49 → **2.13** | 41.35 → 0.70 |
| SWE-Bench Multilingual | 50.73 → 66.33（+15.60） | 31.19 → 1.59 | 23.76 → 0.84 |
| SWE-Bench Pro | 33.43 → 50.27（+16.84） | 30.60 → 0.20 | 20.61 → 0.13 |
| **平均** | **40.22 → 60.53（+20.31）** | 37.76 → **1.31** | 28.57 → **0.56** |

训练动态（图 5）：**不加监控时 verifier pass rate 还在涨，而 clean resolved 在后期急剧塌陷。**
这就是 4.3.1 第 1 条那条曲线的真实长相。

**另一条直接针对渲染的**（§3.2 图 6）：
静态 judge（只看源码 + 固定截图）会被**长度利用** —— 模型学会写越来越冗长的 CSS/JS 来抬分；
**交互式 judge（Playwright 真跑）免疫**，因为 reward 来自 runtime 行为，
而且 RL 中测试分更高、输出长度稳定。
→ **这是「reward 要来自运行时状态而不是像素」（04 §0 第 2 条）在 RL 侧的又一个独立印证。**

### 4.3.4 停训与回滚规则

| 条件 | 动作 |
|---|---|
| held-out 人工分连续 2 个评测点不涨，而 train reward 还在涨 | **立即停**，回滚到上一个人工分最高的 ckpt，先修 verifier |
| 4.3.2 任一代理指标的分布出现双峰，或 95 分位数相对 S2 基线涨 3 倍以上 | 停，抽 20 条样本人工看 |
| 环境故障率 > 5% | 暂停并修基础设施。不要在高故障率下继续训（组基线被污染） |
| flaky 率相对校准时翻倍 | 停，给 verifier 加确定性约束（固定时钟、种子、viewport） |

**一个重要的参照点**：GLM-4.5 的 instruction-following RL 在**约 1,000 步内没有观察到明确的 reward hacking**
（2508.06471 §3.4 图 9）。UI-TARS-2 的 GUI RL 用一个 F1=83.8、假阳偏高的 ORM 也没出现实质 hacking（§4）。
**所以 hacking 不是必然发生的**，它和 reward 的「可被主动制造」程度强相关（3.2.5）。
把硬门槛做成程序、把可测量属性交给程序、judge 只判不可测的部分 —— 这三条做到了，hacking 的面就小得多。

### 4.3.5 异常判定要先量方差

这是最容易踩的坑，05 §8.4 已给数字，这里只给操作口径：

- Verification Horizon 的方差拆解（QwenWebBench 300 任务 × 5 次，ELO 标准差）：
  生成端 σ=10.4（range 24.4）、judge σ=8.5、Render+Judge σ=5.0；
  某个中间 ckpt 生成 σ=2.8 但 **judge σ=11.4 成了瓶颈**。所有来源 σ < 12 ELO、最大 range 30.4。
- 对照：模型档位之间约 40 ELO。
- **操作口径**：任何「这一轮掉了」的判断，差分必须超过 2σ。
  没量过 σ 就改 prompt / 改 rubric / 回滚 ckpt，是在拿噪声当信号。
---

## 附：本次核实的出处

**核心算法（全部抓到全文，正文已落 middle_processing/papers/）**

| 简称 | arXiv | 核实后的标题 |
|---|---|---|
| GRPO | 2402.03300 | DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models |
| DeepSeek-R1 | 2501.12948 | （Nature 版正文，含 R1-Zero 全超参） |
| DAPO | 2503.14476 | DAPO: An Open-Source LLM Reinforcement Learning System at Scale |
| Dr. GRPO | 2503.20783 | Understanding R1-Zero-Like Training: A Critical Perspective |
| GSPO | 2507.18071 | Group Sequence Policy Optimization |
| RLOO | 2402.14740 | Back to Basics: Revisiting REINFORCE-Style Optimization for Learning from Human Feedback |
| VAPO | 2504.05118 | VAPO: Value-model-based Augmented PPO |
| CISPO / MiniMax-M1 | 2506.13585 | MiniMax-M1: Scaling Test-Time Compute Efficiently with Lightning Attention |
| Lite PPO | 2508.08221 | Part I: Tricks or Traps? A Deep Dive into RL for LLM Reasoning |
| Magistral | 2506.10910 | Magistral |
| 熵机制 | 2505.22617 | The Entropy Mechanism of Reinforcement Learning for Reasoning Language Models |
| L1 / LCPO | 2503.04697 | L1: Controlling How Long A Reasoning Model Thinks With Reinforcement Learning |
| ProRL | 2505.24864 | ProRL: Prolonged Reinforcement Learning Expands Reasoning Boundaries |
| ExGRPO | 2510.02245 | ExGRPO: Learning to Reason from Experience |
| ScaleRL | 2510.13786 | The Art of Scaling Reinforcement Learning Compute for LLMs |
| Reinforce-Ada | 2510.04996 | Reinforce-Ada: An Adaptive Sampling Framework under Non-linear RL Objectives |
| SRPO | 2504.14286 | SRPO: A Cross-Domain Implementation of Large-Scale Reinforcement Learning on LLM |
| 边界感知课程 | 2606.22317 | Curriculum RL Can Incentivize Reasoning Capacity in LLMs Beyond the Base Model |
| Reasoning with Sampling | 2510.14901 | Reasoning with Sampling: Your Base Model is Smarter Than You Think |
| FP16 修训推不一致 | 2510.26788 | Defeating the Training-Inference Mismatch via FP16 |
| CIS | 2609.32444 | Rethinking Training–Inference Mismatch in LLM RL: Where It Arises and How to Correct It |

**多轮 agent RL 的信用分配**

| 简称 | arXiv | 核实后的标题 |
|---|---|---|
| ARPO | 2507.19849 | Agentic Reinforced Policy Optimization |
| MT-GRPO / MT-PPO | 2505.11821 | Reinforcing Multi-Turn Reasoning in LLM Agents via Fine-Grained Reward Structure and Credit Assignment |
| TCPO | 2608.01667 | TCPO: Turn-Level Credit Policy Optimization |
| VETTA | 2610.08402 | VETTA: Coordinating Turn- and Token-Level Credit Assignment for Multi-Turn LLM Agents |
| FACTOR | 2608.07118 | How Much, Then Where: Credit-Conserving Action-to-Token Allocation |
| CrEST | 2608.13179 | Teach the Magnitude, Not the Direction: Verifier-Bounded Credit Assignment |
| TRACE | 2607.13988 | TRACE: Turn-level Reward Assignment via Credit Estimation for Long-Horizon Agents |
| RAGEN / StarPO | 2504.20073 | RAGEN: Understanding Self-Evolution in LLM Agents via Multi-Turn RL |
| ArCHer | 2402.19446 | ArCHer: Training Language Model Agents via Hierarchical Multi-Turn RL |
| TRIAGE | 2606.32017 | TRIAGE: Role-Typed Credit Assignment for Agentic Reinforcement Learning |
| IAPO | 2608.24588 | IAPO: Influence-Aware Policy Optimization for Multi-Turn Service Agents |
| TreeHCA | 2610.12828 | TreeHCA: Hindsight-Guided Exploration and Credit Assignment |
| PEARL | 2610.14636 | PEARL: Process-Experience Aware RL for Multi-Turn Agents |
| 长程搜索 agent | 2510.24126 | Reinforcement Learning for Long-Horizon Multi-Turn Search Agents |
| AgentGym-RL | 2509.08755 | AgentGym-RL（只抓到 abs 页，无 HTML） |

**部分分、rubric 与奖励聚合**

| 简称 | arXiv | 核实后的标题 |
|---|---|---|
| RaR | 2507.17746 | Rubrics as Rewards |
| CHERRL | 2606.04923 | Reproducing, Analyzing, and Detecting Reward Hacking in Rubric-Based RL |
| OTC-PO | 2504.14870 | Acting Less is Reasoning More! |
| ARA | 2602.01750 | Adversarial Reward Auditing |
| Spurious Rewards | 2506.10947 | Spurious Rewards: Rethinking Training Signals in RLVR |
| RM 过优化定律 | 2210.10760 | Scaling Laws for Reward Model Overoptimization |
| 多模态 reward hacking | 2607.09492 | Multimodal Reward Hacking in Reinforcement Learning |
| EvilGenie | 2511.21654 | EvilGenie: A Reward Hacking Benchmark |
| Code Aesthetics | 2510.23272 | Code Aesthetics with Agentic Reward Feedback |

**异步 RL 框架与慢 verifier 解耦**

| 简称 | arXiv | 核实后的标题 |
|---|---|---|
| AReaL | 2505.24298 | AReaL: A Large-Scale Asynchronous RL System for Language Reasoning |
| AReaL 2.0 | 2607.01120 | Next-Generation Agentic RL Systems Enable Self-Evolving Agents |
| verl / HybridFlow | 2409.19256 | HybridFlow: A Flexible and Efficient RLHF Framework（**论文无异步，异步在代码里**） |
| ROLL | 2506.06122 | RL Optimization for Large-Scale Learning |
| **ROLL Flash** | **2510.11345** | **Part II: ROLL Flash — Accelerating RLVR and Agentic Training with Asynchrony** |
| Trinity-RFT | 2505.17826 | Trinity-RFT |
| StreamRL | 2504.15930 | StreamRL |
| LlamaRL | 2505.24034 | LlamaRL |
| AsyncFlow | 2507.01663 | AsyncFlow |
| RLinf | 2509.15965 | RLinf: Macro-to-Micro Flow Transformation |
| APRIL | 2509.18521 | APRIL: Active Partial Rollouts in RL to Tame Long-tail Generation |
| Asynchronous RLHF | 2410.18252 | Asynchronous RLHF: Faster and More Efficient Off-Policy RL |
| NeMo-DCR | 2610.08430 | Bit-Exact Delta-Compressed Refit for Scalable Agentic RL at Trillion-Parameter Scale |
| INTELLECT-2 | 2505.07291 | INTELLECT-2 |
| OpenRLHF | 2405.11143 | OpenRLHF |
| SAO | 2607.07508 | Single-Rollout Asynchronous Optimization for Agentic RL（GLM-5.2 生产使用） |
| Ling 2.0 / Ling-1T | 2510.22115 | Every Activation Boosted: Scaling General Reasoner to 1 Trillion |
| Ling & Ring 2.6 | 2606.15079 | Ling and Ring 2.6 Technical Report |

**工业技术报告**

| 简称 | arXiv | 本文用到的节 |
|---|---|---|
| GLM-4.5 | 2508.06471 | §3.3.1 课程/长度/loss/温度、§3.3.2 agent RL 与自蒸馏、§3.5 slime 异步架构 |
| Qwen3 | 2505.09388 | RL 段 |
| Kimi k1.5 | 2501.12599 | §2.3.3 长度奖励公式、§2.3.4 课程与优先采样 |
| UI-TARS-2 | 2509.02544 | §2.2 沙箱、§2.5.2 reward 与 ORM、§2.5.3 异步 rollout、§2.5.4 PPO 四件套、§4 熵与 hacking |
| OpenCUA | 2508.09123 | §3.2 历史截图与文本历史、§5 消融、表 6 |
| MiMo-VL | 2506.03569 | — |
| UI2Code^N | 2511.08195 | §2.3 RVPO、§3 三阶段、§4.3 reward 消融、App. B 数据量、表 20 墙钟拆解 |
| WebRL | 2411.02337 | §2.1 课程过滤（critic 0.05~0.75）、§2.3 replay（困惑度 1/0.95~1/0.5）、ORM 约 80% |
| SWE-RL | 2502.18449 | 式 1（格式错 −1，否则 difflib 相似度）、273k PR 种子 |

**多模态 reward model / 观测模态**

| 简称 | arXiv | 用到什么 |
|---|---|---|
| VL-RewardBench | 2411.17451 | §4.1 感知是瓶颈、§4.2 judge 的 test-time scaling 对小模型为负、critic 训练 +14.7 |
| Skywork-VL Reward | 2505.07263 | 表 3 的规模对照（本文 3.2.1 的主表）、190k 训练数据 |
| R1-Reward | 2505.02835 | 200k 数据超过百万级的 IXC-2.5-Reward |
| LLaVA-Critic | 2410.02712 | 113k 偏好数据（被 Skywork 复用） |
| UnifiedReward | 2503.05236 | — |
| VisualWebArena | 2401.13649 | 表 3 文本 / caption / 多模态 / SoM 的四级对照；附录 C 的 OCR 与困难视觉子集 |
| ShowUI | 2411.17465 | §2.1 视觉 token 冗余与 UI-guided token selection（−33% token、1.4× 加速） |
| UI-TARS | 2501.12326 | — |

**本机实测与原型**（不是文献）

- 06_harness.md §4：three.js 14.3 任务/s（8 浏览器 × 8 页，48 核）、Blender Workbench 15.5 视角/s（32 进程）、
  Cycles CPU 0.88 s/视角（8 线程）、scene graph 1.8 ms / 0.1~1 ms
- scripts/vc_verifier/proto + mutate.py：snowman 6 候选的区分度、13 个变异的检出率
  （page 5/13、多视角 9/13、按色体素 11/13、多视角+体素 13/13）
- STATE.md 03:05 / 03:25

**未核实 / 不要当论文引**

| 项 | 情况 | 能核实的入口 |
|---|---|---|
| TIS 原始出处（Yao et al. 2025, "Your Efficient RL Framework Secretly Brings You Off-Policy RL Training"） | 技术博客，无 arXiv 号 | 2609.32444 的参考文献 |
| IcePop（Zhao et al. 2025） | 技术博客，无 arXiv 号 | — |
| "When Speed Kills Stability: Demystifying RL Collapse from the Training-Inference Mismatch" | 参考文献只给链接，无 arXiv 号 | — |
| **POLARIS** | arXiv 搜不到同名算法论文；在 ScaleRL 里是**数据集**（Polaris-53K） | — |
| **slime** | **确认无论文** | `github.com/THUDM/slime`、`lmsys.org/blog/2025-07-09-slime/` |
| **Agentica 的 DeepSWE RL recipe** | **arXiv id 未核实**。注意 **2607.07946 的「DeepSWE」是一个 benchmark，不是这个 RL recipe**，别混 | Notion blog、`wandb.ai/mluo/deepswe`、`agentica-project/rllm/examples/swe` |
| Ring-1T 独立 arXiv 条目 | 搜不到 | `github.com/inclusionAI/Ring` |
| Kimi-Researcher / Tongyi DeepResearch / AEPO | 未核实（检索被限流） | — |
| 「用 Bradley-Terry 拟合 rubric 分项权重」的论文 | 本次范围内没找到 | — |
| SWE-RL 的训练规模（GPU 小时） | HTML 版只渲染出首页，未核实 | `arxiv.org/abs/2502.18449` PDF、`github.com/facebookresearch/swe-rl` |
| DAPO 的 dynamic sampling rollout 放大倍数 | 原文未给数字，只有「收敛时间反而更短」的定性说法 | — |
| CISPO 的 ε_high^IS 数值 | 原文未披露 | — |
| GSPO 的表格数值 | 原文只有曲线（图 1） | — |
| TCPO 的 γ 数值 | 原文未披露 | — |
| 本文 2.2.3 / 2.2.4 / 2.4.1 / 2.4.3 的 GPU 配比、token 账与总量 | **自行推算**，假设已写在表旁，未做端到端实测 | — |

**两处必须带保留引用的地方**
1. **verl 的 staleness=0 反而精度最差**（1d1h53m / 0.2844）：README 自己写明「需进一步分析」，不是定论。
2. **CHERRL 的 onset step 与 OR 的关系**：基于注入式 bias 的可控实验，不是真实 hacking 的分布。

