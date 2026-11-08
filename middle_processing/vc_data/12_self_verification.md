# 自检能力：怎么训出「截图→发现问题→改→再截图」

> 课题：visual coding 里「模型在执行过程中自己用视觉工具验证并修正」的能力，
> 是否是前沿模型相对开源模型的关键差距；怎么训出来。
> 本篇与 `04_verifier.md`（verifier 选型）、`05_trajectory_repair.md`（轨迹层）互补，重复的证据只给交叉引用。
> 另含本机实测：snowman 任务 18 个候选 × 4 judge × 单图/多视角 × 2 重复（283 条判定）的拆解分析。

---

## 0. 结论速览

| 问题 | 答案 | 最硬的数字 |
|---|---|---|
| 「能自检」是 visual coding 的主要增益来源吗 | **不是「自检」，是「自验证器」**。收益几乎全部来自「有一个独立的判别信号」，不是来自模型反思自己 | BlenderAlchemy 表 3：把视觉给**评估器**拿回 84% 的增益，给**编辑生成器**只拿回 16% |
| 纯粹的自我修订（无外部判据）呢 | 对前沿模型微小正收益，对开源模型是**灾难** | Design2Code 表 1：GPT-4V block 85.8→88.8；DeepSeek-VL-7B text 77.0→**38.9**，Idefics2-8B block 46.7→**12.3** |
| 没有判据时多轮会怎样 | **单调变差** | BlenderAlchemy 去视觉后逐轮 27.4/26.1/26.5/25.7；Huang 2310.01798 表 3：GPT-4 GSM8K 95.5→91.5→89.0 |
| 有判据（oracle）时呢 | 立刻转正 | 同一篇表 2：GPT-4 95.5→**97.5**，GPT-3.5 75.9→**84.3** |
| 为什么模型自检会失败 | ①VLM 低层视觉本来就瞎 ②自己评自己有确认偏误 ③单图把真错误解释成「取景差异」 | BlindTest 两线相交 47~85%；BLINK 人 95.70% / GPT-4V 51.26%；本机实测：single 条件下 8 次漏判有 4 次明确援引「相机取景差异」豁免 |
| 怎么训：数据层 | **故意改坏 → 渲染 → 标注错在哪 → 修复 diff**，且难度要对着当前 critic 做对抗筛选 | CriticGPT：篡改数据要求「critic 三次采样里至少漏一次」；最终 critique 在 63% 的 case 上优于人类 |
| 怎么训：轨迹层 | 离线纠错轨迹做 SFT 学不到自检，会塌成「从不改」或「乱改」 | SCoRe 表 1：base Δ=−11.2%，STaR −14.2%，Pair-SFT D+ 恰好 **0%/0%/0%**（完全不改） |
| 怎么训：RL 层 | **只在严格超过历史最佳时才接受这次反思**；不要用退步罚分 | ReLook：罚分导致模型学会少反思来躲罚（reward hacking），改成 Forced Optimization 后 +2.0 分 |
| 怎么训：工具层 | 并排参考图 > 单图；多视角提召回但**砍特异度**；可读的确定性状态 > 任何图 | 本机实测：multi 把竖向位移召回 0.57→0.88，但把「换实现」正例 8/8 判成 1/8；SimWorlds 读 Blender 活状态 MPR 0.87 对纯视觉 verifier 0.67 |

**一句话配方**：不要训「模型会反思」，要训「模型会调用一个它自己无法糊弄的判别器，并在判别器分数不升时回滚」。

---

## 1. 证据：「能自检」到底贡献了多少

### 1.1 BlenderAlchemy：截图用于「选择」有效，用于「生成改法」收益小

arXiv 2404.17672（ECCV 2024）表 3，text-based material editing，ViT-B/32 CLIP 分（越高越好），
系统为 4×8（深度 4 × 宽度 8）。Edit 1~4 是四轮迭代精修后各轮的输出。

| 变体 | 谁看得见图 | Edit 1 | Edit 2 | Edit 3 | Edit 4 |
|---|---|---|---|---|---|
| `-Vision` | 生成器 G 和评估器 V **都瞎** | 27.4 | 26.1 | 26.5 | **25.7** |
| `-Vision G` | 只有评估器 V 能看图 | 27.6 | 27.6 | 27.6 | **27.8** |
| `Ours` | G 和 V 都能看图 | 27.8 | 27.9 | 28.4 | **28.2** |

**增益拆解（第 4 轮）**：

| 来源 | 分差 | 占总增益 |
|---|---|---|
| 视觉总增益 | 28.2 − 25.7 = **+2.5** | 100% |
| 其中：**给评估器看图**（选择） | 27.8 − 25.7 = **+2.1** | **84%** |
| 其中：**给生成器看图**（生成改法） | 28.2 − 27.8 = **+0.4** | **16%** |

三个附带结论，都在同一张表：

1. **瞎着迭代会越改越差**：`-Vision` 从 27.4 单调掉到 25.7（−1.7）。
   「多轮」本身没有价值，有价值的是多轮里那个判别信号。
2. **只要评估器能看图，曲线就不再下跌**：`-Vision G` 27.6→27.8，单调非降。
   也就是说，**哪怕改法是闭着眼瞎猜的，只要有人能挑出好的那一个，系统就不退化**。
3. **去掉回滚（`-Revert`）同样单调发散**：27.1/26.4/26.6/25.8，且在做结构性大改（leap）的轮次掉得最狠
   → 自检必须配回滚，光有评分不够。

同篇表 2（image-based material editing，固定总调用 32 次）：

| d×b | 1×32 | 2×16 | 4×8 | 8×4 | 16×2 | 32×1 |
|---|---|---|---|---|---|---|
| ViT-B/32 ↑ | 81.7 | 82.9 | 81.7 | **84.1** | 83.6 | 81.6 |
| Photometric ↓ | 0.066 | 0.066 | **0.049** | 0.050 | 0.056 | **0.087** |
| LPIPS ↓ | 0.64 | 0.54 | 0.52 | **0.50** | 0.52 | 0.59 |

- `32×1` = 纯串行自我精修（每轮只有一个假设、没有选择）→ photometric **最差**（0.087）。
- `1×32` = 纯 best-of-32（有选择、无精修）→ 0.066，已经明显好于纯串行。
- **「选择」比「精修」更值钱；两者结合（8×4 / 4×8）才最好。**

另：`-Imagin.`（去掉用文生图先「想象」一张目标参考图）逐轮 26.8/27.1/26.8/26.9，比 Ours 低 1.3~1.6 分
→ **抽象文字意图下，先合成一张参考图再做并排比较，本身就是个增益点**（对应第 4 节的「并排」）。

### 1.2 BlenderGym：verifier 比 generator 更值得加算力

arXiv 2504.01786（CVPR 2025）。管线沿用 BlenderAlchemy 的 generator-verifier 结构。

| 结论 | 数字 | 位置 |
|---|---|---|
| VLM verifier 与人的两两选择一致率 | Claude-3.5-Sonnet **0.66**（最高），inter-human **0.79**，随机 0.50；7,950 次判断 / 50 名参与者 | §4.2.2 + 图 4 |
| 位置偏置 | Qwen 不管候选怎么排列**总选第二个** | §4.2.2 |
| verifier inference scaling 有效 | 重选参数 k ∈ {1,2,4,8,16,32,64}，三项指标随 k 单调改善；**scaled InternVL2-8B 超过未 scale 的 GPT-4o 与 Claude-3.5-Sonnet（三项全超）** | §4.3 |
| 算力该怎么分 | VeriRatio 0.33 / 0.62 / 0.73（总 query 12→245）：**总算力越大，越该把更大比例给 verification** | §4.4 + 表 2 |
| 人机差距 | blend shape PL：人 0.934 / GPT-4o 9.140（差一个数量级）；geometry CD：人 0.334 / GPT-4o 1.192。人限时 8 分钟/题 | 表 1 + §3.2 |
| 开源模型连代码都写不出来 | 除 MiniCPM 外，**所有开源 VLM 系统在 geometry editing 上 >75% 的实例产不出可执行脚本** | §4.2.1 |
| 视角是刻意设计的 | 「遮挡或不完整的渲染视角会给 VLM 编辑引入偏置」→ 每个 start-goal 对**人工固定至少 3 个视角**，保证①至少一个 comprehensive view ②每个物体至少被一个视角拍到。VLM 输入用 2 个视角，评测用全部视角 | §3.1.2 |

> BlenderGym 的 §3.1.2 是本课题最直接的「工具层」背书：
> 做这套 benchmark 的人**不敢让 VLM 只看一个视角**，而且不敢让视角随机。

### 1.3 Design2Code：自我修订在前端上几乎没用，对小模型是毁灭性的

arXiv 2403.03163（v3）表 1。484 个真实网页，截图→HTML。Direct / Text-Augmented / **Self-Revision**
（Self-Revision = 让模型比较「自己上一版的渲染截图」和「输入参考截图」，自行改进）。

