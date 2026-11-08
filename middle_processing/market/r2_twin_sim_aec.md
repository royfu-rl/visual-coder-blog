# Round 2: Digital Twins, Robotics/AV Simulation & Synthetic Data, 3DGS Commercialization, AEC/Interior 3D (国内+国外), as of 2026-10-13

This round fills the gaps left by `twin_aec_ecom.md` and avoids repeating it.

**Source-type tags.** Every number below carries one of these tags:
- **[P]** primary: a filing, a vendor's own newsroom, or a price page.
- **[CO]** company claim, as quoted in press.
- **[PR]** press report.
- **[EST]** third-party estimate or aggregator.

**Method note.**
- I made 10 WebSearch calls before the shared session search budget ran out. After that I made about 65 WebFetch calls to known primary URLs (newsroom, SEC, price pages, HF, Sina financial statements), for about 75 calls in total.
- With search unavailable, several items could not be found: 像衍, 中标公告 examples, Bentley iTwin pricing, and 群核 prospectus MAU/ARPU. They are listed under Gaps.

---

## Q1. Robotics/AV simulation and synthetic-data vendors: revenue, valuation, contracts, NVIDIA stack

### Takeaway
- **Applied Intuition is the one at-scale business.** It has about $800–830M of 2025 revenue/ARR at about 80% gross margin and a $15B valuation, and less than half of that revenue is now simulation.
- **Pure-play synthetic-data vendors are small.** Parallel Domain, Cognata, Bifrost and Duality have each raised $8–30M, and none has a reported round in 2025–26.
- **China's 光轮智能 (Lightwheel) is the breakout.** It raised more than ¥2B in 1H2026 and reports ¥550M of new orders in Q1 2026 alone. That dwarfs 群核 SpatialVerse (¥6.8M of orders in 1H2026) and 51WORLD's 51Sim (¥28.7M contract backlog).
- **NVIDIA's March 16, 2026 GTC releases make Omniverse/Isaac/Cosmos the default substrate.** The robot OEMs, ABB, FANUC, KUKA and YASKAWA, embed it for virtual commissioning.

