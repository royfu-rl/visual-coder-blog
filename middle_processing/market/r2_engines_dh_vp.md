# Real-time engines beyond games: automotive HMI, virtual production, broadcast, digital humans, engine financials (round 2, as of 2026-10-13)

Method note
- About 100 calls: ~25 WebSearch and ~75 WebFetch. The shared session WebSearch budget (200 across all agents) ran out early. After that I mostly fetched primary pages directly: SEC EDGAR, Wikipedia (for reference URLs), vendor pages, and Chinese news. Many gaps below come from the missing search budget, not from evidence that the data doesn't exist.
- This file builds on `web3d_engines.md` (Q3 there) and doesn't repeat it. Already covered there: the UE $1,850/seat non-game subscription, Epic's "35 models / 2M+ cars", 51WORLD, TUDN MetaHumans, VP market-size estimates.
- Source-type tags:
  - **[filing]** = SEC/HKEX filing or earnings release
  - **[co]** = company page or press release
  - **[press]** = independent journalism
  - **[st-media]** = Chinese state or provincial media
  - **[analyst]** = market-research firm
  - **[wiki]** = Wikipedia, used only to find dates and reference URLs
  - **unverified** = item found only in a search snippet or secondary source
- unrealengine.com, epicgames.com and businesswire.com returned **HTTP 403** to WebFetch. Those pages are cited from search-result listings: they exist, but their full text was not read.

---

## Q1. Automotive HMI: which engine, which carmakers, how many cars, what it costs

### Takeaway
Most Chinese OEM 3D cockpits are built on **Unity / 团结引擎**. Unity China claims 35 OEMs, 77 production models and "~85%" of the domestic smart-cockpit 3D market (self-reported, Apr 2025). **Unreal** has a smaller but prominent list: Geely Galaxy E8, Lotus Hyper OS, HiPhi, MG Cyberster, plus Ford, GM and Rivian in the West. It also appears to be in **Tesla** (UE binaries in software 2025.20; Tesla does not use Godot, as far as these sources show). **Kanzi** (Rightware, a 中科创达 subsidiary) is the legacy 2D/2.5D HMI incumbent. No source discloses per-vehicle royalty rates. Unity Industry's list terms do show a ~4% runtime distribution fee model for non-game products.

