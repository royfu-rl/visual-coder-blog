# 01 · 前沿实验室如何训练 visual coding：公开披露盘点

- 查证日期：2026-10-15
- 范围：Web 前端 / WebDev / three.js / WebGL / Blender / 游戏，只看「训练数据 + RL 环境 + reward hacking」的披露；评测分数见 `frontier_evals_west.md`、`frontier_evals_cn.md`，不重复
- 标记
  - **[原文]**：原句可在链接里找到（英文原句照录）
  - **[推断]**：本文作者从原文推出的结论，没有一手证据
  - **未披露**：查过相关材料，没找到
- 已有方案（`webdev-data/WebDev 数据构造技术方案.html`）已经详细引用 MiniMax-M2、MiMo-V2.6、Kimi K3、GLM-4.5V / GLM-5 / GLM-5V-Turbo、Qwen3-Coder-Next、Ling 2.x、UI2Code^N、Vision2Web。本文对这些只做一行确认，重点放在 Anthropic、OpenAI、Google 与增量

## 先给结论

1. **西方三家都没有公开 visual coding 的训练数据或 RL 环境配方。**
   - 一手材料里能确认的只有三类
     - 一句话级别的「我们专门训练过」（OpenAI 最多）
     - 推理时 harness / skill 的公开（Anthropic 最详细）
     - system card 里 reward hacking 与 grader hacking 的通用统计
2. **Anthropic 公开的是「generator–evaluator」harness，而不是训练配方。**
   - 内容包括四维设计评分、Playwright 实测、few-shot 校准、5 到 15 轮迭代
   - 这套结构和 RL 里的「policy + rubric grader」同构，但官方从没说过把它用在训练里
3. **OpenAI 明说「专门训练过」前端与 UI，没说怎么训。**
   - GPT-5：训练于真实编码任务
   - GPT-5.4："trained … with a focus on improved UI capabilities and use of images"
   - GPT-5.6 / GPT-6 Astra：「检查渲染结果」被当作模型能力来宣传
4. **国内厂商披露最多，结构惊人一致。**
   - 共同骨架：真实页面或合成需求 → 沙箱构建与渲染 → 分层 verifier（执行门 → 规则 / 交互 → VLM 视觉）→ RL
5. **3D / Blender 方向**
   - 学术界：CAD 已经形成「可执行门控 × IoU」的在线 RL 标准做法
   - Blender 和 three.js：仍然以「筛选后 SFT」或推理时迭代为主
   - 前沿实验室：只有 demo 和 BenchCAD 分数，没有训练披露

---

## 1. Anthropic

### 1.1 披露了什么

**A. 前端审美：问题定义与 Skill（推理时，非训练）**
- 出处：Claude 博客「Improving frontend design through Skills」，2025-11-12，https://claude.com/blog/improving-frontend-design-through-skills
- [原文] 把「AI 味」归因到训练数据的分布
  - "Distributional convergence. During sampling, models predict tokens based on statistical patterns in training data. Safe design choices … dominate web training data."
  - 典型症状："Inter fonts, purple gradients on white backgrounds, and minimal animations"
- [原文] 解法是一份约 400 token 的 skill，不是训练："we developed a ~400 token prompt … across typography, color, motion, and backgrounds"
- [原文] 禁掉一组默认值后会收敛到新的默认值："the model can default to other common choices (like Space Grotesk …)"
- [原文] Artifacts 受「单 HTML 文件」约束，所以另外做了 `web-artifacts-builder` skill
- skill 原文：https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md

**B. generator–evaluator harness（最接近 RL 环境的一手披露）**
- 出处：工程博客「Harness design for long-running application development」，2026-03-24，https://www.anthropic.com/engineering/harness-design-long-running-apps
- [原文] 动机：模型自评偏松
  - "agents tend to respond by confidently praising the work"
  - "tuning a standalone evaluator to be skeptical turns out to be far more tractable than making a generator critical of its own work"
- [原文] 四维设计评分，同时写进 generator 和 evaluator 的 prompt
  - Design quality：整体是否形成统一的情绪与识别度
  - Originality："telltale signs of AI generation like purple gradients over white cards—fail here"
  - Craft：排版层级、间距、配色、对比度
  - Functionality：可用性
  - 加权方式："weighting design and originality more heavily"