| 模型 | 条件 | Block | Text | Position | Color | CLIP |
|---|---|---|---|---|---|---|
| GPT-4o | Direct | **93.0** | 98.2 | **85.5** | **84.1** | **90.4** |
| GPT-4o | Self-Revision | 92.7 | 98.6 | 84.9 | 83.3 | 90.1 |
| GPT-4V | Direct | 85.8 | 97.4 | 80.5 | **73.3** | 86.9 |
| GPT-4V | Self-Revision | **88.8** | 98.1 | **81.1** | 72.9 | 87.2 |
| Claude 3 Opus | Direct | 90.2 | 97.5 | 77.9 | **71.4** | **87.0** |
| Claude 3 Opus | Self-Revision | 90.3 | 98.1 | 78.1 | 69.7 | 86.6 |
| Gemini 1.0 Pro V | Text-Augmented | **84.8** | **96.9** | 70.4 | **66.3** | 84.4 |
| Gemini 1.0 Pro V | Self-Revision | 84.1 | 96.6 | 70.1 | 66.2 | 84.3 |
| LLaVA 1.6-7B | Text-Augmented | **68.4** | **93.0** | 68.7 | 64.0 | 84.5 |
| LLaVA 1.6-7B | Self-Revision | 62.6 | 91.0 | 64.7 | 62.6 | 83.8 |
| DeepSeek-VL-7B | Text-Augmented | **66.1** | **93.4** | **69.2** | **67.9** | 84.3 |
| DeepSeek-VL-7B | Self-Revision | 30.1 | **38.9** | 28.9 | 28.1 | 79.9 |
| Idefics2-8B | Direct | **46.7** | **80.3** | **55.9** | **58.9** | **81.7** |
| Idefics2-8B | Self-Revision | **12.3** | 22.6 | 13.2 | 14.5 | 78.4 |

原文（§4.1 第 3 条）：
> "Self-revision has some minor improvement on block-match and position similarity for GPT-4V and Claude 3,
> but brings no improvement on Gemini Pro Vision and all other open-source models,
> potentially due to the limited capabilities of LLMs to do self-revision (Huang et al., 2023)."

人类两两偏好（§4.2，100 例 × 5 名标注员多数票）：GPT-4o 上**文本增强与自我修订都没带来实质提升**；
只有 GPT-4V 两种 prompting 都能改善 direct。原文的解释值得抄下来：

> "self-revision needs the model to understand the differences between the two given images
> (the reference screenshot and the screenshot of the initial model generation) and reflect them
> correspondingly in the modified HTML code, which is harder than leveraging text augmentation
> and thus might require more advanced model capabilities."

**这就是「前沿 vs 开源」的关键差距落在哪里的直接证据：差距不在生成，在「看出两张图哪里不一样并把它映射回代码」。**

参考量：GPT-4V self-revision 的产物里，49% 被人判为可与原页互换；64% 的 case 人**更喜欢 AI 生成的页面**
（§4.2 Direct Assessment）→ 高层美观早就饱和，剩下的全是细粒度差异，正是 VLM 的盲区。

### 1.4 自我修正被证伪的主线（非视觉，但是地基）

**Huang et al. 2310.01798（ICLR 2024）"LLMs Cannot Self-Correct Reasoning Yet"**

表 3（intrinsic self-correction，无 oracle）：

| | #calls | GSM8K | CommonSenseQA | HotpotQA |
|---|---|---|---|---|
| GPT-3.5 Standard | 1 | 75.9 | 75.8 | 26.0 |
| GPT-3.5 Self-Correct r1 | 3 | 75.1 | **38.1** | 25.0 |
| GPT-3.5 Self-Correct r2 | 5 | 74.7 | 41.8 | 25.0 |
| GPT-4 Standard | 1 | **95.5** | **82.0** | **49.0** |
| GPT-4 Self-Correct r1 | 3 | 91.5 | 79.5 | 49.0 |
| GPT-4 Self-Correct r2 | 5 | **89.0** | 80.0 | **43.0** |

表 2（**有 oracle 标签**决定何时停）：

| | GSM8K | CommonSenseQA | HotpotQA |
|---|---|---|---|
| GPT-3.5 Standard | 75.9 | 75.8 | 26.0 |
| GPT-3.5 Self-Correct (Oracle) | **84.3** | **89.7** | **29.0** |
| GPT-4 Standard | 95.5 | 82.0 | 49.0 |
| GPT-4 Self-Correct (Oracle) | **97.5** | **85.5** | **59.0** |

**同一个循环，唯一区别是「有没有一个不是自己的判据」，结果从 −6.5 分变成 +2.0 分。**
Llama-2 更极端：62.0 → 43.5 → 36.5（表 4），和 Design2Code 里开源模型的崩塌同形。

机制（§3.3）：GSM8K 上 GPT-3.5 有 74.7% 的 case 不改答案；改的那些里「对→错」多于「错→对」。
三种不同措辞的反馈 prompt 都没能翻正（表 5、表 6）→ **这是能力问题，不是 prompt 问题**。

多智能体辩论也不是自检（§4，表 7）：

| | #responses | GSM8K |
|---|---|---|
| Standard | 1 | 76.7 |
| Self-Consistency | 3 | 82.5 |
| Multi-Agent Debate r1 | 6 | 83.2 |
| **Self-Consistency** | 6 | **85.3** |
| Multi-Agent Debate r2 | 9 | 83.0 |
| **Self-Consistency** | 9 | **88.2** |

→ 等算力下，**朴素多数投票打败辩论**。所谓「批评」带来的提升其实是「一致性」带来的。

**Stechly et al. 2310.12397 "GPT-4 Doesn't Know It's Wrong"**（图着色，NP-complete）：
① LLM 解图着色很差 ② **验证一个着色并不比生成一个更擅长** ③ 批评的「正确性与内容」对迭代 prompting 的最终表现**几乎无影响**
④ 迭代模式看起来有效，真正原因是「正确答案恰好在 top-k 候选里，被外部 verifier 认出来了」。

> 这条和 BlenderAlchemy 的 84%/16% 拆解是同一件事的两种说法：**起作用的是选择，不是批评。**

### 1.5 视觉编码场景里「多轮带截图」的分差（交叉引用 05 节 8.1/8.2）

`05_trajectory_repair.md` §8 已经整理过，这里只抽与本题直接相关的：

| 场景 | 单轮 → 多轮带视觉反馈 | 来源 |
|---|---|---|
| 3D 代码可执行率（报错反馈，非视觉） | 0.692 → 0.972（最多 2 次重试） | 3DCodeBench（2606.01057）表 1 |
| 同上，**形状质量** | 两边都成功的交集上条件 SigLIP **−0.010**、Chamfer +0.001、Uni3D −0.003 | 同上 |
| text-to-3D 视觉自我批评（2 轮，给 4 张自己的渲染图） | ΔSigLIP **+0.003~+0.009** | 3DCodeBench 附录 D.2 |
| **image-to-3D** 视觉自我批评 | ΔSigLIP **−0.006~−0.009**（胜负比 0.58~0.78，即越改越差） | 同上（注：表里 Gemini 3.5 Flash 的 image 行是 +0.0126，与正文矛盾） |
| UI2Code 合成集 N=1,2,3 | 92.0 / 97.0 / 97.0（**N=3 饱和**） | UI2Code^N（2511.08195）表 3 |
| UI2Code 真实集 N=1..5 | 66.0 / 68.0 / 70.0 / 73.0 / 74.0（**N=5 还在涨**） | 同上 |
| CAD 代码 + VLM 自提问自回答验证 | GPT-4：点云距离 **−7.30%**，编译率 **+5.5%**（200 题 CADPrompt） | CADCodeVerify / 2410.05340 摘要 |
| 纯视觉 verifier vs 读确定性状态 | VIGA（Opus 4.7，15 轮纯视觉）MPR 0.67 / SPR 0.70；SimWorlds（读 Blender 活状态）MPR **0.87** / SPR **0.89** | SimWorlds（2607.01766）/ 4DBuildBench 50 场景 |
| 强制单调改进（只接受 reward 超历史最佳） | ArtifactsBench-Lite 21.59 →（+视觉 MLLM reward）24.89 →（+不可渲染判零）25.84 →（+Forced Optimization）**27.88** | ReLook（2510.11498） |

**三条可以直接下的判断**：

1. **「能跑起来」和「做对了」是两件事。** 报错闸只管前者，而前者的提升幅度（+0.28）
   远大于后者（≈0），很容易被误读成「自检有效」。
2. **饱和轮次是任务复杂度的函数**，不是常数（UI2Code 合成 N=3 vs 真实 N=5）。
   固定「反思 3 轮」的 harness 在简单任务上烧算力、在难任务上提前收手。
3. **参考图的「强弱」决定自检的符号**：text-to-3D（弱参考，只有文字）自检微正，
   image-to-3D（强参考，有目标图）自检**转负** —— 因为有强参考时，差异都落在 VLM 看不见的细粒度上。

### 1.6 ArtifactsBench：评测侧已经默认「截图是必需的」

arXiv 2507.04952（腾讯混元，1,825 题）。虽然不是 with/without 视觉反馈的 ablation，但它的协议本身是证据：
自动渲染 + **三步时序截图** + 源码一起交给 MLLM-as-Judge，配**每题平均细粒度 checklist**。
结果：与 WebDev Arena 的排名一致性 **94.4%**，与人类专家的两两一致率最高 **90.95%**。

> 含义：**「截图 + 逐条 checklist」已经足以把人类偏好复刻到 94% 的排名一致性。**
> 这说明做一个够用的视觉 verifier 是可行的 —— 难的不是「评」，是「让生成模型自己去评自己」。
> 该文附录 A.1 自己把 "Exploring Agentic and Iterative Development" 列为未来工作，即**迭代式开发的 ablation 尚无公开数字**。

---

## 2. 为什么模型自检会失败

三类原因，层层叠加：**看不见 → 不想看见 → 没有尺子**。

