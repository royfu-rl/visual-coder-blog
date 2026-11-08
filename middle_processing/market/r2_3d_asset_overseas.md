# 海外 AI 3D 资产生成市场：深挖版（R2，截至 2026-10-13）

> **和第一轮（`3d_asset_gen.md`）的关系**：不重复 R1 已有内容（Meshy ARR 时间线、CSM 收购、Luma C 轮、Kaedim A 轮、Backflip A 轮等），只补缺口、纠错、加量化。
> **口径标签**：[公司自报] / [第三方估算] / [媒体报道] / [实测]（本轮亲自抓取或调用 API 得到的读数）。所有日期都写明。
> **本轮调用量**：约 85 次 search/fetch/API 调用。WebSearch 在中途撞到会话共享上限（200 次），之后只能直接抓一手页面和 GitHub / HF API。所以 Reddit 实测口碑、PitchBook/Sacra 片段都没覆盖到，列在 Gaps 里。
> **原始数据快照**（HF 3D Arena 排行榜 JSON，2026-10-13 拉取）：
> - `/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/market/r2_3d_asset_overseas_arena_render_20261013.json`
> - `/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/market/r2_3d_asset_overseas_arena_topology_20261013.json`

---

## Q1 全量玩家表：路线 / 融资 / 收入 / 定价 / 客户 / Demo 实测

### Takeaway
- 海外市场分成三层，每层的格局都和 R1 的印象不同：
  1. **独立 C 端生成器**：只剩 Meshy 一家规模化。Tripo、Rodin、Hi3D 都是中国团队在海外卖。
  2. **西方创业公司**：大面积**掉队或转型**。
     - CSM 被收购，Luma 的 Genie 页面已下线，3DFY 访问不到
     - Backflip 从"文本→可打印模型"转成了 **CAD copilot**
     - Sudo AI 转做机器人
     - Kaedim 转成"平台 + 人工审核"的企业外包
     - Anything World 改名 Everything Universe
     - Masterpiece X 转做场景 copilot
  3. **大厂**：开源（TRELLIS.2、Cube、SF3D、SAM 3D）或者研究 demo（Edify 3D、LATTE3D、Bernini、Apple Matrix3D），**都没有直接卖"按模型计费"的商品**。
     - Unity 的 3D 生成是外包给 Scenario 的
     - Autodesk 把 AI 押在动画（MotionMaker）和 VFX（Flow Studio）上

### Cited Findings

#### A. 独立生成器（订阅 + API）

