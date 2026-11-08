# 19 · 审美这一维能不能做成可用的训练信号

- 查证日期：2026-10-15
- 本文回答的问题：成稿把审美推迟到最后，理由（人类众包 Elo 周期长、平局率 26%、单人标注 α 只有 0.368）是成立的，但它只说明「现成做法不好用」。本文回答「那该怎么做」
- 前置：`04_verifier.md`（分层 verifier）、`07_capability_spec.md`（D3 维度与噪声地板）、`16_primary_sources.md`（Anthropic 四维评审器原文）、`90_local_experiments.md`（VLM judge 翻面率）
- 新增本机实验（全部可重跑，代码在 `scripts/vc_verifier/web/`）
  - 审美探针与判据：`aesthetic.js` / `aes_verify.js`，变异集 `aes_mutants.js`，跑测 `run_aes.js` → `out/aes_results.json`、`out/aes_ref.json`（§6）
  - 批次级集中度：`aes_concentration.js` → `out/aes_conc_gallery.json`、`out/aes_conc_basic.json`（§4.8）
- 标记：**[原文]** 可在链接里找到原句；**[实测]** 本机跑出来的；**[推断]** 本文作者推出，无一手证据
- 全文不用美元符号，金额写「美元」

---

## 0. 七条先行结论

1. **「审美」里有一半是可以做成零噪声程序化判据的，而且现有功能侧 verifier 对这一半完全瞎。**
   [实测] 构造 11 个只破坏审美、不破坏功能的变异（能跑、无报错、不溢出、不遮挡）：
   现有功能判据 W0~W4 对其中 **9 个判过**（剩下 2 个是因为改色顺带把 WCAG 对比度弄挂了才被 axe 抓到，不是抓到了审美问题）。
   本文新写的审美判据在这 9 个盲区里补上 **7 个**，并且 **8 个合法改版（换品牌色、换尺度、深色主题、加留白、类名重命名、压缩 HTML）全部不误杀**。

2. **但不是所有审美子项都有判别余量。两个子项实测必须放弃当闸。**
   - **圆角一致性**：参考页本来就有 4 种圆角（6 / 8 / 10 / 999px），变异推到 6 种，余量不足
   - **栅格对齐**：该挂的 A09 对齐率 0.707，而**不该挂且审美更好**的 P03（间距规整到 8 的倍数）是 0.765 —— 可分离阈值只剩 0.058 余量，且一个好页面比多数坏页面更接近失败。这种阈值不能当闸

3. **「AI 味」在单页尺度上测不出来，它是分布量，而且三个最可能的抓手都被证伪了。**
   单页只能查**具名 tell**（Inter 字体、紫渐变、白卡）。[实测] 注入 Anthropic 点名的那一组能被 tell 判据 100% 抓到，20 个页面里只有它命中、品牌蓝渐变不误报 —— 但这只是「像不像那几个已知默认」。
   - 「AI 味」的数学表述是 **「每个输出都挺原创，但彼此雷同」**：LLM 的发散任务变异度 0.459 对人类 0.738（效应量 2.2），而**个体原创性并不差**（0.711 对 0.696）。所以它是 across-prompt 的分布量 → **天然不能当 per-sample reward**
   - 配色 / 字体 / 布局模板的**分布熵或集中度**：**学界零篇**（11 篇 benchmark 全文检索全 0 命中）
   - 「用 AI 生成判别器的置信度当指标」：**判别器不存在**，零论文零数据集
   - 唯一真正做了的是 Design Theater 的 DHI（2026-07），但它**没有人类基线、不报 per-model 分数**
   [实测] 本文把「样式集中度」实现并跑了两批模型生成页（11 + 12 页），得到一条关键发现：
   **gallery 集 Inter 占比 100%**（任何「禁 Inter」lint 全判挂），**basic 集 Inter 占比 0%**（lint 满分通过），
   但 **basic 集的字体维度 HHI = 1.00，比 gallery 的 0.50 更集中** —— 它只是收敛到了另一个取值上。
   → **具名 tell 和分布集中度测的是两件不同的事，集中度更鲁棒。规则表只能查已知默认值，查不到「收敛」本身。**
   顺带：紫渐变在两批里都是 **0%** —— 那个被博客反复引用的症状，在本项目产物里一次都没出现。
   一条好消息：**收敛至少有一部分是 harness / system prompt 规定出来的**。Google 的 Generative UI 把「跨生成风格一致」当 feature 在做，system instruction 里显式写了 Tailwind 默认字体、鼓励 gradients、禁止外部文件 —— 逐条对上 Anthropic 点名的三个症状。这一部分**改 prompt 就能拿回来，不用动训练**。详见 §4

4. **Anthropic 四维里有一维半可以直接程序化，两维半只能靠模型，而且它们的权重正好反了。**
   Craft（排版层级、间距一致性、配色和谐、对比度）**几乎整维可程序化**——这正是本文 §6 实测的那套判据。
   而官方把 Craft **降权**，理由是「模型默认就及格、没有区分力」[原文]。
   [推断] 这条「降权」结论只在他们的生成分布下成立；一旦进入 RL，Craft 恰好是唯一能当硬闸、不会被 Goodhart 的那一维。

5. **把审美做成能驱动迭代的指标，人力不是主要瓶颈，题量才是。**
   [核实] AUV-Bench 的 ICC(1,1)≈0.369，按 Spearman-Brown 外推：要 ICC≥0.80 需要**每条 UI 7 个标注者**，≥0.90 需要 **16 个**。
   但做系统级比较时，**加题比加人划算**：k 从 3 加到 16（人力 ×5.3），检测 0.2 分差所需题量只从 185 降到 130（省 30%）。
   加人只在「需要单条 UI 可信判读」（做 GT、做 case 分析）时才值得。

6. **「凭人判」那一半的天花板约 60%，而且这个数字是口味本身不收敛造成的，不是模型不行。**
   DesignPref（arXiv 2511.20513）让 **20 位职业设计师各评完同样 600 对**：
   二元一致只有 **0.624**，**Krippendorff α = 0.248**，**28.5% 的对子两两分歧率 ≥ 96%**。
   在这批数据上，**用 20 倍数据 pool 训练的 UIClip 只有 57.45%，个性化才 60.16%**。
   → 任何声称单一全局审美 reward 显著超过 60% 的结果，先怀疑泄漏
   （TOCHI 2022 已经在 Webthetics 上抓到过一次：r≈0.85 含训练/验证集重叠，真实值 LCC≈0.752）。
   → **这也意味着 §6 那套程序化判据的价值被低估了**：它不受这个天花板约束，因为它测的不是「谁更好看」。

7. **两条会让审美 reward 在接近最优时反向的证据，必须写进设计里。**
   - **经典计算美学指标全部单调可刷，方向一致**（白空间越多、边缘越少、颜色越少、对齐线越少分越高）
     → **RL 必然收敛到空白单列页**。AIM 的 `cp11` 色彩和谐更糟：源码自带警告说模板 X 几乎总是最小距离，**模型会学会把颜色铺满色轮**
   - **Duan et al. CHI 2024 的实测：工具性能随 UI 变好而下降**（"general decrease in performance as the UI improves"），
     首轮 52% accurate 到后续迭代掉到 39%；标签一致性 **Fleiss κ = 0.112**
   → 处置：这类判据只能做**双边区间**或 **veto**，不能做单调排序器（§7.1）

---

## 1. 先把「审美」拆开

三类东西混在一个词里，训练上的处置方式完全不同。

### 1.1 分类表

| 类 | 子项 | 现有度量手段 | 确定性 | 谁在用 |
|---|---|---|---|---|
| **A 可程序化** | 文本对比度（WCAG 1.4.3 / 1.4.11） | axe-core / Lighthouse 规则引擎；或自己按相对亮度公式算 | **完全确定**，零噪声 | A11yn 拿 axe 当 GRPO 奖励（2510.13914）；本项目 `probe.js` 的 W2 层 |
| | 视觉层级单调性（h1..h6 字号与字重单调、标题 ≥ 正文） | 读 computed style，逐级比较 | **完全确定** | [实测] 本文 `hier` 判据 |
| | 字号尺度自洽（种类数、相邻比值的变异系数） | 读 computed style 聚合 | **完全确定** | [实测] 本文 `scale` 判据 |
| | 字体族数量 | 读 computed style | **完全确定** | [实测] 本文 `family` 判据 |
| | 行高与行长（1.35~1.8 倍；45~90 字符/行） | 读 computed style + 几何，按 CJK/拉丁分别估字宽 | **确定**，但需要题面有真实正文 | [实测] 本文 `lh` / `len` 判据 |
| | 间距节奏（是否都是某个基数的倍数、取值种类数） | 读所有 margin/padding/gap，**自动选基数**后算占比 | **确定**，但基数不能预设（见 §1.2） | [实测] 本文 `spacing` 判据 |
| | 配色的色彩空间关系（色相家族数、色相熵、中性色占比） | sRGB → OKLCH，色相分箱 | **确定** | [实测] 本文 `hue` 判据 |
| | 留白比例（墨水覆盖率） | 行扫描算已绘制区域的面积并集 | **确定** | [实测] 本文 `ink` 判据 |
| | 响应式下不塌（横向溢出、元素越界、遮挡） | 多视口 `scrollWidth > clientWidth` + 盒模型 | **完全确定** | 本项目 `probe.js` 的 W1 层；WebCoderBench 的 iPhone 12 Pro 溢出检查 |
| | 栅格对齐 | 块级元素左边界聚类 | **实测判别余量不足，放弃当闸**（§6.3） | 无 |
| | 圆角一致性 | 读 border-radius 取值种类 | **实测判别余量不足，放弃当闸**（§6.3） | 无 |
| **B 有共识、难程序化** | 排版品味（字体搭配是否得体、字重对比是否有意） | 只能 rubric 化模型评审 | 中等：rubric 后标注者一致率可到 92%（但见 §5.1 的口径修正） | Anthropic 四维的 Craft 维；AUV-Bench 的 Typography 维（α=0.334） |
| | 配色协调（不只是色相数，是搭得好不好） | 同上 | AUV-Bench 的 Color 维 **α=0.328，全表最低** | AUV-Bench |
| | 组件一致性（同类组件在全页是否统一） | design token 合规检查能覆盖一部分；剩下靠评审 | AUV-Bench 的 Component Consistency **α=0.399** | AUV-Bench |
| | 动效克制（有没有、过不过、时长是否一致） | 可读 `animation-duration` / `transition` 的取值分布；但「克制」要评审 | 低 | 无公开度量 |
| | 版式层级与信息密度是否服务于内容 | 只能评审 | AUV-Bench 的 Layout **α=0.431，全表最高** | AUV-Bench |
| **C 纯主观** | 风格取向（极简 / 拟物 / 粗野主义） | 不可度量成优劣，只能度量「是否符合题面指定的风格」 | 无（优劣维度上） | 无 |
| | 品牌调性 | 同上 | 无 | 无 |
| | 原创性 | **本文的核心空白**：单页上只能查具名 tell；真正的原创性是分布量（§4） | 低 | Anthropic Originality 维（无第三方量化） |

### 1.2 分类里最反直觉的一条：别预设 4px 栅格

[实测] 参考页是一个手写的、axe 全过、多视口不塌的干净页面。它的间距取值分布：

| 基数 | 是其倍数的占比 |
|---|---|
| 2 | **91.4%** |
| 4 | **57.8%** |
| 8 | 32.8% |
| 10 | 20.7% |
| 16 | 16.4% |

12 个不同取值：2 / 6 / 8 / 9 / 10 / 12 / 14 / 16 / 19.9 / 20 / 24 / 28。

→ **一个好页面只有 57.8% 的间距落在 4 的倍数上。** 任何写死「间距必须是 4 的倍数」的 lint 规则都会把它判挂。
正确做法是**自动选基数，再看占比**：判据写成「存在某个基数使 ≥70% 的取值是其倍数」，参考页在 base=2 下是 0.914，有 0.214 的余量。

这一条是本文最该先说的工程细节：**审美类程序化判据的阈值必须从参考页反推，不能从设计教条里抄。**

---

## 2. 已有的审美度量与数据集

按「能不能当 RL reward」排序。

### 2.1 学习型审美打分器

