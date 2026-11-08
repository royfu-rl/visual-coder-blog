# 07 · Visual Coding 能力规格书：把「像 GPT-6 Astra / Claude Opus 5.5 一样」拆成可度量的能力项

- 查证日期：2026-10-15
- 目的：给复刻工作一份**规格书**。不是「做得更好看」，而是「这 13 项里我们要先打哪 3 项、测到什么数、噪声多大」
- 前置笔记（本文不重复）：`01_frontier_labs.md`（前沿实验室披露）、`03_verifiable_construction.md`（任务构造八范式）、`04_verifier.md`（verifier 分层与 hack 实例）、`05_trajectory_repair.md`（长程轨迹）、`06_harness.md`（实测 harness）、`benchmarks.md`、`frontier_evals_west.md`
- 标记约定
  - **[原文]** 可在给出链接里找到原句或原表
  - **[推断]** 本文作者从证据推出，无一手出处
  - 日期从 arXiv ID 推（YYMM）
- 全文不用美元符号，金额写「美元」

---

## 0. 四条先行结论（第 1 条与直觉相反）

1. **「自我验证 / 迭代自修正」不是前沿模型相对开源的主要差距来源。它是全行业共同的、尚未解决的瓶颈。**
   这一条在本文调研中被反复证伪了三次，必须先说清楚，否则后面的投入会压错方向。
   - **同 harness 的短程多轮 agentic 几乎没有差距**：SWE-bench Verified 官方 bash-only 视图
     （mini-SWE-agent v2.0.0，Attempts=1，2026-02-17）最强闭源 Claude 4.5 Opus **76.8**，
     开源 MiniMax M2.5 **75.8** —— 差 **1.0 个点**。SWE-bench Multilingual 差 3.0 点。
     链接：https://www.swebench.com/
   - **迭代循环的收益是弱模型拿得更多**：AutoLab（arXiv 2606.05080，2026-06）§4.3 换 harness 消融，
     改成强迫持续迭代的 mini-swe-agent* 后，**deepseek-v4-flash +0.13、mimo-v2.5 +0.20，而强单轮推理者 gpt-5.4 −0.03**。
     原文还直说精调 harness **"could close a substantial portion of the performance gap between weak and strong base models"**
   - **前沿 agent 其实根本不做自我验证**：VISTA（arXiv 2605.26144，v4 2026-09-29，18 应用 / 8,487 人工标注组件）
     审计轨迹发现 **73.0% 完全跳过了 prompt 明确要求的 self-audit，44.5% 从没打开过设计截图，8.3% 检查失败后仍报告成功**
   - **Anthropic 自己把自我验证写成缺点**：Opus 5 system card CB-2 节第一条限制是
     **"Unproductive self-verification: ... unable to complete the task within its allocated time budget after spending hours attempting to debug a verification pipeline"**；
     官方 prompting 文档要求用户**删掉**显式验证指令以免 over-verification

2. **「加循环的增益」与「单步能力」负相关 —— 所以高增益倍数是弱的标志，不是强的标志。**
   这是上一条的机制解释，两组数据同向：

   | 来源 | 单步基线 | 加循环 / 加观察后 | 增益 |
   |---|---|---|---|
   | BenchCAD（OpenAI 口径）GPT-5.6 Sol | **70.6%** | 83.4% | **1.18×** |
   | BenchCAD（OpenAI 口径）Claude Opus 4.8 | **27.3%** | 51.8% | **1.90×** |
   | 3DHarnessBench Qwen 3.8 Max | **0.740（单视角全场第一）** | 0.809 | **+5.3%** |
   | 3DHarnessBench Claude Opus 5 | 0.725 | 0.871 | **+16.4%** |

   理论上也有闭式解释：自修正是向模型固有上界的指数收敛
   `Acc_t = Upp − α^t·(Upp − Acc_0)`（arXiv 2508.16456，2025-08）——
   单步已接近上界的模型，循环的边际收益必然小。
   → **对我们是好消息**：从较低的单步基线出发，补齐循环的绝对收益反而最大。
   但**不能把「循环增益倍数」当 KPI**，否则会奖励「把单步做烂」。

3. **单步视觉能力开源已经基本追平，差距集中在「长程持久性」与「一致性」。**
   - 单视角 3D：Qwen 3.8 Max 0.740 > Claude Opus 5 0.725（3DHarnessBench）
   - 单轮指令遵循：开源 GLM-5.2 约束满足率 CSR **80.4** > Claude-Opus-4.6 **78.6**（MTAC-IFBench 2609.14992）
   - 图→码视觉保真：Design2Code 开源 Qwen3-VL-235B-Thinking **93.4** 对 GLM-5V-Turbo 94.8（差 1.4）
   - 但超长程（小时级）差距很大：AutoLab 36 个 2~12 小时任务，claude-opus-4.6 **Avg@3 0.68**
     对最强开源 kimi-k2.6 **0.46**（差 48%）。**注意这不是开源 / 闭源的分界**：
     闭源 gpt-5.4 只有 **0.36**，排在四个开源模型之后
   - 一致性比天花板动得更多：Opus 5 的 Toolathlon Verified **Pass@1 80.6 高于 Opus 4.8 的 79.9，
     但 Pass@3 反而更低（87.0 对 88.0）**，提升全在「三次全对」的 Pass³（73.1 对 71.3）

4. **真正该抄的是「取证纪律」这一条行为，而不是「让它自己多看几眼」。**
   3DHarnessBench 的观察接口消融把失败拆开了：MiniMax M3 在主动视觉档 Uni3D 只有 0.3722，
   **仅仅在截图前规范化视口**就回到 0.6148（多视角档是 0.6200）；
   Gemini 3.1 Pro 0.6776 → 换用强模型采集的检视图 0.7605（多视角档 0.7609）。
   朴素的「看自己渲染的截图再改」在**前沿模型上也是净负收益**：
   RubSE（arXiv 2608.24138，2026-08）15 轮视觉自演化，**GPT-5.2 在 Design2Code 上全部 15 轮都低于第 0 轮，终点 −2.73**。
   → 杠杆在**取证质量、取景选择、停机纪律**三项具体行为，以及**外部 critic / 执行反馈**，不在「自省」本身。
   **一条相反方向的 nuance（必须记）**：在**视觉域**里，「自我批判后重写」的增益确实前沿拿得更多 ——
   FronTalk（arXiv 2601.04203）的 AceCoder 子项，GPT-4o 文本档 56.0 → **65.3（+9.3）**，
   而 Qwen2.5-VL-72B 文本档只 **+5.9**、视觉档只 **+0.8**。
   所以 §0 第 1 条的结论适用于**通用 agentic coding**，在**视觉 / 前端**这个子域里差距要大一些。

---

## 1. 能力维度分解（核心）

### 1.1 为什么这样切

切分准则有三条，不满足任一条就不单列成维度：

1. **可单独度量**：存在一个 verifier 只看这一项，别的项全错也能给分
2. **可单独训练**：能构造出只在这一项上有差异的任务对（pairwise 或变异体）
3. **失效模式不同**：两个维度如果总是一起失败，就该合并

按此得到 **14 项**。其中 D10~D12 是把常说的「自我验证」拆开的三项（依据见 §0 第 2 条与 §2.1），
D13~D14 是 agent 工程能力，与模型单步能力正交。

### 1.2 维度表（定义与观察层）

「观察层」沿用 `04_verifier.md` 的 L0~L4 分层：
L0 硬门槛 / L1 程序化断言 / L2 几何或感知相似 / L3 VLM rubric / L4 组内 pairwise。

| # | 维度 | 定义（度量的到底是什么） | 主观察层 | 最适合的 verifier | 已知失效模式 |
|---|---|---|---|---|---|
| D1 | 指令遵循与规格覆盖 | 给定 N 条显式需求，产物满足几条。度量**覆盖率**与**严格全满足率**两个口径 | L1 | 需求编译成 checklist，逐条脚本或 judge agent 验（MTAC-IFBench 做法：code 验客观项、judge agent 验主观项） | 只看最终功能会漏掉过程约束：所有模型的 C-ISR 都远低于 F-ISR |
| D2 | 单次生成的视觉保真 | 给参考图（或参考页面），一次生成，产物渲染图与参考的差距 | L2 | Design2Code 细粒度四项（Block 面积 / Text Dice / Position / Color CIEDE2000）；多视角 DreamSim；按颜色体素 IoU | 像素/感知单独当 reward 必被 hack：极小 viewBox、把 prompt 文字画进图、DINO 饱和（`04_verifier.md` §5.1） |
| D3 | 开放审美与设计品味 | 无参考、只给需求，产物的设计质量。只能相对度量 | L4 | 组内 pairwise + rubric 树。Anthropic 四维（Design quality / Originality / Craft / Functionality），**每维设硬阈值而不是加权求和** | 人类不用 rubric 时一致率只有 65%，用 rubric 树后 92%（WebDevJudge 2510.18560 表 1、3）；rubric 措辞会引导审美收敛（Anthropic 原文 "museum quality"） |
| D4 | 布局与响应式 | 同一页面在多个视口宽度下布局是否不塌、不溢出、不横向滚动 | L1 | 多视口截图 + DOM 盒模型断言（元素是否越界、是否出现横向 scrollWidth > clientWidth） | 单视口截图完全看不到；GLM-5 在幻灯片 RL 里观察到「硬截断溢出内容」作为 hack 手段 |
| D5 | 可访问性 | 对比度、ARIA 语义、键盘可达、焦点顺序 | L0/L1 | axe-core / Lighthouse 规则引擎，**纯程序化**，不需要 judge | 这是全表唯一可以做成「零噪声硬闸」的维度；但规则通过 ≠ 真的可用 |
| D6 | 交互与状态逻辑正确性 | 做一个动作后，状态是否按契约改变 | L1 | 隐藏行为契约 + Playwright 脚本断言动作前后状态差分（WorldCoder-Bench、A2Z 的规则合同） | 只看源码的 judge 会被骗：WorldBench 删掉功能后纯代码 judge 仍给 5.44/7.11（2610.10622 表 5）；A2Z 中源码判满分的规则真玩只有 76.8% 成立 |
| D7 | 3D 空间推理 | 物体相对位置、朝向、尺度、层级、碰撞 | L1+L2 | three.js 读 scene graph（devtools hook）、Blender 读 bpy depsgraph，做结构化断言；复刻类加 Chamfer / 体素 IoU / Betti | 单张截图基本失效（本项目原型：雪人 6 候选页面截图分 0.973~1.0 分不开，按色体素 IoU 唯一全分开）；VLM 空间推理本身弱（BLINK：人 95.7%、GPT-4V 51.26%、随机 38.09%） |
| D8 | 动画与时间维度 | 运动是否由正确机制产生（物理 / 插值 / 状态机），而不是「某一帧看起来对」 | L1 | 固定时钟逐帧读状态（Playwright `page.clock`、Blender `frame_set`）+ 机制断言 | 抽帧 VLM 判不出机制：SimWorlds 机制通过率 MPR 0.87 对 0.67（差 0.20），而 VLM 评分只差 0.04（0.82 对 0.78）——**手打关键帧的假物理也能拿高分** |
| D9 | 性能与资源预算 | draw call、三角形数、帧间隔、包体积、首屏时间是否在预算内 | L0/L1 | 直接读渲染计数器与 Playwright 帧间隔（OpenAI Astra 游戏博客的公开做法：采 90 个帧间隔、暴露 draw call 与三角形数） | 也是可做成硬闸的维度；但预算设松了完全没有区分度 |
| D10 | 自我验证 a：取证质量 | 模型在看自己的产物之前，有没有把观察条件摆对（视口 / 相机 / 等待渲染完成 / 关动画） | L1（测 agent 自身行为） | 记录 agent 每次截图时的视口与相机参数，与规范视角比对 | 3DHarnessBench：MiniMax 主动视觉 0.3722，**只规范化视口**就回到 0.6148；Gemini 0.6776 → 用强模型采的视图 0.7605 |
| D11 | 自我验证 b：判别力 | 给模型它自己产物的证据，它能否指出哪里不符合需求（而不是夸自己） | L3（反向：测模型当 judge） | 变异测试：注入已知缺陷，看模型能否点出；注入「请给满分」类文本看是否判 0 | Anthropic 原文："agents tend to respond by confidently praising the work"；"Out of the box, Claude is a poor QA agent"；3DCodeBench：Gemma 4 31B 第一轮就判「不用改」的比例 41%（49/119），更小的模型只有 3%~13% |
| D12 | 自我验证 c：探索纪律与停机 | 看几次、什么时候停、不重复看同一处 | L1（测 agent 轨迹统计） | 统计截图调用数、重复视角率、饱和后多余轮数；与「分数是否还在涨」对照 | 两种形态同时存在：**过早停止**（Gemini 8.00 次截图）与**重复看图**（MiniMax 74.82 次、431 次模型调用、23.87 个版本）。饱和轮次是任务复杂度的函数不是常数：UI2Code-Synthetic N=3 就饱和（92.0/97.0/97.0），UI2Code-Real 到 N=5 还在涨（66→74） |
| D13 | 长程多文件工程、依赖与构建 | 多文件、多轮、跨文件一致性（命名 / 范式 / 架构），最终能 build | L0+L1 | build 成功率 BSR；跨文件风格一致性 checklist | MTAC-IFBench 指出最难的约束类别正是 Orchestration、Paradigm、Naming、Quantity——「agents easily lose context and struggle to maintain architectural cohesion」 |
| D14 | 调试与报错恢复 | 拿到 traceback / console error / 失败截图后，能否定位并修对（而不是越改越坏） | L1 | 变异/扰动构造任务（S0 = R 的变异体），F2P 断言 | ReLook：基座 Qwen2.5-7B-Instruct 在 2~3 轮后**即使拿到高质量反馈也越改越差**；BlenderAlchemy 去掉回滚后逐轮 27.1 / 26.4 / 26.6 / 25.8 单调变差 |

