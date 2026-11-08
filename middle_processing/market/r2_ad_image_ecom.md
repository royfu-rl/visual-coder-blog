# AI-generated ad images & e-commerce product imagery (国内+国外), round 2 — as of 2026-10-13

Method note
- About 70 tool calls: ~37 WebSearch, ~25 WebFetch, plus ~8 direct curls of vendor pricing pages.
  - The session-wide WebSearch budget (shared across agents) ran out partway through.
  - Most of the 国内 (China) block therefore rests on official sites and IR fetched directly, plus a few earlier hits.
  - Gaps are flagged explicitly.
- This round avoids repeating `ad_creative_gen.md` (round 1: Meta/Google/TikTok adoption counts, 巨量/磁力/阿里妈妈 volumes, Meitu H1 headline, video players). It goes deeper on image/product-photo players.
- Source-type tags on every number:
  - **[OFF]** = company/IR/official page
  - **[PRESS]** = news outlet
  - **[EST]** = third-party tracker/estimate (Sacra, GetLatka, aggregators)
  - **[VEND]** = vendor marketing claim
  - **[WIKI]** = Wikipedia, citing press

## Q1. 国外 (outside China) player map: funding, revenue, users, status

### Takeaway
The category splits into three revenue tiers:
- **Horizontal creative platforms** at $100M–$4B ARR: Canva about $4B, Freepik/Magnific $230M, Midjourney about $500M (estimate), Photoroom about $94M+ (estimate).
- **Vertical product-photo tools**, mostly bootstrapped or seed-stage and small: Pebblely, Pixelcut, Claid, Flair, Botika, Caimera, ZMO.
- **Creative-ops/ad-creative SaaS**, being absorbed or repositioned: AdCreative.ai → Appier for $38.7M; Lalaland → Browzwear; Booth.ai acquired; Creatopy renamed "The Brief"; Marpipe pivoted to catalog/DPA creative.

Photoroom is the only pure product-photo player that has demonstrably broken out.

### Cited Findings

