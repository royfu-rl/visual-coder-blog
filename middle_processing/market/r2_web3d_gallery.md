# Commercial Web 3D: verified showcase gallery and who pays (round 2, as of 2026-10-13)

Method and tags
- About 90 tool calls. The web-search budget ran out after 5 searches, so almost everything below comes from **direct fetches of primary pages**: awwwards.com site pages and hall of fame, studio sites, vendor pricing pages, the npm registry API, GitHub, and caniuse.
- **URL verification.** Every gallery URL was checked on 2026-10-13 with `curl -L` (HTTP status recorded). "200" means the page is live. JS-only pages may still render empty to a bot.
- **Tech fingerprints.** Where a page loads three.js, I grepped its HTML and first-party JS bundles for `THREE.WebGLRenderer` and `REVISION` strings. These are tagged **[fp]**. They only show what is bundled on the landing page, which is a lower bound.
- **Source-type tags:**
  - **[award]** awwwards.com primary page
  - **[site]** the studio's or brand's own page
  - **[data]** registry or API numbers
  - **[vendor]** a vendor or agency blog with a commercial interest
  - **[wiki]** Wikipedia, which cites secondary press
- This round does not repeat Round 1 (`web3d_engines.md`). It fixes Round 1's unverified SOTY 2025 claims, which are now confirmed.

## Q1. Verified gallery of standout public web-3D work (2022–2026)

### Takeaway
Awwwards annual winners for 2022–2025 are now confirmed from Awwwards' own hall of fame:
- **2025:** Lando Norris (OFF+BRAND) won Site of the Year (SOTY); Messenger (abeto) won Developer SOTY.
- **2024:** Igloo Inc (abeto) won both SOTY and Developer SOTY.
- **2023:** Lusion v3 won both.
- **2022:** KPR (Resn) won SOTY; Persepolis Reimagined (Monks/Getty) won Developer SOTY.

The 2026 Sites of the Month show three.js work concentrating in a few studios: Lusion, Immersive Garden, Resn, Unseen and abeto. Brand clients include Shopify, Cartier, Audemars Piguet/GQ, Getty and Lacoste. Big brands and agencies still mostly ship WebGL builds of three.js (r148 to r185 in fingerprints). Only Bruno Simon's 2026 portfolio and Utsubo's IVRESS are documented WebGPU/TSL builds.

### Cited Findings

