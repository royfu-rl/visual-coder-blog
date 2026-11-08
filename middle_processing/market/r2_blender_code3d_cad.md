# Blender's commercial footprint and "code as 3D" businesses (agentic DCC, LLM-written 3D code, text-to-CAD), as of 2026-10-13

This file fills gaps in `web3d_engines.md`. Facts already covered there are not repeated: Flow's Oscar and EEVEE use, Infinigen basics, BlenderMCP's PyPI and security notes, Meshy, Rosebud and Spline's funding. Backflip's $30M Series A is in `3d_asset_gen.md`.

**Method**
- About 90 tool calls: about 75 WebFetch, about 12 WebSearch, plus GitHub API calls and a PDF parse.
- The WebSearch budget is shared across the session, and it ran out mid-task several times. Many facts therefore come from fetching primary URLs directly (blender.org, vendor sites, GitHub API, arXiv).

**Source-type tags**
- **[official]**: the organization's own page or filing
- **[vendor]**: the company's own marketing about itself
- **[press]**: trade or news press
- **[3rd]**: a third-party blog, aggregator or data tracker
- **[API]**: GitHub API, read live on 2026-10-13
- **[bg]**: background knowledge, not re-verified

---

## Q1. Blender Development Fund: corporate members, amounts, total revenue

### Takeaway
- Blender Foundation income in 2024 was €3.106M, up from €2.553M in 2023.
- Corporate Patrons paid €1.17M of that, or 38%. Their share fell from 47%, while individual and small donations rose to about 40%.
- The Patron tier has risen from about €120k/yr (2019–22) to about €240k/yr (2024–26), roughly four developer salaries.
- The fund currently shows about $327k per month from 46 corporate and 7,655 individual supporters, which is roughly €3.9M/yr annualized.
- AI money is politically toxic in the community. Anthropic's €240k/yr Patron membership (Apr 28, 2026) was downgraded to a one-off donation within a week.

