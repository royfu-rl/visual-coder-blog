# World Models / Interactive Generative Video: technical + commercial dossier (国内+国外), as of 2026-10-13

Research notes, round 2. This goes deeper than `game_world_gen.md` and does not repeat it.

**Method**
- About 70 tool calls: ~38 WebSearch, ~30 WebFetch, 3 curl batches.
- The shared WebSearch budget ran out partway through. After that I worked only from direct fetches of primary pages plus curl.

**Source-type tags used on every number**
- **[官方]** = company blog, docs, GitHub/HF, or SEC filing
- **[媒体]** = trade or tech press
- **[三方]** = aggregator, wiki, or estimate site; weaker
- **[自测]** = my own curl check on 2026-10-13, run through the overseas squid proxy
- **[推算]** = my arithmetic from the cited numbers

---

## Q1. Per-player dossier: specs, open weights, funding, pricing, demo URL

### Takeaway
- **Spec ceiling (Oct 2026):** 720p at 20–40 fps for streamed pixel-video world models.
  - Exceptions:
    - PixVerse R1 claims 1080p.
    - World Labs Atlas reaches 1440p, but it is not real-time.
  - Consistent memory lasts roughly 1 to several minutes.
  - Matrix-Game 3.0 claims 40 fps but needs 8 GPUs per stream.
- **Two technical routes are pulling apart:**
  - **Pixel-stream models:** Genie 3, Odyssey, Decart, Runway GWM, PixVerse R1, HappyOyster, Matrix-Game, HY-World 1.5.
  - **Explicit-3D asset models:** World Labs Marble, Tencent HY-World 2.0. These export Gaussian splats and meshes.
- **The capital story changed in Sep 2026:**
  - AMD agreed to buy World Labs for about $8.2B in stock.
  - Anthropic walked away from Decart at about $6B.
  - Roblox absorbed Morpheus, Dynamics Lab and Lucid.
- **The Chinese side is mostly open-weight:** Tencent, Skywork/Riemann Dynamics, SenseTime/大晓. Alibaba and PixVerse are the exceptions, both closed products.

### Cited Findings