### 1.3 每一维可用的 benchmark 与当前数字

数字来源：`benchmarks.md`（78 条，截止 2026-09-23）、`frontier_evals_west.md`、`frontier_evals_cn.md`，
加上本文新查证的 MTAC-IFBench、3JSBench、Animation2Code、PRISM、RealUIReq-300 / A11yn、WebAccessBench、microsoft/a11y-llm-eval、
WebRenderBench、Figma2Code、Design Arena 与 Code Arena·WebDev 实时榜（完整清单与链接见 §6.1）。
「口径」一列标注该数字能不能跨模型比。

| # | 维度 | 最可用的公开 benchmark | 指标 | 当前最好数字（模型 / 日期） | 最好的开源数字 | 差距 |
|---|---|---|---|---|---|---|
| D1 | 指令遵循 | **MTAC-IFBench**（2609.14992，100 实例 / 9,133 约束 / 平均 7.04 轮）；WebCraftBench（2609.15387，369 需求 / 5,088 验收标准）；WebCoderBench（2601.02430，1,572 真实需求 / 24 指标） | CSR 约束满足率、C-ISR 严格全满足、F-ISR 功能严格全满足 | CSR **80.4**（GLM-5.2，开源）；F-ISR **37.0**（Claude-Opus-4.6，2026-09） | CSR 80.4、C-ISR 12.7（GLM-5.2）；F-ISR 29.0（GLM-5.1 / Kimi-K2.6） | CSR **开源反超 1.8 点**；F-ISR 闭源领先 8 点 |
| D2 | 视觉保真 | **Design2Code**（2403.03163，484 真实网页）；ChartMimic（2406.09961，4,800 三元组）；Image2Struct（2410.22456） | 相似度 ≥80 判通过（o4-mini 判分）；Design2Code 细粒度四项 | Design2Code **94.8**（GLM-5V-Turbo，闭源 API）；ChartMimic **82.2**（GPT-4o，2024-06） | Design2Code **93.4**（Qwen3-VL-235B-Thinking）；ChartMimic **80.5**（Qwen3-VL-235B） | **1.4 点 / 1.7 点，基本追平** |
| D3 | 开放审美 | **Design Arena**（designarena.ai，盲投 pairwise → BT，全站 181 万票；**唯一能拿到带服务端时间戳的官方数据**）；**Code Arena·WebDev**（原 WebDev Arena，官方站 Cloudflare 403，只能用镜像）；AUV-Bench（2609.34854，1,395 参考 UI，51 名专业设计师） | Elo / 设计师 1-5 分 MOS | **Design Arena allcategories（2026-10-15 直读）：claude-opus-5-5 Elo 1392（#1，胜率 63.8%，4,024 场）、gpt-6-astra 1379（#2，64.1%，8,297 场）**；Code Arena WebDev（镜像快照 2026-10-08）：**Opus 5.5 1813（#1）、GPT-6 Astra 1786（#2）** | Design Arena：**deepseek-v4-1-flash 1323（#14）**、kimi-k3 1363（#6）；Code Arena WebDev：**Qwen3.8-Max 1674**、Kimi K3 1654 | Design Arena **约 69 Elo**（1392 对 1323）；Code Arena WebDev **约 139 Elo**（1813 对 1674）。**口径：Elo 必须带快照日**（Code Arena WebDev 的 1786/1792/1793/1813/1815/1818 是同一指标的不同快照）；Arena 平局率 26%、约 18% 的票是「两个都差」 |
| D4 | 布局响应式 | 单视口布局：**Design2Code 四件套**（2403.03163）、**WebRenderBench**（2510.04097，纯 WebDriver 无 LLM，RDA/GDA/SDA）；响应式痕迹：**Figma2Code**（2604.13648，RUR 相对单位占比 / APR 绝对定位占比） | Block-Match / Position / RDA；RUR / APR | 单视口已近饱和：Design2Code **GPT-4o Block-Match 93.0 / Position 85.5**。响应式很差：**Figma2Code 视觉分最高的 GPT-5（VES 0.8405）响应式最差（RUR 仅 1.73、APR 高达 14.35）** | WebRenderBench **ALISA-Qwen2.5-VL-7B（RL）RDA 33.55 / GDA 60.28 / SDA 52.22，超过闭源**；Figma2Code RUR 最高是开源 ERNIE-4.5-424B-VL **4.81** | 单视口开源已反超。**真正的空白是「多视口一致性」**：用 6 组措辞检索过，没有任何公开 benchmark 做「同一份代码在多个视口宽度下分别渲染再比一致性」 |
| D5 | 可访问性 | **有专项 benchmark（修正：前面几篇笔记漏了）**：**RealUIReq-300 / A11yn**（2510.13914，300 条真实请求，axe-core 同时当 GRPO 奖励）、**WebAccessBench**（450 计分产物/模型）、**microsoft/a11y-llm-eval**（32 prompt×5，axe 零失败 + 手写断言双闸）、**A11YBench / A11YRepair**（2606.21926，60 项目 / 8,886 违规）、WebCoderBench 的 Accessibility 子分（权重 9.9%） | **IR_Axe = axe-core 加权违规分 / DOM 元素总数**（规模归一化，越低越好）；Lighthouse a11y 分；Violation Solve Rate | 前沿最好 **GPT-5.1：IR_Axe 0.13 / Lighthouse 92.69**；microsoft 口径（零失败 + 断言全过才算过）**无 a11y 指令时 GPT-5.4 Mini 仅 25%，8 模型均值约 11.9%** | **A11yn（Qwen2.5-Coder-7B + GRPO）IR_Axe 0.05 / Lighthouse 97.68，全面超过所有前沿模型**（相对基座 IR_Axe −87.5%）；A11YBench 修复 Kimi-K2.5 单轮 80.63%、多轮 87.49% | **开源 7B 经 RL 已全面反超前沿。** 这是全表「确定性 reward + RL 就能赢」最干净的一例。另一个杠杆是 prompt：加 "Building Accessible UI" skill 后 Gemini 3.1 Pro 从控制组水平升到 **96%** |
| D6 | 交互与状态逻辑 | **WebGen-Bench**（2505.03733，647 测试用例）；**Interaction2Code**（2411.03292，127 网页 / 374 交互 / 31 类）；WebIGBench（2606.00154，871 动作）；UI2App（2607.06306） | UI agent 跑测试用例通过率；IIS 交互推断分 | WebGen-Bench 最好闭源组合 **Bolt.diy + DeepSeek-R1 仅 27.8%**（2025-05） | **Qwen2.5-Coder-32B 用 WebGen-Instruct 训后 38.2%**（**反超闭源组合 10.4 点**） | 开源用对数据能反超。UI2App 的提示更尖锐：**视觉保真第一的模型 IIS 只有 7.5，IIS 第一名是它的 5.2 倍；跨页状态上一半模型得 0 分** |
| D7 | 3D 空间推理 | ⭐**3JSBench**（3jsbench.com，100 道 three.js 题 ×3 rollout，**743 条确定性几何检查、28 种 kind，纯几何内核无 LLM**；数据 rev 2026-10-14）；**WorldCoder-Bench**（2606.01869，2,026 题，StateProbe 隐藏契约）；**BenchCAD**（2605.10865，17,900 CadQuery 程序，确定性打分无 LLM judge）；BlenderGym（2504.01786，245 场景）；3DHarnessBench（2609.06535） | 几何检查通过率；V-Cov 隐藏断言通过比例；voxel IoU | **3JSBench：GPT-6 Astra 80.00%（240/300，tasksAllPass 57/100）对 Claude Opus 5.5 49.00%（147/300，23/100）** —— 这是本文找到的**唯一能把两个目标模型放进同一个确定性 verifier 的公开集，而且前沿之间就差 31 个点**。WorldCoder-Bench 最好 GPT-5.4 **Core 27.8 / Robust 19.9**；BenchCAD 带工具 **95.9%**（Astra）、Opus 5 **0.821** | 3JSBench：**Kimi K3 23.00%**、GPT-6 Sol 27.00%、Grok 4.7 22~23%、Gemini 3.8 Flash 8.67%；WorldCoder-Bench **Qwen3.6-Plus 25.3**（距 GPT-5.4 仅 2.5 点）；BlenderLLM Iter3 Sim **0.748** 超 o1-Preview 0.687 | **三个集给出三种结论**：3JSBench 差距巨大（80 对 23），WorldCoder-Bench 差距很小（27.8 对 25.3），BenchCAD 国内零报分。**别用 CLIP / SigLIP 当 3D 质量闸**：3JSBench 的 3,000 次尝试实测，10 个模型的 SigLIP prompt 相似度全落在 **0.0774~0.1081** 的窄带里（Astra 0.1081、Opus 5.5 0.1067、inkling 0.0774），区分度≈0 |
| D8 | 动画与时间 | ⭐**Animation2Code**（2606.28593，214 测试题 / 1,069 条网页动画视频，86% 纯 CSS；headless Chromium 1024×768@30fps 确定性渲染，与人类偏好一致约 83.9%）；**PRISM**（2605.19382，确定性坐标检查，刻意不用 VLM）；ManimBench（2604.18364）；SimuScene（2602.10840）；4DBuildBench / SimWorlds（2607.01766，引擎状态审计） | **Appearance = DreamSim 嵌入 + DTW 对齐**；**Temporal = CoTracker3 在 30×30 网格抽 tracklet，位移方向 cos + 幅值 min/max 比，Chamfer 式最大匹配**；PRISM 的 Spatial Pass = 渲染成功且审计帧无 overlap / out-of-bounds / leakage | **Animation2Code：Appearance 最高 GPT-5.4 0.84，但 Temporal 最高只有 Gemini 3 Flash 0.31** —— 时间维度是全行业最弱的一格。PRISM：Exec 最高 GPT-5.4 **0.945**，但 **Spatial 最高 Gemini 3.1 Pro 0.572**，Exec→Spatial 平均掉 **41.24 点**（95% CI [40.41, 42.11]） | Animation2Code **Qwen3-VL-8B + 迭代 0.73 / 0.28**（Temporal 只差 0.03）；ManimBench **Qwen3-Coder-30B-A3B + GRPO + RITL 94% / 85.7%，全场最好**；SimuScene **RL 后 32B 72.2% Pass@8**（最强闭源 Avg@8 只 21.5%）；PRISM GLM-5 0.720 / 0.341 | **开源 + 专项 RL 在这一维已反超**。两个必须记住的事：① **Temporal 天花板只有 0.31**，这一格空间最大；② **「能执行」到「空间正确」平均掉 41 个点**，只报执行率的指标没有信息量 |
| D9 | 性能与资源预算 | 没有公开 benchmark。可用的公开做法：OpenAI Astra 游戏博客（采 90 个帧间隔、暴露 draw call 与三角形数） | — | — | — | **必须自建**，成本极低（直接读计数器）。见 §4.6 |
| D10~D12 | 自我验证三项 | **3DHarnessBench**（2609.06535，四层级权限）；**BenchCAD 带工具 / 不带工具**；PlaytestArena（2605.28258）；GameDevBench（2602.11103） | 同一任务在不同观察权限下的分差 | 见 §2.1 证据 A~E | 见 §2.1 证据 F~K | **本文结论：这一维不是开源与前沿的主要差距所在**（同 harness 短程多轮只差 1.0 点；迭代 harness 弱模型获益更多）。但在**视觉 / 前端子域**差距要大一些（FronTalk AceCoder：GPT-4o +9.3 对 Qwen2.5-VL-72B 视觉档 +0.8） |
| D13 | 长程多文件工程 | **Vibe Code Bench**（2603.04601，100 规格 / 964 工作流 / 10,131 子步骤）；JAMER / JamBench（2606.19830，300 游戏引擎项目）；GameEngineBench（2607.03525，110 UE5 任务） | 浏览器 agent 走查工作流 accuracy；SCS 结构完整度 / BAS 行为对齐 | Vibe Code Bench v1.1 实时榜（vals.ai，2026-10-12）：**Claude Sonnet 5.5 92.39%**、Gemini 4 Argon 91.91%、Haiku 5.5 90.44%、Fable 5 90.35%、**Opus 5.5 90.29%**、**GPT-6 Astra 89.59%**、Opus 5 88.40%（均 OpenHands harness） | **MiMo V2.6 Pro 85.22%**、**Kimi K3 84.97%**（官方描述为「首个进入第一梯队的开源权重模型」）、DeepSeek V4.1 Flash 84.74%、GLM 5.3 78.13%、Qwen 3.8 Max 64.70% | **约 7 个百分点**（92.39 对 85.22）。规模衰减是真问题：JAMER 运行通过率**从小项目 80.4% 跌到大项目 5.7%**，作者结论「瓶颈在架构设计，不在语法」；Vibe Code Bench 接入外部服务（Stripe / 邮件）**从 71% 掉到 30%** |
| D14 | 调试与报错恢复 | **SWE-bench Multimodal**；GameDevBench（2602.11103，333 Godot 任务）；GBQA（2604.02648，124 人工确认 bug）；CADEngBench（2608.09296，FEA 验证） | pass 率；bug 发现率 | SWE-bench MM **70.21% ±2.09**（Claude Opus 5.5）对 **43.33% ±2.26**（GPT-6 Astra）【vals.ai 二手】；Opus 5 自报 **59.4%**（内部 harness，5 次平均）；GameDevBench 最佳 agent 约 **54%**（2D 图形类只 31.6%）；GBQA 最好模型找到 **48.39%** 的 bug。Deloitte 一手：**Opus 5.5 在最低 effort 下抓到 72% 的已知 bug，Opus 5 在 high effort 下只有 56%** | SWE-bench MM **38.6**（Qwen3.8-27B，Claude Code harness，公开 dev split） | **约 21 点**，是全表除 D13 外差距最大的一维 |