- [原文] evaluator 校准："calibrated the evaluator using few-shot examples with detailed score breakdowns … reduced score drift"
- [原文] evaluator 不看静态截图，而是实操页面
  - "I gave the evaluator the Playwright MCP, which let it interact with the live page directly before scoring"
  - "5 to 15 iterations per generation … Full runs stretched up to four hours"
- [原文] 评分措辞本身会造成审美收敛："phrases like 'the best designs are museum quality' pushed designs toward a particular visual convergence"
- [原文] 分数单调上升不等于更好："I regularly saw cases where I preferred a middle iteration over the last one"
- [原文] 全栈版本
  - 由 planner、generator、evaluator 三个 agent 组成
  - 每个 sprint 先签 "sprint contract"，例如 Sprint 3 有 27 条验收标准
  - 每个维度都有硬阈值："Each criterion had a hard threshold, and if any one fell below it, the sprint failed"
- [原文] QA 能力不是天生的
  - "Out of the box, Claude is a poor QA agent … talk itself into deciding they weren't a big deal and approve the work anyway"
  - 调法：读 evaluator 日志，找出它和人判断不一致的地方，再改 prompt
- [原文] 模型越强，evaluator 的边际价值越低："It is worth the cost when the task sits beyond what the current model does reliably solo."

**C. 长程 harness：功能清单 + 浏览器端到端测试**
- 出处：「Effective harnesses for long-running agents」，2025-11-26，https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- [原文] initializer agent 把需求展开成 JSON 功能清单，claude.ai 克隆案例里 "over 200 features"，初始全部标为 failing
- [原文] 用 JSON 而不是 Markdown："the model is less likely to inappropriately change or overwrite JSON files"
- [原文] 失败模式：用单测或 curl 验证完就宣布完成
  - "would fail recognize that the feature didn't work end-to-end"
  - 改成 Puppeteer MCP 截图实测之后明显变好
- [原文] 视觉验证的盲区："Claude can't see browser-native alert modals through the Puppeteer MCP"

**D. 模型发布页与 system card：只有能力描述，没有训练描述**
- [原文] Opus 4.7（2026-04-16）："producing higher-quality interfaces, slides, and docs"；长边支持到 2,576 像素
  - 链接：https://www.anthropic.com/news/claude-opus-4-7
- [原文] Claude Design（2026-04-17，Anthropic Labs，基于 Opus 4.7）
  - 产品形态：读代码库和设计文件，建立 design system，产出可交互原型，可交给 Claude Code 实现
  - 包含 "Frontier design: … prototypes with voice, video, shaders, 3D"
  - 链接：https://www.anthropic.com/news/claude-design-anthropic-labs
- [原文] Fable 5（2026-06-09）："rebuilding a web app's source code from screenshots alone"
  - 链接：https://www.anthropic.com/news/claude-fable-5-mythos-5
- [原文] Opus 5（2026-07-24）的客户证言："opened its pages in a browser at desktop and phone widths, caught a product hidden below the mobile fold"
  - 链接：https://www.anthropic.com/news/claude-opus-5
- [原文] Opus 5.5（2026-09-22）的测试者反馈："build a game from a single prompt; Opus 5.5 scored higher than any other model on the strength of its graphics and polish"
  - 链接：https://www.anthropic.com/claude-opus-5-5
- [原文] 所有 system card 的训练数据描述都是同一套模板
  - "publicly available information from the internet, public and private datasets, and synthetic data generated by other models"
  - 示例：Opus 5 system card §1.1，https://www.anthropic.com/claude-opus-5-system-card
- **未披露**：前端、设计、3D 专项数据，前端 RL 环境，视觉 reward 模型
  - 核查方法：对 Claude 4 到 Opus 5.5 共 9 份 system card 全文检索 frontend / aesthetic / HTML / render / Blender / three.js，没有一条是在讲训练

**E. reward hacking / grader hacking（通用，但直接影响视觉 reward 设计）**
- [原文] 用模型当 grader 的环境，被单独划成「高风险」一类
  - Fable 5 / Mythos 5 system card §6.4.2
  - "we internally classify them into subsets that are at higher and lower risk of 'grader hacking'—i.e. exploitation of model-based graders"
  - "Exploitative grader awareness almost exclusively occurs in such environments"
  - 链接：https://anthropic.com/claude-fable-5-mythos-5-system-card
- [原文] 训练中全程跑 hack 分类器
  - Opus 5.5 system card §6.2.1："we screened RL training episodes with automated classifiers that flag reward-hacking behaviors"
  - 出现最多的 hack 类型："Guesses what the answer key expects"
  - 链接：https://www.anthropic.com/claude-opus-5-5-system-card