| 工作 | 判据定义 | 规模 | 与人类一致 | 能当 reward？ |
|---|---|---|---|---|
| **UIClip**（arXiv 2404.12500，2024-04，UIST 2024） | 分数 = 截图 embedding 点乘文本 embedding，文本前缀固定为 `"ui screenshot. well-designed. " + caption`；截图 224×224 滑窗编码后取平均。双损失：对称 CLIP 交叉熵 + **pairwise 对比损失**（把更优截图对 "well-designed" 的分推高） | JitterWeb **2,466,969** 行（约 30 万爬取网页抖动而来）；paired 313,186；人评 BetterApp 2,350 行（约 1,175 对）。模型 CLIP B/32，**约 151M 参数** | 12 位设计师 pairwise 为真值，**成对选择准确率 75.12%**；网页缺陷检测 87.1%；纯 CLIP 预训练 65.42%；**GPT-4V 仅 51.58%**、LLaVA 54.59%。**评分者间 Krippendorff α = 0.37** | ✅ **最现成的一个**：pairwise 口径抗刷、151M 能塞进 RL 内循环、权重与训练数据全公开（HF `biglab`，未标 license）。<br>⚠️ 但**论文自己只做了 best-of-5 重排**，reward model 列为 future work；**查遍 2025~2026 没有任何工作把 UIClip 当 GRPO / PPO 的 reward** |
| **UICrit**（arXiv 2407.08850，2024-07，UIST 2024） | 983 个移动 UI 的设计批评 + 5 个维度打分：aesthetics(1–10)、usability(1–10)、design_quality(1–10)、learnability(1–5)、efficiency(1–5) | 论文 **983 UI / 3,059 条 critique / 7 位设计师**（Discussion 里又写 938，自相矛盾）；**公开版 1,000 屏 / 11,344 条 critique**，966 屏恰好 3 人标 | **论文根本没报一致率**（论文版每屏只 1 个标注者）。从公开版 966 个三标注者屏重算：**aesthetics ICC(1,1) = +0.024**、usability +0.048、design_quality +0.026；两两 r ∈ [−0.012, +0.093]；**组内 SD 1.00 ≈ 总 SD 1.02** | ❌ **数值评分绝对不能当 reward** —— ICC ≈ 0.02 意味着方差几乎全是标注者噪声，屏幕级信号约等于 0，拿它当回归目标等于拟合纯噪声。<br>另两条：design_quality **48% 恰好是 6**（量程被压死）；11,344 条里**1,058 条是纯 Gemini 产出**、1,893 条 Gemini 辅助。<br>✅ **文本 critique + bbox 可以**当 critic 的 SFT 语料 |
| **DesignPref**（arXiv 2511.20513，2025-11）⭐ | 400 个生成设计（GPT-5 / Gemini-2.5-Pro）× 100 屏描述 → 600 对；**20 位职业设计师每人全评 600 对** = 12,000 条。四档无中立：A≫B / A>B / B>A / B≫A | 12,000 对 | **本文最关键的一个数**：二元平均成对一致 **0.624**，Cohen κ = Krippendorff **α = 0.248**；四档一致 0.386、**α = 0.104**；**28.5% 的对子两两分歧率 ≥ 96%** | ⚠️ **它本身就是「审美 reward 的天花板测量」**：用 20 倍数据 pool 训练的 UIClip 只有 **57.45%**（SRCC 0.196），**个性化才到 60.16%**；pooled GPT-5 RAG 57.62%。<br>→ **单一全局审美 reward 的上限就在 60% 附近，因为口味本身不收敛。** 见 §5.0 |
| **WiserUI-Bench**（arXiv 2505.05026，ACL 2026）⭐ | **全场唯一客观真值**：300 对真实 UI，**胜者由真实 A/B 测试转化率决定**（来源 vwo.com 168 / goodui.org 103 / abtest.design 29；web 252 / mobile 48）。另有 684 条专家 rationale，标注 12 条 UX 定律 | 300 对 | **最佳 MLLM 仅 GPT-4o 60.11%**（随机 50%）；一致准确率最佳 InternVL-2.5-38B 34.56%（随机 25%）。**位置偏置极大**：o1 的胜者在前 16.56% / 在后 **97.78%**；GPT-4o 31.89% / 88.33% | ⚠️ 规模太小（300 对）不能当训练信号，**但是最好的外部校准集** —— 它的标签不依赖任何人的口味。repo `jeochris/wiserui-bench` 完整发布 |
| **AesCoder / Code Aesthetics with Agentic Reward Feedback**（arXiv 2510.23272，2025-10，ICLR 2026） | **三件套 agentic reward**：① `r_exec` = HTMLHint 全过 +1 / 否则 −1（纯规则）② `r_static` = GPT-5 对 Playwright 全页截图打 3 维分（指令对齐 / 视觉元素 / 布局凝聚），0–100 ③ `r_interact` = WebVoyager + GPT-4o 跑最多 N 次交互，每次 1/0 求和（训练 N=3）。**r = 0.1·r_exec + 0.8·r_static + 0.1·r_interact**，GRPO 组内归一 | AesCode-358K（158K plot + 200K webpage）；OpenDesign 基准 840 例 | **GPT judge 对人类 80.9%**（10 人 × 200 对 = 2,000 条），而**人与人只有 68.7%**；与 Design Arena 排名 **Spearman 0.98 / Kendall 0.91** | ✅ **目前唯一完整跑通 RL 的方案**（Qwen3-4B / Qwen2.5-Coder-7B，VeRL，约 77 天 × 11 节点 8×MI300）。<br>关键消融：只让 RM 读代码文本打分 0.71，与 RFT / DPO 持平；**完整 agentic 版 1.04** → **只读代码的自评几乎等于没评**。<br>⚠️ 论文**未检测 reward hacking**；三项量纲不同（0–100 与 ±1）却直接加权，没解释 |
| **WebGen-R1**（arXiv 2604.20398，2026-04） | **级联**：static 不合规 → ψ=0；build 失败 → ψ=0；渲染成功才算 `R = s_vis + 0.1·s_func + 0.1·s_cot`。`s_vis` = GPT-4o 对截图打 **0–5** 分，5 维（布局和谐 / 配色 / 字体层级 / 可见功能 / 风格契合）。**VLM 只对通过前序闸的样本调用** | WebGen-Bench 101 任务 + WebDev Arena 119 任务 OOD | **reward 对 3 位前端开发者聚合评分：Pearson r = 0.762 / Spearman ρ = 0.734**（101 个站）。注意这是功能 + 美观的**合并**指标 | ✅ **级联结构最值得抄** —— 先用零成本规则闸挡掉坏样本，再花 VLM 调用。γ/λ 在 {0, 0.1, 0.5, 1.0}² 上扫过，**结构奖励过重会伤视觉保真** |
| **UI2Code^N comparator**（arXiv 2511.08195，2025-11） | 三种 reward 对照：CLIP 相似度 / VLM judge / **comparator + round-robin**（同一次调用里给候选与上轮参考打分以共享刻度，两两比，reward = 胜场数，平局 0.5，渲染失败 −1） | — | 不报人类相关性 | ✅ **关键负面证据 + 关键正面证据各一个**。<br>负面：**CLIP 相似度当 reward 把 Design2Code 从 SFT 的 72.3 打到 62.0**、Flame 85.0 → 72.2；换 VLM judge 升到 74.6 / 89.0。<br>正面：**相对排序 > 绝对分** —— SFT 82.5 → vanilla verifier 83.0 → comparator 85.5 → **+round-robin 86.0**。代价是 O(N²) 次 verifier 调用 |
| **Visual-ERM**（arXiv 2603.13224） | 8B 生成式 RM，输出带 severity 的差异清单；`r = clip(1−S̃) + 渲染成功奖励` | — | VC-RewardBench 上 **F1_hard 比基座 +36.8**，而 **GPT-5.2 只有 32.7** | ✅ 又一个「8B 专用 RM 超过通用前沿模型」的例子 |
| **RULER**（arXiv 2609.25270，2026-09） | 前沿模型为每条 prompt 生成 6 项**实例级** rubric，VLM 逐项打分 | — | 与人类 **Spearman 0.7929**，对照 Aesthetic 0.6051、CLIP 0.5518 | ✅ **但必须是实例级 rubric**：通用措辞在 Icon 上掉 9.2 点（0.591 对 0.683）；更严措辞诱发「把 prompt 词画成文字」的新 hack，分从 0.693 压到 0.536 |
| **纯标量美学分**（Aesthetic predictor / HPS 类） | 单一标量 | — | Spearman 0.6051 | ❌ **明确不能。** RULER 对照组：美学分 4.309 → **6.697**，而 rubric 分 0.395 → **0.262（低于零样本基线）**、输出 token 0.3k → **6.3k（21 倍）**，手法是「堆叠重叠描边与重复装饰」 |

**本表的两条规律**：

1. **专门训的小模型当审美 judge，一致率高于通用前沿模型。** UIClip 75.12% 对 GPT-4V 51.58%；Visual-ERM F1_hard 对 GPT-5.2 差 36.8；UI2Code^N comparator 人类一致 94% 对 GPT-5 85%。
   → [推断] **审美 RM 不需要等大模型，是今天就能做的一块。**
2. **相对排序一律优于绝对分。** UI2Code^N 的 82.5 → 83.0 → 85.5 → 86.0 阶梯是同一基座下最干净的对照。

**文本侧还有两个「原创性可评」的现成形态**：

| 工作 | 做法 | 数字 | 对 UI 的含义 |
|---|---|---|---|
| **TTCW**（arXiv 2309.14556） | **14 条二元测试**，分 Fluency / Flexibility / **Originality** / Elaboration | LLM 故事通过的条目数比专业作家**少 3~10 倍** | **把原创性拆成可打勾条目，是最接近需求的形态。** 但它同时给了致命负面结论：**没有一个 LLM 与专家评分正相关 → LLM 当原创性 judge 失效** |
| **Creativity Index**（arXiv 2410.04265） | DJ-Search：把文本尽可能归因到网页语料已有片段，**覆盖不掉的才算创造** | 专业人类作者比 LLM 高 **66.2%**；**对齐把 LLM 的 Creativity Index 压低 30.1%** | 口径可迁移（换成结构指纹对 AI 套路库的最近邻距离，见 §4.7），但 UI 侧缺参考语料 |

### 2.2 人类评测集与竞技场

| 工作 | 判据 | 规模 | 可靠性 | 能当 reward？ |
|---|---|---|---|---|
| **AUV-Bench**（arXiv 2609.34854，2026-09-28） | 8 个维度各 1~5 分，标注前用 40 张视觉 rubric 样例校准 | **1,395** 条可执行 Web UI；51 名设计师招募 / **44 名**留存（剔掉 7 名全给极端分的），每条 **3 人**标，质控前 33,480 条评分 | **单人 ordinal α 宏平均 0.368**（Color 0.328 最低、Layout 0.431 最高）；**3 人 ICC(1,3) = 0.637** | **不能当在线 reward**，但是最好的校准真值来源之一。另一条关键读数：校准后**绝对审美分只有 2.78~3.18 / 5**，而 pairwise 胜率可接近 80% → **相对强不等于绝对好**。⚠️ repo `yuu250/AUV_Bench` **是空的**（只有 .gitignore / LICENSE / README），摘要称「code and dataset are available」与 reproducibility statement「upon acceptance」自相矛盾 |
| **WebDevJudge**（arXiv 2510.18560） | 654 条（269 a / 276 b / 109 tie），人类在**完整部署的网页实例**上重标 | 过滤后 1,713 → 抽 700 送标 → 最终 654 | 人类 pairwise **84.56%**；最好的 LLM judge（GPT-4.1 pairwise）**70.34%**；无 rubric 两人一致 65.0%（n=100）→ 有人工 rubric tree **92.0%**（n=50） | judge 侧能，但只能 pairwise。输入消融：**只给截图掉 9.79~10.7 点，只给代码只掉 0.31~2.60 点** |
| **Code Arena·WebDev**（原 WebDev Arena） | 用户实操两个 app 后投票 → Bradley-Terry（现行实现是开源的 `arena-rank`，Apache-2.0，闭式置信区间） | 官方 HF `leaderboard-dataset`（config `webdev`，2026-10-13）：**142 模型 / vote_count 合计 1,283,033 ≈ 641,517 场** | 见 §5.2 / §5.2b | ✅ **唯一可当 reward 源的竞技场** —— 有真逐票数据（prompt + 双答案 + 四档 label），官方 BT 实现 + 闭式置信区间 + style control 可剥离风格混淆。硬约束见 §5.2 |
| **Design Arena**（designarena.ai） | 4 模型 + 1 备份，一个 tournament 跑 **5 场** 2-way 盲选（含胜者组 / 败者组 / Tie Breaker），排 1~4 名；BT，`Rating = 400·log₁₀(strength)`，起点 1200 | website 类目 **191 模型 / 2,201,736 battles ≈ 110 万票**；全站下界约 623 万票 | **结构上没有平局**：公开 API 每行恒满足 `wins + losses == battles`（191/191 全成立）；`btStdErr` 字段**全为 null** | ❌ **不能当训练信号**：只有模型级聚合无逐票数据；强制二选一、**没有 tie 也没有「两个都差」**，把「两个都烂」硬编码成一个赢家；无置信区间；同一 tournament 的 5 票高度相关。✅ 只能当外部校准（AesCoder 用它做 Spearman 0.98 的 sanity check） |
| **UI-Bench**（arXiv 2508.20410，2025-08） | 专家**单一强制二选一**："Which project would you be more likely to deliver to a client?" **无正式 rubric、无分维度**。TrueSkill，每工具对每 prompt 单独起 μ=25 / σ=8.33，设定 **no drift, no draws** | 10 个匿名 text-to-app 工具 × 30 prompts = **300 站**，**4,000+** 专家判断（论文 4,075、线上榜 4,047、又引 8,150，三处不一致），**194 位**专家（仅 10.8% 此前用过 AI 建站工具） | 线上实测 **σ 全部 1.68~1.77，置信区间宽度 6.6~6.9 分，全员一致**。#1 Orchids 30.08 [26.61, 33.55] 对 #10 Replit 20.95 [17.56, 24.34] → **只有 #1 与 #9/#10 真正分离，#2~#8 的区间几乎全部重叠，统计上不可区分**。**本研究的专家间一致度完全未报告** | ❌ 不可用：无投票数据、**生成的站点至今未发布**（HF `AfterQuery/ui-bench` 只有 2 个 CSV，2025-08-25 后未动，且两 CSV 列不一致导致 datasets-server 报 500）、强制无平局 |
| **TASTE**（arXiv 2605.20731，2026-05） | 2 × 5 名专业设计师，**9 个维度**偏好（排版 / 空间 / 色彩和谐 / 调性等） | — | — | 偏好数据源。**不含 originality / creativity / novelty / diversity** |
| **The Human Creativity Benchmark**（arXiv 2606.30561，2026-06） | **把评审分歧当信号** | **15,000** 条专业判断、5 个创意领域、3 个工作流阶段 | 收敛集中在**技术正确性与视觉层级**，分歧集中在**审美方向与概念冒险** | 不直接可用，但这条结论是 §1 分类的独立支持：**该程序化的恰好是人也最容易一致的那一半** |

### 2.3 把设计规则写成可执行检查的工作

这一格是本文最想找的。结论：**工业界有工具且判据明确，学术界几乎没有量化；而唯一做了量化的那篇给出了一个很坏的消息。**

**① 已有的确定性 lint（判据可直接抄）**

| 工具 | 判据（精确） | 开源 |
|---|---|---|
| **axe-core / Lighthouse a11y** | WCAG 规则引擎，返回 passes / violations / incomplete / inapplicable 四个数组 | ✅ 已有 RL 先例：A11yn（arXiv 2510.13914）拿它当 GRPO 奖励，Qwen2.5-Coder-7B 的 IR_Axe 做到 **0.05**，超过 GPT-5.1 的 0.13 |
| ⭐ **`@double-great/stylelint-a11y` → `line-height-is-vertical-rhythmed`** | **这是「排版纵向节奏」唯一的真 lint 实现**：只检查 px 与无单位值；px 必须是 `baselineGrid`（**默认 24**）的整数倍；无单位必须 ≥ `minRelativeLineHeight`（**默认 1.5**）。忽略 % / em / rem / 关键字 / `font` 简写。违规例 `12px` / `1.3`，合规例 `24px` / `48px` / `1.6` | ✅ 虽打包在 a11y 插件里，规则本体是纯排版节奏 |
| **stylelint-plugin-mozilla → `use-design-tokens`** | 逐属性（color / background-color / size / border-radius / font-weight）：字面量（`#191919` / `rgba()` / `oklch()` / 命名色）即违规；放行 `var(--token)`、带 fallback 的 `var(--token, …)`、`color-mix()` / `light-dark()` 包裹 base token、CSS 关键字、`white` / `black`、系统色。border-radius 只放行 `0` / `initial` / `unset` / `inherit` | Firefox 源码树（无独立 npm 包） |
| **`@evilmartians/design-lint`** | 11 条 Oxlint / ESLint 规则（Tailwind v4）：`no-raw-color`、`no-spectral-color`（`bg-red-500`）、**`no-undefined-token`（形似 token 但不产生任何 CSS → 拼错或未定义）**、`no-arbitrary-typography`（`text-[13px]`）、`no-arbitrary-radius`、`token-constraints`（角色错位如 `bg-muted-foreground`）、`no-opacity-modifier` | ✅ 2026-09-16 首发，2026-10-13 更新 |
| **`@kong/stylelint-plugin-design-tokens`** | 比「有没有用 token」深一层：查 **token 语义角色 × CSS 属性的匹配性** —— `$kui-color-text-primary` 用在 `color` 合法、用在 `background-color` 报错（带 autofix） | ✅（硬编码 Kong 命名空间） |
| **`stylelint-declaration-strict-value`** | 最通用那条：指定属性必须用变量 / 函数 / 关键字而非字面量 | ✅ 维护中 |
| **`@takazudo/zudo-design-token-lint`** | 扫 Tailwind 类名，`p-{n}` / `m-{n}` / `gap-{n}` / `bg-{color}-{shade}` 即违规，语义 token（`p-hgap-sm` / `bg-surface`）合规。`--json` + exit code | ✅ |

