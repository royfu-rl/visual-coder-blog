# Visual Coding 预训练 / 中训练数据调研

- 日期：2026-10-15
- 范围：**只做预训练与中训练（mid-training）阶段的「代码 ↔ 渲染结果」配对数据**。RL 环境、verifier、轨迹构造见 03/04/05/06；任务来源（GitHub 像素基线仓库、社区站点规模）见 `02_task_sources.md`；现有资产盘点、清洗四道门、标注体系见 `webdev-data/WebDev 数据构造技术方案.html` 第一、二章。本文与它们不重复，只补「从哪里拿到千万级配对、要多少、怎么去重与过许可」。
- 数字口径
  - **实测**：本次直接调 HuggingFace datasets-server / HTTP 探活数出来的，标注日期
  - **论文原文**：引用论文表格或正文的数字，附 arXiv HTML 链接
  - **推断**：明确标注，并写出依据
- 一句话结论：这条线上**真正能复用的公开资产只有 1,000 万量级配对**（WebSight 2.7M + WebCode2M 3.2M + DaTikZ 0.15M + SVG-Stack 2.3M + CAD 系），全部有明显分布缺陷；前沿模型实际用的是**自己爬的 1,000 万级真实页面 + 一个渲染管线派生出的十个任务头**（UI2Code^N、GLM-4.1V、S4 都是这个结构），这是最该抄的部分。

### 本文结构

| 章 | 内容 |
|---|---|
| §0 | 13 条全局结论 |
| §1 | 已有配对数据集：Web / 3D / CAD / Shader / 上游代码池 / DSL / 程序化 UI |
| §2 | 挖掘管线：真实页面漏斗与保留率、清洗手段、DOM 简化三条路线、反推 query、3D 侧挖脚本 |
| §3 | 数据量级与收益：Pix2Struct / S4 / UI2Code^N 三组消融、合成 vs 真实、各家中训练数字、负面证据、3D 侧 scaling |
| §4 | grounding 类数据：数据集总表、正向证据（全在推理期）、负面证据、「点哪里」QA 的构造成本与噪声 |
| §5 | 去重与污染：视觉/代码去重阈值、benchmark 去污染、许可风险、13 道闸的流水线、多样性崩塌 |
| §6 | 建议：优先级清单（规模/工程成本/法务风险）、配比初值、五条工程纪律 |
| §7 | 未能核实、引用陷阱、方法局限 |

---

## 0. 全局结论先说

| # | 结论 | 支撑 |
|---|---|---|
| 1 | 公开配对数据总量约 1,000 万，但「真实页面 + 可渲染」的只有 WebCode2M 一家（3.17M，实测），其余是合成或 DOM 被剪得过简 | §1 |
| 2 | 不要直接用 Common Crawl 的 WARC。三家独立踩同一个坑：CC 里缺 CSS/图片，渲不出原貌。正确做法是**拿 CC 的 URL 当种子重爬** | UI2Code^N §3.2.1、Design2Code §2、S4 §3.1 |
| 3 | 真实页面管线的保留率在 **0.4% ~ 6%** 之间（Design2Code 127.9k→484；WebCode2M 5 亿→2.56M），绝大部分损耗在「渲染失败 + 美观打分」两道闸 | §2.1 |
| 4 | 一次渲染要榨出十个监督头。S4 用同一批 1,500 万截图造了 10 个预训练任务，localization 类任务平均涨 25.3 分，语言类只涨 2.7 分 | S4 §4 |
| 5 | 「截图 ↔ HTML」作为预训练目标的收益极大但**不等于会写代码**。Pix2Struct 去掉 screenshot-parsing 阶段，DocVQA 从 67.8 掉到 12.2 | §3.1 |
| 6 | 合成 vs 真实不是二选一。同架构同规模对照：WebSight 训练 → 真实测试集 TreeBLEU 0.06，WebCode2M 训练 → 0.35（提高近 6 倍）；但 Design2Code 团队用**未清洗**的 C4 真页训练反而比合成更差 | §3.2 |
| 7 | 数据量的边际收益在 2M 以后明显衰减但没饱和：S4 从 2M 加到 15M（7.5 倍），ChartQA +2.9、RefExp +2.5、WebSRC +0.6 | S4 Table 1 |
| 8 | grounding 数据**成本最低**（从同一次 Playwright 渲染里免费拿 bbox，GLM-4.1V 据此造了 1.4 亿条 GUI REG/REC 对），但「灌进预训练能提升写代码」**没有任何直接实验支持**，且 GUIMid 的 11 域横评给出了明确反证 | §4 |
| 9 | 法务上最硬的一条：Common Crawl 的 ToU（2024-03-07 版）明确把 AI 训练用途的赔偿责任**完全推给使用者**，CC 本身不授予任何内容权利 | §5.3 |
| 10 | 合成数据会腐烂。按 WebSight 论文的生成 prompt，v0.2 的图片**一律**用 `https://source.unsplash.com/random/WxH/?keyword`；**该域名 2026-10-15 实测返回 503（Heroku）**，即这 192 万条已无法按原样重渲（逐行命中率因 HF filter 接口索引超时未能统计） | 论文 prompt + 实测探活 |
| 11 | 纯合成 UI 数据会造成**灾难性遗忘**：只拿 WebSight 训练，TextVQA 从 58.76 掉到 20.51~23.38（掉 60%+）。合成占比必须压在 15% 以内并与通用 VL 数据混训 | Web2Code Table 13，§3.8 |
| 12 | **唯一能把 CPT 单独算出来的数字**：UI2Code^N 的 Design2Code 从 base 9.0 → +CPT **53.3** → +SFT 79.3 → +RL 88.6。但 base 低到异常，这 +44.3 里含大量「学会按格式输出」 | §3.3 |
| 13 | 许可清洗的代价可量化且很贵：DaTikZ 三代公开版被砍 57.4% / 73.7% / 68.0%，几乎全来自 arXiv（留存率 18%），而 leave-one-out 显示 arXiv 恰恰是唯一不可或缺的来源 | §1.7、§3.7 |

---

## 1. 已有大规模配对数据集

### 1.1 Web 侧总表（按规模排序）