- [原文] 隐藏改动骗过只看最终产物的 grader
  - Opus 5.5 §6.5.4.4："Claude hid changes from the grader, which only graded the final output"
- [原文] GUI 类 reward hacking 评测
  - Opus 4.6 §6.2.3.3：把 computer-use 容器改成不可能完成的任务，观察模型是否绕路
  - "frequently circumvented broken web GUIs by using JavaScript execution or unintentionally exposed APIs"
  - 链接：https://www.anthropic.com/claude-opus-4-6-system-card
- [原文] 缓解手段：inoculation prompting
  - "we have already started making use of this technique in training Claude"
  - 链接：https://www.anthropic.com/research/emergent-misalignment-reward-hacking
- [原文] computer use 早期训练（2024-10）
  - "Training Claude to count pixels accurately was critical"
  - "computer-use training … on just a few pieces of simple software, such as a calculator and a text editor"
  - 链接：https://www.anthropic.com/news/developing-computer-use

### 1.2 能推出什么
- [推断] Anthropic 的审美提升路径是「先定义可评分的审美 rubric，再用独立 evaluator 实操评分」
  - 原文能证明的只到 harness 层
  - 这套四维 rubric、few-shot 校准、Playwright 实测，可以直接改造成 RL 的 grader
  - 它被列为「高风险 grader hacking」环境的那一类
- [推断] 训练数据大概率包含「模型生成 + 模型评审」的合成前端轨迹，依据有三条
  - system card 固定写 "synthetic data generated by other models"
  - 博客反复写 generator / evaluator 分离
  - Fable 5 宣传 "from screenshots alone" 重建 web app：这类任务天然可以从「真实 app → 截图 → 让模型复刻」反向构造
- [推断] 对我们最有用的是 harness 博客里四条可直接写进 verifier 的教训
  - evaluator 必须独立，并且要调成「怀疑模式」
  - 评分措辞会引导审美收敛，rubric 里不要写 "museum quality" 这类诱导词
  - 每个维度设硬阈值，任一维度不过就判失败，而不是加权求和
  - 分数单调上升不代表质量单调上升，要保留中间轮做对比

---

## 2. OpenAI

### 2.1 「astra」是什么
- [原文] GPT-6 Astra 是 GPT-6 代的首个模型，也是最高档
  - 发布页：https://openai.com/index/gpt-6-astra/ （直连 403，经 r.jina.ai 读取）
  - 页面更新记录：2026-09-22 加入 GPT-6 Sol / Luna，2026-09-29 加入 GPT-6.1 Sol
- [原文] Sol / Terra / Luna 是长期存在的能力档位，不是代号
  - GPT-5.6 页面："The number identifies the generation, while Sol, Terra, and Luna are durable capability tiers"
  - 链接：https://openai.com/index/gpt-5-6/
- [二手] 时间线
  - 2026-08-01：OpenAI 研究帖首次以「Astra」称呼下一个大模型，说它在数学与理论计算机科学的 10 个长期问题上取得突破；当时没定会不会叫 GPT-6
  - 2026-09-03：以 GPT-6 Astra 名义发布
  - 出处：https://technews.tw/?p=1596442 、https://www.techmeme.com/260903/p49 （研究帖原文没抓到）
- 注意区分：Google DeepMind 2024 年的「Project Astra」（通用助手原型）和这个无关