### Cited Findings
**Unity / 团结引擎 (Unity China)**
- Apr 2024 (Beijing auto show, Unity China's first time exhibiting): "近 30 家整车厂", "超 60 款量产车型" with Unity HMI; ">80% of smart-EV brands" built real-time 3D HMI on Unity. 36Kr Japan flags that figure as "不完全統計" (incomplete statistics). Cockpit kit: 3D map, ADAS/NOP rendering, 3D Launcher, QNX instrument cluster, in-car game center, HDRP for Orin/8295, 6K 7.1.4 entertainment cockpit — [DoNews 2024-04-28](https://www.donews.com/news/detail/4/4197717.html) [press]; [36Kr Japan 2024-05-05](https://36kr.jp/287636/) [press]
- 36Kr Japan names **Mercedes-Benz, NIO, Xpeng and Li Auto** as Unity smart-cockpit users. Unity China valuation: US$1B — [36Kr Japan](https://36kr.jp/287636/) [press]
- Apr 2025 (Auto Shanghai, Unity China's third year in automotive): 35 global OEMs, 77 cumulative mass-produced models, ">85%" share (market undefined, self-reported). Tuanjie Engine is described as "succeeding Unity 6" for China. Chip partners: MediaTek, Rockchip, Unisoc, SemiDrive. Map partners: Amap, Tencent, Baidu, NavInfo. NIO digital-twin factory project — [KrASIA 2025-04-29](https://kr-asia.com/unity-china-steps-up-automotive-push-with-digital-twins-smart-cockpits-and-in-car-gaming) [press]; [36Kr EN 2025-04-26](https://eu.36kr.com/en/p/3266640500609668) [press]; [S&P AutoTechInsight](https://autotechinsight.spglobal.com/news/5281777/auto-shanghai-2025-unity-china-unveils-digital-twins-smart-cockpits-and-in-car-gaming-solution) (title only)
- **Leapmotor**: strategic agreement signed 2025-10-24. The C10 and C16 already ship Unity-powered 3D HMI. Leapmotor delivered ~396k vehicles in Jan–Sep 2025 — [Gasgoo 2025-10-27](https://autonews.gasgoo.com/articles/ev/unity-china-leapmotor-forge-long-term-partnership-to-redefine-in-car-interaction-70039580) [press]
- **Xiaomi and NIO** ("全系") built their 3D desktops on Unity. **Mercedes MB.OS** uses Unity (the "Unity Industrial Collection" package) for 3D cluster, infotainment and navigation. Unity is co-developing with chipmakers 芯驰 and 芯擎 — [电车通 via 36氪 2025-08-12](https://www.36kr.com/p/3418484154587273) [press]
- **Toyota** picked Unity for the GUI of its next-gen HMI (2025-02-06), involving "hundreds of software engineers". No models named — [Unity news](https://unity.com/cn/news/unity-chosen-by-toyota-motor-corporation-for-next-generation-hmi) [co]
- **Mazda**: partnership covering models launching 2025–2027 (Mar 2024) — [BusinessWire 2024-03-06](https://businesswire.com/news/home/20240306534030/en/Unity-Partners-with-Mazda-to-Transform-In-Cabin-Car-Experience) [co] (title and snippet only)
- Tuanjie Engine was announced Aug 2023. It is based on Unity 2022 LTS and supports Weixin Mini Games, OpenHarmony and AliOS — [Wikipedia: Unity](https://en.wikipedia.org/wiki/Unity_(game_engine)) [wiki]

**Unreal Engine**
- Epic (Oct 2025): 35+ models and 2M+ cars, as noted in round 1. Geely Galaxy E8 cockpit runs on UE. Per search snippet, Geely's GARI team evaluated Unity, Cocos and Unreal and chose UE for real-time rendering and HMI customizability — [Epic tech blog: Geely Galaxy E8](https://www.unrealengine.com/en-US/tech-blog/geely-galaxy-e8-smart-cockpit-inspired-by-the-stars-powered-by-unreal-engine) [co] (403 on fetch; snippet only)
- **Tesla**: per leaker @greentheonly, software update 2025.20 added Unreal Engine binaries. AMD-chip Model S/X can activate a UE-based visualization with zoomable 3D models. There is no evidence for Godot — [电车通 via 36氪 2025-08-12](https://www.36kr.com/p/3418484154587273) [press, relaying a leaker = unverified]
- **HiPhi (华人运通)**: company-level strategic deal with Epic (Nov 2021). HiPhi Z (2022) was billed as China's first "真·3D 数字座舱". HiPhi has since stopped production; that is background knowledge, not from this source. **Lotus Hyper OS** (ELECTRE, 2× Snapdragon 8155) was billed as the first UE-based cockpit OS. Geely Galaxy E8 and **MG Cyberster** also use UE. Epic and Qualcomm co-optimize UE on Snapdragon — [36氪](https://www.36kr.com/p/3418484154587273) [press]; [Autocar Pro: Qualcomm–Epic](https://autocarpro.in/news-international/qualcomm-partners-epic-games-to-elevate-in-vehicle-user-experiences-with-scalable-solution-122865) (title only)
- **2024 Ford Mustang**: UE drives the 12.4" cluster and 13.2" infotainment. Rivian infotainment also runs UE — [Wikipedia: Unreal Engine](https://en.wikipedia.org/wiki/Unreal_Engine) [wiki]

**Kanzi (Rightware / 中科创达 ThunderSoft)**
- Kanzi launched in 2011. The first car shipping it was the Audi A3 (Jun 2012). Rightware claimed "35 automotive brands" by 2017. It became a ThunderSoft subsidiary in 2017. Kanzi One followed in 2021 — [Wikipedia: Rightware](https://en.wikipedia.org/wiki/Rightware) [wiki]
- ThunderSoft (中科创达) E-Cockpit includes a Kanzi-based HMI framework and was cited as the cockpit supplier for 理想 ONE — [IT之家 via search snippet](https://www.ithome.com/0/606/788.htm) [press, snippet]

**Cocos**
- Cocos says Creator serves "汽车、XR、教育". It names no carmakers on its site. A Ford smart-cockpit cooperation appeared only in a search summary — [cocos.com](https://www.cocos.com/) [co]

**License economics (the only public numbers found)**
- **Unity Industry**: $4,950/seat/yr. Applies to non-game companies with revenue above US$1M. The distribution license fee is "generally ~4.0% of revenue from products that include the Unity runtime" — [unity.com/products/unity-industry](https://unity.com/products/unity-industry) [co]
- **Unreal**: $1,850/seat/yr for non-game companies (see round 1). The 5% royalty above $1M applies to games, not HMI — [Wikipedia: Unreal Engine](https://en.wikipedia.org/wiki/Unreal_Engine) [wiki]
- Market context: KPMG forecasts China's smart-cockpit market at ¥2,127亿 by 2026, with >82% penetration — [36氪](https://www.36kr.com/p/3418484154587273) [analyst, via press]

### Inferences
- In China the split looks like this. Unity/团结 is the default for mass-market NEV 3D desktops: NIO, Xiaomi, Li Auto, Xpeng, Leapmotor. Unreal is chosen for flagship "showcase" cockpits: Geely Galaxy/Lotus, HiPhi, MG. Kanzi survives in clusters and legacy 2D HMI.
- Per-car economics are almost certainly negotiated per-unit runtime fees plus engineering services, which is why none are public. The ~4% "distribution fee" anchor on Unity Industry suggests runtime-based pricing is the template.
- "Unity China 85%" is self-reported and its denominator is undefined. Treat it as "most Chinese 3D cockpits", not as a measured share.

### Gaps
- **BYD (DiLink), 华为鸿蒙座舱 (HarmonyOS cockpit), 吉利 beyond Galaxy, 小鹏 engine**: no sourced statement. I could not run the searches; the budget was exhausted. Huawei likely uses in-house ArkGraphics 3D, but that is unverified.
- **Unity China revenue and its automotive share**: no figure was found. The 10-K doesn't break it out (see Q5). Per-vehicle license fee: not public.
- Epic's 2026 update to the "35 models" figure was not found.

---

## Q2. Virtual production: volumes, ILM StageCraft, Pixomondo/Disguise, Chinese stages and day rates, growth vs. contraction 2023–2026

### Takeaway
After the 2020–22 boom (Epic counted ~300 stages by Oct 2022), Western LED-volume VP consolidated in 2025–26. Sony is **winding down Pixomondo**, including its VP division (announced Mar 2026, ~500 people affected), and **Dark Slope bought Pixomondo's VP assets** (Sep 2026). Producers report that the promised ~10× savings did not materialize. China, by contrast, is still building: iQIYI's Hengdian flagship stage, Deqing's "world's largest single LED volume" (2025–26), and state-backed parks for micro-dramas (短剧). Chinese day rates fell from **¥16万/day to as low as ¥3.5万/day** (iQIYI, Jun 2025).

### Cited Findings
**Global stage count and the cycle**
- Epic's Miles Perkins estimated ~300 LED stages by Oct 2022, up from 3 in 2019 (THR 2022-10-19, cited by Wikipedia) — [Wikipedia: Virtual production](https://en.wikipedia.org/wiki/Virtual_production) [wiki → THR]
- Disguise says its site lists **402 VP and xR studios**, "~90% of Tier-1 live shows" and "~80% of the biggest A-list tours", across 116 countries (company claims, 2026 page) — [disguise.one](https://www.disguise.one/en/) [co]
- VFX Voice (Apr 2025): producers expected ~10× cost savings, and they "didn't materialize" ("dramatic but not that dramatic", Danny Firpo, All of it Now). Volumes are now used mainly for vehicle process shots and fast environment changes. LED walls are poor key lights. Interest rates are making productions more cost-cautious — [VFX Voice, Spring 2025](https://vfxvoice.com/virtual-production-now-and-going-forward) [press]
- **Pixomondo** (Sony): on 2026-03-20 Sony said it will wind down Pixomondo's VFX and **virtual production division** after current contracts. VFX moves to Sony Pictures Imageworks. "500 people affected" per Pixomondo management, "a few hundred" per Sony. Pixomondo had 3 LED stages when Sony bought it in 2022 — [AWN 2026-03-20](https://www.awn.com/news/sony-wind-down-pixomondo-consolidate-vfx-work-imageworks) [press]
- On 2026-09-29, **Dark Slope** (Toronto; *Heated Rivalry*) acquired Pixomondo's VP assets. The article is paywalled, so this rests on the headline only — [THR 2026-09-29](https://www.hollywoodreporter.com/business/business-news/virtual-production-company-dark-slope-buys-pixomondo-assets-1236714455/) [press]; [Wikipedia: Pixomondo](https://en.wikipedia.org/wiki/Pixomondo) [wiki]
- Pixomondo's Vancouver stage (built for Netflix's *Avatar: The Last Airbender*) holds the Guinness "largest LED stage" record (GWR 2023 edition). It measures 80 ft × 27.5 ft, with 3,260 panels (2,500 wall + 760 ceiling) — [AWN 2022-05-13](https://www.awn.com/news/pixomondos-led-stage-biggest-ever-says-guinness-world-records) [press]
- **Openings still happen**: Studio Ulster (Belfast) opened Jun 2025. It cost £72M, covers 75,000 sq ft, has 3 VP stages (VP1 is 61 m wide), and runs ROE panels, Brompton processors and Unreal Engine. An early job is a BBC NI Titanic drama — [SVG 2025-07-25](https://www.sportsvideo.org/2025/07/25/285462/) [press]

**ILM StageCraft**
- StageCraft launched with *The Mandalorian* (2019) on Unreal Engine. StageCraft 2.0 added ILM's own **Helios** renderer. Announced volumes: Manhattan Beach ×2, Pinewood London, Fox Studios Australia, Vancouver (2022) — [Wikipedia: StageCraft](https://en.wikipedia.org/wiki/StageCraft) [wiki]
- Productions listed for 2024–26: *Avatar: The Last Airbender*, *Doctor Who* S14, *Skeleton Crew*, *Transformers One*, *Tron: Ares*, *The Lost Bus*, *A Big Bold Beautiful Journey*, *The Mandalorian and Grogu* (2026) — [Wikipedia: StageCraft](https://en.wikipedia.org/wiki/StageCraft) [wiki]
- ILM's StageCraft page lists studios in San Francisco, Vancouver, London, Mumbai and Sydney. It gives no volume count — [ilm.com/stagecraft](https://www.ilm.com/stagecraft/) [co]
- Amazon's Stage 15 in Culver City (opened Dec 2022, 34,000 sq ft, 3,000+ LED panels, 100 mocap cameras) later hosted *Mercy* (Amazon MGM). No closure report was found — [aboutamazon](https://www.aboutamazon.com/news/aws/aws-virtual-soundstage-stage-15-movies-tv-shows) [co, via search]

**China**
- **iQIYI**:
  - Timeline: XR system at Hebei 大厂 (end-2020), then a 2,400 m² stage at Hengdian (2022), then the Hengdian 13号棚 flagship (2024).
  - Flagship spec: 500 m² LED, 1.9–1.95 mm pitch, 225° curve, and a 100-ton motorized turntable.
  - Price: **¥16万/day before the cut; from 2025-06-01 as low as ¥3.5万/day** (full HW/SW, no scene build).
  - Volume: VP projects up 50% YoY.
  - Shows: *云之羽* (first Chinese commercial series released using VP) and *大梦归离* (95% of shots needed no post VFX).
  - Seven more series shot after the upgrade (e.g. 唐朝诡事录之长安, 天地剑心).
  - Sources: [IT之家](https://www.ithome.com/0/857/782.htm) [press]; [扬子晚报 2025-10-29 (open day 2025-11-02)](https://www.yzwb.net/news/wy/202510/t20251029_283136.html) [press]
- A 30-day shoot at the old price ≈ ¥500万 for VP scenes. After the price cut, more mid-tier crews came. Use is mostly 古装 and 玄幻 dramas, and the value is "提效而非降本" (efficiency, not cost saving). Other Chinese stages:
  - Tencent IEG: 3,000 m² LED stage
  - Youku: 帧享 stage, 周庄
  - Wuxi National Digital Film Park: "largest film-grade screen"
  - Main LED supplier: 洲明科技 (Unilumin)
  - Sources: [快科技/差评 2025-11-01](https://news.mydrivers.com/1/1083/1083801.htm) [press]
- **Deqing (德清) AI virtual film base**:
  - Stage: "world's largest single LED volume", 3,700 m² of LED, 50 m diameter curve.
  - Status: open for less than six months as of Jan 2026; 43 VP/AI-film firms moved in.
  - Funding: a ¥1亿 "虚拟拍摄预演基金" (previsualization fund).
  - Current shoot: a HK football film rendering Kai Tak stadium with 10,000 digital spectators.
  - Sources: [扬子晚报 citing CCTV 2026-01-13](https://www.yzwb.net/news/yw/202601/t20260113_310552.html) [st-media]
  - The Absen × Versatile Media volume (unveiled 2025-07-14) is a 270° curved wall, 50 m diameter × 12 m high, with 1,700 m² of LED at 1.5 mm pitch — [AVIXA](https://www.avixa.org/explore/articles/largest-led-virtual-production-volume) [press]
- **Micro-drama (短剧) shift, 2025–26**:
  - New XR LED parks: Chengdu 东八区数字片场 (Apr 2026), Nanning (Feb 2026), Wuxi, Beijing 宋庄 (May 2026).
  - Pricing: state-backed (广电) park rent is 15–25% below private stages; 20% off for rentals of 15+ days.
  - Speed: a 100-episode vertical drama takes ~2 weeks virtual vs. ~30 days on real sets.
  - Regulation: tiered NRTA filing from 2026-07-01; dramas over 50% AI-generated frames must be labeled.
  - Source: [网易号 2026](https://c.m.163.com/news/a/L20KBOD40517CABB.html) [press, low-medium reliability]
- Taiwan reference point: AUO × 再現影像 stage at CMPC (Dec 2022), 380 panels, 12 m diameter × 5 m high, 180° — [數位時代](https://www.bnext.com.tw/article/73355/auo-reno-studios) [press]

### Inferences
- **Growth or contraction?** In the West, the period looks like **plateau then consolidation**. Openings continue (Studio Ulster), while marquee operators exit: Sony/Pixomondo VP closed, and its assets went to Dark Slope. Volumes are becoming rented infrastructure, not a growth engine. In China, **capacity grew in 2025–26** but prices fell ~78% at the market leader. That points to oversupply relative to premium-drama demand, with cheap micro-dramas as the new demand.
- Engine share inside volumes is still overwhelmingly Unreal: the Studio Ulster spec, the iQIYI article, and StageCraft's lineage all point there. ILM's Helios is the main proprietary exception.

### Gaps
- No reliable 2024–2026 worldwide LED-volume count. Disguise's 402 is its own installed base. THR's ~300 dates from 2022.
- Western day rates: none were found from a citable source. The usual industry range of tens of thousands of USD per day is background only.
- 博纳 and 华策 VP stages: no sourced data. 横店 beyond iQIYI: no data.
- Lux Machina/NEP, ILM StageCraft volume count in 2026, and Disguise financials (Kohlberg investment, 2022) were not verified. The disguise Wikipedia page returned 404.

---

## Q3. Broadcast and live: Vizrt, Unreal in sports/weather/elections, CCTV Spring Festival Gala XR

### Takeaway
Broadcast graphics remain a Vizrt-centric market that now **integrates** Unreal rather than being replaced by it. Little 2024–26 broadcast detail could be verified with the search budget gone.

### Cited Findings
- Vizrt is owned by Nordic Capital (taken private 2015). It bought NewTek (TriCaster, NDI) for $95.25M in May 2019 and has customers in 100+ countries (CNN, BBC, Fox Sports, CBS, Sky, Al Jazeera…). Election history: CNN "holograms" (2008), US 2012, and others — [Wikipedia: Vizrt](https://en.wikipedia.org/wiki/Vizrt) [wiki]
- Viz Engine 5.5 lists "Unreal Engine integration". CBS News says Viz Engine 5 "complimented what we were looking to achieve with Unreal Engine" in its 2022 US election coverage — [vizrt.com Viz Engine](https://www.vizrt.com/products/viz-engine/) [co]
- Unreal is used by cable news for real-time graphics (generic statement) — [Wikipedia: Unreal Engine](https://en.wikipedia.org/wiki/Unreal_Engine) [wiki]
- CCTV/CMG Spring Festival Gala 2026 (aired 2026-02-16) used "AI technology [to enhance] visual effects". The source page didn't render, so only the headline was read — [CGTN Radio/CRI 2026-02-16](https://chinaplus.cri.cn/podcast/news/5/AI-technology-enhances-visual-effects-at-CMG-Spring-Festival-Gala/2718970) [st-media, headline only]
- TUDN MetaHumans at the 2022 World Cup: see round 1. The IBC paper page lists the title only — [IBC](https://www.ibc.org/technical-papers/ibc2023-tech-papers-using-metahumans-in-large-scale-sports-production/10279.article)

### Inferences
- Unreal in broadcast now ships mostly through Vizrt, Disguise, Pixotope and Zero Density front-ends. Epic gets seat or royalty revenue indirectly; broadcasters don't buy "Unreal" as a product.

### Gaps
- No verified 2024–26 cases for Weather Channel IMR, Fox Sports, NBC Olympics 2024, BBC/CNN 2024 elections, or 春晚 2025/2026 XR details (engine, vendor). All need searches I couldn't run.
- Vizrt revenue is not public (private, Nordic Capital).

---

## Q4. Digital humans: MetaHuman, Soul Machines, UneeQ, Chinese live-commerce digital humans

### Takeaway
In the West, "digital human" value moved from bespoke real-time 3D avatars to **video-generation avatars**. Soul Machines (~US$135M raised) went into **receivership in Feb 2026**, owing NZ$19.5M+. Synthesia reached a $4B valuation and $100M+ revenue (Oct 2025). In China the market is large by analyst count: iiMedia puts the core market at ¥480.6亿 in 2025. Baidu discloses "AI-native marketing services (agents + digital humans)" at ~¥2.6–2.8B **per quarter**, but growth went flat by Q2 2026. Prices collapsed to roughly ¥8,000 for a basic clone as early as 2023.

### Cited Findings
**West**
- **Soul Machines** (Auckland; founded 2016 by Mark Sagar and Greg Cross; ~US$135M raised from SoftBank VF2, Temasek, Salesforce Ventures):
  - Receivers: KPMG's Leon Bowker and Luke Norman, appointed 2026-02-05.
  - Debts: over **NZ$19.5M** owed to creditors, per the first receivership report (NBR 2026-04-13).
  - Deployments with Mercedes-Benz, ANZ and Air NZ were wound down.
  - Status: no buyer reported in what I found. The company website still shows products (©2025).
  - Sources: [NBR: in receivership](https://www.nbr.co.nz/tech/soul-machines-in-receivership) [press, via search]; [NBR: owes $19.5m](https://www.nbr.co.nz/tech/soul-machines-owes-19-5m-in-receivership) [press, via search; 403 on fetch]; [soulmachines.com](https://www.soulmachines.com/) [co]
- **UneeQ** is still operating. It repositioned to AI roleplay training ("Immersive Training Platform", "AI Buddy" shown at Gartner CSO 2026) and Digital Human OS Gen2. Case studies: Qatar Airways, Deutsche Telekom, Pearson. No pricing — [digitalhumans.com](https://www.digitalhumans.com/) [co]
- **Synthesia**:
  - Funding: $180M Series D at $2.1B (Jan 2025); $200M Series E at **$4B** (Oct 2025, GV, Nvidia, Accel).
  - Revenue: "exceeding $100M annually".
  - Customers: 65k (Jun 2025).
  - Reportedly rejected a $3B Adobe offer.
  - Source: [Wikipedia: Synthesia](https://en.wikipedia.org/wiki/Synthesia_(company)) [wiki]
- **HeyGen**: $60M at a $500M valuation (Jun 2024), ARR $35M, 40k+ customers. Early investors were HongShan and ZhenFund — [Wikipedia: HeyGen](https://en.wikipedia.org/wiki/HeyGen) [wiki]
- **MetaHuman** is included in the standard UE license and usable in UEFN (Fortnite's editor). No usage counts are published — [metahuman.com/llms.txt](https://www.metahuman.com/llms.txt) [co]

**China**
- iiMedia market size:
  - Core market: ¥339.2亿 (2024), ¥480.6亿 (2025), ¥935.6亿 (2030E).
  - "带动" (induced) market: ¥4,785亿 (2024), ¥6,403亿 (2025).
  - Global digital-human live-commerce market: US$49.3B (2024), US$76.8B (2026E). This is an analyst figure and looks very high.
  - Source: [iiMedia tag page](https://report.iimedia.cn/tag/数字人) [analyst]
- **Baidu**, quarterly "AI-native marketing services" (agents + digital humans):
  - **¥2.8B in Q3 2025 (+262% YoY)**. Robin Li: "agents and digital humans delivered rapid revenue growth" — [Baidu Q3 2025 6-K EX-99.1, 2025-11-18](https://www.sec.gov/Archives/edgar/data/1329099/000119312525285391/d52736dex991.htm) [filing]
  - ¥2.7B in Q4 2025 (+110% YoY) — [Baidu Q4 2025 6-K, 2026-02-26](https://www.sec.gov/Archives/edgar/data/1329099/000119312526076505/d117608dex991.htm) [filing]
  - **¥2.6B in Q2 2026, ~flat YoY** — [Baidu Q2 2026 6-K, 2026-08-18](https://www.sec.gov/Archives/edgar/data/1329099/000119312526355431/d112854dex991.htm) [filing]
  - None of these releases mentions livestream GMV or Luo Yonghao.
- **SenseTime 如影 (SenseAvatar)**: led national standard GB/T 46483-2025 for customer-service digital humans (Nov 2025). Clients: Bank of China, China Mobile, New Oriental, Taobao. Its "直播带货数字人" serves "上千个直播间" (thousands of livestream rooms) on Taobao, Meituan and JD. No prices or GMV — [量子位 2025-11-18](https://www.qbitai.com/2025/11/354033.html) [press]; [澎湃 2025-11-20](https://www.thepaper.cn/newsDetail_forward_32005394) [press]
- **Prices (2023)**: a 硅基智能 basic clone cost ~¥8,000 (~$1,100) including a year of maintenance. Xiaoice clones cost under $1,000 from 1 minute of video. 硅基智能 had generated **400,000** virtual streamers (goal: 100M "silicon-based laborers" by 2025). One Xiaoice streamer earned over ¥10,000 in one hour — [MIT Technology Review 2023-09-19](https://www.technologyreview.com/2023/09/19/1079832/chinese-ecommerce-deepfakes-livestream-influencers-ai/) [press]

### Inferences
- Bespoke real-time 3D "digital humans" (Soul Machines, early UneeQ) failed as a stand-alone business. Value accrued to (a) video-avatar SaaS (Synthesia, HeyGen) and (b) platform-bundled livestream avatars in China (Baidu, JD, SenseTime), where the avatar is a feature that sells ads or commerce.
- Baidu's flat Q2 2026 suggests the digital-human and agent ad product has saturated after its 2025 ramp.

### Gaps
- **Live-commerce GMV via digital humans**: no verified figure. The widely repeated Luo Yonghao × Baidu digital-human livestream (Jun 2025; GMV reportedly ¥5,500万+) could **not** be sourced, because searches were blocked and Baidu's filings don't mention it. JD 言犀 and 腾讯智影 pricing and usage: pages didn't render or were blocked. 硅基智能 revenue and IPO status: not found. IDC 数字人 vendor-share report: not found.

---

## Q5. Engine companies' financials (Unity, Epic, Godot, Cocos, Galacean)

### Takeaway
Unity's Create segment, which holds all engine and industry revenue, is flat at **~$621M (2025)**. All of Unity's growth is in ads (Grow). Unity is reportedly exploring a **sale of Unity China** at more than $1B (≈Mar 2026). Epic doesn't disclose its revenue split. It cut 1,000+ staff (Mar 2026) on a Fortnite slump, divested ArtStation and Sketchfab, and announced **UE6** (May 2026). Godot runs on ~€36k/month in donations. Cocos was **sold to SUD for $72M** (Nov 2025). Galacean remains Ant Group's open-source web engine.

### Cited Findings
**Unity**
- FY2025 revenue was $1,849.6M (FY2024: $1,813.3M). **Create Solutions: $621.4M (2024: $614.0M); Grow: $1,228.2M (2024: $1,199.3M).** Non-strategic revenue, "primarily in Create", was ~$28M (2025) vs. ~$90M (2024). Redeemable noncontrolling interests (mainly Unity China) were $252.6M at end-2025 — [Unity 10-K FY2025](https://www.sec.gov/Archives/edgar/data/1810806/000181080626000011/unity-20251231.htm) [filing]
- The 10-K says Create serves "automotive, retail, manufacturing, healthcare, public sector, robotics…" but gives **no non-gaming revenue figure**. China showed "softness throughout 2023 and 2024". Unity China investors hold ~20.5% (bought for $197M) with redemption rights until Aug 2027, triggered among other things by a China IPO valued above ¥25B — [Unity 10-K](https://www.sec.gov/Archives/edgar/data/1810806/000181080626000011/unity-20251231.htm) [filing; Unity China stake details via search snippet]
- Q4 2025: Create $165M (+8%), Grow $338M (+11%). Q1 2026 guidance: revenue $480–490M — [Unity Q4 FY2025 release](https://investors.unity.com/news/news-details/2026/Unity-Reports-Fourth-Quarter-and-Fiscal-Year-2025-Financial-Results/default.aspx) [filing]
- **Q2 2026**: revenue $546M (+24%). Create $158M (+2%; strategic Create +5%, or +14% excluding a one-off). Grow $389M (+35%). The ironSource Ads network was sunset 2026-04-30 and Supersonic sold 2026-08-04. Q3 2026 guidance: strategic revenue $540–550M. There is no Industry, China or automotive disclosure — [Unity Q2 2026 release](https://investors.unity.com/news/news-details/2026/Unity-Reports-Second-Quarter-2026-Financial-Results/default.aspx) [filing]
- China was "20% of total revenue, up from 15%" (management, per secondary site). Greater China Q2 2025 revenue was $83.6M (+34.7%) — [itiger summary](https://www.itiger.com/hans/news/1100252571) [secondary, unverified]
- Unity is reportedly evaluating a sale of Unity China at more than $1B (around Mar 2026, "知情人士", i.e. unnamed insiders) — [澎湃](https://www.thepaper.cn/newsDetail_forward_32682710) [press relaying anonymous report]
- Unity Industry: $4,950/seat/yr (see Q1). The old ~$58M Industry estimate in round 1 remains the only figure.
- Unity bought Weta Digital's tools for $1.625B (Dec 2021). It laid off all Wētā Digital staff and ended the service agreement (effective 2023-12-10) — [Wikipedia: Wētā FX](https://en.wikipedia.org/wiki/W%C4%93t%C4%81_FX) [wiki]

**Epic Games**
- Revenue was ~US$6B in 2022 (infobox). No later figure. Ownership: Sweeney 41.4%, Tencent 28%, **Disney 9% ($1.5B, Feb 2024)**, Sony 5.4% — [Wikipedia: Epic Games](https://en.wikipedia.org/wiki/Epic_Games) [wiki]
- **2026-03-24**: Epic laid off 1,000+ staff and cut ~$500M in costs, "amid Fortnite downturn" (Variety, NYT). About 4,000 staff remain. **2026-08**: ArtStation and Sketchfab were sold to KitBash. **UE6** was announced 2026-05-24, with early access "late 2027-ish" — [Wikipedia: Epic Games](https://en.wikipedia.org/wiki/Epic_Games) [wiki → Variety/NYT]; [Wikipedia: Unreal Engine](https://en.wikipedia.org/wiki/Unreal_Engine) [wiki]
- UE royalty: 5% above $1M for games, waived on the Epic Games Store. Non-game: seat subscription (round 1) — [Wikipedia: Unreal Engine](https://en.wikipedia.org/wiki/Unreal_Engine) [wiki]

**Godot**
- Godot Development Fund: **€35,679/month**, 1,833 members, 23 corporate sponsors. Platinum sponsors include Battlefield Studios, W4 Games, JetBrains. Arm and DeNA are Gold. Page undated, fetched 2026-10-13 — [fund.godotengine.org](https://fund.godotengine.org/) [co]
- History: Epic MegaGrant $250k (2020); Re-Logic $100k plus $1k/month (Sep 2023). Godot overtook Unity at the GMTK Game Jam in 2026. Battlefield 6's Portal editor uses Godot — [Wikipedia: Godot](https://en.wikipedia.org/wiki/Godot_(game_engine)) [wiki]; [Wikipedia: Unity](https://en.wikipedia.org/wiki/Unity_(game_engine)) [wiki]

**Cocos**
- **SUD acquired Cocos for US$72M (Nov 2025)**, per PocketGamer.biz 2025-11-18 as cited by Wikipedia. The cocos.com footer reads "©2026 SUD" — [Wikipedia: Cocos2d](https://en.wikipedia.org/wiki/Cocos2d) [wiki]; [cocos.com](https://www.cocos.com/) [co]
- Company claims: ~1.7M developers, 203 countries and regions, 2B+ end users, uses in automotive, XR and education — [cocos.com/about](https://www.cocos.com/about) [co]

**Galacean (Ant Group)**
- MIT-licensed TypeScript WebGL/glTF engine with 5.9k GitHub stars. Version 1.6 is the latest announced. Its browser editor exports to Alipay mini-programs; the named showcase is Alipay "神奇海洋" — [GitHub](https://github.com/galacean/engine) [co]; [galacean.antgroup.com](https://galacean.antgroup.com/engine) [co]

### Inferences
- Engine licensing is a flat ~$620M/yr business at Unity and undisclosed (probably similar order) at Epic. Both firms' growth and pain come from ads and Fortnite, not from non-game engine use. Selling down Unity China would remove Unity's strongest automotive asset from its consolidated numbers.
- The Chinese engine layer is consolidating under platform or social-game owners: Cocos→SUD, Galacean→Ant, Tuanjie→a JV possibly up for sale.

### Gaps
- Epic's 2024/2025 revenue and Fortnite-vs-engine split: not disclosed; no reliable estimate was found. Unreal royalty totals: not disclosed.
- Unity China's standalone revenue: not found. The "sale" report's original outlet (likely Bloomberg/Reuters) was not verified.

---

## Q6. Industrial, training, medical and military uses

### Takeaway
Documented uses exist, but this session found few with contract values.

### Cited Findings
- Unreal Government Network (with Virtual Heroes, Mar 2012). Projects include US Army anesthesiology training, FBI Academy crime-scene sim, IARPA bias training, and the DHS S&T plus US Army **EDGE** first-responder platform — [Wikipedia: Unreal Engine](https://en.wikipedia.org/wiki/Unreal_Engine) [wiki]
- Unity for government and defense: Teledyne FLIR UAS training sim; HAVIK VR JTAC/sUAS training; Port of Corpus Christi security digital twin — [unity.com government](https://unity.com/solutions/government-aerospace) [co]
- Bohemia Interactive Simulations (VBS) was split off to Riverside Co. in 2013. Its engine lineage is shared with Arma/Enfusion, not UE or Unity — [Wikipedia: Bohemia Interactive](https://en.wikipedia.org/wiki/Bohemia_Interactive_Simulations) [wiki]
- China digital twin and simulation: see 51WORLD in round 1.

### Gaps
- No contract values for the US Army STE, UK MoD, or medical simulation (e.g. surgical training on UE or Unity). Sources needed searches.

---

## Q7. Standout demos and cases (URL status)

### Takeaway
These URLs were opened in this session unless marked otherwise.

### Cited Findings
- Pixomondo Vancouver Guinness LED stage, 2022 (opened OK) — https://www.awn.com/news/pixomondos-led-stage-biggest-ever-says-guinness-world-records
- iQIYI Hengdian flagship VP stage, price cut and open day, 2025 (opened OK) — https://www.ithome.com/0/857/782.htm ; https://www.yzwb.net/news/wy/202510/t20251029_283136.html
- Deqing "world's largest single LED volume", CCTV report 2026-01 (opened OK) — https://www.yzwb.net/news/yw/202601/t20260113_310552.html
- Studio Ulster VP stages, 2025 (opened OK) — https://www.sportsvideo.org/2025/07/25/285462/
- Geely Galaxy E8 UE cockpit (exists in search results; **403 on fetch**) — https://www.unrealengine.com/en-US/tech-blog/geely-galaxy-e8-smart-cockpit-inspired-by-the-stars-powered-by-unreal-engine
- Epic's "five years, 35 car models" HMI post (exists; **403 on fetch**) — https://www.unrealengine.com/en-US/news/five-years-35-car-models-how-unreal-engine-is-accelerating-hmi-innovation
- Tesla UE visualization leak, 2025.20 (opened OK; leaker-sourced) — https://www.36kr.com/p/3418484154587273
- Unity × Leapmotor C10/C16 3D HMI (opened OK) — https://autonews.gasgoo.com/articles/ev/unity-china-leapmotor-forge-long-term-partnership-to-redefine-in-car-interaction-70039580
- Galacean engine repo (opened OK) — https://github.com/galacean/engine

### Gaps
- No video demo URLs (YouTube) could be found or verified without search.

