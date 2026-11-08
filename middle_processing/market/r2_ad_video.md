# AI-Generated Ad VIDEO (国内+国外), round 2 deep pass, as of 2026-10-13

Method:
- About 80 tool calls: 15 searches, about 66 fetches.
- About 75% of attempted searches were blocked by the shared session search quota, so coverage of the 国内 brand TVC cases is thinner than planned (see Gaps).
- This pass builds on `ad_creative_gen.md` and does not repeat it.

Source-type tags on each number:
- [FILING] = exchange filing or official results release
- [CO] = company or vendor page or exec statement
- [FOUNDER] = founder's own claim
- [PRESS] = journalist reporting
- [3P-EST] = third-party estimate or tracker
- [AGG] = aggregator or blog repeating others

## Q1. Landmark brand cases: production facts, links, backlash

### Takeaway
"Hero" AI spots now cluster into two cost tiers:
- **Solo creator, about $2k in tooling, 2 days.** Example: Kalshi × PJ Accetturo, Veo 3.
- **Studio team, roughly 1 month, dozens to about 100 people, tens of thousands of generations.** Examples: Coca-Cola 2025 and Svedka at Super Bowl LX (Silverside).

Brand AI spots have reliably drawn backlash: Coca-Cola 2024 and 2025, McDonald's NL 2025 (pulled), Svedka 2026, Under Armour 2024. Media-cost-heavy placements like the Super Bowl ($10M per 30s) dwarf any production savings.

In China, the strongest documented brand use is not TVC. It is **branded AI short dramas / 漫剧**, where production runs about ¥800–1,500 per minute and Kuaishou now discloses AIGC-driven ad spend in its filings.

### Cited Findings