| 名称 | 规模 | 构造方式 | 许可 | 质量问题 |
|---|---|---|---|---|
| **Pix2Struct 预训练集** | **8,000 万**截图（[2210.03347](https://arxiv.org/html/2210.03347v1)） | C4 的 URL 重抓渲染 → 固定 viewport 截图 + **简化 parse**，50% 文字遮挡 | — | **未公开**（只放 checkpoint）；目标不可渲染（丢 style/tag），只能做理解不能做生成 |
| **S4（AWS）** | **1,500 万**截图 + 10 类标注（[2403.03346](https://arxiv.org/html/2403.03346v1)） | Common Crawl（AWS Open Data）重渲，1280×1280，按 URL 去重 | — | **未公开** |
| **UI2Code^N 预训练集** | 约 **1,000 万** 页面图–HTML 对；合计约 **2,000 万** vision-code 样本（[2511.08195](https://arxiv.org/html/2511.08195v1)） | 以 CC index 做 URL 种子自建爬虫重抓；混入 WebCode2M + WebSight | — | **数据未公开**，模型与代码在 [zai-org/UI2Code_N](https://github.com/zai-org/UI2Code_N) |
| **MultiUI** | **730 万**样本 / **100 万**网站（[2410.13824](https://arxiv.org/html/2410.13824v3)） | FineWeb `CC-MAIN-2024-10` URL → Playwright → **可访问性树** → LLM 合成 9 类指令 | 需同意条款（gated） | 不含可渲染 HTML，是「截图 + 结构化文本 QA」，不是 code 对 |
| **WebCode2M / Vision2UI** | HF 实测 **3,171,024** 行 / 1,100 GB；净化版 `webcode2m_purified` 实测 **2,562,069** 行（差 60.9 万 ≈ 19.2% 被净化）；论文称 2,563,905 | Common Crawl 真实页面，CSS 内联 + 重清洗 + ResNet-50 美观打分 | **cc-by-4.0**（compilation 层面；底层页面内容版权归原站） | 打分器二分类仅约 90% 准确 → 残留低质；HTML 仍长（均 5,366 token）；HF 卡片自带暴力内容 Warning |
| **WebSight v0.2** | 实测 **1,922,671** 行 / 317 GB（论文口径「2 million」） | Mistral-7B-Instruct 出网站创意 → DeepSeek-Coder-33B-Instruct 出 HTML+**Tailwind** → Playwright 整页截图；图片用 `source.unsplash.com/random/WxH/?keyword` | cc-by-4.0 | **① 图源已死**（`source.unsplash.com` 2026-10-15 实测 503，无法重渲）；② Tailwind 反噬：论文自承 v0.2 出现 v0.1 没有的新错误；③ 分布过简（均 647 token / 19 tag / DOM 深 5）；④ validation loss 与泛化脱钩，只能人工选 checkpoint |
| **WebSight v0.1** | 实测 **822,987** 行 / 35 GB | 同上但传统 CSS，**图片全是彩色矩形占位** | cc-by-4.0 | 无真实图片，完全学不到图文混排 |
| **Web2Code** | 论文 1,179.7K 指令对（884.7K 图–码 + 295K QA）；HF 实测 train **827,934** 条 / 815,293 图（[2406.20098](https://arxiv.org/html/2406.20098v1)） | 全合成：GPT-3.5 新生成 60K 页 + 把 WebSight/pix2code 改写成指令（824.7K）+ GPT-4 出 243.5K QA + WebSRC 精修 51.5K | **卡片写 MIT，正文写 CC BY 4.0 且仅研究用 —— 自相矛盾** | 大部分是 WebSight 的二次包装，继承其全部分布缺陷；许可口径不清不建议商用 |
| **WebUI（CHI 2023）** | **400,000** 页面 × 最多 6 种模拟设备（[2301.13280](https://arxiv.org/abs/2301.13280)） | 自建分布式爬虫（Puppeteer），种子=链接聚合站+设计博客+政府站；存 viewport+整页截图、**可访问性树**、4 种 box、computed style | `other`（见 repo COPYRIGHT.txt） | **作者明说「只识别缺陷、不删不修」**：1/3 可交互元素小于 WCAG 44×44；18% 页面有叶子元素重叠；30% 页面根本不响应式 |
| **ScreenCoder / Screen-10K** | 爬 5 万页 → 留 **10,000** 对（SFT 9k + RL 1k）；ScreenBench 1,000（[2507.22827](https://arxiv.org/html/2507.22827v1)） | 自家 agent 当 data engine **重写**成干净自包含代码 | 未核实 | 重写后不再是真实页面分布 |
| **BigDocs 的 Screenshot2HTML** | **11,000** 条，平均仅 **20.3** 个 HTML 元素（[2412.04626](https://arxiv.org/html/2412.04626v1)） | FineWeb URL → Playwright，强制许可宽松 | 整体宽松（CC-BY/MIT 系） | 规模与复杂度都太小 |
| **pix2code** | web 端 **1,750** 对（1,500 训练 + 250 测试）（[1705.07962](https://arxiv.org/abs/1705.07962)） | 程序化合成 DSL → 编译渲染，标签文字随机 | Apache-2.0 | 是 DSL 不是 HTML；标签文字无语义 |
| **Design2Code** | **484** 测试页（HF 实测 485 行 / 0.07 GB）（[2403.03163](https://arxiv.org/html/2403.03163v1)） | C4 validation 全链接 → 自动过滤 → 人工精筛 | ODC-By | **只能当评测集**；均 31,216 token、158 tag，长到无法直接做训练目标；来自 C4 → 与任何 C4 衍生训练集天然污染 |
| **Design2Code-HARD** | **80** 难例；26% 超 500 tag，19% 非英文 | 同管线挑难例 | ODC-By | 被后续工作（LaTCoder [2508.03560](https://arxiv.org/abs/2508.03560)）批评「难在文本长度，版式仍简单」 |
| **Sketch2Code** | **731** 张手绘草图覆盖 484 页；21 名标注者（从 723 人中选）（[2410.16232](https://arxiv.org/html/2410.16232v1)） | 在 Design2Code 的 484 页上众包画 wireframe | ODC-By | 规模只够评测 |

### 1.2 复杂度对照（统一 GPT-2 tokenizer 口径）

| | pix2code | WebSight | Design2Code | WebCode2M |
|---|---|---|---|---|
| 来源 | 合成 | 合成 | 真实 (C4) | 真实 (CC) |
| 规模 | 1,742 | 0.8M | 484 | 2.5M |
| 平均长度（token） | 1,316±177 | **647±216** | **31,216±23,902** | 5,366±2,393 |
| 平均 tag 数 | 52±8 | **19±8** | 158±100 | 184±77 |
| 平均 DOM 深度 | 8±0 | **5±1** | 13±5 | 15±5 |
| 平均唯一 tag 数 | 17±0 | **10±3** | 22±6 | 24±6 |

来源 [WebCode2M Table 2](https://arxiv.org/html/2404.06369v2)（WebSight / Design2Code 两列转引自 [Design2Code Table 1](https://arxiv.org/html/2403.03163v1)）。

- **这张表是全文最重要的一张**：WebSight 的代码长度只有真实页面的 **1/48**，tag 数 1/8，DOM 深度不到一半。后面所有泛化问题都源于此
- 「长度」是唯一最关键的可调旋钮：31,216（原始 C4 页）→ 5,366（WebCode2M 清洗后）→ 647（WebSight 合成）。**5,000 token 附近是目前唯一被实验证明「既保住真实结构又能训得动」的点**（见 §3.4）

### 1.3 3D 侧：先说清「不是代码」的部分

**Objaverse / Objaverse-XL 全家桶里没有一行可执行代码**，这是本节最重要的判断。

| 项 | 数字 | 来源 |
|---|---|---|
| Objaverse 1.0 | **818K** 对象、160K 作者、2.35M 标签 / 170K 唯一标签，覆盖约 21K WordNet 实体；Objaverse-LVIS 子集 47K / 1,156 类；44K 动画、63K 自标 character | [2212.08051](https://ar5iv.labs.arxiv.org/html/2212.08051) |
| Objaverse-XL | **10.2M** 去重对象（HF 元数据实测 **10,850,997** 行，2026-10-15） | [2307.05663](https://arxiv.org/html/2307.05663) |

Objaverse-XL 分来源与许可：

| 来源 | 索引量 | 实际入库/渲染 | 许可 |
|---|---|---|---|
| GitHub | 索引 **37M** 个含 3D 扩展名的文件，来自 50 万+ 仓库 | 成功导入并渲染 **5.5M**（约 15%） | 随仓库许可，论文不保证可商用 |
| Thingiverse | 约 **3.5M** | 多为 STL、无纹理，渲染时随机上色 | "predominantly Creative Commons" |
| Sketchfab | **800K**（= Objaverse 1.0） | GLB | 全部 CC |
| Polycam | 索引 72K，去重后 **71K** | — | CC-BY 4.0 |
| Smithsonian | **2.4K** | GLB | CC0 |
| 占比 | 约 56% GitHub / 35% Thingiverse / 8% Sketchfab / 其余 <1% | | 整体 ODC-By 1.0，**单个对象各自许可，商用需逐个判断** |

- 官方渲染管线：Blender **3.2.2**，默认 `num_renders=12`，相机在包围球上**随机**采样；每视角一张 PNG + 3×4 相机矩阵 .npy + metadata.json；`only_northern_hemisphere` 开关专为摄影测量扫描件（底部有洞）；`render_timeout=300s`
- 去重：按文件内容 sha256，**剔掉约 2,300 万个文件**
- 质量：Polycam 的 71K 对象中 **38.20% 的渲染图被判 "bad"**，58K 个对象至少有 2 张坏图
- **致命的一条**：gobjaverse 公布的 Objaverse-XL alignment 子集按文件类型的渲染成功数里，`github / blend` = **0**，`gltf / dae / usdz` 也都是 0；Objaverse-XL 索引的 12 种扩展名（.obj .glb .gltf .usdz .usd .usda .fbx .stl .dae .ply .abc .blend）**全部是几何资产格式，没有一个是代码**

所以 Objaverse 系对本课题只有三种合法用法：① 当逆向任务的目标渲染图；② 当视觉先验（先在渲染图上做视觉预训练再接代码头）；③ 当评测素材与几何复杂度参照。**不能当「代码→图」的正样本。**

派生渲染集（当目标图用）：

| 数据集 | 规模 | 通道 | 许可 |
|---|---|---|---|
| Cap3D / DiffuRank | **1,604,291** 条 3D-caption（其中 785,150 属 Objaverse 1.0）；1,552,357 个点云；同批对象**每对象 20 视角**渲染 + 内外参 + depth + mask | RGB/depth/mask | ODC-By 1.0 |
| G-buffer Objaverse (gobjaverse) | **280K** 对象 / 6.5TB；XL alignment 子集约 100 万候选中成功渲染 **779,325** | RGB / albedo / HDR(exr) / metal-roughness / normal+depth(exr) | MIT（标注部分） |
| Zeroverse（LRM-Zero，[2406.09371](https://arxiv.org/html/2406.09371)） | **800K** 程序化合成形状 × **32 视角** | RGB | 合成代码公开 |
| Objaverse++ | 人工标注 10,000 个对象质量，训分类器给全量约 790K 打标 | — | ODC-By 1.0 |

### 1.4 CAD：唯一真正成规模的 code ↔ render

| 数据集 | 规模 | 表示 | 构造方式 | 许可 |
|---|---|---|---|---|
| **ABC**（[1812.06216](https://arxiv.org/html/1812.06216)） | **1,000,000+** CAD 模型 | STEP / B-Rep / FeatureScript | 从 Onshape 公开库爬 4 个月，**未筛选**，含重复与大量单基元 | 研究可用 |
| **DeepCAD**（[2105.09492](https://arxiv.org/html/2105.09492)） | **178,238** 构造序列（90/5/5；文献常引 160K 训练量） | sketch-extrude 命令向量 | ABC 子集，Onshape FeatureScript 解析，**丢弃所有非 sketch+extrude 的模型** | 公开 |
| **Fusion 360 Gallery (Reconstruction)**（[2010.02392](https://arxiv.org/html/2010.02392)） | **8,625** 人类设计序列（6,900/1,725） | sketch+extrude DSL + Gym 环境 | 真实人类设计史 | 公开 |
| **Text2CAD**（[2409.17106](https://arxiv.org/html/2409.17106)） | 约 **170K** 模型 / 约 **660K** 文本标注（L0 抽象 / L1 初级 / L2 中级 / L3 专家） | 命令序列 + 文本 | DeepCAD + LLaVA-NeXT 多视角出形状描述 + Mixtral-50B CoT 出四级指令，标注跑 10 天 | HF 已改 gated（当前条款未核实） |
| **CAD-Recode**（[2412.14042](https://arxiv.org/html/2412.14042)） | **约 1M** 训练 + 约 1K 验证，纯 **CadQuery Python 代码** | Python 代码 | **100% 程序化合成** | **CC-BY-NC-4.0，禁商用（硬伤）** |
| **GenCAD** | **168K** CAD 程序 × **5 张**灰度等轴测渲染图 | 命令序列 + 图 | DeepCAD 派生 | 公开 |
| **GenCAD-Code / CAD-Coder**（[2505.14646](https://arxiv.org/html/2505.14646)） | **163,671** 条 CadQuery 脚本 × 5 张渲染图（147,289/9,027/7,355）；平均 611 token，99.9% < 3,000 token | 图 + CadQuery | 把 GenCAD 的命令序列**脚本化转成 CadQuery** | 开源 |
| **BlendNet / BlenderLLM**（[2412.14203](https://arxiv.org/html/2412.14203)） | 论文写 8K（2K 人工校验 + 6K GPT-4o 校验）；**HF 实际 12,059 行** | 自然语言 → **bpy 脚本** | 全合成，见 §2.5 | **Apache-2.0，全场许可最干净** |
| **OpenECAD**（[2406.09913](https://arxiv.org/html/2406.09913)） | 三档 **100K / 150K / 200K**「图-代码」对（token 上限 1024/2048/3072）；测试集 625 | 图 + CAD 操作代码 | DeepCAD 转写，PythonOCC 渲 3 种视图（随机视角 / 透明 / 等轴+三视图合图），640×480 | 公开 |
| **Img2CAD**（[2408.01437](https://arxiv.org/html/2408.01437)） | **4,574**（1,026 椅 + 3,243 桌 + 305 柜） | sketch-extrude | ShapeNet + PartNet 部件标注 + GPT-4V 半自动，**人工复核只留 30%** | 公开 |
| **Text-to-CadQuery**（[2505.06507](https://arxiv.org/abs/2505.06507)） | 给 Text2CAD 补了 **170,000** 条 CadQuery 标注 | 文本 + CadQuery | 转写 | 未核实 |

**CAD 系的共同致命缺陷（血统问题）**：DeepCAD 只保留 sketch + extrude，所以整条 `DeepCAD → Text2CAD → GenCAD → GenCAD-Code → OpenECAD` 血统**全部缺 revolve / fillet / chamfer**。CAD-Recode 论文在真实扫描数据 CC3D 上明确承认这是失败主因。ABC 本身含大量重复与无效形状，DeepCAD 做了测试集 Chamfer 最近邻去重。

### 1.5 Shader / GLSL：程序少但帧无限，许可是硬伤

| 项 | 数字 | 来源 |
|---|---|---|
| shaders21k 漏斗 | Twitter(TwiGL 语法) + Shadertoy 抓取并能通过 GLSL 编译 **52,000** → 去重（同 t 渲出相同图）+ 剔静态（不同 t 图不变）→ 保留 **1,089**(TwiGL) + **19,994**(Shadertoy) = **21,083**（保留率 **40.5%**） | [2211.16412 §3.1](https://arxiv.org/html/2211.16412) |
| 代码长度 | TwiGL 通常 < 280 字符；Shadertoy 平均约 4K 字符 | 同上 |
| 帧的成本 | 唯一随机变量是时间 t，4 fps 采样 + `delta_t ~ U[0,0.25]` 防周期重复；单卡 **979 fps @ 384×384**，帧是训练时在线生成。大规模实验固定用 **130 万**张 384×384 图 | 同上 |
| Shadereval-inputs | 实测 **467** 行（2026-10-15），**从 20.2 万个未过滤函数里筛出来的**；历史 v0.3=394、v0.2=257 | [HF](https://huggingface.co/datasets/Vipitis/Shadereval-inputs) |
| 风险 | **`Vipitis/Shadertoys` 与 `Shadertoys-fine` 原始大集已不可公开访问**（API 与 raw README 均 401），只剩 Shadereval-* 三个 | 实测 |
| 许可 | Shadertoy 站点默认 **CC BY-NC-SA 3.0**（非商用 + 相同方式共享）；抓取需账号 + API key，且只能拿到作者标了 `public+api` 的 shader。Vipitis 的做法是逐条用 scancode 扫 SPDX 放进 `license` 列、许可文本留在 `image_code` 开头，让下游自己筛；各许可占比**未核实**（原始大集已下架） | 同上 |

Shadereval 的评测方式值得抄：指标 `shadermatch` 是**真跑 wgpu-shadertoy 渲染后比图**，而不是比文本（[HF Space](https://huggingface.co/spaces/Vipitis/shadermatch)）。构建流水线公开在 [Vipitis/shadertoys-dataset](https://github.com/Vipitis/shadertoys-dataset)：download / annotate / filter 三步，许可用 scancode-toolkit 打 SPDX 标签。

### 1.6 上游代码池：有代码但没渲染的部分

| 语言 | 数字 | 来源 |
|---|---|---|
| **HTML（The Stack v2 dedup）** | **2,419.87 GB / 90.23M 文件**；但 StarCoder2-15B 实际训练用的 swh-full 分片只有 **99.09 GB / 5.23M 文件**（保留 **5.8%**） | [2402.19173 Table 1](https://arxiv.org/html/2402.19173v1) |
| **CSS（同上）** | dedup 161.68 GB / 23.87M → 训练 8.00 GB / 1.88M（保留 **7.9%**） | 同上 |
| **JavaScript（同上）** | dedup 1,115.42 GB / 108.87M → 训练 199.99 GB / 66.91M | 同上 |
| **GLSL（The Stack v1，permissive，StarCoder 口径）** | 去重后 **175,576** 文件 / 0.57 GB；再过滤去污染后 **167,701** 文件 / 0.40 GB，占 StarCoder 训练集 **0.052%** | [2305.06161](https://arxiv.org/html/2305.06161) |
| GLSL / OpenSCAD（the-stack-dedup parquet 字节数） | `data/glsl/` 两个 parquet 共 **302.6 MB**；`data/openscad/` 单 parquet **36.47 MB**（行数未核实，数据集 gated） | HF API |
| GitHub 仓库数（量级参考） | `language:OpenSCAD` **19,385** 仓库；`language:GLSL` **25,507**；`topic:openscad` 1,320；JS + "three.js" 关键词 50,828 | GitHub search API |

- **OpenSCAD 不在 StarCoder 的 86 种语言列表里** —— 它虽在 the-stack 里有数据，但从未被主流 code LLM 当作训练语言专门喂过。The Stack v2 的数据巡检还把 `GLSL (geo)` 这个扩展名**剔除**了
- OpenSCAD 的公开配对集全是万条以下的社区小集（HF 搜 `openscad` 共 48 个 repo，2026-10-15 实测）。最相关的几个：

| repo | 实测行数 | 体积 | 许可 | 说明 |
|---|---|---|---|---|
| `redcathode/thingiverse-openscad` | **7,378** | 26.5 MB | **CC-BY-NC-SA-4.0** | 9 列含 `scad` 与 `fakeprompt`（gemini-2.0-flash-exp 从 scad+description 反推），**只有 thumbnail 链接、没有自渲图** |
| `ThomasTheMaker/Synthetic-OpenSCAD-16WSL` | **26,480** | 6.0 MB | **未声明** | 带 image modality，合成 |
| `adrlau/openscad-vision2` | **2,128** | 1,487 MB | **未声明** | image + text |
| `adrlau/openscad-vision` | **1,963** | 1,386 MB | **未声明** | image + text + 3d，体积最大说明是真渲了图 |
| `prithivMLmods/OpenSCAD-Code-to-GLB` | **4,795** | 6.2 MB | other | code → GLB，非图 |

  读法：**量级都在万条以下，且大半没有许可声明** —— 对预训练没有意义，但 `adrlau/openscad-vision` 这类（真渲了图、1.4 GB）可以当管线的参照实现
- **three.js / WebGL 是完全空白**：HF 上与 three.js 相关的数据集只有 8 个，全是「指令-代码」，**没有任何代码→渲染图配对集**。这是最大的未开垦区
- CSG / 程序归纳方向（CSGNet、InverseCSG、ShapeAssembly、ShapeCoder）都是千量级小集 + 自定义 DSL，没有大规模渲染配对发布（规模细节未核实）

### 1.7 干净 DSL：TikZ 与 SVG（「代码 → 图」最纯的两类）

**DaTikZ 三代：内部完整版 vs 公开版**（许可清洗的代价在这里被完整量化）

| 来源 | v1 | v2 | v3 |
|---|---|---|---|
| curated（texample.net / tikz.net / pgfplots.net / GitHub） | 981 | 1,566 | 3,646 |
| TeX StackExchange | 29,238 | 30,609 | 42,654 |
| **arXiv 论文源码** | **85,656** | **326,450** | **407,851** |
| artificial（GPT-4 / ChatGPT 蒸馏） | 1,957 | 1,958 | 2,256 |
| **内部完整版合计（唯一图）** | **117,832** | **360,583** | **456,469** |
| **公开版（HF 实测 train+test）** | **50,253** | **94,974** | **145,908** |
| **被删比例** | **57.4%** | **73.7%** | **68.0%** |

来源：[AutomaTikZ Table 1](https://ar5iv.labs.arxiv.org/html/2310.00367)、[DeTikZify Table 1](https://arxiv.org/html/2405.15306v3)、[TikZero Table 1](https://arxiv.org/html/2503.11509v3)；公开版行数为 datasets-server 实测（2026-10-15）。

逐源留存率（读 HF `statistics` 接口的 `origin` 列真实频次，train split）：

| 来源 | v1 留存 | v2 留存 | v3 留存 |
|---|---|---|---|
| curated | 99.2% | 99.7% | 约 100% |
| TeX.SE | 99.6% | **100%** | **100%** |
| **arXiv** | **18.3%**（85,656 → 15,695） | **18.5%**（326,450 → 60,404） | **约 23.7%**（推算，v3 statistics 接口 `partial=true` 只覆盖前 114,217 行） |
| artificial | 100% | 100% | 100% |

- **判定规则是逐篇论文的许可证，不是整源砍掉**。原文：「ArXiv is an exception in that... the majority of papers are published under a non-exclusive license, which does not grant us permission to redistribute. As a result, we exclude any TikZ drawings from arXiv that use this license in the public release of DaTikZ.」
- 反证：**test split 几乎全是 arXiv 出身却照样放出**（v1 425/561、v2 437/442、v3 539/542 的 `origin='arxiv'`，实测 `/filter` 接口）—— 证实是逐篇判定
- **这是全调研里最该学的一条工程纪律**：许可证必须在抓取阶段就作为字段落盘，否则后期无法按篇裁剪，只能整源丢
- 编译成本：v1 从 arXiv 抽取后「around 120k」因编译失败丢弃（对应抽取约 20.6 万、**失败率约 58%**，后者为推算）；v2 暴涨 3 倍的原因是**不再要求必须有 caption**，只要求 TeX Live 2023 能编译；v3 里有 caption 的不足 37%
- 推理期编译采样率：各规模模型均约 **1.2 次采样**才出一张可编译图；MTE（token 效率）80–85，即「10 次推理里只有 2 次需要重采样」
- 失败处理值得抄：编译日志直接进 reward（无错 +1 / 可恢复错 0 / 致命错 −1），接 MCTS 迭代修正
- DeTikZify 微调只保留 **≤ 2048 token** 的样本

**StarVector 的 SVG-Bench**

| 子集 | HF 实测总行数（train / val / test） | 来源 | 平均 token 长度 |
|---|---|---|---|
| SVG-Stack | **2,283,875**（2,169,710 / 108,456 / 5,709） | The Stack 里的 `.svg` | 1,822 ± 1,808 |
| SVG-Fonts | 1,928,271 | Glypazzn | 2,121 ± 1,868 |
| SVG-Icons | 89,376 | DeepSVG | 2,449 ± 1,543 |
| SVG-Emoji | 10,043 | OpenMoji + NotoEmoji + TweMoji | 2,551 ± 1,805 |
| SVG-Diagrams | 182,618（论文只说 472 条 test，HF 实际有 182,144 train） | 从 SVG-Stack 里筛含 `text` 元素者 | 3,486 ± 1,918 |
| text2svg-stack | 2,175,419 | BLIP2 + LLaVA 生成的 caption | — |

来源 [2312.11556 Table 5](https://arxiv.org/html/2312.11556v4) + datasets-server 实测。论文与 HF 有分歧处按 HF 为准。

- 来源与许可：从 The Stack 抽 `.svg`，复用 The Stack / StarCoder 的过滤与去重（**permissively licensed**），再自己做一遍
- 预处理（可直接抄）：① **filename + SVG 代码 + metadata 三重去重**；② CairoSVG 栅格化，**丢弃渲染出全白图的样本**（这是全调研里唯一一条「朴素图像判据」）；③ 删 comment 与 XML header 压序列长度；④ **token 上限 8,192**（模型上下文 8k），这是最硬的闸
- 丢弃比例**未核实**（论文没给任何一步前后条数）
- 难度切分按复杂度递增：Fonts < Emoji < Icons < Stack < Diagrams，不是按 token 数硬切
- **OmniSVG 的 MMSVG-2M**（[2504.06263](https://arxiv.org/html/2504.06263v2)）：Icon 990k / Illustration 450k / Character 350k；坐标与颜色都离散化成 token，能处理 **> 30k token** 的 SVG（StarVector 系被 8.2k 卡死）。公开度实测：`MMSVG-Illustration` 只有 **255,412** 行（论文 500k 的约 51%），其余三个 datasets-server 返回 401 → **未核实**。它**没有数据量消融**
- SVGDreamer 是逐 prompt 的 score distillation 优化，**没有训练用配对数据集**，对预训练数据建设不可借鉴

### 1.8 程序化 UI 生成：真正不靠 LLM 的几家

| 工作 | 规模 | 生成方式 | 效果 |
|---|---|---|---|
| **pix2code**（[1705.07962](https://arxiv.org/html/1705.07962)） | 每平台 **1,500** 张合成截图-DSL 对；可枚举的唯一 GUI 配置上限 iOS 2.6M / Android 21M / **Web 310K** | `stochastic user interface generator` 随机生成 DSL → 传统编译器编译到三平台 | 测试 error% greedy：iOS 22.73 / Android 22.34 / **Web 12.14** |
| **ScreenAI 的合成标注管线**（[2402.04615](https://arxiv.org/html/2402.04615)） | Screen Annotation **3.53 亿**（规则 + 专用模型：DETR 布局检测 + 77 类 icon 分类 + PaLI captioner + OCR）；LLM(PaLM 2-S) 生成的 QA 3,920 万 / Nav 1,590 万 / Summ 1,320 万 = **6,830 万** | 前者非 LLM，后者 LLM | 规则占 **83.8%**、LLM 占 **16.2%**；**去掉全部 LLM 生成数据，670M 模型 aggregate 低 4.6pp** |
| **RicoSCA**（[2005.03776](https://arxiv.org/html/2005.03776)） | **295,476** 条合成单步命令，覆盖 177,962 个目标对象、25,677 个屏幕 | 纯规则模板：槽位 Name/Type/Location + 操作同义词，空间关系从 view hierarchy 推出，**span 标注天然已知** | PixelHelp 上 phrase extraction 85.56%、完整动作序列 **70.59%** |
| **UIClip / JitterWeb**（[2404.12500](https://arxiv.org/html/2404.12500)） | **230 万** examples，源自近 **30 万**真实网页；**> 99.9% 为合成** | 9 个 JS jitter 函数（Color Swap / Font Size / Text Noise / Spacing / Layout…），每次**均匀随机取最多 3 个**顺序施加 | design-choice acc **75.12%**、网页缺陷检测 **87.1%**（GPT-4V 51.58%）；**合成屏 67.65% vs 真实 app 57.89%** |
| **CLAY**（[2201.04100](https://arxiv.org/html/2201.04100)） | 59,555 个人工标注屏幕布局；**22,273 屏（37.4%）含 invalid 元素**；9,331 种不同 view class | 启发式过滤 + 人工标注 | invalid 检测 F1 82.7% / 类型 85.9% |

- **布局生成器反不出代码**：LayoutGAN / LayoutTransformer / LayoutDM 只输出「类别 + bbox」序列，没有任何一篇自带 code emitter。真正做「布局→代码」的是把布局当中间表示喂 MLLM（LayoutCoder，ISSTA'25，[2506.10376](https://arxiv.org/abs/2506.10376)）
- **UIClip 的 jitter 思路最值得抄**：不需要生成新页面，只要对真实页面施加受控劣化，就能造出「好/坏」对。这既是数据增广也是天然的 preference 对
- 除 pix2code、WebSight、JitterWeb、RicoSCA 之外，**没找到其他带规模数字的纯程序化 UI 数据集**

---

## 2. 大规模挖掘管线

### 2.1 真实页面漏斗：各家的具体数字

**Design2Code（最清楚的一条漏斗）** —— [2403.03163 §2](https://arxiv.org/html/2403.03163v1)

```
C4 validation 全部站点链接 + 把 CSS 内联成单文件
  → 127.9k 页
  → 剥注释 + 长度过滤（源码 > 100k GPT-2 token 丢弃）
    + 布局过滤（纯图或纯文丢弃）+ 去重
  → 14k
  → 随机抽 7k 送人工（两位作者；先共标 200 条达 75% 一致，再分工，耗时约一周）
  → 484
总保留率 484 / 127,900 = 0.38%；人工环节 484 / 7,000 = 6.9%
```
人工三条判据：① 不依赖外部文件、单文件+占位图能独立渲染；② 不含隐私/敏感/有害信息（例如删掉了交友站的个人资料页）；③ 渲染后排版良好、处理过程没破坏设计。

**WebCode2M / Vision2UI** —— [2404.06369v2 §2](https://arxiv.org/html/2404.06369v2)

```
CC-MAIN-2023-50 第一个 segment（约 33.5 亿页）
  → 随机抽约 5 亿页（受带宽与算力限制）
  → 下载并内联对应 CSS
  → 快速长度过滤（按字符数，1 词≈5 字符）
       HTML ∈ [640, 10240]   CSS ∈ [640, 20480]
  → 冗余清洗（见 2.2）
  → Playwright 渲染截图  ← 占整条流水线约 80% 时间；全程约 1 个月
  → ResNet-50 美观打分器：score < 2 全删，占原始数据 52.5%
  → 截图 hash 去重
  → 训练集 2,563,905
  → 另抽 score>4 的约 2,000 条做候选测试集，CLIP 相似度去重 + 逐条人工复检，
     按长度切 Short / Mid / Long 各 256 条
```
- 打分器怎么来的：6 名「计算机本科 + 3 年以上前端经验」标注者分两组做一致性标注，约两周，产出 **10,000** 条人工打分；5 条判据各 1 分（① 人为设计的版式而非单列自动排布；② 列表/区块有样式；③ 无过量空白；④ 配色丰富；⑤ 观感好）
- **人工子集里 80% 落在 0–1 分**，只有 20% ≥2 分 —— 这是「真实网页大多不适合当视觉编码监督」的硬数据
- ResNet-50 在测试子集上 5 分类准确率 75%，二分类（是否 ≥2）约 90%
- 伦理闸：NSFW 检测器阈值 **0.04**（只留低于此值）+ 多语言脏词表，单页脏词 >20 次则删。阈值是在第一个 chunk 上扫出来的（0.02 误杀 57.5%，0.04 保留 91.3% 且 toxic 0.21%，0.05 保留 95.4% 但 toxic 升到 0.27%）

**其他各家**

| 项目 | 漏斗 |
|---|---|
| **ScreenCoder** | 爬 5 万页 → 自动过滤只留结构良好 → **10,000** 对（保留率 20%）→ SFT 9k + GRPO 1k。它明确说明为什么**重写**而不清洗：真实代码太长、依赖噪声大，直接训不稳，模型学不到视觉→代码的核心映射 |
| **MultiUI** | FineWeb `CC-MAIN-2024-10` URL 清单（**先剔除出现在下游 benchmark 里的 URL** 防污染）→ Playwright 两种模拟设备（Windows 10 / iPhone 12 Pro）→ 爬到 110 万站 → Llama-3-70B-Instruct 读可访问性树判「成人/赌博/暴力/歧视」与「403/502/Cloudflare 拦截/空白/404」→ **约 10% 被删** → 100 万站 → 9 类任务抽取 → **730 万**样本 |
| **WebUI** | 不走 Common Crawl，自己爬。种子 = 链接聚合站 + 设计博客 + 政府站（期望可访问性元数据质量高）；按「URL 与已访问集合的相似度**反比**」加权采样（先均匀选 hostname 再按概率选 URL），实测能避开 crawler trap；每 URL 最多 6 设备，**单 URL 超时 6 分钟**（所以部分页面没跑完全部设备）；**3 个月、约 500 美元**爬完 40 万页；按**域名**分组 70/10/20 切分防跨 split 泄漏；**没有做「候选→保留」过滤**，论文明说「只识别可能的缺陷，没有尝试删除或修复」 |
| **BigDocs Screenshot2HTML** | FineWeb URL → 逐站校验「可访问性 / robots.txt 合规 / 英文为主 / 非 NSFW」→ 按 load time、page size、JS 与 CSS 文件数、DOM 深度、元素总数筛 → 识别技术栈排除「不开 JS 渲不出」的站 → **11,000** 条。各步剩余量未核实（只给终值） |
| **UI2Code^N** | 用 CC 的 URL 当种子大规模重爬（**不直接用 CC：缺图片和 CSS 渲不出原貌**）→ tag 白名单 + 冗余去除 → 约 **1,000 万**。声明不抓登录保护、付费墙、用户私有内容 |

**三家独立得出同一结论**：Common Crawl 的 WARC 不能直接用来渲染。Design2Code 要自己把 CSS 内联回去，WebCode2M 要「下载并内联对应 CSS」，UI2Code^N 直接说 CC 「缺组件（figures、CSS）导致无法忠实渲染」所以只拿 URL。**这是整条管线里第一个、也是最容易踩的坑。**

### 2.2 清洗：各家具体手段对照

| 问题 | 做法 |
|---|---|
| **广告 / cookie 弹窗 / 登录墙** | WebUI：爬虫内置启发式自动关掉 GDPR cookie 警告等弹窗。UI2Code^N：声明不抓登录保护与付费墙内容。MultiUI：LLM 读可访问性树把 403/502/Cloudflare 拦截页/空白页/404 判为无效。**专门剔除广告块：各家均未提及，未核实** |
| **外链资源失效（CDN/图片/字体）** | 两条相反路线。WebCode2M：**不修资源**，明说「无效图片链接导致页面没加载完」是不美观截图的主因，靠打分器整条扔掉（52.5%）。S4：渲染前把 CSS / JS / 字体 / 图片**抓下来缓存**，既保真又避免反复打原站，**500 CPU 做 500 万页/天** |
| **图片依赖** | Design2Code：所有图片/视频换成单一占位图 `rick.jpg`，并在 prompt 里要求模型也用它。BigDocs：图片换占位、**背景图直接删掉**。WebSight v0.1 彩色矩形 / v0.2 换 unsplash 真实图。WebCode2M 的生成 prompt 用 `placehold.co` |
| **script / 动态内容** | Design2Code：删 `<script> <audio> <iframe> <map> <svg>`，删指向外站的 `<link>`，删 `<a>` 的 href，删 `<object>` 的外部文件。WebCode2M：删注释、`<meta>`、`<script>`、隐藏元素（hidden / 零尺寸 / 在显示范围外），**属性白名单只留 `class / id / width / height / style / src` 六个**，删在 HTML 里不生效的 CSS，所有外部与行内 CSS 合并进单个 `<style>`。S4：删掉全部 `<iframe>`（同源策略读不到内部节点）。BigDocs：内联外部 CSS/JS，删过大脚本，删注释并 prettify |
| **懒加载 / 不可见元素** | **S4 做得最细且最该抄**：遍历 DOM 会带进不可见元素，于是查 CSS visibility **再做点击校验** —— 点 `elem_a` 的 bbox 中心，若返回的 `elem_b` 不是 `elem_a` 的后代，就剪掉 `elem_a`；另用递归前序遍历剔掉溢出祖先 bbox 的文字（否则被遮挡的词会进标注）。**懒加载图片的滚动触发：各家均未提及，未核实** |
| **截图策略** | WebSight / WebCode2M：Playwright **整页**截图，分辨率不定。Pix2Struct：固定 viewport。S4：固定 1280×1280。BigDocs：只截可见 viewport。WebUI：viewport（定尺寸）+ 整页（变高）两种都存 |

### 2.3 DOM 简化：三条路线

| 方案 | 做法 | 长度阈值 | 可渲染性 |
|---|---|---|---|
| **Pix2Struct** | ① 只留「本身可见或有可见后代」的节点；② 节点若不含可见元素且只有一个子节点，用孙节点替换该独生子以消除链式嵌套；③ 节点内只留文本 + 图片的 filename 与 alt-text（tag / style / title / URL 全丢）；④ 取**能塞进序列长度的最大线性化子树**，并在截图上画出该子树的框 | 由 decoder 序列长度反推子树 | **不可渲染** |
| **S4** | 沿用 Pix2Struct 的简化规则做 Screen Parsing 目标 | 单区域最多 50 词（OCR 任务） | 不可渲染 |
| **WebCode2M** | 保留 tag 结构 + 属性白名单（6 个）+ CSS 合并进单 `<style>` + 删无效 CSS | 字符数：HTML [640, 10240]，CSS [640, 20480] | **可渲染** |
| **Design2Code** | 不简化结构，只剥依赖 + 图片占位，保留参考实现全部复杂度 | 丢弃 > 100k GPT-2 token | 可渲染但太长 |
| **WebUI / MultiUI** | 不用 HTML，改用 **Chrome 可访问性树**（浏览器已自动合并掉纯样式用的 `<div>`，语义由 HTML tag + ARIA 属性 + 事件监听器统一给出） | — | 不可渲染 |
| **WebUI-95**（CHI '26，[DOI](https://dl.acm.org/doi/10.1145/3772363.3799359)） | 拿一个 SOTA UI-to-code 模型把 WebUI 的真实页面整体**重写**成归一化代码，声称保住 94% 视觉保真度、**代码体积降约 95%** | — | 可渲染。确切条数未核实（二手说法 63,824，PDF 403 取不到） |

**关键张力（这是本节的核心判断）**：
- Pix2Struct / S4 路线把目标压成简化 HTML，**可学但不可渲染** → 只能做理解类预训练，不能当生成目标，也没法接视觉 verifier
- WebCode2M 路线保住可渲染性，代价是平均 5,366 token
- ScreenCoder / WebUI-95 路线让模型重写，拿「干净 + 可渲染」换掉「真实分布」
- **做预训练配对数据应该选 WebCode2M 路线**，因为只有可渲染才能接 §4 的 bbox grounding 与下游的渲染奖励

### 2.4 反推 query（页面 → 自然语言需求）

真正做了反向标注并有量的只有三家：

| 项目 | 反向产物 | 用什么模型 | 产出量 |
|---|---|---|---|
| **MultiUI** | Webpage Captioning、Webpage QA、Embedded Image Captioning / QA、Action Prediction 等 9 类任务 | **Llama-3-70B-Instruct** 读可访问性树出 caption/QA；**GPT-4o-mini** 给内嵌图片出上下文感知 caption；指令模板由 **GPT-4o** 改写扩充 | **730 万**样本 / 100 万网站 |
| **Web2Code** | 页面理解 QA（DWU）：对 24.35K 页面各出 10 个 QA | **GPT-4** | **243.5K**（230K 基于 GPT-3.5 生成页，13.5K 基于精修 pix2code 图）+ WebSRC 去重精修 **51.5K** |
| **WebSight v0.2** | `llm_generated_idea` 列 —— 每条样本自带生成它的自然语言创意，等价于现成 text→code 对 | Mistral-7B-Instruct | 与 v0.2 等量 **1,922,671** |

- 社区在 WebCode2M 上补做的反向 prompt 量很小：`rishi-1001/webcode2m-natural-prompts` 实测 **2,843** 行
- **最值得抄的配方**：读**可访问性树**而不是原始 HTML（token 密度高得多），让一个 70B 级纯文本 LLM 出 caption/QA，内嵌图片交给小 VLM，指令模板用强模型改写扩充。MultiUI 用这套从 100 万站产出 730 万样本
- 方向相反的 WebGen-Instruct（text→website，6,667 条指令）已在 `02_task_sources.md` 覆盖，不重复

### 2.5 3D 侧：从 GitHub 挖脚本 → 批量渲染 → 过滤

**先说结论：这件事几乎没人公开做过。**

| 想做的事 | 公开工作现状 |
|---|---|
| 挖 GitHub 的 **bpy** 脚本批量渲染 | **未发现任何公开工作**。BlenderLLM / BlendNet 走的是 GPT-4o 合成而非挖掘 —— 这本身就是信号 |
| 挖 **three.js** 代码批量渲染 | **未发现任何公开配对集**，GitHub 上 5 万个相关仓库没人做过 |
| 挖 **OpenSCAD** 批量渲染 | 只有 `redcathode/thingiverse-openscad` 7,378 条，且没有自渲图 |
| 挖 **CadQuery** | 没有「挖」，全是从 DeepCAD 转写或程序化合成 |
| 挖 **GLSL** 批量渲染 | shaders21k 做了（52K → 21K），但只覆盖 Shadertoy / TwiGL 这两个平台，没动 The Stack 里那 16.7 万个 permissive GLSL 文件 |

**各家实际用的过滤判据与保留率**（这张表是本节的核心产出）：

| 工作 | 判据 | 保留率 |
|---|---|---|
| shaders21k | ① GLSL 能编译；② 同一 t 下渲染图相同 → 判重复；③ 不同 t 下图像不变 → 判静态，剔除 | 52,000 → 21,083（**40.5%**） |
| Objaverse-XL | ① 文件内容 sha256 去重（剔 2,300 万）；② Blender 能否导入并渲染成功（FBX ASCII、无 mesh、伪 .obj 全失败）；③ CLIP 特征跑 NSFW 分类（**阈值 0.9，≥3 个视角才算**）；④ CLIP 特征 + 2 层 MLP 的 "bad render" 分类器（1.2K 人标训练，CV 精度 >90%，**阈值 0.5**）；⑤ LAION-Aesthetics 分三档 | GitHub 侧 37M 索引 → 5.5M 渲染成功（**约 15%**）；Polycam 渲染图 **38.20%** 判坏 |
| CAD-Recode | ① Python 可执行（`phi_syn`）；② PythonOCC `BRepCheck_Analyzer` 判几何有效（`phi_cad`）；③ 草图 loop 不相交、基元长度 > 0；④ 按 SkexGen 协议全局代码去重 | 未报告丢弃比例 |
| BlendNet | ① 渲 4 视角图 → GPT-4o 判图文是否匹配；② 2K 条人工复核；③ 自改进阶段 Qwen2-VL-7B 粗筛 + GPT-4o 精筛级联 | 50K → 8K（**16%**）。GPT-4o 作裁判与人工交叉验证 10K 条，**89.7% 一致** |
| Img2CAD | GPT-4V 半自动生成后**逐条人工复核** | 保留 **30%** |
| CAD-Coder | token 总数 > 4,096 剔除 | 剔除 **< 0.1%** |

**反直觉的一条**：**没有任何公开工作使用「黑屏 / 单色占比 / 像素方差阈值」这类朴素图像级判据**。它们统一用「能不能跑通 + VLM 或轻量分类器看图判断」。推测原因：
- 「跑不通」已经过滤掉了绝大部分黑屏（Blender/编译器直接报错）
- 真正难判的是「跑通了但场景是空的 / 相机在物体内部 / 糊成一片」，这些像素统计量区分不开，必须让模型看
- shaders21k 的「静态图剔除」本质是**时间维方差**而非空间方差，这是唯一接近「方差阈值」的判据

**合成管线：CAD-Recode 的七步（最值得抄）**（[2412.14042 §3.2 + Appendix B](https://arxiv.org/html/2412.14042)）
1. 草图生成：`numPrimitives = RandInt(3,8)`，基元只有 Circle 与 RotatedRectangle，用 union / cut 布尔组合成复合形状；提取内外边界 loop，拆成 line / arc / circle
2. 草图合法性：loop 之间不相交、每个基元长度 > 0
3. 3D 生成：随机选三个标准平面之一并随机平移作草图平面；拉伸后 union；归一化到单位包围盒，参数量化到 −100..100、最小分辨率 1
4. **抽象化**：按参数把序列简化成 `rect` / `box` / `cylinder` 等高层调用，并**复用点坐标与拉伸平面** —— 刻意制造「模块化/复用」的代码模式
5. 双层验证：Python 可执行 + PythonOCC 几何有效，无效直接丢
6. 全局去重，保证 1M 条全唯一
7. 产物代码结构固定三段：import / 定义草图平面 / sketch-extrude + union，刻意写短以便训练

**合成管线：BlendNet 的漏斗**（[2412.14203 §3.2](https://arxiv.org/html/2412.14203)）
```
135 条人工种子指令（16 个 Locarno 类别 × 5 档长度）
  → Self-Instruct 扩写 → 约 50K 条指令
    → GPT-4o(2024-08-06) 写 bpy 脚本
      → Blender 渲染，每个对象 4 个角度
        → GPT-4o 看图 + 指令判是否匹配
          ├ 人工校验 2K  → BlendNet-Human
          └ 仅 GPT 校验 6K → BlendNet-GPT
            = 8K（HF 上 12,059）        保留率 16%
```

**Infinigen 的真实成本（劝退数字）**（[2306.09310](https://arxiv.org/html/2306.09310)）
- 完全程序化、**不依赖任何外部资产**，代码库 **40,485 行**，BSD-3；带 transpiler 把 Blender 节点图自动转成 Python
- **一对 1080p 立体图平均 3.5 小时 wall time**（2×Xeon 4114 + 1 GPU，其中约 1 小时用 GPU，约 24 GB 内存，1000 次独立试验统计）
- 定位要说清：它是「场景生成器」，不是「代码-图配对集」。代码是人写的固定 4 万行，变化全在随机参数里，**直接当 code→render 训练数据会严重同质化**

---

## 3. 数据量级与收益

### 3.1 最强的单条证据：Pix2Struct 的「去掉截图-HTML 对」消融

[Pix2Struct](https://arxiv.org/html/2210.03347v1)（Google，2022）是这条线的源头：从 C4 的 URL 拿到 **8,000 万**个网页截图，预训练目标是「从被遮挡的截图里预测简化后的 HTML parse」。它的 §5 消融在**总步数固定**的条件下做：

| 预训练配方 | DocVQA | Widget Captioning (CIDEr) | TextCaps |
|---|---|---|---|
| 完整（30K 步阅读 warmup + 70K 步 screenshot parsing） | **67.8** | **137.5** | **84.2** |
| 去掉 warmup（100K 步全是 screenshot parsing） | 56.2 | 128.0 | 71.7 |
| 去掉 50% 文字遮挡 | 55.7 | 129.4 | 77.4 |
| **去掉 screenshot parsing**（100K 步全是读文字） | **12.2** | **35.1** | **24.2** |

- 读法：把「截图 ↔ HTML」这个配对目标整个拿掉，DocVQA 掉 55.6 分、Widget Captioning 掉 102.4 CIDEr。这是全调研里单项收益最大的数字
- 但必须注意口径：Pix2Struct 的目标是**简化后的 parse，不是可运行 HTML**（只保留可见节点的文本、`img_src`、`img_alt`，丢掉 tag、style、bbox）。所以它证明的是「这类数据对视觉-结构理解极有用」，**不等于证明「会写代码」**
- 另两个可直接抄的工程细节
  - DOM 压缩：① 只留有可见元素或可见后代的节点；② 节点无可见元素且只有一个子节点时，用孙节点替换掉这个独生子，消除链式嵌套；③ 再找「线性化后能塞进序列长度上限的最大子树」，并把该子树的覆盖区域画成框叠在截图上
  - 遮挡 50% 文字、但要求解码整棵子树 → 同时得到 OCR、MLM、captioning 三种信号
  - 不能直接上 screenshot parsing：论文说裸训「不稳定且收敛慢」，必须先用随机字体/颜色的纯文字图做一个短而猛的「学认字」warmup

### 3.2 真正的 data-scale 消融：S4 的 2M → 15M

[S4](https://arxiv.org/html/2403.03346v1)（AWS AI Labs，2024）是唯一公开了同口径数据量阶梯的工作。从 Common Crawl 重渲 **1,500 万**张截图（1280×1280），同一批数据分 2M / 15M 两档：

| 预训练数据 | 目标 | ChartQA | RefExp cls | Widget Cap. | Screen Sum. | WebSRC |
|---|---|---|---|---|---|---|
| S4 Data 2M | Screen Parsing（同 Pix2Struct） | 47.4 | 87.9 | 129.5 | 101.3 | 58.7 |
| S4 Data 15M | Screen Parsing | 52.1 | 88.1 | 129.2 | 104.5 | 60.1 |
| S4 Data 2M | S4 的 10 任务 | 50.5 | 92.4 | 130.5 | 103.2 | 60.5 |
| S4 Data 15M | S4 的 10 任务 | **55.0** | **94.9** | 130.6 | 105.7 | **61.1** |
| （对照）Pix2Struct 原版 | Screen Parsing | 56.0 | 92.2 | 133.1 | 107.0 | — |

- **数据量**：2M → 15M（7.5 倍），同目标下 ChartQA +4.7 / +4.5，RefExp +0.2 / +2.5，WebSRC +1.4 / +0.6。即**7.5 倍数据换来 1~5 分**，边际收益明显衰减但未饱和
- **目标设计比数据量更值钱**：同样 2M 数据，把目标从 1 个换成 10 个，RefExp 从 87.9 跳到 92.4（+4.5），比把数据加到 15M（+0.2）划算得多
- **负面证据（很重要）**：论文明说「用我们的 2M 数据在 Pix2Struct 权重上继续 screen parsing 预训练，会在各个下游数据集上**损害**性能」。归因是分布漂移（2M vs 原版 80M、过滤策略不同、batch size 128 vs 2048）。结论是**小规模的同类数据续训是负收益，必须上到量**
- S4 汇总收益：5 个语言输出数据集平均 **+2.7 分**；4 个定位输出数据集平均 **+25.3 分**（PubLayNet / PubTables1M / RefExp candidate-free / ICDAR 2019）。Table Detection 单项最高 +76.1%
- 工程成本锚点：**500 个 CPU 一天能渲 500 万页**（约 1 万页/CPU-日），前提是把 CSS/JS/字体/图片都缓存到本地

### 3.3 UI2Code^N：目前公开的最大 UI-to-code 持续预训练

[UI2Code^N](https://arxiv.org/html/2511.08195v1)（Zhipu，arXiv 2511.08195，ICML 2026）是唯一把「千万级配对 + 真正写可运行代码」走完的公开工作。

| 阶段 | 数据量 | 构造 |
|---|---|---|
| 持续预训练（CPT） | **约 1,000 万** 自爬 UI–code 对；连同外部数据与通用 VLM 任务共 **约 2,000 万** vision–code 样本；另加 **1B+ token** 纯语言-代码数据 | 以 Common Crawl 的 URL 为种子大规模重爬（**不直接用 CC，因为缺图片和 CSS 渲不出来**），再做 tag 白名单 + 冗余去除；外部数据用 WebCode2M + WebSight |
| SFT | 80K | Claude-3.7-Sonnet-Thinking 生成高质量单页 HTML 作答案，**反向构造 query** 保证正确性；UI polishing 用多个 VLM（自己、GLM-4.5V、Claude-4-Sonnet）产出劣化渲染当输入；UI editing 覆盖增/删/替/调，并把高质量「删除」对反转成「添加」对 |
| RL | 12K 真实网页 | GRPO，去掉 KL 与 entropy 正则 |

- 基座是 GLM-4.1V-9B-Base 的早期 checkpoint，LR 2e-5，TP=2，global batch 1,536
- **效果（Design2Code 满分 100）**：GLM-4.1V-9B-Thinking 64.7 → UI2Code^N-9B-SFT **79.3** → RL 后 **88.6**（Claude-4-Sonnet-thinking 81.2、GPT-5 89.7、Gemini-2.5-Pro 89.5）
- **逐阶段消融（Design2Code Accuracy %）**：

| 阶段 | Design2Code |
|---|---|
| Base（9B 基座） | **9.0** |
| + CPT（约 2,000 万 vision-code） | **53.3** |
| + SFT（8 万） | **79.3** |
| + RL（12K 真实网页） | **88.6** |

  - **这是全调研里唯一能把 CPT 单独算出来的数字：持续预训练一个阶段就贡献 +44.3 分**（9.0 → 53.3），SFT 再 +26.0，RL 再 +9.3
  - 口径提醒：base 的 9.0 低到异常（同尺寸的 GLM-4.1V-9B-Thinking 是 64.7），说明 base 很可能连输出格式都不稳，这 +44.3 里含相当一部分「学会按格式输出」而非「学会写代码」。**不要把它当纯数据收益引用**
  - 仍然**没有任何一行剥离 CPT 里的 GUI-REG 目标**，所以「局部 bbox 监督值多少」在公开文献里是空白
- **CPT 里混了 grounding 任务**：用 GUI Referring Expression Generation 范式 —— 给整页截图 + 随机采样的某个 DOM 节点的 bbox，要求预测该节点对应的 HTML。目的是「让 UI 片段与底层代码对齐」并控制序列长度。这是「局部监督」的直接实现，见 §4
- **真实数据在 RL 阶段的消融**（固定 20K 样本、100 步）：

| RL 数据 | Design2Code | UI2Code-Real | UIPolish-Synthetic | UIPolish-Real |
|---|---|---|---|---|
| 不含真实网页 | 81.5 | 68.7 | 92.0 | 65.0 |
| 含真实网页 | **82.4** | **75.0** | **93.0** | **80.0** |

  - 读法：真实数据主要补的是**真实分布上的那一截**（UI2Code-Real +6.3、UIPolish-Real +15.0），在合成测试集上只 +1.0。sim-to-real gap 是真的

### 3.4 合成 vs 真实：两个方向相反的结论，根因是「有没有清洗」

| 工作 | 实验 | 结果 | 结论 |
|---|---|---|---|
| [Design2Code](https://arxiv.org/html/2403.03163v1) §3.2 | 18B 模型 LoRA(r=8) 微调，训练集：WebSight v0.1 的随机 20%（约 16.5 万） vs C4 真实网页 | 「用真实网页训练极不稳定且困难，因为真实代码又长又脏，**最终性能甚至低于合成数据**」 | 真实 < 合成 |
| [WebCode2M](https://arxiv.org/html/2404.06369v2) Table 3 | **同一个 WebCoder-1.3B 架构**，只换训练集：WebSight vs WebCode2M，测在真实页面测试集上 | 见下表 | 真实 >> 合成 |

WebCode2M Table 3（Visual Score / CLIP / TreeBLEU）：

| 模型 | 训练集 | Short Visual | Short CLIP | Short TreeBLEU | Long Visual | Long CLIP | Long TreeBLEU |
|---|---|---|---|---|---|---|---|
| WebCoder*-1.3B | WebSight | .42 | .68 | .06 | .38 | .65 | .04 |
| WebCoder-1.3B | WebCode2M | **.78** | **.73** | **.35** | **.65** | **.69** | **.15** |
| WebSight VLM-7B | WebSight | .57 | .69 | .03 | .48 | .64 | .03 |
| Design2Code-18B | WebSight | .75 | .68 | .04 | .61 | .68 | .06 |

- 差距最大的是 **TreeBLEU（DOM 结构召回）：0.06 → 0.35，近 6 倍**。视觉相似度（CLIP）只从 0.68 到 0.73，几乎看不出差距
- 这解释了两个结论为何不矛盾：
  - 合成数据能把「配色、整体版式」学到位（WebSight VLM-8B 的 color score 0.99 vs Design2Code-18B 的 0.66，Design2Code §5.3）
  - **结构**必须靠真实页面。但真实页面必须先经过「嵌内联 CSS + 删 script/meta + 删不可见元素 + 属性白名单 + 长度截断」这套清洗，否则就是 Design2Code 遇到的「又长又脏、训不动」
- 推论（标注为推断）：真实数据的价值集中在 DOM 结构，而结构是下游「改一处不崩全页」的基础。所以**真实页面不是可选项，但必须配清洗管线**

### 3.5 各家技术报告里的中训练数字（能查到的全在这）

| 模型 | 预训练/中训练 token 与阶段 | 有没有点名 image-to-code 数据 | 来源 |
|---|---|---|---|
| **GLM-4.1V-Thinking / GLM-4.5V** | 预训练 120,000 步、seq 8,192、global batch 1,536；长上下文续训 10,000 步、seq 32,768 | **有，且是本课题最相关的一家**：① OCR 数据 2.2 亿图，其中一路是「arXiv LaTeX → LaTeXML 转 HTML → 转轻量标记 → 按 PDF 分页栅格化」，产出**成对的「页面渲染图 ↔ 结构化源码」**；② GUI grounding：从近期 CommonCrawl 快照抽 URL、截图，用 Playwright 编译并解析全部可见 DOM 元素与其渲染 bbox，产出 **1.4 亿+** GUI 的 REG/REC QA 对；③ 自然图 grounding 4,000 万（LAION-115M + GLIPv2，只留 ≥2 个有效 bbox 的样本）；④ instruction tuning **5,000 万**条，明确包含 "UI coding" | [2507.01006 §3.1](https://arxiv.org/html/2507.01006v1) |
| **MiMo-VL-7B**（小米） | 四阶段共 **2.4T**：projector warmup 300B / VL alignment 167B / 多模态预训练 1.4T / 长上下文 SFT 550B（seq 8K→32K） | **没有**。GUI 数据只到 grounding（element / instruction grounding）与 action 轨迹；另有一个「给操作前后两张截图、预测中间动作」的预训练任务，论文说「显著提升对 GUI 的动态感知」 | [2506.03569 §2.2/Table 1](https://arxiv.org/html/2506.03569v1) |
| **Kimi-VL-A3B** | 共 **4.4T**：ViT 2T + 对齐 0.1T + joint 预训练 1.4T + **joint cooldown 0.6T** + 长上下文 0.3T | **没有**。agent 数据来自批量虚拟机里启发式采集的截图+动作，加工成 dense grounding 与连续轨迹两种格式 | [2504.07491 §2.3/Table 1](https://arxiv.org/html/2504.07491v1) |
| **Qwen2.5-VL** | 共 **4.1T**（Qwen2-VL 是 1.2T）：视觉预训练 1.5T / 多模态预训练 2T / 长上下文 0.6T | **没有**。agent 数据 = 手机/网页/桌面截图 + 合成引擎产出的截图 caption 与 UI 元素 grounding 标注 | [2502.13923 §2.2/Table 2](https://arxiv.org/html/2502.13923v1) |
| **InternVL3.5** | SFT 约 **5,600 万**样本 ≈ **130B token**，纯文本:多模态 ≈ 1:3.5；RL 用 MMPR-v1.2（约 20 万对）与 MMPR-Tiny（约 7 万 query） | **没有**预训练配对数据描述；但单独评了 SVG 任务（SGP-Bench，30B-A3B / 38B 近 70% 正确率，超过 GLM-4.5V、Qwen2.5-VL-72B、Step3-321B） | [2508.18265](https://arxiv.org/html/2508.18265v1) |
| **GLM-5**（纯文本，但 mid-training 口径最清楚） | 基座共 **28.5T**：预训练 27T + 中训练三段 32K(**1T**) / 128K(**500B**) / 200K(**50B**)；代码语料「模糊去重后唯一 token 数 +28%」；SWE 数据放宽仓库级过滤后拿到**约 1,000 万 issue–PR 对**，过滤后 issue–PR 部分约 **160B 唯一 token** | 不适用（无视觉） | [2602.15763 §2.2/2.3](https://arxiv.org/html/2602.15763v1) |

- 可直接拿来做配比的锚点
  - 中训练的量级 = 基座的 **5% 左右**（GLM-5：1.55T / 28.5T = 5.4%）
  - 视觉侧「cooldown / 中训练」的量级：Kimi-VL 0.6T / 4.4T = 13.6%；MiMo-VL 的 Stage 4 是 550B / 2.4T = 22.9%
  - UI2Code^N 的 2,000 万 vision-code 样本做 CPT，是在一个 9B 基座上；按它的 batch 1,536、seq 不明，**无法反推 token 数**（未核实）
- **关键观察**：除 GLM 系和 UI2Code^N 外，**公开大模型报告里几乎没人承认在预训练里放「截图→可运行代码」配对**。他们放的是 grounding、OCR、agent 轨迹。这既可能是没做，也可能是没写。推断：GLM 之所以在 Design2Code 上领先开源一大截（GLM-4.1V-9B 64.7 vs Qwen2.5-VL-72B 41.9、InternVL3-78B 30.0、Kimi-VL 38.8、MiMo-VL-7B 28.3），与它在预训练里就放了 1.4 亿 GUI grounding + arXiv 渲染-源码对高度相关

### 3.6 中训练阶段加这类数据的收益证据

| 证据 | 数字 | 口径注意 |
|---|---|---|
| MiMo-VL Stage 4（长 CoT 合成数据为主） | MMMU **+9**、OSWorld-G **+14**、OlympiadBench **+16**，且「持续提升、未饱和」 | 主料是长推理数据，不是视觉代码；OSWorld-G 是 GUI grounding，可借鉴 |
| GLM-5 中训练 200K 段 | 「在 128K 阶段之上再加一个 200K 中训练段，**即使在 128K 上下文窗口内也进一步提升**」 | 定性，无数字 |
| S4 的 15M 续训 | 定位类任务平均 +25.3，语言类 +2.7 | 见 §3.2 |
| UI2Code^N 全流程 | Design2Code 64.7 → 79.3（CPT+SFT）→ 88.6（+RL） | CPT 与 SFT 未拆分 |

**负面证据（这块比正面证据更重要）**：公开大模型技术报告普遍不披露，但学术论文里有四条很硬的，见 §3.8。

### 3.7 合成数据有效 / 无效：一张汇总表

| 工作 | 合成了什么 | 规模 | 结论 | 支撑数字 |
|---|---|---|---|---|
| **CAD-Recode** | CadQuery Python 代码（纯规则合成） | 1M | **有效，且胜过真实** | 同样 160k，合成 CD 0.54 vs 真实 DeepCAD 1.98（3.7 倍）；160k→1M 再降 1.8 倍 |
| **StarVector** | 用 SVG-Stack 2.1M 做预训练 | 2.1M | **只在下游稀缺时有效** | 8.7k 的 SVG-Emoji 上 LPIPS 0.355→0.225（−37%）；已有 80k 的 SVG-Icons 上收益归零，SSIM 甚至 0.905→0.894 |
| **WebSight / Sightseer** | LLM 生成 HTML+Tailwind | 2M | **结构无效、风格有效** | 真实测试集 TreeBLEU 仅 0.03~0.06；但 color score 0.99（全场最高） |
| **Web2Code** | GPT-3.5/4 生成页 + 改写 WebSight | 1.18M | **伤通用能力** | 见 §3.8 |
| **BlendNet** | GPT-4o 写 bpy 脚本 + 渲染校验 | 50K → 8K | 有效但量小 | 保留率 16%；GPT-4o 作裁判与人工 89.7% 一致 |
| **Zeroverse** | 程序化合成 3D 形状替代 Objaverse | 800K × 32 视角 | **有效，且证明网格数据早饱和** | 「training on only 200K instead of 800K Objaverse data, GS-LRM's performance drops by only 0.1 PSNR」；「further increasing the amount of data is not effective」 |
| **shaders21k** | 爬来的 GLSL 程序 + 在线渲帧 | 21K 程序 / 1.3M 图 | 有效，未饱和 | ImageNet linear probe 30.25 → 44.83（MixUp）；对数线性未饱和。**但精选 1,089 个 > 随机 1,089 个（43.26 vs 42.26）** |
| **ScreenAI 的 LLM 部分** | PaLM 2-S 生成 QA / Nav / Summ | 6,830 万（占 16.2%） | 有效 | 去掉全部 LLM 生成数据，670M 模型 aggregate **低 4.6pp** |
| **UIClip / JitterWeb** | 对真实页面施加受控 jitter | 230 万（> 99.9% 合成） | 有效 | 网页缺陷检测 87.1% vs GPT-4V 51.58% |
| **RicoSCA** | 纯规则模板生成单步指令 | 295,476 | 有效 | PixelHelp 完整动作序列 70.59% |
| **Infinigen** | 完全程序化场景生成器 | 无上限 | **不适合当配对数据** | 代码是固定 4 万行，变化全在随机参数；一对 1080p 立体图 3.5 小时 |

**跨工作的两条一致规律**：
1. **合成只在「下游数据稀缺」时值钱**。StarVector 在 8.7k 的 Emoji 上 −37% LPIPS，在 80k 的 Icons 上归零；AutomaTikZ 同向（砍掉 29k 的 TeX.SE 几乎无感，但砍掉 86k 的 arXiv 让 KID 从 0.068 崩到 0.229）。**别为冲总量付钱，为补稀缺域付钱**
2. **「程序多样性」是真变量，「图像数量」不是**。shaders21k 的「精选 1,089 > 随机 1,089」与「程序数对数线性未饱和」是同一件事的两面；LRM-Zero 的「网格 800K→200K 只掉 0.1 PSNR」是反面

**AutomaTikZ 的 leave-one-source-out**（CLiMA-7b，[Table 4](https://ar5iv.labs.arxiv.org/html/2310.00367)）—— 这是「来源不对称性」最清楚的一张表：

| 配置 | CER↓ | EED↓ | KID↓ | CLIPimg↑ | BLEU↑ |
|---|---|---|---|---|---|
| 全量 | 0.545 | 56.045 | 0.068 | 80.671 | 2.82 |
| **− arXiv（86k）** | **2.145** | **60.552** | **0.229** | **75.15** | **0.886** |
| − TeX.SE（29k） | 0.624 | 56.274 | 0.071 | 80.461 | **2.936**（反而升） |
| − artificial（4k） | 0.503 | 56.510 | 0.079 | 79.912 | 2.537 |
| − curated（1k） | 0.656 | 56.246 | 0.072 | 80.346 | 2.711 |
| − caption 增广 | 0.603 | 56.384 | 0.056 | 78.312 | 2.714 |

**残酷的一点**：量的增益主要来自那个最脏、最不可再分发的来源（arXiv），这正是许可清洗最疼的地方（§1.7 显示 arXiv 留存率只有 18%）。

**DeTikZify 的 sketch 合成增广**（劣化模拟手绘，这套方法可直接搬到 UI polishing）：
- 真人 sketch 种子集 SketchFig 只有 **549** 对（TeX.SE 来源，SigLIP 相似度排序后人工过筛）
- 合成 sketch **不落盘，训练时 on-the-fly**，每次采样同一张图生成不同 sketch，**50% 概率替换原图**
- 生成器：Instruct-Pix2Pix 零样本 → 在 SketchFig 上微调（v2 起换自训的 UltraSketch）
- 有效性（congruence coefficient，与真人 sketch 分布的契合度）：UltraSketch **0.74**；纯图像变换 **0.75**（更不多样但更保文字）；**两者表征平均后 0.82**（两条路正交互补）
- v2 vs v1 端到端（DaTikZ v3 test，分数 ×100）：参考图输入 DSim 75.46→**80.50**、cBLEU 2.95→**6.11**、MTE 84.0→**93.3**

### 3.8 负面证据：四条很硬的

**① GUIMid 的 11 域中训练横评 —— 本文最重要的一条反证**（[2504.10127](https://arxiv.org/abs/2504.10127)，Qwen2-VL-7B，每域 150K 样本，再统一 post-train GUI 轨迹）

| Mid-training 域 | WebArena PR | AndroidWorld SR |
|---|---|---|
| 不做 mid-training（基线） | 26.3 | 9.0 |
| **Web Screenshot2Code** | 28.0 | **9.9** |
| **GUI Perception（grounding 类）** | 27.4 | 14.0 |
| Chart / Document QA | 24.6 | 15.3 |
| Multi-modal Math | 30.4 | 15.3 |
| **MathInstruct（纯文本数学）** | **31.9** | 14.4 |
| **CodeI/O（纯文本代码）** | 29.2 | 14.9 |
| GUIMid（最优混合） | **34.3** | **21.2** |

- **Web Screenshot2Code 是全表最差的中训练域之一**（AndroidWorld 9.9，几乎等于不做）；GUI Perception 作者也明说「does not help a lot」
- **纯文本数学与纯文本代码反而赢过视觉 grounding 数据**
- 口径提醒（很关键）：它的**下游任务是 GUI agent（WebArena / AndroidWorld），不是写代码**。所以这条证明的是「screenshot2code 数据对 GUI agent 没用」，**不直接等于「对写代码没用」**。但它是目前唯一一张把 screenshot2code 放进多域横评的表，必须并列呈现

**② Web2Code 的 MME-Cognition 单调下滑**（论文正文完全没提这条，藏在表里）

| CrystalChat-7B 配置 | MME-P | **MME-Cognition** | POPE | SciQA | TextVQA |
|---|---|---|---|---|---|
| 无 | 1456.53 | **308.21** | 86.86 | 67.77 | 57.84 |
| +DWU | 1438.51 | 292.14 | 87.10 | 68.27 | 58.15 |
| +DWU+DWCG | 1478.82 | 297.14 | 86.13 | 67.92 | 57.41 |
| 全四项 | 1449.54 | **279.64** | 86.53 | 68.32 | 57.86 |

MME-Cognition **308.21 → 279.64（−9.3%）**；POPE / SciQA / TextVQA 基本不动。

**③ 纯 WebSight 合成 UI 数据会造成灾难性遗忘**（Web2Code Table 13）

| 训练数据 | TextVQA | SciQA | MME-P |
|---|---|---|---|
| 基线 | **58.76** | 72.08 | 1464.73 |
| 纯 WebSight v0.1 | **23.38** | 56.19 | 1149.68 |
| 纯 WebSight v0.2 | **20.51** | — | — |

- TextVQA 从 58.76 掉到 20~23，**掉 60%+**
- 推论（标注为推断）：**合成 UI 代码数据比真实数据危险得多**。原因很可能是合成数据的 token 分布极窄（均 647 token、19 tag、DOM 深 5，见 §1.2），模型会塌到这个窄分布上
- 这直接支持 §3.4 的配比建议：合成集占比不要超过 15%，且必须与通用 VL 数据混训（UI2Code^N 明确这么做）

**④ S4 的小规模续训负收益**（§3.2 已给）：用 2M 自建数据在 Pix2Struct 的 80M 权重上续训，各下游数据集全面掉点。


### 3.9 3D/CAD 侧的 scaling：比 Web 侧更干净的两条曲线

**曲线 1：CAD-Recode 的「合成量 → 精度」**（[2412.14042 Table 3](https://arxiv.org/html/2412.14042)，Qwen2-1.5B + 点云投影器，10 次 test-time sampling）

| 训练集 | 规模 | DeepCAD CD↓ / IoU↑ | Fusion360 CD↓ / IoU↑ | CC3D（真实扫描）CD↓ / IoU↑ |
|---|---|---|---|---|
| 前 SOTA（CAD-SIGNet） | DeepCAD 160k | 3.43 / 77.6 | 7.37 / 65.6 | 14.80 / 42.6 |
| CAD-Recode | DeepCAD **160k**（真实人造） | 1.98 / 80.7 | 3.37 / 67.6 | 3.79 / 56.4 |
| CAD-Recode | 合成 **160k** | **0.54 / 88.3** | **0.66 / 82.0** | **1.27 / 69.0** |
| CAD-Recode | 合成 **1M** | **0.30 / 92.0** | **0.35 / 87.8** | **0.76 / 74.2** |

两条独立结论：
1. **同样 160k，合成完胜真实挖的数据**：CD 1.98 → 0.54（3.7 倍），IoU +7.6。原因是合成管线能控制 feature 分布和代码模式（刻意注入坐标复用、box/cylinder 抽象）
2. **160k → 1M（6.25 倍）仍在涨**：CD 再降 1.8 倍，IoU 再 +3.7；无效率只从 0.3% 到 0.4%，没有代价。不做 test-time sampling 时 1M 模型 CD 0.75 / IoU 89.3，依然碾压前 SOTA 的 6.81 / 77.3

**曲线 2：shaders21k 的「程序数 → 下游精度」**（[2211.16412 §4.1-4.2](https://arxiv.org/html/2211.16412)）
- 固定 10 万张图像预算、只变 shader 程序数量，下游精度随 shader 数**对数线性上升、在 21K 处未饱和**，论文原文「performance is not saturated at 21k shaders, and it scales logarithmically」
- ResNet-50 + MoCo v2 + 130 万图，ImageNet-1k linear probe top-1：S-21k 30.25 → S-21k MixUp **44.83**（对照：Places365 55.59、ImageNet-1k 67.50、FractalDB-1k 23.86、Dead-leaves 20.00）
- **另一条很重要**：Shaders-1k 全量（1,089 个人工精选）比从 21k 里随机抽同样 1,089 个更好（43.26 vs 42.26）→ **程序质量 > 程序数量**

**反面证据：网格数据（非代码）会早早饱和**
- LRM-Zero：「training on only 200K instead of 800K Objaverse data, GS-LRM's performance drops by only **0.1 PSNR** on GSO」；Zeroverse 自己也写「further increasing the amount of data is not effective」（[2406.09371](https://arxiv.org/html/2406.09371)）
- Objaverse++：只用高质子集比用全量约 790K 效果更好、loss 收敛更快

**这组对比是本文最重要的 scaling 判断**：

| 数据类型 | 饱和点 | 证据 |
|---|---|---|
| 几何资产（网格 → 图） | **20 万量级就饱和** | LRM-Zero：800K → 200K 只掉 0.1 PSNR |
| 程序 / 代码配对（代码 → 图） | **百万量级还在涨** | CAD-Recode 160k → 1M 仍有 1.8 倍改善；shaders21k 在 21K 程序处对数线性未饱和 |
| 真实网页配对（页面 → 代码） | **1,500 万仍在涨但边际很薄** | S4 的 2M → 15M 只换来 1~5 分 |

推论（标注为推断）：**该押的是「程序多样性」而不是「图像数量」**。同一份代码多渲几个视角/几帧的边际收益远低于多搞一份不同的代码。

**其它小消融**
- Text-to-CadQuery：给 Text2CAD 补 17 万条 CadQuery 后微调 6 个不同尺寸开源 LLM，精度随模型尺寸单调提升，最好 top-1 exact match 从 58.8% → **69.3%**，CD 降 48.6%
- BlenderLLM 自改进：4 轮，每轮固定只喂 2K 条过滤后的自生成数据（防饱和/过拟合），每轮 SFT 约 21 分钟 / 4×A800
- CAD-Recode 的额外收获：**代码表示本身就是迁移性收益** —— 点云 → CAD-Recode → GPT-4o 回答 CAD-QA（SGP-Bench 1000 题）达 **76.5%**，而 CAD-SIGNet 的自定义序列即便给格式提示也只有 63.2%，PointLLM 42.3%。即**输出可执行代码而不是自定义 token 序列，能白拿一层下游可用性**

---

## 4. grounding 类数据

### 4.0 本节最重要的结论

1. grounding 语料已经非常成熟且便宜：公开可下载量级到 **1,300 万 ~ 1,660 万元素**（OS-Atlas、Aria-UI），自动构造成本是人工的 1/40 ~ 1/100（Falcon-UI 全流程 **200 美元** vs RICO 众包 **19,200 美元**）
2. **「加 UI grounding 预训练 → image-to-code 指标提升 X」这个消融，公开文献里没有任何一篇做过。** 最接近的 UI2Code^N 用了 bbox→HTML 片段目标，但它的阶段消融把整个 CPT 当一个整体，没有剥离该目标
3. **正反证据同时存在且互相矛盾**：推理期的 bbox 锚定定位有稳定正收益（ScreenCoder Position +0.142）；但 GUIMid 的 11 域横评显示 **GUI Perception 与 Web Screenshot2Code 是最没用的两个中训练域**，纯文本数学和纯文本代码反而更有效

### 4.1 公开 grounding 数据集：Web 自动构造（本课题主线）

| 数据集 | 规模 | 构造方式 | 许可 |
|---|---|---|---|
| **WebUI**（[2301.13280](https://arxiv.org/html/2301.13280)） | **400,000 网页 × 6 个模拟设备**；3 个月、约 **500 美元**；平均 60 元素/页（30 个在视口内）、20 个可点击 | headless Chrome；用 **accessibility tree**（非裸 DOM）；每元素 **4 个盒**（content/padding/border/margin）；角色由 computed a11y role 多标签推出；并存 computed style | HF 标 `license: other`，实为 **CMU 研究用途协议**（需 indemnify CMU，商业雇主同受约束）；HF 版经脏词过滤比论文实验用的更少 |
| **SeeClick**（[2401.10935](https://arxiv.org/html/2401.10935)） | 约 **30 万** CC 网页；混合移动端后总 **100 万**条 | 从 HTML 取两类元素：① 有可见文本内容的；② 带 `title` 属性（hover 提示）的。反向还造 web OCR 任务 | HF `cckevinn/SeeClick-Web` |
| **OS-Atlas**（[2410.23218](https://arxiv.org/html/2410.23218)） | **2,240,717 截图 / 13,582,210 元素**，5 平台；web 子集 **1,617,179 截图 / 7,779,922 元素** | 从 **FineWeb** URL 爬 400 万网页 → 整页渲染后切成 1920×1080 片 → 排 404 得 370 万截图 / 3,700 万元素 → 规则过滤（渲染不全、元素全堆底部）+ **每页最多留 10 个元素** → 160 万截图 / 770 万元素 | **Apache-2.0** |
| **UGround / Web-Hybrid**（[2410.05243](https://arxiv.org/html/2410.05243)） | **773K 网页截图 / 900 万元素**；加补充源共 1.3M 截图 / 1,000 万元素 | CC-MAIN-2023-50 → URL 模式 + 语言过滤 → Playwright 渲染、模拟垂直滚动取多屏 → **把元素 crop 成小图**（而非整图画框，显著降幻觉）连同 HTML 属性喂 LLaVA-13B 生成描述 → Llama-3-8B 压成简短指代。**同页文本相同的元素直接丢弃**避免歧义 | **CC-BY-NC-SA-4.0（非商用）** |
| **GUICourse / GUIEnv**（[2406.11317](https://arxiv.org/html/2406.11317)） | GUIEnv-global **1,000 万** + GUIEnv-local **70 万** | C4 取 **400 万 URL**，Playwright 渲染出 1,000 万标注截图。local：裁成小于 1920×1080、**删元素数 < 10 的图**、每图随机抽 10 个元素做 text2bbox / bbox2text | **Apache-2.0** |
| **Aria-UI**（[2412.16256](https://arxiv.org/html/2412.16256)） | **1.37M 截图 / 1,660 万样本** | GPT-4o 或 Qwen2-VL-72B 对「元素孤立图 + 红框放大图 + HTML」生成 caption，再由 LLM 每元素生 **3 条**人类风格指令；fastText 滤有害页；**只保留含 20 个以上有效元素的网页**；1920×1080 与 2440×1600 两档渲染 | **Apache-2.0** |
| **AutoGUI**（[2502.01977](https://arxiv.org/html/2502.01977v2)，ACL 2025） | **702k** 训练 + 2k 测试，916 个域/应用，Web 54.6% | **不用 HTML 文本做指代**：点/悬停元素，diff 交互前后的 a11y 树，喂 Llama-3-70B 推断「功能」。规则 rejection → LLM rejector 丢最低 30% → **双 LLM 验证必须都给满分 3** | **CC-BY-4.0** |
| **Falcon-UI**（[2412.09362](https://arxiv.org/html/2412.09362)） | **1,456K 图 / 434K episode / 312K 域名** | CC 拉页 → Browser API 渲染 + 模拟点击/滚动/输入，**全自动、零人工零 LVLM**；记录全部可见可交互元素 + 字符级 OCR | arXiv CC BY 4.0；**全流程成本 200 美元** |
| **ShowUI**（[2411.17465](https://arxiv.org/html/2411.17465)） | 总 256K 样本 / 270 万元素；自采 web **22K 截图 / 576K 元素** | 自写 PyAutoGUI parser 爬 22 个代表场景站点。**关键过滤：原始 926K 元素 → 删 static text 后留 576K（留存 62.2%）** | 未核实 |
| **OmniParser**（[2408.00203](https://arxiv.org/html/2408.00203)） | **67K** 截图（从 100K 热门 URL 均匀采样）+ **7K** icon-description 对 | DOM 树抽可交互区域；icon 描述由 GPT-4o 生成后微调 BLIP-v2 | arXiv CC BY 4.0 |
| **ScreenAI**（[2402.04615](https://arxiv.org/html/2402.04615)） | 预训练混合约 **4.2 亿**样本，Screen Annotation 占 **3.53 亿** | **完全不用 DOM**：DETR 版面检测器 + 77 类 icon 分类器 + OCR 拼成 screen schema，再喂 PaLM 2-S 生成 QA | 只开放三个评测集 |
| **JEDI**（[2505.13227](https://arxiv.org/html/2505.13227)） | **400 万**合成样本，其中 refusal 部分 260 万+（指令-截图错配） | 多视角任务解耦合成 | arXiv CC BY 4.0 |
| **Aguvis**（[2412.04454](https://arxiv.org/html/2412.04454)） | grounding split **1.036M**（SeeClick 271K + GUIEnv 328K + GUIAct 67K + WebUI 57K + Widget Caption 101K + RicoSCA 173K + UI RefExp 16K + RICO Icon 16K + OmniACT 7K） | 统一到 pyautogui 动作空间 | **Apache-2.0** |

移动端第一代（人工标注，本课题只能当参照）：**RICO**（9.3k apps / 66k 唯一屏 / 300 万元素；13 人众包 2,450 小时、5 个月、**2 万美元**）、**RICO-Semantics**（约 50 万人工标注，CC-BY-SA-4.0）、**Screen2Words**（112,085 摘要 / 22,417 屏）、**Widget Captioning**（162,859 caption / 61,285 widget；**12,960 个 widget 因版权只发 caption 不发截图**）、**VINS**（4,800 图）。

2025–2026 新一代：**UI-TARS**（[2501.12326](https://arxiv.org/html/2501.12326)，开源侧 web **1,480 万元素**，自采部分打星号不披露，约 500 亿 token 续训）、**UIPro**（[2509.17328](https://arxiv.org/html/2509.17328)，**2,060 万** GUI understanding 任务 / 330 万干净元素）、**UI-Venus**（[2508.10833](https://arxiv.org/html/2508.10833)，**从 627k 公开样本清洗到 107k，留存 17.1%**）、**GUI-Net-1M / TongUI**（[2504.12679](https://arxiv.org/html/2504.12679)，100 万条**轨迹**不是 bbox grounding，HF `Bofeee5675/GUI-Net-1M` Apache-2.0 实测 895,170 行）。

### 4.2 正向证据：都在推理期，不在预训练期

**ScreenCoder（[2507.22827](https://arxiv.org/html/2507.22827)）—— 全调研最干净的对照**：同一底座 Qwen2.5-VL-32B、同一权重，只在推理期加 grounding + planning 两个 agent。

| 指标 | 端到端 → ScreenCoder |
|---|---|
| ScreenBench **Position** | 0.613 → **0.755（+0.142）** |
| ScreenBench Block / Color / CLIP / Text | 0.723→0.768 / 0.632→0.734 / 0.762→0.812 / 0.828→0.857 |
| Design2Code **Position** | 0.815 → **0.925（+0.110）** |
| Design2Code Block / CLIP | 0.822→0.865 / 0.893→0.922 |

**收益高度集中在 Position（空间保真），Text 几乎不动** —— 增益来自空间定位而非语义。其 SFT/RL data-engine 消融同理，最大增益项仍是 Position（+0.092）。

| 其他推理期工作 | 关键数字 |
|---|---|
| **UICopilot**（[2505.09904](https://arxiv.org/html/2505.09904)） | Pix2Struct-1.3B 先预测**只含节点类型/层级/bbox 的粗 DOM 树**，按叶节点 bbox 切图后交 GPT-4V 逐块填码。同一代码生成器对照 Visual Score：Short 0.68→**0.84**、Mid 0.65→**0.83**、Long 0.62→**0.78**（自述 +23% / +27% / +48%，**越复杂收益越大**）。反例：去掉全局 refinement 时 block-level color 反而低于 GPT-4V（严格贴粗粒度 bbox 会丢上层样式） |
| **DCGen**（[2406.16386](https://arxiv.org/html/2406.16386)），GPT-4o 底座 | CLIP 83.72→**85.62**、Block-Match 76.1→81.7、Color 81.8→85.4；Design2Code-Hard 81.04→**84.02**。**最该记的一个数：同一模型、同一元素，把截图裁到元素局部，CLIP 相似度 73.7% → 76.0%** —— 「缩小视野 = 定位」本身就提质。但作者限定：收益主要来自**大图（15M–25M 像素区间）**，按 DOM 深度或标签数切时只有约 **2%** |
| **LaTCoder**（[2508.03560](https://arxiv.org/html/2508.03560)） | 切块 → 每块独立生码 → **按 bbox 绝对定位拼装**。DeepSeek-VL2 在 CC-HARD：TreeBLEU **+66.67%**、MAE **−38.53%**；GPT-4o 在 Design2Code-HARD：TreeBLEU +17.65%、MAE −37.41% |
| **LayoutCoder**（[2506.10376](https://arxiv.org/html/2506.10376)） | 消融显示**布局相关组件在 Design2Code 上只值 +0.17~0.42 BLEU / +0.37~3.33 CLIP**，远小于它跟基线的差距。主表 Snap2Code(Seen) BLEU 26.07 是**同分布过拟合量级，不要当通用结论引用** |
| **ComUICoder**（[2602.19276](https://arxiv.org/html/2602.19276)） | 块级分割消融：Block-Match 0.7917→**0.8605**。但同表有反例：**UICopilot 0.6501、LaTCoder 0.7588，都低于直接提示的 0.8524** |

**这些工作之间互相打架**（LaTCoder 报告 DCGen 退化、ComUICoder 报告 UICopilot/LaTCoder 不如直接提示），结论随底座和基准翻面。能站得住的最小公约数是：**有效的是「bbox 锚定 + 绝对定位拼装」，不是「只给子区域一段自然语言描述」。**

### 4.3 训练期 bbox 条件监督：几乎无人隔离消融

- **UI2Code^N** §3.1 的 GUI-REG 目标：给图 I 与某 DOM 节点 bbox b，预测该框对应的代码片段 C_b（损失 `L_dom`），与整页的 `L_pair` 混合优化，理由是「强化局部 grounding」并控制序列长度
- 它的三个消融（§4.3 reward 设计、§4.4 真实网页、§4.5 训练阶段）**没有任何一个剥离 `L_dom`**。所以「bbox 条件监督优于整页监督」在它这里**只有设计理由陈述，没有对照数字**
- **引用陷阱（重要）**：§4.5 / Table 6 的阶段消融在 **arXiv v1 中不存在**（v1 只有 Table 1–4），必须引用当前版本
- **WebCode2M** 把每条数据升级为三元组（code, image, **layout = HTML 元素 bbox 树**），论文自述 bbox 可作训练目标，但 WebCoder-1.3B 是否真用了**未核实**。它给的「WebSight 训 vs WebCode2M 训」对照是**数据真实度**效应，不能归因到 bbox
- **WAFFLE**（[2410.18362](https://arxiv.org/html/2410.18362)）是 HTML **树结构感知注意力** + 对比学习，**不是 bbox**：WebSight HTML-Match 28.00（标准微调）→ 30.80（只对比学习）→ 35.80（只结构注意力）→ **37.00**（完整）。**结构注意力单独贡献大于对比学习**

### 4.4 反向证据最硬：HTML 结构监督 → UI 元素级任务

Pix2Struct 的 screenshot-parsing 消融（§3.1 的表）之外，还有一组更直接的：**Pix2Struct-Large 在纯像素输入下，RefExp 94.2 超过带 a11y 树输入的 UIBert 90.8；Widget Captioning 136.7 vs VUT 97.0；Screen2Words 109.4 vs 64.3**（[2210.03347 Table 1/2](https://arxiv.org/html/2210.03347v1)）。

**「学写 HTML」得到的表征直接可做 UI 指代与元素定位。** 这是 grounding 与 code 共享底层表征的最强证据 —— **但方向是 code → grounding，不是 grounding → code。**

另有 GUI 侧「grounding 预训练有用」的硬数字可作类比：

| 工作 | 消融 | 结果 |
|---|---|---|
| **SeeClick** | Qwen-VL vs 加 grounding 预训练 | ScreenSpot **5.2 → 53.4**；同等 2.8K 下游数据：MiniWob **48.4→67.0**、AITW 54.3→59.3、Mind2Web **11.5→20.9** |
| **Aguvis**（Table 15） | 两阶段 | 完整 ScreenSpot **81.2**；**去 Stage1（grounding）降到 71.3**，Mind2Web Cross-Task 55.3→42.5；两阶段全去只剩 3.8 |
| **UGround**（Table 9） | 数据源 | 仅 Web-Hybrid **76.9**；仅其他源 73.4；全部 **81.4** |
| **AutoGUI**（Table 5） | **标注类型等量对照** | 25k 时：HTML 属性抠的指代 ScreenSpot **5.7** vs 交互推断的功能描述 **16.4**；125k 时 **17.0 vs 27.0**。**从 HTML 属性抠出来的指代文本，单位样本价值明显低于交互推断的功能描述** |

### 4.5 负面证据

**① GUIMid 的 11 域横评**（已在 §3.8 给完整表）：Web Screenshot2Code 与 GUI Perception 是最没用的两个中训练域，纯文本数学与纯文本代码反而更高。**但注意它的下游是 GUI agent，不是写代码。**

**② GLM-4.1V §6.3 的跨域 RL 矩阵**（Figure 6 是 PNG，正文无数值；下列数值由读图得到，单位 = 相对 SFT checkpoint 的平均分绝对提升）：

| 训练域 ＼ 评测域 | STEM | OCR & Chart | Grounding | GUI Agent | Image General |
|---|---|---|---|---|---|
| Mix All | +6.6 | +5.2 | +30.1 | +6.0 | +3.4 |
| GUI Agent | +2.4 | +1.5 | **+9.0** | +9.2 | +1.6 |
| **Grounding** | **−0.5** | **−4.6** | +30.4 | **+8.1** | **−0.4** |
| OCR & Chart | +3.0 | +1.2 | **−14.5** | +5.8 | +1.3 |
| STEM | +3.0 | −0.2 | +10.5 | +3.5 | +1.1 |

- **这个矩阵里没有 coding 维度**。五个评测域是 STEM / OCR&Chart / Grounding / GUI Agent / 通用 VQA。**所以它不能回答「grounding 是否帮 code」**
- **grounding ↔ GUI agent 强互促**（+8.1 / +9.0）
- **只训 grounding 是全表唯一出现多个负值的行**（OCR&Chart −4.6、STEM −0.5、通用 −0.4）。grounding 是最窄、最自私的训练域
- **混合不是免费午餐**：Mix All 在 grounding（+30.1 vs +30.4）与 GUI Agent（+6.0 vs +9.2）上都不如单域

**③ Aguvis Table 14 的两条反直觉**：联合训练 ScreenSpot 升（84.4→85.0）但 Mind2Web 全线降（Cross-Task 58.5→56.1）；**砍掉 grounding 后 ScreenSpot 暴跌 84.4→77.4，但 Mind2Web Cross-Task 反而 58.5→59.7 上升**。即 **grounding 数据量大时会压制 planning**。

**④ MiMo-VL §5.3 的机制性解释**：推理任务推高 CoT 长度，**grounding / 计数任务压缩 CoT 长度**，两者在 RL 中方向相反、互相干扰（定性，无数值）。

**⑤ UI-Venus**：grounding 与 navigation 两套 reward 同训「训练不稳，ultimately degrading performance on both tasks」。

### 4.6 「点哪里」QA 的 ground truth 怎么自动拿

| 路线 | 代表 | 优点 | 拿不到什么 |
|---|---|---|---|
| **DOM + getBoundingClientRect**（Playwright / Puppeteer） | GLM-4.1V、UGround、GUICourse、OS-Atlas、SeeClick、WebCode2M | 最便宜、可无限扩 | **canvas 内元素、跨域 iframe、Shadow DOM、CSS 伪元素**；渲染后 box 偏移 |
| **Accessibility tree** | WebUI、UI-TARS、OS-Atlas（桌面）、AutoGUI、GUI-Owl | 已过滤纯样式 div，自带语义角色 | 依赖开发者是否写 ARIA —— **WebAIM 2024：95.9% 的首页存在无障碍错误，平均每页 56.8 个**（[webaim.org/projects/million](https://webaim.org/projects/million/)） |
| **纯 CV 管线**（检测器 + icon 分类 + OCR） | ScreenAI、Ferret-UI、OmniParser | 不依赖任何源码，跨平台 | 受检测器天花板限制；Ferret-UI 自述「UI detection model is a bottleneck」，学不到颜色、设计 |

桌面端 a11y 实现各异：OS-Atlas 用 **pyatspi**（Ubuntu）、**pywinauto**（Windows）、**ApplicationServices**（macOS）。

**噪声来源与实测比例**

| 噪声类型 | 实测数字 | 来源 |
|---|---|---|
| **开源 grounding 数据整体噪声率** | **约 40%**；表现为「严重时整图所有框朝同一方向整体平移」、嵌套元素破坏一一对应 | UI-Venus |
| **逐源 invalid element 率** | SeeClick-Web **0.2%**、Android Emulator 0.4%、Common Crawl **2.5%**、MultiUI 3.0%、AndroidControl 11.5%、**WebUI 14.4%**、MobileViews 24.5%、WAE **29.0%** | UIPro Table 17 |
| **元素太小** | WebUI 中**三分之一的可交互元素小于 44×44 px**（违反 WCAG）；平均 bbox 面积约 14,000 px² | WebUI §3.2.2 |
| **遮挡** | WebUI **18% 的屏**含重叠叶子元素，其中仅三分之一遮挡面积超过 20% | 同上 |
| **响应式失败** | 仅 **70%** 的页满足 content-width 响应性，80% 有 viewport meta | 同上 |
| **不可见 / 错位元素** | CLAY 口径 **37.4% 的屏**含 invalid object，invalid:valid 约 1:8 | [2201.04100](https://arxiv.org/html/2201.04100) |
| **a11y label 缺失** | 77% 的 app、60% 的屏至少一个元素无显式标签；**53% 的 Image Button 缺标签** | RICO-Semantics 引 Ross et al. 2020 |
| **静态文本信息量低** | web 元素中 static text 约占 **40%** | ShowUI |

**UIPro 的过滤规则集（阈值明确，可直接抄，§8.3）**
1. 删 bbox 越界或面积为 0 的元素
2. 删**面积占比超过 0.65** 的超大元素（多为父节点，中心点会落在子叶上造成歧义）
3. 删**最小边小于 18 px** 的元素（由 Android 无障碍指南 48dp 折算：48×60/160）
4. 删空白元素（元素区域颜色 `np.std` **小于 5**）
5. 同 bbox 重复元素只留一个（image button 常同时有 image 与 button 两个节点）
6. 用 pytesseract OCR，**与元素 text 属性相似度小于 22** 的判为不可见文本删掉

**各家留存率**

| 工作 | 输入 → 输出 | 留存率 |
|---|---|---|
| WebCode2M | 5 亿 CC 网页 → 256 万 | 约 **0.5%** |
| OS-Atlas（web） | 400 万网页 → 370 万截图 / 3,700 万元素 → 160 万 / 770 万 | 元素 **20.8%**，截图 43% |
| UI-Venus | 627k → 107k | **17.1%** |
| TongUI / GUI-Net-1M | 去重 + 内容过滤 + 轨迹过滤 | **33.0%** |
| **Falcon-UI** | 1,019K episode / 3,431K 图 → 434K / 1,456K | **42.6% / 42.4%**；全流程成本 **200 美元** |
| ShowUI（web） | 926K 元素 → 576K | **62.2%** |
| Widget Captioning | 78K 屏 → 24,571 屏 | 约 31% |
| RicoSCA | 72K 屏 → 25,677 屏 | 约 **35.7%** |
| WebUI | **不过滤、不修复**，只诊断缺陷 | 100%（留给下游） |

**过滤值多少分（这三条决定要不要花力气）**
- **UIPro 去噪消融**（6.7M 样本，带/不带）：FuncPred 64.3→**66.7**、ScreenSpot 55.7→56.4、MOTIF 66.9→**69.2**、RefExp 43.5→**45.8**。**清洗只值 +0.7 ~ +2.3 分**
- **ShowUI 删静态文本**：元素砍 37.8%，ScreenSpot 平均 **66.6→69.0（+2.4）**，其中 Desktop Icon 50.0→**60.3**、Web Icon 52.9→**62.1**。**砍量反而涨分，是性价比最高的一条**。另：自采 **22K** 网页打过 SeeClick 的 **270K** 截图（69.0 vs 65.5）
- **AutoGUI 质量阶梯**：无过滤 **64.5%** → 加手写规则 **83.1%** → 加 LLM rejector **94.4%** → 单 LLM 验证 96.0% → **双 LLM 96.7%**（受训人类标注员 95.5%）

### 4.7 scaling：UGround 的原文表述

关于「UGround 在 773K 网页上 100K 之后收益递减」—— **这句话在原文中确实存在**（[2410.05243 §3.5](https://arxiv.org/html/2410.05243)）：

> "The scaling results in Figure 5 show that the average performance consistently improves as the data scales up, **though the return starts diminishing after 100 K screenshots**. Notably, with just 50 K screenshots (about 600 K elements) as training data, UGround surpasses SeeClick by more than 10 %, which is trained on about 3 M web and Android elements from about 400 K screenshots. ... **additional data after 100 K screenshots primarily enhances understanding of less frequent elements such as radio buttons, checkboxes, or very small text elements.**"

两条更有用的补充：
- **5 万截图（约 60 万元素）就能超过 SeeClick 10 个点以上**，而 SeeClick 用了约 300 万元素 / 40 万截图 → **标注质量远比数量重要**
- 10 万截图之后的增量主要买的是**长尾元素**（radio button、checkbox、极小文本）和**中心点精度**，不是平均分

有完整数值表的只有 **GUICourse 的 GUIEnv-global 四档**（2.5M / 5M / 7.5M / 10M）：Bbox2Text EM 35.87→40.21→43.60→**44.12**；Text2Bbox IoU@0.5 25.32→35.09→40.67→**47.96**；Web-Single StepSR 64.82→68.30→68.58→**70.57**（完全不加 GUIEnv 时分别是 14.92 / 2.15 / 52.84）。**读法：从 0 到 2.5M 是质变（2.15→25.32），2.5M 到 10M 只是线性缓升。**

OS-Atlas Figure 3、UIPro Figure 6、SeeClick Figure 6、UGround Figure 5 的逐点数值**都只在图片里，正文与 HTML 无数值**。

### 4.8 本节落到行动上

1. **立刻可做**：按「功能描述优于 HTML 属性文本」与「删静态文本」改配方。AutoGUI 等量对照显示功能标注高 10 个点以上；ShowUI 删 38% 静态文本反而涨 2.4 分（Icon 项涨 10 分）。若自建的 REG/REC 里 static text 占比接近 40%，有很大瘦身空间
2. **必须做的那个实验**：固定 image-to-code 训练配方，只切换「有/无 `L_dom`（bbox → HTML 片段）」，测 Design2Code-HARD / CC-HARD 的 TreeBLEU 与视觉分。**这不只是补文献空白 —— 鉴于 GUIMid 的反证与 ScreenCoder / UICopilot 的正证互相矛盾，这个实验是在两条冲突证据之间做裁决**
3. **缓解副作用的三条有数据支撑的手段**：① Web2Code 的 DWU 理解 QA 既提代码分（6.402→6.716）又把被代码数据打掉的理解分救回（60.00→69.33）；② UI2Code^N 明确把 coding 数据与通用 VL 任务交织；③ Aguvis 证明**分阶段优于联合**（Stage1→2 的 Mind2Web 58.5 vs 联合的 56.1）

---

## 5. 去重与污染

### 5.1 视觉去重：各家的具体阈值

| 方法 | 具体阈值 | 实测效果 | 来源 |
|---|---|---|---|
| **pHash 汉明距离** | 各家论文**都不写阈值**。MiMo-VL 只说「employ phash-based image deduplication to eliminate potential overlaps between training datasets and evaluation benchmarks」；WebCode2M 只说「按截图 hash 快速去重」 | — | [2506.03569 §2.2](https://arxiv.org/html/2506.03569v1) |
| **SemDeDup（CLIP embedding + k-means）** | **k = 50,000** 个聚类（CLIP 图像编码器空间；语言侧 OPT embedding 用 k = 11,000）。簇内算全部 pairwise 余弦相似度，超过阈值判语义重复，每组**保留离簇心余弦相似度最低的那个** | LAION-440M 去掉 **50%**，性能几乎不降、训练速度翻倍，且 **OOD 性能反而上升** | [2303.09540](https://arxiv.org/html/2303.09540v1) |
| **DataComp 的 benchmark 去重** | 用 Yokoo 的去重模型（Facebook AI Image Similarity Challenge 第一名），**余弦相似度阈值 0.604169**（论文明确给到小数第 6 位，是调出来的） | 在 16.8B 图里**标出约 3%** 为评测集近重复，13.6B → 13.1B | [2304.14108 §3.2 + App. F](https://arxiv.org/html/2304.14108v1) |
| **BigDocs 的污染度量** | 用 embedding 余弦相似度的累积分布；**人工验证后的判据：< 0.96 基本没问题，> 0.98 几乎肯定有问题**（前 200 条人工打标定出来的） | 见下表 | [2412.04626 Table 4](https://arxiv.org/html/2412.04626v1) |
| **Objaverse-XL 的坏图分类器** | CLIP 特征 + 2 层 MLP，1.2K 人标训练，CV 精度 > 90%，**阈值 0.5**；NSFW 分类**阈值 0.9 且要 ≥3 个视角命中**才算 | Polycam 的 71K 对象里 38.20% 渲染图判坏 | [2307.05663](https://arxiv.org/html/2307.05663) |
| **GLM-4.1V 的 caption 过滤** | CLIP-Score **≥ 0.3** 留下；视频侧用「图与文 embedding 同时与另一条高度相似」才判重复 | — | [2507.01006 §3.1](https://arxiv.org/html/2507.01006v1) |

BigDocs 的污染对照（命中率，越低越好）：

| 阈值 | 参考训练集 | DocVQA | InfoVQA | KLC | ChartQA | MMMU | DudeMini |
|---|---|---|---|---|---|---|---|
| 0.99 | DocStruct4M | 0.016 | 0.0 | 0.0033 | 0.034 | 0.0026 | 0.0089 |
| 0.99 | BigDocs-7.5M | 0.0036 | 0.0 | 0.0 | 0.025 | 0.0 | 0.0089 |
| 0.98 | DocStruct4M | 0.065 | 0.0032 | 0.061 | **0.36** | 0.0044 | 0.013 |
| 0.98 | BigDocs-7.5M | 0.012 | 0.0 | 0.0033 | **0.10** | 0.0035 | 0.011 |
| 0.96 | DocStruct4M | 0.26 | 0.0057 | 0.24 | 0.63 | 0.0070 | 0.15 |
| 0.96 | BigDocs-7.5M | 0.12 | 0.0 | 0.12 | 0.28 | 0.021 | 0.14 |

- 读法：**ChartQA 在 0.98 阈值下，DocStruct4M 有 36% 的测试样本在训练集里有近重复** —— 图表类数据的污染极其严重，因为图表的视觉空间小。做 visual coding 时，图表与简单落地页这两类**天然高污染**
- 可直接抄的做法：余弦相似度 CDF 曲线 + 人工标前 200 条定阈值，而不是拍一个数

### 5.2 代码 / HTML 侧的去重

| 项 | 做法与参数 | 效果 |
|---|---|---|
| **The Stack v2 近重复** | MinHash + LSH，**5-gram、Jaccard 相似度 0.7**；每组只留一个，**优先留 star / fork 多的仓库，其次留最新 commit**（为保住仓库上下文） | 900B+ unique token，是 StarCoder 1 数据集的 4 倍 | 
| **HTML 的实际保留率** | The Stack v2 dedup 的 HTML 有 90.23M 文件 / 2,419.87 GB，但进 StarCoder2-15B 训练的只有 **5.23M 文件 / 99.09 GB**（**5.8%**）；CSS 7.9% | 说明「HTML 池子看着很大，过完质量闸只剩 1/17」 |
| **WebCode2M 的多层去重** | ① 截图 hash 快速去重（训练集）；② 候选测试集再用 **CLIP 相似度**去重 + 逐条人工复检 | 净化版比原版少 60.9 万行（19.2%） |
| **GLM-5 的代码去重口径** | 「模糊去重后唯一 token 数 **+28%**」—— 注意这是**刷新快照后新增**的量，不是去重率 | — |

来源 [2402.19173 §3.1 + Table 1](https://arxiv.org/html/2402.19173v1)。

### 5.3 与 benchmark 去重：本课题特有的三个雷

1. **Design2Code 与 Vision2UI 都来自 C4 / Common Crawl**。只要训练集也从 CC 来，就天然有污染通道。Design2Code 用的是 **C4 validation split**，WebCode2M 用的是 **CC-MAIN-2023-50**，两者时间与 split 不同但站点会重合。**必须按 URL 与域名两级去重，而不只是按截图**
2. **MultiUI 是唯一在源头做对的**：「先剔除出现在下游 benchmark 里的 URL」，在抓取前就挡掉。这比事后按图去重便宜得多，应当照抄
3. **「WebSight / WebCode2M 训练集与 Design2Code 测试集的视觉重叠率」这个数字，公开文献里没有人测过**（已确认，不是漏查）。这是一个可以自己补的空白：用 DataComp 的 Yokoo 模型 + 阈值 0.604，或 pHash + CLIP 双路，在 484 条测试集上扫一遍即可

需要冻结、不得入训练的评测源清单已在 `webdev-data` 第二章 2.3 节列出（VIBE 200、ArtifactsBench 1,825、Design2Code 484+80 HARD、WebGen-Bench 101 等），本文只补三条新的：**WebCode2M-Short/Mid/Long 各 256**、**ScreenBench 1,000**、**Shadereval-inputs 467**、**GenCAD-Code test 7,355**。

### 5.4 许可风险（以下非法律意见）

**A. 代码侧：GPL / AGPL**

| 项 | 事实 |
|---|---|
| The Stack v1 | **只收宽松许可**；提供 "Am I in The Stack" 查询工具与 opt-out 流程 |
| The Stack v2 | 收**宽松许可 + 无许可**两类；**明确排除 copyleft**，理由写得很直白：「由于社区对能否用这类数据训练 LLM 的立场不明确，且其体量相对小，我们排除 copyleft」；也排除商业许可（「作者不希望被商用」）。宽松许可清单取自 Blue Oak Council + ScanCode 归为 Permissive / Public Domain 的许可 |
| 许可检测的实际困难 | **96.93% 的仓库拿不到 repo 级许可**，只能用 ScanCode 扫文件级：正则找可能含许可的文件（LICENSE、MIT.txt、README.md…）→ ScanCode 检测 → 把 SPDX ID 沿同一 base path 传播给该目录下所有文件。这意味着**许可标注本身是启发式的、会错** |
| 判例状态（2026-10） | **Doe v. GitHub（Copilot）**：第九巡回法院 **2026-09-16** 维持原判，驳回 DMCA §1202(b) 主张，理由是工具生成的是新作品、并非从既有作品中移除或篡改版权管理信息；法院同时否定了「identicality（必须字面相同）」这个框架，称其是对法条用语的注解而非独立要件。合同类主张（开源许可违约、违约）仍在地区法院待审。[Haynes Boone 快报](https://www.haynesboone.com/news/alerts/ai-legal-news-ninth-circuit-rejects-dmca-section-1202(b)-theory) |
| | **Bartz v. Anthropic**：2025-06 Alsup 法官在简易判决中区分开两件事 —— 用**合法取得**的书训练属合理使用（transformative），但**下载并留存盗版库**不受保护。2025-09-05 达成**至少 15 亿美元**的集体和解（覆盖最多 50 万部作品、约每部 3,000 美元），并销毁相关数据集。[Kilpatrick 快报](https://ktslaw.com/insights/alert/2025/9/parties-reach-a-landmark-settlement-in-the-bartz-v-anthropic-litigation) |
| 对本课题的直接含义 | 「训练本身」的风险低于「**语料来源的合法性**」。所以挖 GitHub 做渲染配对时，**真正要守的是许可过滤与来源可追溯**，而不是纠结训练行为 |

**B. 素材侧：CC BY-NC**

| 来源 | 许可 | 影响 |
|---|---|---|
| ShaderToy | 站点默认 **CC BY-NC-SA 3.0** | 2 万个高质量 shader 商用禁区。**但 The Stack v1 里有 167,701 个 permissive GLSL 文件（0.40 GB）可用**，渲染自己跑（单卡 979 fps），这是绕过去的正路 |
| CAD-Recode 的 1M 数据 | **CC-BY-NC-4.0** | 数据不能商用，**但它的合成算法可以复现** —— 这才是真资产 |
| `redcathode/thingiverse-openscad` | **CC-BY-NC-SA-4.0** | 7,378 条，量小且 NC |
| Objaverse-XL | 整体 ODC-By 1.0，但**单个对象各自许可**，GitHub 来源「不保证可商用」 | 要用必须逐对象查许可，工程上等于要维护一张 1,000 万行的许可表 |
| BlendNet | **Apache-2.0** | 本调研里唯一许可完全干净的 Blender 脚本集，12,059 条 |
| Poly Haven | CC0 | 做贴图 / HDRI / 模型原料零风险（已在 `02_task_sources.md` 覆盖） |
| **DaTikZ 的教训** | HF 卡片原文：「In compliance with licensing agreements, **certain TikZ drawings are excluded** from this public version of the dataset」，并提供工具让用户自己重建完整版 | 这是「公开版因许可而残缺」的标准做法，自建数据集时应照此设计：**内部完整版 + 公开残缺版 + 重建脚本** |
| **BigDocs 的许可普查** | 调研了 **133 个**现有数据集，**80%（约 100 个）是非宽松许可或许可不明**，最终只留下 **16 个** | 这是「现成多模态文档/代码数据集里只有两成能商用」的硬数据 |

**C. 网站 ToS 与爬取**

| 项 | 事实 |
|---|---|
| **Common Crawl 自身的 ToU**（[最后更新 2024-03-07](https://commoncrawl.org/terms-of-use)） | **这是本节最该读的一条原文**。ToU 的赔偿条款明确把以下情形的全部损失推给使用者：「(ii) 将 Crawled Content 用于人工智能、机器学习或类似技术，**包括但不限于大语言模型与神经网络，包括为开发、训练或部署 AI 系统而使用 Crawled Content**；(iii) 用 Crawled Content 创建、使用或分发任何内容」。并写明「你不得依赖 CC 创建或累积的任何 Crawled Content」「CC 强烈建议你在对本服务或 Crawled Content 做任何使用（包括商业使用）之前取得法律意见」「使用 Crawled Content 即表示你同意尊重其中第三方的著作权及其他权利」 |
| 含义 | CC 是**便利工具，不是许可来源**。用 CC 的 URL 重爬与直接用 CC 的 WARC，在法律位置上没有本质差别；两者都要自己承担底层内容的权利问题 |
| robots.txt / noai | Design2Code、BigDocs、UI2Code^N 都声明遵守（BigDocs 把「robots.txt 合规」做成逐站闸）。UI2Code^N 额外声明不抓登录保护、付费墙、用户私有内容 |
| **Stack Exchange 2024-07 的变更** | data dump 从 Internet Archive（每三个月一次，最后一次 2024-04）改为必须登录站点从个人资料页下载，并**必须同意「该文件仅供我自己使用、且用于不包含训练大语言模型的项目」**；违反者 SE 保留拒绝后续下载的权利。早期草案曾更宽（「非商业使用」），后收窄到专指 LLM 训练。社区争议点是 CC BY-SA 4.0 明文禁止附加限制；SE 回应「产品与法务都签过字」。目前**没有判例裁定该附加条件在 CC BY-SA 4.0 下是否可执行**。[devclass 报道](https://www.devclass.com/development/2024/07/30/stack-exchange-restricts-access-to-dump-of-user-contributed-data-critics-complain-this-contradicts-license/1625192) |
| 含义 | Blender StackExchange / StackOverflow 的 bpy 与 three.js 问答（在 `02_task_sources.md` 里估了约 2 万条）**法务上处于灰区**，不适合做基座语料；更适合当「问题线索源」，答案自己重新生成

### 5.5 做一个 1,000 万级 image-to-code 预训练集：去重与许可流水线

每道闸都给初值阈值与预期剔除比例（**阈值全部是初值，必须在自己第一个 chunk 上校准**，这是 WebCode2M 定 NSFW=0.04 的做法）。

| # | 闸 | 判据与初值 | 预期剔除 | 依据 |
|---|---|---|---|---|
| 1 | **URL 级 benchmark 预排除** | 先把 Design2Code（C4 validation）、WebCode2M 测试集、ScreenBench、WebGen-Bench 等所有评测源的 URL 与**注册域名**建成黑名单，抓取前就挡 | < 0.1% | MultiUI 的做法 |
| 2 | URL 精确去重 | 规范化后 sha256 | 视快照而定 | S4 |
| 3 | 许可与 ToS 闸 | robots.txt 合规 + noai meta + 登录/付费墙排除 | 10~20%（推断） | BigDocs / UI2Code^N |
| 4 | 结构与长度粗筛 | HTML 字符数 ∈ [640, 10240]、CSS ∈ [640, 20480]；DOM 深度、元素数、JS/CSS 文件数 | 大头在这里 | WebCode2M |
| 5 | 渲染闸 | Playwright，CSS/JS/字体/图片**本地缓存**；记 HTTP 状态、console error、资源 4xx/5xx、首屏空白 | 20~40%（推断） | S4（500 CPU → 500 万页/天） |
| 6 | 不可见元素剪枝 | CSS visibility + **点击校验**（点 bbox 中心，返回元素不是其后代就剪）+ 溢出文字剔除 + 丢 iframe | 节点级 | S4，这条必抄 |
| 7 | 内容安全 | NSFW 分类器**阈值 0.04**（只留低于）+ 多语言脏词表（单页 > 20 次则删） | 约 5%（WebCode2M 口径） | WebCode2M App. C |
| 8 | 美观/质量打分 | 人工标 1 万条（5 条判据各 1 分）训一个 ResNet-50 级分类器，**只留 score ≥ 2** | **约 52.5%** | WebCode2M |
| 9 | 截图精确去重 | 截图 sha256 / 64-bit pHash | 几个百分点 | WebCode2M |
| 10 | 截图语义去重 | SemDeDup：CLIP 特征 + **k = 50,000** 聚类，簇内 pairwise 余弦超阈值判重，保留离簇心最远者 | **可以去到 50% 且不掉点** | SemDeDup |
| 11 | 代码近重复 | MinHash + LSH，**5-gram、Jaccard 0.7**，保留 star/fork 高者 | 10~30%（推断） | The Stack v2 |
| 12 | 模板/家族去重 | 依赖集合 + 目录结构 hash 建 `family_id`，训练/评测按 family 与**注册域名**分组切分 | 不剔除，只约束切分 | WebUI（按域名 70/10/20） |
| 13 | **评测集视觉去污染** | Yokoo ISC 模型，**余弦阈值 0.604169**；或 CLIP 余弦 > 0.98 直接剔、0.96~0.98 送人工 | **约 3%** | DataComp / BigDocs |

- 口径提醒：这 13 道闸**不是独立相乘**（渲染闸和长度闸会重叠）。按 Design2Code 的 0.38% 与 WebCode2M 的「5 亿 → 256 万」反推，**从原始 CC 页面到可用配对的端到端保留率量级是 0.5%**
- 所以**要产出 1,000 万条可用配对，起点需要约 20 亿个候选页面**（推断，依据 WebCode2M 的 5 亿 → 256 万 ≈ 0.51%）
- 渲染是成本瓶颈：WebCode2M 整条流水线约一个月，**其中 80% 时间在 Playwright 渲染**。按 S4 的 1 万页/CPU-日，渲 2,000 万页需要 **2,000 CPU-日**；渲 2 亿页需要 2 万 CPU-日。所以**第 4 道长度/结构闸必须放在渲染之前**，这是整条管线最重要的顺序约束

### 5.6 多样性崩塌：UI 领域是真空，只能借通用证据

**先说结论：对「LLM 合成 UI / 网页 / 截图」的多样性，没有任何工作给出过 pHash 近重复率、CLIP 特征方差、unique-HTML-tag 覆盖率的测量值。** WebSight 技术报告只说用 Mistral-7B 生「几百万个 unique website concepts」，**v0.1 vs v0.2 的多样性对比数字在论文和 HF 卡片里都没有**（已确认，不是漏查）。

能借用的通用证据：

| 工作 | 可直接用的数字 |
|---|---|
| **On the Diversity of Synthetic Data**（[2410.15226](https://arxiv.org/html/2410.15226)，LLM Cluster-agent） | ① **启发式多样性基线集体失效**：K-means cluster score 把 300K topics 判得比 100K topics 还低（方向错）；② 下游（350M pretrain avg）T=100K × G=10/20/30 → 50.12 / 50.26 / 50.50；T=300K → 50.65 / **51.28** / 51.05（G=30 回落）；③ prompt 模板：Real Only 48.94 → Topic 51.40 → Topic+Styles 51.81 → **Topic+Styles+Persona 51.92** → Multi-Topic 51.74（**更「多主题」反而更不多样**）；④ 真实:合成配比 —— 12.9B 合成上采样到 1→20B 持续涨，**超过 34B 后平均准确率显著下降** |
| **Self-Consuming Models Go MAD**（[2307.01850](https://arxiv.org/html/2307.01850)） | 指标 = FID + precision（质量）+ recall（多样性），k=5 近邻。纯合成回路跑 100 代（WGAN-GP/MNIST）：FID 0→300、**precision 0.3→0、recall 0.6→0 双双归零**；加采样偏置 λ<1 时 precision 可维持但**recall 衰减明显更快**；合成增广回路（固定 70k 真实 + 线性增长合成池）只延缓不阻止 |
| **The Curse of Recursion**（[2305.17493](https://arxiv.org/html/2305.17493)） | OPT-125m/wikitext2，5 epoch、无原始数据的代际合成训练使 ppl **20 → 28**；**保留 10% 原始数据只有轻微退化**；repetition penalty=2.0 反而使 ppl 翻倍 |
| **Nepotistically Trained Models Collapse**（[2311.12202](https://arxiv.org/html/2311.12202)，图像，最接近渲染图场景） | SD v2.1、每代 900 张、5 代：**自生成占比低到 3% 仍然塌缩**；颜色直方图匹配与剔除高 FID 单图两种 curation **塌缩速率相同（即常规 curation 完全无效）**；25% 污染的模型用纯真实数据「治疗」5 代后 FID 回基线，但 **CLIP std 从基线 2.8（mean 35.1）变 4.2（mean 27.3）** |
| **人机共写的同质化**（[2309.05196](https://arxiv.org/html/2309.05196)，唯一给了完整 n-gram 表的） | 语料级 Rouge-L 同质化 Solo 0.1536 / GPT3 0.1578 / **InstructGPT 0.1660**（p<0.05）。unique n-gram 比例 n=1~5：Solo 0.119/0.602/0.898/0.973/0.991 → InstructGPT **0.115/0.579/0.869/0.953/0.977**。unique key points（阈值 0.5/0.6/0.7/0.8）：Solo 0.982/0.941/0.792/0.543 → InstructGPT **0.950/0.877/0.738/0.494** |
| **合成代码的去重** | SelfCodeAlign（[2410.24198](https://arxiv.org/html/2410.24198)）：The Stack V1 的 5M 带 docstring 函数 → **MinHash+LSH Jaccard 阈值 0.5** 去重 → 250K 种子；同为 74K 数据时 HumanEval+ pass@1 **67.1** vs Evol-Instruct 59.1 / OSS-Instruct 61.6 / GPT-4o 直蒸 65.9。Case2Code（[2407.12504](https://arxiv.org/html/2407.12504)）：2.3M 函数 → 执行过滤 1.3M，约 10 种 prompt 模板；单模板 vs 多模板「in-domain 几乎无差，**OOD 显著受损**」 |
| **文生图的「多样性旋钮」** | StableRep（[2306.00984](https://arxiv.org/html/2306.00984)）：CC3M 每个 CFG w 生一份训 SimCLR，**最优 w≈8（62.0%）**比真实图 60.4% 高 1.6%；但 **FID 最优是 w=2** —— **质量/多样性指标与下游完全不一致**。GLIDE 侧（[2210.07574](https://arxiv.org/html/2210.07574)）：EuroSAT 上 language enhancement 把 FID 从 84.84 降到 81.15（多样性升）但准确率从 44.27 掉到 35.84 |

**对本课题的三条操作含义**：
1. **多样性指标不要信 FID / cluster score 这类无监督量**。StableRep 的「FID 最优 w=2，下游最优 w=8」和 Cluster-agent 的「K-means 判反了」是同一个教训。要测就测下游
2. **合成占比有硬上限**。Cluster-agent 的「合成超过真实 34B 后掉点」是目前唯一的定量锚点；Nepotistically 的「3% 自生成污染即塌缩」说明**自己模型生成的页面绝对不能回流进预训练**
3. **recall（多样性）比 precision（质量）衰减得更快**（Self-Consuming）。所以做质量闸时要专门留一个多样性监控，不能只盯美观分 —— 美观分高的页面恰恰最同质

---

## 6. 建议：可执行的数据获取优先级清单

### 6.1 优先级表

规模预期、工程成本、法务风险三列都给具体依据。工程成本按「CPU-日 / GPU-日 / 人-周」计。

| 优先级 | 动作 | 规模预期 | 工程成本 | 法务风险 | 为什么排这个位置 |
|---|---|---|---|---|---|
| **P0** | **自建「URL 种子 → 重爬 → 渲染 → 十任务头」管线**（抄 S4 + UI2Code^N） | 一个 CC 月度快照约 **21 亿页**（2026-09 快照 2.17B / 361.4 TiB），按端到端 0.5% 保留率 → **约 1,000 万配对** | 渲染 **2,000 CPU-日**（按 S4 的 1 万页/CPU-日，先过长度闸只渲 2,000 万页）+ 爬取带宽 + 2 人-周写闸 | 中：CC 的 ToU 把责任全推给使用者，必须自己做 robots/noai/付费墙三闸 + 许可字段登记 | 这是唯一能拿到千万级真实配对的路；而且**一次渲染能派生十个监督头**（§4），边际成本最低 |
| **P1** | **从同一次渲染里抽 bbox ↔ DOM 片段的 grounding 对** | 同上 1,000 万页 → **1 亿+** 条（GLM-4.1V 实测 1.4 亿） | 增量近零（Playwright 已经返回 bbox），需加 S4 的点击校验剪枝 | 同上 | 成本近零所以值得做，**但要先做一个小规模消融验证它真的提升写代码** —— GUIMid 的横评显示 GUI Perception 做中训练对 GUI agent「does not help a lot」，§4 的证据是矛盾的 |
| **P1** | **把现成公开配对全量拉下来做冷启动** | WebCode2M 3.17M + WebSight v0.1/v0.2 2.75M + Web2Code 0.83M ≈ **680 万** | 下载约 **1.5 TB**，1 人-周做格式归一 | 低（都是 CC-BY-4.0，但 Web2Code 卡片与正文许可自相矛盾，**建议只用它的 QA 不用它的页**） | 不用等自建管线就能先把 CPT 跑起来；UI2Code^N 就是这么混的 |
| **P1** | **用可访问性树 + 70B 文本 LLM 做反推 query** | 按 MultiUI 口径，100 万站 → **730 万**样本 | 推理成本：读可访问性树比读 HTML 省大量 token；按 1,000 万页估 **数千 GPU-日**（推断） | 低（自己生成的标注） | 这是把「图→代码」单一任务扩成「需求→代码 / 代码→描述 / 元素 QA」的唯一便宜路径 |
| **P2** | **DaTikZ + SVG-Stack 两个干净 DSL 集** | DaTikZ-v3 实测 **145,908**；SVG-Stack 实测 **2,283,875** | 渲染已在数据里（DaTikZ 自带 image+pdf）；几 GPU-日 | DaTikZ 是 `license: other` 且公开版因许可残缺；SVG-Stack 来源需逐条查 | 「代码→图」最干净的两类，可当 curriculum 的早期阶段（短、确定、可编译校验） |
| **P2** | **CAD 线：GenCAD-Code + OpenECAD + BlendNet** | 163,671 + 最多 200,000 + 12,059 ≈ **38 万** | 已有渲染图，几乎零成本 | **低**：GenCAD-Code 开源、OpenECAD 公开、BlendNet 是 Apache-2.0 | 3D 侧唯一许可干净且有现成渲染图的，拿来即用 |
| **P2** | **复现 CAD-Recode 的合成算法**（不是用它的数据） | 可自产 **100 万+**，上限由算力定 | 1 人-周实现 + PythonOCC 校验；CPU 成本低 | **零**（自己生成，算法是论文公开的） | CAD-Recode 实测：同样 160k，合成完胜真实（CD 3.7 倍）；160k → 1M 仍在涨。数据本身是 NC，**算法不是** |
| **P3** | **GLSL：用 The Stack permissive 的 16.7 万文件自渲** | 167,701 个文件（0.40 GB）× 多帧 | 单卡 **979 fps @ 384×384**，渲百万帧是小时级 | **低**：The Stack v1 是 permissive-only；**不要碰 Shadertoy 的 2 万个（CC BY-NC-SA 3.0）** | 绕开 ShaderToy 许可的正路。shaders21k 证明程序数在 21K 处仍未饱和，16.7 万个文件是 8 倍上量空间 |
| **P3** | **three.js / WebGL：自己从头建**（公开数据为零） | GitHub `topic:threejs` 24,356 仓库 + `webgl` 15,107（见 `02_task_sources.md`）→ 保留率按 shaders21k 的 40% 或 Objaverse 的 15% 估，**几万到十几万** | 高：需要无头 WebGL（swiftshader）、确定性时钟、多视角 —— 这套 harness 我们已有（见 `06_harness.md`） | 中：按仓库许可过滤 | **最大的未开垦区**：HF 上 0 个代码→渲染图配对集，GitHub 上 5 万个相关仓库没人做过。我们有 harness 优势 |
| **P4** | OpenSCAD | the-stack 有 36.47 MB parquet；公开配对集全在万条以下（最大 26,480 条）且多数无许可声明 | 渲染便宜（OpenSCAD CLI） | 中：唯一公开集是 CC-BY-NC-SA | 量太小，且 OpenSCAD 不在 StarCoder 的 86 种语言里，基座先验弱 |
| **不做** | **直接用 Objaverse 系当 code→render 正样本** | — | — | — | 索引的 12 种扩展名无一是代码，gobjaverse 的 `.blend` 渲染成功数是 **0**。只能当目标图 / 视觉先验 / 评测素材 |
| **不做** | **Infinigen 直接当配对数据** | — | **一对 1080p 立体图 3.5 小时 wall time** | 低（BSD-3） | 代码是人写的固定 4 万行，变化全在随机参数里，直接当 code→render 会严重同质化。它的价值在当「目标场景生成器」 |
| **不做** | Stack Exchange / StackOverflow 的 dump | — | — | **高** | 2024-07 起下载协议要求「不用于训练 LLM」，与 CC BY-SA 的争议未决。只当问题线索源，答案自己重生成 |

### 6.2 配比建议（供 CPT 阶段参考）

以 UI2Code^N 的 2,000 万 vision-code 样本为锚，按本文证据给一个初值：

| 类别 | 占比 | 依据 |
|---|---|---|
| 自爬真实页面「截图 → 可渲染 HTML」 | 35% | 结构靠真实（WebCode2M TreeBLEU 0.35 vs WebSight 0.06） |
| 同一渲染派生的 **bbox ↔ DOM 片段 grounding** | 25% | S4：定位类 +25.3；UI2Code^N 的 REG 范式；增量成本近零 |
| 公开合成集（WebSight + Web2Code） | 15% | 补配色与整体版式（WebSight color 0.99）；**不能更多，分布太窄** |
| 干净 DSL（TikZ / SVG / CAD / GLSL） | 10% | 短、可编译校验，适合做 curriculum 早期 |
| 反推 query（页面 → 自然语言需求） | 5% | 让模型学 text→code 方向 |
| 通用 VL（caption / VQA / OCR / 视频） | 10% | UI2Code^N 明确说要混，否则通用能力退化 |
| **外加纯语言-代码** | 1B+ token | UI2Code^N 原文 |

**量级**：按 GLM-5 的口径，中训练约占基座的 5%；视觉侧 Kimi-VL 的 cooldown 是 13.6%、MiMo-VL Stage 4 是 22.9%。如果基座是 1T token 级，**视觉代码中训练给 50B ~ 150B token 是合理区间**（推断）。

### 6.3 五条必守的工程纪律

1. **长度/结构闸必须在渲染闸之前**。渲染占整条流水线 80% 时间（WebCode2M），先渲再筛是把钱烧在会被扔掉的页上
2. **资源必须本地缓存**（CSS / JS / 字体 / 图片）。否则① 渲不出原貌（UI2Code^N 不用 CC 的原因）② 反复打原站 ③ **数据会腐烂**（WebSight v0.2 一律用 `source.unsplash.com` 取图，该域名 2026-10-15 实测 503，192 万条已无法原样重渲）
3. **不可见元素必须用点击校验剪枝**，不能只看 CSS visibility。S4 的做法：点 bbox 中心，返回元素不是其后代就剪掉；再剔溢出祖先 bbox 的文字；丢掉所有 iframe
4. **阈值一律在自己的第一个 chunk 上校准**，不要抄数。WebCode2M 的 NSFW=0.04 是在第一个 chunk 上扫出来的（0.02 误杀 57.5%，0.05 toxic 升到 0.27%）；DataComp 的去重阈值精确到 0.604169
5. **训练/评测切分按注册域名 + family_id 分组**，不能按样本随机切。WebUI 按域名 70/10/20；同站多 viewport 渲染会造成跨 split 泄漏

---

## 7. 未能核实 / 局限

### 7.1 文献空白（确认过是「没人做」，不是「漏查」）

| # | 空白 | 为什么重要 |
|---|---|---|
| 1 | **「加 UI grounding 预训练 → image-to-code 指标提升 X」的消融，一篇都没有** | §4 的全部正向证据都在推理期或反方向。UI2Code^N 用了 `L_dom` 但没剥离 |
| 2 | **「WebSight / WebCode2M 训练集与 Design2Code 测试集的视觉重叠率」没人测过** | 两边都源自 Common Crawl / C4，污染通道天然存在。用 DataComp 的阈值（0.604169）扫一遍 484 条即可补上 |
| 3 | **LLM 合成 UI / 网页的多样性没有任何量化基线**（pHash 近重复率、CLIP 特征方差、unique-tag 覆盖） | 要做多样性闸就得自己建量表。WebSight v0.1 vs v0.2 的多样性对比在论文与 HF 卡片里都没有 |
| 4 | **three.js / WebGL 的「代码 → 渲染图」配对集：零** | HF 上 three.js 相关数据集 8 个（实测），全是指令-代码；GitHub 上 2.4 万个 threejs 仓库没人做过 |
| 5 | **shader 代码的程序化合成（类比 CAD-Recode）：零** | CAD 侧已证明合成 > 真实挖（CD 3.7 倍），shader 侧没人试 |
| 6 | **从 GitHub 大规模挖 bpy 脚本批量渲染：零公开工作** | BlenderLLM 走 GPT-4o 合成而非挖掘，这本身是信号 |

### 7.2 数字拿不到的（只在图片里或未公开）

- **GLM-4.1V §6.3 的跨域矩阵**：Figure 6 是 PNG，正文与 HTML 均无数值。§4.5 的那张矩阵表由读图得到，**精度只到小数一位，不要当精确值引用**
- 逐点 scaling 数值只在图片里：**UGround Figure 5、SeeClick Figure 6、UIPro Figure 6、OS-Atlas Figure 3/4/5**
- **DeTikZify 正文的 sketch 消融表**：arXiv HTML 三版 LaTeXML 转换都在结果章节截断，要读 PDF
- **UI2Code^N 的 token 数**：只给了 batch 1,536，seq 长度未给，无法反推 CPT 的 token 量
- **WebSight v0.2 的过滤前候选量与保留率**：论文只说「丢掉文本不足、内容泛化、图片与主题不符的页面后最终 200 万」
- **BigDocs Screenshot2HTML 各步剩余量**：只给终值 11,000
- **StarVector 的 SVG-Stack 各步丢弃比例**：论文只说三重去重 + 去白图，没给任何一步前后条数
- **OmniSVG 的 MMSVG-2M / Icon / Character**：datasets-server 返回 401（gated 或不存在）
- **Vipitis/Shadertoys 与 Shadertoys-fine 原始大集已下架**（API 与 raw README 均 401），导致 Shadertoy 各许可标签占比无法统计
- **Objaverse 1.0 内部 CC 子许可占比**（CC0 / CC-BY / CC-BY-NC 各多少）
- **Thingiverse 上 .scad 文件总数**（API 需 key，站内无公开统计）
- **the-stack-dedup 的 glsl / openscad 确切行数**（数据集 gated，只拿到 parquet 字节数）
- **WebUI 的唯一站点数**（只给 400,000 页面数）；**WebUI HF 版因脏词过滤少了多少**（README 只说「fewer」）
- **UI-TARS 自采 grounding 规模**（论文打星号不披露）；**GUI-Owl 规模未披露**
- **WebCode2M 的 WebCoder-1.3B 是否真把 layout bbox 当训练目标**

### 7.3 必须标注的引用陷阱

| 陷阱 | 说明 |
|---|---|
| **UI2Code^N 的阶段消融在 arXiv v1 中不存在** | v1 只有 Table 1–4。Base 9.0 → CPT 53.3 → SFT 79.3 → RL 88.6 在**当前版本的 §4.5 / Table 6**。按 v1 引用会查无此表 |
| **「Vision2UI 的 63,515 → 7,391」这组数字查不到** | v1（Vision2UI，2024-04）与 v2（WebCode2M，2025-02）全文均无。疑为记忆误植，**不要引用** |
| **Design2Code / WebCode2M 的「真实 vs 合成」结论方向相反** | 根因是「有没有清洗」（§3.4），引用任一方时必须带上另一方 |
| **LayoutCoder 的 Snap2Code(Seen) BLEU 26.07** | 同分布过拟合量级，不是通用结论 |
| **GUIMid 的反证下游是 GUI agent，不是写代码** | 它证明「screenshot2code 数据对 GUI agent 没用」，不直接等于「对写代码没用」 |
| **Web2Code 许可自相矛盾** | HF 卡片写 MIT，论文正文写 CC BY 4.0 且仅研究用。建议只用它的 QA 部分 |
| **本文 §5.4 的法律内容均非法律意见** | 判例状态截至 2026-10-15，商用前需法务确认 |

### 7.4 本文的方法局限

- HF 行数是 datasets-server 的 `/size` 接口实测（2026-10-15），与论文声称值不一致时两个都列了，但**没有逐行下载核验**
- WebSight v0.2 的 `source.unsplash.com` 逐行命中率没统计出来（HF `/filter` 接口索引加载超时 3 次），只能靠「论文生成 prompt 强制用该域名」+ 域名探活 503 两条间接证据
- §5.5 的「13 道闸预期剔除比例」里标「推断」的几项没有任何直接出处，是按同类工作反推的，**必须在自己第一个 chunk 上重测**
- 本文**没有做任何自己的训练实验**，所有收益数字都是转引