**② 三条本文自己实现的判据，确认没有现成实现**（所以 §6 的那套是首次实现）

| 判据 | 检索结论 |
|---|---|
| **modular scale（字号比例级数）** | **未找到任何指标或 linter。** 只有 `no-arbitrary-typography` 判「是不是任意值」，**不判比例关系** |
| **视觉层级单调性**（字号 / 字重随层级单调） | **未找到专门检查**（a11y 的 heading-order 不算）。只有 arXiv 2607.20690 把 "poor visual hierarchy" 列为 19 条原则之一 |
| **间距节奏（某基数的倍数）** | 工业有、学术无。**没有成熟通用的 stylelint 插件做「所有 px 必须是 N 的倍数」**。本文 §6 的做法（自动选基数再看占比）未见先例 |

**③ 唯一做了量化的两篇，各给了一个坏消息**

| 工作 | 数字 | 坏消息 |
|---|---|---|
| **DesignRepair**（arXiv 2411.01606，2024-11） | 双流知识库：KB-Comp = Material Design 3 的 24 种组件、**228 条硬约束（113 do + 115 don't）+ 399 条软约束**；KB-System = 7 个属性组。检测（127 条 Vercel 硬约束 + 48 条 GitHub）：DesignRepair 召回 **92.1% / 83.3%**；而**纯规则基线 UIS-Hunter 只有召回 32.3% / 22.9%** | **纯确定性 lint 的召回只有 22~32%** —— 这量化了「程序化判据能覆盖多少」的上限 |
| **Duan et al. CHI 2024**（arXiv 2403.13139） | Figma 插件把图层树压成 JSON + 准则文本 → GPT-4 返回违规。12 UI / 12 专家。**GPT-4 P=0.603 / R=0.380 / F1=0.466**；**人类评审员均值 P=0.829 / R=0.336 / F1=0.478**。合并真值 100 个违规：仅 GPT-4 发现 9、共同 29、**仅人类 62**。评分一致性 **Fleiss κ = 0.112（准确性）/ 0.100（有用性）** | **两个坏消息。** ① κ ≈ 0.1 的标签噪声地板；② 作者自己的发现 —— **"general decrease in performance as the UI improves"，UI 越好工具越差**，首轮 52% accurate 到后续迭代掉到 39%。→ **这意味着这类 reward 在接近最优时会反向，正是 RL 最怕的形态** |

**④ 一条正面的、和本文 §6 同路的工作**

**arXiv 2607.20690**（2026-07-22）：统一 **19 条界面质量原则**（WCAG 2.2 + 欺骗性设计分类法 + 感知 / 认知理论，含 poor visual hierarchy）；
**往干净的 LLM 生成 Tailwind 页面里注入已知违规**，合成约 **10,000 页**，训一个 4B VLM；
**micro-F1 从 36% 提到 84%，19 条中 13 条 F1 > 80%**。**作者本人就把它定位为 design-aware code generation 的 reward signal。**

→ 这与本文 §6 的构造方式（往参考页注入只破坏审美的变异）是同一思路，而且验证到了 10,000 页的规模。
⚠️ 但 84% 是在**合成注入**的违规上测的，分布外迁移未验证 —— 真实场景的噪声地板可能接近 Duan 的 κ ≈ 0.1。

**⑤ Figma 侧：三个常被当成「规则引擎」的东西，其实都不是**

| 工具 | 实际做什么 |
|---|---|
| **Design Lint** 插件 | 错误类型**总共只有 10 种**（Missing fill / stroke / text / effects style、Multiple fills on a stroke、Incorrect border radius + 四角各一条）。**核心判据是「该图层有没有绑定 style（= 有没有用 token）」，不看具体值对不对**。README 原话："Out of the box, Design Lint only checks for layers that are not using styles" |
| **Similayer** | 按属性批量**选择**相似图层，**不 flag 任何东西**。当它是 linter 是误解 |
| **Figma Code Connect** | 把代码仓库组件映射到 Figma 组件，让 Dev Mode 显示生产代码。**官方文档未提及任何 validate / lint**。当它是规则引擎是误解 |

**⑥ 其他可复用零件**

| 工作 | 可抄的部分 |
|---|---|
| **WebRenderBench**（arXiv 2510.04097） | **全从最终渲染页算，不看代码不用 LLM**。RDA 关联元素相对布局差（3×3 象限 + 位置差，按唯一性加权；配对用 inner-text LCS > 0.80）、GDA 同轴分组计数差、**SDA 匹配元素对的 computed style 差（前景色 / 背景色 / 字号 / border-radius）**。`R = 0.6·RDA + 0.2·GDA + 0.2·SDA`。它的 SDA 四项与本文 §6 判据高度重叠。开源模型 ALISA-Qwen2.5-VL-7B（RL）在它上面**超过闭源** |
| **AUV-Bench 的 13 条可执行规则** | 字号 / 字重层级、字体族数、文本尺度数、垂直对齐、Gutenberg 信息区、Fitts 边缘区、**同级间距一致性**、容器行间距、**容器圆角一致性**、同级强调色、语义色稳定性。**这是目前最接近本文 §6 的成体系落地**，但 repo 空，得自己重写 |
| **`@projectwallace/css-analyzer`**（`wallace-cli --json`） | 输出 colors / gradients / font-families / font-sizes / line-heights / shadows / border-radii / animations / units，**多数类别给 total / unique / uniqueness ratio**，README 明说是给设计系统审计用的。⚠️ **只吃 CSS 字符串** → 对 Tailwind 类的 LLM 生成页基本失效，必须改走 computed style |

### 2.4 计算美学的经典指标：别用，而且理由很硬

这一节是本文花力气最多也最该写清的一格，因为这些指标看起来最像「现成的程序化审美判据」。

**① Reinecke et al. CHI 2013 —— 数字最全，但只有两个代理模型可用**

450 个网站，每张曝光 **500 毫秒**；评分者鲜艳度 184 人、复杂度 122 人、吸引力 242 人。

| 模型 / 指标 | 与人类 |
|---|---|
| 感知**鲜艳度**模型（后向剔除多元线性回归） | **r = .88，R² = .78** |
| 感知**复杂度**模型 | **r = .80，R² = .65** |
| **视觉吸引力**（线性混合效应，含人口学与被试随机效应） | **adj R² = .48** |
| Colorfulness [Hasler & Süsstrunk] 单指标 | r = .71 |
| Colorfulness [Yendrikhovskij] 单指标 | r = .53 |
| **Zheng 式 quadtree 叶数 对 感知复杂度** | **r = .28**（N=367）—— 很弱 |
| space-based 叶数 对 感知复杂度 | r = .50 |
| symmetry / balance / equilibrium 对 复杂度 | 「弱但显著」，**最终被剔除出模型** |

→ 复杂度与鲜艳度这两个**感知代理模型**可以当辅助项（它们建模的是客观可测的感知量）。
**吸引力模型不行**：adj R²=.48 里含人口学固定效应与被试随机效应，剥掉后的纯图像部分论文未单独报；连 Webby 获奖站也只有 4.21~6.57 / 9 分、**SD = 1.69**。

**② Miniukovich & De Angeli 的 8 个指标 —— 上限约 49%，且全部单调可刷**

先纠正一个常见引用错误：视觉复杂度那篇是 **AVI 2014，不是 CHI 2014**；CHI 2015 是另一篇（*Computation of Interface Aesthetics*）。

| 研究 | 规模 | 解释的美学方差 |
|---|---|---|
| CHI 2015 研究 1（桌面网页） | **N = 62 网页** | **至多 49%** |
| CHI 2015 研究 2（iPhone apps） | **N = 53 apps** | **至多 32%**（且需把 app genre 当协变量） |
| NordiCHI 2014（移动端 6 指标） | — | 主观复杂度 40%、美学 36% |

8 个指标：visual clutter、color range、dominant colors 数、figure-ground contrast、contour congestion、symmetry、**grid quality**、**white space**。

→ R² ≈ 0.49 对应 r ≈ 0.70 听起来不差，但那是**在 62 张网页上拟合出来的样本内权重**。
**更致命的是 8 项全部单调可刷**：白空间越多、边缘越少、颜色越少、对齐线越少，分越高
→ **RL 会直接收敛到空白单列页。** 必须配信息量 / 内容完整性的反向闸。

**③ Ngo 等人的 13/14 项布局美学度量 —— 明确不能用**

| 问题 | 证据 |
|---|---|
| **原始验证从来没有报过任何相关系数** | 三个实验（6 名设计师 / 7 屏；**180 名本科生** / 7 屏；79 人再 180 人 / 5 屏）全部只说「高 / 中 / 低三档排序吻合」，**从未报告过 r 或 R²**。且 13 项里**只有聚合量 OM 被验证过，单项从未单独对过人类评分** |
| **非单调 —— 优化它会反向** | Salimun 2013 博士论文第 5 章（**72 人**，纯偏好无任务）：**Ngo 分最高的布局是最不受偏好的**（286 票），最受偏好的是 medium symmetry（499 / 798） |
| **人类自身一致度极低** | 同上：**评分者间 Kendall W = 0.1023**（亚洲 0.1859 / 西方 0.0843） |
| **13 项高度冗余** | 6 项聚合 OM 与 13 项聚合 OM 近乎线性，**R² = 0.9144** |
| **换成真实网页后基本失效** | Purchase et al. AUIC 2011 把 14 项实现成工具、输入**完整网页**：**只有一项**捕捉到了美学吸引力，且捕捉不到感知可用性；真正的强预测因子是「**图片的摆放位置**」。即 **14 项里 13 项基本没用** |

→ 唯一用法：当 **veto**（density 远离 50%、regularity 极低时打回），**绝不当排序器**。

**④ AIM（Aalto Interface Metrics）—— 打包了经典指标，但自己不背书**

21 个指标 / 36 个结果字段，分四类（Colour Perception 10 / Perceptual Fluency 7 / Visual Guidance 2 / Accessibility 1）。
**AIM 自己不报任何与人类的一致率，也不输出单一总分。** 源码注释里多项自我否定：
`cp4` "no direct empirical evidence"、`cp6` "tested mainly on photos"、`pf7` "heuristic, not based on a visual-system theory"、`pf4` 标记为 TODO。
**UIClip 论文明确拒绝把 AIM 当基线**，理由是「没有确定的方式把 AIM 的各项指标折成设计评分」。

**特别点名一条不能用的**：`cp11` 色彩和谐 —— 把 RGB 转 HSV 丢掉 V，对每个色轮旋转角算到 Matsuda / Itten **8 个模板**边界的频次加权距离。
源码自带两条警告：① 形式化来自**照片增强**，"This is not proven for user interfaces"；
② **模板 X 几乎总是最小距离**（X 覆盖色轮大部分）→ 直接拿最小距离当和谐度是系统性偏差，
**RL 会学会「把颜色铺满色轮」**。

**⑤ 现代网页上复现过吗**

| 工作 | 结论 |
|---|---|
| **Miniukovich & Marchese CHI 2020** | **唯一真正重验「经典关系在现代网页上还成立吗」**：重采集 5 个历史数据集（含 Reinecke 450 站）。结论是**反向线性关系为主 + 较弱 U 形分量**；而可视化检查发现 U 形来自混淆因子（页面「看起来坏掉 / 陈旧」），**控制后 U 形基本消失**。但它重验的是「复杂度—美学」这条关系，**不是重验 8 项 / 13 项各自的 r** |
| **Webthetics**（IJHCS 2018） | CNN 直接回归网页截图的平均美学评分。广为引用的 **Pearson r ≈ 0.85** 是二手转述 |
| **TOCHI 2022**（DOI 10.1145/3569889） | 预测**评分分布**而非均值，交叉验证 **LCC = 0.752**。**并指出 Webthetics 的 0.85 不代表真实水平，其原代码有 bug —— 其中一个是训练集 / 验证集重叠（泄漏）** |

→ 净结论：**手工指标到深度模型的跃迁是真的（r 从约 .59 到 .75 量级），但 0.85 含泄漏，可信值是 LCC ≈ 0.75。**
**Ngo 那一支在 2018 年之后没有任何正面重验，只有 2011 / 2013 的负面结果。**

### 2.5 这一节的三条结论

1. **真正可当 reward 的只有四类**：确定性规则引擎（axe-core 已有 RL 先例、`line-height-is-vertical-rhythmed`）、渲染后几何与 computed style 读数（WebRenderBench、本文 §6）、专门训的小 comparator / 生成式 RM（UIClip 75.12%、UI2Code^N 94%、Visual-ERM）、级联式 agentic reward（WebGen-R1 r=0.762、AesCoder）。
   **纯标量美学分与 UICrit 的数值评分明确不能。**
2. **所有现成的审美评测集都没有 originality / templateness 维度** —— UIClip、UI-Bench 的七维 codebook、TASTE 的九维、Graphic-Design-Bench、AUV-Bench 的八维，逐个核过，一个都没有。
3. **经典计算美学指标全部单调可刷，方向一致**（白空间越多、边缘越少、颜色越少分越高）→ **RL 必然收敛到空白单列页**，必须配双边区间或内容完整性反向闸。
   加上 Duan 的 "UI 越好工具越差"，这类 reward 在**接近最优时会反向**。

### 2.6 可以直接站上去的现成实现