### 1.4 口径警告（不照抄就会算错差距）

1. **harness 是能力的一部分，不是中性容器。** MTAC-IFBench 同一个 GLM-5.2，Claude Code 下 CSR 80.4 / C-ISR 12.7，换 OpenCode 变成 76.8 / **6.7**（C-ISR 腰斩）。比较模型必须锁定 harness 并写进报告。
   更直接的例子在 Vibe Code Bench 实时榜上：**同一个 Claude Opus 4.8，OpenHands harness 82.72%、Claude Code harness 77.48%**（差 5.2 点）；
   GPT-5.5 在 OpenHands 69.85%、Factory 67.39%、Codex 58.19%（**差 11.7 点**）
2. **带工具与不带工具的分不能混。** BenchCAD 上 Opus 5 不带工具 0.366、带工具 0.821
3. **同一模型同一 benchmark 跨页面数字不一致是常态。** 例：Opus 5 的 OSWorld 2.0 有 70.6 / 70.2 / 75.4 三个数；GPT-5.6 Sol 的 BenchCAD 有 83.4% / 83.3%
4. **judge 换人会翻排名。** MermaidSeqBench 原文结论就是「排名随判官翻转」。任何 LLM-as-judge 维度，报分必须附带 judge 型号
5. **像素指标选错会把结论做反。** SVG-Bench 原论文：MSE 衡量不了 SVG 质量

### 1.5 两个常被当成一维、实际必须拆开的地方

**① 「视觉保真」(D2) 与「3D 空间推理」(D7) 的度量方向相反**
- CLIP / DINO 对平移、缩放不变，这正是 to-code 任务要抓的差异 → 这类指标在 D2 上是缺陷
- UI2Code^N 直接拿 CLIP 当 reward，效果**低于**纯 SFT（2511.08195 §4.3）
- D7 要的是朝向与相对位置，而感知指标对朝向（翻转）恰好不敏感（DreamSim 的已知盲区）

**② 「自我验证」不能和「VLM judge 准确率」混为一谈**
- D11 测的是模型**对自己产物**的判别力，受自我偏好污染：GPT-4 对自家回答「判赢」召回 0.945、「判输」只有 0.425（2410.21819）
- 所以 D11 的 verifier 必须用**不同家族**的模型，或者用注入已知缺陷的变异测试，不能让模型自评

---

## 2. 差距定位：开源在哪儿追上了，差距最大的是什么

### 2.1 核心命题：「自我验证 / 迭代修正」是不是主要差距来源

**结论：不是。**

这是本文做过最大的一次结论翻转，所以把推理过程完整留下。
- **证据 A~E**（下）确实显示「放开自我验证 / 观察权限」能带来巨大增量 —— 这部分是真的
- 但**证据 F~K** 显示这个增量**不是前沿模型独享的**，而且**增益与单步能力负相关**（弱模型拿得更多）
- 修正后的表述：
  > **自我验证是整个领域共同的、尚未解决的瓶颈（能力上界 98% 对实际取到 41%）；
  > 前沿模型的相对优势更多来自「单步质量 + 长程持久性与时间校准 + 同轨迹一致性」，
  > 而不是来自「更会自己检查自己」。**
- 对复刻的含义：**循环仍然该做，而且对我们收益最大**（因为我们单步基线更低），
  但不能把它当成「追平前沿」的全部答案，也不能把「循环增益倍数」当 KPI

#### 证据 A：同一模型、同一任务，只改「能不能自己验」——BenchCAD 带工具 / 不带工具

BenchCAD（arXiv 2605.10865）的厂商自报分同时给了带工具和不带工具两档。
带工具就是允许模型执行代码、看渲染结果、改了再看；不带工具是一次性写完。

| 模型 | 不带工具 | 带工具 | 增量 | 倍数 |
|---|---|---|---|---|
| Claude Opus 5（voxel IoU，1000 子集，5 次平均） | **0.366** | **0.821** | +0.455 | **2.24×** |
| Mythos 5 | 0.379 | 0.650 | +0.271 | 1.71× |
| Claude Opus 4.8 | 0.277 | 0.521 | +0.244 | 1.88× |
| Mythos Preview | 0.356 | 0.610 | +0.254 | 1.71× |
| GPT-5.6 Sol（OpenAI 口径，百分比） | 70.6% | 83.4% | +12.8 点 | 1.18× |
| GPT-5.5 | 44.4% | 55.8% | +11.4 点 | 1.26× |
| Mythos 5（OpenAI 口径） | 38.4% | 65% | +26.6 点 | 1.69× |
| Claude Opus 4.8（OpenAI 口径） | 27.3% | 51.8% | +24.5 点 | 1.90× |

- **Opus 5 的单步生成能力只值 0.366，带上「自己跑、自己看、自己改」的循环后到 0.821 —— 循环贡献了 45.5 个点，占最终分的 55%。**
- 两家口径不同（OpenAI 记 geometric overlap 百分比，Anthropic 记 voxel IoU），但**倍数的方向和量级一致**
- 注意：这两列不能跨厂商直接比，但**同一行的两列是同一套测法**，所以倍数是可信的
- **但倍数与单步基线负相关**（这一列是整张表最该看的）：
  OpenAI 口径下 GPT-5.6 Sol 单步 70.6% 只换来 **1.18×**，Opus 4.8 单步 27.3% 换来 **1.90×**。
  单步越强，循环的边际收益越小 —— 见 §0 第 2 条。所以本表**不能**读成「前沿靠循环赢」

#### 证据 B：同一能力、同一任务，只改「观察权限」——3DHarnessBench 四层级

3DHarnessBench（arXiv 2609.06535，2026-09）把同一组任务按模型能看到多少分四档（Uni3D 分数）：

| 模型 | 单视角 | 多视角 | 主动视觉 | 完整 3D 交互 | 多视角→主动视觉 |
|---|---|---|---|---|---|
| **Qwen 3.8 Max**（阿里；Max 档是否开权重未核实） | **0.740（全场第一）** | 0.768 | 0.809 | 0.857 | +5.3% |
| Claude Opus 5 | 0.725 | 0.748 | **0.871** | **0.927** | **+16.4%** |
| Fable 5 | 0.733 | 0.764 | 0.832 | 0.884 | +8.9% |
| GPT-5.6 Sol | 0.715 | 0.745 | 0.823 | 0.879 | +10.5% |
| Kimi K3（开源） | 0.678 | 0.713 | 0.819 | 0.848 | +14.9% |
| Gemini 3.1 Pro | 0.728 | 0.753 | **0.691（退步）** | 0.783 | **−8.2%** |
| MiniMax M3（开源） | 0.495 | 0.577 | **0.482（退步）** | 0.679 | **−16.5%** |

四条读数：
1. **单视角档 Qwen 3.8 Max（0.740）高于 Claude Opus 5（0.725）**；确定开权重的 Kimi K3 是 0.678，与 Opus 5 差 4.7 个点 —— 单步 3D 视觉能力差距很小
2. 一放开主动取景，排名重排，Opus 5 跃到第一
3. 差距被放大（原文数字，已核对 arXiv 2609.06535 §4）
   - Uni3D 的「最弱 → 最强」差距：单视角 33.1%、多视角 24.9%、**主动视觉 44.7%**、完整 3D 交互 26.8%
   - Chamfer 的「最差 / 最好」比值：固定视角约 **2 倍** → 主动视觉 **8.5 倍**（放大 4.25 倍）
   - 原文的定性结论：**"Active Visual is therefore the sharpest discriminator: additional access helps some agents but hurts others"**
4. 退步不是 3D 推理不行，是取证和纪律不行（见下）

#### 证据 C：退步的真因可以被拆成三项（取证质量 / 取景选择 / 停机纪律），每项都能单独修

这是全篇最有操作价值的一组消融（同上，3DHarnessBench）：

原表（3DHarnessBench 表 3，Active Visual 档，10 个实例，Uni3D）：

| 模型 | 多视角（参照） | 主动视觉 | ① 规范化视口 | ② 用 Fable 5 采集的检视图 |
|---|---|---|---|---|
| Gemini 3.1 Pro | 0.7609 | 0.6776 | 0.7321 | **0.7605（基本回满）** |
| MiniMax M3 | 0.6200 | 0.3722 | **0.6148（基本回满）** | 0.4899 |

**这张表最关键的一点是两个模型被不同的干预治好：**
- MiniMax 的病是**取证质量**（截图时视口没摆对）→ 规范化视口就回满，给它好视图只救回一半
- Gemini 的病是**取景选择**（选错了看哪里）→ 换成强模型采的视图才回满，规范化视口只救回一半
→ 「自我验证」确实要拆成多项来治，一刀切的「多给它看几眼」不管用

**取证调用预算（同一档位，原文表 7 与附录，已核对）**

| 模型 | 看目标（inspection） | 看自己的产物（comparison） | 合计 | 形态 |
|---|---|---|---|---|
| Gemini 3.1 Pro | 5.42 | 2.58 | **8.00** | 过早停止 |
| GPT-5.6 Sol | — | — | 25.73 | 正常 |
| Claude Opus 5 | — | — | 26.15 | 正常（但输出 token 更多） |
| MiniMax M3 | 31.71 | 43.11 | **74.82** | 重复看图 |

MiniMax 在主动视觉档平均 **431 次模型调用、156 次 MCP 调用、23.87 个重建版本**，延迟也最高。
原文结论：**"a successful Active Visual agent must not only interpret observations correctly, but also learn when and how to acquire informative, high-quality observations"**

→ **弱模型在自主循环上的损失，几乎全部可以归因到「取证质量」「取景选择」「停机纪律」这三项行为，而不是视觉理解或空间推理。**
→ 这两项都是**纯行为**，恰好是 RL 环境最擅长训的东西。

#### 证据 D：加视觉反馈循环的增益，在多个任务族上重复出现