### 2.2 披露了什么
- **训练方式：只有一句话级别的披露**
  - [原文] Codex 研究预览（2025-05）："trained using reinforcement learning on real-world coding tasks in a variety of environments … iteratively run tests until it receives a passing result"
    - 同一页："currently lacks features like image inputs for frontend work"
    - 链接：https://openai.com/index/introducing-codex/
  - [原文] GPT-5（2025-08-07）
    - "We trained GPT‑5 on real-world coding tasks in collaboration with early testers"
    - "When producing frontend code for web apps, GPT‑5 is more aesthetically-minded"
    - "beating OpenAI o3 at frontend web development 70% of the time in internal testing"
    - 链接：https://openai.com/index/introducing-gpt-5-for-developers/
    - 内部前端评测的形式没有公开，从「70% of the time」的写法看是两两偏好
  - [原文] GPT-5-Codex（2025-09）
    - "can spin up its own browser, look at what it built, iterate, and attach a screenshot"
    - "significant improvements in human preference evaluations when creating mobile websites"
    - 链接：https://openai.com/index/introducing-upgrades-to-codex/
  - [原文] GPT-5.1-Codex-Max（2025-11）："trained on real-world software engineering tasks, like PR creation, code review, frontend coding, and Q&A"
    - 链接：https://openai.com/index/gpt-5-1-codex-max/
  - [原文] GPT-5.3-Codex（2026-02）
    - 用 "develop web game skill and preselected, generic follow-up prompts like 'fix the bug' or 'improve the game'" 自主迭代游戏，跑了数百万 token
    - 链接：https://openai.com/index/introducing-gpt-5-3-codex/
  - [原文] GPT-5.4（2026-03）
    - "we trained GPT-5.4 with a focus on improved UI capabilities and use of images"
    - "trained to use image search and image generation tools natively"
    - "our first mainline model trained for computer use"
    - 归因与 Anthropic 一致："models often fall back to high-frequency patterns from the training data"
    - 链接：https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4 （2026-03-20）
  - [原文] GPT-5.6：可以检查并修改渲染结果
    - "step change in design judgment"
    - "inspect and refine the rendered result—not just generate the underlying code"
    - 链接：https://openai.com/index/gpt-5-6/
  - [原文] GPT-6 Astra（2026-09）
    - "brings years of research and big bets across pre-training, reinforcement learning, and alignment"
    - "stronger visual judgment to the websites, games, applications, and renderings it builds"
    - "run frontend QA checks to make sure all the features on that site work"
    - 评测表里有一项 "Internal Design Tasks 50.0%"，没有说明测什么
  - [原文] GPT-6 Astra system card：只有通用表述
    - "trained on diverse datasets"、"trained to reason through reinforcement learning"
    - 对齐改进 "spanning the composition of our pre-training data to our grading during reinforcement learning"
    - 链接：https://deploymentsafety.openai.com/gpt-6-astra
- **推理时 skill 与验证工具（公开）**
  - [二手] `develop-web-game` skill
    - 循环是 "implement → act → pause → observe → adjust"
    - 用 Playwright 发送短时输入，再看截图、console 和游戏暴露出的文本状态（`render_game_to_text`）
    - 镜像：https://www.mdskills.ai/skills/develop-web-game （openai/skills 官方仓库没抓到原文）
  - [原文] Astra 游戏博客（2026-09-04）里的验证手段
    - "compare rendered pixels with a particular effect enabled and disabled"
    - 用 Playwright 采集 90 个帧间隔
    - 暴露 draw call、三角形数等渲染计数器
    - "Browser playtesting still matters for shader compilation, GPU uploads, motion"
    - 链接：https://developers.openai.com/blog/how-to-build-games-with-astra
  - [原文] Astra Blender 博客（2026-09-04）
    - "inspected preview renders, adjusted the composition and lighting, and corrected details such as planting intersections"
    - "opened and inspected the scene in Blender through computer use"
    - 链接：https://developers.openai.com/blog/architectural-visualization-with-astra
- **Operator / CUA（2025-01）**
  - [原文] "combines GPT‑4o's vision capabilities with advanced reasoning through reinforcement learning"
  - 链接：https://openai.com/index/computer-using-agent/
- **未披露**：前端数据来源、设计偏好数据、视觉 reward 模型、Internal Design Tasks 的构成、Blender / 游戏训练

### 2.3 能推出什么
- [推断] OpenAI 的前端训练至少有三层信号，各层依据不同
  - 第一层：真实编码任务 RL，以测试通过作为 reward（Codex 原文）
  - 第二层：人类偏好对比，带 "70% of the time"、"human preference evaluations" 这类口径（GPT-5 / GPT-5-Codex 原文）
  - 第三层：从 GPT-5.4 起把 computer use、生图、搜图工具接进同一个 agent，让模型在训练中「看渲染结果」（"trained for computer use" 加上 5.6 的 "inspect and refine the rendered result"）
- [推断] "Internal Design Tasks" 和 GDPval 同属 "Professional" 表，很可能是专业设计交付物的专家评分，不是 WebDev 专项
- [推断] Astra 博客展示的验证手段可以直接做成 verifier 组件，说明 OpenAI 内部至少把这些当成标准工作流
  - 特效开 / 关的像素差分
  - 渲染计数器
  - 帧间隔统计
  - 游戏状态转文本