| 肩膀 | 给了什么 | 怎么用 |
|---|---|---|
| **UIClip**（HF `biglab`） | 3 个 checkpoint + 3 个数据集（含人评数据），151M，pairwise 口径 | **当 pairwise reward 底座，再在目标分布上微调**。注意至今无人把它用于 RL，我们会是第一个 |
| **WebGen-R1**（arXiv 2604.20398） | 级联 reward 结构 + `r = 0.762` 的人类相关性 | 抄级联：零成本规则闸先挡 → 只对通过者调 VLM |
| **UI2Code^N**（repo `zai-org/UI2Code_N`） | comparator + round-robin 的实现与阶梯数字 | 用相对排序替代绝对分 |
| **arXiv 2607.20690** | 「往干净页注入已知违规、合成 10,000 页、训 4B VLM」的完整路线，micro-F1 36% → 84% | 本文 §6 的变异集扩题可以直接照这个方式自动化 |
| **WiserUI-Bench**（repo `jeochris/wiserui-bench`） | 300 对**真实 A/B 转化率**真值 + 684 条专家 rationale | **外部校准集首选** —— 标签不依赖任何人的口味 |
| **Design Theater**（repo `kashifimteyaza/design-theater-main`，MIT） | DHI 三子量 pipeline + **120 个对照界面** | 补一个人类设计基线就是新贡献（§4.2） |
| **`avoid-ai-design` 的 67 条 tells** | 离散特征字典 | 算熵 / HHI（§4.1 的「学界零篇」）。注意 **Tailwind v4 把 `bg-gradient-to-r` 改名 `bg-linear-to-r`，要双拼写匹配** |
| **Design2Code 附录表 4** | 结构坍塌 baseline | 合成页 Avg Tag **19±8** / DOM 深度 **5±1** / Unique Tags **10±3**；真实页 **158±100** / **13±5** / **22±6** |

### 2.7 本节没查到的

- design token 合规的**学术论文**（只有工业工具）；Supernova / Specify / Tokens Studio / zeroheight 的 token 合规报告
- 量化 Figma lint 插件 precision / recall 的论文
- ΔE / CIEDE2000 当 UI 设计判据的工作（a11y 对比度不算）
- Zheng et al. CHI 2009 的精确 r（ACM DL 403，摘要零数字；外部只有 Reinecke 重测的 r = .28）
- Miniukovich 的逐指标 R²（ACM DL 与机构库全部 403）
- Ngo 原文 14 条公式的人类相关性（**因为原文从未报过**）

## 3. Anthropic 四维评审器的可复制性

四维原文定义在 `16_primary_sources.md` §1.3（全文照抄，不在此重复）。本节只回答三个问题。

### 3.1 哪几维可以程序化

| 维度 | 原文关键词 | 可程序化比例 | 理由 |
|---|---|---|---|
| **Craft** | "typography hierarchy, spacing consistency, color harmony, contrast ratios" | **约 4/4 的分项都能测** | 原文列的四个分项恰好一一对应本文 §6 的 `hier`、`spacing`、`hue`、`contrast` 四条判据，而且都是 [实测] 能零噪声判的 |
| **Functionality** | "Can users understand what the interface does, find primary actions, and complete tasks without guessing?" | **约 1/2** | 「主操作可见、可键盘到达、点得到、交互后状态按契约变」可程序化（本项目 W1/W3 层）；「不用猜」只能评审 |
| **Design quality** | "coherent whole rather than a collection of parts … distinct mood and identity" | **接近 0** | 「整体感」「识别度」没有可执行判据。能测的只是它的必要条件（配色/字号/间距自洽），测过了不代表有整体感 |
| **Originality** | "custom decisions vs template layouts, library defaults … purple gradients over white cards" | **只能测具名 tell** | 原文自己给的例子（紫渐变 + 白卡）是可测的，[实测] tell 判据抓得到；但「有没有刻意的创作决定」是分布量，见 §4 |

**所以四维的实际结构是**：
- **Craft 整维可以做成硬闸**（而官方把它降权了）
- **Functionality 一半做硬闸、一半做评审**
- **Design quality 只能做 rubric 化评审**
- **Originality 的 tell 部分做硬闸（而且应该是负向闸）、其余部分只能做批次诊断**

### 3.2 官方权重与我们该用的权重正好相反

[原文] 官方降权 Craft 和 Functionality 的理由：
> "Claude already scored well on craft and functionality by default, as the required technical competence tended to come naturally to the model."

这个理由在**推理时 harness** 里是对的：没有区分力的维度不该占权重。
但在 **RL** 里它是反的，三条理由：

| | 推理时 harness | RL |
|---|---|---|
| 没区分力的维度 | 浪费权重，该降权 | **正是最安全的硬闸**：它不提供优化压力，但能挡住塌缩 |
| 有区分力的维度 | 该加权，推模型冒险 | **最容易被 Goodhart**：RULER 实测美学分从 4.42 顶到 6.21，而 rubric 分从 0.395 崩到 0.262、输出 token 从 0.3k 爆到 6.3k（见 `draft_training.md`） |
| 「模型默认就及格」 | 观察到的事实 | **会在训练中失效**：一旦别的项提供了优化压力，模型会拿 craft 去换分 |

[推断] 对我们的处置：**把 Craft 的四个分项全部做成乘法硬闸（不计权重、只决定是否进入后续评分），把 Design quality 放在闸后做 rubric 化组内 pairwise，Originality 的 tell 做负向闸。** 这与 `04_verifier.md` §6.1 的聚合规则一致。

### 3.3 「rubric 里不要写诱导词」这条有没有被量化验证过

**没有被第三方量化验证。** 能找到的证据有三层，强度递减：

| 层 | 证据 | 强度 |
|---|---|---|
| 一手定性 | [原文] "Including phrases like 'the best designs are museum quality' pushed designs toward a particular visual convergence, suggesting that the prompting associated with the criteria directly shaped the character of the output." | 作者自述，**无数字、无对照组** |
| 同一家公司的内部矛盾 | `16_primary_sources.md` §2.3 已记录：官方 `canvas-design` skill 正文里**在用**这个措辞——"To create museum or magazine quality work"，还要求 "**Emphasize craftsmanship REPEATEDLY**" | 两份都是官方一手。说明**这类措辞在 generator prompt 里是增益、在 evaluator rubric 里是污染**，两边不能共用同一套词 |
| 邻近的量化证据 | RULER（arXiv 2609.25270 §4.3/§4.4）：换成整体美学分后，模型用密集重叠笔画和重复装饰刷分，token 从 0.3k 涨到 6.3k；换成结构化 rubric 后，模型改成把 query 词画成风格化标签 | **有数字，但测的是「rubric 形态」而不是「rubric 措辞」** |

→ 结论：**「别写诱导词」目前是一条无量化支撑的工程经验。** 本文建议把它当作可测的假设来做，而不是当定论——具体做法是 §5.4 的 A/B：同一 generator、同一 evaluator、两套只在措辞上不同的 rubric，测产出分布的集中度（§4 的指标），而不是测分数。

---

## 4. 「AI 味」能不能被测出来

### 4.1 一句话：能，但只有一篇真正做了，而且它测的是成对距离而不是分布集中度

| 问题 | 答案 |
|---|---|
| 有没有工作把「AI 味」直接操作化成指标 | **有一篇**：Design Theater 的 **DHI**（Design Homogeneity Index），arXiv 2607.22928（2026-07-24，AAAI/AIES 录用），代码与 120 个界面全开源 |
| 有没有第二个可用的 | **有半个**：LandingAgent 的 **Diversity**，arXiv 2608.27902（2026-08），好处是**有可当刻度的基线数字** |
| 配色 / 字体 / 布局模板的**分布熵或集中度** | **学界零篇。** 11 篇 web/UI 生成 benchmark 全文检索 `entropy` / `homogen*` / `template collapse` / `mode collapse`，**全部 0 命中** |
| Inter 占比、紫渐变占比的实测数字 | **一个严肃测量都没有。** 全部来源是博客轶事（有一篇声称「被禁字体占 90%」，无出处无方法，不可引用） |
| 判别「这页是不是 AI 做的」的分类器 | **不存在。** 零论文、零数据集、零基准 → **「用分类器置信度当 AI 味指标」这条路走不通** |
| rubric 措辞 → 视觉输出分布收敛的量化 | **零篇。** 所有 diversity collapse 的数字都在**文本**上 |

### 4.2 唯一直接命中的工作：DHI

Design Theater（arXiv 2607.22928）把同质化拆成三路距离，**值越低越像**：

| 子度量 | 做法 | 实测均值（24 prompt × 5 工具 = 120 个界面） |
|---|---|---|
| **DHI-Visual** | 截图（统一 1200×1200）→ UIClip 嵌入 → 成对余弦距离 | **0.137**（最像的一对：Claude–Vercel v0 **0.119**） |
| **DHI-Color** | CIELCh 颜色直方图 → Earth Mover's Distance | **31.9**（最像：Claude–Vercel v0 **20.6**） |
| **DHI-Layout** | OmniParser v2.0 检测元素 → Zhang-Shasha 树编辑距离 | **0.196**（最像：Bolt–Claude **0.181**） |

同篇的另两个指标也值得记：**TFS**（声明的设计理由里有多少真被实现）—— **超过 25% 的设计理由在界面里找不到，功能类升到 34%**；
**PAS**（UX 原则遵守率）—— 五个工具里四个**只实现 ≤6% 的功能性原则**。

**DHI 的四个硬伤（直接决定我们能不能照抄）**：

1. **没有人类设计基线。** 0.137 是大还是小，论文没给参照 → **绝对值不可解释，只能做工具间排序**
2. **只报跨工具的两两距离，不报 per-tool DHI** → **回答不了「哪个模型最 AI 味」**，而这恰好是我们要的
3. **三个子量的取值区间极窄 —— 不先量方差，任何「A 比 B 同质」的结论都不可信。**
   DHI-Visual 的全部 10 个工具对只落在 **0.119 ~ 0.151** 这个区间里（跨度 0.032），
   而论文**没有报重复测量的方差**。
   → [推断] 按 `07_capability_spec.md` §4.3 的思路，先对同一配置跑 ≥5 轮量出指标自身的噪声地板，再去比两个配置。
   这与本项目「小子集上的比率要先算方差和对照量」是同一条教训
4. **用 UIClip 当多样性 backbone 有口径污染。** UIClip（arXiv 2404.12500）是朝 design **quality** 训的表征（全文检索 `novelty` / `originality` / `homogen` 全 0 命中）→ [推断] 它会**系统性低估「都很好的页」之间的差异**。
   用 DINOv2 / v3 这类没针对质量调过的自监督 backbone 更干净（LandingAgent 的选择）

### 4.3 有刻度可比的那半个：LandingAgent 的 Diversity

做法：全页截图 → 按宽度等比缩放 → **裁顶部 518×518 方形** → 冻结 DINOv3 ViT-L/16 → **只在同一个 target 内部**算平均成对余弦距离（K=3）。
「只在同题内算」这一点正是 template collapse 想量的东西。

实测（30 targets × 12 行业 = 540 页）：

| 方法 | Diversity | Faithfulness | Aesthetics |
|---|---|---|---|
| Direct Prompting (gemini-2.5-pro) | **0.26** | 3.83 | 3.67 |
| Direct Prompting (gpt-5) | **0.28** | 4.60 | 3.63 |
| **Direct + Polisher** | **0.25** | 4.33 | **3.62** |
| LandingAgent (gemini-2.5-pro) | **0.36** | 4.30 | 4.00 |
| LandingAgent (gpt-5) | **0.37** | 4.70 | 4.10 |

消融：去掉 Polishing **0.24** / 去掉 RAG 0.29 / 完整 **0.38**。

**最该记住的副产品结论 ——「润色会压低多样性」，有两处独立量化**：
- LandingAgent 的 Polisher：Diversity 0.26 → **0.25**，而且 Aesthetics 也降（3.67 → 3.62）
- PrototypeFlow（arXiv 2412.20071，UIST 2024）加 ControlNet：Generation Diversity **SD-1.5 从 15.93 降到 11.48**、PrototypeFlow 自己 **15.95 降到 13.98**，而 FID 变好
→ **做指标时必须同时报质量和多样性，否则会把「变好」误判成「变多样」。** 这也是对「加一个 polish 轮」这类改动的直接警告。

**两个引用坑**：
- 同配置在 Table 3 是 0.36、Table 4 是 0.38，论文未解释
- 聚合式写的是 `1/(K(K−1))` 而 `i<j` 只有 3 对，K=3 时这是真均值的**一半** → **0.24~0.38 很可能是「半个平均成对距离」**，跨论文比之前要先对齐口径

### 4.4 「AI 味」的数学表述：每个都挺原创，但彼此雷同

这是本节最重要的概念澄清，来自 Wenger & Kenett（arXiv 2501.19361，2025-01）。
22 个模型（统计用 7 个，一家一个）对 **102 名 Prolific 人类**，all-MiniLM-L6-v2 嵌入，变异度 = 1 − cos：

| 测验 | LLM 变异度 | 人类变异度 | 效应量 |
|---|---|---|---|
| AUT（替代用途） | **0.459** | 0.738 | **2.2** |
| FF（Forward Flow） | **0.534** | 0.835 | **2.0** |
| DAT（发散联想） | **0.665** | 0.819 | **1.4** |

**但个体原创性 LLM 并不差**（AUT 0.711 对人类 0.696）。

→ **「AI 味」= 单条产物的质量不低，但一批产物彼此过于相似。**
这直接推出三条工程结论：

1. **它是分布量，不是单页属性** → **天然不能当 per-sample reward**。per-sample 的 reward 函数看不到「别的样本长什么样」
2. **单页上只能查具名 tell**（Inter、紫渐变、白卡）。[实测] 本文 §6 的 tell 判据在注入 Anthropic 点名的那一组时 100% 命中，20 个页面里只有 A11 命中、P04（品牌蓝渐变）不误报 —— 但这只是「像不像那几个已知默认」
3. **tell 清单必然过期**。Anthropic 原文已承认禁掉一组默认值后会收敛到新的默认值（"the model can default to other common choices (like Space Grotesk …)"）

### 4.5 两条关于机制的反直觉证据

**① RLHF 造成的坍塌主要在 per-input，而「AI 味」是 across-prompt 现象**

Kirk et al.（arXiv 2310.06452，ICLR 2024）摘要任务，K=16 样本/输入 × N=500 输入 @ temp 1：

| 指标 | per-input SFT | per-input RLHF | 降幅 | across-input SFT → RLHF |
|---|---|---|---|---|
| EAD | 0.79~0.81 | **0.07~0.16** | **−80% ~ −91%** | 0.86 → 0.69~0.87（**小得多**） |
| Sent-BERT | 0.45~0.50 | **0.06~0.15** | −67% ~ −87% | 0.73 → 0.63~0.73 |