### 2.1 第一层：VLM 的低层视觉本来就瞎（看不见）

| 盲区 | 实测 | 来源 |
|---|---|---|
| 两线是否相交 | 判 0/1/2 个交点准确率 **47%~85%** | BlindTest / 2407.06581 §4.1 |
| 两圆是否重叠 | **73%~93%**（离得近时更差） | 同上 §4.2 |
| 字母上叠一个圈，问圈的是哪个字母 | 单独认圈、单独认词都 100%，**叠起来就不行** | 同上 §4.3 |
| 计数：相交 / 嵌套的图形 | 分散远离的能数对，**重叠或嵌套的全军覆没** | 同上 §4.4 |
| 网格行列计数 | 「震惊地数不出来」，而同样模型在 DocVQA 上 >90% | 同上 §4.5 |
| 顺着彩色线找终点（2~8 条路径、4 个站） | **23%~50%** | 同上 §4.6 |
| 核心感知任务（相对深度、视觉对应、多视角推理等 14 类，3,807 题） | 人 **95.70%**；GPT-4V **51.26%**、Gemini **45.72%**（仅比随机高 13.17 / 7.63 个点） | BLINK / 2404.12390 摘要 |
| CLIP-blind pair 上的细节分辨 | 人 **95.7%**；除 GPT-4V / Gemini 外**所有 MLLM 低于随机（25%）**；GPT-4V 与人差距 >50 个点 | MMVP / 2401.06209 §2.3 |
| 3D 空间推理（高度 / 朝向 / 位置 / 多物体，2,772 题） | 人 **95.7**；最好的开源 InternVL2.5-8B **50.9**，Claude-3.5V-Sonnet **48.2**，Gemini-2.0-Flash **49.8**；随机 20.9 | 3DSRBench / 2412.07825 表（3DSRBench-real） |
| 非常规相机视角 | 同一个 3D 场景，**常规视角答对、非常规视角答错**，而人类两种都不费力 | 同上 §3.3 + 图 3 |
| 朝向（orientation）子项 | Claude-3.5V-Sonnet **31.4**、Gemini-2.0-Flash **32.2**，随机 16.8 → 几乎是随机水平 | 同上同表 |

**映射到 visual coding 的具体后果**：

| 代码里的错 | 渲出来的样子 | 对应哪个盲区 |
|---|---|---|
| margin 差 4px / transform 偏 0.3 单位 | 两个框挨得近一点 | 两线/两圆是否相交（47~85%） |
| z-index 反了 / 元素被遮住 | 层叠关系 | 重叠与嵌套计数 |
| 颜色 `#f4f6fa` 写成 `#f0f2f6` | 肉眼几乎无差 | 轻微色差（本机实测里是**正例**，一视同仁放行 8/8） |
| 3D 部件装到了背面 | 单视角下「看不见」= 和「不存在」同形 | 单视角深度/朝向歧义（orientation 31~32 分） |
| flex 方向错导致整行换列 | 布局大改 | **不在盲区**（本机实测 wrong_layout 8/8 全抓到） |

→ **规律：错误的「视觉显著性」决定自检能不能成立，和错误的「严重性」无关。**
   一个 0.3 单位的位移在代码里是硬错误，在单张截图里是噪声。

### 2.2 第二层：自己评自己有确认偏误（不想看见）

**Anthropic 官方文档（code.claude.com/docs/en/best-practices，2026 年版）**，逐条原文：

| 主题 | 原文 |
|---|---|
| 没有判据时的停机准则 | "Claude stops when the work looks done. Without a check it can run, **'looks done' is the only signal available**, and you become the verification loop: every mistake waits for you to notice it." |
| 视觉验证的推荐写法 | "**[paste screenshot] implement this design. take a screenshot of the result and compare it to the original. list differences and fix them**" |
| 为什么要换一个模型来判 | "**By a second opinion**: a verification subagent or a dynamic workflow that checks its own findings **has a fresh model try to refute the result, so the agent doing the work isn't the one grading it**." |
| 自我偏爱（最直接的一句） | "**A fresh context improves code review since Claude won't be biased toward code it just wrote.**" |
| 为什么新 context 有效 | "A reviewer running in a fresh subagent context **sees only the diff and the criteria you give it, not the reasoning that produced the change**, so it evaluates the result on its own terms." |
| 官方命名的失效模式 | "**The trust-then-verify gap.** Claude produces a plausible-looking implementation that doesn't handle edge cases. **Fix: Always provide verification (tests, scripts, screenshots). If you can't verify it, don't ship it.**" |
| 证据而非断言 | "Have Claude show evidence rather than asserting success: the test output, the command it ran and what it returned, or **a screenshot of the result**." |
| critic 过激的反面 | "**A reviewer prompted to find gaps will usually report some, even when the work is sound**, because that is what it was asked to do. Chasing every finding leads to over-engineering." |

> Anthropic 自己的工程立场就是「**不要让干活的那个模型给自己打分**」。
> 这不是对模型能力的谦辞，是写进 best-practices 的硬规则。

学术侧的三条佐证：

| 现象 | 数字 | 来源 |
|---|---|---|
| 自我偏爱与自我识别相关 | GPT-4、Llama 2 **开箱就能以非平凡准确率分辨「这是我自己写的」**；微调后自我识别能力与自我偏爱强度**线性相关**，且排除了直接混淆因子 | 2404.13076（ICML 2024） |
| 迎合（sycophancy） | 五个前沿 AI 助手在多种任务上**一致地表现出迎合**；人类偏好数据本身在相当比例上偏好「迎合性回答」 | Anthropic 2310.13548 |
| LLM judge 的自我增强偏置 | MT-Bench 论文把 self-enhancement bias 与 position bias、verbosity bias 并列为 LLM-as-judge 的三大系统性偏置 | 2306.05685 摘要 + §3 |

**判别-批评鸿沟（DC gap）**：CriticGPT（2407.00215 附录 7.7）训了判别器（预测代码是否被篡改）去测
「模型知道多少 vs 说出多少」，结论是**判别器分数不太能预测 critic 的表现**：
在「最大判别器最自信地判错」的那 10% case 上，critic 仍然约 **54%** 抓到了插入的 bug。
→ 「模型其实知道、只是不说」这个直觉**没有被证实**；两条能力路径是分开的，
   所以**训判别器和训 critic 要分开做**（见 §3.1）。

### 2.3 第三层：没有对比基准（没有尺子）

这一层是本机实测最大的发现，单独在 §4 给数据，这里先给机制：

**豁免条款滥用**。给 judge 的 rubric 必须写「不算错」的清单（光照、背景、取景角度、网格精细度），
否则误报满天飞。但**这个清单会被当成挡箭牌**：模型看到一个真实的位移/比例错误，
找不到确切证据，就归因到「相机取景差异」然后放行。

本机实测（snowman，4 judge × 2 rep）：

| 条件 | 应判 fail 却放行 | 其中理由里明确援引「取景/相机/透视/朝向差异」豁免 |
|---|---|---|
| single（单视角并排） | 8 条 | **4 条（50%）** |
| multi（4 视角并排） | 6 条 | **4 条（67%）** |

逐字例子（都是放行，都是错的）：

- `head_up_0.3`（头球上移 0.3，和身体脱开）claude-opus-5-5：
  「…部件形状、相对位置、大小比例与颜色一致，**仅整体取景位置和缩放不同，属允许差异**。」
- `head_up_0.3` doubao：「…**顶部遮挡属于取景带来的允许差异**。」
- `body_r_+20%`（底球放大 20%）doubao：「…**透视带来的视觉大小差异属于相机取景角度范畴，不算错误**。」
- `nose_back`（鼻子长到后脑勺）claude-opus-5-5（多视角条件）：
  「…雪人整体**绕竖轴旋转约 180° 属于取景方向差异，不计入错误**。」

→ **一个把真错误解释成允许差异的模型，和一个看不见这个错误的模型，产物完全一样。**
   而第二种可以靠换工具（多视角）救，第一种只能靠**让模型无法行使豁免权**（固定相机、确定性状态读数、
   代码闸）来救。这与 `04_verifier.md` 的结论一致：**量化阈值和豁免判定都该写成代码，不该写进 rubric。**

**位置偏置**是「并排」方案自带的税：

| judge | prompt | 交换顺序后一致率 | 偏向第一个 | 偏向第二个 |
|---|---|---|---|---|
| Claude-v1 | default | **23.8%** | 75.0% | 0.0% |
| Claude-v1 | rename | 56.2% | 11.2% | 28.7% |
| GPT-3.5 | default | 46.2% | 50.0% | 1.2% |
| GPT-4 | default | **65.0%** | 30.0% | 5.0% |
| GPT-4 | +few-shot | **77.5%** | — | — |

（2306.05685 表 2 + 附录 D.2；BlenderGym §4.2.2 的 Qwen「恒选第二个」是同一现象的极端版。）

→ **做并排对比必须同时跑两种排列并取一致结果**，否则测到的是位置偏置不是视觉能力。
  本机实测里参考恒在上、候选恒在下，这是一个**已知的、未控制的混淆**（见 §5 的改进项）。

---

## 3. 怎么训出自检能力

四层，按「性价比 × 可落地性」排序：**工具层 > 数据层 > RL 层 > 轨迹层**。
（轨迹层最贵且最容易做坏，见 §3.2。）

### 3.1 数据层：故意改坏 → 渲染 → 标注错在哪 → 修复 diff

