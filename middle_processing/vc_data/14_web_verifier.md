# 14 Web 前端产出的确定性验证：能力清单、判别力测法、本机实测

本文只做 **Web / DOM 侧不需要 VLM 就能判的信号**。
视觉奖励（像素、感知、VLM judge、rubric）已在 `04_verifier.md` 与 `webdev-data/` 的第七章覆盖，本文不重复。
方法论照搬 3D 侧（`90_local_experiments.md`、`91_3jsbench_verified.md`）：分层、准入测试、变异测试、留出验证、作弊测试。

代码 `scripts/vc_verifier/web/`，日志 `scripts/vc_verifier/web/BENCH_LOG.md`。
核实日期统一 **2026-10-15**；工具版本：Chrome 148.0.7778.97 无头 + SwiftShader、node v20.18.0、axe-core 4.12.1。

---

## 0 结论先行

1. **Web 侧的确定性信号比 3D 侧强得多，因为状态本来就是可读的。**
   本机 22 个带标签变异上，五层程序化 verifier **22/22**（检出 11/11，误杀 0/11）；
   两遍全量重跑 **判定翻面 0、明细逐字节一致**。3D 侧的对照是 47/47，但要先自己造体素和剪影；
   Web 侧的读数全是浏览器原生 API 直给。

2. **这里的问题不是「像素噪声淹没信号」，是「信号根本不在像素里」。**
   参考页自比自的像素差是 **0.000**（逐像素完全一致，噪声地板为零），
   但 11 个该挂的变异里 **7 个在 1440 首屏截图上与参考完全相同（相似度 1.0）**。
   给单张截图配最优阈值也只有 **14/22**、检出 **4/11**，且已经开始误杀等价重写。
   零噪声 + 四成检出，说明截图这个观测口就是看不到这些错误。

3. **多视口不是锦上添花，是必需的一维。**
   只看 1440 单视口 12/22（检出 1/11），加上 375 与 768 后 13/22（检出 2/11）。
   窄视口溢出这一类在桌面视口上完全不可见。公开 benchmark 里**没有一家**把多视口一致性做成确定性判据（见 §3.6）。

4. **a11y 是全表唯一「确定性 reward + RL 就能赢闭源」已被公开验证的维度。**
   A11yn（arXiv 2510.13914 v2）用 axe-core 严重度加权违例做 GRPO reward，
   Qwen2.5-Coder-7B 的 IR_Axe **0.40 → 0.05**，低于 GPT-5.1 的 **0.13**、Gemini 3 Pro 的 0.24、Claude Sonnet 4.6 的 0.45。
   但它的口径有五个坑（§3.1），其中最要紧的三条：
   **reward 与评测主指标是同一个量**（reward = 1 − IR_Axe），所以 0.05 vs 0.13 是「直接优化的量 vs 零样本」不是公平比较；
   **20 条「WCAG 规则」里 12 条根本没有 WCAG 依据**；
   **丢弃 axe 的 incomplete** 等于给渐变 / 图片背景上的文字发了对比度豁免。
   它真正的独立证据只有 IR_AChecker（0.26 vs GPT-5.1 的 0.35）和人工 pairwise（胜 39.3% / 平 39.3% / 负 21.4%）。

5. **规则引擎没有大家以为的那么「全自动」。**
   axe-core 4.14.0 共 **105 条规则**，其中 **64 条（61%）带 needs review**，真正纯自动可判的只有 **41 条（39%）**；
   9 条默认关闭，**WCAG 2.2 唯一那条 `target-size` 就在关闭名单里**。
   「axe 自动覆盖 57% 的 WCAG」是失真转述：57% 的分母是**问题实例条数**（Deque 的 13000 页 / 约 30 万问题样本），
   按 WCAG 成功准则条数算，业界共识仍是 20~30%，Deque 自己在同一篇里引了这个数。

6. **作弊是真能作弊的，而且第一版判据挡不住。**
   手写 7 个作弊页：第一版挡住 5 个。两个漏的分别是
   「把不合格文字藏起来用伪元素画回屏幕」和「加载时硬编码写存储、按钮其实不工作」。
   补两条判据后 6/7；剩下那一个是 **axe 的结构性盲区**（伪元素文字连 incomplete 都不报，对应 axe issue #2680，至今 open），
   确定性信号在这里确实到顶了。

7. **成本可以忽略。** 单次完整探针 **4.9 秒**，其中工具开销极小：
   浏览器启动 181ms、新页加载 61ms、注入 axe 72ms、`axe.run` 30~71ms、复用浏览器开页约 50ms/页。
   4.9 秒里绝大部分是我自己写的固定 settle 等待和 40 帧采样，要吞吐可以压到 1 秒以内。
   对照 3D 侧单次探测 0.8~1.0 秒（但那是纯渲染，不含状态机）。

---

## 1 可确定性判定的 Web 能力清单

判据分五层，命名沿用 3D 侧的 L0~L3 习惯，改成 W0~W4。**门控是乘法的**：任一层挂即判挂。

```
W0 正确性门   控制台报错 / 未捕获异常 / 未捕获 Promise / 4xx5xx / 请求失败 / 混合内容
W1 布局与响应式  三视口下的横向溢出、越界、截断、零尺寸、遮挡、两两重叠、断点列数
W2 可访问性    axe-core 违例（含 needs review 闸）+ 语义结构 + 键盘可达 + 焦点可见
W3 交互与状态   状态机断言（模态框 / 标签页 / 表单校验 / 路由 / 本地存储往返）
W4 性能预算    资源数与体积、长任务、帧间隔、CLS、DOM 节点、堆、重排重绘计数
```

### 1.1 可访问性（W2）

| 查什么 | 用什么工具读 | 判据怎么写 | 已有公开基准 / 规则引擎 | 误判风险 |
|---|---|---|---|---|
| axe-core 全量违例 | 注入 `axe.min.js`，`axe.run(document, {resultTypes:['violations','incomplete']})` | critical + serious 节点数 = 0；带 `wcag*` tag 的节点数 = 0 | axe-core 4.14.0（105 条规则 / 96 默认启用）；A11yn 2510.13914；WebAccessBench（Zenodo 10.5281/zenodo.18750348） | **按 impact 当 reward 要小心**：impact 声明在 check 级不是 rule 级，同规则不同 check 可报不同 impact。30 条带 `best-practice` tag 的规则**无 WCAG 依据**，混进分子会让「WCAG 合规度」名不副实 |
| needs review（incomplete） | 同上返回的 `incomplete[]` | **至少对 `color-contrast` 一族把 incomplete 也当闸**（本机实测：不加这条闸，「隐藏真文字 + 伪元素画回」能直接绕过） | axe `doc/API.md`：incomplete 的定义是「既不能判定通过也不能判定失败」 | 全量 incomplete 当闸会误杀（渐变背景是合法设计）。只对对比度族开闸是折中 |
| 对比度 | axe `color-contrast`（impact serious，tags `wcag2aa` / `wcag143`） | 违例 + 该规则的 incomplete 都为 0 | — | **官方设计就会漏**：`color-contrast.json` 把判不了的原因写死成 16 个 key，`bgGradient` / `bgImage` / `fgAlpha` / `bgOverlap` / `pseudoContent` / `outsideViewport` 全部落 incomplete 而非 violation。渐变背景是 LLM 生成页的常见写法，等于自动豁免。相关 issue #4628 / #2680 / #3464 至今 open |
| 语义结构 | `document.querySelectorAll` 自查：`html[lang]`、`h1` 数、标题层级跳级数、`main` / `nav` / `header` landmark 数 | lang 非空、h1 = 1、跳级 = 0、main ≥ 1、nav ≥ 1 | axe 对应 `html-has-lang`（wcag311）、`page-has-heading-one` / `heading-order` / `region` / `landmark-one-main`（**后四条都是 best-practice，不是 WCAG**） | 单页应用动态插入标题会抖；要在 load 后固定时刻读 |
| 替代文本 / 可访问名 | `img:not([alt])`、`button` 无文本且无 `aria-label`、`input` 无 `label[for]` 且无 `aria-label(ledby)` | 全部 = 0 | axe `image-alt` / `button-name` / `label`（均 wcag2a / 412，Lighthouse 权重 10） | `alt="image"` 这种**语法通过语义无效**的写法规则引擎抓不到（Calò et al. CHI EA'26 的批评点）。想抓只能上 LLM/VLM |
| ARIA 引用完整性 | `aria-labelledby` / `aria-controls` / `aria-describedby` 指向的 id 是否存在 | 悬空引用 = 0 | axe `aria-valid-attr-value` 等 | 自定义元素（`ElementInternals`、Shadow DOM）上 axe 有一串 open 的误报 issue：#4750 / #5409 / #5450 / #5162 / #4048 / #5028 / #5351 |
| 假按钮 | 被当按钮用（有 `onclick` 或按钮类名）但不是 `button` / `a` / `input`，且没有 `role=button` + `tabindex` | = 0 | — | 自己写的启发式，会误伤「容器上做事件委托」的合法写法。本机实测对此做了白名单（只认按钮类名与 `onclick`） |
| 键盘可达 | 反复 `page.keyboard.press('Tab')`，读 `document.activeElement.id` | 题面钉死的交互元素清单必须全部可达 | — | **必须有题面给定的交互元素清单**，否则会退化成「verifier 比问题描述知道得多」（3D 侧踩过，见 90 节 §5）。本机实测用 11 个 id 的白名单 |
| 焦点可见 | 聚焦后读 `outlineWidth` / `outlineStyle` / `boxShadow` | 不存在「既无 outline 又无 box-shadow」的可聚焦元素 | WCAG 2.4.7 | 用背景色变化、border 变化做焦点指示的合法写法会被误杀。阈值要留口子 |
| 点击目标尺寸 | `getBoundingClientRect()` + 间距 | **24 × 24 CSS px**（WCAG 2.2 SC 2.5.8），或 24px 直径圆不相交 | axe `target-size`（**默认关闭**）；Lighthouse 现行审计也是它（旧的 `tap-targets` 48px 口径已在 LH 12.0.0 被替换） | 「48×48」是旧口径，别再用 |

**引擎选型要先对齐口径**，四套引擎的规则集、严重度分级、「需人工」归类全不一样：

| 引擎 | 最新版 | 规则 / 审计数 | 纯自动可判 | 需人工的类别 | 谁在用 |
|---|---|---|---|---|---|
| axe-core | 4.14.0（2026-10-05） | **105**（96 默认启用） | **41 / 105** | `incomplete` 64 条涉及 | A11yn、WebAccessBench、microsoft/a11y-llm-eval、Lighthouse 底层 |
| Lighthouse accessibility | 13.5.0（2026-09-18） | 76 auditRefs / **58 计分**，权重和 **416** | 每条审计**二值 pass/fail** | 10 条 manual（权重 0） | WebCoderBench |
| IBM Equal Access | 4.0.34（2026-09-08） | **175** | VIOLATION 143 | RECOMMENDATION 37 / INFORMATION 2 | A11YBench、FeedA11y |
| HTML_CodeSniffer | 2.5.1（**2020-04-13**，6 年未更新） | WCAG2AA：52 sniff / 152 消息 | **Error 60** | Warning 38 + Notice 54 | pa11y 的默认 runner |

两条额外的坑：
- **Lighthouse 分不能和 IR_Axe 互为佐证**。它每条审计是二值的（官方原文：一个按钮没名字，整条审计就是 0 分），
  而 IR_Axe 是节点级密度。A11yn 的 Lighthouse 90.88 → 97.68 与 IR_Axe 0.40 → 0.05 是两个粒度。