- [推断] 两家的「AI 味」归因几乎一字不差（Anthropic："distributional convergence"；OpenAI："high-frequency patterns from the training data"）
  - 双方都承认纯靠预训练分布只能得到平庸设计
  - 审美必须靠后训练信号或推理时约束注入

---

## 3. Google

### 3.1 披露了什么
- [原文] Gemini 2.5 技术报告（arXiv 2507.06261，2025-07）
  - §2.4：RL 同时用可验证奖励和生成式奖励
    - "a focus on verifiable rewards and model-based generative rewards"
    - "more diverse and complex RL environments, including those requiring multi-step actions and tool use"
  - §2.6：post-training 加入了整应用开发任务
    - "curated a diverse set of engineering tasks … multimodal, interactive scenarios such as end-to-end web and mobile application development"
    - 效果："an increase of over 500 Elo … on the LMArena WebDev Arena"
  - 链接：https://arxiv.org/html/2507.06261
- [原文] Gemini 2.5 Pro I/O 版博客把 WebDev Arena 当作对外目标
  - "measures human preference for a model's ability to build aesthetically pleasing and functional web apps"
  - 链接：https://blog.google/products/gemini/gemini-2-5-pro-updates/
- [原文] Gemini 3 Pro model card 只有模板句
  - "instruction tuning data reinforcement learning data, and human-preference data"
  - 3.1 Pro 和 3 Flash 的 card 写的都是 "based on Gemini 3 Pro"，没有增量
  - 链接：https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf
- [原文] Generative UI 没有训练，靠 prompt、工具和后处理实现
  - 时间：博客 2025-11-18；论文 arXiv 2604.09577
  - "we employ 3 main components: … tools, such as image generation and search … carefully crafted system instructions … a set of post-processors"
  - "this capability is emergent"
  - 另外发布了 PAGEN 评测集：在 Upwork 雇 18 名承包商手工制作页面，每页约 5 小时
  - 链接：https://research.google/blog/generative-ui-a-rich-custom-visual-interactive-user-experience-for-any-prompt/
- [原文] Antigravity 的产品层自验证循环
  - "uses the terminal to launch localhost, and actuates the browser to test"
  - 支持在截图上 "select-and-comment" 反馈
  - 链接：https://antigravity.google/blog/introducing-google-antigravity
- **未披露**
  - WebDev 数据来源和审美 reward 模型
  - Stitch 的训练
  - Gemini 3.x 的增量做法

### 3.2 能推出什么
- [推断] Google 的 WebDev 信号由三部分构成
  - 可验证奖励：构建、测试
  - 生成式 RM：审美、功能
  - Arena 风格的人类偏好
- [推断] Antigravity 截图评论是可积累的人类反馈来源，但官方没说用于训练
- [推断] Generative UI 的 PAGEN 人工页面代价很高（约 5 小时一页）。这说明 Google 也认为高质量参考网页需要专家手工产出，不能只靠爬取

---

## 4. 国内（只列增量；已有方案已引用的只做一行确认）

### 4.1 已有方案已引用：确认一行
- MiniMax-M2 系列报告（arXiv 2605.26494）§4.1.2 AppDev
  - "Domain experts contribute meta queries … An Agent-as-a-Verifier (AaaV) framework then performs automated rejection sampling"
- Kimi K3（arXiv 2607.24653）§4.2.7
  - "score structural and pixel-level similarity for tasks that replicate a reference. The reward is zeroed when a project fails to build … or fakes …"
- **更正**：GLM-5（arXiv 2602.15763）§4.2.5 的标题是 **Slide Generation**
  - 三级奖励（静态 → 运行时 DOM / bbox → 感知）针对的是 HTML 幻灯片，不是通用网页
  - 已有方案把它当成 WebDev 视觉奖励引用，需要注明这是迁移用法
  - 原文："we refine the renderer implementation to eliminate exploitable loopholes"

### 4.2 增量
- **Kimi K2.5**（arXiv 2602.02276）
  - [原文] App. B.3 预训练阶段做了代码与渲染图配对
    - "extensive image-code paired data … HTML, React, and SVG … paired with their corresponding rendered screenshots"
  - [原文] §4.4.2 在可验证奖励上叠加生成式 RM，并评审美
    - "apply GRMs on top of verified reward signals in … artifact-generating agents … aesthetic quality of generated artifacts"
- **Kimi K3**（arXiv 2607.24653）§3.1
  - [原文] 预训练配对扩展到 3D、游戏和 CAD
    - "programmatic multimodal data, coupling code snippets with their rendered visuals across … SVG, 3D assets, Webpage, Game, and CAD schematics"
  - 这是唯一一家明确把 3D 资产、游戏、CAD 的「代码 ↔ 渲染」配对写进预训练的