这条路线有公开背书，且三个领域各有一个标杆。

#### ① CriticGPT（OpenAI，2407.00215）——「篡改」数据流水线的标准做法

管线（§2.2）：

```
Step 0  篡改：标注员在模型写的答案里插入细微 bug，
              并写下「如果我在 code review 里抓到它会怎么说」→ 这就是 gold critique
Step 1  对同一个 (question, tampered answer) 采样多条 critique
Step 2  标注员给 critique 打属性分（综合质量、是否 comprehensive、是否有 nitpick/幻觉、是否包含该 bug=CBI）
Step 3  训 reward model 拟合人类的综合质量排序
Step 4  PPO 优化 critic policy
Step 5  推理期 Force Sampling Beam Search（FSBS）调节 comprehensiveness / 幻觉的取舍
```

**四个必须抄的设计决策**：

| 决策 | 原文做法 | 为什么 |
|---|---|---|
| **难度对抗筛选** | 标注员手里有一个 LLM critic，要求「**三次采样里至少有一次漏掉**」他插的这个 bug | 不加这条，插的 bug 太显眼，训出来的 critic 学不到东西。原文：adversarial collection "noticeably increased the subtlety" |
| **难度随 critic 更新** | 数据收集过程中**换了两次**标注员可用的 critic（先对抗 ChatGPT，后对抗早期 CriticGPT） | 否则数据对最新模型已经太容易 |
| **非平凡性验证** | 训「这段代码是否被篡改过」的判别器，确认**小模型做不了这个二分类**，且随规模平滑提升 | 防止 bug 带有格式/风格类捷径特征 |
| **保留一部分未篡改样本** | 大多数数据来自篡改，但**也混入未改动的样本** | 纯篡改会让分布偏；但未改动样本「标注员一致率更低、训出来更差」，所以只能混、不能主打 |

**结果**：在真实出现的 LLM 错误上，模型写的 critique 在 **63%** 的 case 上被标注员判为优于人写的；
两种 LLM critic（prompted ChatGPT 和 CriticGPT）**抓到插入 bug 的比例都显著高于人类标注员**
（人类中位处理时长 50 分钟）。原文给的三条人类落后原因，按重要性排序：
**评审写得更短 → 缺领域知识 → 任务本身难**。

**迁移性**（最关键的一条，回答「扰动造的数据能不能迁移到真实错误」）：
- 在 **Human Detected Bugs** 分布（真实 RLHF 流程里被人抓到的 bug）上同样有效（图 6、图 7）；
- 能在「被评为 flawless」的 ChatGPT 训练数据里找出**数百个真实错误**，而其中多数是**非代码任务**（OOD）。
→ **篡改造的 error-detection 数据会迁移。**

**必须注意的副作用**：critique 越长越容易抓到 bug，但 nitpick / 幻觉也同比上升
（原文明言这是 precision/recall 取舍）；模型的幻觉率显著高于人类，Human+CriticGPT 组合居中。
→ **RL 的 reward 不能只给 recall**，否则会训出「每次截图都报一串疑似问题」的模型。
   这与 Anthropic best-practices 的 "a reviewer prompted to find gaps will usually report some" 是同一条警告。

#### ② UIClip（2404.12500）—— 视觉侧的同构做法

- 流程：拿现成 UI（网页），**故意修改 style 和 layout 属性引入设计缺陷**，得到 (原版, jitter 版) 成对数据。
- 规模：**230 万对** UI 配质量相关描述；另外收 **1.2K 份专业设计师评分**做对齐与验证。
- 结果：在 design quality / improvement suggestions / design relevance 三项任务上**全面超过体量更大的 LVLM**。
- 落地：论文自己把「quality-aware UI code generation」列为三个应用之一。
→ **这就是「并排的 jitter pair」直接当 reward model 训练数据用的完整先例。**

#### ③ Img-Diff（2408.04594）—— 让 MLLM 学会「找差异」本身

- 用图像编辑生成「物体替换」的近似图像对，经相似度过滤、图文匹配过滤、difference detector 定位差异区，
  再两阶段生成 difference captions。
- 结果（§4.2，图 5）：用「物体替换」数据微调后，
  **LLaVA-1.5-7B 超过 LLaVA-1.5-13B**；微调后的 MGM-7B 在 MMVP 上**比 GPT-4V 和 Gemini 高出最多 12 分**。
- 意义：MMVP 正是「CLIP 看起来一样但内容不同」的细粒度差异集 —— **自检的核心子能力可以被直接训出来，而且 7B 就够**。

#### ④ 现成的 benchmark 构造法也是数据流水线

| 来源 | 构造方式 | 可直接复用的点 |
|---|---|---|
| BlenderGym（2504.01786） | **从目标场景做扰动得到起始场景** | 扰动即监督：扰动参数就是「错在哪」的标签 |
| 本项目 `scripts/vc_verifier/proto/mutate.py` | 13 种 three.js 场景扰动（半径/位移/颜色/缺件/朝向/网格/灯光/背景/相机），`should` 人工定 | 已跑通，见 §4 |
| Design2Code / WebSight | 真实网页做清洗与去外链 | 参考图来源，不含扰动 |

**扰动类别清单建议**（按本机实测的可检出性分层，细节见 §4.3）：

| 层 | 扰动 | 单视角可检出 | 用途 |
|---|---|---|---|
| A 语义级 | 部件缺失、部件换色、布局/堆叠顺序错、维度退化（3D 变 2D 剪影） | **高** | 训基础自检；别只用这层，太容易 |
| B 几何级 | 小位移（横向/竖向）、比例错、嵌入体内 | **中到低** | 主力训练信号 |
| C 视角依赖 | 部件装到背面、朝向反、被遮挡面的错误 | **低（单视角必漏）** | 训「该换视角」的工具调用 |
| D 负例（不许报错） | 换实现方式、换风格、网格精细度、灯光、背景、相机位置、轻微色差 | — | 训特异度；**这层样本不够会训出一个狼来了的 critic** |

### 3.2 轨迹层：离线纠错轨迹做 SFT 学不到自检

`05_trajectory_repair.md` §3.3 / §7 已有完整论证，这里只给与「自检」最相关的一张表。

SCoRe（2409.12917）表 1，MATH，self-correction 的两次 attempt：

| 方法 | Acc@t1 | Acc@t2 | Δ(t1,t2) | Δ 错→对 | Δ 对→错 |
|---|---|---|---|---|---|
| Base model | 52.6% | 41.4% | **−11.2%** | 4.6% | **15.8%** |
| STaR（D_STaR） | 55.4% | 41.2% | **−14.2%** | 5.4% | **19.6%** |
| STaR（D_STaR+） | 53.6% | 54.0% | +0.4% | 2.6% | 2.2% |
| Pair-SFT（D_SFT） | 52.4% | 54.2% | +1.8% | 5.4% | 3.6% |
| Pair-SFT（D_SFT+） | 55.0% | 55.0% | **0%** | **0%** | **0%** |

**两种失败模式一眼可辨**：
- **乱改**：base / STaR 的「对→错」是「错→对」的 3~4 倍 → 模型在改它不该改的东西。
- **行为坍塌**：Pair-SFT+ 的三个 0 —— 模型学会了**第二次 attempt 完全不动**。
  这是「惩罚退步」最自然的收敛点，也是 ReLook 放弃退步罚分的原因（§3.3）。

SCoRe 本体（on-policy 两阶段 RL）把 self-correction 提升 **+15.6%（MATH）/ +9.1%（HumanEval）**。

**SFT 轨迹里该保留什么（结合 05 §7.3 的分层结论）**：

```
一个自检步 = 【为什么要截这张图】+【截图/工具调用】+【从图里读出了什么】+【改法】+【改完再截图】
              ↑ 保留，算 loss        ↑ 保留，算 loss   ↑ 保留，算 loss   ↑ 看后效   ↑ 必须保留
```

| 要素 | 处理 | 依据 |
|---|---|---|
| **验证意图**（"我改了 header 的 margin，先截图确认没把 nav 撞下去"） | **保留且算 loss** —— 这是要学的核心行为 | 这一步是工具调用的触发器，删了就学不到何时该验 |
| **读图结论必须是可核验的具体陈述** | 保留；「看起来不错」一律改写成具体差异或删除 | Anthropic best-practices：show evidence rather than asserting success |
| **验证后发现没问题** | **保留**，比例控制在 25~35% | 否则模型学到「截图必然意味着要改」，会无脑改（对应 SCoRe 的「对→错 15.8%」） |
| **无效自检**（连续截同一张图、看了不改、看了改错） | **删**，但删完要重写衔接处的思考 | WebClipper：去掉「上下文感知的选择性重写」原文用词是 catastrophic collapse |
| **错误的读图结论 + 错误的修改** | 错误前缀**留在上下文、不算 loss** | AgentRefine：错误轮算 loss 最差 |
| **工具调用的原始观察（大图 base64 / 冗长 DOM）** | 压缩成结论，原文删 | SelfCompact：垃圾会锚定后续生成 |

### 3.3 RL 层：怎么给「有效自检」正反馈

**唯一有 visual coding 实测的机制是 ReLook 的 Forced Optimization**（2510.11498，见 05 §4.6）：