- **pa11y + axe 和裸 axe 的违规数不一样**：pa11y 的 `--level-cap-when-needs-review` 默认是 `error`，
  也就是把 axe 的 needs review 直接升级成错误。

### 1.2 布局与响应式（W1）

| 查什么 | 用什么工具读 | 判据怎么写 | 已有公开基准 / 工具 | 误判风险 |
|---|---|---|---|---|
| 横向滚动 | `document.scrollingElement.scrollWidth - documentElement.clientWidth` | 差 ≤ 1px。**用 `documentElement.clientWidth` 不要用 `window.innerWidth`**，后者含滚动条 | MDN 把 `scrollWidth > clientWidth` 直接写成示例函数 `isOverflowing` | `scrollWidth` / `clientWidth` 的**分数像素取整规则 MDN 未明文**（只写 "An integer"），所以必须留 1px 容差。quirks 模式下 `scrollingElement` 可能是 null |
| 元素越界 | 遍历可见元素的 `getBoundingClientRect()` | `right > 视口宽 + 1`，或 `left < -1 且 right > 0` | — | **经典的 `.skip{left:-9999px}` 跳转链接会被误报**，本机实测踩到，修法是「整体在视口外不算越界，只算一半在里一半在外」 |
| 文字截断 | `el.scrollWidth > el.clientWidth + 1` 且 `overflow-x != visible` | = 0 | — | 故意做的单行省略号（`text-overflow:ellipsis`）是合法设计，需要白名单 |
| 关键元素零尺寸 / 缺失 | 题面钉死的元素清单 + `getBoundingClientRect()` + `getComputedStyle` | 宽高 ≥ 1px、`visibility != hidden`、`opacity > 0.05` | — | 同样依赖题面清单 |
| 遮挡（点不到） | `document.elementFromPoint(中心)` 必须命中自己或后代 | 被遮挡数 = 0 | Playwright 的 actionability「Receives Events」用的就是同一口径（命中测试）；`Element.checkVisibility()` **明文不管遮挡** | 中心点在视口外的元素要排除。`IntersectionObserver` 的 `trackVisibility:true` 能查遮挡，但官方说「算法保守，可能漏掉技术上可见的元素」且计算昂贵 |
| 两两重叠 | 关键元素矩形相交面积 / 较小者面积 | ≤ 0.05 | **`layout-lint`**（npm 1.2.1，2026-08-27，声明式 DSL：`main below header 24px;`、`card-1 same-width card-2;`、`count visible card-* is >= 3;`）；Galen Framework（语义最全但维护状态存疑） | 合法的徽章叠在卡片角上就是重叠；判据只能限定在「文本与交互元素之间」 |
| 断点行为 | 三视口下同一容器的子项分几列（同 top 的个数） | 375 单列、1440 ≥ 2 列 | **公开 benchmark 零结果**（见 §3.6）；SE 侧有 **ReDeCheck**（ISSTA 2017，RLG 响应式布局图 + 视口连续扫描，26 个生产页里在 16 个页上找到 33 处失败）与 **ReDeFix**（arXiv 2511.00678，ICSME 2025） | **绝不能把判据绑在表现型类名上**。本机实测第一版用 `.card` 选择器，被「类名改哈希名」这个等价重写打成误判。改成结构化定位（主内容里第一个有 ≥2 个子项的列表）才对 |
| 布局跳动 | `PerformanceObserver({type:'layout-shift'})`，累加 `value`（跳过 `hadRecentInput`） | CLS ≤ 0.1（web.dev，75 分位；> 0.25 为 poor） | web.dev `defining-core-web-vitals-thresholds` | 无头环境下 CLS 常是 0，区分度低 |

工具侧补充：**纯像素视觉回归（BackstopJS / Percy / reg-suit / Playwright `toHaveScreenshot`）不是 layout linter**，
它能告诉你「图变了」，不能告诉你「按钮被盖住了」。本课题要的是后者。

### 1.3 交互与状态逻辑（W3）

| 查什么 | 用什么工具读 | 判据怎么写 | 已有公开基准 | 误判风险 |
|---|---|---|---|---|
| 组件状态机 | Playwright / Puppeteer 驱动点击 + `page.evaluate` 读 DOM 状态 | 每条断言带**前置态 + 终态 + 往返**三段。例：模态框「点击前必须 hidden → 点击后可见且尺寸 > 10px → 关闭后 hidden」 | Web-Bench（2505.07473，50 项目 × 20 任务 = 1000，纯 Playwright E2E，无 judge）；WebApp1K（2408.00019，1000 题，Jest(jsdom) + RTL，无真浏览器） | **只断终态会被硬编码骗过**。本机实测的 K6 作弊页就是加载时无条件写 dark，按钮不工作，而终态断言全过 |
| 表单校验 | HTML 原生约束校验 API：`checkValidity()`、`validity`（11 个只读布尔）、`validationMessage`、`:invalid` / `:user-invalid` | 非法输入 → 错误文案非空 且 成功态隐藏 且 `checkValidity()` 为 false；合法输入 → 反之 | FullFront（2505.17399）的交互成功率用的是同类可执行断言（hover 后 `textDecoration` 含 underline、`fontWeight ≥ 600`、`.modal` 或 `[aria-modal=true]` 等） | 两个硬坑：`tooLong` 在 Gecko 下**永远 false**；`tooLong` / `tooShort` 要求 dirty value flag 且最后一次修改来自**用户编辑**，用 `evaluate` 直接赋 `el.value` 不触发。`{...el.validity}` 在部分引擎下是空对象，要显式枚举 11 个键 |
| 路由 | 改 `location.hash` 或 `page.goto`，读 `aria-current` / 可见面板 | 导航态与 URL 一致 | Vision2Web（2603.26648）L2/L3 走 workflow agent，**不是确定性判据** | 单页应用的异步路由要等；等待本身引入非确定性（见下） |
| 本地存储 | `page.evaluate(() => JSON.stringify(localStorage))`，或 Playwright `context.storageState()` | 清空 → 初始态正确 → 操作 → 存储值正确 → 刷新 → 仍正确 → 再操作 → 能回到初始态 | — | **sessionStorage 没有官方持久化 API**（Playwright 原文：does not provide API to persist session storage），只能 `evaluate` 读、`addInitScript` 逐 key 恢复。`storageState({indexedDB:true})`（v1.51）可以带 IndexedDB，但返回结构里这几个字段**未文档化**，别按文档写死 schema |
| 状态覆盖率 | model-based testing | 路径枚举 | **`xstate/graph`**（现推荐，`getShortestPaths` / `getSimplePaths` / `createTestModel().getPaths().test()`，官方称 simple paths 提供完整转移覆盖）；**`fast-check`** 4.10.2 的 `ICommand` + `fc.asyncModelRun` / `fc.scheduledModelRun`（专测竞态，失败给 seed + replayPath 可精确重放） | **`@xstate/test` 已 deprecated**（npm latest 0.5.1，2022-01-27），别再用。fast-check 官方文档**没有 UI / 浏览器示例**，胶水层要自己写 |

**「自动重试断言 ≠ 确定性断言」**，这条要写进检查项规范：

| 维度 | Playwright 的 web-first 断言（32 条） | 确定性断言 |
|---|---|---|
| 结果是什么的函数 | 状态、时间、调度、机器负载 | 只是状态 |
| 失败含义 | 「5 秒内没看到期望状态」——可能是真错，也可能只是慢 | 状态不符 |
| 掩盖什么 | **掩盖性能回归与竞态**：接口从 50ms 退化到 4.9s，断言照样绿 | 不掩盖 |
| 瞬态 | 一闪而过的 spinner 会漏判；会自己翻回去的状态会误判 | 不受采样影响 |

所以真正零噪声的检查项只能建立在三类读数上：**事件流**（console / pageerror / requestfailed / response / Audits）、
**存储快照**、**原生 API 的同步读数**。这三类都是一次读取、与时间无关。
另外 Playwright 官方对 flaky 给了可操作定义：**首次运行失败、重试通过**——这个定义可以直接当指标。

### 1.4 性能预算（W4）

| 查什么 | 用什么工具读 | 判据怎么写 | 阈值依据 | 误判风险 |
|---|---|---|---|---|
| 首屏资源数与体积 | 请求拦截自己记账，或 Lighthouse 的 `resource-summary` | 资源数 ≤ N、字节 ≤ M（本机实测取 20 个 / 300KB，参考页 13 个 / 43.6KB） | **`budget.json` 已在 Lighthouse 12.0.0（2024-04-22）被移除**（changelog 的 breaking change 里一行 `remove budgets`）。今天只能走 Lighthouse CI 的 `resource-summary:<type>:(size\|count)` 断言，**单位是字节**（旧 budget.json 是 KiB）。9 个 resourceType：`total / document / script / stylesheet / image / media / font / other / third-party` | 「首屏 130~170KB」这个常被引的数字**出处是 Alex Russell 2017 年的个人博客**，不是 web.dev；是区间不是单值，前提是约 200 美元安卓机 / 400Kbps / 400ms RTT 下 TTI < 5s。写成「170KB JS 预算」是失真 |
| 长任务 | `PerformanceObserver({type:'longtask', buffered:true})` | 最长任务 ≤ 100ms（本机实测阈值；参考页 0 个长任务） | **50ms 的定义出处是 W3C Long Tasks API**（Working Draft, 2026-03-19）：「duration exceeds 50ms」，且 §4.1 写明小于 50ms 直接 abort。50ms 的来由在 RAIL：输入响应要在 100ms 内，其中只有约 50ms 能给输入处理 | 无头 + 软渲染下首屏偶发长任务；阈值要高于噪声。更现代的口径是 LoAF 的 `blockingDuration`，但 MDN 标 **Limited availability**，Chrome 起始版本号该页未给 |
| 帧间隔 | `requestAnimationFrame` 时间戳差分取分位 | p95 ≤ 34ms（两帧 @60Hz；参考页 16.7~16.8ms） | **「p95 帧间隔」没有官方口径**，规范和 web.dev 都没有，要标成自定义指标。官方口径是 LoAF `blockingDuration` + 长任务计数 | rAF 频率「generally match the display refresh rate」，60/75/120/144Hz 都常见，所以**帧预算不是跨机常数**；后台标签页 rAF 会被暂停 |
| 重排 / 重绘计数 | CDP `Performance.enable` + `Performance.getMetrics()`，取 `LayoutCount` / `RecalcStyleCount` 的**交互前后差分** | 一次完整交互脚本引起的 Layout ≤ 20、RecalcStyle ≤ 40（参考页 2 / 4） | 字段名不在 protocol JSON 里，权威来源是 Blink 的 `inspector_performance_agent.cc`，共 **36 个** metric。⚠️ 所有 `*Duration` / `ThreadTime` / `ProcessTime` 单位是**秒**不是毫秒。Puppeteer 的 `page.metrics()` 只暴露 13 个子集 | 绝对计数跨 Chrome 版本会漂；用差分比用绝对值稳 |
| 内存 / DOM 规模 | 同上的 `JSHeapUsedSize`、`Nodes` | 堆 ≤ 12MB、节点 ≤ 1500（参考页 2.77MB / 852 节点）| — | 本机实测这两个在 5 次重复里**逐字节一致**，可以当强信号。但不同 Chrome 版本之间不可比 |
| CLS / LCP / INP | `PerformanceObserver`；现场采集用 `web-vitals` 6.2.3（含 attribution build） | CLS ≤ 0.1 / LCP ≤ 2.5s / INP ≤ 200ms（poor 线 0.25 / 4.0s / 500ms） | web.dev `vitals` + `defining-core-web-vitals-thresholds`，**75 分位、移动与桌面分段**；阈值定法原文：至少 10% 的来源能达标，最差的 10~30% 判 poor | web.dev **不给 FCP / TBT 的数值阈值**（TBT 只被定性为 INP 的实验室代理）。CrUX API 的 p75 是 28 天滚动 + 滞后约 2 天 + 配额 150 QPM，**不能当 PR 级闸** |