#### A. Google DeepMind: Genie 3 / Project Genie
- **Specs:** Genie 3 runs at 720p and 24 fps, with about 1 minute of memory. Genie 2 managed 10–20 s at 360p.
  - The 11B parameter figure is wiki-sourced and not confirmed by DeepMind — [三方] [Wikipedia: Project Genie](https://en.wikipedia.org/wiki/Project_Genie_(website))
- **Session cap:** Project Genie sessions are capped at **60 seconds**. DeepMind's reason is that Genie 3 is autoregressive and compute-heavy, so longer sessions raise cost with little added value — [三方] [Wikipedia](https://en.wikipedia.org/wiki/Project_Genie_(website)); 60 s, 720p and 24 fps are confirmed by [媒体] [Engadget, 2026-05-19](https://engadget.com/2176797/project-genie-adds-google-street-view-integration-and-goes-live-for-global-ai-ultra-users)
- **Availability timeline:**
  - 2026-01-29: US only, AI Ultra subscribers aged 18+.
  - 2026-05-19: rolled out worldwide to adult AI Ultra subscribers, plus Street View "real places", which are US-only at first — [媒体] [Engadget](https://engadget.com/2176797/project-genie-adds-google-street-view-integration-and-goes-live-for-global-ai-ultra-users)
  - It sits on the $200/month Ultra tier, after the Ultra plan was split into $100 and $200 tiers — [三方] search digest of the heise and Engadget coverage, not verified on Google's pricing page.
  - Still labelled an experimental research prototype in Labs.
- **Open weights:** none.
- **API:** none public.
- **Usage numbers:** not disclosed.
- **Critiques:**
  - Verge: slow.
  - Fast Company: 24 fps is too low.
  - TechCrunch: blocks copyrighted characters — [三方] [Wikipedia](https://en.wikipedia.org/wiki/Project_Genie_(website))
- **Internal "customer": Waymo World Model** (2026-02-06), built on Genie 3 — [官方] [Waymo blog](https://waymo.com/blog/2026/02/the-waymo-world-model-a-new-frontier-for-autonomous-driving-simulation)
  - Outputs camera and lidar (4D point clouds).
  - Controlled by language, driving inputs and layout.
  - Turns dashcam or phone video into simulations.
  - An efficient variant handles long rollouts.
  - Waymo cites ~200M real autonomous miles and "billions" of virtual miles.
- **Demo URL:** `https://labs.google/projectgenie` returns HTTP 200 [自测]. A login and an Ultra subscription are required.

#### B. World Labs (Fei-Fei Li): Marble / World API / RTFM / Atlas → AMD
- **Products and dates** — [官方] [World Labs blog index](https://www.worldlabs.ai/blog)
  - RTFM, a real-time frame model: 2025-10-16.
  - Marble GA: 2025-11-12.
  - World API: 2026-01-21.
  - New funding: 2026-02-18.
  - Spark 2.0 (3DGS web streaming): 2026-04-14.
  - Acquired SceniX: 2026-07-21.
  - "Building Worlds That Train Robots": 2026-07-28.
  - Atlas: 2026-09-01.
  - "World Labs is Joining AMD": 2026-09-28.
- **Pricing**
  - Reported tiers: Free (4 outputs), $20/month (12 outputs), $35/month (25 outputs, with expansion and commercial rights), $95/month (75 outputs) — [媒体] [DeepLearning.AI The Batch](https://charonhub.deeplearning.ai/world-labs-makes-its-marble-generative-world-model-public-adds-chisel-editing-tool/)
  - A Marble world costs 1,500 credits. Expansion, HQ mesh export and video enhancement cost extra. API credits are prepaid and expire after one year — [三方] [Sacra](https://sacra.com/c/world-labs/)
  - Per-world API USD price is unconfirmed. Third-party claims range from ~$0.12 per Draft world to ~$1.20 per standard world — [三方] search digests. The official API doc gives no USD figure — [官方] [docs.worldlabs.ai/api](https://docs.worldlabs.ai/api)
- **Export formats** — [官方] [docs.worldlabs.ai/api](https://docs.worldlabs.ai/api)
  - Gaussian splats in SPZ at 100k, 500k and full resolution, and in PLY.
  - Collider mesh as GLB.
  - High-quality textured mesh as GLB.
  - Full-resolution vertex-coloured mesh as GLB.
  - Panorama and thumbnail images.
  - Generation takes about 5 min. API model IDs are `marble-1.1` and `marble-1.1-plus`.
  - Plan gating (official docs, quoted via search digest):
    - Standard: splats, panorama and collider mesh.
    - Pro: HQ GLB mesh and commercial rights.
    - Free: cannot export.
- **API launch partners (Jan 2026)** — [官方] [World API post](https://www.worldlabs.ai/blog/announcing-the-world-api)
  - Preview (film previs), Fenestra (architecture), Escape.ai (2D film → 3D), Lightwheel (robotics), xFigura (architecture), Interior AI.
  - Simulator integrations: Isaac Sim, MuJoCo, RoboSuite.
  - HTC VIVERSE has a collaboration that produced 3 experiences — [官方 PR] [Nasdaq/HTC](https://www.nasdaq.com/press-release/htc-viverse-collaborates-world-labs-turn-ai-generated-worlds-interactive-experiences)
- **RTFM:** runs on a single H100 at "interactive framerates" and treats posed frames as spatial memory. World Labs itself calls naive approaches "neither feasible nor economically viable". Demo at rtfm.worldlabs.ai — [官方] [RTFM post](https://www.worldlabs.ai/blog/rtfm)
- **Atlas** (2026-09-01)
  - Omni world model producing up to 1 min of camera-controlled video at **1440p**.
  - Reconstructs from 2–3 photos and outputs point clouds or 3DGS.
  - Early access goes to selected partners.
  - No paper, no pricing, no GA date.
  - Raters preferred it 75% of the time over MiniMax H3 and 94% over Seedance 2.5 (vendor-reported) — [媒体] [Implicator](https://www.implicator.ai/world-labs-atlas-withholds-paper-price-partners/), [Gigazine](https://gigazine.net/gsc_news/en/20260902-world-model-atlas)
- **Funding and exit**
  - Funding history:
    - $230M at launch (Sep 2024).
    - $1B on 2026-02-18, with Autodesk putting in $200M.
    - About $1.23B raised in total — [三方] [Sacra](https://sacra.com/c/world-labs/)
  - **AMD acquisition:**
    - About **$8.2B, all-stock**, announced 2026-09-28; merger agreement dated 2026-09-26 per SEC filing. Expected to close by end of 2026.
    - Li becomes AMD EVP and Chief Scientist.
    - Implied premium of about 75% over the roughly $5B February valuation.
    - Revenue, users and headcount were not disclosed even at the deal — [媒体] [The Next Platform](https://www.nextplatform.com/ai/2026/09/29/amd-buys-world-labs-for-82-billion-to-get-ai-model-cred/5299801), [Data Center Knowledge](https://datacenterknowledge.com/data-center-chips/amd-to-acquire-world-labs-for-8-2b-to-advance-ai-models-and-robotics), [SDxCentral](https://www.sdxcentral.com/news/amd-acquires-ai-research-firm-world-labs-in-all-stock-deal-worth-82b/)
    - Next Platform frames it as a reaction to "Nvidia's $12.9B Hugging Face acquisition". I did not verify that deal; it is single-source here.
- **Demo URLs:** `marble.worldlabs.ai` and `platform.worldlabs.ai` both return HTTP 200 [自测].

#### C. Decart (Israel): Oasis 1/3, MirageLSD, Lucy, DOS
- **Oasis 1** (2024-10-31, with Etched)
  - 360p at 20 fps on H100.
  - 500M-parameter weights open on GitHub (`etched-ai/open-oasis`, 2,145 stars [自测 via GitHub API]).
  - Known faults: hazy output, forgets layout when the player turns around — [媒体] [The Decoder](https://the-decoder.com/ai-generated-game-oasis-now-turns-images-into-playable-3d-worlds/); [官方] [Etched blog](https://etched.com/blog-posts/oasis)
  - **"Oasis 2":** I found no product by that name. The line went from Oasis to Oasis 3.
- **MirageLSD** (2025-07-19)
  - 768×432 at 20 fps, <40 ms per frame, tuned for Hopper. Web version at mirage.decart.ai — [媒体] [The Decoder](https://the-decoder.com/decart-launches-miragelsd-an-ai-model-that-transforms-live-video-feeds-in-real-time)
  - Wired and eWeek report about **100 ms** end-to-end latency. A wiki claim of 24 fps / 40 ms is unverified — [媒体] search digest.
  - Mirage is no longer on the decart.ai homepage, and `mirage.decart.ai` timed out (HTTP 000) [自测]. It looks retired or replaced by Lucy.
- **Lucy 2.5** ("World Editing", live video at 30 fps) — [官方] [decart.ai](https://decart.ai)
  - Uses: try-on, live ads, streaming.
  - Partners: Comcast (edge, sub-35 ms) and ElevenLabs (living characters).
  - The public platform lists Lucy, Virtual Try-On and Restyle. No price is shown — [官方] [platform.decart.ai](https://platform.decart.ai)
- **Oasis 3** (TechCrunch 2026-06-10) — [媒体] [TechCrunch](https://techcrunch.com/2026/06/10/decarts-new-world-model-can-simulate-hours-of-photorealistic-driving-with-some-caveats/)
  - Photorealistic **multi-camera driving** (front plus two sides), built on Lucy.
  - Autoregressive, about 8,000 tokens per frame.
  - **API at $0.02 per second**; enterprise pricing on request.
  - No set length limit.
  - CEO claims it is "more than an order of magnitude cheaper than anyone else" (unverified).
  - Lifetime burn is "drastically less" than $100M.
  - **100,000+ developers**, mostly on Lucy.
- **Funding** — [媒体] [InvestGame, 2026-05-25](https://investgame.net/news/decart-raises-300m-series-b-at-4b-valuation)
  - Rounds:
    - $21M seed (Oct 2024).
    - $32M Series A at >$500M.
    - $100M at $3.1B (Aug 2025).
    - **$300M Series B at ~$4B post**, led by Radical.
  - New investors in the Series B: NVIDIA, Adobe Ventures, Toyota Ventures, eBay Ventures, Atreides, Valor.
  - **Amazon is a strategic customer** and chip co-design partner via Annapurna/Trainium.
  - DOS 2.0 claims full-HD video at up to 100 fps and sub-30 ms input response.
- **Revenue**
  - No company figure.
  - Third-party estimate: **$12.6M revenue in 2024** — [三方] [GetLatka](https://getlatka.com/companies/decart.ai)
  - A 2024 Hebrew-press headline says it became "profitable within 3 months" — [媒体, via decart.ai homepage press list]
- **M&A**
  - Reports said Nvidia talks happened and the founders weighed a $6–7B sale — [媒体] [Runtimewire](https://runtimewire.com/article/decart-sale-talks-nvidia-bid-dean-leitersdorf-moshe-shalev)
  - **Anthropic ~$6B talks were abandoned after due diligence**, per Bloomberg on 2026-09-08. Both companies declined to comment — [媒体] [Ynet](https://ynetnews.com/business/article/bkiumz6dze), [TNW](https://thenextweb.com/news/anthropic-walks-away-decart-6bn-acquisition)
  - The rationale centred on DOS chip efficiency, not world models.
  - Status today: independent.
- **Demo URLs**
  - `oasis.decart.ai` → `/welcome`, HTTP 200 [自测].
  - `platform.decart.ai`: HTTP 200 [自测].
  - `mirage.decart.ai`: timeout [自测].

#### D. Odyssey (Palo Alto; founders from self-driving)
- **Odyssey-1** (May 2025)
  - Up to 30 fps, a frame every 40 ms.
  - Runs on H100 clusters at **$1–2 per user-hour**.
  - Layouts are unstable — [媒体] [TechCrunch 2025-05-28](https://techcrunch.com/2025/05/28/odysseys-new-ai-model-streams-3d-interactive-worlds/)
- **Odyssey-2** (2025-10-27)
  - Causal and autoregressive, a frame every 50 ms (about **20 fps**), "multi-minute" streams.
  - The API was "coming soon" at launch — [官方] [Odyssey-2 post](https://odyssey.systems/introducing-odyssey-2)
- **Odyssey-2 Pro API:** launched about 2026-01-26 via a developer portal. No public price — [媒体] [Aihola](https://aihola.com/article/odyssey-2-pro-api-real-time-video)
  - One review says 720p at about 22 fps — [三方] [Stork](https://www.stork.ai/tool/odyssey-2-pro)
  - An "Odyssey-2 Max" reportedly came in Apr 2026 at about 50 ms per frame, 720p — [三方] [Noqta](https://noqta.tn/en/blog/odyssey-2-max-world-models-real-time-simulation-2026)
- **Odyssey-3** (2026-10-08) — [官方] [Meet Odyssey-3](https://odyssey.systems/meet-odyssey-3)
  - Three variants:
    - Base: 832×480.
    - **Pro: 1280×720.**
    - Flash: distilled, few-step, real-time.
  - Physics-IQ Verified V2V score of 66.1, best-of-8. That falls short of the benchmark's record-submission protocol — [媒体] [TNW](https://thenextweb.com/news/odyssey-3-world-model-robots-humanoids-cars-drones)
  - **Robotics partner: Flexion** (humanoid policies). Real-road driving in India using about 20 h of data.
  - The cost charts assume **$1 per AMD MI355X GPU-hour**, which shows Odyssey runs on AMD.
  - No fps, latency or pricing published.
  - Base model is 14B parameters per a secondary source — [三方] [OrcaRouter](https://www.orcarouter.ai/es/blog/odyssey-3-research-preview-launch)
- **Other models:** Agora-2 (multi-agent shared simulation, agora.odyssey.systems), PROWL-2 (RL) and Starchild-1 — [官方] [odyssey.systems](https://odyssey.systems)
- **Funding:** $310M Series B at $1.45B (June 2026). Investors include Amazon and AMD Ventures — [媒体] [TNW](https://thenextweb.com/news/odyssey-3-world-model-robots-humanoids-cars-drones)
- **Revenue:** none disclosed.
- **Demo URLs:** `experience.odyssey.systems`, `agora.odyssey.systems` and `odyssey.systems/meet-odyssey-3` all return HTTP 200 [自测].

#### E. Runway: GWM-1 → GWM Worlds 2
- **GWM-1** (2025-12-11) — [官方] [Runway](https://runway.com/research/introducing-runway-gwm-1); [媒体] [TechCrunch](https://techcrunch.com/2025/12/11/runway-releases-its-first-world-model-adds-native-audio-to-latest-video-model)
  - Built on Gen-4.5, at 720p and 24 fps. Runway's page says up to 2 min.
  - Three post-trained variants:
    - **Worlds**
    - **Avatars:** available via API as "Runway Characters".
    - **Robotics:** Python SDK through the developer portal.
  - Customers: none named; "in conversations with several robotics firms".
- **GWM Worlds 2** (2026-09-03) — [官方] [Runway](https://runway.com/research/introducing-gwm-worlds-2)
  - 720p at 24 fps, with 48 kHz audio.
  - **No fixed duration** ("can generate indefinitely").
  - Memory is a sliding KV-cache window; Runway admits long-term memory is imperfect.
  - **Multiplayer via roles** (player 1, player 2, director), with LiveKit broadcasting.
  - Free-form text actions ("WorldPrompt").
  - Access is a research preview via contact form. No price.
- **Open weights:** none.
- **Demo:** no public demo. `app.runwayml.com` returns HTTP 200, but that is the generic app [自测].

#### F. Dynamics Lab: Mirage / Mirage 2 → Roblox
- **Mirage 2** (Aug 2025)
  - Turns uploaded images into worlds.
  - About 200 ms latency, 10+ min sessions, runs on a single consumer-grade GPU in the cloud.
  - fps and resolution never published.
  - Controls are imprecise — [媒体] [Gigazine](https://www.gigazine.net/gsc_news/en/20250825-ai-generative-world-mirage-2), [Plain Concepts](https://www.plainconcepts.com/world-simulation/)
- **Status:** founder Joe Chenn joined Roblox in late 2025 — [媒体] [PocketGamer.biz](https://pocketgamer.biz/roblox-strengthens-ai-ambitions-with-morpheus-ai-acquisition-and-founder-hires/)
- **Demo URL:** `demo.dynamicslab.ai/chaos` **timed out** (HTTP 000) [自测]. `dynamicslab.ai` returns 200 but the page is empty. Treat the demo as **dead or unreachable**.

#### G. Morpheus AI → Roblox Reality (plus Lucid AI)
- Roblox acquired the Morpheus AI team and technology; the deal was reported 2026-06-09, price undisclosed.
  - Founder **Xun Huang** invented **Self Forcing**, a method that turns offline video diffusion into a real-time autoregressive generator. The code is at github.com/guandeh17/Self-Forcing, HTTP 200 [自测].
  - **Roblox Reality** is a hybrid: video world models handle the visuals, while the Roblox Engine keeps game logic and **multiplayer state sync**. The target is **4K at 60 Hz** — [媒体] [PocketGamer.biz](https://pocketgamer.biz/roblox-strengthens-ai-ambitions-with-morpheus-ai-acquisition-and-founder-hires/)
- **Roblox Q2-2026 shareholder letter** (2026-07-30) — [官方] [SEC 8-K Ex.99.1](https://www.sec.gov/Archives/edgar/data/0001315098/000162828026051059/ex991-robloxq22026earnin.htm)
  - Calls Morpheus a "foundational, multi-year bet". Roblox Reality is named as incremental Q3 infrastructure spend.
  - Infra and T&S expense up 54% YoY, mainly from AI.
  - Cube generates **60k+ 3D assets per day**, and ~1,400 games use Cube content daily.
  - No launch date for Roblox Reality.
- **Lucid AI** (YC W25; founders Alberto Hojel and Rami Seid)
  - Lucid-v1 (2024-11-11) was a Minecraft world model running in real time on an RTX 4090.
  - Its tokenizer used 15 tokens per frame — [官方] [Lucid substack](https://ramimo.substack.com/p/lucid-v1-a-world-model-that-does); [官方] [YC](https://www.ycombinator.com/companies/lucid)
  - Hojel joined Roblox in late 2025 — [媒体] PocketGamer.biz
  - The "Lucid sim" in the brief may mean MIT's LucidSim (robot sim). `lucidsim.ai` timed out [自测]; not researched further.

#### H. Etched (Oasis co-developer)
- Projected Oasis on Sohu at up to 4K; this was never shown as measured — [官方] [Etched blog](https://etched.com/blog-posts/oasis)
- I found **no 2026 world-model product**. 2026 news is about the chip:
  - Out of stealth 2026-06-30, with an 8-chip rack.
  - A reported $300M Series C at $10.3B (Jul 2026). Another report says $21B (Aug); the two conflict — [媒体/三方] [Gadgetscout](https://www.gadgetscout.co.uk/articles/etched-reaches-10-3bn-valuation-with-sk-hynix-backing.html), [Kami-labs](https://kami-labs.fr/en/tech/etched-21-milliards-puce-transformers/)
- Oasis 500M weights: `huggingface.co/Etched/oasis-500m` returns HTTP 200 [自测].

#### I. AMI Labs (LeCun)
- Launched Mar 2026 with a $1.03B seed at $3.5B pre-money. CEO Alexandre LeBrun, CSO Saining Xie. JEPA-based (non-generative) — [媒体] [Latent Space](https://www.latent.space/p/ainews-yann-lecuns-ami-labs-launches)
- No product, weights or API as of the latest sources.
- LeCun told the BBC (July) it would refine models for the rest of 2026, with industrial use in 2027 — [三方] [FutureSearch](https://futuresearch.ai/ami-labs-forecast/)
- One known partner arrangement: Nabla (healthcare).
- Context: Meta V-JEPA 2 (2025-06-11) — [官方] [Meta AI](https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/)
  - 1.2B parameters, trained on 1M+ hours of video plus 62 h of robot data.
  - Zero-shot pick-and-place succeeds 65–80% of the time.
  - Open checkpoints at huggingface.co/facebook/vjepa2-*, HTTP 200 [自测].

#### J. Tencent Hunyuan: HY-World 1.0 → 1.5 (WorldPlay) → 2.0/2.1; GameCraft
- **HY-World 1.5 / WorldPlay** (2025-12-17) — [官方] [GitHub HY-WorldPlay](https://github.com/Tencent-Hunyuan/HY-WorldPlay), arXiv 2512.14614
  - Streams at **24 fps**, 480p I2V.
  - Two models: 8B (HunyuanVideo-based) and 5B (WAN-based, released 2026-01-06).
  - Inference memory for 125 frames: 72 GB on 1 GPU, 28 GB per GPU with sequence parallelism 8.
  - Memory method: "Reconstituted Context Memory".
  - WorldCompass RL post-training released 2026-03-08.
  - GitHub: 1,612 stars [自测].
- **HY-World 2.0** (2026-04-16) — [官方] [GitHub HY-World-2.0](https://github.com/Tencent-Hunyuan/HY-World-2.0), arXiv 2604.14268; [媒体] [凤凰科技](https://tech.ifeng.com/c/8sN4vJfV3rG)
  - **Pivots to explicit 3D.** Pipeline: HY-Pano 2.0 (~80B) → WorldNav → WorldStereo 2.0 (~17B) → WorldMirror 2.0 (~1.2B).
  - **Exports mesh, 3DGS and point clouds** to Blender, Unity, UE and Isaac Sim.
  - Character mode includes collision.
  - Weights released in stages: 04-16, 05-11, 05-18.
  - **HY World 2.1** was announced in Jul 2026 and is product-page only.
  - GitHub: 2,724 stars [自测].
  - Product entry: `3d.hunyuan.tencent.com/sceneTo3D`, HTTP 200 [自测].
- **Hunyuan-GameCraft:** covered in the shallow pass. The repo `Hunyuan-GameCraft-1.0` returns HTTP 200 [自测].

#### K. Skywork (昆仑万维) Matrix-Game 2.0 / 3.0 → 3.5 (Riemann Dynamics)
- **Matrix-Game 2.0** (2025-08-12): 25 fps — [官方] [GitHub](https://github.com/SkyworkAI/Matrix-Game)
- **Matrix-Game 3.0** (2026-03-27) — [官方] [project page](https://matrix-game-v3.github.io), arXiv 2604.08995
  - **720p at 40 fps** with a 5B distilled model, using **8 GPUs for the DiT plus 1 for the VAE**.
  - A 2×14B variant improves quality.
  - Memory: camera-aware retrieval plus Plücker encoding and a sink latent. Stable for "minute-long" sequences.
  - MIT repo; weights at HF `Skywork/Matrix-Game-3.0` (HTTP 200 [自测]); 2,350 stars [自测].
- **Matrix-Game 3.5** (WAIC, Jul 2026)
  - 720p at about **20 fps on a single GPU**.
  - Memory: "Patch Memory", which retrieves 3D patches by camera geometry.
  - Weights open under **Apache-2.0** — [三方] [ai-bot.cn](https://ai-bot.cn/matrix-game3-5/); [官方] [project page](https://matrix-game-v3-5.github.io/)
  - **The 3.5 project page lists the affiliation as "Riemann Dynamics", not Skywork.** The repo is `Riemann-Dynamics/Matrix-Game-3.5` (created 2026-07-15, Apache-2.0, 179 stars [自测]).
  - Whether Riemann Dynamics is a Skywork spin-out is **not confirmed**. Skywork appears on the page only as the source of LightX2V.

#### L. 爱诗科技 PixVerse R1
- Launched 2026-01-12/14 as a "first general real-time world model at **1080p**".
  - Sampling steps cut from 50+ to **1–4**.
  - Latency is described only as "millisecond-level" or "instant", with no number — [官方] [PixVerse blog](https://pixverse.ai/en/blog/pixverse-launches-r1-real-time-world-model); [媒体] [科技日报](https://www.stdaily.com/web/gdxw/2026-01/15/content_462139.html)
- **2026-04-01 update** — [官方] [PixVerse blog](https://pixverse.ai/en/blog/pixverse-updates-r1-real-time-world-model)
  - Solo sessions were previously **capped at 5 min**.
  - New **Shared World**: a multi-user livestream with no time cap.
  - **Free "for a limited time"**; enterprise API for qualified partners.
  - PixVerse reports **100M+ registered users** platform-wide.
- **Funding:** AISphere raised ¥2.98B. Caixin's full text is paywalled, so round date and investors are unverified — [媒体] [Caixin Global](https://www.caixinglobal.com/2026-08-14/in-depth-game-studios-have-bought-into-ai-but-players-still-arent-sold-102474160.html)
- **Demo URL:** `realtime.pixverse.ai` now **301-redirects to `world.pixverse.video`**, HTTP 200 [自测].

#### M. Alibaba HappyOyster (快乐生蚝), from the ATH unit that made HappyHorse
- First shown 2026-04-16.
  - Wander mode: about **1 min** of real-time movement.
  - Direct mode: **3+ min** at 480p or 720p.
  - No fps published — [媒体] [PingWest](https://www.pingwest.com/w/312970), [杭州网](https://hznews.hangzhou.com.cn/jingji/content/2026-04/17/content_9207648.htm)
- **1.0 launched 2026-06-17** — [媒体] [IT之家](https://www.ithome.com/0/965/652.htm)
- **On 阿里云百炼** for enterprise and developer grey testing from 2026-07-19 — [媒体] [腾讯新闻/IT之家](https://news.qq.com/rain/a/20260719A04FU700)
- A "HappyOyster 2 Preview" was slated for 云栖 (Sep 22–24, 2026). Not confirmed as shipped — [三方] [DataLearner](https://www.datalearner.com/ai-models/pretrained-models/happy-oyster-2-preview)
- Closed weights.
- **Demo URL:** `happyoyster.cn` → `www.happyoyster.cn`, HTTP 200 [自测]. Waitlist.

#### N. 智源 / 商汤 / 阶跃 / 智谱
- **智源 悟界·Emu3.5** (2025-10-30, open)
  - "Next-State Prediction". About 34B dense, 10T+ multimodal tokens, about 790 years of video [三方].
  - Demos include first-person game-world roaming.
  - Published in Nature in Jan 2026 — [媒体] [36氪](https://www.36kr.com/p/3531575554104450)
  - It is **not a real-time interactive** model.
- **商汤 / 大晓机器人 开悟 Kairos 3.1** (WRC, 2026-08-19)
  - Embodied world model unifying understanding, generation and prediction.
  - Claims #1 on embodied world-model benchmarks against Cosmos 3 and Wan2.2.
  - Claimed to be "open source", but no repo was cited.
  - Commercial partners are named for retail-fulfilment robots, not the model — [媒体] [科技日报](https://www.stdaily.com/web/gdxw/2026-08/20/content_566906.html)
  - SenseTime H1-2026 revenue was ¥2.91B (+23.4%) — [媒体 digest] [北京商报](https://www.bbtnews.com.cn/2026/0717/599759.shtml)
- **阶跃星辰 (StepFun):** no world-model release found. In 2026 it pivoted to "physical world" devices: the STEPX Neo phone (Jul 2026) and 印奇 as chairman — [媒体] [同花顺](https://news.10jqka.com.cn/20260718/c678267589.shtml)
- **智谱 (Zhipu):** no world-model release found. Its model list has no world-model entry — [三方] [DataLearner](https://www.datalearner.com/ai-organizations/zhipu-ai)
  - The **HiDream-O1-World** model (智象未来 / HiDream) topped the WBench Navi sub-board — [三方] search digest. Not verified.

#### O. NVIDIA Cosmos
- **Cosmos 3** (May 2026) — [官方] [GitHub NVIDIA/Cosmos](https://github.com/NVIDIA/Cosmos), [nvidia.com/cosmos](https://www.nvidia.com/en-us/ai/cosmos/)
  - "Omnimodal" Mixture-of-Transformers. Sizes: Super 64B, Nano 16B, Edge 4B (Edge released Jul 2026).
  - Two surfaces:
    - Reasoner: outputs text.
    - Generator: outputs vision, sound and action.
  - License: **OpenMDW-1.1** (Linux Foundation), open weights.
  - GitHub: 12.0k stars.
- Earlier repos (Predict 2.5, Transfer 2.5, Reason 2) remain active — [官方] [github.com/nvidia-cosmos](https://github.com/nvidia-cosmos)
- Odyssey's page notes that **"Cosmos3 V2V uses compute-based pricing from Oct 1"**, implying a hosted, paid Cosmos 3 endpoint as of 2026-10-01 — [官方, Odyssey] [Meet Odyssey-3](https://odyssey.systems/meet-odyssey-3)
- Named adopters are not on the 2026 pages I could fetch (gap).

#### P. Microsoft Muse / WHAM
- Published 2025-02-19 in Nature.
  - WHAM-1.6B at **300×180**, trained on 1B+ frames of Bleeding Edge (about 7 years of gameplay).
  - **Weights open** on Azure AI Foundry / HF `microsoft/wham` (HTTP 200 [自测]) — [官方] [Microsoft Research](https://www.microsoft.com/en-us/research/blog/introducing-muse-our-first-generative-ai-model-designed-for-gameplay-ideation/)
- The Copilot WHAM demo page (`copilot.microsoft.com/wham`) returned **403** through the proxy [自测]. The block may be regional.
- I found no 2026 Muse update (search budget exhausted).

#### Q. Wayve GAIA-3 (AV)
- Published 2025-12-02. A **15B** latent-diffusion world model, double the size of GAIA-2. Multi-camera.
- Used **internally for evaluation**: NCAP-style crash scenarios, what-if perturbations, embodiment transfer.
- Not publicly available. Real-time generation is listed as future work — [官方] [Wayve](https://wayve.ai/thinking/gaia-3/)

### Inferences
- **Spec frontier (Oct 2026)**
  - Real-time pixel world models are at **720p / 20–40 fps / ~1–few-minute coherent memory**.
  - Higher numbers either are not real-time (Atlas 1440p) or have no latency data (PixVerse R1 1080p).
  - Roblox's 4K/60 target is about 10× the pixel throughput of today's best real-time systems.
- **Open-weight split**
  - Every Chinese lab except Alibaba and PixVerse ships open weights.
  - Every US startup except the Oasis-500M toy keeps weights closed.
  - NVIDIA (Cosmos) and Microsoft/Meta (WHAM, V-JEPA 2) are the US open exceptions.
- **The explicit-3D route is the one that monetises as a tool:** World Labs (splats and GLB) and HY-World 2.0. It slots into existing engines and simulators, while pixel-stream models need a new runtime.
- **Matrix-Game moving to a "Riemann Dynamics" org with Apache-2.0** may signal a spin-out or a separate entity. Needs confirmation.

### Gaps
- No primary USD API price for World Labs, Odyssey-2/3, Runway GWM, PixVerse R1 or HappyOyster. Decart Oasis 3 ($0.02/s) is the only published per-second world-model price found.
- Exact Genie 3 parameter count and compute per session have not been disclosed by DeepMind; the 11B figure is wiki-sourced.
- Cosmos 3 named adopters and download counts, and Microsoft Muse's 2026 status, were not reached because the search budget ran out.
- PixVerse ¥2.98B round details (date, lead) are behind the Caixin paywall.

---

## Q2. Who are the paying customers today? Any disclosed contracts?

### Takeaway
- No pure world-model startup has disclosed revenue tied to a named world-model contract.
- **Disclosed or semi-disclosed commercial relationships:**
  - **Robotics/AV:** Odyssey–Flexion, Waymo using Genie 3 internally, World Labs–Lightwheel plus Isaac Sim/MuJoCo, Decart Oasis 3 aimed at AV.
  - **Strategic investor-customers:** Amazon for Decart and Odyssey; Toyota, eBay and Adobe for Decart.
  - **Film previs and architecture:** World Labs API partners.
- **Real revenue sits in adjacent products:** Decart's Lucy live-video editing (estimated $12.6M in 2024) and PixVerse's video app, not in the world models themselves.

### Cited Findings
- **Robotics / physical AI**
  - Odyssey-3: Flexion built humanoid control policies on it. That is a research collaboration, not a stated paid contract — [官方] [Odyssey](https://odyssey.systems/meet-odyssey-3)
  - World Labs: Lightwheel is named as a robotics collaborator, with Isaac Sim, MuJoCo and RoboSuite integrations — [官方] [World API](https://www.worldlabs.ai/blog/announcing-the-world-api)
    - A Jul 2026 post covers "worlds that train robots" — [官方] [blog index](https://www.worldlabs.ai/blog)
  - Runway GWM Robotics: SDK available. Runway is "in active conversations with several robotics firms", none named — [媒体] [TechCrunch](https://techcrunch.com/2025/12/11/runway-releases-its-first-world-model-adds-native-audio-to-latest-video-model)
  - NVIDIA Cosmos 3 is open, with compute-based hosted pricing from 2026-10-01 per Odyssey's footnote — [官方] [Odyssey](https://odyssey.systems/meet-odyssey-3)
- **Autonomous-vehicle simulation**
  - Waymo World Model built on Genie 3. This is the clearest production-scale use, but it is within Alphabet — [官方] [Waymo](https://waymo.com/blog/2026/02/the-waymo-world-model-a-new-frontier-for-autonomous-driving-simulation)
  - Decart Oasis 3 targets AV companies at $0.02/s. Toyota, Adobe and eBay are strategic investors and potential customers. **No paying AV customer is named** — [媒体] [TechCrunch](https://techcrunch.com/2026/06/10/decarts-new-world-model-can-simulate-hours-of-photorealistic-driving-with-some-caveats/)
  - Wayve GAIA-3 is internal only, funded in part by the UK grant project DriveSafeSim — [官方] [Wayve](https://wayve.ai/thinking/gaia-3/)
  - Odyssey drove a real car in India with a policy trained on about 20 h of data. That is a demonstration, not a customer — [官方] [Odyssey](https://odyssey.systems/meet-odyssey-3)
- **Film previs / media / architecture**
  - World Labs API partners: Preview (filmmakers), Escape.ai, Fenestra, xFigura, Interior AI — [官方] [World API](https://www.worldlabs.ai/blog/announcing-the-world-api)
  - HTC VIVERSE produced 3 experiences with Marble — [官方 PR] [HTC](https://www.nasdaq.com/press-release/htc-viverse-collaborates-world-labs-turn-ai-generated-worlds-interactive-experiences)
  - Decart Lucy is in production for try-on, live ads and streaming.
    - Amazon/AWS is a strategic customer.
    - eBay is an investor and customer.
    - Comcast is an edge-deployment collaborator — [媒体] [InvestGame](https://investgame.net/news/decart-raises-300m-series-b-at-4b-valuation); [官方] [decart.ai](https://decart.ai)
    - Livestreamers such as CodeMiko use it on Twitch, TikTok and YouTube (CEO remark) — [媒体 digest] [Calcalist](https://www.calcalistech.com/ctechnews/article/hkbg4d1wgl)
- **Games / consumer**
  - Google Project Genie is bundled in the $200/month AI Ultra tier. There is no standalone revenue line — [媒体] [Engadget](https://engadget.com/2176797/project-genie-adds-google-street-view-integration-and-goes-live-for-global-ai-ultra-users)
  - World Labs Marble consumer subscriptions run $20–$95/month — [媒体] [The Batch](https://charonhub.deeplearning.ai/world-labs-makes-its-marble-generative-world-model-public-adds-chisel-editing-tool/)
  - PixVerse R1 is free for a limited time — [官方] [PixVerse](https://pixverse.ai/en/blog/pixverse-updates-r1-real-time-world-model)
  - Roblox is the only game platform committing capex to world models (Roblox Reality). It is building in-house, not buying a service — [官方] [Roblox Q2 letter](https://www.sec.gov/Archives/edgar/data/0001315098/000162828026051059/ex991-robloxq22026earnin.htm)
  - Alibaba HappyOyster is in enterprise grey test on 百炼 — [媒体] [IT之家/腾讯新闻](https://news.qq.com/rain/a/20260719A04FU700)
- **Revenue figures that exist**
  - Decart: $12.6M in 2024, a third-party estimate covering the whole company, mostly Lucy/DOS — [三方] [GetLatka](https://getlatka.com/companies/decart.ai)
  - World Labs: none, even at the $8.2B AMD deal — [媒体] [The Next Platform](https://www.nextplatform.com/ai/2026/09/29/amd-buys-world-labs-for-82-billion-to-get-ai-model-cred/5299801)

### Inferences
- Buyers are paying for **world models as a feature or input**, not as a product: simulation data for AV and robotics, 3D assets for previs and architecture, and live-video effects.
- Exits are priced on **teams and compute strategy**, not revenue:
  - AMD–World Labs is described as a compute-roadmap and team purchase.
  - Anthropic–Decart centred on chip efficiency.
- AV and robotics sim is the most plausible near-term paying segment. The pull comes from Waymo internally plus investor-customers (Toyota, Amazon). Every startup now pitches it: Decart, Odyssey, Runway, World Labs.

### Gaps
- No contract values, seat counts or ARR for any world-model product.
- Whether Flexion, Lightwheel or Preview are paying customers or unpaid design partners is not stated.

---

## Q3. Technical limits cited, and cost per user-hour

### Takeaway
- **Recurring limits:**
  - Memory or persistence: revisiting a place shows something different.
  - Drift: Decart's NYC prompt slid toward a generic city.
  - Physics: cars pass through cars.
  - Control responsiveness.
  - **No deterministic shared state for multiplayer.**
- **Cost per user-hour** spans about **$1–2** (Odyssey-1, H100, company-reported in 2025) to **$72 list price** (Decart Oasis 3 at $0.02/s).
  - My estimate for open models with self-hosted GPUs: about $2–$20/h depending on GPU count.
  - Google caps sessions at 60 s explicitly because of cost.

### Cited Findings
- **Cost and pricing data points**
  - Odyssey-1: **$1–2 per user-hour** on H100 clusters (company-reported) — [媒体] [TechCrunch 2025-05-28](https://techcrunch.com/2025/05/28/odysseys-new-ai-model-streams-3d-interactive-worlds/)
  - Odyssey-3's cost analysis assumes **$1 per MI355X GPU-hour** — [官方] [Odyssey](https://odyssey.systems/meet-odyssey-3)
  - Decart Oasis 3 list price is **$0.02/s**. CEO claims Decart is ">10× cheaper than anyone else" (unverified) — [媒体] [TechCrunch](https://techcrunch.com/2026/06/10/decarts-new-world-model-can-simulate-hours-of-photorealistic-driving-with-some-caveats/)
  - Genie 3: Project Genie is capped at 60 s per session. DeepMind's reason is that the model is autoregressive and compute-heavy, so longer sessions add cost with little value — [三方] [Wikipedia](https://en.wikipedia.org/wiki/Project_Genie_(website))
  - World Labs RTFM runs on a single H100. The team calls naive video world models "neither feasible nor economically viable" on today's infrastructure — [官方] [RTFM](https://www.worldlabs.ai/blog/rtfm)
  - Hardware per stream for open models:
    - Matrix-Game 3.0: **8 GPUs for the DiT plus 1 for the VAE** at 720p/40 fps — [官方] [project page](https://matrix-game-v3.github.io)
    - Matrix-Game 3.5: **1 GPU** at 720p/~20 fps — [三方] [ai-bot.cn](https://ai-bot.cn/matrix-game3-5/)
    - HY-World 1.5: 72 GB on 1 GPU, or 28 GB per GPU across 8 GPUs (8B model) — [官方] [GitHub](https://github.com/Tencent-Hunyuan/HY-WorldPlay)
    - Mirage 2: claims a single consumer-grade GPU — [媒体] [Plain Concepts](https://www.plainconcepts.com/world-simulation/)
    - Lucid-v1: runs on an RTX 4090 — [官方] [Lucid](https://ramimo.substack.com/p/lucid-v1-a-world-model-that-does)
  - Session caps as a cost signal:
    - Genie: 60 s.
    - PixVerse R1 solo: 5 min (shared worlds uncapped) — [官方] [PixVerse](https://pixverse.ai/en/blog/pixverse-updates-r1-real-time-world-model)
    - HappyOyster Wander: ~1 min; Direct: 3+ min — [媒体] [PingWest](https://www.pingwest.com/w/312970)
    - Runway GWM-1: 2 min, while Worlds 2 is unbounded — [官方] [Runway GWM-1](https://runway.com/research/introducing-runway-gwm-1), [Worlds 2](https://runway.com/research/introducing-gwm-worlds-2)
- **Limits cited by researchers, operators and investors**
  - Morgan Stanley (2026-02-02):
    - Determinism, memory and updates "may prove difficult to resolve".
    - World models are probabilistic with no "source of truth", so multiple players could see inconsistent game states.
    - Base case is that incumbents adopt AI while leveraging existing engines — [媒体] [Yahoo/Investing.com](https://finance.yahoo.com/news/video-game-stocks-morgan-stanley-134811296.html)
  - Roblox (acquirer): standalone world models lack long-term memory, consistent logic and structured input, so the engine keeps the logic and multiplayer sync — [媒体] [PocketGamer.biz](https://pocketgamer.biz/roblox-strengthens-ai-ambitions-with-morpheus-ai-acquisition-and-founder-hires/)
  - Decart Oasis 3 hands-on test:
    - Thematic drift.
    - Places are not persistent.
    - Unresponsive steering.
    - Cars pass through cars; the CEO calls this a "major research problem".
    - The context window fills fast — [媒体] [TechCrunch](https://techcrunch.com/2026/06/10/decarts-new-world-model-can-simulate-hours-of-photorealistic-driving-with-some-caveats/)
  - Runway, on its own model:
    - Real-time generation trades fidelity for speed.
    - Fast camera rotation degrades geometry.
    - Long-term memory is imperfect (sliding KV window).
    - Free-text control may need an external harness tracking world state — [官方] [GWM Worlds 2](https://runway.com/research/introducing-gwm-worlds-2)
  - Oasis 1: forgot the layout when turning around, and Custom Worlds lost resemblance to the source quickly — [媒体] [The Decoder](https://the-decoder.com/ai-generated-game-oasis-now-turns-images-into-playable-3d-worlds/)
  - MirageLSD: only a small window of past frames is used, so consistency degrades over long videos — [媒体] [The Decoder](https://the-decoder.com/decart-launches-miragelsd-an-ai-model-that-transforms-live-video-feeds-in-real-time)
  - Odyssey-1: layouts unstable, surroundings shift when turning, capacity bound by GPU availability — [媒体] [TechCrunch](https://techcrunch.com/2025/05/28/odysseys-new-ai-model-streams-3d-interactive-worlds/)
  - Benchmarks are self-reported: Odyssey-3 used best-of-8 on Physics-IQ; Atlas used vendor-run preferences; Kairos claims rankings — [媒体] [TNW](https://thenextweb.com/news/odyssey-3-world-model-robots-humanoids-cars-drones), [Implicator](https://www.implicator.ai/world-labs-atlas-withholds-paper-price-partners/)
  - Frame rate: Fast Company argued 24 fps is too low against 120 fps modern games — [三方] [Wikipedia](https://en.wikipedia.org/wiki/Project_Genie_(website))
  - V-JEPA 2: current video models score at or near chance on IntPhys 2 intuitive physics — [官方] [Meta](https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/)
- **Memory methods (what each lab does about memory)**
  - Camera/pose-indexed retrieval:
    - Matrix-Game 3.0: camera-aware retrieval plus Plücker encoding.
    - Matrix-Game 3.5: 3D Patch Memory.
    - World Labs RTFM: posed frames plus "context juggling".
    - HY-World 1.5: Reconstituted Context Memory.
  - Sliding window: Runway Worlds 2 (KV window).
  - Explicit 3D (sidesteps the problem): World Labs Marble, HY-World 2.0.
  - Sources: links above.

### Inferences
- **Cost per user-hour** [推算]
  - Decart Oasis 3 at list price: $0.02 × 3,600 = **$72/h**. That is aimed at B2B sim data, not consumer play.
  - Self-hosted open models, at an assumed $1–2.5 per H100/H20-class GPU-hour (Odyssey itself assumes $1/GPU-h):
    - Matrix-Game 3.0 (9 GPUs): about **$9–22/h**.
    - Matrix-Game 3.5 (1 GPU): about **$1–2.5/h**.
    - Odyssey-1's company figure: **$1–2/h**.
  - A consumer game ($0–$0.10/h implied by $10–60 games or F2P ARPU) needs another **10–100× cost drop**. That explains why consumer access is either bundled at $200/month and capped at 60 s (Google), free as a promotion (PixVerse), or not offered (Runway, Odyssey-3 API contact-only).
- **The multiplayer/determinism gap is architectural, not a scaling issue.** Every serious game-platform plan uses a hybrid where the engine owns the state and the world model renders: Roblox Reality, and Runway's "external harness" note.
- **Memory is converging on geometry-indexed retrieval** (pose, Plücker, 3D patches). This brings pixel models closer to the explicit-3D camp.

### Gaps
- No primary per-hour cost for Genie 3, Runway or PixVerse.
- No independent latency measurements (input-to-photon) for any model. All fps and latency numbers are vendor-reported.
- No third-party analysis (e.g. a16z, Sequoia) with cost per hour found. The a16z speedrun "Big Idea" piece (Jonathan Lai, 2025-12-18) cites **no limits or costs** — [官方-VC] [a16z speedrun](https://speedrun.substack.com/p/14-big-ideas-for-2026)

---

## Q4. Timeline of key releases, 2024–2026

### Takeaway
- 2024 was research demos: Genie 1/2, Oasis, Lucid.
- 2025 brought real-time 720p (Genie 3, Odyssey-2, Matrix-Game 2, HY-World 1.5) and the first commercial products (Marble GA, MirageLSD).
- 2026 brought consumer access (Project Genie), 1080p and multiplayer (PixVerse R1, Runway Worlds 2), domain verticals (Waymo, Oasis 3 driving, Odyssey-3 robotics), and consolidation: Roblox–Morpheus, AMD–World Labs, and the failed Anthropic–Decart deal.

### Cited Findings
**2024**
- Mar: Genie (2D, ~1 fps) — [三方] [Wikipedia](https://en.wikipedia.org/wiki/Project_Genie_(website))
- Sep: World Labs launched with $230M — [三方] [Sacra](https://sacra.com/c/world-labs/)
- 10-31: Decart and Etched Oasis (360p/20 fps; 500M weights open) — [官方] [Etched](https://etched.com/blog-posts/oasis)
- Oct: Decart $21M seed — [媒体] [InvestGame](https://investgame.net/news/decart-raises-300m-series-b-at-4b-valuation)
- 11-11: Lucid-v1 (Minecraft on an RTX 4090) — [官方] [Lucid](https://ramimo.substack.com/p/lucid-v1-a-world-model-that-does)
- Dec: Genie 2 (3D, 360p, 10–20 s) — [三方] [Wikipedia](https://en.wikipedia.org/wiki/Project_Genie_(website))

**2025**
- 02-19: Microsoft Muse/WHAM (Nature; weights open) — [官方] [MSR](https://www.microsoft.com/en-us/research/blog/introducing-muse-our-first-generative-ai-model-designed-for-gameplay-ideation/)
- 05-12: Matrix-Game 1.0 — [官方] [GitHub](https://github.com/SkyworkAI/Matrix-Game)
- 05-28: Odyssey-1 ($1–2 per user-hour) — [媒体] [TechCrunch](https://techcrunch.com/2025/05/28/odysseys-new-ai-model-streams-3d-interactive-worlds/)
- 06-11: Meta V-JEPA 2 — [官方] [Meta](https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/)
- 07-19: Decart MirageLSD — [媒体] [The Decoder](https://the-decoder.com/decart-launches-miragelsd-an-ai-model-that-transforms-live-video-feeds-in-real-time)
- Aug: Genie 3 announced (720p/24 fps, minutes of memory) — [三方] [Wikipedia](https://en.wikipedia.org/wiki/Project_Genie_(website))
- Aug: Mirage 2 — [媒体] [Gigazine](https://www.gigazine.net/gsc_news/en/20250825-ai-generative-world-mirage-2)
- 08-12: Matrix-Game 2.0 (25 fps) — [官方] [GitHub](https://github.com/SkyworkAI/Matrix-Game)
- Aug: Decart $100M at $3.1B — [媒体] [InvestGame](https://investgame.net/news/decart-raises-300m-series-b-at-4b-valuation)
- 10-16: World Labs RTFM — [官方] [RTFM](https://www.worldlabs.ai/blog/rtfm)
- 10-27: Odyssey-2 — [官方] [Odyssey](https://odyssey.systems/introducing-odyssey-2)
- 10-30: 智源 Emu3.5 — [媒体] [36氪](https://www.36kr.com/p/3531575554104450)
- 11-12: Marble GA — [官方] [World Labs](https://www.worldlabs.ai/blog/marble-world-model)
- Late 2025: Dynamics Lab and Lucid founders joined Roblox — [媒体] [PocketGamer.biz](https://pocketgamer.biz/roblox-strengthens-ai-ambitions-with-morpheus-ai-acquisition-and-founder-hires/)
- 12-02: Wayve GAIA-3 (15B) — [官方] [Wayve](https://wayve.ai/thinking/gaia-3/)
- 12-11: Runway GWM-1 — [官方] [Runway](https://runway.com/research/introducing-runway-gwm-1)
- 12-17: Tencent HY-World 1.5 / WorldPlay (24 fps, open) — [官方] [GitHub](https://github.com/Tencent-Hunyuan/HY-WorldPlay)
- 12-18: a16z speedrun names world models "Big Idea #1" for 2026 — [VC] [a16z](https://speedrun.substack.com/p/14-big-ideas-for-2026)

**2026**
- 01-12/14: PixVerse R1 (1080p real-time) — [官方] [PixVerse](https://pixverse.ai/en/blog/pixverse-launches-r1-real-time-world-model)
- 01-21: World Labs World API — [官方] [World Labs](https://www.worldlabs.ai/blog/announcing-the-world-api)
- ~01-26: Odyssey-2 Pro API — [媒体] [Aihola](https://aihola.com/article/odyssey-2-pro-api-real-time-video)
- 01-29: Project Genie (US, AI Ultra). Game stocks sold off. Morgan Stanley's note followed on 02-02 — [媒体] [Yahoo](https://finance.yahoo.com/news/video-game-stocks-morgan-stanley-134811296.html)
- 02-06: Waymo World Model (on Genie 3) — [官方] [Waymo](https://waymo.com/blog/2026/02/the-waymo-world-model-a-new-frontier-for-autonomous-driving-simulation)
- 02-18: World Labs raised $1B (~$5B valuation) — [媒体] [The Next Platform](https://www.nextplatform.com/ai/2026/09/29/amd-buys-world-labs-for-82-billion-to-get-ai-model-cred/5299801)
- Mar: AMI Labs $1.03B seed — [媒体] [Latent Space](https://www.latent.space/p/ainews-yann-lecuns-ami-labs-launches)
- 03-27: Matrix-Game 3.0 (720p/40 fps, 8+1 GPUs) — [官方] [project page](https://matrix-game-v3.github.io)
- 04-01: PixVerse R1 Shared Worlds — [官方] [PixVerse](https://pixverse.ai/en/blog/pixverse-updates-r1-real-time-world-model)
- 04-16: Tencent HY-World 2.0 (3DGS/mesh, open) — [官方] [GitHub](https://github.com/Tencent-Hunyuan/HY-World-2.0)
- 04-16: Alibaba HappyOyster debut — [媒体] [PingWest](https://www.pingwest.com/w/312970)
- May: NVIDIA Cosmos 3 (64B/16B; OpenMDW) — [官方] [GitHub](https://github.com/NVIDIA/Cosmos)
- 05-19: Project Genie global, with Street View — [媒体] [Engadget](https://engadget.com/2176797/project-genie-adds-google-street-view-integration-and-goes-live-for-global-ai-ultra-users)
- 05-25: Decart $300M at ~$4B — [媒体] [InvestGame](https://investgame.net/news/decart-raises-300m-series-b-at-4b-valuation)
- 06-09: Roblox acquired Morpheus AI (Roblox Reality) — [媒体] [PocketGamer.biz](https://pocketgamer.biz/roblox-strengthens-ai-ambitions-with-morpheus-ai-acquisition-and-founder-hires/)
- 06-10: Decart Oasis 3 (driving, $0.02/s) — [媒体] [TechCrunch](https://techcrunch.com/2026/06/10/decarts-new-world-model-can-simulate-hours-of-photorealistic-driving-with-some-caveats/)
- Jun: Odyssey $310M at $1.45B — [媒体] [TNW](https://thenextweb.com/news/odyssey-3-world-model-robots-humanoids-cars-drones)
- 06-17: HappyOyster 1.0 — [媒体] [IT之家](https://www.ithome.com/0/965/652.htm)
- Jul: Cosmos3-Edge (4B) — [官方] [GitHub](https://github.com/NVIDIA/Cosmos)
- Jul: HY World 2.1 — [官方] [GitHub](https://github.com/Tencent-Hunyuan/HY-World-2.0)
- Jul: Matrix-Game 3.5 (WAIC; Riemann Dynamics org; Apache-2.0) — [官方] [project page](https://matrix-game-v3-5.github.io/)
- 07-19: HappyOyster on 百炼 grey test — [媒体] [腾讯新闻](https://news.qq.com/rain/a/20260719A04FU700)
- 07-21: World Labs acquired SceniX — [官方] [World Labs blog](https://www.worldlabs.ai/blog)
- 07-30: Roblox Q2 letter calls Morpheus a "multi-year bet" — [官方] [SEC](https://www.sec.gov/Archives/edgar/data/0001315098/000162828026051059/ex991-robloxq22026earnin.htm)
- 08-19: SenseTime/大晓 Kairos 3.1 at WRC — [媒体] [科技日报](https://www.stdaily.com/web/gdxw/2026-08/20/content_566906.html)
- 09-01: World Labs Atlas (1440p, early access) — [媒体] [Implicator](https://www.implicator.ai/world-labs-atlas-withholds-paper-price-partners/)
- 09-03: Runway GWM Worlds 2 (unbounded, multiplayer roles, audio) — [官方] [Runway](https://runway.com/research/introducing-gwm-worlds-2)
- 09-08: Anthropic walked away from the ~$6B Decart deal (Bloomberg) — [媒体] [TNW](https://thenextweb.com/news/anthropic-walks-away-decart-6bn-acquisition)
- 09-28: AMD to acquire World Labs for ~$8.2B in stock — [官方] [World Labs blog](https://www.worldlabs.ai/blog); [媒体] [Data Center Knowledge](https://datacenterknowledge.com/data-center-chips/amd-to-acquire-world-labs-for-8-2b-to-advance-ai-models-and-robotics)
- 10-01: Cosmos3 V2V compute-based pricing begins (per Odyssey footnote) — [官方] [Odyssey](https://odyssey.systems/meet-odyssey-3)
- 10-08: Odyssey-3 (480p base, 720p Pro, Flash; Flexion) — [官方] [Odyssey](https://odyssey.systems/meet-odyssey-3)

**Demo URL verification table** [自测, 2026-10-13]
- HTTP 200 means the page is reachable. It does not mean the demo is free or playable without login.

| URL | Result |
|---|---|
| labs.google/projectgenie | 200 (Ultra login) |
| marble.worldlabs.ai | 200 |
| platform.worldlabs.ai | 200 |
| experience.odyssey.systems | 200 |
| agora.odyssey.systems | 200 |
| oasis.decart.ai | 302 → /welcome, 200 |
| platform.decart.ai | 200 |
| mirage.decart.ai | timeout (likely retired) |
| demo.dynamicslab.ai/chaos | timeout (likely dead after Roblox) |
| realtime.pixverse.ai | 301 → world.pixverse.video, 200 |
| www.happyoyster.cn | 200 |
| 3d.hunyuan.tencent.com/sceneTo3D | 200 |
| copilot.microsoft.com/wham | 403 (possibly regional) |
| HF: Skywork/Matrix-Game-3.0, RiemannDynamics/Matrix-Game-3.5-Base, tencent/HY-WorldPlay, tencent/HY-World-2.0, Etched/oasis-500m, microsoft/wham | all 200 |

### Inferences
- Since late 2025 the release cadence is about one major Western and one major Chinese world-model release per month.
- Chinese labs lead on open weights and on spec claims (1080p, 40 fps).
- Western labs lead on capital, exits and vertical deployments (Waymo).
- 2026 H2 shows **consolidation into platforms and chip vendors**: Roblox, AMD, and Nvidia/Anthropic bidding for Decart. Hardware vendors are buying world-model teams to shape compute roadmaps; the AMD rationale is stated explicitly.

### Gaps
- Unconfirmed whether HappyOyster 2 Preview shipped at 云栖 (Sep 2026).
- Exact date and lead of PixVerse's ¥2.98B round.
- Whether Meta, Microsoft or 智谱 released new interactive world models in 2026. Not found, and the search budget was exhausted.

