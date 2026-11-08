# AI 3D 资产生成：创业公司与市场格局（国内 + 国外，截至 2026-10-13）

> 口径说明：ARR / 用户数几乎全是公司自报、经媒体转载，未经审计。每条都标了日期。
> 本轮约 18 次搜索/抓取；"Demo URL" 一栏是产品主页，本轮未逐个抓取验证。

## Q1 国外玩家：产品、技术路线、融资、收入、客户

### Takeaway
- 国外头部只剩一家独立的规模玩家：**Meshy**（华人创始团队，ARR > $1 亿，2026-09）。
- 其余要么被收购（**CSM → Google DeepMind**，2026-01），要么转向（**Luma** 转做视频 / 多模态，估值 $40 亿），要么停在小额种子轮（Kaedim、Sloyd、Backflip）。
- 大厂（Microsoft TRELLIS、Roblox Cube、Tencent Hunyuan3D）的开源模型把"基础图生 3D"这一层的价格压平了。

### Cited Findings

#### Meshy（美国注册，创始人胡渊鸣 / Ethan Hu，MIT PhD）
- **ARR 时间线**
  - 2025-11/12：约 $15M — [arr.club](https://www.arr.club/meshyai/meshyai-scales-from-1m-to-40m-arr-in-one-year)
  - 2026-03（GDC）：$30M，用户 > 1000 万 — [36Kr EU](https://eu.36kr.com/en/p/3783556211825920)
  - 2026-04：> $40M — [36Kr EU](https://eu.36kr.com/en/p/3783556211825920)
  - 2026-09-30：**> $100M**，两年内从 $1M 涨约 100 倍；自称"第一家 ARR 过 $1 亿的 AI 3D 公司" — [Dealroom](https://dealroom.co/news/158079-meshy-hits-100m-arr-first-ai-3d-firm-to-reach-milestone/)
- **规模**：注册用户 > 1500 万；3000+ 公司和学校生成了 1 亿+ 模型；客户覆盖全球市值前十公司中的 5 家、财富 500 强中的 200 家（2026-09） — [Dealroom](https://dealroom.co/news/158079-meshy-hits-100m-arr-first-ai-3d-firm-to-reach-milestone/)
- **a16z 榜单**：a16z 第 7 版 Top 100 消费级 AI 应用首次按收入排 Top 50（数据来自 YipitData 的美国消费者刷卡数据），Meshy 排 **#31**，是榜单上唯一一家 AI 3D 公司（2026-10） — [量子位](https://qbitai.com/2026/10/501791.html)
- **融资**：2026-07 完成近 **$4 亿 B 轮**，投后估值 **$15 亿**（中文稿写"超 100 亿元"）；IDG、经纬中国（Matrix China）、Monolith 领投 — [Dealroom](https://dealroom.co/news/158079-meshy-hits-100m-arr-first-ai-3d-firm-to-reach-milestone/)；[PingWest](https://www.pingwest.com/w/318094)
  - 有冲突：Dealroom 另一处数据写估值 $9.706 亿 — [Dealroom](https://dealroom.co/news/158079-meshy-hits-100m-arr-first-ai-3d-firm-to-reach-milestone/)
- **技术与产品**
  - 自研多模态 3D 基础模型 — [量子位](https://qbitai.com/2026/10/501791.html)
  - Meshy 7.1 把几何生成提到 "Ultra 4K"，并开源了一套图生 3D 对齐评测
  - 手机 App（基于 Meshy 7）带可打印性检查、AR 预览，可导出 STL/GLB/OBJ — [Dealroom](https://dealroom.co/news/158079-meshy-hits-100m-arr-first-ai-3d-firm-to-reach-milestone/)
- **场景**：游戏工作室、影视团队、教育，以及**家庭 3D 打印爱好者** — [Dealroom](https://dealroom.co/news/158079-meshy-hits-100m-arr-first-ai-3d-firm-to-reach-milestone/)
- **定价**
  - 四档：Free $0（100 credits/月，产出按 CC BY 4.0 授权）/ Pro $20/月（1000 credits）/ Studio $60/月 / Enterprise 定制
  - 单次生成 20 credits；Remesh 和 Rigging 0 credits；AI 贴图 10 credits — [Meshy docs](https://docs.meshy.ai/en/webapp/pricing)；[meshy.ai/pricing](https://meshy.ai/pricing)
- **Demo**：https://www.meshy.ai

#### Luma AI（Genie）
- Genie 于 2024-01 作为 "research preview" 的 3D 基础模型发布，10 秒内出模型；同期 a16z 领投 $43M B 轮 — [TechCrunch](https://techcrunch.com/2024/01/09/luma-raises-43m-to-build-ai-that-crafts-3d-models)
- 2025-11-19：沙特 HUMAIN 领投 $9 亿 C 轮，估值 **$40 亿**；媒体把 Luma 定位成"AI 视频创业公司"，主打产品是 Dream Machine — [Bloomberg Gov](https://news.bgov.com/artificial-intelligence/saudis-humain-backs-ai-video-startup-luma-at-4-billion-value)
- 没找到官方说 Genie 已停止的消息；只有一个二手聚合页提到 Luma 从 3D 转向 — 见 Gaps

#### CSM（Common Sense Machines，产品 "Cube"，与 Roblox Cube 不是一回事）
- 2026-01-24 被 Alphabet 收购，约 12 名员工并入 Google DeepMind；交易条款未披露
- 此前融资约 $10M（含 a16z），上一轮估值 $15M
- 产品能从草图 / 图片 / 文本生成带贴图、可进游戏引擎的网格 — [The Decoder](https://the-decoder.com/google-deepmind-goes-on-acquisition-spree-with-three-ai-deals-in-one-week/)；[Gunderson Dettmer](https://www.gunder.com/en/news-insights/client-news/gunderson-dettmer-represents-common-sense-machines-in-acquisition-by-google)；[Ben's Bites](https://news.bensbites.com/posts/56170-google-acquires-common-sense-machines-whose-ai-models-create-3d-assets-from-2d-images-and-was-last-valued-at-15m-after-raising-10m-from-a16z-and-others)

#### Kaedim（伦敦，2D 图转 3D）
- 2024-03 完成 $15M A 轮，累计 $16.01M；投资方含 a16z、Pioneer Fund — [CB Insights](https://www.cbinsights.com/company/kaedim/financials)；[VCBacked](https://www.vcbacked.co/company/kaedim)
- 没找到 2025–2026 的新融资

#### Sloyd（奥斯陆，参数化 / 程序化 + AI 路线）
- €3M 种子轮，投资方含 Autodesk、Antler、a16z GAMES SPEEDRUN — [bebeez](https://bebeez.eu/2024/06/07/norwegian-startup-secures-e3-million-to-transform-3d-creation-with-ai-driven-innovation/)
  - 日期有冲突：2024-06 还是 2025-08 — [Techleap](https://finder.techleap.nl/news/feed/sloyd-secures-3m-seed-funding)
- 注册用户 25 万+ — [Techleap](https://finder.techleap.nl/news/feed/sloyd-secures-3m-seed-funding)
- 订阅制，Plus 版 $15/月起 — [Sloyd blog](https://www.sloyd.ai/blog/ai-3d-model-generator-rankings)

#### Backflip（Markforged 创始人 Greg Mark 创立，专攻 3D 打印）
- 2024-12-19 走出隐身，完成 $30M A 轮（NEA、a16z 联合领投）
- 产品：文本 / 照片 → **可 3D 打印**的设计
- 公司自称训练效率高 60 倍、推理快 10 倍、空间分辨率高 100 倍 — [TechCrunch](https://techcrunch.com/2024/12/19/backed-by-a16z-and-nea-backflip-raises-30m-series-a-to-turn-text-into-ai-generated-designs/)；[3D Printing Industry](https://3dprintingindustry.com/news/markforged-founders-launch-new-ai-3d-model-generator-backflip-with-30m-funding-led-by-nea-and-a16z-235400/)

#### Masterpiece X
- 2025-12 发布 WorldEngen："面向 3D 生产工作流的 AI copilot"，能读懂工程文件、调度模型、接入 DCC 软件 → 从"生成器"转向"流程 agent" — [AWN](https://www.awn.com/print/news/masterpiece-x-launches-worldengen-ai-copilot)

#### 开源大厂模型
- **Roblox Cube 3D**：2025-03 开源，文本生成网格，同时开放 Mesh Generation API beta；Roblox 说 Cube 会成为它后续 AI 工具的底座 — [Maginative](https://www.maginative.com/article/roblox-open-sources-cube-3d-its-ai-model-for-generating-3d-objects/)
- **Microsoft TRELLIS / TRELLIS.2**（结构化 latent，原生 3D）
  - TRELLIS.2：约 10.5k stars（2026-08-09） — [Star History](https://www.star-history.com/microsoft/trellis.2/)
  - TRELLIS.2 在 2026-08-01 冲到 GitHub Trending #5 — [Trendshift](https://trendshift.io/repositories/16488)
  - 初代 TRELLIS：约 12.2k stars（2026-04） — [Star History](https://star-history.com/microsoft/trellis)

### Inferences
- 头部的"规模化"是在付费意愿高的长尾个人和专业用户上做出来的
  - Meshy 能进 a16z 消费刷卡榜，说明收入大头是**个人信用卡订阅**，不是大企业合同
- 纯模型、没有分发的西方小公司正在被收购或被边缘化
  - CSM 只拿到约 $15M 估值就被收；Luma 放下 3D 转去做视频

### Gaps
- Luma Genie 现在还在不在：没有官方来源
- 本轮没覆盖到：3DFY.ai、Alpha3D、Spline AI、Krea 3D、NVIDIA（Edify 3D / LGM）、Adobe（Substance 3D / Firefly 3D）、Stability SF3D / SPAR3D 的最新状态和融资
- 没查到 Kaedim / Sloyd 的收入数据

## Q2 国内玩家：VAST/Tripo、影眸 Rodin、腾讯混元 3D、字节 Seed3D、光影焕像、数美万物等

### Takeaway
- 2026 年是国内 AI 3D 的"融资年"
  - **VAST（Tripo）**：半年约 50 亿元，B 轮约 $4.46 亿
  - **影眸（Rodin）**：ARR 数千万美元，约 80% 收入来自海外
  - **数美万物（Hi3D）**：累计近 $5000 万
- 大厂（腾讯、字节）用**开源 + 云 API** 卡生态位。腾讯通过拓竹（Bambu Lab）旗下的 MakerWorld 直接打进了 3D 打印人群

### Cited Findings

#### VAST / Tripo（北京，2022-11 成立，CEO 宋亚宸，首席科学家曹炎培）
- **2026 融资**
  - 03-05：A 轮 $5000 万，阿里、恒旭领投
  - 06：A+ / A++ 约 $2 亿；彭博称估值 ≥ $10 亿
  - 07-02：A3 轮超 10 亿元，吉利、4399、巨人等参投
  - 09-01：B / B+ 合计约 30 亿元（约 $4.46 亿）
- **口径冲突**
  - 半年累计：一处说约 50 亿元，正文又说成立以来近 60 亿元
  - B 轮领投方：36Kr 写经纬创投，Investgame 写 Matrix China（两者是同一家机构的中英文名）
  - 来源：[36Kr](https://eu.36kr.com/zh/p/3964719241305607)；[DealStreetAsia](https://www.dealstreetasia.com/stories/tripo-ai-series-b-rounds-493956)；[Investgame](https://investgame.net/news/matrix-partners-china-has-led-a-446m-series-b-and-b-into-vast-maker-of-tripo-ai-in-its-fourth-round-of-2026/)
- **产业投资方**：完美世界、三七互娱、蓝色光标、中科创达等 — [36Kr](https://eu.36kr.com/zh/p/3964719241305607)
- **技术**
  - Tripo P2.0（2026-09-01）自称"行业首个原生四边面拓扑的 3D 原生基座模型"，面数可控
  - 内置 agent 负责规划、写代码和调试，可做部件命名和部件级动画
  - 此前版本：H3.1、P1.0 — [36Kr](https://eu.36kr.com/zh/p/3964719241305607)
- **收入 / 用户（口径冲突大）**
  - ARR > $1200 万、已盈利 — [ARInsider 2025-09](https://arinsider.co/2025/09/22/can-tripos-gen-ai-step-change-unlock-3d-tiktok/)
  - 创作者 650 万+、模型 1 亿+ — [ARInsider](https://arinsider.co/2025/09/22/can-tripos-gen-ai-step-change-unlock-3d-tiktok/)
  - Latka 估算 2025 年收入仅 $1.5M（第三方估算，可信度低） — [Latka](https://getlatka.com/companies/tripo3d.ai)
- **场景**：游戏、动画、广告、**3D 打印**、工业设计；支持导出 STL — [CB Insights](https://www.cbinsights.com/company/tripo-ai)
- **排名**：Top 3D AI 社区竞技场里 Tripo v3.1 以 ELO 1042 排第 1，$0.30/次（2026-08-03 快照）
  - 注意：这个来源是竞品 Sloyd 的博客 — [Sloyd blog](https://www.sloyd.ai/blog/ai-3d-model-generator-rankings)
- **Demo**：https://www.tripo3d.ai

#### 影眸科技 Deemos（Hyper3D Rodin，上海，2020 成立，CEO 吴迪，团队约 60 人）
- **技术路线**
  - 2023 年选了**原生 3D**，没走"2D 升 3D"
  - 2024 年发布 CLAY 框架（SIGGRAPH 最佳论文提名）
  - 2025 年末发布 Gen-2.5，自称"千万面级"
  - 2026-01-28 发布 Gen-2 Edit，把生成和编辑合在一起
  - 2026 年 CES 上，黄仁勋 keynote 演示的 3D 资产生成用的是 Rodin
  - 来源：[界面](https://m.jiemian.com/article/14631332.html)
- **融资**
  - 2025 年两轮：一轮字节、美团龙珠领投；另一轮 2025-08 蓝驰领投数千万美元
  - 2026-06-23：数亿元，凯辉、上海国投先导领投 — [第一财经](https://www.yicai.com/news/103242038.html)；[界面](https://m.jiemian.com/article/14631332.html)
- **收入**
  - 上线 45 天 ARR 达 $100 万 — [3Printr](https://www.3printr.com/hyper3d-chinese-ai-3d-model-platform-secures-millions-in-series-a-round-funding-3276516/)
  - 现在 ARR "数千万美元"
  - Gen-2.5 首月订阅用户与 ARR 环比增长 > 400%
  - C 端用户占比 60% — [界面](https://m.jiemian.com/article/14631332.html)
  - 约 80% 收入来自海外 — [搜狐](https://m.sohu.com/a/1040643865_114986/)
- **客户**
  - 头部游戏工作室几乎都买了账号，部分做了私有化部署
  - 用法：生成三视图、发外包前先出白盒
  - 公开提到的客户：字节、Unity、Figma、Canva — [界面](https://m.jiemian.com/article/14631332.html)；[搜狐](https://m.sohu.com/a/1040643865_114986/)
- **Demo**：https://hyper3d.ai

#### 腾讯混元 3D（Hunyuan3D）
- **开源**
  - 2.x 系列开权重（2.0 / 2.1 / 2.5 / Turbo / mini / 多视图）
  - 主仓库约 13.6k stars（2026-04） — [ToolWorthy](https://www.toolworthy.ai/en/tool/tencent-hunyuan3d)
  - 3.x（v3.1 Pro / Rapid）只走 API — [CostGoat](https://costgoat.com/pricing/hunyuan-3d)
- **商业化**
  - 2025-04 上线腾讯云 API
  - 2025-11 全球发布前，国内已有 150+ 家企业接入
  - 2025-07 接入拓竹 MakerWorld，预计月调用 10 万+（这是预期，不是实际统计）
  - 2026-03 与 3D AI Studio 合作 — [腾讯云 x 3D AI Studio PR](https://tools.prnewswire.com/en-us/live/20823/release/20260319EN13277)；[cinevva](https://app.cinevva.com/zh-CN/news/2025-11-26-tencent-hunyuan-3d-engine)
- **价格**：fal.ai 上 v3 图生 3D $0.375/次、v3.1 Rapid $0.225/次（2026-08） — [CostGoat](https://costgoat.com/pricing/hunyuan-3d)
- **Demo**：https://3d.hunyuan.tencent.com

#### 字节 Seed3D
- 1.0（2025-10）：单图 → 仿真级 3D，带几何 + PBR 材质 — [PingWest](https://www.pingwest.com/w/308485)
- 2.0（2026-04-23）
  - 架构：粗到精的两阶段 DiT
  - 新能力：部件分割与补全、铰接资产、场景组合
  - API 已上火山引擎
  - 自评：60 名 3D 打分员盲评偏好率 > 69% — [DoNews](https://www.donews.com/news/detail/1/6525541.html)
- 定位偏**世界模拟器 / 具身仿真**的资产来源 — [PingWest](https://www.pingwest.com/w/308485)

#### 光影焕像（港科大谭平创立）
- 2025-05 与阶跃星辰联合开源 Step1X-3D（4.8B 参数） — [量子位](https://www.qbitai.com/2025/05/283247.html)

#### 数美万物（Hi3D）
- 2026-08-20 完成 A+ 轮，半年两轮累计近 $5000 万
  - 领投：BAI、华业天成
  - 跟投：红杉中国、IDG 等
- Hi3D V3.0 自称"首个商用级 2048³ 体素分辨率模型"
- 计划做"一键定制到家"（生成 → 实物交付） — [CSDN](https://www.csdn.net/article/2026-08-22/163958116)

#### 其他
- Hitem3D v2.0、Triverse 3.0、N4D-2.5 都进了 Top 3D AI 竞技场前 5 — [Sloyd blog](https://www.sloyd.ai/blog/ai-3d-model-generator-rankings)
- 元象 XVERSE：没找到 3D 生成模型开源的证据，公开开源的主要是 LLM 和多模态模型 — [阿里云开发者社区](https://developer.aliyun.com/article/1500374)

### Inferences
- 国内 3D 公司收入大多靠**出海订阅**：影眸约 80% 海外，Meshy 本身就是"华人团队 + 海外收入"
- 游戏公司做产业投资（4399、巨人、三七、完美世界）说明游戏是**战略合作**场景，但从收入结构看，C 端订阅占大头（影眸 C 端 60%）

### Gaps
- Tripo 2026 年的 ARR / 用户数没有可靠的最新披露
- 混元 3D 2026 年的调用量 / 收入没有官方数据
- 阿里有没有自有的 3D 生成产品：没找到；阿里只以投资方身份出现在 VAST A 轮
- 生数在 3D 上的进展：本轮没查

## Q3 谁在付钱：定价、B2B vs prosumer、3D 打印

### Takeaway
- 已被证实付费的是 **prosumer 订阅**，最明确的三类人：
  - 3D 打印爱好者
  - 独立 / 小团队游戏开发者
  - 设计师
- B2B 收入主要来自游戏工作室买账号 / 私有化部署，以及大平台的 API 集成（Canva、Figma、Unity、MakerWorld）
- 单次生成价格已压到 **$0.2–0.8**

### Cited Findings
- **个人订阅**
  - Meshy 收入能被美国**消费者刷卡数据**排进 Top 50 消费 AI 应用 → 个人订阅是主力 — [量子位](https://qbitai.com/2026/10/501791.html)
  - 影眸 C 端用户占比 60% — [界面](https://m.jiemian.com/article/14631332.html)
- **3D 打印**
  - Meshy App 内置可打印性检查和 STL 导出，"家庭 3D 打印爱好者"被列为核心用户 — [Dealroom](https://dealroom.co/news/158079-meshy-hits-100m-arr-first-ai-3d-firm-to-reach-milestone/)
  - Backflip 整个公司押在 3D 打印上，拿了 $30M — [TechCrunch](https://techcrunch.com/2024/12/19/backed-by-a16z-and-nea-backflip-raises-30m-series-a-to-turn-text-into-ai-generated-designs/)
  - 混元接入拓竹 MakerWorld — [cinevva](https://app.cinevva.com/zh-CN/news/2025-11-26-tencent-hunyuan-3d-engine)
  - 数美万物在做"生成 → 实物交付" — [CSDN](https://www.csdn.net/article/2026-08-22/163958116)
- **游戏 B2B**：头部工作室买账号 / 私有化，用来出三视图和外包白盒 — [界面](https://m.jiemian.com/article/14631332.html)
- **价格带**
  - Meshy Pro $20/月 — [Meshy docs](https://docs.meshy.ai/en/webapp/pricing)
  - Sloyd $15/月起
  - 单次生成：Tripo $0.30、Rodin $0.29、Meshy 6 $0.40、Hitem3D $0.73 — [Sloyd blog](https://www.sloyd.ai/blog/ai-3d-model-generator-rankings)
  - 混元 fal.ai $0.225–0.375 — [CostGoat](https://costgoat.com/pricing/hunyuan-3d)
- **具身 / 仿真**：新出现的需求方向（Seed3D 定位、影眸提到合作机会），但还没有收入数据 — [PingWest](https://www.pingwest.com/w/308485)；[界面](https://m.jiemian.com/article/14631332.html)

### Inferences
- 3D 打印是天然适合 AI 3D 的场景：只要封闭、可打印，**不需要拓扑 / UV / 绑骨**，正好绕开了 AI 网格最弱的地方。这很可能是 prosumer 收入高的原因（推断，没有直接的收入拆分数据）
- 电商 / AR、影视：没找到能证明大规模付费的数据

### Gaps
- 没有任何公司公开按场景拆收入（3D 打印 vs 游戏 vs 其他）

## Q4 商业化卡点：拓扑 / UV / 绑骨，谁在解决

### Takeaway
- AI 网格的主要问题
  - 三角面密而乱，UV 没优化，贴图不符合 PBR 规范
  - 结果是绑骨和变形会出问题
  - 所以 AI 出的模型在生产里往往只是"参考雕塑"
- 解法分两类
  - 生成侧直接出四边面（Tripo P2.0）、把 remesh + rig 免费打包（Meshy）
  - 独立后处理工具（Anything World 绑骨、Scenario / Nilo 自动重拓扑）

### Cited Findings
- **问题本身**
  - AI 网格常见问题：拓扑和 UV 乱、有自交面和内部几何、UV 没做 texel density 优化、贴图不是 PBR — [Nilo](https://nilo.io/articles/ai-generated-assets-for-games)
  - 密集不规则三角面会让自动绑骨崩溃 — [Neural4D blog](https://blog.neural4d.com/?p=3281)
  - 拓扑决定动画变形质量 — [Autodesk](https://www.autodesk.com/solutions/retopology)
- **生成侧解法**
  - Tripo P2.0 原生四边面、面数可控 — [36Kr](https://eu.36kr.com/zh/p/3964719241305607)
  - Meshy 的 Remesh 和 Rigging 0 credits — [Meshy docs](https://docs.meshy.ai/en/webapp/pricing)
  - 影眸 Gen-2 Edit 把生成和编辑打通 — [界面](https://m.jiemian.com/article/14631332.html)
- **后处理工具**
  - Scenario：可控面数的四边 / 三角重拓扑 — [Scenario](https://www.scenario.com/features/3d-editing)
  - Nilo：生成 → 重拓扑 → 绑骨 → LOD → 导出，浏览器里一条链 — [Nilo](https://nilo.io/articles/ai-generated-assets-for-games)
  - Anything World 的 Animate Anything（2023）：自动绑骨 + 动画，支持非人形
    - 限制：没有控制曲线、没有面部 blendshape、超过 2 万顶点会被减面 — [CG Channel](https://www.cgchannel.com/2023/10/animate-anything-uses-ai-to-rig-your-3d-characters)
- **人工兜底**：Fiverr 上大量"给 AI 模型做重拓扑"的接单 — [Fiverr](https://fiverr.com/lukakukhiani343/retopologize-and-optimize-your-ai-generated-3d-model)

### Inferences
- 竞争焦点正从"生成好不好看"转到"能不能直接进管线"：四边面、绑骨、部件、编辑
  - Tripo P2.0、Seed3D 2.0（部件 / 铰接）、Masterpiece X 的流程 agent 都指向这里

### Gaps
- Mixamo 后继者的情况本轮没查（例如 Adobe Mixamo 现状、AccuRIG、Tripo / Meshy 绑骨质量评测）
- 没有独立第三方的"进管线可用率"数据

