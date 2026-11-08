# AI Game Creation: Text-to-Game, UGC-Platform AI, AI-Native Games, China 小游戏 (R2 deep pass, as of 2026-10-13)

Scope and method notes
- Round 2 deepens `game_world_gen.md`. It does not repeat world models (Genie / World Labs / Decart / Odyssey), Unity AI, or Scenario/Layer.
- Budget: ~64 search/fetch calls. The session-wide WebSearch budget ran out mid-run, so the rest was done with WebFetch on known or primary URLs. Several China items (抖音互动空间, 小红书小工具, 逆水寒 GDC numbers, 微信 AI tools) could not be re-verified as a result. They are listed under Gaps.
- Source-type tags on each number:
  - **[Co]** company or official primary (filing, newsroom, product page, exec on stage)
  - **[Co-via-press]** company figure quoted by press
  - **[Press]** trade or news reporting
  - **[3P-est]** third-party estimate (SteamDB-derived, Naavik, Boxleiter)
  - **[Self]** founder self-report on social media
  - **[Agg]** aggregator or SEO site, low trust
- Dates are publication dates unless noted.

## Q1. Text-to-game / vibe-coded game platforms: who, what engine, traction, money

### Takeaway
- **Astrocade is the only Western text-to-game platform with large disclosed traction:**
  - 10M MAU and 220M sessions/month, Oct 2026 [Co-via-press].
  - It is still pre-monetization and pays creators out of a reported $10M VC-funded incentive fund.
- **Everyone else monetizes the creator, not the player:**
  - Rosebud, Ludo, Bezi and SEELE sell $15–$300/month credit subscriptions.
  - Commercial rights or export sit behind paid tiers.
- **Pure vibe-coded hits are spiky:**
  - fly.pieter.com went from a self-reported $87K MRR (Mar 2025) to "$0/m" on levelsio's own bio by mid-2026.
  - Its business model was sponsor ad-slots plus a $29.99 jet. That is a launch-virality model, not a recurring one.

### Cited Findings