| 设计 | 内容 |
|---|---|
| 接受条件 | 一次 refinement 只在 reward **严格超过本轨迹内历史最佳**时被接受 |
| 不达标 | 重采，每轮最多 **10 次**；10 次都不行就终止该轨迹的反思、用历史最佳 |
| 效果 | 得到**单调改进**的轨迹；ArtifactsBench-Lite（3 seed）21.59 → 24.89（+视觉 reward）→ 25.84（+不可渲染判零）→ **27.88**（+Forced Optimization） |
| 训练后行为 | 反思频率**自然收敛到约 2 轮**（不是靠步数惩罚压出来的） |
| **反面教训** | 作者先试了「对退步给负 reward」，模型学会**减少反思次数来躲罚** → reward hacking，弃用 |
| 基座对照 | Qwen2.5-7B-Instruct 在 2~3 轮后**即使拿到高质量反馈也越改越差** |

**SCoRe 的 reward shaping 是同一思想的解析式写法**（§5.2）：
第二次 attempt 的 reward 加一个 progress bonus

```
b(y2 | y1, y*) = α · ( r(y2, y*) − r(y1, y*) )，α > 1.0
```

只强调「翻转了正确性」的转移；外加对参考策略的 KL 约束防止坍塌。
前置还有 Stage I：先做一轮多轮 RL 得到「两次 attempt 解耦」的初始化，否则 Stage II 会塌回「不改」。

**工具调用预算**：OTC（2504.14870，Qwen-2.5 / Qwen-Math，多个 QA benchmark）
把「工具使用效率」直接写进 reward（OTC-PPO / OTC-GRPO）：
**工具调用最多减少 68.3%，tool productivity 最多提升 215.4%，答案准确率基本不变**。

**三条可以直接落地的 reward 设计规则**：

| 规则 | 写法 | 为什么 |
|---|---|---|
| **① 只在提升时给分，不要罚退步** | 接受条件 `r_t > max(r_0..r_{t-1})`；不达标就重采而不是扣分 | ReLook：罚分 → 少反思（hacking）；SCoRe：罚分的自然收敛点是「完全不改」（Pair-SFT+ 的 0/0/0） |
| **② 把「验证」和「修改」分开计分** | 验证步给 shaping bonus（发现了真缺陷 = 下一步 reward 真涨），修改步给终局 reward | BlenderAlchemy 84%/16%：值钱的是判别，要单独给信号 |
| **③ 效率项只做预算不做惩罚** | 硬上限（每轮最多 K 次截图、整条轨迹最多 M 次工具调用）+ 超限直接截断；而非连续扣分 | OTC 证明效率可训；但连续扣分会和 ①冲突 |

**不要做的事**：
- 不要用「单次 VLM 打分的差分」做接受判据。`05` §8.4 的方差拆解：
  Claude Opus 4.7 做 judge 的 σ=8.5 ELO、Qwen3.7-Max 中间 ckpt 的 judge σ=11.4 ELO，
  **而 Web-Shepherd 的实测是单次看输出词 12.2 → 单次取概率 43.1 → 5 次取概率平均 51.4**。
  → 接受判据必须是 K 次重复的均值，且**只有差分超过 2σ 才允许判定**，否则是把噪声当信号。
- 不要让 reward 模型和 policy 同族同权重。自我偏爱与自我识别线性相关（2404.13076）。

### 3.4 工具层：给什么工具最有效

#### 排序（强到弱）

| 排名 | 工具 | 证据 |
|---|---|---|
| **1** | **可读的确定性状态**（scene graph / DOM / a11y tree / BVH 测距 / 修改器栈） | SimWorlds 读 Blender 活状态 MPR **0.87** / SPR **0.89**，对纯视觉 verifier（Opus 4.7，15 轮）0.67 / 0.70 |
| **2** | **与参考并排**（pairwise 而非 pointwise） | PairS 2403.16950 表 1：Mistral-7B NewsRoom coherence 直接打分 0.32 → 两两比 **0.57**；GPT-4-turbo 0.55 → **0.64**；Llama-2-7B 0.02 → **0.43** |
| **3** | **多视角**（固定相机、覆盖所有部件） | BlenderGym §3.1.2 人工固定 ≥3 视角；本机实测：竖向位移召回 0.57 → **0.88**（但特异度崩，见 §4） |
| **4** | **元素级标注 / diff 高亮**（Set-of-Mark 类） | VisualWebArena 表 3：GPT-4V image+caps+a11y 15.05% → **+SoM 16.37%**（+1.32pt） |
| **5** | **合成一张「想象的目标图」再比较** | BlenderAlchemy `-Imagin.` 比 Ours 低 1.3~1.6 CLIP 分 |
| **6** | 单张截图 | 本机实测里对语义级错误够用（缺件/换色/布局 8/8），对几何级不够（比例 4/7、竖向位移 4/7） |

#### 「视觉通道」到底值多少：VisualWebArena 表 3（2401.13649）

| 类型 | 骨干 | 输入 | Overall 成功率 |
|---|---|---|---|
| Text-only | GPT-4 | a11y tree | 7.25% |
| Caption-augmented | GPT-4 | a11y tree + BLIP-2 caption | 12.75% |
| Multimodal | GPT-4V | image + caps + a11y tree | 15.05% |
| Multimodal (SoM) | GPT-4V | image + caps + **SoM** | **16.37%** |
| GPT-4o（后补） | — | image + caps + SoM | 19.78% |
| **Human** | — | 网页 | **88.70%** |

→ 两条读法：
① **纯文本结构（a11y tree）只到 7.25%，加视觉翻倍到 15.05%** —— 视觉通道不可替代；
② **但人类 88.70%** —— 瓶颈不在「有没有图」，在「看不看得懂图」。
   所以「多给一个工具」的收益是递减的（SoM 只 +1.32pt），而**训练感知能力**的空间是 70 多个点。

#### 并排对比为什么更容易发现问题（机制 + 代价）

| 机制 | 证据 |
|---|---|
| 两两比较有**已知的均匀先验**，可以校准；直接打分没有 | PairS §5.2 Calibration |
| 交换两种排列取平均能再提一截 | PairS 表 3：Mistral-7B SummEval 25.6 → **32.9**；Llama-2-7B 15.6 → 16.2；GPT-3.5 36.8 → 38.5（过度自信的模型校准收益小） |
| **代价：位置偏置** | MT-Bench 表 2：Claude-v1 default 一致率 **23.8%**、偏向第一个 75.0%；GPT-4 65.0% → few-shot **77.5%**。BlenderGym：Qwen 恒选第二个 |

→ **工程结论：并排是对的，但必须「两种排列都跑、取一致」**，否则拿到的是位置偏置。

---

## 4. 本机实测：单视角并排 vs 多视角并排

### 4.1 设置

| 项 | 内容 |
|---|---|
| 任务 | snowman（three.js，三球堆叠 + 橙色锥形鼻子），参考场景固定 |
| 候选 | **18 个**：5 个人写候选（`ok_restyled` `ok_lathe` `flat_cutout` `nose_back` `wrong_layout`）+ 13 个程序化变异体（`mutate.py`） |
| 真值 | 9 个 `should=fail`、9 个 `should=pass`，人工标 |
| 条件 A `single` | 上=参考、下=候选，**各一张页面相机截图**（最常见的「截图 + VLM 打分」） |
| 条件 B `multi` | 上=参考、下=候选，**各 4 张 verifier 视角**（正面 0°、侧面 90°、背面 180°、俯视）拼成一行 |
| judge | gpt-6-astra、claude-opus-5-5、gemini-3.8-flash、doubao-seed-2.1-pro |
| 重复 | 每格 2 次，temperature=0 |
| 规模 | 18 × 2 × 4 × 2 = **288 次判定**，7 次 API 失败未解析，**281 条有效** |
| rubric | 算对：形状、部件相对位置与大小、部件颜色一致。不算错：光照、背景、相机取景角度、网格精细度、轻微色差、代码写法 |
| 脚本 | `scripts/vc_verifier/proto/vlm_judge.py`，结果 `runs/vlm_judge.jsonl` |

**两条必须先声明的局限**（否则下面的数字会被过度解读）：

1. **两个条件都是「并排参考」**。本实验对照的是「单视角 vs 多视角」，
   **不是「并排 vs 单图」** —— 后者需要再加一条「只给候选、不给参考」的臂（见 §5）。
2. **参考恒在上、候选恒在下，没有交换排列**。位置偏置是已知未控制的混淆
   （MT-Bench 表 2：Claude-v1 default 一致率只有 23.8%）。

### 4.2 总体：多视角并没有整体占优

| 条件 | 错误召回（should=fail） | 特异度（should=pass） | 总判对率 |
|---|---|---|---|
| single | 70/78 = **0.897**（95% CI 0.81–0.95） | 60/62 = **0.968**（0.89–0.99） | 130/140 = 0.929 |
| multi | 71/77 = **0.922**（0.84–0.96） | 57/64 = **0.891**（0.79–0.95） | 128/141 = 0.908 |

配对比较（同 case × 同 judge × 同 rep）：

| | 计数 |
|---|---|
| 两条件都判对 | 117 |
| 只 single 对 | 11 |
| 只 multi 对 | 8 |
| 都判错 | 2 |
| McNemar 精确双侧 p | **0.65**（不一致对仅 19） |

→ **总体 p=0.65，没有显著差异。单看总分会得出「多视角没用」的错误结论。**
   真正的信息全在拆解里。

### 4.3 拆开看：哪类错误单图能抓、哪类要多视角

按错误类别合池（4 judge × 2 rep，括号为 Wilson 95% CI）：