**Kalshi "NBA Finals" (Jun 11, 2025)**
- 30s spot aired in the YouTube TV stream of NBA Finals Game 3 on 2025-06-11. Made essentially solo by P.J. Accetturo in 2 days [PRESS] — [NPR/MPR News](https://www.mprnews.org/story/2025/06/23/npr-ai-video-ad-kalshi-advertising-nba-finals)
- Cost: Kalshi's Jack Such said AI prompting cost was "under $2,000" [CO via PRESS]
  - Accetturo's own fee was not disclosed, and media cost is excluded
  - Source: same NPR piece
- Workflow: about 300–400 Veo 3 generations for 15 usable clips. Gemini/ChatGPT wrote the script and shot prompts; edited in CapCut/FCPX/Premiere [FOUNDER] — [PJ Ace newsletter](https://pjace.beehiiv.com/p/i-can-t-believe-disney-allowed-us-to-run-this-ai-ad-during-the-nba-finals-f77e73388ab4ca62)
- Accetturo claims about 95% lower cost than "$400K+ 2-month productions" [FOUNDER] — same source
- Over 3M views on Kalshi's X account in one week [PRESS] — [NPR](https://www.mprnews.org/story/2025/06/23/npr-ai-video-ad-kalshi-advertising-nba-finals)
- URLs:
  - Ad: <https://www.youtube.com/watch?v=-QMftwmyW-A>
  - Kalshi post: <https://x.com/Kalshi/status/1932891608388681791>
  - Accetturo post: <https://x.com/PJaccetturo/status/1932893260399456513>
  - (Listed by NPR)

**Coca-Cola "Holidays Are Coming", AI 2024 (Nov 2024)**
- Three AI studios (Secret Level, Silverside AI, Wild Card) each made a version, using four gen-AI models (per Forbes as cited by NBC) [PRESS] — [NBC News](https://www.nbcnews.com/tech/innovation/coca-cola-causes-controversy-ai-made-ad-rcna180665)
- Over 56M views; called "soulless"; mocked by Gravity Falls creator Alex Hirsch [PRESS] — same
- Coca-Cola said: "a collaboration of human storytellers and the power of generative AI" [CO] — same
- Precedent: the Mar 2023 "Masterpiece" spot was made with OpenAI [PRESS] — same
- Backlash list with IGN/NYT links — [Wikipedia: AI slop](https://en.wikipedia.org/wiki/AI_slop)
- Silverside's 2024 version "Secret Santa" was the only one of the three that used **Kling**, plus Leonardo and Runway [PRESS] — [量子位 2024-12-01](https://www.qbitai.com/2024/12/226696.html)
  - Started in June, released in December
  - Over 10,000 images and over 5,000 video clips; more than 100 market versions
  - First draft within 3 days of the first client meeting
  - Described as about 5x faster than traditional production
  - Human animators fixed the logo and trucks; live musicians re-recorded the soundtrack

**Coca-Cola "Holidays Are Coming", AI 2025 (Nov 2025)**
- Two versions, one US-only, made by Silverside AI and Secret Level, airing in about 140 countries [PRESS] — [Ads of the World credits](https://www.adsoftheworld.com/campaigns/holidays-are-coming-ai-generated-2025-christmas-ad); [eWEEK](https://www.eweek.com/news/coca-cola-ai-ads/)
- Credited execs: Pratik Thakar (Global VP and Head of GenAI) and Islam ElDessouky [CO] — [Ads of the World](https://www.adsoftheworld.com/campaigns/holidays-are-coming-ai-generated-2025-christmas-ad)
- Team: about 100 people, including 5 gen-AI specialists, generated over 70,000 clips (WSJ, via secondary) [PRESS, 2nd-hand]
- Time: about 1 month vs about 1 year for a traditional cycle. CMO told WSJ it was "cheaper", with no $ given [PRESS, 2nd-hand]
- Sources for team and time: [WebSearch summary of eWEEK/WSJ](https://www.eweek.com/news/coca-cola-ai-ads/); [TrueFutureMedia](https://www.truefuturemedia.com/articles/coca-cola-ai-holiday-ads-2025)
- Animals were used instead of humans to avoid the uncanny effect. Artifacts drew criticism (trucks with inconsistent wheels) [PRESS] — same
- Silverside lists "Coca-Cola Holidays 2025" and "Coca-Cola Rivals" in its portfolio [CO] — [silverside.ai](https://www.silverside.ai/)
- Secret Level lists Coca-Cola "Stitched Together" [CO] — [secretlevel.co](https://www.secretlevel.co/)

**Svedka "Shake Your Bots Off", Super Bowl LX (Feb 8, 2026)**
- Billed as the "first primarily AI-generated Super Bowl commercial". Also Sazerac's first Super Bowl spot [PRESS] — [Adweek](https://www.adweek.com/creativity/svedka-bets-on-ai-and-its-fembot-to-make-super-bowl-history/); [TechCrunch](https://techcrunch.com/?p=3090483)
- Production: Silverside AI with Sazerac's in-house team [CO] — [Comfy case study](https://comfy.org/customers/svedka-silverside)
  - Built on ComfyUI workflows, with custom-trained character and world models
  - Production took under 1 month vs about 6 months historically for this scale
  - Changes were still being made a week before air
  - Silverside's PJ Pereira and Sazerac CMO Sara Saunders are quoted
- WSJ (via TechCrunch): about 4 months to rebuild the Fembot and train AI on facial and body motion; humans wrote the storyline [PRESS] — [TechCrunch](https://techcrunch.com/?p=3090483)
- The 1-month and 4-month figures measure different phases. Both are reported.
- Heavy social backlash [PRESS] — [Wikipedia: AI slop (cites USA Today Ad Meter)](https://en.wikipedia.org/wiki/AI_slop)
- Context: NBC base rate was **$10M per 30s** in 2026 [PRESS] — [Wikipedia: Super Bowl LX, citing USA Today](https://en.wikipedia.org/wiki/Super_Bowl_LX)
  - Media dwarfs AI production savings; this is my inference.
- Pepsi's "The Choice" (Taika Waititi), with a polar bear choosing Pepsi, was read as a jab at Coke's AI Christmas ads [PRESS] — same

**Other Super Bowl LX AI items**
- iSpot: 15 of 66 ads (about 23%) "contained or promoted AI"
  - Most promoted AI products (OpenAI, Anthropic, Google Nano Banana Pro, Amazon Alexa+, Meta/Oakley, Ring, Wix, Ramp) rather than being AI-made
  - Sources [PRESS] — [Cortland Dragon Chronicle](https://sites.cortland.edu/dragon-chronicle/2026/02/16/15-ads-zero-soul-analyzing-the-23-ai-presence-in-super-bowl-2026/); [TechCrunch](https://techcrunch.com/?p=3090483)
- Unsourced claims on one agency blog [AGG] — [AdventureMedia](https://adventuremedia.ai/blog/ai-takes-center-stage-at-super-bowl-lx-why-2026-is-the-year-of-real-adoption-in-creative-advertising):
  - Artlist.io's spot was made in 5 days for "a few thousand dollars"
  - Xfinity used AI de-aging on the Jurassic Park cast
  - Ro/Serena Williams used AI in pre-production
  - 50%+ of spots used gen-AI somewhere (an Anomaly exec's prediction)
- Pre-game, Gary Vaynerchuk predicted 100% AI commercials were unlikely [PRESS] — [Axios](https://axios.com/2026/02/04/early-super-bowl-ads-2026-gary-vee)

**Toys"R"Us "Origin Story" (Sora, Cannes Lions, Jun 2024)**
- Agency: Native Foreign (Nik Kleverov). Sora took the film to about 80–85%; about a dozen people did "corrective VFX". Over 1 minute long; premiered at Cannes [PRESS] — [Tech Times](https://www.techtimes.com/articles/306053/20240626/toys-r-us-comeback-iconic-retail-chain-uses-openai-sora-brand-film)
- Hosted at <https://www.toysrus.com/pages/studios>
- Postscript: OpenAI announced Sora's discontinuation on 2026-03-24 [PRESS/CO] — [Wikipedia: Sora](https://en.wikipedia.org/wiki/Sora_(text-to-video_model)); [TechCrunch 2026-03-29](https://techcrunch.com/2026/03/29/why-openai-really-shut-down-sora/)
  - App closed 2026-04-26; API closed 2026-09-24
  - Reported cost was about $1M/day; users peaked around 1M
  - The Disney $1B deal unwound
  - **The landmark Sora ad tool no longer exists as a product.**

**Under Armour × Anthony Joshua (Mar 2024)**
- Director Wes Walker billed it as the "first AI-powered sports commercial". It mixed AI video, AI photo, 3D CGI, VFX and 35mm film [PRESS] — [TechCrunch](https://techcrunch.com/2024/03/14/ai-powered-ad-ignites-creator-controversy-on-instagram/amp/); [Euronews](https://euronews.com/next/2024/03/15/massively-concerning-under-armours-ai-powered-sports-commercial-sparks-controversy)
- Backlash: it reused footage directed by Gustav Johansson two years earlier without credit. Credits were later added [PRESS] — same

**McDonald's Netherlands AI Christmas ad (Dec 2025)**
- "It's the Most Terrible Time of the Year". Comments were turned off and the original upload was hidden after backlash [PRESS] — [Forbes 2025-12-09 (via Wikipedia: AI slop)](https://www.forbes.com/sites/danidiplacido/2025/12/09/mcdonalds-ai-generated-ad-controversy-explained/)
- Forbes was 403 when fetched, so the agency and production-house credits were not verified.

**Other backlash cases**
- A24 "Civil War" AI posters (Apr 2024)
- Paramount "Novocaine" AI narration (Mar 2025)
- Activision AI fake-game ads (Mar 2025)
- Source [PRESS] — [Wikipedia: AI slop](https://en.wikipedia.org/wiki/AI_slop)

**Enterprise Veo creative (Google-reported) [CO]** — [Google Cloud "101 real-world gen-AI use cases"](https://cloud.google.com/transform/101-real-world-generative-ai-use-cases-from-industry-leaders)
- eToro uses Veo for culturally specific ad video
- WPP and Authentic Brands use Veo 3 / Imagen 4 for "hundreds or thousands" of variations "in hours"
- AdVon Commerce: Veo lifestyle videos; a 93,673-SKU catalog processed in under a month; one client saw a $17M revenue lift in 60 days
- Monks for Hatch: CTR +80%, CPP −31%, cost −97%. This was Gemini personalization, not video.

**国内: AI 短剧 / 漫剧 as the brand vehicle (2026)**

Branded AI drama cases (all [PRESS] unless noted) — [数英 2026-06-23](https://www.digitaling.com/articles/1526531.html); [澎湃 2026-06-18](https://www.thepaper.cn/newsDetail_forward_33391539)
- 烙色 (beauty), 《伪装AI》: product features drive the plot; first 5 episodes had 25.72M plays on Douyin
- OPPO, 《震惊！钟馗都来给我当红娘》: season 1 was a success; seasons 2 and 3 are planned, with game and light-novel spin-offs
- 红旗 (Hongqi), 《大明天工合伙人》: self-made AI drama; 76M+ plays; produced two reusable digital-human IPs
- if果酒 × 《有山灵》: concept to launch in 1 month; the co-branded product passed ¥2M GMV in 2 weeks
- 贵州酱板鸭, 《雪山救狐》: total cost "一千多元"; claimed 5B plays and 70%+ store sales growth
  - These are campaign claims; treat them as unverified
- 剧查查: in Apr 2026, 3 of the top-10 branded short dramas were AI dramas (brands included 烙色, OPPO, 知交酒) [3P] — same
- Kuaishou ad spend on 漫剧 [PRESS citing Kuaishou] — [广告门 2026-05-29](https://m.adquan.com/detail/0-360907); [蓝鲸 2026-07-21](https://www.lanjinger.com/d/1784036025417585113)
  - Q1 2026 marketing spend on AI 漫剧 grew 100x+ YoY, with a daily peak above ¥20M
  - 漫剧 ad spend rose about 20x in half a year
  - Kuaishou committed ¥2B to short drama in 2026: ¥800M revenue share, ¥200M incubation fund, ¥1B traffic pool
- Kuaishou's official Q2 2026 release says short-play-driven marketing spend grew 100%+ YoY, and supply of short plays (including AI-generated ones) grew more than 5x since Jan 2026 [FILING] — [Kuaishou Q2 2026 release (TechNode/PRNasia)](https://technode.global/?p=990300)
- 巨量引擎: AI 漫剧 ad spend averages over ¥1M per day, peaking above ¥4M per day [PRESS, undated] — [蓝鲸](https://www.lanjinger.com/d/1784036025417585113)
- Regulation: from Apr 2026, 红果 + 抖音 tightened 漫剧 review (filing before launch), removed 3,522 titles in one week, and pulled 20K+ low-quality 漫剧 [PRESS] — [澎湃](https://m.thepaper.cn/newsDetail_forward_33585816); [数英](https://www.digitaling.com/articles/1526531.html)

**国内 brand AI films / TVC-style spots**
- **美团 《麻烦死了》 (April Fools' 2026), fully AI-made, mainly 可灵** [PRESS interview] — [数英 2026-04-12](https://www.digitaling.com/articles/1485301.html)
  - Creator: 可灵 super-creator @希希叔叔; creative: 一界创意; agency: 木瓜创意; production: 剑阁制作
  - **4-person team, about 2 weeks**, vs 4–6 weeks for a traditional project
  - Time split: about 40% style development, 30% AI generation, 30% post-production polish and client communication
  - Budget not disclosed
  - Called a "刷屏级" (went viral) case, but no play data given
  - The same creator made 《马力全开》 for CNY using 可灵 O1 and 3.0, and reportedly did a NIKE spot (details not given)
- **可灵 brand partnerships** (as listed by 可灵 / 数英, no metrics) [CO via trade press] — [数英](https://www.digitaling.com/articles/1487072.html)
  - 周大福, 青岛啤酒 and 玛氏: physical, mass-produced AIGC-IP co-branding
  - 饿了么: Mother's Day branded short drama
  - 蜜雪冰城: brand-custom AIGC effect
  - 可灵 is the official tool of the 2026 大中华区艾菲 (Effie) AIGC contest, with briefs from 潮宏基, 华帝, 云南白药 and 999澳诺
  - Platform stats in the same piece: 60M+ global users, 600M+ videos generated, **30K+ enterprise customers and developers**
- **可灵 4K** (launched 2026-04-23): VML China (WPP) says it uses it internally. Creator tests include a credit-card ad for a financial client, with no campaign named [PRESS] — [数英 2026-04-29](https://www.digitaling.com/articles/1495927.html)
- **磁力引擎 at the China International Advertising Festival, 2025-10-24** [CO] — [数英](https://www.digitaling.com/articles/1423099.html)
  - 可灵-made 《保山不恼火》 for the "500个家乡" hometown-promotion IP
  - 女娲 digital-human livestream for an auto brand at 618 2025, claimed to "run volume as well as real people" (vague)
- **Earlier 国内 AIGC brand films (2023–25), roundup with no cost or time data** [PRESS] — [人人都是产品经理](https://www.woshipm.com/ai/6216096.html)
  - 联想 《生于1984》 (40th anniversary, 2024)
  - 淘宝造物节 (2023, "first fully AI-made" in the industry)
  - 携程 Double 11 2024 "躺平的埃及法老"
  - 美团 "团圆2024"
  - 一汽丰田 格瑞维亚 (Midjourney / Runway / AnimateDiff, by the 治柱Ai team)
  - 宁德时代 interactive AIGC film at the Guangzhou auto show
  - Hybrid AI + live action: 安踏 "欧文一代" (breathe工作室), 三得利 CNY (异数文化), 东阿阿胶 (寻光文化 / 异数文化)
- **Backlash cases from the same roundup**
  - McDonald's Japan 2024 (extra fingers)
  - KFC 2025 viral AI spot, accused of plagiarism by director David Blagojević
  - VW Brazil "revived" the late singer Elis Regina; CONAR (Brazil's ad self-regulator) opened an investigation
  - Dove pledged not to use AI-generated people ("The Code")

**国内 e-commerce brand AIGC video**
- 阿里妈妈 at 618 2025 (published 2025-05-28) [CO via trade press] — [数英](https://www.digitaling.com/articles/1360673.html)
  - Logitech, 毛戈平, 立白 and FILA batch-generated AI images and video
  - Add-to-cart up to +60%; conversion up to +70%
  - AI image-to-video CTR +60%
  - Three AI shorts with the Palace Museum (故宫)

### Inferences
- The costs that matter for a "hero spot" are talent, review and cleanup, not GPU. Coke 2025 used about 100 people for a 1-month job. Kalshi's "$2k" excludes the creator's fee and only works for absurdist, artifact-tolerant comedy.
- Every high-profile full-AI brand spot (Coke ×2, McDonald's NL, Svedka, Under Armour) generated negative earned media. Brands now pick non-human characters (animals, robots) or absurdist formats to avoid uncanny humans.
- In China, the AI-native ad format is branded serialized drama, not the 30s TVC. Brands own character IP (OPPO, 红旗) and plug into platform revenue-share and traffic subsidies. Unit economics are falling fast (¥3–5k/min → under ¥1k/min within a year), squeezing studios.

### Gaps
- **国内 brand TVCs made with 可灵/即梦 for 伊利, 蒙牛, 瑞幸, 中国移动 and 小米**: no verified case pages found. The search quota blocked further lookup. The best verified 国内 AI brand-film case is 美团 《麻烦死了》 (可灵, 4 people, 2 weeks).
- No 即梦/Seedance brand-TVC case was verified.
- No sourced 2025–26 AI ad case found for Liquid Death, Heinz (the 2022 "A.I. Ketchup" DALL-E campaign is known but unverified here), Nike, Volvo, Porsche or Mint Mobile.
- No sourced dollar budget for Coca-Cola, Svedka or Toys"R"Us.

## Q2. AI-native ad studios and agencies: who, scale, pricing

### Takeaway
The US AI-native ad studio tier is small and concentrated:
- **Silverside AI** (Coke 2025, Svedka SB, Amazon, BMW, Sephora)
- **Secret Level** (Coke)
- **Genre.ai** (PJ Accetturo, Kalshi)
- **Native Foreign** (Toys"R"Us)

Film-oriented AI studios such as Promise, Asteria/Moonvalley and Utopai are mostly not doing ads. No studio discloses per-spot pricing. In China the analogous players are AI 漫剧 / short-drama studios, whose per-minute price collapsed from ¥3–5k to under ¥1k in 2026.

### Cited Findings
- **Silverside AI** (San Francisco; also New York, Berlin, Munich) [CO] — [silverside.ai](https://www.silverside.ai/)
  - Client logos: Amazon, Coca-Cola, Sephora, Panasonic, Williams Sonoma, BMW, Goodwill, Pacsun, Svedka, CyberArk, SimpliSafe
  - Claims 68% cost reduction, 87.5% shorter time to market, 20x content volume and 7B impressions
  - Claims a network of "30+ offices / 6,000 creatives", which implies it sits inside a larger holding network
  - Ownership is not stated on its site
  - PJ Pereira (Pereira O'Dell co-founder) is quoted as Silverside's leader — [Comfy](https://comfy.org/customers/svedka-silverside)
- **Secret Level**: "An Entertainment Studio Powered by AI". Brand work: Coca-Cola, Raising Cane's, will.i.am/Taboo. Also originals [CO] — [secretlevel.co](https://www.secretlevel.co/)
- **Genre.ai** (PJ Accetturo, "PJ Ace") [CO/FOUNDER]
  - Self-described "world's leading AI-native Ad Agency", claiming 300M+ people saw its AI ads
  - No pricing; hiring comedy writers and AI filmmakers
  - Sources: [PJ Ace newsletter](https://pjace.beehiiv.com/p/i-can-t-believe-disney-allowed-us-to-run-this-ai-ad-during-the-nba-finals-f77e73388ab4ca62); [genre.ai](https://www.genre.ai/)
- **Native Foreign**: Toys"R"Us Sora film, about 12 people [PRESS] — [Tech Times](https://www.techtimes.com/articles/306053/20240626/toys-r-us-comeback-iconic-retail-chain-uses-openai-sora-brand-film)
- **Wild Card**: one of the three Coca-Cola 2024 studios [PRESS] — [NBC](https://www.nbcnews.com/tech/innovation/coca-cola-causes-controversy-ai-made-ad-rcna180665)
- **Asteria**: founded 2022 by Natasha Lyonne and Bryn Mooser; AI animated features; owned by Moonvalley [PRESS] — [Wikipedia: Natasha Lyonne, citing Inc./Vulture](https://en.wikipedia.org/wiki/Natasha_Lyonne)
  - No ad work found. The asteria.xyz domain is now parked for sale.
- **Utopai Studios** (Mountain View) [CO] — [utopaistudios.com](https://www.utopaistudios.com/)
  - Films and series only: Cortés, Space Nation, Journey to the West pilot in 2026
  - PAI production engine
  - No ad work listed
- **Groove Jones** (Dallas): FOOH holiday campaign for Dick's Sporting Goods / Crocs × NFL on ComfyUI [CO] — [Comfy customers](https://comfy.org/customers)
- **国内 AI 漫剧 / short-drama studios** [PRESS interviews] — [蓝鲸 2026-07-21](https://www.lanjinger.com/d/1784036025417585113); [人人都是产品经理](https://www.woshipm.com/operate/6429518.html)
  - 米粿AI (丁黎): price per minute fell from ¥3,000–5,000 (2025) to under ¥1,000 after CNY 2026
  - 杭州友和文化: first 60-minute AI 漫剧 cost ¥30–50k with a 5-person team over about 1 month. By Jan 2026, AI 漫剧 brought in about ¥70M of about ¥100M monthly revenue (about 80%)
  - 九州文化: AI cut an overseas short drama to ¥20–30k per title
  - Pure paid-traffic 漫剧 ROI fell to about 1.1; only the top-5 producers sustain ≥1.2
  - One producer spent ¥60k on ads for about ¥1k in paid conversions

### Inferences
- Silverside is the de facto Western "AI agency of record" for big brands: Coke, Svedka, Amazon. Its network claim suggests that holding-company-backed AI shops win the large briefs, not standalone startups.
- The Chinese AI studio market is in a price war. Per-minute price fell about 3–5x in roughly 9 months and paid-traffic ROI is near breakeven, so margin is shifting to platforms (subsidies, traffic) and IP owners.

### Gaps
- No funding, revenue or pricing data found for Promise (site unreachable), Wonder Project, Secret Level, Silverside or Genre.ai.
- Named 国内 studios 鬼灵, 闪影 and 坚果 were not found. Search quota blocked further lookup.
- No disclosed per-spot price from any AI ad studio.

## Q3. Performance-video tools: ARR, pricing, customers (incremental to round 1)

### Takeaway
The breakout is **Higgsfield**, a model-aggregator creative app aimed at marketers and creators. Reported ARR went from about $11M (May 2025) to $230M (Jan 2026), $700M (Aug 2026), and a claimed $1B (Sep 24, 2026), which makes it bigger than HeyGen and Synthesia. Ad-specific UGC tools stay at the $10–15M scale (Arcads: 8 employees, $10M ARR).

Pricing for finished UGC-style ad videos lands around **$1–$11 per video** on self-serve plans. Most tools now resell third-party models (Seedance 2.5, Kling, Veo, Nano Banana).

### Cited Findings
- **Higgsfield**
  - Sacra estimates about $11M ARR (May 2025), $100M (Nov 2025) and about $230M (Jan 2026) [3P-EST] — [Sacra](https://sacra.com/research/higgsfield-at-230m-arr/)
    - About 3M generations a day across 15M accounts
    - Targets social media managers, e-commerce brands and marketers
    - Aggregates Kling, Sora and Veo
    - 60+ ad presets
  - $700M annualized revenue with a $400M Series B at a $5.4B valuation, Aug 2026, citing a PR Newswire release [CO via AGG] — [ARR Club](https://www.arr.club/higgsfield/higgsfield-surpasses-700m-arr-with-400m-series-b-at-5-4b-valuation)
  - Crossed $1B annualized on 2026-09-24, 20x since Sep 2025, 300% NRR, enterprise adoption +115% MoM since June [CO via AGG] — [Digg summary](https://digg.com/ai/5c9uxe03); investor post <https://x.com/rockyrmit/status/2103288005327032655>
  - A primary Higgsfield release was not fetched.
- **Arcads**
  - Founder Romain Torres's dashboard showed $10M ARR on 2025-11-14 (from $5M in Apr 2025 and $1M in Jun 2024) [FOUNDER] — [GetLatka](https://getlatka.com/blog/arcads-revenue-ceo)
    - About 6,000 paying customers; 8 employees (about $1.25M ARR per employee)
    - Growth was above 20% a month
    - Largest ACV was "six figures"
    - Said to be profitable
  - $16M seed led by Eurazeo on 2025-12-17 [CO] — same
  - The site now advertises Seedance 2.5, Seedream, Nano Banana, GPT Image and Kling, plus 1,000+ AI actors and 30+ languages [CO] — [arcads.ai](https://www.arcads.ai/)
- **Creatify** pricing [CO] — [creatify.ai/pricing](https://creatify.ai/pricing)
  - Starter $39/mo for 100 credits; Pro $99/mo for 300 credits; API $99 for 500 credits or $299 for 2,000 credits
  - The free tier gives about 2 videos for 10 credits, implying about 5 credits per video, or about $1.65–$1.95 per ad (my calculation)
  - Funding: $15.5M Series A co-led by WndrCo [PRESS] — [TechCrunch](https://techcrunch.com/2025/06/02/former-dreamworks-ceo-jeffrey-katzenberg-co-leads-15-5m-series-a-for-ai-video-ad-platform/)
- **MakeUGC** pricing: Starter $29/mo for 500 credits; Growth $39/mo for 1,000 credits; Pro $79/mo for 2,000–5,000 credits (billed yearly) [CO] — [makeugc.ai/pricing](https://www.makeugc.ai/pricing)
- **HeyGen**
  - ARR $35M in Jun 2024 (Bloomberg), with 40K+ customers at a $500M valuation [PRESS] — [Wikipedia: HeyGen](https://en.wikipedia.org/wiki/HeyGen)
  - $100M ARR in Oct 2025 (see round 1)
  - Pricing: Creator $29/mo for 600 credits; Pro $49 for 1,000; Business $149 + $20/seat for 1,500 [CO] — [heygen.com/pricing](https://www.heygen.com/pricing)
- **Synthesia** [PRESS] — [Wikipedia: Synthesia](https://en.wikipedia.org/wiki/Synthesia_(company))
  - Revenue above $100M annually as of Oct 2025 (Forbes)
  - $200M Series E at $4B (GV, Nvidia, Accel)
  - Rejected a reported $3B Adobe offer
  - Used by 90% of the Fortune 100
  - Ads are secondary to L&D; an early ad case was Lay's "Messi Messages" (Cannes Bronze)
- **国内 platform tools**
  - 巨量引擎 AIGC 动态创意 is free and switched on in 千川, 巨量AD and 本地推 [CO via PRESS] — [新浪 2025-12-11](https://news.sina.cn/sx/2025-12-11/detail-inhamakh9109248.d.html?vt=4)
    - Video features: 灵感前贴, 数字人贴片, 通用混剪, 个性化智能口播, 短剧二剪
    - One auto client's single asset ran to 400K+ volume with 4x impressions
  - 即创: agency reports a 3-day video now takes hours; 2,000+ real-person digital humans [PRESS] — [新浪科技 2025-06-04](https://finance.sina.com.cn/tech/roll/2025-06-05/doc-ineyyvpk1750644.shtml)
  - 美图开拍, H1 2026: oral-presentation and marketing-video workflow [FILING/CO] — [美图官方](https://www.meitu.com/zh/media/439)
    - MAU +100%+, paid subscribers +150%+, ARR +100%+ YoY (absolute figures not disclosed)
    - Productivity-app ARR about ¥620M overall
    - Vmake (overseas e-commerce video) ARR about $5M
  - 快手 (Kuaishou), H1 2026: 850K+ merchants used free AI business tools (including marketing asset creation). This is free-tool adoption, not revenue [CO via PRESS] — [腾讯新闻 2026-09-28](https://news.qq.com/rain/a/20260928A09LJV00)

### Inferences
- The revenue pool has moved to **aggregator "creative OS" apps** (Higgsfield) and **model owners** (Kling, Runway), not ad-specific UGC wrappers. Arcads and Creatify are thin layers over Seedance, Kling and Veo, and platform-native free tools (巨量, 磁力, TikTok Symphony) compete with them directly.
- The 8-person, $10M Arcads shows the UGC-ad niche is profitable but capped.

### Gaps
- 2026 ARR or funding not found for Hedra, Tavus, Icon or Captions/Mirage beyond round 1.
- No primary source for HeyGen's 2026 ARR.
- No volume data found for 腾讯妙思, 磁力 女娲 or 阿里万相营造 2026.
- Higgsfield's $1B is company-stated via secondary sources only.

## Q4. Foundation-model enterprise and ad usage; verification of Kuaishou's AIGC ad metric

### Takeaway
**Verified from the HKEX filing:** "In the fourth quarter of 2025, the total spending from online marketing services driven by AIGC marketing materials reached RMB4.0 billion." That is about 17% of Q4 online-marketing revenue of RMB23.6B (my ratio; spend and revenue are not identical bases).

Later quarters switch metrics:
- Q1 2026: AIGC short-video materials reached a **10.0%** spend share as of Mar 2026
- Q2 2026: AIGC short-video material spend **+70% YoY**

The "+20–30% conversion" claim attached to the ¥4B in round 1 does **not** appear in the filing text.

### Cited Findings
- **Kuaishou Q4 2025 results** (2026-03-25) [FILING]
  - Exact text: "While reducing the cost of generating online marketing materials, AIGC technology also unlocked additional budgets from our marketing clients. In the fourth quarter of 2025, the total spending from online marketing services driven by AIGC marketing materials reached RMB4.0 billion."
  - Online marketing revenue +14.5% to RMB23.6B
  - UAX auto-placement covered nearly 80% of non-e-commerce spend
  - Kling Q4 revenue RMB340M; Dec 2025 monthly revenue above $20M (ARR $240M)
  - Sources: [HKEX filing PDF](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0325/2026032500367.pdf) (text extracted locally); [PRNasia/TechNode release](https://technode.global/prnasia/kuaishou-technology-announces-fourth-quarter-and-full-year-2025-financial-results/)
  - The filing also says AIGC tools helped lifestyle-services SMB merchants produce marketing materials.
- **Kling ARR, Jan 2026**: CEO said ARR exceeded $300M; full-year 2025 Kling revenue was about ¥1.04B (0.7% of group revenue) [CO/PRESS] — [澎湃](https://www.thepaper.cn/newsDetail_forward_32833762); [Caixin Global](https://www.caixinglobal.com/2026-03-25/kuaishou-ramps-up-ai-commercialization-as-kling-revenue-hits-150-million-102427380.html)
- **Kuaishou Q1 2026** [FILING via syndication] — [Taiwan News/PR syndication](https://www.taiwannews.com.tw/news/6370880)
  - "AIGC short video marketing materials spending contributed 10.0%" as of Mar 2026
  - Kling revenue above RMB650M (+300%)
  - Generative recommendation and bidding drove "roughly 3.0%–4.0%" domestic online-marketing growth
- **Kuaishou Q2 2026** [FILING via syndication] — [TechNode/PRNasia](https://technode.global/?p=990300)
  - "Over 70% year-over-year growth in spending on AIGC short video marketing materials"
  - Kling revenue above RMB850M (+200%)
  - Online marketing RMB20.6B (+4.4%)
  - Short-play-driven marketing spend +100%+
- **Runway**
  - Funding: $315M at a $5.3B valuation, Feb 2026 [PRESS] — [Wikipedia: Runway, citing TechCrunch](https://en.wikipedia.org/wiki/Runway_(company))
  - Partnerships: Lionsgate (custom model, Sep 2024); AMC Networks (marketing images and previz, Jun 2025)
  - Pricing: Gen-4.5 at 12 credits/s; Seedance 2.0 Pro is resold inside Runway at 40 credits/s. Enterprise promo: "2 months of usage free, sign by 10/31" [CO] — [runway.com/pricing](https://runway.com/pricing)
- **Seedance**: "Dreamina-seedance-2.5 API now fully available" on BytePlus [CO] — [BytePlus](https://www.byteplus.com/en/product/seedance)
  - Seedance 2.5 also powers Arcads, and Seedance 2.0 is resold by Runway (see above)
- **Sora**: discontinued in 2026 (see Q1)
  - This removes OpenAI from the ad-video model race as of Sep 24, 2026.

### Inferences
- Kuaishou is the only platform giving a **monetary** AIGC-creative figure. ¥4.0B in one quarter equals about 1.6x Kling's full-year 2025 revenue. The ad-platform effect of AIGC is larger than the model-subscription business, though "spend driven by" is an attribution metric, not incremental revenue.
- The model layer is consolidating to Google Veo, ByteDance Seedance (resold even by competitors Runway and Arcads), Kling and Runway. Sora's exit shows how expensive running consumer video generation is.

### Gaps
- Kuaishou has not disclosed an RMB amount for AIGC-driven spend in Q1 or Q2 2026, only the share and growth.
- No Kling enterprise customer count was verified in the Q2 release. Round 1's "close to 50K" is from secondary press; 可灵/数英 separately cite "30K+ enterprise customers and developers" (see Q1).
- No Google or Alphabet disclosure found on Veo enterprise ad revenue.

## Q5. Cost per finished second / per creative: AI vs traditional

### Takeaway
Raw generation cost is now **$0.05–$0.60 per second** (Veo 3.1 API) or about **$0.10–$0.77 per second** (Runway credits). Real hero spots need 20–30x over-generation (Kalshi: 300–400 generations for 15 clips) plus human labor:
- About $2k tooling plus a creator fee for a 30s comedy spot
- About 1 month and about 100 people for Coke 2025

Benchmarks:
- Traditional: about $400K+ and 2 months per national spot (Accetturo's comparison, [FOUNDER]); "$1M+" for Super Bowl creative (unsourced blog)
- Performance UGC ads: about $1–$11 per video via SaaS
- Chinese AI drama: ¥800–1,500 per minute (vs about ¥8–15k for live action)

### Cited Findings
- **Veo 3.1 API per second, with audio** [CO] — [Google AI pricing](https://ai.google.dev/gemini-api/docs/pricing)
  - Standard $0.40 (720p/1080p), $0.60 (4K)
  - Fast $0.10 / $0.12 / $0.30
  - Lite $0.05 / $0.08
  - An 8s Standard 1080p clip costs about $3.20 (my calculation)
  - Veo 3 Fast was "20 cents per generation" in Flow in mid-2025 [FOUNDER] — [PJ Ace](https://pjace.beehiiv.com/p/i-can-t-believe-disney-allowed-us-to-run-this-ai-ad-during-the-nba-finals-f77e73388ab4ca62)
- **Runway, implied per second** (my calculation from plan credit prices) [CO] — [runway.com/pricing](https://runway.com/pricing)
  - Gen-4.5: about $0.10–0.23/s
  - Aleph 2.0: about $0.22–0.54/s
  - Seedance 2.0 Pro 1080p: about $0.32–0.77/s
- **Kalshi math**: under $2k for about 300–400 generations yielding 15 clips [CO/FOUNDER] — [NPR](https://www.mprnews.org/story/2025/06/23/npr-ai-video-ad-kalshi-advertising-nba-finals)
  - Usable yield is about 4–5%
  - About $5–7 tooling per generation including subscriptions (my calculation)
- **Traditional comparison**: "$400K+ 2-month productions" [FOUNDER] — [PJ Ace](https://pjace.beehiiv.com/p/i-can-t-believe-disney-allowed-us-to-run-this-ai-ad-during-the-nba-finals-f77e73388ab4ca62)
  - NPR: competing spots "likely cost hundreds of thousands of dollars and months" (Accetturo's view)
- **Super Bowl**: Artlist spot in 5 days for "a few thousand dollars" vs "$1M-plus" typical (no source given) [AGG] — [AdventureMedia](https://adventuremedia.ai/blog/ai-takes-center-stage-at-super-bowl-lx-why-2026-is-the-year-of-real-adoption-in-creative-advertising)
  - Media: $10M per 30s [PRESS] — [Wikipedia: Super Bowl LX](https://en.wikipedia.org/wiki/Super_Bowl_LX)
- **Agency-claimed savings**
  - Silverside claims −68% cost and −87.5% time to market [CO] — [silverside.ai](https://www.silverside.ai/)
  - Svedka: under 1 month vs about 6 months historically [CO] — [Comfy](https://comfy.org/customers/svedka-silverside)
  - Coke 2025: about 1 month vs about 1 year [PRESS] — [TrueFutureMedia](https://www.truefuturemedia.com/articles/coca-cola-ai-holiday-ads-2025)
- **Performance-creative unit cost**
  - Creatify about $1.65–1.95 per ad (inferred from credits) [CO] — [Creatify pricing](https://creatify.ai/pricing)
  - Arcads about $11 per video (round 1, third-party) [3P] — [eesel](https://www.eesel.ai/blog/arcads-ai-pricing)
  - 巨量即创: 3 days → a few hours per video; adapted variants in 3–5 minutes [PRESS] — [新浪科技](https://finance.sina.com.cn/tech/roll/2025-06-05/doc-ineyyvpk1750644.shtml)
- **国内 AI drama / brand content** [PRESS] — [澎湃](https://www.thepaper.cn/newsDetail_forward_33391539); [数英](https://www.digitaling.com/articles/1526531.html); [蓝鲸](https://www.lanjinger.com/d/1784036025417585113)
  - AI 漫剧 costs ¥800–1,500 per minute (about 1/10 of live-action short drama)
  - A premium live-action short drama costs up to ¥3M
  - Per title: live action ¥500–800k vs AI 漫剧 ¥50–240k (−60–90%)
  - Per minute: ¥2–5k in mid-2025, now under ¥1k, as low as about ¥400
  - A traditional brand film costs "数十万元" (hundreds of thousands of RMB) vs a branded AI short [PRESS] — [数英](https://www.digitaling.com/articles/1526531.html)

### Inferences
- **Compute is under 1% of a hero spot's cost.** At $0.40/s, even 400 eight-second generations is about $1.3k. Cost is dominated by human iteration, cleanup, legal and brand review, which is why Coke still needed about 100 people.
- A practical ladder (my synthesis):
  - Performance UGC variant: about $1–10
  - Social hero spot by a solo AI director: about $2k tooling + $10–50k fee (fee unverified)
  - Brand TV spot by an AI studio: weeks and a team; budget undisclosed, claimed 60–90% cheaper
  - Traditional national spot: about $400K+
- In China, per-minute AI drama costs fell about 3–10x in a year, so price is no longer a differentiator. Distribution subsidies and ROI (about 1.1) decide winners.

### Gaps
- No authoritative 2026 benchmark found for traditional TVC cost per second (e.g., ANA or 4A's surveys). Search quota prevented lookup.
- Fees paid to AI studios (Silverside, Secret Level, Genre.ai) are undisclosed.
- No 国内 AI TVC price list found (e.g., ¥ per 15s brand spot).
- Kling API per-second price could not be fetched (JS-rendered page).

