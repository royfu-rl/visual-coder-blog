# 13 把可验证任务从几十个扩到十万量级

**范围**：只做**规模化**角度的增量。任务来源盘点见 `02_task_sources.md`，构造范式见 `03_verifiable_construction.md`，
单任务闭环的实测见 `90_local_experiments.md` 与 `10_blender_tasks.md`，这里不重复。

**日期约定**：arXiv 日期按 ID 前四位 YYMM 推断（如 2306.09310 → 2023-06）。**这是假设**，不是论文自报日期。
所有数字标注来源；标【实测】的是本机或接口实际返回，标【估】的是外推。

---

## 0 结论先行

### 0.1 十条

| # | 结论 | 最硬的那个数字 |
|---|---|---|
| 1 | **「组合空间有多大」是零信息量的多样性陈述。** 要验收必须用有效多样性（Hill number 的 q=1，即 Vendi Score），并同时报 D_0/D_1 的折损倍数 | 本机槽位表算术：组合空间 **7.0e8**，渲染后可被 verifier 分开的等价类约 **1.6 万**，**折损 4.4 万倍**。公开对照：Stacked-MNIST 模式计数满分 1000 而 VS 只有 746.7 |
| 2 | **「场景多」不等于「数据好」，这件事在具身领域已被实证打穿。** 所以扩产必须盯有效多样性，不是条数 | HSSD-200：**122 个场景打过 ProcTHOR 的 10,000 个**（HM3DSem 零样本 19% vs 17%）；ProcTHOR 自己从 122 扩到 10,000（**82 倍**）微调后零增益甚至退化 |
| 3 | **「只交付目标、不交付参考解、verifier 验最终状态」有直接文献；「不交付生成器源码以防拟合代码风格」没有，那是推论** | RST 原文「cannot access the reference solution or private verifier」+「checks task outcomes rather than a fixed command sequence」；反之生成器源码那条只有 Infinigen 对静态资产库「easier to overfit」的类比 |
| 4 | **我们缺一条准入闸：verifier 在初始状态必须判挂。** 本机三条准入（参考必过 / 破坏必挂 / search 唯一）里没有它 | FACET 判据 ii「the verifier **does not pass in the initial state**」+ negative discrimination「partial solutions must fail」 |
| 5 | **难度标定不要追求连续分。** 粗闸 n=8 够用，连续档在 n=64 下桶边界误分率仍有 15%~23%，且几乎不随 n 下降 | 本机精确枚举：真 p=0.35 时三档桶误分率 n=8 为 45.3%、n=64 仍 **22.5%**。公开对照：n=16 的难度集合复现性只有 **0.727**，要 0.90 得 **242 次** |
| 6 | **带状过滤必须对称、必须在线。** 单边切和离线做都是负收益 | 只剔全对全错值 **+1.0 pp**，再收紧到 (0.3,0.7) 多拿 **+2.8 pp**；而 skewed 单边切**全部低于 plain GRPO**；AdaRFT 的离线 10%~90% 过滤**六个设置全输、4/6 比不过滤还慢** |
| 7 | **「难」和「坏」必须两套闸。** 当前主流 benchmark 上模型失败里过半是题坏不是能力差 | OpenAI 自己审计 SWE-bench Verified 失败题：**≥59.4%** 的测试会拒掉功能正确解。Platinum 的 benchmark 归因占比**横跨 0%~93%** |
| 8 | **判「题坏」优先用响应模式统计，不要用人工标注。** 人判「这题欠规约吗」的一致性低到不可用 | Krippendorff **α = 0.24**（对照：判「多难」是 Fleiss kappa 0.78）。而 item-total 相关 flag-50 的 precision 最高 **84%**，1,000 题只要 **1 分钟** |
| 9 | **十万量级的去重是免费的，所以没有理由做糙。** 但也不要做过头 | 10 万 × 768 维全对全余弦 = **15.36 TFLOP ≈ 0.14 秒**（A100 TF32）；embedding 推理 **1.25 GPU 小时**。反面：FineWeb 全局去重把 20T 砍到 4T，下游**几乎没提升** |
| 10 | **成本瓶颈不是算力，是 LLM 调用和人工；而 LLM 调用的 65% 花在难度标定上** | 两条线合计约 **2,500 core-h**（一台 48 核机器两天）；LLM 约 **0.95 M 次**；人工约 **360 人时** |

### 0.2 产能的真实量级（这是最该先对齐的预期）

| 路线 | 端到端留存率 | 10 万任务需要的输入 | 性质 |
|---|---|---|---|
| **程序化生成 + 自动破坏** | **约 37%**（本机准入实测 88~96%，其余是去重 / 可解性 / 难度带的外推） | 26.9 万候选 | **主力产能** |
| **真实素材挖掘（three.js）** | **约 3.2%**【估】 | 2,401 个仓库 × 约 3 页/仓 ⇒ 只能出**约 230 个任务** | **多样性注入，不是产能** |
| 公开对照：真实挖矿的文献带宽 | SWE-bench 2.46% / SWE-rebench 4.74% / SWE-Gym 3.77% / Design2Code 0.38% / ShaderMatch 0.23% | — | **0.2%~5% 是经验上限** |
| 公开对照：合成 / 变异 | SWE-smith **50.1%** / BlenderLLM 16% / WorldCoder-Bench ≲20% | — | 合成把 yield 抬约 20 倍 |

**⇒ 配比问题在我们这里不是选择题：真实素材客观上只能占 0.2% 量级的条数。**
所以它的 KPI 应该是「在 Vendi Score 口径下贡献 ≥ 20% 的有效多样性」，而不是条数。

### 0.3 最该先钉死的一个数

**§5.2 漏斗里「难度带筛选留存 0.60」这条外推是整个成本模型最敏感的一项。**

- 如果实际是 0.30，候选数直接从 26.9 万翻到 53.8 万，LLM 调用从 0.95 M 翻到 1.9 M。
- 而公开实测说这条**很可能偏乐观**：Skywork-OR1 实测**开训前就有 54%（7B）/ 63%（32B）的题是 0/N 或 N/N**；
  GRESO 实测训练中有效 prompt 比例会掉到**约 20%**。
- 理论上界（题库 pass rate 服从 U(0,1) 时 G=16 只丢 11.8%）与实测 5× 过采样的差距，
  正是「pass rate 极度堆在两端」的量化体现。

**所以 S0/S1 阶段（§6）必须在 200~2,000 个任务的小规模上先把这个数测出来，再定产能规划。**

### 0.4 一个统一骨架：三件事都是 p(1−p)

```
伯努利方差 p(1−p) 同时是：
  ① RL 学习信号的上界      策略改进下界 ∝ p(1−p)；group 内 (1/N)ΣA_i² = p(1−p)
  ② 题目的 Fisher 信息      IRT：I_i(θ) = a_i²·P_i(1−P_i)，在 P=0.5 最大
  ③ 难度估计本身的方差      p̂ 的方差 = p(1−p)/n
```

**①② 说「要挑 p ≈ 0.5 的题」，③ 说「p ≈ 0.5 的题最难挑准」。**
这个张力解释了本文几乎所有工程折中：为什么用软权重不用硬阈值、
为什么粗闸比细分桶划算、为什么「最能区分模型的题」和「最能提供梯度的题」是同一批题。

---

## 1. 程序化场景生成器怎么保证多样性不塌缩

### 1.1 已有工作：各自的规模、多样性度量方式、成本

日期按 arXiv ID 前四位 YYMM 推断（如 2306.09310 → 2023-06），这是假设，不是论文自报日期。