| 类别 | 变异体 | single | multi | Δ |
|---|---|---|---|---|
| **部件缺失** | `nose_missing` | 8/8 = 1.00 [0.68,1.00] | 8/8 = 1.00 | 0 |
| **部件换色** | `nose_green` | 8/8 = 1.00 | 8/8 = 1.00 | 0 |
| **布局/堆叠错** | `wrong_layout` | 8/8 = 1.00 | 8/8 = 1.00 | 0 |
| **比例错（中球 −20%）** | `mid_r_-20%` | 8/8 = 1.00 | 8/8 = 1.00 | 0 |
| **部件嵌入体内** | `nose_z_half` | 8/8 = 1.00 | 7/7 = 1.00 | 0 |
| **几何维度退化（3D→2D 剪影）** | `flat_cutout` | 7/8 = 0.88 [0.53,0.98] | 7/7 = 1.00 | +0.12 |
| **小位移 · 横向 0.3** | `head_x_0.3` | 7/8 = 0.88 | 8/8 = 1.00 | +0.12 |
| **比例错（底球 +20%）** | `body_r_+20%` | 4/7 = **0.57** [0.25,0.84] | 5/7 = 0.71 | +0.14 |
| **小位移 · 竖向 0.3** | `head_up_0.3` | 4/7 = **0.57** [0.25,0.84] | 7/8 = **0.88** | **+0.30** |
| **朝向错（装到背面）** | `nose_back` | 8/8 = 1.00 | 5/8 = **0.62** | **−0.38** |

负例（should=pass，数字是正确放行率）：

| 类别 | 变异体 | single | multi | Δ |
|---|---|---|---|---|
| 换风格 / 背景 / 灯光 / 半径+5% / 轻微色差 | 5 项 | 8/8 = 1.00（各项） | 8/8 = 1.00 | 0 |
| 网格更粗（segments 16） | `segments_16` | 7/8 = 0.88 | 8/8 = 1.00 | +0.12 |
| 相机移动 | `cam_moved` | 5/6 = 0.83 | 8/8 = 1.00 | +0.17 |
| **换实现方式（球 → LatheGeometry）** | `ok_lathe` | 8/8 = 1.00 | **1/8 = 0.12** [0.02,0.47] | **−0.88** |

**可以下的四条结论**：

1. **语义级错误单图就够**：缺件、换色、布局顺序、明显比例错，single 全是 8/8。
   这类错误的视觉显著性高，不需要换视角。
2. **几何级错误是单图的真空区，多视角能救**：
   竖向小位移 0.57 → 0.88（唯一超出 CI 重叠范围的 Δ）。
   机制很直白：页面相机是透视投影且有仰角，竖向 0.3 的位移被透视吸收了；
   固定的正面 / 侧面正交视角把它变成一条可见的缝。
3. **朝向错是个陷阱：single 的 8/8 是「答案对、理由错」**。
   在 283 条判定里逐条读理由：

   | 条件 | verdict 判对 | 理由中点出「朝向 / 背面 / 反了」 |
   |---|---|---|
   | single | **8/8** | **0/8** |
   | multi | 5/8 | **7/8** |

   single 条件下 judge 一致说「**候选缺少鼻子**」或「**鼻子长到中间那个球上了**」—— 因为页面相机拍不到后脑勺，
   「装在背面」和「不存在」在单张图里完全同形。
   multi 条件下 7/8 正确诊断出「鼻子朝向反了、正面看不到背面才有」，
   但其中 3 条把它归因成「整体绕竖轴旋转 180°，属取景方向差异」而放行。
   → **多视角把诊断质量从 0/8 提到 7/8，代价是给了模型一个新的豁免借口。**
   → **做训练数据时必须用「诊断正确性」而不是 verdict 做标签**，否则 single 的 8/8 会被当成优质样本收进去。
4. **多视角把特异度打崩的 7 条全部来自 `ok_lathe` 一个 case**。

### 4.4 `ok_lathe`：多视角抓到了人和程序化 verifier 都漏掉的真实缺陷

`ok_lathe` 的设计意图是「换一种实现方式（LatheGeometry 代替 SphereGeometry）做出同样的雪人」，
人工标为 `pass`。multi 条件下 4 个 judge 的 8 次判定里有 7 次判 fail，理由高度一致：

- gpt-6-astra：「候选雪人的**头顶存在明显圆形孔洞**，而参考头部是完整封闭的球体。」
- claude-opus-5-5：「**俯视图**中候选场景的头部球体顶端有明显的圆形凹陷/孔洞…」
- gemini-3.8-flash：「候选模型头部的球体**顶部缺失并呈扁平开口状**…」
- doubao-seed-2.1-pro：「候选的雪人头部不是完整球体，**顶部被削平且存在孔洞**…」

查看俯视渲染图：**判定属实**。LatheGeometry 在极点没有封口，头顶是一个真实的洞。

对照三个「权威」的读数：

| 判据 | 对 `ok_lathe` 的读数 | 是否发现孔洞 |
|---|---|---|
| 人工标签 | `pass` | **没有** |
| page 单视角像素分 | 1.000 | **没有** |
| 多视角剪影 IoU | mv_mean 0.998 / mv_min 0.997 | **没有**（结构性盲区：孔洞在内部，不改变外轮廓） |
| 按色体素 IoU | f4f6fa 0.995、ff7a1a 1.000 | **没有**（孔洞体积占比太小） |
| **multi 条件 VLM judge** | 7/8 判 fail，诊断一致 | **发现了** |

**这是本次实验最有价值的单条发现**：

> **剪影 IoU 对「内部孔洞」在数学上就是盲的；体素 IoU 对小体积缺陷在数值上被淹没。
> 而 VLM 读的是 RGB，恰好能补上这两个结构性盲区。
> 程序化 verifier 和 VLM judge 是互补的，不是替代关系。**

同时这也说明：**所谓的「特异度崩塌」里，至少 7/7 是标签错误而不是模型错误。**
把 `ok_lathe` 从负例里剔除后：

| 条件 | 特异度（剔除 ok_lathe） |
|---|---|
| single | 52/54 = 0.963 |
| multi | **56/56 = 1.000** |

→ **修正标签后，multi 在召回和特异度上都不输给 single，在几何类错误上明显占优。**

### 4.5 豁免条款滥用的量化

| 条件 | 应判 fail 却放行 | 理由中援引「取景/相机/透视/朝向差异」 | 涉及的 case |
|---|---|---|---|
| single | 8 | **4（50%）** | `head_up_0.3`×3、`body_r_+20%`×3、`flat_cutout`×1、`head_x_0.3`×1 |
| multi | 6 | **4（67%）** | `nose_back`×3、`body_r_+20%`×2、`head_up_0.3`×1 |

**漏判高度集中在两类**：几何比例（`body_r_+20%`）与竖向位移（`head_up_0.3`）。
这两类恰好是「透视能解释掉」的两类 —— **模型不是没看见，是找到了一个合法的解释**。

→ 工程含义：**凡是能被透视/取景解释掉的判据，一律不要交给 VLM**，
  改用固定正交相机 + 程序化数值断言（本项目的按色体素 IoU 对 `body_r_+20%` 读到 0.679，
  对 `mid_r_-20%` 读到 0.897，都在阈值外，**全部正确判 fail**，见 `runs/snowman_mut/mutation.json`）。

### 4.6 噪声地板：单次 judge 判定不能直接当 reward

| 条件 | judge | 两次重复一致 |
|---|---|---|
| single | gpt-6-astra | 16/17 |
| single | claude-opus-5-5 | **15/18** |
| single | gemini-3.8-flash | 17/18 |
| single | doubao-seed-2.1-pro | 16/16 |
| multi | gpt-6-astra | 17/18 |
| multi | claude-opus-5-5 | **13/16** |
| multi | gemini-3.8-flash | 18/18 |
| multi | doubao-seed-2.1-pro | 17/17 |

temperature=0 下，claude-opus-5-5 在 multi 条件的自一致率只有 **81%**。
这与 `05_trajectory_repair.md` 记录的「collapse stage2 temp0 逐条只 81.6% 一致」是同一个量级。

**聚合后立刻变稳**（4 judge × 2 rep = 8 票多数）：

| 条件 | 多数票判对 | 判错的 |
|---|---|---|
| single | **18/18** | — |
| multi | 17/18 | `ok_lathe`（如 §4.4，实为标签错误） |

→ **硬规则：单次 VLM 判定的 σ 太大，不能直接做 RL 的 accept/reject 判据；
  必须 K≥4 次聚合（多模型优于同模型多采样，因为同模型的错误相关）。**
  注意 single 的 18/18 是靠 4/7 这种薄多数撑起来的（`body_r_+20%`、`head_up_0.3` 都只有 4/7 fail 票），
  换一组 judge 就可能翻面 —— **「多数票判对」和「判得稳」不是一回事**。

---

## 5. 本地实验设计：把「并排 vs 单图」和「单视角 vs 多视角」拆干净

§4 的实验缺一条关键臂（无参考图），且没控位置偏置。下面是补齐后的完整设计，**可在本机跑完**。

### 5.1 四臂设计（2×2 交叉）