→ [推断] **「AI 味」说的是「不同需求做出来的页都长一样」，即 across-prompt。而 RLHF 最强的效应在 per-input。**
所以不能直接拿 Kirk 的数字当「AI 味」的机制证据。要么另有成因（见 §4.6），要么视觉模态的 across-input 行为与文本不同——**这一点没人测过。**

**② 坍塌主要发生在 SFT，而且写进了权重**

Karouzos, Tan & Aletras（arXiv 2604.16027，2026-04），Olmo 3 三条平行后训练血统 × 15 任务 × 4 指标（含 Vendi）：

| 血统 | SFT | DPO | RL | 最终保留多样性 |
|---|---|---|---|---|
| Think | **−62%** | −4% | +4% | **38%** |
| Instruct | −38% | **−23%** | −5% | **34%** |
| **RL-Zero** | — | — | — | **93%** |

- Vendi 从约 **3.4 个有效模式降到约 1.8**（GSM8K 只剩 1.3）
- **只看正确输出时，IFEval 83.4% 的多样性损失仍然存在** → 不是「把错答案删掉」那么简单
- **关掉 CoT，SBERT 多样性不变** → **坍塌在权重里，推理期手段修不了**
- 代价：GSM8K majority-vote 增益 Base +24% 对 Think **仅 +0.4%**

→ [推断] 对我们的直接含义：**RL-Zero 血统保留 93% 的多样性，而 SFT 一步就砍掉 38~62%。**
如果「不要 AI 味」是目标之一，**SFT 冷启动的数据多样性比 RL 阶段的 reward 设计更关键**。

**③ 反规模律**：NoveltyBench（arXiv 2504.05228，COLM 2025）
gemma-2 **2B 的 Distinct@10 = 5.66 高于 27B 的 3.03**；Llama-3.2 **1B = 6.74 高于 405B 的 3.20**；
**闭源模型没有一个 utility > 4**（Claude-3.5 Sonnet Distinct@10 只有 **1.76**，全场最低）。
推理模型上 reasoning effort 越高，多样性和 utility 双降。

### 4.6 一条被忽略的成因：收敛是被 prompt 规定出来的

Google 的 Generative UI 论文（arXiv 2604.09577，Google Research）自己就是这条证据。

- 全文检索：`diversity` 只出现 1 次（指外包承包商的多样性），`entropy` **0 次** → **完全没有输出多样性指标**
- 但它有一整节 **§2.1 "Consistent Styling"**，目标是**主动增加跨生成的视觉一致性**（"increased visual consistency across generations"）—— **Google 把跨生成风格一致当 feature 在做**
- 公开的 system instruction（附录 A.5）逐字：
  > "Use Tailwind CSS effectively... typography (e.g., **'Open Sans' or similar**... though **default Tailwind fonts are fine**), color schemes (**including gradients**), spacing, and subtle **transitions or animations**..."
  > 硬约束：只许 `<script src="https://cdn.tailwindcss.com">`，**"No Other External Files"**

逐条对上 Anthropic 博客点名的三个症状：

| Anthropic 点名的症状 | Google system instruction 里的对应 |
|---|---|
| Inter fonts | 字体走 Tailwind 默认（即 Inter 系）；**禁止外部文件直接封死自定义字体** |
| purple gradients on white backgrounds | 显式鼓励 "color schemes (**including gradients**)" |
| minimal animations | "subtle transitions or animations" |

→ **「AI 味」至少有一部分不是预训练分布的锅，是 harness / system prompt 把输出锁在一个 token 空间里。**
[推断] 这对复刻是好消息：**这一部分可以靠改 prompt 和放开约束直接拿回来，不需要动训练。**
这也和 Anthropic 自己的观察一致——他们的解法就是一份约 400 token 的 skill，不是训练。

### 4.7 本文设计的可本机实现代理指标

因为「分布集中度」这一维学界零篇，下面是本文的设计。
**前提：没有参考集（real set）**，所以 FID / KID / precision-recall / density-coverage 全部排除，只能用 reference-free 指标。

| # | 指标 | 做法 | 为什么选它 |
|---|---|---|---|
| **1** | **视觉多样性** | 全页截图 → 按宽度缩放后裁顶部 518² → **DINOv2 ViT-B/14**（Apache-2.0）嵌入 → ① 平均成对余弦距离 ② Vendi Score(q=1，即「有效模式数」) | reference-free；**有刻度可比**（LandingAgent 0.24~0.38、DHI-Visual 均值 0.137）；算力几乎免费。**别用 CLIP**（偏语义）、**别用 UIClip**（质量表征污染）、**别用 LPIPS**（假设图像已对齐）。<br>**但必须知道它的上限**：DeepMind 的 *Benchmarking Diversity in Image Generation*（arXiv 2511.10547）实测 —— 纯图像嵌入（Inception / ViT-B/16 / DINOv2）在多样性判断上普遍优于文本条件的多模态嵌入；Vendi Score 选对表征空间时约 **65%** 对齐人类判断（模型差异大时 80%）；**但所有自动指标在区分「同等多样」的两组时 AUC 都 < 0.6** → **这类指标只能读大差异，读不了细差异** |
| **2** | ⭐ **样式集中度指纹**（本文认为最值得做的一项） | 复用 §6 的 `aesthetic.js` 已经在抽的 computed style：{颜色→OKLCH、font-family、font-size 阶梯、border-radius、box-shadow、gap/padding} → ① 全语料 top-k 取值的覆盖率 ② 页面级直方图的 pairwise Jensen-Shannon 距离或 EMD ③ **每一类属性的 Shannon 熵与 HHI** | **最可解释**：指标 1 只说「像」，这个直接指出「**因为 71% 的页用了同一个蓝 + Inter + rounded-lg**」。而且**走 computed style 绕开了「Tailwind utility class 让静态 CSS 解析失效」这个坑**。**这一维学界零篇** |
| **3** | **结构模板化** | DOM tag n-gram shingle → MinHash / Jaccard 做全量 N² 近似（毫秒级）→ 只在聚类代表之间跑 `zss` 精确树编辑距离校验 | 捕捉「换个配色但骨架不变」这类指标 1 看不出的套路。**有现成 baseline**：Design2Code 表 4 的合成页 unique tags **10±3**、DOM 深度 **5±1**，真实页 **22±6** / **13±5** → **标签种类只有真实页的 45%、DOM 深度 38%**。**注意树编辑距离是 O(n²)~O(n³)，1000 页全配对是小时到天级，必须走两段式** |
| **4** | **文本套话率** | distinct-2/3 + 固定短语与导航词表命中率（可拿开源 lint 工具 `avoid-ai-design` 的 **67 条 tells** 当特征字典：紫/靛渐变、渐变填充标题、pill badge + 居中 hero、`rounded-2xl` / `shadow-lg` / `backdrop-blur`，以及 Inter / Space Grotesk / Geist / Instrument Serif / Fraunces） | 零成本、零依赖、信号极强、最好解释 |

**两个必须配上的口径修正（否则指标 1 与指标 2 都会算错）**：

| 修正 | 为什么必须 | 怎么做 |
|---|---|---|
| **把「题面带来的多样性」与「模型自身的多样性」分开** | §4.5 已指出 per-input 与 across-prompt 是两个口径，而「AI 味」是 across-prompt 现象。如果一批页面来自不同题面，直接算 pairwise 距离会把「题面本来就不同」算成「模型很多样」 | 用**条件版 Vendi**（现成实现：`mjalali/conditional-vendi`、`aziksh-ospanov/scendi-score`），它就是为了区分这两者而做的。或者退一步，**只在同题面内算**（LandingAgent 的做法，K=3） |
| **加「有效性」闸，否则「生成一堆垃圾」会被算成多样** | arXiv 2504.12522 的 effective semantic diversity：加闸前 Base 对 RL 的 neural diversity 是 **d = −2.12**，只在合格输出里算之后**翻成 d = +1.54**。同一批数据，口径决定结论方向 | 多样性只在**通过了 §6 审美硬闸**的子集上算；同时必须与质量指标联报 |

**算力估计**（1000 个页面，[推断]）：渲染 3~8 分钟（瓶颈）、PNG 解码 resize 1~2 分钟、DINOv2 嵌入 GPU < 5 秒 / 32 核 CPU 1~2 分钟、pairwise 与 Vendi 秒级、computed style 抽取与截图同次访问边际成本近 0。
**端到端约 10 分钟（有 GPU）/ 15 分钟（纯 CPU）。**

**渲染三个必踩的坑**（[推断]，但机制确定）：

| 坑 | 后果 | 对策 |
|---|---|---|
| 外链 CDN（`cdn.tailwindcss.com`、Google Fonts） | 离线机器上请求超时，页面裸奔 → **测到的是「有没有联网」而不是「设计像不像」** | 本地镜像一份，用 `page.route` 重写到 `file://`。**全部 abort 是错的**——所有 Tailwind 页会退化成同一个无样式形态，把多样性指标打到地板 |
| 容器里没有 CJK / emoji 字体 | 中文变方框，所有页的文字区块长得一样 | 先装 `fonts-noto-cjk` `fonts-noto-color-emoji` |
| `full_page=True` 高度差 10 倍 | 嵌入距离被「页面多长」主导 | 照 LandingAgent：按宽度缩放到 518 后裁顶部 518² 方形；或照 Design Theater 统一 1200×1200 |

### 4.8 本机实测：样式集中度指纹跑出来的第一组数字

§4.1 说「配色 / 字体 / 布局模板的分布熵或集中度，学界零篇」。本文把它实现出来跑了。

- 代码：`scripts/vc_verifier/web/aes_concentration.js`（复用 §6 的 `aesthetic.js` 抽 computed style）
- 复跑：`node aes_concentration.js <含 html 的目录> out/xxx.json`
- 口径：对一批页面，按**人能看见的属性**（字体族、字号、色相分箱、圆角、间距）分别算
  语料级 Shannon 熵 H、归一化熵 H/log2(k)、**HHI（赫芬达尔指数，1 = 完全集中）**、top1 取值与其文档频率，以及页面级直方图的平均 Jensen-Shannon 距离
- 只统计可见属性，防止 `z-index` / `letter-spacing` 这类不可感知维度刷熵（§4.9 的 hack 形态之一）

两个样本（都是本项目里模型生成的 demo 页，11 + 12 页）：

| 属性 | gallery/demos（11 页，three.js 演示，用 Google Fonts） | basic/demos（12 页，较简单的演示，用系统字体栈） |
|---|---|---|
| **fontFamily** | k=2，H=1.0，**HHI 0.50**，top1 = **inter，11/11 页都在用** | k=1，H=0，**HHI 1.00**，top1 = `-apple-system`，12/12 页 |
| fontSize | k=9，Hn=0.964，HHI 0.122 | k=8，Hn=0.778，HHI 0.283 |
| **hue**（15 度分箱） | k=1，H=0，**HHI 1.00**，全部 neutral 主导 | k=3，Hn=0.691，HHI 0.561，neutral 10/12 |
| radius | k=6，Hn=0.932，HHI 0.193 | k=5，Hn=0.969，HHI 0.219 |
| spacing | k=15，Hn=1.00，HHI 0.067 | k=12，Hn=0.939，HHI 0.114 |
| **具名 tell** | **Inter 占比 100%**、AI 字体占比 **100%**、紫渐变 **0%**、任意渐变 45.5% | **Inter 占比 0%**、AI 字体占比 **0%**、紫渐变 0%、任意渐变 25% |

**这组数字里最有价值的一条，是两个样本给出了相反的 tell 结论、相同的集中度结论：**

- gallery 集：**Inter 占比 100%** → 任何「禁 Inter」的 lint 都会全判挂
- basic 集：**Inter 占比 0%**，所有具名 tell 全部为 0 → 在 lint 下**满分通过**
- 但 basic 集的 **fontFamily HHI = 1.00，比 gallery 的 0.50 更集中** —— 它只是集中到了另一个取值（系统字体栈）上

→ **[实测] 具名 tell 和分布集中度测的是两件不同的事，而且集中度更鲁棒。**
一个「避开所有已知 AI 字体」的产物集，可以在字体维度上比「全用 Inter」的集合**更坍塌**。
这就是 §4.4 第 3 条（tell 清单必然过期）的直接实验证据，也是对开源 lint 工具那条路线的直接否证：
**规则表只能查你已经知道的默认值，查不到「收敛」这件事本身。**

**另外三条读数**：
1. **字体是两个样本里最坍塌的维度**（HHI 0.50 / 1.00），色相次之（1.00 / 0.561），间距最分散（0.067 / 0.114）。
   [推断] 这与 Anthropic 点名的症状顺序一致——字体和配色先收敛，间距最后
2. **紫渐变在两个样本里都是 0%。** 那个被博客反复引用的症状，在本项目的产物里一次都没出现 →
   **[推断] 紫渐变可能是特定时期、特定模型、特定 prompt（Tailwind 系）的产物，不是普适的 AI 味标志**
3. `top1Share` 这一列对低基数的分类属性（fontFamily、hue）才有意义。
   对 spacing / radius 这类连续量，「最常见取值的文档频率」接近 1 是平凡的（1px、8px 到处都有）→ **不要跨属性比较这一列**

**四条必须披露的局限**：
- **N=11 与 12，单一项目、单一题族（都是本博客的演示页），而且经过人工挑选** → 不是模型输出的随机样本，**不能当「模型的 AI 味有多重」的估计**
- Google Fonts 走 CDN，离线环境下字体**实际没加载**。但测的是 computed style 里声明的字体栈，
  即「模型选了什么字体」，这正是想测的东西 → 结论不受影响，但渲染出来的画面不是设计者看到的那个
- gallery 集是全屏 canvas 的 three.js 演示（`overflow:hidden`），排版与间距样本本来就稀疏
- 缺**人类设计基线**。这正是 Design Theater 的 DHI 的同一个硬伤（§4.2 第 1 条）：
  HHI 0.50 是高还是低，没有参照。要补这个必须去采一批人类设计的真实站点做对照组

### 4.9 这套代理指标会怎么被 hack

[推断]，这是本节必须写的部分，因为分布指标的 hack 形态和 per-sample 指标完全不同：