| 工作 | 规模口径 | **多样性是怎么论证的** | 成本（论文原文数字） |
|---|---|---|---|
| **Infinigen Nature** [2306.09310](https://arxiv.org/html/2306.09310v2) | **182 个生成器 / 1070 个可解释自由度**，代码 40,485 行；Table 1 自标 `#Scenes = ∞ / #Assets = ∞ / External Asset Source = None` | **只有参数自由度计数**（论文自称 "a proxy of overall diversity"）。**没有做任何 coverage / FID / 最近邻距离 / pairwise 相似度** | **一对 1080p 立体图平均 3.5 小时墙钟**（其中约 1 小时 GPU），内存约 24 GB，场景 16M 三角面，Cycles 10,000 spp。CPU-hours 只在直方图里，**正文无数值** |
| **Infinigen-Indoors** [2406.11824](https://arxiv.org/html/2406.11824v1) | 79 个物体生成器 / 741 个参数 + 30 个材质生成器 / 120 参数 | 唯一的覆盖率数字：**材质覆盖 OpenSurfaces 类别的 78%**（Infinigen Nature 只有 21%）。布局质量靠 AMT 人评（Mean Error Freq 0.175，最好） | 求解器消融：全优化版约 3× 加速、等时长下 score +28%。**每场景 CPU 小时 / 墙钟 / 内存未报告** |
| **ProcTHOR** [2206.06994](https://arxiv.org/html/2206.06994v1) | 16 个 room spec、1,633 资产 / 108 类型、18 个语义资产组；**「over 100 billion layouts」「roughly 20 million unique asset groups」** | **纯组合计数 + 分布直方图，零多样性度量** | 生成 10K 房屋 **1 小时**（4×RTX A5000，≈0.36 秒/屋）。对照：ArchitecTHOR 的 10 栋人工房屋约 **320 人·小时** |
| **HSSD-200** [2306.11290](https://arxiv.org/html/2306.11290v1) | 211 场景 / 18,656 资产 / 466 类别；**实例/场景 329.7**（ProcTHOR 74.7，高 4.4 倍） | **把「真实度」和「多样性」分开量化**：FID→HM3D 88.2（ProcTHOR 104.0）、类别共现聚类 Jaccard **0.40（ProcTHOR 0.14）** | — |
| **BlenderProc** [1911.01911](https://arxiv.org/html/1911.01911v1) | **不自带资产库、不做程序化几何**，只做「已有资产的摆放 + 采样」；2020 年支持 15 个数据集 loader | 无多样性度量；只有 sim2real 下游数字 | 渲染约 **3,000 张/小时（单 GPU）**；2020 年口径 **&lt;2 秒/图**（两套口径不同场景，不能混算） |
| **Kubric** [2203.03570](https://arxiv.org/html/2203.03570v1) | 13 个挑战（Conclusion 里却写 11，**论文自相矛盾**）；资产 ShapeNetCore.v2 51,300 + GSO 约 1k | **无任何定量多样性度量**。只有 MOVi-A→E 的复杂度阶梯 + test split 用完全留出的物体与背景 | 全文**唯一**算力数字：光流数据集约需 **3 CPU-years**；ShapeNet 预处理 16 小时 @ 80 核。总视频数/总 TB/成本**未给** |
| **ATISS** [2110.03675](https://arxiv.org/abs/2110.03675) | 3D-FRONT 6,813 房屋 / 约 14,629 房间 | FID / SCA / CKL；Fig.5 "Scene Diversity" **纯定性**；有「最近训练场景」对照图（防记忆意识） | 单场景生成 **102 ms**（FastSynth 13,194 ms） |
| **Holodeck** [2312.09067](https://arxiv.org/abs/2312.09067) | 51,464 标注资产、236 材质 × 148 色 | 只有定性变体图 + 人评（680 名研究生配对投票，Overall Preference 64.4%） | **3+3k 次 API 调用**（k 个房间）；约 **0.2 美元/房间**；M1 MacBook 约 3 分钟/房间 |
| **PhyScene** [2404.09465](https://arxiv.org/abs/2404.09465) | 自称「提供无限场景」 | 只有 FID/KID/CKL，**未区分组合容量与有效多样性**；但把**可行性**量化得最细（Col_obj / Col_scene / R_out / R_reach / R_walkable） | — |
| **3D-GPT** [2310.12945](https://arxiv.org/abs/2310.12945) | 驱动 Infinigen 的参数空间 | **唯一给出多样性数字的一篇**：Parameter Diversity（类别 Shannon 指数）**6.32 → 7.34**，Failure Rate 3.6% → 0.8% | — |
| **SceneCraft** [2403.01248](https://arxiv.org/abs/2403.01248) | 40 条人工 query（20 建库 / 20 测试） | 无多样性指标；但消融极干净：**去掉内循环 Constraint Score 掉 38.4**（88.9 → 26.1），去掉关系图崩到 3.2 | — |

**三条可以直接拿走的判断**：

1. **「规模数字」几乎全是组合计数，不是多样性。** 182 个生成器、1000 亿 layout、∞ scenes 都是容量陈述。
   7 篇场景图采样工作里**只有 3D-GPT 一家给了多样性数字**。
2. **ProcTHOR 自己的消融就打穿了组合计数**：房屋数 10 → 100 → 1,000 → 10,000 时，
   HM3D 零样本成功率是 **1.60% → 10.4% → 4.65% → 9.70%**，**非单调**（1,000 房比 100 房更差）。
3. **HSSD-200 给出了最硬的反例**：**122 个场景打过 ProcTHOR 的 10,000 个场景**
   （HM3DSem 零样本成功率 19% vs 17%），而 ProcTHOR 自己从 122 扩到 10,000（**82 倍**）
   微调后几乎零增益（46/21 → 45/21，甚至退化）。论文原话：
   「scale helps in generalization, but the benefits **quickly saturate**」。

### 1.2 「生成器只出目标场景、不出参考代码」这条原则

**这条原则要拆成两半，因为两半的证据强度完全不同。**

#### A 半：只交付目标与初始状态、参考解对求解者不可见、verifier 验最终状态 —— 有直接文献

| 工作 | 原文判据 |
|---|---|
| **RST** [2608.05466](https://arxiv.org/html/2608.05466v3) | 「it **cannot access the reference solution or private verifier**. After the interaction ends, Harbor runs the verifier **on the final workspace state**. The verifier **checks task outcomes rather than a fixed command sequence**, allowing different valid solutions to receive credit.」 |
| **SKT** [2608.02287](https://arxiv.org/html/2608.02287v2) | 三道闸：① 规则闸「**Visible task materials do not copy reference values or required skill rules verbatim**」；② Agent 语义闸「solver-visible materials … **do not semantically reveal the hidden answer, evaluation logic, or decisive skill-derived requirements**」；③ 配对 rollout（给 skill / 不给 skill 打两份分，看分差） |
| **FACET** [2608.18580](https://arxiv.org/html/2608.18580v1) | 四条验证判据：环境能建起来、**verifier 在初始状态必须不过**、参考解从干净初态能跑通、verifier 在终态过；另加 negative discrimination「**incomplete or partial solutions must fail the verifier**」 |

**RST 还把「泄露」做成了可测量的指标**，这是最值得抄的工程实践：

| 指标 | R1 → R15 |
|---|---|
| hidden-check protection（隐藏检查受保护比例） | 38.2% → **63.5%** |
| short-instruction risk（指令太短导致 verifier 要求无法推断） | 41.6% → **7.5%** |
| 指令里提到私有测试 | → **0.1%** |
| **literal leakage（字面泄露）** | → **0%** |
| median requirement coverage | 0.42 → 0.57 |
| weakly grounded tasks | 32.8% → **1.2%** |

规模与成本：639 个种子任务 → 15 轮产出 **37,484 个已验证终端任务，约 0.05 美元/通过任务**，全程无人工创作；
论文给的人工对照是「hundreds to thousands of 美元 per task」。

**这条原则在本机也有独立实测支持**：10_blender_tasks.md §2.1 里的 `cube_size2`
——换一条实现路径、世界几何逐点相同的改写，**几何信号全部放行（分部件 F-score 0.9993），
只有按代码比的 A2/A3 会误杀**。也就是说「验状态不验代码」不是美学偏好，是本机可复现的必要条件。

#### B 半：不交付生成器源码，以防模型拟合生成器的代码风格 —— **未找到直接文献**

两轮扩展检索没有找到任何论文明确主张这一点，也没有任何论文做过这种消融。
最接近的间接证据按强度排：

| 强度 | 证据 | 要点 |
|---|---|---|
| 1 | **Infinigen 的反向论证** | 「Most synthetic datasets are constructed by using a static library of 3D assets… The downside of a static library is that the synthetic data would be **easier to overfit**.」—— 但针对的是**资产库**，不是代码风格 |
| 1b | **Infinigen 自身的做法与此原则相反** | 它把全部程序化代码 BSD 开源，并把「Provides Procedural Code」列为 Table 1 的**优点列**，完全没讨论发布生成器的风险 |
| 2 | **Procgen 的关卡过拟合实证** [1912.01588](https://ar5iv.arxiv.org/html/1912.01588) | 「agents **strongly overfit to small training sets** in almost all cases. To close the generalization gap, agents need access to **as many as 10,000 levels**.」固定关卡序列时「agents … **learned almost nothing** about the underlying level distribution」，但「giving an **illusion of meaningful progress**」 |
| 3 | FACET 的 trivial bypass 排除 | 58 个候选在验证前被排除，理由含「workflows that permit **trivial bypasses**」 |
| 4 | Shortcut Learning [2004.07780](https://arxiv.org/abs/2004.07780) | 「decision rules that perform well on standard benchmarks but **fail to transfer**」——总论框架，未涉及程序化生成器 |

**所以这条原则该这样写**：
「只交付目标、不交付参考解、verifier 验最终状态」有直接文献（RST / SKT / FACET）；
「不交付生成器源码以防拟合生成器代码风格」**目前是推论**，依据是 Infinigen 对静态资产库「easier to overfit」的论断
加 Procgen 关于需要约 10,000 个关卡才能闭合泛化 gap 的实证。**不要把它写成已验证的结论。**

#### 实现方式（本机口径）

```
生成器产出三样，第四样不产出：
  ✅ 目标场景（.blend / 场景图 / 9 视角参考渲染）
  ✅ spec.json（被钉死的槽位 → 断言族 + 字段路径 + 容差）
  ✅ 题干（槽位短语拼接，或 LLM 改写）
  ❌ 参考代码不进 problem statement，只用于：
       - 跑准入测试①（参考解自比自必须过 verifier）
       - 跑 FACET 式判据②（verifier 在初始状态必须不过）
       - 难度标定的上界参照
```

一个必须补的闸（FACET 的判据 ii）：**verifier 在初始状态必须判挂**。
本机 gen_tasks.py 目前只有「参考必过 + 破坏必挂 + search 唯一」三条，
**缺「初始状态必不过」这一条** —— 如果起始场景恰好已经满足 spec，这个任务就是免费分，
进了 RL 就是纯噪声（而且是 DAPO 会过滤掉的那种全对组，白烧采样）。

### 1.3 组合爆炸 vs 有效多样性：怎么量化

#### 1.3.1 这个区分最早、最明确的出处

**Smith & Whitehead, "Analyzing the Expressive Range of a Level Generator", PCGames 2010**
（[pcgworkshop.com/archive/smith2010analyzing.pdf](https://www.pcgworkshop.com/archive/smith2010analyzing.pdf)，非 arXiv）。原文：

> a generator that can create **tens of thousands of levels** in a matter of minutes is **useless if many of those levels are effectively identical to each other**.

它的量化方法（Expressive Range Analysis，四步）直接可搬：

1. 选度量 —— **必须是产物的全局、涌现属性，不能直接用生成器的输入参数**（这一条最容易违反）；
2. 大量运行生成器采样打分（论文用 **10,000 个关卡**）；
3. 用 **2D 直方图 / 六边形分箱**画生成空间，看「峰」（常见内容）与「洞」（生成空间缺口）；
4. 比较不同参数设置下的图差异。

论文最有价值的一条自述：它靠这个分析发现生成空间严重偏向线性关卡，
真因是「**某组件被选中后再次出现的概率会略微提高**」这个**后期加入的小实现细节** ——
作者说若不做这种分析**永远发现不了**。

#### 1.3.2 定量定义：Hill number 的 q=0 vs q=1

这是目前唯一干净的定量答案（[2310.12952](https://arxiv.org/html/2310.12952v1)）：

| 阶 q | 量 | 含义 |
|---|---|---|
| **q = 0** | D_0 = 支撑集大小 | **就是「组合计数」**；论文直接称之为 *an uninformative measure of diversity* |
| **q = 1** | D_1 = exp(Shannon 熵) = **Vendi Score** | **有效独特元素数**（effective number of unique elements） |
| q → ∞ | 只由最大特征值决定 | 论文建议用它测**重复 / 记忆化** |

**所以「组合空间 / 有效多样性」的折损倍数就是 D_0 / D_1。**

**Vendi Score 的定义**（[2210.02410](https://arxiv.org/html/2210.02410v1)）：

```
给相似核 k（k(x,x)=1），K_ij = k(x_i, x_j)，取 K/n 的特征值 λ_1..λ_n
VS = exp( − Σ_i λ_i log λ_i )  = exp( − tr( (K/n) log(K/n) ) )
     即 K/n 的 von Neumann 熵的指数，也就是 K/n 的 effective rank
```

- 性质：互不相似时 **VS = n**（最大），全同时 **VS = 1**；模式数翻倍 VS 也翻倍。
- 成本：一般核 **O(n³)**；核是显式特征内积 K=XᵗX 且 d ≪ n 时降到 **O(d²n)**（与 FID 同阶）。
- **致命前提：VS 完全由核决定。** Inception 核量语义、像素核量亮暗颜色，两者结论可以相反。

**最有说服力的两组数字**（都在 2210.02410）：

| 场景 | 「名义计数」 | **有效多样性** | 结论 |
|---|---|---|---|
| Stacked-MNIST 模式计数 | Self-cond. GAN / PresGAN / Original 的 **NoM 全是满分 1000** | **VS = 746.7 / 866.6 / 943.7** | 同一张表上把组合计数和有效多样性摆开了 |
| MOSES 分子生成 | IntDiv（平均成对不相似度）把 **HMM 排第一（0.871）** | **VS 把 HMM 排最后（250.9，其余 475~537）** | HMM 产生的是**成簇的完全重复**分子；**平均成对距离类指标对成簇重复是盲的** |
| MS-COCO caption | 人类 5 条 caption | **VS = 4.88**（≈5 条互不相似）；beam search **3.00**（每 5 条只有 3 条真不同） | 直接给出「有效条数」的读法 |

#### 1.3.3 覆盖度与最近邻距离分布：三代指标和它们的超参

| 指标 | 论文 | 定义 | 特征空间与超参 | 已知失效 |
|---|---|---|---|---|
| PRD (α,β) | [1806.00035](https://ar5iv.labs.arxiv.org/html/1806.00035) | 分布分解 P=βμ+(1−β)ν_P、Q=αμ+(1−α)ν_Q | Inception + mini-batch **k-means k=20**；报 (F_8, F_{1/8}) | 过于乐观；截断时反报更低 precision |
| **improved Precision / Recall** | [1904.06991](https://arxiv.org/html/1904.06991v1) | 以每点到**第 k 近邻的距离**为半径作超球，并集 = 流形估计 | **VGG-16 第二个全连接层激活**（不是 Inception），**k=3**，\|Φ\|=50000 | 对**离群点敏感**：一个真实离群点就能把流形撑大。**真假分布完全相同时 P/R 也只有 0.68 / 0.67** |
| **Density / Coverage** | [2002.09797](https://arxiv.org/html/2002.09797v1) | density = 落在多少个真实邻域球里的**叠加计数**；**coverage = 邻域球建在真实样本上**，看有多少真实点被至少一个生成点覆盖 | **k=5，N=M=10000** | 需要选对嵌入（见下） |

**Density / Coverage 为什么是这三代里唯一能「按理论选超参」的**：

- Lemma 1：P 与 Q 同分布时 **E[density] = 1**。
- Lemma 2：**E[coverage] = 1 − 1/2^k**（M=N→∞），**与数据分布类型和维度无关**。
  所以 k=5 给 E[coverage] ≈ 0.969 —— 这就是 k=5 的来历。
  原文对 P&R 的 k=3 的评价是：「The exact principle behind the choices of those values for P&R is **unknown**」。
- 抗离群实测：真实图像里按第 k 近邻距离 10:1 切出离群点后，
  **recall 上升 >11%（CelebA）/ >15%（LSUN bedroom），而 coverage 上升 <2%**。

**一条对我们极重要的嵌入选择结论**（2002.09797 Table 1）：
当目标域与 ImageNet 统计差距大时，**随机初始化的 64 维嵌入（R64）比 ImageNet 预训练的 VGG16 fc2（T4096）更合理**：

| 域 | 指标 | T4096 → R64 |
|---|---|---|
| MNIST | Coverage | **0.108 → 0.714** |
| MNIST | Density | 0.047 → 0.491 |
| 音频（WaveGAN/SC09） | Coverage | **0.020 → 0.653** |

这和 12_self_verification.md 已记的「**别用 CLIP/SigLIP 当 3D 质量闸**（SigLIP 在 10 个模型上全落 0.077~0.108 窄带）」是同一件事的两个面：
**程序化 3D 场景离 ImageNet 分布很远，预训练视觉特征在这个域里会把一切压成一团。**

#### 1.3.4 pairwise 相似度与「远离群体」类指标

canonical 定义在 Directed Diversity, CHI 2021（[2101.06030](https://arxiv.org/abs/2101.06030) Table 3）：

| 指标 | 定义 | 原文给的失效模式 |
|---|---|---|
| **Remote-Clique** | (1/N²) Σ_{i,j} d(x_i, x_j)（平均成对距离） | 「**it is insensitive to highly clustered points**」 |
| **Chamfer Distance** | (1/N) Σ_i min_{j≠i} d(x_i, x_j)（平均最近邻距离） | 「**it is biased when points are clustered**」 |
| MST Dispersion | 最小生成树边权均值 | — |
| Span | percentile_{90%} d(x_i, x̄) | 抗离群的「半径」 |
| Sparseness | (1/N) Σ d(x_i, medoid) | — |
| Entropy | Shannon-Wiener | **512 维必须先 UMAP 降到 2 维再切 5×5 网格**；不同网格尺寸结论不同 |

**COV / MMD（Chamfer-to-dataset，[1707.02392](https://ar5iv.labs.arxiv.org/html/1707.02392)）** 里有一句正中本题：

> Our coverage metric can identify parts of the data distribution that are **completely missed** by the generative model,
> something that **diversity metrics based on cardinality might fail to capture**.

**质量 × 多样性一起表达：k-DPP 的分解**（[1207.6083](https://arxiv.org/html/1207.6083v1) 式 92–94）：

```
B_i = q_i · φ_i，‖φ_i‖ = 1
L_ij = q_i φ_iᵗφ_j q_j，S_ij = L_ij / √(L_ii L_jj)
P_L(Y) ∝ (Π_{i∈Y} q_i²) · det(S_Y)
         └── 质量项 ──┘   └ 多样性项 ┘
```

对我们的映射：**q_i = 任务的可解性 / verifier 判别力评分，det(S_Y) = 特征空间体积**。
一个 k-DPP 就同时表达了两者，**不需要手调权重** —— 这是选任务子集（例如从 26.9 万候选里选 10 万）最合适的工具。

#### 1.3.5 本机算术：我们的槽位表差多少倍

拿 10_blender_tasks.md §2.1 的 `SLOTS` 伪代码做一次 D_0 / D_1 的粗估：

| 槽位 | 离散化后档数 | **渲染后可被 verifier 分开的档数** |
|---|---|---|
| table.size（20 × 14） | 280 | 约 70（容差 0.005 m，但剪影分辨率下只能分到约 4 倍粗） |
| table.bevel（0.005~0.03） | 26 | **约 3**（48³ 体素 + 剪影分辨率下） |
| bulb.energy（20~200 W） | 19 | **0 —— Workbench 下完全不可见** |
| arm.anim（两个角度各 41 档） | 1,681 | 约 25（5×5） |
| mug.subsurf | 3 | 3 |

```
组合空间 D_0 = 280 × 26 × 19 × 1681 × 3 = 697,547,760 ≈ 7.0e8
有效等价类 D_1 ≈ 70 × 3 × 1 × 25 × 3   = 15,750
折损倍数 ≈ 44,000 倍
```

**结论：一张看起来能出 7 亿种场景的槽位表，实际只能出约 1.6 万种可被区分的任务。**
要做到 10 万任务，**单模板是不够的，必须靠模板数和跨模板组合**（这正是 §6 的 S2 阶段要做的事）。

**顺带得到一条验收规则**：`bulb.energy` 这种「采样空间里有、但渲染后 verifier 看不出」的槽位
**必须禁止进 spec.json**。本机 Blender 留出集唯一的误杀正是「日光功率 3.0 → 3.5 被 A6 判错」，
就是因为题干没钉死它而 verifier 查了它。这条在 §6 的 S1 阶段作为「可见性审计」卡死。

#### 1.3.6 一套可直接抄的工程化多样性仪表盘

§6 的指标大多是为图像生成设计的。**和「程序化任务生成器」最贴合的现成仪表盘来自 RST**
（[2608.05466](https://arxiv.org/html/2608.05466v3)，它把任务从 639 个种子递归放大到 37,484 个）：

| 维度 | 口径 | R1 → R15 实测 | 我们对应什么 |
|---|---|---|---|
| **模式均衡** | 改写族（rewrite-family）上的**熵** | **2.26~2.31 bits**，上限 log₂5 = **2.32**；**最大族占比仅 24.9%~28.9%** | 模板族上的熵；要求最大模板占比 < 30% |
| **变换机制覆盖** | 40 个改写算子的使用覆盖 | 每轮用 **31~38 个**；R15 仍有 **36/40** 在用；**最频繁算子只占 8.0%**（全程最多 12.2%）；前 12 之外的算子仍占 **31.0%** | 破坏算子表（本机 Blender 侧已有 A2/A4/A5/A6/A7/A8/A9 七族）的覆盖率与最频繁算子占比 |
| **血统集中度** | 种子覆盖率 | **98.3%（R2）→ 60.1%（R15）**；R15 保留 363 个种子中的 218 个；**单个种子贡献不超过 0.77%** | 手工场景种子的贡献分布；要求单场景贡献 < 1% |
| **亲子新颖度** | 父子 token 级新颖度（中位） | R15：instruction **0.36**、solution **0.18**、verifier **0.33**（三个组件都还在被改） | 题干 / 参考解 / spec 三者各自的变动率 |
| **去重** | 轮内最近邻相似度（中位 / p95） | **0.223（R1）→ 0.464（R15）**，中位仍 **< 0.5**；**p95 = 0.703**（高相似集中在有限上尾） | 直接套用（见 §3） |

**这五条比任何单一指标都更能抓塌缩**，因为它同时盯住了「模式是否均衡」「机制是否全被用到」
「是否被少数种子主导」「是否还在产生新东西」「是否出现近重复」。
**RST 还顺带证明了污染是可控的**：归一化 13-token 滑窗下**没有任何 benchmark 任务匹配任何合成轮次**，
最大 pairwise 5-gram Jaccard **< 0.009**，且 unigram JSD 从 R1 到 R15 对三个 benchmark **全部上升**
—— 递归合成产出的是**越来越远离 benchmark 的分布**，不是向其收敛。

### 1.4 落到我们身上：防塌缩的六条可执行规则

| # | 规则 | 依据 |
|---|---|---|
| 1 | **验收用 D_1（Vendi Score）不用 D_0（组合计数）**，并同时报 D_0/D_1 的折损倍数 | 2310.12952 明确 q=0 是 uninformative；本机算术显示折损可达 4.4 万倍 |
| 2 | **嵌入用随机初始化的低维投影或自己的几何特征，不要用 CLIP/SigLIP/ImageNet 预训练特征** | 2002.09797 的 MNIST Coverage 0.108→0.714；12_self_verification.md 的 SigLIP 窄带实测 |
| 3 | **覆盖度用 Coverage（k=5, N=M=10000）而不是 recall** | Coverage 有闭式期望 1−1/2^k 可校准；recall 被离群点撑大 >11% 而 coverage <2% |
| 4 | **平均成对距离（Remote-Clique）只能当辅助，不能当闸** | 它对成簇重复是盲的（MOSES 上 IntDiv 把 HMM 排第一、VS 排最后） |
| 5 | **画 Expressive Range 2D 直方图，轴必须是涌现属性（如 mesh 数、连通块数、开放边界边数），不能是槽位参数本身** | Smith & Whitehead 2010 的第一条方法要求 |
| 6 | **选子集用 k-DPP，把「可解性评分」当 q、特征体积当多样性，不要手调权重** | 1207.6083 式 92–94 |

一条额外的工程提醒（来自 Infinigen-Indoors Table 3 的坑）：
**该表里 `w/o Discrete change` 的分数（86.20）反而比全系统（80.84）高**，
作者明说离散改动「necessary for compelling visuals, but **decrease the quantitative score**」——
**量化指标和观感会反向**。所以多样性指标涨了不等于数据变好，反过来也成立。

## 2. 难度分布怎么控制

### 2.0 先说骨架：三件事是同一个 p(1−p)

这一节所有结论都挂在一个量上。把它写在最前面，后面每条都能对回来：

```
伯努利方差 p(1−p) 同时是三样东西：

  ① RL 学习信号的上界      2504.03380 Prop 3.1：策略改进下界 ∝ p(1−p)
                           2601.02648：group 内二元 reward 时 (1/N)ΣA_i² = p(1−p)
  ② 题目的 Fisher 信息      IRT：I_i(θ) = a_i² · P_i(1−P_i)，在 P=0.5 最大
  ③ 难度估计本身的方差      p̂ 的方差 = p(1−p)/n
```

**①② 说「要挑 p ≈ 0.5 的题」，③ 说「p ≈ 0.5 的题最难挑准」。**
这个张力决定了整节的所有工程选择。

### 2.1 pass@k 分桶：具体做法与代价

#### 2.1.1 无偏估计式与它的坑

Codex 论文（[2107.03374](https://arxiv.org/abs/2107.03374) §2.1 Eq.1 + Appendix A）：

```
pass@k := E_problems [ 1 − C(n−c, k) / C(n, k) ]      n ≥ k，c = 正确样本数
```

论文取 **n = 200**，温度 0.8（pass@1 最优 T*=0.2，pass@100 最优 T*=0.8）。

**为什么不能用 `1 − (1 − p̂)^k`**（原文）：

> estimating pass@k ... with 1 − (1 − p̂)^k using the empirical pass@1, **results in a consistent underestimate** ...
> **The gap doesn't fully close even when n > 5k**, and results can seem better with more samples.

这个偏差大致按 1/n 衰减，n = 5k 时仍有 2~4 个点。
它和「拆块取交集」是同一类错误：**把相关子样本当独立的**。

注意一个常被忽略的点：**论文没有给出该估计量方差的闭式表达**。
[2510.04265](https://arxiv.org/html/2510.04265v2) 点名这一点：「lacks closed-form expressions for variance,
relying instead on computationally intensive approximations like bootstrapping」。

#### 2.1.2 要采样多少次才够：方差估算表

**表 A：用 n 次采样估计单题 pass@1 的 95% CI 半宽**（Wilson 区间，本机算）

| p̂ | n=2 | n=4 | n=8 | n=16 | n=32 | n=64 |
|---|---|---|---|---|---|---|
| 0.10 | 0.358 | 0.287 | 0.215 | 0.153 | 0.107 | 0.075 |
| 0.25 | 0.388 | 0.327 | 0.260 | 0.197 | 0.144 | 0.104 |
| **0.50** | **0.405** | **0.350** | **0.285** | **0.220** | **0.164** | **0.119** |
| 0.75 | 0.388 | 0.327 | 0.260 | 0.197 | 0.144 | 0.104 |
| 0.90 | 0.358 | 0.287 | 0.215 | 0.153 | 0.107 | 0.075 |

**最硬的一个数**：Wald 口径下 **n=4、p=0.5 时 95% CI 全宽 0.98**，即几乎整个 [0,1] 区间。
**n=4 标难度等于没标。**

**达到目标精度所需的 n**（`n ≥ (1.96/h)² · p(1−p)`）：

| 目标半宽 h | p=0.3 | p=0.5 |
|---|---|---|
| 0.20 | 20 | 24 |
| 0.15 | 36 | 43 |
| 0.10 | 81 | 96 |
| 0.05 | 323 | 385 |

**表 B：全对 / 全错的概率 `p^n + (1−p)^n`**（= DAPO 式硬闸会丢掉它的概率，本机算）

| 真 p | n=4 | n=8 | n=16 | n=32 | n=64 |
|---|---|---|---|---|---|
| 0.05 / 0.95 | 81.5% | 66.3% | 44.0% | 19.4% | 3.8% |
| 0.10 / 0.90 | 65.6% | 43.0% | 18.5% | 3.4% | 0.1% |
| 0.20 / 0.80 | 41.1% | 16.8% | 2.8% | 0.1% | 0.0% |
| 0.30 / 0.70 | 24.8% | 5.8% | 0.3% | 0.0% | 0.0% |
| 0.50 | 12.5% | 0.8% | 0.0% | 0.0% | 0.0% |

**表 C：三档桶（易 p≥0.7 / 中 0.3~0.7 / 难 p≤0.3）的误分率**（本机精确枚举）

| 真 p | n=4 | n=8 | n=16 | n=32 | n=64 |
|---|---|---|---|---|---|
| 0.10 | 5.2% | 3.8% | 1.7% | 0.1% | 0.0% |
| **0.25** | 26.2% | 32.1% | **37.0%** | 26.3% | **15.6%** |
| **0.35** | 68.9% | 45.3% | 29.1% | 26.8% | **22.5%** |
| 0.50 | 62.5% | 28.9% | 7.7% | 2.0% | 0.2% |
| **0.65** | 68.9% | 45.3% | 29.1% | 26.8% | **22.5%** |
| **0.75** | 26.2% | 32.1% | 37.0% | 26.3% | **15.6%** |
| 0.90 | 5.2% | 3.8% | 1.7% | 0.1% | 0.0% |

**这张表是本节最重要的发现**：桶中心（p=0.5）和桶外（p=0.1/0.9）都能分准，
但**桶边界附近（p=0.25/0.35/0.65/0.75）的误分率在 n=64 时仍有 15%~23%，而且几乎不随 n 下降**。
原因很简单：真 p 恰在边界上时本来就是 50/50，这部分方差**不可能靠加 n 消除**。

**⇒ 硬边界的难度桶在数学上是做不到的，只能用软权重 / 重叠桶。**

**表 D：标签复现性 —— 这是「n 要多大」最直接的公开答案**

[2609.40115](https://arxiv.org/html/2609.40115v1)：Qwen2.5-0.5B/1.5B，1023 个候选 prompt，难度阈值 τ=0.1，
两次独立构集比 Jaccard。原文：

| 预算 n | 难度集合的 Jaccard 复现性 |
|---|---|
| 8 | **0.632** |
| 16 | **0.727** |
| 40 | 约 0.80 |
| 128 | **0.876** |
| 242（外推） | 0.90 |
| 2,111（外推） | 0.95 |

同文还有三条可直接引用的：

| 发现 | 数字 |
|---|---|
| 「跨训练种子的难度差异」里 **81% 其实只是采样噪声** | 同 checkpoint 重采两次 N=32 的 Jaccard **0.798**；独立训练种子间 **0.751** |
| **同预算下「深采一次」优于「拆块取交集」** | 128 次一次性 Jaccard **0.8770**；4×32 且四块都判难才保留 **0.7906**，差 **+0.0864 [+0.0380, +0.1349]** |
| 聚合多种子不是降噪，是换集合 | 同一候选池，官方五种子规则选 **74** 题，另一聚合规则选 **228** 题，单种子 145~150 题 |
| 结论原句 | 「**low-budget difficulty labels are unreliable for classifying individual prompts**」 |

#### 2.1.3 公开工作实际用了多少次

| 工作 | n | 温度 | 打难度的模型 | 分桶规则 |
|---|---|---|---|---|
| **Qwen2.5-Math** [2409.12122](https://arxiv.org/abs/2409.12122) | **8** | 未给 | 自家多尺寸 SFT 模型 | 只留 8 中对 **2~5**（最终 66K 题） |
| **Kimi k1.5** [2501.12599](https://arxiv.org/abs/2501.12599) | **10** | "relatively high" | 自家 SFT 模型 | pass rate 越低越难；另用 **N=8** 次无 CoT 直接猜答案剔「易被猜中」题 |
| **Skywork-OR1** [2505.22312](https://arxiv.org/html/2505.22312v2) | **16（数学）/ 8（代码）** | **1.0**，32K | R1-Distill-Qwen-7B / 32B | 丢 0/N 与 N/N |
| **rStar-Math** [2501.04519](https://arxiv.org/abs/2501.04519) | **16**（难题 +16；第 4 轮 16→64→128） | 未给 | 7B 策略 SLM | easy=全对 / medium=混 / hard=全错 |
| **Big-Math** [2502.17387](https://arxiv.org/abs/2502.17387) | **64**（约 3,000 万次 rollout） | 未给 | Llama-3.1-8B | 五分位，最低桶 solve rate < 20% |
| LiveCodeBench | 不采样（用竞赛平台评级） | — | — | LeetCode 原标签 / AtCoder 分段 / CF 分段 |
| SWE-bench Verified | 不采样（人类计时估计） | — | 3 名标注员/题 | <15min / 15min–1h / 1–4h / >4h |
| **DeepSeek-R1 / DeepSeekMath** | **未找到**任何基于采样的难度标定（DeepSeekMath 全文 "difficult" 出现 0 次） | — | — | — |
| NuminaMath | **官方无难度字段** | — | — | — |

**对「n=4 不够、要 n≥16」这个说法**：没有找到这个确切措辞的论文，但
LZE（[2605.17003](https://arxiv.org/html/2605.17003v2) 附录 F）的原文最接近：

> **Smaller N (= 4) yields noisier group-level pass-rate estimates** ... larger N (≥ 12) provides more stable
> estimates but offers **diminishing returns** ... **N = 8 is a robust default.**

#### 2.1.4 一个必须分清的口径：题集指标 vs 单题难度

| 对象 | 方差 | 加采样的收益 |
|---|---|---|
| **题集整体指标** | `Var(μ̂\|K) = Var(μ̂\|K=1) × (1 + 2/K) / 3`（Miller 2024，[2411.00640](https://arxiv.org/html/2411.00640v1)） | **上限只有 2/3**：K=2 降 1/3、K=4 降 1/2、K=6 降 5/9，很快饱和 |
| **单题难度分** | `p(1−p)/n` | **一点都不饱和** |

**两件事不能混着论证。** Miller 还警告：把 K·N 个答案当独立样本算 pooled SE 是 **inconsistent** 的。

#### 2.1.5 代价估算（落到我们的成本模型）

| 方案 | 每候选 rollout | 10 万任务（26.9 万候选）的 LLM 调用 | 能支撑的结论 |
|---|---|---|---|
| n=2 | 2 | 0.54 M | 只能判「两次都对 / 都错 / 混合」 |
| **两段式 n=2 → n=8** | 平均 4.7 | **0.78 M** | 硬闸（丢 0/N、N/N）+ 三档粗桶 |
| n=8 一次性 | 8 | 1.33 M | 同上，**但贵 0.55 M 次** |
| n=16 | 16 | 2.67 M | 集合复现性 0.727 |
| n=64 | 64 | 10.7 M | 边界桶误分率仍 15%~23% |

**结论：我们用两段式 n=2 → n=8，只做硬闸 + 软权重三档桶，不追求稳定的连续难度分。**
理由是表 C：连续难度分在 n=64 下边界误分率仍有 20% 量级，为它多花 10 倍 LLM 调用换不到相应精度。

### 2.2 课程学习在 agent RL 里的公开做法

#### 2.2.1 机制：GRPO 里全对 / 全错的 group advantage 恒为 0

GRPO 的 outcome supervision advantage（DeepSeekMath [2402.03300](https://arxiv.org/html/2402.03300) §4.1.2，
**该式在原文里没有编号**，常被误引成 Eq.3 —— Eq.3 是目标函数）：

```
Â_{i,t} = r̃_i = ( r_i − mean(r) ) / std(r),   r = {r_1, …, r_G}
```

二元 verifiable reward 下：
- 全对 r_i ≡ 1 ⇒ mean = 1 ⇒ 分子 = 0 ∀i
- 全错 r_i ≡ 0 ⇒ mean = 0 ⇒ 同样 = 0 ∀i

⇒ **消耗了全部 rollout 算力，贡献零梯度。**

**一个方向性矛盾，必须知道**（Dr. GRPO [2503.20783](https://arxiv.org/html/2503.20783) §3.1）：

> **Question-level difficulty bias**: ... **Questions with lower standard deviations (e.g., those that are too easy
> or too hard, with the outcome rewards being almost all 1 or 0) are given higher weights during policy updates.**

**std 归一化给「几乎全对/全错」的题加权，而 dynamic sampling 把它们扔掉 —— 两者方向相反。**
Dr. GRPO 的解法是把 std 归一化整项删掉。**别同时用而不自觉。**

#### 2.2.2 DAPO 的 dynamic sampling

[2503.14476](https://arxiv.org/html/2503.14476) §3.2，约束挂在目标函数上（Eq.11）：

```
s.t.  0 < | { o_i | is_equivalent(a, o_i) } | < G
```

原文做法：**over-sample 并过滤掉 accuracy ∈ {0, 1} 的 prompt**，
「Before training, we keep sampling until the batch is fully filled with samples whose accuracy is neither 0 nor 1.」
配置：prompt batch 512 × **G=16 rollouts**，mini-batch 512。

**Table 1 累加消融（AIME24 avg@32，Qwen2.5-32B base）**：

| 配置 | 分数 | 增量 |
|---|---|---|
| Naive GRPO | 30 | — |
| + Overlong Filtering | 36 | +6 |
| + Clip-Higher | 38 | +2 |
| + Soft Overlong Punishment | 41 | +3 |
| + Token-level Loss | 42 | +1 |
| **+ Dynamic Sampling（= DAPO）** | **50** | **+8** |
| （参考）DeepSeek-R1-Zero-Qwen-32B | 47 | — |

**dynamic sampling 在这条累加路径上贡献 8 分，是单个 trick 里最大的。**
（注意这是「最后加上去」的位置效应，不是独立消融。）

**开销**：论文只说「The sampling cost for each batch is **dynamic**」，**没给倍数**。
Figure 3(b) 是曲线，**具体读数未找到**。但别的论文实测了同一现象：

| 来源 | 数字 |
|---|---|
| **GRESO** [2506.02177](https://arxiv.org/html/2506.02177) | Qwen2.5-Math-7B 做 GRPO，**有效 prompt 比例后期只剩约 20%**；「if the zero-variance prompt ratio is 80%, DS needs to perform **around five times rollouts**」 |
| SRPO [2504.14286](https://arxiv.org/html/2504.14286) | 「**nearly 50% of the sampled groups within batches produce identical rewards**」 |
| **Skywork-OR1** | **开训前**就有 0/N 或 N/N：7B **54%**（21.4% 全错 + 32.4% 全对）、32B **63%**（20.7% + 42.0%） |

**理论上界 vs 实测的差距（本机算）**：若题库 pass rate 服从 U(0,1)，
则 `P(丢弃) = E[p^G + (1−p)^G] = 2/(G+1)`：

| G | 保留率 | 理论过采样倍数 |
|---|---|---|
| 4 | 0.600 | 1.67× |
| 8 | 0.778 | 1.29× |
| **16** | **0.882** | **1.13×** |
| 32 | 0.939 | 1.07× |

**G=16 的理论倍数 1.13× 与实测 5× 的巨大差距，正是「题库 pass rate 极度堆在两端」的量化体现。**
现实中绝大多数题不是 U(0,1)，而是堆在 p≈0 或 p≈1。
**对我们的直接含义**：§5.2 漏斗里「难度带筛选留存 0.60」这条外推，
如果我们的任务分布也堆在两端，实际可能只有 0.2~0.4 —— 这是整个成本模型最敏感的一项。

#### 2.2.3 「只留中等难度」的收益：唯一有完整阈值扫描的论文

[2504.03380](https://arxiv.org/html/2504.03380)（Online Difficulty Filtering），Qwen2.5-3B，每步 16 prompts × 16 rollouts。

理论（Prop 3.1 / Remark 3.3）：

```
E_{y~π_init}[ log π*/π_init ] ≤ − p(x)(1 − p(x)) / (2β²)
```

> The lower bound ... is proportional to the **Bernoulli variance p(x)(1−p(x))**,
> which attains its **maximum at p(x)=0.5**.

**Table 1 节选（五个数学 benchmark 平均）**：

| 类别 | 区间 | **Avg.** |
|---|---|---|
| SFT 起点 | — | 20.2 |
| 离线 Curation（外部模型代理） | — | 28.4 |
| 离线 Curation（初始模型代理） | — | 26.3 |
| **Plain GRPO** | 0 ≤ p ≤ 1 | **26.3** |
| Skewed（只切一边） | 0 < p ≤ 1 | 24.9 |
| Skewed | 0.2 < p ≤ 1 | 25.9 |
| Skewed | 0.4 < p ≤ 1 | 23.8 |
| Skewed | 0 ≤ p < 0.8 | 24.8 |
| Skewed | 0 ≤ p < 0.6 | 25.8 |
| **Balanced** | **0 < p < 1（= DAPO 口径）** | **27.3（+1.0）** |
| Balanced | 0.1 < p < 0.9 | 28.4 |
| **Balanced** | **0.2 < p < 0.8** | **29.8（+3.5）** |
| **Balanced** | **0.3 < p < 0.7** | **30.1（+3.8，全表最高）** |
| Balanced | 0.4 < p < 0.6 | 29.9 |

**四条可直接引用的结论**：

| 结论 | 数字 |
|---|---|
| **只剔全对全错（DAPO 口径）只值 +1.0 pp** | 26.3 → 27.3 |
| **再收紧到中段多拿 +2.8 pp** | 27.3 → 30.1 |
| **Skewed（只切一边）全部输给 plain GRPO** | 23.8~25.9 < 26.3 ⇒ **必须对称切** |
| **过紧有代价** | (0.4,0.6) 回落到 29.9，且「can require **significantly more rollouts** to fill a batch, leading to longer training times」 |

7B 扩展（Table 2）：SFT 37.3 → plain 39.6 → (0,1) 39.9 → **(0.3,0.7) 41.8**。

**在线为何胜过离线（Figure 2）**：训练中 checkpoint 感知的 batch 平均难度稳定在 0.5 附近；
而 before/after-GRPO checkpoint 与外部代理都偏移 —— 离线代理模型的难度与被训模型**系统性错位**。

#### 2.2.4 反面证据：同一个区间，离线做可能负收益

| 出处 | 区间 | 结论 |
|---|---|---|
| **AdaRFT** [2504.05520](https://arxiv.org/abs/2504.05520) 的 baseline "PPO (w/ Filter)" | pass@40 **离线**丢 ≤10% 或 ≥90% | **六个设置无一打过 AdaRFT，且 4/6 比普通 PPO 还慢**。原文：「removes a **large fraction of the data**, including many potentially informative examples ... the filtering must be **recomputed whenever the model or the data distribution changes**」 |
| **Polaris** aggressive filtering | 只留 ≤4/8（40K→19K） | **变差**：「overly saturated with difficult problems」。最优是 26K（只去掉全部 8/8） |
| 2504.03380 skewed 全档 | 单边切 | **全部低于 plain GRPO** |

**Polaris 的难度分布消融是「过滤过头反而更差」最干净的证据**：

| 训练集 | 规模 | 构造 | 结果 |
|---|---|---|---|
| Full | 40K | 原始 J 形，被 8/8 易题主导 | 进展受阻 |
| **Removal of Perfect Scores** | **26K** | 去掉全部 8/8 → 镜像 J 形 | **最优** |
| Aggressive Filtering | 19K | 只留 ≤4/8 | **变差** |

#### 2.2.5 固定 batch size 的三种实现与代价

| 实现 | 机制 | 代价 |
|---|---|---|
| **DAPO** | over-sample + buffer，凑满 N 才训 | 实测约 **5×** rollout |
| **Polaris 的两招** | ① **Rollout Rescue**：per-example 离线 sink buffer 存早期正确回答，再遇 0/8 就替换一条失败 rollout ② **Intra-Batch Substitution**：batch 内把有非零 advantage 的样本复制去替换零 advantage 的 | **零额外 rollout**（原文：「matching DAPO's benefits but requiring only a few tensor index operations—no extra rollouts」），代价是重复样本、有效 prompt 多样性下降 |
| **GRESO** [2506.02177](https://arxiv.org/html/2506.02177) | 用历史 reward **在 rollout 前**预测 zero-variance prompt 并跳过 | **省 2.0~2.4× 端到端训练时间**，精度持平（7B：57.5 vs 57.8）；rollout 数 13.1M → 6.3M |
| **LUFFY** [2504.14945](https://arxiv.org/abs/2504.14945) | 不过滤，把 off-policy（R1）轨迹并进 group 一起算 advantage ⇒ 全错组因此有非零 advantage | on-policy RL 在 Hard 子集 **reward 塌到 0**，LUFFY 两子集都稳定上升；对 on-policy RL **+8.0** |

**GRESO 的一条时序统计决定了「能不能静态剪枝」**：

> P(Previous|Current)：**超过 90%** 的当期零方差 prompt 在更早 epoch 也是零方差；
> 但 P(Current|Previous)：**约 20%** 的历史零方差 prompt 会重新变成 effective。

⇒ **不能静态永久剪枝，必须留探索概率。**

#### 2.2.6 自动难度提升：UED 线放弃了显式 pass-rate 区间

| 工作 | 瞄准的难度区间 | 机制 |
|---|---|---|
| **纯 Minimax adversary** | 瞄 **0%**（退化为不可解） | `Λ^M(π) = argmin_θ U^θ(π)`。PAIRED 原文：「a minimax adversary is incentivized to make the environments **completely unsolvable**, generating mazes with unreachable goals」 |
| **PAIRED** [2012.02096](https://ar5iv.labs.arxiv.org/html/2012.02096) | 无显式区间；实际瞄 **protagonist 失败而 antagonist 成功的最简任务** | `Regret^θ(π^P, π^A) = U^θ(π^A) − U^θ(π^P)`；adversary 与 antagonist reward = +Regret，protagonist = −Regret。因 reward 含效率项，**最大 regret 出现在刚超出能力边界处**，原文称 "zone of proximal development" |
| **PLR** [2010.03934](https://ar5iv.labs.arxiv.org/html/2010.03934) | 隐式瞄「阈值 level」 | 打分 = **GAE 幅值（L1 value loss）**；`P_replay = (1−ρ)·P_S + ρ·P_C`（P_C 是 staleness）。**Value Correction Hypothesis**：阈值 level 回报非稳态 ⇒ value error 大；远超能力的 level 价值目标稳定指向失败 ⇒ value error 小。**所以 value loss 隐式对准能力边界，不需要外部难度度量**。ρ=0 和 ρ=1 都比 uniform 差，**必须混合** |
| **Robust PLR** [2110.02439](https://arxiv.org/abs/2110.02439) | 按 regret 排名取 top | 两个 regret 代理：**positive value loss**（只取正号）与 **MaxMC**（`R_max − V(s_t)`，去掉对当前策略的依赖）。核心机制：**只在 replay 的 level 上做梯度更新**，随机新生成的只评估不训练。原文结论叫 **"it is optimal to train on less data"** |
| **ACCEL** [2203.01302](https://arxiv.org/abs/2203.01302) | **有意去掉手工区间** | 对高 regret 的 level 做小幅编辑（mutation），编辑后**先评估、只有 PVL 高才入 buffer**。核心主张：**regret 是 domain-agnostic 的 fitness function**，取代 POET 那种手写难度区间 |
| **POET** [1901.01753](https://arxiv.org/abs/1901.01753) | **回报 ∈ [50, 300]**（解决线 230，繁殖资格 ≥200） | 显式 minimal criterion，太难太易都剔；MC 超额时**按分从低到高录取**（偏好更难的）。注意：网上流传的「[25, 340]」**不存在**，真值是 [50, 300] |
| **ADR**（OpenAI，[1910.07113](https://arxiv.org/abs/1910.07113)） | **单回合成功次数 10~20** 之间不动 | t_L=10 / t_H=20，均值 >t_H 扩宽该维区间（步长 Δ=0.02），<t_L 收窄；boundary sampling 概率 0.5，性能队列 m=240。**最直白的「双阈值自动难度」实现** |

**PLR 的 Procgen 数字**（Table 2，10 run × 100 test episode，归一化 test return）：

| 方法 | 归一化 test return |
|---|---|
| Uniform（基线） | 100.0 ± 4.5 |
| mixreg | 113.8 ± 2.8 |
| UCB-DrAC | 129.8 ± 8.2 |
| **PLR** | **128.3 ± 5.8（+28%）** |
| **UCB-DrAC + PLR** | **176.4 ± 6.1（+76%）** |

**ACCEL 的 MiniGrid zero-shot**（5 run × 100 trial）：平均 PAIRED 0.39 / Minimax 0.05 / DR 0.62 / PLR 0.71 / **ACCEL 0.88~0.90**。

**LLM 侧分成两派**（这个分歧对我们有直接影响）：

| 派 | 目标 | 机制 |
|---|---|---|
| **AZR**（Absolute Zero，[2505.03335](https://arxiv.org/abs/2505.03335)） | **峰值在最小非零通过率（约 1/G），即「最难可解」** | `r_propose = 0 if r̄_solve = 0 else 1 − r̄_solve`。原文：「if a task is either trivial to solve (r̄=1) or unsolvable (r̄=0), the task provides **little to no learning signal**」 |
| **R-Zero**（[2508.05004](https://arxiv.org/abs/2508.05004)） | **明确瞄 50%** | `r_uncertainty = 1 − 2·\|p̂ − 1/2\|`；难度过滤只保留 10 次采样中与多数票一致数在 **3~7** 之间的题。**去掉难度过滤，通用域均分掉 6 点以上** |
| SPIRAL（[2506.24119](https://arxiv.org/abs/2506.24119)） | 无显式目标，**实测稳定在 50~52% 胜率** | 零和语言博弈自对弈，对手就是不断变强的自己 |

2026 年的后续已经在脱离纯通过率口径：
**CompassPlay**（2609.32228）改按**梯度对齐**发奖（任务的 solver loss 梯度与参考任务梯度的一致性）；
**Beyond Uncertainty**（2608.30035）指出**单 solver 采样不确定度会在 solver 变自信后塌到 0**，改用异构 solver 集合的熵。

### 2.3 「难度」和「verifier 判别力」必须分开

#### 2.3.1 一句话结论

**在当今主流 benchmark 上，模型「失败」里有一半以上不是能力问题，而是题目欠规约或测试过严。**
这不是推测 —— 是 OpenAI 自己两次公开推翻自己的评测集。

#### 2.3.2 SWE-bench Verified 的人工筛查（2024-08）

| 项 | 数字 |
|---|---|
| 人工筛查者 | **93** 名有经验的 Python 开发者 |
| 标注样本量 | 从 2,294 条随机抽 **1,699** 条 |
| **问题描述欠规约被标记** | **38.3%** |
| **单测可能把正确解误判为错被标记** | **61.1%** |
| **合计被筛掉** | **68.3%** |
| 最终数据集 | **500** 条 |
| **GPT-4o 分数（同一 scaffold）** | SWE-bench **16%** → SWE-bench Verified **33.2%（翻倍以上）** |
| 过滤规则 | ensemble label ≥ 2 即剔除；ensemble = 三名标注者**取最大值**（任一人判严重即剔除） |

（38.3% / 61.1% / 68.3% 不是互斥三分；前两个是两个维度的标记率，可重叠。
openai.com 在本机代理下 403，数字来自全文镜像，建议在办公网复核。）

#### 2.3.3 OpenAI 自己两次推翻（2026）—— 最强证据

**(a) 停用 SWE-bench Verified（2026-02）**

| 项 | 数字 |
|---|---|
| 审计范围 | 500 题中 **138** 条（27.6%，都是模型常失败的） |
| **测试会拒掉功能正确解** | **至少 59.4%** |
| 其中「强制与任务无关的具体实现细节」 | **35.5%** |
| 其中「检查了题面没要求的功能」 | **18.8%** |
| 动机 | 近 6 个月 SOTA 仅 74.9% → 80.9%，需判断是模型到顶还是**数据集到顶** |

**(b) 又推翻对 SWE-bench Pro 的推荐（2026-07）**

| 项 | 数字 |
|---|---|
| 公开集规模 | 731 题 |
| Codex agent + 人类研究员定论 | **200 条（27.4%）**为缺陷题 |
| 并行 5 名资深开发者独立评审 | **249 条（34.1%）** |
| 两条流水线一致率 | **74%** |
| 缺陷四类 | 测试过严 / 题面过于含糊（要求只藏在 hidden test 里）/ 测试过浅（残缺解也能过）/ 题面指向错误 |
| 实例 | OpenLibrary 题面要求 1 个空格，hidden test 要求 2 个 |

**这两条对我们的直接含义**：
本机 90_local_experiments.md §5 已经独立踩到同一个坑
（cup-wood-color 要求「有别于木色的独立颜色」而 verifier 要求恰好是 0x3a9ad9；
legs-centered 要求「位于四个角落附近」而 verifier 要求几乎重合）。
**OpenAI 在 500 题上栽的和我们在 9 题上栽的是同一个错误，比例也接近**
（我们 2/9 = 22%，他们审计的失败题里 ≥59.4%）。

#### 2.3.4 第三方批评性分析

**SWE-Bench+** [2410.06992](https://arxiv.org/html/2410.06992v1) —— 人工复核 251 条「判通过」的补丁：

| 模式 | 条数 | 占 251 |
|---|---|---|
| **Solution leak（答案直接写在 issue / 评论里）** | 82 | **32.67%** |
| Incorrect fixes | 32 | 12.75% |
| Different files/functions changed | 9 | 3.59% |
| Incomplete fixes | 37 | 14.74% |
| **可疑修复合计** | **160** | **63.75%** |
| 真正正确（与 gold 不同实现） | 76 | 30.27% |
| 比 gold 更全面 | 15 | 5.98% |

- 滤掉问题实例后，SWE-Agent+GPT-4 解决率 **12.47% → 3.97%**。
- **泄题在「已清洗」数据集里依旧存在**：Lite **18 条（33.33%）**、**Verified 37 条（33.04%）**；
  可疑修复占比 Lite 48.14%、**Verified 55.36%**；解决率 **Verified 22.4% → 10.0%**。

**UTBoost** [2506.09289](https://arxiv.org/html/2506.09289v1) —— 自动补测试反查假阳性：
发现 **36** 条任务测试不足，揪出 **345** 个被错判为 pass 的补丁，
影响 **Lite 排行榜条目的 40.9%、Verified 的 24.4%**，造成 18 和 11 处名次变动。

#### 2.3.5 最干净的分离证据：Platinum Benchmarks

[2502.03461](https://arxiv.org/html/2502.03461v1)。**方法本身就是最低成本的坏题筛法，可直接抄**：

```
把每题发给多个前沿模型，只人工复核「至少有一个模型答错」的题
  gold 错   → 前沿模型普遍与 gold 不一致
  题本身坏  → 模型互相不一致
作者明说这给出的是下界（所有模型一致错且与 gold 一致的坏题会漏掉）
```

**Table 4 —— 「模型错误里有多少其实是 benchmark 的错」**：

| 数据集 | 原始平均错误 | 清洗后 | **benchmark 归因占比** |
|---|---|---|---|
| SingleEq | 1.1 | 0.1 | **93%** |
| HotpotQA | 26.4 | 2.3 | **91%** |
| SingleOp | 2.5 | 0.3 | **90%** |
| MultiArith | 3.5 | 0.4 | **89%** |
| SQuAD2.0 | 56.2 | 9.9 | **82%** |
| SVAMP | 18.8 | 4.3 | 77% |
| DROP | 28.4 | 6.6 | 77% |
| GSM8K | 10.1 | 5.2 | 48% |
| Object Counting | 6.3 | 4.8 | 24% |
| Winograd WSC | 16.6 | 15.0 | 10% |
| MMLU HS Math | 20.5 | 19.5 | 5% |
| Navigate / Logic Ded. 3-Obj | 5.9 / 2.4 | 5.9 / 2.4 | **0%** |

**这一列从 0% 到 93% 横跨全区间 —— 同一批模型、同一个 pipeline。
这就是「任务难」与「题/判分器坏」可以被量化分离的最直接证据。**

#### 2.3.6 ceiling check：公开做法与数字

| 做法 | 公开案例与数字 |
|---|---|
| **参考解执行校验**（gold 必须让 F2P 翻转） | SWE-bench 构造：**砍掉约一半候选任务** |
| **人类 ceiling**（让人写解，看能否过全部测试） | **BigCodeBench：32/33 = 97%**（随机把 33 条最终题面分给 11 名标注者）。低于此阈值的题 = 测试过严或题面欠规约 |
| **evaluator 满分可达性证明** | TheAgentCompany：每任务须有**截图证明「正确完成即满分」**；LLM judge 若「交付物正确却因中间步骤误判而 0 分」，框架会**覆盖评分给满分** |
| **oracle 信息注入**（给对文件 / 给上下文） | SWE-bench Table 20：Claude 2 BM25 **2.27% → oracle 4.01%**；SWE-Llama 13b **0.70% → 4.54%**（**2~6 倍跳升**）⇒ 之前的失败很大一部分是「信息没给到」而非不会修 |
| **交互式澄清**（允许问用户） | **Ambig-SWE** [2502.13069](https://arxiv.org/abs/2502.13069)：SWE-bench Verified 的欠规约变体，模型**分不清** well-specified 与 under-specified；但允许向用户提问后性能**最高 +74%** |
| **默认猜中率** | [2505.13360](https://arxiv.org/abs/2505.13360)：LLM 默认能猜中未写明需求的比例 **41.1%**；欠规约 prompt 在换模型/换 prompt 时**回归概率是 2 倍** |
| **补测试反查假阳性**（verifier 太松的反向 ceiling） | UTBoost：345 个假通过补丁 |

#### 2.3.7 一个致命的实测：「这题欠规约吗」人与人只有 α=0.24 的一致性

| 场景 | 指标与数值 | 来源 |
|---|---|---|
| **SWE-bench Verified 的 OpenAI 公开标注（第三方重算）** | Krippendorff **α = 0.24**（issue clarity / 欠规约判定）、**α = 0.41**（test adequacy） | SPICE [2507.09108](https://arxiv.org/html/2507.09108v1) |
| 同 rubric 的独立复刻（7 名 SE 研究者、7 周、840 实例、约 882 人时） | α 始终**未超过 0.67** 的可信阈值，实测落在 **0.0~0.4**；OpenAI 用 moderator 裁决分歧，复刻要再加 **25%** 开销 | 同上 |
| SQuAD 坏题三分类标注 | α = **0.344** | Rodriguez et al. ACL 2021 |
| 对照：**SWE-bench M 的难度标注** | **Fleiss kappa = 0.78** | [2410.03859](https://arxiv.org/html/2410.03859v1) |
| LLM 替代人工的上限 | SPICE 在 SWE-V 标签上：ICA 准确率 **87.3%**、TCA **68.5%**；人工复评 ICA 93.5% 正确、**TCA 仅 60%**。成本 1,000 实例从约 **10 万美元**人工降到 **5.10 美元** | SPICE |

**「这题欠规约吗」的人际一致性（α≈0.24）比「这题多难」（kappa 0.78）低了一个量级。**
⇒ 任何单人判定都不可信，必须多标注者取 max / 裁决，或改用响应模式统计（IRT / point-biserial）。

#### 2.3.8 把「难」和「坏」分开的量化工具：IRT 与 point-biserial

**IRT 2PL**：

```
P(X_ij = 1 | θ_j) = σ( a_i · (θ_j − b_i) )
  θ_j : 模型 j 的潜在能力
  b_i : 题 i 的难度
  a_i : 题 i 的区分度

Fisher 信息：I_i(θ) = a_i² · P_i(1 − P_i)     ← 在 P=0.5 最大，且可加
```

**判据分工（这就是「难」与「坏」的分离）**：

| 参数 | 含义 | 判据 |
|---|---|---|
| **b_i 高** | **难** | 正常，是我们想要的 |
| **a_i ≤ 0** | **坏** | Rodriguez et al. ACL 2021 特意允许 γ<0 来抓坏题：**γ<0 ⇒ 标注错误**（能力越低越容易答对） |
| **feasibility（4PL 的 d）低** | **欠规约** | PSN-IRT [2505.15055](https://arxiv.org/html/2505.15055v3) Finding 5：**低 feasibility 常源于 under-specified / 过于宽泛的题** |
| 零方差（全对或全错） | 区分度不可识别 | Vania et al. ACL 2021：**占全数据的 4%**，29 个数据集中 13 个至少含一条；NewsQA 约 **16%** 的样本被所有模型答错 |

**规模参照**：
- Rodriguez et al.：SQuAD 2.0 排行榜 **161** 个 dev subjects、**11,873** items（190 万对）。
- **tinyBenchmarks** [2402.14992](https://arxiv.org/html/2402.14992v2)：Open LLM Leaderboard **395** 个 LLM、约 29k items。
  **每 scenario 100 题即可把性能估计误差压到约 2%**：MMLU 14k → 100（**140 倍降本**）。
- **metabench** [2407.12844](https://arxiv.org/html/2407.12844v2)：**n > 5000** 个 LLM、**28,632** items
  → 压到 **858** 题（**< 原规模 3%**），重建总分 RMSE **0.58%**，Spearman r = **0.998**。
- PSN-IRT Finding 2：**最难题的 IRT 难度很少超过 1.0**，而 DeepSeek-V3 的能力估计 **>3.0**（benchmark 已饱和）。

**point-biserial（成本最低的一招）**：

```
r_pb(i) = corr( X_i , S − X_i )        ← 必须用 rest-score 版，不剔自身会被系统性抬高
```

**理论依据**（[2511.16842](https://arxiv.org/html/2511.16842v1) Corollary 2）：
若 Rasch 模型成立，**item-total 相关必为正**。
因此**低或负的 item-total 相关 = 单维假设被违反 = 该题可疑**。

实测效果：

| 项 | 数字 |
|---|---|
| 实际用的统计量 | **tetrachoric correlation**（inter-item），约 **1,000 题的 benchmark 1 分钟**跑完 |
| 送审深度 | 每个 benchmark 只 flag **50 题**给专家，报 precision@50 |
| **命中率** | 九个 benchmark 上，被 flag 的题**最高 84%** 经人工确认存在实质缺陷 |
| 新发现的第三类无效题 | **grading issues**：答案 `4.00` 但 grader 只认 `4`；`15.0` ≠ `15`；`3 PM` ≠ `15:00` |
| 增量 | **在 GSM8K 上，在 Platinum 已修订的基础上又找出 16 条此前未发现的无效题** |

**阈值惯例**（经典测量学）：

| r_pb | 判定 |
|---|---|
| ≥ 0.30 | 区分良好 |
| 0.20 ~ 0.29 | 勉强可接受 |
| < 0.20 | 区分差，需修订 |
| **≤ 0** | **红旗：可能答案键写错** |

**注意**：区分度在极易/极难题上会被天然压低（因为 `I_i(θ) = a_i² P_i(1−P_i)`，P→0 或 1 时信息趋 0），
**不能脱离难度孤立判读 r_pb**。

一个真用了这套阈值的 LLM benchmark（EduArt，2607.02007）：871 道题、12 个模型，
**831/871 可算区分度** —— 剩下 **40 条被所有模型答对、方差为零，区分度无法定义**；
平均 r_pb = 0.514；**最差题型是 True/false：83 题平均 r_pb 仅 0.245，其中 poor 24 条** ——
**题型本身就是坏题源**。

#### 2.3.9 落到我们身上：两套闸必须分开

本机已有的闸只覆盖了一半。对照补齐：

| 要判的 | 判据 | 本机现状 |
|---|---|---|
| **任务难不难** | pass@8 分桶（两段式 n=2 → n=8） | **待建**（§6 的 S2 阶段） |
| **题干欠规约吗** | **ceiling check**：把参考 9 视角渲染图加进 problem statement，重测通过率。**跳升 ≥ 0.3 判为欠规约** | 90_local_experiments.md §6 已把它设计成实验矩阵的独立一维（text vs text+参考图），**但还没当闸用** |
| **verifier 查多了吗** | `spec.json` 白名单 + **可见性审计**（§1.3.5）：题干没钉死的字段不许进 spec | Blender 侧有 spec.json，**three.js 侧还没有** |
| **verifier 查少了吗** | 变异集的检出率（本机 47/47）+ 作弊页面拦截率（本机 7/7） | **已有，是本机最强的一环** |
| **这题是坏题吗** | ① 多模型分歧三角定位（Platinum 的方法，只复核「至少一个模型答错」的题）② **item-total 相关 < 0.10 或 ≤ 0 送人工**（1,000 题 1 分钟）③ 零方差题单列 | **待建** |
| **verifier 在初始状态就通过了吗** | FACET 判据 ii | **缺这一条**（§1.2 已指出） |

**最该补的一条，也是最便宜的一条**：
**item-total 相关 + 零方差检测**。它不需要额外采样（难度标定的 rollout 结果直接复用），
1,000 题 1 分钟，precision@50 最高 84%。
按 §5.2 的 10 万任务规模，每轮 flag 1,200 条送人工（正好对上 §5.8 的抽检配额）。

### 2.4 本节的六条可执行规则

| # | 规则 | 依据 |
|---|---|---|
| 1 | **粗闸（丢 0/N、N/N）用 n=8 就够；不要追求稳定的连续难度分** | n=16 的集合复现性只有 0.727（2609.40115）；桶边界误分率在 n=64 时仍 15%~23%（本文表 C） |
| 2 | **带状过滤必须对称、必须在线、不要收太紧** | 单边切全部输给 plain GRPO；(0.3,0.7) 最优 30.1，(0.4,0.6) 回落 29.9；离线做（AdaRFT baseline）是负收益（§2.2.3 / 2.2.4） |
| 3 | **同预算优先深采一次，不要拆块取交集** | 0.877 vs 0.791，差 +0.086（2609.40115） |
| 4 | **固定 batch 用 GRESO 式「rollout 前预测」而不是 DAPO 式过采样** | 省 2.0~2.4× 端到端；但**必须留 20% 探索概率**（历史零方差 prompt 有约 20% 会变 effective） |
| 5 | **「难」和「坏」用两套闸，且「坏」的闸优先用响应模式统计而不是人工标注** | 人工判「欠规约」α 只有 0.24；item-total 相关 precision@50 达 84%、1000 题 1 分钟 |
| 6 | **别同时用 std 归一化和 dynamic sampling 而不自觉** | Dr. GRPO 证明 std 归一化给「几乎全对/全错」的题**加权**，方向与 dynamic sampling 相反 |

**一个必须记住的量级**：Skywork-OR1 实测**开训前就有 54%（7B）/ 63%（32B）的题是零梯度**。
所以 §5.2 漏斗里「难度带筛选留存 0.60」这条外推**很可能偏乐观** ——
如果我们的任务分布也堆在两端，实际可能只有 0.2~0.4，候选数要再翻 1.5~3 倍。
**这是整个成本模型里最该先用小规模实验钉死的一项。**

## 3. 去重与污染隔离在十万量级怎么做

### 3.0 先说结论：十万量级的去重是免费的，所以没有理由做得糙

| 项 | 算式 | 结果 |
|---|---|---|
| 视觉 embedding（10 万任务 × 9 视角 = 90 万图） | DINOv2 ViT-B 单卡约 200 图/s | **1.25 GPU 小时** |
| pHash 90 万图 | imagededup 官方 benchmark：dHash **277~426 图/s**（AWS r5.xlarge，4 vCPU，无 GPU） | **约 40 分钟**（4 核） |
| 全对全余弦（10 万 × 768 维） | 一次 GEMM = **15.36 TFLOP**；A100 TF32 Tensor Core 156 TFLOPS，按 70% 实效 | **0.14 秒** |
| MinHash + LSH（题干 + 代码） | text-dedup 在 10 万篇文档上实测约 11 秒 | 秒级 |
| 向量存储 | 10 万 × 768 × 4B | 307 MB（int8 后 77 MB） |

**两条工程判断**：

1. **十万量级完全不需要 ANN 索引。** 分块暴力 GEMM + 块内 top-k 就是最优解。
   FAISS 官方也说「只做 1,000~10,000 次检索时直接用 Flat，建索引摊不回来」。
   ANN 的门槛在百万级。真正的约束不是算力，是**那 40 GB 的输出矩阵**
   （10 万 × 10 万 fp32），所以必须分块归约、永不物化全矩阵。
2. **百万级才会碰到唯一的串行墙**：datatrove 官方 FineWeb 脚本里，
   MinHash 的第三阶段（连通分量聚类）是**单任务、8 核、约 200 GB 内存、30 小时墙钟**，
   不可并行。十万量级碰不到，但做扩产规划时要记住这个墙在哪。

### 3.1 结构去重：场景图哈希与代码 AST 哈希

#### 3.1.1 一个反直觉的事实：主流代码数据集没有一个用 AST 等价做去重

The Stack v1/v2、StarCoder/2、CodeGen、AlphaCode、CodeParrot、OpenCoder **全部**是
「精确 hash + MinHash-LSH on token / 字符 n-gram」。理由：600+ 语言无法统一解析，且 MinHash 可亚线性扩展。

真的用结构哈希的只有两个：

| 项目 | 判据 | 结果 |
|---|---|---|
| **ComPile**（LLVM IR 数据集）[2309.15432](https://arxiv.org/html/2309.15432) | LLVM **StructuralHash**：module 内全局变量 + 函数的组合哈希；**精确结构等价，无阈值**；对不改语义的变化不变（除函数调用名外），**刻意忽略 attributes 与指令依赖** → 也会误并一部分近重复 | 990 GB bitcode → 853 GB（体积 **−35%**）；Julia 重复率约 40% |
| 解题程序去重 [2307.07940](https://arxiv.org/html/2307.07940) | 用 AST 决定哪些标识符该匿名化（库函数不动、用户定义的匿名化），去注释空白后格式化再精确匹配；**作者明说不用 AST 当去重单位**，因为要还原可运行源码 | — |

**明确未找到**：没有任何预训练级公开代码数据集用 AST 规范化哈希 / Merkle 树哈希 + 阈值做去重并公布去重比例。

#### 3.1.2 对我们而言，正确的结构去重单位是场景图，不是 AST

这是本课题和通用代码去重的**关键分叉**，而且本机已经有证据：

> 10_blender_tasks.md §2.1 的 `cube_size2`：换一条实现路径、世界几何逐点相同的改写，
> 几何信号全部放行（分部件 F-score **0.9993**），只有按代码比的 A2/A3 会误杀。

也就是说**同一个任务可以有无穷多种代码写法，AST 哈希会把它们算成不同任务**（假阴性），
而**不同的任务也可能有近似的代码骨架**（假阳性）。
所以去重单位必须是**产物**（场景图 / 几何），不是**代码**。

建议的三级结构指纹（全部取自本机探针已有的产物，零额外成本）：

| 级别 | 指纹 | 用途 | 判重判据 |
|---|---|---|---|
| L-exact | 场景图规范化哈希：`sorted([(几何类型, round(顶点数), round(世界 bbox, 3), 量化主色)])` + 灯光类型多重集 + 连通块数 + 开放边界边数 | 抓完全同构的场景 | **哈希相同即判重**（无阈值，对标 ComPile 的 StructuralHash） |
| L-near | 上面那些标量拼成的**低维特征向量**（约 20~40 维）：mesh 数、顶点数分位、bbox 体积比、颜色多重集直方图、连通块数、开放边界边数、层级深度 | 抓「同一个模板换种子」 | 欧氏/余弦近邻 + 人工标阈值（见 3.1.3） |
| L-spec | `spec.json` 的**断言集合**（族 + 字段路径，不含具体数值） | 抓「不同场景但考同一个点」—— 这是产能爬坡时最容易出的重复 | Jaccard ≥ 0.9 且 L-near 近邻 → 判重 |

**L-spec 这一层是别人没有的，也是最该做的。** 因为程序化生成最容易塌缩的不是「场景长得一样」，
而是「考的点一样」：10 万个任务里如果有 3 万个都在考「某个部件缺失」，
那么 verifier 层级分布（90_local_experiments.md §4.1 的 L1 6 / L2 8 / L3 2）就是一个**现成的粗粒度 L-spec 监控**。

#### 3.1.3 阈值怎么定：抄数字之前必须做的一件事

公开实践里的数字（表里的值可以当起点，但**不能直接照抄**）：

| 来源 | 判据 | 阈值 | 去重比例 |
|---|---|---|---|
| Lee et al. NearDup [2107.06499](https://arxiv.org/html/2107.06499) | **5-gram，9000 签名，b=20 × r=450** | s=0.75 → 76% 命中、s=0.8 → 99.4% | C4 3.04%、RealNews 13.63%、LM1B 4.86% |
| RefinedWeb [2306.01116](https://arxiv.org/html/2306.01116) | 同上参数 | 同上（**故意不做二次校验，只要召回**） | MinHash 后再 ExactSubstr，再降约 40% |
| FineWeb [2406.17557](https://arxiv.org/html/2406.17557) | 5-gram，**签名只有 112**，8 × 14 桶 | 0.7→56%、0.75→77%、0.8→92%、0.85→98.8% | 见 3.1.4 |
| **The Stack v1** [2211.15533](https://arxiv.org/html/2211.15533) | 非字母数字切词、丢 <10 token，**256 permutations** | **Jaccard > 0.85** | **38.6% 文件 / 53.7% 体积** |
| **StarCoder2 / Stack v2** [2402.19173](https://arxiv.org/html/2402.19173) | **5-gram** | **Jaccard 0.7** | 原始 67.5 TB → 训练集约 900B+ token |
| CodeParrot | MinHash 建簇 + 精确 Jaccard 归约 | **0.85** | 0.1% 唯一文件占全部文件的 15% |
| OpenCoder / RefineCode [2411.04905](https://arxiv.org/html/2411.04905) | 5-gram，**2048 签名**，128 × 16 bands | 由 b/r 隐含 | SHA256 阶段约 **75% 文件完全重复**；fuzzy 再去 6% 体积 |
| text-dedup 默认 | ngram=5，num_perm=240 | threshold=0.7，**开 false-positive 校验** | — |
| **Allamanis 的代码判据** [1812.06469](https://arxiv.org/html/1812.06469) | identifier + literal token 的集合 T0 与多重集 T1 | **J(T0) ≥ 0.8 且 J(T1) ≥ 0.7**；token ≤ 20 的文件直接排除 | 被后续大量沿用 |

**banding 的 S 曲线**：`P(命中) = 1 − (1 − s^b)^r`，近似阈值 `t ≈ (1/r)^(1/b)`。
各家 b/r 命名互换，但乘积 = 签名长度。

**num_perm 不能照抄 128**（datasketch 官方实测）：

| 语料形态 | num_perm=128 的精度/召回 | 查询耗时 |
|---|---|---|
| 「少量孤立近重复」 | **P、R 在所有 num_perm 下都是 0.92~1.0** | 约 0.03 ms，比线性扫描快 100 倍以上 |
| **「大片高度重叠的同族」** | **P 0.69~0.77，R 0.69~0.84** | 0.4~1 ms，只快约 6 倍 |

**我们的任务集属于后者**（同模板换种子就是高度重叠的同族）。所以要么上
**256~512 permutations**（开销只多 10%~35%），要么必须加精确 Jaccard 的二次复核。
十万量级两者都负担得起。另外 datasketch 官方提醒：
在聚类型语料上**精度不随 num_perm 单调改善**，而是跟着优化器解出的离散 (b, r) 台阶走。

### 3.2 视觉去重

#### 3.2.1 公开阈值表（最该抄的一张）

| 来源 | 度量 | 阈值 | 效果 |
|---|---|---|---|
| imagededup 默认（哈希） | pHash/dHash，64 bit | **max_distance_threshold = 10**（区间 0~64） | 精确副本集 d=0 时 **P=R=1.0**；变换类近重复 d=10 时 precision 只有 0.341 / recall 0.079；d=32 时 recall 0.847 但 **precision 0.003** |
| imagededup 默认（CNN） | MobileNetV3 余弦 | **min_similarity_threshold = 0.9** | 近重复集 cos 0.9 → P 0.995 / R 0.127；cos 0.5 → R 0.999 / **P 0** |
| **imagededup 官方结论原文** | — | — | 「**Hashing methods do not perform well for finding near duplicates**」；精确重复用 dHash d=0，近重复用 CNN cos 0.5~0.9 |
| phash.org 官方设计文档 | DCT hash 64 bit | T = 22 | — |
| **Meta PDQ 生产常量** | PDQ 256 bit | **31**（占 12.1%） | `PDQ_CONFIDENT_MATCH_THRESHOLD` |
| Prokos et al. [2106.09820](https://arxiv.org/html/2106.09820) | pHash / aHash / dHash / PDQ | pHash **6 / 10 / 14**；aHash 3/5/7；dHash 4/9/12；PDQ 70/85/90 | 1.18M ImageNet 图上 FPR：**pHash T=6 约 0.044%，T=14 飙到 73%**；aHash T=3 已 3.9%（任何阈值都不堪用） |
| COYO-700M | pHash | **0（完全相同）** | 生产数据集的实际选择 |
| **DataComp 对评测集去重** [2304.14108](https://arxiv.org/html/2304.14108) | ISC 冠军 copy-detection descriptor（**不是 CLIP**） | **余弦 > 0.604169** | 标记 16.8B 图的 3%；该阈值对应 precision 0.9 / recall 0.8。**CLIP ViT-B/32 同 precision 需阈值 0.96 而 recall 只有 0.02** |
| DataComp 池内自去重 | 压缩 CLIP ADC | T_ADC 0.1 / 0.2 / 0.5 | 下游「与只用 CLIP filter 基本相同」——**池内自去重在 DataComp 上无额外收益** |
| **DINOv2 自去重** [2304.07193](https://arxiv.org/html/2304.07193) | **SSCD** 余弦，k=64 NN + 连通分量 | **> 0.6** | 1.3B → 1.1B（**−15.4%**） |
| DINOv2 对评测集去重 | 同上 | **> 0.45**（更严） | 1.1B → 744M（**−32.4%**） |
| **SSCD 官方推荐** | sscd_disc_mixup 余弦 | **> 0.75** | DISC 上 90% precision（等价 euclidean < 0.7） |
| Somepalli 2022/2023 | SSCD 余弦 | **0.5**（判复制，= top 1.88 百分位）/ 0.7（LAION 近同簇）/ 0.95（数据集内重复） | SD2.1 生成 100K 中 1.2% 超 0.5 |
| Carlini et al. [2301.13188](https://arxiv.org/html/2301.13188) | CLIP 选候选 + tiled modified ℓ2 | **δ=0.15 判抽出；δ=0.1 判 eidetic 记忆**；clique ≥ 10/500 | 175M 生成图中 50 张记忆图 **0 误报**；记忆集中在重复 k ≥ 100 次的样本 |
| 同上 CIFAR-10 消融 | imagededup CNN 余弦 | **> 0.85** | 删 10.55%，重现训练样本 1,280 → 986（**仅降 23%**） |
| **MONET**（1 亿级生产集）[2605.21272](https://arxiv.org/html/2605.21272) | pHash d=0 清精确 + **SSCD ≥ 0.75** | 0 / 0.75 | 累计 −7.7%。**实证 pHash 不可靠：真近重复可达 d=26，而 d=1 存在语义无关的假阳性簇** |
| LAION-400M / 5B 自身 | **只有 URL ⊕ alt-text 的 bloom filter** | — | **没有图像内容哈希、没有 embedding 去重、没有对评测集去重**；datasheet 明说存在近重复 |
| CLIP 原论文重叠分析 | 自训 near-dup detector | 每个评测集人工设阈值 | 重叠率中位 2.2% / 均值 3.2% / 最大 Country211 **21.5%**；整体精度变化很少超 0.1% |

**明确未找到**：`pHash Hamming ≤ 5` 或 `≤ 8` 作为公开论文或库的推荐值 —— 查不到权威出处。
`imagehash` 官方 README 不给推荐值。所以**别说「业界通常用 pHash ≤ 5」**，那是传说。

#### 3.2.2 阈值必须随库规模重标 —— 这是最容易踩的坑

ISC2021 实测（[2106.09672](https://arxiv.org/html/2106.09672)）：
**库从 100 万涨到 1,000 万，同一阈值下 recall 不变而 precision 从 0.8 跌到约 0.29。**

所以照抄任何数字之前，必做 MONET 的那一步：**按 0.05 分箱人工抽检**。
十万量级下这件事只要几十条样本就能定，别省。

#### 3.2.3 对我们的具体选型

| 决定 | 理由 |
|---|---|
| **第一层：对 9 视角剪影图做 dHash，d = 0** | 只清精确重复，对标 COYO-700M。我们的剪影图是程序渲的、确定性的，d=0 能抓到「完全同构场景」，而 d>0 会误并（MONET 实证 d=1 就有语义无关假阳性簇） |
| **第二层：不用 CLIP / SigLIP** | DataComp 实测 CLIP ViT-B/32 在 precision 0.9 时 **recall 只有 0.02**；12_self_verification.md 已记 SigLIP 在 10 个 3D 模型上全落 0.077~0.108 窄带 |
| **第二层改用：L-near 的 20~40 维几何特征向量**（见 3.1.2） | 本机探针已经产出这些量，零额外成本，而且它们**本来就是 verifier 的判据**，所以「去重指标」和「判别力指标」口径一致 |
| **第三层（可选）：SSCD 余弦 ≥ 0.75** | 如果非要上视觉 embedding，用 SSCD 而不是 CLIP/DINO —— 它是**专为 copy detection 训的**，官方 0.75 对应 90% precision，MONET 在 1 亿级生产环境也用 0.75 |
| **第四层：L-spec 的断言集合 Jaccard ≥ 0.9** | 抓「考的点重复」，这是程序化生成最容易塌缩的方向 |

### 3.3 需求文本去重

题干是程序化模板拼出来的短句，所以**精确匹配和 n-gram 几乎没用**（短 prompt 集精确匹配失效，
3JSBench 的 100 条短句就是这个毛病）。做法：

| 层 | 判据 | 阈值 |
|---|---|---|
| 1 | MinHash 5-gram，**num_perm = 256**（不是 128，见 3.1.3） | Jaccard ≥ 0.7（StarCoder2 口径），**开精确 Jaccard 二次复核** |
| 2 | 语义：句向量 k-means + 簇内余弦 | 对标 SemDeDup：**ε = 0.03（cos ≥ 0.97）判近重复**；[2303.09540](https://arxiv.org/html/2303.09540) 在图像上该阈值下 50% 有重复，删 37% 无损、删 50% ImageNet top-1 只降 0.47%（68.27 vs 68.74）、训练时间减半 |
| 3 | **题干 ∧ 产物联合判重**：题干近重复**且** L-near 近邻 → 判重；题干近重复但场景差很远 → **不判重，反而是好数据**（同一句话的多种实现） | — |

第 3 条是我们的特殊之处：**题干重复不等于任务重复。**
「桌面上放一个杯子」这句话可以对应无穷多种具体几何，
而 spec.json 里钉死的字段才决定任务是否相同。

### 3.4 与公开 benchmark 去重

#### 3.4.1 各家 decontamination 判据

| 系统 | 判据 | 结果 |
|---|---|---|
| **GPT-3** | **13-gram** 重叠（小写、空白分词、去标点）；删命中 13-gram 加前后 200 字符窗口；切成 >10 片的文档整篇删；**忽略命中 >10 个训练文档的 13-gram**（多为套话） | — |
| **PaLM** | **放弃纯 n-gram**，改人工把 29 个评测集分四类；对前两类切 clean vs contaminated 子集，判据是「题干/prompt/target 中 **≥70% 的 8-gram** 在训练数据出现过至少一次」 | clean 子集的正负 delta 数量相当 |
| **Llama 2** | **token 级 10(+)-skipgram**，在分词后的完整 verbalized 样本上匹配；允许 skipgram budget 4 个 token。分级 clean <20% / not clean ≥20% / not dirty <80% / dirty ≥80% | 只有 HellaSwag 与 MMLU-Humanities 被污染抬分；**70B 受益大于 7B** |
| **Llama 3** | **8-gram**；「样本中有比例 T_D 的 token 属于某个在预训练语料出现 ≥1 次的 8-gram」即判污染；**T_D 逐数据集单独选，取能让「估计性能增益」最大化的值** | 见下 |
| **GPT-4** | 子串匹配，训练与评测都去空格符号、只留字符含数字；每条评测样本随机取 **3 个 50 字符子串**，任一命中即污染 | HumanEval **25% 污染**，去污后 67.0% → 65.58%；DROP 约 21% 污染但 degradation 0；另发现 BIG-bench 被误混入训练集，整个排除 |
| **Dolma** | 段落级 Bloom filter 精确匹配，段落须 >13 个 Unicode token（防短段假阳性）；任一段落污染则整篇删 | 只删 0.003% 数据。**但事后 WIMBD 体检：6 个数据集 100% 污染**（Winograd、SICK、GLUE-AX、SemEval-2014-T1、COPA、SuperGLUE-AXb），HumanEval、WiC、ESNLI、SNLI >90%；**很多污染来自 code 子集**（GitHub 上常有数据集副本） |
| **FineWeb** | 全文只提 decontamination 一次，且是说**对 Paloma 故意不做去污** | 论文未记载任何 benchmark 去污步骤 |
| **The Pile** | **明确拒绝做 decontamination**，理由是「无法预判所有下游评测，任何选择都会过时或妨碍新 benchmark 的开发」 | — |
| **The Stack v2 / StarCoder2** | 删包含 HumanEval/MBPP 的 docstring 或 solution、APPS docstring、GSM8K 题目、DS1000 prompt 的文件；比 v1 多了「字符串匹配时去空白」提召回 | **Stack v1 实测：python-all-license 近重复后仍有 291 个 HumanEval 污染文件** |
| **Platypus** [2308.07317](https://arxiv.org/html/2308.07317) | ①精确重复删 ②SentenceTransformers **余弦 > 80%** 内部去重 ③对 benchmark 题目余弦 > 80% 的**全部人工三分类**：duplicate / gray-area / similar-but-different，**三类全删** | 泄漏题数：PRM800K 77、MATH 77、SciQ 71 |
| **infini-gram mini** [2506.12229](https://arxiv.org/html/2506.12229) | 评测条目的全部 **50 字符子串**（stride = 一个词），η = 在语料中出现过的占比；沿用 Llama 2 分级 | 对 DCLM-baseline：MMLU **27.70% dirty**、ARC-C 32.6%。**新集子随时间被污染**：AIME-2024 在 Pile/DCLM 上干净，在 CC-2025-21 上 **40% dirty**；GSM8K 在 CC-2025-21 上 **74.2% dirty** |

**Llama 3 Table 15 节选**（污染率 % / 8B / 70B / 405B 估计性能增益）：

| Benchmark | 污染率 | 8B | 70B | 405B |
|---|---|---|---|---|
| AGIEval | 98% | 8.5 | **19.9** | 16.3 |
| BIG-Bench Hard | 95% | 26.0 | 36.0 | **41.0** |
| HellaSwag | 85% | 14.8 | 14.8 | 14.3 |
| GSM8K | 41% | 0.0 | 0.1 | 1.3 |
| MATH | 1% | 0.0 | −0.1 | −0.2 |
| **MMLU / MMLU-Pro / HumanEval / MBPP / DROP / RACE** | — | **全部报不出** | | |

**Llama 3 自己的结论**：对 MBPP、HumanEval、MMLU、MMLU-Pro，
**即使提高阈值，8-gram 重叠给出的污染率也高到无法得出任何可用的性能增益估计，需要换方法。**
这是 n-gram 去污在代码类 benchmark 上失效的官方承认。

#### 3.4.2 n-gram 挡不住改写：LMSYS 的硬证据

[2311.04850](https://arxiv.org/html/2311.04850)：让 GPT-4 改写测试题（循环改写直到 n-gram 检测不到），再微调模型。

| 实验 | 原始分 | 改写样本上微调后 |
|---|---|---|
| MMLU / Llama-2-13B | 54.8 | **89.9** |
| **HumanEval pass@1 / CodeLlama-13B** | 36.0 | **81.1**（GPT-4 只有 67.0） |
| HumanEval / CodeLlama-7B | 32.9 | 67.7 |
| GSM-8K / Llama-2-13B | 28.7 | **95.3** |

检测方法的 F1（200 对）：

| 方法 | 原测试集 | 改写英文 | 改写中文 | 改写 Python | 改写 C |
|---|---|---|---|---|---|
| **10-gram 重叠** | 0.816~1.0 | **0** | **0** | **0** | **0** |
| Emb (Multi-QA BERT, 阈值 0.5) | 0.98~0.995 | 0.805~0.985 | **0~0.179** | 0.938 | 0.774 |
| **LLM Decontaminator**（top-k embedding 召回 + GPT-4 逐对判定） | **1.0** | 0.940~0.970 | 0.950~0.990 | 0.995 | 0.974 |

**嵌入阈值不可统一的直接证据**：阈值 0.8 时 Abstract Algebra 能抓到但 Sociology 的改写漏掉；
阈值 0.4 时 Abstract Algebra 大量假阳性。

真实数据集里的改写污染率（GPT-4 判定）：
**The Stack 对 HumanEval 18.9%（31/164）**、StarCoder-Data 15.9%、CodeAlpaca 12.8%、
RedPajama-1T 8.5%、MATHInstruct 对 MATH test **15.4%（769/5000）**。
**注意最后两条口径：合成数据（GPT-3.5/4 生成的）也会无意污染。**

#### 3.4.3 时间切分

| 系统 | 做法 | 实证 |
|---|---|---|
| **LiveCodeBench** [2403.07974](https://arxiv.org/html/2403.07974) | 滚动抓周赛题并打 release date；对每个模型只评「训练截止日之后」的题 | DeepSeek-Ins-33B 在 2023-08 之后性能陡降；GPT-4-O 在 2023-11（其官方 cutoff）之后陡降。**该跌落只出现在 LeetCode 题上，AtCoder 题跨月份基本平稳**。作者明说「先前的精确+模糊匹配去污是非平凡的，且改写就能绕过」 |
| **SWE-bench** [2310.06770](https://arxiv.org/html/2310.06770v3) | ① 训练集与评测集的仓库**完全不交叠（repo-disjoint，而非 instance-disjoint）** ② 只评模型训练日期之后创建的 issue | oracle 检索下按 2023 年切分：GPT-4 1.96% → **0.0%**；Claude 2 4.87 → 4.23；ChatGPT-3.5 0.49 → 0.77。**只有 GPT-4 有明显跌落** |

#### 3.4.4 要和哪些公开集去重：黑名单可行性分级

| 级别 | Benchmark | 规模 | 清单可得性 | 做法 |
|---|---|---|---|---|
| **A（直接下载做黑名单）** | **3JSBench**（3jsbench.com，benchmark.json 627 KB，taskCount=100，MIT） | 100 | **全量可下**，逐条含 id/prompt/caption/tier/parts/checks | 精确 + 模糊双拉黑 |
| A | **ArtifactsBench** [2507.04952](https://arxiv.org/abs/2507.04952) | **1,825** | 全量可下（含 question/checklist/class/difficulty，无 answer），**CC-BY-NC-4.0 非商用** | 同上 |
| A | **BenchCAD** [2605.10865](https://arxiv.org/html/2605.10865) | **17,900** 条执行校验过的 CadQuery 程序 / 106 零件族 | 全量可下，CC-BY-4.0 | **程序级指纹最好做** |
| A | **PRISM** [2605.19382](https://arxiv.org/html/2605.19382) | **10,372** instruction-code 对 | 全量可下，Apache-2.0 | 同上 |
| A | **Animation2Code** [2606.28593](https://arxiv.org/html/2606.28593) | 1,069（train 769 / val 86 / test 214） | 全量可下，CC-BY-4.0 | 同上 |
| A | Design2Code / Web-Bench / Web2Code / Interaction2Code / WebSight / SWE-bench / BigCodeBench / HumanEval / MBPP / ChartMimic / Plot2Code / OmniDocBench | — | 全量可下 | 同上（OmniDocBench 的匹配键是**图像指纹不是文本**） |
| **B（部分拉黑 + 时间切分补）** | **WorldCoder-Bench** [2606.01869](https://arxiv.org/abs/2606.01869) | 论文称 2,026，仓库实际 **2,004**（core_205 + hf_snapshot_1799），**差 22 条未公开** | 近全量，每任务 task.json + icg.json；dev_rubrics 只给 5 条；另有 hidden behavioral contracts | 拉黑 2,004 条，缺的 22 条按 id 前缀/主题模糊封一圈 |
| B | **ManiBench**（官方拼写，不是 ManimBench）[2603.13251](https://arxiv.org/abs/2603.13251) | 口径不一致：摘要称 150~200 题，HF 上实际只有 **12 题** pilot | 部分 | 靠 PRISM 的同域 Manim 语料顺带覆盖（PRISM 大 800 倍） |
| B | WebBench（Halluminate × Skyvern） | 全量 5,750，开源 **2,454** / 452 站点 | 开源部分可下 | 其余按 452 个站点域名规避 |
| **C（做不了黑名单）** | **WebCoderBench** [2601.02430](https://arxiv.org/html/2601.02430) | 1,572 真实用户需求 | **不可得**。Limitations 明确：真实用户需求 + 法务限制，数据集与评测代码**均不发布**，并把不公开当作防刷分手段 | 唯一办法是训练语料时间截断在 2026-01-05 之前；但它来自真实用户需求而非公网文档，**时间切分也不保证干净，必须当黑盒信任** |
| C | **WebDev Arena** | 活体榜 288,203 票 / 77 模型；公开 dump 仅 10,501 行 | **活体池永不公开** | 只能拉黑那份 10k dump，2025-02 之后的新 prompt 无法规避 |
| C | **LiveCodeBench** | v1 400 / v2 511 / v3 612 / v4 713 / v5 880 | 全量可下 | **设计上就该走时间切分**；拉黑题面反而会误伤大量正常的 LeetCode/AtCoder/Codeforces 题 |

**两条跨集通用的坑**：

1. **多数前端/文档类集子的题目本身来自公网**（C4、CodePen、GitHub Pages、公开 PDF），
   **只拉黑 benchmark 仓库不够，必须把源 URL / pen-id / arXiv-id 一起进黑名单**
   （Design2Code、Animation2Code、Interaction2Code、OmniDocBench、ChartMimic 都受此影响）。
   **这对我们尤其致命**：§4 的真实素材路线正是从 CodePen / GitHub 挖的，
   所以「素材源 → benchmark」的交集必须在抓取阶段就查，不是在训练前查。
2. **短 prompt 集精确匹配几乎没用**（3JSBench 100 条短句、Plot2Code 132 条），
   只能走域名/仓库级规避 + 人工抽检。

#### 3.4.5 我们的去污协议（三道闸）

```
闸 1（抓取时）素材源 URL / pen-id / repo+path 黑名单
   覆盖 A 类 benchmark 的全部源素材清单。成本：一次性建表，之后是 O(1) 查询
闸 2（造题后）题干 + 代码 + 场景图指纹三路对 A/B 类 benchmark 做
   ① n-gram：50 字符子串 stride=一词（GPT-4/infini-gram mini 口径），阈值 η < 20% 判 clean
   ② embedding 召回 top-k=10 + LLM 逐对判定（LMSYS 的 LLM Decontaminator，F1 0.94~1.0）
   ③ 场景图 L-exact 哈希直接比（这一路是我们独有的，且对改写免疫）
闸 3（发布时）时间切分：所有真实素材按 commit / pen 创建时间排序，
   最近 N 个月整段留出做评测，不进训练
```

**第 ③ 路是我们相对文本/代码数据集的结构性优势**：
场景图哈希比的是**产物的几何**，改写代码、换语言、换实现路径都不影响它。
LMSYS 证明 10-gram 对改写的 F1 = 0，但**改写不可能在保持几何不变的同时绕过场景图哈希**
——因为如果几何变了，那就不是同一道题了。

### 3.5 去重会过头：必须记住的反面教训

**FineWeb 的实测**（[2406.17557](https://arxiv.org/html/2406.17557) §3.4）：

| 做法 | 结果规模 | 下游 |
|---|---|---|
| **全局去重**（96 个 CC 快照迭代互相去） | 15T → **4T** token，最老快照被删掉 **90%** | **相比不去重几乎没有提升**，远落后 RefinedWeb |
| 逐快照独立去重 | **20T** token | 持平 RefinedWeb，且逐步过滤均有提升 |

作者解释：收益来自删掉「跨全部快照、动辄几十万文档的**巨型重复簇**」；
对只有几十个副本的小簇继续去重**反而有害**，被保留下来的是长尾低质数据。
对照实验：2013-48 快照「全局去重后留下的 31B token」训出来**不如**「被删掉的那 460B 单独去重后的 171B token」。

**DataComp 的同向证据**：池内自去重（T_ADC 0.1/0.2/0.5）下游「与只用 CLIP filter 基本相同」——**无额外收益**。

**对十万量级任务集的直接含义**：

| 该做 | 不该做 |
|---|---|
| 定位并打掉**巨型同构簇**（同模板 + 同种子族 + 同 spec 的大片任务） | 无脑拉高召回去清小簇 |
| 对公开 benchmark 去污（这一路**只有收益没有损失**） | 把「去重率」当 KPI |
| 保留「题干近似但几何差很远」的对（见 3.3 第 3 条） | 按题干相似度一刀切 |

### 3.6 去重的收益有多大：别人的数字

| 证据 | 数字 |
|---|---|
| **The Stack 代码近重复去重**（最硬的一条） | permissive 子集 HumanEval pass@100 **27.21% → 37.00%**；MBPP **44.99% → 54.69%**；all-license HumanEval 36.67 → 44.00 |
| RefinedWeb 消融（零样本均值） | OSCAR-22.01 52.7 → **55.6（+2.9）**；The Pile 53.4 → 54.5（+1.1）；C4 **+0.2**（本来就干净） |
| Lee et al. 记忆率 | 无 prompt 下逐字复现训练数据：C4-Original **1.93% → NearDup 0.19% → ExactSubstr 0.14%**（约 10 倍） |
| **Allamanis「代码重复的恶果」** [1812.06469](https://arxiv.org/html/1812.06469) | 不去重会让指标**虚高最多 100%**。JavaScript-150k 语言模型 Acc 55.1 → 去重后 49.1（−10.9%），**只看标识符的 Acc-ID 17.7 → 8.6（−51.4%）**；code2vec 方法命名 F1 50.98 → 44.71；JsNice 变量命名 55.04 → 34.44（−37.4%）。重复率：Concode-Java 68.7%、Java GitHub Corpus 24.8% |
| **重复数据的「双下降」** [2205.10487](https://arxiv.org/html/2205.10487) | 训练 token 中**仅 10% 是重复**，在最坏的重复次数（800M 模型约 100×）下，**性能退化相当于模型缩小 2 倍**；3% 重复数据可让 copying 评测掉 3 倍 |
| SemDeDup [2303.09540](https://arxiv.org/html/2303.09540) | 删 37% 无损；删 50% ImageNet top-1 仅降 0.47%（68.27 vs 68.74），**训练时间减半**；保留 63% 时反而超基线、预训练快 1.6 倍。**去重开销 < 训练 GPU 时的 1%** |

**最后这条是整节的理由**：去重开销不到训练成本的 1%，而不去重的代价是「10% 重复 token ≈ 模型缩小 2 倍」。

## 4. 从真实素材放大

02_task_sources.md 已经盘过来源清单，这里只做**规模化角度的增量**：管线每步保留率、以及真实与合成的配比证据。

### 4.1 素材池：名义规模 vs 真·可用规模

| 素材域 | 名义池 | 真·可用池 | 收缩 | 口径 |
|---|---|---|---|---|
| three.js 代码仓库 | `q=three.js` **89,622** / `topic:threejs` **23,983** | `topic:threejs stars:>10` **2,401** | **约 37 倍** | 【实测】GitHub search API |
| **three.js 官方 examples** | — | **610 条，1:1 带参考截图** | — | 【实测】见下 |
| bpy 脚本仓库 | `q=blender addon` 6,307 / `q=bpy` 1,299 | `bpy language:Python stars:>10` **56** | **约 10~100 倍** | 【实测】 |
| CodePen | 1,000 万 pen（**2016-11** 官方数字，此后无更新） | 公开 dump 约 **2.5 万**，**无列举/搜索 API** | **约 400 倍** | 【公开 + 外推】 |
| ShaderToy | >52,000（2021 年中） | **shaders21k 的 21,083**；官方 API 镜像 `Vipitis/Shadertoys` **已 gated 下架** | 约 2.5 倍 | 【公开】 |
| 3D 资产（Objaverse-XL） | 元数据 **10,850,997** 行 | **只有 5.5M 能被 Blender 成功导入渲染**；商用可用 CC 约 **1.9M** | 约 5.7 倍 | 【公开 + 实测】 |

**three.js 官方 examples 的精确盘点**（走 git tree API，`truncated=false`，全树 6,413 条）：

| 项 | 数字 |
|---|---|
| `examples/*.html`（扣掉 index.html） | **610** |
| 其中 `webgl_*` / `webgpu_*` / `webxr_*` / `misc_*` | 298 / 234 / 27 / 23 |
| `examples/screenshots/*.jpg` | **610** |
| **code ↔ screenshot 配对率** | **610 : 610 = 1 : 1** |
| 单条体积 | 中位 **6,137 字节**（约 150~200 行）；p95 13,651；最大 66,143 |
| 全部 examples 总体积 | 4.4 MB |
| `examples/jsm/*.js`（addon API 面） | 496 |
| `src/*.js`（核心 API 面） | 755 |

**读法：610 条是种子池的天花板，不是规模池。** 中位 6 KB、天然带参考图，
适合当 §6 的 S0/S1 阶段的种子和 API 覆盖率的参照（496 + 755 = 1,251 个 API 面，
可以用来算「我们的 10 万任务覆盖了多少 three.js API」这个多样性指标）。

**两个抓取硬约束**（实测）：
- GitHub **文件级 code search 必须带 token**（未认证 401），所以「多少个 .py 含 `import bpy`」这个数**拿不到**，只能用仓库级口径。
- ShaderToy **整站对海外出口 403**（`/api/v1/shaders`、`/terms`、`/about` 三条路径全 403），许可只能靠二手口径。

### 4.2 管线每步保留率：公开漏斗 + 我们的类比估计

#### 4.2.1 代码/仓库线（SWE 系，公开数字）

| 管线 | 起始 | 关键步 | **总保留率** | 最终 |
|---|---|---|---|---|
| **SWE-bench** [2310.06770](https://arxiv.org/html/2310.06770v3) | 12 仓 / 爬 **93,139 PR** | attribute filter → 11,407（12.25%）；执行校验（≥1 条 F2P）→ 2,294（占上步 20.1%） | **2.46%** | 2,294 |
| **SWE-bench Verified** | 2,294 | 抽 1,699 条人工标注，每条 3 名标注员；判废 **68.3%**（问题欠规约 38.3% + F2P 误杀正解 61.1%） | **21.8%**（500/2,294） | 500 |
| **SWE-Gym** [2412.21139](https://arxiv.org/html/2412.21139) | 358 仓 → **64,689** 条 | 只留 11 个仓 + 人工配依赖 + 执行校验 | **3.77%** | 2,438（约 200 人工小时 + **10,000 CPU core-h**，镜像 6 TB） |
| **SWE-smith** [2504.21798](https://arxiv.org/html/2504.21798v2) | 128 仓 → **100,074 个 bug 候选** | 执行校验（打 patch 必须打断 ≥1 条原通过测试） | **50.1%** | 50,137（约 20 人工小时、**1,360 美元**、环境存储 **295 GB**） |
| **SWE-rebench** [2505.20411](https://arxiv.org/html/2505.20411) | 约 10M PR → 下载约 450,000 | match 约 5% → filter 约 33%（153,400）→ **install & validate 约 14%** → annotate 约 100%；**只有 31% 的仓库能装成至少一个任务** | **4.74%**（以 450K 为分母） | 21,336 |
| **CodeContests** [2203.07814](https://arxiv.org/html/2203.07814) | 原始 hidden test **12.4 条/题** | mutation 造测试，用 30 份正确解跑、输出全一致才留；每题上限 10 CPU 小时或 200 条；**6.3% 的题凑不满** | 测试 **12.4 → 203.7 条/题（16.4×）**；**假阳性 62% → 4%** | train 13,328 |

**SWE-smith 各合成策略的 yield 差 52 倍**（这是最该抄走的细节）：

| 策略 | yield |
|---|---|
| Combine(file) / Combine(module) | 97.43% / 96.16%（**但只组合已验证 patch，不产生新信息**） |
| **LM Modify（让模型「造 bug」）** | **55.98%** |
| Ctrl Invert-If / Remove Assign / Procedural Rm-Funcs | 49.44% / 48.65% / 47.09% |
| **LM Rewrite（让模型「重写函数」）** | **35.04%** |
| PR Mirroring | 33.80% |
| Op Change / Op Swap | 29.86% / 22.56% |
| Class Shuffle Funcs | **1.88%** |

→ **让模型造 bug（55.98%）比让它重写函数（35.04%）高 21 个点。**
本机 gen_tasks.py 走的正是「造 bug」这一路（LLM 提语义性破坏），实测 88%~96% ——
**比 SWE-smith 高得多，因为我们的 verifier 是程序化多层的，不依赖已有单测。**

#### 4.2.2 网页 / shader 线（和 three.js 最像的类比对象）

| 数据集 | 原始素材 | 每步 | **总保留率** | 最终 |
|---|---|---|---|---|
| **Design2Code** [2403.03163](https://arxiv.org/html/2403.03163) | C4 validation 全部网页 **127.9k** | 长度/内容/去重三步 → 14k（**10.9%**）→ 剥依赖、换占位图 → 从 14k 采 7k，**前两位作者逐条人工检查** → 484（占 7k 的 **6.9%**） | **0.38%** | 484 |
| **WebCode2M** [2404.06369](https://arxiv.org/html/2404.06369v2) | CC 一个 segment 随机采约 **0.5B 页** | 长度过滤 → Playwright 渲染（**占总耗时约 80%、历时约 1 个月**）→ **神经打分器 score<2 剔掉 = 52.5%，保留 47.5%**（唯一公开的单步比例）→ 截图 hash 去重 | **约 0.5%** | 训练 2,563,905 |
| **WebSight** [2403.09029](https://arxiv.org/html/2403.09029v1) | **不是爬真实网页，是 LLM 从头合成** | 概念 → 写 HTML → 丢弃图文不符 → Playwright 截图 | 丢弃比例**未报告** | v0.1 822,987 → v0.2 1,922,671 |
| **ShaderMatch / ShaderEval** | **202k 未过滤函数池** | 只留「已发布到 API + 宽松许可」（scancode 标 SPDX） | **约 0.23%** | **467**（v0.2 257 → v0.3 394 → 467） |

#### 4.2.3 3D / Blender / three.js 已有 benchmark 的构造漏斗

| Benchmark | 起始 | 保留 | 最终 |
|---|---|---|---|
| **BlenderGym** [2504.01786](https://arxiv.org/pdf/2504.01786) | 手工搭 | — | **245** 实例（每实例含 base .blend + start/goal 两份 Python + 两份渲染图 + 差异描述） |
| **BlenderLLM / BlendNet** [2412.14203](https://arxiv.org/html/2412.14203v1) | **135 条手写 seed instruction** | self-instruct 扩到约 **50k** → GPT-4o 写 bpy → 四视角渲染 → GPT-4o 判图文一致 → 人工复核 10k 条（与 GPT-4o 一致率 **89.7%**，**人工池通过率只有 20%**） | **约 16%** → BlendNet **8k** |
| **3DCodeBench** [2606.01057](https://arxiv.org/html/2606.01057v1) | **Infinigen 的 243 个 procedural factories**（其中 212 带随机种子） | 代码简化 → Blender 5.0 沙箱执行 → 视觉 critique → mesh 分析 → 人工审核 | 各步剔除率**未找到** | 语料 **12,963** 实例，评测集 212 |
| **WorldCoder-Bench** [2606.01869](https://arxiv.org/html/2606.01869v2) | 5 位 3D 图形 PhD 手工做 seed（耗时 2 个月） | LLM 辅助扩到 **>10,000** 候选 → 人工剔歧义/过易/欠定义/无法转成确定性 runtime check → 无头浏览器验资产与接口 → 专家写 behavioral contract，执行不稳的剔除 | **≲20%** | **2,026**（Core 205 隐藏 + Extended 1,621 + Dev 200）；SOTA 最好 Core **27.8%** |

#### 4.2.4 我们的 three.js / bpy 管线：类比估计

**整列都是估计**（公开数字已在上面列明，这里是外推）：

| 过滤层 | 公开可参照的保留率 | **我们的估计取值** | 为什么 |
|---|---|---|---|
| 粗筛（长度/结构/去重） | Design2Code 10.9% | **30~60%** | 代码线比网页线干净得多 |
| 自动质量打分 | WebCode2M 打分器 **47.5%** | **40~50%** | 直接套用 |
| **环境/渲染可执行（最大瓶颈）** | SWE-rebench install&validate **约 14%**，仓库级成功率 31%；SWE-bench 执行校验 20.1%；Objaverse-XL「能进 Blender」**5.5M/37M ≈ 15%** | three.js **50~80%**；bpy **15~30%** | three.js 环境统一（一个无头浏览器全搞定），比装 Python 依赖容易得多；bpy 跟 Blender 版本 + addon 强绑定，Objaverse-XL 的 15% 是同类问题的实测锚点 |
| 人工逐条确认 | Design2Code **6.9%**；BlenderLLM 人工池 **20%**；SWE-bench Verified **31.7%** | **7~30%** | 取决于是不是真要人看每一条 |
| **端到端（真实挖矿）** | SWE-bench 2.46% / SWE-rebench 4.74% / SWE-Gym 3.77% / Design2Code 0.38% / WebCode2M 约 0.5% / ShaderMatch 0.23% | **three.js 1~8%；bpy 0.3~2%** | 文献的经验带宽是 0.2%~5% |
| **端到端（合成/变异）** | SWE-smith **50.1%** / BlenderLLM 16% / WorldCoder-Bench ≲20% | **本机实测 88~96%** | 我们的 verifier 不依赖已有单测，所以比 SWE-smith 高 |

**三条结论**：

1. **真实挖矿的天花板是 2~5%，瓶颈不在筛选而在「能不能跑起来」。**
   SWE-rebench 自己点名 install & validate 只有约 14%、仅 31% 的仓库能装成功。
   对 three.js 这是**好消息**（浏览器环境统一），对 bpy 是**坏消息**（Blender 版本 + addon 依赖）。
2. **合成/变异把 yield 抬约 20 倍（2.46% → 50.1%），而我们的实测是 88~96%，比 SWE-smith 再高一档。**
   所以 §5 的成本模型里真实素材那一路的性价比远低于程序化那一路。
3. **判据强度排序（从硬到软）**：
   shader 逐帧像素比对（ShaderMatch）> 运行时 behavioral contract（WorldCoder-Bench，不进 prompt）
   > mesh / 几何分析 + 沙箱执行（3DCodeBench）> 渲染截图的 VLM 打分（WebCode2M、Web2Code）。
   **three.js examples 的 610 组 1:1 code+screenshot 恰好只支撑最软的那一档** ——
   要上硬判据必须自己写 contract，这和本机的四/五层 verifier 是同一件事。

#### 4.2.5 从真实素材到任务的管线（本机口径的一步步保留率估计）

```
GitHub three.js 仓库（topic:threejs stars:>10）     2,401 个仓库   【实测】
  ↓ 抽单文件自包含页面（<script type="module"> 且无私有资产）  约 20%    【估】
  ↓ 无头浏览器能跑起来且渲出 >=1 个 mesh（L0 执行门）         约 60%    【估，锚 Objaverse-XL 的 15% 与 three.js 环境统一性】
  ↓ 能被 __THREE_DEVTOOLS__ 抓到 scene（本机实测 CDN/importmap/打包版都能）  约 95%  【半实测】
  ↓ 冻结时钟后两次渲染逐字节一致（否则不可验证）             约 70%    【估，06_harness.md §4.1.4 实测只有页面钩子能逐字节一致】
  ↓ 自动造题（LLM 提破坏）+ 三条准入                         约 90%    【实测 88~96%】
  ↓ 去重 + 可解性闸 + 难度带                                约 45%    【估，同 §5.2】
                                                 端到端约 3.2%
```

按每个仓库平均能挖出 3 个可用页面估，2,401 × 3 × 3.2% ≈ **230 个任务**。
**这就是真实素材路线的真实量级：三位数，不是五位数。**
它的价值不在产能，在**多样性注入**（真实的 API 用法、真实的视觉风格），所以配比应该按「多样性需求」定，不按产能定。

### 4.3 真实素材 vs 程序化合成的配比：有没有公开证据

#### 4.3.1 各家的配比说法

| 模型/数据 | 配比 | 口径 |
|---|---|---|
| **phi-1** [2306.11644](https://arxiv.org/html/2306.11644v2) | 过滤后真实 code-textbook 约 **6B token** : 合成教科书 **<1B** + CodeExercises **<180M** ≈ **6 : 1** | 【公开 + 外推】 |
| **phi-1.5** [2309.05463](https://arxiv.org/html/2309.05463v1) | 150B token = **80% 合成 + 20% phi-1 数据**；phi-1.5-web = 40% 过滤网页 / 20% 代码 / **40% 合成** | 【公开】 |
| **phi-3** [2404.14219](https://arxiv.org/html/2404.14219v4) | 两阶段，**任何阶段的真实:合成百分比都未给** | 【未找到】 |
| **Nemotron-4 340B** [2406.11704](https://arxiv.org/html/2406.11704v1) | 摘要原文「**over 98% of data used in our model alignment process is synthetically generated**」；人工只有约 20K 条（SFT 10K + HelpSteer2 10K） | 【公开】 |
| **Nemotron-CC** [2412.02595](https://arxiv.org/html/2412.02595v1) | 全量 6.3T = 4.4T 真实 + **1.9T 合成（30.2%）**；HQ 子集 1.1T ≈ 0.6T 真实 + 0.5T 合成（**约 45%**） | 【公开】 |
| **Llama 3** [2407.21783](https://arxiv.org/html/2407.21783v3) | 代码 SFT **>2.7M 条合成**（执行反馈约 1M + 回译约 1.2M），初始错误解约 **20%** 被执行反馈自修正；长上下文混 **0.1% 合成**；多语 SFT 里**翻译来的合成推理数据占 34.6%**。合成总占比的单一数字**未给** | 【公开 + 未找到】 |
| **AlphaGeometry** | **没有真实数据混合**，语言模型 from scratch。**Nature 摘要只说 "millions"，「1 亿」只在 DeepMind 博客** —— 引论文必须用 "millions" | 【公开】 |

#### 4.3.2 Nemotron-CC：唯一有对照组的大规模混合实证

| 实验 | 结果 |
|---|---|
| 低质文档改写（1T token 训练） | 平均 **+1.50 分** |
| HQ 的 8 个 epoch 里 **4 个换成合成**（HQ-Synthetic vs HQ-Base） | 平均准确率 **55.8 → 56.7**；作者归因「新鲜 token + 新文体」 |
| 1T token | MMLU **59.0** vs DCLM 53.4（+5.6） |
| 全量 6.3T | MMLU **53.0**（与 DCLM 持平） |
| 作者自述风险 | 承认改写可能引入错误信息，**未验证改写文本的事实准确性** |

#### 4.3.3 model collapse：有没有「安全上限」

| 来源 | 结论 | 性质 |
|---|---|---|
| **Shumailov et al.** [2305.17493](https://arxiv.org/abs/2305.17493) → Nature 631, 755–759（2024-07） | 「use of model-generated content in training causes **irreversible defects**」，**分布尾部先消失**。口径注意：设定是 **replace（每代替换）** | 实证 |
| **「Is Model Collapse Inevitable?」** [2404.01413](https://arxiv.org/abs/2404.01413) | **本题最硬的定理**。ridgeless 回归下：**accumulate**（累积真实 + 历代合成）误差 = σ²d/(T−d−1) · Σ_{i=1..n} 1/i² ≤ σ²d/(T−d−1) · **π²/6 ≈ 1.645**，**与迭代数 n 无关的有界上界**；**replace** 误差 = σ²d/(T−d−1) · **n**，随迭代数**线性增长**。作者定调「**data accumulation avoids model collapse**」，并明说这不只是「推迟」 | 理论 + 实证（TinyStories / GeoDiff / CelebA VAE 三处复现） |
| **「Self-consuming models go MAD」** [2307.01850](https://arxiv.org/abs/2307.01850) | synthetic augmentation（固定真实 + 每代追加合成）**"only delays"** 退化。**通用比例阈值论文明确不给**；给的是定性相变：「可容许的合成量 **does not increase with the amount of real data**」。论文里的 n_r=100 / n_s=900（真实 10%）只是示例设定 | 理论 |
| **「Beyond Model Collapse」** [2406.07515](https://arxiv.org/abs/2406.07515) | 「**verifiers, even imperfect ones, can indeed be harnessed to prevent model collapse**」；并导出一个不训练即可预判 verifier 是否有用的 proxy 度量 | 理论 + 实证 |
| **「Strong Model Collapse」** [2410.04840](https://arxiv.org/abs/2410.04840) | 最悲观侧：「even the smallest fraction of synthetic data (e.g., **as little as 1%** of the total training dataset) can still lead to model collapse」 | 理论 |
| [2404.05090](https://arxiv.org/abs/2404.05090) | 给出可避免崩塌的**最大合成量**显式上界：n ≤ 2πe⁻² · min[s−2, log(√2 π N ε /(6es))]，gloss 是「合成量应**对数级**于真实量」 | 理论（集中不等式，很保守） |

**综合判断：没有任何论文给出可直接搬用的「合成占比安全线」。** 文献给的是三条口径不同、看似矛盾的结论：

1. 最坏情况（2410.04840）：**1% 即可触发** —— 前提是**不筛选 + 替换式迭代**。
2. 理论上界（2404.05090）：合成量应**对数级**于真实量。
3. **决定性变量不是比例，是协议**：**accumulate 而非 replace**（2404.01413）
   + **verifier 筛选**（2406.07515）。这两条满足时，工程实测能做到 **30%~45% 合成仍为正收益**（Nemotron-CC）。

**对我们的直接含义 —— 这三条我们全部天然满足**：

| 文献要求的条件 | 我们的状况 |
|---|---|
| accumulate 而非 replace | 我们是**从零造任务**，不是「用模型输出再训模型再造」的自噬循环。模型生成的只有「破坏提案」和「题干措辞」，**标签来自程序化 verifier，不来自模型** |
| verifier 筛选 | 本机准入测试就是 verifier 筛选，88~96% 通过率，被弃的精确指出 verifier 盲区 |
| 合成占比 | 按 §4.2.5，真实素材路线只能出三位数任务，**所以我们必然是 95%+ 合成** |

**所以「配比」在我们这里不是 collapse 风险问题，是多样性问题。**
collapse 一线的理论对我们不直接适用（我们不做自噬迭代）；
真正适用的是 **HSSD-200 的 122 : 10,000** 那条结论。

#### 4.3.4 sim2real / 程序化生成的配比证据（这条才真正对口）

| 来源 | 结论 |
|---|---|
| **HSSD-200** [2306.11290](https://arxiv.org/html/2306.11290v1) | **122 个高保真场景打过 10,000 个程序化场景**（HM3DSem 零样本 19% vs 17%），**比例 1 : 82**。FID→HM3D：ProcTHOR 104.0 vs HSSD **88.2**。参考量：**两个真实集之间的 FID 只有 27.5** —— 真实到真实的距离远小于任何合成集到真实的距离 |
| 口径提醒 | 这是**合成 vs 合成**（高保真 vs 程序化）的样本效率对比，**不是**「多少合成 ≈ 多少真实扫描」；后者论文没给 |
| **Infinigen Nature** | **没有 real-data mixing 消融**。RAFT-Stereo 是「仅用 Infinigen from scratch」后零样本评测 |
| **Infinigen-Indoors** [2406.11824](https://arxiv.org/html/2406.11824v1) §4.2 | **唯一一个明确的混合消融**（阴影去除）：R = 仅真实 ISTD；R+S = ISTD + **2k 条合成**。内域 ISTD PSNR **34.13 → 33.80（略降）**；零样本 SRD PSNR **27.93 → 29.37（+1.44）**，RMSE 7.68 → 6.67，阴影区 PSNR 25.59 → 27.39（+1.80） |

**→ 程序化合成数据的收益形态是「内域略亏、跨域明显赚」。**

#### 4.3.5 配比建议（结论）

| 问题 | 答案 |
|---|---|
| 有没有公开证据支持某个具体比例？ | **没有。** 唯一能引的量化锚点是 HSSD-200 的 **1 : 82**（高保真 vs 程序化的样本效率），和 Nemotron-CC 的 **30%~45% 合成仍为正收益**（但那是文本预训练，域不同） |
| 那按什么定？ | 按**产能上限**定，不按理论比例定。§4.2.5 算出真实素材路线端到端只有约 3.2%、约 230 个任务，所以真实占比**客观上只能是 0.2% 量级** |
| 真实素材怎么用才值？ | ① 当**评测集**（时间切分留出，对标 LiveCodeBench 的 cutoff）；② 当**多样性注入的种子**（反推需求后喂给程序化模板，扩张槽位域）；③ 当**API 覆盖率的参照**（three.js 的 1,251 个 API 面）。**不要指望它贡献产能** |
| 一个可操作的配比目标 | **按「有效多样性贡献」而不是「条数」配**：要求真实素材衍生的任务在 Vendi Score 口径下贡献 ≥ 20% 的 D_1，哪怕它只占 2% 的条数。如果达不到，说明反推需求做烂了（只是把真实素材重新表述成了模板能出的东西） |

### 4.4 许可（会卡死规模化的那部分）

| 素材域 | 默认许可 | 对规模化的影响 |
|---|---|---|
| **CodePen** | public Pen **自动 MIT**（[官方](https://blog.codepen.io/documentation/licensing/)），但 MIT 模板含 **"Copyright (c) YEAR - YOUR NAME - URL TO ORIGINAL"**，即**必须保留作者名 + 原始 URL**；private Pen「owned by you with **no implicit license**」 | 许可干净，**但无 API、CF 拦截**，所以规模化受抓取而非许可限制 |
| **ShaderToy** | **CC BY-NC-SA 3.0**（官方一手页 403 拿不到，二手口径一致）。踩 **NC 禁商用 + SA 同样方式共享**两条 | **硬伤**。用 shaders21k（学术镜像）的 21,083 条，或者干脆不用 |
| **Objaverse-XL** | 数据集 ODC-By 1.0，单对象沿用原许可。实测 license 分布：**空/null 41.02%**、CC-BY 29.76%、MIT 9.69%、CC-BY-NC 5.65%、CC-BY-NC-SA 4.52%、GPL v3 2.51% | **商用可用 CC（CC-BY + SA + CC0 + PDD）只有 34.82%**；有明确 license 的合计 58.98% |
| **Blender 官方 render tests** | GPL | 02_task_sources.md 已标；**适合当评测集和阈值校准集，训练用要法务** |
| **The Stack 的教训** | permissive 过滤是一次 **10 倍级损失**：30 语言全许可 **29.6 TB / 1,633.05M 文件** → permissive 过滤后 **3.1 TB / 317.41M 文件**（约 10.6% 体积 / 19% 文件数）→ 近似去重后 **1.45 TB / 194.79M**（仅为原始全许可的 **约 4.9%**） | **规划素材池时要先按许可打 10 倍折扣，再按可执行性打折扣** |
| opt-out 的实际量级 | StarCoder 时期「**44 people opted out**」；The Stack v2 截止 2023-11-20 移除 91 个用户/组织的 1,561 个仓库、22,066 个文件（占 784.30M 文件的 **约 0.0028%**） | **opt-out 的意义是流程合法性，不是数据体量上的实质约束** |

### 4.5 一个必须记下来的口径坑：论文数 ≠ HuggingFace 行数

| 数据集 | 论文 | HF 实测 |
|---|---|---|
| Design2Code | 484 | 485 |
| Design2Code-HARD | card 写 80 个网页 | **162 行**（html + png 双条目） |
| Web2Code | 论文 **1,179.7K**（不是 1.28M） | default config **仅 100 行**（样例占位） |
| SWE-bench | 2,294 | **2,519**（含 dev + test） |
| R2E-Gym | 8,135 | 8,101 |
| SWE-smith | 50,137 | **59,136** |
| Objaverse-XL | 10.2M | **10,850,997**（元数据按**文件**计，1 模型可多文件） |
| WebCode2M | 训练 2,563,905 | 3,171,024 / purified 2,562,069 |

**任何对外引用都要说清是哪个口径。** 这条在我们自己发布数据集时同样适用 ——
「10 万任务」必须说清是候选数、准入通过数、还是去重后的最终数（§5.2 的三个数字差 2.7 倍）。

## 5. 成本模型：造 10 万个带 verifier 的任务要多少钱

### 5.0 实测口径（全部来自本机，不是文献）

| 口径 | 数字 | 出处 |
|---|---|---|
| three.js 单次探针（起浏览器 + 9 视角 + 场景图 + 体素） | 0.8 ~ 1.0 s | 90_local_experiments.md §1.5 |
| three.js 复用浏览器吞吐（8 浏览器 × 8 页，48 核无 GPU） | 14.3 任务/s，p50 4.1 s / p95 4.9 s | 06_harness.md §4.1.3 |
| three.js 独立起 chrome（不复用） | N≥8 即饱和在 3.6 任务/s | 06_harness.md §4.1.2 |
| Blender Workbench 稳态渲染 | 15.5 视角/s（0.065 s/视角；首视角 0.49 s 含 shader 编译） | 10_blender_tasks.md §3.5 |
| Blender 单任务生成 + 验证（冷启动单进程） | 2.3 s（exec 0.27 + 状态 0.11 + 采样 0.18 + 10 视角渲染 1.15） | 10_blender_tasks.md §3.5 |
| Blender 几何全套（Chamfer + F-score + 分部件体素） | 0.4 s/候选 | 10_blender_tasks.md §4.4 |
| 准入通过率（LLM 提破坏 → 收） | 26 提 25 收（96%）；加 L3 之前 26 提 23 收（88%） | 90_local_experiments.md §4 |
| VLM judge 吞吐 | 176 次调用 865 s（并发 12）≈ 0.2 次/s | 10_blender_tasks.md §5 |

### 5.1 假设清单（每条都标明是实测还是外推）

| 编号 | 假设 | 取值 | 依据 |
|---|---|---|---|
| H1 | 机器规格 | 48 核 CPU，无 GPU（去重那一步另算 1 张卡） | 本机配置 |
| H2 | three.js 探针复用浏览器池 | 14.3 任务/s ⇒ 单探针 48/14.3 = **3.36 core-s** | 实测吞吐换算，**外推**：假设 48 核全部被打满 |
| H3 | Blender 做进程池、摊掉 shader 编译 | 单任务 0.27+0.11+0.18+10/15.5 = **1.21 s 墙钟** | 10_blender_tasks.md §3.5 自己预估「可到 1.3 s 以内」，**外推** |
| H4 | 每个 bpy 进程平均占多少核 | 中位取 2 核 ⇒ **2.41 core-s/探针**；给出 1/2/4 核三档 | **外推**：swrast 渲染多线程、trimesh 采样单线程，没实测 |
| H5 | 每个候选在准入阶段的探针次数 | 3 次（参考解自比自 1 + 破坏版 1 + 参考解复跑做翻面检查 1） | 90_local_experiments.md §4 的三条准入 + 11_hacking_defense.md 的重测要求 |
| H6 | 难度标定用两段式 | 先 n=2 筛，存活者再补 6 次（合计 n=8） | 本文 §2.1 的方差表 + 记忆里的「A/B 先 2 轮筛再补到 n=6」 |
| H7 | n=2 筛掉的比例 | 55%（全对或全错） | **外推**：§2.1 表 B，真 p=0.5 时 n=2 有 50% 概率全对/全错，p 偏离 0.5 更高 |
| H8 | LLM 一次提案出 16 条破坏 | 实测 desk 场景一次提 16 条 | 90_local_experiments.md §4 |
| H9 | 一次 solve rollout = 1 次 LLM 调用 + 1 次探针 | 单轮不给反馈的档 | 简化；多轮档要乘轮数 |

### 5.2 产出漏斗：要 10 万合格任务，得造多少候选

留存率里只有「准入②」和「准入①」是实测，其余是外推，逐条标注。

| 阶段 | 单阶段留存 | 性质 | 累计留存 | 进入该阶段的候选数 |
|---|---|---|---|---|
| LLM 提破坏 / 采样参数 → 候选 | 1.00 | — | 1.000 | 268,700 |
| 准入① 参考解自比自过 verifier | 0.97 | 实测 ≈1.0，留 3% 余量 | 0.970 | 268,700 |
| 准入② 破坏版必须被判挂 | 0.90 | **实测** 88% ~ 96%，取 90% | 0.873 | 260,600 |
| 准入③ search 片段唯一 / 脚本可执行 | 0.95 | 外推 | 0.829 | 234,500 |
| 结构 + 视觉 + 文本三路去重 | 0.85 | 外推（见 §3） | 0.705 | 222,800 |
| 可解性闸（题干信息量 ≥ verifier 查的字段） | 0.88 | **半实测**：本机 9 个桌子任务里 2 个因此不可解（78%），Blender 留出集 7 个里 1 个（86%） | 0.620 | 189,400 |
| 难度带筛选（去掉 n=8 全对 / 全错） | 0.60 | 外推，对标 DAPO 的 dynamic sampling | 0.372 | 166,700 |
| **合格任务** | | | **0.372** | **100,000** |

**要造约 26.9 万个候选才能收到 10 万个合格任务。** 这个 2.7 倍的放大系数是成本模型里最敏感的一项：
「难度带筛选」那条 0.60 如果实际是 0.30，候选数直接翻倍。

### 5.3 探针次数

```
准入阶段   268,700 候选 x 3 次探针                        =   806,000 次
难度标定   166,700 候选 x 2 次（n=2 筛）                   =   333,400 次
           166,700 x 45% 存活 x 6 次（补到 n=8）           =   450,000 次
                                                            ---------
                                             探针总计      ≈ 1,589,000 次
```

### 5.4 three.js 的 CPU 账

| 口径 | 算式 | 结果 |
|---|---|---|
| 单探针 core-s | 48 核 / 14.3 任务每秒 | 3.36 core-s |
| 总 CPU | 1,589,000 × 3.36 / 3600 | **1,480 core-h** |
| 折成 48 核整机 | 1,480 / 48 | **31 台机小时 ≈ 1.3 机日** |
| 对照：不复用浏览器（3.6 任务/s） | 1,589,000 / 3.6 / 3600 | 123 小时墙钟，整机 **5.1 机日** |
| 对照：单进程串行 0.9 s | 1,589,000 × 0.9 / 3600 | 397 小时，但只占 1 核 |

**结论：three.js 侧的 CPU 成本可以忽略 —— 一台 48 核机器跑 1.3 天就够 10 万任务。**
前提是把浏览器池做出来（复用把吞吐从 3.6 抬到 14.3，接近 4 倍）。

### 5.5 Blender 的 CPU 账

| 每进程占核数假设 | 单探针 core-s | 总 CPU | 折 48 核整机 |
|---|---|---|---|
| 1 核（纯串行、乐观） | 1.21 | 532 core-h | 11 台机小时 = 0.5 机日 |
| **2 核（中位取值）** | **2.41** | **1,064 core-h** | **22 台机小时 = 0.9 机日** |
| 4 核（swrast 吃满） | 4.82 | 2,128 core-h | 44 台机小时 = 1.8 机日 |
| 不做进程复用（冷启动 2.3 s × 1 核） | 2.30 | 1,015 core-h | 21 台机小时 |

**结论：Blender 侧和 three.js 同一个量级，1,000 core-h 上下。**
注意一个反直觉的点：**Blender 比 three.js 更便宜**，因为 Workbench 稳态渲染 0.065 s/视角，
比 SwiftShader 下的 WebGL 快；three.js 贵在浏览器本身。

如果把 Workbench 换成 Cycles（512×512 / 32 spp）或者 EEVEE Next，这个账要重算 ——
10_blender_tasks.md §4.4 的结论是「几何指标比渲染便宜 3 倍、判别力还更高」，
所以**扩产阶段应该只渲 Workbench 剪影 + 算几何，不渲 Cycles**。

### 5.6 LLM 调用账

| 用途 | 次数 | 占比 |
|---|---|---|
| 破坏 / 参数提案（每场景 1 次出 16 条） | 16,800 | 1.4% |
| 题干改写 + spec.json 导出（每候选 1 次） | 268,700 | 22% |
| **难度标定 rollout（两段式 n=2 → n=8）** | **783,000** | **65%** |
| 欠规格诊断（难桶 25% × 3 次 ceiling check） | 125,000 | 10% |
| VLM 抽检（2% 任务 × 4 judge × 2 次） | 16,000 | 1.3% |
| **合计** | **≈ 1.21 M 次** | |

两个可以省钱的点：

1. **两段式筛选省掉 0.55 M 次调用。** 一次性 n=8 要 1.33 M 次标定调用（总计 1.76 M）；
   先 n=2 筛掉 55%、再补 6 次只要 0.78 M（总计 1.21 M）。**省 31%**。
2. **题干改写那 22% 可以用模板省掉。** 程序化路线（§1）的题干是槽位短语拼出来的，
   不需要 LLM；只有「从真实素材反推需求」那一路（§4）必须调 LLM。
   如果程序化占 70%，这一项降到 8 万次。

**优化后约 0.95 M 次 LLM 调用。** 按一次 rollout 平均 2k 输入 + 1k 输出 token 估，
约 1.9 B 输入 + 0.95 B 输出 token。

### 5.7 去重的算力（§3 的工程成本）

| 项 | 算式 | 结果 |
|---|---|---|
| 视觉 embedding（10 万任务 × 9 视角 = 90 万图） | DINOv2 ViT-B 单卡约 200 图/s | **1.25 GPU 小时** |
| pHash 90 万图 | 单核 1 ms/图 | 15 分钟 |
| 全对全余弦（10 万 × 768 维） | 3.8 TFLOP，单机 BLAS 100 GFLOPS | **38 秒** |
| 向量存储 | 10 万 × 768 × 4B | 307 MB（int8 量化后 77 MB） |
| MinHash + LSH（题干 + 代码） | 10 万文档，datatrove 量级 | 分钟级 |

**结论：10 万量级的去重是免费的。** 真正的成本是 embedding 推理的 1.25 GPU 小时。
到 100 万量级也只是 12.5 GPU 小时 + FAISS IVF 索引，仍然不构成瓶颈。
**不要因为「怕去重贵」而跳过去重** —— 这是整条流水线里性价比最高的一步。

### 5.8 人工抽检账

抽检量和置信区间的关系（p=0.5 最坏情况，95% CI 半宽）：

| 单层抽检条数 | CI 半宽 |
|---|---|
| 50 | ±13.9% |
| 100 | ±9.8% |
| 200 | ±6.9% |
| 384 | ±5.0% |
| 1,000 | ±3.1% |

建议口径：**12 层 × 100 条 = 1,200 条/轮**（分层维度 = 2 个引擎 × 3 个难度桶 × 2 个来源 × ...）。
层内 ±9.8%，全局 ±2.8%。

| 项 | 量 | 工时 |
|---|---|---|
| 分阶段抽检 4 轮 × 1,200 条 × 3 分钟 | 4,800 条 | **240 人时** |
| verifier 逐条一致性标定（11_hacking_defense.md 要求 ≥92%，每层 50 条） | 600 条 × 5 分钟 | **50 人时** |
| 欠规格仲裁（难桶里 ceiling check 翻面的那些，估 2,000 条 × 2 分钟） | 2,000 条 | **67 人时** |
| **合计** | | **≈ 360 人时 ≈ 1.5 人月** |

### 5.9 总账

| 项 | three.js 线 | Blender 线 | 说明 |
|---|---|---|---|
| CPU | 1,480 core-h（31 台机小时） | 1,064 core-h（22 台机小时） | 各按 10 万任务独立算；如果 10 万是两条线合计则各减半 |
| GPU | 1.25 GPU 小时（去重 embedding） | 1.25 GPU 小时 | 共用 |
| LLM 调用 | ≈ 0.95 M 次（优化后） | ≈ 0.95 M 次 | 难度标定占 65% |
| LLM token | ≈ 1.9 B 输入 / 0.95 B 输出 | 同 | 按 2k+1k/次 |
| 人工 | 360 人时 | 360 人时 | 抽检 + 标定 + 仲裁 |
| 存储 | 见下 | 见下 | |

存储：three.js 单任务 = 源码约 5 KB + 9 视角 JPEG 约 9 × 15 KB + 体素 48³ 稀疏约 50 KB ≈ 0.2 MB
⇒ 10 万任务约 **20 GB**。Blender 单任务 = ref.py 约 4 KB + state.json 约 30 KB + 10 视角 PNG 约 10 × 30 KB + points.npz 6 万点约 700 KB ≈ 1 MB
⇒ 10 万任务约 **100 GB**。`.blend` 不存（可由 ref.py 确定性重建）。

**一句话总结：这件事的瓶颈不是算力（两条线合计约 2,500 core-h，一台 48 核机器两天），
是 LLM 调用（约 100 万次）和人工（1.5 人月）。
而 LLM 调用里 65% 花在难度标定上 —— 所以「难度标定要采样多少次」是整个成本模型里唯一值得反复优化的旋钮。**

## 6. 分阶段扩产方案：从 100 个手工场景到 10 万任务

设计原则（三条，都来自本机踩的坑）：

1. **每个阶段的验收标准必须包含一条「留出集」指标**，而且阈值在进入该阶段前定死。
   本机 29/29 要打折扣、补了 18 个留出才敢信（90_local_experiments.md §2.3）—— 这个教训在每个量级上都会重演。
2. **规模每翻 10 倍，verifier 必须重新校准一次**，不是只校准一次。
   盲区是被具体 case 逼出来的（圆台翻转逼出颜色容差、细长部件逼出 L3、LatheGeometry 的洞逼出开放边界）。
3. **每个阶段只放大一个变量。** 不要同时放大场景数、模板数和来源数，否则出问题分不清是谁的锅。

### 阶段总览

| 阶段 | 场景数 | 任务数 | 新增的放大变量 | 主要风险 | 预计周期 |
|---|---|---|---|---|---|
| S0 校准 | 3 → 10 | 50 → 200 | 无（只加场景） | verifier 阈值不迁移 | 1 周 |
| S1 模板化 | 10 手工 → 8 个槽位模板 | 2,000 | 程序化生成器 | 同质化 | 2 周 |
| S2 多样性扩张 | 8 → 40 模板 | 20,000 | 模板族 + 难度标定 | 有效多样性塌缩 | 4 周 |
| S3 真实素材注入 | +GitHub / examples / CodePen | 50,000 | 真实素材管线 | 许可 + 反推需求质量 | 4 周 |
| S4 满产 | 全部 | 100,000+ | 产能（并发 + 多引擎） | 污染 + 分布漂移 | 持续 |

---

### S0 校准阶段：3 个场景 → 10 个场景，50 → 200 任务

**目的**：确认 verifier 阈值在「没见过的场景类别」上迁移得住，并把阈值一次性冻结。

做法：
- 10 个场景覆盖互不重叠的结构类别：刚体堆叠、层级 / 父子、镜像对称、细长部件、透明 / 玻璃、
  重复阵列、曲面 / 旋成体、动画关键帧、灯光主导、文字 / 贴图。
  本机现有 3 个（雪人 = 旋成体、桌子 = 刚体堆叠、小车 = 层级）只覆盖 3 类。
- 每个场景 20 个带标签变异（约 10 该挂 / 10 不该挂），**标签先写死再跑**。
- 阈值沿用现在的五信号，**一个不动**。

| 验收标准 | 阈值 | 为什么是这个数 |
|---|---|---|
| 留出场景（后 7 个）上的变异判别率 | ≥ 90%（126/140 以上） | 本机前 3 个场景 47/47，打折到 90% 留足余量 |
| 检出率（该挂的被挂） | ≥ 0.95 | 漏检会污染训练集，比误杀贵 |
| 保真率（不该挂的放行） | ≥ 0.90 | 误杀让任务不可解，表现为「模型明明做对了却 0 分」 |
| 参考解复跑翻面率 | = 0 | 本机实测噪声地板是 0（逐位相同），这条不能让步 |
| 可解性闸：给足参考图后一轮通过率 | ≥ 0.80 | 低于此说明题干还是说不清 |
| 新增盲区条数 | 记录下来，每条都要有对应的新信号或明确的「不查」决定 | §4 的「准入测试即 verifier 体检报告」 |

**S0 不通过就不许进 S1。** 如果留出判别率低于 0.90，先补信号、再从 S0 重跑，不要靠调阈值。

---

### S1 模板化：10 个手工场景 → 8 个槽位模板，2,000 任务

**目的**：把手工场景改写成参数化生成器，验证「生成器只出目标场景、不出参考代码」这条原则站得住。

做法：
- 每个模板 = 一张槽位表（见 10_blender_tasks.md §2.1 的 `SLOTS` 伪代码），
  槽位带：取值域、**可见性标注**（这个槽位渲染后能不能被 verifier 分开）、归属断言族、容差、题干短语。
- `spec.json` 从「被钉死的槽位」导出，**没写进题干的槽位不进 spec**。
- 每模板 250 个任务（25 个种子 × 10 种钉死组合）。
- 同步做结构去重（场景图哈希）—— 这是第一次能发现「生成器出重复」的机会。

| 验收标准 | 阈值 | 说明 |
|---|---|---|
| **可见性审计通过率** | 100% | 每个槽位必须标注「能/不能被哪个信号分开」。不能被任何信号分开的槽位**不许进 spec** |
| 结构去重后留存 | ≥ 0.90 | 低于此说明槽位域太窄或种子采样有问题 |
| 有效多样性比（见 §1.3） | 有效等价类 / 任务数 ≥ 0.7 | 本机算术显示组合空间可以比有效等价类大 4 万倍，必须按**有效**口径验收 |
| 实现路径不变性 | 换一条实现路径写同一场景，verifier 必须放行 | 本机 `cube_size2` 已验证：几何信号放行（分部件 F 0.9993），按代码比的 A2/A3 会误杀 ⇒ **A2/A3 不能单独当闸** |
| 难度分布 | pass@8 的中位数落在 0.3 ~ 0.7 | 这一阶段先看分布形状，不做精细分桶 |
| 准入通过率 | ≥ 0.85 | 对标本机 88% ~ 96% |

**S1 的核心交付物不是 2,000 个任务，是 8 张经过可见性审计的槽位表。**
槽位表错了，后面 10 万个任务全是错的。

---

### S2 多样性扩张：8 → 40 个模板，20,000 任务

**目的**：把量级抬一个数量级，并第一次上真正的难度标定与完整去重。

做法：
- 模板从 8 扩到 40：按「结构类别 × 领域」的二维表铺（10 个结构类别 × 4 个领域：
  室内家具 / 机械装置 / 数据可视化 / 抽象几何）。
- 加**跨模板组合**：两个模板的场景拼在一个坐标系里（这是性价比最高的多样性来源，
  因为组合出的空间关系不在任何单模板的槽位域里）。
- 难度标定上两段式 n=2 → n=8。
- 去重上三路（结构 + 视觉 + 文本）全套。

| 验收标准 | 阈值 | 说明 |
|---|---|---|
| 三路去重后留存 | ≥ 0.80 | 低于此要回去扩槽位域，而不是放宽阈值 |
| 最近邻距离分布的 5 分位 | 大于「同模板换种子」对的中位距离 | 即：**跨模板的最近邻必须比同模板换种子更远**。这条比任何单一阈值都更能抓塌缩 |
| 难度三桶占比 | 易 / 中 / 难 各 ≥ 15% | 任何一桶不足说明槽位难度旋钮没接好 |
| 边界桶的标定噪声 | 承认不可控：真 p=0.35 时 n=8 的桶误分率 45%、n=64 仍 22%（§2.1 表 C）⇒ **用软桶 / 重叠桶，不用硬边界** | |
| 欠规格检出率 | 难桶里 ceiling check（给参考图后）通过率跳升 ≥ 0.3 的，判为欠规格并修题干；修完复测 | §2.3 |
| verifier 重新校准 | 在 S2 新出的模板上再做一次 S0 的留出测试，判别率仍 ≥ 0.90 | 原则 2 |
| 与公开 benchmark 的 n-gram 重合 | 0 条命中（黑名单见 §3.4） | |

---

### S3 真实素材注入：+GitHub / examples / CodePen，到 50,000 任务

**目的**：解决程序化路线的「生成器风格」问题，把真实世界的 API 用法和视觉风格带进来。

做法见 §4 的管线。这一阶段的特殊点是**许可与污染都在这里出问题**。

| 验收标准 | 阈值 | 说明 |
|---|---|---|
| 许可白名单覆盖率 | 100%（每个任务可追溯到一个 permissive 许可） | 02_task_sources.md 已标出 ShaderToy 是 NC、Blender 是 GPL、Figma / FEM 禁再分发 |
| 真实素材管线端到端保留率 | 记录实际值，与 §4 的估计对账；偏差 > 2 倍要重新估 | 估计值全部标【估】 |
| 真实 vs 合成占比 | 真实 ≥ 30%（见 §4.3 的配比讨论） | |
| 真实素材任务的难度分布 | 和程序化任务的难度分布做 KS 检验，**预期显著不同**，这是好事 | 如果分布一样，说明真实素材没带来新信息 |
| 时间切分 | 所有素材按 commit / pen 的创建时间排序，最近 N 个月**整段留出**做评测，不进训练 | 对标 LiveCodeBench 的 cutoff 做法 |
| 反推需求的人工抽检通过率 | ≥ 0.85（抽 200 条，看题干是否真的描述了参考解做的事） | 这是真实素材路线最容易烂的一环 |

---

### S4 满产：10 万 +

| 验收标准 | 阈值 | 说明 |
|---|---|---|
| 全集难度三桶占比 | 易 20% / 中 55% / 难 25%（± 10 个点） | 中等桶占大头是 RL 的需要（group 不全对不全错才有梯度） |
| 全集去重：pairwise 相似度 > 阈值的对数 | 0 对（按 §3 的三路阈值） | |
| 分层抽检（12 层 × 100 条）通过率 | 每层 ≥ 0.85，全局 ≥ 0.90 | 层内 ±9.8%，全局 ±2.8%（§5.8） |
| verifier 一致率 | ≥ 0.92（11_hacking_defense.md §2 的门槛） | |
| 作弊页面拦截率 | 100%（7 个已知攻击 + 每轮新增的） | 本机 7/7 已过，离屏 renderer 那条是真实攻击 |
| 分布漂移监控 | 每周算一次「新增 1 万任务」相对全集的特征分布 KL；> 0.1 要查 | 防止产能爬坡时悄悄只出某一类 |
| 训练侧回归 | 每加 2 万任务，在固定留出评测集上跑一次；**指标不涨就停止扩产去查原因** | 这是唯一真正的验收标准 |

### 一条贯穿所有阶段的红线

**任何阶段都不许用「正在用来调阈值的集合」做验收。**
本机已经犯过一次（13 个变异集既当调参集又当验收集，tol=60 是看到误杀后加的），
11_hacking_defense.md §2.1 把它当反面教材写进了校准协议。
扩到 10 万量级时这个错误的代价是：整个数据集在一个你看不见的方向上过拟合，
而且因为指标都很漂亮，你不会发现。

## 7 附录

### 7.1 明确「未找到」的条目（不要在下游写作里当成已有结论）

| 问题 | 状态 |
|---|---|
| 「不交付生成器源码以防模型拟合生成器的代码风格」的直接文献 | **未找到**。两轮扩展检索无任何论文主张或做过这种消融。最近的间接证据：Infinigen 对**静态资产库**「easier to overfit」的论断 + Procgen 的「需约 10,000 个关卡才闭合泛化 gap」。**注意 Infinigen 自身做法与此相反** —— 它把生成器全部 BSD 开源并视为优点 |
| 「effective diversity」作为正式命名的 PCG 指标 | **未找到**该术语的正式定义文献。可用的替代是 Hill number 的 q=0 vs q=1 |
| 「合成数据占比的安全上限」的可搬用数字 | **没有任何论文给出。** 文献给三条口径不同的结论：最坏 1% 即触发（2410.04840，前提是不筛选 + 替换式迭代）/ 合成量应对数级于真实量（2404.05090）/ 决定性变量是协议而非比例（accumulate 不 replace + verifier 筛选，2404.01413 + 2406.07515） |
| 「多少合成场景 ≈ 多少真实扫描场景」的等价换算 | **未找到**。HSSD 的 122 : 10,000 是**合成 vs 合成**（高保真 vs 程序化）的样本效率对比 |
| pHash Hamming ≤ 5 或 ≤ 8 作为公开推荐值 | **未找到权威出处。** `imagehash` 官方 README 不给推荐值。有出处的是 imagededup 默认 **10**、Meta PDQ 生产常量 **31**、Prokos et al. 的 pHash **6/10/14** |
| 预训练级公开代码数据集用 AST 规范化哈希去重并公布比例 | **未找到。** The Stack v1/v2、StarCoder/2、CodeGen、AlphaCode、CodeParrot、OpenCoder **全部**是 token/字符 n-gram 的 MinHash。唯一的结构哈希是 ComPile 的 LLVM StructuralHash（990 GB → 853 GB，**−35%**） |
| 「n=4 不够、要 n≥16」的确切论断 | **未找到这个措辞。** 最接近的是 LZE 附录 F：「Smaller N (= 4) yields noisier ... **N = 8 is a robust default**」 |
| DAPO 的 dynamic sampling 过采样倍数 / Figure 3(b) 的具体读数 | **论文未给。** 替代数字：GRESO 实测约 **5×**、有效 prompt 后期只剩约 20% |
| DeepSeekMath 对 std → 0 的数值处理（eps） | **论文没写**（verl 等框架加小常数） |
| Infinigen 的 CPU-hours / GPU-hours 数值 | 只在直方图里。论文给的是**墙钟 3.5 小时**，不是 core-hours |
| Infinigen-Indoors 的每场景 CPU 小时 / 墙钟 / 内存 | **论文未报告** |
| Kubric 的总视频数 / 总帧数 / 总 TB / 成本 | **论文完全不给。** 全文唯一算力数字是光流数据集约 **3 CPU-years** |
| CodePen 2026 当前 pen 总数 | **未找到。** 唯一官方数字是 **1,000 万（2016-11）**，此后无更新 |
| ShaderToy 的 shader 总数与官方许可一手页 | **整站对海外出口 403**（`/api/v1/shaders`、`/terms`、`/about` 三条路径）。许可（CC BY-NC-SA 3.0）只有二手口径 |
| GitHub 上含 `import bpy` 的 .py 文件数 | **拿不到。** 文件级 code search 必须带 token（未认证 401），grep.app 返回 429 |
| WebCoderBench 的题目清单 | **作者明确不发布**（真实用户需求 + 法务限制，并把不公开当作防刷分手段）。唯一办法是训练语料时间截断在 2026-01-05 之前，但**时间切分也不保证干净，必须当黑盒信任** |

### 7.2 论文内部自相矛盾 / 跨论文不可比（引用前必查）

| # | 坑 |
|---|---|
| 1 | **Kubric 的挑战数自相矛盾**：摘要与 Table 2 说 **13 个**，Conclusion 写 **11 个** |
| 2 | **ProcTHOR 的 SAG 组合数自相矛盾**：§3 说「roughly 20 million」，§4 说「19.3 million」 |
| 3 | **跨论文 FID 完全不可比**：同一个 ATISS 的卧室 FID 在四篇论文里是 **38.39 / 18.60 / 36.92（或 30.19）/ 119.73** —— 渲染方式（RGB 俯视 vs 语义图 vs Blender）与条件设定（有/无平面图、无条件/指令驱动）各不相同 |
| 4 | **SCA 的方向是「越接近 50% 越好」**，不是越低越好 |
| 5 | **ProcTHOR 自报 HM3D 数字与 HSSD 复现不一致**，三条原因：HM3DSem v1 test vs v2 val、episode 生成方案不同、AI2-THOR 渲染 vs Habitat 渲染 |
| 6 | **ProcTHOR Table 1 的「1 GPU 大屋 6,280 FPS」是笔误**（HSSD 称已与作者确认），真值未知 |
| 7 | **Infinigen-Indoors Table 3 里 `w/o Discrete change` 的分数反而更高**（86.20 vs 80.84）。作者明说离散改动「necessary for compelling visuals, but **decrease the quantitative score**」—— **量化指标与观感会反向** |
| 8 | **GRPO advantage 那条式子在 DeepSeekMath 原文里没有编号**，常被误引成 Eq.3（Eq.3 是目标函数） |
| 9 | **POET 的「reward in [25, 340]」不存在**，真值是 **[50, 300]** |
| 10 | **ManiBench 是官方拼写**（不是 ManimBench），且摘要称 150~200 题而 HF 上只有 **12 题** pilot |
| 11 | **WorldCoder-Bench 论文称 2,026，仓库实际 2,004**，差 22 条未公开 |
| 12 | **AlphaGeometry 的「1 亿」只在 DeepMind 博客**，Nature 摘要写的是 "millions"。引论文必须用 "millions" |
| 13 | **Web2Code 不是 1.28M**，是 **1,179.7K**（884.7K 图码对 + 295K QA） |
| 14 | **论文数 ≠ HuggingFace 行数**：SWE-smith 50,137 vs 59,136；SWE-bench 2,294 vs 2,519；Objaverse-XL 10.2M vs 10,850,997（按文件计）。**我们自己发布时也适用**：「10 万任务」必须说清是候选数、准入通过数还是去重后的最终数（§5.2 的三个数字差 2.7 倍） |
| 15 | **BlenderProc 的「3,000 张/小时」（2019 arXiv）与「< 2 秒/图」（2020 workshop）口径不同**，场景复杂度不一样，不要混算；而 26.2 → 33.8 mAP50 那组数字**只在 RSS 2020 workshop paper**，arXiv 1911.01911 完全没有实验章节 |
| 16 | **本机对 Infinigen 生成器数的计数与论文不一致**：10_blender_tasks.md §2.1 按 `src/infinigen/assets` 下 568 个 py 文件数出「约 246 个生成器」，而论文 Table 2 的口径是 **182 个生成器 / 1,070 个可解释 DOF**。**用论文口径对外引用** |

### 7.3 与本系列其他笔记的关系

| 本文的哪一节 | 依赖 / 延伸了谁 |
|---|---|
| §1.2 的「验状态不验代码」 | 延伸 03_verifiable_construction.md §3.1「参考代码只是一种解」；本机证据是 10_blender_tasks.md 的 `cube_size2`（分部件 F-score 0.9993 放行，A2/A3 误杀） |
| §1.3 的「别用预训练视觉特征」 | 与 12_self_verification.md 的「SigLIP 在 10 个模型上全落 0.077~0.108 窄带」是同一件事的两个面 |
| §2.3 的「难 vs 坏」 | 把 90_local_experiments.md §5「verifier 比问题描述知道得多」从个案上升为可量化的闸 |
| §3 的 verifier 校准 | 承接 11_hacking_defense.md §2 的六阶段校准协议（逐条一致率 ≥92%、变异检出率、重测翻面率）；本文补的是**规模化之后每翻 10 倍要重做一次** |
| §5 的成本模型 | 口径全部来自 06_harness.md §4.1（three.js 14.3 任务/s）与 10_blender_tasks.md §3.5/§4.4（Blender 2.3 s、15.5 视角/s、几何 0.4 s） |
| §6 的分阶段方案 | S0 的留出测试方法来自 90_local_experiments.md §2.3（第三个场景 18/18，阈值不动） |

### 7.4 下一步该做什么（按性价比排序）

| 优先级 | 事情 | 成本 | 为什么值 |
|---|---|---|---|
| **1** | **在现有 47 个任务上先测 pass@8 分布**，把 §5.2 漏斗里「难度带留存 0.60」这个数钉死 | 47 × 8 = 376 次调用，几十分钟 | 这是成本模型最敏感的一项，公开实测暗示它可能只有 0.2~0.4 |
| **2** | **给 gen_tasks.py 补上 FACET 判据 ii**：verifier 在初始状态必须判挂 | 几行代码 | 现在可能已经混进了「免费分」任务而不自知 |
| **3** | **给 three.js 侧补 spec.json + 可见性审计** | 半天 | 本机唯一的两次失败都是「verifier 查了题干没给的信息」；Blender 侧已有，three.js 侧没有 |
| **4** | **把 9 视角探针的输出直接拼成 L-near 特征向量**，先在 47 个任务上看最近邻距离分布 | 零额外成本（探针产物已有） | 去重和多样性验收共用同一组特征，而且不用 CLIP |
| **5** | **算一次现有槽位表的 D_0 / D_1 折损倍数** | 几小时 | §1.3.5 的 4.4 万倍只是粗估，要用真实采样算 |
| **6** | **建 A 类 benchmark 的黑名单表**（3JSBench 100 / ArtifactsBench 1,825 / BenchCAD 17,900 / PRISM 10,372 / Animation2Code 1,069 全量可下） | 一次性半天 | 去污这一路**只有收益没有损失**，而且越早建越便宜（素材抓取阶段就能查） |