### Cited Findings
**Applied Intuition (US)**
- 2025 ARR was about $830M, up 2x from $415M in 2024, with about 80% gross margin [EST]. — [Sacra, May 2026](https://sacra.com/research/applied-intuition-at-830m-year/)
  - Valuation was $15B at the June 2025 Series F ($600M, co-led by BlackRock funds and Kleiner Perkins), about 18x forward revenue.
  - Sacra's page also shows a $622M ARR / 24x figure that it does not reconcile.
- Forbes, via an aggregator, reports about $800M of 2025 revenue at more than 80% gross margin [PR]. The Information reported about $400M ARR in 2024 [PR]. — [Texxr summary](https://texxr.com/entity/applied-intuition)
- Mix and customers [EST]. — [Sacra](https://sacra.com/research/applied-intuition-at-830m-year/)
  - Automotive sim/testing is about 33% of revenue. Defense is the largest new line, and trucking, mining, ag, construction and ports are also verticals.
  - Its sim sells to 18 of the top 20 automakers (Toyota, VW, Hyundai, Stellantis, GM).
  - Its largest Vehicle OS deal is with Stellantis (Oct 2025). Other customers are TRATON (Scania/MAN), Komatsu, US Army, USAF, HII and Northrop.
  - It acquired Reblika (AI 3D pedestrians) in July 2025 and announced an NVIDIA Cosmos partnership in March 2026.
- No 2026 priced round was found. Dealroom's "$10–50B" range is uninformative [EST]. — [Dealroom](https://dealroom.co/companies/applied-intuition/)

**Western pure-play sim / synthetic-data vendors (all [EST] unless noted)**
- **Foretellix (AV verification):**
  - Series C first close: $43M (May 2023), led by 83North, with Woven Capital and NVIDIA. — [Pulse 2.0](https://pulse2.com/foretellix-43-million-funding/)
  - Final Series C reported at $85M, $135M total; new investors include Temasek and Isuzu [CO via LinkedIn]. — [LinkedIn](https://il.linkedin.com/in/doron-ilan-9a89b355)
  - Foretify was integrated with NVIDIA DRIVE AV in Oct 2025 (a partnership, not funding). — [startupim](https://slimpages.startupim.com/company_page/foretellix)
  - Foretellix is named as an early Cosmos adopter [P]. — [NVIDIA newsroom, Mar 18 2025](https://nvidianews.nvidia.com/news/nvidia-announces-major-release-of-cosmos-world-foundation-models-and-physical-ai-data-tools)
- **Parallel Domain:** last round was a ~$30M Series B (Nov 2022; investors include Toyota Ventures, Costanoa, Foundry). — [VCBacked](https://www.vcbacked.co/company/parallel-domain)
  - No 2025–26 funding or acquisition was found.
  - It is named as a Cosmos user [P]. — [NVIDIA newsroom](https://nvidianews.nvidia.com/news/nvidia-announces-major-release-of-cosmos-world-foundation-models-and-physical-ai-data-tools)
- **Cognata (Israel):** $18.5M Series B (2018), with $23.5–27.8M total depending on source. There is no 2025 round. ECARX selected it as a sim partner (2021). — [Calcalist](https://www.calcalistech.com/ctech/articles/0%2C7340%2CL-3747865%2C00.html); [AV International](https://www.autonomousvehicleinternational.com/news/simulation-software/cognata-to-provide-ecarx-with-autonomous-driving-simulation-software.html)
- **Bifrost AI:** $8M Series A (Oct 30–31, 2024), led by Carbide Ventures, with Airbus Ventures, Peak XV Surge, Wavemaker and Techstars. Totals are reported between $7.9M and $13.7M. Targets: aerospace, maritime, defense. — [Kyodo/PR Newswire](https://kyodonewsprwire.jp/release/202411019210); [Salestools](https://salestools.io/en/report/bifrost-ai-raises-8-million-series-a-october-2024)
- **Duality AI (Falcon):** funding conflicts. Caplight says $15.22M total, with the latest a June 2024 grant; CB Insights says $120K.
  - Customers are defense: US Army (XM30 counter-UAS synthetic data) and the DARPA ASIMOV program with CoVar (May 2025).
  - Sources — [Caplight](https://www.caplight.com/company/duality); [CB Insights](https://www.cbinsights.com/company/duality/financials); [BusinessWire May 2025](https://www.businesswire.com/news/home/20250519561860/en)
- **Hillbot (San Diego, robot sim + generative assets):** PitchBook lists $82.5M on May 7, 2025, with 28 employees. CB Insights calls it a seed with no amount. Treat as unconfirmed. — [PitchBook](https://pitchbook.com/profiles/company/601892-11); [CB Insights](https://www.cbinsights.com/company/hillbot/financials)
- **Genesis AI:** genesis-ai.company now redirects to genesis.ai.
  - The site is a waitlist page for a product called "Eno" (Commercial/Home), with "targeted customer deployments by end of 2026". The legal entity is Genesis AI SAS (France) [P].
  - No data-strategy statement is on the site. The $105M seed is in round 1.
  - Source — [genesis.ai](https://www.genesis.ai/)

**Data strategies of robot-foundation-model labs (relevant to whether sim vendors get paid)**
- **Skild AI** pre-trains on "large-scale simulation" plus internet/human video. It uses "targeted real-world data" only for customer post-training and calls real data "slow and prohibitively expensive" (blog, Jul 29 2025) [P]. — [Skild blog](https://www.skild.ai/blogs/building-the-general-purpose-robotic-brain)
  - The homepage now leads with "learns by watching human videos". Investor logos include SoftBank, Sequoia, Coatue, Amazon, Bezos and Lightspeed [P]. — [skild.ai](https://www.skild.ai/)
- **Physical Intelligence** is a named customer and "deep technical partner" of Scale's Physical AI Data Engine. That engine is real-world teleop/egocentric collection, and the page does not mention simulation.
  - Scale claims "1000+ hours of demonstration data collected... every day". Customers include PI, Generalist, Cobot and Dyna [P].
  - Source — [Scale Physical AI](https://www.scale.com/physical-ai)
- **NVIDIA GTC 2026:** Generalist AI is "exploring Cosmos for synthetic data generation", and FieldAI and Skild use Cosmos and Isaac [P]. — [NVIDIA newsroom Mar 16 2026](https://nvidianews.nvidia.com/news/nvidia-and-global-robotics-leaders-take-physical-ai-to-the-real-world)

**NVIDIA primary GTC 2026 sources (fills round-1 gap)**
- **Mar 16, 2026 robotics release [P]:**
  - Cosmos 3 is described as "the first world foundation model unifying synthetic world generation, vision reasoning and action simulation".
  - Isaac Lab 3.0 is in early access, built on Newton 1.0 + PhysX with multiphysics.
  - GR00T N1.7 is in early access *with commercial licensing*. GR00T N2 was previewed for year-end, with the claim that it succeeds more than 2x as often as leading VLAs on new tasks.
  - The Physical AI Data Factory Blueprint is being integrated by Microsoft Azure and Nebius.
  - The ABB/FANUC/YASKAWA/KUKA install base is "over 2 million robots", embedding Omniverse/Isaac virtual commissioning and Jetson.
  - NVIDIA counts about 2M robotics developers and more than 40K Inception members. Hugging Face (13M builders) is integrating Isaac and GR00T into LeRobot.
  - Lightwheel is co-developing and calibrating Newton with Samsung for cable-handling robots.
  - Source — [NVIDIA newsroom](https://nvidianews.nvidia.com/news/nvidia-and-global-robotics-leaders-take-physical-ai-to-the-real-world)
- **Mar 16, 2026 industrial software release [P]:**
  - Siemens launched "Digital Twin Composer" on Omniverse libraries; customers named are Foxconn, HD Hyundai, PepsiCo and KION.
  - PTC added an Onshape CAD → Isaac Sim / OpenUSD workflow (FANUC America, Fauna Robotics).
  - Dassault: 3DEXPERIENCE "Virtual Companions" agents.
  - Synopsys/Ansys: Fluent on GPU (Honda 34x).
  - Krones builds Omniverse digital twins of bottling lines on Azure.
  - KION + Accenture build warehouse twins for GXO forklifts.
  - Source — [NVIDIA IR](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-and-Global-Industrial-Software-Giants-Bring-Design-Engineering-and-Manufacturing-Into-the-AI-Era/default.aspx)
- **GTC 2026 live blog [P]:**
  - Alpamayo 1.5 is a reasoning VLA for AV. AlpaDreams does real-time multi-camera generative scene simulation. Fidler: "We have entered the era of generative simulation."
  - The robotaxi platform is attracting BYD, Hyundai, Nissan and Geely, with an Uber deployment partnership.
  - FieldAI uses Omniverse NuRec + Cosmos. UR's AI Trainer was built with Scale AI on Isaac Sim.
  - Healthcare: Open-H dataset (700–776 hours), Cosmos-H. PeritasAI is working with Lightwheel.
  - Source — [NVIDIA blog](https://blogs.nvidia.com/blog/gtc-2026-news/)
- **NuRec [P]:** Omniverse NuRec is "agent-friendly 3D Gaussian splatting libraries" that reconstruct camera/lidar data into OpenUSD scenes.
  - It runs on the open-source gsplat and integrates with Isaac Sim, AlpaSim and CARLA via gRPC. It adds Harmonizer (Cosmos-based) and Asset Harvester.
  - The NGC container is tagged "nre-ga". The page itself gives no GA date, which is consistent with the round-1 GA claim but does not date it.
  - Source — [NVIDIA developer](https://developer.nvidia.com/omniverse/nurec)
- **Earlier context (GTC Mar 18 2025) [P]:**
  - Cosmos early adopters: 1X, Agility, Figure, Foretellix, Skild, Uber. Also named: Parallel Domain, Nexar, Oxa, Linker Vision, Milestone, Waabi. — [NVIDIA newsroom](https://nvidianews.nvidia.com/news/nvidia-announces-major-release-of-cosmos-world-foundation-models-and-physical-ai-data-tools)
  - Omniverse adopters: Foxconn/Fii, GM, Hyundai, Mercedes-Benz, Pegatron, Schaeffler, Unilever. Integrators: Accenture, Ansys, Cadence, Databricks, Dematic, Hexagon, Intrinsic, KION, Omron, Rockwell, SAP, Schneider/ETAP, Siemens, Vertiv. — [NVIDIA newsroom](https://nvidianews.nvidia.com/news/nvidia-omniverse-physical-ai-operating-system-expands-to-more-industries-and-partners)
- **Omniverse Enterprise licensing:**
  - A search snippet said NVIDIA states "$4,500 per GPU per year". The current NVIDIA Omniverse Enterprise and free-trial pages I fetched show **no price**, only that production use requires an NVIDIA Enterprise Support entitlement [P]. — [NVIDIA free trial](https://www.nvidia.com/en-us/omniverse/enterprise/free-trial/); [NVIDIA AU](https://www.nvidia.com/en-au/omniverse/enterprise)
  - Reseller prices [EST]: UK about £4,809.49 per GPU per year (scan.co.uk; page 403'd on fetch, figure from snippet). An EU bundle of AI Enterprise + Omniverse is €5,800 per GPU per year, with an education example of €1,500.
  - Omniverse licensing is now merged with NVIDIA AI Enterprise. — [pi3g](https://pi3g.com/nvidia-ai-enterprise-subscription-cost-in-2026/)
  - **Treat $4,500/GPU/yr as the historical list price (2021–24 era), consistent with resellers, but not shown on NVIDIA's current page.**

**China embodied / AV simulation & synthetic data**
- **光轮智能 Lightwheel (founded 2023; CEO 谢晨, ex-NVIDIA/Cruise/NIO sim lead):**
  - Funding [PR]:
    - Mar 11 2026: Series A++/A+++ combined, ¥1B (新希望, 鼎邦/三安 family office, 奥克斯, 鼎石; 建投华科, 国方创新, 道禾, 清新). — [EqualOcean](https://www.equalocean.com/news/2026031121786-light-wheel-intelligence-raises-rmb-1b-build-physical-ai-infrastructure)
    - Late May 2026: a round led by 蚂蚁集团, amount undisclosed.
    - Jun 23 2026: a ¥1B strategic round (中关村科学城基金, 四川发展, 山东发展, 巨人网络, 宇信, 宝通, 中科产投; returning 建投, 三七互娱, 森马). — [瑞财经](https://m.rccaijing.com/news-7475022293489087978.html)
    - That is three rounds and more than ¥2B in 1H2026. — [Gasgoo](https://autonews.gasgoo.com/articles/market-industry/2069795751096725504)
  - It self-describes as "the world's first unicorn in embodied data" [CO].
  - Revenue/orders [CO]:
    - 2025 revenue grew 10x, and Q1 2026 revenue was expected to exceed all of FY2025. — [EqualOcean](https://www.equalocean.com/news/2026031121786-light-wheel-intelligence-raises-rmb-1b-build-physical-ai-infrastructure)
    - **Q1 2026 new orders were ¥550M.** — [Gasgoo](https://autonews.gasgoo.com/articles/market-industry/2069795751096725504)
    - It claims more than 80% of sim assets and synthetic data used by leading embodied teams globally come from Lightwheel [CO].
  - Unit economics claims [CO]:
    - Premium-scenario data resale rate is above 10x, and "one hour of standardized data can serve 10 clients".
    - Physical-AI data needs are "~1,000x autonomous driving".
  - Listed partners [CO]: NVIDIA, Google, Figure, 1X, ByteDance, Alibaba, AgiBot, Galbot, Toyota, Bosch, BYD, Geely. Gasgoo adds OpenAI and DeepMind.
  - 2026 alliances [CO]: 摩尔线程 (May), 生数 (Jun 15), 阿里云 (Jun 17), PICO human-data hardware (Jun 18), and JVs with 宝通 and 新希望.
  - Products [P]: SimReady Library, EgoSuite (egocentric human data), RoboFinals (VLA/world-model evaluation), Lightwheel-Platform Enterprise. It co-open-sourced Isaac Lab-Arena with NVIDIA. — [lightwheel.ai](https://www.lightwheel.ai/)
- **群核 SpatialVerse:**
  - 1H2026 SpatialVerse order value was ¥6.8M, already above FY2025 (whose revenue was ¥5.2M from 16 customers, round 1) [PR citing interim]. — [同花顺 Sep 7 2026](https://stock.10jqka.com.cn/20260907/c679671811.shtml)
  - New partners in Dec 2025: Motphys and 地瓜机器人 (Digital Origin). SpatialTwin (industrial twin for embodied AI, Nov 2025) partners are 杭叉 and 斯坦德.
  - One client reportedly trains on sim:real data at 9:1 [PR].
  - Source — [中证网 Dec 23 2025](https://www.cs.com.cn/./ssgs/gsxw/202512/t20251223_6529615.html)
  - InteriorGS open dataset [P]: 1,000 indoor scenes as 3DGS (.ply), with more than 554K object instances in 755 categories and floorplans/occupancy maps, 43.8GB, gated license. v1 (500 scenes) was released 2025-07-24 and v2 on 2025-08-01. — [Hugging Face](https://huggingface.co/datasets/spatialverse/InteriorGS)
  - SPEAR simulator has more than 14,000 Python APIs (with Intel). WalkerBench covers 161 cities, and the best model completes 24.5% of tasks. Partners: 字节, 智元, 银河通用, 禾赛, 穹彻, 智平方, 松应 [PR]. — [量子位 Jul 1 2026](https://www.qbitai.com/2026/07/441237.html)
- **51WORLD 51Sim** (prospectus via press) [PR]:
  - In-hand contracts as of Nov 30, 2025: 18 contracts worth ¥28.7M for 51Sim, out of 128 contracts worth ¥194M company-wide.
  - 51Aes (twin) has been more than 79% of revenue every period. — [Cnyes](https://hao.cnyes.com/post/222558)
- **银河通用 Galbot:** GraspVLA is pre-trained on **SynGrasp-1B**, "a billion-frame robotic grasping dataset generated in simulation".
  - It uses more than 10K Objaverse meshes in 240 categories, with BoDex grasps, cuRobo trajectories and photoreal domain randomization. Galbot is affiliation #1 [P].
  - The page gives no quantitative sim-to-real metric.
  - Source — [GraspVLA project page](https://pku-epic.github.io/GraspVLA-web/)
- **地瓜机器人 D-Robotics:** the English site shows only RDK compute boards (X3 5 TOPS, X5 10 TOPS, S100 80+ TOPS) and 200+ open algorithms. No sim/data platform, funding or shipment numbers are on the page [P]. — [d-robotics.cc](https://en.d-robotics.cc/)

### Inferences
- **Revenue concentration is extreme.** Applied Intuition (about $0.8B) plus NVIDIA's ecosystem capture most of the value.
- **The China sim-data market is bifurcating:**
  - Lightwheel sells *data + evaluation as a service* to model labs and OEMs at nine-figure-RMB order scale.
  - Asset-library spinoffs (群核 SpatialVerse, 51Sim) are at single- to low-double-digit ¥M.
  - Lightwheel's figures are company claims and are not audited.
- **Leading labs hedge.** Skild and Galbot lean on sim and synthetic data. PI and Generalist buy real teleop and egocentric data from Scale. That split defines the addressable market for sim vendors.
- **NVIDIA's model is platform/licensing plus GPUs.** GR00T N1.7 now carries a "commercial licensing" label, the first explicit commercial license flag on a GR00T release seen in primary sources. Pure-play vendors increasingly position as layers *on* Cosmos and Isaac.

### Gaps
- 腾讯 TAD Sim: the site was unreachable (proxy refused, Tencent Cloud page 404). No revenue or customer data.
- 百度 sim: nothing gathered.
- 51Sim customers by name: not found.
- Applied Intuition 2026 numbers and an official NVIDIA–Applied press release: not retrieved.
- Genesis AI, Hillbot and Bifrost revenue: none disclosed.
- Skild and PI 2026 valuations: not verified in this round, because search was exhausted.

---

## Q2. Digital twin: China vendor economics, contract sizes, Western platform pricing

### Takeaway
- **China's listed twin vendors are low-margin, loss-making project businesses.** 51WORLD's gross margin fell from 65% to 41% (1H25). 凡拓数创 (301313) runs at about 20–24% gross margin with ¥130–190M annual losses.
- **The average 51WORLD contract is about ¥1.5M**, and top-5 customers are about 50% of revenue.
- **Western geospatial-twin pricing is transparent and cheap at the entry level.** Cesium ion runs from $149 to $874 per month. The money is in incumbents' enterprise suites (Siemens Digital Twin Composer, Bentley).

### Cited Findings
**51WORLD (6651.HK), prospectus figures via press [PR]** — [Cnyes](https://hao.cnyes.com/post/222558)
- Revenue / gross margin / net loss:

  | Period | Revenue | Gross margin | Net loss |
  |---|---|---|---|
  | 2022 | ¥170M | 65% | −¥190M |
  | 2023 | ¥256M | 54.2% | −¥87M |
  | 2024 | ¥287M | 51.1% | −¥79M |
  | 1H2025 | ¥54M | 41.1% | −¥94M |

  - The 1H2025 revenue is highly seasonal, which matches round-1's 1H2026 figure of about ¥124M (+130%).
- Customer concentration:
  - Top-5 customer share rose from 23.6% (2022) to 38.3% (2023) to 46.4% (2024) to 51.5% (1H25).
  - 摩尔线程 was the largest customer in 2023 at 15.9% of revenue, and is also a shareholder.
  - "Customer C" overlaps with suppliers.
- **Contract size:** 128 in-hand contracts worth about ¥194M as of Nov 30 2025, about ¥1.5M on average.
  - 51Aes: 108 contracts, about ¥139M (about ¥1.3M average).
  - 51Sim: 18 contracts, about ¥28.7M (about ¥1.6M average).
  - 51Earth: 2 contracts, about ¥1M.
- Market cap at debut was about HK$15.35B, and net proceeds were about HK$653M (80% to R&D).
- The prospectus (CIC-style) puts the China digital-twin *solutions* market at ¥12.2B in 2024, with a 2020–24 CAGR of 31.6%. This is another definition that conflicts with IDC's ¥628M platform figure from round 1.
- Company site [CO]: more than 1,000 enterprise customers. Named projects include 国家会议中心二期, 北京CBD管委会, 华为园区 IOC 2.0, 中电建成都院 小浪底, 昆山交通发展集团, plus a South China airport, a coal mine and a water group.
  - Products: AES6 (twin base), WDP (developer platform, 300+ APIs), 51Sim, 51Earth. Solutions: CIM, WIM (water), GIM (geology/energy).
  - Source — [51aes.com](https://www.51aes.com/)

**凡拓数创 FTSC (301313.SZ), the listed 3D-visualization/twin integrator [P, financial statements]**
- FY2024: revenue ¥365.0M, operating cost ¥290.5M (≈**20.4% gross margin**), net loss −¥188.8M. — [Sina Finance](https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/301313/ctrl/2024/displaytype/4.phtml)
- FY2025: revenue ¥630.8M (+73% YoY), operating cost ¥482.7M (≈**23.5% gross margin**), net loss −¥132.6M (attributable −¥135.0M). — [Sina Finance](https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/301313/ctrl/2025/displaytype/4.phtml)
  - Gross margins are my calculation from the revenue and cost lines.

**Private WebGL/大屏 vendors (no new financials found)**
- 易知微 EasyV (Hangzhou) [P]:
  - Products: EasyV, EasyTwin engine, EasyModel (new), EasyHuman AI digital human (new). Services: twin project customization, page customization, 3D modeling.
  - SaaS tiers are 高级版, 尊享版, 孪生版 and 私有化部署, with no prices published.
  - Its customer, user and partner counters render blank. Named clients: 浙江大学, 青大附院, 中国燃气, 深圳国际, 中国十五冶. Xinchuang certifications include UOS, 麒麟 and 鲲鹏.
  - Source — [easyv.cloud](https://www.easyv.cloud/)
- 图扑 Hightopo [P]: HT for Web, a WebGL 2D/3D component library aimed at telecom topology and power/gas HMI/SCADA. No prices or customers are listed; it is trial on request. — [hightopo.com](https://www.hightopo.com/)

**Western twin platforms**
- **Cesium ion pricing [P]**:

  | Tier | Price | Storage | Streaming |
  |---|---|---|---|
  | Community | free, non-commercial | 10GB | 15GB/mo |
  | Commercial | $149/mo individual, $524/mo team of 5 | 100GB | 150GB/mo |
  | Premium | $499/mo individual, $874/mo team | 500GB | 500GB/mo |
  | Custom / Self-Hosted | contact sales | n/a | n/a |

  - A paid license is required for any government project or for orgs with revenue or funding above $50K. There is no limit on apps or end users.
  - Source — [cesium.com/pricing](https://cesium.com/pricing/)
- **Siemens Digital Twin Composer** (built on Omniverse libraries) launched at GTC 2026. Customers: Foxconn, HD Hyundai, PepsiCo, KION [P]. — [NVIDIA IR](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-and-Global-Industrial-Software-Giants-Bring-Design-Engineering-and-Manufacturing-Into-the-AI-Era/default.aspx)
- **Dassault 3DEXPERIENCE:** at GTC 2026 it announced "Virtual Companions" agents. No twin-specific numbers [P]. — same source.

### Inferences
- **China twin business model.** About ¥1–1.5M per project is the representative ticket for a listed vendor; small 大屏 jobs from WebGL vendors are presumably smaller. With concentrated customers and gross margins of 20–50%, this is systems integration, not software.
- **凡拓数创 is the low-margin end** (CG/exhibition-hall integration). 51WORLD's margin has slid toward the integrator level as it chases revenue.
- **The "physical AI / synthetic data" relabel is visible in contract data** but small: 51Sim is about 15% of 51WORLD's backlog.

### Gaps
- 中国政府采购网 中标公告 examples: not retrieved, because search was exhausted. Use 51WORLD's ¥1.3–1.6M average contract as a proxy.
- Revenues of 数字冰雹, 优锘, 图扑, 飞渡 and 易知微: still undisclosed (all private).
- 华晟经世: no information gathered.
- Bentley iTwin pricing, and a Siemens/Dassault twin revenue breakout: not found.
- 51WORLD 1H2026 segment split: not retrieved (Bamboo Works 403).

---

## Q3. AEC / interior 3D and AI rendering

### Takeaway
- **群核 is a high-margin (82.2%) but flat-growth subscription business.** 97% of revenue is software subscription, and AI products are only ¥31M in 1H2026, though growing 177%.
- **Matterport inside CoStar contributed $147M in its first ~10 months**, consistent with roughly a $170M run rate.
- **The AI-rendering long tail is a $29–$199/month SaaS market.** Interior AI, mnml, Veras (now under Chaos) and D5 (3M+ users) all sit there. Usage numbers are claims, and revenue is mostly undisclosed.

### Cited Findings
**群核科技 Manycore (00068.HK)**
- FY2025 [PR from prospectus/results]:
  - Revenue ¥820M, adjusted net profit ¥57.1M (first profit), **gross margin 82.2%**.
  - Overseas revenue +28% YoY. Cumulative R&D above ¥1B over 2023–25.
  - IPO: up to HK$1.227B at HK$7.62, cornerstones about HK$455M, sponsors JPM and CCB International.
  - Source — [华尔街见闻](https://wallstreetcn.com/articles/3769573)
- Day-one trade was HK$20.62 (+170% vs offer) intraday on Apr 17, 2026. Kujiale/Coohom serve 200+ countries and regions [PR]. — [IT之家](https://www.ithome.com/0/940/178.htm)
- 1H2026 [PR from interim]:
  - Revenue ¥405M (+1.5%), with software subscription at 97.1% of revenue. Adjusted net profit ¥55.42M (+210.9%).
  - **AI new apps/products revenue ¥31M (+177%).** AI design platform orders above ¥20M.
  - June MAU of the AI design platform was +50% vs Dec 2025. LuxReal (AI video, launched May) June revenue was +470% MoM.
  - Capex +124% for compute.
  - The platform holds more than 500M 3D design scenes and 480M 3D models (end-2025).
  - Source — [同花顺](https://stock.10jqka.com.cn/20260907/c679671811.shtml)
- New products: LuxReal (closed beta Dec 2025), the Aholo open platform (Dec 2025), and an overseas Kujiale AI version (Korea, Thailand, Europe; early Dec 2025) [PR]. — [中证网](https://www.cs.com.cn/./ssgs/gsxw/202512/t20251223_6529615.html)

**Matterport after CoStar [P, CoStar FY2025 10-K]**
- The deal closed **Feb 28, 2025**. The exchange ratio was 0.03552, set at the collar floor ($77.42 CoStar price).
- **Matterport contributed $147M revenue** from closing to year-end 2025.
- "Other CRE" segment revenue went from $77M (2024) to $216M (2025), +181%, now about 7% of CoStar revenue.
- Matterport added about $28M of equipment and capture-service costs.
- Homes.com's "Homes AI" uses Matterport digital-twin tech.
- Matterport and Domain were together under 10% of revenue and were excluded from ICFR.
- Source — [CoStar 10-K](https://www.sec.gov/Archives/edgar/data/1057352/000105735226000020/csgp-20251231.htm)
- matterport.com/pricing returns 404 and /plans shows no prices [P, observed 2026-10-13].

**AI interior/architecture tools, pricing and usage (company pages, observed Oct 2026)**
- **Interior AI (Pieter Levels) [P]:**
  - Pro $49/mo (1,000 designs), Premium $99/mo (5,000), Ultra $199/mo (25,000).
  - Yearly: $349, $599 or $1,199 per year.
  - It claims staged homes "sell 87% faster, 15% higher". No user or revenue count is on the page.
  - Source — [interiorai.com](https://interiorai.com/)
- **RoomGPT (open-source origin, Hassan El Mghari):** "Used by over 4 million people" [CO]. — [roomgpt.io](https://www.roomgpt.io/)
- **Spacely AI:**
  - Usage claims: "580,000+ users" and "440,000+ architects, interior designers, realtors" [CO].
  - Logos: Gensler, Perkins&Will, Corgan, Cooper Carry, Nelson.
  - Southeast-Asia signals: a Thai LinkedIn page, Thai language, and an Echelon SEA Top-10 award. 2nd runner-up at the SketchUp Innovation Challenge 2024. No funding is shown.
  - Source — [spacely.ai](https://www.spacely.ai/)
- **D5 Render (China-origin, GMT+8):**
  - "3M+ active professionals, 50K+ design firms". Pro from $38/mo; Community and Edu are free. #1 on G2 [CO].
  - Products: D5 Lite (AI plugin), D5 Works, D5 Arco (AI co-design, coming soon). Case studies: KPF, BIG, SWA.
  - Source — [d5render.com](https://www.d5render.com/)
- **Veras (EvolveLAB):** "now part of the Chaos ecosystem".
  - $59/mo, or $348/yr named; floating $612/yr; enterprise at 25 seats and up.
  - Host apps: SketchUp, Revit, Rhino, Forma, Archicad, Vectorworks [P].
  - Source — [evolvelab.io/veras](https://www.evolvelab.io/veras)
- **mnml.ai [P]:** Lite $29/mo, Plus $49/mo, Studio $119/mo. A one-time pack is $149 for 10K credits. — [mnml.ai/pricing](https://mnml.ai/pricing)
- **LookX AI:** web app plus SketchUp/Rhino plugins, custom model training, real-time and video generation. No prices, users or origin are stated on the homepage [P]. — [lookx.ai](https://www.lookx.ai/)

### Inferences
- **群核's margin structure is SaaS-like (82%) but flat.** AI is about 7.7% of 1H26 revenue (¥31M / ¥405M), so the "空间智能 / physical AI" valuation premium (a HK$20+ trade vs a HK$7.62 IPO) is narrative ahead of revenue.
- **Matterport's run rate implies little growth** relative to its pre-deal revenue of about $170M (my recollection of pre-acquisition 10-Ks, not re-verified here). CoStar uses it as a listing-media feature.
- **AI render tools converge on $29–$59/month entry pricing.** Distribution through BIM/CAD plugins and the Chaos/Enscape channel is the moat, not the model.

### Gaps
- 群核 prospectus MAU, paying customers, ARPU and Coohom overseas revenue share: not retrieved. The HKEX prospectus URL was unknown and search was exhausted.
- 三维家 and 打扮家 2025–26 figures: not found.
- Interior AI revenue: levelsio's public figure was not re-verified (round-1 GetLatka figure was about $600K in 2023).
- Planner 5D: nothing new.
- D5 funding: not found.
- CGarchitect survey: not fetched.

---

## Q4. Gaussian splatting commercialization: pricing and Chinese players

### Takeaway
- **3DGS has become product plumbing.** NuRec (NVIDIA), SPZ (Niantic, with a claimed 90% size reduction), InteriorGS (群核), SuperSplat 3.0 (PlayCanvas) and Zillow SkyTour all ship it.
- **Capture apps price at about $80 to $1,200 per year per user**, and enterprise tiers are quote-only.
- **Niantic Spatial has pivoted to enterprise.** scaniverse.com now redirects to its "Capture" product page, and target sectors are embodied AI, defense and oil & gas.

### Cited Findings
- **Niantic Spatial [P]:**
  - Products: Localize (VPS, "50M neural networks / 150T parameters"), Reconstruct (meshes + Gaussian splats; created the SPZ format), Understand, Capture.
  - Scale claims: 30B+ posed images and 140+ patents.
  - Named: Coco Robotics, ExxonMobil, Vantor, NVIDIA/Flexion (sim-to-real).
  - scaniverse.com 302-redirects to nianticspatial.com/products/capture. Scaniverse runs on iOS, Android and web, does on-device splat and mesh, and claims a 90% size reduction with SPZ.
  - Sources — [nianticspatial.com](https://www.nianticspatial.com/); [Capture page](https://www.nianticspatial.com/products/capture)
- **Polycam pricing [P]:**
  - Free; Basic $150/yr (or $30/mo); Business $400/user/yr; Enterprise $1,200/user/yr with a 3-user minimum.
  - "Pro" has been discontinued (now Legacy). It claims to be "trusted by half of the Fortune 500".
  - Source — [poly.cam/pricing](https://poly.cam/pricing)
- **Teleport by Varjo [P]:** Professional is pay-as-you-go "start with $30", priced by image count. Enterprise Cloud is per-seat annual or reserved capacity, and on-prem is one-time plus support; enterprise prices are unlisted. — [get.teleport.varjo.com/pricing](https://get.teleport.varjo.com/pricing)
- **KIRI Engine (KIRI Innovation) [P]:** Free (150 photos per scan); Pro $79.99/yr or $17.99/mo (500 photos). Logos: HBO, Ubisoft, Tesla, Sony. — [kiriengine.app/pricing](https://www.kiriengine.app/pricing)
- **Radiance Fields stats (updated Jul 9 2026) [EST]:** no Chinese 3DGS firm (像衍, 智谱, 群核, KIRI) appears in its funding table. Wayve ($1B+) and Pico ($62M) are listed alongside the round-1 names. — [radiancefields.com](https://radiancefields.com/gaussian-splatting-statistics)
- **群核 InteriorGS** (1,000 3DGS indoor scenes, 554K objects) is the most concrete Chinese 3DGS-as-data product found [P]. — [Hugging Face](https://huggingface.co/datasets/spatialverse/InteriorGS)

### Inferences
- **Standalone splat capture is a commoditizing prosumer tier**, priced under about $150 per year. Enterprise value accrues where splats feed localization (Niantic VPS) or simulation (NuRec, InteriorGS, Niantic USDZ Places).

### Gaps
- **像衍科技:** no information found. Search budget was exhausted and no URL was known. This remains an explicit gap.
- Teleport, Polycam and Scaniverse user or revenue figures: still undisclosed.
- Zillow SkyTour adoption numbers: zillow.com returned 403.

---

## Q5. Standout demo URLs (verified reachable 2026-10-13 via fetch unless noted)

### Takeaway
All URLs below returned content on fetch except Zillow (403, likely bot-blocking) and Tencent TAD Sim (unreachable).

### Cited Findings
- **SuperSplat** (PlayCanvas): browser 3DGS editor and gallery. The Editor 3.0 is on WebGPU, with "Walkable Worlds" and CC-licensed downloads; the largest scene listed has 2.72M splats. Live. — [superspl.at](https://superspl.at/)
- **InteriorGS** 3DGS indoor dataset viewer/download (gated). Live. — [huggingface.co/datasets/spatialverse/InteriorGS](https://huggingface.co/datasets/spatialverse/InteriorGS)
- **GraspVLA / SynGrasp-1B** project page with real-robot videos (Galbot). Live. — [pku-epic.github.io/GraspVLA-web](https://pku-epic.github.io/GraspVLA-web/)
- **NVIDIA Omniverse NuRec** developer page (3DGS to sim; Isaac/CARLA/AlpaSim). Live. — [developer.nvidia.com/omniverse/nurec](https://developer.nvidia.com/omniverse/nurec)
- **Niantic Spatial Capture**, the former Scaniverse. Live, redirected. — [nianticspatial.com/products/capture](https://www.nianticspatial.com/products/capture)
- **51WORLD AES / WDP** product site. Live. — [51aes.com](https://www.51aes.com/)
- **Zillow SkyTour** announcement: zillow.com/news returned 403 on fetch, and the zillowgroup.com URL redirects there. Not verified by fetch. — [zillow.com/news](https://www.zillow.com/news/take-home-listings-to-new-heights-with-skytour/)

### Inferences
- The best "visual" demos for a blog are SuperSplat (in-browser splats), NuRec (splat-to-sim) and InteriorGS (splat as training data). Together they show 3DGS used for viewing, for simulation and for data.

### Gaps
- No 国内 twin 大屏 demo URL was verified. 易知微 and 图扑 demos exist on their sites but were not individually fetched.

