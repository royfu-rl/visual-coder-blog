# AI Game Generation & World Generation Companies (国内+国外), state as of Oct 2026

Scope note: research ran 2026-10-13 with about 20 tool calls. Most figures come from trade press or aggregators, not company filings. Where sources conflict, I say so. Category map used below:
- (a) world models / interactive video
- (b) LLM-coded games / text-to-game
- (c) AI-native games & NPCs
- (d) AI tooling inside engines

## Landscape by category: product, route, funding, traction, demo

### Takeaway
Capital is concentrated in (a) world models, where 2026 rounds totalled about $3B and valuations are in the billions, but none of these companies discloses meaningful revenue. Category (b) has real user traction (Astrocade 10M MAU) and little disclosed revenue. Category (c) is contracting or pivoting. Category (d) is now mostly a bundled feature of the engines themselves (Unity, Roblox).

### Cited Findings

**(a) World models / interactive video**
- **Google DeepMind Genie 3 / Project Genie**
  - Launched Jan 29, 2026 as a website for Google AI Ultra subscribers, US-only. Users create and remix worlds that are generated as they move — [Wikipedia: Project Genie](https://en.wikipedia.org/wiki/Project_Genie_(website))
  - Game stocks fell on the launch. Per Morgan Stanley via Investing.com: Unity −24%, AppLovin −17%, Roblox −13%, Take-Two −7% — [Investing.com](https://www.investing.com/news/analyst-ratings/googles-genie-3-rollout-triggers-video-game-stock-selloff-93CH-4477348)
    - Reuters-based figures differ: Take-Two −10%, Roblox −12%, Unity −21% — [Seeking Alpha](https://seekingalpha.com/news/4544948-video-game-stocks-nosedive-as-googles-project-genie-allows-virtual-world-creation)
  - Morgan Stanley flagged "determinism, memory, and updates" as open obstacles — [Yahoo Finance](https://finance.yahoo.com/news/video-game-stocks-morgan-stanley-134811296.html)
- **World Labs (Fei-Fei Li), Marble**
  - Route: generates explorable 3D worlds; the output is 3D assets, not pixel video.
  - Marble went GA Nov 12, 2025. The World API launched Jan 21, 2026. The successor model Atlas entered early access Sep 1, 2026 — [Sacra](https://sacra.com/c/world-labs/)
  - Business model: subscriptions at $20–$95/month plus credits, with commercial rights from the Pro tier up. API usage is billed separately. Revenue and ARR are not disclosed — [Sacra](https://sacra.com/c/world-labs/)
  - Raised $1B in Feb 2026, with AMD, NVIDIA and Fidelity among backers — [VKTR](https://www.vktr.com/ai-news/world-labs-raises-1b-to-advance-spatial-intelligence-and-3d-world-modeling/)
    - Forbes reported a ~$5.4B post-money valuation. Another source says the company declined to confirm it — [ValueAdd VC](https://valueaddvc.com/blog/world-labs-valuation-what-fei-fei-lis-spatial-intelligence-startup-is-worth-at-5b)
- **Decart, Oasis**
  - Route: real-time, action-conditioned video world model, offered via API. Oasis was co-launched with Etched in Oct 2024 as a playable Minecraft-like demo. A 500M-parameter model and the code were open-sourced. Etched positioned its Sohu chip for future versions — [Forklog](https://forklog.com/en/etched-and-decart-unveil-ai-generated-game-demo/amp)
  - Oasis is now pitched for physical AI too (robotics and autonomous systems) — [Investgame](https://investgame.net/news/decart-raises-300m-series-b-at-4b-valuation)
  - Raised $300M in May 2026, led by Radical Ventures, at a ~$4B valuation (up from $3.1B in Aug 2025). Total raised is over $450M — [Investgame](https://investgame.net/news/decart-raises-300m-series-b-at-4b-valuation)
  - Sale talks at ~$6–7B are reported but conflicting:
    - Nvidia talks reportedly collapsed — [Calcalist](https://calcalistech.com/ctechnews/article/mrrffazk1)
    - Anthropic reportedly walked away after due diligence — [FourWeekMBA](https://fourweekmba.com/ai-anthropic-decart-acquisition-walk-away/)
    - None of these reports is confirmed.
  - No revenue figures found.
- **Odyssey**
  - Series B of $310M at a $1.45B valuation, announced June 17, 2026. Natural Capital led, with Amazon, AMD Ventures, GV and EQT participating. Total raised is $337M — [The AI Insider](https://theaiinsider.tech/2026/06/18/world-models-startup-odyssey-raises-310m-in-series-b-funding-valued-at-1-45b/)
  - Amazon signed Odyssey and Decart as Trainium customers — [Forbes](https://www.forbes.com/sites/josipamajic/2026/06/30/world-model-startups-raise-3-billion-vcs-bet-beyond-llms/)
- **Dynamics Lab, Mirage / Mirage 2**
  - Mirage (Jul 2025) was billed as the "first AI-native UGC game engine." Mirage 2 (Aug 2025) turns uploaded images into explorable worlds, with ~200ms latency and 10+ minute sessions — [Korben](https://korben.info/en/mirage-2-ai-game-engine-generates-worlds-real-time.html)
  - In June 2026 the Dynamics Lab founders were brought into Roblox, alongside the Morpheus AI acquisition — [PocketGamer.biz](https://pocketgamer.biz/roblox-strengthens-ai-ambitions-with-morpheus-ai-acquisition-and-founder-hires/), [Roblox newsroom](https://about.roblox.com/ko/newsroom/2026/06/pioneering-ai-founders-join-to-accelerate-roblox-reality-vision)
  - This is effectively an exit by acqui-hire. I did not verify Mirage's standalone status.
- **Sector totals**
  - VCs committed over $3B to world-model startups in H1 2026 — [Forbes](https://www.forbes.com/sites/josipamajic/2026/06/30/world-model-startups-raise-3-billion-vcs-bet-beyond-llms/)
  - AMI Labs (LeCun) raised a $1.03B seed at $3.5B — same source.
  - General Intuition: $220M round at a reported $6.2B (secondary tracker, unverified) — [AI Funding Tracker](https://aifundingtracker.com/best-gaming-startups-funding-stats/)
- **Tencent Hunyuan**
  - Hunyuan-GameCraft (built on HunyuanVideo): weights released Aug 14, 2025 under the Hunyuan Community License. Users control the camera with WASD from a single image. It is not real-time — [AMD ROCm blog](https://rocm.blogs.amd.com/artificial-intelligence/hunyuan-gamecraft/README.html), [CGWorld](https://cgworld.jp/flashnews/01-202508-Hunyuan-GameCraft.html)
  - HY-World 1.5 (WorldPlay): open-source real-time streaming world model at a claimed 24 FPS. Described as research/prototype grade — [Toolnavs](https://toolnavs.com/en/article/978-hy-world-15-worldplay-open-source-release-an-interactive-world-model-for-live-st), [CGWorld](https://cgworld.jp/flashnews/01-202601-HYWorld15.html)
- **昆仑万维 Matrix-Game**
  - 3.0 released Mar 2026 at the 中关村论坛, adding memory — [鱼皮AI导航](https://ai.codefather.cn/news/2038645316604960776)
  - 3.5 released Jul 2026 at WAIC: 5B model, 720p, 20 FPS on a single GPU, patch-level memory injection, core architecture open source — [Chinaz](https://www.chinaz.com/ainews/29705.shtml)
  - Chairman 方汉 declared 2026 the "世界模型元年" and named games as the first industry to be transformed — [网易订阅](https://www.163.com/dy/article/L2945VK805527PMU.html)
  - No revenue disclosed.
- **Other China**
  - AISphere (爱诗) released PixVerse R1, a real-time world model, and raised ¥2.98B — [Caixin Global](https://www.caixinglobal.com/2026-08-14/in-depth-game-studios-have-bought-into-ai-but-players-still-arent-sold-102474160.html)

**(b) LLM-coded games / text-to-game**
- **Astrocade**
  - Funding: $56M (Series A led by Sea, Series B led by Sequoia), May 2026. Google AI Futures Fund, NVIDIA and LG also invested — [Traded](https://traded.co/deals/national/all/sale/astrocade-secures-56-million-in-series-a-and-b-funding-led-by-sequoia-capital/)
  - Traction (company-reported): MAU went from 5M to 10M in four months, with 220M sessions per month — reported Oct 2026 by GamesBeat via [Mezha](https://mezha.ua/en/news/ai-slop-games-is-popular-315954/)
  - Content quality issues: 100K+ projects, including Minecraft and Roblox clones and copyrighted characters — same source.
- **Rosebud AI**
  - Prompt-to-3D-games and web apps. Funding data conflicts: $1.5M seed / $15M Series A / $6.6M in 2021 — [Seedtable](https://seedtable.com/companies/rosebud-ai), [Signalbase](https://www.trysignalbase.com/news/funding/breaking-boundaries-rosebud-ai-secures-15m-in-series-a-funding-for-game-changing-ai-platform), [PitchBook](https://pitchbook.com/profiles/company/343168-12)
  - No traction data found.
- **Ludo.ai**: an ideation and asset tool, not a full game generator — [Cinevva](https://app.cinevva.com/guides/ai-game-generators-2026)
- **SEELE (全灵)**
  - Founded end of 2022. Its first overseas product reached nearly 1M users in six months — [智源社区](https://hub.baai.ac.cn/view/41167)
  - Demoed text → playable game clip at WAIC 2026 — [腾讯新闻](https://news.qq.com/rain/a/20260716A0BH3200)
- **Tencent 代号 Craft**: an AIGC game-creation platform unveiled at SPARK 2026, with 10K+ free art assets — [IT之家](https://www.ithome.com/0/956/225.htm)
- **TapTap 制造**: an AI game-creation agent, Jan 2026 — [OFweek / 知乎 summary](https://zhuanlan.zhihu.com/p/2075159815358361699)
  - TapTap hosts 4,000+ AI-generated mini-games — [Caixin Global](https://www.caixinglobal.com/2026-08-14/in-depth-game-studios-have-bought-into-ai-but-players-still-arent-sold-102474160.html)
- **抖音 / 小红书**
  - 抖音 "互动空间" and 小红书 "小工具" generate mini-games with AI. Both are in closed beta, and 互动空间 does not yet support monetization (IAA is being considered) — [知乎](https://zhuanlan.zhihu.com/p/2075159815358361699)
  - 抖音 IAA mini-game revenue grew 80% YoY in Q1 2026 — same source.
- **微信**
  - 500M+ mini-game MAU (May 27, 2026 dev conference) — [OFweek](https://cloud.ofweek.com/news/2026-06/ART-178808-8110-30689646.html)
  - 阿里 Meoo(秒悟) added WeChat mini-program generation in Jun 2026 — same source.
  - No official WeChat AI-game generator found.
- **"One-sentence game"**: 崇祯模拟器 was made with a one-sentence-game engine and drew 25K players — [Caixin Global](https://www.caixinglobal.com/2026-08-14/in-depth-game-studios-have-bought-into-ai-but-players-still-arent-sold-102474160.html)

**(c) AI-native games & NPCs**
- **Inworld AI**
  - Pivoted from game NPCs to a general voice-AI stack (TTS/STT plus the C++ "Agent Runtime"). Realtime TTS-2 shipped in 2026; the month is given as May or Aug depending on source — [AIWiki](https://www.aiwiki.ai/wiki/inworld_ai)
  - Funding: ~$117–153M total, last major round 2023 (Series A-1 ~$520M post-money per one profile) — [Welcome to the Jungle](https://app.welcometothejungle.com/jobs/a73Ec_ja/company), [Tracxn](https://tracxn.com/d/companies/inworld-ai/__tjWZC3FjI2Vxjo9ijvchq0joN7t3zWc5nHkAN9FWwuk)
  - No 2026 round found.
- **Convai**: $4.75M over 2 rounds, last in Jan 2023. No revenue data — [CB Insights](https://www.cbinsights.com/company/convai-1/financials)
- **Latitude / AI Dungeon**
  - Estimated $1.4–1.8M ARR (third-party estimate). ~$4M seed, last raised Apr 2023 — [IntelPilot](https://www.intelpilot.ai/company/latitude/6a028ebda6715bdc30963e7e)
  - The "Voyage" platform (Apr 2026) is single-source and unverified.
- **网易《逆水寒》手游**
  - 2023: first Chinese mobile game with AI NPCs.
  - Feb 2025: DeepSeek-driven NPC 沈秋索 — [China Daily](http://ex.chinadaily.com.cn/exchange/partners/82/rss/channel/cn/columns/sz8srm/stories/WS67b2f7e1a310ff9bbd9f371b.html)
  - GDC 2026: "剧组站" (in-game AI video UGC feed) reached 5M swipes/day. 36氪 headline says players earn "年收入破亿" via in-game AI — summarized via [搜索摘要 of 36氪](https://36kr.com/p/3722503178041737). I couldn't load the page (blocked), so I did not verify the figure.
  - 2026 roadmap: more 智能NPC plus a Seedance integration — [IT之家](https://www.ithome.com/0/922/195.htm)
- **Anuttacon (蔡浩宇), Whispers from the Star**
  - Steam launch Aug 2025. Est. 34.2K copies and ~$290K gross; 80% positive across 1,677 reviews (Raijin estimate) — [Raijin](https://raijin.gg/app/3730100/Whispers_from_the_Star/sales-revenue)
  - The team stopped development of later versions, citing a lack of conflict and goal pacing.
  - The AnuNeko chat app shut down in under a year.
  - Compute moved to ~90% LLM work. The chief scientist left for OpenAI (May 2026).
  - Cai's LinkedIn shows his Anuttacon role ending Jul 2026. There has been no official closure announcement — [投资界/QbitAI](https://news.pedaily.cn/202607/567090.shtml)
- **Ubisoft Teammates**
  - A playable generative-AI R&D experiment: voice-commanded AI squadmates, Google Gemini plus in-house middleware on Snowdrop, ~80-person team. It is not a product — [Game Developer](https://www.gamedeveloper.com/business/ubisoft-s-first-playable-generative-ai-experience-is-an-r-d-experiment-called-teammates-)
  - Ubisoft is "accelerating investment" in it — [Insider Gaming](https://insider-gaming.com/ubisoft-investment-playable-generate-ai-experience/)

**(d) AI tooling inside engines**
- **Unity AI**
  - Muse was retired on Oct 1, 2025 and replaced by Unity AI in Unity 6.2+.
  - Components: Assistant (code and actions) plus Generators (sprites, textures, sound, animation). It uses third-party models.
  - AI Gateway lets Claude, Codex and Gemini agents drive the Editor, and an MCP server is available.
  - Pricing: Personal tier $10/month for 1,000 credits. Included in Pro and Enterprise seats — [Unity docs](https://docs.unity.com/ai/ai-overview), [unity.com/ai](https://unity.com/ai)
- **Roblox**
  - Cube 3D generated 1.8M+ objects since Mar 2025 — [Roblox newsroom](https://about.roblox.com/de/newsroom/2026/02/accelerating-creation-powered-roblox-cube-foundation-model)
  - 4D generation (interactive objects such as cars and planes) went to open beta Feb 5, 2026.
    - Wish Master players generated 160K objects, with +64% playtime among users — same source / [TechCrunch via Dealroom](https://app.dealroom.co/news/feed/roblox-launches-4d-creation-tool-in-open-beta-lets-users-design-interactive-objects-with-ai)
  - Acquired Morpheus AI (Self Forcing real-time video world models) Jun 3, 2026 for "Roblox Reality", a hybrid engine plus world-model architecture. An early version is due in 2026 — [Shacknews](https://www.shacknews.com/article/149425/roblox-acquires-morpheus-ai-company)
- **Scenario**
  - $6M seed (Jan 2023, Play Ventures) — [TechCrunch](https://techcrunch.com/2023/01/19/scenario-lands-6m-for-its-ai-platform-that-generates-game-art-assets)
  - 15K+ customers including Ubisoft, Unity and Scopely — [Caplight](https://www.caplight.com/company/scenario)
- **Layer AI**
  - $6.5M seed (May 2025), with King co-founder Zacconi's vehicle participating.
  - 200+ studios use it for live-service content pipelines — [Layer blog](https://www.layer.ai/blog/layer-raises-6-5m-usd-next-gen-tools-game-studios)
- **Promethean AI**: ~$300K total raised (Disney Accelerator), status active, no new round — [CB Insights](https://www.cbinsights.com/company/promethean-ai/financials)
  - Not to be confused with Bezos's Project Prometheus.
- **Tencent Hunyuan 3D**: used for asset creation — [Caixin Global](https://www.caixinglobal.com/2026-08-14/in-depth-game-studios-have-bought-into-ai-but-players-still-arent-sold-102474160.html)

### Inferences
- The world-model category is priced on frontier-lab and physical-AI optionality, not on game revenue.
  - Decart is being repositioned toward robotics.
  - Roblox absorbed Morpheus and the Dynamics Lab founders.
  - The likeliest path for a game world-model startup appears to be acquisition by a platform.
- Text-to-game is converging on the "UGC feed of tiny games" model: Astrocade, 抖音互动空间, 小红书小工具, TapTap. Distribution is the moat, and quality/IP is the problem.

### Gaps
- No disclosed revenue for World Labs, Decart, Odyssey, Astrocade, Rosebud, SEELE or Matrix-Game.
- Bezi, Jabali, Playroom and Cybever were not researched (tool budget). Etched's 2026 world-model work was not found.
- I could not verify Hunyuan-GameCraft adoption numbers. The "300万下载" WorldPlay figure comes from a single blog.

## Which approach has real revenue vs. just demos?

### Takeaway
Real money flows in three places:
- Platform-embedded AI that lifts engagement (逆水寒, Roblox 4D)
- Engine and asset tooling sold as seats or credits (Unity AI, Scenario, Layer)
- Mini-game distribution (抖音/微信 IAA)

Standalone world models remain demo plus subscription with undisclosed revenue. AI-native narrative games have flopped commercially.

### Cited Findings
- Whispers from the Star: ~$290K estimated gross on Steam. The studio has stalled — [Raijin](https://raijin.gg/app/3730100/Whispers_from_the_Star/sales-revenue), [投资界](https://news.pedaily.cn/202607/567090.shtml)
- AI Dungeon: est. $1.4–1.8M ARR — [IntelPilot](https://www.intelpilot.ai/company/latitude/6a028ebda6715bdc30963e7e)
- World Labs does not disclose revenue. Monetization is $20–95/month plans plus API — [Sacra](https://sacra.com/c/world-labs/)
- Roblox 4D: +64% playtime among users of the showcase game — [Roblox newsroom](https://about.roblox.com/de/newsroom/2026/02/accelerating-creation-powered-roblox-cube-foundation-model)
- 抖音 IAA mini-games +80% YoY in Q1 2026, but the AI 互动空间 is not yet monetized — [知乎](https://zhuanlan.zhihu.com/p/2075159815358361699)
- China: 70 AI titles at ChinaJoy 2026 and thousands of AI demos on Steam in H1 2026. A "trust crisis" is emerging, and many say AI "fails to create genuinely new gameplay" — [Caixin Global](https://www.caixinglobal.com/2026-08-14/in-depth-game-studios-have-bought-into-ai-but-players-still-arent-sold-102474160.html)

### Inferences
- The revenue ranking, roughly: engine/tool seats ≳ platform engagement features > text-to-game UGC (traffic, little revenue) > world-model subscriptions > premium AI-native games.

### Gaps
- No audited revenue for any pure-play AI game company was found.

## What do big studios actually deploy?

### Takeaway
Big studios deploy AI mostly in production pipelines and as live-ops features, not as generated gameplay. NetEase (逆水寒 AI NPC + AI video UGC) and Roblox (Cube/4D, Morpheus) ship to players. Ubisoft Teammates is still R&D. Developer sentiment has turned sharply negative.

### Cited Findings
- GDC 2026 State of the Industry survey (2,300+ respondents):
  - 36% use gen-AI at work (30% at studios vs 58% in business roles).
  - 52% say gen-AI is negative for the industry (up from 30%); 7% say positive.
  - Use is mostly brainstorming (81%) and code (47%) — [Sean Kim blog summarizing GDC](https://blog.imseankim.com/gdc-2026-ai-game-development-npcs-procedural-content-voice-acting/)
- Tencent:
  - Hunyuan 3D for assets — [Caixin Global](https://www.caixinglobal.com/2026-08-14/in-depth-game-studios-have-bought-into-ai-but-players-still-arent-sold-102474160.html)
  - Open-source GameCraft / HY-World — see category (a)
  - 代号 Craft creator platform — [IT之家](https://www.ithome.com/0/956/225.htm)
- miHoYo plans to invest ¥100B in AI — [Caixin Global](https://www.caixinglobal.com/2026-08-14/in-depth-game-studios-have-bought-into-ai-but-players-still-arent-sold-102474160.html)
- Ubisoft Teammates (Gemini-based R&D) — [Game Developer](https://www.gamedeveloper.com/business/ubisoft-s-first-playable-generative-ai-experience-is-an-r-d-experiment-called-teammates-)
- EA: the only source is a blog listing it as a confirmed gen-AI user — [PokeIndie](https://pokeindie.com/blog/major-studios-admitted-using-ai-what-they-said)

### Inferences
- What studios ship is AI as a feature inside existing hits (NPC chat, UGC video, object generation), not AI-generated games.

### Gaps
- EA's specific 2026 deployments and NetEase's internal pipeline usage were not verified from primary sources.

## Notable 2025–2026 fundings and shutdowns

### Takeaway
2026 brought mega-rounds for world models: World Labs $1B, AMI $1.03B, Decart $300M, Odyssey $310M. Text-to-game drew mid-size rounds (Astrocade $56M). Exits and shutdowns hit the NPC and AI-native game side: Anuttacon stalled, AnuNeko closed, and Dynamics Lab and Morpheus were absorbed by Roblox.

### Cited Findings
- Fundings:
  - World Labs $1B (Feb 2026) — [VKTR](https://www.vktr.com/ai-news/world-labs-raises-1b-to-advance-spatial-intelligence-and-3d-world-modeling/)
  - Decart $300M at ~$4B (May 2026) — [Investgame](https://investgame.net/news/decart-raises-300m-series-b-at-4b-valuation)
  - Odyssey $310M at $1.45B (Jun 2026) — [The AI Insider](https://theaiinsider.tech/2026/06/18/world-models-startup-odyssey-raises-310m-in-series-b-funding-valued-at-1-45b/)
  - AMI Labs $1.03B seed — [Forbes](https://www.forbes.com/sites/josipamajic/2026/06/30/world-model-startups-raise-3-billion-vcs-bet-beyond-llms/)
  - Astrocade $56M (May 2026) — [Traded](https://traded.co/deals/national/all/sale/astrocade-secures-56-million-in-series-a-and-b-funding-led-by-sequoia-capital/)
  - Layer $6.5M (May 2025) — [Layer](https://www.layer.ai/blog/layer-raises-6-5m-usd-next-gen-tools-game-studios)
  - AISphere ¥2.98B — [Caixin Global](https://www.caixinglobal.com/2026-08-14/in-depth-game-studios-have-bought-into-ai-but-players-still-arent-sold-102474160.html)
- M&A and exits:
  - Roblox acquired Morpheus AI (Jun 2026) — [Shacknews](https://www.shacknews.com/article/149425/roblox-acquires-morpheus-ai-company)
  - Dynamics Lab and Lucid AI founders joined Roblox — [PocketGamer.biz](https://pocketgamer.biz/roblox-strengthens-ai-ambitions-with-morpheus-ai-acquisition-and-founder-hires/)
  - Decart sale talks (Nvidia, Anthropic) unconfirmed — [Calcalist](https://calcalistech.com/ctechnews/article/mrrffazk1)
- Shutdowns and retreats:
  - Anuttacon's AnuNeko closed. Whispers sequel development halted. Cai's role ended Jul 2026 — [投资界](https://news.pedaily.cn/202607/567090.shtml)
  - Unity Muse retired on Oct 1, 2025 — [Unity docs](https://docs.unity.com/ai/ai-overview)
  - Inworld pivoted away from game-only NPCs — [AIWiki](https://www.aiwiki.ai/wiki/inworld_ai)
- Thesis: a16z speedrun (Jonathan Lai) calls world models "the big storytelling story of 2026" and expects new "generative world experiences" — [a16z speedrun](https://speedrun.substack.com/p/14-big-ideas-for-2026)

### Inferences
- Money is following "world model as foundation-model category" rather than games specifically. Game-first startups exit into platforms like Roblox.

### Gaps
- No shutdown reports found for Rosebud, Ludo.ai, Convai, Scenario or Promethean. That absence does not prove they are healthy.
- Bezi, Jabali, Playroom and Cybever status was not checked.