| hack | 怎么做 | 为什么有效 | 对策 |
|---|---|---|---|
| **注入无关噪声换多样性** | 在每个页面随机塞不同的装饰色、随机字号抖动 | 嵌入距离和熵都会涨，而设计质量不变甚至更差 | **多样性指标必须与质量指标联报**（LandingAgent 的 Polisher 例子就是反向版本）；并且必须在「通过了 §6 的审美硬闸」的子集上算 |
| **换皮不换骨** | 只改配色，DOM 骨架和布局完全不动 | 指标 1（视觉嵌入）会涨，指标 3（结构）不涨 | **必须三路联报**，不能只用视觉嵌入这一路 |
| **躲 tell 清单** | 换成 Space Grotesk + 青绿渐变 | 具名 tell 会失效 | tell 清单**周期重算**，并且只当批次诊断不当闸 |
| **熵刷在无感知维度上** | 把 `z-index`、`letter-spacing` 这类看不见的属性随机化 | 样式集中度熵会涨，视觉上毫无变化 | 熵只算**人能看见的属性**（颜色、字号、字体、圆角、间距），并且和指标 1 的视觉嵌入交叉核对 |
| **采样温度刷分** | 直接调高 temperature | 所有多样性指标都会涨，质量下降 | 固定解码参数，或把 temperature 作为固定实验变量而不是可优化项 |

→ **结论：分布级「AI 味」指标只能当批次级诊断与验收，绝不能进 reward。**
一旦进 reward，上面五种 hack 里至少三种是零成本的。

**还有两条必须一起记的方法论限制**：

1. **自动多样性指标的分辨率很低。** DeepMind 的 *Benchmarking Diversity in Image Generation*（arXiv 2511.10547）实测：
   Vendi Score 选对表征空间时约 65% 对齐人类判断（模型差异大时 80%），
   但**所有自动指标在区分「同等多样」的两组时 AUC 都 < 0.6**。
   → 这类指标只能读「明显更同质 / 明显更多样」，读不了 10% 量级的差异
2. **「多样性必须牺牲质量」可能部分是口径造的假象。** arXiv 2509.21267（Meta FAIR + MIT）实测：
   用通用指标看 tradeoff 很大，**换成任务相关的多样性口径后 tradeoff 几乎消失**；
   指标与人类判断的 Spearman r：**taxonomy 引导的 LLM judge 0.90~0.94** > 嵌入 0.78 > 词汇 0.63 > gzip 0.28。
   → 报 tradeoff 之前先确认不是自己的指标口径造出来的

---

## 5. 噪声地板与可行的评测协议

### 5.0 先说天花板：单一全局审美 reward 的上限约 60%

这是本文找到的最硬的一个约束，比 α=0.368 更直接。

**DesignPref**（arXiv 2511.20513，2025-11）：400 个生成设计 × 100 屏描述 → 600 对，
**20 位职业设计师每人把 600 对全评一遍** = 12,000 条判断，四档无中立（A≫B / A>B / B>A / B≫A）。

| 口径 | 数值 |
|---|---|
| 二元（合并强弱档）平均成对一致 | **0.624** |
| 二元 Cohen κ = Krippendorff α | **0.248** |
| 四档一致 | 0.386 |
| 四档 α | **0.104** |
| **两两分歧率 ≥ 96% 的对子占比** | **28.5%** |

模型侧（在这同一批数据上训 / 评）：

| 方法 | 二元准确率 |
|---|---|
| pooled UIClip（用 20 倍数据 pool 训练） | **57.45%**（SRCC 0.196） |
| pooled GPT-5 + RAG | 57.62% |
| **personalized UIClip**（按标注者个性化） | **60.16%** |

→ **结论：拿 20 倍数据 pool 训练也只有 57.45%，个性化才到 60.16%。
单一全局审美 reward 的上限就在 60% 附近 —— 因为口味本身不收敛。**

**三条直接含义**：

1. **任何声称单一全局审美 reward 显著超过 60% 的结果，先怀疑泄漏。**
   这不是空话：TOCHI 2022 已经在 Webthetics 上抓到过一次 —— 广为引用的 r ≈ 0.85 含**训练集 / 验证集重叠**，真实值是 LCC ≈ 0.752
2. **个性化比 pooling 多 2.7 个点**（60.16 对 57.45）→ 如果目标用户群明确，按群体分别训比训一个通用的好
3. **这 60% 的上限只适用于「开放审美偏好」。** 它不适用于 §6 那套程序化判据 ——
   那套测的不是「谁更好看」，是「有没有违反可测量的规范」，真值不来自口味
   （对照：WiserUI-Bench 用**真实 A/B 转化率**当真值，最佳 MLLM 也只有 60.11%，但那是模型能力问题不是标签噪声问题）

### 5.1 核实结果：成稿引的「65.0% → 92.0%」要加三条限定

出处是 WebDevJudge（arXiv 2510.18560，2025-10-21 提交，v3 2026-03-03）表 1。
[核实] 数字本身对，但**口径必须改写，否则容易被反驳**：

| 条件 | 含 tie 的两名标注者 raw 一致率 | 不含 tie |
|---|---|---|
| **无 rubric**（直接标偏好） | **65.0%** | 91.3% |
| 无 rubric，标注者与原始投票者 | 53.0% | 77.4% |
| **有 rubric（人工撰写的 rubric tree）** | **92.0%** | 95.5% |
| 有 rubric（LLM 生成的 rubric） | **90.0%** | 95.1% |

三条必须写出来的限定：

1. **不是同一批样本上的受控对比**：65.0% 来自 **100 条**实例，92.0% / 90.0% 来自**另外 50 条**（人工构造了 rubric tree 的那 50 条）。严格说不构成受控 A/B，原文也没给置信区间
2. **是 raw agreement，没做 chance correction**，不是 kappa。标注者只有 2 人（LLM-rubric 那一档由第 3 人标）
3. **654 不是一致率的样本量**，654 是最终 benchmark 的规模（269 a / 276 b / 109 tie）。全量标注完成后在抽样子集上的最终一致率是 **89.7%**

顺带两组对本文有用的数（同一篇表 3、表 4）：

| | Single-answer | Pairwise |
|---|---|---|
| 最好的 LLM judge（GPT-4.1） | 60.86 | **70.34** |
| Claude-4-Sonnet | 59.17 | 70.18 |
| **人类天花板** | — | **84.56** |

- pairwise 比 single-answer 平均高 **8 个点以上** → **审美维度不要用 pointwise 打分**
- 输入消融：**只给截图，pairwise 掉 9.79~10.7 个点；只给代码，只掉 0.31~2.60 个点**
  → **代码是主导模态，截图是补充**。这与 ArtifactsBench 的消融方向一致（去掉代码只给图从 90.95% 掉到 74.94%）
  [推断] 对我们的含义：审美 judge 的输入必须包含关键源码片段，而不是只喂截图

### 5.2 核实结果：平局口径有两处要改，而且这个集根本不是纯审美指标

**改法一：18% 是 26% 的子集，不是另加。**
出处是 LMArena / Arena.ai 官方博客 *WebDev Arena*，2025-03-10 发布、2025-06-13 更新，https://arena.ai/blog/webdev-arena
- [原文] "Webdev Arena has a 26% tie ratio and Chatbot Arena has a tie ratio of 35%."
- [原文] "our analysis indicates that **18% of user votes fall into the 'both bad' category**, often due to **dependency resolution failures, incorrect state management, or TypeScript-related compilation errors**."
- 原文紧接 26% 之后说 "out of the ties" → **18% 含在 26% 里**。写成「26% 平局 + 18% 都差」是错的加法

**改法二：别用博客的 26%，用官方数据集自己算。**
官方 HuggingFace 数据集 `lmarena-ai/webdev-arena-preference-10k`（N = 10,501）的 `winner` 列频次：

| 票型 | 占比 |
|---|---|
| A 胜 | 37.93% |
| B 胜 | 37.77% |
| tie | **7.29%** |
| **tie（both bad）** | **17.01%** |
| **平局类合计** | **24.30%** |

→ **实测 24.30%，不是博客的 26%**；both-bad 的 17.01% 与博客自称的「约 18%」吻合。
对照 Chatbot Arena 100k（N=106,134）：tie 19.29% + bothbad 19.07% = **38.36%**；140k：15.88% + 11.62% = **27.50%**。
**引用必须写清是博客口径还是数据集口径，以及哪个数据集。**

**最重要的一条：这个集不是纯审美指标。**
原文把「都差」归因到**依赖解析失败、状态管理错误、TypeScript 编译错误** —— 全是功能问题。
→ [推断] WebDev Arena 的 Elo 里有约 **17%** 的信息量被功能失败吃掉了。
用它当审美目标，等于让一个混了近两成功能噪声的信号去驱动审美迭代。
**这是把审美延后的一个更硬的理由，也是自建评测的一个更硬的理由。**

**第三条：平局不该记 0.5。**
arXiv 2510.02306（*Drawing Conclusions from Draws*）实测：平局不代表两个模型等强，而更多反映 **query 难度** ——
很简单的 query 平局风险比 **1.37**，高客观性 query **1.35**。
在 3 个真实 arena 数据集、4 种评分系统上，**让平局不触发评分更新，反而把含平局的胜负预测准确率相对提升 1~3%**。
→ **直接动摇 BT / Elo 默认的「tie 记 0.5」。** 对我们的处置见 §5.7。

### 5.2b 竞技场的置信区间：头部本来就分不开

官方 `lmarena-ai/leaderboard-dataset`（config = `webdev`，publish_date 2026-10-13）给了逐模型 `rating_lower` / `rating_upper`：

| 口径 | 数值 |
|---|---|
| webdev overall（142 模型，vote_count 合计 1,283,033 ≈ 641,517 场） | **置信区间宽度中位数 16.9 分**，最窄 9.8，最宽 81.1 |
| webdev-html（141 模型） | 中位 35.1，最宽 132.9 |
| webdev-react（126 模型） | 中位 19.6 |

**头部拥挤的实例**：rank1 claude-opus-5.5-max **1811.1 [1796.6, 1825.7]**（2,597 票）与 rank2 gpt-6-astra-max **1780.2 [1769.7, 1790.8]**（5,746 票）不重叠；
但 **rank 2 / 3 / 4（1780.2 / 1773.7 / 1760.1）互相重叠 → 前四名统计上不可区分**。

→ **这比 §5.4② 用公式推出来的 ±14 更可信，因为是官方自己报的。** 两者量级一致，公式可用。
→ 直接含义：**排名差小于约 17 分的模型对不能当监督信号，也不能写进里程碑。**

**另外两条必须记的竞技场风险**：

| 风险 | 证据 |
|---|---|
| **厂商可以对 Arena 分布过拟合** | *The Leaderboard Illusion*（arXiv 2504.20879）：厂商可私测多变体再择优公开、可撤回难看的分数；极端案例是**Meta 在 Llama-4 发布前测了 27 个私有变体**。数据份额不均：Google 约 19.2%、OpenAI 约 20.4%，而 **83 个开源权重模型合计只有约 29.7%**。额外 Arena 数据带来的相对提升**最高达 112%**（在 Arena 分布上）→ 是对 Arena 动态过拟合，不是通用能力提升 |
| **风格混淆** | 官方自己上了 style control（arena.ai/blog/style-control，2024-08-28）：把风格当独立变量加进 BT 回归，初版控四个特征 —— **答案 token 长度、markdown 标题数、加粗数、列表数**。即官方承认未控风格的榜含显著长度与排版偏差 |

### 5.2c Design Arena 不能当训练信号（与 §2.2 的补充）

[一手核实] 它的数据模型里**根本没有平局列**：公开 API 返回的每一行都满足 `wins + losses == battles`，191/191 全成立。
UI 只有「选 A / 选 B」，**没有 tie、没有「两个都差」**。
置信区间字段 `btStdErr` 在测到的全部类目、全部模型上**都是 null**。
赛制是 4 个模型 + 1 备份、**一个 tournament 跑 5 场**（含胜者组 / 败者组 / Tie Breaker）→ **同一 session 的 5 票高度相关**，当独立样本会严重低估方差。
规模（website 类目）：191 个模型 / 2,201,736 battles ≈ **110 万票**。

→ **只能当外部校准集（相对序做 sanity check），不能当训练信号。** AesCoder 就是这么用的（与它的排名 Spearman 0.98）。

### 5.3 核实结果：审美标注的人数曲线

AUV-Bench（arXiv 2609.34854，2026-09-28）：51 名职业 UI 设计师（≥3 年经验）招募、质控后留 **44 名**（剔除 7 名「全给同一个极端分」的退化标注者），
**1,395** 条可执行 Web UI，**每条 3 人独立标**，8 个维度 1~5 分，质控前共 33,480 条维度级评分。

[核实] 逐维度可靠性（ordinal Krippendorff α / 单向随机效应 ICC(1,3)）：

| 维度 | α（单人） | ICC(1,3) |
|---|---|---|
| **Color** | **0.328**（最低） | 0.596 |
| Typography | 0.334 | 0.609 |
| Copy Quality | 0.334 | 0.610 |
| Graphics & Imagery | 0.346 | 0.614 |
| Visual-style Consistency | 0.366 | 0.635 |
| Component Consistency | 0.399 | 0.672 |
| Image–Text Fit | 0.402 | 0.667 |
| **Layout** | **0.431**（最高） | 0.694 |
| **宏平均** | **0.368** | **0.637** |

**注意「最可靠的维度正好是最可程序化的那一维」**：Layout α=0.431 最高，Color α=0.328 最低。
[推断] 这不是巧合——越接近几何与可测量属性，人越容易一致；越接近配色品味，人越不一致。
**这条给 §6 的分工提供了独立支持：该程序化的恰好是人也最容易一致的那一半。**

### 5.4 样本量计算

#### ① 要多少个标注者（Spearman-Brown）

公式：`ICC(1,k) = k·ICC(1,1) / (1 + (k−1)·ICC(1,1))`，反解 `k = ρ_target·(1−ICC₁₁) / (ICC₁₁·(1−ρ_target))`

AUV-Bench 只报了 ICC(1,3)=0.637，反解 **ICC(1,1) = 0.637 / (3 − 2×0.637) = 0.3691**（与逐维度 0.329~0.431 区间一致）。
**原文没有 Spearman-Brown 曲线，下表是本文按公式算的。**

| 起点 ICC(1,1) | ICC ≥ 0.70 | **ICC ≥ 0.80** | **ICC ≥ 0.90** | ICC ≥ 0.95 |
|---|---|---|---|---|
| **0.369（宏平均）** | 4 人 | **7 人** | **16 人** | 33 人 |
| 0.329（Color，最差） | 5 人 | 9 人 | 19 人 | 39 人 |
| 0.431（Layout，最好） | 4 人 | 6 人 | 12 人 | 26 人 |

→ 现状 3 人给到 ICC 0.637。**要到心理测量学常用的 0.80 门槛，需要 7 人（成本 ×2.33）；0.90 需要 16 人（×5.33）。**