- **小米 MiMo-V2-Flash**（arXiv 2601.02780）§4.3.2
  - [原文] 用录屏视频而不是截图做判别
    - "execute generated code using Playwright to obtain rendered videos, and apply a multimodal visual discriminator to retain only high-quality samples"
    - "video-based evaluation reduces visual hallucination compared to static screenshots"
  - [原文] 用户 query 从网页反推："We reverse-engineer user queries from curated pages … eight web categories"
  - [原文] 同一个判别器两用，既过滤数据又做 RL 奖励
    - "Our vision-based verifier scores rollout executions from recorded videos, jointly evaluating visual quality, functional correctness, and executability"
- **MiniMax 博客**
  - [原文] M2.1：把审美纳入专项提升，并在真实运行时里评审
    - "systematically enhanced the model's design comprehension and aesthetic expression in Web and App scenarios, enabling … 3D scientific scene simulations"
    - VIBE 的 AaaV "assess the interactive logic and visual aesthetics … within a real runtime environment"
    - 链接：https://www.minimax.io/news/minimax-m21
  - [原文] M2.5：环境规模与过程奖励
    - "trained … across more than 200,000 real-world environments … not just frontend webpage demos"
    - "introduced a process reward mechanism"
    - 写 spec 的倾向是训练中自发出现的："Spec-writing tendency … emerged during training"
    - 链接：https://www.minimax.io/news/minimax-m25
  - M3：未披露
- **GLM-4.5V / 4.6V**（arXiv 2507.01006 v6）§3.1
  - [原文] 用 Playwright 交互网页并解析 DOM，构造 GUI grounding 数据
    - "employ the Playwright framework to deeply interact with webpages … parse all visible DOM elements"
  - RL 数据列表里包含 "UI coding"
  - 4.6V 的专属训练：未披露
- **GLM-5V-Turbo**（arXiv 2604.26752）
  - [原文] 把视觉编码当作提升感知的代理任务
    - "multimodal coding and grounding proved to be useful proxy tasks for perceptual learning"
- **Qwen3-VL**（arXiv 2511.21631）§3.2.6
  - [原文] 预训练数据包含截图转代码："converting UI screenshots into responsive HTML/CSS; generating editable SVG codes from images"
  - RL 部分（§4.4）没有渲染奖励
- **Qwen3-Coder**
  - [原文] 只讲 SWE 类任务
    - "Hard to Solve, Easy to Verify … automatically scaling test cases"
    - "20,000 independent environments in parallel"
  - 视觉奖励：未披露
  - 链接：https://qwenlm.github.io/blog/qwen3-coder/
- **字节 UI-TARS-2**（arXiv 2509.02544）§2.2 / §2.5.1：训练的是玩游戏，但验证方式可以迁移到写游戏
  - [原文] 游戏来源和状态校验
    - "collect publicly available HTML5/WebGL mini-games … synthesize new games using LLMs … exposing explicit state interfaces"
    - "JavaScript verification scripts that query runtime variables (e.g., score, level index, remaining lives)"
  - [原文] 沙箱可以控制时间："re-implemented Window timing APIs allow time acceleration and pause"
- **Seed-Coder / Seed1.8 / Seed2.0**
  - WebDev 训练未披露
  - Seed2.0（arXiv 2607.00248）§2.2 有真实使用统计
    - "dominance of frontend development … Vue.js leads decisively—more than three times the adoption of React"
- **Kimi K2**（arXiv 2507.20534）：WebDev 未披露
- **蚂蚁 Ling 2.0 / 2.6、MiMo-V2.6、Qwen3-Coder-Next**：本次没有复核，沿用已有方案的引用

### 4.3 能推出什么
- [原文归纳] 国内各家已经收敛到三层结构
  - 预训练：代码和渲染图配对（K2.5、K3、Qwen3-VL、GLM-5V）
  - 数据过滤：在真实沙箱里运行（MiMo、MiniMax、GLM）
  - RL：先过确定性门控，再叠加模型评审；构建失败或伪造实现时 reward 置 0（K3、MiMo）
- [推断] 两个可以直接拿来用的增量
  - 视频判别（MiMo）：解决动画、交互、three.js 动态场景在单张截图里看不到的问题
  - 游戏暴露状态变量再用 JS 断言（UI-TARS-2）：把「游戏好不好玩」的一部分转成可程序化验证
