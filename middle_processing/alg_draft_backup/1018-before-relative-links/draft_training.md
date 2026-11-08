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

数据解读：two gates 的顺序不能颠倒，第一道闸问的是教师，第二道才问判据。three.js 复刻这一族两道闸都亮绿灯——判据干净，而且教师非常强，100 道题里 96 道至少有一次做对（[3JSBench 榜单](https://3jsbench.com/) Astra 的 pass@3，核验见 [91 号记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/91_3jsbench_verified.md)）。这种情况下先花算力做 RL 是把便宜的那一步跳过去了：蒸馏能把大部分能力以十分之一的代价搬过来，RL 该留给蒸馏之后仍然做不对的那一部分。

反过来，3D 开放设计这一族两道闸都亮红灯。注意这里的 27.8% 是模型在隐藏运行时契约上的覆盖率，不要和前面 Verifier 视图里那个 2.7% 混淆——那个 2.7% 是「截图加 VLM」这种**判定方式**的通过率（[WorldCoder-Bench 判定范式对照](https://arxiv.org/abs/2606.01869)，核验记录见 [92 号笔记](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/92_number_audit.md)），衡量的是判据坏掉了，不是模型做不出来。

RL 把 reward 的误差当成梯度方向反复放大，所以它只在误差结构最干净的那一格里值得付钱。审美类任务要先拆开再说：靠人判的那一半，reward 噪声来自人本身，用 RL 去优化等于把噪声刻进权重；而可程序化的那一半（排版层级、尺度、间距节奏、色相数、对比度）不经过人，判定本身没有方差，它和可访问性是同一类信号，该在早期就接进去。（人判有多吵：44 名职业 UI 设计师的标注者间一致性，八个维度的 Krippendorff α 宏平均只有 0.368，[AUV-Bench 表 8](https://arxiv.org/abs/2609.34854)。）

第二道闸是延迟的形状，不是延迟的大小。[ROLL Flash](https://arxiv.org/abs/2510.11345) 的模拟很直接（§5.2.1）：环境延迟服从均值 10 秒标准差 10 秒时，环境级异步加速 2.46 倍；均值同样 10 秒而标准差 1 秒，只有 1.16 倍；均值 50 秒标准差 5 秒，也只有 1.20 倍。真实任务同向（图 11），软件工程类 10.22 小时降到 8.32 小时，ALFWorld 13.37 小时降到 8.44 小时。

判据写成一个数（本文给的经验判据，不是文献值）：先量 verify 延迟的标准差与均值之比，小于 0.3 就别上异步，直接同步加多并发摊平。本项目混了约 0.4 秒的 three.js 断言、约 7 秒的 Cycles 终局渲染和 5 到 8 秒的 VLM judge（[本机实测，08 笔记 §2.4.2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/08_rl_recipe.md)），按快慢两类各占一半推算这个比值约 0.9，慢任务占比越小比值越大，远高于 0.3，该上。

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

落到本项目，聚合结构是硬闸相乘、连续分在闸后加权（本项目的设计，不是文献结论）：能执行、画布非空、无运行时报错是第一道乘法闸；核心断言（对象存在、数量、层级）是第二道乘法闸；细节断言、几何相似、rubric 分只在两道闸都过之后进加权，而且几何相似的权重压在 0.3 以内。美学分、全局 CLIP 与 DINO 相似度、任何与 token 数相关的项，一律不进 reward。这套结构的文献依据汇总在 [08 笔记 §1.5.2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/08_rl_recipe.md)。

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

本项目在自己的 16 个修复任务上复现了这条规律，而且把它拆得更细（[本地实验记录 §7](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。283 组有效运行，四种反馈乘两种问题描述，每轮都用同一个 Verifier 判定，模型看不到判定理由。

核心发现：首轮挂掉之后能不能救回来，几乎完全由问题描述里有没有参考图决定，而不是由反馈的精确度决定。

| 问题描述（[本地实验 §7](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)） | 反馈给页面相机一张图 | 反馈给四视角拼图 | 反馈给场景图文本 |
|---|---|---|---|
| 纯文本需求 | 1/14 | 0/12 | 1/11 |
| 文本加参考渲染图 | 4/12 | 6/10 | 1/9 |

数据解读：纯文本描述下三种反馈合计救回 2/37，约 5%；给了参考图之后是 11/31，约 35%。四视角拼图那一格从 0/12 变成 6/10。每格分母只有 9 到 14，单格之间的比较要打折扣，合计那一行才站得住。模型不是不会改，是不知道该改成什么——让它看自己的产物，只有在它手里有一个可比对象时才有用（数据见 [本地实验 §7 与 §7.4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。

还有一条反直觉的：场景图文本是四种反馈里信息最精确的，每个物体的几何类型、世界包围盒、颜色全是数字，而它在两种描述下都是最差的一档。问题描述给的是图，反馈给的是数字，模型要先把图翻译成数字才能比对，而这一步正是它不擅长的。**反馈必须和问题描述在同一个量纲上**，精确度不能替代可比性。

再加一个对照更能说明问题。第五臂只多给一样东西：Verifier 判出的那一层的**名字**，翻译成一句人话，不给阈值也不给数值（[本地实验记录 §7.2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。

| 问题描述（[本地实验 §7.2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)） | 反馈 | 首轮挂后救回 |
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

给 judge 和 policy 的图像预算要分开算。在最便宜的那一档配置下，图像只占一条 40 步轨迹累计输入的 8%，文本历史才是大头；但那一档的前提是图被压得很小。**换成「文字还看得清」的配置，图像占比升到 16% 到 36%。**（三个数都是本项目推算，[20 号笔记 §3](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/20_base_model.md)。）所以「图像不是上下文爆炸的主因」这句话只在不要求可读性时成立。

这里藏着整节最该记住的一个陷阱。

核心发现：整页长截图在 Claude 标准档计费下**比小图还便宜**，因为它被压得谁也看不清，而账单上看不出任何异常。

| 做法（按 [Claude 视觉文档](https://platform.claude.com/docs/en/build-with-claude/vision) 的公式与上限推算，标准档） | 视觉 token | 宽度保真 |
|---|---|---|
| 1440 宽、900 高的一屏 | 约 1,550 | 高 |
| 1440 宽、8000 高的整页长图 | 约 616 | 约 20%，被压到 282 像素宽 |
| 同一张长图切成 9 片 | 约 13,950 | 约 96% |

数据解读：最自然的做法——把整页截下来丢进去——既最便宜又完全看不清，而且它不会报错、不会超限、账单还更好看。**这类失败在监控上是隐形的**，只有去看模型实际收到的那张图才能发现。要文字可读就得切片，代价是 token 涨 22 倍。算式已用官方文档给的样例校验，见 [20 号笔记 §3.1](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/20_base_model.md)。

所以预算优先级是：先设历史滑窗，再定分辨率与切片策略，最后才考虑换成文本。滑窗取 3 张有实测依据：[OpenCUA](https://arxiv.org/abs/2508.09123) 的消融里，从 3 张加到 5 张只有边际收益，却多约 3K token 并拖慢收敛（图 10 与正文）。

顺带纠正一个容易用错的口径：「多视角拼图比分开发图省 8 倍」不是同口径比较——那两个数字的像素量本身就差 12 倍。**同像素下拼图只省约 12%**（本项目推算，[20 号笔记](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/20_base_model.md)）。想真正省 token 只有降分辨率一条路，而降分辨率直接伤可读性。

<a class="anchor" id="tr-6"></a>

## 6 Hacking Does Not Show Up in the Reward Curve

看 reward 曲线找 hacking 是无效的。[ARA](https://arxiv.org/abs/2602.01750) 在 500 条真实样本与 500 条高 proxy 的 exploit 样本上测检测力（表 2）：proxy reward 自己给出 0.91 对 0.89，差 0.02，没有区分力；GPT-4 作检测器 0.78 对 0.34，差 0.44；专训的 Auditor 0.82 对 0.19，差 0.63。proxy 不可能检出自己的漏洞，这是定义决定的。

还有一条更麻烦的：通用 LLM judge 榜也验不出来。[CHERRL](https://arxiv.org/abs/2606.04923) 实测里，部分遭 hack 的模型在 Arena-Hard 上不降分，self-praise 偏置的 10.5 还高于无偏置的 8.5（表 3）——同样的 hacking 模式把通用 judge 一起骗了。

但「用程序化的 held-out 判据来验」这句话有一个前提，很容易漏掉：**held-out 判据不能和训练判据同源。** 如果 held-out 只是换了题、判据仍是同一套分层 Verifier，那么 Verifier 的盲区会让训练分和 held-out 分一起涨，第一条告警结构性失效。本项目的设计现在正好踩在这个坑上。

修法不贵：held-out 里必须至少含一路与程序化信号盲区互补的判据，并且单独报它的曲线。最便宜的选择是多模型 VLM 投票——本项目已经量过两者的盲区是互补的（[本地实验记录 §3.3 与 §3.4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）：VLM 擅长「有没有这个东西」，程序化信号擅长「这个东西的尺寸对不对」，4 模型 8 票投票在 48 例里漏掉的几例全是定量几何偏差，而程序化信号漏掉的那一例（车床体顶部的洞）靠 VLM 抓回来。两路曲线同时涨才算真涨。

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

阶段 0 不产出模型，但跳过它后面全部白做。出闸条件：同一产物取证两次关键断言 100% 一致；变异测试判别力不低于 12/13（本项目原型多视角加体素做到 13/13，[本地实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）；注入样本一律得 0；在 50 条已标注轨迹上量出噪声地板并写进配置；三类终止原因能自动分开且环境故障有独立计数器。

核心发现：四个阶段的量级可以从公开配方反推，而且冷启动的量级是万条级别，不是百万级别。下表是本文的规划，不是实测。

| 阶段（规划，推导见 [08 笔记 §4.1.2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/08_rl_recipe.md)） | 数据量级 | 算法选择 | 监控指标 | 验收标准 |
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

所以正确的做法不是直接把 S1 加到 48K，而是先用一次多臂实验把这三件事的边际增益量出来：15K 加 RL、48K 不加 RL、48K 加推理时选择、48K 加 RL 加推理时选择。在它出结果之前，S3 的预算都是拍的。这个四臂设计来自 [18 号红队记录 §3](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/18_redteam.md)。

需要注意口径：上面这组数字来自软件工程任务，不是 visual coding。可迁移的是结构——有一个靠谱的验证器时，推理时选择是比 RL 便宜得多的杠杆；不可直接迁移的是具体幅度。零 SFT 直接上 RL 在本场景不可行（本文判断）——要学的是工具调用协议加多轮自检行为，基座完全没有这个格式，绝大多数 rollout 会卡在格式错得 0 分，组内无方差。每题留几条也有实测（[SWE-Gym 表 6](https://arxiv.org/abs/2412.21139)，7B，SWE-bench Lite）：留 1 条 9.0%、留 2 条 9.7%、留 3 条 7.7%、不设上限 9.3%，同题内优先留轮数少的。

停训与回滚规则只有四条，但要写死在流程里（本文规则，推导见 [08 笔记 §4.3.4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/08_rl_recipe.md)）。held-out 人工分连续两个评测点不涨而 train reward 还在涨，立即停并回滚到人工分最高的 ckpt，先修 Verifier。任一代理指标的分布出现双峰，或 95 分位数相对 S2 基线涨 3 倍以上，停下抽 20 条人工看。环境故障率超过 5%，暂停修基础设施，不要在高故障率下继续训，因为组基线遭污染之后差答案也能拿到正优势。取证 flaky 率相对校准时翻倍，停下给 Verifier 加确定性约束。

成本要先算清，再决定 rollout 形态。下面一组全部是推算，不是实测，假设写在表后，算式见 [08 笔记 §2.2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/08_rl_recipe.md)。

| 形态（推算，[08 笔记 §2.2.2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/08_rl_recipe.md)） | 1024 并发 rollout 的渲染 CPU | 折 48 核机器 |
|---|---|---|
| 多轮 three.js | 43 核 | 0.9 台 |
| 多轮 Blender（自检走 Workbench，终局走 Cycles） | 365 核 | 7.6 台 |
| 单轮 three.js | 129 核 | 2.7 台 |
| 单轮 Blender | 1,670 核 | 34.9 台 |

数据解读：多轮形态下渲染池几乎免费，因为轨迹墙钟遭解码占满，渲染只占百分之几；单轮形态把墙钟从 1200 秒压到 80 秒而取证成本不变，单位成本涨 15 倍，这时才需要独立渲染集群（推算见 [08 笔记 §2.2.2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/08_rl_recipe.md)）。假设有五条：每条轨迹 40 个模型步、其中 12 步带渲染自检、终局取证重复 3 次测 flaky、轨迹墙钟 1200 秒（单序列约 25 token 每秒）、单位成本取本机 48 核配额下的实测吞吐（three.js 一次完整取证 3.35 核秒，Blender Workbench 一个视角 3.09 核秒，Cycles 一个视角 7.04 核秒）。常驻 worker 能省掉每进程约 1 秒的启动与加载，这里不扣，算保守。

一轮 RL 的总量同样是推算，而且这里有一个容易漏掉的放大项：动态采样会把「全对或全错」的组丢掉重采，通过率落在 5% 到 10% 这一段时，组大小 8 下实际要采的轨迹是名义值的 1.76 到 2.97 倍（即 1 除以非零梯度组的比例）。先给名义值：400 个优化步乘 64 个 prompt 乘组大小 8，等于 204,800 条轨迹；乘上重采放大之后是 36 万到 61 万条，对应 2.2 万到 3.8 万 GPU 小时——**比它自己引作参照的 Qwen3 纯 RL 的 17,920 小时还高**（[Qwen3 表 21](https://arxiv.org/abs/2505.09388)）。规划预算时要按放大后的数算。渲染 CPU 折 2.5 机日（多轮 three.js）到 21 机日（多轮 Blender）；GPU 按 64 张做 rollout 加 64 张做训练算，名义上约 12,800 GPU 小时，计入重采放大后是 2.2 万到 3.8 万。渲染型 Verifier 不改变成本量级，改变的是工程复杂度。这里的 GPU 假设是一个 30B 量级的 MoE 在 8 卡上服务约 128 条并发序列，本机未实测。

异步解耦的参数也要定死。staleness 取 1 到 2 代，不要贪：[AReaL](https://arxiv.org/abs/2505.24298) 实测吞吐从 27.1k 涨到 47.8k token 每秒，76% 的提升在第一代就拿到了，再加到 16 代只多 9%（表 7）；而精度风险是超线性的——不开解耦 PPO 时，staleness 4 把 AIME24 从 42.0 砍到 23.3，近乎腰斩（表 2）。各家默认值独立印证这个区间：[ROLL Flash](https://arxiv.org/abs/2510.11345) 取 2（Takeaway 3），[NeMo-RL](https://github.com/NVIDIA-NeMo/RL/blob/main/docs/guides/async-grpo.md) 默认 1，[verl](https://github.com/verl-project/verl/blob/main/docs/advance/fully_async.md) 建议小于 1（它的口径是陈旧样本比例，不是代数）。

配方之外，还有四件事要按顺序做。一是把前端、复刻、开放设计三族分开立项，前端那族先只做蒸馏对照，用它量出「判定模糊的任务族上 RL 到底亏多少」，目前这个判断只有 Qwen3 一组跨域数字支撑。二是在真实 rollout 上量每一层 Verifier 的触发分布与假阳率，现在的判别力全部来自我们自己构造的单处改动变异。三是把前一节的七条告警接成自动化，阈值先在 S2 的拒绝采样数据上校一遍基线，因为 [CHERRL](https://arxiv.org/abs/2606.04923) 里 onset 之后的窗口只有约 100 步，靠人看曲线来不及。四是先训一个专用的小 reward model 再开 S3，它既省 judge 侧的推理卡，也是压低 judge 噪声的直接手段（单次 judge 的标准差可到 11.4 ELO，[Verification Horizon](https://arxiv.org/abs/2606.26300)）。

<a class="anchor" id="tr-8"></a>

## 8 What the Base Model Has to Have

前面七节都在讲数据和训法，但有一件事没定：用什么底座。visual coding 对底座的要求和纯文本编码不一样，而且公开证据足够把几个旋钮的优先级排出来。各条的原始表号汇总在 [20 号笔记](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/20_base_model.md)。

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

但场景图单独用会欠载：只给结构图 13.6%、只给视觉 45.7%、两者一起 63.5%（[GraphEQA 表 2](https://arxiv.org/abs/2412.14480)）。颜色这类属性在转译中会丢（[DePlot](https://arxiv.org/abs/2212.10505)）。**两路必须交叉核对**，这和本文量到的「按几何类名断言，29 个变异只判对 14 个」是同一个病（[本地实验记录 §2.1](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。

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

**一个可执行的起点配置**（推断，不是实测，推导见 [20 笔记 §6.2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/20_base_model.md)）：9B 量级的原生分辨率多模态稠密底座，像素面积预算放到八百万以上，文本上下文 64K；当前视口给一张 1440 宽的截图，历史只留三张低分辨率；单条轨迹的视觉 token 设上限；场景图走摘要而不是转储，并与视觉通道交叉核对。

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

本项目内部记录（KML 网关 /view 链接，非公开）：[90 本地实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)、[92 数字核验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/92_number_audit.md)、[08 RL 配方笔记](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/08_rl_recipe.md)、[20 基座笔记](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/20_base_model.md)、[91 3JSBench 核验](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/91_3jsbench_verified.md)、[18 红队记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/18_redteam.md)。