### Cited Findings
**Totals (2024 annual report, published Sep 2025) [official]**
- Total income: €3,106,361 in 2024, against €2,553,392 in 2023 — [Blender Foundation Annual Report 2024 PDF](https://download.blender.org/foundation/Blender-Foundation-Annual-Report-2024.pdf)
- Income breakdown, 2024 (2023 in parentheses), same source:
  - Dev Fund Patron: €1,172,704, 38% (€1,193,261, 47%)
  - Dev Fund Corporate (non-Patron tiers): €355,495, 11% (€256,209, 10%)
  - Dev Fund Individuals: €612,402, 20% (€404,916, 17%)
  - Blender Market (now Superhive): €132,653, 4% (€149,556, 6%)
  - Other large donations: €214,322, 7%
  - Generic small donations: €618,785, 20% (€263,256, 10%)
- Expenses, 2024:
  - Staff and grants made up 87% (€2.713M)
  - Developer contributions were €2.153M, up from €1.777M
  - Developer grants were €564,598
  - The reservation was negative (−€73,853)
  - The report notes that "some companies decided to not renew in 2024, but other new members joined" — [same PDF](https://download.blender.org/foundation/Blender-Foundation-Annual-Report-2024.pdf); [CGPress, 2025-09-16](https://cgpress.org/archives/blender-foundation-reports-higher-donations-but-warns-of-low-reserves-in-2024-annual-report.html) [press]
- Usage scale: about 21M downloads from blender.org in 2024, plus about 2M from Microsoft Store, Steam and Snap. The site had about 30M unique visitors a year, and 7,000+ people answered the first user survey (Oct 2024) — [Annual Report 2024 PDF](https://download.blender.org/foundation/Blender-Foundation-Annual-Report-2024.pdf) [official]
- Members contribute engineers as well as money:
  - AMD funds a small team for Cycles HIP, Hydra and MaterialX
  - Apple ported Blender to Metal
  - Intel works on oneAPI
  - NVIDIA has two developers on OSL and USD — [same PDF, p.73](https://download.blender.org/foundation/Blender-Foundation-Annual-Report-2024.pdf) [official]

**Live fund page (read 2026-10-13) [official]**
- $326,902 per month, 7,655 individual members, 46 corporate members. Note: the page shows "$", but its activity feed uses €.
- Corporate Patrons: Aras Pranckevičius, NVIDIA, Netflix Animation Studios, Qualcomm, Wacom, PICO, Bolt Graphics
- Corporate Gold: Arrowhead, Facebook/Meta, Chaos, Dell, Superhive, BlenderKit, Adobe — [fund.blender.org](https://fund.blender.org/)
- Epic, AMD, Apple, Intel and AWS are not in the current Patron list. Either they did not renew or they sit in other tiers; the page does not say.

**Per-company amounts and dates [press, mostly CG Channel]**

| Company | Date | Tier / amount | Source |
|---|---|---|---|
| Epic Games | Jul 2019 | $1.2M MegaGrant over 3 years (not a tier); €10k in 2014 | [CG Channel tag p3](https://www.cgchannel.com/tag/blender-development-fund/page/3/) |
| Ubisoft | Jul 22 2019 | Gold, €30k/yr; Ubisoft Animation Studio "will use Blender for its productions" | [blender.org press](https://www.blender.org/press/ubisoft-joins-blender-development-fund/) [official]; [CG Channel p2](https://www.cgchannel.com/tag/blender-development-fund/page/2/) |
| NVIDIA | Oct 2019 | Patron, €120k/yr | [CG Channel 2019](https://www.cgchannel.com/2019/10/nvidia-backs-blender-development/) |
| AMD | Oct 2019 | $120k/yr | [CG Channel p2](https://www.cgchannel.com/tag/blender-development-fund/page/2/) |
| Microsoft | Jul 2020 | €30k/yr | same |
| Unity | Aug 2020 | $120k/yr | same |
| Facebook/Meta | Nov 2020 | Patron, $120k+/yr | [CG Channel 2020](https://www.cgchannel.com/2020/11/facebook-becomes-corporate-patron-of-blender/) |
| AWS | Dec 2020 | Patron, ≥€360k (period not stated) | [CG Channel p2](https://www.cgchannel.com/tag/blender-development-fund/page/2/) |
| Adobe | Jul 2021 | Gold, €30k/yr | same |
| Apple | Oct 2021 | Patron, amount undisclosed | same |
| Intel | Dec 2021 | Patron, ≥€120k/yr | same |
| Volkswagen | Oct 2022 | ≥€120k/yr | [CG Channel p1](https://www.cgchannel.com/tag/blender-development-fund/) |
| Otoy | Feb 2024 | Patron, ≥€240k/yr | same |
| Chaos (V-Ray/Corona) | Jul 2025 | €30k/yr | same |
| Wacom | Aug 2025 | Patron, €210k/yr per CG Channel | same |
| Bolt Graphics | Sep 2025 | Patron, €240k/yr | same |
| Dell | Jan 23 2026 | €30k/yr | same |
| Netflix Animation Studios | Jan 27 2026 | Patron, ≥€240k/yr ("first major animation studio" to back Blender) | [blender.org press](https://www.blender.org/press/netflix-animation-studios-joins-the-blender-development-fund-as-corporate-patron/) [official]; [CG Channel](https://www.cgchannel.com/2026/01/netflix-donates-e240000year-to-the-blender-development-fund/) |
| Arrowhead (Helldivers 2) | Feb 2026 | €30k/yr | [CG Channel p1](https://www.cgchannel.com/tag/blender-development-fund/) |
| Anthropic | Apr 28 2026 | Patron, €240k/yr, aimed at the Python API. Downgraded to a one-off donation (amount undisclosed) after backlash; logo removed | [CG Channel 2026-04-29](https://www.cgchannel.com/?p=175735); [blender.org press](https://www.blender.org/press/anthropic-joins-the-blender-development-fund-as-corporate-patron/); [blender.org "Upcoming Dev Fund and AI Policies"](https://www.blender.org/news/upcoming-blender-development-fund-and-ai-policies/) [official] |

- Khara joined as Corporate Silver and its subsidiary Project Studio Q as Bronze (2019). Amounts were not given — [Neowin/ANN via search](https://www.neowin.net/news/anime-studio-khara-is-planning-to-use-open-source-blender-software/) [press]

**Governance and AI stance [official]**
- Francesco Siddi became chairman and CEO on Jan 1, 2026; Ton Roosendaal moved to the supervisory board — [blender.org press 2025-09-17](https://www.blender.org/press/blender-foundation-announces-new-board-and-executive-director/)
- After the Anthropic episode, the Foundation said Blender "is made by humans for humans" and that "no generative AI functionality is currently available or planned for integration." AI policy drafts will be discussed publicly — [blender.org](https://www.blender.org/news/upcoming-blender-development-fund-and-ai-policies/)
- Anthropic's own post (Apr 28; updated May 1, 2026) says the donation supports Blender's Python API — [Anthropic](https://www.anthropic.com/news/claude-for-creative-work) [vendor]

### Inferences
- Blender's whole core budget (about €3M) is smaller than one mid-size AI-3D seed round. Corporate money buys hardware-vendor backends (Metal, HIP, oneAPI, OptiX) more than features.
- The Anthropic reversal shows that Blender will tolerate LLM agents *using* Blender over MCP and Python. It will not allow *generative AI inside Blender* or AI-lab branding. "Code-as-3D" businesses must therefore live outside Blender: as add-ons, MCP servers or cloud services. That also means no official in-app LLM competitor is coming from the Foundation.

### Gaps
- No 2025 annual report was found; it is presumably due around Sep–Nov 2026.
- Current amounts for Qualcomm and PICO were not found. Whether Epic, AMD, Apple, Intel, Unity and AWS still contribute is unconfirmed; they are absent from the current Patron list.
- Anthropic's one-off donation amount was not disclosed.

---

## Q2. Blender in shipped productions, archviz/product viz share, Superhive, and 5.x automation features

### Takeaway
- Blender's production footprint is broad but mostly indie or mid-tier. Examples include Flow, Wolfwalkers, Next Gen, Maya and the Three, RRR VFX, Ubisoft's Rabbids, Khara, Grease Pencil in Across the Spider-Verse, and A24's Backrooms (2026).
- Netflix Animation Studios' Patron membership (Jan 2026) is the first top-tier studio signal.
- In archviz, Blender is still small: 8% in a 2024 community poll, against 59% for 3ds Max. It is growing fast, though, having doubled from 4% in 2022.
- Superhive (formerly Blender Market) is the clearest creator economy: $52.8M paid to 6,455 creators since 2014.
- Blender 5.x (5.0 Nov 2025, 5.1 Mar 2026, 5.2 LTS Jul 2026, 5.3 with native Gaussian splats) keeps expanding Geometry Nodes into a general programming environment. This makes Blender a stronger target for code-generating agents.

### Cited Findings
**Flow economics (adds to web3d_engines.md)**
- Budget about €3.5M (about $3.6–4M); 15–20 artists (other counts say about 50); EEVEE frames under 10s at 4K on the director's PC — [Film Stories](https://filmstories.co.uk/features/flows-oscar-should-be-an-inspiration-for-indie-filmmakers-everywhere/) [press]; [TheWrap](https://www.thewrap.com/flow-interview-gints-zilbalodis) [press]; [Gold Derby](https://www.goldderby.com/article/2025/flow-movie-punk-ethos-oscars/) [press]
- Box office:
  - About $36M worldwide as of Mar 17, 2025 (Variety via Baltic Times)
  - $30.5M on The Numbers
  - Unifrance: €42.5M cumulative and 8.14M admissions abroad
  - About 10x budget — [Baltic Times](https://www.baltictimes.com/zilbalodis__animated_feature__flow__glosses_over_eur_33_million_worldwide); [The Numbers](https://oak3.the-numbers.com/movie/Flow-le-chat-qui-navait-plus-peur-de-leau-(2024-France)) [3rd]; [Unifrance](https://japan.unifrance.org/ニュース/17244/box-office-international-de-l-animation-francaise-janvier-aout-2025) [official-industry]

**Studios and productions (Wikipedia compiles primary refs) [3rd]**
- Wolfwalkers (2020, partial); Next Gen (2018, entirely Blender, Tangent Animation); Maya and the Three (2021, Netflix); I Lost My Body (2019, Grease Pencil); RRR (Makuta VFX)
- Spider-Man: Across the Spider-Verse (2023): Sony Imageworks used Grease Pencil for line work and 2D FX, plus the Lego sequence by Preston Mutanga
- Backrooms (2026, A24): concept, previs and some full scenes
- SPA Studios (hiring Blender artists since 2021) and Warner Bros. Animation (since 2022) — [Wikipedia: Blender](https://en.wikipedia.org/wiki/Blender_(software))

**Studio adoption stories [official]**
- blender.org user stories: Ubisoft Film & TV *Rabbids Invasion: Mission to Mars* (Jun 2021); Cartoon Saloon *Wolfwalkers* (Mar 2021); Makuta *RRR* (Jun 2022); Blue Zoo (2021); Gentilhomme (Nashville airport, 2023); *Il Baracchino* (Italy's first adult animated series in Blender) — [blender.org user stories](https://www.blender.org/user-stories/)
- Khara (Evangelion) announced on Jul 30, 2019 a move from 3ds Max to Blender after *Evangelion 3.0+1.0*:
  - Reasons: cost (3ds Max was about $2,396 per seat per year), scale, and Grease Pencil
  - Unity fills Blender's gaps
  - 3.0+1.0 itself was mainly 3ds Max — [blender.org](https://blender.org/?p=64752) [official]; [Anime News Network](https://m.animenewsnetwork.com/news/2019-08-18/khara-to-completely-switch-to-blender-open-source-3d-software-after-evangelion-3.0-1.0/.150173) [press]
- Embark Studios: Wikipedia mentions Blender only for designing the studio's interior, and a general "procedural content / ML" emphasis. ARC Raiders (Oct 2025) sold 12M+ copies with a 960k concurrent-player peak — [Wikipedia: Embark](https://en.wikipedia.org/wiki/Embark_Studios) [3rd]. **No source confirms Blender as Embark's main DCC.**

**Archviz / product viz share**
- Community poll by VWArtclub, published on the RebusFarm blog on 2024-12-06 — [RebusFarm](https://rebusfarm.net/blog/the-state-of-3d-modeling-rendering-and-post-production-tools-insights-from-the-archviz-community) [3rd]
  - Modeling share, 2022 → 2024: 3ds Max 58→59%, SketchUp 16→13%, **Blender 4→8%** (1,069 votes in 2024)
  - Render-engine share, 2021 → 2024: Corona 40→43%, V-Ray 35→26%, Unreal 2→4%, **Cycles 2→3%** (1,099 votes)
- CGarchitect's older renderer surveys (2018–2020) did not show Blender in the top 10; V-Ray was at 64.9% in 2020 — [CG Channel 2020](https://www.cgchannel.com/2020/09/cgarchitect-2020-rendering-survey-reveals-trends-in-arch-viz) [press]
- CGarchitect is now part of Chaos and redirects to cgconnect.chaos.com.
- Poliigon "State of 3D 2024" (n=6,251; skews toward archviz): about 87% of 3ds Max and C4D users use them professionally, against "50-ish%" for Blender users — [Poliigon](https://poliigon.com/articles/state-of-3d-2024) (snippet via search; the page returned 403 on fetch) [3rd]

**Superhive (formerly Blender Market, run by CG Cookie)** [vendor, live counter, read 2026-10-13]
- **$52,795,662 paid to creators** since launch on Jun 10, 2014
- 6,455 creators; 5,730,935 items sold; $1,021,222 donated to the Dev Fund
- 71,546 products; creators keep up to 90% — [superhivemarket.com/market-stats](https://superhivemarket.com/market-stats); [about](https://superhivemarket.com/about)
- Blender's annual report shows the market sent the Foundation €132,653 in 2024 — [Annual Report PDF](https://download.blender.org/foundation/Blender-Foundation-Annual-Report-2024.pdf) [official]

**Blender 5.x features relevant to automation [official]**
- **5.0 (Nov 18, 2025)**:
  - Geometry Nodes Bundles and Closures
  - Volume Grid and SDF nodes; Repeat Zones in shader nodes
  - Scenes as assets
  - Inline Shader Nodes Python API
  - ACES 1.3/2.0 and HDR output — [blender.org 5.0](https://www.blender.org/download/releases/5-0/)
- **5.2 LTS (Jul 14, 2026; supported to Jul 2028)**:
  - Node-based XPBD cloth and hair
  - GN Lists, string fields, PCA nodes, recursive closures
  - Remote asset libraries
  - Python API:
    - `bpy.data.all_ids`
    - `gpu.init()` for GPU in background mode
    - `Window.screenshot` returns pixels without saving to disk, which is useful for agent "look" loops
  - Breaking change: GN modifier inputs became RNA properties — [blender.org 5.2](https://www.blender.org/download/releases/5-2/)
- **5.3**: native Gaussian splat support — [CGconnect, Sep 2026](https://cgconnect.chaos.com/insights/articles/7d0cb288-blender-5-3-gets-gaussian-splats-ai-agents-enter-3d?from=cgarchitect) [press, Chaos-owned]

### Inferences
- In 2026 Blender wins on *cost and scriptability*, not on top-studio pipelines. Indie features, 2D/3D hybrid work, mid-tier TV and agencies all fit that pattern.
- Netflix becoming a Patron is the first sign that a top studio is moving.
- For "code as 3D", Blender's growing node and Python surface plus headless GPU rendering (5.2 `gpu.init()`) make it the most programmable free renderer. Archviz remains locked to 3ds Max plus Corona/V-Ray, owned by Autodesk and Chaos. An LLM-driven archviz product would most plausibly target Blender or SketchUp first.

### Gaps
- No sourced data on ad agencies' product CGI in Blender; the search budget was exhausted. **[bg]** leads: Ian Hubert, and the many Blender product-viz freelancers on ArtStation and Behance.
- No reliable ArtStation software-share statistic.
- No confirmed facts on Ubisoft Animation Studio's 2024–26 status, or on Geometry Nodes procedural-asset businesses beyond Superhive. **[bg]** leads: Erindale, BlenderKit (Gold member), Kit Bash 3D.

---

## Q3. Code-as-3D / agentic 3D: MCP servers, DCC vendor assistants, research, viral demos

### Takeaway
- By mid-2026 "LLM drives a DCC via code" became an official vendor feature everywhere:
  - Blender Lab MCP (v1.0, Apr 2026) and Anthropic's Claude creative connectors (Blender, Autodesk Fusion, SketchUp, Adobe; Apr 28, 2026)
  - Unity's free MCP, CLI and plugin, plus a credit-based AI Assistant
  - Epic's experimental Unreal MCP plugin (UE 5.8)
  - SideFX Houdini 22 MCP for APEX Script
  - Maxon Cinema 4D's built-in MCP server (Oct 2026)
  - Autodesk Assistant, generally available across Fusion, Forma and Flow
- The open-source BlenderMCP (now "mcp-for-blender") is the largest community project: 30.6k GitHub stars and about 490k PyPI downloads per month.
- Almost none of this is directly monetized. Vendors give MCP away to drive seat sales, and the community servers are free.

### Cited Findings
**Blender MCPs**
- ahujasid/blender-mcp, renamed **ahujasid/mcp-for-blender**: **30,585 stars, 2,767 forks**, created 2025-03-07 — [GitHub API](https://api.github.com/repos/ahujasid/mcp-for-blender) [API]
  - PyPI: 3.53M all-time downloads, **~490k in the last 30 days**; v2.0.0 on Sep 16, 2026 — [pepy.tech](https://pepy.tech/projects/blender-mcp) [3rd-stats]
  - Features: `execute_blender_code`, a `look` tool (viewport, render, wireframe), `BLENDER_MCP_SAFE_MODE`
  - Integrations: Poly Haven, Sketchfab, Poly Pizza, and Hyper3D Rodin, Hunyuan3D and Tripo generation
  - Clients: Claude, Codex, Cursor, VS Code, Antigravity — [GitHub README](https://github.com/ahujasid/blender-mcp) [official-repo]
- **Official Blender Lab MCP**: add-on v1.0.3, requires Blender 5.1+
  - Use cases: scene analysis, renaming, data-relation queries, explaining Geometry Nodes
  - The page warns it "will execute LLM generated code in Blender without any guards" — [blender.org/lab/mcp-server](https://www.blender.org/lab/mcp-server/) [official]
  - Version history (v0.1.0 Mar 24 → v1.0.0 Apr 27 → v1.0.3 Sep 11, 2026) comes from a competing vendor's blog — [StraySpark](https://www.strayspark.studio/blog/official-blender-mcp-server-comparison-2026) [3rd]
- **Anthropic "Claude for Creative Work"** (Apr 28, 2026): connectors for Blender (MCP to the Python API), **Autodesk Fusion** ("create and modify 3D models through conversation", requires a Fusion subscription), **SketchUp** ("turn a conversation into a 3D modeling starting point"), Adobe (50+ tools), Affinity, Ableton, Resolume and Splice — [Anthropic](https://www.anthropic.com/news/claude-for-creative-work) [vendor]

**Other DCC and engine vendors**
- **NVIDIA SIGGRAPH 2026** (Jul 20, 2026):
  - A blueprint integrating Omniverse libraries with Blender for NemoClaw agents
  - **Houdini 22 adds MCP via APEX Script** (LLMs generate procedural rig code)
  - Unreal Editor connects to AI clients via MCP
  - Foundry Griptape supports MCP with Blender and Nuke
  - Nous Research's Hermes Agent added Blender — [NVIDIA blog](https://blogs.nvidia.com/blog/siggraph-news-2026/) [vendor]
- **Unreal Engine 5.8**: an experimental first-party "Unreal MCP" plugin, local only (127.0.0.1:8000/mcp), with no authentication — [SEELE guide, Jul 2026](https://www.seeles.ai/resources/blogs/de/unreal/unreal-engine-ai-assistant-ue-5-8-mcp-setup-and-safety-bcc63ed46d) [3rd; Epic primary docs not fetched]
- Community Unreal MCPs (GitHub stars):
  - chongdashu/unreal-mcp: 2,094
  - flopperam/unreal-engine-mcp: 1,098
  - ChiR24/Unreal_mcp: 921 — [GitHub search API](https://api.github.com/search/repositories?q=unreal+mcp) [API]
- **Unity AI** (beta) — [unity.com/products/ai](https://unity.com/products/ai) [vendor]
  - In-Editor Assistant uses credits and is included in Pro, Enterprise and Industry; Personal trial converts to $10/mo
  - **AI Gateway** lets you bring your own third-party agent without spending Unity credits
  - The **MCP server via CLI is free**; the official plugin for Claude Code, Codex and Grok is free (Unity 6+)
  - Community CoplayDev/unity-mcp: **14,886 stars**; IvanMurzak/Unity-MCP: 4,424 [API]
- **Maxon Cinema 4D**: a built-in MCP server lets ChatGPT and Claude organize objects and materials and prepare renders, UVs and animation (Oct 7, 2026) — [CGconnect](https://cgconnect.chaos.com/insights/articles/a0f12d9e-chatgpt-can-now-control-cinema-4d?from=cgarchitect) [press]
- **Autodesk (AU 2026, Sep 15, 2026)** — [Autodesk press release](https://adsknews.autodesk.com/en/pressrelease/autodesk-advances-agentic-ai-in-its-three-industry-clouds/); [Autodesk news](https://adsknews.autodesk.com/en/news/autodesk-ai-design-manufacturing-au-2026/) [vendor]
  - Autodesk Assistant is generally available across Fusion, Forma and Flow
  - A next-generation Assistant is in preview, with a standalone version, Assistant Builder (bring your own agents) and an AI Orchestrator. Pricing and rollout will be announced in 2027.
  - Fusion: AutoTimeline (imported geometry to editable parametric parts), AutoAssemble, AutoConstrain
  - Inventor Assistant drives the Inventor API and iLogic
  - Maya MotionMaker was named a 2026 Fast Company "Next Big Thing" (Oct 6, 2026) — [Autodesk news](https://adsknews.autodesk.com/en/news/motionmaker-maya-fast-company-next-big-things-in-tech/) [vendor]
- Houdini, Maya and Fusion community MCPs (GitHub stars):
  - capoomgit/houdini-mcp: 305; healkeiser/fxhoudinimcp: 332
  - PatrickPalmer/MayaMCP: 108
  - Fusion 360 MCPs: ≤127
  - neka-nat/freecad-mcp: 2,831
  - Onshape MCPs: ≤175 — [GitHub search API](https://api.github.com/search/repositories) [API]

**Web and no-code 3D with AI**
- **Spline AI V2**: text- or image-to-3D (choice of generation models), exports GLB, and publishes to web, Swift or Kotlin — [spline.design/ai](https://spline.design/ai) [vendor]
  - Pricing: Hobby $12–15, Pro $25–30, Max $60–70 per seat per month, with 2k/3k/10k AI credits — [spline.design/pricing](https://spline.design/pricing) [vendor]
  - No user or revenue numbers were found.
- **Womp**: free browser modeler with text-to-3D, an integrated 3D-print order flow, and a Pro tier. No user or funding data on the site — [womp.com](https://womp.com/) [vendor]
- **Promethean AI**: claims 10,000+ users including PlayStation Studios, backed by Disney Accelerator, with an Unreal-first plugin. The site footer is still "© 2024", so its 2026 status is unclear — [prometheanai.com](https://www.prometheanai.com/) [vendor]
- **Esri CityEngine** (rule-based CGA procedural cities) is bundled only in ArcGIS Professional and Professional Plus user types; no standalone price on the page — [Esri](https://www.esri.com/en-us/arcgis/products/arcgis-cityengine/buy) [vendor]

**Viral "LLM writes three.js" and the vibe-coded game economy**
- **fly.pieter.com** (levelsio):
  - "100% made with AI", credited to Cursor and three.js
  - Sells in-game ads claiming "100,000+" reach; the F-16 costs $29.99 — [fly.pieter.com](https://fly.pieter.com/) [vendor]
  - **[bg]** Widely reported to have hit about $1M ARR in early 2025 from ads. Not verified this session.
- **Vibe Jam 2026** (organized by levelsio): ≥90% AI-written code, browser-only, three.js recommended; Apr 1 – May 1, 2026; $50k+ prizes
  - Sponsors: Cursor, Bolt.new, Glif, Tripo3D
  - The 2025 jam paid $17.5k — [vibejam.com](https://vibejam.com/) [official]
- Other demos — [search summary: Digg](https://digg.com/ai/cp2hu6bo); [Developers Digest](https://www.developersdigest.tech/blog/gpt-6-threejs-world-in-minutes); [aireiter](https://aireiter.com/blog/3d-website-prompts) [3rd, low reliability]
  - Karpathy shared a Claude Opus three.js "Lord of the Rings" scene (via Digg)
  - A GPT-6 / Codex walkable four-room three.js world (Developers Digest)
  - In a Jul 2026 test, claude-sonnet-5 produced 5 of 6 working one-prompt three.js pages (aireiter)
  - A Nov 2025 Gemini 3 vs GPT-5.1 vs Claude three.js Rubik's-cube comparison (social post)
  - None of these view counts were verified.
- three.js: **116,329 stars** [API]

**Research → product (code-as-3D lineage)**
- **SceneCraft** (Google; arXiv 2403.01248, Mar 2024): an LLM agent writes Blender Python, using scene-graph constraints and GPT-V critique, for scenes of up to about 100 assets. It also uses a library-learning mechanism — [arXiv](https://arxiv.org/abs/2403.01248)
- **3D-GPT** (Chuny1/3DGPT, Oct 2023): an LLM drives Infinigen's procedural functions. 857 stars [API]
- **BlenderGym** (Gu, Huang, Je, Yang, Guibas; CVPR 2025 Highlight; arXiv 2504.01786): a VLM benchmark for Blender graphics editing
  - The top systems "struggle with tasks relatively easy for human Blender users"
  - Inference scaling helps, and the verifier can be scaled too — [arXiv](https://arxiv.org/abs/2504.01786); [repo](https://github.com/richard-guyunqi/BlenderGym-Open) (45 stars)
- **LL3M** ("Large Language 3D Modelers"; threedle lab, UChicago assets): multi-agent Blender code generation with BlenderRAG and visual self-critique. 555 stars. The README says the Claude 3.7 model it used is retired and the hosted server discontinued — [project page](https://threedle.github.io/ll3m/); [GitHub](https://github.com/threedle/ll3m)
- **Infinigen** (Princeton): 7,320 stars; the latest work is ProcFunc (2026, arXiv 2604.26943) and Infinigen Articulated (2025). BSD-licensed, with no stated commercial spinout — [infinigen.org](https://infinigen.org/); [API]
- **BlenderProc**: 3,744 stars [API]

### Inferences
- Code-as-3D became a *distribution channel* for incumbents rather than a business. Every DCC now ships or blesses an MCP so that Claude, ChatGPT, Codex and Cursor drive *their* seats. Unity explicitly lets outside agents in for free through AI Gateway.
- Standalone opportunity remains in two places:
  - (a) paid, hardened MCP and plugin layers (StraySpark-style Unreal/Blender servers with 400+ tools; Unity credits)
  - (b) vertical outputs where code is the deliverable: CAD (Q4), configurators, and web games (Rosebud, Vibe Jam's ecosystem)
- The academic line (SceneCraft → BlenderGym → LL3M) shows that VLM "look-and-fix" loops are the key technique. Vendors productized it: BlenderMCP `look`, Zookeeper snapshots, Unity "verify changes", and Blender 5.2 `Window.screenshot`.

### Gaps
- No official Epic page for the UE 5.8 MCP plugin was fetched.
- No numbers on Unity AI revenue or credit consumption.
- SideFX does not mention AI or MCP on its own H22 pages; the NVIDIA blog is the only source.
- Spline, Womp and Promethean have no user, revenue or funding data in 2026.
- Viral-demo view counts and origin posts were not verified.
- **CADGPT** could not be identified as a distinct company. The name is used generically by several tools.

---

## Q4. Text-to-CAD and AI CAD: Zoo, Adam, Leo, Backflip, incumbents, China

### Takeaway
Text-to-CAD is where code-as-3D has the clearest per-unit pricing.

**Startups**
- **Zoo** (formerly KittyCAD) has metered Text-to-CAD since Jan 2024 ($0.50 per minute). Its 2026 Zookeeper agent writes Zoo's **KCL** code: Free gives $10 of credit, Plus is $20, Pro is $99/mo. Its funding is small (about $5M seed in 2023; about $10–11M total per trackers).
- **Adam** (YC W25) raised a $4.1M seed (TQ Ventures, Oct 2025). Users had generated 1M+ models. By May 2026 it moved to a "CAD-as-code" agent inside Fusion and Onshape, and it open-sourced CADAM (5.3k stars).
- **Leo AI** raised $9.7M total. It is an engineering-knowledge copilot that claims 20k engineers (Jul 2025), and its site now claims 50k+. Customers include Scania, HP and Mobileye.
- **Backflip** raised the largest startup round ($30M A) and sells parametric "scan, photo or drawing to CAD" for Fusion.

**Open source**
- The fastest-growing artifact is **earthtojake/text-to-cad** (19.8k stars in about 6 months): agent "skills" that write build123d/OpenCascade code.

**Incumbents**
- Autodesk, Dassault and PTC ship assistants, not true text-to-CAD. Onshape AI Advisor explicitly "does not generate designs".
- Autodesk's real code-as-CAD path is the Claude Fusion connector plus Inventor iLogic automation.

**China**
- ZWSoft (中望) positions ZW3D "悟空" 2027 as "AI-native CAD", with natural-language modeling, private deployment and agents.

### Cited Findings
**Zoo (formerly KittyCAD; Malibu, CA)**
- Founders: Jessie Frazelle (CEO, ex-Oxide CPO) and Jordan Noone (exec chair, ex-Relativity Space CTO). It has a proprietary GPU-native geometry engine. Text-to-CAD outputs B-rep/STEP — [DEVELOP3D, Jan 2024](https://develop3d.com/cad/zoo-ecosystem-lays-foundation-for-modern-hardware-design-toolkit/) [press]
- Funding: a **$5M seed** led by Venrex, with Madrona, Nat Friedman, Tom Preston-Werner's family office, Gaingels and Liquid 2 (Oct 5, 2023) — [VC News Daily](https://vcnewsdaily.com/kittycad/venture-capital-funding/hpkkmwzqlh) [press]
  - Totals: CB Insights says $10.12M over 4 rounds; Caplight says $11M; VCBacked lists Sequoia as an investor and an undisclosed Apr 2025 round — [CB Insights](https://www.cbinsights.com/company/kittycad/financials); [Caplight](https://www.caplight.com/company/zoo); [VCBacked](https://www.vcbacked.co/company/zoo) [3rd, conflicting]
- Text-to-CAD launched Dec 18, 2023. Billing started Jan 15, 2024: **$0.50 per minute** after 20 free minutes a month, now billed per second — [Zoo blog](https://zoo.dev/blog/turning-on-billing-for-text-to-cad) [vendor]
- A Blender add-on shipped Mar 2024; a Text-to-CAD MCP shipped Oct 2025; KCL 3.0 was announced Oct 8, 2026 — [Zoo blog index](https://zoo.dev/blog) [vendor]
- **Zookeeper** (Feb 5, 2026) — [Zoo blog](https://zoo.dev/blog/announcing-zookeeper) [vendor]
  - A conversational CAD agent that writes and modifies **KCL**
  - It is selection-aware, uses vision snapshots to self-check, and runs web searches for datasheets and standards
  - It imports STEP and STL
  - Pricing: **Free $10/mo credit, then $0.50/min; Plus $20/mo (~400 min); Pro $99/mo unlimited**
  - API and MCP usage share the same credit pool — [zoo.dev/pricing](https://zoo.dev/pricing)
- GitHub: KittyCAD/modeling-app has 1,316 stars [API]
- No customer names or usage numbers are published.

**Adam (Adam AI Labs, SF; YC W25)**
- Founders: Zach Dive (CEO) and Aaron Li (CPO); team of 4 per YC. Pitched as the "Vercel v0 for CAD" — [YC](https://www.ycombinator.com/companies/adam) [official]
- **$4.1M seed led by TQ Ventures (Oct 31, 2025)**; "users have created over 1 million 3D models" — [Adam blog](https://adam.new/blog/seed) [vendor]
- "The Bitter Lesson of AI CAD" (May 24, 2026): the agent "writes CAD represented as code" with just two tools (codegen and screenshot). The team dropped its custom DSL and feature-specific tools; the product is a Fusion extension — [Adam blog](https://adam.new/blog/bitter-lesson-ai-cad) [vendor]
- 2026 product: a copilot across Onshape, Autodesk Fusion and Rhino, plus a REST API, MCP and OAuth. Plans run Free, Pro, Max, Team (per seat) and Enterprise; prices are JS-rendered and were not captured — [adam.new](https://adam.new/); [pricing](https://adam.new/pricing) [vendor]
- Open-source **CADAM**: 5,254 stars, created Sep 2025 [API]

**Leo AI (Israel)**
- An AI copilot for mechanical engineers: Q&A over 1M+ references and PLM, part search across 120M+ vendor parts, calculations
- Integrations: SolidWorks, PDM, Inventor, Fusion, NX, Teamcenter, SAP PLM
- The site claims **50,000+ engineers**; testimonials from Jon Hirschtick and Bertrand Sicot — [getleo.ai](https://www.getleo.ai/) [vendor]
- A $5M seed brought the total to **$9.7M** (lead Flint Capital; TechAviv, OurCrowd, Mento; Bertrand Sicot)
  - Then: 20,000+ engineers; customers Scania, HP, Mobileye; sold through VARs in 8 countries; "substantial revenue milestones" with no figure
  - Dated Jul 27, 2025 — [Leo blog](https://www.getleo.ai/blog/leo-ai-raises-9-7m-to-build-the-world-s-first-ai-for-mechanical-engineering) [vendor]
- Founders: Maor Farid (CEO) and Moti Moravia (CTO); about 19 people listed — [getleo.ai/about](https://www.getleo.ai/about)

**Backflip** (see 3d_asset_gen.md for the $30M A)
- In 2026 it sells Drawing-, Scan- and Photo-to-CAD producing "parametric 3D models with full feature trees", as a Fusion add-in and web app; Onshape is "coming soon" — [backflip.ai](https://www.backflip.ai/) [vendor]

**Open-source code-CAD stack (GitHub stars, 2026-10-13) [API]**
- earthtojake/text-to-cad: **19,760** (created 2026-04-22). Agent skills for build123d/OCP that output STEP, STL and 3MF, plus DFM checks, URDF and Bambu printing — [GitHub](https://github.com/earthtojake/text-to-cad)
- OpenSCAD: 10,436
- CadQuery: 5,925
- build123d: 3,395
- Pan-Chera/Multi-Agent-CAD: 1,033
- SadilKhan/Text2CAD: 488

**Incumbents**
- **Autodesk**
  - Assistant is generally available in Fusion. AutoTimeline turns imported geometry into parametric parts. Inventor Assistant drives iLogic. A next-generation agentic Assistant will be priced in 2027 — [Autodesk](https://adsknews.autodesk.com/en/pressrelease/autodesk-advances-agentic-ai-in-its-three-industry-clouds/) [vendor]
  - A Claude connector for Fusion creates and modifies models conversationally — [Anthropic](https://www.anthropic.com/news/claude-for-creative-work)
  - **Project Bernini**: the autodesk.com research page returned 403. **[bg]**: a research generative-3D model (2024) and "neural CAD" teased at AU 2025. Unverified this session.
- **PTC Onshape AI Advisor** (introduced 2025): a documentation Q&A assistant that "does not generate designs, predict errors in real time, or make complex engineering decisions" — [Onshape](https://www.onshape.com/en/features/ai-advisor) [vendor]
- **Dassault Systèmes**: an NVIDIA partnership announced Feb 3, 2026 (3DEXPERIENCE World) for "virtual companions" on Nemotron and Industry World Models. 3DEXPERIENCE has 45M+ users and 400k customers — [NVIDIA blog](https://blogs.nvidia.com/blog/huang-3dexperience-2026/) [vendor]. SOLIDWORKS-specific AI (AURA etc.) could not be fetched.
- **nTop**: implicit modeling with "Physics AI"; claims "100–1000x more configurations"; customer Specter Aerospace — [ntop.com](https://www.ntop.com/) [vendor]

**China**
- **中望 ZWSoft** — [中望官网 2026-08-03](https://www.zwsoft.cn/news/291-16150.html) [vendor]
  - The "AI Native CAD" strategy has three parts: geometry kernel, IPX conversion and an AI workbench
  - Scenarios: intelligent search, automated assembly, **natural-language modeling**; fully private intranet deployment and agent collaboration
  - ZW3D "悟空" 2027 adds AI batch drawing generation
  - Validated customers: 创维, 万里扬, 中集陕汽; cases at 中船动力 and 联想
- **新迪数字 (天工CAD)**: no data; the search budget was exhausted.

### Inferences
- Code is winning as the CAD representation for LLMs. Zoo's KCL, Adam's "CAD as code" (dropping its DSL), build123d/CadQuery skills (text-to-cad, 19.8k stars), and Inventor iLogic are all the same bet. Generic frontier models plus a screenshot verifier beat bespoke B-rep generators for editability.
- Monetization is still small:
  - Zoo's public price ($0.50/min, $20–99/mo) implies a prosumer business
  - Adam has 1M models and $4.1M raised
  - Leo has the most enterprise-like traction (named OEMs, VAR channel) but is a knowledge copilot, not a geometry generator
- No text-to-CAD startup has disclosed ARR.
- Incumbents can bundle "good-enough" assistants into existing seats (Autodesk is generally available, Dassault has a 400k customer base). Startups survive as copilots *inside* Fusion, Onshape and SolidWorks (Adam, Backflip, Leo), not as replacement CAD tools. Zoo's own CAD plus engine is the exception and the riskiest bet.

### Gaps
- No ARR or revenue for Zoo, Adam, Leo, Backflip or Spline.
- No Zoo customer names.
- Adam prices were not captured (JS-rendered).
- Primary sources were not reached for Autodesk Bernini or neural CAD status, SolidWorks AI, PTC's 2026 Onshape agent plans, 新迪数字, or 36氪 coverage of Chinese AI-CAD startups.

---

## Q5. Who has paying customers, and how much

### Takeaway
Disclosed money in this space is modest, and most of it is in the "asset store / human creator" layer, not in AI code generation.

### Cited Findings
| Entity | Paying evidence | Magnitude disclosed | Source |
|---|---|---|---|
| Blender Foundation | Donations from corporates and individuals | €3.11M income (2024); about $3.9M/yr run-rate (Oct 2026) | [Annual Report PDF](https://download.blender.org/foundation/Blender-Foundation-Annual-Report-2024.pdf); [fund.blender.org](https://fund.blender.org/) |
| Superhive (formerly Blender Market) | Marketplace sales | $52.8M paid to 6,455 creators cumulative since 2014 | [market-stats](https://superhivemarket.com/market-stats) |
| Flow (Blender-made film) | Box office | About $30–36M worldwide on about €3.5M budget | [Baltic Times](https://www.baltictimes.com/zilbalodis__animated_feature__flow__glosses_over_eur_33_million_worldwide) |
| Zoo | Metered Text-to-CAD and Zookeeper plans | $0.50/min; $20/$99 per month; revenue undisclosed | [Zoo blog](https://zoo.dev/blog/announcing-zookeeper) |
| Adam | Free/Pro/Max/Team/Enterprise plans | 1M+ models generated; revenue undisclosed | [Adam blog](https://adam.new/blog/seed) |
| Leo AI | Enterprise via VARs; Scania, HP, Mobileye | 20k → 50k+ engineers (claimed); revenue undisclosed | [Leo blog](https://www.getleo.ai/blog/leo-ai-raises-9-7m-to-build-the-world-s-first-ai-for-mechanical-engineering) |
| Spline | Seat plans with AI credits | $12–70 per seat per month; revenue undisclosed | [Spline pricing](https://spline.design/pricing) |
| Unity AI | Credit-based Assistant inside paid tiers | Undisclosed; MCP, CLI and Gateway are free | [Unity AI](https://unity.com/products/ai) |
| Autodesk Assistant | Bundled in subscriptions; next-generation pricing due 2027 | Undisclosed | [Autodesk](https://adsknews.autodesk.com/en/pressrelease/autodesk-advances-agentic-ai-in-its-three-industry-clouds/) |
| fly.pieter.com / Vibe Jam | In-game ads, plane sales, sponsor-funded prizes | $50k+ prize pool (2026); ad revenue unverified **[bg]** | [vibejam.com](https://vibejam.com/); [fly.pieter.com](https://fly.pieter.com/) |
| BlenderMCP, Blender Lab MCP, community MCPs | Free and open source | 0 direct revenue; about 490k PyPI downloads per month | [pepy](https://pepy.tech/projects/blender-mcp) |

### Inferences
- The only sizable, verified cash flows are around Blender itself: donations of about €3M/yr and the human-made asset market (about $53M cumulative).
- AI code-as-3D companies publish prices but not revenue. Their combined disclosed funding (Zoo about $10M, Adam $4.1M, Leo $9.7M, Backflip $30M) is much smaller than single AI asset-generation rounds such as Meshy's about $400M (see web3d_engines.md).
- Frontier labs and DCC vendors capture the agent layer for free (MCP connectors), which compresses the room for standalone "agent for DCC X" startups. Defensible niches:
  - Hard-surface and parametric CAD inside incumbent tools
  - Enterprise knowledge and PLM (Leo)
  - Manufacturing-tied outputs (Backflip, Womp printing)

### Gaps
- No disclosed ARR for any company in this file.
- No market-size estimate for "AI CAD" or "text-to-CAD" from a reliable analyst was found; the search budget was exhausted.

