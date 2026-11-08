# Landscape 数字核查（market.md，2026-10-13）

- 范围：Overview 各表 + 五个 tab 的「1 Industry Landscape」表（营收 / 估值 / 融资 / 用户数），顺带核了表下「数据解读」里的数字
- 依据：先看 middle_processing/market/ 下的 r2_*.md，再看第一轮笔记；关键链接实际抓取（Dealroom、digg、第一财经、36氪、TechNode、Gasgoo、美图、Sacra×2、MiniMax IR、GetLatka）；Threekit、Roblox Cube 两条笔记里没有，另做了网页搜索
- 判定：CONFIRMED（确认）/ WRONG（错误）/ UNSUPPORTED（无出处）/ OUTDATED（有更新数字）；「注」= 数字没错，但口径、标签或日期需要修

| tab | company | field | page says | verdict | correct value | source URL |
|---|---|---|---|---|---|---|
| Overview | 快手 | AIGC 带动营销消耗 | 2025Q4 40 亿元（财报） | CONFIRMED | 港交所公告原文 "RMB4.0 billion" | https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0325/2026032500367.pdf |
| Overview | Meshy | 营收 | 年收入超 1 亿美元（自报） | CONFIRMED（注） | 这是 ARR > $100M（2026-09-30），不是「年收入」；建议写成「年化收入（ARR）」 | https://dealroom.co/news/158079-meshy-hits-100m-arr-first-ai-3d-firm-to-reach-milestone/ |
| Overview | Applied Intuition | 营收 | 约 8.3 亿美元/年（估算） | CONFIRMED（注） | Sacra 估算的 2025 年 ARR $830M；同页另有 $622M 的口径，未作调和 | https://sacra.com/research/applied-intuition-at-830m-year/ |
| Overview | Astrocade | 月活 / 变现 | 月活 1000 万，计划 2027 变现 | CONFIRMED | 2026-10 CEO 访谈：MAU 1000 万；变现定在「明年」（2027）。Kotaku 抓取 403，依据笔记 | https://kotaku.com/ai-generated-games-platform-already-has-10-million-monthly-users-2000741894 |
| Overview | World Labs | 收购价 | AMD 约 82 亿美元 | CONFIRMED | 约 $8.2B，全股票（2026-09-28） | https://datacenterknowledge.com/data-center-chips/amd-to-acquire-world-labs-for-8-2b-to-advance-ai-models-and-robotics |
| Overview | 世界模型（合计） | 融资 | 一年超 30 亿美元 | CONFIRMED | 约 $3B（Forbes 2026-06）；World Labs 1B + AMI 1.03B + Decart 0.3B + Odyssey 0.31B + PixVerse ¥29.8 亿 ≈ $3.06B | https://www.forbes.com/sites/josipamajic/2026/06/30/world-model-startups-raise-3-billion-vcs-bet-beyond-llms/ |
| Overview | 3D 单价 | 降幅 | 四年降 95% 以上 | CONFIRMED | 2022 年 $7.7–10/个 → 2026 年 $0.2–0.4，降 95–98% | r2_3d_asset_overseas.md |
| Overview | Blender 基金会 | 收入 | 311 万欧元 | CONFIRMED | 2024 年 €3,106,361 | https://download.blender.org/foundation/Blender-Foundation-Annual-Report-2024.pdf |
| Overview | three.js | npm 下载 | 月下载 7022 万，一年 6.4 倍 | CONFIRMED | 2026-09 为 70.2M，2025-09 为 11.0M；react 3.8 倍也对得上 | https://api.npmjs.org/downloads/point/2026-09-01:2026-09-30/three |
| Overview | Unity | Create 板块营收 | 2025 年 6.2 亿美元，+1% | CONFIRMED | $621.4M，2024 年 $614.0M（+1.2%） | https://www.sec.gov/Archives/edgar/data/1810806/000181080626000011/unity-20251231.htm |
| Overview | 国内小游戏 | 市场规模 | 2025 年约 610 亿元 | CONFIRMED | DataEye：约 610 亿元（+22%） | https://www.thepaper.cn/newsDetail_forward_32682540 |
| Overview | Khronos glTF 3DGS | 日期 | 2026-02 进入候选标准 | CONFIRMED | 2026-02-03 发布 Release Candidate | https://www.khronos.org/news/press/gltf-gaussian-splatting-press-release |
| Overview | NVIDIA 机器人生态 | 装机 | 四大机器人厂 200 万台 | CONFIRMED | "over 2 million robots" | https://nvidianews.nvidia.com/news/nvidia-and-global-robotics-leaders-take-physical-ai-to-the-real-world |
| Overview | 原生 3D 生成 | 单价 | 0.2–0.8 美元/个（链接 fal TRELLIS.2） | WRONG（出处对不上） | 链接页只能支撑 TRELLIS.2 的 $0.25/0.30/0.35；$0.2–0.8 是多家合起来的区间（Tripo $0.20 到 Meshy 6 $0.80）。要么改链接，要么改数字 | https://fal.ai/models/fal-ai/trellis-2 |
| Overview | 可灵 | 营收 | 2026Q2 超 8.5 亿元 | CONFIRMED | 快手 2026-08-19 中期业绩公告（TNGlobal 转载）："over RMB850 million" | https://technode.global/?p=990300 |
| Overview | BlenderMCP | GitHub star | 3.06 万 | CONFIRMED（注） | 30,585；仓库已改名 ahujasid/mcp-for-blender | https://api.github.com/repos/ahujasid/mcp-for-blender |
| Overview | 拓竹 | 营收 | 破 100 亿元 | CONFIRMED（注） | CEO 陶冶 2026-01-28 原话是「年营收破百亿的预期已经比较明朗」，属于预期，不是正式披露数；应标「自报」 | https://www.yicai.com/news/103029400.html |
| Overview | earthtojake/text-to-cad | star | 半年 1.98 万 | CONFIRMED | 约 6 个月 19.8k | r2_blender_code3d_cad.md |
| Overview | 品牌 Web 3D | 单项目价格 | 2–12 万美元 | CONFIRMED | Utsubo：$20k–60k（产品故事）/ $60k–120k（配置器） | https://www.utsubo.com/blog/interactive-website-vs-video-launch-budget |
| Overview | 光轮智能 | 新签订单 | 单季 5.5 亿元 | CONFIRMED | 2026Q1 新签 5.5 亿元 | https://autonews.gasgoo.com/articles/market-industry/2069795751096725504 |
| Overview | Poki | 月玩家 | 1 亿 | CONFIRMED | "100 million" monthly players | https://developers.poki.com/ |
| Overview | 国内孪生 | 单价 / 毛利 | 每单约 150 万元；毛利 20–50% | CONFIRMED | 51WORLD 在手合同均价约 ¥1.5M；毛利：凡拓数创 20–24%，51WORLD 41–51% | https://hao.cnyes.com/post/222558 |
| Overview | three.js vs Babylon | 倍数 | 约 47 倍 | CONFIRMED | 70.2M ÷ 1.50M ≈ 46.8 | r2_web3d_gallery.md |
| 3D Assets | Meshy | 营收 | 年收入超 1 亿美元（自报） | CONFIRMED（注） | ARR > $100M（2026-09-30），口径问题同 Overview | https://dealroom.co/news/158079-meshy-hits-100m-arr-first-ai-3d-firm-to-reach-milestone/ |
| 3D Assets | Meshy | 估值 | 15 亿美元 | CONFIRMED（注） | B 轮近 $4 亿，估值 $15 亿（2026-07）；同一篇 Dealroom 另一处写 $9.706 亿，两者冲突 | 同上 |
| 3D Assets | VAST Tripo | 营收 | 1200 万美元/年（2025-09 自报） | CONFIRMED（注） | ARR > $1200 万（ARInsider，2025-09）。数据已一年多，2026 年 ARR 找不到公开数 | https://arinsider.co/2025/09/22/can-tripos-gen-ai-step-change-unlock-3d-tiktok/ |
| 3D Assets | VAST Tripo | 估值 | 10 亿美元以上 | CONFIRMED | Bloomberg：A+/A++ 后 ≥ $1B（2026-06）；之后 B/B+ 约 30 亿元（2026-09），估值未披露 | https://aiweekly.co/alerts/tripo-ai-hits-10m-users-as-vast-raises-200m |
| 3D Assets | 影眸 Rodin | 营收 | 数千万美元/年（自报） | CONFIRMED | ARR「数千万美元」，海外约 80% | https://m.jiemian.com/article/14631332.html |
| 3D Assets | 数美万物 Hi3D | 融资 | 融资近 5000 万美元 | WRONG（口径） | 近 5000 万美元只是最近半年两轮的合计；公司共融了五轮，累计额未披露。另：两份笔记对「Hitem3D = 数美万物」说法相互矛盾，r2_3d_asset_overseas 写的是「没有一手确认」 | https://www.pingwest.com/a/316644 |
| 3D Assets | Kaedim | 融资 | 1600 万美元 | CONFIRMED | 累计 $16.01M（2024-03 A 轮 $15M） | https://www.cbinsights.com/company/kaedim/financials |
| 3D Assets | Roblox Cube | 用量 | 每天生成 6 万个资产 | UNSUPPORTED / 可能 WRONG | 能找到的只有累计数：2025-03 到 2026-02 共 180 万+ 个，折合约每天 5000 个；Wish Master 玩家生成 16 万个 | https://about.roblox.com/de/newsroom/2026/02/accelerating-creation-powered-roblox-cube-foundation-model |
| 3D Assets | 拓竹 | 营收 | 2025 年超 100 亿元（第一财经） | CONFIRMED（注） | 同 Overview：属于 CEO 的预期性说法 | https://www.yicai.com/news/103029400.html |
| 3D Assets | MakerWorld（数据解读） | 月活 | 约 1000 万 | CONFIRMED | 2025 年自报 | https://3dprint.com/324181/bambu-lab-says-2025-was-a-breakout-year-10-million-monthly-users-and-real-business-growth/amp/ |
| Game & World | Roblox | 创作者分成 | 2025 年付开发者 15 亿美元（财报） | CONFIRMED / OUTDATED | FY2025 DevEx $1.503B；截至 2026-09 的过去 12 个月约 $1.7B | https://www.sec.gov/Archives/edgar/data/1315098/000131509826000024/rblx-20251231.htm |
| Game & World | World Labs | 估值 | AMD 约 82 亿美元收购 | CONFIRMED | $8.2B（2026-09-28） | https://datacenterknowledge.com/data-center-chips/amd-to-acquire-world-labs-for-8-2b-to-advance-ai-models-and-robotics |
| Game & World | Decart | 营收 | 约 1260 万美元（2024 估算） | CONFIRMED（注） | GetLatka 写 $12.6M（2024-12），但自己也没标来源，可信度低 | https://getlatka.com/companies/decart.ai |
| Game & World | Decart | 估值 | 约 40 亿美元 | CONFIRMED | B 轮 $3 亿，估值约 $40 亿（2026-05）；Anthropic 约 $60 亿的收购谈判已终止（2026-09） | https://investgame.net/news/decart-raises-300m-series-b-at-4b-valuation |
| Game & World | Odyssey | 估值 | 14.5 亿美元 | CONFIRMED | B 轮 $3.1 亿，估值 $14.5 亿（2026-06） | https://thenextweb.com/news/odyssey-3-world-model-robots-humanoids-cars-drones |
| Game & World | Runway | 营收 / 估值 | 全公司 2 亿美元/年；53 亿美元 | CONFIRMED（注） | ARR $200M（联合 CEO 自报，2026-09）；估值 $5.3B（2026-02）。本 tab 这一格既没标签也没链接 | https://www.briefs.co/news/runway-s-arr-jumps-to-200-million-as-ai-video-finds-its-groo/ |
| Game & World | Astrocade | 融资 | 5600 万美元 | CONFIRMED | A+B 轮合计 $56M（2026-05） | https://www.fortune.com/2026/05/05/astrocade-raises-56-million-series-b-sequoia-video-games-platform-ali-amir-sadeghian/ |
| Game & World | 网易 蛋仔派对 | 创作者分成 | 超 2 亿元/年 | CONFIRMED | 2025-07 到 2026-07 激励与分成「突破 2 亿元」 | https://www.36kr.com/p/3896755010963333 |
| Game & World | 爱诗 PixVerse | 融资 | 29.8 亿元 | CONFIRMED（注） | ¥29.8 亿（财新）；日期和领投方在付费墙后，未核到 | https://www.caixinglobal.com/2026-08-14/in-depth-game-studios-have-bought-into-ai-but-players-still-arent-sold-102474160.html |
| Game & World | AMI Labs（缺失） | 融资 / 估值 | 表里没有 | 缺失 | 2026-03 种子轮 $10.3 亿，投前估值 $35 亿；世界模型赛道单轮第二大 | https://www.latent.space/p/ainews-yann-lecuns-ami-labs-launches |
| Game & World | Epic / Fortnite UGC（缺失） | 创作者分成 | 表里没有 | 缺失 | 2024 年 $3.52 亿，到 2026-01 累计超 $10 亿；可以和 Roblox、蛋仔并列比较 | r2_text_to_game.md |
| Ad Creative | 快手 可灵 | 营收 | 2026Q2 超 8.5 亿元（财报） | CONFIRMED | 中期业绩公告；链接是 TechNode 转载 | https://technode.global/?p=990300 |
| Ad Creative | 阿里妈妈 | 用量 | 双 11 生成 1.5 亿张素材 | WRONG（措辞） | 原文是双 11 期间淘宝天猫用 AIGC 生成 1.5 亿张**图片和视频**，不是全由万相营造生成、也不全是图片；万相营造对应的是覆盖约 100 万商家、每天节省 4000 万元以上 | https://news.sina.com.cn/o/2025-11-08/doc-infwschz3878925.shtml |
| Ad Creative | 美图 | 营收 | 生产力工具 6.2 亿元/年（财报） | CONFIRMED（注） | 这是 ARR 约 6.2 亿元（截至 2026-06），不是收入，建议写明 ARR | https://www.meitu.com/zh/media/439 |
| Ad Creative | MiniMax 海螺 | 营收 / 上市 | 全公司 2026H1 1.17 亿美元；上市 | CONFIRMED | $116.6M（+283%）；港交所 00100 | https://www.minimax.io/news/minimax-announces-first-half-2026-financial-results-1787744160 |
| Ad Creative | Higgsfield | 营收 / 估值 | 年化 10 亿美元（自报）；54 亿美元 | CONFIRMED | 公司 2026-09-24 自称；B 轮 $4 亿，估值 $5.4B（2026-08） | https://digg.com/ai/5c9uxe03 |
| Ad Creative | Runway | 营收 / 估值 | 2 亿美元/年（自报）；53 亿美元 | CONFIRMED | 同上 | https://www.briefs.co/news/runway-s-arr-jumps-to-200-million-as-ai-video-finds-its-groo/ |
| Ad Creative | HeyGen | 营收 / 估值 | 1 亿美元/年（自报）；5 亿美元（2024） | CONFIRMED（注） | ARR $100M 是 2025-10 公司在 X 上公布的；格子里没有链接和日期。「2026 年 $200M」没有一手出处 | https://x.com/HeyGen_Official/status/1978903438974161329 |
| Ad Creative | Synthesia | 营收 | 超 1 亿美元/年（无标签） | CONFIRMED / OUTDATED（注） | 2025-04 公司确认 ARR 过 $100M，应标「自报」并补日期；2026 年第三方估算约 $150M | https://www.arr.club/synthesia |
| Ad Creative | Synthesia | 估值 | 40 亿美元 | CONFIRMED | E 轮 $2 亿，估值 $40 亿（两份笔记分别写 2025-10 和 2026-01） | https://techcrunch.com/?p=3085527 |
| Ad Creative | Arcads | 营收 | 1000 万美元/年，8 人（自报） | CONFIRMED / OUTDATED（注） | 2025-11 创始人展示后台；GetLatka 估算 2026-04 约 $15M（自身页面互相矛盾）。估值写「未披露」没问题，但可以补上种子轮 $1600 万（2025-12） | https://getlatka.com/blog/arcads-revenue-ceo |
| Ad Creative | Photoroom | 营收 / 估值 | 约 9400 万美元/年（估算）；5 亿美元 | CONFIRMED（注） | Sacra 估算的 2024 年 ARR；估值 $5 亿来自 2024-03 B 轮。两个数都缺年份；公司最后一次自己确认的是 2023 年 €5000 万 ARR | https://sacra.com/c/photoroom/ |
| Ad Creative | Higgsfield（数据解读） | 增长 | 一年从 1100 万到 10 亿美元 | CONFIRMED（注） | 2025-05 的 $11M 是 Sacra 估算，2026-09 的 $1B 是自报，两种口径混在一起 | https://sacra.com/research/higgsfield-at-230m-arr/ |
| Ad Creative | Creatify（缺失） | 营收 / 融资 | 表里没有 | 缺失 | ARR 超 $900 万（上线 18 个月时）；A 轮 $1550 万，累计 $2300 万（2025-05）；和 Arcads 同属一类 | https://techcrunch.com/2025/06/02/former-dreamworks-ceo-jeffrey-katzenberg-co-leads-15-5m-series-a-for-ai-video-ad-platform/ |
| Web 3D | Threekit | 融资 | 融资 4360 万加元 | WRONG（口径） | 4360 万加元（约 3500 万美元）只是 2021-11 的 B 轮；累计约 8010 万加元。这条笔记里没有，靠网页搜索补的 | https://betakit.com/ottawa-founded-threekit-raises-43-6-million-cad-to-bolster-product-visualization-tech/ |
| Web 3D | Zakeke | 定价 | 59–300 美元/月 + 交易抽成 | CONFIRMED | 年付最低 $59/月，月付最高 $299.90/月；抽成 1.5–1.9% | https://admin.zakeke.com/en-US/pricing |
| Web 3D | Spline | 融资 | 2500 万美元 | CONFIRMED | 种子轮 $1500 万（2023）+ A 轮 $1000 万（2024-08） | https://pulse2.com/spline-collaborative-3d-design-platform-company-secures-10-million-series-a |
| Web 3D | PlayCanvas | 估值 | Snap 收购 | CONFIRMED | 2017 年被收购 | https://gamedeveloper.com/game-platforms/snapchat-acquires-cloud-based-engine-playcanvas |
| Web 3D | Poki | 月玩家 | 1 亿 | CONFIRMED | 自报 1 亿；Bloomberg（2025-11）写约 1 亿 MAU | https://developers.poki.com/ |
| Web 3D | Cocos | 收购价 | SUD 以 7200 万美元收购 | CONFIRMED（注） | 2025-11 $72M；出处是 Wikipedia 转引 PocketGamer，属二手 | https://en.wikipedia.org/wiki/Cocos2d |
| Web 3D | 配置器市场（数据解读） | 规模 | 约 17 亿美元 | CONFIRMED | 2025 年 $1.70B（Verified Market Research） | https://www.verifiedmarketresearch.com/product/3d-visual-product-configurator-software-market/ |
| Web 3D | Amazon 3D（数据解读） | 转化 | 约 2 倍 | CONFIRMED（注） | Amazon 卖家资料，2022 年数据 | https://sellercentral.amazon.com/seller-forums/discussions/t/6e3086f7-9c18-4d73-9a9c-4b66f89b5573 |
| Web 3D | CrazyGames（缺失） | 用户 / 融资 | 表里没有 | 缺失（可选） | 月用户 3100 万–6000 万（两处说法冲突）；Smartfin 投资超 €1000 万（2025 年底） | https://en.wikipedia.org/wiki/CrazyGames |
| Industrial 3D | Epic | 持股 | 腾讯持股 28% | CONFIRMED | Wikipedia 信息框 | https://en.wikipedia.org/wiki/Epic_Games |
| Industrial 3D | Unity | 营收 | 2025 年 18.5 亿美元（10-K） | CONFIRMED | $1,849.6M | https://www.sec.gov/Archives/edgar/data/1810806/000181080626000011/unity-20251231.htm |
| Industrial 3D | Unity 中国 团结引擎 | 估值 | 10 亿美元 | CONFIRMED（注） | 36Kr Japan（2024）写 $1B；2026-03 有消息称 Unity 拟以超 $10 亿出售 Unity 中国（匿名信源） | https://36kr.jp/287636/ |
| Industrial 3D | Applied Intuition | 营收 / 估值 | 约 8.3 亿美元/年（估算）；150 亿美元 | CONFIRMED | Sacra 估算 2025 年 ARR；$15B 来自 2025-06 F 轮 | https://sacra.com/research/applied-intuition-at-830m-year/ |
| Industrial 3D | 光轮智能 | 订单 / 融资 | 2026Q1 新签 5.5 亿元（自报）；融资超 20 亿元 | CONFIRMED | 2026 上半年三轮合计超 20 亿元；估值未披露 | https://autonews.gasgoo.com/articles/market-industry/2069795751096725504 |
| Industrial 3D | 群核科技 | 营收 | 2025 年 8.2 亿元，毛利 82% | CONFIRMED（注） | ¥820M，毛利率 82.2%；格子里没有标签和链接（属财报） | https://wallstreetcn.com/articles/3769573 |
| Industrial 3D | 51WORLD | 营收 | 2024 年 2.87 亿元 | CONFIRMED / OUTDATED | 2024 年数字没错；已有更新数据：2026H1 约 1.24 亿元（+130%），但只来自搜索摘要。FY2025 全年数未查到。格子里也没有标签和链接 | https://thebambooworks.com/zh/tag/%e4%ba%94%e4%b8%80%e8%a6%96%e7%95%8c/ |
| Industrial 3D | Matterport / CoStar | 营收 / 收购价 | 10 个月贡献 1.47 亿美元（10-K）；16 亿美元收购 | CONFIRMED | 2025-02-28 交割至年底贡献 $147M；收购 EV 约 $1.6B | https://www.sec.gov/Archives/edgar/data/1057352/000105735226000020/csgp-20251231.htm |
| Industrial 3D | 爱奇艺 | 用量 | 虚拟制片项目同比 +50% | CONFIRMED | iQIYI 2025 年 | https://www.ithome.com/0/857/782.htm |
| Industrial 3D | Adam | 融资 | 种子轮 410 万美元 | CONFIRMED | $4.1M（2025-10-31，TQ Ventures） | https://adam.new/blog/seed |
| Industrial 3D | 群核（数据解读） | 增长 | 2026H1 收入只增 1.5% | CONFIRMED | ¥405M（+1.5%） | https://stock.10jqka.com.cn/20260907/c679671811.shtml |
| Industrial 3D | 团结引擎（数据解读） | 覆盖车型 | 77 款量产车型 | CONFIRMED | 2025-04 自报 | https://kr-asia.com/unity-china-steps-up-automotive-push-with-digital-twins-smart-cockpits-and-in-car-gaming |
| Industrial 3D | Bentley（缺失） | 营收 | 表里没有 | 缺失 | FY2025 $15.02 亿（+11%），西方孪生 / 基建软件头部（iTwin + Cesium） | https://finance.yahoo.com/news/bentley-systems-q4-earnings-call-170635732.html |
| Industrial 3D | 凡拓数创（缺失） | 营收 | 表里没有 | 缺失 | FY2025 营收 6.31 亿元（+73%），毛利约 23.5%，净亏 1.33 亿元；Overview 的毛利区间 20–50% 就是用它算的 | https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/301313/ctrl/2025/displaytype/4.phtml |
| Industrial 3D | Genesis AI（缺失，可选） | 融资 | 表里没有 | 缺失（可选） | 种子轮 $1.05 亿（2025 年中），做机器人合成数据 | https://techcrunch.com/2025/07/01/genesis-ai-launches-with-105m-seed-funding-from-eclipse-khosla-to-build-ai-models-for-robots |

## 国家标签与来源类型标签

- 国家标签：没发现错误。「数美万物 Hi3D（国内）」有个小风险：hitem3d.ai 的版权方是 Oceano HK Holding Limited，「Hitem3D = 数美万物」这一对应关系，两份笔记的说法互相矛盾
- 来源类型标签：
  - 拓竹「超 100 亿」应标「自报」，而且是预期性说法
  - Synthesia、群核、51WORLD、Game tab 的 Runway：格子里没有标签和链接
  - 可灵、MiniMax 标「财报」是对的：前者是 TechNode 转载的业绩公告，后者是公司 IR 页