| 臂 | 看什么 | 问什么 | 回答哪个问题 |
|---|---|---|---|
| **A1 单图 · 无参考** | 只给候选的 1 张页面截图 | 「这个场景有没有明显做错的地方？错在哪？」 | 自检的下界：**没有尺子时模型能发现什么** |
| **A4 多视角 · 无参考** | 只给候选的 4 视角拼图 | 同上 | 多视角对「无参考自检」的增益 |
| **B1 单图 · 并排参考** | 参考 1 张 + 候选 1 张 | 「候选是否复现了参考？不一致在哪？」 | = §4 的 `single` |
| **B4 多视角 · 并排参考** | 参考 4 张 + 候选 4 张 | 同上 | = §4 的 `multi` |

- **主效应「并排」** = (B1+B4) − (A1+A4)：回答「有没有参考图」值多少。
  这是真正映射到生产的那个问题 —— agent 在改自己代码时，**大多数时候没有参考图**，
  它只有「我想要的样子（文字）」和「我做出来的样子（截图）」。
- **主效应「多视角」** = (A4+B4) − (A1+B1)：= §4 已有的对照，再加一次独立复现。
- **交互项**：预期**多视角在无参考条件下增益更大**（因为无参考时模型更依赖自洽性线索，
  比如「正面看不到鼻子但背面有」这种只能跨视角得到的矛盾）。

### 5.2 必须加的三个控制

| 控制 | 做法 | 依据 |
|---|---|---|
| **位置交换** | 每个 (case, judge, rep) 同时跑「参考在上」和「候选在上」两种排列，**只有两种排列判定一致才计入**；不一致单独统计为「位置敏感」 | MT-Bench 表 2：Claude-v1 default 一致率 23.8%；PairS 表 3：两排列平均（calibration）把 Mistral-7B SummEval 从 25.6 提到 32.9 |
| **标签复核** | 跑之前把 9 个负例逐个看俯视 + 背面渲染图，确认「确实没有缺陷」 | §4.4：`ok_lathe` 标错，直接把 multi 的特异度从 1.000 打到 0.891 |
| **诊断正确性标签** | 除 verdict 外，再标一个 `diag ∈ {正确, 答对理由错, 错}`，用关键词 + 人工抽检 | §4.3：`nose_back` single verdict 8/8 但 diag 0/8 |

### 5.3 规模：要多少才算得准

基于 §4 观测到的效应量做功效计算（α=0.05，power=0.8）：

| 要检出的差 | 每臂需要的判定次数 |
|---|---|
| 0.57 → 0.88（竖向位移，§4 观测到的最大效应） | **32** |
| 0.60 → 0.80 | 82 |
| 0.70 → 0.85 | 121 |
| 0.80 → 0.90 | 199 |

配对 McNemar（§4 实测不一致率 19/138 ≈ 0.14）：

| 真实 OR | 需要的不一致对 | 对应总配对数 |
|---|---|---|
| 2.0 | 69 | **488** |
| 2.5 | 41 | 288 |
| 3.0 | 29 | 207 |
| 4.0 | 20 | 138 |

**→ 推荐配置**（总 2,304 次判定，本机约 1~2 小时）：

```
任务数      3  （snowman + table + desk，tasks/ 下已有）
每任务候选 12  （6 fail + 6 pass，fail 覆盖 A/B/C 三层，pass 覆盖 D 层）
臂          4  （A1 / A4 / B1 / B4）
位置排列    2  （仅 B 臂需要；A 臂无参考，置 1）
judge       4
重复        2
```

- 单个错误类别（跨 3 任务 × 4 judge × 2 rep = 24 次）足以检出 0.57→0.88 级别的差；
- 总配对 ≈ 864 对，足以在 OR=2 的水平上检出主效应。
- **单任务（§4 的做法）只能看定性分层，不能下「谁更好」的结论** —— §4 的 p=0.65 就是这么来的。

### 5.4 要记录的字段

```
task, case, should(fail/pass), mutation_type(A/B/C/D 四层 + 具体类别),
arm(A1/A4/B1/B4), layout(ref_top/cand_top/none), judge, rep,
verdict, diag(正确/答对理由错/错), reason_text,
cited_exemption(bool, 正则匹配 取景|相机|透视|朝向|缩放),
latency_ms, prompt_tokens, image_tokens
```

### 5.5 预注册的判读规则（防止事后挑数字）

1. **主指标**：诊断正确率（`diag == 正确`），**不是 verdict 判对率**。
2. **次指标**：错误召回、特异度、两次重复一致率、位置敏感率。
3. 按错误类别拆开报，每格给 Wilson 95% CI；**CI 重叠的差一律报「未检出差异」**，
   不写「有提升趋势」。
4. 任何 Δ 都要同时给配对 McNemar 的 p 和不一致对数；不一致对 < 20 的直接标「功效不足」。
5. 负例里出现 ≥3 个 judge 一致判 fail 的，**先去复核标签**，不要先下「特异度不够」的结论。

### 5.6 扩展实验（低成本、高信息量）

| 实验 | 做法 | 预期回答 |
|---|---|---|
| **E1 工具消融** | 在 B4 基础上再加两臂：①给场景图文本（物体列表 + 位置/尺寸/颜色）而不给图；②图 + 场景图文本 | 对应 §3.4 排名 1：结构化文本比图强多少 |
| **E2 diff 高亮** | 给参考与候选的逐像素差分热力图（第三行） | 对应 §3.4 排名 4：SoM 在 VWA 上只 +1.32pt，视觉 diff 能不能更多 |
| **E3 想象参考图** | 无参考臂（A1/A4）里，先让文生图按任务描述生成一张参考图再并排 | 对应 BlenderAlchemy `-Imagin.` 的 1.3~1.6 分 |
| **E4 critic 过激度** | 把 rubric 里「不算错」的清单删掉，重跑 B1/B4 | 量化「豁免条款」的双刃效应：删掉后召回多少、误报多少 |
| **E5 自己评自己** | 用生成候选的那个模型当 judge，对比用别的模型 | 直接测自我偏爱（2404.13076），这是本课题最缺的国产模型实测 |

> E5 是唯一能直接验证「Claude 会说服自己放行」这条假设的实验，
> 而且本项目的候选集里 `ok_restyled` / `ok_lathe` 正好是不同实现方式的同一目标，天然适合做自我识别测试。

---

## 6. 结论：自检能力的训练配方

### 6.1 先把问题重述对

公开证据不支持「教会模型反思」这条路线。它支持的是：

```
自检 = 调用一个自己无法糊弄的判别器 + 读懂它的输出 + 在分数不升时回滚
       ↑ 工具/环境的事            ↑ 感知能力的事    ↑ RL 的事
```

三个支点各有独立证据：

| 支点 | 证据 |
|---|---|
| **判别器必须独立** | BlenderAlchemy：视觉给评估器拿回 84% 增益，给生成器只 16%；Huang 2310.01798：有 oracle 时 GPT-4 95.5→97.5，无 oracle 时 95.5→89.0；Anthropic 官方："the agent doing the work isn't the one grading it" |
| **感知能力可以单独训** | Img-Diff：物体替换的差异数据微调后 7B 超过 13B，MGM-7B 在 MMVP 上比 GPT-4V/Gemini 高最多 12 分；UIClip：230 万 jitter 对训出的小模型全面超过大 LVLM |
| **回滚必须是硬机制** | BlenderAlchemy `-Revert` 逐轮 27.1/26.4/26.6/25.8 单调发散；ReLook Forced Optimization +2.0 分；罚分会被 hack 成「少反思」 |

### 6.2 配方（按实施顺序）

#### 第 0 步：先把环境做成可读、可回滚的（最高优先级，非训练工作）

| 要做的 | 为什么 |
|---|---|
| 固定正交多视角渲染（≥3 视角，保证每个部件至少被一个视角拍到） | BlenderGym §3.1.2 的原话是「遮挡或不完整的视角会给 VLM 编辑引入偏置」 |
| 把能程序化判的全部程序化（按色体素 IoU、BVH 测距、DOM 几何、a11y tree） | §4.5：`body_r_+20%` VLM 只有 4/7，体素 IoU 0.679 稳判 fail；SimWorlds MPR 0.87 对纯视觉 0.67 |
| 场景快照 + 可回滚（含上下文与文件系统对齐） | 05 §9①：AgentRewind 不回滚环境 −43.9pp |
| **保留 VLM judge 作为补充，不要替换掉** | §4.4：剪影 IoU 对内部孔洞数学上盲，VLM 7/8 抓到了 |

#### 第 1 步：数据层 —— 造「看图发现错误」的样本

```
取一个已验证正确的参考实现
  → 程序化扰动出 K 个坏版本（四层：A 语义 / B 几何 / C 视角依赖 / D 不该报错的负例）
  → 渲染（固定多视角 + 页面相机）
  → 标注：错在哪（自然语言）+ 对应的代码 diff + 应该用哪个视角才能看到
  → 对抗筛选：当前 critic 三次采样至少漏一次才收（CriticGPT §2.2.1）
  → 非平凡性校验：训个「有没有被扰动」的二分类器，确认小模型做不了（CriticGPT 附录 7.7）
```

配比建议（无公开最优解，以下为基于 §4 可检出性分层的推断）：

| 层 | 占比 | 理由 |
|---|---|---|
| A 语义级（缺件/换色/布局） | 15% | 太容易，single 全 8/8，只做 anchor |
| **B 几何级（小位移/比例/嵌入）** | **40%** | 主力信号，single 只有 0.57~0.88 |
| **C 视角依赖（朝向/遮挡面）** | **20%** | 唯一能训出「该换视角」这个工具调用决策的 |
| **D 负例（换实现/换风格/灯光/相机/微色差）** | **25%** | 不够会训出狼来了的 critic；§4 里 7 条误报全在这层 |