### 1.5 正确性类（W0）

| 查什么 | 用什么工具读 | 判据怎么写 | 误判风险 |
|---|---|---|---|
| 控制台报错 | `page.on('console')` → `.type()` | error 数 = 0 | **字面量跨框架不一致**：Playwright 是 `'error'` / `'warning'`，Puppeteer 是 `'error'` / `'warn'` 还多一个 `verbose`。**Puppeteer 的 console 事件包含页面抛错，Playwright 不包含**（官方测试 `should not receive console message for pageError` 固化了这一点）→ Puppeteer 下会重复计数 |
| 未捕获异常 | `page.on('pageerror')` | = 0 | — |
| 未捕获 Promise | 两框架都**没有专门事件**。确定性做法是 `addInitScript` / `evaluateOnNewDocument` 里挂 `window.addEventListener('unhandledrejection')` 自己计数 | = 0 | Playwright 当前由 `pageerror` 覆盖，但**规范层无承诺**，只有测试用例和 issue #14165 作为行为证据。别依赖 |
| 404 / 5xx | `page.on('response')` → `.status() >= 400` | = 0 | **404 不会触发 `requestfailed`**。官方原文：HTTP 错误响应「从 HTTP 角度仍是成功响应」，走 `requestFinished`；只有拿不到 HTTP 响应（如 `net::ERR_FAILED`）才算 failed。另外**别用 `!response.ok()`**，`ok()` 的定义是 200~299，3xx 会被判 false |
| 请求失败 | `page.on('requestfailed')` + `request.failure().errorText` | = 0（需白名单） | **`ERR_ABORTED` 在单页应用里大量正常出现**（导航打断、AbortController），必须白名单，否则全是误报。Puppeteer 还额外警告「不保证有 failure text」 |
| 混合内容 | **首选 CDP `Audits.issueAdded` 的 `MixedContentIssue`**：`{resolutionStatus, insecureURL, mainResourceURL, request?, frame?}`，`resolutionStatus` 三态 `MixedContentBlocked` / `MixedContentAutomaticallyUpgraded` / `MixedContentWarning` | = 0 | **三条常见做法全是死路**：`Security.securityStateChanged` 的 PDL 描述就是 "No longer being sent."；`Security.InsecureContentStatus` 的每个字段注释是 "Always false."；`Response.securityDetails()` 只有 TLS 证书信息，无混合内容语义。CSP `block-all-mixed-content` 已 obsolete；`upgrade-insecure-requests` **反而会掩盖问题**。兜底只能匹配控制台消息前缀 `Mixed Content: The page at '<URL>'`（Blink 六处消息统一这个前缀），但耦合文案，且 Playwright 的 `ConsoleMessage` 没有 source 字段 |
| HTML 合法性 | **自建 `html-validate`**（npm 11.16.2，6 个预设：`recommended` / `standard` / `a11y` / `document` / `prettier` / `browser`） | 选定预设下 0 error | W3C Nu Checker 的 JSON API 可用（`?out=json&doc=`），但①共享代理首请求会收到 **429**；②官方 about 页明确警告「检查器行为会变，今天 0 error 明天可能报错」→ **要确定性必须自建并 pin 版本** |
| 安全响应头 | **OWASP Secure Headers 的机器可读清单**（`ci/headers_add.json` / `headers_remove.json`，2026-10-04 更新） | 应加 13 个（带推荐值，如 `Referrer-Policy: no-referrer`、`HSTS: max-age=63072000; includeSubDomains`、`X-Content-Type-Options: nosniff`、`X-Frame-Options: deny`），应删约 90 个指纹头 | 本地沙箱页无服务端，这一类只在真实部署场景可用 |
| 其他结构化问题 | CDP `Audits` 的 `InspectorIssueCode` 共 31 种。对确定性检查最有用的：`ContentSecurityPolicyIssue`（比 `securitypolicyviolation` 更结构化、含 report-only）、`CorsIssue`、`BlockedByResponseIssue`、**`StylesheetLoadingIssue`**（CSS 加载/解析失败，看 response 状态码看不出）、`QuirksModeIssue` | 按需 | `Audits` 整个 domain 标 Experimental。`Audits.checkContrast` **在当前 PDL 里已不存在** |

### 1.6 可复现性（横切所有层）

| 要素 | 官方手段 | 定性 | 坑 |
|---|---|---|---|
| 时钟 | Playwright `page.clock.{install, setFixedTime, setSystemTime, fastForward, runFor, pauseAt, resume}`，**全部 Added in v1.45** | **官方** | `setFixedTime` 固定 `Date` 但**定时器继续跑**；`setSystemTime` 改时间**不触发**定时器；`fastForward` 每个到期定时器**最多触发一次**，`runFor` 全部触发。**无 uninstall**。Puppeteer **没有等价 API**（只有 `emulateTimezone`），要冻结只能走 CDP 或自注 |
| 虚拟时间（CDP） | `Emulation.setVirtualTimePolicy`，policy 三态 `advance` / `pause` / `pauseIfNetworkFetchesPending` | **Experimental** | 配 `budget` 用尽后发 `virtualTimeBudgetExpired`；`maxVirtualTimeTaskStarvationCount` 防死锁 |
| 动画 | `page.emulateMedia({reducedMotion:'reduce'})` / `emulateMediaFeatures`；浏览器 flag `--force-prefers-reduced-motion`；截图 `animations:'disabled'` | **官方** | **默认不是 reduce**（Playwright 原文 defaults to `'no-preference'`）。`animations:'disabled'` 的语义是：有限动画**快进到完成并触发 `transitionend`**，无限动画取消到初始态、截完再播——不是「冻结在当前帧」 |
| 随机数 | 没有官方 seed 选项。只能 `addInitScript` / `evaluateOnNewDocument` 覆写 `Math.random` 与 `crypto.getRandomValues` | **注入机制官方，覆写本身是 hack** | Playwright 原文：初始化脚本「在 document 创建后、页面脚本执行前」求值，但**多个脚本之间的求值顺序未定义** |
| 字体 | `--font-render-hinting=none`（默认 `full`，**只在 headless 生效**）、`--disable-font-subpixel-positioning`、`--disable-lcd-text` | **官方 flag** | **没有任何浏览器厂商提供的「字体回退确定性」开关**。工程做法只有两条：基线与 CI 同镜像；截图时用 `style` 强制字体族。另外 `screenshot({scale:'css'})` 是消 DPR 差异的正道 |
| 视口 / DPR | `newContext({deviceScaleFactor})`（默认 1）、`setViewport`、CDP `Emulation.setDeviceMetricsOverride` | **官方** | Playwright 对 `viewport: null` 的官方警告可以直接抄进规范：「让视口取决于操作系统窗口大小，**使测试执行非确定性**」 |
| locale / 时区 / 配色 | `locale`（影响 `navigator.language`、`Accept-Language`、**数字与日期格式**）、`timezoneId`、`colorScheme`（默认 light）、`forcedColors`、`contrast` | **官方** | CDP 的 `setLocaleOverride` 是 Experimental |
| 网络 | 请求拦截 + 从内存返回 + 阻断外域；`serviceWorkers:'block'` | **官方** | 理论基石是 Google 的 hermetic servers：外部依赖因「缺乏确定性或不可用」引入 flakiness，**先消网络，再谈阈值** |
| 一揽子 | `--deterministic-mode` | **官方但 experimental、headless 专用** | 源码注释：它把浏览器置于「begin frame 需通过 DevTools 协议下发」的模式——**用了它就必须自己驱动出帧，否则页面不出帧** |

---

## 2 判别力怎么测：和 3D 侧同构的变异集设计

3D 侧的做法是：参考解 + 一组人工标注「该挂 / 不该挂」的变异 + 阈值先冻结 + 留出集。
Web 侧照搬，但「不该挂」这一侧要换成前端特有的等价重写。

### 2.1 设计原则（三条，照抄 3D 侧并加一条）

1. **阈值只在参考页上校准，变异集上一次都不调。** 跑完如实报告，不回头调阈值。
2. **准入测试三条**：① 参考解必须过（自比自，防判据本身坏掉）；② 该挂的变异必须至少被一层抓到，
   否则这条变异不可验证，**从数据集剔除而不是放松判据**；③ 每条 search 片段在目标文件中必须唯一出现。
3. **判据能查的信息量 ≤ 问题描述给出的信息量。** 本文的 `SPEC`（交互元素清单、必须可见的元素、
   不许遮挡的元素）就是题面的一部分；判据不许查题面没钉死的东西。
4. **（Web 侧新增）判据不许绑在表现型类名、选择器或实现手法上。**
   这是本机实测里唯一一次误判的真因，也是前端相对 3D 的新风险：3D 的几何量天然实现无关，
   而 DOM 的类名、标签、CSS 写法都可以在视觉与功能完全等价的前提下随便换。

### 2.2 该挂的（功能性缺陷）

每一类都要能点名「该被哪条检查抓到」。设计时就写死，跑完对账。

| 变异类 | 具体做法 | 该被哪条抓到 |
|---|---|---|
| 对比度降级 | 正文灰阶提亮到 WCAG 1.4.3 不过 | W2 `axe color-contrast` |
| 替代文本缺失 | 删掉 `img` 的 `alt` | W2 `axe image-alt` + 自查 `imgNoAlt` |
| 语义降级 | 原生 `button` 换成 `div` + `onclick` | W2 键盘可达（Tab 到不了）+ 假按钮自查 |
| 标题层级与 landmark | `h2` 跳成 `h4`，`main` 换成普通 `div` | W2 `headingSkips` + `landmark_main` |
| 窄视口溢出 | 卡片写死 `min-width: 420px` | W1 `h_overflow@375` + `out_of_viewport@375` |
| 遮挡 / 点不到 | 负边距 + `z-index:-1` 让主按钮被页头压住 | W1 `occluded`（中心点命中测试） |
| 表单校验摘除 | 去掉 `required` / `pattern`，校验逻辑只判非空 | W3 `formInvalid` |
| 状态不持久 | 主题切换不落 localStorage | W3 `themePersist` |
| 坏链接 | 图片路径写错 | W0 `http_4xx5xx` + `console_error` |
| 运行时异常 | 脚本尾部一个未定义变量（处理器已全部绑定，所以只炸控制台） | W0 `pageerror` |
| 主线程阻塞 | 启动时同步忙等 300ms | W4 `long_task` |

### 2.3 不该挂的（等价重写）—— 这一侧才是 Web 侧的难点