**A. Awwwards annual winners (from Awwwards hall of fame pages, fetched 2026-10-13) [award]**
- **2025:**
  - Site of the Year: Lando Norris (43 jury votes)
  - Developer SOTY: Messenger (54)
  - E-commerce of the Year: Scout Motors
  - Agency of the Year: Immersive Garden
  - Studio of the Year: Malvah
  - Independent of the Year: Louis Paquet
  - SOTY Users' Choice: Lando Norris (596 votes)
  - Source: [Awwwards winners](https://www.awwwards.com/annual-awards/winners); [Hall of fame](https://www.awwwards.com/annual-awards/hall-of-fame)
- **2024:**
  - SOTY and Developer SOTY: Igloo Inc
  - E-commerce: Opal Tadpole
  - Agency: Locomotive
  - Studio: Immersive Garden
  - Independent: Jesper Landberg
  - Users' Choice: Don't Board Me
  - Source: [Awwwards hall of fame 2024](https://www.awwwards.com/annual-awards/hall-of-fame/2024)
- **2023:**
  - SOTY and Developer SOTY: Lusion v3
  - E-commerce: Mana Yerba Mate
  - Agency: Locomotive
  - Studio: Obys
  - Independent: Aristide Benoist
  - Users' Choice: Noomo Agency
  - Source: [Hall of fame 2023](https://www.awwwards.com/annual-awards/hall-of-fame/2023)
- **2022:**
  - SOTY: KPR
  - Developer SOTY: Persepolis Reimagined
  - E-commerce: Mr. Pops
  - Agency: Locomotive
  - Studio: Synchronized Studio
  - Independent: Jesper Landberg
  - Users' Choice: The Other Side of Truth
  - Source: [Hall of fame 2022](https://www.awwwards.com/annual-awards/hall-of-fame/2022)
- Caveat: the hall-of-fame pages don't print the year label in their text. The year comes from the URL path. It matches the year column on the [Sites of the Year listing](https://www.awwwards.com/websites/sites_of_the_year/), which also lists earlier winners (2017–2021).
- The 2026 annual awards are not yet decided. Awwwards normally announces them in early 2027.

**B. The gallery (54 entries, all URLs checked live on 2026-10-13 unless noted)**

Column key: SOTD = Site of the Day; SOTM = Site of the Month; Dev = Developer Award. A "self" client means the studio's own site.

| # | Work | URL (status) | Studio | Client | Year | Award (source) | Tech (source) |
|---|---|---|---|---|---|---|---|
| 1 | Lando Norris official site | https://landonorris.com/ (200) | OFF+BRAND. | Lando Norris (McLaren F1) | 2025 | SOTD 17 Nov 2025 (8.18); **SOTY 2025 + Users' Choice 2025** [award](https://www.awwwards.com/sites/lando-norris) | WebGL, GSAP, Webflow, 3D [award]; three.js `REVISION 174` bundled [fp]; Webflow CDN and Rive [site] |
| 2 | Messenger (tiny multiplayer planet) | https://messenger.abeto.co (200) | abeto | self/experiment | 2025 | SOTD 10 Nov 2025; Dev 8.21; **Developer SOTY 2025** [award](https://www.awwwards.com/sites/messenger) | Three.js, WebGL, WebSockets [award] |
| 3 | Igloo Inc | https://www.igloo.inc/ (200) | abeto + Bureaux | Igloo Inc (parent of Pudgy Penguins) | 2024 | SOTD 23 Jul 2024; **SOTY 2024 + Dev SOTY 2024** [award](https://www.awwwards.com/sites/igloo-inc) | Three.js, three-mesh-bvh, Svelte, GSAP, Vite, Houdini/Blender, a VDB volume-to-browser exporter, procedural ice [award case study](https://www.awwwards.com/igloo-inc-case-study.html) |
| 4 | Don't Board Me | https://dontboardme.com (200) | The First The Last | n/s | 2024 | SOTD 11 Mar 2024; **Users' Choice 2024** [award](https://www.awwwards.com/sites/dont-board-me) | Scrolling/storytelling (no 3D tag) |
| 5 | Opal Tadpole | https://www.opalcamera.com/opal-tadpole (200, now redirects to op.al) | Claudio Guglieri (design), Ingamana (dev) | Opal Camera | 2024 | SOTD 11 Jan 2024; **E-commerce of the Year 2024** [award](https://www.awwwards.com/sites/opal-tadpole) | 3D, e-commerce product page |
| 6 | Lusion v3 | https://lusion.co/ (200) | Lusion (Bristol) | self | 2023 | SOTD 2 Oct 2023 (Dev 8.41; Animations 10.0); **SOTY + Dev SOTY 2023** [award](https://www.awwwards.com/sites/lusion-v3) | three.js `REVISION="158"` [fp] |
| 7 | Noomo Agency | https://noomoagency.com (200) | Noomo | self | 2023 | **Users' Choice 2023** [award](https://www.awwwards.com/annual-awards/hall-of-fame/2023) | n/v |
| 8 | Mana Yerba Mate | https://en.manayerbamate.com/ (200) | Louis Paquet | Mana | 2023 | **E-commerce of the Year 2023** [award](https://www.awwwards.com/annual-awards/hall-of-fame/2023) | n/v |
| 9 | KPR | https://kprverse.com/ (200) | Resn | KPR (Web3 collectibles) | 2022 | SOTD 26 Dec 2022; **SOTY 2022** [award](https://www.awwwards.com/sites/kpr) | `three.module` imported [fp] |
| 10 | Persepolis Reimagined | http://www.getty.edu/persepolis (200, now persepolis.getty.edu) | Monks | Getty | 2022 | SOTD 1 Jun 2022; **Dev SOTY 2022** [award](https://www.awwwards.com/sites/persepolis-reimagined) | WebGL, GSAP, Vue.js, 360 [award] |
| 11 | The Other Side of Truth | https://theothersideoftruth.com (200) | The First The Last | n/s | 2022 | **Users' Choice 2022** [award](https://www.awwwards.com/annual-awards/hall-of-fame/2022) | n/v |
| 12 | Bruno Simon portfolio (2026 rebuild) | https://bruno-simon.com (200) | Bruno Simon | self | 2026 (case study 11 Mar 2026; just over a year of work) | **SOTM Jan 2026** [award](https://www.awwwards.com/websites/sites_of_the_month/); the 2019 version was SOTY 2019 [award](https://www.awwwards.com/websites/sites_of_the_year/) | three.js + TSL, uses WebGPU when available and falls back to WebGL; world built in Blender; Rapier physics, Howler; DRACO and KTX (ETC1S/UASTC); about 78,400 single-triangle grass blades; MIT code, CC0 music; multiplayer "whispers" moderated by the OpenAI moderation model [award case study](https://www.awwwards.com/brunos-portfolio-case-study.html); [site](https://bruno-simon.com/) |
| 13 | Oryzo AI (spoof AI-coaster launch) | https://oryzo.ai (200) | Lusion | self (fictional product) | 2026 | SOTD 13 Apr 2026 + Dev; **SOTM Apr 2026** [award](https://www.awwwards.com/sites/oryzo-ai) | Three.js, WebGL, GSAP [award]; `REVISION="178 - modified by Lusion"` [fp] |
| 14 | EverSwap | https://everswap.com/ (200) | Lusion | EverSwap (startup) | 2026 | SOTD 22 Jun 2026 [award](https://www.awwwards.com/sites/everswap) | WebGL, Blender |
| 15 | Shopify Editions Winter '26 "The Renaissance Edition" | https://www.shopify.com/editions/winter2026 (200) | Shopify Design (in-house) | Shopify | 2026 | SOTD 9 Feb 2026 (Dev 8.05); **SOTM Feb 2026** [award](https://www.awwwards.com/sites/the-renaissance-edition) | WebGL, Blender; presents 150+ product updates [award] |
| 16 | Shopify Editions Summer '25 "Drive" | https://www.shopify.com/ca/editions/summer2025/drive (200) | Shopify | Shopify | 2025 | Listed on the three.js showcase [site](https://threejs.org/) | three.js |
| 17 | Shopify BFCM live globe | https://bfcm.shopify.com/ (200, now /2025/) | Shopify | Shopify | 2025 | three.js showcase [site](https://threejs.org/) | three.js |
| 18 | GQ & AP "The Extraordinary Lab" | https://www.gq.com/sponsored/story/the-extraordinary-lab (200) | Immersive Garden | Audemars Piguet (sponsored GQ story) | 2026 | SOTD 26 Mar 2026; **SOTM Mar 2026** [award](https://www.awwwards.com/sites/gq-ap-the-extraordinary-lab) | WebGL, Nuxt.js, Blender |
| 19 | Cartier Watches & Wonders 2025 | https://cartier-waw-0225.dev.60fps.fr/ (200) | Immersive Garden + 60fps | Cartier | 2025 | SOTD 18 Aug 2025; **SOTM Aug 2025** [award](https://www.awwwards.com/sites/cartier-watches-wonders-2025) | WebGL; the 2026 edition is vanilla three.js with GLSL, Lenis and Web Audio [vendor](https://www.utsubo.com/blog/best-threejs-websites-2026) |
| 20 | Montfort | https://mont-fort.com/ (200) | Immersive Garden | Montfort | 2025 | SOTD 23 Jun 2025; **SOTM Jun 2025** [award](https://www.awwwards.com/sites/montfort) | 3D, scrolling |
| 21 | David Whyte Experience | https://davidwhyte.com/experience/ (200) | Immersive Garden | David Whyte (poet) | 2024 | **SOTM Dec 2024** [award](https://www.awwwards.com/websites/sites_of_the_month/) | n/v |
| 22 | Immersive Garden website | https://immersive-g.com/ (200) | Immersive Garden (Paris) | self | 2025 | **SOTM Jan 2025** [award](https://www.awwwards.com/websites/sites_of_the_month/) | three.js `"170"` and WebGLRenderer [fp]; also lists work for Louis Vuitton VIA, Cartier, Longines, OMEGA, Dioriviera [site](https://immersive-g.com/) |
| 23 | Tracing Art | https://www.getty.edu/tracingart/ (200) | Resn | Getty | 2025 | SOTD 22 Jul 2025; **SOTM Jul 2025** [award](https://www.awwwards.com/sites/tracing-art) | Data visualization, scrolling |
| 24 | Zentry | https://zentry.com/ (200) | Resn | Zentry (gaming/Web3) | 2024 | **SOTM Aug 2024** [award](https://www.awwwards.com/websites/sites_of_the_month/) | `three.module` [fp] |
| 25 | Slosh Seltzer | https://sloshseltzer.com/ (200) | Active Theory | Slosh | 2024 | **SOTM Jun 2024** [award](https://www.awwwards.com/websites/sites_of_the_month/) | No three.js signature [fp]. This fits Active Theory's in-house "Hydra" engine (Round 1, [vendor](https://www.psychoactive.co.nz/content-hub/best-webgl-interactive-3d-agencies)) |
| 26 | Ponpon Mania | https://ponpon-mania.com/ (200) | Patrick Heng | self | 2025 | SOTD 22 Oct 2025; **SOTM Oct 2025** [award](https://www.awwwards.com/sites/ponpon-mania) | WebGL, GSAP, Nuxt.js |
| 27 | Why Zero | https://why.zero.university/ (200) | Sindhur Dutta + Zero | Zero (edu startup) | 2026 | SOTD 7 Sep 2026; **SOTM Sep 2026** [award](https://www.awwwards.com/sites/why-zero) | Three.js, GSAP, Blender [award]; glb models [fp] |
| 28 | Hubtown | https://hubtown.co.in/ (200) | Unseen Studio (Bristol/London) | Hubtown (Indian real estate) | 2026 | SOTD 10 Jun 2026 [award](https://www.awwwards.com/sites/hubtown) | WebGL, GSAP |
| 29 | IVRESS brand site | https://brand.ivress.co.jp (200) | Utsubo (Osaka) | IVRESS | 2026 | FWA SOTM May 2026 (claimed by the studio itself) [vendor](https://www.utsubo.com/blog/best-threejs-websites-2026) | **WebGPURenderer + TSL with WebGL fallback**. This is the only agency brand site documented as WebGPU-first |
| 30 | Lacoste Ace Breaker (Roland-Garros game) | https://members-play.lacoste.com/ace-breaker-rg/gb/en/ (200) | n/s | Lacoste | 2026 | Awwwards nominee [vendor](https://www.utsubo.com/blog/best-threejs-websites-2026) | three.js/WebGL brick-breaker |
| 31 | Lacoste Members Experience "Create" | https://membersexperience-create.lacoste.com/ (200) | n/s (Merci-Michel lists Lacoste work in 2022 and 2024 [site](https://www.merci-michel.com/)) | Lacoste | 2022–24 | Featured on the three.js homepage [site](https://threejs.org/) | WebGL |
| 32 | Montblanc "The Run" | https://therun.montblanclegend.com/ (200) | n/s | Montblanc | n/d | three.js showcase [site](https://threejs.org/) | three.js |
| 33 | SpaceX ISS Docking Simulator | https://iss-sim.spacex.com/ (200) | SpaceX | SpaceX | 2020 | three.js showcase [site](https://threejs.org/) | three.js `REVISION="112"` [fp] |
| 34 | NASA Eyes on the Solar System | https://eyes.nasa.gov/apps/solar-system/ (200) | NASA/JPL | NASA | ongoing | three.js showcase [site](https://threejs.org/) | three.js r185-era bundle, WebGLRenderer [fp] |
| 35 | Choo Choo World | https://choochooworld.com/ (200) | Lusion | self/game | n/d | Lusion portfolio [site](https://lusion.co/) | three.js `REVISION="148"` [fp] |
| 36 | Meta "Spatial Fusion" | https://spatialfusion.io/ (200) | Lusion | Meta | n/d | Lusion portfolio [site](https://lusion.co/) | three.js `"145dev"` [fp] |
| 37 | Kode Sports Club | https://www.kodeclubs.com/ (200) | Merci-Michel | Kode (New Cairo) | 2020 | **SOTY 2020** (one of that year's SOTY winners) [award](https://www.awwwards.com/websites/sites_of_the_year/) | three.js showcase [site](https://threejs.org/) |
| 38 | Coastal World | https://coastalworld.merci-michel.com/ (200) | Merci-Michel | Coastal (bank) | 2022 | three.js showcase [site](https://threejs.org/); client year from [site](https://www.merci-michel.com/) | three.js |
| 39 | Blobmixer | https://blobmixer.14islands.com/ (200) | 14islands (Stockholm/Reykjavík) | self | n/d | three.js showcase [site](https://threejs.org/) | three.js / R3F (R3F not verified) |
| 40 | Daimaru Matsuzakaya VI site | https://www.daimaru-matsuzakaya.com/vi/ (200) | n/s | Daimaru Matsuzakaya (dept. store) | 2025 (assets rev. 2025-12-18) | three.js showcase [site](https://threejs.org/) | three.js WebGLRenderer [fp] |
| 41 | Apple AirPods Pro product page | https://www.apple.com/airpods-pro/ (200) | Apple in-house | Apple | 2025 assets | n/a | Loads **`/ac/libs/three/92/three.min.js`** (three.js r92) plus a USDZ for AR Quick Look [fp]. So Apple's scroll-driven product pages do use three.js for some 3D moments, alongside image sequences and video |
| 42 | Xiaomi SU7 product page (小米 SU7) | https://www.xiaomiev.com/su7 (200) | Xiaomi in-house/agency n/s | Xiaomi EV | 2024– | n/a | three.js `THREE.WebGLRenderer` bundled; revision hints "155"/"169" [fp] |
| 43 | Porsche Car Configurator | https://configurator.porsche.com/porsche-code/en-US (200) | n/s | Porsche | live | n/a | Exists; the renderer was not identified from the initial HTML [fp] |
| 44 | Porsche real-time render app (demo) | https://dyadstudios.com/renderapp/porsche/ (200) | Dyad Studios | Porsche (demo) | n/d | three.js showcase [site](https://threejs.org/) | three.js |
| 45 | Nike By You | https://www.nike.com/nike-by-you (200) | Nike | Nike | live | n/a | Page exists; no 3D tech is mentioned on the landing page [site](https://www.nike.com/nike-by-you) |
| 46 | Google Earth (web) | https://earth.google.com/web/ (200) | Google | Google | live | n/a | Shows "Launch Wasm Multiple/Single Threaded" options [site](https://earth.google.com/web/) |
| 47 | SuperSplat (splat hub + editor) | https://superspl.at/ (200) | PlayCanvas | self | 2024–26 | n/a | Editor 3.0 "rebuilt on WebGPU" (Sep 9 2026); streamed LOD; Publishing API (Aug 2026) [site](https://superspl.at/); [PlayCanvas blog](https://blog.playcanvas.com/) |
| 48 | Grace Cathedral Experience | (PlayCanvas blog, 20 Jul 2026; URL not checked) | PlayCanvas | Grace Cathedral, SF (capture by Vincent Woo) | 2026 | n/a | Gaussian splat app on PlayCanvas [PlayCanvas blog](https://blog.playcanvas.com/) |
| 49 | Polytrack (web racing game) | https://www.kodub.com/apps/polytrack (200) | Kodub | self | n/d | three.js showcase [site](https://threejs.org/) | three.js |
| 50 | Krunker.io (web FPS) | https://krunker.io/ (200) | Yendis/now FRVR (ownership not verified this round) | self | 2018– | three.js showcase [site](https://threejs.org/) | three.js-based |
| 51 | Merci-Michel "no." | https://no.merci-michel.com/ (200) | Merci-Michel | self | n/d | three.js showcase [site](https://threejs.org/) | three.js |
| 52 | Funtech experience 2026 | https://experience2026.funtech.inc/ (200) | Funtech (JP) | self | 2026 | First entry on the three.js homepage [site](https://threejs.org/) | WebGL2; probes `navigator.gpu` [fp] |
| 53 | Wind Waker three.js tribute | https://wind-waker-threejs.com/ (200) | indie | — | n/d | three.js showcase [site](https://threejs.org/) | three.js |
| 54 | AI-made demos on the official showcase | https://claude.ai/artifact/N1cRTZqiUZyxDVP7dJGTau (200); https://whiteout.plgb.chatgpt.site (200) | users of Claude / ChatGPT | — | 2026 | The three.js homepage showcase now links a Claude artifact (item #3 of 244) and a chatgpt.site page (#8) [site](https://threejs.org/) | three.js |

Other 2026 Awwwards SOTMs. All URLs return 200; their 3D content was not checked.
- Lama Lama (Jul 2026), https://lamalama.com/
- ERA Residence by The First The Last (Aug 2026), https://www.era-residence.com/
- Son Daven by The First The Last (Jun 2026), https://sondaven.com/en
- Floema by Bürocratik (May 2026), https://www.floema.com/en
- MindMarket by Louis Paquet (Dec 2025), https://mindmarket.com/
- Source: [award](https://www.awwwards.com/websites/sites_of_the_month/)

**C. Studio roster: existence and client facts from their own sites [site]**
- **Lusion** (Bristol, UK; "3D and Interactive Web Studio")
  - Portfolio: Oryzo AI, Atlas Motion, Devin AI, Of The Oak, EverSwap, Porsche "Dream Machine", Synthetic Human, Meta "Spatial Fusion", Spaace, DDD 2024, Choo Choo World, Soda AR — [lusion.co](https://lusion.co/)
- **Immersive Garden** (Paris)
  - Clients: Louis Vuitton (VIA), Cartier (several), Longines, OMEGA, Dioriviera, Orano, Girard-Perregaux, Masar — [immersive-g.com](https://immersive-g.com/)
  - Awwwards Agency of the Year 2025 and Studio of the Year 2024 [award](https://www.awwwards.com/annual-awards/winners)
- **14islands** (Stockholm, Reykjavík)
  - Clients: Cartier, Neko Health, Breakthrough Energy, UNDP Sweden, Google Interland, PolyAI, Antler — [14islands.com](https://14islands.com/)
- **Merci-Michel** (France)
  - Clients: Lacoste (2022, 2024), Red Bull, Boucheron, Cartier (2023), KPR (2024), Miu Miu, Kenzo, Play-Doh/Hasbro, Volkswagen — [merci-michel.com](https://www.merci-michel.com/)
- **Dogstudio** (Belgium and Chicago)
  - Clients: Tomorrowland, Navy Pier, MSI Chicago, Kennedy Center, Microsoft
  - Its cookie notice links to deptagency.com, which suggests DEPT ownership but is not confirmed — [dogstudio.co](https://dogstudio.co/)
- **Unseen Studio:** Bristol and London — [unseen.co](https://unseen.co/)
- **Garden Eight:** Tokyo — [garden-eight.com](https://garden-eight.com/)
- **Active Theory and Resn:** the sites are live (200) but render via JS only, so no detail could be extracted — [activetheory.net](https://activetheory.net/), [resn.co.nz](https://resn.co.nz/)
- **Locomotive:** Awwwards Agency of the Year in 2022, 2023 and 2024 [award](https://www.awwwards.com/annual-awards/hall-of-fame/2024)

**D. China**
- **Xiaomi SU7:** the product page bundles three.js (see row 42) [fp].
- **NIO ES8** (https://www.nio.cn/es8, 200) and **Huawei Mate X7** (https://consumer.huawei.com/cn/phones/mate-x7/, 200): both pages are live, but neither showed a three.js, Babylon or Galacean signature in its initial HTML or scripts [fp].
- **Galacean (Ant Group, formerly Oasis):**
  - Engine: "a typescript interactive engine… 2D, 3D, animation, physics, built on WebGL and glTF"; MIT; 5.9k GitHub stars; WebGL/WebGL2 listed, WebGPU not mentioned — [GitHub](https://github.com/galacean/engine)
  - Docs: v1.6; exports to H5 and WeChat Mini Games — [docs](https://galacean.antgroup.com/engine/docs/)
  - Effects runtime: 748 stars — [GitHub](https://github.com/galacean/effects-runtime)
  - npm `@galacean/engine`: ~10.4k downloads in Sep 2026 [data](https://api.npmjs.org/downloads/point/2026-09-01:2026-09-30/@galacean/engine)

### Inferences
- Award-winning web 3D is still mostly **vanilla three.js on WebGL**, built by fewer than ~10 studios. Fingerprints span r145 to r185, and no award site in the sample bundled `WebGPURenderer` as its primary path except the IVRESS vendor claim. WebGPU is a portfolio flex (Bruno Simon, SuperSplat) rather than the client default.
- Active Theory's builds show no three.js signature, which fits its proprietary engine. Agencies with in-house engines are the exception.
- Self-promotional and spec work wins a large share of the top awards. Of the SOTY and Developer SOTY winners above, Lusion v3, Messenger, Bruno Simon and Oryzo are studio self-promotion (Oryzo is a fictional product). The paying-client winners are Igloo (Web3 brand), Lando Norris (athlete brand), KPR (Web3) and Getty (museum). The award circuit works mainly as agency marketing.
- Brand money for web 3D in 2024–26 comes from luxury (Cartier, AP, LV, Montblanc, Lacoste), Shopify's in-house team, Web3/crypto (Igloo/Pudgy, KPR, Zentry), and athlete/celebrity sites.
- AI-generated three.js now appears on the official showcase (a Claude artifact and a chatgpt.site page), and npm growth (Q3) points the same way. LLMs have become a three.js distribution channel.

### Gaps
- **FWA:** thefwa.com renders by JS and returned only a title, so no FWA of the Year or Month list was verified. The one FWA claim (IVRESS) comes from the studio itself.
- **Codrops and the three.js forum showcase:** both returned 403 or Cloudflare blocks to the fetcher and the API. Not covered.
- **Missing site pages:** no live pages were retrieved for Louis Vuitton VIA, Prada, Nike 3D (Nike By You has no 3D evidence), the Tesla configurator (403), the Cartier.com pages (403), slowroads.io (403), the Gucci 1955 Horsebit page (connection failure), or Kubota Future Cube (404). Those are excluded as unverified.
- **China:** no primary sources were found for 天猫 3D, 网易 Web3D cases, or Alipay campaigns built on Galacean. The search budget was exhausted.
- **Spline community and Needle showcase:** spline.design/community returned 404. Needle's homepage names logos (The Met, Google, Autodesk, Unity, Khronos) but no verified project URLs [site](https://needle.tools/).

## Q2. Economics: who pays, and how much

### Takeaway
There are four ways money flows into web 3D:
1. **Bespoke agency builds.** Agencies publish planning ranges from about $20k to $200k+. The top studios set Clutch minimums of $25k–50k+ and rates of $100–199/hr, and run 10–49 staff.
2. **Configurator and viewer SaaS.** This is polarized:
   - Self-serve tools are $15–$300/mo (Zakeke also takes a 1.5–1.9% transaction fee).
   - Enterprise configurators (Threekit, Expivi) are quote-only.
3. **Tool SaaS.** Spline is $12–70/seat/mo; PlayCanvas is $15–50/seat/mo; Needle requires a paid Pro plan for commercial use.
4. **Web game portals.** This is by far the largest audience. Poki has about 100M monthly players and 1B+ gameplays/month; CrazyGames claims 31–60M. Both are ad-funded and accept three.js, Babylon and PlayCanvas builds.

### Cited Findings

**Agency build prices**
- **Utsubo planning ranges** for an interactive launch site [vendor] — [Utsubo](https://www.utsubo.com/blog/interactive-website-vs-video-launch-budget):
  - Video-led landing page: $10k–15k
  - Interactive product story (scroll-driven 3D product moment): $20k–60k
  - Product experience or configurator (WebGL/WebGPU): $60k–120k
- **Utsubo retail ranges** [vendor] — [Utsubo](https://www.utsubo.com/blog/interactive-retail-web-experience-guide):
  - One interactive product moment: $20k–50k
  - Integrated interactive retail: $50k–100k
  - Full shoppable brand world: $100k–200k+
  - Custom 3D/WebGL adds $15k–80k
  - Multilingual adds 30–50% per language
- **Flagship WebGL builds** run "upwards of US$100,000," according to an agency that ranks itself in the same list [vendor] — [Psychoactive](https://www.psychoactive.co.nz/content-hub/best-webgl-interactive-3d-agencies)
- **Clutch profiles** (self-reported) [site]:
  - Active Theory: min project $25k+, $150–199/hr, founded 2012, LA HQ. Headcount is inconsistent on the profile (2–9 vs 10–15) — [Clutch](https://clutch.co/profile/active-theory)
  - 14islands: min $25k+, $100–149/hr, 10–49 staff — [Clutch](https://clutch.co/profile/14islands)
  - Locomotive: min $50k+, $150–199/hr, 10–49 staff (HQ listing says 21–30), founded 2006. Reviewed project budgets span $10k–49k up to one $200k–999k SaaS site (Jan–Oct 2026); most common size is $10k–49k (7 reviews) — [Clutch](https://clutch.co/profile/locomotive)
  - Immersive Garden: 10–49 staff (Paris HQ 10–15), founded 2014, no rates listed — [Clutch](https://clutch.co/profile/immersive-garden)
  - Dogstudio: 10–49 staff, founded 2006 — [Clutch](https://clutch.co/profile/dogstudio)
- The Awwwards-adjacent client mix (luxury, Shopify, Web3, athletes) is listed in Q1 [award](https://www.awwwards.com/websites/sites_of_the_month/)

**Configurator, viewer and 3D platform SaaS**
- **Zakeke** [site] — [Zakeke pricing](https://admin.zakeke.com/en-US/pricing):

  | Plan | Monthly ($/mo) | Annual ($/mo) | Products | Transaction fee |
  |---|---|---|---|---|
  | Starter | 69.90 | 59 | 10 | 1.9% |
  | Grow | 129.90 | 110 | 50 | 1.7% |
  | Scale | 299.90 | 255 | 100 | 1.5% |
  | Enterprise | custom | custom | custom | listed as 0% |

  - Add-ons: Virtual Try-On from $40, 3D DAM/AR Viewer Pro $29.90
  - This corrects Round 1's "from ~$29/mo"
- **Threekit:** no public prices ("Pricing is custom and varies based on your specific use case") — [Threekit](https://www.threekit.com/pricing)
- **Expivi:** no public prices; pricing comes after a demo, framed around payback. A "Core" CPQ is always included, with Visualization, Modular and Design-to-Print add-ons — [Expivi](https://expivi.com/pricing/)
- **Vectary:** Free / Starter / Team / Business tiers with credit-based GenAI (3,000 or 40,000 credits); paid "Distribution" add-on for public configurators. Prices did not render in the fetch — [Vectary](https://www.vectary.com/pricing/)
- **Sketchfab:** Basic free; Pro $15/mo billed yearly ($180); Enterprise custom — [Sketchfab](https://sketchfab.com/plans)
- **Spline** [site] — [Spline pricing](https://spline.design/pricing):
  - Free
  - Hobby $15/mo ($12/mo yearly), 2k AI credits
  - Pro $30 ($25), 3k credits
  - Max $70 ($60), 10k credits
  - Enterprise custom (SSO, team library)
  - Funding from Round 1: $15M seed (2023) and $10M Series A (Aug 2024)
- **PlayCanvas:** Free (public projects, 1GB); Personal $15/mo; Organization $50/seat/mo — [PlayCanvas](https://playcanvas.com/plans)
- **Needle:** "Free for personal projects. A Pro plan is required for commercial use" (removes watermark). The prices page returned 404 — [Needle](https://needle.tools/)

**Web game portals (the largest web-3D audience)**
- **Poki** [site] — [Poki for developers](https://developers.poki.com/):
  - "100 million" monthly players, "over 1 billion" gameplays per month
  - 500+ developers; high-performing games reach 5M+ monthly players
- **Poki background** [wiki] — [Wikipedia](https://en.wikipedia.org/wiki/Poki_(website)):
  - Founded 2014 in Amsterdam by Sebastiaan Moeys and Michiel van Amerongen
  - Ad-funded; Bloomberg (7 Nov 2025) reports ~100M MAU and that Poki takes more than the typical 30% app-store cut
  - MCV/Develop (10 Aug 2026, citing Ahrefs) estimates ~122.5M monthly visits, up ~569% over five years
- **CrazyGames** [wiki] — [Wikipedia](https://en.wikipedia.org/wiki/CrazyGames):
  - Founded 2014 in Leuven
  - Grew from 37 to 47 employees in late 2025
  - Smartfin invested more than €10M (late 2025, per De Tijd/Fortune)
  - Revenue from programmatic ads plus in-game purchases via Xsolla
  - "31 million users per month"
- **CrazyGames, own sites** [site]:
  - Its own site claims "60 million players" — [CrazyGames about](https://about.crazygames.com/) (conflicts with the 31M on Wikipedia; likely a different metric or date)
  - Supported engines: Unity, three.js, Babylon, PlayCanvas, Godot — [CrazyGames developer](https://developer.crazygames.com/)
  - Technical limits: initial download ≤50MB, total ≤250MB — [CrazyGames docs](https://docs.crazygames.com/requirements/intro/)
- **Revenue:** neither portal discloses it. No primary figure was found.

### Inferences
- A realistic award-tier brand site ($100k–$500k) sits at the top of, or above, the published agency ranges. The only evidence above $200k is one $200k–999k Locomotive review. Treat $500k builds as rare, not typical.
- Studio revenue can be roughly bounded: 10–49 staff at $100–199/hr implies about $2M–15M/yr per studio. This is my arithmetic, not a sourced figure.
- The configurator market splits cleanly:
  - SMB Shopify apps earn through monthly fees plus transaction fees (Zakeke).
  - Enterprise vendors (Threekit, Expivi) hide prices and sell on ROI.
- Web portals give web 3D its only mass-consumer business model, which is ads. They are engine-agnostic, and their size caps (50MB initial) favor light engines like three.js and PlayCanvas over Unity WebGL builds.

### Gaps
- Poki and CrazyGames revenue or developer payout totals: not disclosed in any fetched source. The search budget prevented finding press interviews.
- Threekit, Expivi and Needle actual prices; Needle and Threekit funding.
- Agency revenue: no verified revenue figure for any studio. Clutch shows only bands.

## Q3. Tech adoption: npm, WebGPU, Gaussian splats

### Takeaway
three.js npm downloads went from 3.4M/month (Sep 2022) to 11.0M (Sep 2025) to 70.2M (Sep 2026), about 21M/week now. That is a 6.4x rise in one year. npm as a whole also inflated (react rose 3.8x over the same window), so three.js's share relative to react rose from about 5.7% to 9.6%. The 2026 surge most plausibly comes from AI app builders and CI installs, not 6x more human developers. WebGPU now reaches about 86% of users (caniuse), but award sites still ship WebGL. Gaussian splats are mainstream on the web through PlayCanvas/SuperSplat (WebGPU) and World Labs' Spark for three.js (~229k downloads/week).

### Cited Findings

**npm downloads [data]**
Source: npm registry API (`api.npmjs.org/downloads/point|range`), fetched 2026-10-13. Values are September monthly totals.

| Package | Sep 2022 | Sep 2023 | Sep 2024 | Sep 2025 | Sep 2026 |
|---|---|---|---|---|---|
| three | 3.43M | 4.51M | 5.80M | 11.01M | **70.22M** |
| @react-three/fiber | 0.53M | 0.99M | 1.69M | 3.86M | 22.30M |
| @react-three/drei | 0.27M | 0.60M | 1.08M | 2.94M | 16.28M |
| @babylonjs/core | 0.091M | 0.145M | 0.170M | 0.346M | 1.50M |
| playcanvas | 6.1k | 9.5k | 17.6k | 66.4k | 332k |
| @splinetool/runtime | 0.091M | 0.398M | 0.565M | 0.582M | 2.51M |
| @needle-tools/engine | 0 | 4.4k | 5.6k | 22.8k | 15.2k |
| @galacean/engine | 0 | 2.7k | 1.6k | 2.9k | 10.4k |
| @mkkellogg/gaussian-splats-3d | — | — | — | — | 215k |

- Monthly three.js series (M):

  | Month | three.js (M) |
  |---|---|
  | Dec 2025 | 12.99 |
  | Jan 2026 | 17.10 |
  | Feb 2026 | 23.43 |
  | Mar 2026 | 35.85 |
  | Jun 2026 | 47.60 |
  | Aug 2026 | 61.10 |
  | Sep 2026 | 70.22 |

  The step-change began in Jan–Mar 2026.
- **Last 7 days (5–11 Oct 2026):**
  - three: 21.08M
  - R3F: 6.22M
  - Babylon core: 0.40M
  - playcanvas: 0.12M
  - @sparkjsdev/spark: 0.23M
  - gsap: 5.99M
- **Baselines, Sep 2025 → Sep 2026:**
  - react: 192M → 731M (3.8x)
  - vite: 162M → 748M (4.6x)
  - lodash: 320M → 697M (2.2x)
- **Ratios:**
  - three.js vs Babylon: about 47x in Sep 2026 (70.2M / 1.50M), versus ~32x in Sep 2025. Round 1's vendor claim of "270x Babylon" is not supported by these registry numbers.
  - three.js vs react: 5.7% in Sep 2025, 9.6% in Sep 2026.

**Releases and repo**
- three.js r186 is the latest release, with WebGPURenderer additions:
  - r186: `compileComputeAsync`, WebXR MSAA
  - r185: WebXR support in WebGPURenderer
  - r184: TSL compilation reported 3.0x faster
  - Release date conflicts: GitHub shows r186 on "24 Sep" — [GitHub releases](https://github.com/mrdoob/three.js/releases); Wikipedia says 8 Sep 2026 — [Wikipedia](https://en.wikipedia.org/wiki/Three.js)
- three.js repo: 116.3k stars, 36.6k forks — [GitHub](https://github.com/mrdoob/three.js)
- Wikipedia still calls WebGPU support "experimental" — [Wikipedia](https://en.wikipedia.org/wiki/Three.js)

**WebGPU reach**
- 87.82% of global users are on browsers with WebGPU (85.8% full + 2.02% partial) — [caniuse](https://caniuse.com/webgpu)
- caniuse lists Chrome from 113; Safari as *partial* in 26.x/27; Firefox as no listed full support. This Firefox status conflicts with Round 1's claim that WebGPU is in "all major browsers" and should be verified separately.

**Gaussian splats on the web**
- **PlayCanvas** [site] — [PlayCanvas blog](https://blog.playcanvas.com/):
  - SuperSplat WebGPU renderer and automatic streamed LOD (3 Jun 2026)
  - SuperSplat Editor 3.0 rebuilt on WebGPU (9 Sep 2026)
  - Publishing API with Varjo Teleport, XGRIDS LCC Studio and LichtFeld as partners (17 Aug 2026)
  - "Vibe Code Splat Apps" (9 Jul 2026)
  - SOG format open-sourced (2025)
  - Commercial case: Solaya phone-video 3D twins used by Karl Lagerfeld and Rimowa for e-commerce (6 Oct 2026)
- **Spark:** "an advanced 3D Gaussian Splatting renderer for THREE.js", built by World Labs, MIT, about 3.7k stars, v2.3.1 targets three@0.180 — [GitHub](https://github.com/sparkjsdev/spark)
- **Luma** web splat library is live — [Luma](https://lumalabs.ai/luma-web-library) (status 200; details not fetched)

### Inferences
- The 2026 three.js download curve is a better signal of **LLM-generated code defaulting to three.js/R3F** than of studio adoption. Evidence:
  - The download jump coincides with AI-built three.js entries appearing on the official showcase.
  - R3F and drei grew in step (≈5.8x).
  - Spline's runtime grew 4.3x, close to the npm-wide inflation, and Needle *declined*.
  This matters for a "visual coder" thesis: the default target for AI-written 3D on the web is three.js + R3F.
- WebGPU's ~86% reach means the remaining barrier is studio habit and three.js's "experimental" label, not browsers. Splats are the first web-3D workload to go WebGPU-first in production tooling (SuperSplat).

### Gaps
- No public data separates bot/CI npm downloads from human ones, so the AI-builder attribution is an inference.
- No source was found for the share of production sites using WebGPU (for example HTTP Archive or Web Almanac numbers). The search budget was exhausted.