**三条硬要求**：
1. **标注的是「诊断」不是「verdict」**。§4.3 的 `nose_back`：single verdict 8/8 但诊断 0/8，
   当正样本收进去就是在教模型「看不到就说缺失」。
2. **负例必须包含「不同实现方式产出同一结果」**（本项目的 `ok_lathe` / `ok_restyled`），
   否则模型学成「只要像素不一样就是错」。
3. **标负例之前先看多视角渲染**。`ok_lathe` 的教训：人工标 pass，实际有洞。

#### 第 2 步：工具层 —— 定义模型可以调用的验证动作

| 工具 | 签名 | 何时给分 |
|---|---|---|
| `render(views=[...])` | 返回指定视角的渲染图 | 调用后下一步 reward 真涨才算有效 |
| `scene_state(path)` | 返回结构化场景状态（物体树、包围盒、材质、父子链） | 优先级最高（SimWorlds） |
| `diff_against(reference, layout=both)` | 并排对比，**自动跑两种排列并返回一致/不一致** | 位置偏置必须在工具里消掉，不能指望模型自觉 |
| `assert_geometry(expr)` | 程序化断言（距离、半径比、包围盒重叠） | 把「能被透视解释掉」的判据从 VLM 手里拿走（§4.5） |

预算：每轮最多 K 次截图、整条轨迹最多 M 次工具调用，**超限直接截断，不做连续扣分**（OTC 证明效率可训，
但连续扣分会和「只在提升时给分」冲突）。OTC 的参考量级：工具调用最多减 68.3%，准确率基本不变。

#### 第 3 步：轨迹层 —— SFT 只教格式，不指望教能力

| 保留 | 算 loss | 比例 |
|---|---|---|
| 验证意图（为什么要截这张图） | 是 | — |
| 工具调用本身 | 是 | — |
| 从图里读出的**具体**差异（禁止「看起来不错」） | 是 | — |
| **验证后发现没问题** | 是 | **25~35%** |
| 错误的读图 + 错误的修改 | **否**（留上下文不算 loss） | — |
| 连续重复截图 / 看了不改 / 改完更差 | **删**，并重写衔接处的思考 | — |
| 原始大图 base64 / 冗长 DOM | 删，压成结论 | — |

**不要指望 SFT 能教出自检**：SCoRe 表 1，Pair-SFT D_SFT+ 的 Δ 是 0%/0%/0%（学会了完全不改）。
SFT 的作用是让模型**会用这套工具、输出格式对**，能力靠下一步。

#### 第 4 步：RL 层 —— 让自检变成单调改进

```
for each refinement step t:
    r_t = w_exec · 可执行(0/1)
        + w_prog · 程序化断言通过率
        + w_vlm  · mean(K≥4 个异构 judge 的两两比较分)     # K 次聚合，不是单次
    accept if r_t > max(r_0 .. r_{t-1}) + 2σ               # σ 是 judge 噪声，事先量
    else: 重采（每轮最多 10 次），仍不达标则终止反思、回退到历史最佳
```

| 设计点 | 取值/做法 | 依据 |
|---|---|---|
| 接受判据 | 严格超历史最佳，**不设退步罚分** | ReLook（罚分 → 学会少反思） |
| progress bonus | `b = α·(r_t − r_{t−1})`，α > 1 | SCoRe §5.2 |
| 防坍塌 | 先做一轮解耦两次 attempt 的 RL 初始化，再进第二阶段；带 KL 约束 | SCoRe Stage I |
| 判据噪声 | K ≥ 4 个**异构** judge；差分超 2σ 才判定 | §4.6（claude-opus-5-5 temp0 自一致率 81%）；05 §8.4 |
| judge 不能同族 | reward 模型与 policy 不共权重、不同族 | 2404.13076：自我识别与自我偏爱线性相关 |
| 效率 | 硬预算截断，不连续扣分 | OTC 2504.14870 |
| 分离计分 | 验证步给 shaping、修改步给终局 | BlenderAlchemy 84%/16% |

#### 第 5 步：评测 —— 别用 verdict 判对率收车

| 指标 | 口径 |
|---|---|
| **主**：诊断正确率 | 不是 verdict；§4.3 的 8/8 vs 0/8 |
| 分层召回 | 按 A/B/C 四层分开报，CI 重叠就报「未检出」 |
| 特异度 | 负例里必须含「换实现」类 |
| 自一致率 | 同条件两次重复；<85% 的 judge 不能单独做 reward |
| 位置敏感率 | 两种排列判定不一致的比例 |
| **无效自检率** | 截了图但下一步 reward 没涨的比例；ReLook 训练后收敛到约 2 轮反思 |

### 6.3 最容易踩的六个坑

| 坑 | 症状 | 解药 |
|---|---|---|
| 把「可执行率提升」当成「自检有效」 | 报错反馈把可执行率从 0.692 拉到 0.972，但形状质量 ΔSigLIP −0.010 | 分开报「能跑」和「做对」两个指标 |
| 用单次 VLM 分差做剪枝/接受判据 | 剪掉的是噪声 | K≥4 聚合 + 2σ 门槛 |
| 负例里没有「换实现」 | critic 学成像素比对器 | D 层占 25% |
| 只看 verdict 不看诊断 | 收进「看不到就说缺失」的毒样本 | 主指标改成诊断正确率 |
| 对退步罚分 | 模型学会少反思（reward hacking） | 只在超历史最佳时接受，否则重采 |
| 让生成模型自己当 judge | 自我偏爱 + 豁免条款滥用 | 异构 judge；能程序化的判据全部代码化 |

### 6.4 一句话

> **不要训「会反思的模型」，训「会调用一个它糊弄不了的判别器、并在分数不升时回滚的模型」。**
> 前沿模型相对开源模型的差距，实测落在「看出两张图哪里不一样并把它映射回代码」这一步
> （Design2Code：GPT-4V self-revision block 85.8→88.8，Idefics2-8B 46.7→12.3），
> 而这一步是可以用「故意改坏 → 渲染 → 标注错在哪」的合成数据单独训出来的
> （Img-Diff：7B 微调后在 MMVP 上超过 GPT-4V 最多 12 分）。

---

## 附录：本篇引用清单

| 编号 | 标题 | 用在哪 |
|---|---|---|
| 2404.17672 | BlenderAlchemy: Editing 3D Graphics with Vision-Language Models（ECCV 2024） | §1.1 84%/16% 拆解、表 2/表 3 |
| 2504.01786 | BlenderGym（CVPR 2025） | §1.2 verifier 一致率 0.66/0.79、verifier scaling、§3.1.2 视角设计 |
| 2403.03163 | Design2Code（v3） | §1.3 self-revision 表 1、人类评测 |
| 2310.01798 | LLMs Cannot Self-Correct Reasoning Yet（ICLR 2024） | §1.4 表 2/3/4/7 |
| 2310.12397 | GPT-4 Doesn't Know It's Wrong（图着色） | §1.4 |
| 2507.04952 | ArtifactsBench（腾讯混元） | §1.6 94.4% / 90.95% |
| 2410.05340 | Generating CAD Code with VLMs（CADCodeVerify，ICLR 2025） | §1.5 点云 −7.30%、编译率 +5.5% |
| 2407.06581 | Vision language models are blind（BlindTest） | §2.1 |
| 2404.12390 | BLINK | §2.1 人 95.70% / GPT-4V 51.26% |
| 2401.06209 | Eyes Wide Shut?（MMVP） | §2.1、§3.1③ |
| 2412.07825 | 3DSRBench | §2.1 朝向 31.4/32.2 |
| 2404.13076 | LLM Evaluators Recognize and Favor Their Own Generations（ICML 2024） | §2.2 自我偏爱 |
| 2310.13548 | Towards Understanding Sycophancy in LMs（Anthropic） | §2.2 |
| 2306.05685 | Judging LLM-as-a-Judge（MT-Bench） | §2.3 位置偏置表 2 |
| 2403.16950 | Aligning with Human Judgement / PairS | §3.4 pairwise vs pointwise 表 1、校准表 3 |
| 2407.00215 | LLM Critics Help Catch LLM Bugs（CriticGPT） | §2.2 DC gap、§3.1① 篡改流水线 |
| 2404.12500 | UIClip | §3.1② 230 万 jitter 对 |
| 2408.04594 | Img-Diff | §3.1③ MMVP +12 |
| 2409.12917 | SCoRe（Google DeepMind） | §3.2 表 1、§3.3 reward shaping |
| 2504.14870 | OTC: Optimal Tool Call | §3.3 −68.3% / +215.4% |
| 2401.13649 | VisualWebArena | §3.4 表 3 模态分差 |
| 2310.11441 | Set-of-Mark Prompting | §3.4 |
| 2305.20050 | Let's Verify Step by Step | §3.3 PRM 背景 |
| — | Anthropic, Best practices for Claude Code（code.claude.com/docs/en/best-practices，2026） | §2.2 全部原文引用 |
| 交叉引用 | `05_trajectory_repair.md` §4.6 / §7 / §8 / §9 | ReLook、3DCodeBench、UI2Code^N、SimWorlds、Visual-SDPO、噪声地板 |
| 交叉引用 | `04_verifier.md` | verifier 选型、「阈值写代码不写 rubric」 |
| 本机实测 | `scripts/vc_verifier/proto/vlm_judge.py` + `runs/vlm_judge.jsonl`（288 次判定） | §4 全部 |