| 等价重写类 | 具体做法 | 为什么容易被误杀 |
|---|---|---|
| 换 CSS 布局写法 | 卡片容器 flex → `grid-template-columns: repeat(auto-fit, minmax(260px,1fr))` | 列数判据若绑在 flex 属性上就挂 |
| 换类名 | 所有类名改哈希名（模拟 CSS Modules / 构建产物） | **任何绑类选择器的判据都会挂**。本机实测的唯一误判就在这 |
| 换配色 | 整套品牌色换另一个色系，对比度仍达标 | 像素相似度会掉到 0.90，截图类判据必挂 |
| 换单位 | px → rem（16px 基准下渲染等价） | 若判据比对字符串化的样式值会挂 |
| 换组件写法 | 规则拆成原子类（Tailwind 风格）；逐个绑定改事件委托 | 结构哈希、事件监听计数类判据会挂 |
| 换标签 | `section[aria-labelledby]` → `div[role=region][aria-labelledby]` | DOM 标签序列判据会挂 |
| 换资源形态 | 外链 logo 换内联 svg（少一个请求，可访问名保留） | 资源数、DOM 标签序列都会变 |
| 换字体栈 | 换另一组系统字体 | 像素会变，文本盒尺寸会变 |
| 压缩 | HTML 去标签间空白与缩进 | 文本节点结构会变 |
| CSS 简写 / 逻辑属性 | `margin-bottom` → `margin-block-end`，`min-width` → `min-inline-size` | 计算样式读法若按物理属性名取会挂 |

### 2.4 留出集与作弊集

- **留出集**：标签与「预期挂在哪层」先写死，阈值沿用，只跑一次。
  本文的留出集故意选了三类在开发集里没出现过的缺陷（运行时异常 / 标题层级与 landmark / 状态不持久）
  和三类没出现过的等价重写（事件委托 / HTML 压缩 / CSS 简写）。
- **作弊集**：手写「看起来过了判据、实际体验是坏的」页面。
  这一组的目的不是刷分，是找判据的可绕性。3D 侧 7 个作弊页第一轮挡 6 个，本文 7 个第一轮挡 5 个。

---

## 3 已有公开证据（核实）

### 3.1 A11yn —— 唯一「确定性 a11y reward + RL 赢过闭源」的公开证据

