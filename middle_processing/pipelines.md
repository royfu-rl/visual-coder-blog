# 视觉交互 Coding · 开源数据管线 / 训练数据总表

> 截至 2026-09-23。每条都在 arXiv（API 元数据 + HTML 正文）、GitHub 或 HF 上核实过。
> 「开源」列：`是` = 数据可下载（给出 HF/GitHub）；`仅模型/代码` = 数据未放出；`承诺` = 论文说「将开源」，但写作时找不到链接；`—` = 纯方法或框架，没有独立的数据集。
> 规模一律按论文或数据卡原文写；原文没说的写 `—`。

---

### 总表 · Web / UI 代码

| 时间 | 名称 | 数据形态 | 规模 | 生成方式 | 开源 |
|---|---|---|---|---|---|
| 2017-05 | [pix2code](https://arxiv.org/abs/1705.07962) | GUI 截图 → DSL 代码（iOS/Android/Web） | 3 平台合成 GUI | 由 DSL 随机合成 GUI 再渲染，最早的截图→代码配对数据 | 是 |
| 2024-03 | [WebSight](https://arxiv.org/abs/2403.09029) | 截图 → HTML(+Tailwind) 对 | v0.1 823K；v0.2 2M | LLM 先生成网站主题，再由代码 LLM 写 HTML，最后用 Playwright 渲染截图，全程纯合成 | 是 [HF](https://huggingface.co/datasets/HuggingFaceM4/WebSight) |
| 2024-03 | [Design2Code](https://arxiv.org/abs/2403.03163)（训练部分） | 截图 → HTML | 训练用 WebSight 随机 20%（约 165K）；测试集 484 张真实网页 | 没有独立训练集：Design2Code-18B 用 CogAgent-18B 在 WebSight 子集上微调，试过 C4 真实网页因太长太噪而放弃 | 测试集是 |
| 2024-04 | [Vision2UI → WebCode2M](https://arxiv.org/abs/2404.06369) | 设计图 → 网页代码 + 布局信息 | v1（Vision2UI）2K；v2 2.56M | 抓 Common Crawl 真实网页，渲染后用打分模型滤掉审美差、元素不全的样本 | 是 [HF](https://huggingface.co/datasets/xcodemind/webcode2m) |
| 2024-06 | [UICoder](https://arxiv.org/abs/2406.07739) | 文本 → SwiftUI 代码（自生成） | 5 轮，每轮 10~20 万，累计近 100 万段程序 | StarChat 自己生成，再用编译器 + CLIP 分数 + 密度去重狠滤（首轮通过率 0.4%），然后迭代自训 | 论文称放出（链接未核实） |
| 2024-06 | [Web2Code](https://arxiv.org/abs/2406.20098) | 截图 → HTML + 网页 QA | 1,179.7K 条（884.7K 代码 + 295K QA） | GPT-3.5 生成 60K 新网页，GPT-4 精修 WebSight/pix2code 824.7K 条，另加 WebSRC QA | 是 [HF](https://huggingface.co/datasets/MBZUAI/Web2Code) |
| 2024-10 | [Sketch2Code](https://arxiv.org/abs/2410.16232) | 手绘草图 → HTML（含多轮交互评测） | 731 张草图 / 484 个网页 | 人工按线框规范为 Design2Code 网页手绘草图，并用模拟用户做多轮反馈 | 是 [HF](https://huggingface.co/datasets/SALT-NLP/Sketch2Code) |
| 2024-11 | [Interaction2Code](https://arxiv.org/abs/2411.03292) | 交互前后截图 → 交互式网页代码 | 127 个网页 / 374 个交互 | 人工整理真实网页的交互原型，覆盖 15 类页面、31 类交互（评测集） | 评测集 |
| 2025-05 | [WebGen-Bench / WebGen-Instruct](https://arxiv.org/abs/2505.03733) | 指令 → 多文件网站代码库 + GUI-agent 测试用例 | 训练指令 6,667 条；测试 101 条指令 / 647 条用例 | 人工 + GPT-4o 写指令，GPT-4o 生成功能用例后人工筛；在 Bolt.diy 轨迹上 SFT | 是 [HF](https://huggingface.co/datasets/luzimu/WebGen-Bench_train_data) |
| 2025-07 | [ArtifactsBench](https://arxiv.org/abs/2507.04952) | 交互式 artifact 代码 + 时序截图 + 逐题 checklist | 1,825 题 | 渲染后按时间序列截图，由 MLLM-as-Judge 对照逐题 checklist 打分（可直接当 reward 模板） | 是 [HF](https://huggingface.co/datasets/tencent/ArtifactsBenchmark) |
| 2025-07 | [ScreenCoder](https://arxiv.org/abs/2507.22827) | 截图 → HTML | Screen-10K（9K SFT + 1K RL） | 爬 5 万网页后自动过滤；grounding → planning → generation 三个 agent 充当数据引擎；RL 奖励为 −MSE | 代码是；数据集见 [HF](https://huggingface.co/datasets/Leigest/ScreenCoder)（未逐一核对内容） |
| 2025-09 | [WebGen-Agent](https://arxiv.org/abs/2509.22644) | 多步 agent 轨迹（代码 + 截图分 + GUI-agent 分） | 约 700 条 SFT 轨迹 + 500 条 Step-GRPO 指令 | DeepSeek-V3 跑 agent 采轨迹；每步用 VLM 截图打分（0~5）和 GUI-agent 测试打分（1~5），两者相加作为逐步奖励 | 是 [HF](https://huggingface.co/datasets/luzimu/webgen-agent_train_sft) |
| 2025-10 | [WebRenderBench / ALISA](https://arxiv.org/abs/2510.04097) | 截图 → 网页代码 + 布局/样式一致性奖励 | 45.1K 真实门户网页 | 爬真实门户网站；从渲染结果算布局和样式一致性，作为 RL reward | 是 [HF](https://huggingface.co/datasets/aleversn/WebRenderBench) |
| 2025-10 | [ReLook](https://arxiv.org/abs/2510.11498) | 生成 → 诊断 → 修复 RL 轨迹 | 3,000 个纯前端任务 | Qwen2.5-VL-72B 看截图当 critic 打分；渲染失败直接给 0；只接受严格变好的修订（Forced Optimization） | 承诺 |
| 2025-11 | [WebVIA](https://arxiv.org/abs/2511.06251) | 多状态交互截图 → 交互式 HTML/CSS/JS；探索轨迹 | WebView 11K 网页（每页 4~6 个交互状态）；探索数据约 180K 条 / 20K 网页 | 合成网页 → agent 探索并截取多状态 → Claude-Sonnet-4 生成交互代码 → 验证模块确认交互确实生效 | 仅模型 |
| 2025-11 | [UI2Code^N](https://arxiv.org/abs/2511.08195) | 截图 → HTML；起草 / 打磨 / 编辑三种多轮任务 | CPT 约 20M；SFT 约 80K；RL 约 42K | 先造复杂 HTML 真值，再逆向合成「待打磨」的输入；RVPO 用 GLM-4.5V 做相对排序奖励 | 仅模型（明确不放数据） |
| 2026-03 | [AnyDoc / DocHTML](https://arxiv.org/abs/2603.25118) | 意图 / 截图 / 元素 → HTML/CSS 文档 | 265,206 份，111 类，32 种风格 | 文档库抽元数据 → InternVL3 标注意图 → Qwen3-Coder-480B 写 HTML → FLUX 生成配图 → 渲染后过滤溢出；HARL 以高度比作奖励 | 未见链接 |
| 2026-08 | [MT-Web2Code](https://arxiv.org/abs/2608.03474) | 多轮区域重建 / 局部修改的修复轨迹 | 102 页 × 5 轮 | 反向腐蚀引擎：往金标准页面注入结构或样式缺陷（设像素变化阈值），再把过程倒过来就得到确定性的修复轨迹 | 承诺 |

### 总表 · 图表 / SVG / TikZ 代码

| 时间 | 名称 | 数据形态 | 规模 | 生成方式 | 开源 |
|---|---|---|---|---|---|
| 2023-09 | [AutomaTikZ / DaTikZ](https://arxiv.org/abs/2310.00367) | caption ↔ TikZ 代码 | 120K | 从 arXiv、TeX.SE 等处收集真实 TikZ 并对齐 caption | 是 [HF](https://huggingface.co/datasets/nllg/datikz) |
| 2023-12 | [StarVector / SVG-Stack](https://arxiv.org/abs/2312.11556) | 图像 / 文本 → SVG 代码 | 2M | 从 The Stack 抽 SVG，经清洗、渲染后得到配对 | 是 [HF](https://huggingface.co/datasets/starvector/svg-stack) |
| 2024-05 | [DeTikZify / DaTikZv2](https://arxiv.org/abs/2405.15306) | 科研图 / 草图 → TikZ | 360K+ | 人写 TikZ 加合成草图；推理时用 MCTS 迭代精修 | 是 [HF](https://huggingface.co/datasets/nllg/datikz-v2)（部分，受许可证限制） |
| 2024-10 | [ReachQA (CIT)](https://arxiv.org/abs/2410.18798) | 绘图代码 → 图表 + 推理 QA | 3K 图 / 20K QA | 以代码为中介：LLM 扩写 matplotlib 代码并渲染，再基于代码生成推理 QA | 是 [HF](https://huggingface.co/datasets/hewei2001/ReachQA) |
| 2024-12 | [LLM4SVG / SVGX-SFT](https://arxiv.org/abs/2412.11102) | 文本 ↔ SVG 指令数据 | 580K 条指令（HF 版名为 1M） | 人工设计的 SVG 经自动管线生成理解和生成两类指令 | 是 [HF](https://huggingface.co/datasets/xingxm/SVGX-SFT-1M) |
| 2025-01 | [ChartCoder / Chart2Code-160k](https://arxiv.org/abs/2501.06598) | 图表 → Python 绘图代码（+ Snippet-of-Thought） | 160K | LLM 合成多类型图表代码并执行渲染；SoT 把直接生成改写成分步生成 | 是 [HF](https://huggingface.co/datasets/xxxllz/Chart2Code-160k) |
| 2025-02 | [CoSyn-400K](https://arxiv.org/abs/2502.14846) | 代码（Python/HTML/LaTeX…）渲染出的富文本图 + 指令 | 400K 图 / 2.7M 条指令 | 纯文本 LLM 按领域主题写渲染代码，再基于代码生成 QA | 是 [HF](https://huggingface.co/datasets/allenai/CoSyn-400K) |
| 2025-04 | [OmniSVG / MMSVG-2M](https://arxiv.org/abs/2504.06263) | 文本 / 图像 → SVG（Icon / Illustration / Character） | 2M（1.1M + 0.5M + 0.4M） | 爬 Iconfont、IconScout、Freepik；CairoSVG 渲染后用 BLIP-2 写 caption，CLIP 分 < 30 的滤掉 | 部分 [HF Icon](https://huggingface.co/datasets/OmniSVG/MMSVG-Icon) / [Illustration](https://huggingface.co/datasets/OmniSVG/MMSVG-Illustration) |
| 2025-05 | [ChartGen](https://arxiv.org/abs/2507.19492) | 图表 ↔ 代码（27 类，11 个绘图库） | 222.5K 对（种子 13K） | VLM 把种子图重建成脚本，代码 LLM 迭代扩增变体 | 是（论文称开源） |
| 2025-05 | [ChartGalaxy](https://arxiv.org/abs/2505.18668) | 信息图表 + 数据表 + D3.js 代码 | 1.70M 合成 + 61.8K 真实（真实图只给 URL） | 从真实信息图归纳出 75 类图、440 种变体、68 个布局模板，再用 D3 程序化合成 | 是 [HF](https://huggingface.co/datasets/ChartGalaxy/ChartGalaxy) |
| 2025-05 | [RLRF](https://arxiv.org/abs/2505.20793) | 图像 → SVG 的 RL rollout | SFT 1.7M；RL 20K 条高熵样本 | 数据取自 SVG-Stack；奖励 = L2/边缘 L2 + DreamSim + 代码长度惩罚 | 未明确 |
| 2025-05 | [Reason-SVG / SVGX-DwT-10k](https://arxiv.org/abs/2505.24499) | 设计推理（DwT）+ SVG | 10K | 先写显式设计推理再写 SVG；GRPO 用混合奖励（结构、语义、视觉） | 未明确 |
| 2025-06 | [VisCoder / VisCode-200K](https://arxiv.org/abs/2506.03930) | 指令 → Python 绘图代码 + 多轮执行纠错 | 200K+（含 45K 多轮纠错） | 从开源仓库抽可执行绘图代码并渲染验证；纠错对话取自 Code-Feedback | 是 [HF](https://huggingface.co/datasets/TIGER-Lab/VisCode-200K) |
| 2025-08 | [UniSVG](https://arxiv.org/abs/2508.07766) | 文本 / 图像 → SVG；SVG 理解 | 525K | 整合多源 SVG，统一成生成 + 理解两类任务 | 是 [HF](https://huggingface.co/datasets/lili24/UniSVG) |
| 2025-08 | [SVGen / SVG-1M](https://arxiv.org/abs/2508.09168) | 文本 → SVG（含 CoT 子集） | 1M | 数据增强 + 标注，训练走课程学习 + RL | 是 [GitHub](https://github.com/gitcat-404/SVGen) |
| 2025-08 | [ChartMaster / ReChartPrompt-240K](https://arxiv.org/abs/2508.17608) | 真实 arXiv 图表 → 代码 | 240K | 用 arXiv 真实图表当 prompt 生成代码；ChartSimRL 奖励 = 属性相似度 + CNN 视觉相似度 | 是 [HF](https://huggingface.co/datasets/TwT-6/ReChartPrompt-240K) |
| 2025-10 | [InternSVG / SAgoge](https://arxiv.org/abs/2510.11341) | SVG 理解 / 编辑 / 生成，含动画 | 约 16M 训练样本 | 爬 Iconfont、SVGRepo 等，PubChem 经 OpenBabel 转 SVG，合成插画和动画，多个 MLLM 负责标注 | 是 [HF](https://huggingface.co/datasets/InternSVG/SAgoge) |
| 2025-10 | [VisCoder2 / VisCode-Multi-679K](https://arxiv.org/abs/2510.23642) | 12 种语言可视化代码 + 多轮纠错 | 679K（其中纠错对话 66K+） | 从 the-stack-v2、svg-diagrams、CoSyn 抽代码 → 在 Jupyter 执行验证 → GPT-4.1 写五段式指令 | 是 [HF](https://huggingface.co/datasets/TIGER-Lab/VisCode-Multi-679K) |
| 2025-11 | [VinciCoder](https://arxiv.org/abs/2511.00391) | 图 → 代码（图表 / Web / SVG / TikZ / 化学），含「看图修代码」 | SFT 1.3M 直接生成 + 300K 修正；RL 42K | 汇总各域开源数据；让初版模型产出不完美代码，组成修正对；ViRL 用 DINOv2 多尺度 patch 相似度做奖励 | 是 [HF](https://huggingface.co/datasets/DocTron-Hub/VinciCoder-1.6M-SFT) |

### 总表 · 3D / Blender / CAD 代码

| 时间 | 名称 | 数据形态 | 规模 | 生成方式 | 开源 |
|---|---|---|---|---|---|
| 2021-05 | [DeepCAD](https://arxiv.org/abs/2105.09492) | CAD 构造序列（sketch-extrude） | 178,238 个模型 | 从 Onshape 公开模型解析出构造序列 | 是 [GitHub](https://github.com/ChrisWu1997/DeepCAD) |
| 2023-06 | [Infinigen](https://arxiv.org/abs/2306.09310) | 程序化生成器（Blender）→ 自然场景 / 资产 | 无上限 | 形状和纹理全部由随机数学规则生成，可当代码 → 3D 的数据源 | 是 [GitHub](https://github.com/princeton-vl/infinigen) |
| 2024-03 | [SceneCraft](https://arxiv.org/abs/2403.01248) | 文本 → Blender 场景脚本 + 可复用函数库 | —（方法） | 用场景图约束写脚本，GPT-V 看渲染图迭代修改；library learning 把常用函数沉淀成库 | 未找到官方仓库 |
| 2024-06 | [Infinigen Indoors](https://arxiv.org/abs/2406.11824) | 程序化室内资产 + 约束 DSL | 无上限 | 程序化家具和建筑资产，加上约束求解器负责排布 | 是（BSD） |
| 2024-09 | [Text2CAD](https://arxiv.org/abs/2409.17106) | 多级文本 → CAD 序列 | 约 170K 模型 / 660K 条文本 | Mistral + LLaVA-NeXT 为 DeepCAD 生成从初级到专家级的描述 | 是 [HF](https://huggingface.co/datasets/SadilKhan/Text2CAD) |
| 2024-11 | [CAD-MLLM / Omni-CAD](https://arxiv.org/abs/2411.04954) | 文本 + 多视图 + 点云 + 命令序列 | 约 450K | 给每个 CAD 模型配齐多模态数据 | 是 [HF](https://huggingface.co/datasets/jingwei-xu-00/Omni-CAD) |
| 2024-12 | [CAD-Recode](https://arxiv.org/abs/2412.14042) | 点云 → CadQuery Python 代码 | 1M 程序化序列 | 3~8 个图元做布尔运算 → 拉伸 → 合并；BRepCheck 校验 + 去重 | 是 [HF](https://huggingface.co/datasets/filapro/cad-recode) |
| 2024-12 | [BlenderLLM / BlendNet](https://arxiv.org/abs/2412.14203) | 指令 → Blender 建模脚本 | 12,059 条 | 2K 人工标注 + 10K GPT-4o 标注，之后自我改进迭代 | 是 [HF](https://huggingface.co/datasets/FreedomIntelligence/BlendNet) |
| 2025-01 | [CADFusion](https://arxiv.org/abs/2501.19054) | 文本 → CAD 序列 + 渲染偏好 | — | 序列学习与视觉反馈两阶段交替：渲染结果被偏好的序列得奖励 | 代码 [GitHub](https://github.com/microsoft/CADFusion) |
| 2025-04 | [BlenderGym](https://arxiv.org/abs/2504.01786) | 基于代码的 3D 重建 / 编辑评测 | — | 起始场景加目标渲染图，VLM 写 Blender 代码去逼近目标 | 是 [GitHub](https://github.com/richard-guyunqi/BlenderGym-Open) |
| 2025-05 | [CAD-Coder（VLM 版）/ GenCAD-Code](https://arxiv.org/abs/2505.14646) | CAD 图像 → CadQuery | 163K+ | 把 GenCAD 的模型转成 CadQuery 代码并渲染出图 | 是 [HF](https://huggingface.co/datasets/CADCODER/GenCAD-Code) |
| 2025-05 | [CAD-Coder（文本版）](https://arxiv.org/abs/2505.19713) | 文本 → CadQuery → 3D 三元组 | 110K + 1.5K CoT | DeepSeek-V3 为 Text2CAD 生成多个候选 → 执行 → 取 Chamfer 距离最小者；RL 奖励为 CD | 未明确 |
| 2025-05 | [cadrille](https://arxiv.org/abs/2505.22914) | 点云 / 图像 / 文本 → CAD 代码 | 复用程序化数据 | 在程序化数据上 SFT，再用程序化几何反馈做在线 GRPO | 代码 [GitHub](https://github.com/col14m/cadrille) |
| 2025-08 | [LL3M](https://arxiv.org/abs/2508.08228) | 文本 → Blender 代码（多 agent） | —（方法） | 规划、检索、写代码、调试、看图自评；检索库由 Blender API 文档构建 | 代码 [GitHub](https://github.com/threedle/ll3m) |
| 2025-08 | [MeshCoder](https://arxiv.org/abs/2508.14879) | 点云 → 分部件 Blender Python 代码 | 部件约 10M 对；对象约 1M 对 / 41 类（HF 放出 100K） | 自定义 Blender API 合成部件对；对象取自 Infinigen Indoor，逐部件转成代码后拼装，CD 超阈值的丢弃 | 是 [HF](https://huggingface.co/datasets/InternRobotics/MeshCoderDataset) |
| 2026-05 | [BlenderRAG](https://arxiv.org/abs/2605.00632) | 文本 + Blender 代码 + 渲染图 | 500 条 / 50 类 | Claude Opus 4.1 写初稿，专家校验修正；用于检索增强 | 是 [GitHub](https://github.com/MaxRondelli/BlenderRAG) |

### 总表 · 3D 资产原料与标注

| 时间 | 名称 | 数据形态 | 规模 | 生成方式 | 开源 |
|---|---|---|---|---|---|
| 2022-12 | [Objaverse](https://arxiv.org/abs/2212.08051) | 3D 模型 + 名称 / 标签 / 描述 | 800K+ | 采自 Sketchfab，保留 CC 许可的模型 | 是 [HF](https://huggingface.co/datasets/allenai/objaverse) |
| 2023-06 | [Cap3D](https://arxiv.org/abs/2306.07279) | 3D ↔ 文本 caption | 660K | 多视图渲染 → 图像 caption → CLIP 对齐 → LLM 汇总 | 是 [HF](https://huggingface.co/datasets/tiange/Cap3D) |
| 2023-07 | [Objaverse-XL](https://arxiv.org/abs/2307.05663) | 3D 对象（多来源） | 10M+ | 汇总 GitHub、Thingiverse、Sketchfab 等来源并去重 | 是 [GitHub](https://github.com/allenai/objaverse-xl) |
| 2023-11 | [G-Objaverse（RichDreamer）](https://arxiv.org/abs/2311.16918) | 多视图 RGB / albedo / normal / depth 渲染 | 约 280K 对象，约 6.5TB | 用统一相机和光照批量渲染 Objaverse，按 10 大类整理 | 是 [HF](https://huggingface.co/datasets/3DAIGC/gobjaverse) |
| 2024-04 | [DiffuRank](https://arxiv.org/abs/2404.07984) | 3D ↔ caption（纠正幻觉） | 修正 200K，扩展到 1M | 用 text-to-3D 模型给渲染视角排序，只把高排名的视角送给 GPT-4V | 是（并入 Cap3D） |
| 2024-12 | [GT23D-Bench 400K](https://arxiv.org/abs/2412.09997) | 清洗后的 3D + 64 视图 + 多粒度 caption | 400K 资产 / 70M+ 视觉样本 / 1M+ caption | Objaverse 按碎片、无纹理、LLaVA 语义、CLIP 和美学分位数过滤 | 承诺 |
| 2025-04 | [Objaverse++](https://arxiv.org/abs/2504.07334) | 质量 / 属性标签 | 10K 人工标注 → 约 500K 自动标注 | 人工标 10K 后训练分类器，推广到全量 | 是 [HF](https://huggingface.co/datasets/cindyxl/ObjaversePlusPlus) |

### 总表 · 游戏

| 时间 | 名称 | 数据形态 | 规模 | 生成方式 | 开源 |
|---|---|---|---|---|---|
| 2023-02 | [MarioGPT](https://arxiv.org/abs/2302.05981) | 文本 → 瓦片关卡（字符网格） | — | 用 VGLC 马里奥关卡微调 GPT-2，借新颖性搜索开放式扩增 | 代码 [GitHub](https://github.com/shyamsn97/mario-gpt) |
| 2023-02 | [Level Generation Through LLMs](https://arxiv.org/abs/2302.05817) | Sokoban 关卡文本 | — | LLM 生成关卡再做可玩性校验；性能随数据量明显提升 | — |
| 2024-03 | [IDGE](https://arxiv.org/abs/2404.00276) | 游戏规则 + 动作 → 下一状态 | — | 课程式 next-state prediction，以扑克为例 | — |
| 2025-05 | [Game-RL / Code2Logic / GameQA](https://arxiv.org/abs/2505.13886) | 游戏代码驱动的可验证 VQA | 30 个游戏 / 158 类任务（HF 140K） | 改写游戏代码，批量产出状态图、问题和真值，难度可控 | 是 [HF](https://huggingface.co/datasets/OpenMOSS-Team/GameQA-140K) |
| 2025-09 | [V-GameGym](https://arxiv.org/abs/2509.20136) | 需求 → Pygame 代码 + 运行视频 | 2,219 个游戏 / 100 个簇 | 从 OpenCoder、The Stack v2 筛 pygame 代码 → KMeans 聚类取优 → Claude 改成自动演示并在沙箱验证 → 人工复核 | 未找到数据链接 |
| 2025-10 | [Code World Models](https://arxiv.org/abs/2510.04542) | 规则 + 轨迹 → 可执行 Python 世界模型 | 10 个游戏 | LLM 把规则翻译成状态转移和合法动作代码，供 MCTS 使用 | — |
| 2026-02 | [GameDevBench](https://arxiv.org/abs/2602.11103) | 游戏开发任务（着色器、精灵、动画） | 333 题 | 从网页和视频教程提炼任务 | 未核实 |
| 2026-04 | [OpenGame / GameCoder-27B](https://arxiv.org/abs/2604.18394) | 设计 → Phaser 网页游戏工程 | 未披露 | 继续预训练用 Phaser/JS 游戏仓库；SFT 由 codex 出题、minimax 写解；RL 以单测通过率为奖励；评测用无头浏览器 + VLM | 仅框架 [GitHub](https://github.com/leigest519/OpenGame) |
| 2026-05 | [GameCWM 蒸馏](https://arxiv.org/abs/2605.24375) | 规则 → 游戏代码世界模型 | 30 个游戏 | SFT + RLVR，按结构和语义性质验证生成的代码 | 未明确 |
| 2026-09 | [PlayTrain](https://arxiv.org/abs/2609.09059) | 规格 → 单文件 JS 游戏（同时是 RL 环境） | 24 个游戏套件（16 个 ProcGen + 8 个 Atari 克隆） | LLM 按固定环境接口写 JS 游戏，直接接入 gym 训练像素 agent | 未核实（[官网](https://playtrain.org/)） |

---

### 深度拆解

#### WebGen-Agent（2025-09）

- **定位**：用截图打分和 GUI-agent 测试给网站生成 agent 提供逐步奖励，是目前少见的「多轮修复轨迹 + 过程奖励」开源组合。
<figure class="paper-fig"><img src="../assets/papers/webgen-agent-fig1.png" alt="WebGen-Agent · Fig. 1：带截图与 GUI-agent 反馈的迭代生成（轨迹采集）"><figcaption>WebGen-Agent · Fig. 1：带截图与 GUI-agent 反馈的迭代生成（轨迹采集）</figcaption></figure>

<figure class="paper-fig"><img src="../assets/papers/webgen-agent-fig2.png" alt="WebGen-Agent · Fig. 2：Step-GRPO，每步奖励 = 截图分 + GUI 分"><figcaption>WebGen-Agent · Fig. 2：Step-GRPO，每步奖励 = 截图分 + GUI 分</figcaption></figure>

- **管线步骤**（对照上面两张图，从左往右读）
  - Fig. 1 · 采轨迹
    1. **Instruction → `Code_t`**：从 WebGen-Instruct（6,667 条）取指令，编码 LLM 生成或修改多文件代码库
    2. **Reflection with Execution Feedback**：装依赖、启动服务；报错就带着报错信息反思重写，直到跑通得到 `Code_t+1`
    3. **Web Service → VLM**：页面截图交给 VLM，输出描述、外观分（0–5）和修改建议
    4. **GUI Agent**：外观达标后，按功能执行测试并打分（1–5）
    5. **顶部回路 `Feedback_t`**：截图反馈 + GUI 测试反馈拼进下一轮；连续 5 次执行报错就回溯到最优步；结束时按「GUI 分优先、截图分次之」挑出最佳步
  - Fig. 2 · 训练
    6. **SFT**：用约 700 条 DeepSeek-V3 轨迹
    7. **Step-GRPO**：同一指令展开 K 步，每步奖励 `r_k = r_SHOT + r_GUI`；所有轨迹的步奖励放进集合 R 做归一化（图右框）；500 条指令 × 5 个采样
- **关键数字**
  - Claude-3.5-Sonnet 接上这套 agent 后：准确率 26.4% → 51.9%
  - Qwen2.5-Coder-7B：原始 12.4%，SFT 后 38.9%，Step-GRPO 后 45.4%
  - 人工核验打分准确率：截图分 93~96%，GUI 分 89~93%
- **局限**
  - 奖励完全依赖 VLM 和 GUI-agent 的判断，会继承判官的偏差
  - 训练代价高：7B 模型要 16×A800 跑 24 小时以上，没有验证更大模型
  - 不考虑响应速度和网络状况
- **可借鉴**
  - 把「截图分 + 交互测试分」拆成逐步稠密奖励，比只看终局的 0/1 奖励更稳
  - 带「回溯 + 选最优」的 agent 可以直接当轨迹采集器，SFT 数据就不需要人工标注

#### VinciCoder（2025-11）

- **定位**：跨图表、Web、SVG、TikZ、化学五个域的统一「图 → 代码」语料，并提供一个与实现方式无关的视觉 RL 奖励。
<figure class="paper-fig"><img src="../assets/papers/vincicoder-fig2.png" alt="VinciCoder · Fig. 2：数据构建管线"><figcaption>VinciCoder · Fig. 2：数据构建管线</figcaption></figure>

- **管线步骤**（对照上图，从左往右读）
  1. **Collect Dataset**：汇总 Image-to-SVG、Chart-to-code、Image-to-LaTeX、Web-to-HTML 四类开源数据，加上科研图，共 1.3M 条直接生成对（图表 412K、Web 355K、SVG 463K、TikZ 108K、科研图 238K）
  2. **Filter & Sample**：代码侧用 Ruff 等做静态检查，图像侧用 pHash 去重，再做多样性采样
  3. **Optimize Data**
     - Gen Refine Code：让初版 VLM 在不重叠的样本上产出第一版代码，与目标图、真值代码组成 300K 条「看图修代码」样本
     - Exec & Render：执行并渲染，校验代码能出图
  4. **Training Dataset**：1.6M SFT 数据 + 42K 条难例 RL 数据
  5. **ViRL 奖励**（论文 Fig. 3，图外）：渲染结果与目标图分别算全局缩略图和 448×448 patch 的 DINOv2 相似度取平均（渲染失败给 0），再与语言一致性奖励按 0.9 / 0.1 加权
- **关键数字**
  - 8B 模型：ChartMimic 执行率 91.6%，Design2Code 高层分 88.4%，UniSVG 高层分 94.1%
- **局限**
  - 只能评静态图，覆盖不了交互
  - 视觉奖励教不会模型缺失的领域知识，还可能被投机取巧
  - 长代码、高分辨率场景下渲染和采样成本高
- **可借鉴**
  - 「初版模型的错误输出 + 真值」是廉价的修复数据来源，不用人工造 bug
  - 用 DINOv2 patch 相似度做奖励，不依赖具体代码写法，跨域通用

#### VisCoder2 / VisCode-Multi-679K（2025-10）

- **定位**：12 种语言、执行验证过的可视化代码语料，外加多轮执行反馈纠错对话。
<figure class="paper-fig"><img src="../assets/papers/viscoder2-fig2.png" alt="VisCoder2 · Fig. 2：VisCode-Multi-679K 数据构建管线"><figcaption>VisCoder2 · Fig. 2：VisCode-Multi-679K 数据构建管线</figcaption></figure>

- **管线步骤**（对照上图的三个框）
  1. **Data Filtering**（图中第 1 框）
     - Libs filter：在 the-stack-v2、svg-diagrams（182K）、CoSyn-400K 等多语言代码里，按绘图库关键词初筛
     - Vis code block extraction：GPT-4.1-mini 抽出可独立运行的可视化代码块，缺数据的注入 mock 数据
  2. **Runtime Validation**（图中第 2 框）
     - 在分语言内核的隔离 Jupyter 里用 nbconvert 执行，`--allow-errors False`：一报错就丢
     - Gen. images validation：只保留「出图、非单色、图 > 10KB」的样本
  3. **Instruction Gen.**（图中第 3 框）
     - Split 5 parts desc.：GPT-4.1 为每条写五段式描述（环境、数据与视觉描述、数据块、输出、风格），拼成指令
     - Merge Code-Feedback：混入 66K+ 条多轮纠错对话，得到 VisCode-Multi-679K
- **关键数字**
  - 验证通过 612,982 条，总计 679K（Python 187K / HTML 135K / LaTeX 124K）
  - 32B 模型加迭代 self-debug 后，执行通过率 82.4%
- **局限**
  - 语言分布不均，符号类和领域专用语言偏少
  - 纠错对话是借来的通用代码数据，不是针对视觉错误的修复
  - 只验证「能出图」，不验证「图是否符合指令」
- **可借鉴**
  - 执行加图像的廉价过滤（非单色、字节数阈值）在大规模场景下性价比很高
  - 结构化的五段式指令能让模型同时学到语义和风格，可以直接照搬到 3D 或游戏的指令合成

#### CAD-Recode（2024-12）+ cadrille（2025-05）

- **定位**：纯程序化合成 1M 条可执行 CadQuery 代码；在此基础上，cadrille 加了基于几何反馈的在线 RL。
<figure class="paper-fig"><img src="../assets/papers/cadrille-fig2.svg" alt="cadrille · Fig. 2：从真值 CAD 派生文本、多视图图像、点云三种输入"><figcaption>cadrille · Fig. 2：从真值 CAD 派生文本、多视图图像、点云三种输入</figcaption></figure>

<figure class="paper-fig"><img src="../assets/papers/cadrille-fig3.png" alt="cadrille · Fig. 3：三模态统一进 LLM，输出 CadQuery 代码，由 Python 解释器执行出 CAD"><figcaption>cadrille · Fig. 3：三模态统一进 LLM，输出 CadQuery 代码，由 Python 解释器执行出 CAD</figcaption></figure>

- **管线步骤**
  - 真值来源（CAD-Recode，纯程序化，论文无流程图）
    1. 草图：3–8 个圆或旋转矩形做并、差运算，抽出边界环并校验拓扑
    2. 在随机的标准平面上拉伸，多个体合并；坐标量化到 [−100, 100]
    3. Python 语法检查 + BRepCheck 几何检查双重校验，再去重、归一化到单位包围盒 → 1M 条 CadQuery 代码
  - Fig. 2 · 派生多模态输入
    4. **Point cloud**：在真值 B-Rep 的参数曲面上直接采点
    5. **Images**：B-Rep 三角化成网格，渲染多视图
    6. **Text**：沿用 Text2CAD 的标注协议生成描述
  - Fig. 3 · 训练
    7. 点云经 **Linear Layer**、图像经 **Visual Encoder**、文本经 **Text Tokenizer**，统一送进 **LLM**，输出 `import cadquery ...`
    8. **Python interpreter** 执行出 CAD；SFT 之后，用执行得到的几何反馈做在线 RL（论文用 Dr. CPPO）
- **关键数字**
  - 1M 程序化数据 vs DeepCAD 160K：平均 CD 1.98 → 0.30，IoU 80.7% → 92.0%
- **局限**
  - 只覆盖 sketch-extrude，没有旋转、倒角、B 样条
  - 程序化分布和真实工业件之间有差距
- **可借鉴**
  - 「随机程序 → 执行 → 校验」可以无限生成代码–几何对，而且真值零成本
  - 规模远比「真实但少」有效：程序化 1M 在真实测试集上胜过 DeepCAD

#### MeshCoder（2025-08）

- **定位**：把复杂 3D 对象拆成带语义的部件，每个部件是一段 Blender Python 代码，提供开源的对象–代码配对。
<figure class="paper-fig"><img src="../assets/papers/meshcoder-fig5.jpg" alt="MeshCoder · Fig. 5：用部件→代码模型把整件物体转成对象级代码"><figcaption>MeshCoder · Fig. 5：用部件→代码模型把整件物体转成对象级代码</figcaption></figure>

- **管线步骤**
  - 前置 · 部件级（图外）
    1. 自定义表达力更强的 Blender API：图元、扫掠、bridge loop、布尔、阵列
    2. 随机参数合成部件级点云–代码对，约 10M 条
    3. 训练部件→代码模型 **h**（三平面 tokenizer + Llama-3.2-1B）；图中雪花表示这一步里 h 被冻结
  - Fig. 5 · 对象级（对照上图）
    4. **左上**：Infinigen Indoor 的 157 万个实例，拆成部件点云 `q_1 … q_M`
    5. **右侧放大框**：每个部件 `q_i` 先用 **R, T, s** 变换到 **Canonical Space** 得到 `q'_i` → 冻结的 **h** 推理出代码 `y'_i` → 用 **R⁻¹, T⁻¹, s⁻¹** 变回原位得到 `y_i`
       - 下方代码框：`y'_i` 是规范空间里的原始圆柱，`y_i` 带上真实位置、尺度和名字 `leg_1`
    6. **左下**：按 `# part_k, name_k` 顺序拼成整件物体的代码
    7. 过滤：所有部件 CD ≤ 5e-3 才保留 → 约 1M 条对象–代码对（41 类）
    8. 以部件模型为初始化，训练对象→代码模型
- **关键数字**
  - IoU 86.75%（PLAD 67.62%），CD 0.063e-2
  - 部件阶段训练用 64×A100，约 1 周
- **局限**
  - 只适用于人造物，有机形体做不了
  - 代码里没有颜色和材质
  - HF 只放出了 100K 对象
- **可借鉴**
  - 「程序化生成器（Infinigen）→ 逆向转写成代码 → 用 CD 过滤」是把任意 3D 资产变成代码数据的通用范式
  - 先部件后对象的课程顺序，适合长代码的视觉编程任务

---

### 未能核实

- **Plot2Code 训练数据**：只有 132 条评测集（2024-05），查不到训练集。
- **Design2Code 独立训练集**：不存在，训练用的就是 WebSight 的 20% 子集，已合并进 Design2Code 条目。
- **SceneCraft 函数库**：论文有 library learning，但没找到官方代码或数据仓库。
- **下列条目论文存在，但数据没放出或没找到链接**（已在表中标注，不另计）：
  - WebVIA、UI2Code^N、AnyDoc/DocHTML
  - ReLook、MT-Web2Code、GT23D-Bench（承诺开源）
  - RLRF、Reason-SVG、CAD-Coder（文本版）、V-GameGym、GameCWM
- **游戏方向**：没找到规模化的开源「游戏代码 + 执行轨迹」训练集。
  - 最接近的是 V-GameGym（2.2K 条，评测向，数据链接未找到）和 GameQA（代码驱动的 VQA，不是代码生成）
  - OpenGame 的 GameCoder 训练数据没有放出
- **UICoder 合成数据集**：论文称已放出，但官方仓库链接没核实到（apple/ml-uicoder 返回 404）。

### 总表 · 视频即代码

| 时间 | 名称 | 数据形态 | 规模 | 生成方式 | 开源 |
|---|---|---|---|---|---|
| 2024-02 | [Keyframer](https://arxiv.org/abs/2402.06071) | 静态 SVG → CSS 2D 动画代码 | 13 人设计研究 | LLM 从自然语言生成 CSS 动画，内联预览 + 分解式提示迭代，人在环无自动验证 | 是 [GitHub](https://github.com/apple/ml-keyframer) |
| 2025-01 | [AutoPresent](https://arxiv.org/abs/2501.00912) | 指令 → 幻灯片绘图程序（SlidesLib） | 训练 7k 指令-代码对 | 自然语言指令生成 Python 绘图程序渲染幻灯片，带自我迭代修正 | 是 [GitHub](https://github.com/para-lost/AutoPresent) |
| 2025-01 | [PPTAgent](https://arxiv.org/abs/2501.03936) | 文档 → PPT 编辑指令（.pptx） | Zenodo10K 10,448 份 | 两阶段：分析参考 PPT 聚类抽 schema → 套模板执行编辑动作，每页≤2 次自校正 | 是 [GitHub](https://github.com/icip-cas/PPTAgent) |
| 2025-02 | [TheoremExplainAgent](https://arxiv.org/abs/2502.19400) | 定理 → Manim 视频 agent | 240 定理基准 | Planner + Coder 写 Manim + TTS，agentic RAG 查文档，渲染失败重试≤5 | 是 [GitHub](https://github.com/TIGER-AI-Lab/TheoremExplainAgent) |
| 2025-02 | [MoVer](https://arxiv.org/abs/2502.13372) | GSAP 动画 + 一阶逻辑验证 DSL | 5,600 条 prompt + 真值验证程序 | LLM 同时写动画与 MoVer 验证程序，按谓词检查失败处反馈闭环修复 | 是 [GitHub](https://github.com/jama1017/MoVer) |
| 2025-05 | [Paper2Poster](https://arxiv.org/abs/2505.21497) | 论文 PDF → 海报（可编辑 .pptx） | 约 100 论文-海报对 | Parser → Planner（二叉树版式）→ Painter-Commenter 环（VLM 修溢出对齐） | 是 [GitHub](https://github.com/Paper2Poster/Paper2Poster) |
| 2025-07 | [manimator](https://arxiv.org/abs/2507.14306) | 论文 → Manim 动画系统 | 无自建集，在 TEB 上评 | 两步 LLM：读 PDF 产结构化场景描述 → 转 Manim 代码，多后端，无验证环 | 是 [GitHub](https://github.com/HyperCluster-Tech/manimator) |
| 2025-07 | [PresentAgent](https://arxiv.org/abs/2507.04036) | 文档 → 配音演讲视频 | 30 文档-演讲对 | 切分文档 → 渲染幻灯片帧 → LLM 旁白 + TTS → 音画对齐合成视频 | 是 [GitHub](https://github.com/AIGeeksGroup/PresentAgent) |
| 2025-10 | [Code2Video](https://arxiv.org/abs/2510.01174) | 主题 → Manim 教学视频三 agent | MMMC 456 单元 | Planner 分镜 → Coder 并行写码 + 作用域分级自修复 → Critic 用 6×6 锚点栅格回修 | 是 [GitHub](https://github.com/showlab/Code2Video) |
| 2025-10 | [OpusAnimation](https://arxiv.org/abs/2510.03341) | 文 / 视频 → 动画图表代码 | DCG-8K 约 8K | 两阶段 SFT 冷启动 + 联合代码-视觉奖励 GRPO，配 3B 专家模型 | 承诺开源 |
| 2025-10 | [Paper2Video](https://arxiv.org/abs/2510.05096) | 论文 → Beamer 演讲视频 | 101 篇论文 | 版式树搜索 + 光标 grounding + 字幕 + TTS + 数字人，逐页并行 | 是 [GitHub](https://github.com/showlab/Paper2Video) |
| 2025-10 | [InternSVG](https://arxiv.org/abs/2510.11341) | 统一 SVG MLLM（含动画） | SAgoge 约 5.16M（动画 61K/122K） | 两阶段 SFT，SVG 专用 token + 子词嵌入；配 SArena 基准 | 是 [GitHub](https://github.com/hmwang2002/InternSVG) |
| 2026-02 | [SimuScene](https://arxiv.org/abs/2602.10840) | 文本 → 物理动画代码 | 7,659 场景（SFT 3K + RL 4.3K） | 代码渲染视频后逐条 VLM 二元 Code-Video-Judge 奖励做 GRPO | 是 [GitHub](https://github.com/Yanan-Wang-cs/SimuScene) |
| 2026-03 | [OmniLottie](https://arxiv.org/abs/2603.02138) | 文 / 图 / 视频 → Lottie JSON | MMLottie-2M 约 2M | 参数化 Lottie tokenizer（省 81% token）喂 Qwen2.5-VL 自回归 | 是 [GitHub](https://github.com/OpenVGLab/OmniLottie) |
| 2026-04 | [LottieGPT](https://arxiv.org/abs/2604.11792) | 文 → Lottie 矢量动画 | LottieAnimation-660K | 关键帧式 Lottie tokenizer（只存关键帧 + 缓动）自回归，两阶段静到动 | 部分 [GitHub](https://github.com/yisuanwang/LottieGPT) |
| 2026-05 | [VAnim](https://arxiv.org/abs/2605.01517) | 文 → SVG 动画（持久 DOM 稀疏更新） | SVGAnim-134k | 结构约束规划 + 稀疏状态差分（9.86× 压缩）+ 渲染感知奖励 GRPO | 待发布 |
| 2026-06 | [ManimAgent](https://arxiv.org/abs/2606.30296) | 论文段落 → Manim 动画 | 任务流 + 记忆库 200 条 | 双通道 episodic 记忆（正例软参考 / 负例硬禁区），不改权重不喂人工样本 | 计划开源 |
| 2026-09 | [Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar) | 全代码短片（43 风格） | 43 种影片风格 | Claude Opus 5.5 写 canvas/WebGL 逐帧 + TTS + ffmpeg，无视频生成无素材库 | 是 [GitHub](https://github.com/lemomo-ai/lemo-opuscar) |
| 2026-09 | [PDoomVideo](https://github.com/JohnHeibel/PDoomVideo) | 全代码 MV（九章） | 约 2m37s | p5.js 逐帧绘制 + 无头浏览器 + ffmpeg，每帧由代码画 | 是（无许可文件）[GitHub](https://github.com/JohnHeibel/PDoomVideo) |
| 2026-10 | [huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion) | 讲解动画（35 画风） | 35 画风 + 8 讲解语法 | 代码绘制 + 代码合成配乐，独立 agent 复查节奏与空帧 | 是 [GitHub](https://github.com/alchaincyf/huashu-art-motion) |
| 2018-03 | [3b1b/manim](https://github.com/3b1b/manim) | 渲染器 · Python（OpenGL） | 渲染引擎 | 3Blue1Brown 原版，场景对象图经 OpenGL/GLSL 原生栅格化逐帧 + ffmpeg | 是 [GitHub](https://github.com/3b1b/manim) |
| 2020-06 | [Manim Community](https://github.com/ManimCommunity/manim) | 渲染器 · Python（Cairo/OpenGL） | 渲染引擎 | 原生 scene-graph 栅格化逐帧 + ffmpeg，文档稳定、教学主力 | 是 [GitHub](https://github.com/ManimCommunity/manim) |
| 2021-01 | [Remotion](https://github.com/remotion-dev/remotion) | 渲染器 · TypeScript / React | 渲染引擎 | 每帧是帧号的纯函数，无头 Chromium 逐帧截图 + ffmpeg；按席位/按次收费 | 是（公司许可）[GitHub](https://github.com/remotion-dev/remotion) |
| 2022-05 | [Motion Canvas](https://github.com/motion-canvas/motion-canvas) | 渲染器 · TypeScript | 渲染引擎 | Canvas 过程式渲染，生成器描述时间轴，擅长旁白同步 | 是 [GitHub](https://github.com/motion-canvas/motion-canvas) |
| 2026-01 | [ranim](https://github.com/AzurIce/ranim) | 渲染器 · Rust（wgpu/GPU） | 渲染引擎 | Rust 原生 GPU 渲染，按时间求值帧；实验性、API 不稳 | 是 [GitHub](https://github.com/AzurIce/ranim) |
| 2026-06 | [HyperFrames](https://github.com/heygen-com/hyperframes) | 渲染器 · HTML / CSS / JS | 渲染引擎 | 无头 Chrome 逐帧 seek + ffmpeg，适配 GSAP/Lottie/Three.js；HeyGen 出品，面向 agent | 是 [GitHub](https://github.com/heygen-com/hyperframes) |
| 2026-09 | [Hypit](https://github.com/hypit-ai/hypit) | 视频 DSL / 编译器 · 面向 agent | 视频框架 | 给 Claude Code / Codex 一套以词为锚点的视频语言（.svml），克隆参考视频为可编辑工作流，编译字幕/B-roll/特效；纯代码视觉可零成本出片 | 是（Hypit 开源许可）[GitHub](https://github.com/hypit-ai/hypit) |

