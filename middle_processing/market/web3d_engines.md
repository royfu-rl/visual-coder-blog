# Commercial uses of Web 3D, Blender, game engines (non-game), and "AI writes 3D code" tooling (as of Oct 2026)

Method note: 19 tool calls (WebSearch, plus one Epic WebFetch that returned 403). Most numbers come from vendor or analyst-blog sources and are labeled that way. Items marked **[bg]** are well-known URLs/facts from background knowledge that were NOT re-verified in this session. The writer should treat them as leads, not as citations.

---

## Q1. three.js / WebGL / WebGPU (incl. Babylon.js, PlayCanvas, Spline, R3F): where it lands commercially

### Takeaway
Web 3D earns money in four places: (1) e-commerce product viewers and configurators, a ~$1.7–1.8B software niche; (2) award-chasing brand/marketing sites built by a small set of boutique studios (Immersive Garden, Lusion, Active Theory, OFF+BRAND); (3) China's mini-program games, a ~¥535–610B market (2025) where Cocos is the default engine; and (4) a growing "AI builds a three.js game" segment. WebGPU became usable in three.js from r171 (late 2024) and in all major browsers once Safari 26 shipped (Sep 2025), but most production sites still run WebGL.

### Cited Findings
**E-commerce configurators**
- 3D visual product configurator software market: $1.70B in 2025, projected $4.50B by 2033 (12.9% CAGR) — [Verified Market Research](https://www.verifiedmarketresearch.com/product/3d-visual-product-configurator-software-market/); another estimate is $1.8B (2024), projected $5.6B by 2033 — [DataHorizzon](https://datahorizzonresearch.com/3d-visual-product-configurator-software-market-39527)
- Threekit + Shopify: 3D/AR customization for Shopify merchants, with a claimed "up to 250% increase in conversion" (a Shopify/vendor figure) — [Threekit blog](https://www.threekit.com/blog/shopify-launch-blog-post)
- A Shopify-attributed "94% average conversion lift from 3D/AR" circulates via DesignRush. The more rigorous figure is a 50/50 A/B test over 220k PDP views at a furniture retailer, which found a +35% conversion lift for shoppers who interacted with 3D — [Framesixty](https://framesixty.com/3d-configurator/); [Bogos](https://bogos.io/shopify-product-configurator/)
- Shopify natively shows rotatable 3D/AR models but has no configurator, so configurators come from apps (Zakeke, Threekit, Angle 3D, ShapeDiver, Kickflip) — [Bogos](https://bogos.io/shopify-product-configurator/)
- Zakeke: 3D configurator with AR and virtual try-on, also listed on the Adobe Commerce marketplace; from ~$29/mo — [Adobe Commerce Marketplace](https://commercemarketplace.adobe.com/futurenext-zakekeconfigurator.html); [Framesixty](https://framesixty.com/3d-configurator/)
- Threekit targets furniture, automotive and manufacturing; reported pricing of $50k–150k+/yr comes from a competitor's guide and is unverified — [Framesixty](https://framesixty.com/3d-configurator/)
- Babylon.js (Apache-2.0) in commerce: Apviz SaaS configurator, FrameItEasy picture-frame configurator — [Babylon forum: Apviz](https://forum.babylonjs.com/t/apviz-saas-cloud-based-3d-configurators/31964); [Babylon forum: FrameItEasy](https://forum.babylonjs.com/t/picture-frame-configurator-frameiteasy-com/60203)
- PlayCanvas: acquired by Snap in 2017 (older fact). It has been used for 3D product rendering at Polaris and Trelleborg (older coverage). A blog post from Aug 2025 covers Gaussian Splatting for e-commerce — [Game Developer](https://gamedeveloper.com/game-platforms/snapchat-acquires-cloud-based-engine-playcanvas); [PlayCanvas blog archive](https://blog.playcanvas.com/archive)

**Brand and marketing sites (agencies and demos)**
- Immersive Garden: own site was Awwwards SOTD (Nov 2024) and SOTM (Dec 2024), built with three.js; also made the Cartier Watches & Wonders 2025 site; reportedly Awwwards Agency of the Year 2025 (secondary source) — [Awwwards case study](https://www.awwwards.com/case-study-immersive-gardens-new-website.html); [Metabole](https://metabole.studio/en/blog/immersive-website-examples)
- Lando Norris official site by OFF+BRAND, reportedly Awwwards Site of the Year 2025 (scroll-driven 3D helmet); "Messenger" (a tiny WebGL planet) reportedly Developer SOTY 2025. Both claims are secondary and should be checked against awwwards.com — [Utsubo](https://www.utsubo.com/blog/best-threejs-websites-2026)
- Lusion: EverSwap won SOTD plus a Developer Award (Jun 2026); Oryzo won SOTM (Apr 2026) — [Utsubo agencies list](https://www.utsubo.com/blog/top-threejs-agencies); [Psychoactive](https://www.psychoactive.co.nz/content-hub/best-webgl-interactive-3d-agencies)
- Active Theory runs its in-house "Hydra" WebGL engine for large builds — [Psychoactive](https://www.psychoactive.co.nz/content-hub/best-webgl-interactive-3d-agencies)
- Awwwards curated three.js collection — [Awwwards](https://www.awwwards.com/awwwards/collections/three-js/)

**Tech and adoption**
- three.js r171 (late 2024) lets you swap WebGLRenderer for WebGPURenderer in one line; Safari 26 (Sep 2025) added WebGPU, with WebGL2 fallback for the rest; as of Jan 2026 most three.js projects still run on WebGL — [Utsubo migration guide](https://www.utsubo.com/blog/webgpu-threejs-migration-guide); [Utsubo 2026](https://www.utsubo.com/blog/threejs-2026-what-changed); [VR.org](https://vr.org/articles/webgpu-baseline-2026-three-js-webxr-default)
- three.js npm downloads are claimed at ~2.7M/week, "270x Babylon.js" (vendor blog) — [Utsubo](https://www.utsubo.com/blog/threejs-2026-what-changed)

**Spline (no-code web 3D)**
- $15M seed (Jul 2023); $10M Series A (Aug 2024) led by Third Point Ventures, with Gradient, YC, and Guillermo Rauch (Vercel) and Jorn van Dijk (Framer). Funds were earmarked for "bringing AI to 3D designers" — [Pulse 2.0](https://pulse2.com/spline-collaborative-3d-design-platform-company-secures-10-million-series-a); [BusinessWire Aug 2024](https://businesswire.com/news/home/20240813508808/en/Spline-Becomes-First-3D-Design-Platform-to-Enable-Designers-to-Ship-Interactive-Experiences-Cross-platform)
- "Spline AI V2" (Aug 20, 2026, with WebGPU and Agent Mode) is reported only by a low-reliability directory — [stork.ai](https://www.stork.ai/en/spline-ai)

**China mini-program games (微信/抖音小游戏)**
- WeChat mini games: RMB 53.5B in 2025 (+34.4% YoY), with 68% from IAP and 32% from ads; >5 亿 MAU — [Game Industry Library (Meridian Play/Jinke)](https://gameindustrylibrary.com/documents/meridian-play-jinke-china-s-wechat-mini-games-market-in-2026-sponsored-by-pwn-games)
- DataEye puts China's total mini-game market at ~¥610 亿 in 2025 (+22%), and >¥700 亿 in 2026E — [澎湃](https://www.thepaper.cn/newsDetail_forward_32682540)
- 2024: ¥398 亿, nearly doubling YoY — [Cinevva](https://app.cinevva.com/zh-CN/blog/2026-07-19-ai-engine-wechat-mini-games)
- Platform constraints: 4MB main package and 1GB memory; Cocos and Laya are the officially supported engines; the Cocos runtime is baked into the WeChat client, while Laya's is not — [Cinevva engines guide](https://app.cinevva.com/guides/wechat-mini-game-engines)
- Cocos: $50M Series B (Apr 2022, older fact) from CCB Trust, GGV and Agora to "go beyond games"; reportedly powered ~60% of China's mini games (older CB Insights figure) — [TechCrunch](https://techcrunch.com/2022/04/11/cocos-engine-series-b-50-million-china/amp/); [Yicai](https://www2.yicaiglobal.com/news/game-engine-developer-cocos-closes-funding-round-worth-usd50-million)
- Douyin mini games: ~170M MAU, with 2025 revenue up ~100% (third-party guide) — [Cinevva platforms](https://app.cinevva.com/zh-CN/guides/china-mini-game-platforms)

### Inferences
- Configurators are a small but sticky B2B SaaS market. The money sits in enterprise contracts like Threekit, not in Shopify apps.
- Award-site 3D is a craft market concentrated in maybe 10–20 studios. It works as a showcase and benchmark, not as volume.
- China's mini-game segment is the largest monetized "web-tech 3D/2D" market by far (~$7–8B), and it runs on Cocos and Laya, not three.js.

### Gaps
- No official Awwwards 2025 SOTY page was fetched, so the Lando Norris and Messenger claims are unverified.
- No reliable Cocos vs. Laya share data for 2025 exists. An "87% of TOP100" figure appeared only in an unsourced Kimi page and was excluded.
- No confirmed facts on Resn, 14islands, Apple, or Nike web-3D pages. **[bg]** leads: Bruno Simon portfolio https://bruno-simon.com ; three.js showcase https://threejs.org ; Lusion https://lusion.co ; Active Theory https://activetheory.net ; Immersive Garden https://immersive-g.com ; Resn https://resn.co.nz ; 14islands https://14islands.com ; R3F https://r3f.docs.pmnd.rs
- No reliable Web-3D-overall market size was found.

---

## Q2. Blender: film, ads, archviz, e-commerce, and AI pipelines

### Takeaway
*Flow* (2024) won the Oscar for Best Animated Feature at the 97th Academy Awards (Mar 2025) after being made in Blender and rendered in EEVEE by a small indie team. That made it the flagship proof that Blender reaches the top of film. In AI, Blender has become the default substrate for procedural synthetic data (Infinigen, BlenderProc) and for LLM agents (BlenderMCP; an official Blender Lab MCP server in 2026).

### Cited Findings
- *Flow* (dir. Gints Zilbalodis): made by a small independent team on a limited budget and rendered in EEVEE. The director switched to Blender in 2019 for EEVEE's real-time lighting and camera work — [Blender.org interview](https://www.blender.org/?p=93732); [HTC Vive blog](https://blog.vive.com/us/flow-5-free-lessons-from-an-award-winning-blender-animation)
- *Flow* won Best Animated Feature at the 97th Oscars, described as the first winner made entirely in Blender (secondary repost) — [forum repost](https://forum.agnos.is/topic/980dfa69-5df1-4f09-95ef-fc08677f4076/oscar-winning-animated-film-flow-created-entirely-with-free-and-open-source-software-blender/72)
- Infinigen (Princeton, CVPR 2023): a procedural photorealistic world generator built on Blender (BSD license). It outputs depth, normals, optical flow, segmentation and boxes — [arXiv 2306.09310](https://arxiv.org/pdf/2306.09310)
- Infinigen Indoors (CVPR 2024) exports scenes to Omniverse and Unreal for embodied-agent training; Infinigen-Sim adds articulated objects — [arXiv 2406.11824](https://arxiv.org/html/2406.11824v1)
- BlenderProc is the common research library for Blender-based synthetic data — [Initium/Uni-Obuda survey PDF](https://initium.uni-obuda.hu/wp-content/uploads/2026/02/Data-Generation-for-Robotics-and-AI-Systems.pdf)
- A synthetic data pipeline for manufacturing SMEs' visual assembly control (2025) — [arXiv 2509.13089](https://arxiv.org/pdf/2509.13089)
- BlenderMCP (community; Siddharth Ahuja, integrated with CSM.ai): a socket server addon plus an MCP server. PyPI latest is 1.5.6 (Mar 18, 2026). Its `execute_blender_code` tool runs unsandboxed Python, and security PRs had gone unmerged for 60+ days — [PyPI stats](https://pepy.tech/projects/blender-mcp); [ChatForest review](https://chatforest.com/reviews/blender-mcp-server/); [CSM academy](https://csm.ai/academy/text-to-4d-with-blender-mcp)
- Official Blender Lab MCP server at projects.blender.org/lab/blender_mcp: v1.0.0 on Apr 27, 2026 and v1.0.3 on Sep 11, 2026 (per a vendor blog, not confirmed on blender.org) — [StraySpark](https://www.strayspark.studio/blog/official-blender-mcp-server-comparison-2026)
- Blender 5.2 LTS was released Jul 14, 2026 (per the same vendor blog) — [StraySpark](https://www.strayspark.studio/blog/tag/blender-5-2)

### Inferences
- Blender's AI role is twofold. It renders synthetic data, and it is the most popular "LLM drives a DCC tool" target, because its Python API is complete and it is free to run headless at scale.

### Gaps
- *Flow*'s budget figure was not found. **[bg]** ~€3.5M is widely reported; verify via Variety or Cartoon Brew.
- No sourced data on Blender in ads, packshots or archviz (e.g. Blender Studio, the Blender Development Fund corporate members such as Epic/NVIDIA/AMD, or e-commerce render farms). This needs a dedicated search.
- No named robotics company was confirmed to use Blender as its core data pipeline. Isaac Sim (not Blender-based) dominates vendor lists.

---

## Q3. Unreal / Unity beyond games

### Takeaway
Unreal has won automotive HMI (35+ car models, more than 2M cars, by Epic's figures) and virtual production. It monetizes non-game use through a $1,850/seat/yr subscription for companies with more than $1M in revenue. Unity Industry is small (~$58M estimated, older figure) inside ~$1.85B total Unity revenue (2025). China's digital-twin leader 51WORLD listed in Hong Kong in Dec 2025.

### Cited Findings
- Unreal non-game licensing: the Unreal Subscription costs $1,850/seat/yr for non-game companies with more than $1M in annual revenue; it applies to in-car infotainment developers; games keep the 5% royalty above $1M; Twinmotion is $445/yr and RealityCapture $1,250/yr (from late April 2024, UE 5.4) — [Epic blog](https://www.unrealengine.com/blog/we-are-updating-unreal-engine-twinmotion-and-realitycapture-pricing-in-late-april); [Engadget](https://www.engadget.com/epic-will-charge-non-game-developers-1850-per-seat-to-use-unreal-engine-162015997.html)
- Automotive HMI (Epic, Oct 9 2025): 35+ car models shipped with UE HMI, covering Ford, GM, Rivian (R1T showcase), Geely, Lotus, Lincoln and Volvo; more than 2M cars on the road. Lotus HMI includes an interactive digital twin of the car. Epic also provides an HMI template and an Android multi-display service — [Epic news](https://www.unrealengine.com/en-US/news/five-years-35-car-models-how-unreal-engine-is-accelerating-hmi-innovation) (vendor figures; page 403'd on fetch, details are from the search snippet); [Epic HMI page](https://www.unrealengine.com/uses/hmi)
- Unity in cars: the Mercedes-Benz VISION EQXX concept interior was powered by Unity (GTC 2022, concept car, older fact) — [Unity blog](https://unity.com/en/blog/industry/screens-are-the-new-horsepower-leading-luxury-auto-brand-innovates-with-unity)
- Unity FY2025 revenue was ~$1.85B (+2%) — [Macrotrends](https://www.macrotrends.net/stocks/charts/U/unity-software/revenue). Unity Industry costs $4,950/yr per seat, with revenue estimated at ~$58M and described as the "fastest growing SKU" (undated, ~2024 analyst piece) — [Constellation Research](https://www.constellationr.com/insights/news/unity-software-scales-digital-twin-business)
- Virtual production market estimates for 2025 range from $2.84B (to $12.25B by 2033) to $3.39B, with the LED-volume segment at $2.1B. They conflict, so treat them as directional — [GII/Grand View](https://www.giikorea.co.kr/report/grvi1474942-virtual-production-market-size-share-trends.html); [Market Intelo](https://marketintelo.com/report/led-volume-virtual-production-market/amp); [MarketsandMarkets US: $242.5M 2025](https://www.marketsandmarkets.com/Market-Reports/geography/virtual-production-market/US)
- market.us claims more than 42% of studios had adopted real-time engines/LED volumes and that 780+ productions used them in 2025 (low-reliability analyst claim) — [market.us](https://market.us/report/virtual-production-market/)
- Digital humans in broadcast: TelevisaUnivision's TUDN used MetaHumans driven by live data for 2022 World Cup analysis (IBC 2023 paper; SMPTE journal 2024) — [IBC](https://ibc.org/technical-papers/ibc2023-tech-papers-using-metahumans-in-large-scale-sports-production/10279.article); [disguise whitepaper](https://www.disguise.one/en/insights/whitepaper/using-metahumans-large-scale-sports-production)
- MetaHuman Creator was fully embedded in UE5 (State of Unreal 2025) and is included in the standard UE license — [metahuman.com](https://www.metahuman.com/llms.txt)
- Automotive digital twin market: $2.1B in 2024 and $2.7B in 2025 (GMI), versus >$5.56B in 2025 (R&M). They conflict — [GMI](https://www.gminsights.com/industry-analysis/digital-twin-in-automotive-market); [Research and Markets](https://www.researchandmarkets.com/reports/6176272/digital-twins-in-automotive-market-report)
- **China, 51WORLD (五一视界):** ¥2 亿 Pre-IPO round (Aug 2024); listed on HKEX (6651) on Dec 30, 2025, raising HK$7.31 亿 and calling itself "first Physical AI listco"; H1 2026 revenue ¥1.24 亿 (+130%), with 51Sim (simulation/synthetic data) at 41%; deployed in 100+ cities and ~1000 government/enterprise clients — [投资界](https://news.pedaily.cn/202408/538663.shtml); [36氪](https://eu.36kr.com/zh/p/3617745678468103); [Bamboo Works](https://thebambooworks.com/?p=65680); [新华网 2025-04](https://www.news.cn/tech/20250411/1e6aa154be274664a67547557a08bd51/c.html)

### Inferences
- Non-game engine revenue is real but small next to games. Epic monetizes it via seats, and Unity via Industry seats plus services. Automotive HMI is the clearest case where Unreal won at scale and Unity lost ground.
- In China, digital twin and simulation (51WORLD, which historically built on UE, though this was not confirmed in these sources) is the domestic analogue of "engines beyond games".

### Gaps
- No sourced data on The Mandalorian/StageCraft (**[bg]** ILM StageCraft, 2019, UE4 at launch), Unreal broadcast cases from 2024–2026 (Fox Sports, Weather Channel), or Chinese OEM HMI cases (e.g. Unreal in 吉利/极氪, Unity China/团结引擎 in 理想/蔚来 HMI). All need targeted search.
- Unity does not break out Unity Industry revenue in 2025 filings. Epic does not disclose non-game revenue.

---

## Q4. "LLM writes 3D/visual code" products

### Takeaway
There are three clusters: (a) agents that drive DCC tools via MCP (BlenderMCP; official Blender Lab MCP; Unity/Unreal MCPs); (b) prompt-to-playable-web-game platforms that emit three.js (Rosebud, plus generic vibe-coders like Bolt, Lovable and v0); and (c) asset-generation companies moving toward agents and engine plugins. Meshy is the money leader: a ~$400M Series B at a $1.5B valuation (Jul 2026), 12M+ users, and ARR up ~12x YoY (company figures).

### Cited Findings
- Rosebud AI (SF, YC 2019): turns text into code into a playable game; generated code is JS, three.js and React; three.js is the only renderer. Funding is reported as ~$9.2M (PitchBook) or $9–13M (Dealroom), and conflicts with the $1.5M on SeedTable. Do not confuse it with Rosebud the journaling app ($6M, Jun 2025) — [Dealroom](https://app.dealroom.co/companies/rosebud_ai); [PitchBook](https://pitchbook.com/profiles/company/343168-12); [MVPable review](https://mvpable.com/tool/rosebud); [TechCrunch (journaling Rosebud)](https://techcrunch.com/2025/06/04/rosebud-lands-6m-to-scale-its-interactive-ai-journaling-app/)
- Meshy: ~$400M Series B at a $1.5B valuation (Jul 2026, the largest AI-3D round); 12M+ registered users; 100M+ models; ARR ~12x YoY; a 3D Agent exports to Unity, Unreal and Blender — [AAP/Cision release](https://www.aap.com.au/aapreleases/cision20260721ae06857/); [3D Printing Industry](https://3dprintingindustry.com/news/meshy-raises-nearly-400m-at-1-5b-valuation-in-largest-ai-3d-round-to-date-253294/)
- Tripo has a web app plus a Blender plugin, Pro from $19/mo; no reliable funding or user data was found — [MyArchitectAI roundup](https://www.myarchitectai.com/it/blog/blender-ai)
- BlenderMCP and the official Blender Lab MCP: see Q2 — [StraySpark](https://www.strayspark.studio/blog/official-blender-mcp-server-comparison-2026)
- Spline AI (text/image to 3D scene) and Spline's AI-focused funding: see Q1 — [Pulse 2.0](https://pulse2.com/spline-collaborative-3d-design-platform-company-secures-10-million-series-a)
- An AI-native engine aimed at WeChat mini games (Cinevva) positions itself against Cocos (vendor content) — [Cinevva vs Cocos](https://app.cinevva.com/guides/cinevva-vs-cocos); [Cinevva blog 2026-07-19](https://app.cinevva.com/zh-CN/blog/2026-07-19-ai-engine-wechat-mini-games)
- Bolt, Lovable and v0 comparisons don't mention three.js. They are positioned as SaaS-MVP and UI generators — [Techsy](https://techsy.io/en/blog/lovable-vs-bolt-vs-v0)

### Inferences
- Capital in "AI × 3D" is flowing to asset generation (Meshy) far more than to code-as-3D. Code-as-3D is mostly open-source MCP glue plus small startups (Rosebud), and general vibe-coding tools produce three.js only incidentally.
- The official Blender MCP (2026) signals that DCC vendors now treat LLM agents as first-class clients.

### Gaps
- No sourced evidence that Bolt, Lovable or v0 market three.js generation. No data on Unity AI / Muse or Unreal's AI assistant, or Chinese code-to-3D startups (e.g. 腾讯混元3D, VAST/Tripo, 影眸 Rodin engine plugins). These need follow-up.
- Market sizing for "AI 3D generation" was not found from a reliable source.