- **Meshy**（native 3D latent diffusion，自研 Meshy 6 / 7 / 7.1；另有 Meshy T2 低模线）
  - **R1 没有的新数据**
    - 企业页 logo 墙 [公司自报，2026-10-13 抓取]：Nexon、DNEG、Meta、Supercell、Square Enix、FunPlus、Niantic、PICO XR、Bambu Lab、Flashforge、ELEGOO、Microsoft、Google(DeepMind)、Stanford、MIT、Harvard 等；"3,000+ teams · 100M+ models generated"。注意：页面**没有明确标注这些是付费客户** — [Meshy Enterprise](https://www.meshy.ai/enterprise)
    - 企业案例 [公司自报]
      - 37 Interactive（三七互娱）：高模工作量降 30–40%，单资产周期减半
      - Jupiter：基础模型制作从 7 天降到 2 小时（-98%）
      - Thorns Tavern（桌游手办）：单模型成本降 80%，发布频率翻 4 倍
      - 来源：[Meshy Enterprise](https://www.meshy.ai/enterprise)
    - 企业版功能：SAML SSO、多 workspace、共享 credit 池、年度 PO 结算；ISO 27001:2022 / SOC 2 Type II / GDPR；数据存在 AWS US — [Meshy Enterprise（检索摘要）](https://www.meshy.ai/sv/enterprise)
    - 公开案例库共 41 个 [公司自报]
      - 绝大多数是独立开发者、学校、手办 / 打印玩家
      - 唯一的中大型游戏厂商是 37 Interactive
      - **没有一个案例明确写"已上线的商业作品"** — [casestudies.com/meshy](https://www.casestudies.com/company/meshy)
    - a16z 第 7 版 Top 100（2026-10-05）
      - 方法：首次加入 YipitData 美国刷卡面板的消费支出榜
      - a16z 原文自己声明这个榜"不应被视为公司总收入"
      - 原文链接列表按字母排序，**Meshy 排第 31 来自量子位转述**，a16z 页面的名次在图表里，本轮读不到 — [a16z](https://a16z.com/100-gen-ai-apps-7/)；[量子位](https://qbitai.com/2026/10/501791.html)
    - 2026-04-27：用户破 1000 万，ARR 同比约 14 倍 [公司自报，媒体转述] — [量子位相关阅读](https://qbitai.com/2026/10/501791.html)
    - Dealroom 写的 B 轮：近 $4 亿、估值 $15 亿；**文中没写投资方名字** — [Dealroom](https://dealroom.co/news/158079-meshy-hits-100m-arr-first-ai-3d-firm-to-reach-milestone/)
  - **定价细节**（R1 只写了 web 端）
    - API credit 表 [实测，2026-10-13，[Meshy API pricing](https://docs.meshy.ai/en/api/pricing)]

      | 功能 | 模型 / 规格 | credits |
      |---|---|---|
      | Text-to-3D Preview | meshy-7.1 / 6 | 20 |
      | Text-to-3D Preview | 6-lite / T2 | 5 |
      | Text-to-3D Refine | 2K/4K 贴图 | +10 |
      | Text-to-3D Refine | 8K 贴图 | +15 |
      | Image-to-3D | 仅网格 | 20 |
      | Image-to-3D | 带 2K/4K 贴图 | 30 |
      | Image-to-3D | 带 8K 贴图 | 35 |
      | Image-to-3D | Ultra 几何（7.1） | +5 |
      | Retexture | — | 10 / 15 |
      | Remesh | — | 5 |
      | UV Unwrap | — | 5 |
      | Rigging | — | 5 |
      | Animation | 每个动作 | 3 |
      | Text-to-Motion | prime / swift | 10 / 3 |

    - Web 端：Remesh / Rigging / Animation 都是 0 credits — [Meshy webapp pricing](https://docs.meshy.ai/en/webapp/pricing)
    - Pro 版：1000 credits/月、10 个并发任务、含 API；Free 版产出按 CC BY 4.0 授权。本轮 pricing 页的价格卡没渲染出来，**$20/月沿用 R1 的读数** — [meshy.ai/pricing](https://www.meshy.ai/pricing)
    - 第三方渠道：fal.ai 上 Meshy 6 图生 3D **$0.80/次** [实测] — [fal Meshy v6](https://fal.ai/models/fal-ai/meshy/v6/image-to-3d)
  - **Demo**：https://www.meshy.ai → HTTP 200 [实测 2026-10-13]

- **Tripo（VAST，北京）**：海外收入为主，在海外竞技场上是主力玩家
  - **纠错 R1**
    - ARInsider（2025-09-22）**没有说"已盈利"**
    - 原文数据：ARR > $1200 万；300 万+ 专业用户，集中在欧美日韩；4 万+ 工作室 / 企业伙伴，点名 Tencent、NetEase、Microsoft、Sony、HTC、Stability AI；约 100 人；2023-03 以 "Vast" 名义成立 [公司自报，媒体转述] — [ARInsider](https://arinsider.co/2025/09/22/can-tripos-gen-ai-step-change-unlock-3d-tiktok/)
  - **定价**：fal.ai 上 v2.5 图生 3D [实测] — [fal Tripo v2.5](https://fal.ai/models/tripo3d/tripo/v2.5/image-to-3d)
    - 无贴图 $0.20
    - 标准贴图 $0.30
    - HD 贴图 $0.40
    - 四边面 +$0.05
    - PBR 不另收费
  - 订阅 ~$24/月（中档续费价，竞品博客口径）[第三方] — [3D AI Studio blog](https://www.3daistudio.com/blog/hitem3d-vs-meshy-vs-tripo-comparison)
  - **Demo**：https://www.tripo3d.ai → HTTP **403**（curl 和 WebFetch 都被拦，疑似反爬 / 地区限制）[实测 2026-10-13]，**未能验证**

- **Hyper3D Rodin（影眸 Deemos）**
  - 定价 [实测，[hyper3d.ai/pricing](https://hyper3d.ai/pricing)]

    | 档位 | 月付 | 年付（折月） | 约含模型 | 折合单价 |
    |---|---|---|---|---|
    | Creator | $30 | $24 | ~60 个 | ≈ $0.50/个 |
    | Business | $120 | $96 | ~416 个 | ≈ $0.29/个，含完整 API（120–240 RPM） |
    | 直购 credit | — | — | — | $1.5/credit |

  - fal.ai：$0.40/次；HighPack（4K 贴图 + 高模）是 3 倍，≈ $1.20 [实测] — [fal Rodin](https://fal.ai/models/fal-ai/hyper3d/rodin)
  - 官网 logo 墙（未标明是客户还是伙伴）：Acer、Bambu、ComfyUI、DeepMind、Fal、Meta、NVIDIA、NetEase、PICO、Replicate、Shutterstock、Supercell、Tencent 等 17 家 [公司自报]
  - 8 个 DCC 插件：Blender / Unity / Unreal / Godot / Maya / Max / C4D / Omniverse
  - "Thinking effort" 分 5 档，约 4s–80s — [hyper3d.ai](https://hyper3d.ai/)
  - **Demo**：https://hyper3d.ai → HTTP 200 [实测]

- **Hitem3D = Hi3D**（官网版权方 Oceano HK Holding Limited；**和"数美万物"的对应关系本轮没找到一手确认**）
  - 自报 [公司自报，2026-10-13]：生成模型 10M+，创作者 2M+，120+ 国家
  - 主打 3D 打印
    - 拆件打印、多色打印
    - 一键发送到 Bambu Studio / OrcaSlicer / Elegoo / Snapmaker / Creality 等切片软件
    - 代打印并邮寄到家
  - 模型：v3.0 自称 2048³、8K PBR — [hitem3d.ai](https://www.hitem3d.ai/)
  - 档位 [实测] — [hitem3d.ai/pricing](https://www.hitem3d.ai/pricing)

    | 档位 | credits | 资产数 |
    |---|---|---|
    | Pro | 1,000/月 | 100 个/月 |
    | Max | 2,400/月 | 240 个/月 |
    | Ultra | 8,000/月 | 800 个/月 |

    - 页面没渲染出价格；第三方口径 Pro $19.90/月 → **约 $0.20/资产** — [top3d.ai](https://www.top3d.ai/)
  - **Demo**：https://www.hitem3d.ai → HTTP 200 [实测]

- **Sloyd（奥斯陆，参数化模板 + AI 生成）**
  - 订阅 [实测，[sloyd.ai/pricing](https://www.sloyd.ai/pricing)]

    | 档位 | 月付 | 年付（折月） | 含 credits | 并发 |
    |---|---|---|---|---|
    | Plus | $15 | $12.50 | 50/月 | 2 |
    | Pro | $50 | $41.67 | 350/月 | 5 |

    - 图 / 文生 3D、绑骨、动画、重贴图都"**无限**"
    - credits 只用在多图、拆件（20）、image-to-scene（30）、动作生成（30）、Ultra 50 万面（5）
  - API [实测，[sloyd API pricing](https://www.sloyd.ai/api/pricing)]
    - 汇率 $1 = 75 credits，最低充值 $12 = 900 credits
    - 图生 3D 基础 10 credits，贴图 +10 → **≈ $0.27/个**
    - 文生 3D 25 credits → **≈ $0.33/个**
    - 四边面 +5，拆件 40
  - **Demo**：https://www.sloyd.ai → HTTP 200 [实测]

- **Alpha3D**
  - 官网 meta 描述："Generate, retopologise, unwrap, texture, and convert. **From €5/mo**" [实测]
  - 页面是 JS 渲染，其余内容（客户、融资）抓不到 — [alpha3d.io](https://www.alpha3d.io/)
  - top3d.ai 上的 "Alpha3D 5"：分割榜第 2（2026-10 季），总榜第 10 — [top3d.ai](https://www.top3d.ai/leaderboard)
  - **Demo**：https://www.alpha3d.io → HTTP 200 [实测]

- **Spline AI（Spline 3D 设计工具内置）**
  - AI 3D Generation V2：文 / 图 → 带 PBR（base color、metallic-roughness、normal）的 GLB
  - 一次出 4 个候选
  - 可以"选择多个 SOTA 模型对比"，但**不披露是哪些模型** — [spline.design/ai-generate](https://spline.design/ai-generate)
  - 定价 [实测] — [spline.design/pricing](https://spline.design/pricing)

    | 档位 | 价格 | AI credits |
    |---|---|---|
    | Hobby | $15/席/月 | 2,000/月 |
    | Pro | $30/席/月 | 3,000/月 |
    | Max | $70/席/月 | 10,000/月 |
    | 加购 | $5 / 1,000 credits | — |

    - 每次 3D 生成扣多少 credits：页面没写
  - **Demo**：https://spline.design/ai-generate → HTTP 200 [实测]

- **Krea 3D**
  - 聚合器，不是自研模型：页面列出 **Hunyuan3D-2.1、TRELLIS、Tripo** 可选 [实测 2026-10-13] — [krea.ai/3d](https://www.krea.ai/3d)
  - **Demo**：HTTP 200 [实测]

- **Kaedim（伦敦）**
  - **定位已变**：主页写 "The platform for high quality 3D production at scale"
    - 面向产品设计、游戏、电商三个行业
    - 卖点是"几小时交付 + 无限修改 + 审阅 / 批注 / 审批流程"
    - 官网**已不公开价格**（/pricing 返回 404）[实测]
  - 点名客户 logo [公司自报]：Amazon、DeNA、EA、CBS、Rebellion、Redly Games、Inflexion、Azra Games、Little Buffalo、Newell Brands、Myth Studio、Upland — [kaedim3d.com](https://www.kaedim3d.com/)
  - 背景：2023-09 404 Media 报道其"AI"大量靠人工建模 [媒体报道] — [404 Media](https://404media.co/kaedim-ai-startup-2d-to-3d-used-cheap-human-labor)
  - 融资：累计 $16.01M（5 轮）
    - 2024-03-11 A 轮 $15M
    - A 轮投资方：a16z、Pioneer Fund，以及天使 Tom Blomfield、Siqi Chen、Nate Mitchell 等
    - 来源：[CB Insights](https://www.cbinsights.com/company/kaedim/financials)
  - **Demo**：https://www.kaedim3d.com → HTTP 200 [实测]

- **Backflip（旧金山，Markforged 创始人）**：**已转型**
  - 现在卖的是"**AI copilot for CAD**"：生成带完整特征树的参数化模型
    - Drawing-to-CAD、3D Scan-to-CAD、Photo-to-CAD
    - 形态：Autodesk Fusion 插件 + 独立 web app [实测 2026-10-13] — [backflip.ai](https://www.backflip.ai/)
  - 定价 [实测] — [backflip.ai/pricing](https://www.backflip.ai/pricing)

    | 档位 | 价格 | credits/月 |
    |---|---|---|
    | Builder | $20/月 | 100 |
    | Pro | $50/月 | 300 |
    | Business | $380/月 | 2,500 |

    - Fast 任务 10 credits（≈ $2），Thinking 任务 50 credits（≈ $10）
  - 2026 年没有新融资，最近一轮仍是 2024-12 的 $30M A 轮 [媒体报道] — [TechCrunch](https://techcrunch.com/2024/12/19/backed-by-a16z-and-nea-backflip-raises-30m-series-a-to-turn-text-into-ai-generated-designs)

- **Nilo**（浏览器内做游戏，生成 → 减面 → 绑骨 → 动画 → 导出到 Roblox）
  - 2025-09-24 种子轮 $4M，Supercell + a16z speedrun 领投 [媒体报道] — [GamesBeat](https://gamesbeat.com/nilo-raises-4-million-for-browser-based-ai-powered-collaborative-3d-game-creation-platform/)；[Dealroom](https://app.dealroom.co/news/feed/nilo-raises-4m-for-ai-platform)
  - "+100K Creators" [公司自报]
  - 生成模型"任选各家最新模型"，即聚合路线 — [nilo.io](https://nilo.io/)
  - 定价：Starter 免费（1,500 Bits/月）；Builder $14.99、Pro $37.49（都是 5 折促销价，原价 $29.99 / $74.99）[实测] — [nilo.io/pricing](https://nilo.io/pricing)

- **Masterpiece X**
  - 主产品已换成 **WorldEngen**：Blender / Unity / UE 里的 AI 场景 copilot，7 天试用
  - 3D Web Generator 被列为"legacy"
  - 页面没有价格、客户、融资信息 [实测] — [masterpiecex.com](https://masterpiecex.com/)

- **Polycam**（摄影测量 / 高斯泼溅采集为主，AI 生成是附加功能）
  - 定价 [实测] — [poly.cam/pricing](https://poly.cam/pricing)

    | 档位 | 价格 |
    |---|---|
    | Basic | $150/年（月付 $30） |
    | Business | $400/人/年 |
    | Enterprise | $1,200/人/年，3 人起 |

  - 自称"Trusted by half of the Fortune 500"，logo 有 Zillow、Wayfair、Warner Bros Discovery、Amazon、Target、Costco、Paramount、Adobe 等 [公司自报]
  - 导航里有 "AI 3D model generator" 和 "Texture generator"，但没有说明 — [poly.cam/about](https://poly.cam/about)

- **Anything World → 已更名 Everything Universe Ltd.**
  - anything.world 301 跳转到 everythinguniver.se [实测 2026-10-13]
  - 定价 [实测] — [everythinguniver.se/pricing](https://everythinguniver.se/pricing)

    | 档位 | 价格 | 营收 / 融资门槛 | 席位 |
    |---|---|---|---|
    | Individual | 免费 | < $10 万 | — |
    | Micro | $50/月 | < $20 万 | 5 |
    | Pro | $250/月 | < $400 万 | 10 |
    | Enterprise | 定制 | — | — |

    - 各档都是"无限模型 + 无限动画"

- **Cascadeur（Nekki）**：AI 辅助动画（AutoPosing，含手指和四足），**不是**生成器
  - FAQ 的美元价：Indie $19/月（$96/年），Pro $49/月（$396/年）
  - Indie 和免费版要求年营收 < $10 万 [实测] — [cascadeur.com/plans](https://cascadeur.com/plans)

- **Sudo AI**：**已退出 3D 资产生成**
  - 官网只剩机器人产品 #sudo R1（纯仿真数据训练的抓取模型），没有 3D Studio [实测 2026-10-13] — [sudo.ai](https://www.sudo.ai/)
  - 2026-09 晚期轮约 $1.375–1.49 亿，小米参投，估值近 $20 亿
    - 联合创始人苏昊（Hao Su，PointNet 作者）
    - 叙事是"仿真优先 + 3D 生成式 AI → 机器人基础模型" [媒体报道] — [Dealroom](https://dealroom.co/news/158336-sudo-ai-raises-over-149m-late-stage-round-xiaomi-joins/)；[Pulse 2.0](https://pulse2.com/cherubic-ventures-closes-68-88-million-fund-vi-as-aum-tops-500-million-and-sudo-ai-nears-2-billion-valuation/)

#### B. 状态异常 / 下线的玩家
- **Luma Genie**
  - lumalabs.ai/genie 现在 301 到首页；首页只有 Ray3.2（视频）、Uni-1（图像）、Luma Agents，**完全没提 Genie / 3D** [实测 2026-10-13] — [lumalabs.ai](https://lumalabs.ai/genie)
  - Luma API 文档只列了视频和图像端点，没有 3D [实测] — [Luma API docs](https://docs.lumalabs.ai/docs/api)
  - 冲突：第三方目录仍挂着 "genie-3d / Limited to Pro tier"（刷新于 2026-10-08）[第三方] — [llmreference](https://www.llmreference.com/model/genie-3d/luma-api)
  - 结论：产品入口已经撤下，"API 是否还能调"没有核实
  - 历史数据
    - 2024-01 Genie 4 周内 10 万用户；研究预览期免费
    - 同期 Luma B 轮估值 $2–3 亿，训练集群约 3,000 张 A100 [媒体报道] — [TechCrunch](https://techcrunch.com/2024/01/09/luma-raises-43m-to-build-ai-that-crafts-3d-models/)
- **CSM（Common Sense Machines）**
  - csm.ai / 3d.csm.ai 从本机代理访问返回 502 [实测 2026-10-13]（可能是网络问题，**不能据此断言已下线**）
  - 收购报道没有提到 Cube 产品和客户的去向 [媒体报道] — [The Decoder](https://the-decoder.com/google-deepmind-goes-on-acquisition-spree-with-three-ai-deals-in-one-week/)
- **3DFY.ai**
  - DNS 解析到 162.255.119.24，代理 CONNECT 返回 504 [实测]
  - 这个 IP 段疑似域名停放（**推断，未核实**）
  - 本轮没找到它 2025–2026 的任何动态

#### C. 大厂 / 平台
- **Microsoft TRELLIS.2**（原生 3D 结构化 latent，O-Voxel，4B 参数）
  - H100 实测时间 [公司自报] — [GitHub](https://github.com/microsoft/TRELLIS.2)

    | 分辨率 | 总耗时 | 形状 | 材质 |
    |---|---|---|---|
    | 512³ | ~3s | 2s | 1s |
    | 1024³ | ~17s | 10s | 7s |
    | 1536³ | ~60s | 35s | 25s |

    - 输出 PBR（basecolor / roughness / metallic / opacity）GLB
    - MIT 许可，显存 ≥ 24GB
  - 热度 [实测 2026-10-13]
    - GitHub 11,924 stars（初代 TRELLIS 13,933）
    - HF `TRELLIS.2-4B` 近 30 天下载 202.8 万，累计 928.9 万
    - 初代 `TRELLIS-image-large` 累计 **4,096 万**，30 天 227.8 万
  - fal 价格：$0.25 / $0.30 / $0.35（512 / 1024 / 1536）[实测] — [fal TRELLIS.2](https://fal.ai/models/fal-ai/trellis-2)
  - **Demo**：HF Space `microsoft/TRELLIS.2` 状态 RUNNING（zero-a10g）[实测]
    - 注意：初代 `microsoft/TRELLIS` Space 是 **CONFIG_ERROR**，已坏
- **Roblox Cube**（自回归 shape token，文本 → 网格）
  - 版本时间线 [公司自报] — [GitHub Roblox/cube](https://github.com/Roblox/cube)
    - v0.1：2025-03
    - v0.5：2025-07，多训练了约 280 万合成资产，支持 bbox 条件
    - **CubePart**：2026-05，开放词表、可按部件控制，arXiv 2605.28763
    - 贴图和场景布局：仍是"计划中"
  - GitHub 1,272 stars；HF Space `Roblox/cube3d-interactive` RUNNING [实测]
  - 在 top3d.ai 分割榜上，CubePart 7 个里排第 6（2026-08）— [top3d.ai S10](https://www.top3d.ai/leaderboard/seasons/aug-26)
- **Stability AI**
  - 模型线：SF3D（0.5s，基于 TripoSR）、SPAR3D（<1s，点云 + 可编辑）、SV3D、SV4D、Stable Zero123 — [stability.ai/stable-3d](https://stability.ai/stable-3d)
  - 2025 年后没有新的 3D 模型；SF3D 仓库最后 push 是 2025-01 [实测]
  - HF 下载 [实测 2026-10-13]

    | 模型 | 30 天 | 累计 | HF Space |
    |---|---|---|---|
    | SF3D | 45,446 | 31.0 万 | RUNNING |
    | SPAR3D | 7,513 | 27.9 万 | **BUILD_ERROR** |
    | TripoSR（与 VAST 合作） | 256,720 | 210 万 | — |

  - API 的 credit 价格页面没抓到具体数字
- **NVIDIA**
  - **Edify 3D**：multiview diffusion + 多视图 ControlNet 法线 + Transformer 重建 + 4K 超分投影
    - 约 2 分钟出四边面网格 + 有序 UV + 4K PBR
    - 研究页已从 `labs/dir` 迁到 `labs/cosmos-lab`
    - 页面**没提 Shutterstock / Getty**，也没有公开 API [实测] — [NVIDIA Research](https://research.nvidia.com/labs/cosmos-lab/edify-3d/)
    - 原 `build.nvidia.com/shutterstock/edify-3d` 现在跳转到通用目录页 [实测]，NIM 托管入口疑似已撤
  - **LATTE3D**（ECCV 2024）：摊销式文生 3D，400ms；页面没说权重是否开放 — [NVIDIA Research](https://research.nvidia.com/labs/toronto-ai/LATTE3D/)
- **Adobe**
  - Project Neo 仍挂 "(Beta) from Adobe 3D & Immersive Labs" [实测 2026-10-13] — [projectneo.adobe.com](https://projectneo.adobe.com/)
  - Firefly 的 "scene to image" 用 Neo 的形体搭建做构图控制 — [Adobe](https://adobe.com/uk/products/firefly/features/scene-to-image)
  - 2026-03：Adobe × NVIDIA 宣布做基于 Omniverse 的营销用 3D 数字孪生 [公司自报] — [Adobe PR(FR)](https://news.adobe.com/fr/news/downloads/pdfs/2026/03/alerte-media-adobe-et-nvidia-annoncent-un-partenariat-strategique-pour-proposer-la-nouvelle-generation-de-modeles-firefly-et-des-workflows-creatifs-marketing-et-agentiques.pdf)
  - **没有找到 Adobe 有独立付费的 "Firefly 3D" 网格生成产品**；Substance 3D 的 helpx 页面 403，没能核实
- **Autodesk**
  - Project Bernini：2024 年研究项目，在 1000 万形状上训练，不对外 — [Develop3D](https://develop3d.com/ai/autodesk-unveils-project-bernini-for-3d-generative-ai/)
  - Wonder Studio 已更名 **Flow Studio**（wonderdynamics.com 跳转到 autodesk.com/products/flow-studio，页面 403）[实测]
    - Flow Studio 拿过 Fast Company 2025 Next Big Things
  - 2026-10-06：Maya 里的 AI 动画工具 **MotionMaker** 拿 2026 Next Big Things；没有披露价格和数据 — [Autodesk News](https://adsknews.autodesk.com/en/news/motionmaker-maya-fast-company-next-big-things-in-tech/)
  - AU 2026（2026-09-15）的 agentic AI 发布**没有提到 3D 资产生成** — [Autodesk PR](https://adsknews.autodesk.com/en/pressrelease/autodesk-advances-agentic-ai-in-its-three-industry-clouds/)
- **Unity**
  - Unity AI 测试版：Unity 6+；Personal 版试用后 $10/月，Pro / Enterprise 包含在订阅里，按 credits 计 — [unity.com/products/ai](https://unity.com/products/ai)
  - **3D 网格和贴图生成的伙伴是 Scenario, Inc.**；精灵图是 Layer AI + Scenario；动画是 **Uthana**；Assistant 用 Gemini / Claude / Kimi K3 / GLM [公司自报，2026-10-13] — [Unity Third-Party AI Terms](https://unity.com/legal/third-party-ai-terms)；[Unity AI Guiding Principles](https://unity.com/legal/unityai-guiding-principles)
- **Scenario**（Unity 的 3D 供应商）
  - 3D 编辑页面直接写着用 **Meshy Remesh / Meshy Retexture / Meshy Rigging** → 链条是 Unity → Scenario → Meshy [实测] — [Scenario 3D editing](https://www.scenario.com/features/3d-editing)
  - 定价：Starter $15/月（1,500 credits）、Pro $45、Max $75 — [Scenario pricing](https://www.scenario.com/pricing)
- **Epic / Fab / Sketchfab**
  - Sketchfab 的可售模型已迁到 Fab — [Sketchfab blog](https://sketchfab.com/blogs/community/)
  - Fab 的 AI 内容政策页 403，没核实
  - 本轮**没有找到 Epic 自己的生成式 3D 产品**
- **Apple**
  - 只有研究开源，没有商用生成器：Matrix3D（CVPR 2025 Highlight，"大型摄影测量模型"，604 stars）、Depth Pro、HUGS 等 [实测] — [GitHub apple-aiml-research/ml-matrix3d](https://github.com/apple-aiml-research/ml-matrix3d)
- **Shutterstock / TurboSquid**
  - investor 页和 shutterstock.com/generate/3d 都 403
  - **本轮无法核实**生成式 3D 产品的现状（见 Gaps）
- **Meta SAM 3D Objects**（R1 没覆盖）
  - 2025-09 开源；GitHub 7,513 stars，HF 累计 47,395 下载 [实测]

### Inferences
- **"西方创业公司被中国团队和大厂开源挤出"是结构性的**
  - 在 top3d.ai 2026-10 季榜的前 10 名里，西方背景的只有 Alpha3D 和 Meshy（总部在美国、华人团队）
  - Kaedim、CSM、Luma、Backflip、Sudo、3DFY、Masterpiece X 都离开了"通用图 / 文生 3D"赛道，转去
    - 服务（Kaedim）
    - 垂直行业（Backflip→CAD，Sudo→机器人）
    - 平台和流程（Masterpiece X、Nilo）
- **"模型商品化 → 价值往上游（分发）和下游（流程）走"**有直接证据
  - Krea、Nilo、3D AI Studio 是多模型聚合器
  - Unity 把 3D 外包给 Scenario，Scenario 再调用 Meshy 的接口
  - 生成模型本身正在变成被调度的"后端"

### Gaps
- 没有拿到 Tripo / Rodin / Hi3D 2026 年的海外 ARR 一手数据
- Polycam、Spline、Cascadeur、Masterpiece X、Alpha3D 的融资和收入：搜索额度用完，没能查
- Shutterstock 生成式 3D（Edify 驱动）是否还在卖：页面 403，没能核实
- Fab 对 AI 资产的政策：页面 403，没能核实
- Adobe 有没有 "Firefly 3D" 产品：没有一手证据
- CSM / 3DFY 是否真的下线：只有网络层面的失败，没有官方公告

---

## Q2 单位经济：GPU 成本、毛利线索、单价趋势 2022→2026

### Takeaway
- 开源 SOTA 在 H100 上**单次生成的 GPU 成本约 $0.004–0.07**（TRELLIS.2 512³–1536³）
- 市场零售单价集中在 **$0.20–0.80/个**
- 推理层面的毛利空间理论上有 80–99%，但没有任何一家公司披露真实毛利
- 单价从 2022 年 Kaedim 的约 **$7.7–10/个**（含人工）降到 2026 年的 **$0.2–0.4**，**降了约 95–98%**
- 绑骨从 2024 年约 $1.25/次降到 2026 年 $0.15 或"免费打包"

### Cited Findings
- **GPU 成本（推算基础）**
  - TRELLIS.2 H100 耗时：3s / 17s / 60s（512 / 1024 / 1536）[公司自报] — [GitHub](https://github.com/microsoft/TRELLIS.2)
  - Lambda 按需价：H100 SXM $3.99–4.29/GPU·h，H100 PCIe $3.29，A100 40GB $1.99，B200 $6.69–6.99 [实测 2026-10-13] — [Lambda pricing](https://lambda.ai/pricing)
  - Rodin 自称"思考档" ~4s 到 ~80s — [hyper3d.ai](https://hyper3d.ai/)
  - Hunyuan3D v3 在 fal 上约 1 分钟一次 — [fal Hunyuan3D v3](https://fal.ai/models/fal-ai/hunyuan3d-v3/image-to-3d)
- **2026-10 单次零售价横向对比** [实测，除注明外]

  | 产品 | 渠道 / 规格 | 单价 |
  |---|---|---|
  | TRELLIS.2 | fal | $0.25 / 0.30 / 0.35 |
  | Tripo v2.5 | fal | $0.20（白模）/ 0.30 / 0.40（HD）+ 四边面 $0.05 |
  | Hunyuan3D v3 | fal | $0.225（仅几何）/ 0.375 / 0.45（低模）+ 每项附加 $0.15 |
  | Rodin | fal | $0.40；HighPack $1.20 |
  | Rodin | Business 订阅 | ≈ $0.29 |
  | Meshy 6 | fal | $0.80 |
  | Meshy | 自家 API（30 credits） | ≈ $0.60（按 Pro $20/1000 credits = $0.02/credit **推算**） |
  | Sloyd | API | ≈ $0.27（图生 + 贴图）/ $0.33（文生） |
  | Hi3D | Pro 订阅 | ≈ $0.20（$19.90 / 100 资产，第三方价格口径） |

  - 来源：[fal TRELLIS.2](https://fal.ai/models/fal-ai/trellis-2)、[fal Tripo](https://fal.ai/models/tripo3d/tripo/v2.5/image-to-3d)、[fal Hunyuan3D v3](https://fal.ai/models/fal-ai/hunyuan3d-v3/image-to-3d)、[fal Rodin](https://fal.ai/models/fal-ai/hyper3d/rodin)、[fal Meshy](https://fal.ai/models/fal-ai/meshy/v6/image-to-3d)、[Meshy API pricing](https://docs.meshy.ai/en/api/pricing)、[Sloyd API](https://www.sloyd.ai/api/pricing)、[hitem3d pricing](https://www.hitem3d.ai/pricing)、[top3d.ai](https://www.top3d.ai/)
- **历史单价锚点**
  - 2022-08 Kaedim：$299/月含 30 个模型（≈ $10/个）；最高档 $7,700/月含 1,000 个（≈ $7.7/个）；3 天试用 $6 [媒体报道] — [CG Channel](https://www.cgchannel.com/2022/08/ai-based-web-app-kaedim-turns-2d-concepts-into-3d-assets/)
    - 注意：同期 Kaedim 被曝大量用人工建模 — [404 Media](https://404media.co/kaedim-ai-startup-2d-to-3d-used-cheap-human-labor)
  - 2024-01 Luma Genie：研究预览期免费 [媒体报道] — [TechCrunch](https://techcrunch.com/2024/01/09/luma-raises-43m-to-build-ai-that-crafts-3d-models/)
  - 2024-04 Anything World 绑骨：5 credits/个；credit 包 $25/100、$50/250、$125/750 → **约 $0.83–1.25/次** [媒体报道] — [CG Channel](https://www.cgchannel.com/2023/10/animate-anything-uses-ai-to-rig-your-3d-characters)
  - 2026 绑骨（对照上一条）
    - Uthana：$0.15/次 — [Uthana](https://uthana.com/pricing)
    - Meshy：web 端 0 credits，API 5 credits ≈ $0.10（推算）— [Meshy API pricing](https://docs.meshy.ai/en/api/pricing)
    - Anything World：$50 / $250 档"无限动画" — [everythinguniver.se/pricing](https://everythinguniver.se/pricing)
- **人工基准**：Kaedim 自己的案例写"市场平均"每个资产 32–40 小时，Kaedim 自己 4–8.7 小时（含修改）[公司自报] — [Kaedim Lowe's](https://www.kaedim3d.com/case-study/dynamic/lowes)；[Kaedim Myth Studio](https://www.kaedim3d.com/case-study/dynamic/myth-studio)
- **毛利**：本轮**没有找到**任何 3D 生成公司披露毛利率（Meshy 的 Dealroom 稿也没写）— [Dealroom](https://dealroom.co/news/158079-meshy-hits-100m-arr-first-ai-3d-firm-to-reach-milestone/)

### Inferences
- **推算 GPU 成本**（以 H100 $2–4.29/h 计，只算推理时间、假设满利用率）

  | TRELLIS.2 分辨率 | GPU 成本 | 占 fal 售价 |
  |---|---|---|
  | 512³ | ≈ $0.002–0.004 | ~1% |
  | 1024³ | ≈ $0.009–0.020 | ~3–7% |
  | 1536³ | ≈ $0.033–0.072 | ~10–20% |

  - fal 卖 TRELLIS.2 不用付模型授权费（MIT），推理毛利上限约 80–99%
  - 真实毛利还要扣掉：空闲算力、冷启动、免费用户、重试（Hi3D 每任务给 3–15 次免费重试，Rodin 有 "Free Retry V1–V4"）、存储
- **价格下限被开源锚住**
  - 闭源头部（Meshy $0.6–0.8、Rodin HighPack $1.2）的溢价，靠的是贴图分辨率 / 几何档位 / 工具链（remesh、rig）打包，不是靠基础生成
- **"降价"其实是把后处理变成免费赠品**
  - Meshy web 端 remesh / rig / animation 都是 0 credits
  - Sloyd 订阅里绑骨和动画无限
  - Anything World 动画无限
  - → 后处理层单独收费的空间正在被压缩

### Gaps
- 没有任何公司的真实单次推理成本和毛利
- 2023 年 Meshy / CSM / Tripo 的原始价格表：搜索额度用完，也没用存档服务回溯
- fal / Replicate 和模型方之间的分成比例：没有公开数据

---

## Q3 基准与排行榜（2026）

### Takeaway
- 两个主要竞技场的**结论互相矛盾**，因为参赛模型和投票人群不同：
  - **HF 3D Arena**（Hugging Face 官方、偏开源）
    - 渲染榜第 1 是 PicGen3D 1416，开源最高是 TRELLIS-3DGS 1398
    - 闭源只收了 Meshy，Tripo / Rodin 不在榜上
  - **top3d.ai**（个人运营、按月分赛季、闭源为主）
    - 2026-03 到 2026-09 **连续 7 个赛季 Tripo 夺冠**
    - TRELLIS.2 和 SAM 3D 排倒数
- 付费用户偏好研究只找到一份，而且是厂商自己发的（Meshy 6 对 Tripo 3.1，63.8%）

### Cited Findings
- **HF 3D Arena（3d-arena/3d-arena）**
  - 2026-10-13 通过 Space 内部的 `/api/leaderboard` 实测拉取，**渲染（render）榜**
  - 24 个模型，合计 113,493 票 [实测]

    | 名次 | 模型 | Elo | 票数 | 开源 |
    |---|---|---|---|---|
    | 1 | PicGen3D | 1416 | 4,372 | 闭源 |
    | 2 | TRELLIS-3DGS | 1398 | 4,834 | 开源 |
    | 3 | Meshy-6 | 1356 | 1,012 | 闭源 |
    | 4 | 404_GEN | 1335 | 1,448 | 闭源 |
    | 5 | Meshy-7 | 1307 | 197 | 闭源 |
    | 6 | TRELLIS | 1303 | 5,780 | 开源 |
    | 7 | Zaohaowu3D | 1296 | 2,985 | 闭源 |
    | 8 | Hunyuan3D-2 | 1284 | 5,245 | 开源 |
    | 9 | UniLat3D-3DGS | 1274 | 301 | 开源 |
    | 10 | Hunyuan3D-2.1 | 1273 | 2,208 | 开源 |
    | 11 | InstantMesh | 1269 | 11,612 | 开源 |
    | 12 | SAM-3D-Objects-3DGS | 1267 | 1,406 | 开源 |
    | 15 | SF3D | 1174 | 8,034 | 开源 |
    | 18 | TRELLIS.2-4B | 1126 | 1,426 | 开源 |
    | 19 | SPAR3D | 1113 | 4,928 | 开源 |
    | 20 | TripoSR | 1081 | 11,390 | 开源 |
    | 23 | Meshy-5 | 1002 | 952 | 闭源 |
    | 24 | 3DTopia-XL | 940 | 6,232 | 开源 |

  - **拓扑（topology）榜**：21 个模型，14,936 票 [实测]
    - Hunyuan3D-2 1360、TRELLIS 1328、Meshy-6 1327、Hunyuan3D-2.1 1313、Meshy-7 1271、Hi3DGen 1231、Zaohaowu3D 1230、TripoSG 1223
    - TRELLIS.2-4B 1144（第 11）
  - Space 元数据：最后更新 2026-08-03，414 likes；数据集累计 12,213 次下载 [实测]
  - 原始 JSON：`r2_3d_asset_overseas_arena_*_20261013.json`
  - **方法论**（论文 arXiv 2506.18787，2025-06）
    - 2024-06 上线；截至论文时 123,243 票、8,096 名用户、19 个模型；100 张 iso3D 输入图
    - 用户真实性 99.75%（统计反作弊）
    - **高斯泼溅比网格高 16.6 Elo，有贴图比无贴图高 144.1 Elo** → 人类投票偏向"看起来好看"，不看能不能用 — [arXiv](https://arxiv.org/abs/2506.18787)
  - 入榜要求：图片输入、mesh 或 splat 输出、全流程无人工 — [Space About 源码](https://huggingface.co/spaces/3d-arena/3d-arena)
- **top3d.ai（"Top 3D AI"，运营者 Stefan Vaskevich，个人项目）**
  - 每月一个赛季，每季从 1000 Elo 重新开始；分 6 个子榜：综合 / 贴图 / 几何 / 低模 / 分割 / Smart UV — [top3d.ai](https://www.top3d.ai/)
  - **2026-10 赛季（S12，进行中）综合榜** [实测 2026-10-13] — [top3d.ai/leaderboard](https://www.top3d.ai/leaderboard)

    | 名次 | 模型 | Elo | 胜率 | 票数 |
    |---|---|---|---|---|
    | 1 | Meshy 7 | 1095 | 64.7% | 417 |
    | 2 | Tripo v3.1 | 1091 | 69.8% | — |
    | 3 | Hi3D v3.0 | 1081 | — | — |
    | 4 | Meshy 7.1 | 1072 | — | — |
    | 5 | Lychee Gen 2 | 1064 | — | — |
    | 6 | Hunyuan 3D v3.1 | 1055 | — | — |
    | 7 | YVO3D 2.5 | 1041 | — | — |
    | 8 | Rodin Gen 2.5 | 1039 | — | — |
    | 9 | Seed3D v2.0 | 1035 | — | — |
    | 10 | Alpha3D 5 | 1033 | — | — |
    | 11 | VARCO 3D 2.0 | 1014 | — | — |
    | 15 | Sloyd v3 | 993 | — | — |
    | 20 | TRELLIS.2 | 850 | 24.9% | — |
    | 21 | SAM 3D | 787 | 9.3% | — |

    - 页头写着"0 votes cast"，和各模型的胜负数对不上，属于页面 bug
  - **历届冠军** [实测] — [top3d.ai seasons](https://www.top3d.ai/leaderboard/seasons)

    | 赛季 | 冠军 |
    |---|---|
    | S1–S2（2025-11、12） | YVO3D |
    | S3（2026-01） | Hunyuan 3D |
    | S4（2026-02） | Hi3D |
    | S5–S11（2026-03 至 09） | **Tripo AI**，连续 7 季 |

    - S1–S11 合计约 22.6 万票（各季 1.5 万–2.6 万，按页面数字加总）
  - **S10（2026-08）分项榜** [实测] — [top3d.ai S10](https://www.top3d.ai/leaderboard/seasons/aug-26)

    | 子榜 | 前几名 | 末位 / 备注 |
    |---|---|---|
    | 贴图 | Tripo v3.1 1142 > Rodin 2.5 1106 > Hi3D v3.0 1099 > Meshy 7 1073 | TRELLIS.2 905，SAM 3D 787 |
    | 几何 | Tripo v3.1 1221（胜率 83.7%）> Hi3D v3.0 1211 > Meshy 7 1178 > Hunyuan v3.1 1164 | — |
    | 低模 | Tripo P1.0 1119 > Meshy T2 1085 > YVO3D 1052 > Rodin 1015 | Hunyuan Retopo 918 |
    | 分割 | Tripo Seg v2.1 1096 > Hunyuan Part Splitter 1075 > Meshy Auto Split 1034 | Roblox CubePart 935，Rodin 913 |

  - R1 引用的 Sloyd 博客版本（2026-08-03 快照：Tripo 1042 第 1、Sloyd 1015 第 3）和 top3d.ai 官方 S10 数字**对不上**（S10 里 Sloyd 贴图榜只排第 10，1031）
    - 那个博客出自 Sloyd，对自己的排名有偏向 — [Sloyd blog](https://www.sloyd.ai/blog/ai-3d-model-generator-rankings)
- **厂商偏好研究**
  - 3D AI Studio 博客（2026-07-07）转述："网易和腾讯的 1,331 名资深 3D 美术，63.8% 偏好 Meshy 6 而非 Tripo 3.1"
  - 研究方没有写明，很可能是 Meshy 发布的；3D AI Studio 本身是多模型转售商 [第三方转述，未核实] — [3D AI Studio blog](https://www.3daistudio.com/blog/hitem3d-vs-meshy-vs-tripo-comparison)
  - 同一篇文章：2026-02 top3d.ai 累计 8.2 万票时，Hunyuan 3D v3.1 和 Hitem3D 进了前三 [第三方]
- **Seed3D 2.0 自评**：60 名 3D 打分员盲评偏好率 > 69%（R1 已有，这里不展开）

### Inferences
- **开源和闭源在两个榜上完全倒过来**
  - TRELLIS.2 在 HF Arena 排 18/24，在 top3d.ai 排 20/21
  - 闭源头部（Tripo / Rodin）**根本不参加** HF Arena
  - → 引用"Arena 排名"时必须注明是哪个榜、哪个赛季、哪个子榜
- **HF Arena 渲染榜奖励高斯泼溅和贴图观感**
  - 论文自己证明 splat +16.6、贴图 +144 Elo
  - 所以 TRELLIS-3DGS 排第 2，不代表它能进管线
  - 拓扑榜和 top3d.ai 的低模 / 分割 / UV 子榜，才更接近"生产可用"
- **Tripo 是"管线可用性"子榜的全能王**：低模、分割、Smart UV 都是第 1；Meshy 是综合观感的头部

### Gaps
- PicGen3D、404_GEN、Zaohaowu3D 是谁家的：搜索额度用完，没查到（404_GEN 可能是 Bittensor 子网的项目，**未核实**）
- top3d.ai 运营者的独立性和资金来源不明
- 刷票防护机制没有公开
- 没找到第三方付费、样本 > 100 人、方法公开的用户偏好研究

---

## Q4 客户案例：已上线产品里的 AI 3D

### Takeaway
- **能点名的企业客户很多，但能证明"AI 资产进了已发售商业游戏"的一手案例本轮一个都没找到**
- 厂商案例几乎都停在下面几种：
  - 开发中的项目（Azra Games 的 Project: Legends、Redly 未命名首作）
  - 原型和白盒
  - 电商数字孪生（Lowe's / SharkNinja / Casio）
  - 3D 打印手办
  - 教育

### Cited Findings
- **Kaedim**（指标都是公司自报，页面无日期，© 2026）
  - **Azra Games**：Project: Legends 开发中
    - 角色制作从 6–8 周降到 6–8 天
    - 概念到生产时间降 86%，月产量 ×25
    - CTO Travis Boudreaux 背书 — [Kaedim Azra](https://www.kaedim3d.com/case-study/dynamic/azra-games)
  - **Redly Games**：UE5 手游首作，**明确写着"尚未发布"**
    - 角色从 4–5 周降到 1–2 天，资产月产量 ×14 — [Kaedim Redly](https://www.kaedim3d.com/case-study/dynamic/redly)
  - **Lowe's**：电商数字孪生
    - 页面注明"独立案例，未获 Lowe's 背书"
    - 每资产 8.7 小时 vs 市场平均 32 小时；年省 $60 万（页内另一处写 $100 万，自相矛盾）— [Kaedim Lowe's](https://www.kaedim3d.com/case-study/dynamic/lowes)
  - **Myth Studio**（伦敦动画工作室）：每资产 4 小时 vs 40 小时；用在动作测试和迷你短片 — [Kaedim Myth](https://www.kaedim3d.com/case-study/dynamic/myth-studio)
  - 首页卡片 — [kaedim3d.com](https://www.kaedim3d.com/)
    - SharkNinja：省 80% 时间，年省 $60 万
    - Casio：快 6.4 倍，年省 $47 万
- **Meshy** [公司自报] — [Meshy Enterprise](https://www.meshy.ai/enterprise)；[casestudies.com](https://www.casestudies.com/company/meshy)
  - 37 Interactive：建模时间 -50%
  - 41 个案例里，游戏类大多是独立开发者（CoolPuzzler、Soliloquis、DarkTree、Omar Hernandez Salmeron 做了 3,000+ 飞船资产等）
  - 没有一个写明是已发售作品
- **Tripo** 点名伙伴：Tencent、NetEase、Microsoft、Sony、HTC、Stability AI [公司自报，媒体转述] — [ARInsider](https://arinsider.co/2025/09/22/can-tripos-gen-ai-step-change-unlock-3d-tiktok/)
- **Rodin**：NVIDIA、Meta、Supercell、Tencent、NetEase、Shutterstock 等出现在 logo 墙，**没有说明关系** — [hyper3d.ai](https://hyper3d.ai/)
- **Polycam**：Fortune 500 logo 墙（这是采集类业务，不是生成）— [poly.cam/pricing](https://poly.cam/pricing)
- **平台集成 = 事实上的大客户**
  - Unity（→ Scenario → Meshy 接口）— [Unity Third-Party AI Terms](https://unity.com/legal/third-party-ai-terms)；[Scenario](https://www.scenario.com/features/3d-editing)
  - Hi3D 一键打通 Bambu / Elegoo / Creality 等切片软件 — [hitem3d.ai](https://www.hitem3d.ai/)

### Inferences
- **游戏 B2B 的真实用法**：概念 → 白盒 / 原型 → 加速外包，不是最终资产。和 R1 里影眸"三视图 / 白盒"的口径一致
- 最清楚的"真钱"案例在**电商数字孪生**（Kaedim）和 **3D 打印**（Meshy、Hi3D）。游戏厂商愿意挂 logo，但不愿意公开说"已发售作品里用了 AI 资产"
  - 很可能和 Steam AI 披露政策、玩家舆论有关（**推断**，本轮没有拿到 Steam 披露数据）

### Gaps
- 没能检索 Steam "AI Generated Content Disclosure" 里提到 Meshy / Tripo 的已发售游戏（搜索额度用完）
- Reddit r/gamedev、r/3Dprinting 的真实使用口碑：没覆盖到
- Kaedim 案例里人工参与的比例：页面没写

---

## Q5 绑骨 / 动画 / 重拓扑层：谁在卖、卖多少

### Takeaway
- 这一层正在被**生成器免费打包**（Meshy web 端 remesh / rig / animation 0 credits；Sloyd、Anything World 都是"无限"）
- 独立玩家只能走两条路：
  - 极低单价 API：Uthana 绑骨 $0.15/次，动作 $0.02–0.10/秒
  - 嵌进 DCC 卖席位：Cascadeur $19–49/月、Autodesk MotionMaker
- 免费基线：Reallusion AccuRIG

### Cited Findings
- **绑骨**

  | 产品 | 价格 | 备注 | 来源 |
  |---|---|---|---|
  | Uthana | $0.15/次 | 2026-08 停售新订阅，全部转按量付费 | [Uthana pricing](https://uthana.com/pricing) |
  | Meshy | API 5 credits；web 0 | — | [Meshy API pricing](https://docs.meshy.ai/en/api/pricing) |
  | Anything World / Everything Universe | $50 / $250 月档无限动画 | 2024-04 时是 5 credits/次（约 $0.83–1.25）；2023-10 发布时免费 3 个/月 | [everythinguniver.se](https://everythinguniver.se/pricing)；[CG Channel](https://www.cgchannel.com/2023/10/animate-anything-uses-ai-to-rig-your-3d-characters) |
  | Reallusion AccuRIG | 免费独立版 | 单网格 A/T pose；高级功能在 Character Creator 4 里 | [Reallusion](https://www.reallusion.com/auto-rig/accurig/) |
  | Sloyd | Plus / Pro 订阅里"无限" | — | [Sloyd pricing](https://www.sloyd.ai/pricing) |
  | Nilo | "一键绑骨"，含在 Bits 里 | — | [nilo.io](https://nilo.io/) |

  - Anything World 的已知限制（CG Channel，2023–2024）：
    - 超过 2 万顶点先减面
    - 没有面部 blendshape
    - 不支持分层服装子网格
- **动画**

  | 产品 | 价格 | 备注 / 来源 |
  |---|---|---|
  | Uthana text-to-motion | v1 $0.02/s，v2 $0.03/s，v3 $0.10/s | 同表还有：video-to-motion $0.05/s、角色生成 $0.75/个 — [Uthana](https://uthana.com/pricing) |
  | Meshy | API 每动作 3 credits；Text-to-Motion 10 / 3 credits | — |
  | Sloyd | text / video → animation 30 credits | [Sloyd pricing](https://www.sloyd.ai/pricing) |
  | Cascadeur | Indie $19/月，Pro $49/月 | AutoPosing；Indie 要求营收 < $10 万 — [Cascadeur](https://cascadeur.com/plans) |
  | Autodesk MotionMaker | 未披露 | Maya 内置，2026-10 获 Fast Company 奖 — [Autodesk](https://adsknews.autodesk.com/en/news/motionmaker-maya-fast-company-next-big-things-in-tech/) |
  | DeepMotion SayMotion / Animate 3D | — | 定价子页面没抓到数字 — [DeepMotion](https://www.deepmotion.com/pricing) |

  - Uthana 是 Unity AI 的动画伙伴 — [Unity Third-Party AI Terms](https://unity.com/legal/third-party-ai-terms)
- **重拓扑 / UV**
  - Meshy：Remesh 5、UV Unwrap 5 credits（API），web 端 Remesh 0 — [Meshy](https://docs.meshy.ai/en/api/pricing)
  - Tripo 四边面在 fal 上 +$0.05 — [fal Tripo](https://fal.ai/models/tripo3d/tripo/v2.5/image-to-3d)
  - Sloyd 四边面 +5 credits（≈ $0.07）— [Sloyd API](https://www.sloyd.ai/api/pricing)
  - Alpha3D：重拓扑 + 展 UV + 贴图 + 格式转换打包，€5/月起 — [alpha3d.io](https://www.alpha3d.io/)
  - Scenario：转售 Meshy Remesh，可设目标面数，四边 / 三角都行 — [Scenario](https://www.scenario.com/features/3d-editing)
  - 质量对比（top3d.ai S10 低模榜）：Tripo P1.0（原生低模）1119 > Meshy T2 1085 > … > Tripo 3.1 Retopo 977 > Hunyuan Retopo 918
    - **原生低模生成打败了"先生成再 retopo"** — [top3d.ai S10](https://www.top3d.ai/leaderboard/seasons/aug-26)
  - Smart UV 榜（2026-10）：Tripo Smart UV 1052 ≫ Hunyuan Semantic UV 948 — [top3d.ai](https://www.top3d.ai/)

### Inferences
- **后处理作为独立生意的空间在收窄**
  - 绑骨价格两年降了约 85–90%（$1–1.25 → $0.15，或者免费）
  - Uthana 停掉订阅、转按量付费，也说明订阅制在这一层卖不动（**推断**）
- **技术上，"原生出低模 / 四边面 / 分件"正在取代后处理**（Tripo P 系列、Meshy T2 在低模榜上的领先）
  - 留给独立后处理工具的护城河：
    - 复杂角色（面部、服装）
    - 进 DCC 的深度集成（Cascadeur、MotionMaker、AccuRIG + CC4）

### Gaps
- Mixamo 现状：页面是 JS 加载，没能确认有没有停服公告
- DeepMotion、Move.ai、Radical、Plask 的 2026 价格：没抓到
- 没有独立第三方测过"自动绑骨在 AI 网格上的成功率"