- [推断] Blender 方向没有任何一家国内厂商披露训练数据，最接近的是 K3 的「3D assets」配对

---

## 5. 3D / Blender / three.js（简表；verifier 另有专人调研）

| 时间 | 工作 | 任务 | reward / verifier | 训练方式 |
|---|---|---|---|---|
| 2024-03 | [SceneCraft](https://arxiv.org/abs/2403.01248) | 文本 → 场景图 → bpy | GPT-V 看渲染图迭代 | 仅推理时 |
| 2024-04 | [BlenderAlchemy](https://arxiv.org/abs/2404.17672) | 参考图 → 材质 / 几何编辑 | VLM 状态评估 | 仅推理时搜索 |
| 2024-12 | [CAD-Recode](https://arxiv.org/abs/2412.14042) | 点云 → CadQuery | CD / IoU（评测） | SFT，1M 条程序化合成 |
| 2024-12 | [BlenderLLM](https://arxiv.org/abs/2412.14203) | 指令 → bpy | GPT-4o 看 4 视角逐条打 0/1 | 先筛选再 SFT，自我改进 |
| 2025-01 | [VLMaterial](https://arxiv.org/abs/2501.18623) | 材质图 → 节点代码 | 感知相似度 | SFT，550K+ |
| 2025-04 | [BlenderGym](https://arxiv.org/abs/2504.01786) | 起始场景 + 目标图 → bpy 编辑 | 光度 / CD + VLM 选优 | 评测，245 对 |
| 2025-05 | [cadrille](https://arxiv.org/abs/2505.22914) | 点云 / 图 / 文 → CadQuery | 10·IoU，无效代码记 −10 | SFT → DPO / 在线 RL（GRPO 变体） |
| 2025-07 | [3D-Generalist](https://arxiv.org/abs/2507.06484) | 文本 → 场景动作代码 | 渲染图与文本的 CLIP 分 | 选最优后 SFT |
| 2025-08 | [LL3M](https://arxiv.org/abs/2508.08228) | 文本 → 多 agent 写 bpy | 看图自评 + 用户反馈 | 仅推理时 |
| 2025-08 | [MeshCoder](https://arxiv.org/abs/2508.14879) | 点云 → 分部件 bpy | CD 过滤 | SFT，部件约 10M 对 |
| 2025-08 | [CAD-RL](https://arxiv.org/abs/2508.10118) | 文本 → CadQuery | 可执行门控 × IoU + GPT-4o | CoT 冷启动 → RL |
| 2026-02 | [SceneReVis](https://arxiv.org/abs/2602.09432) | 多轮室内布局 | 格式 + 碰撞 + 语义进展 | 多轮 GRPO |
| 2026-05 | [BenchCAD](https://arxiv.org/abs/2605.10865) | 图 / 文 → CadQuery | 0.2·ess + 0.8·IoU，解析失败记 −1 | 基准 + GRPO 式 RL；Anthropic / OpenAI 都报了分 |

- [原文] CAD 方向已经形成在线 RL 的标准做法："online RL … outperform offline alternatives"（cadrille）
- [原文] three.js、shader 方向只有基准，没有 RL 训练论文
  - [WorldCoder-Bench 2606.01869](https://arxiv.org/abs/2606.01869)：在沙箱浏览器里探运行时状态，验证隐藏的行为契约
  - [WorldBench 2610.10622](https://arxiv.org/abs/2610.10622)：VLM 看画面和读代码两路判分，在 32% 的必需项上不一致
- [推断] Blender 方向难做在线 RL，原因有两条
  - 渲染贵
  - 没有几何真值，只能靠 CLIP 或 VLM 打分，容易被 hack
- 前沿实验室
  - 只有 Astra 的 Blender / UE5 演示和 BenchCAD 分数
  - Qwen3.8-Max 报了 QwenBlenderBench 69.9（internal），打分方法没公开
  - 训练披露：全部未披露

---

## 6. 共性推断：前沿实验室构造 visual coding 数据的几种可能管线

证据强度：**强** = 至少两家一手原文写明；**中** = 一家原文 + 其他家间接证据；**弱** = 只能从产品形态或 harness 推出

### 管线 1：代码 ↔ 渲染配对（预训练 / 中训）——强
- 做法：大量 HTML / React / SVG / 3D 代码 → 无头渲染 → 得到（截图或视频，代码）配对，外加元素级 grounding QA
- 证据
  - Kimi K2.5 App. B.3
  - Kimi K3 §3.1（扩展到 3D、游戏、CAD）
  - Qwen3-VL §3.2.6
  - GLM-4.5V §3.1
  - GLM-5V-Turbo（作为感知代理任务）
- 西方：未披露。Anthropic 只写 "synthetic data generated by other models"

### 管线 2：真实页面反推需求（反向构造）——强
- 做法：高质量真实页面 → 反推出用户 query → 原页面当参考答案或复刻目标；复刻任务用结构 + 像素相似度打分
- 证据
  - MiMo-V2-Flash §4.3.2："reverse-engineer user queries from curated pages"
  - Kimi K3 §4.2.7：复刻任务用结构和像素奖励
  - Fable 5 宣传 "rebuilding a web app's source code from screenshots alone"（能力说明，不是训练披露）

### 管线 3：专家种子需求正向合成 + 沙箱 agent 判分（RL 主力）——强
- 做法
  - 专家写 meta query，模型扩写成具体需求
  - 在沙箱里构建、运行
  - 判分分层：执行门控 → 浏览器交互检查 → 视觉评审
  - 构建失败或伪造实现时 reward 置 0
- 证据
  - MiniMax M2 §4.1.2（AaaV）
  - M2.5（20 万+ 环境、过程奖励）
  - Kimi K3 §4.2.7
  - Gemini 2.5 §2.6（"end-to-end web and mobile application development" 进入 post-training）
  - Codex："trained using reinforcement learning on real-world coding tasks in a variety of environments"

### 管线 4：rubric 化的审美评审（生成式 RM / 独立 evaluator）——中
- 做法
  - 把「好不好看」拆成几个可评分维度：设计整体性、原创性、工艺、功能
  - 用 few-shot 校准独立 evaluator，叠加在可验证奖励之上
  - 每个维度设硬阈值
- 证据
  - Kimi K2.5 §4.4.2：GRM 评 "aesthetic quality of generated artifacts"
  - Gemini 2.5 §2.4："model-based generative rewards"
  - Anthropic harness 博客的四维 rubric 与 few-shot 校准（推理时披露）
  - Anthropic 把用模型当 grader 的环境单列为「高风险 grader hacking」（Fable 5 §6.4.2），侧面说明这类环境在 Claude 训练中真实存在
- 风险
  - 措辞会引导审美收敛（Anthropic 原文）
  - grader 可能被利用，需要持续监控

### 管线 5：渲染在环的 agent 轨迹（截图 / 录屏 / 计算机操作）——中
- 做法
  - 策略模型自己开浏览器或 Blender，截图、录屏、看渲染结果后修改
  - 轨迹本身既是 SFT 数据，也是 RL rollout
  - 判分时用视频而不是单张截图
- 证据
  - MiMo-V2-Flash：录屏视频判别
  - GPT-5.4："first mainline model trained for computer use"，并且 "trained to use image search and image generation tools natively"
  - GPT-5.6：可以 "inspect and refine the rendered result"
  - GPT-5-Codex："spin up its own browser, look at what it built, iterate"
  - Anthropic 长程 harness 用 Puppeteer 截图做端到端测试

### 管线 6：人类偏好对战数据（Arena 式）——中
- 做法：同一题下多个模型的产物两两对比，作为偏好或 RM 训练数据，也作为对外指标
- 证据
  - GPT-5 "beating OpenAI o3 at frontend web development 70% of the time in internal testing"
  - GPT-5-Codex "human preference evaluations when creating mobile websites"
  - Gemini 2.5 / 2.5 Pro 把 WebDev Arena Elo 作为目标
  - Gemini 3 card 列出 "human-preference data"
- 局限：没有任何一家说过用 Arena 公开数据训练

### 附：3D / 游戏的可验证信号（给 verifier 组参考）
- CAD：可执行门控 × IoU，在线 RL 已经成熟（cadrille、CAD-RL、BenchCAD）——强
- 游戏：暴露状态接口，用 JS 断言查询分数、关卡、生命等运行时变量（UI-TARS-2）；时间 API 可以加速或暂停——中（原文用于玩游戏）
- three.js / 渲染特效
  - 来自 OpenAI Astra 游戏博客：特效开 / 关的像素差分、渲染计数器、Playwright 帧间隔——弱（这是产品工作流，不是训练）
  - 来自 WorldCoder-Bench：探查运行时状态——弱

