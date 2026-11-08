# 中国 AI 3D 生成公司 × 3D 打印 / 潮玩消费链（R2 深挖，截至 2026-10-13）

> 口径
> - 本文接着 `3d_asset_gen.md` 往下挖，**那份里已有的内容不再重复**，只补新数字、改口径和纠错。
> - 每个数字都带标签：
>   - **[公司自报]**：公司或创始人自己说的
>   - **[招股书]**：来自招股书，含媒体对招股书的转述
>   - **[媒体报道]**：媒体称，出处不明或匿名信源
>   - **[第三方估算]**：券商、咨询机构、数据库的估算
>   - **[本文计算]**：本文自己算的
> - 每条都注了日期。
> - 调研量：约 65 次搜索 / 抓取。中途 WebSearch 的会话额度（200 次，所有 agent 共用）耗尽两次，后半段只能抓已知 URL，所以游戏公司、阿里、生数那几块偏薄，见各节 Gaps。
> - Demo 页抓取验证结果
>   - 能抓到内容：hyper3d.ai/pricing、hi3d.ai、hitem3d.ai/pricing、neural4d.com、triverse.ai、GitHub / HF 各仓库
>   - 返回 403：tripo3d.ai/pricing、tripo3d.ai/zh/blog/tripo-p2-0-preview、makerworld.com/makerlab
>   - SPA 空壳，抓不到正文：3d.hunyuan.tencent.com、platform.tripo3d.ai

---

## Q1 国内 AI 3D 玩家（一家一行）

### Takeaway
- 已经能看到收入的独立公司只有三家，而且都靠**海外订阅 + 3D 打印 / 游戏 prosumer**：
  - VAST / Tripo
  - 影眸（Hyper3D Rodin）
  - 数美万物（Hi3D，就是原来的 Hitem3D）
- 大厂用开源和云 API 卡位：
  - 腾讯混元 3D：开源 2.x，3.x 只走 API，国内 150+ 企业接入
  - 字节 Seed3D：走火山引擎
  - 阶跃 / 光影焕像 Step1X-3D：Apache 开源
- 阿里、生数、智谱、商汤、网易伏羲：**没有找到**自有的独立 3D 生成商业产品。阿里只以 VAST 投资方的身份出现。

### 总表（一家一行）