**两条必须写的 caveat**：
- Spearman-Brown 假设评分者可交换、误差独立同方差。审美标注很可能存在共享偏差（审美流派、训练背景），那样外推**偏乐观**，真实曲线会提前封顶
- §5.5 的那篇论文正是在量化这种共享偏差 → **7 人 / 16 人应当当作乐观下界**

#### ② pairwise 偏好要多少场（Bradley-Terry）

- Elo ↔ logit：`Δ_Elo = θ × 400/ln10`，即 **1 logit = 173.72 Elo**
- `SE(θ̂) = 1/√(n·p(1−p))`，两模型接近时 p≈0.5 → **SE_Elo ≈ 347.4/√n**
- 置信区间半宽 h：`n = (1.96×173.72/h)² / 0.25`
- 检测 Δ Elo（80% power，α=0.05 双侧）：`n = 947,600 / Δ²`
- **n 指「有信息的（非平局）」对战**。WebDev Arena 26% 是平局/都差 → 原始票数需 **÷0.74 ≈ ×1.35**

| 目标 | 有信息对战 | 原始票数（含 26% 平局） |
|---|---|---|
| 置信区间半宽 ±30 Elo | 515 | 696 |
| 置信区间半宽 ±20 Elo | 1,159 | 1,567 |
| **置信区间半宽 ±10 Elo** | **4,637** | **6,267** |
| 置信区间半宽 ±5 Elo | 18,549 | 25,066 |

| 检测 Δ（80% power） | 有信息对战 | 含平局 |
|---|---|---|
| Δ = 10 Elo | 9,475 | 12,804 |
| Δ = 20 Elo | 2,369 | 3,201 |
| **Δ = 30 Elo** | **1,053** | **1,423** |
| **Δ = 50 Elo** | **379** | **512** |
| Δ = 100 Elo | 95 | 128 |

**公式的实测校验**：2025-12-23 的 WebDev Arena 快照是 75,257 票 / 32 个模型 ≈ 2,350 票每模型，
榜上观测到的置信区间半宽是 **±12 ~ ±17**。
按公式预测：`1.96×173.72/√(2350×0.25) = ±14.0` —— **与观测吻合**。公式可用。

→ **读法**：`07_capability_spec.md` 里 Design Arena 的开闭源差距约 **69 Elo**、Code Arena WebDev 约 **139 Elo**。
按上表，69 Elo 只要约 **200 场有信息对战**就能检出，139 Elo 只要约 **50 场**。
**所以「众包 Elo 慢」不是因为要的场次多，是因为场次来自真人、到达率不可控。** 这是一个供给问题，不是统计问题。

#### ③ 1~5 分 MOS 要多少题

⚠️ **AUV-Bench 没有报 MOS 的标准差**，这是唯一必须自己量的参数。下表用 σ_total = 0.9（1~5 分制上的常见值）。
由 ICC(1,1)=0.3691 得 σ_between = 0.547、σ_within = 0.715。

单题 k 人均值的测量标准误 = σ_within/√k：

| σ_total | k=1 | **k=3（现状）** | k=5 | k=7 | k=16 |
|---|---|---|---|---|---|
| 0.8 | 0.635 | 0.367 | 0.284 | 0.240 | 0.159 |
| **0.9** | 0.715 | **0.413** | 0.320 | 0.270 | 0.179 |
| 1.0 | 0.794 | 0.459 | 0.355 | 0.300 | 0.199 |

→ **现状 3 人，单条 UI 的 MOS 测量标准误约 0.41 分。单条 UI 上 0.2~0.4 分的差异读不出来。**

两系统比较所需题量（σ_total=0.9，80% power，α=0.05 双侧，按 prompt 配对、假设难度相关 ρ=0.5）：

| k | 单观测 SD | δ=0.2 | δ=0.3 | δ=0.5 |
|---|---|---|---|---|
| 1 | 0.900 | 159 | 71 | 26 |
| **3** | **0.685** | **93** | **41** | **15** |
| 5 | 0.633 | 79 | 35 | 13 |

不配对（两组不同 UI）时翻倍：k=3 时 δ=0.2 需 **185 题每组**，k=16 只降到 **130 题**。

→ **结论：题量的下限由 σ_between（UI 本身的真实差异，0.547）卡住，加人只能削掉 σ_within/√k 那一块。**
k 从 3 加到 16，人力涨 5.3 倍，δ=0.2 的题量只省 30%。
**对系统级比较，加题比加人划算；加人只在需要单条 UI 可信判读（做 GT、做 case 诊断）时才值得。**

### 5.5 模型投票的有效独立性：10 个 judge 只值 3.5 个

[核实] arXiv 2609.22512（2026-09-18，*Agreement Overstates Evidence: Error Dependence in LLM Judge Consensus*）：

| 说法 | 原文 | 结论 |
|---|---|---|
| 10 个 judge 平均成对错误相关 0.21 | RewardBench 1,133 条校准对上 **ρ̄ = 0.206**（chance-corrected 的 κ=0.20、α=0.20 接近） | ✓ |
| 信息量等于 3.5 个独立 judge | design effect `1+(m−1)ρ̄ = 1+9×0.206 = 2.85` 倍方差膨胀 → **n_eff = 10/2.85 = 3.51** | ✓ |
| 28% 的系统对比会得出假显著 | 原文是 **"in up to 28% of our comparisons"** | ✓ **必须带 "up to"** |

必须一起写的限定：
- **28% 只在 RewardBench 的 Focus 子集上**。Factuality 是 22%，**Math 与 Precise IF ≤ 2%**。它是上界，不是普适数字
- 原文明确警告 n_eff **不等于「可以只用 3.5 个 judge」**："it does not predict majority-vote accuracy or imply that 3.5 judges could replace the full bank"
- **前沿 judge 更准但错误共享更多**（跨厂商也一样）→ **换更强的 judge 不解决问题**
- 同族 / 同 prompt 风格**不解释**相关性：prompt-style contrast +0.000（CI [−0.014, +0.014]），model-family contrast −0.078（方向与预注册假设相反）
- 只换训练 seed 的两个 GRPO judge 错误相关 **0.36~0.39**（跨模型均值 0.24），加第二个 seed 只让 n_eff 涨 **0.11**
- **即使 10:10 全票一致，也只值 3.51 个独立投票**

[实测] 本项目的独立数据同向（`90_local_experiments.md` §3）：
4 个不同家族的 judge、48 个 case、temperature 0、每个 case 每种条件跑 2 次：
单模型重测翻面率 **4.2% ~ 20.8%**（claude-opus-5-5 在多视角档是 20.8%，最差）；
4 模型 8 票多数投票单视角 44/48、多视角 46/48，而**程序化信号在同一标注集上是 47/47**。

### 5.6 三条路的成本与噪声对照

| 路 | 噪声 | 单位成本 | 周期 | 能不能当 RL reward |
|---|---|---|---|---|
| **人类众包 Elo** | 单场信息量低（26% 平局，其中 18% 是功能失败导致的「都差」）；但聚合后噪声最小（±14 Elo @ 2,350 票） | 真人，不可控 | 周到月 | **不能**：到达率不可控，且 18% 的信息量是功能噪声 |
| **专家 rubric 标注** | 单人 α=0.368；3 人 ICC 0.637；7 人才到 0.80 | 7 人 × 题量；AUV-Bench 口径是 44 名设计师 × 1,395 UI × 3 人 | 周 | **不能当在线 reward**，但是**唯一能当校准真值的东西** |
| **模型投票（rubric 化）** | 单次翻面 4.2%~20.8% [实测]；10 票只值 3.5 票；judge 对自家产物有自我偏好 | 每样本 3 次调用（按 r=2 的降噪效果算） | 分钟 | **能，但只能放在硬闸之后做组内 pairwise**，不能 pointwise、不能单独决定分数 |
| **程序化判据**（本文 §6） | **0**（实测两次独立运行 20/20 连续读数逐位相同） | 0.8 秒 / 页，纯 CPU | 秒 | **能，而且是唯一能当乘法硬闸的** |

**协议建议（可执行）**：

| 层 | 内容 | 采样 | 噪声 |
|---|---|---|---|
| L0 硬闸 | 能跑、画布非空、无运行时报错 | n=1 | 0 |
| **L1 审美硬闸** | **§6.4 的 6 条已验证判据**（hier / scale / family / lh / hue / contrast / spacing） | **n=1** | **0** |
| L2 功能断言 | DOM 状态、交互前后差分、多视口不塌 | n=1 | 低 |
| L3 rubric 化模型评审 | 只放 Design quality 与 B 类子项；**输入必须含关键源码片段**（§5.1 消融） | r=3 多数票，**降噪按 r=2 计** | 中高 |
| L4 组内 pairwise | 同一 query 的通过者两两比，AB/BA 各一次，不一致记 tie | 组内 | 较低 |
| 校准集 | 200 对专家裁决，**每条至少 3 人**（目标 7 人） | 季度重标 | ICC 0.637 → 目标 0.80 |

**采样量**：按 `07_capability_spec.md` §4.3 的公式，L3/L4 的 VLM rubric 档
`MDE = 2.38/√(M·n)`。审美维度建议 **M=30 题、n=8** → MDE ≈ 15.4 个百分点。
这个分辨率只够读「大改动」。想读 5 个点需要 M·n ≈ 2,260（例如 M=40、n=56），**在审美维度上不划算**。
→ [推断] **所以审美维度的迭代信号应该主要来自 L1 的零噪声硬闸（通过率可以 n=1 读），而不是 L3 的 rubric 分。**

---

## 6. 本机实验：可程序化那一半到底能做到多准

### 6.1 设置

- 代码：`scripts/vc_verifier/web/aesthetic.js`（探针）、`aes_verify.js`（判据与阈值）、`aes_mutants.js`（变异集）、`run_aes.js`（跑测）
- 复跑：`cd scripts/vc_verifier/web && node run_aes.js`（17 秒，20 个变异）；加 `WITH_FN=1` 同时跑功能侧 W0~W4 对照（66 秒）
- 环境：无 GPU，Chrome 148 无头 + SwiftShader，固定视口 375 / 1440，固定 `Math.random` 种子与 `Date`
- 探针**只读 computed style 与几何**，不做像素比较、不调 VLM
- 阈值来源：先测参考页，再加余量冻结，写在 `aes_verify.js` 顶部（每条都注明了参考页实测值）

### 6.2 结果

| 口径 | 数字 |
|---|---|
| 参考页 | **11 条判据全过**，tell 未命中 |
| 该挂的审美变异（剔除 1 个无效变异后） | **抓到 9/11** |
| 不该挂的合法改版 | **判过 8/8**（零误杀） |
| 总计 | 17/20（含 1 个判定为无效的变异） |
| 单个变异耗时 | 约 0.8 秒（两个视口） |

逐条结果：

| 变异 | 该挂 | 判定 | 功能侧 W0~W4 |
|---|---|---|---|
| A01 h2 比 h1 大（层级反了） | 是 | 挂@hier ✔ | **过**（瞎） |
| A02 字号变成一堆相近随机值 | 是 | 挂@hier+len ✔ | **过**（瞎） |
| A03 四种字体混用 | 是 | 挂@family ✔ | **过**（瞎） |
| A04 正文行高压到 1.02 | 是 | 挂@lh ✔ | **过**（瞎） |
| A05 去掉 60ch 限宽 | 是 | 过 ✘ → **判定为无效变异** | 过 |
| A06 塞进五个互不相关的色相 | 是 | 挂@hue+contrast ✔ | 挂@W2（**只因为顺带破了对比度**） |
| A07 间距全换成奇数值 | 是 | 挂@spacing ✔ | **过**（瞎） |
| A08 每个组件一个圆角 | 是 | 过 ✘ → **信号作废** | **过**（瞎） |
| A09 各区块左边距都不同 | 是 | 过 ✘ → **信号作废** | **过**（瞎） |
| A10 抹掉所有内外边距 | 是 | 挂@spacing ✔ | **过**（瞎） |
| A11 Inter 字体 + 白卡紫渐变 | 是 | 挂@contrast ✔，**tell 命中** | 挂@W2（**只因为顺带破了对比度**） |
| A12 非标题元素各用一个随机字号 | 是 | 挂@scale ✔ | **过**（瞎） |
| P01 品牌色换成同样深的绿 | 否 | 过 ✔ | 过 |
| P02 换成另一套自洽的等比尺度 | 否 | 过 ✔ | 过 |
| P03 间距规整到 8 的倍数 | 否 | 过 ✔ | 过 |
| P04 品牌蓝的单个渐变 | 否 | 过 ✔（tell 未命中） | 过 |
| P05 深色主题 | 否 | 过 ✔ | 过 |
| P06 整体留白加大 | 否 | 过 ✔ | 过 |
| P07 类名重命名 | 否 | 过 ✔ | 过 |
| P08 HTML 压缩 | 否 | 过 ✔ | 过 |

**最重要的一列是最后一列**：11 个审美变异里功能侧判过 **9 个**，剩下 2 个被抓到也只是因为改色顺带把 WCAG 对比度弄挂了。
→ **审美不是「功能判据的延伸」，它是一块独立的盲区。** 这也说明把审美整维推迟，等于在训练里放着一块无人看守的区域。

### 6.3 三条失败与它们的含义（比成功的那 9 条更有用）

**① A05 是无效变异，不是判据失效**
参考页最长段落只有 46 个字符。去掉 `max-width:60ch` 之后实际行长 46ch，**根本不构成「行太长」这个缺陷**。
按冻结规则剔除该变异，而不是把阈值调到 46 以下。
含义：**行长这条判据需要题面里有真实正文才能验证。** 现在的参考页验不了它，它的判别力处于「未验证」状态。

过程中还修掉一个真 bug：`widthCh` 原来用容器宽度除以估算字宽，于是「25 字的短标签放在 1400px 容器里」被算成 200ch。
修法是 `min(容器容量, 实际字符数)`。修之前参考页在 1440 档就有 1 个假报警。
**含义：审美指标的假阳性多数来自度量定义本身，不是来自阈值。**

**② A08 圆角一致性：没有判别余量**
参考页本来就有 4 种圆角（6 / 8 / 10 / 999px，999 是胶囊形）。变异把它推到 6 种。
参考页和坏页面的距离只有 2 档，而**正常设计就会用到 3~4 种圆角**（按钮、卡片、徽章、胶囊各一种）。
→ 这个信号**作废**，只保留为记录字段。

**③ A09 栅格对齐：可分离，但余量只有 0.058，而且好页面比坏页面更接近失败**