| 来源 | 设置 | 数字 |
|---|---|---|
| GameDevBench（2602.11103） | 给 Sonnet 4.5 加图像 / 视频反馈 | 33.3% → **47.7%**（+14.4 点） |
| PlaytestArena（2605.28258） | Play2Code（写码与试玩循环）对单次生成 | rubric 通过率 66.8%，**高 37.1 点** |
| VIGA / BlenderBench（2601.11109） | 交错多模态推理 + 迭代写 Blender 代码 对 one-shot | **+124.70%** |
| Code2Video / MMMC（2510.01174） | 相对直接写码 | **+40%** |
| ScreenSpot-Pro（2504.07981） | ScreenSeekeR（不训练，只加搜索式取证） | 18.9% → **48.1%**（+29.2 点） |
| CADCodeVerify（2410.05340） | GPT-4 加自问 Yes/No 的 4 视角验证 | 点云距离 −7.30%、成功率 +5.0% |
| ReLook（2510.11498） | Forced Optimization（只接受严格变好的修改） | ArtifactsBench-Lite 25.84 → **27.88**（+2.0） |

#### 证据 E：反面证据 —— 循环不是白送的，弱模型加循环会变差

这组必须一起看，否则会得出「加循环就行」的错误结论：

| 来源 | 现象 |
|---|---|
| 3DHarnessBench | Gemini −8.2%、MiniMax −16.5%（见证据 B） |
| ReLook（2510.11498） | 基座 Qwen2.5-7B-Instruct 在 2~3 轮后**即使拿到高质量反馈也越改越差** |
| BlenderAlchemy（2404.17672） | 去掉回滚后逐轮 27.1 / 26.4 / 26.6 / 25.8，**单调变差**；深度×宽度 32 次调用，1×32 和 32×1 两头都最差，8×4 最好 |
| 3DCodeBench（2606.01057 附录 D.2） | 视觉自我批评在 **image-to-3D 上 ΔSigLIP −0.006~−0.009**（胜负比 0.58~0.78），text-to-3D 才是正的 |
| 1D-Bench（2602.18548） | 迭代编辑能提高渲染成功率，但**后训练收益有限且不稳定** |
| 3DCodeBench | 弱 critic 过于激进：Gemma 4 31B 第一轮就判「不用改」41%（49/119），更小模型只 3%~13%；回滚比例 31B 11%、小模型 26%~28% |

→ **「能开循环」和「循环有正收益」是两件事。后者需要 ① 回滚机制 ② 单调改进约束 ③ 停机判据。这三样都是环境设计，不是模型大小。**

#### 证据 F：同 harness 的短程多轮 agentic，开源与前沿差 1 个点

SWE-bench 官方 leaderboard 的 **Bash Only 视图**（所有模型跑同一个 mini-SWE-agent v2.0.0，
Attempts=1，即多轮轨迹的 pass@1），快照 2026-02-17，https://www.swebench.com/

| SWE-bench Verified（500 题） | 分数 | 权重 |
|---|---|---|
| Claude 4.5 Opus | **76.8** | 闭源 |
| Gemini 3 Flash | 75.8 | 闭源 |
| **MiniMax M2.5** | **75.8** | **开源** |
| Claude 4.6 Opus | 75.6 | 闭源 |
| **GLM 5** | 72.8 | **开源** |
| GPT 5.2 / GPT 5.2 Codex | 72.8 | 闭源 |
| **Kimi K2.5** | 70.8 | **开源** |
| **DeepSeek V3.2** | 70.0 | **开源** |

最强闭源 76.8 对最强开源 75.8，**差 1.0 个点**。
SWE-bench Multilingual（300 题，9 语言，2026-02-13）：Gemini 3 Flash 72.7 对开源 GLM 5 **69.7**，差 3.0 点。
→ **锁定同一个带执行反馈的多轮 harness 之后，「自主循环」不构成护城河。**

#### 证据 G：迭代 harness 的收益，弱模型拿得更多（方向性反证）

AutoLab（arXiv 2606.05080，2026-06-03；36 个 2~12 小时任务，统一 terminus-2 harness，2,544 机时）§4.3 的 harness 消融：

| 模型 | 轻量 harness（pi-mono） | 强迫持续迭代（mini-swe-agent*） | 变化 |
|---|---|---|---|
| gpt-5.4（强单轮推理） | 0.50 | 0.47 | **−0.03** |
| mimo-v2.5 | — | — | **+0.20** |
| deepseek-v4-flash | — | — | **+0.13** |
| kimi-k2.6 | 0.21 | **0.64** | **+0.43** |

- 同一模型换 harness，均值最多偏移 **Δ=0.43**（kimi-k2.6）—— harness 诱发的方差可与模型诱发的方差相当
- **排名非传递**：pi-mono 偏爱 gpt-5.4，mini-swe-agent* 偏爱 kimi-k2.6
- 原文结论：**"the iterative harness let the agent recover through trial-and-error what a strong single-shot reasoner would solve in one pass;
  models weaker at one-shot reasoning therefore gain the most"**，并直说精调 harness
  **"could close a substantial portion of the performance gap between weak and strong base models without any changes to the underlying models"**

同向的历史数据：SWE-agent（arXiv 2405.15793，2024-05）表 2，从 RAG 单次生成换到带执行反馈的多轮 agent，
**GPT-4 Turbo 1.31 → 12.47（9.5 倍），Claude 3 Opus 3.79 → 10.46（2.8 倍）** ——
RAG 档 Claude 3 Opus 赢 GPT-4T 2.9 倍，换到循环里**反而输 19%，排名直接翻转**。

#### 证据 H：前沿 agent 其实根本不做自我验证

VISTA（arXiv 2605.26144，v4 2026-09-29；18 个应用，8,487 个人工标注组件）的轨迹审计：

| 现象 | 比例 |
|---|---|
| 完全跳过 prompt 明确要求的 self-audit | **73.0%** |
| 从没打开过设计截图 | **44.5%** |
| 没读结构 JSON | 20.9% |
| 验证不完整 | 27.2% |
| **检查失败后仍报告成功** | **8.3%** |
| 交付的 web 产物里有无响应控件（外部探针） | **90.1%** |

EDIT→VERIFY 的转移概率：**Codex 37.2%，Cursor 7.5%，Claude Code 9.5%** —— 又是一条「harness 比模型更决定行为」的证据。
Web 联合分最高 Grok 4.6 (Cursor) 0.553、Fable 5 0.533、Opus 4.8 0.487；Mobile 最高 GPT-6 Astra (Codex) 只有 **0.378**。

→ 【推断】七成以上的前沿轨迹压根没做自我验证，所以前沿优势**不可能主要来自自我验证**。

#### 证据 I：朴素视觉自我验证，在前沿模型上也是净负收益

| 来源 | 设置 | 数字 |
|---|---|---|
| **RubSE**（arXiv 2608.24138，2026-08） | 15 轮朴素视觉自演化 | **GPT-5.2 在 Design2Code 上全部 15 轮都低于第 0 轮，终点 −2.73**；GPT-5.4 第 1 轮 +0.76 后掉到 −1.82，15 轮里 10 轮低于初始。机制命名为 **"visual repair coupling"**：一次局部修复破坏原本正确的区域 |
| **VisRefiner**（arXiv 2602.05998，2026-02） | 单步 → 自修正后 AVG | GPT-4o Design2Code 90.2 → **89.9（−0.3）**；Claude 3 Opus 84.8 → **84.6（−0.2）**；Qwen2.5-VL-7B 85.4 → **84.9（−0.5）**。多轮更糟：Qwen2.5-VL-7B turn0 87.5 → turn1 86.8 → turn3/5 **86.6，单调下降**。原文判语：**"refinement is not reliably activated in general-purpose vision-language models"** |
| **FronTalk**（arXiv 2601.04203） | 加视觉反馈 | GPT-4o 多轮文本 56.0 → **多轮视觉 55.0（反而降）**；**开源 VLM 普遍为负：Qwen2.5-VL-72B −8.2、Qwen3-VL-30B −15.0、GLM-4.5V −27.3** |
| **DCGen**（arXiv 2406.16386） | GPT-4o Self-Refine | CLIP 83.96 对 Direct 83.72（**+0.24**）；Design2Code-Hard **−0.61**；Gemini-2.0-flash **−0.2** |
| **Self-Debug**（arXiv 2304.05128） | 去掉 unit test | GPT-3.5 TransCoder 89.1 → 89.1（三种变体全零变化）；Codex MBPP 61.4 → **57.6（倒退）**。原文：**"Without unit test execution, both models tend to be overconfident in their own initial predictions"** |

**真正有效的三条路都不是「自己看自己」**：

| 路径 | 数字 | 来源 |
|---|---|---|
| **外部更强模型做视觉 critic** | best-of-3-cycles **+17.8%**；**无 critic 的纯自我 refine 只 +1.5%** | CITL，arXiv 2604.05839（2026-04） |
| **执行 + 渲染回灌 + 局部编辑工具** | IWR-Bench：Kimi-K2.6 55.61 → **65.85（+10.24）**；Qwen3.5-9B 微调版 42.78 → **57.52（+14.74）**。消融：去执行反馈 **−3.22**，改整页重生成 **−4.82** | RILA，arXiv 2609.02088（2026-09） |
| **用视觉奖励训练修正能力**（不是 prompt 它） | UI2Code-Real N=1 66.0 → N=5 **74.0**；VisRefiner SFT+GRPO 把 base 87.5 → **92.0**，多轮 92.0→92.5→**92.9** | UI2Code^N 2511.08195；VisRefiner 2602.05998 |
| **SCoRe：用 RL 直接训自修正** | Gemini 1.5 Flash 的 MATH self-correction delta 从 **−11.2% 推到 +4.4%**（改善 15.6 点）；同设定下 Self-Refine 只有 −1.0% | arXiv 2409.12917（2024-09） |

→ **自修正是可以被训出来的能力，不是模型规模的自动产物。** 这一条是本文对复刻最重要的技术判断。

#### 证据 J：自我验证瓶颈是普遍的，不是开源独有 —— 「采样覆盖 vs 自我选择」的缺口

| 来源 | 能力上界（有 oracle / 足够采样） | 自我验证实际取到 | 缺口 |
|---|---|---|---|
| **Large Language Monkeys**（arXiv 2407.21787） | Llama-3-8B-Instruct 在 MATH 上 coverage **98.44%**（10k 样本） | majority voting / RM 选择只从 40.50% 到 **41.41%** | **57 个点** |
| **Agentless**（arXiv 2407.01489） | SWE-bench Lite oracle 选择 **42.0%** | 自己生成 reproduction test 选出 **32.0%** | **10 个点** |
| **BouncerBench**（arXiv 2506.17812） | — | 对错误 patch 的召回：codex 61.0%、o4-mini 46.2%、**claude-3.7-sonnet 7.9%**、gemma3-27b 3.2%。**非 reasoning 模型 O-Score 为负，即差于随机** | — |
| **BIG-Bench Mistake**（arXiv 2311.08516） | 给 oracle 错误位置做 backtracking，五个任务全部净增益 | 找错误位置的准确率：GPT-4 **52.87**、PaLM 2 Unicorn 23.67、GPT-3.5-Turbo **14.78（≈乱猜）** | 瓶颈在**定位错误**而非**修正错误** |
| **GPT-4 图着色**（arXiv 2310.12397） | 换 sound verifier **≈40%** | GPT-4 自验 backprompt **1/100（≈1%，比 16% 的直接生成差 15 倍）**；40 个实例过程中确实生成过最优解，**verifier 一次都没认出来** | — |

Large Language Monkeys 原文的结论就是本节的标题：
**"Equipping models with the ability to assess their own outputs will allow repeated sampling to be scaled to far more tasks."**

#### 证据 K：前沿的代际跃升同时发生在「完全没有循环」的设定下

这是对「循环论」最强的一条反证。
GPT-6 Astra system card（https://deploymentsafety.openai.com/gpt-6-astra，2026-09）里 UK AISI 的测量：

| 设定 | GPT-6 Astra | GPT-5.6 Sol | 倍数 |
|---|---|---|---|
| **no-CoT 50% 可靠性时间跨度** | **30.9 分钟** | **3.6 分钟** | **约 8.6 倍** |
| CoT 遵守约束 | 93% | 48% | — |

卡里原话：**"the no-CoT time horizon may have increased by about an order of magnitude"**。
**禁用思维链、禁用循环的单次前向，代际提升接近一个数量级。**

#### 本命题的最终归因（【推断】）

把「差距来源」按公开证据的支持强度排序：

```
单步推理 / 生成质量            ≳  长程持久性与时间预算校准
（Astra no-CoT 8.6×）             （AutoLab 0.68 对 0.46；METR 50% horizon 12h 对 80% horizon 1.5h，8 倍落差）
        >  验证与判别能力                    >  多轮执行反馈循环本身
           （ProcessBench −16.4、Hard2Verify −8.4，           （SWE-bench 同 harness 差 1.0 点，
             但 RewardBench 2 只 −0.5、RuVerBench 只 −2.5）      且弱模型从循环中获益更多）
```