| 项 | 核实结果 |
|---|---|
| 标识 | arXiv **2510.13914**（v1 2025-10-15 / **v2 2026-09-07**），cs.SE。延世大 + 首尔大，Youngjae Yu 组 |
| v2 标题 | *A11yn: Aligning LLMs for Web Accessibility-Aware UI Generation* |
| repo | github.com/jeffrobot/A11yn（2026-08-02 创建，1 star，无 license） |
| 会议 | README 自称 COLM 2026 accepted；**OpenReview / COLM 官方列表核不到** |
| 评测集 | **RealUIReq-300**，300 条真实页面 grounded 请求、61 个归一化域、平均 87 词（对照 Screen2Words 6 词）。训练集 UIReq-6.8K 共 6800 条 |
| reward | `1.0 − Σ_v w(impact_v)·|nodes_v| / max(DOM 节点数, 1)`，权重 `{minor .1, moderate .2, serious .3, critical .4}`。`N_*` 是**受影响 DOM 节点实例数**不是违规规则数；基准分 1.0，**reward 无下界**（DOM 小而违规密集时为负）。另有一条格式 reward（`<think>…<answer>…```html` 正则命中给 1.0）。**没有渲染保持、功能保持、视觉相似度任何辅助项** |
| 跑了多少条规则 | **不筛选**：`axe.run` 无 `runOnly`、无 tag 过滤。vendored 的 4.7.2 共 99 条，6 条 `enabled:false`，**实际生效 93 条，其中 30 条是 `best-practice`（零 WCAG tag）**，7 条 experimental（4.7.2 里 experimental 默认不关，会真跑进 reward） |
| 渲染环境 | Playwright headless Chromium、`--no-sandbox`、10s 超时、**默认阻断全部外部请求**（`A11YN_BLOCK_EXTERNAL_REQUESTS=1`）、Tailwind 2.2.19 本地 vendored 并强行改写成唯一 `<link>`。渲染或审计抛异常 → reward 记 0.0 |
| 指标 | `IR_Axe = WVS / 全部 DOM 元素数`；`IR_AChecker = AChecker 违例 / AChecker 标记元素数`。**两个分母口径不同，不可横比** |
| 核心数字 | **A11yn IR_Axe 0.05 / IR_AChecker 0.26 / Lighthouse 97.68 / WVS 662**；GPT-5.1 **0.13** / 0.35 / 92.69 / 3924；Gemini 3 Pro 0.24；Claude Sonnet 4.6 0.45；Qwen2.5-Coder-7B 基座 0.40 |
| 相对降幅 | vs 基座：moderate −92.2%、serious −82.6%、critical −46.8%、WVS −85.2%、**IR_Axe −87.5%、IR_AChecker −58.1%** |
| 零违例页数 | A11yn **177/300**（axe）/ 166/300（AChecker）/ 151/300（两者同时过）；基座 18 / 19 / 12；Best-of-8 79 / 86 / 62 |
| 防 reward hacking | **DOM 归一化是唯一手段**。消融里用裸 penalty，IR 同样降到 0.05，但 DOM 元素/页从 37.02 塌到 **15.20**、appearance 从 3.60 掉到 **2.41** |
| 副作用度量 | 只有两个软指标：Appearance Score（**GPT-5.1 当 judge**，1~5 Likert，A11yn 3.68 / FeedA11y 3.72 / 基座 3.60）与人工 pairwise（5 人 1330 次，胜 39.3% / 平 39.3% / 负 21.4%）。**没有任何功能性硬度量** |
| 超参 | GRPO，lr 5e-5、β(KL) 0.001、num_generations 8、max_completion 3072、temp 0.7、4 × RTX PRO 6000 96GB、ZeRO-3 + vLLM colocate |

**五个必须跟着一起写的坑**：

0. **reward 和评测主指标是同一个量**：`reward = 1 − IR_Axe`。
   所以「IR_Axe 0.05 超过 GPT-5.1 的 0.13」这句话的真实含义是**直接优化的量 vs 零样本**，不是公平比较。
   它的独立验证只有两路：**IR_AChecker 0.26 vs 0.35**（换引擎）和**人工 pairwise 39.3 / 39.3 / 21.4**。
   引用这个结论时必须带上这两个数，否则是在拿训练目标当排行榜。
   另外 **critical 一档 A11yn（25）反而输给 Best-of-8（12）**，论文的解释是训练分布里 critical 稀疏
   （minor 121 / moderate 17581 / serious 12138 / **critical 672**），`button-name`、`select-name` 在训练审计里只出现 135 / 155 次。

1. **版本漂移**：v1 摘要说降 60%，v2 改成 87.5% / 58.1%。同数据集同名字，数字换了。引用必须锁 v2。
2. **12/20 的「WCAG 规则」没有 WCAG 依据**。论文 §6.2.1 标题叫 "WCAG Rule-Level Diagnostics"、
   附录 L 叫 "WCAG Rule ID Mapping"（20 条规则），逐条对回 axe 的 tag：只有 8 条真带 `wcag*`
   （`color-contrast` / `link-name` / `button-name` / `frame-title` / `select-name` / `document-title` / `html-has-lang` / `label`），
   另外 12 条全是 `best-practice`（9 条 landmark / region 族 + `page-has-heading-one` + `heading-order` + `image-redundant-alt`）。
   而它的 headline 原文是「包括 color contrast、**region**、**landmark-one-main** 的大幅下降」——**三个里两个不是 WCAG 条款**。
   再结合训练期 severity 分布（minor 121 / **moderate 17581** / **serious 12138** / critical 672，
   而 axe 里 moderate 几乎全是 best-practice 的 landmark / region 类），reward 的主要驱动力很可能来自非规范规则。
3. **用的是 2023 年的 axe 4.7.2**（发布 2023-05-25），当前是 4.14.0（2026-10-05），落后 3 年 5 个月、7 个小版本。
   我解析了它 vendored 的 bundle：99 条规则，6 条 `enabled:false`，实际跑 93 条，其中 30 条 `best-practice`、7 条 experimental（4.7.2 里 experimental 默认是开的）。
4. **丢弃 incomplete 开了一条 reward hacking 通道**。它的调用是 `resultTypes:['violations']`，
   `_compute_score` 从不读 incomplete。而 axe 官方把渐变背景 / 图片背景 / 半透明前景 / 被遮挡 / 伪元素 / 视口外
   的对比度一律判 incomplete 而非 violation（16 个原因 key 写死在 `lib/checks/color/color-contrast.json`）。
   也就是说**把文字放到渐变背景上，对比度在 reward 里零代价**——而这恰好是 LLM 生成页最常用的写法。
   论文未讨论这一点。

### 3.2 其它 a11y benchmark

| Benchmark | 标识 | 题量 | 判据 | 数字 |
|---|---|---|---|---|
| **WebAccessBench** | **不在 arXiv**，Zenodo DOI 10.5281/zenodo.18750348；conesible.de/wab，8 页白皮书，2026-02-25，CC-BY-SA | 150 UI 任务 × 3 档引导 × 2 样本 = 450 计分/模型 | **axe-core**，缺陷映射到 WCAG 2.2 A/AA，白皮书自己声明「不主张穷尽覆盖」、「只是自动化缺陷负担的**下界**」。打分 `Q_err = 100·2^(−E/2)`、`Q_dom = 100·2^(−R_dom/2)`、`S = 0.5·Q_err + 0.3·Q_dom + 0.2·Z` | 22 模型**全是 F**，overall 11~64，全局均值 26.84；平均错误数（无引导 / 轻引导 / 专家引导）3.22 / 2.01 / 2.17；零错误占比 7.97% / 11.47% / 11.16% |
| **A11YBench** | **无独立 arXiv 号**，是 **A11YRepair**（arXiv 2606.21926，ASE 2026）内部构建的 | 60 repo / 147 页 / **8886 违例** / 45 类；Lite = 10 repo / 2622 违例 | **IBM Accessibility Checker**（不是 axe）。`R_solve = (|V_before| − |V_after|) / |V_before|`；`N_side = |V_after \ V_before|` | A11YRepair Lite **78.15%** solve / 172 side effect / 59.43 美元；headline 76.8% @ 每问题 0.018 美元；三轮迭代 75.41% → **87.49%**，side effect 1.9% → 0.6%。消融反直觉：塞全量 WCAG 知识 **58.74%**，比 selective 的 78.15% 掉 20 点 |
| **microsoft/a11y-llm-eval** | github.com/microsoft/a11y-llm-eval（61 star） | **7 个 test case** × framework/style 维度 | **全表唯一明确写出「双闸」的**：Playwright(Chromium) 渲染 → axe-core → **外加逐 case 手写断言**。原文「Tests only pass if **zero axe-core WCAG failures** AND **all requirement assertions pass**；Best Practice 断言失败不判挂，单独记账」。支持 pass@k | **SOTA 核不到**（不登榜，分数在 report 仓的生成 HTML 里） |
| **WebCoderBench** | arXiv 2601.02430 v3 | 1572 条真实需求 / 24 metric / 9 perspective | a11y 子维度用 **Lighthouse accessibility module**，11 项指标，`score = Lighthouse 分 × 100` | **笔记里的 9.9% 是错的**：那是 Table 6 里 Accessibility 这个 perspective 的**人类偏好权重**（九个权重和为 100%），不是任何模型得分。论文**全文只给 z-score 不给原始百分数**（GPT-5-Codex-High +1.78% 最好，GPT-5-High −2.05% 最差但 overall 第一），所以「a11y SOTA 是 X%」**核不到** |

**笔记里 9.9% 的真身**：A11yn 附录 K 的 Best-of-N 平台值——axe IR 41.2%(N=1) → **9.9%(N=14~20 不再下降)**，AChecker 61.2% → 34.6%，两者都高于 A11yn 的 5.0% / 26.0%。
这个数同时出现在两篇里，笔记串台了。

### 3.3 把 a11y 当 RL reward 的其它工作：几乎是空白

穷搜 arXiv（`all:"WCAG" AND all:"reward"` 只 2 条；`all:"accessibility reward"` 只 2 条；`ti:"accessibility" AND abs:"GRPO"` 无相关）：

| 工作 | 标识 | reward 构成 | 位置 |
|---|---|---|---|
| **A11yn** | 2510.13914 | axe 严重度加权违例 / DOM 规模 | **生成侧，唯一一篇** |
| **Learning to Detect UI Principle Violations via RL** | **2607.20690**（2026-07-22） | RL 训的是 **critic（4B VLM 判别器）**，不是生成器 | 判别侧 |

2607.20690 的细节值得抄：统一 19 条界面质量原则（WCAG 2.2 + 欺骗性设计分类 + 感知/认知/交互理论），
约 10000 个合成注入违例的 Tailwind 页，critic micro-F1 **36% → 84%**，19 条里 13 条 F1 > 80%。
它对规则引擎的评价原文很适合引用：「axe-core 和 Lighthouse 这类基于规则的工具便宜，但**主要只能捕捉机械可查的可访问性问题**」。
它只说 critic「可以为设计感知的代码生成提供 reward 信号」——**未来工作，本文未做 RL 生成**。

**contrast ratio 当连续 reward：核不到任何工作**（`all:"contrast ratio" AND all:"reward"` 返回 0）。
最接近的是 arXiv **2512.05067**（2025-12-04，cs.HC + math.OC）：
把 WCAG 对比度当**约束非线性优化**，在 OKLCH 空间固定色相只调 L 和 C，三阶段（二分 → 梯度下降 → 渐进松弛）；
10000 组色对上解决 **77.22%** 违例，其中 **88.51%** 的修正 ΔE2000 < 2.0（人眼不可察），中位 0.76，中位耗时 0.876ms/色对；开源库 `cm-colors`。
**它不是 RL，但证明了对比度是可做连续可微目标的**——这正是 A11yn 的一个明确改进口子：
`min(1, ratio/4.5)` 这种连续 reward 比 0/1 违例计数信息量大得多。
（CHI / UIST / ASSETS 会议库未穷搜，这块标为未穷尽。）

### 3.4 Web 代码生成 benchmark 的判据构成

核心问题是：**哪些 benchmark 真的不用 VLM？**

| Benchmark | arXiv | 题量 | 确定性程序判据 | LLM/VLM judge | 浏览器驱动 |
|---|---|---|---|---|---|
| **WebRenderBench** | 2510.04097 ✅ | 22.5k 测试页（清洗后 45.1k 对半分） | **100%**：RDA / GDA / SDA 全是 WebDriver 读实时 DOM | 评测侧无（**建库阶段用过 Qwen2.5-VL-7B** 查空白与重叠） | **Selenium + 注入 JS** |
| **Design2Code** | 2403.03163 | 484（+HARD 80） | **100% 自动指标** | **无** | Playwright（仅渲染） |
| **Vision2UI = WebCode2M** | 2404.06369 | 测试 3×256 / 训练 2.56M | **100%**：TreeBLEU + Visual Score + CLIP | 无 | Playwright（仅渲染） |
| **Web-Bench** | 2505.07473 | 50 项目 × 20 = 1000 | **100%**：Playwright E2E 全过才算 pass | 无 | **Playwright** |
| **WebApp1K** | 2408.00019 | 1000（+Duo 1000） | **100%**：Jest(jsdom) + RTL 单测 | 无 | 无真浏览器 |
| **FullFront** | 2505.17399 | v3：QA 1800 + 代码 700 + 设计 200 | Code Score / CLIP / DINOv2 / **交互断言** / QA 正确率 | **Gemini 2.5 Flash 十维 0~10** | Playwright（交互断言） |
| **WebGen-Bench** | 2505.03733 | 101 指令 / 647 用例 | 只有「启动失败」一项 | **WebVoyager UI agent（Qwen2.5-VL-32B）判 YES/NO/PARTIAL + GPT-4o 打 appearance 1~5** | WebVoyager |
| **Vision2Web** | 2603.26648 | 193（L1 100 / L2 66 / L3 27），1255 test case | 近乎为零（只有部署成功率，论文自标「非官方指标」） | **GLM-4.6V agent + Gemini-3-Pro judge** | WebVoyager → repo 已改 playwright-cli |
| **Interaction2Code** | 2411.03292 | v3：127 页 / 374 交互 | CLIP / SSIM / OCR-BLEU / Position / IR | **无** | **Selenium (Firefox)** |
| **WebDev Arena / Code Arena** | 无 | 实时 | **完全没有** | 无 | 沙箱仅渲染 |

**一句话判别**：真正「完全不用 VLM」的只有四家——WebRenderBench、Design2Code、WebCode2M、Web-Bench / WebApp1K。
但前三家是**静态截图比对口径（不测功能）**，后两家是**单测 / E2E 口径（不测外观）**。
**「测功能 + 不用 VLM」的交集只有 Web-Bench、WebApp1K，和 WebGrader 的 Flow Contract。**

### 3.5 四个关键 benchmark 的判据细节

**WebRenderBench（arXiv 2510.04097，笔记记对了）**——唯一把布局一致性做成纯 WebDriver 判据并直接拿去做 RL reward 的。

- **RDA（关联元素的相对布局差异）**：① 建立关联——有 innerText 的用 **LCS 相似度 > 0.80** 配对，
  无 innerText 的只看位置与尺寸差，且**尺寸差最小值 > 10 判为无有效关联**（阈值 10 来自 Apple HIG 的 padding 偏置）；
  ② **象限硬闸**——横切 left/center/right、纵切 top/middle/bottom，象限不同该对**直接 0 分**；
  ③ 相对位移 `posSim(v1,v2,ref) = max(0, 1 − |v1−v2|/ref)`，`ref` 取窗口宽/高的一半；
  ④ `score = 100·w·posSim(left)·posSim(top)`。**盒模型量只用 left / top / width / height，尺寸只进关联不进打分**。
- **GDA（分组元素计数差异）**：每个元素取 6 个参考轴（左/上/右/下边界 + 水平/垂直中线），
  同轴重合的元素构成组 `G_i`，捕捉列表/网格/表格/导航栏的对齐模式；
  打分 `score = w_j if |S_j| = |T_j| else 0`（**个数全等才给分，硬 0/1**）；
  权重 `w_i = 1/(|race group|·C)`，重复项权重低。**Group Count C 就是复杂度分档量**。
- **SDA（样式差异）**：关联对比前景色、背景色、字号、圆角四属性，跨属性平均后按 race weight 加权。
- RL reward `R = 0.6·RDA + 0.2·GDA + 0.2·SDA`（依据：GDA、SDA 与 RDA 量级差 2~3 倍），rollout N=3、KL λ=0.01、bs 128、lr 1e-6。
- 排名（0~50 档 RDA/GDA/SDA）：**GPT-4.1-mini 28.62/48.83/50.40** 是闭源第一（不是大模型）；
  Qwen-VL-Plus 19.12/49.90/49.48；Qwen2.5-VL-72B 17.22/43.55/43.46；本文的 ALISA-Qwen2.5-VL-7B（RL 后）**33.55/60.28/52.22**。
- 三条可引用读数：① **Group Count > 50 后 RDA 断崖**（28.6 → 13.4 → 4.8 → 6.0），模型只能在简单页上对齐元素；
  ② 直接用爬来的脏代码做 SFT **反而掉点**（0~50 档只有 6.08/12.37/12.36）；
  ③ 消融里只用 SDA 训最差，结论是「布局一致性优先于样式一致性」。
- 核不到：GitHub repo（只有 HF `aleversn/WebRenderBench`）；论文自身「110k pages」与「45.1k」口径不一致，按 45.1k / 测试 22.5k 引用。

**Design2Code（2403.03163，NAACL 2025）**——自动指标构成（笔记问的「CLIP 与 visual 各占什么」）：

- 文本块检测**不用 OCR**：给源 HTML 每个文本段染唯一颜色、背景透明白，多截两张图按像素颜色差定位。
- 匹配：`cost = −SequenceMatcher(r,g).ratio()` → 匈牙利算法（scipy `linear_sum_assignment`）→ **丢弃相似度 < 0.5 的对**。
- 五个指标：**Block-Match**（按块**面积**加权，漏生成与幻觉生成都扣）、**Text**（字符级 Dice）、
  **Position**（归一化中心坐标的 L∞：`1 − max(|Δx|,|Δy|)`）、**Color**（**CIEDE2000**，`max(0, 1−ΔE/100)`）、
  **CLIP**（ViT-B/32，**先用 Telea inpainting 按 bbox 把所有文本框抹掉**再比，以排除文字干扰）。
  代码里的总分是五维等权 `0.2 × Σ`；生成不出合法 HTML 时退化为 `0.2 × CLIP`。
- **与人工偏好的回归系数**：Position 0.7605 / Block-Match 0.7429 / CLIP 0.4929 / Color 0.3461，
  **Text −0.3541（p=0.021，负系数）**。去掉 Text 维后模拟胜率与人工 Pearson r = 0.975 / Kendall τ = 0.931。
- 数字：GPT-4o Direct 93.0/98.2/85.5/84.1/90.4 最佳；Design2Code-18B 78.5/96.4/74.3/67.0/85.8。
  人工侧：**49%** 认为生成页与原页可互换部署；盲比下 GPT-4V 生成页在 **64%** 的情况被认为比原页设计更好。

**Vision2UI / WebCode2M（2404.06369）**——注意 **Vision2UI 不是独立 arXiv 号**，
`2404.06369v1` 标题是 VISION2UI，`v2` 改名 WebCode2M（WWW'25）；arXiv 检索 `all:"Vision2UI"` 返回 0 条。
**Vision2Web（2603.26648，智谱）与它毫无关系。**

- **TreeBLEU（DOM 结构匹配）**：`|S(t) ∩ S(t̂)| / |S(t̂)|`，`S(·)` 是所有 **1-height 子树**集合，剔除终端节点。
  本质是结构层级的 **recall**，**不是树编辑距离**（全文无 TED）。
- **最有用的一条结论**：GPT-4o 视觉最强（Visual .85）但 **TreeBLEU 只 .15，被 1.3B 的 WebCoder（.35）碾压**。
  **视觉像 ≠ DOM 结构对** —— 这是「需要确定性结构判据」的最强外部论据。

**FullFront（2505.17399）**——三阶段不是「设计理解 / 感知 / 代码生成」，准确是**构思 → 理解 → 实现**，
第三阶段再分 4 个子任务（图→码 200 / 文→码 200 / 交互编写 100 / 代码精修 200 = 700，v3）。

- 判据里**确定性的两块**：**Code Score** = `0.25·结构 + 0.20·文本内容 + 0.10·文本样式 + 0.20·图片 + 0.25·表单`
  （权重来自 repo 源码 `self.result_weights`，**论文正文从未写**，引用须注明）；
  `结构 = LCS_θ(S_gen, S_ref)/Length(S_ref)`，**标签匹配阈值 θ=0.9**；缺失用 `Rate_c = |M_c|/|E_ref,c|` 惩罚。
- **交互成功率**是规格化可执行断言：要求模型把交互主元素 id 设为 `#InteractionPart`，然后 Playwright + headless Chromium 断言
  「hover 后 computed `textDecoration` 含 underline」、「bold 类要求 `fontWeight ≥ 600`」、
  「tooltip 命中 `.tooltip` / `[role=tooltip]` / `[data-tooltip]` / id 以 tooltip 结尾之一」、
  「modal 要求 `.modal` 或 `[aria-modal=true]`」、「checkbox 要求原生 checkbox 或 `role=checkbox` 且状态可切换」。
  数字：**o4-mini 93%**、GPT-5 92%、GPT-4o 80%、Claude-3.7 78%、Gemini-2.5-Flash 70%、LLaVA-OV-72B 16%。