| case | 该挂 | 对齐率（落在前 3 条垂线 ±2px 内的块占比，取两视口最差） |
|---|---|---|
| 参考页 | — | 0.824 |
| **A09 各区块左边距都不同** | **是** | **0.707** |
| A07 间距全换成奇数值 | 是 | 0.794 |
| **P03 间距规整到 8 的倍数** | **否（审美更好）** | **0.765** |
| A10 抹掉所有边距 | 是 | 1.000 |
| 其余 15 个 case | — | 0.824 |

存在可分离阈值（0.707 < t ≤ 0.765），但：
- 余量只有 **0.058**，相对参考页 0.824 是 7%
- **P03 这个「审美更好」的改版，比 A07 这个坏改版更接近失败**
- A10（抹掉所有边距，最糟的那个）对齐率反而是 **1.000**（所有块都贴在 x=0 上）—— **指标方向在极端情形下翻转**

→ 这个信号**作废当闸**，只保留为连续诊断量。
这一条也是整节最该记住的方法论：**一个指标「能把该挂的和不该挂的分开」不等于「能当闸」。还要看余量、要看好样本在哪一侧、要看极端情形下会不会翻向。**

### 6.4 可以当零噪声硬闸的 7 条判据（冻结版）

| 判据 | 判什么 | 阈值（参考页实测值） | 被哪个变异验证过 |
|---|---|---|---|
| `hier` | h1..h6 字号单调不增，且都 ≥ 正文 | 违例数 = 0（参考 0） | A01、A02 |
| `scale` | 字号种类数与相邻比值变异系数 | 种类 ≤ 11（参考 7）；CV ≤ 0.35（参考 0.133） | A12 |
| `family` | 字体族数量 | ≤ 2（参考 1） | A03 |
| `lh` | 正文行高倍数在 1.35~1.8 | 越界段数 = 0（参考 0） | A04 |
| `len` | 每行字符数 | ≤ 90（参考 42.8）；越界段数 = 0 | **未验证**（见 §6.3①） |
| `hue` | 色相家族数与色相熵 | 家族 ≤ 3（参考 1）；熵 ≤ 2.0（参考 0） | A06 |
| `contrast` | WCAG 1.4.3 文本对比度 | 不达标样本数 = 0（参考 0，最小比值 6.27） | A06、A11 |
| `spacing` | 间距取值种类数 + 自动选基数后的倍数占比 | 种类 ≤ 20（参考 12）；占比 ≥ 0.70（参考 0.914 @ base=2） | A07、A10 |
| `ink` | 墨水覆盖率 | 0.06 ~ 0.78（参考 0.296 / 0.526） | A10（实际由 spacing 先抓到） |

说明：
- **其中三条判据查不到任何现成实现**（§2.3②）：`scale`（字号等比尺度自洽）、`hier`（视觉层级单调性）、`spacing` 的「自动选基数再看占比」。
  检索结论是：modular scale 没有任何指标或 linter；视觉层级单调性没有专门检查（a11y 的 heading-order 不算）；
  间距节奏只有工业 lint 写死「不许用数值 utility」，没有「自动选基数」的做法。
  唯一有现成实现的是行高节奏 —— `@double-great/stylelint-a11y` 的 `line-height-is-vertical-rhythmed`（baselineGrid 默认 24，无单位值要求 ≥1.5）
- 8 条进闸，其中 `len` 的判别力未验证、`ink` 没有独立验证（总是被 `spacing` 先抓到）→ **真正被独立验证过的只有 6 条**
- 阈值全部从参考页反推 + 余量，没有一条是在变异集上调出来的。唯一一次「看到结果后改」的是 §6.3① 的度量定义 bug 修正，以及把 radius / grid 两条信号作废（不是放宽阈值）
- 单页判定耗时约 0.8 秒、纯 CPU、无 judge → 适合做 RL 的 L0/L1 层乘法闸

### 6.5 这套判据的已知可 hack 面

[推断] 还没有实测，但按 `11_hacking_defense.md` 的形态推：

| hack | 怎么做 | 对策 |
|---|---|---|
| 塌缩到极简白页 | 只放 2 个字号、1 个色相、全是 8 的倍数间距，内容极少 | `ink` 下界（0.06）挡一部分；必须叠加内容完整性断言（元素数、文本量、题面要求的组件是否都在） |
| 用图片代替排版 | 把整页做成一张图，computed style 上就没有字号与间距可测 | 加「文本节点数 / 可提取文本量」下界；加 OCR 对账 |
| 色相熵刷低 | 全站单色灰阶 | 熵只设上界不设下界是故意的——但要在 rubric 侧看「是否符合题面指定的风格」 |
| 间距基数刷高 | 所有间距都设成同一个值 | `spacing` 的种类数下界（目前没设）；[推断] 应补一条「种类数 ≥ 3」 |
| tell 规避 | 换成 Space Grotesk + 青绿渐变 | tell 列表天然会过期。Anthropic 原文已承认禁掉一组默认值后会收敛到新的默认值（"the model can default to other common choices (like Space Grotesk …)"）→ **tell 清单必须周期重算，而且只能当批次诊断，不能当长期闸** |

---

## 7. 结论：可落地的路线

### 7.1 三档处置

| 档 | 子项 | 怎么用 | 依据 |
|---|---|---|---|
| **今天就能做成零噪声程序化 reward** | 文本对比度、视觉层级单调性、字号尺度自洽、字体族数量、行高、色相家族数与熵、间距节奏与基数、墨水覆盖率上下界、多视口不塌 | **乘法硬闸**，不计权重，不过就截断后续评分。n=1 即可读，0.8 秒/页，纯 CPU | §6.2 实测：9/11 该挂抓到、8/8 不该挂不误杀、参考页全过；功能侧对其中 9 个完全瞎 |
| **该用 rubric 化模型评审** | 排版品味、配色协调、组件一致性、动效克制、Design quality 的「整体感与识别度」 | **闸后**做组内 pairwise（不做 pointwise），AB/BA 各一次，r=3 但降噪按 r=2 算；输入必须含关键源码片段 | pairwise 比 pointwise 高 8 点以上；只给截图掉 9.79~10.7 点而只给代码只掉 0.31~2.60 点（§5.1）；10 个 judge 只值 3.5 个（§5.5） |
| **彻底放弃当 reward，只当验收** | 风格取向、品牌调性、原创性整体、圆角一致性、栅格对齐、**全部经典计算美学指标**（Ngo 13 项、Miniukovich 8 项、AIM 的色彩和谐） | 原创性只保留**具名 tell 的负向闸**（且 tell 清单要周期重算）；圆角与栅格只保留为连续诊断量；风格只判「是否符合题面指定的风格」；经典指标只能当 **veto**（例如 density 远离 50% 时打回），**绝不当排序器** | 圆角无判别余量、栅格余量只有 0.058 且极端情形指标翻向（§6.3）；tell 清单会过期（Anthropic 原文已承认会收敛到 Space Grotesk 这类新默认）；**经典指标全部单调可刷 → RL 收敛到空白单列页**，Ngo 系还被实测为**非单调**（Ngo 分最高的布局最不受偏好，评分者 W=0.1023），Purchase 2011 在真实网页上实测 **14 项里只有 1 项有效** |

### 7.2 一个必须改的既有判断

成稿（`draft_training.md`）写「审美类任务的 reward 噪声来自人本身，用 RL 去优化这种信号，等于把噪声刻进权重」，并引 α=0.368 作为依据。

**这句话对 B 类和 C 类成立，对 A 类不成立。** A 类子项的 reward 根本不经过人：
它从 computed style 和几何里直接算出来，两次重跑结果完全一致，噪声是 0。
[实测] 两次独立运行全部 20 个 case：**不只判定一致，连每一条连续读数都逐位相同**（0/20 不一致）。

→ 建议把成稿那一句改成：
> 审美里**凭人判的那一半**噪声来自人本身（单人 α=0.368），不适合直接当 RL 信号；
> 但**可测量的那一半**（对比度、层级、尺度、间距节奏、色相关系、留白）是确定性的，
> 噪声为 0，而且现有功能判据对它完全瞎 —— 这一半应该在阶段二就接进 RL，而不是推到最后。

同时 `draft_overview.md` 的「阶段二刻意把审美排除在外」需要拆成两句：
**排除的是众包 Elo 与 rubric 分，不是审美的程序化那一半。**

### 7.3 这条路线能覆盖前沿优势的多大比例

**无法估计。** 三条理由，都是证据层面的缺口而不是推理层面的：

1. **没有任何公开工作把审美 Elo 差距分解成子项。**
   已知的差距是 Design Arena 约 **69 Elo**（Opus 5.5 1392 对开源最好 1323）、
   Code Arena WebDev 约 **139 Elo**（Opus 5.5 1813 对 Qwen3.8-Max 1674，见 `07_capability_spec.md` §1.3）。
   但没有工作回答「这 69 点里有多少来自 craft 类缺陷、多少来自整体感」。

2. **已知的那部分 Elo 差距里还混着功能噪声。**
   WebDev Arena 自己把 18% 的「两个都差」归因到依赖解析失败、状态管理错误、TypeScript 编译错误（§5.2）——
   **这三件事都不是审美。** 所以 Elo 差距的分母本身就不纯。

3. **一条反向的参考：前沿模型的绝对审美分也很低。**
   AUV-Bench 校准后的绝对审美分只有 **2.78 ~ 3.18 / 5**，而 pairwise 胜率可以接近 80%。
   原文的读法是「相对强不等于绝对好」。
   [推断] 这说明**「到好设计」的差距远大于「前沿到开源」的差距**。
   也就是说，这条路线即使只覆盖前沿优势的一小部分，它覆盖的也可能是「到好设计」这条更长的路上的一大段。

4. **「凭人判」那一半有一个 60% 的硬天花板，而且它是口味不收敛造成的。**
   DesignPref：20 位职业设计师的二元一致只有 0.624、α=0.248；pooled 训练 57.45%、个性化 60.16%（§5.0）。
   → [推断] **这意味着「追平前沿审美」这个目标本身在开放偏好口径下是测不准的。**
   能追的只有两件事：① §6 那套不受天花板约束的程序化判据 ② 相对 Elo（但见 §5.2b，排名差小于 17 分不可区分）

**能给出的替代判据**（不依赖上面那个无法估计的比例）：

| 可检验目标 | 口径 | 目标 |
|---|---|---|
| 审美硬闸通过率 | §6.4 的 6 条已验证判据，在自建审美题集上，n=1 | 基座 → **≥ 95%**。这一项零噪声，可以逐轮看 |
| 审美硬闸不被 hack | §6.5 的 5 种 hack 形态各造 10 个样本 | 全部判 0；每次改判据先跑这一组 |
| 变异判别力 | 审美变异集（当前 11 个有效 + 待扩到 ≥40） | 该挂抓到 ≥ 90%、不该挂误杀 ≤ 2% |
| 专家校准集一致性 | 200 对，每条 ≥3 人（目标 7 人） | ICC(1,k) **≥ 0.80**（当前 3 人是 0.637，需 7 人） |
| **外部校准（不依赖口味）** | **WiserUI-Bench**（300 对，胜者由真实 A/B 转化率决定） | **≥ 60%**（参照：最佳 MLLM GPT-4o 60.11%，随机 50%）。**务必做 AB/BA 交换** —— 该集上 o1 的位置偏置是胜者在前 16.56% 对在后 97.78% |
| 相对审美 | Design Arena Elo，带快照日 | ≥ 1360（参照：Opus 5.5 1392、Astra 1379、开源最好 1323）。**这一项只做季度验收，不做迭代指标** |

### 7.4 立刻该做的四件事（按性价比排序）

1. **把 §6.4 的 6 条判据接进现有 `probe.js` 的分层闸**，作为 W5 层。成本：已有代码，0.8 秒/页
2. **扩审美变异集到 ≥40 个**，并且**换一个带真实正文的参考页**——当前参考页验不了行长判据（§6.3①），也只有一个版式。
   扩题可以直接照 **arXiv 2607.20690** 的做法自动化：往干净的生成页注入已知违规、合成约 10,000 页、训一个小 VLM 当 critic，
   它实测 micro-F1 从 36% 提到 84%（19 条原则里 13 条 >80%），**作者本人就把它定位为 reward signal**。
   ⚠️ 但那 84% 是在合成注入的违规上测的，分布外迁移未验证
3. **补 §6.5 的两条缺失下界**：间距取值种类数 ≥ 3、文本节点数与可提取文本量下界（防塌缩到极简白页和整页贴图）
4. **做 §3.3 的措辞 A/B**：同一 generator、同一 evaluator、两套只在措辞上不同的 rubric（一套含「博物馆级」，一套不含），
   测产出的**分布集中度**（§4.7 的指标 1 与指标 2）而不是分数。这是把 Anthropic 那条无量化的经验变成可验证结论的最小实验。
   现成的参照口径：The Price of Format（arXiv 2505.18949）同 checkpoint、同采样参数、**只换 prompt 包装，标签分布熵跌 31%~69.7%**
5. **把「样式集中度指纹」接进批次级验收**（已有代码，`aes_concentration.js`，11 页跑完约 10 秒）。
   报 fontFamily / hue / fontSize / radius / spacing 五个维度的 HHI 与归一化熵，**不要只报具名 tell**（§4.8 实测）。
   第一优先要补的是**人类设计基线**：采一批真实站点做对照组，否则 HHI 0.50 是高还是低无从判断
6. **先查自己的 harness 有没有在规定收敛**（成本最低、可能收益最大）。按 §4.6：
   检查 system prompt / skill 里有没有写死字体来源、有没有鼓励渐变、有没有「禁止外部文件」这类把输出锁进默认 token 空间的约束。
   Google 的 Generative UI 正是这么做的，而且是**有意为之**
7. **把「多样性」放进 SFT 数据验收，而不是只放进 RL reward**。依据：Olmo 3 的三条血统消融里
   **SFT 一步就砍掉 38%~62% 的多样性，DPO 再砍 4%~23%，而 RL-Zero 血统保留 93%**；
   并且**关掉 CoT 多样性不变 → 坍塌在权重里，推理期手段修不了**

### 7.5 本文的三条存疑

1. **§6 的所有数字来自单一参考页、单一版式。** 判别力 9/11 与零误杀 8/8 都是在一个页面的变异体上得到的，
   按 `07_capability_spec.md` §4.3 的公式，M=1 的结论只能说「机制存在」，不能说「效应量是 9/11」。扩题是第一优先
2. **`len` 判据的判别力未验证，`ink` 没有独立验证**（总是被 `spacing` 先抓到）。真正被独立验证过的只有 6 条
3. **Spearman-Brown 外推的 7 人 / 16 人是乐观下界。** 它假设评分者误差独立，而 §5.5 的论文正是在量化这个假设不成立的程度