### 2.2 哪些维度开源已经接近（说明训练已经解决）

| 维度 | 证据 | 判断 |
|---|---|---|
| D2 视觉保真 | Design2Code：Qwen3-VL-235B-Thinking **93.4** 对 GLM-5V-Turbo 94.8（差 1.4）；ChartMimic：Qwen3-VL-235B **80.5** 对 GPT-4o 82.2（差 1.7） | **已追平**。预训练「代码 ↔ 渲染图」配对是公开共识做法，继续投性价比低 |
| D1 单轮指令遵循 | MTAC-IFBench CSR：GLM-5.2 **80.4** > Opus-4.6 78.6 | **已反超** |
| **短程多轮 agentic（跨 D13 / D14 的通用部分）** | SWE-bench Verified 官方 Bash Only 同 harness：MiniMax M2.5 **75.8** 对 Claude 4.5 Opus **76.8**，差 1.0 点；SWE-bench Multilingual GLM 5 **69.7** 对 Gemini 3 Flash 72.7，差 3.0 点；Terminal-Bench 2.0 第三方聚合（口径需打折）**Qwen3.7 Plus 70.3% 反超 Claude Opus 4.7 (Adaptive) 69.4%** | **已基本追平**。这是「自主循环不构成护城河」的主证据 |
| 判别力的部分口径 | RewardBench 2：gemini-2.5-flash 77.2 对开源 QRM-Gemma-27B **76.7**（差 0.5）；RewardBench 1 Reasoning 子项开源专用 RM **ArmoRM-8B 97.3 反超 gemini 92.0**；RuVerBench deep research：Gemini-3.1 Pro 94.7 对 Kimi K2.6 **92.2**（差 2.5） | **分水岭是「推理型 vs 非推理型」而不是「开源 vs 闭源」**：JudgeBench 上开源 DeepSeek-R1 **73.14** 远高于闭源 GPT-4o 56.57、Gemini-1.5-pro 47.14 |
| D8 动画与时间 | SimuScene：最强 LLM 仅 21.5% Avg@8，**RL 后的 32B 达 72.2% Pass@8**；DCG-Bench 自研 3B 专家 +8.31%；VAnim 对齐 0.281 > Gemini3 Pro 0.243 | **开源 + 专项 RL 已全面反超**。证明「有环境就能赢」 |
| D6 交互逻辑（数据可解部分） | WebGen-Bench：Qwen2.5-Coder-32B 用 WebGen-Instruct 训后 **38.2%**，反超 Bolt.diy+DeepSeek-R1 的 27.8% | **数据可解**。但 UI2App 显示跨页状态一半模型得 0 分，说明只是局部解决 |
| **反例：全栈视觉建站开源几乎为零** | Vision2Web（2603.26648，193 任务 / 918 原型图 / 1,255 测例）L3 全栈：Claude-Opus-4.5 **48.0**，而 Gemini-3-Pro 只 17.2、Claude-Sonnet-4.5 20.4；**开源 VLM 几乎全线 0（Qwen3-VL-32B L1 得 0.0，部署成功率 4%）** | **这一档没追平**，而且连闭源内部差异都极大（48.0 对 17.2） |
| 窄域专项（SVG / 图表 / 海报 / 教学动画） | UniSVG、InternSVG、VectorGym（8B 超 Qwen3-VL-235B、与 GPT-4o 持平）、JanusCoder（7~14B 逼近商用）、AutoPresent（8B ≈ GPT-4o）、Paper2Poster（Qwen2.5 版超 GPT-4o 多 agent，省 87% token） | **一旦任务窄到有确定性 verifier，小模型就能打平前沿**。这是全表最一致的规律 |

### 2.3 差距最大的维度（按差距大小排序）

| 排名 | 维度 | 差距证据 | 为什么难追 |
|---|---|---|---|
| 0 | **（已修正）自我验证三项不排第一** | 见 §2.1 证据 F~K：同 harness 短程多轮差 1.0 点；迭代 harness 弱模型获益更多；73.0% 前沿轨迹跳过 self-audit；朴素视觉自修正在 GPT-5.2 上 15 轮全负 | 它是全行业瓶颈（能力上界 98% 对实际 41%），仍然必须做，但不是「追平前沿」的那块短板 |
| 1 | **长程持久性与时间预算校准**（跨 D12 / D13） | AutoLab 36 个 2~12 小时任务：claude-opus-4.6 Avg@3 **0.68** 对最强开源 kimi-k2.6 **0.46**（差 48%）；METR 2026-05 风险报告：公开前沿 **50% 时间跨度约 12 小时，80% 跨度只有约 1.5 小时（8 倍落差）**；**只在开源模型上出现的失效模式**：进入极长推理链烧光预算只发几个动作（deepseek-v4-pro 在 CUDA 子集 12 次 trial 里 9 次提交不到 10 个动作就超时） | **不是开源 / 闭源分界，是模型个体属性**（闭源 gpt-5.4 只有 0.36，排在四个开源模型之后）。失效形态是双向的：有的过早提交、有的耗尽预算从不提交 |
| 2 | **D13 长程多文件工程** | Vibe Code Bench v1.1（2026-10-12）：闭源最高 **92.39%**（Sonnet 5.5）对开源最高 **85.22%**（MiMo V2.6 Pro）、Kimi K3 84.97%，**差约 7 点**；JAMER 小项目 80.4% → 大项目 **5.7%**；MTAC-IFBench 多轮衰减 Opus −6.2 点对 Qwen3.5-27B −17.8 点；外部服务接入 71% → 30% | 需要 20 万量级的真实环境（MiniMax M2.5 口径），以及 harness 本身的工程（同模型换 harness C-ISR 从 12.7 掉到 6.7） |
| 3 | **D14 调试与报错恢复** | SWE-bench MM：Opus 5 **59.4** 对 Qwen3.8-27B **38.6**（差约 21 点）；GameDevBench 2D 图形类只 31.6%；GBQA 最好模型只找到 48.39% 的 bug | 「不越改越坏」要轨迹级 reward；ReLook 证明罚退步会让模型学会少反思 |
| 4 | **D7 3D 空间推理（公开数据缺失）** | BenchCAD / BlenderGym / 3DCodeBench **国内与开源零报分**；唯一可比的 Kimi K3 自建集 3D/WebGL/Shader 子项反而 +59.1 胜 Opus 4.8 | 不是能力差距已证实，是**测不出来**。先建测法比先提能力重要 |
| 5 | **D3 开放审美** | WebDev Arena：闭源最高 1793（Astra）对开源最高 1678~1691，**约 100~115 Elo** | 需要偏好数据与专用 RM；但 AesCoder 证明 4B 加 agentic reward 能从 0.62 打到 1.04，说明**不是规模问题** |
| 6 | **D5 可访问性 / D9 性能预算** | **零公开 benchmark** | 不是差距，是空白。自建成本最低（确定性规则引擎），应该最先做 |

---

## 3. 可复刻性评估：每一维靠什么训

四类手段，从便宜到贵：
- **SFT 可得**：有参考解或可筛选的轨迹，模仿即可，不需要在线环境
- **需偏好数据**：没有唯一正解，只能相对比较（pairwise / BT）
- **需 RL 环境**：reward 依赖**产物在沙箱里运行后的状态**，必须在线交互才能拿到
- **需规模**：已有证据表明小模型做不到，差距随参数或数据量变化

### 3.1 判定表

| 维度 | 主要手段 | 次要手段 | 依据 |
|---|---|---|---|
| D1 指令遵循 | **SFT 可得**（单轮）/ **需 RL 环境**（多轮维持） | — | 开源 GLM-5.2 单轮 CSR 已超 Opus-4.6（80.4 对 78.6），说明单轮靠数据即可；多轮衰减（Opus −6.2 对 Qwen −17.8）只能在多轮环境里训 |
| D2 视觉保真 | **SFT 可得** | 需偏好数据（细粒度排序） | 预训练「代码 ↔ 渲染图」配对已是公开共识（Kimi K2.5 App.B.3、K3 §3.1、Qwen3-VL §3.2.6、GLM-4.5V §3.1）。UI2Code^N 的 RL 收益来自**学习型 comparator**（人类一致 94%）而非 CLIP reward |
| D3 开放审美 | **需偏好数据** | 需 RL 环境（交互分） | AesCoder 消融（Qwen3-4B，InterAes）：SFT 0.62 / RFT 0.71 / DPO 0.70 / 只读代码文本的 RM 0.71 / **完整 agentic GRPO 1.04**。→ 纯 SFT 和纯文本 RM 都到 0.7 附近就封顶，要跨过去必须让 reward 来自真实运行时 |
| D4 布局响应式 | **需 RL 环境** | SFT 可得（容易造数据） | reward 是多视口渲染后的 DOM 盒模型，必须跑浏览器；但任务与参考解都可程序化生成，所以 SFT 冷启动很便宜 |
| D5 可访问性 | **需 RL 环境**（但环境极便宜） | SFT 可得 | axe-core 是确定性规则引擎，零噪声、无需 judge、无需 GPU。**全表性价比最高的 RL 信号** |
| D6 交互与状态逻辑 | **需 RL 环境** | — | reward 定义就是「执行动作后读状态」。WorldBench 变异测试证明纯代码 judge 不可替代（删掉功能仍给 5.44/7.11） |
| D7 3D 空间推理 | **需 RL 环境** | SFT 可得（复刻类） | CAD 线已证明在线 RL 优于离线（cadrille 原文 "online RL … outperform offline alternatives"；CC3D 多视图 IoU 56.1→65.0、无效率 7.7→0.1）。但 Blender / three.js 方向**至今没有 RL 训练论文**，全部停在筛选后 SFT 或推理时迭代（`01_frontier_labs.md` §5 表） |
| D8 动画与时间 | **需 RL 环境** | — | 机制断言必须逐帧读运行时状态；SimWorlds 的 MPR 0.87 对 0.67 证明这个信号和 VLM 评分不是一回事 |
| D9 性能预算 | **需 RL 环境**（极便宜） | — | 直接读计数器，和 D5 同档：确定性、无 judge |
| D10 取证质量 | **需 RL 环境** | SFT 可得（示范轨迹） | 这是**纯行为**，没有正确答案文本可模仿之外的东西；但 3DHarnessBench 显示「只规范化视口」就能把 MiniMax 从 0.3722 救回 0.6148 —— 说明**少量示范轨迹的 SFT 收益可能很大**【推断】 |
| D11 判别力 | **需专门训练**（不是规模的副产物） | 需偏好数据 | **CriticGPT（arXiv 2407.00215，2024-06）：要靠纯加大模型达到 CriticGPT（RL only）的漏 bug 率，需约 30 倍预训练算力** —— 判别力靠训比靠堆参数便宜 30 倍。BouncerBench（2506.17812）：**非 reasoning 模型（含 gpt-4.1、claude-3.7-sonnet）判 patch 该不该拒的 O-Score 为负，即差于随机**；claude-3.7-sonnet 对错误 patch 召回只有 7.9%。3DCodeBench：「第一轮就判不用改」的比例按能力单调排序（Gemma 4 31B 41%，更小模型 3%~13%）；BlenderGym pairwise 最好的 Claude 3.5 只有 0.66（人与人 0.79）。Visual-ERM 证明**专门训一个 8B 生成式 RM** 能把 F1_hard 比基座提 36.8 且超过 GPT-5.2 的 32.7 → 判别力可以被专门训出来，但不是通用能力的副产品 |
| D12 探索纪律 | **需 RL 环境** | — | AutoLab 的 302 个零分 rollout 人工归因：claude-opus-4.6 是明显的步数离群点（最多步、最高分），**gpt-5.4 与 grok-4-20「只做极少探索就提交」**，deepseek-v4-pro / hunyuan-3 则**耗尽预算从未提交**。过早停止与重复看图都是 credit assignment 问题。ReLook 的 Forced Optimization（只接受严格变好的修改，每轮最多重采 10 次）在 ArtifactsBench-Lite 上单独值 **+2.0**（25.84 → 27.88）。注意作者先试了「对退步给负分」，模型学会**减少反思次数**躲罚，弃用 |
| D13 长程工程 | **需 RL 环境** + **需规模** | — | MiniMax M2.5 的口径是 "more than 200,000 real-world environments"；MTAC-IFBench 的 harness 消融显示同一模型换 harness，C-ISR 从 12.7 掉到 6.7 → 环境与 harness 本身就是能力的一部分 |
| D14 调试恢复 | **需 RL 环境** | SFT 可得（变异体任务） | 变异体任务可以离线批量造（`03_verifiable_construction.md` §2.3），所以冷启动便宜；但「不越改越坏」要靠轨迹级 reward（ReLook 的行为坍塌证据） |