- judge 可靠性（v3 新增，很好用）：自动指标 vs 人工偏好的 Spearman ρ——
  **Gemini Visual Score 0.9364 > Code Score 0.9152 > CLIP 0.8939 > DINOv2 0.8879**。
  跨 judge：Gemini-2.5-Flash ρ=0.769 / ICC=0.846；Claude-3.7 系统偏低；
  **Grok 4 偏差最大（+0.52~+2.50）、ρ 仅 0.361、重测标准差 1.097、跑间相关 0.410——不稳定，别用**。

### 3.6 三个真空白

| 空白 | 核实结果 |
|---|---|
| **多视口 / 响应式一致性当确定性判据** | **有 benchmark 覆盖这个能力，但没有一家是确定性判据**。Vision2Web 对 desktop/tablet/mobile 三套 prototype 各打分，但用的是 **VLM judge**；WebGen-Bench 的 Design Validation 子类有 13 条 Responsive Behavior，但由 **UI agent 判 YES/NO**；MV-Bench（2607.19910）明确只用 Puppeteer **固定 1920×1080 单视口**。确定性检测器在 SE 测试文献里是成熟的（ReDeCheck 的 RLG + 视口连续扫描，三类判据：溢出页面边缘 / 互相重叠 / 错误换行），**但至今没有任何 LLM 前端代码生成 benchmark 把它接进判据** |
| **性能预算当判据** | **检索零结果**。唯一相关的 arXiv 2601.05502 用 Lighthouse 跑 LLM 修改前后的 DOM 做量化分析，但那是修 bug 任务不是 codegen benchmark |
| **控制台无报错当 pass/fail** | **当判据：检索零结果。当反馈信号：有。** TeleGen（2610.04981）给生成的 app 插桩，收集 actions / network events / **errors** / state changes 压成 brief 喂给修复 agent——那是**修复反馈不是评测判据**。WebGen-Bench 的 "Start Failed" 是最接近的确定性闸，但只判「起不起来」不判控制台 |

用过的查询词（便于复核）：arXiv API 的
`all:"Lighthouse" AND all:"code generation" AND all:"LLM"`、`all:"web vitals" AND all:"LLM"`、
`all:"console error" AND all:"LLM"`（0 条）、`all:"console errors" AND all:"web" AND all:"agent"`（0 条）、
`all:"responsive design" AND all:"benchmark" AND all:"LLM"`、`all:"multi-viewport"`、
`abs:"viewport" AND abs:"benchmark" AND abs:"webpage"`（0 条）、`abs:"performance budget" AND abs:"web"`（0 条相关）、
`all:"cross-browser" AND all:"LLM" AND all:"benchmark"`（0 条）、`abs:"runtime error" AND abs:"website generation"`（0 条）。

### 3.7 顺带捞到的、对判据选型有用的新工作

| 名字 | arXiv | 为什么有用 |
|---|---|---|
| **WebGrader** | 2608.06474 | 把每个需求自动编译成可执行 **Flow Contract**，Playwright 沿同一条轨迹收集 visual / DOM / response / **持久化状态** 四类证据，只在观测到请求的状态转移后才判 Pass。WebGen-Bench 上把 8B policy 训到 **52.01%** functional success，比「appearance + 脚本」reward 高 7.88 分。**这是「测功能 + 不用 VLM」最完整的一套** |
| **WebRISE** | 2606.03220 | 需求编译成 **Interaction Contract Graph**（可观测状态 + 用户意图转移 + DOM/视觉断言），实现无关。442 任务 / 5495 转移 / 5271 检查。断言里一部分标 `[VLM]`，是混合不是纯确定性 |
| **WebGen-Agent** | 2509.22644（ICLR 2026 poster） | Step-GRPO + 截图分 + GUI-agent 测试分做 step-level reward。Claude-3.5-Sonnet 26.4% → **51.9%**；训 Qwen2.5-Coder-7B 38.9% → **45.4%**。**和 A11yn 同一个基座（Qwen2.5-Coder-7B）但 reward 正交**，是天然的一组对照 |
| **ReDeCheck / ReDeFix** | ISSTA 2017 / 2511.00678 | 响应式布局失败的确定性检测与修复，26 个生产页里在 16 个页上找到 33 处失败；前作在 5 个站上检出 91% 的注入故障 |

### 3.8 引用口径的四条硬提醒

1. **两个纯程序判据榜都已停更**：Web-Bench 的 HF Space 停在 2025-07-23（当前值 claude-4-0-opus Pass@1 28.0% / gemini-2.5-pro Pass@2 44.0%），
   WebApp1K 停在 2025-12-08（single 版已饱和：o3-mini 0.9610；Duo 版才有区分度：gpt-5 0.7938）。引用 SOTA 必须带快照日。
2. **Web-Bench 的 pass@1 是「顺序中断制」**：首次失败之前通过的任务数才算。官方例：20 任务中第 6 个首次失败 → pass@1 = 5/20 = 25%。
   **和 SWE-bench 的 pass rate 不是同一尺度，不能横比。**
3. **VLM-judge benchmark 的绝对分不可跨 judge 也不可跨时间比**。Vision2Web 作者自己声明每季度换 backbone 重跑；
   ArtifactsBench 官方榜停更在 v1.2 / 2025-08-09。
4. **Code Arena WebDev 当前榜**（HF `lmarena-ai/leaderboard-dataset` 的 webdev parquet，publish date 2026-10-13）：
   claude-opus-5.5-max **1811.15**、gpt-6-astra-max 1780.24、claude-sonnet-5.5-xhigh 1773.66、gpt-6.1-sol-max 1760.09、claude-fable-5.1-max 1742.65。
   子榜 webdev-html 榜首只有 443 票、CI ±35，与 2/3 名重叠严重，**别当稳定排名**。

---

## 4 本机实测

代码 `scripts/vc_verifier/web/`。机器无 GPU，Chrome 148 无头 + SwiftShader。

### 4.1 harness 做了什么

参考页是一个自己写的单页（landmark + 导航 + hero + 卡片网格 + 标签页 + 表单校验 + 模态框 + hash 路由 + 主题持久化），
三个文件（`index.html` / `styles.css` / `logo.svg`），从内存通过请求拦截提供，**外域一律阻断**，缺文件返回真 404。

| 阶段 | 做什么 | 耗时 |
|---|---|---|
| 三视口读数 | 375 / 768 / 1440 各一次：横向溢出、越界元素、文字截断、关键元素零尺寸、中心点命中测试、两两重叠、断点列数、语义结构自查 | 853ms（含浏览器启动） |
| 性能读数 | CDP `Performance.getMetrics` 前后差分、40 帧 rAF 采样、长任务、CLS、节点数、堆 | 1263ms |
| axe-core | 注入 4.12.1，**浅色与深色主题各跑一遍取并集** | 307ms |
| 键盘可达 | 40 次 Tab，记焦点序列与焦点指示 | 36ms |
| 交互状态机 | 7 条断言，8 次页面重载 | 2267ms |
| **合计** | | **4.9s** |

确定性注入：`Math.random` 定种（16807 线性同余，seed 42）、`Date` 固定到 2026-01-01、
`prefers-reduced-motion: reduce`、`deviceScaleFactor: 1`、`--font-render-hinting=none` / `--disable-lcd-text` / `--force-color-profile=srgb`。
`performance.now` 保持真实（性能读数要用）。

**深色主题要单独跑 axe**：参考页第一版在深色下有一条 `color-contrast`（footer 链接没写 color，吃了浏览器默认的 `#0000ee`，
在 `#12161b` 上对比度 1.93）。只跑浅色会漏掉。

### 4.2 可复现性：231 个字段里只有 4 个会变

参考页重复探测 5 次，把报告拍平成键值对逐字段比：

| 项 | 结果 |
|---|---|
| 字段总数 | 231 |
| 跨 5 次有变化的字段 | **4** |
| 变的是哪些 | `ms`（4896~5018）、`loadMs`（15~21）、`framesP95`（16.7 / 16.8）、`layoutDurTotal`（0.0017~0.0019） |
| **全部参与判定的字段** | **逐字节一致**：axe 0 违例、控制台 0、404 0、列数 [1,2,3]、7 条状态机全过、键盘不可达 0、DOM 节点 852、堆 2.77MB、LayoutCount 差分 2、RecalcStyleCount 差分 4 |

四个会变的全是墙钟量，且其中两个（`framesP95`、`layoutDurTotal`）参与判定但抖动远小于阈值余量
（p95 阈值 34ms vs 实测 16.7~16.8ms）。**准入条件 1 通过：参考页 5/5 全过。**

### 4.3 阈值（跑变异之前冻结）

`thresholds.json`，`_frozen: 2026-10-15`。**只在参考页 5 次重复上校准（看方差定余量），在任何变异体上一次都没调。**

| 层 | 阈值 | 参考页实测 |
|---|---|---|
| W0 | 控制台 error / pageerror / 未捕获 Promise / ≥400 状态 / 请求失败 / 不安全子资源 **全部 = 0** | 全 0 |
| W1 | 横向溢出 ≤ 1px、越界 = 0、截断 = 0、缺失 = 0、零尺寸 = 0、遮挡 = 0、两两重叠比 ≤ 0.05、375 单列、1440 ≥ 2 列 | 0 / 0 / 0 / 0 / 0 / 0 / 0 / 1 列 / 3 列 |
| W2 | axe critical+serious = 0、带 wcag tag = 0、总违例 = 0；lang 非空、h1 = 1、跳级 = 0、main ≥ 1、nav ≥ 1、无 alt 图 = 0、无名按钮 = 0、无标签输入 = 0、悬空 ARIA = 0、假按钮 = 0、键盘不可达 = 0、无焦点指示 = 0 | 全部达标（axe 45 条 passes） |
| W3 | 7 条状态机断言全过 | 7/7 |
| W4 | 资源 ≤ 20、字节 ≤ 300KB、最长任务 ≤ 100ms、帧 p95 ≤ 34ms、CLS ≤ 0.1、节点 ≤ 1500、堆 ≤ 12MB、Layout 差分 ≤ 20、Recalc 差分 ≤ 40 | 13 / 43.6KB / 无长任务 / 16.7ms / 0 / 852 / 2.77MB / 2 / 4 |

### 4.4 变异集：16 个开发 + 6 个留出，标签先写死

