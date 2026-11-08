# Visual Coding Benchmark Timeline by Capability

- 截止：2026-09-23；共 78 条，全部经 arXiv / 官方页 / GitHub 查证
- 时间口径：arXiv v1 提交月份（查到 v1 日期的按日期，否则按 arXiv 编号的 YYMM）
- 状态口径：写出会议名的，均为 arXiv 页 comments 或会议官网可查到的录用信息；其余一律记「arXiv 预印本」
- 「关键发现 / SOTA」只摘论文摘要或官方页原文数字；摘要里没有数字的，只写定性结论

### 1. 截图 / 设计稿 → 网页代码

| 时间 | Benchmark | 规模 | 评测方式 | 关键发现 / SOTA | 状态 |
|---|---|---|---|---|---|
| 2024-03 | [Design2Code](https://arxiv.org/abs/2403.03163) | 484 个真实网页（C4 筛选） | 截图 → HTML，渲染后算视觉/布局/文本相似度 + 人评 | v1：标注者认为 GPT-4V 生成页有 49% 可替代原页、64% 优于原页；模型主要输在元素召回与布局 | NAACL 2025 |
| 2024-04 | [WebCode2M](https://arxiv.org/abs/2404.06369) | 2.56M 条（设计图 + 代码 + 布局） | 提出 TreeBLEU 衡量 DOM 结构层级召回 | 用该数据训练后，MLLM 的设计稿转代码能力显著提升 | WWW 2025 |
| 2024-06 | [Web2Code](https://arxiv.org/abs/2406.20098) | 1179.7k 条指令对 + 评测框架 | 网页理解 QA + 截图 → HTML 两套评测 | 当时的 MLLM 看网页截图、写 HTML 都很差；用该数据训练在通用视觉任务上也有增益 | NeurIPS 2024 D&B |
| 2024-10 | [Sketch2Code](https://arxiv.org/abs/2410.16232) | 731 张手绘草图（对应 484 个网页） | 单轮 + 多轮（模拟用户反馈 / 主动提问）；布局与视觉相似度 | 10 个 VLM 都难读懂草图；专家更偏好 agent 主动提问而不是被动收反馈 | NAACL 2025 |
| 2024-10 | [Image2Struct](https://arxiv.org/abs/2410.22456) | 2,400 例（网页 900 / LaTeX 1,200 / 乐谱 300） | 图 → 结构代码 → 渲染回图，用 5 种图像指标对比 | 网页最容易，其次 LaTeX，乐谱最难（EMS 最高 0.660 vs 0.402） | NeurIPS 2024 D&B |
| 2024-11 | [Interaction2Code](https://arxiv.org/abs/2411.03292) | 127 个网页、374 个交互、31 类交互 | 以交互原型为输入，生成可交互网页，对比交互前后效果 | 交互部分明显弱于整页生成；归纳出 10 类失败；视觉上不明显的交互最难 | ASE 2025 |
| 2025-06 | [DesignBench](https://arxiv.org/abs/2506.06251) | 900 个网页样本；React / Vue / Angular / 原生 | 生成、编辑、修复三类任务 | 揭示了各框架特有的短板，以及生成 / 编辑 / 修复各自的瓶颈 | arXiv 预印本 |
| 2025-06 | [WebUIBench](https://arxiv.org/abs/2506.07818) | 21K QA，来自 700+ 真实网站 | 拆成感知、HTML 编程、UI-HTML 理解、UI → 代码四个子能力 | 评了 29 个 MLLM，逐个子能力定位薄弱环节 | arXiv 预印本 |
| 2025-11 | [CANVAS](https://arxiv.org/abs/2511.20737) | 598 个任务（来自 3.3K 个移动端 UI 设计） | VLM 通过工具调用操作设计软件，做复刻 / 局部修改 | 强模型的工具调用更有策略，设计质量更高 | arXiv 预印本 |
| 2026-04 | [Figma2Code](https://arxiv.org/abs/2604.13648) | 3,055 条数据，精选 213 例作 benchmark | Figma 多模态设计稿 → 代码，评 10 个 MLLM | 闭源模型视觉保真度高，但响应式布局和代码可维护性差 | ICLR 2026 |
| 2026-05 | [WebIGBench](https://arxiv.org/abs/2606.00154) | 103 个复杂网页、871 个交互动作（5 类） | UI 自动化按预设路径回放交互，评视觉保真 + 交互一致性 | 静态还原之外，复杂交互仍是明显短板 | arXiv 预印本 |
| 2026-07 | [UI2App](https://arxiv.org/abs/2607.06306) | 327 张截图，组成 45 组多页状态序列 | 评可执行性、导航可达性、视觉保真度、交互推断得分 IIS | 视觉保真第一的模型 IIS 只有 7.5；IIS 第一名是它的 5.2 倍；跨页状态上一半模型得 0 分 | arXiv 预印本 |

### 2. 交互式 Web App / 前端功能正确性

| 时间 | Benchmark | 规模 | 评测方式 | 关键发现 / SOTA | 状态 |
|---|---|---|---|---|---|
| 2024-12 | [WebDev Arena](https://arena.ai/blog/webdev-arena) | 在线众包；官方博客写的是 8 万+ 投票 | 同一 prompt 由两个模型各生成一个 web app，用户上手试用后投票，按 Bradley-Terry 排名 | 平局率 26%（Chatbot Arena 是 35%），区分度更高；约 18% 投票是「两个都差」，多因依赖或编译失败 | 榜单网站 |
| 2025-05 | [WebGen-Bench](https://arxiv.org/abs/2505.03733) | 647 个测试用例，覆盖 13 个子类 | agent 从零生成多文件网站，再由 UI agent 执行测试用例 | 最好组合 Bolt.diy + DeepSeek-R1 只有 27.8%；用 WebGen-Instruct 训出的 Qwen2.5-Coder-32B 达 38.2% | arXiv 预印本 |
| 2025-05 | [FullFront](https://arxiv.org/abs/2505.17399) | 三个任务：设计、感知 QA、代码生成 | 用两阶段流程把真实网页清洗成标准 HTML 再出题 | 页面感知、图片处理、布局、交互实现都与人类专家差距明显 | arXiv 预印本 |
| 2025-07 | [ArtifactsBench](https://arxiv.org/abs/2507.04952) | 1,825 个任务（Web 组件 / SVG 可视化 / 小游戏） | 渲染后按时间序列截图，由 MLLM 对照逐题 checklist 打分 | 与 WebDev Arena 排名一致性 94.4%，与专家两两一致率 >90%；通用模型常优于领域专用模型 | arXiv 预印本 |
| 2025-08 | [UI-Bench](https://arxiv.org/abs/2508.20410) | 10 个工具 × 30 个 prompt = 300 个站点，4,000+ 条专家判断 | 专家两两对比，用 TrueSkill 给出带置信区间的排名 | 专门比 text-to-app 产品的视觉设计；有公开榜单 uibench.ai | arXiv 预印本 |
| 2025-10 | [WebGen-V Bench](https://arxiv.org/abs/2510.15306) | 用 agent 爬取的分区块多模态数据 | 按页面分区对齐文本、布局和视觉来打分 | 首个支持分区级细粒度评测的「指令 → HTML」基准 | arXiv 预印本 |
| 2025-12 | [FronTalk](https://arxiv.org/abs/2601.04203) | 100 段多轮对话（来自真实网站） | web agent 扮演用户多轮提需求，评功能与体验 | 模型普遍会「遗忘」，覆盖掉已实现的功能；AceCoder 基线把分数从 56.0% 提到 65.3% | CoLM 2026 |
| 2026-01 | [WebCoderBench](https://arxiv.org/abs/2601.02430) | 1,572 条真实用户需求 | 9 个视角、24 个指标，规则 + LLM judge，按人类偏好加权 | 12 个 LLM + 2 个 agent 中，没有哪一个在所有指标上占优 | arXiv 预印本 |
| 2026-02 | [1D-Bench](https://arxiv.org/abs/2602.18548) | 取自真实电商工作流 | 多轮组件级编辑，每轮带渲染反馈，对照参考图评分 | 迭代编辑能提高渲染成功率；后训练收益有限且不稳定 | arXiv 预印本 |
| 2026-03 | [Vibe Code Bench](https://arxiv.org/abs/2603.04601)（[v1.1 榜单](https://www.vals.ai/benchmarks/vibe-code)） | 100 份应用规格说明、964 条工作流、10,131 个子步骤 | 从规格说明构建并部署完整 web app，由浏览器 agent 走查工作流 | 论文：最好模型测试集 61.8%，接入外部服务（Stripe / 邮件）时从 71% 掉到 30%；v1.1 榜单（2026-09-22 更新）Claude Fable 5 为 90.35% | CAIS 2026 + 榜单网站 |
| 2026-04 | [WebCompass](https://arxiv.org/abs/2604.18224) | 输入覆盖文本 / 图像 / 视频，7 类任务 | 覆盖生成、编辑、修复的全生命周期，分易 / 中 / 难三档 | 同一框架内可以跨任务、跨模态比较 | arXiv 预印本 |
| 2026-05 | [The Single-File Test](https://arxiv.org/abs/2605.06707) | 17 个公开实验、68 份单文件 HTML（为期 8 周） | 录屏后人评 + Gemini judge | Claude 家族最强也最稳，按人评加权分赢下 17 题中的 9 题 | arXiv 预印本 |
| 2026-05 | [Cookie-Bench](https://arxiv.org/abs/2605.30000) | 11 个领域、54 个子任务、1,000 条 query | 三阶段：静态感知 → agent 自主交互（录屏 + 截图） → 动态打分 | 与专家评分高度一致；13 个前沿 LLM 都还有很大提升空间 | arXiv 预印本 |
| 2026-05 | [I-WebGenBench](https://arxiv.org/abs/2606.00750) | 19 篇论文，各配专家构建的交互系统 | 论文 → 交互式科学 web 应用 | 显式建模交互逻辑的 PaperVoyager 明显更好 | arXiv 预印本 |
| 2026-06 | [LongWebBench](https://arxiv.org/abs/2606.17727) | 490 个长网页 + 129 个网页上的 507 个交互任务 | VLM 评长程结构一致性 + DOM 增强 agent 验证功能 | 页面越长结构保真越差；看起来对的页面常常走不通多步交互 | arXiv 预印本 |
| 2026-08 | [LiveEvalBench](https://arxiv.org/abs/2608.03689) | 开放世界前端项目 | 三个角色 agent（构建 / 代码审查 / UI 测试）协作评审 | 与人类专家判断高度一致 | arXiv 预印本 |

### 3. 图表 / SVG / 可视化代码

| 时间 | Benchmark | 规模 | 评测方式 | 关键发现 / SOTA | 状态 |
|---|---|---|---|---|---|
| 2023-12 | [SVG-Bench（StarVector）](https://arxiv.org/abs/2312.11556) | 10 个数据集、3 类任务；新增 SVG-Emoji 和 SVG-Stack（2M） | 图像矢量化、文本 → SVG、图表生成 | 像素指标（MSE）衡量不了 SVG 质量；StarVector 产出的 SVG 更紧凑、语义更丰富 | CVPR 2025 |
| 2024-02 | [ChartX](https://arxiv.org/abs/2402.12185) | 48K 图表样本、18 类图表、7 类任务 | 包含「重绘代码」任务，用 GPT-score 打分 | 每个样本带图、CSV、重绘代码、描述四种模态 | arXiv 预印本 |
| 2024-05 | [Plot2Code](https://arxiv.org/abs/2405.07990) | 132 张 matplotlib 图、6 类 | 代码通过率 + 文本匹配率 + GPT-4V 整体打分 | 首批系统评测「图 → 绘图代码」的基准之一 | arXiv 预印本 |
| 2024-06 | [ChartMimic](https://arxiv.org/abs/2406.09961) | 4,800 组三元组、22 类、201 个子类 | Direct Mimic / Customized Mimic，同时评代码层和渲染图层 | GPT-4o 平均 82.2，InternVL2-76B 61.6 | ICLR 2025 |
| 2024-07 | [VGBench](https://arxiv.org/abs/2407.10972) | 4,279 条理解 QA + 5,845 条生成样本 | 覆盖 SVG / TikZ / Graphviz 的理解与生成 | 在 SVG 这类底层格式上表现最差 | EMNLP 2024 |
| 2025-05 | [ChartEdit](https://arxiv.org/abs/2505.11935) | 233 张真实图表、1,405 条编辑指令 | 代码层 + 图表层双重评测 | 最好模型只有 59.96 分 | ACL 2025 Findings |
| 2025-06 | [SVGenius](https://arxiv.org/abs/2506.03139) | 2,377 条 query、24 个领域、8 类任务、18 个指标 | 理解 → 编辑 → 生成三级递进 | 复杂度一升，所有模型系统性下滑；强化推理训练比单纯堆规模更有效 | ACM MM 2025 |
| 2025-07 | [ChartM³](https://arxiv.org/abs/2507.21167) | 1,000 例、4 档难度（另有 24K 训练集） | 多模态指令（文字 + 视觉标记）驱动图表编辑 | GPT-4o 看不懂视觉标记；在 24K 训练集上微调后大幅提升 | arXiv 预印本 |
| 2025-08 | [UniSVG](https://arxiv.org/abs/2508.07766) | 525K 条 | SVG 理解 + 文本 / 图像 → SVG 生成 | 在该数据上训练的开源 MLLM 超过了 GPT-4V | ACM MM 2025 |
| 2025-10 | [SArena（InternSVG）](https://arxiv.org/abs/2510.11341) | 覆盖多领域、多难度档位 | SVG 理解、编辑、生成的统一评测 | InternSVG 超过了主流开源与闭源模型 | arXiv 预印本 |
| 2025-10 | [Chart2Code](https://arxiv.org/abs/2510.17932) | 2,023 个任务、22 类图表、3 个层级 | 复现 → 编辑 → 长表格转图表 | 编辑任务上 GPT-5 代码分 0.57、图表质量分仅 0.22 | ACL 2026 |
| 2026-02 | [ChartEditBench](https://arxiv.org/abs/2602.15758) | 5,000 条合成数据（35 类修改），430 条人工核验 | 多步增量编辑链：执行检查 + 像素相似度 + 代码逻辑检查 | 首个专门评测多轮增量图表编辑的基准 | arXiv 预印本 |
| 2026-02 | [VectorGym](https://arxiv.org/abs/2603.29852) | 4 个任务：Sketch2SVG / 编辑 / Text2SVG / 描述，均为人工标注 | VLM-as-Judge（经人类相关性校验） | 8B 基线超过 Qwen3-VL-235B，与 GPT-4o 持平 | EMNLP 2026 |
| 2026-05 | [Vision2Code](https://arxiv.org/abs/2605.11307) | 2,169 例、15 个源数据集（图表 / 几何 / 文档 / 3D 等） | 不需要参考代码：渲染后由 VLM 按数据集 rubric 打分 | 图表类强，空间场景、化学、文档、电路图弱 | arXiv 预印本 |

### 4. 程序化 3D / Blender 代码与编辑

| 时间 | Benchmark | 规模 | 评测方式 | 关键发现 / SOTA | 状态 |
|---|---|---|---|---|---|
| 2024-02 | [UFO（L3GO）](https://arxiv.org/abs/2402.09052) | 50 条非常规物体描述（如「五条腿的椅子」） | 在 Blender 封装环境 SimpleBlenv 里调 API 搭积木，人评 | 按人评，L3GO 优于当时的 text-to-2D / 3D 模型 | NAACL 2025 Demo |
| 2025-04 | [BlenderGym](https://arxiv.org/abs/2504.01786) | 245 个手工场景、5 类任务 | 编辑 Python 脚本，把起始场景改成目标场景 | 最强 VLM 系统也做不好 Blender 用户觉得简单的任务；推理时在生成和验证之间分配算力有收益 | CVPR 2025 Highlight |
| 2026-01 | [BlenderBench（VIGA）](https://arxiv.org/abs/2601.11109) | 视觉 → 代码任务集 | 交错的多模态推理 + 迭代写 Blender 代码 | VIGA 比 one-shot 基线高 124.70% | arXiv 预印本 |
| 2026-05 | [3DCodeBench](https://arxiv.org/abs/2606.01057) | 212 个类别，每类配一份真值脚本 | 文本 / 图像 → Blender 5.0 程序化代码；指标为可执行率、SigLIP / DINO 相似度、Chamfer、LLM judge，另有人评对战平台 3DCodeArena | 失败多来自 API 不匹配；能渲染出来的也常有悬浮或断开的部件；更多思考预算和多轮修正有帮助 | arXiv 预印本 |
| 2026-06 | [WorldCoder-Bench](https://arxiv.org/abs/2606.01869) | 2,026 个任务（仿真 / 渲染 / 应用） | Three.js 生成 3D 世界；StateProbe 在沙箱里验证隐藏的运行时状态约束 | 最好系统在 Core 上 27.8%、在 Robust 上 19.9% | arXiv 预印本 |
| 2026-06 | [P3D-Bench](https://arxiv.org/abs/2606.11152) | 400 个文本 → 3D、400 个图像 → 3D、203 个装配体 | 评可执行性、几何、拓扑、约束、多视角语义、部件结构 | 装配体最难；整体形状对了，精确参数几何做不出来 | arXiv 预印本 |
| 2026-07 | [4DBuildBench（SimWorlds）](https://arxiv.org/abs/2607.01766) | 50 个场景：5 类物理求解器 + 静态，3 档难度 | 引擎状态审计（机制是否正确）+ VLM 逐项判断（视觉是否兑现） | 首个评测文本 → 可编辑动态 4D Blender 场景的基准 | arXiv 预印本 |
| 2026-07 | [Nova3D-Bench](https://arxiv.org/abs/2607.22738) | 54 项、6 个领域、3 档难度，含文本和图像输入 | 与 4 类共 11 个基线（mesh / 部件 / 代码 / CAD）对比 | Nova3D 在全部 54 项上都产出了可执行程序和有效的 GLB | arXiv 预印本 |
| 2026-09 | [3DHarnessBench](https://arxiv.org/abs/2609.06535) | 从单视图到完整 3D 交互，分 4 个层级 | 看 agent 能否把 3D 几何还原为 Blender 代码，工具权限逐级放开 | 给更多函数权限后所有前沿模型都显著提升，但提升幅度因模型而异 | arXiv 预印本 |

### 5. CAD 生成与 CAD agent

| 时间 | Benchmark | 规模 | 评测方式 | 关键发现 / SOTA | 状态 |
|---|---|---|---|---|---|
| 2024-09 | [Text2CAD](https://arxiv.org/abs/2409.17106) | 约 170K 个模型、约 660K 条从新手到专家的文本标注（基于 DeepCAD） | 评视觉质量、参数精度、几何精度 | 首个文本 → 参数化 CAD 序列的框架 | NeurIPS 2024 Spotlight |
| 2024-10 | [CADPrompt](https://arxiv.org/abs/2410.05340) | 200 条 prompt，配专家写的 CAD 代码 | 生成 CAD 脚本后比点云距离、成功率 | CADCodeVerify 让 GPT-4 的点云距离降 7.30%、成功率提 5.0% | arXiv 预印本 |
| 2025-05 | [VideoCAD](https://arxiv.org/abs/2505.24838) | 41K+ 段 Onshape 操作录屏，动作序列最长 186 步 | 学习 CAD 软件 UI 交互 + VQA 基准 | 任务时长比现有 UI 数据集长 20 倍；VideoCADFormer 提升最多约 20% | NeurIPS 2025 |
| 2026-05 | [CADTests（CADTestBench）](https://arxiv.org/abs/2605.07807) | 文本 → CAD，每题配可执行测试 | 用软件测试验证生成模型是否满足几何 / 拓扑要求 | 首个基于测试的 Text-to-CAD 基准；拿测试做引导的简单基线就超过了现有方法 | arXiv 预印本 |
| 2026-05 | [BenchCAD](https://arxiv.org/abs/2605.10865) | 17,900 个 CadQuery 程序、106 个零件族、47 项工业标准 | VQA、代码 QA、图像 → 代码、代码编辑；全部按执行结果确定性打分，不用 LLM judge | 外形大致对，但 sweep / loft / twist-extrude 常被简化成拉伸 | arXiv 预印本 |
| 2026-05 | [CADBench](https://arxiv.org/abs/2605.10873) | 18,000 例、6 个族、5 种输入模态 | 几何保真、可执行性、程序紧凑度，共 6 个指标 | 专用的 mesh → CAD 模型明显强于通用 VLM | arXiv 预印本 |
| 2026-05 | [Text2CAD-Bench](https://arxiv.org/abs/2605.18430) | 600 例人工整理，L1–L4 四级 | 每题两种风格 prompt：非专家的几何描述 + 专家的工序描述 | 超出了传统机械件和简单草图拉伸的范围 | arXiv 预印本 |
| 2026-05 | [MUSE](https://arxiv.org/abs/2605.28579) | 文本 → CAD，带设计意图 rubric | 三段式：代码检查 → 几何检查 → 可制造 / 功能 / 可装配 rubric（VLM judge） | 最强模型在细粒度工程标准上成功率仍有限 | arXiv 预印本 |
| 2026-08 | [CADEngBench](https://arxiv.org/abs/2608.09296) | 300 个零件（600 个任务）+ 150 组装配对 | B-Rep 有效性、DFM、参数扰动、CalculiX 有限元分析 + 装配运动学验证 | 改已有 CAD 比从零生成容易得多；复杂编辑和 FEA 仍然难 | arXiv 预印本 |
| 2026-09 | [CADWorld](https://arxiv.org/abs/2609.16251) | 200 个任务、11 类 CAD 工作流（草图 / 装配 / CAM / FEM 等） | computer-use agent 在真实 CAD 桌面软件中做长程操作，检查产出的原生工程文件 | 最强 agent 17.5%，专家参考 87.0% | arXiv 预印本 |

### 6. Text / Image-to-3D 资产质量评测

| 时间 | Benchmark | 规模 | 评测方式 | 关键发现 / SOTA | 状态 |
|---|---|---|---|---|---|
| 2023-10 | [T³Bench](https://arxiv.org/abs/2310.02977) | 300 条 prompt、3 档复杂度 | 基于多视角图像的质量指标 + 对齐指标（多视角 caption + LLM） | 6 种方法在多物体场景上普遍不行 | arXiv 预印本 |
| 2024-01 | [GPTEval3D](https://arxiv.org/abs/2401.04092) | 用 GPT-4V 生成评测 prompt 集 | GPT-4V 按用户自定准则两两比较，算 Elo | 与人类偏好在多个准则上都高度一致 | CVPR 2024 |
| 2024-12 | [GT23D-Bench](https://arxiv.org/abs/2412.09997) | 400K 个 3D 资产、100 万+ 条描述 | 10 个指标，覆盖文本-3D 对齐和纹理 / 多视角 / 几何质量 | 与人类判断的相关性明显高于现有指标 | arXiv 预印本 |
| 2024-12 | [MATE-3D](https://arxiv.org/abs/2412.11170) | 1,280 个网格、8 类 prompt、107,520 条标注 | 四维度主观评测 + HyperScore 评估器 | HyperScore 在多维质量评估上超过现有指标 | ICCV 2025 |
| 2025-03 | [3DGen-Bench](https://arxiv.org/abs/2503.21745) | 1,020 条 prompt、19 个模型产出的 11,220 个资产、68K+ 偏好投票 | 3DGen-Arena 众包两两对战 + 3DGen-Score / 3DGen-Eval 自动评估 | 首个大规模 3D 人类偏好数据集；自动评估器与人类排名相关性更高 | arXiv 预印本 |
| 2025-08 | [Hi3DEval](https://arxiv.org/abs/2508.05609) | Hi3DBench 大规模标注集 | 物体级 + 部件级分层评测，另评材质真实感 | 突破了只能在物体级用图像指标打分的局限 | arXiv 预印本 |

### 7. 游戏生成 / 游戏开发 agent

| 时间 | Benchmark | 规模 | 评测方式 | 关键发现 / SOTA | 状态 |
|---|---|---|---|---|---|
| 2025-09 | [V-GameGym](https://arxiv.org/abs/2509.20136) | 2,219 个 Pygame 样本、100 个主题簇 | 在 UI 沙箱中运行，评代码和视觉 | 评了 70 个模型，最好的也只有约 45% 成功 | ACL 2026 Findings |
| 2026-02 | [GameDevBench](https://arxiv.org/abs/2602.11103) | 333 个 Godot 任务（来自教程） | agent 改代码和资产（shader / sprite / 动画），测试验证 | 最佳 agent 约 54%（各版本 53.8%–54.5%）；2D 图形类只有 31.6%；加图像 / 视频反馈后 Sonnet 4.5 从 33.3% 升到 47.7% | arXiv 预印本 |
| 2026-04 | [PlayEval（PlayCoder）](https://arxiv.org/abs/2604.19742) | 43 个多语言 GUI 应用 / 游戏 | Play@k：PlayTester agent 实际去玩并检测逻辑错误 | 基线编译通过率高但 Play@3 接近 0；PlayCoder 达 Exec@3 38.1%、Play@3 20.3% | arXiv 预印本 |
| 2026-04 | [GBQA](https://arxiv.org/abs/2604.02648) | 30 个游戏、124 个人工确认的 bug | ReAct + 记忆 agent 长程探索找 bug | 最好模型找到 48.39% 的 bug | ICLR 2026 Workshop |
| 2026-05 | [PlaytestArena](https://arxiv.org/abs/2605.28258) | 200 个浏览器游戏生成任务、8 种类型 | GUI agent 实际游玩，对照行为 rubric 判定 | Play2Code（写码与试玩循环）rubric 通过率 66.8%，比单次生成高 37.1pp | arXiv 预印本 |
| 2026-06 | [GameCraft-Bench](https://arxiv.org/abs/2606.17861) | 140 个 Godot 任务、15 个游戏族 | 回放演示操作 + rubric 引导的多模态判分 | 最强 agent 41.46%，多数低于 40% | arXiv 预印本 |
| 2026-06 | [JAMER / JamBench](https://arxiv.org/abs/2606.19830) | 300 个人工核验的专业游戏引擎项目 | 编译通过率 + 结构完整度 SCS + 行为对齐度 BAS | 运行通过率从小项目 80.4% 跌到大项目 5.7%；瓶颈在架构设计，不在语法 | arXiv 预印本 |
| 2026-07 | [GameEngineBench](https://arxiv.org/abs/2607.03525) | 110 个 UE5 C++ 任务（来自 9 个真实仓库） | 必须编译通过并通过行为测试 | 最强配置 pass@1 55.5%，31 题所有配置都没解出来 | arXiv 预印本 |

### 8. 专业软件 GUI agent（只收视觉创作相关）

| 时间 | Benchmark | 规模 | 评测方式 | 关键发现 / SOTA | 状态 |
|---|---|---|---|---|---|
| 2024-04 | [OSWorld](https://arxiv.org/abs/2404.07972) | 369 个任务，其中含 GIMP 与 LibreOffice Impress 子集 | 真实 OS 环境，按执行结果判分 | 视觉创作相关部分是 GIMP 修图和 Impress 做幻灯片 | arXiv 预印本（会议待核） |
| 2025-04 | [ScreenSpot-Pro](https://arxiv.org/abs/2504.07981) | 23 个专业应用（含 Photoshop / Blender / Illustrator / UE 等）的高分辨率截图 | GUI 元素定位（grounding） | 现有模型 18.9%，ScreenSeekeR 不训练就到 48.1% | arXiv 预印本 |
| 2026-05 | [CutVerse](https://arxiv.org/abs/2605.19484) | 186 个长程任务、7 个专业应用（Premiere / Photoshop 等） | 录屏 + 日志解析成组合式动作轨迹来评测 | 现有 agent 任务成功率 36.0% | arXiv 预印本 |

另见第 5 类的 CADWorld（CAD 桌面软件里的 computer-use）、VideoCAD（Onshape 里的 UI 交互）、CANVAS（在设计软件里做 UI）。

### 未能核实

- **WebSight 的评测部分**
  - [WebSight](https://arxiv.org/abs/2403.09029) 是 2M 条截图-HTML 的合成训练集，论文里没有独立的评测集，所以不收进表
- **OSWorld 的状态**
  - 印象中已被 NeurIPS 2024 D&B 录用，但本次没有在官方页核实，表内先记「会议待核」
- **CAD-Recode**
  - [CAD-Recode](https://arxiv.org/abs/2412.14042)（ICCV 2025）确实存在，但它是方法论文：在 DeepCAD / Fusion360 / CC3D 上评测，没有提出新 benchmark，所以不收
- **MCPWorld**
  - [MCPWorld](https://arxiv.org/abs/2506.07672) 有 201 个任务、10 个应用，但摘要只写了 VS Code、OBS 等；搜索摘要里提到的 Blender 任务没能在原文核实，所以不收
- **WebDev Arena 当前榜首与 Elo**
  - 第三方聚合站给出的榜首和 Elo 互相矛盾，所以表内只写官方博客的机制和投票量
- **缺数字的条目**
  - 以下条目的摘要里没有样本数或最佳模型分数，表内只写定性结论，未编造数字
  - FullFront、WebCompass、LiveEvalBench、WebGen-V、SArena、MUSE、Hi3DEval、3DHarnessBench、BlenderBench、1D-Bench
- **状态没有写会议名的条目**
  - WebGen-Bench、Plot2Code、ArtifactsBench 等可能已被会议录用，但本次只在 arXiv 页核实过，所以一律记「arXiv 预印本」

- 视频即代码口径：LLM / agent 写可执行动画代码，渲染器出视频/动画；含教学动画、矢量/图表/Lottie、幻灯片与演讲视频、全代码成片四组，以及图即代码的静态邻居（已标注）
- 存疑条目 ManiBench（2603.13251）因 ID/日期自相矛盾、来源可疑、仅 12 题 pilot，未收入

### 9. 视频即代码 · 教学动画

| 时间 | Benchmark | 规模 | 评测方式 | 关键发现 / SOTA | 状态 |
|---|---|---|---|---|---|
| 2025-02 | [TheoremExplainBench](https://arxiv.org/abs/2502.19400) | 240 定理，4 学科，3 难度各 80 | 5 项自动指标（LLM 评文本 / 视频 / 关键帧），几何平均 | o3-mini 成功率 93.8% / 总分 0.77；Element Layout 为普遍弱项 | ACL 2025 Oral |
| 2025-10 | [Code2Video · MMMC](https://arxiv.org/abs/2510.01174) | 117 主题 / 13 学科 / 339 子片 = 456 单元 | VLM 观感 5 轴 + TeachQuiz（遗忘后看视频答题）+ 代码效率 | 较直接写码 +40%；Opus 4.1 TeachQuiz 86.0，扩散基线 Veo3 仅 2.5 | ICML 2026 |
| 2025-10 | [DTVBench · JanusCoder](https://arxiv.org/abs/2510.23538) | 102 可视化任务（含 Manim、Mathematica） | 文本 / 视觉双向代码任务 | 7–14B 开源逼近或超过商用模型 | ICLR 2026 |
| 2025-11 | [VisualEDU](https://aclanthology.org/2025.findings-emnlp.889/) | 200 题，6 类 × 3 难度 | 时间一致性 / 逻辑正确性 / 视觉清晰度，9 个 VLM | 难题上 Claude-3.7-Sonnet、GPT-4o 均 <56% | EMNLP 2025 Findings |
| 2026-02 | [SimuScene](https://arxiv.org/abs/2602.10840) | 7,659 场景 / 52 概念 / 5 域（334 测试） | 代码渲染视频后 VLM 逐条二元 Code-Video-Judge 奖励（GRPO） | 最强 LLM 仅 21.5% Avg@8；RL 后 32B 达 72.2% Pass@8 | arXiv 预印本 |

### 10. 视频即代码 · 矢量 / 图表 / Lottie

| 时间 | Benchmark | 规模 | 评测方式 | 关键发现 / SOTA | 状态 |
|---|---|---|---|---|---|
| 2023-10 | [AutomaTikZ](https://arxiv.org/abs/2310.00367) | DaTikZ 120k caption↔TikZ 对 | 人工 + 自动相似度（CLIPScore / 图像相似） | CLiMA / LLaMA 微调相似度优于 GPT-4、Claude 2〔图即代码·静态〕 | ICLR 2024 |
| 2024-05 | [DeTikZify](https://arxiv.org/abs/2405.15306) | DaTikZv2 360k+，另含 SketchFig / MetaFig | 自动 + 人工，推理期 MCTS 自精炼（编译器反馈） | 草图 / 图逆向 TikZ 优于 Claude 3、GPT-4V〔图即代码·静态〕 | NeurIPS 2024 |
| 2024-06 | [ChartMimic](https://arxiv.org/abs/2406.09961) | 4,800 组（图，指令，代码）三元组 | 多层级自动指标，同时评代码与渲染图 | 即便 GPT-4o 仍有明显差距，远未饱和〔图表即代码·静态邻居〕 | ICLR 2025 Spotlight |
| 2024-11 | [DiagramAgent](https://arxiv.org/abs/2411.11916) | 生成 / 编码 6,983 对、编辑 1,600、8 类图 | Pass@1 / CodeBLEU / CLIP-FID / LPIPS + 人工 1–5 | 生成 Pass@1 58.15，编辑 98.00〔图即代码·静态〕 | CVPR 2025 |
| 2025-10 | [DCG-Bench · OpusAnimation](https://arxiv.org/abs/2510.03341) | 700 测试（属 DCG-8K 约 8K） | 执行通过率 + 代码 QA + 视频 QA（Gemini-2.5-Pro 评） | 自研 3B 专家比最强开源 MLLM 平均 +8.31%；唯一动画图表代码基准 | arXiv 预印本 |
| 2025-11 | [MermaidSeqBench](https://arxiv.org/abs/2511.14967) | 132 NL↔Mermaid 时序图对 | 双判官 LLM-as-judge 6 维（语法 / 逻辑 / 错误追踪） | 排名随判官翻转〔图即代码·静态〕 | arXiv 预印本 |
| 2025-12 | [Vector Prism](https://arxiv.org/abs/2512.14336) | 114 指令–SVG 测试对 | GPT-T2V 指令遵循 + 用户研究 + 文件体积 | GPT-T2V 76.1 vs Sora 2 69.1，矢量输出比视频小 54× | arXiv 预印本 |
| 2026-03 | [MMLottieBench · OmniLottie](https://arxiv.org/abs/2603.02138) | 900 条（真 450 + 合成 450），三任务 | FVD + CLIP + Claude-3.5 判对齐（0–10），视频任务加 PSNR/SSIM | OmniLottie 成功率 93.3%，FVD 180 vs AniClipart 266 | CVPR 2026 |
| 2026-04 | [Graphic-Design-Bench](https://arxiv.org/abs/2604.04192) | 约 50 任务，含约 50 条 Lottie 动画子集 | LottieFiles 五帧算 FrameSSIM / FrameMSE，另有五轴 | 动画远难于静态：最佳 Lottie FrameSSIM 0.598 | arXiv 预印本 |
| 2026-05 | [VAnim · SVGAnim-134k](https://arxiv.org/abs/2605.01517) | 134k（SFT 123k / RL 10k / 测试 1k） | PE-Core 语义对齐 + 渲染成功率 + 15 人用户研究 | 对齐 0.281 vs Gemini3 Pro 0.243，成功率 100%，序列压缩 9.8× | ICML 2026 |

### 11. 视频即代码 · 幻灯片与演讲视频

| 时间 | Benchmark | 规模 | 评测方式 | 关键发现 / SOTA | 状态 |
|---|---|---|---|---|---|
| 2025-01 | [AutoPresent · SlidesBench](https://arxiv.org/abs/2501.00912) | 310 decks / 10 域 → 7k 训练 + 585 测试 | reference-based 相似度 + reference-free 设计质量 VLM 判 | 8B AutoPresent 达到与 GPT-4o 相当，程序化优于端到端图像 | CVPR 2025 |
| 2025-01 | [PPTAgent · PPTEval](https://arxiv.org/abs/2501.03936) | 50 参考 + 50 文档 = 500 任务，源集 Zenodo10K | PPTEval 三维（Content / Design / Coherence）VLM + 成功率 | 成功率 95.0%（GPT-4o 97.8%），均分 3.67 | EMNLP 2025 |
| 2025-05 | [Paper2Poster · PaperQuiz](https://arxiv.org/abs/2505.21497) | 约 100 论文–海报对（近期会议） | 四轴 Visual / Textual / Holistic + PaperQuiz（看海报答题） | 开源 Qwen2.5 版多指标超 GPT-4o 多 agent，省 87% token | NeurIPS 2025 D&B |
| 2025-07 | [PresentAgent · PresentEval](https://arxiv.org/abs/2507.04036) | 30 文档–演讲对（Doc2Present） | VLM 三维 + quiz 答题 + 音视频打分 | 接近人类：quiz 0.64（人类 0.56） | EMNLP 2025 Demo |
| 2025-10 | [Paper2Video](https://arxiv.org/abs/2510.05096) | 101 篇论文（配讲者视频 + 幻灯片） | Meta Similarity + PresentArena + PresentQuiz + IP-Memory | PresentQuiz 0.842 超人类 0.738；端到端视频模型各项垫底 | NeurIPS 2025 SEA WS |

### 12. 视频即代码 · 全代码成片与交互

| 时间 | Benchmark | 规模 | 评测方式 | 关键发现 / SOTA | 状态 |
|---|---|---|---|---|---|
| 2025-07 | [ArtifactsBench](https://arxiv.org/abs/2507.04952) | 1,825 任务（Web 组件 / SVG / 小游戏） | 程序化渲染抓三步时序截图 + MLLM judge 逐题 checklist | 与 WebDev Arena 排名一致 94.4%，与专家两两 >90% | arXiv 预印本 |