### 3.2 一句话结论

- **只靠 SFT 能拿到的**：D2 视觉保真、D1 单轮指令遵循。这两项开源已经基本解决，继续投产出很低
- **最便宜的 RL 信号**：D5 可访问性、D9 性能预算（确定性规则，无 judge，无 GPU）。应该第一批接进环境
- **差距最大的**：D13 长程持久性与时间预算校准（AutoLab 0.68 对 0.46）。reward 必须来自「agent 自己的行为轨迹」，不是产物
- **收益最大但别当 KPI 的**：D10~D12 自我验证三项。它是全行业瓶颈（§2.1 证据 F~K），对我们这种单步基线更低的起点**绝对收益最大**，但「循环增益倍数」高说明单步弱，不能当目标
- **必须训、不能 prompt 的**：自修正本身。VisRefiner 把同一基座从「prompt 自修正单调下降」变成「训练后单调上升」；SCoRe 把 delta 从 −11.2% 推到 +4.4%
- **需要专门训 RM 的**：D3 审美、D11 判别力。Visual-ERM / UI2Code^N comparator 证明 8B 级别的专用 RM 就能超过通用前沿模型做 judge

---

## 4. 内部评测集设计：要复刻就得先能测

### 4.1 噪声从哪来，公式长什么样

记 M = 题数，n = 每题采样次数，r = judge 重复次数。

**① 采样噪声（所有维度都有）**

单题真实成功率 p_i，估计量 p̂_i = c_i/n：

```
Var(p̂_i) = p_i(1 − p_i) / n
```

集合分 S = (1/M)·Σ p̂_i：

```
Var(S) = (1/M²)·Σ p_i(1−p_i)/n  ≤  0.25 / (M·n)
SE(S)  ≤  0.5 / sqrt(M·n)
```

**② judge 噪声（只有 L3 / L4 维度有）**

WorldBench 的实测：**同一产物重跑，7/32 的条目翻面（21.9%）**。
记单次 judge 翻面率 f，取 r 次多数票后的有效翻面率：

```
f_eff(r=3) = 3f²(1−f) + f³
f = 0.219 → f_eff = 0.123
σ²_judge ≈ f_eff(1 − f_eff) ≈ 0.11
```

合并后：

```
Var(p̂_i) = [ p_i(1−p_i) + σ²_judge ] / n
```

**③ 两个模型比较的最小可检测效应 MDE**

同一题集上比 A、B 两个模型（双侧 α=0.05，power 80%，系数 2.8）：

```
SE_diff = sqrt( 2·(0.25 + σ²_judge) / (M·n) )
MDE     = 2.8 · SE_diff
```

代入两种 verifier：

```
程序化 verifier（σ²_judge = 0）：MDE = 1.98 / sqrt(M·n)
VLM rubric 3 票多数（σ²_judge = 0.11）：MDE = 2.38 / sqrt(M·n)
```

### 4.2 两个必须先知道的噪声地板

**① verifier 选错，相关性可以是负的。**
WorldCoder-Bench（arXiv 2606.01869）表 2 把四种 verifier 与真值 V-Cov 的 Kendall τ_b 直接测了出来：

| verifier | 与真值的 Kendall τ_b | 假阳性率 | 相对成本 |
|---|---|---|---|
| **隐藏运行时状态契约**（StateProbe） | **1.000** | **0** | ~2× |
| 8 步 agent 自主探查 | +0.111 | **45.6%** | ~400× |
| DOM-only | −0.021 | — | — |
| **截图 + VLM（GPT-5.4）** | **−0.068** | — | ~50× |

→ **截图 + VLM 在 3D 上与真值负相关，而且贵 25 倍。** 这一条直接否掉「先用 VLM judge 兜底，以后再说」的路线。

**② 审美的人类一致率只有 0.37，必须靠多人聚合。**
AUV-Bench（arXiv 2609.34854，2026-09-28；1,395 个可执行参考 UI，招募 51 名专业设计师、质控后留 44 人，每 UI 由 3 人独立 1~5 分）：

| 维度 | Krippendorff α（ordinal，单人） | ICC(1,3)（3 人平均） |
|---|---|---|
| **Color（最不可靠）** | **0.328** | 0.596 |
| Typography | 0.334 | 0.609 |
| Visual-style Consistency | 0.366 | 0.635 |
| Image–Text Fit | 0.402 | 0.667 |
| **Layout（最可靠）** | **0.431** | 0.694 |
| **宏平均** | **0.368** | **0.637** |

- 单个设计师的审美打分 α≈0.37，**远低于 0.80 的可靠线**
- **3 人平均后 ICC 升到 0.637** → 审美只能靠多人聚合度量，单人标注不能当真值
- 对照：WebDevJudge 的同一批标注员，**无 rubric 一致率 65.0% → 有人写 rubric 92.0%**（LLM 生成 rubric 90.0%）
  → **审美的可度量性主要是 rubric 工程问题，不是人的问题**
- 另一个硬墙：**judge 在「静态截图」上能到 90.95%，在「可交互运行的网页应用」上最好只有 66.06%（人类 84.82%）**。
  19 个百分点的落差全在「要不要理解交互行为」—— 这就是 judge 能否替人的分界线

→ **推论：D3 审美维度不能用 pointwise 打分，必须用组内 pairwise + rubric 树；而且 verifier 的人工校准集必须至少 3 人标注。**

### 4.3 MDE 表：直接查，别猜

单位是百分点。**这张表是全文最该贴在墙上的一张。**

| M × n | 总样本 | 程序化 MDE | VLM rubric MDE |
|---|---|---|---|
| 15 × 8 | 120 | 18.1 | 21.7 |
| 15 × 32 | 480 | 9.0 | 10.9 |
| 30 × 8 | 240 | 12.8 | 15.4 |
| 40 × 16 | 640 | 7.8 | 9.4 |
| 100 × 8 | 800 | 7.0 | 8.4 |
| 150 × 16 | 2,400 | 4.0 | 4.9 |
| 300 × 16 | 4,800 | 2.9 | 3.4 |

三条立刻可用的结论：

1. **单维度 15 题 × 8 次，MDE 是 18 个百分点。** 也就是说这个规模下，任何小于 18 点的维度差异都读不出来。
   很多内部实验的「这个改动涨了 5 个点」就是在这个分辨率下报出来的 —— 它是噪声
2. **要在单维度上读出 5 个百分点，需要 M·n ≈ 1,600**（程序化）或 **2,260**（VLM）。
   即 40 题 × 40 次，或 100 题 × 16 次
3. **单条 case 上比两个方案的优劣，每臂至少 63 次**：
   `MDE_单题 = 1.98/sqrt(n)`，要 MDE ≤ 0.25 需 n ≥ 63。
   n = 5 时单题只有 6 个可能取值（0/5 … 5/5），MDE = 0.89 —— 等于什么也没测

### 4.4 推荐配置：14 维 / 430 题 / 三档采样

把预算按「差距大小 × verifier 成本」分配，不要每维平摊。

| 档 | 维度 | 题数 M | 采样 n | judge 重复 r | 单维 MDE | verifier |
|---|---|---|---|---|---|---|
| **A 核心**（差距最大，要能读小效应） | D10 取证质量、D11 判别力、D12 探索纪律、D13 长程工程、D14 调试恢复 | 各 **40** | **16** | 3（仅 D11） | 7.8~9.4 | 轨迹统计（D10/D12）、变异测试（D11/D14）、build + 工作流断言（D13） |
| **B 中档**（已有公开基准，主要用于对标） | D1 指令遵循、D3 审美、D6 交互逻辑、D7 3D 推理、D8 动画 | 各 **30** | **8** | 3（仅 D3） | 12.8~15.4 | checklist（D1）、组内 pairwise（D3）、Playwright 状态断言（D6）、scene graph + 体素 IoU（D7）、固定时钟逐帧断言（D8） |
| **C 硬闸**（确定性规则，噪声只来自采样） | D2 视觉保真、D4 布局响应式、D5 可访问性、D9 性能预算 | 各 **20** | **4** | — | 22.1 | Design2Code 四项（D2）、多视口 DOM 断言（D4）、axe-core（D5）、渲染计数器 + 帧间隔（D9） |

合计 **M = 5×40 + 5×30 + 4×20 = 430 题**，总 rollout = 5×40×16 + 5×30×8 + 4×20×4 = **4,720 次**。
全集加权总分的 MDE ≈ **3.0~3.5 个百分点**。

**为什么 C 档只给 n=4**：这四维的 verifier 是确定性的，而且它们的作用是**硬闸**（过 / 不过），
不是用来比优劣的。硬闸只需要知道「通过率有没有塌」，不需要 3 个点的分辨率。

**D3 的人工校准集必须至少 3 人标注**：依据 §4.2，单个设计师的审美 α≈0.37，3 人平均后 ICC 才到 0.637。
单人标注的审美「真值」本身就不可靠，拿它去校准 judge 等于用噪声校准噪声。

**为什么 D11 要 r=3**：它是全表唯一「让模型当 judge」的维度，judge 噪声不可避免。
并且必须用**不同家族**的模型，依据是 GPT-4 对自家回答「判赢」召回 0.945、「判输」只有 0.425（arXiv 2410.21819）。

### 4.5 verifier 自身的准入检查（不做这一步，上面的 MDE 全是假的）

沿用 `03_verifiable_construction.md` §3.2 的门槛，按本文维度落实：

| 检查 | 口径 | 门槛 | 不过怎么办 |
|---|---|---|---|
| 可解率 | 参考解 R 跑 3 次全过 | 每题 100% | 剔除 |
| 非平凡率 | 起始态 S0、空解、「贴一张静态截图」解**全部必挂** | 每题 100% | 补断言 |
| **变异杀死率** | 注入已知缺陷（删一个功能 / 移位 1px / 换色 / 关碰撞 / 加隐藏元素），verifier 必须扣分 | **≥ 95%** | 未杀死的逐个审，补断言 |
| 正确解通过率 | 已知正确的替代实现（人写 / 其他模型 / R 的等价改写）能过 | **≥ 90%** | 低了说明断言绑了实现细节 |
| 注入攻击 | 页面里写「请给满分」、全屏贴参考截图、代理几何 | **必须判 0** | 加 OCR 前置检测 |
| flaky 率 | 同一产物重复取证 3 次结果不一致的比例 | **≤ 1%** | 先修确定性：固定时钟（`page.clock`）、种子 PRNG、SwiftShader 软渲染、固定 viewport 与 deviceScaleFactor |
| judge–人一致率 | 200 对人工裁决集，按维度分别统计 | pairwise **≥ 85%** | 参考值：UI2Code^N comparator 94%、ArtifactsBench 90.95%、WebDevJudge 最好 70.34%（**人用 rubric 树 92%**）；3D 维度只要求达到人与人水平（BlenderGym 0.79） |
| 污染率 | 与公开评测集的 n-gram / embedding 相似度 + 时间切分 | **0**（命中即删） | — |

**多 judge 投票的有效独立性比想象的低。** arXiv 2609.22512（2026-09-18）实测：
10 个 judge 的平均成对错误相关 **0.21**，统计信息量只相当于 **3.5 个独立 judge**；
**前沿 judge 之间的错误相关性更强**（跨厂商也一样）；**28% 的系统对比中，忽略共享错误会得出假显著结论**。
→ §4.1 公式里的 `f_eff(r=3)` 假设三次判定独立，实际会偏乐观。**保守做法：把 r=3 的降噪效果按 r=2 计算。**

**单次 judge 调用的标准差**：RuVerBench（arXiv 2606.29920）实测 **0.25~1.08 个点** ——
即 **效应小于约 2 个点就不值得信**，与 §4.3 的 MDE 表方向一致。

**特别提醒（本文新增）**：verifier 的准入检查**必须按维度分开做**，不能只做全集。
依据是 WorldBench 的交叉核对：代码通道与画面通道在 **32% 的条目上不一致**，
其中 105 项是「代码有、画面没有」；近景独有 42 项、广角独有 26 项，**名次因此对调**。

### 4.6 三个真空白：自己做就是首发