| 变异 | 标签 | 集合 | 判定 | 挂在 | 设计时的预期 | 1440 首屏像素相似度 |
|---|---|---|---|---|---|---|
| F1 对比度降级 | 该挂 | 开发 | 挂 | W2 | W2 | 0.9883 |
| F2 删 img alt | 该挂 | 开发 | 挂 | W2 | W2 | **1.0** |
| F3 button 换 div | 该挂 | 开发 | 挂 | W2 | W2 | **1.0** |
| F4 卡片写死 420px | 该挂 | 开发 | 挂 | W1 | W1 | **1.0** |
| F5 负边距 + z-index 把按钮压住 | 该挂 | 开发 | 挂 | W1+W3 | W1 | 0.8028 |
| F6 摘掉表单校验 | 该挂 | 开发 | 挂 | W3 | W3 | **1.0** |
| F7 图片路径写错 404 | 该挂 | 开发 | 挂 | W0 | W0 | 0.9996 |
| F8 启动同步忙等 300ms | 该挂 | 开发 | 挂 | W4 | W4 | **1.0** |
| P1 flex → grid auto-fit | 不该挂 | 开发 | 过 | — | — | 1.0 |
| P2 类名全换哈希名 | 不该挂 | 开发 | 过 | — | — | 1.0 |
| P3 换配色（对比度仍达标） | 不该挂 | 开发 | 过 | — | — | **0.9002** |
| P4 px → rem | 不该挂 | 开发 | 过 | — | — | 1.0 |
| P5 拆成原子类 | 不该挂 | 开发 | 过 | — | — | 1.0 |
| P6 外链 logo → 内联 svg | 不该挂 | 开发 | 过 | — | — | 0.9999 |
| P7 section → div[role=region] | 不该挂 | 开发 | 过 | — | — | 1.0 |
| P8 换字体栈 | 不该挂 | 开发 | 过 | — | — | 1.0 |
| H1 脚本尾部未定义变量 | 该挂 | **留出** | 挂 | W0 | W0 | **1.0** |
| H2 标题跳级 + main 换 div | 该挂 | **留出** | 挂 | W2 | W2 | 0.9849 |
| H3 主题不落存储 | 该挂 | **留出** | 挂 | W3 | W3 | **1.0** |
| H4 逐个绑定 → 事件委托 | 不该挂 | **留出** | 过 | — | — | 1.0 |
| H5 HTML 压缩 | 不该挂 | **留出** | 过 | — | — | 1.0 |
| H6 CSS 简写 + 逻辑属性 | 不该挂 | **留出** | 过 | — | — | 1.0 |

**22/22，11 条该挂的全部挂在设计时预期的那一层**（F5 多挂了一层 W3，是真的——按钮被压住后点不动，模态框和主题切换一起失效）。

### 4.5 判别力表（与 3D 侧同格式）

| 信号 | 开发 16 | 留出 6 | 合计 | 检出 | 误杀 |
|---|---|---|---|---|---|
| 朴素①单张截图逐像素（1440 首屏，**阈值取最优** t=0.9999） | 10/16 | 4/6 | 14/22 | 4/11 | **1/11** |
| 朴素②DOM 标签序列一致 | 7/16 | 4/6 | 11/22 | 2/11 | **2/11** |
| 朴素③类名序列一致 | 5/16 | 3/6 | 8/22 | 0/11 | **3/11** |
| 朴素④可见文本一致 | 8/16 | 3/6 | 11/22 | 0/11 | 0/11 |
| W0 正确性（控制台 / 网络 / 未捕获） | 9/16 | 4/6 | 13/22 | 2/11 | 0/11 |
| W1 布局与响应式（三视口） | 10/16 | 3/6 | 13/22 | 2/11 | 0/11 |
| └ W1 只看 1440 单视口 | 9/16 | 3/6 | 12/22 | 1/11 | 0/11 |
| └ W1 只看 375 单视口 | 10/16 | 3/6 | 13/22 | 2/11 | 0/11 |
| W2 可访问性（axe + 语义 + 键盘） | 11/16 | 4/6 | 15/22 | 4/11 | 0/11 |
| └ W2 只跑 axe 默认规则 | 10/16 | 4/6 | 14/22 | 3/11 | 0/11 |
| └ W2 只看语义 / 键盘自查项 | 10/16 | 4/6 | 14/22 | 3/11 | 0/11 |
| W3 交互与状态机 | 10/16 | 4/6 | 14/22 | 3/11 | 0/11 |
| W4 性能预算 | 9/16 | 3/6 | 12/22 | 1/11 | 0/11 |
| **五层组合 W0+W1+W2+W3+W4** | **16/16** | **6/6** | **22/22** | **11/11** | **0/11** |

每层在整个集合上的**唯一贡献**（只有它抓到）：

| 层 | 唯一抓到 | 是哪几条 |
|---|---|---|
| W2 | 4 | F1 对比度、F2 alt、F3 button→div、H2 标题与 landmark |
| W0 | 2 | F7 404、H1 运行时异常 |
| W3 | 2 | F6 表单校验、H3 存储不持久 |
| W1 | 1 | F4 窄视口溢出 |
| W4 | 1 | F8 长任务 |

五层各有不可替代的贡献，没有一层是摆设。另外 F5 被 W1 和 W3 同时抓到。

### 4.6 像素信号为什么不行：噪声地板是零，但信号不在图里

| 项 | 数字 |
|---|---|
| 参考页自比自（同一页跑两次截图） | **平均绝对差 0.000，相同像素占比 1.0000** |
| 11 个该挂的变异里，1440 首屏像素与参考**完全一致**的 | **7 个**（F2 / F3 / F4 / F6 / F8 / H1 / H3） |
| 不该挂的变异里像素差最大的 | **P3 换配色 0.9002** |
| 单张截图的最优阈值表现 | 14/22，检出 4/11，误杀 1/11 |

这组数把问题说得很干净：**像素信号在这台机器上是完全确定的（噪声地板为零），它依然只能抓到四成**。
而且阈值无处可放——要抓 F1（0.9883）就必须把阈值设在 0.9883 以上，
但那样会同时误杀 P3（0.9002）和 P6（0.9999）。换配色这个合法重写的像素差，比大多数真缺陷都大。

对照 3D 侧：3D 侧是「逐像素 12/29，VLM 单模型 30~35/36」——那里 VLM 比像素强得多。
Web 侧的情况不同：**这 7 个该挂的变异在视觉上和参考完全一样，VLM 看图同样看不出来**
（删 alt、button 换 div、摘掉表单校验、长任务、未捕获异常、存储不持久，图上都没有任何痕迹）。
**Web 侧 VLM 的替代空间比 3D 侧更小，不是因为 VLM 弱，是因为这些错误压根不是视觉错误。**

朴素结构信号更糟：类名序列一致这个判据检出 0/11、误杀 3/11，比随机还差——
它只能抓到「换了类名」这件事本身，而换类名正是最常见的等价重写。

### 4.7 多视口的边际贡献

W1 只看 1440：12/22（检出 1/11）。加上 375 和 768：13/22（检出 2/11）。
差的那一条是 F4（卡片写死 420px）：它在 1440 下**一切正常**，列数 3、无溢出、无越界；
到 375 才暴露（横向溢出 65px、10 个元素越界）。

这和 §3.6 的检索结果对上了：公开 benchmark 里没有一家把多视口做成确定性判据，
而本机实测里它贡献了 11 个真缺陷中的 1 个、且是其它四层都抓不到的那一个。

### 4.8 两遍重跑：判定翻面 0

全量 22 个变异跑两遍，逐行比：**判定翻面 0 条，层级列表与明细字典逐字节一致。**

对照 3D 侧的 VLM judge：最差一档两次一致只有 13/18，约 28% 的 case 重判会翻面。
**确定性信号不需要多次投票，这直接省掉乘在成本上的那个系数。**

### 4.9 作弊测试：7 个作弊页，第一版挡 5 个

| 作弊页 | 手法 | 第一版 | 修后 | 挂在 |
|---|---|---|---|---|
| K1 | 整块主内容加 `aria-hidden="true"` 让审计引擎无话可说 | 挡住 | 挡住 | W2（`aria-hidden-focus` + 对比度照样报） |
| K2 | `setInterval` 轮询检测 `window.axe`，一出现就把违规样式改回合格 | 挡住 | 挡住 | W2（轮询 20ms 也来不及，注入与 run 在同一个同步窗口） |
| K3 | 视口外藏一份合格副本，真正显示的那份对比度不足 | 挡住 | 挡住 | W2（axe 查全文档） |
| K4 | **把不合格文字 `font-size:0`，用 `::after` 把同样的字画回屏幕** | **漏** | **仍漏** | — |
| K5 | 标签页只改 `aria-selected` 不切面板（ARIA 状态对，用户看到的内容没变） | 挡住 | 挡住 | W3（断言同时查面板可见性） |
| K6 | **加载时无条件把主题写成 dark，按钮其实什么都不做** | **漏** | 挡住 | W3 |
| K7 | 卡片写死 420px，再给 body 加 `overflow-x:hidden` 把滚动条藏掉 | 挡住 | 挡住 | W1（越界元素判据不依赖滚动条） |

**两个修法（都是补判据，不是调阈值）**：

1. **K6**：状态机断言缺了前置态。修法是每条断言带三段——**清空存储后的初始态 + 操作后的终态 + 能往返**。
   主题断言现在查：清空后必须是 light 且存储为 null → 点击后 attr 与存储都是 dark → 刷新后仍 dark → 再点一次回到 light。
   硬编码写 dark 的页面在第一条和第四条上同时挂掉。
2. **K4**：axe 只报 `violations` 不够。修法是**把 `incomplete`（needs review）里对比度一族也当闸**
   （阈值文件里新增 `axe_incomplete_gate_rules: [color-contrast, color-contrast-enhanced, link-in-text-block]`）。

**补完判据后 22 个变异全量回归：仍然 22/22，零新增误杀。**

**但 K4 仍然漏，而且这是确定性信号的真盲区。** 实测 K4 的 axe 输出是
`violations: []`、`incomplete: []`、`passes: 45` ——**连 needs review 都不报**。
原因是伪元素承载的文字 axe 的 `color-contrast` 根本不检查（对应 axe issue **#2680** "Pseudo elements without position:absolute not picked up by color contrast"，至今 open）。
`font-size:0` 的真元素被当成无文本内容跳过，伪元素又不进检查范围，两头都落空。
**这一类只能靠两条路**：① 代码闸（禁止用 `::before/::after` 的 `content` 承载正文，这是静态可查的）；
② 截图 OCR 或 VLM（看屏幕上实际显示了什么）。纯 DOM 侧确定性信号在这里到顶了。

### 4.10 我自己犯的两个错（都在第一遍跑完之后才发现）

第一遍跑 22 个变异的结果是 **21/22**，唯一误判是 P2（类名全换哈希名），挂在 W1+W2。
拆下来是两个独立问题，性质完全不同：

| 问题 | 性质 | 证据 | 修法 |
|---|---|---|---|
| W1 `breakpoint_375_cols` / `breakpoint_1440_cols` 挂了 | **verifier 的真 bug**：列数测量用了 `.card` 类选择器，类名一换就变成 0 列 | 这正是 §2.1 第 4 条原则说的事 | 改成结构化定位：主内容里第一个有 ≥2 个子项的列表，取其子项矩形 |
| W2 `aria-required-parent` / `aria-roles` 挂了 | **axe 判对了，是我的变异脚本标错了**：重命名用的是全文正则，把 `role="tablist"` 一起改成了 `role="x7a7"` —— 那不是等价重写，是真的破坏 ARIA | — | 重命名只改 HTML 的 `class="..."` token 和 CSS 的 `.name` 选择器 |

两处修完后第二遍是 22/22。**这里要如实声明：22/22 是第二遍的结果，第一遍是 21/22。**
阈值一个没动，改的是一条测量实现和一条变异生成实现。

