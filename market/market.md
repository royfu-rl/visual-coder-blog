# Market

<style>
.doc .mk-card{text-decoration:none;color:inherit}
.doc .mk-card .gal-poster{aspect-ratio:16/10}
.doc .mk-by{font-size:12px;color:var(--ink-soft);margin-top:-2px}
.doc .mk-tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:4px}
.doc .mk-tags span{font-size:11px;padding:2px 8px;border-radius:999px;line-height:1.5}
.doc .mk-heat{background:#fff4e5;color:#a35a00}
.doc .mk-biz{background:var(--bg-band);color:var(--ink-soft)}
.doc .mk-tech{background:#e8f0fe;color:#1a56b0}
.doc .mk-tags span:empty{display:none}
#doc-market .view-switch{max-width:100%;overflow-x:auto;scrollbar-width:none}
#doc-market .view-switch button{white-space:nowrap;padding:7px 14px;flex:none}
.doc .xg-card>a{text-decoration:none;color:inherit}
.doc .xg-proj{display:flex;align-items:center;gap:7px;font-size:15px;font-weight:700;color:var(--ink);text-decoration:none}
.doc a.xg-proj:hover{text-decoration:underline}
.doc .xg-proj img{width:18px;height:18px;border-radius:4px;flex:none;object-fit:contain}
.doc .xg-row{font-size:12px;color:var(--ink-soft);line-height:1.5}
.doc .xg-card .gal-cap b,.doc .xg-row b{font-weight:600;color:var(--ink);margin-right:6px}
@media (max-width:720px){.doc .view-switch{display:flex;max-width:100%;overflow-x:auto;scrollbar-width:none}.doc .view-switch button{white-space:nowrap;padding:7px 14px;flex:none}}
</style>

<div class="view-switch"></div>

<div class="env-view" data-view="overview" data-label="Overview">

<nav class="toc view-toc"><h2>Contents</h2><ul><li class="l2"><a href="#ov-1"><span class="num">1</span> Money Follows Distribution, Not Models</a></li><li class="l2"><a href="#ov-2"><span class="num">2</span> Five Tracks at Three Stages</a></li><li class="l2"><a href="#ov-3"><span class="num">3</span> Where Each Technology Pays</a></li><li class="l2"><a href="#ov-4"><span class="num">4</span> Technology × Track Matrix</a></li><li class="l2"><a href="#ov-5"><span class="num">5</span> What This Means for Visual Coder</a></li><li class="l2"><a href="#ov-6"><span class="num">6</span> Best Practice by Technology Route</a></li><li class="l2"><a href="#ov-7"><span class="num">7</span> Data Caliber</a></li></ul></nav>

<a class="anchor" id="ov-1"></a>

## 1 Money Follows Distribution, Not Models

3D 生成的单价四年降了 95% 以上，世界模型公司一年融资超过 30 亿美元，但这两类公司里披露过规模收入的只有一家。生成能力不是瓶颈。

能赚钱的公司有一个共同点：产品挂在用户本来就在付钱的流程上。本页用三个术语贯穿全文：

| 术语 | 定义 | 例子 |
|---|---|---|
| 现成付费渠道 | 用户已经在为之付钱的流程 | 广告投放、软件订阅、席位授权、平台分成 |
| 确定性环节 | 输出必须逐像素或逐参数正确的环节 | 广告上的价格文字、CAD 尺寸、商品配置选项 |
| visual coder | 用代码生成视觉产出的模型或工具 | 写 three.js 页面、Blender 脚本、CAD 代码、HTML 广告 |

现成付费渠道不是「市场大」。快手广告是现成付费渠道，因为广告主本来就在投放，AIGC 素材只是让同一笔预算多跑了量；世界模型面向的「可玩世界」没有现成付费渠道，玩家还没为它付过钱。

<a class="anchor" id="ov-2"></a>

## 2 Five Tracks at Three Stages

核心发现：五个赛道按是否挂在现成付费渠道上，分成三档。

| 档位 | 赛道 | 现成付费渠道 | 证据 |
|---|---|---|---|
| 已经赚钱 | 广告创意 | 广告主经平台消耗 | 快手 2025Q4 AIGC 素材带动营销消耗 40 亿元（[财报](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0325/2026032500367.pdf)） |
| 已经赚钱 | 3D 资产 | 个人订阅、3D 打印 | Meshy ARR 超 1 亿美元（[自报](https://dealroom.co/news/158079-meshy-hits-100m-arr-first-ai-3d-firm-to-reach-milestone/)） |
| 已经赚钱 | 产业 3D | 席位、授权、项目 | Applied Intuition 约 8.3 亿美元/年（[估算](https://sacra.com/research/applied-intuition-at-830m-year/)） |
| 有流量没收入 | Web 3D 中的 AI 生成部分、文生游戏 | 无，靠 VC 补贴或门户广告 | Astrocade 月活 1000 万，计划 2027 年变现（[Kotaku](https://kotaku.com/ai-generated-games-platform-already-has-10-million-monthly-users-2000741894)） |
| 只有资本 | 世界模型 | 无 | AMD 约 82 亿美元收购 World Labs，收入从未披露（[DCK](https://datacenterknowledge.com/data-center-chips/amd-to-acquire-world-labs-for-8-2b-to-advance-ai-models-and-robotics)） |

数据解读：

- **三档的分界线是渠道，不是技术难度。** 世界模型在技术上最难，收入最少；广告素材技术门槛最低，现金流最大。
- **同一项技术换个渠道就换一档。** 视频模型做广告片段，挂在投放上，已经赚钱；做可玩世界，没有渠道，停在 Demo。

<a class="anchor" id="ov-3"></a>

## 3 Where Each Technology Pays

核心发现：九类技术里，赚钱最稳的是引擎和视频模型，采用度涨得最快的是 three.js。

| 技术 | 在哪赚钱 | 采用度 |
|---|---|---|
| Blender | 独立动画、资产市场、合成数据 | 基金会年收入 311 万欧元；《Flow》用它拿下奥斯卡（[年报](https://download.blender.org/foundation/Blender-Foundation-Annual-Report-2024.pdf)） |
| three.js / WebGPU | 品牌站、配置器、网页游戏、孪生大屏 | npm 月下载 7022 万，一年涨 6.4 倍（[npm](https://api.npmjs.org/downloads/point/2026-09-01:2026-09-30/three)） |
| Unreal / Unity / 团结引擎 | 车机、虚拟制片、广电、仿真 | Unity 引擎板块 2025 年 6.2 亿美元，同比 +1%（[10-K](https://www.sec.gov/Archives/edgar/data/1810806/000181080626000011/unity-20251231.htm)） |
| Cocos / Laya | 微信、抖音小游戏 | 国内小游戏 2025 年约 610 亿元（[DataEye](https://www.thepaper.cn/newsDetail_forward_32682540)） |
| 3D 高斯点（3DGS） | 看房、仿真输入、商品孪生 | glTF 扩展 2026-02 进入候选标准（[Khronos](https://www.khronos.org/news/press/gltf-gaussian-splatting-press-release)） |
| Omniverse / Isaac | 工厂孪生、机器人仿真 | 四大机器人厂 200 万台装机接入虚拟调试（[NVIDIA](https://nvidianews.nvidia.com/news/nvidia-and-global-robotics-leaders-take-physical-ai-to-the-real-world)） |
| 原生 3D 生成模型 | 3D 打印、游戏白盒 | 各家 API 0.2 到 0.8 美元/个；TRELLIS.2 在 fal 上 0.25 到 0.35 美元（[fal](https://fal.ai/models/fal-ai/trellis-2)） |
| 视频 / 世界模型 | 广告素材、数字人、仿真 | 可灵 2026Q2 收入超 8.5 亿元（[TechNode](https://technode.global/?p=990300)） |
| LLM 写 3D 代码 / MCP | 网页游戏、DCC 自动化、text-to-CAD | BlenderMCP 3.06 万 star，零直接收入（[GitHub](https://github.com/ahujasid/blender-mcp)） |

数据解读：

- **three.js 的增长不是 Web 3D 市场变大，而是写代码的人变了。** 同期 react 下载涨 3.8 倍，three.js 涨 6.4 倍，多出来的部分最可能来自 AI 生成代码；官方 showcase 已收录 Claude 生成的作品。
- **MCP 有用户没收入。** 因为 Blender、Unity、Unreal、Houdini、C4D 都免费提供官方 MCP，独立 MCP 工具没有定价空间。

<a class="anchor" id="ov-4"></a>

## 4 Technology × Track Matrix

核心发现：标「赚钱」的格子全部挂在现成付费渠道上。

图例：**赚钱** = 有财报或自报的规模收入；早期 = 有付费但规模小；Demo = 只有演示或融资；— = 无关。

| 技术 | 3D 资产 | 游戏与世界 | 广告创意 | Web 3D | 产业 3D |
|---|---|---|---|---|---|
| Blender | 早期 | 早期 | 早期 | **赚钱** | 早期 |
| three.js / WebGPU | 早期 | 早期 | 早期 | **赚钱** | **赚钱** |
| Unreal / Unity | **赚钱** | **赚钱** | — | 早期 | **赚钱** |
| Cocos / Laya | — | **赚钱** | — | **赚钱** | — |
| 3DGS | 早期 | 早期 | 早期 | 早期 | 早期 |
| Omniverse / Isaac | — | 早期 | — | — | **赚钱** |
| 原生 3D 生成 | **赚钱** | 早期 | — | 早期 | 早期 |
| 视频 / 世界模型 | — | Demo | **赚钱** | — | 早期 |
| LLM 写 3D 代码 | 早期 | 早期 | 早期 | 早期 | 早期 |

数据解读：

- **「LLM 写 3D 代码」整行早期，却横跨全部五个赛道。** 它不是一个赛道，是降低交付成本的生产方式，价值落在它服务的那个赛道里。
- **3DGS 整行早期。** 它解决的是采集，不是分发；等 glTF 标准定稿、浏览器原生支持后才会进入付费流程。

<a class="anchor" id="ov-5"></a>

## 5 What This Means for Visual Coder

visual coder 本身不是生意。它的价值在于接管现成付费渠道里的确定性环节，因为生成模型在这些环节出错就不能交付，代码不会。

核心发现：按「付费方已存在」和「代码就是交付物」两个条件排序，前三名都同时满足。

| 排名 | 方向 | 为什么能做 | 主要风险 |
|---|---|---|---|
| 1 | 广告图与电商图的模板渲染层 | 价格、logo、多尺寸必须逐像素准确；Bannerbear、Placid 已开放 MCP 给广告 agent 调用 | 平台把生成工具免费塞进投放后台 |
| 2 | 面向 3D 打印的 CAD-as-code | 拓竹 2025 年营收预计破百亿元；开源 text-to-cad 半年 1.98 万 star；参数化代码可改可审 | Zoo、Adam 都未披露收入 |
| 3 | 品牌 Web 3D 与配置器降本 | 单项目 2 万到 12 万美元；three.js 下载一年涨 6.4 倍，增量最可能来自 AI 写代码 | 头部作品靠少数工作室手艺 |
| 4 | 程序化合成数据 | 光轮单季新签 5.5 亿元；Blender 支持无头 GPU 渲染 | 主流栈是 NVIDIA Isaac |
| 5 | three.js 网页小游戏 | Poki 月玩家 1 亿 | 单个游戏收入不可持续，只能给平台供货 |
| 6 | 国内孪生大屏交付 | 平均每单约 150 万元 | 集成商毛利 20% 到 50%，回款慢 |

数据解读：

- **第 1 名不是「AI 生成广告图」，而是生成之后的那一层。** 生成模型出画面，代码负责价格、字幕、尺寸改版；Photoroom 为此专门收购了模板公司 Generate Banners。
- **高热度商业 demo 里，代码已是主要的渲染方式，但还不是主要的生产方式。** 本页 90 个 demo 中，Web 3D 的 25 个有 17 个是 three.js 或手写 WebGL；而全部 90 个里，由 AI 写代码产出的只有 3 个：Fly、Astrocade、Adam。渲染层已经是代码，写代码的还是人，这正是 visual coder 的空位。
- **两个方向不建议做。** 独立的 DCC MCP 工具，因为厂商都免费提供；用代码搭可玩世界卖给消费者，因为世界模型自己都卖不动。

下一步：在第 1、2 名方向各做一个可付费的最小产品，用真实广告主和打印用户验证付费意愿。

<a class="anchor" id="ov-6"></a>

## 6 Best Practice by Technology Route

把五个赛道换个切法：按技术路线拆成五条，每个商业场景挑一个最能说明「谁在付钱」的案例。

核心发现：diffusion 路线已经挂在投放和打印上赚钱；code 路线只有前端开发跑出了规模，视频和 3D 的 code 路线还在找付费方。

| 技术路线 | 成熟度 | 钱从哪来 | 场景 → 最佳实践 |
|---|---|---|---|
| 前端开发（webdev） | 已成规模 | 卖给创作者的订阅 | App / MVP → Lovable；网页小游戏 → Fly；Web 3D 产品页 → 小米 YU7 |
| 视频生成（diffusion） | 现金流最大 | 广告主的投放预算 | 效果广告 → Higgsfield；爆款广告 → Kalshi；数字人 → HeyGen；电商素材 → 万相营造；AI 短剧 → 雪山救狐 |
| 视频生成（code） | 早期 | 依附广告与数字人平台 | 发布片 → Deedy；个性化批量 → GitHub Unwrapped；科普动画 → 3Blue1Brown；广告确定性层 → Photoroom |
| 3D 资产生成（diffusion） | 已赚钱，单价在崩 | 3D 打印出口 | 打印手办 → Meshy；游戏资产 → Tripo；平台内生成 → Roblox Cube；电商重建 → SAM 3D |
| 3D 资产生产（code） | 早期，无人披露 ARR | 插件订阅与合成数据合同 | CAD → Adam；DCC 自动化 → BlenderMCP；合成数据 → 光轮；配置器 → Threekit |

数据解读：

- **code 路线有两种活法。** 卖创作者订阅（webdev），或接管别人渠道里的确定性环节（广告模板、CAD、配置器）。直接卖作品给消费者的不稳：Fly 17 天 ARR 100 万美元，2026 年中归零。
- **有三张卡不是 AI 写代码。** 小米 YU7、3Blue1Brown 是人写的，光轮走 Isaac 仿真。放进来是因为它们最能说明这个场景谁在付钱，也正是 visual coder 的空位。

### 前端开发（webdev）

code 路线里唯一跑出规模的一条。钱来自卖工具订阅给做东西的人，不是卖做出来的作品。

<!--BP:webdev-->

<div class="gal-grid">
<a class="gal-card mk-card" href="https://lovable.dev/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/bp-webdev-00.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Lovable</div><div class="mk-by">Lovable（瑞典）</div><div class="gal-cap">一句话描述需求，生成前后端并一键部署；用户 WNTD 靠它每月省下 2.5 万英镑以上的开发费，融到 300 万英镑</div><div class="mk-tags"><span class="mk-tech">LLM 写全栈代码</span><span class="mk-heat">ARR 约 6 亿美元，C 轮估值 133 亿美元（AI Magazine）</span><span class="mk-biz">非程序员做 App / MVP · 订阅</span></div></div></a>
<a class="gal-card mk-card" href="https://fly.pieter.com/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/game-13.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Fly 飞行模拟</div><div class="mk-by">Pieter Levels（@levelsio）</div><div class="gal-cap">AI 写 three.js 的浏览器多人飞行游戏，广告位卖给赞助商、再卖飞机；爆款不持续，2026 年中归零</div><div class="mk-tags"><span class="mk-tech">three.js + AI 写代码</span><span class="mk-heat">上线 17 天 ARR 100 万美元（作者自述）</span><span class="mk-biz">网页小游戏 · 广告 + 内购</span></div></div></a>
<a class="gal-card mk-card" href="https://www.xiaomiev.com/yu7" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-17.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">小米 YU7 官网</div><div class="mk-by">小米汽车</div><div class="gal-cap">three.js + Draco 模型嵌进长滚动产品页，3D 挂在下单流程上；页面是人写的，AI 的空位在这类有套路的产品页</div><div class="mk-tags"><span class="mk-tech">three.js</span><span class="mk-heat">发布 18 小时锁单 24 万台</span><span class="mk-biz">Web 3D 产品页 · 新车上市</span></div></div></a>
</div>

<!--/BP-->

### 视频生成（diffusion）

付费方是本来就在投放的广告主。国内钱落在投放平台（快手 2025Q4 AIGC 素材带动 40 亿元消耗），海外由聚合应用做大。

<!--BP:vdiff-->

<div class="gal-grid">
<a class="gal-card mk-card" href="https://higgsfield.ai/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-10.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Higgsfield 广告模板</div><div class="mk-by">Higgsfield AI（多模型聚合）</div><div class="gal-cap">把多家视频模型包成投放场景模板，三步批量出产品与 UGC 广告；海外聚合应用做大，单功能工具出清</div><div class="mk-tags"><span class="mk-tech">视频模型（聚合）</span><span class="mk-heat">年化 10 亿美元，一年前 1100 万美元（自报）</span><span class="mk-biz">效果广告素材 · SaaS 订阅</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=-QMftwmyW-A" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-00.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Kalshi 总决赛广告</div><div class="mk-by">Kalshi × PJ Accetturo（Google Veo 3）</div><div class="gal-cap">1 人 2–3 天、工具费不到 2000 美元，数百次生成挑出 15 个镜头；低成本整活比大牌节日主片安全</div><div class="mk-tags"><span class="mk-tech">视频模型（Veo 3）</span><span class="mk-heat">上线一周 X 播放超 300 万，上了 NBA 总决赛</span><span class="mk-biz">低成本爆款广告 · 赛事投放</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=yKhZb4Ny_I0" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/industry-05.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">HeyGen 数字分身</div><div class="mk-by">HeyGen</div><div class="gal-cap">拍一段视频克隆本人形象与声音，生成多语种口播；替代的是真人出镜重拍</div><div class="mk-tags"><span class="mk-tech">视频模型 + 声音克隆</span><span class="mk-heat">ARR 2 亿美元，8 个月翻倍（官方，2026-06）</span><span class="mk-biz">数字人口播 · 订阅 / 按分钟</span></div></div></a>
<a class="gal-card mk-card" href="https://www.bilibili.com/video/BV14QFFeMEkz/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-14.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">阿里妈妈万相营造</div><div class="mk-by">阿里妈妈 万相营造</div><div class="gal-cap">一键生成商品图、模特图、图生视频，FILA 换场景 1 分钟出二三十张图；平台免费送，钱从投放里收回</div><div class="mk-tags"><span class="mk-tech">图像 + 视频模型</span><span class="mk-heat">覆盖约 100 万商家，日省 4000 万元以上（新浪）</span><span class="mk-biz">电商商品素材 · 平台内置</span></div></div></a>
<a class="gal-card mk-card" href="https://www.digitaling.com/articles/1477776.html" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-15.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">雪山救狐无限流</div><div class="mk-by">贵州酱板鸭小团队 → 瑞幸 / 肯德基 / 淘宝等接龙</div><div class="gal-cap">4 人小店用邵氏风 AI 短剧卖鸭，总成本一千多元，数十个品牌官号接龙植入；同类还有红旗自制 AI 剧 7600 万播放</div><div class="mk-tags"><span class="mk-tech">视频模型</span><span class="mk-heat">全网约 50 亿播放（极目新闻）</span><span class="mk-biz">品牌 AI 短剧 · 每分钟 800–1500 元</span></div></div></a>
</div>

<!--/BP-->

### 视频生成（code）

还没有独立的大收入公司。独有价值是「一套模板 × N 份数据」和逐像素正确，商业上依附广告或数字人平台。

<!--BP:vcode-->

<div class="gal-grid">
<a class="gal-card mk-card" href="https://x.com/deedydas/status/2102787937482252537" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/bp-vcode-00.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Deedy 发布片</div><div class="mk-by">Deedy Das（Opus 5.5）</div><div class="gal-cap">一句提示，LLM 写 JS 网页动画，Playwright 逐帧捕获、FFmpeg 出片，不用视频模型；HyperFrames 是它的框架化版本</div><div class="mk-tags"><span class="mk-tech">LLM 写网页动画</span><span class="mk-heat">约 1 分钟、约 2 美元（作者自述）</span><span class="mk-biz">产品发布片 · 单个演示</span></div></div></a>
<a class="gal-card mk-card" href="https://www.githubunwrapped.com/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/bp-vcode-01.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">GitHub Unwrapped</div><div class="mk-by">Remotion 团队</div><div class="gal-cap">React 写一套年度回顾模板，按每个用户的数据渲染一支，AWS Lambda 多区域并行；一套模板 × N 份数据是 diffusion 做不到的</div><div class="mk-tags"><span class="mk-tech">Remotion（React → 视频）</span><span class="mk-heat">给 1 万+ GitHub 用户各生成一支（Decibel）</span><span class="mk-biz">个性化批量视频 · Company License</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=aircAruvnKk" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/bp-vcode-02.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">3Blue1Brown</div><div class="mk-by">Grant Sanderson（Manim 作者）</div><div class="gal-cap">几乎所有动画都用自写的开源库 Manim 生成；代码是人写的，LLM 写 Manim 还在研究阶段（Code2Video）</div><div class="mk-tags"><span class="mk-tech">Manim（Python）</span><span class="mk-heat">YouTube 870 万订阅、7.8 亿播放（Vidanalyze）</span><span class="mk-biz">科普动画 · 观众赞助</span></div></div></a>
<a class="gal-card mk-card" href="https://www.photoroom.com/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/bp-vcode-03.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Photoroom × Generate Banners</div><div class="mk-by">Photoroom</div><div class="gal-cap">生成模型出画面，模板负责价格、logo、多尺寸；2025-05 收购模板公司 Generate Banners 补上这一层（以图为主）</div><div class="mk-tags"><span class="mk-tech">图像模型 + 模板渲染</span><span class="mk-heat">约 9400 万美元/年（Sacra 估算），Wolt 14 万商家走 API</span><span class="mk-biz">广告确定性层 · API 计费</span></div></div></a>
</div>

<!--/BP-->

### 3D 资产生成（diffusion）

单个模型从约 8 美元跌到 0.2 到 0.4 美元，大厂又在开源。钱在出口（打印、平台），不在生成质量榜。

<!--BP:3ddiff-->

<div class="gal-grid">
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=EZN8xb1xHzU" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/asset-00.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Meshy 一键多色打印</div><div class="mk-by">Meshy × 拓竹 MakerWorld</div><div class="gal-cap">一张图 → 3D → 自动分色出 3MF，拖进拓竹切片直接打全彩；打印绕开了 AI 最差的拓扑、UV、绑骨</div><div class="mk-tags"><span class="mk-tech">原生 3D 生成</span><span class="mk-heat">ARR 超 1 亿美元；打印视频 886 万播放</span><span class="mk-biz">3D 打印 / 手办 · 订阅</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=g4ozFeSBPfo" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/asset-03.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Tripo P2.0</div><div class="mk-by">VAST / Tripo AI</div><div class="gal-cap">原生四边面拓扑，角色直接可绑骨做动画；竞争点从「像不像」转向「能不能直接进管线」</div><div class="mk-tags"><span class="mk-tech">原生 3D 生成</span><span class="mk-heat">1200 万美元/年；Sony、网易等工作室在用</span><span class="mk-biz">游戏资产 · API + 订阅</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=85PNb99CT68" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/asset-09.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Roblox Cube</div><div class="mk-by">Roblox</div><div class="gal-cap">玩家在游戏里一句话生成可交互物体，4D 版本可动可开；生成不单独卖，换平台时长</div><div class="mk-tags"><span class="mk-tech">原生 3D 生成</span><span class="mk-heat">Wish Master 里使用者平均时长 +64%</span><span class="mk-biz">平台内生成 · 平台自用</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=B7PZuM55ayc" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/asset-14.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Meta SAM 3D</div><div class="mk-by">Meta</div><div class="gal-cap">单张实拍图重建物体和人体 3D；大厂开源压住模型层，价值落在自家交易场景</div><div class="mk-tags"><span class="mk-tech">单图 3D 重建</span><span class="mk-heat">GitHub 7.5k star，Facebook 二手市场已用</span><span class="mk-biz">电商 / 二手重建 · 开源</span></div></div></a>
</div>

<!--/BP-->

### 3D 资产生产（code）

没有一家披露 ARR。DCC 厂商都免费送 MCP，能做的是代码本身就是交付物的地方：CAD、合成数据、配置器。

<!--BP:3dcode-->

<div class="gal-grid">
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=EHu6Vrqo69A" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/industry-15.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Adam 文本生 CAD</div><div class="mk-by">Adam（YC W25）</div><div class="gal-cap">一句话生成可编辑参数化零件，做成 Fusion、Onshape 里的 CAD-as-code 插件，不做替代品</div><div class="mk-tags"><span class="mk-tech">LLM 写 CAD 代码</span><span class="mk-heat">用户已生成 100 万+ 模型，种子轮 410 万美元</span><span class="mk-biz">参数化 CAD · 插件订阅</span></div></div></a>
<a class="gal-card mk-card" href="https://github.com/ahujasid/blender-mcp" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/bp-3dcode-01.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">BlenderMCP</div><div class="mk-by">开源社区（ahujasid）</div><div class="gal-cap">LLM 通过 MCP 写 bpy 驱动 Blender，截图回看再修；厂商都免费送 MCP，独立工具没有定价空间</div><div class="mk-tags"><span class="mk-tech">LLM 写 Blender 代码</span><span class="mk-heat">GitHub 3.06 万 star、PyPI 月下载约 49 万，零直接收入</span><span class="mk-biz">DCC 自动化 · 免费</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=mqEBWpq3VgA" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/industry-11.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">光轮仿真数据</div><div class="mk-by">光轮智能 Lightwheel</div><div class="gal-cap">SimReady 资产 + Isaac Sim 物理仿真，为具身模型批量造数据；主流栈是 Isaac，不是 LLM 写代码</div><div class="mk-tags"><span class="mk-tech">Isaac 仿真</span><span class="mk-heat">2026Q1 新签 5.5 亿元，2026-03 融资 10 亿元</span><span class="mk-biz">程序化合成数据 · 数据服务</span></div></div></a>
<a class="gal-card mk-card" href="https://www.threekit.com/virtual-photographer" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/bp-3dcode-03.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Threekit 虚拟摄影</div><div class="mk-by">Threekit</div><div class="gal-cap">产品建一次 3D，配置器里换选项，批量渲染数万张电商图；商品选项必须逐参数正确，适合代码</div><div class="mk-tags"><span class="mk-tech">3D 配置器 + 批量渲染</span><span class="mk-heat">配置器市场约 17 亿美元，Amazon 称点开 3D 转化约 2 倍</span><span class="mk-biz">配置器 / 虚拟摄影 · 企业 SaaS</span></div></div></a>
</div>

<!--/BP-->

<a class="anchor" id="ov-7"></a>

## 7 Data Caliber

- **四类口径**：财报（交易所文件）、自报（公司或创始人）、估算（Sacra 等第三方）、实测（调研时直接读取的 API 与榜单）。表格链接即出处。
- **截止日期**：2026-10-13。
- **已知缺口**：国内数据偏薄，稿定、LiblibAI、Temu 与 SHEIN 的 AI 商品图、数字人直播 GMV 未查到；世界模型与文生游戏公司都没有经审计的收入。
- **对第一版的更正**：Hitem3D 母公司是数美万物，不是魔芯；「Tripo 已盈利」出处不成立；快手财报里没有「转化 +20% 到 30%」；three.js 约为 Babylon 的 47 倍，不是 270 倍；「Shopify 3D 提升 94% 转化」找不到原始出处。
- **第三轮回源核对的更正**：Roblox Cube「每天 6 万个资产」找不到出处，改为一年 180 万个；Threekit 融资是累计约 8010 万加元，不是单轮 4360 万；阿里妈妈 1.5 亿是淘天全平台的图片与视频总量，不是万相营造单独生成；Meshy、美图、Synthesia、Arcads 的数字是 ARR，不是年收入；拓竹「破百亿」是 CEO 的预期，不是正式披露。逐条核对表见 middle_processing/market/audit_landscape.md。
- **第四轮 demo 复核的更正**：苹果 AirPods 产品页只为 360 度视频播放器按需加载 three.js，产品 3D 画面是预渲染视频，已撤下该卡；SpaceX 对接模拟、Seed3D、HappyOyster、Zillow SkyTour 查不到硬热度，换成有收购、用户数或播放量出处的同类 demo；国内 Web 3D 补入天猫 3D 购、得物 AR、贝壳 VR、云游长城，这几项数字多为 2020 到 2023 年口径。行业表补齐 11 个空格（PixVerse ARR、Odyssey B 轮、Arcads 种子轮、Poki 月活等）；Kaedim 融资改为累计约 1500 万美元；Web 3D 表里查不到数字的 5 家工作室合并为一行。核对记录见 middle_processing/market/r3_landscape_fill.md。
- **第 6 节最佳实践（2026-11-03 新增）**：卡片数据在 middle_processing/market/best_practice.json，由 scripts/market_bestpractice.py 渲染。Lovable、HeyGen ARR、GitHub Unwrapped、3Blue1Brown 四条为当日网络补查，多为二手报道，未核对一手来源。

</div>

<div class="env-view" data-view="asset" data-label="3D Assets">

<nav class="toc view-toc"><h2>Contents</h2><ul><li class="l2"><a href="#as-1"><span class="num">1</span> Industry Landscape</a></li><li class="l2"><a href="#as-2"><span class="num">2</span> Best Practices</a></li><li class="l2"><a href="#as-3"><span class="num">3</span> Insights</a></li></ul></nav>

AI 3D 已经有一家公司 ARR 过 1 亿美元，但游戏厂至今不承认在已发售作品里用过 AI 资产。钱从别处来：3D 打印。

<a class="anchor" id="as-1"></a>

## 1 Industry Landscape

核心发现：独立玩家里只有 Meshy 跑出规模，其余头部几乎都是中国团队，而且靠海外收入。

| 公司 | 定位 | 营收 | 估值 | 代表作 |
|---|---|---|---|---|
| Meshy（海外） | 原生 3D 生成 + 重拓扑、绑骨一站式 | ARR 超 1 亿美元（[自报](https://dealroom.co/news/158079-meshy-hits-100m-arr-first-ai-3d-firm-to-reach-milestone/)） | 15 亿美元 | [Meshy 7](https://www.meshy.ai) |
| VAST Tripo（国内） | 原生 3D，主打可用的四边面拓扑 | 1200 万美元/年（2025-09 [自报](https://arinsider.co/2025/09/22/can-tripos-gen-ai-step-change-unlock-3d-tiktok/)） | 10 亿美元以上 | [Tripo P2.0](https://www.tripo3d.ai) |
| 影眸 Rodin（国内） | 高精度原生 3D，80% 收入来自海外 | 数千万美元/年（[自报](https://m.jiemian.com/article/14631332.html)） | 未披露；2026-06 新一轮数亿元（[东方财富](https://finance.eastmoney.com/a/202606233779269161.html)） | [Rodin Gen-2.5](https://hyper3d.ai/) |
| 腾讯混元 3D（国内） | 2.x 开源，3.x 走腾讯云 API | 不单独披露 | — | [Hunyuan3D 2.0](https://github.com/Tencent-Hunyuan/Hunyuan3D-2) |
| 数美万物 Hi3D（国内） | 生成 + 自动拆件 + 自建工厂代打印 | 未披露 | 近两轮近 5000 万美元，累计未披露 | [Hi3D](https://www.hitem3d.ai/) |
| 字节 Seed3D（国内） | 部件与铰接，面向具身仿真资产 | 不单独披露 | — | Seed3D 2.0 |
| Microsoft TRELLIS.2（海外） | 开源原生 3D 模型 | 开源 | — | [TRELLIS.2](https://github.com/microsoft/TRELLIS.2) |
| Roblox Cube（海外） | 平台自用的 3D / 4D 生成 | 不单独披露；一年生成 180 万个资产（[Roblox](https://about.roblox.com/de/newsroom/2026/02/accelerating-creation-powered-roblox-cube-foundation-model)） | — | Cube 4D |
| Kaedim（海外） | 「AI + 人工」3D 外包；2023 年被曝部分「AI 生成」实为人工建模（[404 Media](https://www.404media.co/kaedim-ai-startup-2d-to-3d-used-cheap-human-labor/)） | 未披露 | 累计融资约 1500 万美元 | Lowe's 电商资产 |
| 拓竹 Bambu Lab（国内） | 分发方：打印机 + MakerWorld 社区 | 2025 年预计破 100 亿元（CEO [自报](https://www.yicai.com/news/103029400.html)） | 未披露 | MakerWorld |

数据解读：

- **拓竹不是 3D 生成公司，却是这张表里收入最大的一家。** 它掌握出口：MakerWorld 月活约 1000 万，Meshy、混元、Hi3D 都在往里接。
- **大厂开源压住了模型层。** 腾讯、微软、Roblox 都开源 3D 模型，独立公司只能在后处理和分发上做差异。

<a class="anchor" id="as-2"></a>

## 2 Best Practices

核心发现：同一家 Meshy，打印实物的视频 886 万播放，模型发布片 9.7 万，相差约 90 倍。观众买账的不是模型，是打印出来的东西。

| 类别 | 代表 demo | 证明了什么 |
|---|---|---|
| 生成后打印 | Meshy 多色打印、Hi3D 打印实测、40cm 手办 | C 端愿意为实物付钱，热度百万级 |
| 模型发布 | Meshy 7、Tripo、Rodin、混元、TRELLIS.2、Unity、Autodesk | 热度多在万级，作用是给 API、开源和引擎订阅引流 |
| 平台内生成 | Roblox Cube、拓竹 PrintU | 生成挂进已有平台，直接拉时长和积分消耗 |

<!--DEMOS:asset-->

<div class="gal-grid">
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=EZN8xb1xHzU" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/asset-00.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Meshy 一键多色打印</div><div class="mk-by">Meshy</div><div class="gal-cap">一张图→3D→自动分色出 3MF，拖进拓竹切片直接打全彩</div><div class="mk-tags"><span class="mk-tech">原生 3D 生成</span><span class="mk-heat">YouTube 886 万播放</span><span class="mk-biz">拓竹 MakerWorld 已集成</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=Vnf69xfmJwg" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/asset-01.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Agent 打印真人手办</div><div class="mk-by">Meshy</div><div class="gal-cap">让 AI Agent 把真人做成一整套系列手办并实际打印出来</div><div class="mk-tags"><span class="mk-tech">原生 3D 生成</span><span class="mk-heat">YouTube 288 万播放</span><span class="mk-biz">C 端手办定制场景</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=A7akdu09D8Q" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/asset-12.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Hi3D 打印实测</div><div class="mk-by">Shark Numbers × Hi3D</div><div class="gal-cap">博主全流程实测 AI 模型能否直接打印，成品细节出圈</div><div class="mk-tags"><span class="mk-tech">原生 3D 生成</span><span class="mk-heat">YouTube 177 万播放</span><span class="mk-biz">200 万+ 创作者平台</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=gjLxktLLLQs" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/asset-11.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Hi3D 模型自动拆件</div><div class="mk-by">数美万物 Hi3D</div><div class="gal-cap">生成后自动拆件分色，免 Blender 直接送切片打印</div><div class="mk-tags"><span class="mk-tech">原生 3D 生成</span><span class="mk-heat">官方视频 44 万播放</span><span class="mk-biz">自建工厂·打印到家</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=6MSSVwN45cg" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/asset-13.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">40cm AI 手办</div><div class="mk-by">Stefan 3D AI（社区）</div><div class="gal-cap">AI 生图→生成→拆件打印上色，做出 40cm 大尺寸成品</div><div class="mk-tags"><span class="mk-tech">原生 3D 生成</span><span class="mk-heat">YouTube 12.6 万播放</span><span class="mk-biz">个人手办生意范本</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=85PNb99CT68" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/asset-09.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Roblox Cube</div><div class="mk-by">Roblox</div><div class="gal-cap">游戏内一句话生成可交互物体，2026 年升级 4D 可动可开</div><div class="mk-tags"><span class="mk-tech">原生 3D 生成</span><span class="mk-heat">官方视频 12.7 万播放</span><span class="mk-biz">4D 生成使游戏时长+64%</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=3IDVZNNsTI0" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/asset-07.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">拓竹 PrintU</div><div class="mk-by">拓竹 Bambu Lab（混元3D）</div><div class="gal-cap">一张自拍→Q 版/大头手办，自动配拓竹耗材色直接开打</div><div class="mk-tags"><span class="mk-tech">原生 3D 生成</span><span class="mk-heat">YouTube 6.9 万播放</span><span class="mk-biz">MakerWorld 10 积分/次</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=FYl0ng2haZ8" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/asset-02.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Meshy 7 发布</div><div class="mk-by">Meshy</div><div class="gal-cap">主打与输入图高度对齐的新一代模型，形体与贴图一致性跃升</div><div class="mk-tags"><span class="mk-tech">原生 3D 生成</span><span class="mk-heat">测评视频 23.7 万播放；官方发布片 9.7 万</span><span class="mk-biz">首家 ARR 破 1 亿美元</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=g4ozFeSBPfo" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/asset-03.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Tripo P2.0</div><div class="mk-by">VAST / Tripo AI</div><div class="gal-cap">业内首个原生四边面拓扑，角色直接可绑骨做动画</div><div class="mk-tags"><span class="mk-tech">原生 3D 生成</span><span class="mk-heat">同期 B 轮融资 4.45 亿美元</span><span class="mk-biz">Sony/网易等工作室在用</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=32wCB_R-YP4" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/asset-04.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">MonsterUP 合作</div><div class="mk-by">MonsterUP × Tripo AI</div><div class="gal-cap">千万播放级动画 IP 频道用 Tripo P2.0 做角色资产</div><div class="mk-tags"><span class="mk-tech">原生 3D 生成</span><span class="mk-heat">YouTube 9 万播放</span><span class="mk-biz">动画 IP 工作室品牌合作</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=ymTb7eKc9ng" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/asset-05.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Rodin 2.5</div><div class="mk-by">影眸科技 Deemos</div><div class="gal-cap">千万面级网格、可调思考档位，数秒出影视级资产</div><div class="mk-tags"><span class="mk-tech">原生 3D 生成</span><span class="mk-heat">上线首月订阅与 ARR 环比增超 400%（第一财经）</span><span class="mk-biz">客户含 Unity/Canva</span></div></div></a>
<a class="gal-card mk-card" href="https://github.com/Tencent-Hunyuan/Hunyuan3D-2" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/asset-06.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">混元3D 开源模型</div><div class="mk-by">腾讯混元</div><div class="gal-cap">开源图生 3D 标杆，带 PBR 贴图，社区二创与插件生态最广</div><div class="mk-tags"><span class="mk-tech">开源 3D 模型</span><span class="mk-heat">GitHub 1.5 万 star</span><span class="mk-biz">腾讯云 API·150+ 企业接入</span></div></div></a>
<a class="gal-card mk-card" href="https://microsoft.github.io/TRELLIS.2/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/asset-08.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">TRELLIS.2</div><div class="mk-by">Microsoft</div><div class="gal-cap">40 亿参数开源图生 3D，PBR 材质可重打光，开源界画质天花板</div><div class="mk-tags"><span class="mk-tech">开源 3D 模型</span><span class="mk-heat">GitHub 1.2 万 star</span><span class="mk-biz">fal 等平台已上 API</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=ca76F7Jo84k" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/asset-10.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Autodesk Flow Studio 3D</div><div class="mk-by">Autodesk</div><div class="gal-cap">Wonder 3D 文/图生 3D，再在 3D 编辑器里摆机位交 AI 渲染</div><div class="mk-tags"><span class="mk-tech">原生 3D 生成</span><span class="mk-heat">官方 3D 编辑器发布片 30.5 万播放</span><span class="mk-biz">Autodesk 订阅产品</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=B7PZuM55ayc" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/asset-14.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Meta SAM 3D</div><div class="mk-by">Meta</div><div class="gal-cap">单张实拍图重建物体和人体 3D，真实场景也能用</div><div class="mk-tags"><span class="mk-tech">单图 3D 重建</span><span class="mk-heat">GitHub 7.5k star；官方 6.9 万播放</span><span class="mk-biz">Facebook 二手市场已用</span></div></div></a>
<a class="gal-card mk-card" href="https://unity.com/blog/unity-ai-3d-object-generator" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/asset-15.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Unity AI 3D 物体生成</div><div class="mk-by">Unity</div><div class="gal-cap">编辑器内文/图生 3D 道具，直接产出带网格材质的预制体</div><div class="mk-tags"><span class="mk-tech">原生 3D 生成</span><span class="mk-heat">Unity AI 公测发布片 2402 万播放</span><span class="mk-biz">Unity 6 内置功能</span></div></div></a>
</div>

<!--/DEMOS-->

<a class="anchor" id="as-3"></a>

## 3 Insights

- **钱在 3D 打印，不在游戏。** 因为打印只要求模型是封闭的实体，不要求干净拓扑、UV 和绑骨，而这三项正是 AI 模型最差的地方。
- **模型层守不住价格。**
  - 单个模型从 2022 年约 8 美元降到 0.2 到 0.4 美元；开源 TRELLIS.2 每次生成的 GPU 成本不到 0.07 美元。
  - 西方创业公司在撤退：谷歌收购了 CSM，Luma、Backflip、Sudo 都已转型。
- **竞争点转向「能不能直接用」。** 直接输出低模、四边面、分件的模型，已取代「先生成再重拓扑」的流程；生成器把绑骨和动画免费打包。
- **风险来自 IP 和平台政策，不来自技术。** 泡泡玛特起诉拓竹后和解下架；MakerWorld 不让 AI 模型进独家激励计划。

下一步：看 3D 打印出口的付费转化，而不是看生成质量榜。

</div>

<div class="env-view" data-view="game" data-label="Game & World">

<nav class="toc view-toc"><h2>Contents</h2><ul><li class="l2"><a href="#gm-1"><span class="num">1</span> Industry Landscape</a></li><li class="l2"><a href="#gm-2"><span class="num">2</span> Best Practices</a></li><li class="l2"><a href="#gm-3"><span class="num">3</span> Insights</a></li></ul></nav>

世界模型公司一年融资超 30 亿美元，没有一家披露收入；同一时期，Roblox 付给创作者 15 亿美元。游戏里的 AI 钱，流向了已有平台。

<a class="anchor" id="gm-1"></a>

## 1 Industry Landscape

核心发现：有收入的是平台，有估值的是世界模型，两者几乎不重叠。

| 公司 | 定位 | 营收 | 估值 | 代表作 |
|---|---|---|---|---|
| Roblox（海外） | UGC 平台：Build 文生游戏、Cube、Roblox Reality | 2025 年付开发者 15 亿美元（[财报](https://www.sec.gov/Archives/edgar/data/1315098/000131509826000024/rblx-20251231.htm)） | 上市 | Roblox 4D 生成 |
| Epic Fortnite（海外） | UEFN 创作者生态 + AI 角色 NPC | 2024 年付创作者 3.52 亿美元，累计超 10 亿美元 | 私有 | AI 达斯·维达 |
| Google DeepMind（海外） | Genie 3 像素流世界模型 | 不单独披露 | — | Project Genie |
| World Labs（海外） | 生成可导出的 3D 世界 | 不公开（[Sacra](https://sacra.com/c/world-labs/)） | AMD 约 82 亿美元收购（[DCK](https://datacenterknowledge.com/data-center-chips/amd-to-acquire-world-labs-for-8-2b-to-advance-ai-models-and-robotics)） | Marble |
| Decart（海外） | 实时世界模型，转向驾驶仿真 | 约 1260 万美元（2024 [估算](https://getlatka.com/companies/decart.ai)） | 约 40 亿美元 | Oasis |
| Odyssey（海外） | 实时交互视频，转向机器人 | 未披露 | 14.5 亿美元（2026-06 B 轮 3.1 亿美元） | Odyssey-3 |
| Runway（海外） | GWM Worlds 世界模型 | 全公司 ARR 2 亿美元（[自报](https://www.briefs.co/news/runway-s-arr-jumps-to-200-million-as-ai-video-finds-its-groo/)） | 53 亿美元 | GWM Worlds 2 |
| AMI Labs（海外） | LeCun 的 JEPA 世界模型，尚无产品 | 无收入 | 种子轮 10.3 亿美元，投前 35 亿美元（[Latent Space](https://www.latent.space/p/ainews-yann-lecuns-ami-labs-launches)） | 计划 2027 年工业应用 |
| Astrocade（海外） | 文生休闲游戏信息流 | 未变现，计划 2027 年 | 融资 5600 万美元 | Astrocade |
| 网易 蛋仔派对（国内） | UGC 游戏 + AI 编辑器 | 创作者激励与分成超 2 亿元/年（[36氪](https://www.36kr.com/p/3896755010963333)） | 上市 | 蛋仔 AI 编辑器 |
| 网易 逆水寒（国内） | 大模型驱动的智能 NPC | 不单独披露；AI 门客破 4000 万个（2026-07 [官方口径](https://stock.10jqka.com.cn/20260710/c678090861.shtml)） | 上市 | 智能 NPC |
| 腾讯混元（国内） | 开源世界生成，导出网格和高斯点 | 不单独披露 | — | HY-World 2.0 |
| 爱诗 PixVerse（国内） | 视频模型 + 实时世界模型 | 全公司 ARR 超 4000 万美元（2025 年底[自报](https://equalocean.com/news/2026031221788-aishi-technology-secures-300m-chinas-biggest-ai-video-funding-round/amp)）；月活 1500 万 | C 轮累计 29.8 亿元 | PixVerse R1 |
| 阿里（国内） | HappyOyster 实时世界模型，闭源 | 不单独披露 | — | HappyOyster |

数据解读：

- **世界模型的估值来自收购方，不来自用户。** AMD 买 World Labs 是为了芯片生态，Roblox 买 Morpheus 是为了引擎，都不是为了它们的收入。
- **文生游戏不是新平台，而是老平台的新功能。** Roblox Build、蛋仔编辑器、TapTap 制造都把 AI 当成补充创作者的工具。

<a class="anchor" id="gm-2"></a>

## 2 Best Practices

核心发现：世界模型 demo 的热度落在资本市场，平台 AI 功能的热度落在玩家身上。

| 类别 | 代表 demo | 证明了什么 |
|---|---|---|
| 世界模型 | Genie、Marble、Oasis、Odyssey、PixVerse R1 | 画面已经可信；Genie 3 发布当天 Unity 股价跌约 24%，但没有玩家付费 |
| 平台内 AI 功能 | Roblox 4D、蛋仔 AI 编辑器、逆水寒 NPC、堡垒之夜达斯·维达 | 挂在月活过亿的平台上，用户规模现成 |
| 独立 AI 游戏 | Fly、星之低语、Astrocade | 个人开发者能赚钱，Fly 17 天 ARR 100 万美元（自报），但不可复制 |

<!--DEMOS:game-->

<div class="gal-grid">
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=YxkGdX4WIBE" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/game-00.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">谷歌Genie世界</div><div class="mk-by">Google DeepMind</div><div class="gal-cap">Genie 3 驱动，一句话或一张图生成可实时走动、可改写的交互世界</div><div class="mk-tags"><span class="mk-tech">世界模型</span><span class="mk-heat">发布当天 Unity 跌约24%、Roblox 跌约13%、Take-Two 跌约8%；官方视频68万播放</span><span class="mk-biz">AI Ultra 订阅专享</span></div></div></a>
<a class="gal-card mk-card" href="https://www.worldlabs.ai/blog/marble-world-model" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/game-01.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Marble 世界</div><div class="mk-by">World Labs（李飞飞）</div><div class="gal-cap">文/图/视频生成可编辑、持久的3D世界，导出高斯泼溅与网格直接进引擎</div><div class="mk-tags"><span class="mk-tech">世界模型</span><span class="mk-heat">2026年9月 AMD 宣布以82亿美元全股票收购 World Labs</span><span class="mk-biz">免费~95 美元/月+API</span></div></div></a>
<a class="gal-card mk-card" href="https://www.decart.ai/publications/oasis-interactive-ai-video-game-model" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/game-02.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Decart Oasis</div><div class="mk-by">Decart</div><div class="gal-cap">无引擎逐帧生成的可玩“AI 我的世界”，已迭代到 Oasis 3 实时驾驶仿真</div><div class="mk-tags"><span class="mk-tech">世界模型</span><span class="mk-heat">WSJ 报道亚马逊洽谈约70亿美元收购；“AI Minecraft”视频119万播放</span><span class="mk-biz">API 0.02 美元/秒</span></div></div></a>
<a class="gal-card mk-card" href="https://odyssey.ml/introducing-odyssey-3" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/game-03.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Odyssey-3</div><div class="mk-by">Odyssey</div><div class="gal-cap">同一世界模型可漫游生成世界、玩游戏，还能驱动人形机器人与汽车</div><div class="mk-tags"><span class="mk-tech">世界模型</span><span class="mk-heat">2026-10-08 发布研究预览，Pro 版称 Physics-IQ 66.1 登顶，Flexion 已采用</span><span class="mk-biz">免费预览+企业 API</span></div></div></a>
<a class="gal-card mk-card" href="https://runway.com/research/introducing-gwm-worlds-2" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/game-04.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">GWM Worlds 2</div><div class="mk-by">Runway</div><div class="gal-cap">720p/24fps 可玩世界模型，带同步音频，支持多人与“导演”实时改戏</div><div class="mk-tags"><span class="mk-tech">世界模型</span><span class="mk-heat">官方发布视频6.3万播放，与游戏开发者合作原型</span><span class="mk-biz">研究预览，合作伙伴申请制</span></div></div></a>
<a class="gal-card mk-card" href="https://3d-models.hunyuan.tencent.com/world/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/game-05.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">混元HY-World2</div><div class="mk-by">腾讯混元</div><div class="gal-cap">一句话/一张图生成可漫游3D世界(网格/3DGS)，可直接导入UE/Unity</div><div class="mk-tags"><span class="mk-tech">世界模型</span><span class="mk-heat">GitHub 2.7k star，HuggingFace 权重全开源</span><span class="mk-biz">开源，服务腾讯游戏管线</span></div></div></a>
<a class="gal-card mk-card" href="https://realtime.pixverse.ai/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/game-06.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">PixVerse R1</div><div class="mk-by">爱诗科技 PixVerse</div><div class="gal-cap">把视频变成持续演化的实时世界，1~4步采样即时响应，已迭代到R2</div><div class="mk-tags"><span class="mk-tech">世界模型</span><span class="mk-heat">平台注册用户超1亿，R1 上线后已迭代到 R2</span><span class="mk-biz">C端免费体验+API</span></div></div></a>
<a class="gal-card mk-card" href="https://www.microsoft.com/en-us/research/articles/whamm-real-time-world-modelling-of-interactive-environments/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/game-07.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">微软 Muse 世界模型</div><div class="mk-by">Microsoft × Xbox</div><div class="gal-cap">由游戏录像训练的世界模型，Copilot 里实时生成可玩《雷神之锤 II》</div><div class="mk-tags"><span class="mk-tech">世界模型</span><span class="mk-heat">论文登 Nature 正刊；Xbox 官方发布片 3 万播放</span><span class="mk-biz">Copilot 公开试玩</span></div></div></a>
<a class="gal-card mk-card" href="https://respawn.outlookindia.com/gaming/gaming-news/cube-3d-powers-robloxs-new-4d-interactive-object-tools" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/game-08.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Roblox 4D 生成</div><div class="mk-by">Roblox（Cube 基座模型）</div><div class="gal-cap">玩家一句话生成能开的车、能飞的龙，物体自带可交互部件</div><div class="mk-tags"><span class="mk-tech">原生 3D 生成</span><span class="mk-heat">Wish Master 内玩家生成16万+物体，使用者平均时长+64%</span><span class="mk-biz">开放 Beta+Studio API</span></div></div></a>
<a class="gal-card mk-card" href="https://gamesbeat.com/roblox-reality-brings-greater-realism-to-roblox-graphics/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/game-09.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Roblox写实层</div><div class="mk-by">Roblox</div><div class="gal-cap">引擎管逻辑、视频世界模型管画面，不改代码即把游戏变写实</div><div class="mk-tags"><span class="mk-tech">视频模型</span><span class="mk-heat">RDC 2026 主舞台现场演示，并吸纳 Morpheus 等 AI 团队创始人</span><span class="mk-biz">平台级渲染层，路线图中</span></div></div></a>
<a class="gal-card mk-card" href="https://www.shacknews.com/article/144316/fortnite-darth-vader-ai" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/game-10.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">堡垒之夜AI达斯维达</div><div class="mk-by">Epic Games × Google × ElevenLabs</div><div class="gal-cap">Gemini+詹姆斯·厄尔·琼斯授权AI声线，玩家可语音招募并对话维达</div><div class="mk-tags"><span class="mk-tech">LLM + 语音</span><span class="mk-heat">上线即被诱导爆粗出圈，Asmongold 相关视频126万播放</span><span class="mk-biz">星战联动赛季付费内容</span></div></div></a>
<a class="gal-card mk-card" href="https://www.bilibili.com/video/BV1Fe4y1A78x/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/game-11.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">逆水寒智能NPC</div><div class="mk-by">网易</div><div class="gal-cap">大模型驱动NPC自由对话、互相传播，玩家可“捏”自己的AI门客</div><div class="mk-tags"><span class="mk-tech">LLM NPC</span><span class="mk-heat">官方“游戏GPT”智能NPC视频54万播放；AI智能体生成破4000万</span><span class="mk-biz">MMO 留存与付费抓手</span></div></div></a>
<a class="gal-card mk-card" href="https://www.bilibili.com/video/BV1hEyYBsE3U/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/game-12.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">蛋仔 AI 编辑器</div><div class="mk-by">网易</div><div class="gal-cap">工坊内一句话生成模型/美术，接入 Kimi/DeepSeek/GLM 编玩法</div><div class="mk-tags"><span class="mk-tech">UGC 编辑器</span><span class="mk-heat">月活超1亿、UGC 开发者超4000万、累计地图超2亿张</span><span class="mk-biz">UGC 平台，头部创作者年入千万</span></div></div></a>
<a class="gal-card mk-card" href="https://fly.pieter.com/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/game-13.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Fly 飞行模拟</div><div class="mk-by">Pieter Levels (@levelsio)</div><div class="gal-cap">纯 AI 氛围编程做出的浏览器多人飞行游戏，引爆 vibe coding 游戏潮</div><div class="mk-tags"><span class="mk-tech">three.js + AI 写代码</span><span class="mk-heat">上线17天达成100万美元 ARR（作者自述）</span><span class="mk-biz">游戏内广告+飞机售卖</span></div></div></a>
<a class="gal-card mk-card" href="https://store.steampowered.com/app/3730100/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/game-14.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">星之低语</div><div class="mk-by">Anuttacon（蔡浩宇）</div><div class="gal-cap">无对话树，全程语音与AI宇航员Stella自由交流决定生死</div><div class="mk-tags"><span class="mk-tech">UE5 + LLM</span><span class="mk-heat">Steam 特别好评，1,662 篇评测80%好评</span><span class="mk-biz">Steam/iOS 买断 9.99 美元</span></div></div></a>
<a class="gal-card mk-card" href="https://www.astrocade.com/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/game-15.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Astrocade</div><div class="mk-by">Astrocade</div><div class="gal-cap">用文字提示生成并发布小游戏的社区平台，8个月7.5万+作品</div><div class="mk-tags"><span class="mk-tech">LLM 写游戏代码</span><span class="mk-heat">红杉、Sea 领投5600万美元，自称8个月用户超2000万</span><span class="mk-biz">UGC 平台+创作者分成</span></div></div></a>
</div>

<!--/DEMOS-->

<a class="anchor" id="gm-3"></a>

## 3 Insights

- **世界模型卖不进游戏，因为成本和一致性都不达标。**
  - 成本：每用户小时 1 到 72 美元，消费级游戏还需降本 10 到 100 倍；Genie 单次会话限 60 秒。
  - 一致性：模型没有唯一的状态源，多人游戏无法同步，引擎必须保留。
- **最可能的付费方是仿真，不是玩家。** Waymo 已在 Genie 3 上建驾驶模拟器；Decart、Odyssey、Runway 都转去讲机器人和自动驾驶。
- **供给泛滥压低了单款价值。** Steam 上 AI 游戏占新品约 33%，只拿到 10% 到 27% 的销售额；TapTap 新品同比 +844% 后取消保底曝光。

下一步：给平台供货（Roblox、蛋仔、TapTap 的创作者激励），而不是自建玩家平台。

</div>

<div class="env-view" data-view="ad" data-label="Ad Creative">

<nav class="toc view-toc"><h2>Contents</h2><ul><li class="l2"><a href="#ad-1"><span class="num">1</span> Industry Landscape</a></li><li class="l2"><a href="#ad-2"><span class="num">2</span> Best Practices</a></li><li class="l2"><a href="#ad-3"><span class="num">3</span> Insights</a></li></ul></nav>

快手一个季度由 AIGC 素材带动 40 亿元营销消耗，这是视觉生成里最大的一笔现金流。拿走这笔钱的是投放平台和模型方，不是中间的工具公司。

<a class="anchor" id="ad-1"></a>

## 1 Industry Landscape

核心发现：国内由平台主导，海外由独立应用主导，两边的收入规模接近。

| 公司 | 定位 | 营收 | 估值 | 代表作 |
|---|---|---|---|---|
| 快手 可灵（国内） | 视频模型 + 磁力引擎投放 | 可灵 2026Q2 超 8.5 亿元（[财报](https://technode.global/?p=990300)） | 上市 | 美团《麻烦死了》 |
| 字节 即梦 / 巨量引擎（国内） | 模型 + 投放后台一键生成 | 不单独披露 | — | 巨量即创 |
| 阿里妈妈（国内） | 万相营造商品图、图生视频 | 不单独披露；覆盖约 100 万商家，日省 4000 万元以上（[新浪](https://news.sina.com.cn/o/2025-11-08/doc-infwschz3878925.shtml)） | — | 万相营造 |
| 美图（国内） | 电商设计、口播视频 | 生产力工具 ARR 6.2 亿元（[财报](https://www.meitu.com/zh/media/439)） | 上市 | 美图设计室 |
| MiniMax 海螺（国内） | 视频模型 + 开放平台 | 全公司 2026H1 1.17 亿美元（[财报](https://www.minimax.io/news/minimax-announces-first-half-2026-financial-results-1787744160)） | 上市 | 海螺视频 |
| Higgsfield（海外） | 多模型聚合创意应用 | 年化 10 亿美元（[自报](https://digg.com/ai/5c9uxe03)） | 54 亿美元 | 广告模板 |
| Runway（海外） | 视频模型 | ARR 2 亿美元（[自报](https://www.briefs.co/news/runway-s-arr-jumps-to-200-million-as-ai-video-finds-its-groo/)） | 53 亿美元 | Gen-4.5 |
| HeyGen（海外） | 视频数字人 | ARR 1 亿美元（2025-10 [自报](https://x.com/HeyGen_Official/status/1978903438974161329)） | 5 亿美元（2024） | 数字分身 |
| Synthesia（海外） | 企业视频数字人 | ARR 超 1 亿美元（2025-04 [自报](https://www.arr.club/synthesia)） | 40 亿美元 | 企业培训视频 |
| Arcads（海外） | AI 演员 UGC 广告 | ARR 1000 万美元，8 名员工（2025-11 [自报](https://getlatka.com/blog/arcads-revenue-ceo)） | 种子轮 1600 万美元，估值未披露（[Jones Day](https://www.jonesday.com/en/practices/experience/2025/12/eurazeo-leads-16-million-seed-financing-in-arcadsai)） | UGC 广告 |
| Creatify（海外） | 端到端视频广告 agent | ARR 超 900 万美元（上线 18 个月，自报） | 累计融资 2300 万美元（[TechCrunch](https://techcrunch.com/2025/06/02/former-dreamworks-ceo-jeffrey-katzenberg-co-leads-15-5m-series-a-for-ai-video-ad-platform/)） | 广告视频 agent |
| Photoroom（海外） | 电商商品图 | 约 9400 万美元/年（2024 [估算](https://sacra.com/c/photoroom/)） | 5 亿美元 | 商品图 API |
| Silverside AI（海外） | AI 原生广告工作室 | 未披露 | 未披露 | 可口可乐 2025 圣诞广告 |

数据解读：

- **国内的工具免费，因为平台靠消耗赚钱。** 巨量、磁力、阿里妈妈都把生成按钮塞进投放后台，独立工具很难收费。
- **海外的聚合应用做大，单功能工具出清。** Higgsfield 年化收入一年从 1100 万涨到 10 亿美元（自报）；AdCreative.ai 卖给 Appier，Lalaland、Booth.ai 也已出售。

<a class="anchor" id="ad-2"></a>

## 2 Best Practices

核心发现：挨骂的全是大品牌的节日主片，爆款全是小团队的低成本整活。

| 类别 | 代表 demo | 证明了什么 |
|---|---|---|
| 低成本爆款 | Kalshi、IM8、雪山救狐、纸手机、蜜雪冰城 | 一人到几人、几天交付；Kalshi 工具费不到 2000 美元上了 NBA 总决赛 |
| 品牌大片 | 可口可乐 2024/2025、麦当劳荷兰、玩具反斗城、Svedka | 算力省钱，舆论风险不变；麦当劳 3 天撤片 |
| 获奖创意 | 亨氏 AI 番茄酱、RealReal、美团 | 把「AI 生成」本身当创意点，拿奖不靠画质 |
| 平台量产工具 | 万相营造、Meta 生成广告、Higgsfield 模板 | 素材按亿条生产，钱落在投放平台 |

<!--DEMOS:ad-->

<div class="gal-grid">
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=-QMftwmyW-A" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-00.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Kalshi总决赛广告</div><div class="mk-by">Kalshi × PJ Accetturo（Google Veo 3）</div><div class="gal-cap">1人2-3天、约2000美元，数百次生成挑出15个镜头，上NBA总决赛</div><div class="mk-tags"><span class="mk-tech">视频模型（Veo 3）</span><span class="mk-heat">上线一周在Kalshi的X账号播放超300万；NPR等媒体专题报道</span><span class="mk-biz">预测市场平台·体育赛事投放</span></div></div></a>
<a class="gal-card mk-card" href="https://pjace.beehiiv.com/p/120m-views-in-two-days-how-we-made-our-new-viral-ai-ad-for-david-beckham-s-company-im8" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-07.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">IM8贝克汉姆广告</div><div class="mk-by">IM8（David Beckham）× Genre.ai / PJ Ace（Veo 3 + Kling）</div><div class="gal-cap">致敬《黑客帝国》，Midjourney定帧+Veo3/Kling出片+AI配音</div><div class="mk-tags"><span class="mk-tech">视频模型（Veo 3 + 可灵）</span><span class="mk-heat">IM8 Instagram两天播放1.2亿；同步登陆时代广场</span><span class="mk-biz">保健品牌·社媒爆款</span></div></div></a>
<a class="gal-card mk-card" href="https://www.digitaling.com/articles/1477776.html" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-15.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">雪山救狐无限流广告</div><div class="mk-by">贵州酱板鸭小团队 → 瑞幸/肯德基/淘宝等接龙</div><div class="gal-cap">4人小店用邵氏风 AI 短剧卖鸭，引出数十个品牌官号接龙植入</div><div class="mk-tags"><span class="mk-tech">视频模型</span><span class="mk-heat">全网刷屏约 50 亿播放（极目新闻）</span><span class="mk-biz">食品带货→全行业借梗投放</span></div></div></a>
<a class="gal-card mk-card" href="https://www.bilibili.com/video/BV1tFApzYEPb/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-16.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">纸手机</div><div class="mk-by">WAI 工作室（可灵 3.0）</div><div class="gal-cap">2 分钟长镜头+乡音配音，角色全程一致，央视人民日报转发</div><div class="mk-tags"><span class="mk-tech">视频模型（可灵）</span><span class="mk-heat">B站 462 万播放；全网破亿，入围戛纳</span><span class="mk-biz">可灵官方标杆案例（非品牌片）</span></div></div></a>
<a class="gal-card mk-card" href="https://www.ifanr.com/1645046" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-13.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">蜜雪冰城百变雪王杯</div><div class="mk-by">蜜雪冰城 × 海螺AI（MiniMax）</div><div class="gal-cap">开放雪王IP给用户AI二创，首尾帧技术保证形象一致，线下门店联动</div><div class="mk-tags"><span class="mk-tech">视频模型（海螺）</span><span class="mk-heat">“雪王大战东方明珠”等作品在B站霸榜，爱范儿专题报道</span><span class="mk-biz">新茶饮·IP共创营销</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=yqxaKfMss4Q" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-04.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Artlist超级碗广告</div><div class="mk-by">Artlist（自有AI工具链，内部团队）</div><div class="gal-cap">3天从创意到可播出、成本不到5000美元，用AI戏仿各大品牌广告</div><div class="mk-tags"><span class="mk-tech">视频模型</span><span class="mk-heat">官方YouTube超4300万播放；MediaPost等报道制作周期与成本</span><span class="mk-biz">素材平台·超级碗LX投放</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=Yy6fByUmPuE" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-01.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">可口可乐AI圣诞2025</div><div class="mk-by">Coca-Cola × Silverside / Secret Level</div><div class="gal-cap">连续两年AI重制1995经典卡车片，改拍拟人动物，CMO称约一月完成</div><div class="mk-tags"><span class="mk-tech">视频模型</span><span class="mk-heat">官方YouTube约290万播放；评论区大量差评，被讥为“最好的百事广告”</span><span class="mk-biz">快消巨头·年度节日主片</span></div></div></a>
<a class="gal-card mk-card" href="https://www.adweek.com/creativity/how-coca-colas-ai-holiday-ad-went-from-praise-to-rage/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-02.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">可口可乐AI圣诞2024</div><div class="mk-by">Coca-Cola × Silverside / Secret Level / Wild Card</div><div class="gal-cap">首支全AI重制的头部品牌节日TVC，开启“大牌敢用AI做主片”的先例</div><div class="mk-tags"><span class="mk-tech">视频模型</span><span class="mk-heat">System1美英双市场满分5.9，随后舆论反转为“抽走了节日温度”</span><span class="mk-biz">快消巨头·年度节日主片</span></div></div></a>
<a class="gal-card mk-card" href="https://www.nbcnews.com/world/europe/mcdonalds-ai-generated-christmas-advert-social-media-backlash-rcna248590" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-06.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">麦当劳荷兰AI圣诞片</div><div class="mk-by">McDonald&#x27;s NL × TBWA\Neboko / The Sweetshop</div><div class="gal-cap">45秒全AI节日片，制作方称耗时7周“不是AI把戏而是电影”</div><div class="mk-tags"><span class="mk-tech">视频模型</span><span class="mk-heat">上线3天即因“诡异、无灵魂”遭撤下，NBC等国际媒体报道</span><span class="mk-biz">快餐品牌·节日季投放</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=F_WfIzYGlg4" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-05.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">玩具反斗城Sora品牌片</div><div class="mk-by">Toys&quot;R&quot;Us × Native Foreign（OpenAI Sora）</div><div class="gal-cap">首支用Sora制作的品牌片，几周内把数百次迭代压成二十余个镜头</div><div class="mk-tags"><span class="mk-tech">视频模型（Sora）</span><span class="mk-heat">戛纳狮子节首映；网友批“毫无灵魂”、引发行业争议</span><span class="mk-biz">零售品牌·品牌起源片</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=pkeWRI2yJGM" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-03.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Svedka超级碗广告</div><div class="mk-by">Svedka（Sazerac）× Silverside AI</div><div class="gal-cap">首支“主要由AI生成”的超级碗广告，30秒机器人夜店片几乎全靠提示词完成</div><div class="mk-tags"><span class="mk-tech">视频模型</span><span class="mk-heat">USA Today Ad Meter 2.18/5，超级碗倒数第二；恐怖谷吐槽刷屏</span><span class="mk-biz">酒类品牌·超级碗LX投放</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=LFmpVy6eGXs" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-08.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">亨氏AI番茄酱</div><div class="mk-by">Heinz × Rethink（DALL-E 2）</div><div class="gal-cap">让AI画“番茄酱”结果全像亨氏，首个视觉全由AI生成的户外+平面广告</div><div class="mk-tags"><span class="mk-tech">图像模型（DALL-E 2）</span><span class="mk-heat">8.5亿次自然曝光，价值超媒介投入25倍；多项国际广告奖</span><span class="mk-biz">快消品牌·AI平面/户外</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=m0PudxvAU5c" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-09.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">RealReal戛纳片</div><div class="mk-by">The RealReal × Lipstick（可灵Kling）</div><div class="gal-cap">用可灵保持主角从特写到球场全景的面部与表演一致</div><div class="mk-tags"><span class="mk-tech">视频模型（可灵）</span><span class="mk-heat">2026戛纳狮子节获奖（可灵称共获影视银狮及AI Craft铜狮等3座）</span><span class="mk-biz">奢品二手平台·愚人节战役</span></div></div></a>
<a class="gal-card mk-card" href="https://www.digitaling.com/projects/364587.html" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-12.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">美团《麻烦死了》</div><div class="mk-by">美团 × 木瓜创意 / 一界创意（可灵AI）</div><div class="gal-cap">4人团队2周全AI完成愚人节短片，给“麻烦”办葬礼，质感接近实拍</div><div class="mk-tags"><span class="mk-tech">视频模型（可灵）</span><span class="mk-heat">数英专题专访；36氪称其为今年愚人节少数“整大活”的大厂</span><span class="mk-biz">本地生活·AI助手推广</span></div></div></a>
<a class="gal-card mk-card" href="https://www.bilibili.com/video/BV14QFFeMEkz/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-14.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">阿里妈妈万相营造</div><div class="mk-by">阿里妈妈 万相营造（淘宝星辰大模型）</div><div class="gal-cap">一键生成商品图/模特图/图生视频，FILA换场景1分钟出二三十张图</div><div class="mk-tags"><span class="mk-tech">图像 + 视频模型</span><span class="mk-heat">2025 双 11 淘天全平台 AI 素材 1.5 亿+条</span><span class="mk-biz">电商平台·商家素材生产</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=bfIzDLVQhWE" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-11.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Meta AI生成广告</div><div class="mk-by">Meta Advantage+ creative / Ads Creative Studio</div><div class="gal-cap">静态商品图一键转视频已全面开放，目录商品批量生成视频进入公测</div><div class="mk-tags"><span class="mk-tech">图像模型</span><span class="mk-heat">2026广告周发布；Meta称采纳AI建议的广告主同成本转化+5%</span><span class="mk-biz">平台内置·中小商家投放</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=3rDs6FhFoUQ" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/ad-10.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Higgsfield模板</div><div class="mk-by">Higgsfield AI（AI广告生成平台）</div><div class="gal-cap">三步工作流批量生成超写实产品/UGC广告，代表“模板化AI投放素材”路线</div><div class="mk-tags"><span class="mk-tech">视频模型</span><span class="mk-heat">官方教程YouTube约68.6万播放</span><span class="mk-biz">AI广告SaaS·效果投放素材</span></div></div></a>
</div>

<!--/DEMOS-->

<a class="anchor" id="ad-3"></a>

## 3 Insights

- **算力便宜了，钱仍然花在人身上。** 可口可乐 2025 圣诞片用了约 100 人、1 个月，算力不到成本的 1%；省下的是拍摄和后期，不是创意和修片。
- **国内跑出了新形态：品牌 AI 短剧。** 它不是 30 秒广告，而是品牌自有 IP 的连续剧；每分钟成本 800 到 1500 元，红旗 AI 剧 7600 万播放。
- **效果提升是个位数。** Meta 可控实验里，AI 生成背景只带来 2% 到 3% 的转化提升；「最高 +40%」这类数字都没有样本量。
- **确定性层仍有空位。** 生成模型出画面，价格、字幕、logo、多尺寸改版必须逐像素准确，只能交给模板或代码。

下一步：在投放平台的 agent 生态里卖确定性渲染能力，而不是再做一个生成工具。

</div>

<div class="env-view" data-view="web" data-label="Web 3D">

<nav class="toc view-toc"><h2>Contents</h2><ul><li class="l2"><a href="#wb-1"><span class="num">1</span> Industry Landscape</a></li><li class="l2"><a href="#wb-2"><span class="num">2</span> Best Practices</a></li><li class="l2"><a href="#wb-3"><span class="num">3</span> Insights</a></li></ul></nav>

一个获奖级 3D 品牌站要 10 万美元以上、一支十人团队做几个月；同一时期，three.js 的下载量一年涨了 6.4 倍。Web 3D 的瓶颈正在从「谁能做」变成「谁来付钱」。

<a class="anchor" id="wb-1"></a>

## 1 Industry Landscape

核心发现：Web 3D 是四门生意：品牌站项目、配置器 SaaS、网页游戏门户、挂在交易平台上的 3D（看房、电商），彼此几乎不重叠。

| 公司 | 定位 | 营收 | 估值 | 代表作 |
|---|---|---|---|---|
| 头部 WebGL 工作室（海外）：Lusion、abeto、OFF+BRAND、Resn、Immersive Garden | 3D 互动品牌站，2022 到 2025 年 Awwwards 年度网站全部出自前四家 | 均未披露 | 私有 | Lando Norris 官网、Igloo Inc、Lusion v3、卡地亚 |
| Threekit（海外） | 企业配置器 + 虚拟摄影 | 未披露 | 累计融资约 8010 万加元（[BetaKit](https://betakit.com/ottawa-founded-threekit-raises-43-6-million-cad-to-bolster-product-visualization-tech/)） | Virtual Photographer |
| Zakeke（海外） | Shopify 配置器 SaaS | 59 到 300 美元/月 + 交易抽成 | 未披露 | 定制商品配置器 |
| Spline（海外） | 无代码 Web 3D + AI | 未披露；创作者超 100 万（2023 [自报](https://techcrunch.com/2023/07/13/spline-a-no-code-design-tool-for-creating-3d-assets-raises-15m/)） | 融资 2500 万美元 | Spline 编辑器 |
| PlayCanvas（海外） | Web 引擎 + 高斯点编辑器 | Snap 内部 | Snap 收购 | SuperSplat |
| Poki（海外） | 网页游戏门户 | 未披露；月活超 1 亿，每月 10 亿次游玩（2026-06 [自报](https://poki.com/blog/web-gaming-report-announcement-2026)） | 自筹资金，无外部估值；65 人 | Poki |
| FRVR（海外） | HTML5 即时游戏发行 + AI 做游戏 | 未披露；触达 10 亿玩家（自报） | 2024 年融资 1320 万美元（[自报](https://corp.frvr.com/?p=2084)） | Krunker.io |
| 蚂蚁 Galacean（国内） | 自研 WebGL 引擎 | 集团内部 | — | 支付宝「神奇海洋」 |
| Cocos（国内） | 小游戏引擎，微信内置 | 未披露 | SUD 以 7200 万美元（约 5.1 亿元）全资收购（2025-11 [自报](https://kyodonewsprwire.jp/release/202511128935)） | 微信小游戏 |
| 如视 Realsee（国内） | VR 看房与 3D 空间重建，贝壳旗下 | 不单独披露；3D 空间模型超 5500 万个，服务 3000 多个品牌（2025 年底[自报](https://kyodonewsprwire.jp/index.php/release/202601072092)） | 未独立融资 | 贝壳 VR 看房 |
| 小米汽车（国内） | 官网产品页用 three.js | — | — | SU7 产品页 |

数据解读：

- **品牌站项目的价格高，但集中在不到 10 家工作室。** 产品故事站 2 万到 6 万美元，品牌世界 10 万美元以上；Awwwards 年度网站 2022 到 2025 年依次出自 Resn、Lusion、abeto、OFF+BRAND。
- **配置器是唯一的标准化 SaaS。** 市场约 17 亿美元；Amazon 称点开 3D 的用户转化约 2 倍。
- **网页游戏门户有流量，变现靠广告。** Poki 月活 1 亿、只有 65 人且不融资，不披露收入。
- **规模最大的 Web 3D 不单独收费。** 如视 5500 万个 3D 空间模型、天猫 3D 购都不单独披露收入，因为它们的价值算在房产成交和电商 GMV 里。

<a class="anchor" id="wb-2"></a>

## 2 Best Practices

核心发现：热度最大的 Web 3D 不是获奖品牌站，而是挂在交易和流量入口上的产品：Shopify 黑五地球背后是 146 亿美元销售，Krunker 累计 2 亿玩家，贝壳 VR 房源超 1800 万套。

| 类别 | 代表 demo | 证明了什么 |
|---|---|---|
| 品牌站 | Lando Norris、Igloo Inc、Lusion、卡地亚 | 质感上限已达电影级，但多是工作室自我宣传 |
| 产品与电商 | 小米 SU7/YU7、Shopify 黑五、天猫 3D 购、得物 AR、贝壳 VR、Sketchfab | 3D 挂在下单流程上，热度来自交易本身 |
| 网页游戏 | Krunker、Smash Karts | 免下载即玩，靠广告和内购变现 |
| 科普与文旅 | NASA Eyes、亚运数字火炬手、数字藏经洞、云游长城 | 国家级项目，人次过千万到上亿，付费方是机构 |
| 平台工具 | SuperSplat、Cesium | 卖给开发者的底座，以收购收场 |

<!--DEMOS:web-->

<div class="gal-grid">
<a class="gal-card mk-card" href="https://landonorris.com/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-00.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">兰多·诺里斯官网</div><div class="mk-by">OFF+BRAND × Lando Norris</div><div class="gal-cap">three.js 3D 头盔随滚动变形，车手品牌做成沉浸叙事</div><div class="mk-tags"><span class="mk-tech">three.js</span><span class="mk-heat">Awwwards 2025 年度网站 + 用户选择奖</span><span class="mk-biz">F1 车手个人品牌官网</span></div></div></a>
<a class="gal-card mk-card" href="https://www.igloo.inc/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-01.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Igloo Inc 冰川</div><div class="mk-by">abeto × Igloo Inc（Pudgy Penguins 母公司）</div><div class="gal-cap">程序化冰晶+Houdini 体积进浏览器，质感近离线渲染</div><div class="mk-tags"><span class="mk-tech">WebGL</span><span class="mk-heat">Awwwards 2024 年度网站 + 开发者年度网站</span><span class="mk-biz">Web3 集团品牌官网</span></div></div></a>
<a class="gal-card mk-card" href="https://messenger.abeto.co/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-02.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">信使小星球</div><div class="mk-by">abeto（工作室自研作品）</div><div class="gal-cap">浏览器多人联网小星球，three.js+WebSocket</div><div class="mk-tags"><span class="mk-tech">three.js</span><span class="mk-heat">Awwwards 2025 开发者年度网站</span><span class="mk-biz">工作室品牌作品/接单名片</span></div></div></a>
<a class="gal-card mk-card" href="https://lusion.co/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-03.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Lusion v3 官网</div><div class="mk-by">Lusion（布里斯托）</div><div class="gal-cap">three.js 流体粒子交互贯穿全站，动效满分</div><div class="mk-tags"><span class="mk-tech">three.js</span><span class="mk-heat">Awwwards 2023 年度网站 + 开发者年度网站</span><span class="mk-biz">3D 交互工作室获客官网</span></div></div></a>
<a class="gal-card mk-card" href="https://kprverse.com/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-04.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">KPR 元宇宙</div><div class="mk-by">Resn × KPR</div><div class="gal-cap">电影级 3D 世界观叙事，把藏品包装成可探索宇宙</div><div class="mk-tags"><span class="mk-tech">WebGL</span><span class="mk-heat">Awwwards 2022 年度网站</span><span class="mk-biz">Web3 藏品 IP 宣发</span></div></div></a>
<a class="gal-card mk-card" href="https://bruno-simon.com/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-05.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Bruno 开车作品集</div><div class="mk-by">Bruno Simon（个人作品）</div><div class="gal-cap">开车逛作品集：TSL+WebGPU、物理引擎、7.8万草叶</div><div class="mk-tags"><span class="mk-tech">three.js</span><span class="mk-heat">Awwwards 2026 年 1 月月度网站</span><span class="mk-biz">独立开发者作品集/接单</span></div></div></a>
<a class="gal-card mk-card" href="https://oryzo.ai/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-06.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Oryzo AI 杯垫</div><div class="mk-by">Lusion（虚构产品发布）</div><div class="gal-cap">发布会级 3D 产品片恶搞 AI 硬件，魔改 three.js</div><div class="mk-tags"><span class="mk-tech">three.js</span><span class="mk-heat">Awwwards 2026 年 4 月月度网站</span><span class="mk-biz">工作室营销（产品发布范式）</span></div></div></a>
<a class="gal-card mk-card" href="https://www.shopify.com/editions/winter2026" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-07.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Shopify 冬季版</div><div class="mk-by">Shopify Design × Shopify</div><div class="gal-cap">文艺复兴 3D 画廊装下 150+ 项更新，日志变展览</div><div class="mk-tags"><span class="mk-tech">WebGL</span><span class="mk-heat">Awwwards 2026 年 2 月月度网站</span><span class="mk-biz">SaaS 季度产品发布</span></div></div></a>
<a class="gal-card mk-card" href="https://www.gq.com/sponsored/story/the-extraordinary-lab" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-08.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">GQ×爱彼实验室</div><div class="mk-by">Immersive Garden × GQ / Audemars Piguet</div><div class="gal-cap">WebGL 沉浸式腕表软文，奢侈品内容营销新样板</div><div class="mk-tags"><span class="mk-tech">WebGL</span><span class="mk-heat">Awwwards 2026 年 3 月月度网站</span><span class="mk-biz">奢侈腕表媒体赞助内容</span></div></div></a>
<a class="gal-card mk-card" href="https://cartier-waw-0225.dev.60fps.fr/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-09.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">卡地亚钟表展</div><div class="mk-by">Immersive Garden + 60fps × Cartier</div><div class="gal-cap">WebGL 实时渲染金属宝石新表，线上复刻表展</div><div class="mk-tags"><span class="mk-tech">WebGL</span><span class="mk-heat">Awwwards 2025 年 8 月月度网站</span><span class="mk-biz">卡地亚日内瓦表展新品发布</span></div></div></a>
<a class="gal-card mk-card" href="https://www.xiaomiev.com/su7" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-13.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">小米 SU7 官网</div><div class="mk-by">小米汽车</div><div class="gal-cap">国内爆款车型官网内嵌 three.js，长滚动叙事</div><div class="mk-tags"><span class="mk-tech">three.js</span><span class="mk-heat">一代 SU7 交付超 38.1 万辆（雷军微博，维基转引）</span><span class="mk-biz">新车上市产品页</span></div></div></a>
<a class="gal-card mk-card" href="https://www.xiaomiev.com/yu7" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-17.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">小米 YU7 官网</div><div class="mk-by">小米汽车</div><div class="gal-cap">three.js+Draco 模型嵌入长滚动页，与 SU7 同套管线</div><div class="mk-tags"><span class="mk-tech">three.js</span><span class="mk-heat">发布 18 小时锁单 24 万台；1 小时预订 28.9 万</span><span class="mk-biz">新车上市产品页</span></div></div></a>
<a class="gal-card mk-card" href="https://bfcm.shopify.com/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-16.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Shopify黑五地球</div><div class="mk-by">Shopify</div><div class="gal-cap">黑五实时订单在 3D 地球上飞线，2025 版塞进弹球机</div><div class="mk-tags"><span class="mk-tech">three.js</span><span class="mk-heat">黑五地球直播 146 亿美元销售（官方）</span><span class="mk-biz">电商大促实时数据营销</span></div></div></a>
<a class="gal-card mk-card" href="https://www.bilibili.com/video/BV1aV411a7VV/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-21.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">天猫3D购样板间</div><div class="mk-by">阿里巴巴·天猫</div><div class="gal-cap">天猫把宜家等门店1:1复刻成3D样板间，手机里可逛可买</div><div class="mk-tags"><span class="mk-tech">移动端 3D</span><span class="mk-heat">卡萨帝冰箱停留时长超300%（中证网）</span><span class="mk-biz">电商大促 3D 导购</span></div></div></a>
<a class="gal-card mk-card" href="https://www.bilibili.com/video/BV17Y41137fY/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-23.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">得物AR试鞋</div><div class="mk-by">得物</div><div class="gal-cap">App内用3D球鞋模型做AR上脚试穿，另有3D陀螺仪看鞋</div><div class="mk-tags"><span class="mk-tech">AR</span><span class="mk-heat">每天助超30%用户决策（投资界）</span><span class="mk-biz">潮流电商 AR 试穿</span></div></div></a>
<a class="gal-card mk-card" href="https://www.bilibili.com/video/BV1J24y1q7Zg/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-22.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">贝壳VR看房</div><div class="mk-by">贝壳找房·如视</div><div class="gal-cap">扫描真实房屋重建三维模型，网页与App内漫游看房</div><div class="mk-tags"><span class="mk-tech">VR 全景 + 三维重建</span><span class="mk-heat">VR房屋模型超1800万套（蓝鲸财经）</span><span class="mk-biz">房产交易线上带看</span></div></div></a>
<a class="gal-card mk-card" href="https://sketchfab.com/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-14.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Sketchfab 3D 嵌入</div><div class="mk-by">Sketchfab（KitBash 旗下）</div><div class="gal-cap">品牌把 3D 商品模型一行 iframe 嵌进官网与电商详情页</div><div class="mk-tags"><span class="mk-tech">WebGL</span><span class="mk-heat">被 Epic 收购时 500 万用户（CG Channel）</span><span class="mk-biz">订阅+模型商店</span></div></div></a>
<a class="gal-card mk-card" href="https://krunker.io/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-10.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Krunker 浏览器射击</div><div class="mk-by">Krunker（FRVR 旗下）</div><div class="gal-cap">免下载即开的浏览器 3D 多人 FPS，支持全量模组与创意工坊</div><div class="mk-tags"><span class="mk-tech">WebGL</span><span class="mk-heat">累计 2 亿玩家（FRVR 收购公告）</span><span class="mk-biz">内购+广告，2022 被收购</span></div></div></a>
<a class="gal-card mk-card" href="https://smashkarts.io/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-24.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Smash Karts 卡丁车</div><div class="mk-by">Tall Team</div><div class="gal-cap">浏览器即开的 3D 多人卡丁车大乱斗，复活间隙插广告变现</div><div class="mk-tags"><span class="mk-tech">WebGL</span><span class="mk-heat">累计 3000 万+玩家（Google 案例）</span><span class="mk-biz">网页游戏广告变现</span></div></div></a>
<a class="gal-card mk-card" href="https://eyes.nasa.gov/apps/solar-system/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-12.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">NASA 太阳系之眼</div><div class="mk-by">NASA / JPL</div><div class="gal-cap">按真实星历实时渲染太阳系与探测器，可回放</div><div class="mk-tags"><span class="mk-tech">three.js</span><span class="mk-heat">好奇号着陆 3 天 120 万访问（NASA）</span><span class="mk-biz">航天机构科普平台</span></div></div></a>
<a class="gal-card mk-card" href="https://galacean.antgroup.com/engine/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-18.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">亚运数字火炬手</div><div class="mk-by">蚂蚁集团 Galacean × 杭州亚组委</div><div class="gal-cap">支付宝内 Web3D 互动，覆盖 97% 机型；数字人与真人同步点燃主火炬</div><div class="mk-tags"><span class="mk-tech">Galacean</span><span class="mk-heat">参与人数破 1 亿（人民日报）；亚运史上首个数字点火</span><span class="mk-biz">国家级赛事×超级 App 营销</span></div></div></a>
<a class="gal-card mk-card" href="https://cave17.e-dunhuang.com/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-19.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">数字藏经洞</div><div class="mk-by">敦煌研究院 × 腾讯</div><div class="gal-cap">游戏引擎 9 亿面模型 1:1 复刻 17 窟，网页端云渲染即点即玩</div><div class="mk-tags"><span class="mk-tech">云渲染</span><span class="mk-heat">上线一周 1400 万用户；获联合国教科文组织创新案例奖</span><span class="mk-biz">文博数字化·云游戏技术输出</span></div></div></a>
<a class="gal-card mk-card" href="https://www.bilibili.com/video/BV1ja411s72V/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-20.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">云游长城</div><div class="mk-by">腾讯游戏·中国文物保护基金会</div><div class="gal-cap">小程序里毫米级数字长城，云游戏渲染可爬可修</div><div class="mk-tags"><span class="mk-tech">云渲染</span><span class="mk-heat">小程序浏览量破4000万人次（深圳新闻网）</span><span class="mk-biz">文旅公益 品牌传播</span></div></div></a>
<a class="gal-card mk-card" href="https://superspl.at/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-15.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">SuperSplat</div><div class="mk-by">PlayCanvas（Snap 旗下）</div><div class="gal-cap">浏览器编辑发布高斯泼溅，WebGPU+流式 LOD</div><div class="mk-tags"><span class="mk-tech">3DGS + WebGPU</span><span class="mk-heat">Editor 3.0 重写上 WebGPU；Rimowa 等电商在用</span><span class="mk-biz">高斯泼溅托管/电商数字孪生</span></div></div></a>
<a class="gal-card mk-card" href="https://cesium.com/platform/cesium-ion/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/web-11.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Cesium 3D 地球</div><div class="mk-by">Cesium（Bentley 旗下）</div><div class="gal-cap">浏览器里流式加载全球地形与谷歌写实 3D 城市瓦片</div><div class="mk-tags"><span class="mk-tech">Cesium / 3D Tiles</span><span class="mk-heat">被 Bentley 收购；月活设备 100 万+（官方稿）</span><span class="mk-biz">Cesium ion 订阅</span></div></div></a>
</div>

<!--/DEMOS-->

<a class="anchor" id="wb-3"></a>

## 3 Insights

- **AI 写代码改变的是中腰部，不是头部。** 获奖作品靠手艺，代码生成替代不了；但 2 万到 6 万美元的产品页和配置器有固定套路，代码生成可以把成本压下来。
- **大奖不等于大生意。** 获奖站多是工作室给自己做的宣传，Lusion v3、Bruno Simon、Oryzo 都是；常见的付费项目预算只有 1 万到 5 万美元。
- **WebGPU 还在炫技阶段。** 浏览器覆盖 88%，但生产站点仍以 WebGL 为主；3DGS 是第一个 WebGPU 优先的生产场景。
- **下载量不等于开发者数。** npm 数字含 CI 和机器安装，「AI 推动增长」是推断，不是测量。

下一步：用 visual coder 批量做中腰部产品页和配置器，以项目单价下降幅度衡量效果。

</div>

<div class="env-view" data-view="industry" data-label="Industrial 3D">

<nav class="toc view-toc"><h2>Contents</h2><ul><li class="l2"><a href="#in-1"><span class="num">1</span> Industry Landscape</a></li><li class="l2"><a href="#in-2"><span class="num">2</span> Best Practices</a></li><li class="l2"><a href="#in-3"><span class="num">3</span> Insights</a></li></ul></nav>

Unity 的引擎收入一年只涨 1%，光轮智能一个季度新签 5.5 亿元。产业 3D 不是一个增长市场，而是一个存量市场里的两个增量。

产业 3D 指游戏和营销之外的 3D：车机、虚拟制片、数字人、数字孪生、仿真数据、建筑设计、CAD。

<a class="anchor" id="in-1"></a>

## 1 Industry Landscape

核心发现：上市公司多、增长平；两个增量是中国车机座舱和具身合成数据。

| 公司 | 定位 | 营收 | 估值 | 代表作 |
|---|---|---|---|---|
| Epic Unreal（海外） | 引擎：车机、虚拟制片、数字人 | 不拆分非游戏收入 | 私有（腾讯持股 28%） | Rivian 车机、MetaHuman |
| Unity（海外） | 引擎 + Unity Industry | 2025 年 18.5 亿美元（[10-K](https://www.sec.gov/Archives/edgar/data/1810806/000181080626000011/unity-20251231.htm)） | 上市 | 丰田下一代 HMI |
| Unity 中国 团结引擎（国内） | 车机座舱、小游戏、鸿蒙 | 不单独披露 | 10 亿美元（2024，[36Kr](https://36kr.jp/287636/)） | 零跑 C10 座舱 |
| NVIDIA（海外） | Omniverse 孪生、Isaac 仿真、Cosmos | 不拆分 | 上市 | 宝马虚拟工厂 |
| Bentley（海外） | 基建工程软件 + Cesium 3D Tiles | 2025 财年 15.02 亿美元，+11%（[财报](https://finance.yahoo.com/news/bentley-systems-q4-earnings-call-170635732.html)） | 上市 | iTwin 基建孪生 |
| Applied Intuition（海外） | 自动驾驶仿真、国防 | 约 8.3 亿美元/年（[估算](https://sacra.com/research/applied-intuition-at-830m-year/)） | 150 亿美元 | 车企仿真平台 |
| 光轮智能（国内） | 具身仿真资产与合成数据 | 2026Q1 新签 5.5 亿元（[自报](https://autonews.gasgoo.com/articles/market-industry/2069795751096725504)） | 融资超 20 亿元 | 仿真资产库 |
| 群核科技（国内） | 酷家乐设计 SaaS + 合成数据 | 2025 年 8.2 亿元，毛利 82%（[财报](https://wallstreetcn.com/articles/3769573)） | 上市 | InteriorGS |
| 51WORLD（国内） | 数字孪生底座 | 2024 年 2.87 亿元；2026H1 约 1.24 亿元，+130%（[Bamboo Works](https://thebambooworks.com/zh/tag/%e4%ba%94%e4%b8%80%e8%a6%96%e7%95%8c/)） | 上市 | 孪生港口 |
| 凡拓数创（国内） | 3D 可视化与展厅集成 | 2025 年 6.31 亿元，+73%，毛利约 23.5%，亏损 1.33 亿元（[财报](https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/301313/ctrl/2025/displaytype/4.phtml)） | 上市 | 数字展厅 |
| Matterport / CoStar（海外） | 实景采集看房 | 10 个月贡献 1.47 亿美元（[10-K](https://www.sec.gov/Archives/edgar/data/1057352/000105735226000020/csgp-20251231.htm)） | CoStar 16 亿美元收购 | 3D 看房 |
| 爱奇艺（国内） | 横店 LED 虚拟制片棚 | 虚拟制片项目同比 +50% | 上市 | 《大梦归离》 |
| Adam（海外） | Text-to-CAD，CAD-as-code | 未披露；用户已生成 100 万+ 模型（[自报](https://adam.new/seed)） | 种子轮 410 万美元 | Adam |

数据解读：

- **存量业务增长平。** Unity 引擎板块同比 +1%；群核首次盈利，但 2026H1 收入只增 1.5%。
- **增量集中在两处。** 团结引擎自报覆盖 77 款量产车型；光轮单季新签额是群核同类业务的数十倍。

<a class="anchor" id="in-2"></a>

## 2 Best Practices

核心发现：产业 3D 的 demo 不是展示品，而是生产工具本身。

| 类别 | 代表 demo | 证明了什么 |
|---|---|---|
| 内容生产 | 曼达洛人、爱奇艺横店棚、MetaHuman、HeyGen、D5 | 3D 替代实拍和后期，按棚天或订阅收费 |
| 车与工厂 | Rivian 车机、团结引擎座舱、宝马虚拟工厂、51WORLD 港口 | 引擎进入量产车和产线规划，按授权或项目收费 |
| 仿真与采集 | Cosmos、Waymo、光轮、InteriorGS、Matterport | 3D 场景变成训练数据和房产孪生，付费方是机器人、自动驾驶和地产平台 |
| CAD | Adam | 参数化代码直接作为交付物 |

<!--DEMOS:industry-->

<div class="gal-grid">
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=gUnxzVOs3rk" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/industry-00.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">曼达洛人虚拟制片</div><div class="mk-by">ILM（工业光魔）</div><div class="gal-cap">LED 环幕+UE 实时渲染替代绿幕，开启 StageCraft 虚拟制片</div><div class="mk-tags"><span class="mk-tech">UE + LED 墙</span><span class="mk-heat">ILM 官方幕后片 YouTube 247 万播放</span><span class="mk-biz">StageCraft 棚租/VFX</span></div></div></a>
<a class="gal-card mk-card" href="https://www.ithome.com/0/857/782.htm" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/industry-01.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">爱奇艺横店虚拟棚</div><div class="mk-by">爱奇艺 IQStage</div><div class="gal-cap">500㎡ LED 幕墙+旋转地台，《大梦归离》95% 画面免后期</div><div class="mk-tags"><span class="mk-tech">UE + LED 墙</span><span class="mk-heat">降价至最低 3.5 万元/天，虚拟制作项目数同比 +50%</span><span class="mk-biz">虚拟棚按天租赁</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=pnaKyc3mQVk" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/industry-04.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">MetaHuman动画</div><div class="mk-by">Epic Games</div><div class="gal-cap">一部 iPhone 拍摄即可驱动影视级数字人面部动画，分钟级出片</div><div class="mk-tags"><span class="mk-tech">UE MetaHuman</span><span class="mk-heat">State of Unreal 2023 演示，IGN 转载 235 万播放</span><span class="mk-biz">随 UE 授权免费捆绑</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=yKhZb4Ny_I0" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/industry-05.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">HeyGen 数字分身</div><div class="mk-by">HeyGen</div><div class="gal-cap">拍一段视频即克隆本人形象与声音，生成多语种口播数字人</div><div class="mk-tags"><span class="mk-tech">视频模型</span><span class="mk-heat">官方 2026 教程片 1 个月 407 万播放</span><span class="mk-biz">SaaS 订阅/按分钟计费</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=yKnyqmYAxYY" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/industry-14.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">D5 年度建筑动画</div><div class="mk-by">D5 Render（大五）</div><div class="gal-cap">实时光追渲染建筑/室内动画，效果图级画质即时出片</div><div class="mk-tags"><span class="mk-tech">实时光追渲染</span><span class="mk-heat">官方 2024 年度作品集 21.5 万播放</span><span class="mk-biz">渲染器订阅</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=dYk7byKHSRw" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/industry-02.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Rivian 电子梦</div><div class="mk-by">Epic Games × Rivian</div><div class="gal-cap">GDC 主舞台 UE5.2 程序化丛林中驾驶 R1T，影视级车辆实时渲染</div><div class="mk-tags"><span class="mk-tech">UE 车机</span><span class="mk-heat">State of Unreal GDC 2023 发布，整场演示 136 万播放</span><span class="mk-biz">UE 车载 HMI 授权</span></div></div></a>
<a class="gal-card mk-card" href="https://www.bilibili.com/video/BV1M142127wt/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/industry-03.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">团结引擎3D座舱</div><div class="mk-by">Unity 中国 团结引擎（零跑等车企量产）</div><div class="gal-cap">实时3D车模+场景化HMI，零跑 C10/C16 已量产上车</div><div class="mk-tags"><span class="mk-tech">团结引擎</span><span class="mk-heat">Unity 中国自称合作 35 家车企/77 款量产车，占国内座舱约 85%</span><span class="mk-biz">引擎授权 + 座舱定制开发</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=g78YHYXXils" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/industry-07.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">宝马虚拟工厂</div><div class="mk-by">BMW Group × NVIDIA</div><div class="gal-cap">德布勒森新工厂开工前先在 Omniverse 全尺寸建成并规划产线</div><div class="mk-tags"><span class="mk-tech">Omniverse</span><span class="mk-heat">「全球首座虚拟工厂」官方发布 14.6 万播放</span><span class="mk-biz">车企产线规划内部部署</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=IuWk0C3MzBQ" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/industry-06.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">机器人车队数字孪生</div><div class="mk-by">NVIDIA Omniverse（Mega）</div><div class="gal-cap">在仓库/工厂孪生体里同时仿真整支机器人车队再上线</div><div class="mk-tags"><span class="mk-tech">Omniverse</span><span class="mk-heat">NVIDIA 官方视频 103 万播放</span><span class="mk-biz">Omniverse 企业授权</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=H0leNFO1ZrA" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/industry-08.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">51WORLD 孪生港口</div><div class="mk-by">51WORLD</div><div class="gal-cap">港口吊机、集卡、船舶全要素实时孪生，城市级可视化大屏</div><div class="mk-tags"><span class="mk-tech">UE 孪生</span><span class="mk-heat">港股上市被称「物理 AI 第一股」，市值 153 亿</span><span class="mk-biz">政企项目制交付</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=9Uch931cDx8" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/industry-09.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Cosmos 世界模型</div><div class="mk-by">NVIDIA</div><div class="gal-cap">物理 AI 世界基础模型，批量生成机器人/自驾合成训练视频</div><div class="mk-tags"><span class="mk-tech">世界模型</span><span class="mk-heat">CES 2025 发布片 72.9 万播放，1X/Figure/Uber 等早期采用</span><span class="mk-biz">开放权重+企业授权</span></div></div></a>
<a class="gal-card mk-card" href="https://waymo.com/blog/2026/02/the-waymo-world-model-a-new-frontier-for-autonomous-driving-simulation" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/industry-10.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Waymo 世界模型</div><div class="mk-by">Waymo × Google DeepMind</div><div class="gal-cap">基于 Genie 3 以文字提示生成可驾驶的长尾极端场景</div><div class="mk-tags"><span class="mk-tech">世界模型</span><span class="mk-heat">底座 Genie 3 发布片 72 万播放</span><span class="mk-biz">Robotaxi 自用仿真</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=mqEBWpq3VgA" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/industry-11.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">光轮仿真数据</div><div class="mk-by">光轮智能 Lightwheel</div><div class="gal-cap">SimReady 资产 + Isaac Sim 物理仿真，为具身模型批量造数据</div><div class="mk-tags"><span class="mk-tech">Isaac 仿真</span><span class="mk-heat">2026-03 融资 10 亿元，NVIDIA 官方案例片 2.5 万播放</span><span class="mk-biz">合成数据/评测即服务</span></div></div></a>
<a class="gal-card mk-card" href="https://huggingface.co/datasets/spatialverse/InteriorGS" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/industry-12.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">InteriorGS</div><div class="mk-by">群核科技 SpatialVerse</div><div class="gal-cap">1000 个室内 3DGS 场景、55 万物体标注，供空间智能训练</div><div class="mk-tags"><span class="mk-tech">3DGS</span><span class="mk-heat">Hugging Face 205 赞、月下载 2390</span><span class="mk-biz">开源数据引流仿真服务</span></div></div></a>
<a class="gal-card mk-card" href="https://matterport.com/" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/industry-13.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Matterport 数字孪生</div><div class="mk-by">Matterport（CoStar 旗下）</div><div class="gal-cap">手机或相机扫一遍，生成可在浏览器漫游的房屋/场馆 3D 孪生</div><div class="mk-tags"><span class="mk-tech">3D 扫描重建</span><span class="mk-heat">CoStar 16 亿美元收购；官方介绍片 1100 万播放</span><span class="mk-biz">房产与建筑孪生订阅</span></div></div></a>
<a class="gal-card mk-card" href="https://www.youtube.com/watch?v=EHu6Vrqo69A" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/industry-15.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 打开原站</span></div><div class="gal-meta"><div class="gal-cn">Adam 文本生 CAD</div><div class="mk-by">Adam（YC W25）</div><div class="gal-cap">一句话生成可编辑参数化零件，CAD 即代码的 AI 机械工程师</div><div class="mk-tags"><span class="mk-tech">LLM 写 CAD 代码</span><span class="mk-heat">410 万美元种子轮，用户已生成 100 万+ 模型</span><span class="mk-biz">Fusion/Onshape 插件订阅</span></div></div></a>
</div>

<!--/DEMOS-->

<a class="anchor" id="in-3"></a>

## 3 Insights

- **具身数据是增长最快的付费点。** 因为机器人缺少真实交互数据，实验室只能用仿真数据预训练；银河通用用十亿帧仿真数据训练抓取模型。
- **3DGS 打通了采集和仿真。** NVIDIA NuRec、群核 InteriorGS 把扫描数据直接变成可仿真的场景，省掉人工建模。
- **CAD 正在收敛到代码表示。** Zoo、Adam、开源 text-to-cad 都押同一件事：通用大模型写参数化代码，再截图自检。
- **两类存量生意在下滑。**
  - 中国孪生是低毛利项目制：51WORLD 毛利从 65% 降到 41%，凡拓数创毛利约 23% 且亏损。
  - 虚拟制片承诺的 10 倍降本没有兑现：Sony 关停 Pixomondo，横店报价一年降约 78%。

下一步：盯具身合成数据和 CAD-as-code，这两处同时满足「付费方已存在」和「代码就是交付物」。

</div>

<div class="env-view" data-view="webdev" data-label="WebDev Gallery">

<nav class="toc view-toc"><h2>Contents</h2><ul><li class="l2"><a href="#xw-1"><span class="num">1</span> Scene Taxonomy</a></li><li class="l2"><a href="#xw-2"><span class="num">2</span> Gallery</a></li><li class="l3"><a href="#xw-s1"><span class="num">2.1</span> 个人作品集与简历站</a></li><li class="l3"><a href="#xw-s2"><span class="num">2.2</span> 动效官网与网页复刻</a></li><li class="l3"><a href="#xw-s3"><span class="num">2.3</span> 3D 交互小世界</a></li><li class="l3"><a href="#xw-s4"><span class="num">2.4</span> HTML 汇报与 PPT</a></li><li class="l3"><a href="#xw-s5"><span class="num">2.5</span> 网页与 H5 小游戏</a></li><li class="l3"><a href="#xw-s6"><span class="num">2.6</span> 运营活动页与 H5</a></li><li class="l3"><a href="#xw-s7"><span class="num">2.7</span> 数据大屏与内部工具</a></li><li class="l3"><a href="#xw-s8"><span class="num">2.8</span> 交互科普与课件</a></li><li class="l3"><a href="#xw-s9"><span class="num">2.9</span> 数字策展与文博</a></li><li class="l3"><a href="#xw-s10"><span class="num">2.10</span> 小程序与独立站</a></li><li class="l2"><a href="#xw-3"><span class="num">3</span> Insights</a></li><li class="l2"><a href="#xw-4"><span class="num">4</span> Data Caliber</a></li></ul></nav>

小红书上 webdev 赞最高的一条，标题是「Vibe Coding 进化成 Visual Coding 了」：丢给 AI 一张截图和一段录屏，像素级复刻网页，1.9 万赞、2.5 万收藏。本页从 25 个关键词、744 条笔记里，按场景挑出 43 个最佳实践。

<a class="anchor" id="xw-1"></a>

## 1 Scene Taxonomy

核心发现：小红书上的 webdev 大多是「做给自己用」：作品集、汇报、给孩子的网站。付费方要么是创作者本人，要么根本没有；能直接看到收入的只有小游戏和小程序，而且数字很小。

| 场景 | 领域 | 常用项目 | 最热案例 | 小红书热度 |
|---|---|---|---|---|
| 个人作品集与简历站 | 求职 · 个人品牌 | three.js、Codex、Claude Code | Kia 把作品集做成泳池 | 赞 10,996 · 藏 6,270 |
| 动效官网与网页复刻 | 品牌官网 · 落地页 | Kimi K2.5、Codex、Claude Code、设计 skill | 赛文乔伊 截图 + 录屏复刻 | 赞 19,318 · 藏 25,322 |
| 3D 交互小世界 | 创意编程 · 内容传播 | three.js、p5.js、Tripo API | Ray 的果冻海岛 Jelly Planet | 赞 11,316 · 藏 3,698 |
| HTML 汇报与 PPT | 职场汇报 · 科研组会 | Claude Design、Codex、TapNow | 交互式 HTML 汇报 | 赞 7,436 · 藏 7,503 |
| 网页与 H5 小游戏 | 游戏 · 粉丝运营 | Codex、Kimi Code、Tripo | 「AI 的 4399」小游戏合集 | 赞 4,154 · 藏 3,588 |
| 运营活动页与 H5 | 电商 · 节日营销 | 即梦、Figma、AI 生图 | Figma + 即梦角色动效 | 赞 5,143 · 藏 5,856 |
| 数据大屏与内部工具 | 企业 B 端 | Cursor、Codex、Lovart | 3 小时搭舆情监控平台 | 赞 1,175 · 藏 1,447 |
| 交互科普与课件 | 教育 · 科普 | Codex、anatomy skill | 人体拆成 2234 块的 3D 站 | 赞 7,575 · 藏 4,559 |
| 数字策展与文博 | 文博 · 文旅 | Gemini、Codex、pretext | 古迹 3D + 文字实时绕排 | 赞 2,499 · 藏 3,339 |
| 小程序与独立站 | 独立开发 · 出海 | Lovable、微信小程序、TapTap | 一个人做网站月入 1.2 万美元（标题自述） | 赞 2,963 · 藏 3,635 |

工具份额（744 条 webdev 笔记，按标题和正文提及计）：

| 项目 | 提及笔记 | 赞合计 |
|---|---|---|
| Codex | 58 | 68,608 |
| Claude / Opus / Sonnet | 57 | 58,186 |
| three.js | 42 | 46,442 |
| GPT-6 / Astra | 30 | 40,722 |
| HTML PPT | 37 | 34,683 |
| 小程序 | 34 | 24,799 |
| Cursor | 12 | 17,226 |
| Gemini | 19 | 7,944 |
| Kimi | 6 | 7,691 |
| GSAP | 18 | 3,676 |
| Lovable | 27 | 2,817 |
| 扣子 / Coze | 15 | 1,725 |
| v0 | 9 | 224 |

数据解读：

- **Codex、Claude、three.js 三家占了大头。** 模型侧是 Codex 和 Claude，渲染侧是 three.js；3D 交互小世界这一组 5 张卡里 4 张用 three.js。
- **海外热门的 app builder 在小红书没有用户基础。** Lovable 被提到 27 次，但赞合计只有 2,817，大多出现在「工具清单」里；v0 几乎为零。
- **HTML 汇报是收藏型刚需。** 这一组的收藏数接近或超过点赞（Claude Design 那条赞 6,417、藏 1.06 万），说明大家是存起来照着做。

<a class="anchor" id="xw-2"></a>

## 2 Gallery

每张卡：封面链到小红书原帖；项目名链到官网（带 logo）；下面依次是示例、谁在用、领域和热度。转述海外案例的注明原作者。

<!--XG:webdev-->

<a class="anchor" id="xw-s1"></a>

### 个人作品集与简历站

小红书 webdev 内容里量最大的一类，付费方是求职者自己。做法很统一：找 5–6 个参考站丢给 AI，three.js 做 3D，GitHub + Cloudflare 免费部署。

<div class="gal-grid">
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6ad4f792000000001400c800?xsec_token=ABvwejsjldc9bIaf2J9wNRhpzdm4F_gCy-OpPEWpupEeU=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6ad4f792000000001400c800.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://threejs.org/" target="_blank" rel="noopener"><img src="posters/logo-threejs.png" alt="">three.js + Claude Code</a><div class="gal-cap"><b>示例</b>作品集做成泳池：每个项目是漂在水上的黏土图标，访客留言变成云的影子，还有夜间版</div><div class="xg-row"><b>谁在用</b>Kia（纽约 ITP 交互专业）</div><div class="mk-tags"><span class="mk-biz">求职作品集 · 交互设计</span><span class="mk-heat">小红书 赞 10,996 · 藏 6,270</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a65e8560000000001031004?xsec_token=ABQunxghBjs2jp8v4HRfEzrU9XipUCF-21ABHz4WRkBQ0=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a65e8560000000001031004.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://openai.com/codex/" target="_blank" rel="noopener"><img src="posters/logo-codex.png" alt="">Codex</a><div class="gal-cap"><b>示例</b>1 小时做出有设计感的作品集：Codex 写站、GitHub 存代码、Cloudflare 部署；先发参考站让 AI 学，再迭代</div><div class="xg-row"><b>谁在用</b>辣味章鱼（AI 版）</div><div class="mk-tags"><span class="mk-biz">个人作品集</span><span class="mk-heat">小红书 赞 7,020 · 藏 8,866</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a604b38000000001b01f92d?xsec_token=ABBAYWhe1fXH9pHXTArOAAJklX6ZmzsAAc-ddflqoY9OE=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a604b38000000001b01f92d.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://threejs.org/" target="_blank" rel="noopener"><img src="posters/logo-threejs.png" alt="">Codex + three.js</a><div class="gal-cap"><b>示例</b>个人网页做成 3D 房间，绝大部分物件可交互，已部署上线</div><div class="xg-row"><b>谁在用</b>Big喷菇（文科生，首次做 3D 网页）</div><div class="mk-tags"><span class="mk-biz">个人主页</span><span class="mk-heat">小红书 赞 4,267 · 藏 3,251</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6aba02c30000000015010e30?xsec_token=AB3XFnG7S_FsCY9rceTsgz_Lal_HIfYv8y4vKRRKqPJpo=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6aba02c30000000015010e30.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.tripo3d.ai/" target="_blank" rel="noopener"><img src="posters/logo-tripo.png" alt="">Tripo + GPT-6</a><div class="gal-cap"><b>示例</b>给 9 个月大的女儿做 3D 房间网站：摆件按她真实拥有的物品建模，每件物品是一个二级页入口</div><div class="xg-row"><b>谁在用</b>ItsVeyra</div><div class="mk-tags"><span class="mk-biz">家庭记录 · 个人主页</span><span class="mk-heat">小红书 赞 2,080 · 藏 1,130</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a7ae8fa0000000025013608?xsec_token=ABhvPV3Vcz3ys8VEQSZHNsYfO5g0_qDrYbXfLQaOMUm4g=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a7ae8fa0000000025013608.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://openai.com/codex/" target="_blank" rel="noopener"><img src="posters/logo-codex.png" alt="">Codex + AI 视频</a><div class="gal-cap"><b>示例</b>简历做成 3D IP 交互站：AI 把静态 IP 图变成动态视频，再用参考图让 Codex 生成整页 HTML</div><div class="xg-row"><b>谁在用</b>书惠的AI自动化日记</div><div class="mk-tags"><span class="mk-biz">简历 · 个人 IP</span><span class="mk-heat">小红书 赞 3,085 · 藏 4,687</span></div></div></div>
</div>

<a class="anchor" id="xw-s2"></a>

### 动效官网与网页复刻

品牌官网和产品落地页。小红书上最受欢迎的不是从零设计，而是「复刻」：截图、录屏或一个参考站丢给 AI，像素级还原动效，再配一个专门去 AI 味的审美 skill。

<div class="gal-grid">
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6978e01f000000002103383e?xsec_token=ABf7eBiClH4cU7LJ5zpFK6mkZtZIVzbXd2AXkUFhmw-jQ=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6978e01f000000002103383e.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.kimi.com/" target="_blank" rel="noopener"><img src="posters/logo-kimi.png" alt="">Kimi K2.5（截图 / 录屏 → 代码）</a><div class="gal-cap"><b>示例</b>只给 AI 一张截图和一段视频，就能像素级复刻网页；标题直接叫「Vibe Coding 进化成 Visual Coding」（封面写明用 K2.5）</div><div class="xg-row"><b>谁在用</b>赛文乔伊</div><div class="mk-tags"><span class="mk-biz">网页复刻 · Visual Coding</span><span class="mk-heat">小红书 赞 1.9 万 · 藏 2.5 万（本组最高）</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a9d696500000000260339b5?xsec_token=ABMCHDxzMf9pi4Jc1S8w8Cesb0nR00O1YuPQqFvJJ9n10=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a9d696500000000260339b5.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://openai.com/codex/" target="_blank" rel="noopener"><img src="posters/logo-codex.png" alt="">Codex（GPT-6 Astra）</a><div class="gal-cap"><b>示例</b>用很短的 skill 让 GPT-6 提取原站素材，还原 Shopify 2026 Winter Edition 的文艺复兴主题和动效</div><div class="xg-row"><b>谁在用</b>Monet.AI</div><div class="mk-tags"><span class="mk-biz">品牌官网复刻</span><span class="mk-heat">小红书 赞 2,817 · 藏 2,180</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a51e0d50000000007010973?xsec_token=ABKPXtncT6uACkrSTL2KqyRSJlJq-pALiF-vhLsQrwRHQ=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a51e0d50000000007010973.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://openai.com/codex/" target="_blank" rel="noopener"><img src="posters/logo-codex.png" alt="">Codex + taste-skill</a><div class="gal-cap"><b>示例</b>液态海獭咖啡站：Gemini 定 IP、可灵出 4 秒动画，Codex 装 taste-skill 做液体折射，专门去「AI 味」</div><div class="xg-row"><b>谁在用</b>书惠的AI自动化日记</div><div class="mk-tags"><span class="mk-biz">餐饮品牌站</span><span class="mk-heat">小红书 赞 1,479 · 藏 2,171</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a45d55b000000001101452e?xsec_token=ABEq2TJm_EOJ9Z-aJYG8JATjRtSvwmumvtBHjWD7hpQYc=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a45d55b000000001101452e.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://claude.com/product/claude-code" target="_blank" rel="noopener"><img src="posters/logo-claude.png" alt="">Claude Code</a><div class="gal-cap"><b>示例</b>Claude Code + Sonnet 5 搭「获奖级」landing page，颜色、布局、交互可直接上生产</div><div class="xg-row"><b>谁在用</b>泰德搞薯条（转述海外 18 分钟教程）</div><div class="mk-tags"><span class="mk-biz">产品落地页</span><span class="mk-heat">小红书 赞 1,123 · 藏 1,693</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6adf00960000000017034a67?xsec_token=ABQg9pAr-D2cJg6uLuPJ2f6485PvuV6kjxNyrk_4Gv8Y4=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6adf00960000000017034a67.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><div class="xg-proj">AI Design Skills（开源）</div><div class="gal-cap"><b>示例</b>landing-page-design skill：先问清核心行动、目标用户、证据，再按首屏→问题方案→社会证明→FAQ→CTA 排结构；MIT 可商用</div><div class="xg-row"><b>谁在用</b>机器之心（转述设计师 Elaya）</div><div class="mk-tags"><span class="mk-biz">高转化落地页</span><span class="mk-heat">小红书 赞 3,006 · 藏 6,710</span></div></div></div>
</div>

<a class="anchor" id="xw-s3"></a>

### 3D 交互小世界

没有付费方，但是流量最大的一类：浏览器里的微缩 3D 世界，靠「AI 一小时做出来」传播。它是模型能力的展示柜，也是 webdev 和 3D 两条线交汇的地方。

<div class="gal-grid">
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6acd9d34000000001803a6da?xsec_token=ABHD0Ewhn9mIaID2UroEU8vw8z_8cMzQUtysvJCtthugY=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6acd9d34000000001803a6da.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://threejs.org/" target="_blank" rel="noopener"><img src="posters/logo-threejs.png" alt="">three.js + AI 编程</a><div class="gal-cap"><b>示例</b>Jelly Planet：把海岛装进果冻，有灯塔、鲸鱼、海浪，可切换昼夜、暴风雨和极光的实时 3D 微缩世界</div><div class="xg-row"><b>谁在用</b>Ray</div><div class="mk-tags"><span class="mk-biz">创意编程 · 内容传播</span><span class="mk-heat">小红书 赞 11,316 · 藏 3,698</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6ac736fa000000001c01cda1?xsec_token=ABoZ5yD4MgUTgwqBKxVVfUJWeidw52UfZ9UtnnIZWvOBE=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6ac736fa000000001c01cda1.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://threejs.org/" target="_blank" rel="noopener"><img src="posters/logo-threejs.png" alt="">three.js + Blender（GPT-6 Astra）</a><div class="gal-cap"><b>示例</b>Cozy Creek 浏览器 3D 溪流，OpenAI 官方留言；作者公开总消耗约 3.17 亿 token、缓存命中 97.7%</div><div class="xg-row"><b>谁在用</b>Process zero（转述 X @chetanankola）</div><div class="mk-tags"><span class="mk-biz">WebGL 场景</span><span class="mk-heat">小红书 赞 2,137 · 藏 1,576</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6ad467670000000029015cbf?xsec_token=ABvwejsjldc9bIaf2J9wNRhsBNNjgL1W85EHNvTcjgBFQ=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6ad467670000000029015cbf.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.tripo3d.ai/" target="_blank" rel="noopener"><img src="posters/logo-tripo.png" alt="">Tripo API + Claude Opus 5.5</a><div class="gal-cap"><b>示例</b>1 小时做出可漫游森林：Tripo 出小鹿和动作循环，Opus 写环境、灯光、雾效；WASD 移动、E 召萤火虫</div><div class="xg-row"><b>谁在用</b>乌头蜜（转述 X @tripoai）</div><div class="mk-tags"><span class="mk-biz">可漫游 3D 场景</span><span class="mk-heat">小红书 赞 1,216 · 藏 797</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6ae581d7000000000300b5f3?xsec_token=AB-UlQMndZAPVjC8wpsfYvDfa1ZjxNF8TWGWH0RX_XR5I=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6ae581d7000000000300b5f3.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://threejs.org/" target="_blank" rel="noopener"><img src="posters/logo-threejs.png" alt="">three.js（Claude Opus 5.5）</a><div class="gal-cap"><b>示例</b>一张参考图 + 「Make the model」，纯代码搭出机械章鱼：202 个连接结构、480 个机械轮，渲染对比自修 3 轮</div><div class="xg-row"><b>谁在用</b>被拉面驯服的金枪鱼</div><div class="mk-tags"><span class="mk-biz">代码建模</span><span class="mk-heat">小红书 赞 1,639 · 藏 1,146</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6acfaaa5000000000a0248dc?xsec_token=ABb7nMgHbRReQMf0cXrTtf53u67oUSkoyxC30zKzknL2Q=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6acfaaa5000000000a0248dc.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://p5js.org/" target="_blank" rel="noopener"><img src="posters/logo-p5js.png" alt="">p5.js</a><div class="gal-cap"><b>示例</b>一扇窗里的海底世界，白色小鱼穿过窗户游进另一个空间</div><div class="xg-row"><b>谁在用</b>小章鱼的日记</div><div class="mk-tags"><span class="mk-biz">生成艺术</span><span class="mk-heat">小红书 赞 3,020 · 藏 711</span></div></div></div>
</div>

<a class="anchor" id="xw-s4"></a>

### HTML 汇报与 PPT

职场和科研汇报，是 webdev 里最接近刚需的一类：收藏数常常高于点赞，说明大家是存起来照着做。HTML 取代 PPT 的理由是换数据不用重排版。

<div class="gal-grid">
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6aacbe20000000002a02dfb0?xsec_token=AB1w4FKjIMRnClxcRpknBpUuPO-qHA07ADR42ZZzq9iFw=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6aacbe20000000002a02dfb0.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.tapnow.ai/" target="_blank" rel="noopener"><img src="posters/logo-tapnow.png" alt="">TapNow</a><div class="gal-cap"><b>示例</b>交互式 HTML 汇报：预算、路线、方案对比、排期这类高密度信息，用滚动、展开、切换来组织</div><div class="xg-row"><b>谁在用</b>快跑啊小卢_</div><div class="mk-tags"><span class="mk-biz">职场汇报</span><span class="mk-heat">小红书 赞 7,436 · 藏 7,503</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a2ac224000000001603e76b?xsec_token=AByKmHuT5Uqhc7B4HKw6fADoHyP5cKdJVzaFat1FIpzWU=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a2ac224000000001603e76b.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://claude.ai/" target="_blank" rel="noopener"><img src="posters/logo-claude.png" alt="">Claude Design</a><div class="gal-cap"><b>示例</b>讲 Anthropic 的 Claude Design：AI 做 PPT 从「图片式」走到可编辑、可交互的 HTML</div><div class="xg-row"><b>谁在用</b>大师的AI小灶</div><div class="mk-tags"><span class="mk-biz">可编辑 PPT</span><span class="mk-heat">小红书 赞 6,417 · 藏 10,632</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a675362000000000f013683?xsec_token=ABIi79alD0g3dxyIjEUCPSqdOzeFsnj7u5f2MFVCxlK50=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a675362000000000f013683.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://openai.com/codex/" target="_blank" rel="noopener"><img src="posters/logo-codex.png" alt="">Codex</a><div class="gal-cap"><b>示例</b>文献汇报：先让 AI 按背景→创新点→方法→结果出逐页大纲，再把 PPT 模板和论文交给 Codex 逐页生成</div><div class="xg-row"><b>谁在用</b>山山而川（研究生）</div><div class="mk-tags"><span class="mk-biz">科研组会</span><span class="mk-heat">小红书 赞 6,133 · 藏 8,531</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a03ec47000000000702361c?xsec_token=AB9AjFMZnnut-BUMq4uZqIsIL7ZzQczdxDJwt0uub6FrQ=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a03ec47000000000702361c.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><div class="xg-proj">AI 生成 HTML 报告</div><div class="gal-cap"><b>示例</b>团队汇报全面 HTML 化：PPT 做一份数据报告要两天；HTML 模板换数据即可，漏斗图、桑基图都能做，老板来要模板</div><div class="xg-row"><b>谁在用</b>AI救我狗命（团队负责人）</div><div class="mk-tags"><span class="mk-biz">数据分析汇报</span><span class="mk-heat">小红书 赞 1,188 · 藏 1,702</span></div></div></div>
</div>

<a class="anchor" id="xw-s5"></a>

### 网页与 H5 小游戏

能直接看到收入的一类，但数字两极分化：粉丝向 H5 靠 IP 传播，上架 TapTap 的靠广告，同一个作者两款游戏日收入差几十倍。

<div class="gal-grid">
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6ae957410000000003009114?xsec_token=ABUIkL4O4zdknKGujQbqDweqnQZ49xRasgPd9s1no4iN8=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6ae957410000000003009114.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://openai.com/codex/" target="_blank" rel="noopener"><img src="posters/logo-codex.png" alt="">Codex + Tripo</a><div class="gal-cap"><b>示例</b>3 天做单依纯「蛋岛」3D H5 小游戏：Tripo 生成模型，Codex 写交互、接 Blender 渲染，粉丝在岛上找巡演彩蛋</div><div class="xg-row"><b>谁在用</b>DAiKONAUT</div><div class="mk-tags"><span class="mk-biz">粉丝运营 · 演唱会周边</span><span class="mk-heat">小红书 赞 3,301 · 藏 476</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6ae2c069000000002b005180?xsec_token=ABOMB3tYIHthqDBFo5-xB_y0e-a4MT3Y3sNiJpYUocRYE=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6ae2c069000000002b005180.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.kimi.com/code" target="_blank" rel="noopener"><img src="posters/logo-kimi.png" alt="">Kimi Code</a><div class="gal-cap"><b>示例</b>2 天做《爱丽丝梦游仙境》3D 网页游戏：Kimi 写设定和代码，Image 2 出原画，Kimi 写脚本在 Blender 绑骨</div><div class="xg-row"><b>谁在用</b>红发魔女Amber</div><div class="mk-tags"><span class="mk-biz">独立游戏</span><span class="mk-heat">小红书 赞 2,504 · 藏 2,217</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6ad895d4000000003302977a?xsec_token=ABBpZEnzBaI6sS_Swpe8pNaUpC54QTX1_O_O26xZT-Ui0=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6ad895d4000000003302977a.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.taptap.cn/" target="_blank" rel="noopener"><img src="posters/logo-taptap.png" alt="">TapTap 小游戏</a><div class="gal-cap"><b>示例</b>AI 做的两款小游戏同时上 TapTap 总榜和热榜；一款广告日收入千元级，另一款只有几十元</div><div class="xg-row"><b>谁在用</b>明月桥investor</div><div class="mk-tags"><span class="mk-biz">广告变现</span><span class="mk-heat">小红书 赞 763 · 藏 725</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6ae86b4b000000003400bff2?xsec_token=ABxkjCkNxbDVck4bpTHc_VJJiQcCbshioM9yQPKl19u2w=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6ae86b4b000000003400bff2.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><div class="xg-proj">AI 编程做游戏</div><div class="gal-cap"><b>示例</b>标题称一位 26 岁女程序员用 AI 做游戏，4 天收入 4.69 万美元（转述，正文无细节）</div><div class="xg-row"><b>谁在用</b>逸蒙的赛博空间</div><div class="mk-tags"><span class="mk-biz">游戏创业</span><span class="mk-heat">小红书 赞 1,225 · 藏 1,319</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a4a60170000000008002b65?xsec_token=ABPY7V8ypccWe-UcIMgzq5hxRW1L1NpYE_IDN6dDUVu98=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a4a60170000000008002b65.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://toy.cedarstar.org/" target="_blank" rel="noopener">MCP 小游戏合集</a><div class="gal-cap"><b>示例</b>「AI 的 4399」：一个 MCP 整合钓鱼、海龟汤、植物大战丧尸等开源小游戏，人和 AI 用同一个网址玩</div><div class="xg-row"><b>谁在用</b>南山君</div><div class="mk-tags"><span class="mk-biz">AI 陪玩</span><span class="mk-heat">小红书 赞 4,154 · 藏 3,588</span></div></div></div>
</div>

<a class="anchor" id="xw-s6"></a>

### 运营活动页与 H5

电商和节日营销的活动页。小红书上做这类的多是视觉设计师：AI 负责主视觉、3D 渲染和角色动画，页面本身仍在 Figma 里拼。

<div class="gal-grid">
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/69e76937000000001a022bba?xsec_token=ABLqD9_380DElJeo26V4kOpxEPpgWfPB6afh82uhUsT80=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-69e76937000000001a022bba.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><div class="xg-proj">AI 渲染 + H5</div><div class="gal-cap"><b>示例</b>五一 H5 运营活动页全流程：IP 绘制→3D 渲染→场景生成→字体设计→H5 页面，提示词可复用</div><div class="xg-row"><b>谁在用</b>做设计的鹿野Loyel</div><div class="mk-tags"><span class="mk-biz">节日运营</span><span class="mk-heat">小红书 赞 804 · 藏 832</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6856ba09000000002201d5f1?xsec_token=ABDUxlj1aKOaZnwwKmU2Em4PGfdq2AntRLxZyPRX9xxPE=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6856ba09000000002201d5f1.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://jimeng.jianying.com/" target="_blank" rel="noopener"><img src="posters/logo-jimeng.png" alt="">Figma + 即梦</a><div class="gal-cap"><b>示例</b>Figma 交互动画里的角色动画，用即梦视频 3.0 的首尾帧功能生成</div><div class="xg-row"><b>谁在用</b>设计师 Cc</div><div class="mk-tags"><span class="mk-biz">交互动效</span><span class="mk-heat">小红书 赞 5,143 · 藏 5,856</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a915373000000002503b6f0?xsec_token=ABRDFdkUaW6BKKbGXwCgBF4yOonufgVnjPgd7W1-SapF0=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a915373000000002503b6f0.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><div class="xg-proj">AI 生图 + 排版</div><div class="gal-cap"><b>示例</b>手绘草图 + 风格配色参考生成主体物，再延展元素、去背景，排成长图文落地页</div><div class="xg-row"><b>谁在用</b>belladonna</div><div class="mk-tags"><span class="mk-biz">中秋活动落地页</span><span class="mk-heat">小红书 赞 1,176 · 藏 1,000</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/69e99cbc0000000023013d93?xsec_token=ABxdSCVD_tC9yd6HT7eCnBT0Z9ZoK7CqqGoqSgroFqM0A=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-69e99cbc0000000023013d93.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><div class="xg-proj">GPT（图像）</div><div class="gal-cap"><b>示例</b>H5 运营游戏页，作者称效果「再次冲击这个行业」</div><div class="xg-row"><b>谁在用</b>北北North（UI 设计师）</div><div class="mk-tags"><span class="mk-biz">运营游戏页</span><span class="mk-heat">小红书 赞 2,545 · 藏 1,805</span></div></div></div>
</div>

<a class="anchor" id="xw-s7"></a>

### 数据大屏与内部工具

企业 B 端。小红书上多是非技术岗自己搭：舆情监控、数据大屏。共识是 AI 适合跑提案和方向验证，真正交付还要回到数据逻辑和组件规范。

<div class="gal-grid">
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6986ee370000000015020308?xsec_token=ABM_wGKkqqoJs_en0kLCYk4ufHZxIGVdWjzcpv01tHPHo=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6986ee370000000015020308.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://cursor.com/" target="_blank" rel="noopener"><img src="posters/logo-cursor.png" alt="">Cursor</a><div class="gal-cap"><b>示例</b>3 小时搭按国家、平台监控品牌舆情的平台：先让模型调研抓取方案写成文档，再逐国逐平台抓</div><div class="xg-row"><b>谁在用</b>是森森吖（非技术岗）</div><div class="mk-tags"><span class="mk-biz">品牌舆情监控</span><span class="mk-heat">小红书 赞 1,175 · 藏 1,447</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a58c19e000000000f030032?xsec_token=ABGj8VeyIS_ETux_Zlfa1jDkhCPj-zgrxzerK4xluVqdM=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a58c19e000000000f030032.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://openai.com/codex/" target="_blank" rel="noopener"><img src="posters/logo-codex.png" alt="">Codex + Image2</a><div class="gal-cap"><b>示例</b>Image2 出视觉稿，Codex 做成可交互的数据可视化大屏</div><div class="xg-row"><b>谁在用</b>自由设计酒窝姐</div><div class="mk-tags"><span class="mk-biz">数据可视化大屏</span><span class="mk-heat">小红书 赞 897 · 藏 1,902</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a61f716000000000100e8b5?xsec_token=ABF-8DHJZzPJ9YQTTrFUSE4LZmEXAOn0xQQlH98ZN4N6E=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a61f716000000000100e8b5.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.lovart.ai/" target="_blank" rel="noopener"><img src="posters/logo-lovart.png" alt="">Lovart → Codex → Figma</a><div class="gal-cap"><b>示例</b>先用建筑主视觉跑通大屏布局、信息密度和动效节奏，用于前期提案；交付要回到数据逻辑和组件状态</div><div class="xg-row"><b>谁在用</b>赵姑娘UI设计师</div><div class="mk-tags"><span class="mk-biz">大屏提案</span><span class="mk-heat">小红书 赞 675 · 藏 969</span></div></div></div>
</div>

<a class="anchor" id="xw-s8"></a>

### 交互科普与课件

教育和科普：把复杂的东西做成能拆开看的 3D 网页。案例少但传播强，人体拆解站一条就 7,500 赞。

<div class="gal-grid">
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a9c967e00000000250342bd?xsec_token=ABQClRorFxvRYrBKBRWi8IRpOLkJ8qPoUkkgE37jpDESw=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a9c967e00000000250342bd.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://openai.com/codex/" target="_blank" rel="noopener"><img src="posters/logo-codex.png" alt="">Codex（GPT-6 Astra）</a><div class="gal-cap"><b>示例</b>人体拆成 2234 块的 3D 网站：肌肉 402、动脉 639、静脉 404，点哪块都有名字和说明，代码开源</div><div class="xg-row"><b>谁在用</b>自游民Nomad（转述 Ashe，前 NASA / 苹果 ML 工程师）</div><div class="mk-tags"><span class="mk-biz">医学科普</span><span class="mk-heat">小红书 赞 7,575 · 藏 4,559</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6acc87c0000000001b023304?xsec_token=ABd7OrLMChB_2SVkYk_R2K57SNI95xQ1vS6KvPY1UwLMM=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6acc87c0000000001b023304.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://github.com/wheresryan22/anatomy" target="_blank" rel="noopener"><img src="posters/logo-github.png" alt="">anatomy skill（开源）</a><div class="gal-cap"><b>示例</b>/anatomy explain how a mechanical watch keeps time：一句话生成可交互、可拆解的机械原理模型，支持 Claude Code、Codex、Cursor</div><div class="xg-row"><b>谁在用</b>小师妹 Kiki</div><div class="mk-tags"><span class="mk-biz">机械原理科普</span><span class="mk-heat">小红书 赞 853 · 藏 2,135</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6ac76004000000001203fc37?xsec_token=ABoZ5yD4MgUTgwqBKxVVfUJfoIJft6MfRiO68WGP4_oiI=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6ac76004000000001203fc37.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><div class="xg-proj">交互课件</div><div class="gal-cap"><b>示例</b>3D 可交互英文密室逃脱，给老师改编成课堂活动</div><div class="xg-row"><b>谁在用</b>Sira</div><div class="mk-tags"><span class="mk-biz">中小学英语课堂</span><span class="mk-heat">小红书 赞 1,279 · 藏 787</span></div></div></div>
</div>

<a class="anchor" id="xw-s9"></a>

### 数字策展与文博

文博和文旅：线上展、古迹可视化。做的人多是策展和设计背景，AI 分工通常是 Gemini 做研究和方案、Codex 写代码。

<div class="gal-grid">
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/69fa1728000000001f002cba?xsec_token=ABszsoBOdF5uqpIFGdg9klHb-HH6qswO1vTkCwkoDGuy8=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-69fa1728000000001f002cba.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.bianjing-hours.art/" target="_blank" rel="noopener">Gemini + Codex</a><div class="gal-cap"><b>示例</b>北宋汴京主题线上博物馆 bianjing-hours.art，做了近一个月：Gemini 负责学术研究和前端方案，Codex 写代码</div><div class="xg-row"><b>谁在用</b>IamYaojun</div><div class="mk-tags"><span class="mk-biz">线上策展</span><span class="mk-heat">小红书 赞 640 · 藏 484</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/69cf6bc90000000022003a5f?xsec_token=ABSKjipNGObtJDy-M9LdOjKMhcsoIvzuPP4rOi6ho_ZSs=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-69cf6bc90000000022003a5f.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://github.com/chenglou/pretext" target="_blank" rel="noopener"><img src="posters/logo-github.png" alt="">pretext + 3D</a><div class="gal-cap"><b>示例</b>古迹 3D 模型 + 文字实时绕排：旋转建筑看细节时文字不挡模型，工作流开源</div><div class="xg-row"><b>谁在用</b>泡椒肥汤圆</div><div class="mk-tags"><span class="mk-biz">古迹展示</span><span class="mk-heat">小红书 赞 2,499 · 藏 3,339</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6ad79205000000002901b973?xsec_token=ABRZ2VykcWE-0NegURQAmfYLnh2-Ulp3HIJFtUxK2muSU=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6ad79205000000002901b973.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://antigravity.google/" target="_blank" rel="noopener"><img src="posters/logo-antigravity.png" alt="">Gemini + Antigravity</a><div class="gal-cap"><b>示例</b>5 个历史遗迹做成可交互 3D 场景，黑白色调 + 悬浮标注，像数字博物馆</div><div class="xg-row"><b>谁在用</b>乌头蜜（转述 X @soumyadesign）</div><div class="mk-tags"><span class="mk-biz">历史遗迹可视化</span><span class="mk-heat">小红书 赞 109 · 藏 79</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6ad64391000000001e02468b?xsec_token=ABMdcVeXBGNL2R_8HNS5ABLoOvKt4SQZzcMvlzFz7bgFg=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6ad64391000000001e02468b.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://threejs.org/" target="_blank" rel="noopener"><img src="posters/logo-threejs.png" alt="">three.js</a><div class="gal-cap"><b>示例</b>卡尔维诺《看不见的城市》做成摆满微缩城市的 3D 书桌，每座城市一边逛一边读</div><div class="xg-row"><b>谁在用</b>乌头蜜（转述）</div><div class="mk-tags"><span class="mk-biz">文学 × 网页</span><span class="mk-heat">小红书 赞 200 · 藏 178</span></div></div></div>
</div>

<a class="anchor" id="xw-s10"></a>

### 小程序与独立站

真正收钱的一类，但小红书上能看到的大多是小数字：一周上万用户还没变现、广告日收入几块到几十元。大数字（月入 30 万美元）基本是转述海外案例。

<div class="gal-grid">
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6ad269ea0000000018019153?xsec_token=ABI2LFQw__JFuxRUSTvpfExzCpByM9W6KvYiMZWhUiwFQ=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6ad269ea0000000018019153.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://lovable.dev/" target="_blank" rel="noopener"><img src="posters/logo-lovable.png" alt="">Lovable</a><div class="gal-cap"><b>示例</b>狗狗肖像网站月入 30 万美元：网站 + 支付 + 推广，关键是把画像做成实物寄到家，而不是只生成图</div><div class="xg-row"><b>谁在用</b>Caroline（转述 Lovable 创始人访谈）</div><div class="mk-tags"><span class="mk-biz">宠物定制 · 电商</span><span class="mk-heat">小红书 赞 783 · 藏 1,186</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6ae3fca7000000000e02f990?xsec_token=ABA3paPlkebqcGglhZ-ecbvx-u4_8XyzeejlF2f4U6Nfg=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6ae3fca7000000000e02f990.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><div class="xg-proj">Vibe Coding 独立站</div><div class="gal-cap"><b>示例</b>标题称一个人 vibe coding 做网站月入 1.2 万美元（正文是活动推广，未给细节）</div><div class="xg-row"><b>谁在用</b>熠辉 indie</div><div class="mk-tags"><span class="mk-biz">出海独立站</span><span class="mk-heat">小红书 赞 2,963 · 藏 3,635</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a2fb0620000000015027c33?xsec_token=AB-VLdrq7ItN0VJWEIZBD1iphOwBLDJf4f2j_uDeKiyAI=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a2fb0620000000015027c33.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://mp.weixin.qq.com/" target="_blank" rel="noopener"><img src="posters/logo-wechat.png" alt="">微信小程序 + DeepSeek</a><div class="gal-cap"><b>示例</b>彩虹饮食记录小程序：免费网页版 DeepSeek 写代码，讲清注册、备案、审核这些坑</div><div class="xg-row"><b>谁在用</b>慢有引力（离职后自己做）</div><div class="mk-tags"><span class="mk-biz">健康记录</span><span class="mk-heat">小红书 赞 1,754 · 藏 2,123</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a882a55000000001f01cf81?xsec_token=ABn6_eyn8LxS7UDBTmENyDSPA9VLeGu-s1gdd5JG_wOgQ=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a882a55000000001f01cf81.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><div class="xg-proj">AI 小程序</div><div class="gal-cap"><b>示例</b>随手做的心理测试小程序，上线一周多累计 1 万多用户，还在想怎么变现</div><div class="xg-row"><b>谁在用</b>莫名其妙</div><div class="mk-tags"><span class="mk-biz">心理测试</span><span class="mk-heat">小红书 赞 931 · 藏 803</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a9d448b000000000b00fdfd?xsec_token=ABMCHDxzMf9pi4Jc1S8w8Cek6NO-Oqxu0PalNcxc22tJI=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a9d448b000000000b00fdfd.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.taptap.cn/" target="_blank" rel="noopener"><img src="posters/logo-taptap.png" alt="">TapTap 小游戏</a><div class="gal-cap"><b>示例</b>纯 AI 开发一周，广告日收入前 3 天 10 元、之后 2 元，10 月回升到日均 50 元</div><div class="xg-row"><b>谁在用</b>猫头大王</div><div class="mk-tags"><span class="mk-biz">广告变现</span><span class="mk-heat">小红书 赞 674 · 藏 581</span></div></div></div>
</div>

<!--/XG-->

<a class="anchor" id="xw-3"></a>

## 3 Insights

- **「复刻」比「生成」更受欢迎。** 本页最高赞是截图 + 录屏像素级复刻；Monet.AI 复刻 Shopify 主题、hi超纯 4 轮对话复刻复杂动效站。输入是图和视频、输出是代码，这正是 visual coder 的形态。
- **收入信号少，而且小。**
  - 国内能看到的数字：心理测试小程序一周 1 万用户还没变现；TapTap 小游戏广告日收入从 2 元到千元级不等。
  - 大数字都是转述或标题：狗狗肖像站月入 30 万美元（转述 Lovable 创始人访谈）、4 天 4.69 万美元、月入 1.2 万美元，正文都没有细节。
- **3D 是 webdev 的流量引擎。** 作品集和科普两组赞最高的都是 3D 网页（泳池作品集、人体拆解）；Tripo API 已经进入网页工作流（森林、蛋岛、《小王子》）。
- **审美 skill 成了新的中间层。** taste-skill、AI Design Skills、anatomy 这类开源 skill 被反复推荐，用来去掉「AI 味」；它们本质上是给 coding agent 的设计规范。

下一步：作品集、HTML 汇报、复刻这三类有固定套路、有明确参考输入，适合做 visual coder 的评测和数据。

<a class="anchor" id="xw-4"></a>

## 4 Data Caliber

- **来源**：小红书网页版搜索，2026-11-03 抓取，每个关键词按综合排序取前 2 页（约 40 条），25 个关键词去重后 744 条。
- **热度**：点赞和收藏取搜索结果当时的数字。
- **工具份额**：按标题和已抓正文的关键词匹配，只代表「被提到」，不代表真实使用；约 100 条入围笔记抓了正文，其余只有标题。
- **转述**：标「转述」的卡片，原作是 X 或海外访谈，小红书博主是搬运者；收入数字均为自述或转述，未核实。
- **数据文件**：`middle_processing/market/xhs/`（search/ 原始结果、notes/ 正文、gallery.json 卡片），由 `scripts/xhs_crawl.py` 和 `scripts/market_xhs_gallery.py` 生成。

</div>

<div class="env-view" data-view="xhs3d" data-label="3D Gallery">

<nav class="toc view-toc"><h2>Contents</h2><ul><li class="l2"><a href="#x3-1"><span class="num">1</span> Scene Taxonomy</a></li><li class="l2"><a href="#x3-2"><span class="num">2</span> Gallery</a></li><li class="l3"><a href="#x3-s1"><span class="num">2.1</span> 3D 打印手办</a></li><li class="l3"><a href="#x3-s2"><span class="num">2.2</span> 大模型操作 Blender</a></li><li class="l3"><a href="#x3-s3"><span class="num">2.3</span> 游戏与资产库</a></li><li class="l3"><a href="#x3-s4"><span class="num">2.4</span> 角色与虚拟人</a></li><li class="l3"><a href="#x3-s5"><span class="num">2.5</span> 高斯泼溅与实景</a></li><li class="l3"><a href="#x3-s6"><span class="num">2.6</span> 影视预演与 AI 视频</a></li><li class="l3"><a href="#x3-s7"><span class="num">2.7</span> 产品外观与工业件</a></li><li class="l2"><a href="#x3-3"><span class="num">3</span> Insights</a></li><li class="l2"><a href="#x3-4"><span class="num">4</span> Data Caliber</a></li></ul></nav>

小红书 3D 线赞最高的一条，是 Blender 教程博主用 Tripo 生成全部资产、再在 Blender 里搭一汪荷塘，1.8 万赞。GPT-6 Astra 发布后，「让大模型经 MCP 开 Blender」成了标配。本页从 13 个关键词、327 条笔记里，按场景挑出 30 个最佳实践。

<a class="anchor" id="x3-1"></a>

## 1 Scene Taxonomy

核心发现：热度在「大模型操作 Blender」，钱在 3D 打印和视频预演。3D 打印的付费方是家长和潮玩爱好者；视频预演已经有商单，AI 短剧公司在发 Blender 白模的单子。

| 场景 | 领域 | 常用项目 | 最热案例 | 小红书热度 |
|---|---|---|---|---|
| 3D 打印手办（AI → 实物） | 亲子 · 潮玩 · 家居摆件 | Hitem3D、Hyper3D Rodin、拓竹 MakerLab、Meshy | 圣诞怪兽派对超大手办 | 赞 1,601 · 藏 1,682 |
| 大模型操作 Blender | 场景美术 · DCC 自动化 | Blender、Tripo、Codex、Hyper3D MCP | KurTips 荷塘教程 | 赞 17,559 · 藏 13,842 |
| 游戏与资产库 | 独立游戏 · 资产规模化 | Tripo、Unity / Godot / UE5 MCP、Codex | 《小王子》同款梵高小岛 | 赞 6,789 · 藏 7,332 |
| 角色与虚拟人 | VTuber · IP · 兵人 | Tripo P2.0、Warudo、Rodin | AI 生成 3D 角色流程 | 赞 2,134 · 藏 2,600 |
| 高斯泼溅与实景 | 沉浸网页 · 旅行 · 数字艺术 | World Labs Marble、Insta360 X6 | 用高斯泼溅做网页 | 赞 3,248 · 藏 2,143 |
| 影视预演与 AI 视频 | 品牌片 · AI 短剧 | Hyper3D Rodin、Blender MCP | 何同学一镜到底幕后 | 赞 1,859 · 藏 2,056 |
| 产品外观与工业件 | 硬件 · 电商产品页 | Codex + FreeCAD、Codex + Blender | Codex 做电路板外壳 | 赞 1,876 · 藏 2,061 |

工具份额（327 条 3D 笔记，按标题和正文提及计）：

| 项目 | 提及笔记 | 赞合计 |
|---|---|---|
| Blender | 58 | 49,393 |
| Tripo | 29 | 35,836 |
| GPT-6 / Astra | 55 | 30,941 |
| 高斯泼溅 / 3DGS | 32 | 9,724 |
| Claude / Opus | 8 | 9,644 |
| Codex | 14 | 9,027 |
| Hyper3D / Rodin | 14 | 7,301 |
| MCP | 15 | 6,159 |
| Meshy | 20 | 4,941 |
| 混元3D | 22 | 4,717 |
| 3D 打印 / 拓竹 | 12 | 3,276 |

数据解读：

- **Tripo 是小红书上 3D 生成的默认选项。** 29 条、3.6 万赞，远高于 Meshy（20 条、4,941 赞）和混元（22 条、4,717 赞）；Meshy 和混元的笔记不少是官方号、招聘和创始人访谈。
- **Blender 成了大模型的 3D 操作系统。** 提及最多（58 条），GPT-6、Codex、Claude 都经 MCP 操作它；UE5、Unity、Godot 也开始出现同样的 MCP 用法。
- **钱在打印和预演，不在建模本身。** Meshy 创始人自述严格口径 ARR 已过 1 亿美元，而小红书上看到的落地是手办和视频预演。

<a class="anchor" id="x3-2"></a>

## 2 Gallery

每张卡：封面链到小红书原帖；项目名链到官网（带 logo）；下面依次是示例、谁在用、领域和热度。

<!--XG:3d-->

<a class="anchor" id="x3-s1"></a>

### 3D 打印手办（AI → 实物）

离钱最近的 3D 场景，付费方是家长和潮玩爱好者。链路固定：生图→图生 3D→拆件修模→切片打印；打印绕开了 AI 3D 最弱的拓扑、UV 和绑骨。

<div class="gal-grid">
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/692d7cd8000000001e0368b9?xsec_token=ABzStfYKx7aJ1pVRSKFeiLmMDwqXVB0bIVWuWCwKK4iUI=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-692d7cd8000000001e0368b9.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.hitem3d.ai/" target="_blank" rel="noopener"><img src="posters/logo-hitem3d.png" alt="">Hitem3D</a><div class="gal-cap"><b>示例</b>圣诞怪兽派对超大手办：豆包出图→Hitem3D 生成 STL→Magics 减面拆件→打印，一周完成</div><div class="xg-row"><b>谁在用</b>村民刘大才</div><div class="mk-tags"><span class="mk-biz">家居摆件</span><span class="mk-heat">小红书 赞 1,601 · 藏 1,682</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a6875ce00000000010325b8?xsec_token=AB7vlyDwyYvwEUCY-O_LauCvvgPFmAgAtQyan4B5UWrH0=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a6875ce00000000010325b8.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.hitem3d.ai/" target="_blank" rel="noopener"><img src="posters/logo-hitem3d.png" alt="">Hi3D + 多色打印</a><div class="gal-cap"><b>示例</b>女儿的画→AI 角色图→Hi3D 纹理模型→多色色区→3MF 切片→多色打印，耗材颜色她自己选</div><div class="xg-row"><b>谁在用</b>SeanIXz带孩子玩3D打印</div><div class="mk-tags"><span class="mk-biz">亲子创作</span><span class="mk-heat">小红书 赞 254 · 藏 344</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6ae433a60000000026025259?xsec_token=ABDmuXPveVZgB4MUKjdl4yRjxy0E_0OiVM-PxqUhr5de8=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6ae433a60000000026025259.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://hyper3d.ai/" target="_blank" rel="noopener"><img src="posters/logo-hyper3d.png" alt="">Hyper3D Rodin</a><div class="gal-cap"><b>示例</b>女儿的铅笔漫画小人直接图生 3D，再打印成手办；作者首次上手建模</div><div class="xg-row"><b>谁在用</b>CHEN天玩事务所</div><div class="mk-tags"><span class="mk-biz">亲子创作</span><span class="mk-heat">小红书 赞 603 · 藏 72</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/69fa69d20000000035021e1c?xsec_token=ABszsoBOdF5uqpIFGdg9klHeNq8kUNNL7IgG5Pg0EjhZU=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-69fa69d20000000035021e1c.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://makerworld.com/" target="_blank" rel="noopener"><img src="posters/logo-makerworld.png" alt="">拓竹 MakerLab</a><div class="gal-cap"><b>示例</b>月牙雪熊：拓竹自带 AI 建模→Blender 修改→打印→上色</div><div class="xg-row"><b>谁在用</b>阿レ</div><div class="mk-tags"><span class="mk-biz">潮玩手办</span><span class="mk-heat">小红书 赞 1,534 · 藏 214</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/69afdf2f000000001b0171e7?xsec_token=ABTEF90g-DVUfBoSP8298osX-4eSmaXXzbtmw3X1uR_Yc=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-69afdf2f000000001b0171e7.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.meshy.ai/" target="_blank" rel="noopener"><img src="posters/logo-meshy.png" alt="">Meshy × MakerWorld</a><div class="gal-cap"><b>示例</b>Meshy 接进 MakerWorld 的 MakerLab Image-to-3D：上传一张图，几分钟出可直接打印的模型</div><div class="xg-row"><b>谁在用</b>Meshy 官方 × 拓竹</div><div class="mk-tags"><span class="mk-biz">3D 打印平台</span><span class="mk-heat">小红书 赞 378 · 藏 288</span></div></div></div>
</div>

<a class="anchor" id="x3-s2"></a>

### 大模型操作 Blender

3D 线热度最高的一类。GPT-6 Astra 发布后，「让大模型经 MCP 开 Blender」成了标配；实际做法是专业 3D 生成模型出资产，大模型负责搭场景、几何节点和渲染。

<div class="gal-grid">
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6ab1e3d9000000003501481d?xsec_token=ABDsRbUR3cajI-eGLCQnFyfXt5nItaqyGjLAqJ8mjdtkc=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6ab1e3d9000000003501481d.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.blender.org/" target="_blank" rel="noopener"><img src="posters/logo-blender.png" alt="">Blender + Tripo</a><div class="gal-cap"><b>示例</b>夏日荷塘教程：水獭、荷花、莲蓬等资产全用 Tripo 生成，Blender 做池水材质、波纹和布光</div><div class="xg-row"><b>谁在用</b>KurTips（Blender 教程博主）</div><div class="mk-tags"><span class="mk-biz">风格化场景</span><span class="mk-heat">小红书 赞 1.8 万 · 藏 1.4 万（3D 组最高）</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6aa6779f000000002902e885?xsec_token=ABf0NpDf4M1mXNOpdPx7b2wM8pmTMSbk5JSZRekJ0z30U=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6aa6779f000000002902e885.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://openai.com/codex/" target="_blank" rel="noopener"><img src="posters/logo-codex.png" alt="">Codex（GPT-6 Astra）+ 几何节点</a><div class="gal-cap"><b>示例</b>让 Astra 搭 Blender 几何节点做程序化植物和动画；过去用 Houdini 写 VEX 要一两周</div><div class="xg-row"><b>谁在用</b>星川同学</div><div class="mk-tags"><span class="mk-biz">程序化建模</span><span class="mk-heat">小红书 赞 2,303 · 藏 1,326</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6aa94131000000001103405e?xsec_token=ABoc0zF7wZX7J5_pA5Vy_XJULKSo5-1-G7PXHIwo86U-M=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6aa94131000000001103405e.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://hyper3d.ai/" target="_blank" rel="noopener"><img src="posters/logo-hyper3d.png" alt="">Hyper3D MCP + GPT-6</a><div class="gal-cap"><b>示例</b>一张图一句话：GPT-6 调 Hyper3D 批量生成资产，在 Blender 里自动搭场景并渲染动画；作者指出 GPT-6 单独建模只会堆几何体</div><div class="xg-row"><b>谁在用</b>T-BOY</div><div class="mk-tags"><span class="mk-biz">全自动场景</span><span class="mk-heat">小红书 赞 1,476 · 藏 1,784</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a21958c0000000022020570?xsec_token=ABg4U0Bbbec8JyjOMwTMK3wDd_CjmsbOzQQ_5aYx5tIH4=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a21958c0000000022020570.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://openai.com/codex/" target="_blank" rel="noopener"><img src="posters/logo-codex.png" alt="">Codex + Blender</a><div class="gal-cap"><b>示例</b>Codex 控制 Blender 自动化建模，15 张图拆解过程</div><div class="xg-row"><b>谁在用</b>白无常C4D</div><div class="mk-tags"><span class="mk-biz">自动化建模</span><span class="mk-heat">小红书 赞 1,701 · 藏 2,096</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6aa4009e000000002802c091?xsec_token=ABVFmTNHLwrvkialnTgGbZR5UL43Ad6CRKqTQVS1U5AjY=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6aa4009e000000002802c091.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.blender.org/" target="_blank" rel="noopener"><img src="posters/logo-blender.png" alt="">GPT-6 + Blender</a><div class="gal-cap"><b>示例</b>从概念设定到成品的 GPT 驱动 Blender 场景工作流（作者自称「标题党，并非 3A」）</div><div class="xg-row"><b>谁在用</b>KaRmAr</div><div class="mk-tags"><span class="mk-biz">场景美术</span><span class="mk-heat">小红书 赞 3,306 · 藏 4,004</span></div></div></div>
</div>

<a class="anchor" id="x3-s3"></a>

### 游戏与资产库

独立游戏和资产规模化。《小王子》3D 游戏是标杆：16 天、近 300 万浏览，带火了 Tripo + 大模型 + 引擎 MCP 这条链路。

<div class="gal-grid">
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6ad15b080000000014001b91?xsec_token=ABxQV50uIXOoQGyY63JTcmnAjnSESTZyo8TWKq2pdsdyE=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6ad15b080000000014001b91.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.tripo3d.ai/" target="_blank" rel="noopener"><img src="posters/logo-tripo.png" alt="">Unity MCP + Tripo</a><div class="gal-cap"><b>示例</b>16 天做出《小王子》3D 游戏，近 300 万浏览：Fable 写 PRD、Image 2.5 出图、Tripo 出资产、Claude 经 Unity MCP 操作项目</div><div class="xg-row"><b>谁在用</b>Kelly的科研日常（整理 X @Saccc_c）</div><div class="mk-tags"><span class="mk-biz">3D 剧情游戏</span><span class="mk-heat">小红书 赞 803 · 藏 958</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6ad1f47000000000140396c9?xsec_token=ABxQV50uIXOoQGyY63JTcmnL0kySH9dNJsOY4TZIDsMZE=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6ad1f47000000000140396c9.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.tripo3d.ai/" target="_blank" rel="noopener"><img src="posters/logo-tripo.png" alt="">Opus 5.5 + Tripo</a><div class="gal-cap"><b>示例</b>照《小王子》同款思路，4 步做出梵高小岛 3D 网页游戏</div><div class="xg-row"><b>谁在用</b>Lala罐头</div><div class="mk-tags"><span class="mk-biz">3D 网页游戏</span><span class="mk-heat">小红书 赞 6,789 · 藏 7,332</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6adf144d0000000015005cc6?xsec_token=ABQg9pAr-D2cJg6uLuPJ2f6_B9zYQq0-tvwBiRmKJqu9k=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6adf144d0000000015005cc6.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://godotengine.org/" target="_blank" rel="noopener"><img src="posters/logo-godot.png" alt="">Claude Code + Godot</a><div class="gal-cap"><b>示例</b>6 周做出怪猎 × 塞尔达风格 3D 原型，工具订阅约 400 美元；规则是一次只做一个功能，测完再下一个</div><div class="xg-row"><b>谁在用</b>Money玩AI（转述海外开发者）</div><div class="mk-tags"><span class="mk-biz">独立游戏原型</span><span class="mk-heat">小红书 赞 840 · 藏 793</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6acfb66a000000001803a5fc?xsec_token=ABb7nMgHbRReQMf0cXrTtf5xU9kMsVPkDcFnt34GrLDJc=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6acfb66a000000001803a5fc.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.unrealengine.com/" target="_blank" rel="noopener"><img src="posters/logo-unreal.png" alt="">UE5 + MCP（GPT-6.1 Sol）</a><div class="gal-cap"><b>示例</b>白盒先在网页版 GPT 出 GLB 定构图（省 API token），再让 AI 经 MCP 铺地形、纹理和树木</div><div class="xg-row"><b>谁在用</b>白蘑菇</div><div class="mk-tags"><span class="mk-biz">UE5 场景</span><span class="mk-heat">小红书 赞 429 · 藏 443</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6aaaa452000000002803068b?xsec_token=ABv4CvemqLeuFMynnuZLrWGEI8z31lqn23TlyTrInP4vw=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6aaaa452000000002803068b.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://openai.com/codex/" target="_blank" rel="noopener"><img src="posters/logo-codex.png" alt="">Codex + Blender</a><div class="gal-cap"><b>示例</b>2770 个城市 3D 资产只用约 7 个 5 小时额度：先做母模型、拆成楼层 / 窗户 / 屋顶规则，再按《城市：天际线》分类批量生成</div><div class="xg-row"><b>谁在用</b>祖师傅的AI工坊</div><div class="mk-tags"><span class="mk-biz">城市资产库</span><span class="mk-heat">小红书 赞 648 · 藏 748</span></div></div></div>
</div>

<a class="anchor" id="x3-s4"></a>

### 角色与虚拟人

VTuber 和 IP 角色：生成→绑骨→导出 VRM 的整条链路，已经能由一个 agent 串起来。

<div class="gal-grid">
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a9ec2f6000000002901b94e?xsec_token=ABEdhXFg3IBhxJe7ljn0gUARtbCek2spmMYFyxvkAtQck=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a9ec2f6000000002901b94e.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://warudo.app/" target="_blank" rel="noopener"><img src="posters/logo-warudo.png" alt="">Tripo P2.0 + Warudo</a><div class="gal-cap"><b>示例</b>一句提示词：Astra 用 GPT Image2 出 T-pose，调 Tripo P2.0 出 8K 贴图角色，skintokens 绑骨，转 VRM 后在 Warudo 里跳舞</div><div class="xg-row"><b>谁在用</b>shadow不傻逗</div><div class="mk-tags"><span class="mk-biz">VTuber</span><span class="mk-heat">小红书 赞 549 · 藏 634</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a8ed9610000000026037a86?xsec_token=ABUAkTTuw0mOgR-dKTRy8wTMCa8fM-kB1QoF8CYYHYTWI=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a8ed9610000000026037a86.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://hyper3d.ai/" target="_blank" rel="noopener"><img src="posters/logo-hyper3d.png" alt="">Hyper3D Rodin</a><div class="gal-cap"><b>示例</b>Rodin 直出荷兰弟头雕，作者称 AI 把头雕门槛「干没了」</div><div class="xg-row"><b>谁在用</b>🤡（兵人玩家）</div><div class="mk-tags"><span class="mk-biz">兵人头雕</span><span class="mk-heat">小红书 赞 209 · 藏 146</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/69eed7c4000000003601c806?xsec_token=ABYOs6WLVYufXWAyBHmpUiOIUJZ17A22vuiJAayNEEvy4=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-69eed7c4000000003601c806.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><div class="xg-proj">AI 生成 3D 角色</div><div class="gal-cap"><b>示例</b>AI 生成 3D 角色的基础流程和关键词，29 张图逐步拆解</div><div class="xg-row"><b>谁在用</b>浇汁儿的小胖子</div><div class="mk-tags"><span class="mk-biz">角色建模</span><span class="mk-heat">小红书 赞 2,134 · 藏 2,600</span></div></div></div>
</div>

<a class="anchor" id="x3-s5"></a>

### 高斯泼溅与实景

把真实空间搬进浏览器：旅行、梦境、古迹。硬件厂商已经下场，影石 X6 全景相机能在 App 里直接生成 3DGS。

<div class="gal-grid">
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/68f75c620000000004015457?xsec_token=ABXT7bP__qHad02lrEw2x9ldnsye1P8C12HEUQjRy8szs=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-68f75c620000000004015457.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.worldlabs.ai/" target="_blank" rel="noopener"><img src="posters/logo-worldlabs.png" alt="">World Labs + three.js</a><div class="gal-cap"><b>示例</b>用高斯泼溅做网页：高斯点可退化成点云做粒子动画；提醒大量高斯点会让 MacBook 风扇狂转，不宜做长停留页</div><div class="xg-row"><b>谁在用</b>DeadRabbit</div><div class="mk-tags"><span class="mk-biz">沉浸式网页</span><span class="mk-heat">小红书 赞 3,248 · 藏 2,143</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a7dc70d0000000025014a5f?xsec_token=ABjSSweEwieP4LR3sazuOgTCEnvFcR5n-8eY019345f3E=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a7dc70d0000000025014a5f.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.insta360.com/" target="_blank" rel="noopener"><img src="posters/logo-insta360.png" alt="">Insta360 X6</a><div class="gal-cap"><b>示例</b>X6 全景相机支持在 App 内生成 3D 高斯泼溅模型，旅行去过的地方拍一下就能建模分享</div><div class="xg-row"><b>谁在用</b>影石刘靖康（影石 CEO）</div><div class="mk-tags"><span class="mk-biz">旅行记录</span><span class="mk-heat">小红书 赞 780 · 藏 179</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/68f8c81100000000050138e0?xsec_token=ABsVvNrPuMtiPHRaSE5PaRtCzqxUMPci-cWuqxkUNg4-M=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-68f8c81100000000050138e0.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://marble.worldlabs.ai/" target="_blank" rel="noopener"><img src="posters/logo-worldlabs.png" alt="">World Labs Marble</a><div class="gal-cap"><b>示例</b>用 Marble 重建被花海占领的地铁站梦境，在浏览器渲染并加音频驱动特效，下一步搬进 Unity VR</div><div class="xg-row"><b>谁在用</b>cocolinux</div><div class="mk-tags"><span class="mk-biz">数字艺术</span><span class="mk-heat">小红书 赞 1,294 · 藏 831</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6ac2834d000000001303efd5?xsec_token=ABc5-SN1k2NG8DxsbjxVh3TlASdUtPaYIWriLT5knWn9w=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6ac2834d000000001303efd5.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><div class="xg-proj">image-blaster（开源）</div><div class="gal-cap"><b>示例</b>一张图生成能走进去的 3D 世界：物体单独出网格带碰撞，背景是高斯泼溅，可导入 Unity / Unreal / Blender；需付费 API</div><div class="xg-row"><b>谁在用</b>鹏大囍的 AI 工具箱</div><div class="mk-tags"><span class="mk-biz">游戏 / 建筑可视化</span><span class="mk-heat">小红书 赞 239 · 藏 444</span></div></div></div>
</div>

<a class="anchor" id="x3-s6"></a>

### 影视预演与 AI 视频

3D 不当成品，而当 AI 视频的「构图蓝图」：先用 3D 定机位和运镜，再交给视频模型。何同学团队和 AI 短剧公司都在用。

<div class="gal-grid">
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6abcbf3a0000000001009dc0?xsec_token=AB2SVSU9PoqkSbtEvrXeThirm4ua443FfnOPtQrzFlUhk=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6abcbf3a0000000001009dc0.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://hyper3d.ai/" target="_blank" rel="noopener"><img src="posters/logo-hyper3d.png" alt="">Hyper3D Rodin</a><div class="gal-cap"><b>示例</b>iPhone 18 视频片头：Rodin 把现场物体照片生成可拆件的 3D 模型，搭出拍摄空间预演多米诺路线，4 天完成</div><div class="xg-row"><b>谁在用</b>何同学团队（Hyper3D 官方幕后）</div><div class="mk-tags"><span class="mk-biz">品牌片 · 一镜到底</span><span class="mk-heat">小红书 赞 1,859 · 藏 2,056</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6aa7d98c0000000026014c15?xsec_token=ABW2FE_lWlWdyYKOX8ePHrzkyNhkTD_8khy6JbgIZyGU8=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6aa7d98c0000000026014c15.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://github.com/ahujasid/blender-mcp" target="_blank" rel="noopener"><img src="posters/logo-github.png" alt="">Codex + Blender MCP</a><div class="gal-cap"><b>示例</b>Codex 经 MCP 在 Blender 搭白模做预演，先控制构图、机位和复杂运镜，提高 AI 视频生成成功率</div><div class="xg-row"><b>谁在用</b>小林Kara</div><div class="mk-tags"><span class="mk-biz">AI 视频预演</span><span class="mk-heat">小红书 赞 1,707 · 藏 2,417</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6a59768b000000001303d671?xsec_token=AB2JahK56MhqvZ1aoZQnowWGc109UqC_N3x_wm-u1n2IM=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6a59768b000000001303d671.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://github.com/ahujasid/blender-mcp" target="_blank" rel="noopener"><img src="posters/logo-github.png" alt="">Blender MCP（Sol）</a><div class="gal-cap"><b>示例</b>Blender 里只放一根参考方块 + 16 台摄像机，73% 的计划切点在 ±0.6 秒内命中；只传镜头信息反而动作更自然</div><div class="xg-row"><b>谁在用</b>天梦君</div><div class="mk-tags"><span class="mk-biz">动作镜头</span><span class="mk-heat">小红书 赞 435 · 藏 445</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6ae1ecfa0000000023007737?xsec_token=ABUrQj_5U43vWwBIj1tIacyID_2IlcEWApzKV2UiKBlbk=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6ae1ecfa0000000023007737.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://hyper3d.ai/" target="_blank" rel="noopener"><img src="posters/logo-hyper3d.png" alt="">Hyper3D WorldGen</a><div class="gal-cap"><b>示例</b>一张洗衣店照片自动拆成可单独编辑的 3D 模型，搭好场景再交给视频模型做动画</div><div class="xg-row"><b>谁在用</b>Parallel Color</div><div class="mk-tags"><span class="mk-biz">场景搭建</span><span class="mk-heat">小红书 赞 296 · 藏 265</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6ad89594000000003301fd48?xsec_token=ABBpZEnzBaI6sS_Swpe8pNaWZ6MV_n0qUf8_iL-1CmV-U=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6ad89594000000003301fd48.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.blender.org/" target="_blank" rel="noopener"><img src="posters/logo-blender.png" alt="">Blender 白模预演</a><div class="gal-cap"><b>示例</b>最近很多承接 Blender 白模的单子：同一套剧本、同一套白模工程，换不同 AI 美术包装，量产十几套短剧压成本</div><div class="xg-row"><b>谁在用</b>千叶真名</div><div class="mk-tags"><span class="mk-biz">AI 短剧量产</span><span class="mk-heat">小红书 赞 316 · 藏 278</span></div></div></div>
</div>

<a class="anchor" id="x3-s7"></a>

### 产品外观与工业件

硬件和电商产品：外壳、产品展示页。目前案例少，是 3D 线里最空的一格。

<div class="gal-grid">
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6aaaa52f0000000026016572?xsec_token=ABv4CvemqLeuFMynnuZLrWGNmZxLFrCWQlegcYml5Ntso=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6aaaa52f0000000026016572.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://www.freecad.org/" target="_blank" rel="noopener"><img src="posters/logo-freecad.png" alt="">Codex + FreeCAD</a><div class="gal-cap"><b>示例</b>Codex 驱动 FreeCAD 给电路板做外壳，拓竹打印出来真的装上了（工具见封面）</div><div class="xg-row"><b>谁在用</b>天桥底下一书童</div><div class="mk-tags"><span class="mk-biz">电路板外壳</span><span class="mk-heat">小红书 赞 1,876 · 藏 2,061</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6aa892c1000000002502d4d7?xsec_token=ABvM5QVgcOfPq8Z295-ZTxphAVZ3_nWlg8-7jgoDXuOGc=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6aa892c1000000002502d4d7.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://openai.com/codex/" target="_blank" rel="noopener"><img src="posters/logo-codex.png" alt="">Codex（GPT-6 Astra）+ Blender</a><div class="gal-cap"><b>示例</b>Astra 调 Blender 优化 Keyshot 导出的耳机模型：拓扑、烘焙、丝印、多色版本，再做成开合动画的官网页，适配 PC 和手机</div><div class="xg-row"><b>谁在用</b>CHENcc10</div><div class="mk-tags"><span class="mk-biz">电商产品页</span><span class="mk-heat">小红书 赞 403 · 藏 231</span></div></div></div>
<div class="gal-card mk-card xg-card"><a href="https://www.xiaohongshu.com/explore/6adf5113000000001802c6c1?xsec_token=ABQg9pAr-D2cJg6uLuPJ2f69ecSBTRSVYYoiciF0SD2DI=&amp;xsec_source=pc_search" target="_blank" rel="noopener"><div class="gal-poster" style="background:url('market/posters/xhs-6adf5113000000001802c6c1.jpg') center/cover no-repeat,#1b1f27"><span class="gal-play">↗ 看示例</span></div></a><div class="gal-meta"><a class="xg-proj" href="https://hyper3d.ai/" target="_blank" rel="noopener"><img src="posters/logo-hyper3d.png" alt="">Hyper3D Rodin</a><div class="gal-cap"><b>示例</b>测试 Rodin 能不能做工业建模</div><div class="xg-row"><b>谁在用</b>AI Token</div><div class="mk-tags"><span class="mk-biz">工业建模</span><span class="mk-heat">小红书 赞 419 · 藏 461</span></div></div></div>
</div>

<!--/XG-->

<a class="anchor" id="x3-3"></a>

## 3 Insights

- **好作品都是「3D 生成模型出资产 + 大模型搭场景」。** T-BOY 直说 GPT-6 单独建模只会堆几何体；KurTips、《小王子》、蛋岛都是 Tripo 或 Hyper3D 出资产，大模型负责搭场景、写交互。
- **3D 当「构图蓝图」，比当成品更值钱。**
  - 何同学团队用 Rodin 把现场物体变成可拆件模型，预演一镜到底，4 天完成。
  - 天梦君只给 Blender MCP 一根参考方块 + 16 台摄像机，73% 的计划切点在 ±0.6 秒内命中。
  - 千叶真名：同一套剧本、同一套白模，换 AI 美术包装能量产十几套短剧。
- **code 路线已经冒头。** Codex + FreeCAD 做电路板外壳并装上、Codex + Blender 批量做 2770 个城市资产、Astra 写几何节点做程序化植物，都是「代码就是交付物」，对应 Overview 里的 3D 资产生产（code）。
- **打印绕开了 AI 3D 最弱的环节。** 手办不需要好拓扑、UV 和绑骨，所以 Hitem3D、Rodin、拓竹 MakerLab、Meshy × MakerWorld 都在抢这个入口。

下一步：盯两件事。一是 3D 预演给 AI 视频当输入，已经有人付费；二是 CAD 和产品件，代码路线最直接，但案例还少。

<a class="anchor" id="x3-4"></a>

## 4 Data Caliber

- **来源**：小红书网页版搜索，2026-11-03 抓取，每个关键词按综合排序取前 2 页（约 40 条）；本轮 20 个 3D 关键词里 13 个有结果，去重后 327 条。
- **待补**：AI CAD 建模、AI 3D 电商展示、AI 3D角色 绑骨、SAM 3D、UE5 AI、Houdini 程序化 AI、世界模型 3D 这 7 个关键词结果为空（采集进程中断），账号触发验证码后暂停，待补搜。
- **热度与工具份额**：口径同 WebDev Gallery。
- **数据文件**：同 WebDev Gallery。

</div>