| 玩家 | 关键数字（标签，日期） | 来源 |
|---|---|---|
| **VAST / Tripo** | 2026 年四轮：A $5000 万（03-05）→ A+/A++ 约 $2 亿（06）→ A3 约 $1.5 亿（07）→ B/B+ 约 30 亿元 ≈ $4.45–4.46 亿（09-01）[媒体报道]；Tripo Studio 创作者 650 万+、累计近 1 亿模型、9 万+ 开发者（2026-03）[公司自报]；个人用户 1000 万、工作室客户 9 万含 Sony / 网易（2026-06，Bloomberg）[公司自报]；ARR $1200 万、专业用户 300 万+、工作室 4 万+、员工约 100（2025-09，Forbes）[公司自报]；**海外收入占比没有公开数** | [新京报](https://m.bjnews.com.cn/detail/1772687503129302.html)、[投中网](https://m.chinaventure.com.cn/news/113-20260901-393044.html)、[AI Weekly 转 Bloomberg](https://aiweekly.co/alerts/tripo-ai-hits-10m-users-as-vast-raises-200m)、[CO/AI 转 Forbes](https://getcoai.com/news/chinese-ai-startup-tripo-hits-12m-revenue-with-3d-generation-tool/)、[PocketGamer](https://www.pocketgamer.biz/genai-firm-tripo-raises-445m-two-months-after-series-a3-round/) |
| **影眸 Deemos / Hyper3D Rodin** | 2026-06-23 数亿元融资（凯辉、上海国投先导领投）；此前 7 个月内两轮；ARR "数千万美元"；海外收入约 80%；C 端用户 60%；Gen-2.5 首月订阅与 ARR 环比 >400% [公司自报]；客户：字节、Unity、Figma、Canva；团队约 60 人 | [界面](https://m.jiemian.com/article/14631332.html)、[搜狐](https://m.sohu.com/a/1040643865_114986/)、[东方财富](https://finance.eastmoney.com/a/202606233779269161.html) |
| **腾讯混元 3D** | 开源 2.0（2025-01-21）/ mini / mv / Turbo（2025-03）/ 2.1（2025-06-13）；v2.5 参数 1B→10B，消费端每天免费 20 次（2025-04-23）；国内 150+ 企业接入 API（2025-11）；Hunyuan3D-2 仓库 15k stars、HF 月下载 131,796；2.1 仓库 4.2k stars、HF 月下载 63,342（2026-10 抓取）；2026-08 新出 Buffalo 1.0（3D 统一多模态）、WorldClaw（agentic 开放世界） | [GitHub](https://github.com/Tencent-Hunyuan/Hunyuan3D-2)、[HF](https://huggingface.co/tencent/Hunyuan3D-2)、[HF 2.1](https://huggingface.co/tencent/Hunyuan3D-2.1)、[格隆汇](https://m.gelonghui.com/live/1888520)、[cinevva](https://app.cinevva.com/zh-CN/news/2025-11-26-tencent-hunyuan-3d-engine)、[org 列表](https://github.com/orgs/Tencent-Hunyuan/repositories?q=3D) |
| **字节 Seed3D** | 1.0（2025-10）、2.0（2026-04-23），走火山引擎 API。**本轮没抓到价格**：火山文档页是 SPA，seed.bytedance.com 已不列 Seed3D | 见 `3d_asset_gen.md` |
| **数美万物 Math Magic（Hi3D = 原 Hitem3D）** | 2024 年初成立，创始人任利锋（前字节 PICO 副总裁）；累计五轮，近半年两轮近 $5000 万（A+ 于 2026-08-20 公布；BAI、华业天成领投）；V3.0（2026-08-19）做到 2048³ 体素；官网称 1000 万+ 模型、200 万+ 创作者、120+ 国家 [公司自报]；珠三角自建工厂、北京有打印实验室；做手办、工艺品、首饰；造好物（Builda）社区 + 造物相机 App（一张照片 → 手办） | [PingWest](https://www.pingwest.com/a/316644)、[36Kr Japan](https://36kr.jp/502619/)、[hi3d.ai](https://www.hi3d.ai/)、[Bernama](https://bernama.com/en/press/news.php?id=2574262) |
| **光影焕像 × 阶跃 Step1X-3D** | 2025-05-13 开源，Apache-2.0；几何 1.3B + 纹理 3.5B；附 80 万 UID 数据集；897 stars、HF 107 likes；作者含谭平（Ping Tan，光影焕像创始人） | [GitHub](https://github.com/stepfun-ai/Step1X-3D)、[HF](https://huggingface.co/stepfun-ai/Step1X-3D) |
| **魔芯科技 KOKONI**（**不是** Hitem3D） | 消费级打印机 EC2 售 999 元；营收 2023 年 753 万元 / 2024 年 545 万元 / 2025 年前 10 月 805 万元，净利润持续为负；哈勃持股 7.98%；2026-03 Pre-A+ 后估值约 8.4 亿元 [媒体推算]；已转向 4D 世界模型（KOKONI-World） | [财联社](https://www.cls.cn/detail/2318756) |
| **元象 XVERSE** | 官网主打 "XVERSE 3D 一站式 3D 内容生成与消费平台"（云渲染、VR 看房、3DGS 插件），偏重建和渲染，**没看到图生 3D 网格产品** | [xverse.cn](https://www.xverse.cn/) |
| **网易伏羲** | 官网没有 3D 生成产品；相关的是"绘梦天工"美术外包平台，称合作 30+ 款游戏 | [fuxi.163.com](https://fuxi.163.com/) |
| **Neural4D / Triverse** | 官网都没写公司主体和所在地；Neural4D 创始人署名 "Feihu"；两家都主打 3D 打印 / 水密 STL | [neural4d.com](https://www.neural4d.com/)、[triverse.ai](https://www.triverse.ai/) |
| 阿里 / 生数 / 智谱 / 商汤 / 爱诗 / 有言 | 没找到自有 3D 生成产品的可靠来源；阿里只是 VAST A 轮领投方 | [新京报](https://m.bjnews.com.cn/detail/1772687503129302.html) |

### Cited Findings
- **VAST / Tripo**
  - **B/B+ 投资方全名单**（2026-09-01）
    - 领投：经纬创投
    - 产业方：完美世界、蓝色光标、芯动能、延趣游戏、中科创达、广电投资、三七互娱
    - 财务方：鼎晖 VGC、中金资本、CMC、洪泰等
    - 老股东：达晨、春华、四三九九、慕华、绿洲、华控
    - FA：华兴 — [投中网](https://m.chinaventure.com.cn/news/113-20260901-393044.html)
  - **A 轮**（2026-03-05）[媒体报道]
    - 领投：阿里、恒旭资本
    - 跟投：元禾璞华、百度风投、东方嘉富
    - "生态合作"企业名单：阿里、腾讯、字节、网易、上汽、**拓竹**、优必选（原文没说这些是付费客户） — [新京报](https://m.bjnews.com.cn/detail/1772687503129302.html)
  - **A+/A++**：英诺（INCE Capital）、国寿长三角基金联合领投，Bloomberg 称估值 ≥ $10 亿（2026-06-01） — [AI Weekly](https://aiweekly.co/alerts/tripo-ai-hits-10m-users-as-vast-raises-200m)
  - **P2.0 发布节奏**
    - Preview 在 Gamescom（2026-08）亮相 — [PocketGamer](https://www.pocketgamer.biz/genai-firm-tripo-raises-445m-two-months-after-series-a3-round/)
    - 2026-09-29 时仍标 "preview"
    - 规格：三角面 500–5 万、四边面 500–2.5 万（P1.0 只有三角面，≤ 2 万）；一次最多出 4 个不同面数的变体；有 Mesh Edit 和自动部件分离；导出 FBX/GLB/OBJ/USDZ/**STL/3MF**
    - 免费只送 2 次，商用权要付费 — [Digital Production](https://digitalproduction.com/2026/09/29/tripo-p2-0-put-quad-mesh-generation-to-the-test/)
    - 评测者的保留意见：四边面 ≠ 能直接绑骨；GLB 导出可能会被三角化
  - **纠错**：旧笔记写"P2.0 2026-09-01 发布"不准。09-01 只是融资公告日，模型那时是 Preview（Gamescom 首发）。
- **影眸**
  - **Gen-2.5 上线日期有冲突**：东方财富写 5-26，搜狐写和融资同日 6-23 — [东方财富](https://finance.eastmoney.com/a/202606233779269161.html)；[搜狐](https://m.sohu.com/a/1040643865_114986/)
  - Gen-2.5 规格：千万面级，最快 4 秒出百万面，12K 原生贴图 [公司自报] — [搜狐](https://m.sohu.com/a/1040643865_114986/)
  - 游戏工作室的两种用法：渲染三视图；发包前出白盒给外包参考 — [界面](https://m.jiemian.com/article/14631332.html)
- **混元许可证**：Tencent Hunyuan Community License **排除欧盟、英国、韩国**；被许可方所有产品月活 > 100 万就要另向腾讯申请授权 — [LICENSE](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/blob/main/LICENSE)
- **数美万物**
  - Hi3D 和 Hitem3D 是同一产品线：hi3d.ai 的静态资源放在 hitem3dstatic 域名，社交账号叫 "Hitem3D"；hitem3d.ai 定价页的联系邮箱是 support@hi3d.ai，页脚主体是 Oceano HK Holding Limited — [hi3d.ai](https://www.hi3d.ai/)、[hitem3d.ai/pricing](https://www.hitem3d.ai/pricing)
  - **纠错**：旧笔记把"魔芯 / Hitem3D"并在一起是错的。魔芯是 KOKONI 打印机公司，和 Hitem3D 无关。

### Inferences
- **三家独立公司**收入都靠订阅制和海外用户；有披露的只有影眸（海外约 80%）。Tripo 的海外占比查不到，但它的英文媒体曝光、Gamescom 首发、Sony 客户这些线索，都指向海外为主。
- **数美万物**是国内唯一明说要做"生成 → 工厂 → 交付"闭环的，商业模式更像"AI 版 Shapeways"，而不是 SaaS。
- **腾讯许可证排除欧盟 / 英国 / 韩国**，等于把这些市场留给了 Tripo / Meshy 的商业 API。

### Gaps
- Tripo 2026 年的 ARR、海外占比：没有任何公开数字
- 影眸 ARR 的具体数值："数千万美元"是区间
- 混元 3D 的实际调用量和收入；Seed3D 价格；阿里 / 生数 / 智谱 / 商汤 有没有 3D 产品：搜索额度耗尽，没查完
- Neural4D、Triverse 的主体公司：官网没写

---

## Q2 3D 打印链：拓竹 / 创想三维 / 智能派 / 纵维立方 / 市场规模

### Takeaway
- 消费级 3D 打印 2025 年全球 GMV 约 **$41–49 亿**，深圳"四小龙"合计约九成。
- 拓竹 2025 年营收破百亿元 [公司确认]，2025 年 GMV 份额 42.7% [招股书]，约为第二名创想三维的 4 倍。
- MakerWorld 月活约 1000 万，是 AI 3D 在 C 端最大的单一分发口。

### Cited Findings
- **拓竹 Bambu Lab**
  - **营收**
    - 2024 年：55–60 亿元，净利润近 20 亿元 [第三方估算，东吴证券]
    - 2025 年：**破 100 亿元** [公司确认] — [第一财经 2026-01-29](https://www.yicai.com/news/103029400.html)；[IT之家](https://www.ithome.com/0/899/665.htm)
  - **出货与份额**
    - 2024 年出货约 120 万台，出货份额 29% [第三方 / 招股书] — [华尔街见闻](https://wallstreetcn.com/articles/3771859)
    - 2024 年 GMV 份额 35.5%，创想三维 11.2%，智能派 10.7%，纵维立方 10.0% [招股书] — [36Kr](https://eu.36kr.com/zh/p/3778683779798018)
    - **2025 年** GMV 份额 **42.7%（约 $13 亿）**，创想三维 11.2%（约 $3.4 亿）[招股书] — [21世纪经济报道 2026-08-24](https://www.sfccn.com/2026/8-24/xMMDE0NDlfMjIxODUxMg.html)
    - Context：2025 年入门级（< $2500）出货份额 37%，排第一 [第三方] — [Tom's Hardware](https://tomshardware.com/3d-printing/bambu-lab-overtakes-creality-as-the-worlds-top-selling-budget-3d-printer-brand)
  - **估值**
    - 36 氪称新一轮估值或达 $100 亿、腾讯参投；拓竹回应"消息不实"（2025-11-24） — [IT之家](https://www.ithome.com/0/899/665.htm)；[KrASIA](https://kr-asia.com/bambu-lab-nears-usd-100-billion-valuation-as-tencent-eyes-new-investment)
    - 2027 年 IPO 传闻：公司也否认（2026-08） — [21世纪](https://www.sfccn.com/2026/8-24/xMMDE0NDlfMjIxODUxMg.html)
  - **融资史**：IDG A 轮 3000 万元（投后约 2 亿元）→ B 轮铭石、五源（估值 $20 亿）→ C 轮 IDG 1.5 亿元 [媒体报道] — [36Kr](https://eu.36kr.com/zh/p/3725272216681093)
  - P1 系列装在全球 70%+ 的打印农场里 [公司自报] — [IT之家](https://www.ithome.com/0/899/665.htm)
- **MakerWorld**（2025 年数据）[公司自报] — [3DPrint.com](https://3dprint.com/324181/bambu-lab-says-2025-was-a-breakout-year-10-million-monthly-users-and-real-business-growth/amp/)
  - 月活约 1000 万
  - 原创模型 260 万，每天新增 7000+，设计师约 28 万
  - 全年打印 2.9 亿小时，一年留存 83%
  - BambuHandy 2025 年下载近 200 万
  - 春晚经豆包渠道送出 6600+ 台
- **MakerWorld 创作者收入**
  - 独家模型计划：1 积分 = $0.066，满 $100 可提现（2024-10） — [Bambu blog](https://blog.bambulab.com/exclusive-model-program-cash-rewards-and-copyright-support)
  - AI 生成模型**被排除在独家计划外**；2026-02 起要求至少一张真实打印照片 — [Bambu wiki](https://wiki.bambulab.com/zh/makerworld/tutorials/exclusive-model-guideline)；[Fabbaloo](https://www.fabbaloo.com/?p=234795)
  - 平台累计向创作者付了多少钱：**没有公开**
- **潮玩 IP 风险**
  - 泡泡玛特 2025-05 / 10 两次发函，2026-02 起诉拓竹（平台侵权）
  - 2026-03-16 拓竹宣布和解，相关内容全部下架
  - 寒木春华也另行起诉了拓竹 — [36Kr](https://eu.36kr.com/zh/p/3725272216681093)
- **创想三维 Creality（3388.HK）[招股书]**
  - **收入**：2023 / 2024 / 2025 年 18.83 / 22.88 / 31.27 亿元
  - **利润**
    - 净利润：1.29 亿 / 8866 万 / **-1.82 亿元**（2025 年亏损因上市前发股、派息 2.4 亿）
    - 经调整净利：2025 年约 9239 万
  - **毛利率**：31.8% / 30.9% / 31.2%
  - **研发**：0.96 亿 → 2.22 亿（占收入 7.1%）
  - **打印机业务收入**：14.0 / 14.2 / 17.9 亿
  - **出货**：2023 年 87 万台 → 2024 年 72 万台；三年依次 87.1 / 72.1 / 74.2 万台
  - **收入地区**：中国大陆占比从 2022 年 49.9% 降到 2025Q1 24.6%，北美 + 欧洲近 60%
  - **上市**：2026-05-29 上市，发行价 18.8 港元，募资净额 12.72 亿港元，首日收涨 36%
  - 来源：[iTiger](https://www.itiger.com/hans/news/2626971776)；[华尔街见闻](https://wallstreetcn.com/articles/3771859)；[36Kr](https://eu.36kr.com/zh/p/3778683779798018)；[21世纪](https://www.sfccn.com/2026/8-24/xMMDE0NDlfMjIxODUxMg.html)
- **智能派 ELEGOO**
  - 营收：2024 年 16 亿元 → 2025 年 23 亿+ [媒体报道] → 2026 年目标 35–40 亿 [公司自报]
  - 光固化份额全球第一，海外收入 90%+
  - 融资：2025-11 大疆战投；2026-04 B+ 轮 5 亿+ 元，美团龙珠领投，深创投、高瓴跟投
  - 2025 年上线 Nexprint 模型平台，设百万美元原创基金
  - 来源：[36Kr](https://eu.36kr.com/zh/p/3562896588242051)；[3DNatives](https://www.3dnatives.com/en/elegoo-funding-round-04052026/)
- **纵维立方 Anycubic**
  - 2026-06 B 轮数亿元，达晨、国泰海通领投
  - "年营收数十亿元"、员工 2000+、用户近 500 万 [公司自报]
  - 投资方判断"AI 生成 3D 模型未来两年行业爆发" — [投资界](https://news.pedaily.cn/202606/565277.shtml)
- **市场规模**
  - **灼识咨询**：全球消费级 GMV 2024 年 $41 亿 → 2029 年 $169 亿；出货 2024 年 410 万台 → 2029 年 1340 万台 [第三方估算，招股书引用] — [第一财经](https://www.yicai.com/news/103029400.html)
    - 36 氪把 410 万台标成 2025 年，有出入 — [36Kr](https://eu.36kr.com/zh/p/3778683779798018)
  - **中商产业研究院**：2025 年 $49 亿 → 2026 年 $63 亿 [第三方估算] — [华尔街见闻](https://wallstreetcn.com/articles/3771859)
  - **出口与出货增速**
    - 2026Q1 3D 打印机出口量同比 +119%（海关） — [36Kr](https://eu.36kr.com/zh/p/3778683779798018)
    - Context：2025Q4 入门级出货同比 +47%，中国厂商占 90%+

### Inferences
- **拓竹 2025 年 GMV 口径**
  - 招股书给的约 $13 亿，比"营收破百亿元（约 $14 亿）"还低
  - 说明招股书的 GMV 口径可能只算打印机、不算耗材和配件，**两者不能混着比**
- **AI 3D 的消费需求大头在 MakerWorld 这类平台上**，但平台同时在压 AI 内容的"变现"：AI 模型不能进独家计划、必须附实拍图
  - AI 生成主要是**给打印机卖耗材 / 提高机器使用时长**的工具
  - 它不是创作者变现的渠道

### Gaps
- 拓竹 2025 年的净利润、出货量：公司没披露
- MakerWorld 累计付给创作者多少钱、AI 生成功能的调用量
- 创想云（Creality Cloud）的用户数：招股书转述里没找到
- 招股书原文（HKEX 披露易 PDF）没直接抓，数字都来自媒体转述

---

## Q3 AI 生成 → 打印 / 潮玩手办的产品和收入

### Takeaway
- **MakerWorld 的 MakerLab 已变成多引擎聚合入口**
  - 2025-07：先接混元
  - 2026-03-17：上线 Meshy 驱动的 Image-to-3D，按导出计费
  - 据第三方说法，可以在 Meshy 6 / 混元 3.1 / Tripo 3.0 之间切换
- 国内"照片 → 手办"闭环：做得最重的是数美万物（自建工厂 + 造物相机），其余多是小红书 / 闲鱼个人卖家用 GPT 生图 + Tripo 拼起来的流程。**没有找到任何闭环产品的收入数据。**

### Cited Findings
- **拓竹 × 腾讯云**（2025-07-30）
  - MakerWorld 全面接入混元 3D，"预计每月调用量突破 10 万次"（预期，不是实际数）
  - 宣称 0.1mm 级精度、1024 几何分辨率、无需后期修复就能打印 — [爱范儿](https://www.ifanr.com/1632456)
- **Meshy × MakerWorld**（2026-03-17 新闻稿）
  - MakerLab Image-to-3D 对所有用户开放，**每次导出 2 个 MakerLab 积分**，支持一键全彩多色打印
  - Meshy 自称 1000 万+ 创作者 — [Utusan / PR Newswire](https://www.utusan.com.my/pr-newswire-en/2026/03/how-to-turn-any-image-into-a-full-color-3d-print-in-one-click-meshys-multi-color-printing-powered-by-meshy-6-is-now-live-on-makerworld/)
- **可选引擎**："Meshy 6 / Hunyuan 3.1 / Tripo AI 3.0" 三选一，免费用户每天刷新积分 [单一第三方博客，官方没确认] — [Sorceress](https://sorceress.games/blog/makerworld-image-to-3d-model-game-ready-glb-path)
- **MakerLab AI 功能改按积分收费**：官方理由是"第三方 AI 服务成本高"；参数化生成器保持免费
- **PrintMon Maker**：送 50 积分，每个定稿模型 10 积分 — [3Printr](https://3printr.com/printmon-maker-bambu-lab-expands-makerworld-with-ai-supported-3d-modelling-2174465)
- **Tripo 与拓竹**：拓竹在 VAST A 轮新闻稿的"生态合作"名单里（2026-03） — [新京报](https://m.bjnews.com.cn/detail/1772687503129302.html)
- **数美万物**
  - Hi3D：Split-to-Print 拆件、多色打印准备，一键发到 Bambu Studio / OrcaSlicer
  - "选模型 → 选材质尺寸 → 打印到家"三步服务 — [hi3d.ai](https://www.hi3d.ai/)
  - 2026-06-29 推出面向积木收藏、机甲、设计师玩具爱好者的端到端打印工作流 — [Bernama](https://bernama.com/en/press/news.php?id=2574262)
  - 造物相机 App：一张照片生成手办模型 — [PingWest](https://www.pingwest.com/a/316644)
- **Hitem3D 套餐**（价格页没显示金额）
  - Free：100 积分（终身），约 10 个资产
  - Pro：1000 积分 / 月，约 100 个
  - Max：2400 积分 / 月，约 240 个
  - Ultra：8000 积分 / 月，约 800 个
  - 来源：[hitem3d.ai/pricing](https://www.hitem3d.ai/pricing)
- **个人卖家案例**（个例，仅供参考）
  - 小红书卖家用 AI 渲染图做手办，69 元一个，100 个售罄
  - 业内反驳：一个品类开模要 3–5 万元，单件工厂成本可能 > 40 元 — [搜索摘要，来源 smzdm / sspai，未逐篇抓取](https://post.smzdm.com/p/ad7d4g9k/)

### Inferences
- **打印平台站在 AI 3D 价值链的分发顶端**
  - MakerLab 能在多家模型之间切换 → 模型厂商被商品化
  - 2 积分 / 次的定价表明拓竹把生成成本**转嫁给用户**，不是拿它当收入来源
- **泡泡玛特诉拓竹和解**说明：潮玩 IP 方会追打"AI / 用户上传 → 打印"这条链，"照片生成手办"小程序的合规风险主要在 IP 衍生上

### Gaps
- 国内 "AI 公仔 / 手办定制" 小程序（淘宝、抖音、微信）的具体名称、单价、销量：搜索额度耗尽，没查到
- MakerLab 的 AI 调用量、各引擎份额、拓竹付给混元 / Meshy / Tripo 的分成：都没有公开
- 数美万物实物交付的订单量、客单价

---

## Q4 国内 B 端付费场景（游戏 / 电商 / 工业）

### Takeaway
- 游戏公司公开说法里，AI 用在**文案、脚本、2D 美术、视频素材**的多，**明确说用 AI 3D 建模的很少**。
  - 少数例子：腾讯《三角洲行动》用 Hy3D 推进场景管线；影眸说头部工作室"基本都买了账号"
- 游戏厂商更常见的参与方式是**投资 AI 3D 公司**（完美、三七、4399、延趣、巨人），不是公开的采购合同。

### Cited Findings
- **腾讯**
  - 《三角洲行动》"通过 Hy3D 推进场景端到端生产管线提效"，没给数字（2026） — [界面](https://m.jiemian.com/article/15162896.html)
  - 混元游戏视觉生成平台"分钟级生成高精度游戏角色"，含专业角色多视图生成（2025-07） — [36Kr](https://www.36kr.com/p/3394131222956417)
- **网易**
  - 2025 年财报：AI 原生管线已在美术、策划、编程、动画大规模部署，"部分环节效能提升达 300%"
  - 《逆水寒》AI 写任务脚本：2 周 → 3 天，人力成本降 40%（不是 3D） — [界面](https://m.jiemian.com/article/15162896.html)；[36Kr](https://www.36kr.com/p/3394131222956417)
  - 伏羲"绘梦天工"美术外包平台，称合作 30+ 款游戏 — [fuxi.163.com](https://fuxi.163.com/)
- **三七互娱**
  - 研发端视频素材 AI 生成占比 80% — [界面](https://m.jiemian.com/article/15162896.html)
  - AI 动捕让《Puzzles & Survival》开发周期缩短 40% — [36Kr](https://www.36kr.com/p/3394131222956417)
  - 同时是 VAST B 轮产业投资方
- **米哈游**
  - 刘伟："未来三年最多投入 1000 亿元深耕 AI"
  - 没有 3D 生成的具体说法 — [界面](https://m.jiemian.com/article/15162896.html)
  - GDC 披露《崩坏：星穹铁道》单角色约 4 万面（面部约 1 万）；对比之下，AI 模型常超 10 万面，更适合影视，不适合实时渲染（GameLook 2025-03-28） — [GameLook / 鉅亨](https://hao.cnyes.com/post/142267)
- **行业层面**
  - 音数协调研：游戏企业 AI 普及率约 86% — [界面](https://m.jiemian.com/article/15162896.html)
  - GameLook：游戏公司抱怨"与其用 AI 生成的 3D 模型，还不如由模型师人工建模"（2025-03） — [鉅亨](https://hao.cnyes.com/post/142267)
- **影眸的游戏客户**：头部工作室"基本都已购买账号"，部分做了私有化部署 — [界面](https://m.jiemian.com/article/14631332.html)
- **Tripo**：工作室客户里有 Sony、网易 [公司自报] — [AI Weekly](https://aiweekly.co/alerts/tripo-ai-hits-10m-users-as-vast-raises-200m)
- **Meshy 的游戏客户**：Supercell、SEGA、Snap、Funplus — [鉅亨](https://hao.cnyes.com/post/142267)
- **游戏厂商投资 AI 3D**
  - VAST B 轮：完美世界、三七互娱、延趣游戏
  - VAST 老股东：4399 — [投中网](https://m.chinaventure.com.cn/news/113-20260901-393044.html)
  - 世纪华通、完美世界分别出资 1.5 亿元、5000 万元，和砺思资本一起布局 AI — [界面](https://m.jiemian.com/article/15162896.html)
- **电商 / 工业**
  - 影眸称服务电商、工业设计客户，没给数字
  - 混元 3D 国内 150+ 企业接入，名单没公开
  - 都没找到量化证据 — [界面](https://m.jiemian.com/article/14631332.html)；[cinevva](https://app.cinevva.com/zh-CN/news/2025-11-26-tencent-hunyuan-3d-engine)

### Inferences
- 国内游戏 B 端是"**买账号 / 私有化部署 + 战略投资**"的结构，看不到单笔大合同
  - 3D 资产在游戏里卡在面数和拓扑上：4 万面角色 vs AI 出的 10 万面以上
  - 所以游戏公司主要拿它做原型、白盒、三视图

### Gaps
- 莉莉丝、米哈游在 3D 生成上的具体公开说法：没找到
- 腾讯游戏内部用混元 3D 的量化数据：没找到
- 电商 3D（淘宝 / 京东商品 3D 化）、工业设计的付费案例：搜索额度耗尽，没查

---

## Q5 国内价格 vs 海外

### Takeaway
- **混元 3D 国内比国际站便宜约三分之一**
  - 国内专业版标准生成按量价 2.4 元 / 次，约 $0.34
  - 国际站后付费 $0.50 / 次
- 海外订阅主流是 $20–30 / 月（Meshy / Rodin）。国内订阅价公开很少，只有 Meshy 中文定价有记录：无限档 698 元 / 月（2025-03）。

### Cited Findings
- **腾讯云国内**（文档更新于 2026-07-24） — [腾讯云计费](https://cloud.tencent.com/document/product/1804/123461)
  - 积分包：1000 积分 100 元 / 1 万积分 980 元 / 5 万积分 4750 元 / 10 万积分 9000 元；后付费 0.12 元 / 积分
  - 每次消耗积分
    - 专业版：Normal 20 / LowPoly 25 / Geometry 15 / Sketch 25；加 PBR、多视图、自定义面数各 +10
    - 极速版：15
    - 后处理：智能拓扑 50 / 纹理 30 / 组件 30 / UV 10 / 绑骨 10 / 格式转换 5
  - 失败不扣积分；页面提示混元相关服务"将逐步迁移至 TokenHub"
- **腾讯云国际**（更新于 2026-05-08） — [Tencent Cloud Intl](https://intl.cloud.tencent.com/document/product/1284/75281)
  - 后付费 $0.02 / 积分；积分包：1000 积分 $15 / 10 万积分 $1350
  - 每次消耗积分：专业版 Normal 25 / LowPoly 30；3.0 和 3.1 版本不加价
  - 新用户免费 200 积分
  - 并发包：$5000 / 并发 / 月
- **混元消费端**：每天免费 20 次（2025-04） — [格隆汇](https://m.gelonghui.com/live/1888520)
- **影眸 Hyper3D**（2026-10 抓取） — [hyper3d.ai/pricing](https://hyper3d.ai/pricing)
  - Creator：$30 / 月（按年付 $24），约 60 个模型
  - Business：$120 / 月（按年付 $96），约 416 个模型，含 API
  - 单买积分：$1.5 / 个
  - Enterprise 可私有化部署
- **Meshy 中文定价**：最高"无限"档 698 元 / 月（2025-03） — [GameLook / 鉅亨](https://hao.cnyes.com/post/142267)
- **MakerWorld**：每次导出 2 MakerLab 积分 — [Utusan](https://www.utusan.com.my/pr-newswire-en/2026/03/how-to-turn-any-image-into-a-full-color-3d-print-in-one-click-meshys-multi-color-printing-powered-by-meshy-6-is-now-live-on-makerworld/)
- **单次价格横向**（第三方，2026-08）：Tripo $0.30 / Rodin $0.29 / Meshy 6 $0.40 / Hitem3D $0.73 — 见 `3d_asset_gen.md` 引用的 Sloyd 博客

### Inferences [本文计算，按 1 USD ≈ 7.1 CNY]
- **混元专业版 Normal（不加 PBR）**
  - 国内：20 积分 × 0.09–0.12 元 = **1.8–2.4 元 / 次（$0.25–0.34）**
  - 国际：25 积分 × $0.0135–0.02 = **$0.34–0.50 / 次**
  - 国内比国际便宜约 25–50%
- **加 PBR 后**
  - 国内：2.7–3.6 元 / 次
  - 国际：$0.47–0.70 / 次
- **混元极速版**：国内 1.35–1.8 元 / 次（约 $0.19–0.25），是公开渠道里最便宜的一档商用 API 价
- **Hyper3D 折算单模型**：Creator 约 $0.40–0.50，Business 约 $0.23–0.29
  - 和混元国际站专业版价位差不多
  - 但订阅包含 UI 和编辑能力
- **结论**：国内云 API 单价已压到 2 元 / 次级别，独立公司在国内很难靠 API 收费，这和影眸、Tripo 收入偏海外订阅是一致的。

### Gaps
- Tripo 国内 / 海外订阅价：定价页 403，没拿到
- Seed3D 火山引擎价格、Hi3D 套餐美元价：页面没显示
- 国内消费端 App（混元、豆包等）有没有付费墙：没查到