第二个错和 3D 侧的「ok_lathe 翻案」是同一类事：**人工标签不是金标准，判据判错之前先怀疑标签**。
3D 侧是 4 个 VLM 都看出雪人头顶有洞而标注者没看出；这里是 axe 看出 ARIA 被破坏而我以为自己做的是等价重写。

### 4.11 成本

| 项 | 实测 |
|---|---|
| 单次完整探针 | **4.9s**（三视口 0.85s 含启动 / 性能 1.26s / axe 双主题 0.31s / 键盘 0.04s / 7 条状态机含 8 次重载 2.27s） |
| 22 个变异全量 | **114~117s**，平均 **5.2s/个** |
| 作弊集 7 个 | 36s |
| 浏览器启动 | 181ms |
| 新开页 + 加载 | 61ms |
| 注入 axe（572KB） | 72ms |
| `axe.run` | 首次 71ms，之后 30~34ms |
| 复用浏览器开 5 个页 | 248ms（约 50ms/页） |

**4.9 秒里的工具开销不到 0.5 秒**，剩下全是我写的固定 settle 等待和 40 帧 rAF 采样。
要吞吐可以压到 1 秒以内（去掉帧采样、settle 改成事件驱动、状态机复用同一个页面上下文）。
按 1 秒/次估，1024 并发 rollout 的 Web verifier 池只需要个位数核心——
对照 3D 侧推算的「多轮 three.js 43 核 / 多轮 Blender 365 核」，**Web 侧的 verifier 成本可以忽略**。

---

## 5 结论：哪些今天就能做成零噪声的 RL 信号

### 5.1 三档分级

**第一档：今天就能做成零噪声信号，直接进 reward**

| 能力 | 为什么能 | 本机证据 | 外部证据 |
|---|---|---|---|
| **正确性（W0）** | 事件流读数，一次读取、与时间无关 | 5 次重复逐字节一致；唯一抓到 2 个真缺陷 | 公开 benchmark 里**零家**用它当判据（空位） |
| **可访问性的结构性部分（W2 的语义 + 键盘 + 替代文本 + ARIA 引用）** | 全是 DOM 查询，没有不确定性 | 唯一抓到 4 个真缺陷，是贡献最大的一层 | **A11yn 已经证明 RL 能训出来**（IR_Axe 0.05 vs GPT-5.1 0.13，但那是直接优化的量；独立证据是换引擎的 IR_AChecker 0.26 vs 0.35 与人工 pairwise 39.3/21.4）；microsoft/a11y-llm-eval 的「axe 零失败 AND 手写断言全过」是现成的双闸范式。**做自己的版本要把 best-practice 与 WCAG 分开记账，并换一个引擎（IBM Equal Access）做独立验证** |
| **交互与状态（W3）** | 断言读的是 DOM 与存储的同步快照 | 唯一抓到 2 个真缺陷；挡住 2 个作弊页 | Web-Bench / WebApp1K 已证明纯 E2E / 单测可排序；WebGrader 的 Flow Contract 把 8B 训到 52.01% |
| **布局与响应式（W1）** | 盒模型读数在固定视口下完全确定 | 5 次重复一致；375 视口贡献 1 个其它层抓不到的缺陷 | **确定性检测器成熟（ReDeCheck）但零 benchmark 接入**，是最干净的空位 |

**第二档：能做确定性信号，但阈值要小心，当辅助项或代码闸**

| 能力 | 为什么要小心 |
|---|---|
| **性能预算（W4）** | 资源数、字节、DOM 节点、堆、Layout/Recalc 差分在本机 5 次重复里逐字节一致，**可以当硬闸**；但长任务与帧 p95 依赖机器负载，阈值必须留大余量。而且 `budget.json` 已被 Lighthouse 移除，「170KB」那类常引数字出处不可靠。**帧 p95 没有官方口径，要标成自定义指标** |
| **对比度** | axe 的 `color-contrast` 对渐变 / 图片背景 / 半透明 / 伪元素**官方就判 needs review 而非 violation**。只看 violations 会被绕过（本机 K4 实证）；全量 incomplete 当闸会误杀合法设计。折中是只对对比度族开 incomplete 闸，并**另加一条代码闸禁止伪元素承载正文**。连续化（`min(1, ratio/4.5)`）是明确的改进方向，arXiv 2512.05067 证明对比度是可做连续优化目标的，但**当 RL reward 的工作核不到** |
| **点击目标尺寸** | 阈值是 24×24 CSS px（WCAG 2.2 SC 2.5.8），但 axe 的 `target-size` **默认关闭**，要显式打开 |
| **HTML 合法性 / 安全响应头** | 要自建并 pin 版本（W3C Nu Checker 官方自己警告行为会变 + 有限速）。OWASP 的 13+90 条 header 清单是机器可读的，但本地沙箱页用不上 |

**第三档：必须靠 VLM 或人**

| 能力 | 为什么 | 证据 |
|---|---|---|
| **审美与视觉层级** | 没有确定性定义 | 3D 侧已有：审美单人 α=0.368、3 人 ICC=0.637 |
| **替代文本的语义正确性** | `alt="image"` 语法通过语义无效，规则引擎抓不到 | Calò et al. CHI EA'26 的批评；2607.20690 原文「规则工具主要只能捕捉机械可查的问题」 |
| **屏幕上实际显示了什么** | 伪元素 / canvas / 图片里的文字，DOM 侧完全不可见 | **本机 K4 实证**：axe 连 incomplete 都不报（issue #2680 open） |
| **需求是否被满足** | 「这个页面看起来像不像一个数据分析产品的首页」不是确定性问题 | Design2Code 的人工侧：49% 认为可互换部署 |
| **布局意图** | 「这个间距是设计还是失误」 | WebRenderBench 用象限 + 相对位移近似，但那是**相似度不是正确性**，要有参考解 |

### 5.2 优先级清单

按「判别力增量 ÷ 实现成本」排：

1. **W0 正确性门（半天）**。十几行事件监听，零误杀，而且公开 benchmark 里**一家都没做**。
   先把 `ERR_ABORTED` 白名单和 Playwright/Puppeteer 的 console 字面量差异处理对。
2. **W2 的语义 + 键盘自查（一天）**。不依赖任何第三方引擎，判别力在本机是最高的一层（唯一抓到 4 个）。
   **先把题面的交互元素清单做成 spec 的一部分**，否则立刻掉进「判据比问题描述知道得多」的坑。
3. **W3 状态机断言（两三天，按任务族写）**。判别力高且**完全不可被视觉信号替代**。
   硬性要求：每条断言带「前置态 + 终态 + 往返」三段，否则会被硬编码骗过（K6 实证）。
   现成的路径枚举用 `xstate/graph`，别用已 deprecated 的 `@xstate/test`。
4. **W1 三视口（一天）**。最大的公开空位。
   **判据绝不能绑表现型类名**（P2 实证），要么结构化定位，要么用 `layout-lint` 的声明式约束。
5. **axe-core 接入（半天）**，但要做三件事：用 4.14.0 而不是老版本（cdnjs 落后在 4.12.1，要最新走 jsDelivr/unpkg）；
   **把 best-practice 规则和 WCAG 规则分开记账**，别混进同一个「WCAG 合规度」；
   **对比度族把 incomplete 也当闸**。
6. **W4 性能预算（一天）**，只把确定性强的几项（资源数、字节、DOM 节点、堆、Layout/Recalc 差分）当硬闸，
   长任务与帧间隔当告警不当闸。
7. **自动造题 + 准入测试（照搬 3D 侧的 `gen_tasks.py`）**。
   Web 侧的准入第二条尤其重要：让 LLM 提破坏，**挡不住的破坏直接剔除**，
   被剔除的那些就是判据盲区的体检报告（3D 侧的 L3 就是这么逼出来的）。
8. **作弊集常态化**。本机 7 个页抓出 2 个真漏洞，成本 36 秒。
   建议每次改判据都跑一遍，并把「漏掉的作弊手法」单独存档——它们定义了确定性信号的边界。

### 5.3 两条必须写进规范的约束

1. **判据的信息量 ≤ 问题描述的信息量。** Web 侧比 3D 侧更容易违反，因为 DOM 里什么都查得到。
   具体做法是把「要查哪些元素、哪些状态要往返、哪些视口」写进题面的 spec，判据只能读 spec 里有的东西。
2. **判据不许绑实现手法。** 类名、标签名、CSS 写法、事件绑定方式、单位、字体栈、是否压缩——
   这七样全都可以在视觉与功能完全等价的前提下任意更换。
   本机 10 类等价重写里有 6 类会打垮朴素结构判据（类名序列判据误杀 3/11，DOM 标签序列误杀 2/11）。

---

## 附 口径与打折声明

1. **22/22 是第二遍的结果**，第一遍 21/22。阈值一个没动，改的是两条实现（列数测量去掉类名依赖、变异生成只改 class token）。详见 §4.10。
2. **作弊集补判据发生在作弊测试之后**（§4.9 的两条）。补完做了 22 个变异的全量回归，仍 22/22、零新增误杀；但「补完之后 6/7」这个数要和「第一版 5/7」一起看。
3. **阈值只在参考页上校准**，变异集上一次没调。参考页 5 次重复的方差见 §4.2。这比 3D 侧干净（3D 侧的 `blk_min` 和颜色容差在变异集上看过）。
4. **单任务单参考页。** 3D 侧有三个场景、47 个变异、其中 18 个真留出。本文只有一个参考页、22 个变异、其中 6 个留出。**判别力数字要按单任务打折，换页面必须复验。**
5. 本机用的 axe 是 **4.12.1**（cdnjs 当前最新），npm 最新是 **4.14.0**。规则数、needs review 占比、impact 分布等引自 4.14.0 文档。
6. **帧 p95、层级重排计数、两两重叠比、假按钮、焦点可见**这五项是自定义指标，没有官方口径或权威阈值，引用时要标。
7. 像素比较用的是 1440 首屏 `clip` 截图的平均绝对差与「相同像素占比（阈值 6）」，**不是 SSIM 也不是感知指标**。它在本机噪声地板为 0，不代表换机器仍为 0。
8. **A11yn 的 COLM 2026 收录核不到**（只有 repo README 自述）；**WebAccessBench 不在 arXiv**；**A11YBench 无独立 arXiv 号**；
   **WebCoderBench 的 a11y 原始百分数核不到**（只给 z-score）；**microsoft/a11y-llm-eval 的 SOTA 核不到**；
   **Interaction2Code 的 UR / win rate 具体数值核不到**（只在图里）；**FullFront 的 Code Score 权重来自 repo 源码，论文正文未写**；
   **WebRenderBench 的 GitHub repo 核不到**（只有 HF）。
9. **笔记需要更正的三处**：① A11YBench 的 arXiv 号 2606.21926 实际是 A11YRepair；
   ② WebCoderBench 的「a11y 子分 9.9%」是人类偏好**权重**，不是得分，而 9.9% 这个数真身是 A11yn 附录 K 的 Best-of-N 平台值；
   ③「axe 自动覆盖 57% 的 WCAG」要改成「在 Deque 的 13000 页 / 约 30 万问题样本上，57% 的**问题实例**被自动化完整覆盖」。
10. **Vision2UI 不是独立 arXiv 号**（是 2404.06369 的 v1 标题，v2 改名 WebCode2M），**与 Vision2Web（2603.26648）无关**。
11. `budget.json` 在 Lighthouse 12.0.0 已移除，`tap-targets` 的 48px 口径已被 `target-size` 的 24px 取代，**这两条是旧资料的高频错误**。

