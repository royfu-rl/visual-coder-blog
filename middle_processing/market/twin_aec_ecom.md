# Commercial 3D: Digital Twins, Robotics Sim, AEC/Interior, E-commerce 3D/AR, Gaussian Splatting (国内+国外, as of Oct 2026)

Note on sourcing: about 15 searches/fetches. Several numbers come from secondary press (36氪/财联社/Bamboo Works/radiancefields). Primary filings (HKEX prospectuses, NVIDIA newsroom) were not fetched directly, and the Bamboo Works page returned 403. Claims that only come from press are marked as such.

## Q1. Digital twin / smart city / industry: stack, companies, market size

### Takeaway
There are two very different markets. In the West, the industrial digital twin is moving to NVIDIA Omniverse/OpenUSD libraries embedded in incumbent CAD/PLM stacks (Siemens, Cadence, Schneider), with Foxconn as the flagship. Geospatial work runs on Bentley+Cesium (3D Tiles). China's "数字孪生" is mostly government/park/city WebGL 可视化大屏 projects. It is small and fragmented: the IDC platform market was only ¥628M in 2024. 51WORLD is now HK-listed and is pivoting its story to "physical AI / synthetic data".

### Cited Findings
**NVIDIA Omniverse / Cosmos (West, industrial)**
- At GTC Washington DC (Oct 2025), the "Mega" Omniverse Blueprint was expanded to factory-scale digital twins. Siemens Digital Twin software was the first to support it, and FANUC and Foxconn Fii were the first to connect robot models. — [Barchart/NVIDIA release](https://www.barchart.com/story/news/35736078/nvidia-and-us-manufacturing-and-robotics-leaders-drive-americas-reindustrialization-with-physical-ai)
- Foxconn's Fii Omniverse Digital Twin (FODT) platform uses Omniverse libraries to build virtual replicas of its factories. It was used to design its 242,287 sq ft Houston AI-server plant, and NVIDIA reports CFD thermal simulation 150x faster via PhysicsNeMo. — [NVIDIA case study](https://www.nvidia.com/en-us/case-studies/foxconn-develops-physical-ai-enabled-smart-factories-with-digital-twins/)
- An Omniverse Blueprint for AI-factory (datacenter) digital twins covers layout, cooling and electrical design. Cadence and Schneider Electric were the first integrators. — [Digital Engineering 24/7](https://www.digitalengineering247.com/article/nvidia-expands-omniverse-with-generative-physical-ai/news)
- Automakers using Omniverse in parts of their workflows: BMW, Mercedes-Benz, Volvo, Toyota, GM, Lotus, Lucid. — [eWeek](https://www.eweek.com/news/nvidia-omniverse-gtc/)
- At GTC 2026 (March), ABB, FANUC and KUKA were reported as using NVIDIA digital twins and Jetson to optimize production lines. This comes from a single secondary source. — [ARC Advisory](https://www.arcweb.com/blog/nvidia-partners-us-manufacturing-leaders-drive-physical-ai); [The Energy Mag](https://www.theenergymag.com/news/market-news/nvidia-expands-physical-ai-ecosystem-with-new-models-and-industrial-partnerships)

**Bentley / Cesium (geospatial and infrastructure)**
- Bentley acquired Cesium on Sep 6, 2024; terms were undisclosed. Cesium ion reaches more than 1M active devices/month, and its open source has more than 10M downloads. 3D Tiles became an OGC community standard in 2019. — [Geo Week News](https://www.geoweeknews.com/news/bentley-systems-cesium-acquisition-geospatial-3d-itwin); [ENR](https://enr.com/articles/59240-bentley-buys-cesium-geospatial-information-and-digital-twin-platform)
- Google Photorealistic 3D Tiles are delivered in the 3D Tiles format. MicroStation 2025 can import any 3D Tiles content, including Google's. — [Geo Week News](https://www.geoweeknews.com/articles/bentley-cesium-acquistion-geospatial-3d-visualization-digital-twins/)
- Bentley FY2025 revenue was $1.502B (+11%), with 92% from subscriptions and FCF of $520M. 2026 guidance is $1.685–1.715B. iTwin is not broken out. — [Yahoo Finance Q4 call](https://finance.yahoo.com/news/bentley-systems-q4-earnings-call-170635732.html); [MarketBeat](https://www.marketbeat.com/instant-alerts/bentley-systems-q4-earnings-call-highlights-2026-02-26/?.tsrc=rss)

**China: 51WORLD 五一视界 (6651.HK), listed**
- Listed on HKEX Dec 30, 2025 at HK$30.5/share, raising about HK$730M. It opened at HK$35 (+14.8%). — [Bamboo Works](https://thebambooworks.com/?p=55928); [Techleap](https://finder.techleap.nl/news/feed/51world-surges-14-8-to-hk-35-in-hong-kong-ipo-debut)
- Prospectus figures via press: revenue was ¥126M / 170M / 256M / 287M for 2021–2024. Cumulative losses were about ¥505M, the 2024 net loss was ¥82M, and gross margin fell from 65.2% to 51.1%. It claims to be the largest digital-twin solution provider in China by 2024 revenue. — [DoNews](https://www.donews.com/news/detail/1/5479730.html); [Cnyes](https://hao.cnyes.com/post/222558)
- 1H2026 revenue was about ¥124M (+130% YoY), with the loss narrowing to ¥70.1M. The headline says "物理AI增五倍". This is from a search-result snippet; the page itself returned 403. — [Bamboo Works 中文](https://thebambooworks.com/zh/tag/%e4%ba%94%e4%b8%80%e8%a6%96%e7%95%8c/)
- Stack: the AES digital-twin platform, built on UE-based cloud rendering. It is positioned as a "空间智能" provider for 政企. — [Aliyun dev article](https://developer.aliyun.com/article/1741250)

**China: WebGL 大屏 vendors**
- 优锘科技 Uinnova (ThingJS): ¥180M B+ in 2020 (宽带资本, 晨山), with Jack Ma–linked backing. A later C round of more than ¥300M (2022-06) is reported by an aggregator. — [36氪](https://www.36kr.com/p/795095271395080); [KrASIA](https://kr-asia.com/china-brief-jack-ma-backed-software-company-uinnova-closes-usd-25-6-million-series-b-round)
- 图扑 Hightopo (HT for Web): FY2021 revenue about ¥53.4M (Craft estimate); no funding was found. — [Craft](https://craft.co/hightopo)
- 数字冰雹 Digital Hail: angel 2015, A 2019-07, A+ 2019-12, amounts undisclosed. — [36氪 pitchhub](https://pitchhub.36kr.com/project/1678464392524807)
- 易知微 EasyV: products are the EasyTwin rendering engine (2022, low-code) and the EasyV visualization builder. The tech mixes WebGL, game engine, GIS, BIM and CIM. Verticals are 文旅, 水利, 医疗, 园区, 工厂. No revenue or funding was found. — [itbear](https://www.itbear.com.cn/html/2023-04/453224.html); [Bilibili demos](https://www.bilibili.com/opus/1149415892214349827)
- Common web stacks in China are Three.js, Babylon.js and Cesium.js, with Cesium preferred for GIS/city-scale 3D Tiles. — [Aliyun dev](https://developer.aliyun.com/article/1718826)

**Market size (definitions differ widely)**
- IDC: China's 数字孪生平台 market was ¥628M in 2024 (report published Aug 2025). — [IDC press](https://www.idc.com/resource-center/press-releases/%e4%bb%8e%e8%a7%84%e6%a8%a1%e6%89%a9%e5%bc%a0%e5%88%b0%e4%bb%b7%e5%80%bc%e6%b7%b1%e8%80%95%ef%bc%8cidc-2024%e5%b9%b4%e6%95%b0%e5%ad%97%e5%ad%aa%e7%94%9f%e6%8a%a5/)
- IDC (via 前瞻): the China digital-twin *solution* market was ¥2.5B in 2023, and it is fragmented. The top 3 are 吉奥时空 10.8%, 超图 10.7% and 奥格 9.9%. — [前瞻](https://www.qianzhan.com/analyst/detail/220/250311-82790832.html)
- 前瞻's own figures conflict: one says more than ¥18.8B for 2024 and another says ¥3.5B. — [前瞻 bg](https://bg.qianzhan.com/trends/detail/506/250325-ac84396b.html)

### Inferences
- In China, paid demand is project-based G2B/G2G (smart city, 水利, 园区, 应急), delivered as WebGL/UE 大屏. Margins are falling (51WORLD gross margin 65%→51%) and cash burn is chronic. This looks like a services business more than SaaS.
- In the West, value accrues to incumbents (Siemens, Bentley, Cadence) that embed Omniverse/Cesium. NVIDIA monetizes GPUs and enterprise licenses rather than twin projects.
- Both 51WORLD and 群核 are re-labeling twin/scene assets as "physical AI / embodied synthetic data". This narrative pivot is a common pattern in 2026.

### Gaps
- No primary NVIDIA GTC 2026 press release was retrieved, and "Cosmos 3" is unverified. Omniverse revenue is not disclosed.
- There is no Gartner/IDC 2025 global digital-twin figure from a primary source.
- 易知微 and 数字冰雹 revenue are unknown, and 51WORLD's 1H2026 segment split was not retrieved.

## Q2. Robotics / embodied simulation and synthetic data

### Takeaway
Simulation-for-robot-data is the fastest-growing narrative, but revenue is still tiny outside NVIDIA's ecosystem. Isaac Sim/Lab plus Cosmos is the de facto Western stack, now with 3DGS-based NuRec at GA. Genesis raised a $105M seed. 群核 SpatialVerse made only ¥5.2M in 2025 from 16 customers, though its named customers include 智元, 银河通用 and 字节.

### Cited Findings
- GTC 2026 (March) brought new Isaac simulation frameworks plus new Cosmos and Isaac GR00T open models. — [Robotics 24/7](https://www.robotics247.com/article/nvidia-gtc-2026-nvidia-global-robotics-leaders-look-to-take-physical-ai-to-the-real-world)
- Also at GTC 2026 (secondary source): a Physical AI Data Factory Blueprint (Cosmos + OSMO) that expands one real scenario into thousands of synthetic variants. Omniverse NuRec reached GA, turning sensor scans into interactive 3D Gaussian-splat simulations. Isaac Teleop reached GA, and Isaac Lab 3.0 was announced. — [Blockchain.News](https://blockchain.news/news/nvidia-isaac-gr00t-robotics-platform-gtc-2026)
- Named industry builders on NVIDIA's robotics platform: ABB, AGIBOT, Agility, FANUC, Figure, Hexagon Robotics, KUKA, Skild AI, Universal Robots, World Labs, YASKAWA. — [Robotics 24/7](https://www.robotics247.com/article/nvidia-gtc-2026-nvidia-global-robotics-leaders-look-to-take-physical-ai-to-the-real-world)
- Cosmos world foundation models plug into Isaac Sim synthetic-data pipelines to narrow the sim-to-real gap. — [NVIDIA blog](https://blogs.nvidia.com/blog/scaling-physical-ai-omniverse)
- A claimed Gartner projection says synthetic data is about 20% of edge-AI training data today and will reach 90% by 2030. It is unverified and has no primary source. — [Blockchain.News](https://blockchain.news/news/nvidia-isaac-gr00t-robotics-platform-gtc-2026)
- Genesis AI: a $105M seed (Eclipse, Khosla; with Bpifrance, Eric Schmidt, Xavier Niel) in mid-2025. Its in-house physics engine (from the academic Genesis project across 18 universities) generates synthetic data. It plans to open-source parts. — [TechCrunch](https://techcrunch.com/2025/07/01/genesis-ai-launches-with-105m-seed-funding-from-eclipse-khosla-to-build-ai-models-for-robots); [Sifted](https://sifted.eu/articles/genesis-ai-105m-round)
- 群核 SpatialVerse launched Nov 2024 as interactive, material-accurate synthetic 3D data for robot grasp training. — [36氪](https://www.36kr.com/p/3045483903601545)
  - Prospectus via press: 16 customers and ¥5.2M revenue in 2025.
  - Partners: 智元, 银河通用, 穹彻, 智平方, 松应; 2026 coverage adds 字节 and 禾赛.
  - The company says 1H2026 orders already exceeded all of FY2025 (company claim).
  - Open models: SpatialLM (spatial language model) and SpatialGen.
  - Sources — [QbitAI](https://www.qbitai.com/2026/07/441237.html); [中证网](https://www.cs.com.cn/./ssgs/gsxw/202512/t20251223_6529615.html)
- Niantic Spatial launched a "Places Library": 100 real-world environments as USDZ (Gaussian splat + collision mesh) for Isaac Sim, dated Oct 4, 2026. — [Radiance Fields](https://radiancefields.com/niantic-spatial-bets-big-on-scaniverse-and-gaussian-splatting)
- Parallel Domain (synthetic data for AV/CV) raised an $11M Series A (2020) and a $30M Series B (March Capital). No acquisition was found. — [VentureBeat](https://venturebeat.com/ai/parallel-domain-raises-11-million-to-generate-synthetic-data-for-ai-model-training); [PD blog](https://paralleldomain.com/announcing-our-series-a-to-accelerate-computer-vision-development/)

### Inferences
- The paying buyers for sim data are well-funded humanoid/manipulation labs and AV companies. Asset libraries (群核's interior scenes, Niantic's real-place splats) are becoming the product, sold into the Isaac/USD ecosystem.
- Gaussian splatting is becoming a sim input format (NuRec, Niantic USDZ). Real-to-sim capture is converging with the AEC/real-estate capture market.

### Gaps
- No Scale AI physical-AI or synthetic data revenue was found. No Infinigen commercialization data was found (it is an academic open-source project). No market-size figure for robotics synthetic data was found from a primary analyst.

## Q3. AEC / interior design / real-estate 3D

### Takeaway
群核科技 (酷家乐/Coohom) IPO'd in HK in April 2026 and is the clearest public comp. It is profitable but growing slowly (~¥820M FY2025, +1.5% in 1H26), with AI products growing fast. In the West, Matterport now sits inside CoStar ($1.6B deal). Gaussian-splat exterior tours went mainstream via Zillow SkyTour.

### Cited Findings
**群核科技 (00068.HK)**
- Listed Apr 17, 2026 at HK$7.62, raising about HK$1.224B gross. It is the first of the "杭州六小龙" to IPO and calls itself "全球空间智能第一股". It later fell below the offer price, then jumped 29.9% on inclusion in 港股通 (Sep 7). Press reports a price of about HK$18.3 and market cap above HK$30B at one point. — [财联社](https://www.cls.cn/detail/2328214); [同花顺](https://stock.10jqka.com.cn/20260907/c679648252.shtml); [IT之家](https://www.ithome.com/0/940/178.htm)
- FY2025 revenue was about ¥820M, with adjusted net profit of ¥57.1M (its first profit). 1H2026 revenue was ¥405M (+1.5%), adjusted net profit ¥55.4M (+211%), and AI new products grew more than 177%. Space-design subscriptions remain the core revenue. — [华尔街见闻](https://wallstreetcn.com/articles/3769573); [同花顺](https://stock.10jqka.com.cn/20260907/c679671811.shtml)

**三维家 AiHouse (custom furniture design-to-manufacturing)**
- A Series D of several hundred million ¥ in 2023 (国科投资, 汇川科技), with a post-money valuation near $600M. A ¥500M Series C in 2019 was led by Alibaba. The company reports more than 4,000 factory users and more than 1M designers (company-reported, dated). — [EqualOcean](https://equalocean.com/news/2023062819826-aihouse-is-completing-hundreds-mn-cny-series-d-financing); [投资界](https://news.pedaily.cn/202306/515822.shtml)

**Matterport / CoStar**
- CoStar agreed in April 2024 to buy Matterport for about $1.6B EV ($2.75 cash + $2.75 stock per share). The deal closed ahead of schedule, and Matterport is reported within CoStar's "Other CRE" segment. Revenue comes from hosting subscriptions plus capture services and cameras. — [CoStar FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1057352/000105735226000020/csgp-20251231.htm); [RISMedia](https://www.rismedia.com/2024/04/22/costar-drops-1-billion-acquire-3d-camera-pioneer-matterport/)
- Benchmark: Apartments.com had more than 7.4M Matterport tour views in March 2024, and users spent 20% more time on listings with tours. — [TipRanks/press release](https://www.tipranks.com/news/press-releases/matterport-the-global-leader-in-3d-digital-twins-to-be-acquired-by-costar-group)

**Zillow SkyTour (Gaussian splatting in real estate)**
- Launched July 2025. It turns drone footage into an interactive exterior 3DGS tour on Showcase listings and is sold via the Zillow Media Experts premium package. — [Zillow Group](https://www.zillowgroup.com/news/take-home-listings-to-new-heights-with-skytour); [GeekWire](https://www.geekwire.com/2025/zillow-uses-drone-imagery-for-new-exterior-3d-tour-feature/); [Inman](https://www.inman.com/2025/11/25/zillows-skytour-uses-complex-3d-tech-to-simplify-home-search/)

**Consumer/AI interior tools**
- Planner 5D claims more than 100M users and 540M projects (company claim; earlier claims were 40M and 74M). — [Planner 5D](https://planner5d.com/reviews); [MarTech Series](https://martechseries.com/predictive-ai/augmented-reality/ai-powered-interior-design-tool-planner-5d-hits-40-million-users/)
- Interior AI (Pieter Levels) had an estimated ~$600K revenue in 2023 with no outside funding (GetLatka estimate). — [GetLatka](https://getlatka.com/companies/InteriorAI)

### Inferences
- What pays in AEC/interior: SaaS seats for designers and 家居 brands (酷家乐, 三维家, which close the loop to factory CNC), listing-media upsells (Matterport, SkyTour), and infrastructure engineering subscriptions (Bentley).
- 群核's flat top line plus fast-growing AI products suggests the classic seat market is saturated. Growth now comes from AI rendering/generation and from SpatialVerse data.

### Gaps
- Spacely AI financials were not found. The 三维家 2025 figures were not found. Matterport standalone revenue after the acquisition is not disclosed.

## Q4. E-commerce / retail 3D & AR, with measured conversion uplift

### Takeaway
Measured uplift figures exist, but almost all are vendor- or platform-reported case studies, not controlled studies. The often-quoted "94% higher conversion with 3D (Shopify)" could not be traced to any Shopify publication. Amazon's own seller material is the strongest first-party source. China's figures are engagement-style (visits, % of users helped), not conversion.

### Cited Findings
- Amazon (seller materials): a 2x purchase-conversion improvement on average in 2022 when customers click AR Virtual Try-On or View in 3D. A 9% average sales improvement when "View in Your Room" is enabled (2023 Amazon study). — [Amazon Seller Forums](https://sellercentral.amazon.com/seller-forums/discussions/t/6e3086f7-9c18-4d73-9a9c-4b66f89b5573); [CGIFurniture summary](https://cgifurniture.com/blog/amazon-glb-model/)
- Shopify Gunner Kennels case: after adding native 3D/AR, cart conversion rose +3%, order conversion +40%, and returns fell 5%. — [Shopify case study](https://www.shopify.com/case-studies/gunner-kennels)
- Rebecca Minkoff (via the Shopify Partners blog): shoppers who interacted with 3D were 44% more likely to add to cart and 27% more likely to order. AR users were 65% more likely to buy. — [Shopify Partners](https://www.shopify.com/ng/partners/blog/ar-ecommerce)
- The "94% higher conversion with 3D (Shopify)" figure appears only on an uncited German blog. — [Xictron](https://www.xictron.com/de/blog/augmented-reality-online-shop-ar-commerce-2026/)
- IKEA Kreativ (June 2022) is built on Geomagical Labs, which Ingka acquired in April 2020. It scans the user's room, erases existing furniture and places IKEA products photorealistically. — [IKEA newsroom](https://ikea.com/us/en/newsroom/corporate-news/ikea-launches-new-ai-powered-digital-experience-empowering-customers-to-create-lifelike-room-designs-pub58c94890); [TechCrunch](https://techcrunch.com/?p=2340297)
- Hexa (Israel; AI 2D→3D product assets) raised a $20.5M Series A in 2023 (Point72 Ventures, HTC and others), about $27.2M total. — [TechCrunch](https://techcrunch.com/2023/03/02/hexa-raises-20-5m-to-turn-images-into-3d-objects-for-vr-ar-and-more); [Globes](https://en.globes.co.il/en/article-israeli-3d-asset-visualization-co-hexa-raises-205m-1001439867)
- VNTANA (3D content management for e-commerce) is backed by Mark Cuban and a former Oculus CEO. — [TechCrunch](https://techcrunch.com/2021/11/04/mark-cuban-and-former-oculus-ceo-back-3d-e-commerce-startup-vntana)
- Threekit (product visualization/configurator) raised C$43.6M. — [BetaKit](https://betakit.com/ottawa-founded-threekit-raises-43-6-million-cad-to-bolster-product-visualization-tech/)
- No VNTANA–Threekit deal was found.
- 天猫 3D 家装城 (100 floors, tech from 每平每屋) drew more than 60M 云逛街 visits during Double 11 2020. No conversion rate was disclosed. — [投资界](https://news.pedaily.cn/20210331/13478.shtml)
- 得物 AR: AR virtual try-on "每天帮助超过30%的用户进行消费决策" (2021–22). Later wording is "每天帮助近千万用户", covering AR try-on, makeup, watches and 3D space. At the 2024 进博会, 70,000 watch models were available for 云试戴. — [界面](https://m.jiemian.com/article/13999315.html); [中新网](https://www.chinanews.com/cj/2024/11-08/10315641.shtml)

### Inferences
- What pays is asset production (2D→3D, configurators) for furniture, footwear and luxury, plus the platforms' own AR features that raise conversion and cut returns. The bottleneck is cheap 3D asset creation, which is where AI 3D generation and 3DGS compete.
- Uplift claims should be presented as ranges from case studies: low single digits up to roughly 2x among engaged users. Selection bias is a concern, since engagers are already high-intent.

### Gaps
- No Snap AR commerce revenue figures were retrieved. There is no CGTrader financial data and no 淘宝 3D conversion rate.

## Q5. Gaussian splatting commercialization

### Takeaway
3DGS has moved from research to shipped features in 2025–26: Zillow SkyTour, NVIDIA NuRec GA, Cesium/Babylon/PlayCanvas support, and the Khronos glTF extension as a release candidate. Pure-play capture companies are small, though: Polycam has raised $22.1M, and Luma has pivoted to video generation. Niantic Spatial ($250M capitalization) is the largest dedicated bet.

### Cited Findings
- As of July 2026, 212 3DGS platforms/tools are tracked: 43 capture studios and 38 cloud services. By industry tag: AEC 24, GIS 25, e-commerce 11, hospitality 9, simulation 8.
  - 13 companies have disclosed more than $1.5B in total funding. Dedicated spatial/reconstruction startups account for about $480M.
  - Selected totals: Niantic Spatial $250M, World Labs $100M+, Luma $68.5M, Polycam $22.1M, SpAItial $13M.
  - 415 open job listings.
  - Source — [Radiance Fields stats](https://radiancefields.com/gaussian-splatting-statistics)
- Niantic Spatial was spun out in May 2025 when the games business went to Scopely. It was capitalized with $250M ($200M from Niantic, $50M from Scopely) and kept Scaniverse. Inhi Cho Suh became CEO in March 2026. — [Radiance Fields](https://radiancefields.com/niantic-spatial-bets-big-on-scaniverse-and-gaussian-splatting)
- Khronos released the KHR_gaussian_splatting glTF extension as a release candidate on Feb 3, 2026. It was not found ratified as of the search. CesiumJS/Cesium for Unreal shipped support in March 2026, followed by Babylon.js and PlayCanvas. — [Khronos](https://www.khronos.org/news/press/gltf-gaussian-splatting-press-release); [Digital Production](https://digitalproduction.com/2026/02/04/gltf-learns-to-splat-without-losing-the-plot/)
- Polycam has offered 3DGS since Sept 2023, alongside LiDAR and photogrammetry, with a free tier plus Pro. — [Radiance Fields](https://radiancefields.com/polycam-gaussian-splatting-out-of-beta)
- Luma AI's flagship is now Dream Machine (video), and capture users are seeking alternatives (commentary). — [Radiance Fields](https://radiancefields.com/luma-ai-alternatives)
- Teleport by Varjo captures phone/drone footage into 3DGS for VR and real-estate tours. It launched at $30/month, with enterprise API tiers. — [Mixed News](https://mixed-news.com/en/varjo-teleport-launch/); [Teleport](https://teleport.varjo.com/help/en_US/what-is-teleport)
- KIRI Engine (China-origin team) 4.2 ships "3DGS to Mesh 3.0" (about 20% faster) and a 3DGS Render 5.0 Blender add-on with 4DGS. — [RenderHub](https://www.renderhub.com/3d/news-260416); [Radiance Fields](https://radiancefields.com/kiri-engine-ships-3dgs-render-5.0-for-blender)
- NVIDIA Omniverse NuRec (3DGS from sensor data, for robot/AV testing) reached GA at GTC 2026 (secondary source). — [Blockchain.News](https://blockchain.news/news/nvidia-isaac-gr00t-robotics-platform-gtc-2026)

### Inferences
- 3DGS monetizes through distribution owners (Zillow listings, NVIDIA sim, Cesium geospatial) more than through standalone capture apps. Standardization in glTF and USDZ is the enabler.
- The 3DGS-to-mesh tools (KIRI) and splat+collision-mesh packaging (Niantic) show that downstream buyers still need meshes for physics, games and e-commerce AR.

### Gaps
- 像衍科技 and Chinese 3DGS startups: no information found. 智谱 3DGS: nothing found.
- No user/revenue figures exist for Polycam, Scaniverse or Teleport.