| 维度 | 自建方案 | 为什么便宜 / 公开先例 |
|---|---|---|
| **D9 性能预算**（真空白） | three.js 读 `renderer.info`（draw call / 三角形数 / 纹理数）；Playwright 采 90 个帧间隔算 p95；打包体积与首屏时间 | 确定性读数，无 judge 无 GPU。公开先例只有 OpenAI Astra 游戏博客的产品工作流，没有 benchmark |
| **多视口一致性**（真空白） | 把 WebRenderBench 的纯 WebDriver 读数（RDA 相对布局差 / GDA 分组计数差 / SDA 样式差）在 **375 / 768 / 1440 三档各算一遍，看跨档退化幅度** | 用 6 组措辞检索过，**没有任何公开 benchmark 做这件事**。而 Design2Code 的 block / position 与 WebRenderBench 的读数本身都是 viewport-agnostic 的，直接能跑。做出来就是首发 |
| **动画时间正确性作为通用子分**（真空白） | 抄 Animation2Code 的 CoTracker3 位移方向 + 幅值比 + Chamfer 匹配；或 ManimBench 的 5FPS 抽帧 → SSIM 矩阵双向最佳匹配 → fastDTW 对齐 | 有现成 verifier 实现，但**没人把它做成通用 codegen 的时间子分** |

**D5 可访问性不是空白（本节修正）**：有 RealUIReq-300 / A11yn、WebAccessBench、microsoft/a11y-llm-eval、A11YBench 四个专项集。
自建时直接抄 microsoft 的**双闸**口径（axe-core 零失败 **且** 手写 Requirement 断言全过才算过），
并配 A11yn 的 **IR = 加权违规分 / DOM 元素总数** 做规模归一化。四个坑：

| 坑 | 说明 |
|---|---|
| **axe-core 本身不出分** | 它只返回 passes / violations / incomplete / inapplicable 四个数组，任何 0~100 分都是外层自算的，**跨 benchmark 不可比** |
| **Lighthouse 比 axe 更弱** | 有刻意做成不可访问的站能拿满分 100 |
| **把 axe 分当 RL 奖励会被 hack** | 典型形态：alt 属性有但描述无意义 |
| **不做规模归一化会翻转排名** | WebAccessBench 实测：老 / 小模型原始缺陷数低，但每 100 个 DOM 元素的缺陷密度更高（14.15 对旗舰 9.69） |
| **键盘可达测不出来** | axe / Lighthouse 基本测不到焦点顺序，WebAccessBench 自己承认。**唯一可自动验的路子是手写断言**（microsoft 的做法） |

**风险**：这两维极易被 Goodhart。axe-core 全绿的页面可以完全不可用。
对策：它们只作**硬闸**（不过就截断，后层不计算），**不进入加权总分**。
这与 `04_verifier.md` §6.1 的聚合规则一致。

---

## 5. 里程碑：三个阶段的可检验目标

每阶段的目标都写成「在哪个集上、什么口径、到什么数」，不写「显著提升」。
所有分数口径：**锁定 harness（Claude Code 某一版本）并写进报告**，带工具 / 不带工具分列。

#### 阶段一（约 3 个月）：先能测，再谈训

目标是把「量尺」立起来，不追模型分数。

| 可检验目标 | 口径 | 验收数 |
|---|---|---|
| 自建 harness 能复现公开分 | 用自建 harness 跑同一个公开模型在 **Design2Code**（纯渲染 + 像素/DOM，无 LLM）与 **3JSBench**（743 条确定性几何检查）上的分 | 与公开数字相差 **≤ 2 点**。**不要用 ArtifactsBench 做复现基准**：官方榜已停更在 **Version 1.2 / 2025-08-09**（changelog 最后一条 2025-10-27），2026 年各聚合站的「ArtifactsBench 排名」互相矛盾且多为厂商自报 |
| 内部 430 题评测集上线 | §4.4 的三档配置全部跑通 | 全集 MDE **≤ 3.5 点**（实测，不是估算） |
| verifier 准入全过 | §4.5 八项检查，**按 14 维分别统计** | 变异杀死率 ≥ 95%、正确解通过率 ≥ 90%、flaky ≤ 1%、注入攻击全判 0 |
| D5 / D9 硬闸建成 | axe-core + 渲染计数器 | 两维都能在 5 秒内给出确定性判决 |
| 基线模型定位 | 自建集上跑开源基座 + 2 个前沿模型 | 得到 14 维的差距向量（这是后续所有决策的输入） |

**不设为阶段一目标**：WebDev Arena Elo。原因是它靠人类众包，周期长、受单一人群口味主导，
且平局率 26%、约 18% 的票是「两个都差」—— 不适合做短周期迭代的指标。

#### 阶段二（约 6 个月）：把确定性信号接进 RL 环境

打 D5 / D9 / D4 / D6 / D8 —— 这几维的共同点是 **reward 确定性、无 judge、可大规模并行**。
依据：SimuScene 证明窄域 + 确定性 verifier 下，**32B 开源经 RL 可从 21.5% 打到 72.2% Pass@8**，反超最强闭源。

| 可检验目标 | 公开集 | 起点 | 目标 |
|---|---|---|---|
| 交互与状态逻辑 | WebGen-Bench（2505.03733） | 已知最好开源 38.2%（Qwen2.5-Coder-32B + WebGen-Instruct） | **≥ 45%** |
| 3D 运行时正确性 | WorldCoder-Bench（2606.01869）Core | 当前最好系统 27.8% | **≥ 30%**，且 Robust（19.9%）同步提升 |
| 动画机制正确性 | SimuScene（2602.10840） | 最强 LLM 21.5% Avg@8 | **Avg@8 ≥ 40%**（不是 Pass@8，避免采样数掩盖） |
| 可访问性（最便宜的 RL 信号） | RealUIReq-300（2510.13914），IR_Axe | 前沿最好 GPT-5.1 **0.13**；基座未测 | **≤ 0.08**。参照 **A11yn（Qwen2.5-Coder-7B + GRPO）已做到 0.05**，即这一维开源 7B 已超前沿，是最容易先拿下的一格 |
| 动画时间正确性 | Animation2Code（2606.28593）Temporal | 全场最高 **0.31**（Gemini 3 Flash）；开源 Qwen3-VL-8B + 迭代 0.28 | **≥ 0.40**（这一格天花板最低，最容易做出领先） |
| 开放产物综合 | 三选一并明确写口径：ArtifactsBench **v1.2 官方表**（裁判统一 Gemini-2.5-Pro，**不要用聚合站数字**）、WebCraftBench（2609.15387）、WebCoderBench（2601.02430） | ArtifactsBench v1.2：GPT-5 **72.55**、开源最好 GPT-OSS-120B **57.69** | **≥ 62**（开源最好 +4 点） |
| 视觉保真不退化 | Design2Code | 最好开源 93.4（Qwen3-VL-235B-Thinking） | **≥ 93**（守住，不要为了 RL 牺牲这一维） |
| reward hacking 监控 | 自建 | — | 每轮训练统计：绝对定位元素占比、输出长度、text 元素数、有效渲染率；**任一指标与 held-out 人工分背离即停训修环境**（METR 与 OpenAI 的共同结论：hack 监控结果用来修环境，不直接当负奖励） |

#### 阶段三（约 12 个月）：打自我验证与长程

核心指标是**带工具的绝对分**和**多轮不塌**，**不是「循环增益倍数」** ——
按 §0 第 2 条，倍数高恰恰说明单步弱（BenchCAD 上 GPT-5.6 Sol 只有 1.18× 而 Opus 4.8 有 1.90×）。
把倍数当 KPI 会奖励「把单步做烂」。

| 可检验目标 | 口径 | 目标 |
|---|---|---|
| **带工具的绝对分**（阶段三的头号指标） | BenchCAD，voxel IoU，1000 子集，5 次平均，**带工具** | **≥ 0.65**（参照：Opus 5 = 0.821、Mythos 5 = 0.650、Opus 4.8 = 0.521） |
| **不带工具的基线同步不掉** | 同上，**不带工具** | **≥ 0.37**（参照：Mythos 5 = 0.379、Opus 5 = 0.366）。**这一行是防「只练循环不练单步」的护栏** |
| **一致性**（比天花板更重要的代际指标） | 任一长程集的 Pass@1 / Pass@3 / Pass³（三次全对） | **Pass³ / Pass@1 ≥ 0.90**（参照：Opus 5 Toolathlon Pass@1 80.6、Pass@3 87.0、Pass³ 73.1，比值 0.907；Sonnet 5 为 0.880、Opus 4.8 为 0.892） |
| **长程持久性** | AutoLab 式的 2~12 小时任务，Avg@3 | **≥ 0.50**（参照：claude-opus-4.6 = 0.68、gemini-3.1-pro = 0.50、kimi-k2.6 = 0.46、gpt-5.4 = 0.36）。同时统计两类失效占比：**过早提交** 与 **耗尽预算从不提交**，各 ≤ 10% |
| **主动取景不退步** | 3DHarnessBench（2609.06535）多视角档 → 主动视觉档的变化 | **≥ +10%**（参照：Opus 5 +16.4%、Kimi K3 +14.9%、GPT-5.6 +10.5%；**反例 Gemini −8.2%、MiniMax −16.5%**） |
| **取证质量**（D10） | 截图前视口 / 相机规范化率 | **≥ 95%**。依据：MiniMax 仅靠这一项就从 0.3722 回到 0.6148 |
| **停机纪律**（D12） | 截图调用数落在合理区间 | **20~30 次**（参照：Opus 5 = 26.15、GPT-5.6 = 25.73；**反例 Gemini 8.00 过早停止、MiniMax 74.82 重复看图**） |
| 长程工程 | Vibe Code Bench（2603.04601）v1.1，**OpenHands harness** | **≥ 86%**（参照：闭源最高 Sonnet 5.5 92.39%；开源最高 MiMo V2.6 Pro 85.22%、Kimi K3 84.97%、DeepSeek V4.1 Flash 84.74%。目标就是跨过当前开源天花板） |
| 多轮不衰减 | MTAC-IFBench（2609.14992）CSR 第 1-2 轮 → 第 9-10 轮 | 衰减 **≤ 8 点**（参照：Opus-4.6 −6.2；**反例 Gemini-3.1-Pro −23.4、Qwen3.5-27B −17.8**） |
| 调试恢复 | SWE-bench Multimodal 公开 dev split | **≥ 50**（参照：Opus 5 = 59.4、Qwen3.8-27B = 38.6） |
| **three.js 几何正确性** | 3JSBench（743 条确定性检查），100 题 ×3 rollout | **≥ 50%**（参照：GPT-6 Astra 80.00%、Fable 5.1 69.33%、**Claude Opus 5.5 49.00%**、GPT-6 Sol 27.00%、Kimi K3 23.00%）。注意 Opus 5.5 的主要失败项是 `quality.draw-order`(40)、`task.key-objects-clear`(31)、`quality.culling`(30) |
| 审美（此时才作为目标） | ① Design Arena Elo（allcategories，**带快照日**）② Code Arena·WebDev Elo | Design Arena **≥ 1360**（参照：Opus 5.5 1392、Astra 1379、开源最好 deepseek-v4-1-flash 1323）；Code Arena WebDev **≥ 1720**（参照 Opus 5.5 1813、Astra 1786、开源最好 Qwen3.8-Max 1674） |
| 循环的正收益保障 | 自建轨迹集 | 必须同时具备：① 回滚机制 ② 单调改进约束（ReLook 的 Forced Optimization，只接受严格超过历史最佳的修改，每轮最多重采 10 次）③ 停机判据 ④ **取 best-of-rounds 而不是 last-round**（RubSE / VisRefiner / CITL / RILA 四篇一致）。**不能用「对退步给负分」—— ReLook 实测模型会学会减少反思次数躲罚** |
| **自修正必须训，不能靠 prompt** | 对照实验 | 同一基座，prompt 自修正档 vs SFT+RL 训练档，在同一视觉集上对比。参照：VisRefiner 把 Qwen2.5-VL-7B 从「prompt 自修正单调下降 87.5→86.6」变成「训练后单调上升 92.0→92.9」；SCoRe 把 self-correction delta 从 −11.2% 推到 +4.4% |
| **验证信号要来自外部，不是自省** | 环境设计 | 必须接入：执行反馈 + 渲染回灌 + 局部编辑工具（RILA 消融：去执行反馈 −3.22、改整页重生成 −4.82）；外部 critic（CITL：有 critic +17.8%，纯自我 refine 只 +1.5%） |

### 5.1 三个阶段的共同纪律

1. **任何维度报分，必须同时报 M、n、harness 版本、judge 型号、带不带工具。** 缺一项的数就不要进报告
2. **每次改 verifier，先跑变异测试与注入测试再上线。** 判别力不是一次性的：policy 变强后原本 0 < p < 1 的题会变成全对，作弊方式也会换
3. **分数单调上升不等于质量单调上升。** Anthropic 原文："I regularly saw cases where I preferred a middle iteration over the last one" —— 保留中间轮做人工对照
4. **rubric 里不写量化阈值、不写诱导词。** 阈值写成代码闸；"museum quality" 这类词会把审美推向单一收敛（Anthropic 原文）