**Astrocade (US; web, prompt → casual game, UGC feed)**
- **Funding:** $56M combined (Series A led by Sea, Series B led by Sequoia), announced May 5–7, 2026 [Press] — [Fortune](https://www.fortune.com/2026/05/05/astrocade-raises-56-million-series-b-sequoia-video-games-platform-ali-amir-sadeghian/), [PocketGamer.biz](https://pocketgamer.biz/astrocade-raises-56m-to-expand-ai-powered-games-creation-platform/)
  - Other investors: Google, Nvidia, LG Ventures, Dentsu Ventures, Conviction Embed.
  - Founders Ali and Amir Sadeghian; founded 2022.
  - Launched Aug 2025 with a 13-person team.
- **Traction at funding, May 2026** [Co-via-press]:
  - ~5M MAU, ~140M plays/month, 75K+ games from creators in 80 countries — [Fortune](https://www.fortune.com/2026/05/05/astrocade-raises-56-million-series-b-sequoia-video-games-platform-ali-amir-sadeghian/)
  - PocketGamer cites "20M+ users within eight months." This is likely cumulative sign-ups, not MAU — [PocketGamer.biz](https://pocketgamer.biz/astrocade-raises-56m-to-expand-ai-powered-games-creation-platform/)
- **Traction, Oct 2026** [Co-via-press, from a CEO interview]:
  - MAU grew 5M → 10M in four months.
  - 220M sessions/month across 100K+ "playable" games — [GamesBeat](https://gamesbeat.com/?p=336386) (403 on fetch; text via search snippet), [Kotaku](https://kotaku.com/ai-generated-games-platform-already-has-10-million-monthly-users-2000741894)
- **Monetization:**
  - Revenue not disclosed.
  - Top creators reportedly earn "thousands of dollars a month" [Co-via-press] — [Fortune](https://www.fortune.com/2026/05/05/astrocade-raises-56-million-series-b-sequoia-video-games-platform-ali-amir-sadeghian/)
  - $10M creator incentive program paying "per play," modeled on YouTube/TikTok, with the company "intentionally burning VC money" — [SuperDataScience ep. 997](https://superdatascience.com/997) (podcast summary via search; page 403)
  - A Mezha writeup of GamesBeat instead says payouts are "based on the number of launches," and that active monetization of the platform is planned for "next year" (2027) — [Mezha](https://mezha.ua/en/news/ai-slop-games-is-popular-315954/)
  - **Conflict:** per-play vs per-launch payout wording.
- **Demo:** [astrocade.com](https://www.astrocade.com/) is live and loads "Play Free Online Games or Create Your Own with AI." Verified by fetch 2026-10-13; no pricing shown.
- **Engine/stack:** not disclosed in any source fetched.

**Rosebud AI (US; browser, prompt → 2D/3D web games)**
- **Pricing** [Co], verified 2026-10-13 — [rosebud.ai/pricing](https://rosebud.ai/pricing):

  | Tier | Price | Credits | Adds |
  |---|---|---|---|
  | Free | $0 | 8K/week | — |
  | Indie Dev | $15/mo | 100K/mo | — |
  | 10x Dev | $30/mo | 300K/mo | Full commercial rights, no branding |
  | Pro | $50/mo | 1M/mo | Code download, Windows export for Steam |
  | Scale | $100/mo | 2M/mo | — |

  - A default "Rosie" edit costs ~2K credits; a premium-model edit ~20K.
- **Product lines:** game creator, AI Storybook, Tokkingheads, Educators, 3D website builder (three.js in URL slug), "X Playables" — [rosebud.ai](https://rosebud.ai/)
- **Traction:** "over 2.1 million games have already been created" (undated) [Co] — [Rosebud Education](https://lab.rosebud.ai/education-initiative)
  - Product Hunt relaunch Aug 12, 2025: #15 of the day [Agg] — [hunted.space](https://hunted.space/product/rosebud-ai-2)
  - Revenue and MAU not found. Funding conflicts are noted in R1.
  - Not to be confused with "Rosebud," the journaling app ($6M seed).

**Ludo.ai (ideation / asset / "game design" assistant)**
- **Pricing** [Co], verified 2026-10-13, annual billing — [ludo.ai/pricing](https://ludo.ai/pricing):

  | Tier | Price | Credits | Seats | Notes |
  |---|---|---|---|---|
  | Indie | $15/mo | 3K/yr | — | — |
  | Pro | $35/mo | 12K/yr | — | API / MCP / CLI access |
  | Studio | $300/mo | 120K/yr | 10 | — |
  | Enterprise | Custom | — | — | — |

  - Credit price: $0.03–0.06.
  - It is a B2B/prosumer SaaS, not a consumer game platform.

**Bezi (US; AI agent inside Unity)**
- **Funding:** $13M Series A led by Benchmark (Uncork, Designer Fund), raised in 2023 when Bezi was a 3D-design tool, before its pivot to AI for game makers [Press/law-firm PR] — [Fenwick](https://www.fenwick.com/insights/experience/fenwick-represents-bezi-in-series-a-financing)
  - **Conflict:** [Neuronfeed](https://neuronfeed.com/startups/bezi) names Uncork/Designer Fund as leads.
- **Pricing** [Co], verified 2026-10-13 — [bezi.com/pricing](https://www.bezi.com/pricing)
  - Trial: free, 100 credits
  - Pro: $20/mo, 800 credits
  - Advanced: $60/mo, 2,400 credits
  - Ultimate: $180/mo, 7,200 credits
  - On-demand usage billed at API pricing.
- At Gamescom (BGA lineup Aug 26, 2026) — [eGamers](https://egamers.io/ai-agent-that-works-inside-unity-heads-to-gamescom-as-bga-stacks-its-aug-26-lineup/)
- No customer counts.

**Jabali (US; prompt-to-game)**
- **Funding:** $5M seed, Mar 6, 2024, led by BITKRAFT (with Sapphire Sport, Sony Innovation Fund, Canonical) [Co] — [jabali.ai](https://www.jabali.ai/fundingannoucement). CEO Vatsal Bhardwaj.
- **Product today:** Jabali Web (browser prompt-to-game, 23 game types), Jabali Studio ("NEW": desktop 2D/3D), Jabali Play [Co], verified 2026-10-13 — [jabali.ai](https://www.jabali.ai/)
- No pricing or stats.
- An Oct 2025 report of "Jabali Studio by rock.ai (Perth) raises $5M" looks like a name collision or confusion — [Techleap](https://finder.techleap.nl/news/feed/jabali-studio-secures-5m-for-ai-gaming)

**SEELE / Seele AI (国内出身团队, overseas product)**
- **Product:** SeeleAgent, prompt → games, 3D, video and code, built on in-house models Seele02 and eva01. "PEGA Worldmodel" listed as coming soon.
- **Exports:** Three.js (browser), Unity 6 (C# packages), and Unreal. Its own structured data hedges that browser-3D output is not a native Unreal project.
- **Business model:** free credits; Pro tier for Unity export and commercial use; a payments/ads integration and a "Creator Program" revenue share ("not guaranteed").
- **Traction:** "Trusted by 3M+ creators as of 2026" [Co, self-claimed]. R1 had "~1M users in 6 months."
- Self-reported benchmarks: GameCraft-Bench 65.3%, GameDevBench pass@1 65.8% — [seeles.ai](https://www.seeles.ai/), verified 2026-10-13.

**Gambo.ai ("first Game Vibe Coding Agent")**
- Prompt → full game with generated sprites, animations, BGM and SFX. Output is TypeScript game code (e.g. `DoodleJumpScene.ts`). Optional Supabase backend.
- A Doodle-Jump clone took ~12 minutes.
- The advertised "earn from day one" built-in ads were not live at review (2025-10-27) [Press] — [woshipm/硅星人](https://www.woshipm.com/ai/6284105.html), [Gambo help](https://laced-basil-120.notion.site/Gambo-Get-Help-26a9b6f7c4d580958510c99f7fac701f)
- The homepage fetched empty, so I could not verify current state.

**Sett (Israel)**
- An agentic AI platform for mobile studios, generating UA video ads and in-game content. It is B2B and not text-to-game for consumers.
- $27M total ($12M seed + $15M Series A, Bessemer lead), May 2025 [Press] — [TechCrunch](https://techcrunch.com/2025/05/07/game-sett-funding-a-startup-building-ai-agents-for-game-development-emerges-from-stealth-with-27m)
- Customers named: Playtika, SuperPlay, Candivore. TechCrunch adds Zynga, Scopely, Rovio, Plarium, Unity.

**Series Entertainment (US)**
- An AI-first studio plus the "Rho Engine" toolset.
- $28M round (Netflix, Dell Technologies Capital, a16z, BITKRAFT, F4), Sep 30, 2024 [Press] — [TechCrunch](https://techcrunch.com/2024/09/30/series-the-genai-startup-reinventing-game-development-has-quietly-raised-28m-from-netflix-dell-a16z-others)
- PitchBook valuation estimate ~$190M (unconfirmed).
- Acquired Pixelberry (*Choices*) in 2024.
- No 2026 Rho availability or pricing found.

**Cybever**
- Was an AI 3D-world tool for game prototyping (beta Sep 2024) — [BusinessWire](https://businesswire.com/news/home/20240912018771/en/Cybever-Unveils-Beta-for-AI-Powered-3D-World-Creation-Platform-Advancing-Its-Mission-to-Democratize-Content-Development)
- It has since rebranded as **Utopai Studios**, an AI film/TV studio claiming "$110 million in revenue for their upcoming projects" (projected slate value, not booked revenue) [Co] — [Utopai](https://www.utopaistudios.com/news-blog/cybever-rebrands-as-utopai-studios-with-110-million-in-revenue-and-a-hollywood-slate)
- Effectively exited games.

**Playroom (multiplayer SDK for web games)**
- Built *Death by AI*, a Jackbox-style AI party game soft-launched Nov 2023. It burned "nearly $30,000 in just the first few days" on LLM/TTS calls while scaling [Co blog] — [Playroom Substack](https://playroom.substack.com/p/case-study-building-and-scaling-a)
- Little Umbrella, the studio using Playroom, raised a $2M seed (a16z speedrun, Breakpoint) in Jan 2025 for three AI party games [Press] — [Techleap](https://finder.techleap.nl/news/feed/little-umbrella-raises-2m-for-ai-games)
- Playroom's own funding was not found.

**levelsio / fly.pieter.com (archetype of the vibe-coded game)**
- **Build:** a Cursor prompt, "Make a 3d flying game in browser with skyscrapers"; working game in ~3 hours, Feb 2025 [Self] — [dev.to recap citing X](https://dev.to/promptway/he-built-a-flight-simulator-in-three-hours-and-hit-1m-a-year-in-17-days-then-it-went-to-zero-1b1l)
- **Stack:** credits read "@levelsio + Cursor + ThreeJS." Verified live 2026-10-13 — [fly.pieter.com](https://fly.pieter.com/)
  - Monetization visible on the page: buy an in-game ad (Stripe, claimed "100,000+ people" reach); Cessna and "Cyberpink" free; F-16 $29.99.
- **Revenue arc** [Self, via press]:
  - ~$5K/month from ads ~10 days in — [AvGeekery](https://avgeekery.com/?p=39779)
  - "$50,000+ a month," Mar 5, 2025 — [404 Media](https://404media.co/this-game-created-by-ai-vibe-coding-makes-50-000-a-month-yours-probably-wont)
  - $67K MRR at day 13 and $87K MRR (= "$1M ARR") at day 17, with Levels himself saying sustainability was a guess — [X post cited by dev.to](https://x.com/levelsio/status/1899596115210891751)
  - By mid-2026 his X bio lists "Pieter.com $0/m" [Self] — [dev.to](https://dev.to/promptway/he-built-a-flight-simulator-in-three-hours-and-hit-1m-a-year-in-17-days-then-it-went-to-zero-1b1l)
  - **Caveat:** "MRR" here was one-off sponsor slots plus jet purchases annualized. I could not fetch X directly.

**Vibe Jam (levelsio's game jam)**
- **2025 "Bolt Vibe Coding Game Jam"** (April 2025): 1,000+ entries, $17.5K prizes [Co] — [vibejam.com/2025](https://vibejam.com/2025/)
  - Gold ($10K): *The Great Taxi Assignment* by @tomasbencko — [great-taxi-assignment.netlify.app](https://great-taxi-assignment.netlify.app/). Page live; title "Great Taxi Assignment: Vibe City."
  - Silver ($5K): *Vibeware* by @mattgordonxyz — [vibeware.vercel.app](https://vibeware.vercel.app/). **Now only a teaser page, not playable** (verified 2026-10-13).
  - Bronze ($2.5K): *Vector Tango* by @scobelverse (vector-tango.com, not fetched).
- **2026 "Cursor Vibe Jam"** (Apr 1 – May 1, 2026) [Co] — [vibejam.com/2026](https://vibejam.com/2026/) (vibej.am and jam.pieter.com now 301 to vibejam.com)
  - Sponsors: Cursor (Diamond), Bolt.new (Gold), Glif and Tripo3D (Silver).
  - Prizes: Gold $25K / Silver $10K / Bronze $5K + 12×$1K.
  - Rules: ≥90% AI-written code; free, web, no login; "any engine, Three.js recommended."
  - The official page still showed winners "TBA" and placeholder counters on 2026-10-13.
- **2026 stats:** 945 submissions, 242K+ players, ~12M views on X [Press, vendor blog] — [Summer Engine](https://www.summerengine.com/blog/cursor-vibe-jam-2026-guide)
  - 48 entries (~5%) used the Colyseus multiplayer server, ~15% of multiplayer entries [Co blog] — [Colyseus](https://colyseus.io/blog/vibe-jam-2026/)
  - A single report (via Reddit) says a "Capybara food delivery" game made with zero hand-written code won $25K. Unverified against the official page — [aibase](https://www.aibase.com/news/29583)

### Inferences
- **The Western text-to-game market has split in two:**
  - (a) A consumer UGC-feed play (Astrocade) that copies the Roblox/YouTube playbook: subsidize creators per play now, monetize with ads or IAP later.
  - (b) A creator-tool SaaS play (Rosebud, Ludo, Bezi, SEELE) at $15–$300/month, with commercial rights and Unity/Steam export as the upsell gates.
- **three.js is the de-facto runtime for vibe-coded web games.** Evidence: Vibe Jam recommends it, fly.pieter.com uses it, and SEELE's browser export uses it. Unity is the target when "real" export is the upsell (SEELE Pro, Bezi).
- **Vibe-coded hits are attention arbitrage.** fly.pieter's revenue was sponsorship sold against a viral audience, and it did not recur.
  - 1 of 3 2025 Vibe Jam podium URLs is no longer a playable game, which is a hint of short shelf life.

### Gaps
- Not verified this round (search budget exhausted):
  - Lovable, Bolt, Replit and Claude-artifacts game-specific traction (only Bolt/Cursor sponsorship of Vibe Jam is confirmed)
  - Google and OpenAI official game demos
  - 2026 Vibe Jam winners
- No revenue for Astrocade, Rosebud, Ludo, Bezi, SEELE, Jabali or Gambo. No Astrocade engine/stack disclosure.
- No Playroom funding figure. Series Entertainment's 2026 status is unknown.

## Q2. UGC platforms' AI and creator economics

### Takeaway
- **The incumbents have absorbed text-to-game:**
  - Roblox **Build** (Jul 2026, mobile prompt → game): ~9,000 games published by RDC (Sep 2026); 71% of makers had never used Studio.
  - 网易蛋仔派对 ships DeepSeek/GLM/Kimi inside its editors.
  - TapTap 制造: ~5,000 games from 3,000 creators in six months.
- **Creator money is real and large where distribution and payments already exist:**
  - Roblox DevEx: $1.503B in FY2025 (10-K), ~$1.7B trailing 12 months as of Sep 2026.
  - Fortnite: >$1B cumulative (Jan 2026), $352M in 2024.
  - 蛋仔: >¥200M incentives and revenue share Jul 2025 – Jul 2026; top creators earn ¥10M+/yr.

### Cited Findings

**Roblox**
- **Build:** mobile "Build" tab, announced Jul 16, 2026. Text prompt → starter game with mechanics, environment, characters, sound and style; shares its backend with Studio. Mix of open-source and proprietary models, plus Cube for game-ready objects [Press] — [The Next Web](https://thenextweb.com/news/roblox-build-mobile-ai-game-creation), [Nasdaq PR](https://www.nasdaq.com/press-release/roblox-introduces-build-new-way-create-platform-2026-07-16)
  - Base version free; paid options for power users, price unspecified.
  - Public alpha in New Zealand from Jul 28, 2026, for age-verified users aged 9+.
  - Discovery ranks by long-term retention. Kids-catalog titles get extended review.
- **RDC 2026** (San Jose, Sep 2026) [Co-via-press] — [GamesBeat keynote](https://gamesbeat.com/roblox-hits-20-and-opens-rdc-2026-to-invite-the-world-to-play-and-make-games-dave-baszucki-keynote/)
  - Build: ~9,000 games published; 71% of makers were Studio-naive; expanding to Serbia and Singapore.
  - Scene Generator (text + reference image → layout) "later in 2026."
  - Creators paid >$5B since 2013, ~$1.7B in the past 12 months.
  - Roblox Plus incentives >300M Robux in four months.
- **FY2025 10-K** [Co] — [10-K](https://www.sec.gov/Archives/edgar/data/1315098/000131509826000024/rblx-20251231.htm), via [Statista](https://statista.com/statistics/1376672/roblox-developer-payout)
  - Developer exchange fees $1,503.1M (+63% vs $922.8M in 2024), driven by the Creator Rewards Program (Jul 2025) and +8.5% DevEx rate (Sep 5, 2025).
  - 127M average DAU.
  - 23,500+ creators paid in fiat in 2025; 35,500+ qualified.
  - The 10-K names Assistant, Code Assist, Material Generator and Cube, with **no adoption numbers**.
  - Build announcement cites 132M DAU [Press] — [TNW](https://thenextweb.com/news/roblox-build-mobile-ai-game-creation)
- **AI pillars:** coding, 3D objects, multiplayer NPCs, video/realism — [allthings.how](https://allthings.how/roblox-rdc-every-major-announcement-for-players-and-creators/)
  - Cube/4D and Morpheus/"Roblox Reality" are covered in R1.

**Fortnite / UEFN (Epic)**
- **AI NPCs:** the Persona device (Darth Vader tech, State of Unreal Jun 2025) was renamed **"conversations."** It is Experimental as of Apr 16, 2026, and **publishing islands that use it is not yet allowed** [Co, title/snippet; page 403] — [Fortnite news](https://www.fortnite.com/news/bring-npcs-to-life-with-ai-powered-conversations), [CGMagazine](https://www.cgmagonline.com/news/state-of-unreal-2025-fortnite-ai/), [GamesBeat](https://gamesbeat.com/unreal-editor-for-fortnites-ai-character-creation-tool-has-ambitions-beyond-darth-vader/)
  - Darth Vader drew a SAG-AFTRA complaint after players got it to swear — [TechSpot](https://www.techspot.com/community/topics/fortnite-to-add-even-more-ai-npcs-following-darth-vader-incident.292745/)
- **Creator payouts:**
  - $352M in 2024 to ~70K creators [Co via Statista] — [Statista](https://statista.com/statistics/1602861/fortnite-ugc-user-engagement)
  - >$1B cumulative since 2023, threshold crossed Jan 2026, announced at Unreal Fest Jun 17, 2026 [Co-via-press]
  - 2025 engagement pool ~$370M (Naavik estimate $350–390M) [3P-est]
  - Creator islands at 47% of player hours, May 2026
  - In-island sales: creators get 50% of V-Bucks value, with 100% promo through Dec 2026
  - Source for these four: [tech-insider](https://tech-insider.org/ca/fortnite-creator-economy-1-billion-2026/) (secondary aggregator; Epic attributions partly vague)
- **Pool mechanics:** 40% of net Item Shop revenue goes to the engagement pool. Since Nov 2025, creators get 75% of new or lapsed players' contribution for six months — [esports.gg](https://esports.gg/guides/fortnite/how-do-fortnite-creators-make-money/), [Fortnite Sep 18, 2025](https://www.fortnite.com/news/fortnite-developers-will-soon-be-able-to-sell-in-game-items)

**网易《蛋仔派对》**
- **Scale** [Co, exec 余志恒 at the Global Digital Economy Conference, Jul 3, 2026] — [新华网 2026-07-07](https://www.xinhuanet.com/digital/20260707/abc56da5139a4707befb0a7541c8a834/c.html), [36氪 2026-07-15](https://www.36kr.com/p/3896755010963333)
  - 700M+ registered users, 100M+ MAU, 200M+ maps published.
  - Native UGC developers: **conflict** — 4,000万+ per Xinhua vs 5,000万+ per 36氪.
- **Creator income** [Co]:
  - Top creators earn tens of millions of ¥ a year; mid-tier >¥100K a year; a single hit map earns >¥5M.
  - Student examples: 武大 developer 15M plays and >¥300K/yr; 三峡大学 studio >¥1.3M/yr; 重庆工商 studio >¥1.5M/yr.
  - Seven channels: traffic incentives, ads, IAP, sponsorship, esports, events, brand orders.
- **Economics** [Co, per 36氪]:
  - >¥200M incentives and revenue share Jul 2025 – Jul 2026.
  - 5B+ ad plays in the past year.
  - IAP split: creator keeps 70% after channel costs and refunds. The platform cut on ads and tips was lowered.
- **AI in the editors** [Co, per 36氪 and Xinhua]:
  - "双子星编辑器" (蛋仔世界编辑器 + 原点编辑器) unveiled Jul 11, 2026 at the 4th creator conference (乌镇).
  - DeepSeek V4 Pro, GLM-5.2 and Kimi K2.7 Code are built in.
  - 影眸 Rodin text-to-3D.
  - AI assistant (since Oct 2025): 859K authors, 2.243M sessions, 855K map edits assisted.
  - The dev assistant wrote 377K lines of code in internal test.
  - Team AI usage rose >10x in H1 2026.
  - Seedance IP partnership with 火山引擎.

**TapTap 制造 (TapTap Maker)**
- Launched Jan 30, 2026. Browser-based, natural-language AI game creation; AI-native engine plus TDS; creators choose model and compute [Press] — [中华网](https://m.tech.china.com/articles/20260131/202601311806283.html), [新浪财经 2026-09-23](https://cj.sina.com.cn/articles/view/1850649324/6e4eaaec02002k0ge)
- **Traction:** ~3,000+ creators made ~5,000 games in six months, with 11M+ cumulative players [Co-via-press] — [新浪财经](https://cj.sina.com.cn/articles/view/1850649324/6e4eaaec02002k0ge), [InvenGlobal](https://www.invenglobal.com/articles/24194/80-of-5002-new-games-on-taptap-in-first-half-of-year-created-with-ai)
- **Platform-wide, H1 2026** [Co, CEO 黄一孟 at TDW Jul 26, 2026] — [InvenGlobal 2026-07-27](https://www.invenglobal.com/articles/24194/80-of-5002-new-games-on-taptap-in-first-half-of-year-created-with-ai)
  - 5,002 playable new games, +843.8% YoY from 530.
  - ~4,000 (~80%) were small AI-made games.
  - TapTap **ended "guaranteed exposure for new releases"** in favor of curation and developer credit ratings.
- Monetization for 制造 creators: not found.

**腾讯 代号Craft**
- An AIGC game-creation platform from the Tencent 生态发展部, shown at SPARK 2026 (May 27, 2026). Prompt → 2D/3D game prototype; Unity adaptation mentioned [Press] — [IT之家](https://www.ithome.com/0/956/225.htm), [TMTPost](https://www.tmtpost.com/8026124.html), [DoNews](https://www.donews.com/news/detail/3/6573620.html)
  - First test "开发者先锋营" with 深圳前海.
  - Asset library: **conflict** — "超万种" (IT之家) vs "超2万款" (TMTPost).
- 元梦之星 AI creation tools / economics: **not found** (search returned nothing relevant).

**WeChat 小游戏**
- 500M+ MAU (dev conference May 27, 2026) [Co-via-press] — [OFweek](https://cloud.ofweek.com/news/2026-06/ART-178808-8110-30689646.html). Page text was garbled, and developer-revenue numbers were unreadable.
- No WeChat-native AI game generator was found in this pass.

### Inferences
- The incumbents hold the scarce asset: distribution plus payments plus a payout rail.
  - Roblox ($1.5B/yr), Epic (~$370M/yr) and 蛋仔 (>¥200M/yr) already pay creators at scale.
  - Their AI creation tools (Build, 蛋仔 AI assistant, UEFN conversations) need not monetize directly; they lift creator supply.
  - That structurally caps standalone text-to-game players, who must subsidize payouts with VC money (Astrocade's $10M fund).
- Supply flood is now the platform problem. Evidence:
  - TapTap +844% releases and the end of guaranteed exposure.
  - Roblox ranking by retention and extended kids review.
  - Epic not allowing publishing with AI NPCs yet.

### Gaps
- Not verified:
  - 抖音 "互动空间" and 小红书 "小工具" AI mini-game details (R1 cites a 知乎 summary; it returned 403 this round, and search was exhausted)
  - 元梦之星 AI
  - Minecraft AI features
  - WeChat developer revenue figures
  - TapTap 制造 creator monetization
- No Roblox Assistant or Cube usage numbers beyond R1's 1.8M Cube objects.

## Q3. AI-native games: traction and money

### Takeaway
- **AI-native games remain commercially small or short-lived:**
  - *Whispers from the Star*: ~1.66K Steam reviews ≈ low tens of thousands of units.
  - AI Dungeon's peak economics: Patreon ~$15K/month (2019); now a web/app subscription product.
- **The bright spots are free, viral, ad-light toys** (Infinite Craft: 300M recipes/day) **and AI features inside big live games** (逆水寒, see Gaps).
- **Steam disclosure share is rising fast, but AI games under-earn:**
  - AI-disclosed games are ~31–33% of new releases in 2026.
  - They earn ~10–27% of sales and reach the 100-review tier at ~55% of the non-AI rate.

### Cited Findings
- **Steam AI disclosure:**
  - **SteamDB-based census** by Sulka Haro, published Jul 13, 2026 [3P-est] — [fragwyz Substack](https://fragwyz.substack.com/p/three-years-of-ai-on-steam)
    - 53,597 releases Jul 2023 – Jul 2026, ~9,400 AI-disclosed.
    - AI launches ~530/month vs non-AI ~1,320/month.
    - AI share of new releases ~1% pre-2024 → ~7% in Feb 2024 → ~33% in mid-2026.
    - AI-disclosed share of estimated sales: ~3–6% (2024) and ~10–27% (late 2025–2026).
    - AI games reach ≥100 reviews at ~55% of the non-AI rate.
    - The top-2 AI games each quarter take 45–79% of AI revenue.
    - 22% of significant-revenue AI games added the flag after release, clustered around Valve's Jan 2026 rule rewrite.
    - Method: Boxleiter (reviews × 30 × price).
  - **Same census by year** [3P-est] — [games.gg 2026-07-20](https://games.gg/news/steam-ai-disclosure-games-2028-trend/)
    - Share of new releases: 10.9% (2024), 19.9% (2025), 30.8% (2026 YTD).
    - Total releases: 21,382 (2025); 13,359 by mid-Jul 2026.
  - **Earlier count:** ~1,000 games disclosed in 2024, ~8,000 in H1 2025 [Press] — VGC via search summary (page 403): [VGC](https://www.videogameschronicle.com/news/valve-has-significantly-rewritten-steams-rules-for-how-developers-much-disclose-ai-use)
  - **Steam Next Fest, Jun 2026:** 1,704 of 8,700 titles (19.5%) tagged gen-AI (Eurogamer, SteamDB data) [Press] — [Dataconomy 2026-06-17](https://dataconomy.com/2026/06/17/steam-next-fest-19-5-percent-demos-generative-ai/)
  - **Rule change:** Valve's Jan 2026 rewrite exempts internal workflow tools, so counts before and after are not strictly comparable — same VGC source.
- **Whispers from the Star (Anuttacon/蔡浩宇):**
  - Released Aug 14, 2025, Windows; "Very Positive," 80% of 1,662 reviews [Co, Steam], verified 2026-10-13 — [Steam](https://store.steampowered.com/app/3730100/)
  - R1's Raijin estimate: ~34K copies, ~$290K gross.
  - Studio wind-down signals are in R1 (投资界).
- **AI Dungeon / Latitude** [Press/encyclopedic] — [Wikipedia](https://en.wikipedia.org/wiki/AI_Dungeon)
  - 1.5M players by Jun 2020.
  - Patreon ~$15K/month in Dec 2019; GPT-2 bandwidth costs >$20K within days.
  - $3.3M seed (Feb 2021, NFX).
  - Retired from Steam Mar 12, 2024.
  - **Voyage** (formerly "Heroes," renamed Oct 2025): expanded beta Apr 2026; Voyage Studio Aug 2026; **opened to all on web, iOS and Android Aug 26, 2026**.
  - The AI Dungeon homepage is live (© 2026 Latitude), verified 2026-10-13 — [aidungeon.com](https://aidungeon.com/)
  - R1's ~$1.4–1.8M ARR estimate is single-source.
- **Hidden Door:** live as a "playable stories" platform with a Narrator, collectible cards, and a writer/creator world-builder; pricing and partners pages exist but no figures [Co], verified 2026-10-13 — [hiddendoor.co](https://www.hiddendoor.co/)
- **Infinite Craft (Neal Agarwal):** web launch Jan 31, 2024; uses Llama 2 / Mistral; "over 300 million recipes are created each day" [Press/encyclopedic] — [Wikipedia](https://en.wikipedia.org/wiki/Infinite_Craft)
  - Monetization not documented; neal.fun returned 403.
- **Inworld AI:** homepage now sells realtime TTS/STT, Realtime API, a 100+ LLM router, inference (Gemma 4, DeepSeek V4, GLM-5.2) and GPU compute for "consumer-facing applications" [Co], verified 2026-10-13 — [inworld.ai](https://inworld.ai/)
  - Games are one use case among many. Named customers are non-game (Wishroll/Status, Bible Chat, Talkpal).
  - This confirms the pivot away from game NPCs.
- **逆水寒手游:**
  - Feb 17, 2026 roadmap [Press] — [IT之家](https://www.ithome.com/0/922/195.htm)
    - A higher share of 智能NPC.
    - AI "造梦模式" (infinite-flow interactive play) after 春节.
    - 剧组 system to generate 3D models.
    - First game to integrate Seedance video gen, in v3.3.1 (early March).
  - No player or revenue numbers in that article.
  - The R1 36氪 "年收入破亿" / 剧组站 5M swipes/day item remains **unverified**: 36氪 served a 火山 anti-bot page on refetch.
- **Death by AI (Playroom):** ~$30K inference burn in the first days — an example of AI-native unit-economics risk [Co] — [Playroom](https://playroom.substack.com/p/case-study-building-and-scaling-a)
- **China, 2026:**
  - ChinaJoy 2026 was the first AI-themed edition, with a 70-title AI zone out of ~1,000 games.
  - 崇祯模拟器, built on a "one-sentence game" engine, drew 25K players.
  - *Sherlock Holmes: Night Stalker* uses LLM NPCs.
  - Source for all three [Press, paywalled; partly AI digest] — [Caixin Global 2026-08-14](https://www.caixinglobal.com/2026-08-14/in-depth-game-studios-have-bought-into-ai-but-players-still-arent-sold-102474160.html)

### Inferences
- Disclosure share (~33% of launches) far exceeds revenue share (~10–27%), and the visibility tier is reached at 55% of the non-AI rate.
  - So on Steam, AI is a cost-reducer for low-budget releases, not a demand driver.
  - The few AI-disclosed revenue winners (e.g., inZOI) use AI as a feature inside conventional games.
- Pure LLM-driven narrative games face inference cost per player-hour against premium one-time pricing. Examples:
  - Death by AI's $30K in days.
  - Whispers' ~$290K gross.
- Survivors are either subscription (AI Dungeon/Voyage) or free and lightweight (Infinite Craft, with a tiny token budget per element).

### Gaps
- Not verified this round:
  - Suck Up! sales (official site SSL failure; no Wikipedia page)
  - 1001 Nights Steam figures
  - 逆水寒 AI NPC user numbers and the 36氪 revenue claim
  - 网易伏羲 2026 metrics
  - Infinite Craft revenue
  - Hidden Door pricing
- No primary Valve dataset; all Steam AI numbers are SteamDB-derived third-party censuses.

## Q4. Which business models work, with numbers

### Takeaway
Ranked by verified dollars:
1. **Platform creator economies with AI layered in:**
   - Roblox: $1.5B DevEx in FY2025.
   - Fortnite: ~$370M pool (2025 estimate).
   - 蛋仔: >¥200M a year.
   - AI here is a supply-side subsidy, not a SKU.
2. **Creator-tool SaaS on credits:** Rosebud $15–100/mo, Ludo $15–300/mo, Bezi $20–180/mo, SEELE Pro. Revenue undisclosed but structurally positive per seat.
3. **VC-subsidized UGC feeds** (Astrocade: 10M MAU, $10M creator fund, monetization planned for 2027).
4. **One-off viral vibe-coded games** (fly.pieter.com: $87K "MRR" → $0).
5. **Premium AI-native narrative games** (Whispers ~$290K gross; Steam AI titles under-index on revenue).

### Cited Findings
- Roblox developer exchange fees $1,503.1M in FY2025 (+63%) — [Roblox 10-K](https://www.sec.gov/Archives/edgar/data/1315098/000131509826000024/rblx-20251231.htm), [Statista](https://statista.com/statistics/1376672/roblox-developer-payout)
  - ~$1.7B trailing 12 months (Sep 2026) — [GamesBeat](https://gamesbeat.com/roblox-hits-20-and-opens-rdc-2026-to-invite-the-world-to-play-and-make-games-dave-baszucki-keynote/)
- Fortnite >$1B cumulative creator payouts (Jan 2026) and ~$370M 2025 pool estimate — [tech-insider](https://tech-insider.org/ca/fortnite-creator-economy-1-billion-2026/)
- 蛋仔 >¥200M incentives and revenue share in one year; 70% IAP share; 5B+ ad plays — [36氪](https://www.36kr.com/p/3896755010963333)
- Astrocade: $10M per-play creator fund and burn-for-growth (podcast), monetization planned for next year — [SuperDataScience](https://superdatascience.com/997), [Mezha](https://mezha.ua/en/news/ai-slop-games-is-popular-315954/)
- Credit SaaS price points — [Rosebud](https://rosebud.ai/pricing), [Ludo](https://ludo.ai/pricing), [Bezi](https://www.bezi.com/pricing), [SEELE](https://www.seeles.ai/)
- fly.pieter.com: ads, blimps and a $29.99 F-16, peaking at $87K MRR and later $0/m — [dev.to](https://dev.to/promptway/he-built-a-flight-simulator-in-three-hours-and-hit-1m-a-year-in-17-days-then-it-went-to-zero-1b1l), [fly.pieter.com](https://fly.pieter.com/)
- Steam AI-disclosed games: ~33% of launches, ~10–27% of sales — [fragwyz](https://fragwyz.substack.com/p/three-years-of-ai-on-steam)
- B2B adjacent money is real: Sett $27M raised for AI ad and live-ops content for Playtika and others — [TechCrunch](https://techcrunch.com/2025/05/07/game-sett-funding-a-startup-building-ai-agents-for-game-development-emerges-from-stealth-with-27m)
- Jams as marketing channels: Cursor, Bolt.new, Glif and Tripo3D sponsor Vibe Jam ($50K+ prizes in 2026 vs $17.5K in 2025) — [vibejam.com/2026](https://vibejam.com/2026/)

### Inferences
- **Small games:** the business that works is "take a cut of player spend on a platform you own" (Roblox, Epic, 蛋仔, potentially TapTap and 抖音 IAA). Text-to-game is a creator-acquisition feature on top of it.
- **Startups:** the defensible revenue is selling tools to creators (SaaS credits, export rights), or selling AI to studios (Sett).
- **Coding-tool vendors** (Cursor, Bolt) treat game jams as marketing spend, which is evidence that "vibe-coded games" are currently a showcase category for coding agents rather than a market in themselves.

### Gaps
- No audited revenue for any pure-play text-to-game company.
- 抖音 / 微信 IAA revenue attributable to AI-made games is unknown.
- TapTap 制造, 代号Craft and Build monetization terms for creators are unpublished.