**A. Pure-play product photo / AI photoshoot**
- **Photoroom** (Paris, founded 2019/20)
  - Funding: $43M Series B, Feb 2024, led by Balderton and Aglaé, at a $500M valuation; $64M raised in total [PRESS] — [TechCrunch](https://techcrunch.com/2024/02/27/confirmed-photoroom-the-ai-image-editor-raised-43m-at-a-500m-valuation); [Sifted](https://sifted.eu/articles/photoroom-43m-series-b)
  - ARR history (Sacra estimates) [EST] — [Sacra](https://sacra.com/c/photoroom/)
    - $1M (Aug 2020) → $2M (Dec 2020) → $50M (Dec 2023) → about $65M (Mar 2024) → about $94M (2024, +89% YoY)
    - The $500M valuation is about 7.7x the $65M ARR
    - 100M app downloads as of Dec 2023
  - Sifted (Oct 2024): €50M ARR "last year". Break-even one year after launch and "still profitable"; the co-founder declined to update the figure [PRESS] — [Sifted](https://sifted.eu/articles/photoroom-interview-gen-ai-profit)
  - The company page says it is "profitable and used by millions every month" [OFF] — [photoroom.com/company](https://www.photoroom.com/company)
  - Unverified claims:
    - "$150M ARR by Jan 2026": only on a SWOT-template site [EST, low quality] — [businessmodelcanvastemplate](https://businessmodelcanvastemplate.com/products/photoroom-swot-analysis)
    - Tracxn's "$15–40M" revenue estimate contradicts all of the above [EST] — [Tracxn](https://tracxn.com/d/companies/photoroom/__3Eb7XKd5tPi6IJQFKmZrfp2xHmMSn4DH7M3WdkToYPY)
  - Acquired Generate Banners (a templated banner generator) on 2025-05-22 [EST] — [Tracxn](https://tracxn.com/d/companies/photoroom/__3Eb7XKd5tPi6IJQFKmZrfp2xHmMSn4DH7M3WdkToYPY)
  - Enterprise/API proof points [VEND] — [photoroom.com/pricing](https://www.photoroom.com/pricing)
    - Wolt: over 140K merchants in 27 countries
    - Depop: over 1M listings
    - Decathlon: −99% editing cost
  - Sacra also names Netflix, Lionsgate, Zomato, Shopify, Audi, Faire and Zepto as API customers [EST] — [Sacra](https://sacra.com/c/photoroom/)
- **Pixelcut** (Oakland, founded 2020)
  - Rebranded to **Pixa** in Feb–Mar 2026, then **reverted to Pixelcut in May 2026** [OFF] — [pixa.com notice](https://www.pixa.com/pixelcut-is-now-pixa); [press release](https://www.news-graphic.com/online_features/press_releases/pixelcut-rebrands-to-pixa-launches-new-ai-creative-workspace-at-pixa-com/article_c6cb032e-77fd-590b-9d11-b0761725b543.html)
  - Users: "trusted by more than 70 million sellers, creators, and brands" [VEND] — [pixelcut.ai/about-us](https://www.pixelcut.ai/about-us)
  - Funding: CB Insights shows only $250K (convertible note, 2022) [EST] — [CB Insights](https://www.cbinsights.com/company/pixelcut/financials). Caplight shows $774K with a pre-seed in Oct 2025 [EST] — [Caplight](https://www.caplight.com/company/pixa)
  - Metronome: 15M MAU, over 100M images a month, about $19.8M "gross spending" [EST] — [Metronome pricing index](https://metronome.com/pricing-index/pixelcut-from-pixa)
  - This is effectively a bootstrapped, consumer-scale app.
- **Pebblely** (Singapore, Pebblely Pte Ltd)
  - Launched 2023-01-04 and bootstrapped "with only our savings"
  - 1.06M signups by 2023-08-23 with a team of 3.5 people; paying customers in more than 100 countries [OFF blog] — [Pebblely blog](https://pebblely.com/blog/one-million-signups/)
  - Homepage (2026): "1,000,000+ creatives" and "25,000,000+ images generated" [VEND] — [pebblely.com](https://pebblely.com/)
  - The user count has not grown publicly since 2023, which suggests a plateau (inference).
  - No revenue or funding disclosed.
- **Flair.ai** (founded 2022, Mickey Friedman)
  - Reported funding varies by source:
    - $5M seed [PRESS] — [Practical Ecommerce](https://www.practicalecommerce.com/flair-remakes-product-photography)
    - $10M total with AI Grant and CRV, seed dated 2024-01-10 [EST] — [Caplight](https://www.caplight.com/company/flair)
  - Neither figure comes from a primary announcement.
- **Claid.ai** (Let's Enhance; Ukrainian-American)
  - $3M seed led by Chamaeleon, 2021-10-27
  - At that time: revenue above $1M a year; customers included Mixtiles and Vente-privée [PRESS/OFF] — [BusinessWire](https://www.businesswire.com/news/home/20211027005182/en/Lets-Enhance-Raises-%25243M-Seed-Round-to-Help-Marketplaces-Scale-Faster-With-Next-Gen-AI-Photo-Editing); [tech.eu](https://tech.eu/2021/10/27/ukrainian-american-image-processing-startup-lets-enhance-raises-3-million/)
  - No later round found.
  - Product has moved from "enhance API" to AI Photoshoot, AI Fashion Models and Image-to-Video APIs [OFF] — [claid.ai/pricing](https://claid.ai/pricing)
- **Booth.ai** (YC W23; Nick Locascio, Ian Baldwin; team of 3)
  - YC lists it as **"Acquired"**, with no acquirer named
  - It pivoted from "Instant Product Photography with AI" to a no-code gen-AI app builder [OFF] — [YC profile](https://www.ycombinator.com/companies/booth-ai)
  - CapCut pages say the service is discontinued [VEND-competitor] — [CapCut](https://www.capcut.com/id-id/resource/booth-ai)
  - Related consolidation: Treat (an AI product photography company) was acquired by Typeface in Sep 2024 [EST] — [CB Insights compare](https://www.cbinsights.com/compare/booth-ai-vs-treat-technologies-1)
- **Botika** (Tel Aviv; AI fashion models)
  - $8M seed on 2025-01-16, co-led by Stardom Ventures and Secret Chord, with Seedcamp
  - Revenue grew 9x and its customer base 11x YoY; "serving over 1000 brands in the US and Europe" [OFF] — [Botika blog](https://botika.com/thethread/news/a-big-step-forward-botikas-mobile-app-and-8m-seed-round)
  - GetLatka estimates about $3M revenue for 2025 (cited in round 1) [EST]
- **Caimera** (India; developed by Bahaal Technologies)
  - Wellfound shows a $700K pre-seed, Jul 2022 [EST] — [Wellfound](https://wellfound.com/jobs/3005851-ai-fashion-prompter)
  - A "$5M Series A" on stork.ai is unreliable [EST, low quality] — [stork.ai](https://www.stork.ai/en/caimera)
- **Lalaland.ai** (Amsterdam, founded 2019)
  - 100% acquired by **Browzwear** (Singapore, 3D digital product creation / VStitcher) around 2025-07-25; terms undisclosed [PRESS] — [FashionUnited](https://fashionunited.uk/news/business/browzwear-acquires-lalaland-ai/2025072583016); [Silicon Canals](https://siliconcanals.com/lalaland-ai-gets-acquired-by-browzwear)
  - This is a gen-AI model tool folded into a 3D garment pipeline (see Q6).
- **ZMO.ai** (Hangzhou / Sacramento; CEO Ella Zhang, ex-Google/Apple)
  - $8M Series A in May 2022; investors include Hillhouse/GL Ventures, GGV and GSR; it used GANs at the time
  - No later round found [PRESS] — [TechCrunch](https://techcrunch.com/2022/05/17/zmo-ai-generate-human-8-million); [EqualOcean](https://equalocean.com/news/2022051918067-ai-content-generator-zmo-ai-raises-usd-8mn-series-round-hillhouse-leads)

**B. Ad-creative SaaS (performance creative)**
- **AdCreative.ai → Appier** (TSE: 4180)
  - Announced 2025-02-12; expected to close 2025-03-04
  - **Total $38.7M (base $27.3M plus earn-out)** [OFF/PRESS] — [Appier release via AAP](https://www.aap.com.au/aapreleases/cision20250212ae17659/); [FrenchWeb](https://www.frenchweb.fr/appier-acquiert-la-startup-francaise-adcreative-ai-pour-387-millions-de-dollars/451864)
  - TechSoda's "≈100M yen" is wrong: $38.7M is about ¥5.8B — [TechSoda](https://techsoda.substack.com/p/appiers-acquisition-of-adcreativeai)
  - The adcreative.ai/pricing URL now returns 404 (checked 2026-10-13).
- **Marpipe**
  - Funding:
    - $2M seed in 2019, backed by Adobe, Laconia and others
    - $8M Series A on 2021-09-08, led by Stage 2 Capital with Samsung participating; more than $10M in total [PRESS] — [AdExchanger](https://adexchanger.com/platforms/creative-testing-platform-marpipe-snags-8m-from-big-name-investors); [BusinessWire](https://www.businesswire.com/news/home/20210908005280/en)
  - No later round or acquisition found.
  - **Pivoted from multivariate creative testing to catalog/DPA creative**: "Catalog Creative", "Generative Catalogs", "Product Level Video", Feed Management [OFF] — [marpipe.com/pricing](https://www.marpipe.com/pricing)
    - Claims 7,000+ users
    - A Meta partnership subsidizes the cost for qualified brands
    - Pricing: Free; Startup $199/mo (500-SKU cap); Enterprise $999/mo plus $0.5/SKU; Feed management $0.05/SKU ($400 minimum) [OFF]
- **Omneky**
  - About $10–13M raised (seed $2.5M, then a $7M+ extension in Nov 2022) [PRESS/EST] — [mrweb](https://www.mrweb.com/drno/news34203.htm); [CB Insights](https://www.cbinsights.com/company/omneky/financials)
  - Reg CF crowdfunding in Feb 2025 at about an $80M valuation (company-sourced) [VEND] — [yespress](https://yespress.io/omneky)
  - No 2026 data found.
- **Pencil**: now inside Brandtech (round 1).
- **Creatopy → "The Brief"**: the site now reads "The Brief, formerly Creatopy" [OFF] — [creatopy.com](https://www.creatopy.com/)
  - Pricing: Pro $29/mo and Ultra $79/mo, billed annually, with "no credits"
  - Ultra adds ad serving to 25+ networks and publishing to Meta and Google Ads [OFF] — [pricing](https://www.creatopy.com/pricing/)
  - Claims 70% faster launches and 40% lower cost per asset [VEND]

**C. Horizontal gen-image / design platforms**
- **Canva**
  - $4B ARR at end-2025, including $500M B2B (25+ seats); 265M MAU; over 31M paid users [PRESS via WIKI] — [Wikipedia: Canva](https://en.wikipedia.org/wiki/Canva) (cites TechCrunch, 2026-02-18)
  - $42B valuation (employee sale, Aug 2025) [PRESS via WIKI]
  - Aug 2026: cut its growth guide from 30% to 20% because of **AI serving costs**; cost per AI task down about 90% since Canva AI 2.0 (Apr 2026) [PRESS via WIKI, Fortune 2026-08-12] — [Wikipedia: Canva](https://en.wikipedia.org/wiki/Canva)
  - Sacra [EST] — [Sacra](https://sacra.com/c/canva/)
    - 800M AI tool uses a month (+700% YoY)
    - Magic Studio used over 24B times in the past year
    - Leonardo.ai acquired for about $370M; its Phoenix model is the base for Canva's own model
  - Other aggregators give "5B" and "16B" cumulative uses; these conflict [EST] — [sqmagazine](https://sqmagazine.co.uk/canva-statistics/)
- **Adobe** (Q3 FY2026, call on 2026-09-11) [OFF transcript] — [Motley Fool transcript](https://www.fool.com/earnings/call-transcripts/2026/09/11/adobe-adbe-q3-2026-earnings-call-transcript/)
  - AI-first ending ARR above $650M (+150% YoY); total ending ARR $27.5B
  - Firefly ending ARR (app plus credit packs) +40% QoQ; no absolute figure given
  - Creative freemium MAU (Firefly plus Express) above 100M (+70% YoY)
  - GenStudio ARR is only described as growing ">20% YoY", bundled with AEM and AEP. **No standalone GenStudio for Performance Marketing ARR is disclosed**
  - New product: "GenStudio for Commerce Media Networks" lets retailers offer self-serve creative to the brands advertising on their media networks
  - Q1 FY2026: GenStudio family ARR +30% YoY [OFF] — [Adobe Q1 FY26 script](https://www.adobe.com/cc-shared/assets/investor-relations/pdfs/21306202/c545hjdryueyw34.pdf). Growth is decelerating
- **Freepik → Magnific** (rebranded 2026-04-28)
  - **$230M ARR** (via Fortune); over 1M paying subscribers; over 250 enterprise customers (Puma, BBC, Amazon Prime Video…); bootstrapped and profitable
  - EQT bought about 53% in 2020 at about a €250M valuation
  - A multi-model aggregator (Veo 3.1, Seedance 2.0, plus its own Magnific upscaler) [PRESS] — [TNW](https://thenextweb.com/news/freepik-rebrands-as-magnific)
  - "Video ≈ half of revenue" is reported only in secondary summaries [EST] — [creativeainews](https://www.creativeainews.com/articles/freepik-rebrands-magnific-ai-creative-platform/)
- **Midjourney**
  - Revenue estimates [EST] — [GetLatka](https://getlatka.com/companies/midjourney); [axis-intelligence](https://axis-intelligence.com/midjourney-statistics/)
    - About $200M (2023), about $300M (2024), **about $500M (2025)**
  - Sacra: $200M ARR (2023); about 1.4M paying subscribers; 21M Discord members [EST] — [Sacra](https://sacra.com/c/midjourney/)
  - Meta licensing partnership, 2025-08-22, terms undisclosed [EST] — [Sacra](https://sacra.com/c/midjourney/)
  - Plans: $10 / $30 / $60 / $120 a month
  - Profitable since Aug 2022 per Holz [WIKI] — [Wikipedia](https://en.wikipedia.org/wiki/Midjourney)
- **Ideogram**
  - $16.5M seed (2023) and **$80M Series A in Feb 2024**, led by a16z [PRESS] — [BNN Bloomberg](https://www.bnnbloomberg.ca/startup-ideogram-raises-80-million-for-ai-image-generation-1.2040466)
  - No reliable 2025–26 round or ARR found; the TechStackIPO pages are self-contradictory.
- **Recraft**
  - **$30M Series B on 2025-05-05**, led by Accel; over 4M registered users; about $42M raised in total [PRESS] — [Wikipedia: Recraft](https://en.wikipedia.org/wiki/Recraft); [TheSaaSNews](https://www.thesaasnews.com/news/recraft-raises-30-million-in-series-b/)
- **Krea**
  - $47M Series B (Apr 2025, Bain Capital Ventures) at about a $500M valuation; $83M raised in total [PRESS] — [Techleap](https://finder.techleap.nl/news/feed/krea-raises-83m-at-500m-valuation)
  - About $8M ARR with over 20M users (Jul 2025) [PRESS-CN] — [虎嗅](https://m.huxiu.com/article/4551311.html)

**D. Platform / marketplace-native, free inside the stack** (detail in Q7)
- Google Product Studio, Amazon Ads Image Generator / Creative Agent, Shopify Magic, Meta Advantage+ creative, Adobe GenStudio for CMN.

### Inferences
- Product photography is "commoditizing upward":
  - Single-function tools (Pebblely, Booth, Pic Copilot, Pixelcut's rebrand churn) stall or exit.
  - Winners either own distribution (Photoroom via the mobile app plus Wolt/Depop-type API deals; Canva) or aggregate many models (Freepik/Magnific, WeShop).
- Fashion "AI model" startups (Lalaland, Botika, ZMO, Caimera, Claid AI Fashion) have converged on the same feature set. Exits so far are tuck-ins into adjacent workflow owners (Browzwear 3D, Typeface), not standalone scale-ups.
- Rising AI inference cost is now a margin factor even at Canva's scale (the 20% guide cut). Credit-based pricing, which nearly every vendor below uses, is the industry's response.

### Gaps
- No 2025–26 primary ARR for Photoroom; the last company-confirmed figure is €50M ARR (2023).
- No revenue for Pebblely, Flair, Claid (after 2021), Pixelcut (only "gross spend"), Caimera or ZMO.
- Booth.ai's acquirer and date are unknown.
- AdCreative.ai's revenue contribution inside Appier was not found (Appier FY2025 results were not fetched).
- No standalone GenStudio for Performance Marketing ARR is disclosed by Adobe.

## Q2. 国内 (China) player map: 阿里 / 美图 / 稿定 / 创客贴 / 京东 / WeShop / LiblibAI / 即梦 …

### Takeaway
In China the category is dominated by **platform-owned free tools**:
- 阿里妈妈 万相营造 and 绘蛙 (Alibaba 100%)
- 巨量 即创 (ByteDance)
- 腾讯 妙思 (Tencent)

Plus **Meitu**, the only listed pure-play with disclosed numbers:
- Productivity apps: ARR about ¥620M, 2.35M paying subscribers
- 美图设计室: a high-ARPPU e-commerce tier
- Designkit: its overseas twin

The most interesting cross-border pure-play is **WeShop 唯象**. It is backed by **蘑菇街 (NYSE: MOGU)**, claims 3M+ users, and runs a multi-model aggregator. Alibaba's cross-border **Pic Copilot** shows a "Service Closure Notice" (Oct 2026).

### Cited Findings
- **美图 (Meitu), H1 2026** [OFF] — [美图官方业绩](https://www.meitu.com/zh/media/439)
  - Productivity apps:
    - 2.35M paying subscribers (+29.8%); MAU 33M (+43.5%); ARR about ¥620M
    - ARPPU about 50% above lifestyle apps
    - AI compute-credit consumption +113% in the half-year
  - **美图设计室** (e-commerce design workflow): Agent Teams launched Jun 2026 to generate multi-marketplace-ready assets; "thousands of users" at about 10x company ARPPU
  - Company-wide paying subscribers: 18.44M (+19.7%); penetration 6.5%
  - **Vmake Labs** (overseas): ARR about $5M; MAU +54%
  - 开拍 (marketing/talking-head video): ARR +100%+
  - Product-level split of the ¥620M not disclosed
- **Designkit** (designkit.com)
  - Meitu's overseas "E-Commerce Design AI Agent / AI Marketing Studio": marketplace images, UGC and product video; footer "© 2026 Meitu, Inc."
  - Plans: Free (20 credits); Basic 500 credits a month; Pro 1,500 credits a month (prices not rendered) [OFF] — [designkit.com/pricing](https://www.designkit.com/pricing)
- **阿里 绘蛙 (Huiwa)**
  - Developer: 杭州连凡信息技术有限公司, 100% owned by 阿里巴巴(中国)有限公司
  - Invite test from Jan 2024; aimed at Taobao/Tmall merchants and 达人 (influencers): AI model training, product/model photos, 种草 (seeding) copy [PRESS] — [36氪 2024-03-07](https://www.36kr.com/p/2679408525358600); [界面](https://www.jiemian.com/article/10870368.html)
  - Site now advertises 小红书 images, product main images, cross-border main images, virtual try-on, face swap and more [OFF] — [ihuiwa.com](https://www.ihuiwa.com/)
  - **No user or merchant count found** (gap carried over from round 1).
- **阿里妈妈 万相营造** (formerly 万相实验室)
  - Official description: "万相融绘" offers product digital-twin training, high-fidelity brand reproduction, creative background fusion, model-holding-product shots, and custom model/scene try-on [OFF] — [agi.alimama.com](https://agi.alimama.com/)
  - Volumes: see round 1 (Double 11 2025: 150M AIGC images/videos; about ¥40M/day saved).
- **Pic Copilot** (Alibaba International cross-border; images hosted on alicdn; partner links to Alibaba.com, AliExpress, Accio)
  - Claims 1.5M sellers (elsewhere "1,030,000 merchants") and "$1.5B in content costs saved" [VEND]
  - CTR claims conflict: "54.7% increase" vs "7.69% product CTR increase" [VEND] — [piccopilot.com](https://www.piccopilot.com/)
  - **Homepage banner "PicCopilot Service Closure Notice"** (seen 2026-10-13); notice text is JS-loaded and not retrieved [OFF] — [piccopilot.com](https://www.piccopilot.com/); [pricing](https://www.piccopilot.com/pricing)
- **WeShop 唯象**
  - "WeShop AI is backed by MOGU, NYSE-listed (NYSE: MOGU)"; entity WeShop.com Limited
  - Claims "Trusted by 3,000,000+ users worldwide" [VEND/OFF] — [weshop.ai](https://www.weshop.ai/); [weshop.com 中文](https://www.weshop.com/)
  - Product: AI 模特 (AI models), virtual try-on, AI 静物 (still-life), mannequin-to-model, pose change; API; iOS/Android/desktop
  - Integrates third-party models: Seedream 5.0, Qwen Image Edit, Z-Image, FireRed Image Edit, Seedance 2.0/2.5, Kling, Wan, Hailuo, Vidu Q3, MiniMax, plus GPT Image / Nano Banana / Midjourney on the global site
  - So the answer to "蘑菇街?" is yes: MOGU's AI bet is WeShop.
  - MOGU IR pages were not retrievable, so no WeShop revenue line.
- **稿定设计 (Gaoding)**
  - Site promotes an "AI 电商" (AI e-commerce) section and "全能商品精修…一键出图" (one-click product retouching) [OFF] — [gaoding.com](https://www.gaoding.com/)
  - **No revenue or funding found this round** (the search budget ran out; Baike returned 403).
- **创客贴 (Chuangkit)**
  - Site lists "AI商品图", 出海电商主图 (cross-border main images), batch cutout, image translation, an open API, and "8000万图片素材" (80M images) [OFF] — [chuangkit.com](https://www.chuangkit.com/)
  - No financials.
- **堆友 (d.design, Alibaba design community)**
  - Now branded "堆友Agent": design Skill workflows, e-commerce design [OFF] — [d.design](https://d.design/)
  - No numbers.
- **京东 (JD)**
  - 言犀 (yanxi.jd.com) is positioned as an intelligent human-machine interaction platform (customer service, marketing), not an image tool [OFF] — [yanxi.jd.com](https://yanxi.jd.com/)
  - **京点点** (JD's AIGC content tool) could not be verified: the guessed URL jdd.jd.com redirects to the JD homepage. No numbers found.
- **LiblibAI 哩布哩布**
  - Site: "AI绘画原创模型分享社区，10万+模型", i.e. 100K+ models, a webUI/ComfyUI community [OFF] — [liblib.art](https://www.liblib.art/)
  - Funding not retrieved this round (search budget exhausted).
- **即梦 (Jimeng / ByteDance)**
  - Text/image-to-image and video, smart canvas (inpainting, outpainting, cutout) [OFF] — [jimeng.jianying.com](https://jimeng.jianying.com/)
  - Its Seedream/Seedance models show up as engines inside WeShop and Freepik (see above).
  - TikTok Symphony uses Dreamina/Seedance (round 1).

### Inferences
- Chinese marketplaces give creative generation away (万相营造, 即创, 妙思) because it lifts ad spend. Independents therefore monetize via:
  - **cross-border sellers** (WeShop, Pic Copilot, Designkit, 创客贴 出海主图), or
  - **high-ARPPU pro tiers** (美图设计室 at 10x ARPPU).
- The WeShop model list shows independents increasingly act as **model aggregators plus e-commerce workflow**. Chinese open-weight image-edit models (Qwen Image Edit, Seedream, Wan) are the cost base.

### Gaps
- 绘蛙 users, 稿定 revenue/funding, 京点点 volumes, LiblibAI funding, 拼多多/Temu/SHEIN in-house AI product-image usage, 小红书 AI 种草图, and 鹿班's current status: **none found this round**. The shared search budget was exhausted; these need a follow-up pass on 36氪/晚点/亿邦/雨果跨境.
- WeShop revenue: MOGU quarterly releases were not retrievable.
- Pic Copilot closure: date and scope are unknown.

## Q3. Pricing: per-image and subscription benchmarks

### Takeaway
Prices fall in three bands:
- **API per-image prices**: $0.02 for background removal to about $0.10 for a generative edit (Photoroom)
- **Prosumer subscriptions**: $8–40 a month for roughly 30–600 images
- **Fashion-model / brand tiers**: about $45–120 per seat a month, with enterprise from about $1.5K a month

Platform tools (Google, Amazon, Meta, 阿里, 巨量) are free, which caps what SMB-facing independents can charge.

### Cited Findings
- **Photoroom API** [OFF] — [photoroom.com/api/pricing](https://www.photoroom.com/api/pricing)
  - Basic (Remove Background) **$0.02/image**
  - Plus (Image Editing API: AI backgrounds, etc.) **$0.10/image**
  - Example: $20 for 1,000 images on Basic
- **Photoroom web/app** [OFF] — [photoroom.com/pricing](https://www.photoroom.com/pricing)
  - Pro: 8K credits / 1K exports
  - Max: 25K credits; adds video and Shopify
  - Ultra: 75K credits; 4K
  - Enterprise: usage-based; generative operations carry an extra fee
- **Photoroom mobile Pro**: $4.99/week or $89.99/year (US) [EST] — [Sacra](https://sacra.com/c/photoroom/)
- **Pebblely** [OFF] — [pebblely.com/pricing](https://pebblely.com/pricing)
  - Lite $9/mo for 30 images (about $0.30/image)
  - Basic $19/mo for 200 images (about $0.095)
  - Pro $39/mo for 500 images (about $0.078)
- **Pixelcut** [OFF] — [pixelcut.ai/pricing](https://www.pixelcut.ai/pricing)
  - Pro $10/mo ($8 billed yearly) for 600 AI credits
  - Business $30/mo ($24 yearly) for 3,600 credits
- **Flair.ai** [OFF] — [flair.ai/pricing](https://flair.ai/pricing)
  - Pro $8/mo; Pro+ $26/mo (80 images); Scale $38/mo (150 images, API early access)
  - "Ad generation costs 4x" an image
- **Claid.ai** [OFF] — [claid.ai/pricing](https://claid.ai/pricing)
  - Credits per operation: background removal 1 credit; AI Photoshoot / AI Fashion 4 credits; AI Video 60 credits per 5s
  - Essentials / Pro / Business tiers allow 125 / 500 / unlimited AI photoshoots
  - Dollar prices did not render
- **Botika** [OFF] — [botika.io/pricing](https://botika.io/pricing)
  - Pro: $46/mo billed annually, 600 credits a year (more than 240 photos a year)
  - Advanced: about $40–100/mo, 1,000 credits a year (page rendering ambiguous)
  - Includes human retouch rounds
  - Roughly $2–3 per finished photo (inference)
- **Caimera** [OFF] — [caimera.ai/pricing](https://www.caimera.ai/pricing)
  - Mini $15 per user a month (120 credits); Starter $45 (350); Pro $117 (1,000)
  - Enterprise **from $1,500**: custom brand AI, digital twins, legal indemnification
- **Freepik/Magnific**: €12 / €27 / €66 a month, annual (Sep 2026 listing) [EST] — [usagepricing](https://usagepricing.com/blueprint/freepik)
- **Midjourney**: $10 / $30 / $60 / $120 a month [EST] — [Sacra](https://sacra.com/c/midjourney/)
- **Creative-ops**
  - Creatopy/The Brief: $29 / $79 a month per seat [OFF] — [creatopy pricing](https://www.creatopy.com/pricing/)
  - Marpipe: $199 / $999 a month plus $0.5 per SKU [OFF] — [marpipe pricing](https://www.marpipe.com/pricing)
  - Bannerbear: $49 / $149 / $299 a month for 1K / 10K / 50K API credits [OFF] — [bannerbear pricing](https://www.bannerbear.com/pricing/)
- **Free in-platform**
  - Google Product Studio: "for free" [OFF] — [Google blog](https://blog.google/products/shopping/google-product-studio-generative-ai-product-photos/)
  - Amazon Creative Agent: "no additional cost" [OFF] — [About Amazon EU](https://www.aboutamazon.eu/news/innovation/amazon-ads-launches-creative-agent-new-agentic-ai-tool-that-creates-professional-quality-ads)
  - Shopify Magic: included in plans [OFF] — [Shopify help](https://help.shopify.com/en/manual/shopify-admin/productivity-tools/shopify-magic)

### Inferences
- Marginal price per generated product image has converged to **about $0.05–0.10** for SMB and API use, while fashion on-model shots with QA run **about $2–5** per image.
- The gap is paid for with human retouch, brand-consistent "digital twin" models, and indemnification. It is not model quality.

### Gaps
- Claid and Designkit dollar prices did not render.
- WeShop and Pic Copilot plan prices were not shown.
- No CNY per-image prices were collected for 美图设计室, 稿定 or 创客贴.

## Q4. Cross-border sellers' adoption

### Takeaway
Cross-border is where independent AI product-image tools find paying demand:
- Pic Copilot (claims 1.5M sellers; now closing)
- WeShop (3M+ users, MOGU)
- Photoroom (Depop / Wolt / eBay / Poshmark sellers)
- Pixelcut (70M "sellers, creators, and brands")
- Pebblely (1M signups, 100+ countries)
- Meitu's Designkit and Vmake (overseas ARR about $5M for Vmake)

Hard adoption-rate data (share of cross-border SKUs using AI images) was **not found**.

### Cited Findings
- Pic Copilot: "1.5 million sellers" / "over 1,030,000 merchants", for Amazon, Shopify, Etsy, TikTok and Instagram [VEND] — [piccopilot.com](https://www.piccopilot.com/)
- WeShop: 3M+ users; marketplace logos for Mercado Libre, Etsy, Lazada, Shopee, eBay, Amazon and Allegro [VEND] — [weshop.ai](https://www.weshop.ai/)
- Photoroom's core users are online sellers on eBay, Depop and Poshmark [EST] — [Sacra](https://sacra.com/c/photoroom/). Wolt has 140K merchants in 27 countries on its API [VEND] — [Photoroom pricing](https://www.photoroom.com/pricing)
- Pebblely: paying customers in more than 100 countries [OFF] — [Pebblely blog](https://pebblely.com/blog/one-million-signups/)
- Meitu: overseas paid subscribers growing about 2x faster than mainland China; productivity apps outside mainland MAU +80%; Vmake ARR about $5M [OFF] — [美图](https://www.meitu.com/zh/media/439)
- 绘蛙 and 创客贴 both market "跨境电商主图 / 出海电商主图" (cross-border main images) [OFF] — [ihuiwa.com](https://www.ihuiwa.com/); [chuangkit.com](https://www.chuangkit.com/)

### Inferences
- Cross-border sellers need many locale variants (models of different ethnicities, image translation, marketplace-specific formats), which multiplies image count per SKU. This is why AI model and translation features are bundled.

### Gaps
- No 雨果跨境 / 亿邦动力 survey numbers on AI image adoption among cross-border sellers (searches were not possible after the budget ran out).
- Temu/SHEIN in-house AI imagery usage was not found.

## Q5. Measured CTR/CVR uplift (prefer A/B with sample size)

### Takeaway
Rigorous evidence is thin. The best-specified figures are Meta's own Advantage+ docs, all modest:
- **+2–3% conversions** for background generation
- **+13%** for related-media variants
- **+2%** for video expansion

Marpipe publishes a live **about 20% catalog-ad lift averaged over 650+ ad accounts**. Most other numbers are vendor "up to" claims (Amazon "up to 40% CTR"; Pic Copilot 54.7%) or single anecdotes.

### Cited Findings
- **Meta** (Advantage+ creative docs, retrieved Jul 2026) [OFF via secondary] — [Digital Applied](https://www.digitalapplied.com/blog/meta-muse-image-video-paid-social-creative-2026)
  - Background generation in catalog ads: +2–3% conversions
  - Related-media variants: +13%
  - Reels video expansion: +2%
  - Muse Image comes to Advantage+ "in the coming weeks" (2026-07-07)
- **Meta 2025 case studies** (no sample sizes) [VEND] — [eMarketer](https://www.emarketer.com/content/meta-launches-11-new-ai-ad-tools-cannes-lions-2025); [medianews4u](https://www.medianews4u.com/meta-launches-advanced-genai-ad-features-for-advertisers-and-agencies/)
  - Avimee Herbal: −62% cost per sale, 1.8x conversions
  - BigBasket three-cell test: +2.7% CTR, −3.4% CPI
- **Independent (agency) data**
  - Digital Applied: +12% CTR but about 8% worse conversion above $100 AOV (Mar 2026) [EST] — [Digital Applied](https://www.digitalapplied.com/blog/meta-muse-image-video-paid-social-creative-2026)
  - A practitioner across 50 campaigns: −23% cost per conversion; gains rose from 11% to 47% with 15 distinct concepts vs 5 background variants (unreplicated) [EST] — [dev.to](https://dev.to/synergistdigitalmedia/we-tested-metas-advantage-creative-in-50-campaigns-heres-what-actually-moved-the-needle-4mle)
- **Amazon**: lifestyle-scene images "can lift CTR up to 40%" on mobile Sponsored Brands vs white-background images (Oct 2023, beta, no n) [OFF via PRESS] — [Search Engine Journal](https://searchenginejournal.com/amazon-introduces-generative-ai-image-tool-for-advertisers/499439); [TechRadar](https://www.techradar.com/pro/amazons-new-ai-image-generator-might-finally-mean-the-end-of-boring-ads)
- **Google**: offers with more than one image get +76% impressions and +32% clicks vs offers with one image. This is the rationale for Product Studio, **not** an AI-vs-real test [OFF] — [Google blog](https://blog.google/products/shopping/google-product-studio-generative-ai-product-photos/)
- **Marpipe**: "~20% lift in catalog ads… live average from 650+ connected ad accounts, updated monthly" [VEND] — [marpipe.com/pricing](https://www.marpipe.com/pricing)
  - Ridge CEO: "multicell test… performance improve 53% vs BAU Meta catalog" [VEND testimonial]
- **Pic Copilot**: "54.7% increase in CTR" and, separately, "7.69% product CTR increase" on the same page [VEND] — [piccopilot.com](https://www.piccopilot.com/)
- **China (round 1)**: 阿里 AIGC image-to-video +60% CTR; 巨量 即创 +8% ROI; 快手 AIGC +20–30% conversion; all platform-reported.
- **Creatopy/The Brief**: 40% lower cost per asset, 2x output (an efficiency metric, not CTR) [VEND] — [creatopy.com](https://www.creatopy.com/)

### Inferences
- Where a platform publishes controlled-ish numbers (Meta), the creative-attributable conversion lift is **low single digits**. Double-digit claims come from "up to", cherry-picked or catalog-enrichment contexts.
- In catalog contexts the comparison baseline is a plain white-background DPA, which is weak.
- Creative *diversity* (more distinct concepts) matters more than the AI-ness of each image, consistent with Meta's Andromeda-era guidance.

### Gaps
- No peer-reviewed or academic field experiment with a sample size was found this round.
- The searches needed to locate Alibaba/AliExpress gen-AI field-experiment papers could not be run.
- No independent study of AI on-model fashion images vs real photoshoots on return rates or CVR.

## Q6. Where 3D / code fits (CGI packshots, programmatic templates, HTML-to-ad)

### Takeaway
3D and templates are the **deterministic layer**. Gen-AI is moving into both:
- **3D-first**: Threekit (generates "tens of thousands of photorealistic 2D images from a few 3D files", with AI lifestyle scenes), and Browzwear absorbing Lalaland to attach AI models to 3D garments.
- **Template-first**: Bannerbear, Placid, Creatopy/The Brief, and Marpipe catalog templates. These render price, logo and text exactly, at per-API-credit pricing.

Photoroom buying **Generate Banners** in May 2025 shows gen-AI photo players acquiring template-rendering capability.

### Cited Findings
- **Threekit Virtual Photographer**: "create tens of thousands of photorealistic 2D images from a few 3D files"; "generate lifestyle scenes… with AI"; a material library; tied to its product configurator [OFF] — [threekit.com/virtual-photographer](https://www.threekit.com/virtual-photographer)
- **Browzwear** (3D digital product creation / VStitcher) bought Lalaland.ai to integrate AI models into the 3D DPC workflow; the AI team joins its R&D on body-data accuracy and automated imagery [PRESS] — [FashionUnited](https://fashionunited.uk/news/business/browzwear-acquires-lalaland-ai/2025072583016); [Silicon Canals](https://siliconcanals.com/lalaland-ai-gets-acquired-by-browzwear)
- **Bannerbear** (template → image/video via REST API/MCP): Automate $49/mo (1K API credits plus 200 AI credits); Scale $149; Enterprise $299 for 50K credits [OFF] — [bannerbear.com/pricing](https://www.bannerbear.com/pricing/)
- **Placid**: "Dynamic design templates with dynamic data placeholders", Image/PDF/Video Automation APIs, an **MCP** to "connect AI agents to your templates", and an embeddable Editor SDK [OFF] — [placid.app/pricing](https://placid.app/pricing)
- **Creatopy → The Brief**: HTML5/AMP export, ad serving to 25+ networks, edit 100 ads at once, AI resize [OFF] — [creatopy.com](https://www.creatopy.com/)
- **Marpipe**: feed-driven catalog templates (DPA overlays, countdowns, product-level video) on Meta, TikTok, Snap, Reddit and Pinterest catalogs [OFF] — [marpipe.com/pricing](https://www.marpipe.com/pricing)
- **Photoroom** acquired Generate Banners on 2025-05-22 [EST] — [Tracxn](https://tracxn.com/d/companies/photoroom/__3Eb7XKd5tPi6IJQFKmZrfp2xHmMSn4DH7M3WdkToYPY)
- **Hexa** (hexa3d.io) and **CGTrader** modeling services: pages are JS-rendered and no text could be retrieved. Unverified this round.

### Inferences
- The emerging stack has three layers:
  1. **Exact SKU geometry** from 3D, or a trained "product digital twin" (万相营造, Flair, Caimera)
  2. **Gen-AI scene and model** generation
  3. **Template/code rendering** for text, price, legal copy and format variants (Bannerbear, Placid, catalog overlays)
- MCP endpoints on template APIs (Placid, Bannerbear) make them callable by ad agents (Amazon Creative Agent, TikTok Symphony Agent). This is the natural slot for HTML/code-to-ad pipelines.

### Gaps
- No revenue or traction for Bannerbear, Placid or Hexa.
- No market sizing for CGI packshots.
- Figma/HTML-to-ad pipelines: no sourced adoption data.

## Q7. How ad platforms and marketplaces embed it

### Takeaway
Every major ad platform and marketplace now ships free gen-image tools inside the buying or listing flow. Each has moved from a "generate button" (2023) to an "agent" (2026):
- Google Product Studio → Asset Studio
- Amazon Image Generator (2023) → Creative Agent (Feb 2026, UK/EU) → Ads Agent (unBoxed 2026)
- Meta Advantage+ creative → Muse Image
- Shopify Magic
- Adobe GenStudio for Commerce Media Networks (retail media)
- 阿里 万相营造/绘蛙 (round 1)

### Cited Findings
- **Google Product Studio** (May 2023): inside Merchant Center Next; scene generation, background removal, upscaling; "for free"; also via the Google & YouTube app for Shopify [OFF] — [Google blog](https://blog.google/products/shopping/google-product-studio-generative-ai-product-photos/)
  - For 2026 Asset Studio and Gemini adoption (about 70M assets in Q4 2025), see round 1.
- **Amazon Ads**
  - Image Generator beta (Oct 2023): select a product in the Ad Console, then Generate. Free [PRESS] — [Search Engine Journal](https://searchenginejournal.com/amazon-introduces-generative-ai-image-tool-for-advertisers/499439)
  - **Creative Agent** (2026-02-24): UK, FR, DE, IT and ES; research → storyboard → images, video, voiceover; formats for DSP, Sponsored Display/Brands, STV and Brand Stores; built on Bedrock (Nova, Claude); "no additional cost". **No adoption numbers disclosed** [OFF] — [About Amazon EU](https://www.aboutamazon.eu/news/innovation/amazon-ads-launches-creative-agent-new-agentic-ai-tool-that-creates-professional-quality-ads)
  - unBoxed 2026: creative tools fold into the conversational Amazon Ads Agent [OFF] — [Amazon Ads unBoxed 2026](https://advertising.amazon.com/library/news/unboxed-2026-news-announcements); [MediaPost 2026-09-29](https://www.mediapost.com/publications/article/418323/amazon-reboots-ad-business-emphasizes-agentic.html)
- **Shopify Magic**: background removal and replacement with a solid colour or an AI-generated scene (preset or custom prompt), inside the admin [OFF] — [Shopify help](https://help.shopify.com/en/manual/shopify-admin/productivity-tools/shopify-magic)
  - **No usage numbers found.**
- **Meta**: Muse Image (in-house model, #2 on the Arena per Meta) is to power Advantage+ image generation (Jul 2026) [OFF via secondary] — [Digital Applied](https://www.digitalapplied.com/blog/meta-muse-image-video-paid-social-creative-2026)
  - Licensing deal with Midjourney (Aug 2025) [EST] — [Sacra](https://sacra.com/c/midjourney/)
  - Adoption counts (8–9M advertisers/SMBs): round 1
  - Marpipe gets **Meta-subsidized** pricing for qualified brands: Meta pays third-party creative tools to enrich catalogs [OFF] — [marpipe.com](https://www.marpipe.com/pricing)
- **Adobe**: GenStudio for Commerce Media Networks lets retailers offer self-serve creative to their advertisers [OFF] — [Adobe Q3 FY26 transcript](https://www.fool.com/earnings/call-transcripts/2026/09/11/adobe-adbe-q3-2026-earnings-call-transcript/)

### Inferences
- Platform tools set the price floor at zero for SMBs. Independents survive via:
  - (a) multi-platform output, since a seller lists on Amazon, Shopify, TikTok and Shopee at once
  - (b) brand control and digital twins
  - (c) being subsidized or partnered by the platform (Marpipe–Meta)
  - (d) API/OEM to marketplaces (Photoroom–Wolt/Depop)
- Retail media networks (Amazon, Walmart via Adobe GenStudio for CMN, 阿里妈妈) are the next embedding point, where creative generation is sold to the retailer, not the brand.

### Gaps
- No usage counts for Google Product Studio, Shopify Magic or Amazon image generation.
- No info on Walmart Connect, Instacart or Pinterest gen-AI image tools (searches unavailable).