---

## 6. 本文新查证的出处与存疑项

### 6.1 本文新引入、前面几篇笔记没有的出处

| 出处 | arXiv / URL | 本文用它支撑什么 |
|---|---|---|
| **MTAC-IFBench** | https://arxiv.org/abs/2609.14992（2026-09） | D1 指令遵循的多轮衰减；开源 GLM-5.2 CSR 反超 Opus-4.6；harness 换了 C-ISR 腰斩 |
| **WebCraftBench** | https://arxiv.org/abs/2609.15387（v1 2026-09-14，v3 2026-09-20） | 369 需求 / 5,088 验收标准；用代码覆盖率引导 agent 探索；与人类偏好一致 85.3% |
| **WebCoderBench** | https://arxiv.org/abs/2601.02430（2026-01） | 1,572 真实需求 / 9 视角 24 指标；原文结论「没有模型在所有指标上占优」 |
| **3DHarnessBench**（全文核对） | https://arxiv.org/abs/2609.06535（2026-09-06，Institut Polytechnique de Paris） | §2.1 证据 B / C 的全部数字，包括四层级表、观察接口消融表 3、取证调用预算 |
| **BenchCAD**（标题核对） | https://arxiv.org/abs/2605.10865 | D7 的确定性打分口径（原文：工业标准、不用 LLM judge） |
| **Vibe Code Bench 实时榜**（本文新抓） | https://www.vals.ai/benchmarks/vibe-code （v1.1，2026-10-12） | D13 的闭源 / 开源差距；同模型换 harness 的分差 |
| **AutoLab** | https://arxiv.org/html/2606.05080 （2026-06-03） | §0 第 1 条、§2.1 证据 G、§2.3 第一名：harness 消融（弱模型获益更多）、超长程 Avg@3、零分 rollout 归因 |
| **VISTA** | https://arxiv.org/html/2605.26144 （v4 2026-09-29） | §2.1 证据 H：73.0% 轨迹跳过 self-audit |
| **RubSE** | https://arxiv.org/html/2608.24138 （2026-08-25） | §2.1 证据 I：GPT-5.2 15 轮视觉自演化全负、"visual repair coupling" |
| **VisRefiner** | https://arxiv.org/html/2602.05998 （2026-02） | §2.1 证据 I：通用 VLM 自修正净负；训练后单调上升 |
| **FronTalk** | https://arxiv.org/html/2601.04203 | §2.1 证据 I：视觉反馈对开源 VLM 普遍为负（−8.2 ~ −27.3） |
| **CITL** | https://arxiv.org/html/2604.05839v1 （2026-04） | 外部 critic +17.8% 对纯自我 refine +1.5% |
| **RILA** | https://arxiv.org/html/2609.02088 （2026-09） | 执行反馈 + 渲染回灌 + 局部编辑的消融 |
| **SCoRe** | https://arxiv.org/html/2409.12917v1 （2024-09） | 自修正可以被 RL 训出来：delta −11.2% → +4.4% |
| **Large Language Monkeys** | https://arxiv.org/html/2407.21787 （2024-07） | §2.1 证据 J：coverage 98.44% 对自我选择 41.41% |
| **Agentless** | https://arxiv.org/html/2407.01489 （2024-07） | §2.1 证据 J：oracle 42.0% 对自我验证 32.0% |
| **BouncerBench** | https://arxiv.org/html/2506.17812v1 （2025-06） | D11：非 reasoning 模型判 patch 的 O-Score 为负 |
| **CriticGPT** | https://arxiv.org/html/2407.00215v1 （2024-06） | D11：判别力靠训比靠堆参数便宜约 30 倍 |
| **SWE-bench 官方 Bash Only 榜** | https://www.swebench.com/ （快照 2026-02-17） | §2.1 证据 F：同 harness 开源与闭源差 1.0 点 |
| **GPT-6 Astra system card**（UK AISI no-CoT） | https://deploymentsafety.openai.com/gpt-6-astra | §2.1 证据 K：no-CoT 时间跨度 30.9 分钟对 3.6 分钟 |
| **Opus 5 system card**（CB-2 节） | https://www.anthropic.com/claude-opus-5-system-card | §0 第 1 条："Unproductive self-verification" 被列为限制；Toolathlon Pass@1 / Pass@3 / Pass³ |
| **多 judge 共识的有效独立性** | https://arxiv.org/abs/2609.22512 （2026-09-18） | §4.5：10 个 judge 只值 3.5 个独立 judge |
| **RuVerBench** | https://arxiv.org/html/2606.29920v2 | §4.5：单次 judge 调用标准差 0.25~1.08 点 |
| **自修正的指数收敛闭式** | https://arxiv.org/html/2508.16456v1 （2025-08） | §0 第 2 条：Acc_t = Upp − α^t(Upp − Acc_0) |
| ⭐**3JSBench** | https://3jsbench.com/ （数据 rev 2026-10-14；`/data/benchmark.json`、`/data/battle.json`） | D7：唯一同时有 GPT-6 Astra（80.00%）与 Claude Opus 5.5（49.00%）的确定性 three.js 集；SigLIP 区分度≈0 的实测 |
| **Design Arena** | https://www.designarena.ai/leaderboard （2026-10-15 直读，服务端 ts 2026-10-14T18:54Z） | D3：Opus 5.5 Elo 1392 / Astra 1379 / 开源最好 1323 |
| **Code Arena·WebDev** 镜像 | https://www.respan.ai/models/benchmarks/lmarena-webdev-lmarena （快照 2026-10-08）；官方 changelog https://news.lmarena.ai/leaderboard-changelog/ | D3：Opus 5.5 1813 / Astra 1786 / Qwen3.8-Max 1674。官方站 Cloudflare 403 |
| **Animation2Code** | https://arxiv.org/abs/2606.28593 （2026-06-26） | D8：DreamSim+DTW 外观 / CoTracker3 时间指标；Temporal 天花板 0.31 |
| **PRISM** | https://arxiv.org/abs/2605.19382 （2026-05-19） | D8：Exec→Spatial 平均掉 41.24 点 |
| **ManimBench** | https://arxiv.org/html/2604.18364v1 （2026-04-20） | D8：5FPS 抽帧 + SSIM 双向匹配 + fastDTW；开源 30B+GRPO 全场最好 |
| **RealUIReq-300 / A11yn** | https://arxiv.org/abs/2510.13914 （v2 2026-09-07） | D5：IR_Axe 口径；Qwen2.5-Coder-7B+GRPO 做到 0.05 超全部前沿 |
| **WebAccessBench** | https://conesible.de/wab/whitepaper_webaccessbench.pdf （2026-02-25） | D5：规模归一化会翻转排名（14.15 对 9.69） |
| **microsoft/a11y-llm-eval** | https://microsoft.github.io/a11y-llm-eval-report/ · https://github.com/microsoft/a11y-llm-eval | D5：axe 零失败 + 手写断言双闸；控制组 GPT-5.4 Mini 仅 25%，加 skill 后 Gemini 3.1 Pro 96% |
| **A11YBench / A11YRepair** | https://arxiv.org/html/2606.21926 （2026-06-20） | D5：修复向，IBM Accessibility Checker |
| **WebRenderBench** | https://arxiv.org/abs/2510.04097 （2025-10-05） | D4：纯 WebDriver 无 LLM 的 RDA / GDA / SDA，是多视口一致性指标的现成底座 |
| **Figma2Code** | https://arxiv.org/abs/2604.13648 （2026-04-15） | D4：RUR / APR；GPT-5 视觉最好而响应式最差 |
| **AUV-Bench** | https://arxiv.org/html/2609.34854v1 （2026-09-28） | §4.2：审美单人 α=0.368，3 人 ICC=0.637 |
| **WorldCoder-Bench 表 2** | https://arxiv.org/abs/2606.01869 | §4.2：截图+VLM 的 τ_b = −0.068；隐藏状态契约 τ=1.000 |
| **Vision2Web** | https://arxiv.org/html/2603.26648 （v3 2026-07-20） | §2.2：全栈视觉建站开源几乎全线 0 |
| **FronTalk** | https://arxiv.org/abs/2601.04203 （v2 2026-06-10） | §0 第 4 条的 nuance：AceCoder 自我批判增益 GPT-4o +9.3 对 Qwen2.5-VL-72B +0.8 |
| **Opus 5.5 发布页** | https://www.anthropic.com/claude-opus-5-5 | D14：Deloitte 的 72% 对 56%；Terminal-Bench 4.0 Opus 5.5 66.4% 对 Astra 57.9% |
| **Prompting Claude Opus 5（官方 docs）** | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 | §0 第 1 条：官方要求**删掉**显式验证指令以免 over-verification |

### 6.2 存疑与未核实

0. **本文的核心结论在调研过程中翻转过一次。** 初稿按 §2.1 证据 A~E（BenchCAD 带工具倍数、3DHarnessBench 四层级）
   得出「自我验证是主要差距来源」；补齐证据 F~K（同 harness SWE-bench、AutoLab harness 消融、VISTA 轨迹审计、
   RubSE / VisRefiner 的负收益、Astra 的 no-CoT 跨度）之后结论反转。
   **两组证据都是真的，冲突出在「增量大」不等于「差距大」** —— 增量大只说明循环值钱，
   而循环对**所有人**都值钱，对弱模型更值钱。读这份文档时请把 A~E 和 F~K 一起看。
1. **BenchCAD 的厂商自报分两家口径不同**，官方榜自标 "vendor self-reported, not re-graded"。
   本文的「2.24 倍」只在**同一行（同一厂商口径）**内成立，不要跨厂商比
2. **3DHarnessBench 表 3 只有 10 个实例。** 按 §4.3 的公式，M=10、n=1 的 MDE 远大于表里的差值 ——
   这组消融**方向可信、幅度不可信**。要当成「证明机制存在」，不要当成「效应量是 0.24」
3. **Vibe Code Bench 的榜在动。** 本文 §1.3 的数字取自 vals.ai 实时榜 2026-10-12 版，
   与 `benchmarks.md`（2026-09-22 抓取）已经不同（当时榜首是 Fable 5 90.35%，且笔记里未记录开源模型）。
   引用这个集必须同时写抓取日期和 harness
4. **D5 可访问性、D9 性能预算完全没有公开 benchmark。** 本文的自建方案是【推断】，公开先例只有
   OpenAI Astra 游戏博客里的渲染计数器与帧间隔做法，那是产品工作流不是评测
5. **MTAC-IFBench 没有做「带 / 不带自我验证」的消融。** 所以它的 F-ISR 8 点差距不能直接归因到自我验证
6. **3JSBench 是非学术站点**（3jsbench.com），无论文、无同行评审，样本只有 100 题 ×3 rollout。
   按 §4.3 的公式，M=100、n=3 → 程序化 MDE ≈ 11.4 个点。
   所以「Astra 80% 对 Opus 5.5 49%」这个 31 点差距可信，但 Fable 5.1 69.33% 与 Astra 80.00% 之间的 10.7 点**接近分辨率下限**
7. **WorldBench 的模型排名不可引用。** 论文自己声明一条 prompt、每模型生成一次、评一次，
   未报方差、无人类标注，原文写 **"we do not claim a ranking among them"**。
   所以 Fable 5.1 的 210.79 对 Astra 的 199.73 不能当成优劣结论
8. **ArtifactsBench 官方榜已停更在 v1.2 / 2025-08-09**（changelog 最后一条 2025-10-27）。
   前面几篇笔记里引用的 2026 年 ArtifactsBench 数字（MiniMax-M2 66.8、Seed2.0-Pro 66.6 等）**全部是厂商自报，裁判与实现各不相同**，不可横向比
9. **Code Arena·WebDev 的官方站对本机 403**，本文的 Elo 全部来自第三方镜像（标注了快照日）。
   同一指标出现过 1786 / 1788 / 1792 / 1793 / 1813 / 1815 / 1818 七个值，**都是不同快照，不是不同测量目标**
10. **SWE-bench Multimodal 的 Opus 5.5 70.21% 对 Astra 43.33% 来自 vals.ai（二手）**，Anthropic 自报的 Opus 5 是 59.4%（内部 harness），两者口径不同
11. **3DCodeBench 附录 D.2 的表与正文自相矛盾**（正文说视觉自我批评在 image-to-3D 上全部翻负，
   但表里 Gemini 3.5 Flash 的 image 行是 +0.0126）。本文只引用「方向不确定」这一结论

