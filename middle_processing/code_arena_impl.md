# LMArena Code Arena / WebDev Arena 实现调研

- 调研日期：2026-09-24；全部出处为当天用 curl 抓取的原文
- 「未公开」表示抓到的官方页、论文、仓库里都没有写，不做推测

## 0 时间线

- 2023-04：Chatbot Arena 开始收集投票（[2403.04132](https://arxiv.org/abs/2403.04132)）
- 2024-12：WebDev Arena 上线；博客 2025-03-10 发布（[arena.ai/blog/webdev-arena](https://arena.ai/blog/webdev-arena)）
- 2025-11-12：Code Arena 发布，新开 WebDev V2 榜，旧榜改名 WebDev Legacy 并计划退役，数据不合并（[arena.ai/blog/code-arena](https://arena.ai/blog/code-arena)）
- 2026-05-08：Code Arena WebDev 按 7 个任务类别分榜，依据 5 个月内 25 万+ 条过滤后的 prompt（[arena.ai/blog/new-categories-code-arena](https://arena.ai/blog/new-categories-code-arena)）
- 2026-07-02：Fullstack Code Arena 发布（[arena.ai/blog/fullstack-code-arena](https://arena.ai/blog/fullstack-code-arena)）

## 1 用户从哪来

- **谁在投票**：公开网站的普通访客，官方称来自 AI 爱好者、学生、研究者、开发者与普通用户，「不只是专家意见」（[FAQ](https://arena.ai/faq)）
  - Code Arena 另靠 Discord 社区提出新题目、参与测试（[code-arena](https://arena.ai/blog/code-arena)）
- **是否需要登录**：未公开
  - 抓到的 FAQ、How it works 页都没有写投票前必须登录
  - Chatbot Arena 论文只写用户使用前须接受服务条款，同意数据公开（[2403.04132](https://arxiv.org/abs/2403.04132) §3.1）
- **为什么愿意来**：免费使用前沿模型
  - 论文原文：为吸引参与，「已免费提供 50 多个最先进模型」；「我们提供免费服务」是用户自带 prompt 的动力（[2403.04132](https://arxiv.org/abs/2403.04132) §1、§3.1）
  - FAQ：匿名代号模型让用户提前用到未发布的前沿模型（[FAQ](https://arena.ai/faq)）
- **投票量级**
  - 全平台：月访客 1,000 万+，累计对话 7 亿+，累计投票 8,200 万+（[arena-100m-revenue](https://arena.ai/blog/arena-100m-revenue)，2026-06-29）
  - WebDev Arena：上线到 2025-03 共 8 万+ 票；去重前 103,096 票、去重后 61,473 票（[webdev-arena](https://arena.ai/blog/webdev-arena)）
  - Code Arena：5 个月 25 万+ 条过滤后的 prompt；投票数未公开（[new-categories-code-arena](https://arena.ai/blog/new-categories-code-arena)）
- **付费标注员或专家**：公开排行榜靠社区投票，未见付费标注员的说明
  - Chatbot Arena 论文另请专家复核 160 场对战，众包与专家一致率 72%–83%，专家之间 79.4%–89.8%（[2403.04132](https://arxiv.org/abs/2403.04132)）
  - 「Arena Expert」是按 prompt 难度筛出的子集（占全部 prompt 5.5%），不是专家标注员（[leaderboard-changelog](https://arena.ai/blog/leaderboard-changelog)）

## 2 怎么接各家模型

- **接入方式**：官方政策只要求模型能通过以下任一途径公开使用：开源权重、公开 API、公开服务（如 ChatGPT、Gemini App），或厂商公开承诺后在 Arena 首发（[Leaderboard Policy](https://arena.ai/blog/policy)）
  - 具体调官方 API 还是 OpenRouter 这类聚合商：未公开
  - 论文写与 OpenAI、Google、Anthropic、Mistral、Hugging Face 等厂商合作接入最新模型（[2403.04132](https://arxiv.org/abs/2403.04132) §1）
- **谁付 API 费**：未公开
  - 早期：论文致谢列出 Kaggle、MBZUAI、a16z、Together AI、Anyscale、HuggingFace 赞助（[2403.04132](https://arxiv.org/abs/2403.04132)）
  - 现在：公司靠向企业、模型实验室、开发者出售 AI 评测服务营收，年化收入 1 亿美元（[FAQ](https://arena.ai/faq)，[arena-100m-revenue](https://arena.ai/blog/arena-100m-revenue)）
- **匿名私测未发布模型**：允许（[Leaderboard Policy](https://arena.ai/blog/policy)）
  - 每个匿名模型一个唯一代号，攒到分数稳定（至少 1,000 票，通常更多）或厂商撤回为止
  - 结果只私下给厂商，然后从 Arena 下线
  - 厂商可以在发布前测多个变体
  - 测过的模型公开发布后，分数先标为 preliminary，直到发布后攒够新票
  - 测试未发布模型的对话数据会分享给厂商
- **上榜规则**：只收第一方基础模型，且必须对全球公众开放（开源权重、公开 API、公开服务三选一，或满足条件的 Arena 首发）；至少 1,000 票且分数稳定后上榜（[Leaderboard Policy](https://arena.ai/blog/policy)）
  - Arena 首发的条件：厂商公开承诺 2 周内正式开放，书面确认与正式版相同，开放不少于 30 天；做不到就下榜
- **下榜规则**
  - 公开发布后 API 可用不足 30 天就下榜；Arena 保留弃用模型的权利（不再公开、同系列有新版、有更便宜且更强的模型）；退役模型列入公开清单（[Leaderboard Policy](https://arena.ai/blog/policy)）
- **采样规则**：每场对战至少一方是公开模型；至少 20% 的对战只在公开模型之间进行；公开模型的抽样概率通常均匀，但会为体验与榜单完整性做调整，回归时重新加权保证分数无偏（[Leaderboard Policy](https://arena.ai/blog/policy)）

## 3 执行环境

### 3.1 WebDev Arena（旧版，2024-12 起）

- 出处均为 [arena.ai/blog/webdev-arena](https://arena.ai/blog/webdev-arena)
- **沙箱**：E2B 的基础设施，底层是 Amazon Firecracker microVM（KVM）；每个应用一个独立 microVM，启动约 150 ms，可同时运行上千个应用
- **技术栈**：预设 Next.js 框架；TypeScript React 组件、Tailwind（禁用任意值写法）、单文件；图表类需求可用 recharts 与 shadcn/ui chart；不许改 package.json 等依赖文件
- **系统提示词**：原文公开，开头为 "You are an expert frontend React engineer who is also a great UI/UX designer..."，要求默认导出、无必需 props、列出并安装全部额外依赖
- **输出格式**：结构化 JSON，字段含 commentary、template、title、description、additional_dependencies、install_dependencies_command、file_path 等
  - 不支持结构化输出的模型走两段式：先用原生格式生成，再用 GPT-4-mini 转成该 JSON（原文写作 GPT-4-mini）
- **多文件 / 工具 / 多轮**：只有单文件；没有工具调用；原文把单文件与只支持 Next.js 列为局限
- **多模态**：后来支持图片输入（base64 或 URL），当时 7 个视觉模型可用

### 3.2 Code Arena（2025-11-12 起）

- 出处均为 [arena.ai/blog/code-arena](https://arena.ai/blog/code-arena)，另注的除外
- **Agent 多轮**：模型通过结构化工具调用执行动作，工具有 create_file、edit_file、read_file、run_command；支持多轮、多步迭代
- **文件结构**：每次生成带完整项目结构（HTML、CSS、JS）
  - 发布时写明多文件 React 应用、agent 支持、多模态输入、多文件项目的隔离沙箱「将在未来几个月推出」
  - 2026-05 的分类博客称用户已经在让模型构建多文件 React 应用，模型可用文件编辑、执行、联网、媒体理解等工具（[new-categories-code-arena](https://arena.ai/blog/new-categories-code-arena)）
- **记录与渲染**
  - 每个动作记录并版本化，快照存在 Cloudflare R2，并关联 Arena 数据库
  - 前端用 CodeMirror 6 显示源码，同时给实时预览
  - 会话可持久化，可凭链接分享
- **沙箱服务名**：Code Arena 博客没有点名 E2B 或其他服务商，只写在「受控、隔离的环境」里运行；是否沿用 E2B 未公开
- **评分维度**：投票时参考 Functionality、Usability、Fidelity 三个轴；每票记录模型版本、延迟与环境
- **与 WebDev Arena 的区别**：
  - 架构重建，从单次生成改为 agent 工具调用
  - prompt、生成、投票都在 Arena 自己的基础设施里完成
  - 新开 WebDev V2 榜，不合并旧数据
  - 每次改界面前先做偏差审计，测它对投票行为的影响
- **Fullstack Code Arena（2026-07-02）**（[fullstack-code-arena](https://arena.ai/blog/fullstack-code-arena)）
  - 支持 PostgreSQL 数据库、用户认证、Row Level Security，可接第三方 API key
  - 沙箱里常驻 dev server，支持热重载
  - 新增 bash 与联网搜索工具
  - 可一键部署到 Vercel

## 4 防作弊与打分

- **匿名与揭晓**：投票时模型匿名，投票后立刻揭晓名字；只有揭晓前的票计入排名；每次投票后重新匿名抽模型（[FAQ](https://arena.ai/faq)）
  - Side by Side（用户自选模型）和 Direct 模式的票不进榜
- **去重**：WebDev Arena 发现大量票来自首页示例 prompt，去重后票数从 103,096 降到 61,473，排名只有少数交换（[webdev-arena](https://arena.ai/blog/webdev-arena)）
- **防刷票**：Chatbot Arena 论文给出异常用户检测方法（[2403.04132](https://arxiv.org/abs/2403.04132) §5.1）
  - 把用户的投票与历史分布比较，算出 p 值，再用 Fisher 合并检验加 Bonferroni 类校正做序贯检验
  - 检测时点随机选取，防止被针对
  - 另用 OpenAI moderation API 标记不安全对话
  - Code Arena 专门的防刷票机制：未公开
- **Bradley-Terry 打分**：用 Bradley-Terry 模型从两两对战估计模型强度，界面写作类 Elo 分数（[FAQ](https://arena.ai/faq)，[webdev-arena](https://arena.ai/blog/webdev-arena)）
  - 置信区间：论文用 pivot bootstrap 与 sandwich 稳健标准误（[2403.04132](https://arxiv.org/abs/2403.04132) §4）
  - Arena-Rank（2025-12-18 开源）改为闭式置信区间，加入重新加权，保证对战少的模型也被公平处理，比旧 FastChat 实现快 30 倍以上（[arena-rank](https://arena.ai/blog/arena-rank)，[GitHub lmarena/arena-rank](https://github.com/lmarena/arena-rank)）
- **Style control**：把回答长度、markdown 标题数、加粗数、列表项数作为额外协变量放进 Bradley-Terry 回归，分离风格与内容的影响（[style-control](https://arena.ai/blog/style-control)，2024-08-29）
  - WebDev / Code Arena 是否使用 style control：未公开
- **平局与「两个都差」**
  - 界面给 tie 与 both are bad 两个按钮（[2403.04132](https://arxiv.org/abs/2403.04132) §3.1）
  - WebDev Arena 平局率 26%（Chatbot Arena 为 35%），其中「两个都差」占比更高；18% 的票是「两个都差」，多因依赖安装失败或无法编译
  - 按类别算胜率时平局记 0.5 胜（[webdev-arena](https://arena.ai/blog/webdev-arena)）
  - 平局和「两个都差」在排行榜的 BT 拟合里怎么计入：抓到的博客与论文都没有写明，未公开

## 5 数据公开

- **HF 数据集**（组织 [lmarena-ai](https://huggingface.co/lmarena-ai)，下载量为 HF API 近 30 天）
  - [webdev-arena-preference-10k](https://huggingface.co/datasets/lmarena-ai/webdev-arena-preference-10k)：1 万场 WebDev Arena 对战，10 个模型；需填写姓名、邮箱、单位并同意协议，协议禁止转给第三方；375 次下载
  - 同组织另有：arena-human-preference-55k / 100k / 140k、arena-expert-5k、search-arena-24k、repochat-arena-preference-4k、VisionArena-Battle、leaderboard-dataset 等
  - Code Arena 对战数据集：HF 上未找到
- **公开范围**：官方只公开部分匿名投票数据，含 prompt、投票结果与模型配对，不发布完整对话日志（[FAQ](https://arena.ai/faq)）
- **代码**
  - 排名方法：[lmarena/arena-rank](https://github.com/lmarena/arena-rank)（120 star）
  - 旧平台：[lm-sys/FastChat](https://github.com/lm-sys/FastChat) 的 serve/monitor 模块
  - WebDev Arena 分析：博客附 Colab 笔记本
  - WebDev / Code Arena 平台本身的代码：lmarena 组织的 GitHub 仓库里没有（只有 copilot-arena、search-arena、p2l、nextjs-tailwind-starter 等），未公开

## 6 已知批评与回应

- **批评**：「The Leaderboard Illusion」（Singh 等，Cohere Labs 等，[2504.20879](https://arxiv.org/abs/2504.20879)）
  - 数据范围：2024-01 至 2025-04，200 万场对战、42 家厂商、243 个模型
  - 私测多版本只公开最好的：Meta 在 Llama 4 发布前测了 27 个私有变体
  - 数据不对称：闭源模型抽样率更高、更少被下线；Google、OpenAI 分别拿到约 19.2%、20.4% 的对战数据，83 个开源权重模型合计 29.7%
  - 静默下线：243 个公开模型中 205 个被静默弃用，官方列表只列 47 个；被静默弃用的模型 64% 是开源权重，下线会违反 Bradley-Terry 的前提
  - 过拟合：用 Arena 数据训练，在 ArenaHard 上相对提升最高 112%
  - 建议：禁止撤回已提交的分数、公开下线清单、限制私测变体数量等
- **LMArena 回应**（[our-response](https://arena.ai/blog/our-response)，2025-05-09）
  - 接受并调整
    - 在政策中明确所有厂商都可以私测多个变体
    - 标明哪些模型从对战中退役
    - 同时私测超过 10 个模型的，发布后先标 provisional，再攒 2,000 张新票
  - 反驳
    - 开源模型占比实为 40.9%，不是 8.8%
    - 「私测可提升 100+ 分」出自高斯模拟；按官方分析，50 次测试加 3,000 票时约 +11 Elo，并随新票累积趋近 0
    - 同一 checkpoint 分数差异在置信区间内，例如 1069 ±27 与 1054
    - 各厂商按同一政策对待，Cohere 自 2025-01 起私测 9 个模型
    - 112% 的数字来自 LLM 判官的静态 benchmark Arena-Hard，不代表 Chatbot Arena
  - 说明：各厂商最好的模型会被上采样以改善用户体验
  - 现行政策（2026-09-01 更新）已写入「允许测多个变体」与「preliminary 分数」条款（[Leaderboard Policy](https://arena.ai/blog/policy)）
- **WebDev / Code Arena 专属的批评**：抓到的材料里没有；官方博客自述的局限是单文件、只支持 Next.js、18% 的票为「两个都差」（[webdev-arena](https://arena.ai/blog/webdev-arena)）

