<a class="anchor" id="tk-1"></a>

## 1 Rendering Repos Already Ship Their Own Pixel Baselines

渲染库的回归测试里早就躺着一批现成的 Verified Task。three.js、Babylon.js、Blender 这类仓库把「场景代码 + 参考图」一起提交进版本库，CI 渲染后逐像素比对。关键在于提交习惯：任何改变渲染行为的 PR 必须同时更新参考图，于是每一个这样的 commit 都自带一对数据——旧代码配新参考图必然失败，新代码配新参考图必然通过。这正是 [SWE-bench](https://arxiv.org/abs/2310.06770) 的 fail-to-pass 结构，只是测试换成了像素阈值，不需要 VLM judge。

核心发现：参考图的存量是万张量级，而改动过基线的 commit 是千条量级，后者才是任务供给的真实约束。

| 仓库 | 许可 | 参考图 | 改过基线的 commit | 测试机制 |
|---|---|---|---|---|
| [three.js](https://github.com/mrdoob/three.js/tree/dev/examples/screenshots) | MIT | 610 张，对应 611 个 example | 1,143 | [无头浏览器](https://github.com/mrdoob/three.js/tree/dev/test/e2e)渲染 400×250，像素阈值 0.1，差异像素上限 0.1%，注入确定性随机数与时钟，54 个 example 在豁免名单 |
| [Babylon.js](https://github.com/BabylonJS/Babylon.js/tree/master/packages/tools/tests/test/visualization) | Apache-2.0 | 975 张，对应 901 个测试 | 397 | 分 WebGL1 / WebGL2 / WebGPU 三套，338 个测试声明了排除引擎 |
| [Blender](https://github.com/blender/blender/tree/main/tests/files/render) | GPL | 2,596 张，对应 839 个场景文件，48 个类别 | 未统计（主仓库托管在 Gitea，表中链接为 GitHub 镜像） | cycles / eevee / workbench 各一套参考图 |
| [maplibre-gl-js](https://github.com/maplibre/maplibre-gl-js/tree/main/test/integration/render) | BSD-3 | 1,950 张 | 203 | 声明式样式配参考图 |
| [pixijs](https://github.com/pixijs/pixijs/tree/dev/tests/visual) | MIT | 1,711 张 | 249 | 视觉快照 |
| [primer/react](https://github.com/primer/react/tree/main/.playwright/snapshots) | MIT | 7,766 张 | 481 | 浏览器驱动的组件截图 |
| [Chart.js](https://github.com/chartjs/Chart.js/tree/master/test/fixtures) | MIT | 约 667 张 | 315 | fixture 配参考图 |
| [p5.js](https://github.com/processing/p5.js/tree/main/test/unit/visual) | LGPL-2.1 | 604 张 | 156 | 视觉单测 |
| [openlayers](https://github.com/openlayers/openlayers/tree/main/test/rendering/cases) | BSD-2 | 235 个 case | 291 | 入口脚本配参考图 |
| [deck.gl](https://github.com/visgl/deck.gl/tree/master/test/render/golden-images) | MIT | 252 张 | 178 | golden image |
| [plotly.js](https://github.com/plotly/plotly.js/tree/master/test/image/baselines) | MIT | 1,324 张 | 未取到（目录级接口只返回 1 条） | mock 配参考图 |

表中数字均为本项目用 GitHub / Gitea 接口实测：参考图读文件树计数，commit 数读 `commits?path=` 分页（[查询方法与原始记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/02_task_sources.md)；three.js、Babylon.js、Blender 三项另做过[独立复核](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/92_number_audit.md)）。

数据解读：9 个 GitHub 仓库（上表除 Blender、plotly.js）合计 3,413 个改过基线的 commit，参考图约 1.9 万张（[本项目实测汇总](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/02_task_sources.md) §1.1：commit 数按 `GET /repos/{repo}/commits?path={基线目录}&per_page=1` 读 Link 头末页页码，参考图按 `git/trees/{branch}?recursive=1` 过滤计数）。这个 3,413 是**上界，不是可用任务数**，原因有两条。第一，一部分 commit 只是整体重新生成截图（换浏览器版本、换字体、换 GPU 驱动都会触发），代码没动，构造不出 fail-to-pass 对。第二，像素基线对环境极度敏感，必须把浏览器、字体、渲染后端全部锁进同一个 Harness 镜像，锁不住的 commit 直接作废。结论是先做这一层：环境脚本现成、Verifier 确定、许可干净，three.js 加 Babylon.js 合计约 1,500 个 commit，Blender 另有 839 个场景。

<a class="anchor" id="tk-2"></a>

## 2 The Rest of the Supply Is Blocked by Licence or Missing a Verifier

离开像素基线仓库，供给立刻分化成两类：量大但要自建 Verifier，或者技术上完美但许可过不去。

| 级别 | 来源 | 可验证性 | 规模 | 许可风险 |
|---|---|---|---|---|
| S | [渲染库像素基线仓库](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/02_task_sources.md) | 仓库自带像素阈值 | 参考图约 1.9 万张，改基线 commit 3,413 个 | 低（Blender 为 GPL，需单独评估） |
| S | 带截图的 issue 加修复 PR（[SWE-bench Multimodal](https://arxiv.org/abs/2410.03859) 范式） | PR 自带单测 | 候选 issue 约 30 万（[GitHub 搜索实测](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/02_task_sources.md)），按实测转化率折算约 1,400 个 | 低，按仓库许可过滤 |
| A | [浏览器截图比对生态的长尾仓库](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/02_task_sources.md) | 高，但截图会漂移 | 估几千仓库、几万 PR | 低 |
| A | 程序化生成器（[Infinigen](https://arxiv.org/abs/2306.09310) 系，[仓库](https://github.com/princeton-vl/infinigen)） | 可确定性重渲 | 论文自报 182 个生成器乘无限种子 | 低（BSD） |
| A | [CodePen](https://blog.codepen.io/2016/11/25/10000000/) | 要自己截图造目标 | 1,000 万以上作品（官方 2016 年数字） | 低，公开作品默认 MIT（[官方说明](https://blog.codepen.io/documentation/licensing/)） |
| A | [js13kGames](https://js13kgames.com/sitemap.xml) | 要自建试玩 Verifier | 2,799 个（sitemap 实测） | 中，各作者自定 |
| B | [ShaderToy](https://www.shadertoy.com/)、[shaders21k](https://arxiv.org/abs/2211.16412) | 逐帧像素，最干净 | shaders21k 约 2.1 万个程序；ShaderToy 全站总数未能核实 | 高，默认 NC-SA（二手口径，官方 [terms](https://www.shadertoy.com/terms) 未能实测） |
| B | Blender StackExchange、图形类问答标签 | 要补 Verifier | `python` 加 `scripting` 两个标签约 2 万个问题（[API 实测](https://api.stackexchange.com/2.3/tags/python;scripting/info?site=blender)） | 中，数据 dump 条款限制 LLM 训练（[heise](https://heise.de/-9823083)） |
| B | 设计稿站点 | 设计稿当目标图 | 中等 | 中，robots 点名禁 AI 爬虫（[Figma robots](https://www.figma.com/robots.txt)）或禁止再分发设计稿（[Frontend Mentor FAQ](https://www.frontendmentor.io/faqs)） |
| C | 作品展示站、付费资产站 | 没有源码 | — | 高（[逐站记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/02_task_sources.md)） |

数据解读：带截图的 issue 数量看着有 30 万，但端到端转化率是千分之几。[SWE-bench Multimodal](https://arxiv.org/abs/2410.03859) 的实测是 13.5 万 PR 筛到 1,478 个候选、最后 617 个实例，折合 0.457%；按同样的转化率，30 万候选只能出约 1,400 个任务，是千量级不是万量级。这个口径和后面讲产能时 three.js 漏斗算出的约 230 个任务（[本项目估算](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/13_scaling_tasks.md)）是一致的——真实素材的产出量级就是三位到四位数。ShaderToy 是全表技术上最好的 shader 源——逐帧像素就是确定性 Verifier——但默认许可是非商用，这一条单独把它踢出训练池。云端托管的视觉回归服务（[Chromatic](https://www.chromatic.com/)、[Percy](https://percy.io/) 一类）同理排除：基线存在服务商那边，仓库里根本不存在。

预训练与中训练阶段的「代码配渲染图」是另一套供给，它的上限比任务池更早见底。公开可复用的配对总量约 1,000 万条（[本项目汇总](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/09_pretrain_data.md)），其中真实页面且可渲染的只有 [WebCode2M](https://arxiv.org/abs/2404.06369) 一家（[HF 实测](https://huggingface.co/datasets/xcodemind/webcode2m) 317 万行，[净化版](https://huggingface.co/datasets/xcodemind/webcode2m_purified) 256 万行）。合成数据的分布缺口是硬的：[WebSight](https://arxiv.org/abs/2403.09029) 平均 647 个 token、19 个标签、DOM 深度 5，而 WebCode2M 清洗后的真实页面是 5,366 个 token、184 个标签、深度 15，[Design2Code](https://arxiv.org/abs/2403.03163) 收的原始 C4 页面更是 31,216 个 token（WebCode2M 表 2）。同架构同规模对照下，合成数据训练后在真实测试集上的 TreeBLEU 是 0.06，真实数据是 0.35（WebCode2M 表 3）。合成数据还会腐烂：[WebSight](https://huggingface.co/datasets/HuggingFaceM4/WebSight) 的图片一律引用一个随机图床域名，该域名 2026-10-15 [实测返回 503](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/09_pretrain_data.md)，这批数据已无法按原样重渲。3D 侧更干脆——[Objaverse-XL](https://arxiv.org/abs/2307.05663) 论文自报 1,020 万个去重对象（HF 元数据 1,085 万行），里面没有一行可执行代码，它索引的 12 种扩展名全是几何资产格式（[仓库](https://github.com/allenai/objaverse-xl)，[本项目核对](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/09_pretrain_data.md)），只能当逆向任务的目标图，不能当「代码到图」的正样本。

<a class="anchor" id="tk-3"></a>

## 3 Verification Lands on State, Not on Code

一个 Verified Task 的最小描述是五元组：初态、Problem Statement、对模型公开的观察接口、对模型隐藏的断言集、参考解。reward 只看任意实现能否把初态推到满足断言的状态，不看它和参考解像不像。

这不是风格偏好，是被等价实现逼出来的。多份不同的 CAD 脚本能产出几何等价的模型，SFT 学不动这件事，所以 [CAD-Coder](https://arxiv.org/abs/2505.19713) 在 RL 阶段改用几何距离（Chamfer）做奖励。把参考解当整体对照打分的做法也实测更差：[Rubrics as Rewards](https://arxiv.org/abs/2507.17746) 在 HealthBench 上，让 judge 拿参考答案做 Likert 对照是 31.7%，先用参考答案生成逐条 rubric 再打分是 35.9%（表 1）。

### 3.1 Eight Paradigms, Ranked by What They Cannot See

| 范式 | 目标来源 | 主要观察层 | 最大短板 |
|---|---|---|---|
| fail-to-pass 与 pass-to-pass | 参考解的状态 | 状态与结构 | 断言覆盖不到即漏检 |
| 逆向构造（从渲染图出发） | 已有产物的渲染 | 像素与几何 | 机制不可见，一图多解 |
| 变异扰动（破坏正确产物） | 参考解的状态 | 状态 | 变异分布偏离真实错误 |
| 需求编译为 rubric | 需求加参考解辅助 | 全部，逐条标层 | judge 幻觉 |
| 交互行为测试 | 隐藏行为契约 | 动作前后的状态差分 | 契约编写成本高 |
| 属性与不变量 | 通用性质 | 状态与几何 | 不判需求是否满足 |
| 开放偏好对比 | 组内两两比较 | 像素与录屏 | 不判功能，成本是组大小的平方 |
| 难度与质量筛选 | 当前 policy 的通过率 | — | 依赖 policy 能力，需周期重跑 |

数据解读：前六种都能落到程序化信号上，后两种只能做兜底。选哪一层不是自由选择，而是被「这个需求的信息藏在哪」决定的。截图看不到物理和状态机，DOM 看不到画在画布里的东西——[WorldCoder-Bench](https://arxiv.org/abs/2606.01869) 在 1,434 对产物上实测，DOM 打分与隐藏状态真值的 Kendall τb 是 −0.021，截图加 VLM 是 −0.068，隐藏状态契约本身就是真值（1.000）；严重缺陷的误放率，DOM 33.7%、8 步 agent 式检查 45.6%、状态契约为 0（表 2）。

### 3.2 Reference Code Has Exactly Five Jobs

开发者写死的代码不是标准答案，它可能冗余、过时、性能差。拿代码相似度当奖励会把这些缺点一起学进去。它有五个正确用途（本项目设计，整理见 [03 可验证构造](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/03_verifiable_construction.md) §3.1，准入实现见 [gen_tasks.py](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/gen_tasks.py)）：

1. **证明可解**。参考解必须在 Harness 里跑通并通过全部断言，重复 3 次稳定（对应 [SWE-bench](https://arxiv.org/abs/2310.06770) 的 gold patch 规则与 [GameDevBench](https://arxiv.org/abs/2602.11103) 的已验证参考解）；做不到，问题在 Verifier 或题目，不在 policy。
2. **生成断言与 rubric**。从参考解的运行状态抽断言，把它的渲染结果交给 rubric 生成器，产出「桌面上有 4 把椅子、间距大致相等」这类可观察条目，而不是「和参考截图一样」。
3. **当可破坏的底子**。对参考解注入缺陷得到初态，修复题和 Verifier 校准集一起产出。
4. **校验 Verifier**。参考解必过、初态必挂、变异体必挂，三条任一不满足就先修 Verifier。
5. **SFT 冷启动**。它是多条合格轨迹之一，不进 RL 的 reward（同 [CAD-Coder](https://arxiv.org/abs/2505.19713) 的 SFT 再 GRPO 两阶段）。

参考解应被当作下界：reward 只要求满足断言，超过参考解不受惩罚。把它放进开放维度的组内比较池当锚，统计 policy 解对它的胜率；胜率持续很高的题说明参考已经不是好参考，用通过全部断言且胜率最高的 rollout 替换它，并重跑准入测试。

<a class="anchor" id="tk-4"></a>

## 4 Admission Testing Is Where Tasks Come From, Not Generation

让 LLM 在一个能跑的页面上提出若干语义性破坏，再附一句用户视角的需求，这一步很便宜。贵的是判断哪些破坏值得收。我们自己的流程（[gen_tasks.py](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/gen_tasks.py)）是三条准入测试全过才收：参考解必须过 Verifier（自比自，防 Verifier 本身坏掉）、破坏版必须被判挂（否则这个破坏不可验证）、被替换的代码片段必须在源码中唯一（防止改到别处）。

核心发现：LLM 提的破坏里约有一成是 Verifier 根本看不出来的（桌子 1/10，工作台补层前 2/16），准入测试把它们挡在数据集外，比事后在 RL 里发现噪声便宜得多（[实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §4）。

下面这个 demo 是那一轮造题的真实产物。默认停在被挡掉的那一条：模型提议把杯子整个倒过来，需求写得也合理，但杯子是一个圆台，倒过来之后占据的空间几乎没变，Verifier 判不出来，于是这道题被丢弃。

<iframe class="demo-frame" style="height:430px" src="demos/task-admission.html" loading="lazy"></iframe>

| 场景 | LLM 提 | 收 | 弃 | 弃的原因 |
|---|---|---|---|---|
| 桌子加杯子 | 10 | 9 | 1 | 杯子倒置：杯子是圆台，翻转后占据几乎不变 |
| 桌面工作台（13 个 mesh，带层级和旋转） | 16 | 14 → 16 | 2 → 0 | 立杆缺失、灯臂镜像；补上连通块统计后都能抓到 |

来源：[本项目实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §4。

数据解读：弃掉的 case 不是损失，是 Verifier 的体检报告。它精确指出了两处盲区——轴对称部件翻转后占据不变、细长部件在全局 IoU 里权重太小。其中细长部件这一条直接催生了一个新的检查层：按颜色统计连通块数与体积比。补上之后，前面两组共 29 个带标签变异仍然全部判对，零新增误杀（[实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §2.1，[mutate.py](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/mutate.py)）。这说明盲区是被具体 case 逼出来的，设计阶段想不出来；先造题再补 Verifier，比先定 Verifier 再造题有效。

收下来的 16 个任务按挂在第几层分布：6 个挂在多视角剪影层，8 个挂在按颜色的体素占据层，2 个挂在部件与拓扑层（[实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §4.1）。这个分布本身就是难度分布的粗略代理——挂在第一层的是一眼可见的粗错，挂在最后一层的是细节错。

<a class="anchor" id="tk-5"></a>

## 5 The Verifier Must Not Know More Than the Problem Statement

预实验里 opus-5.5 在 9 个桌子任务上一轮过 7 个。两个没过的，查下来都不是模型的问题（[实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §5）。

| 任务 | 需求原文 | Verifier 实际要求 | 结果 |
|---|---|---|---|
| 杯子颜色 | 杯子应使用有别于桌面木色的独立颜色 | 必须恰好是参考里那一种蓝 | 模型换了另一种颜色，该色体素 IoU 为 0，判挂 |
| 桌腿位置 | 桌腿应位于桌面四个角落附近 | 腿的位置要和参考几乎重合 | 模型把腿放到角上但缩进量不同，剪影 0.885 差一点点，判挂 |

数据解读：两次失败的根因同一条——Verifier 能查的信息量超过了 Problem Statement 给出的信息量。这类任务不是难，是不可解；进了 RL 就是纯噪声，而且会被误读成模型能力不足。两条解法：把参考渲染图放进 Problem Statement，让它变成信息补齐后的复刻任务；或者把 Verifier 放松到与描述同精度，例如判「颜色与木色的距离大于阈值」而不是「等于某个具体值」。第一条更好做也更可扩展，正好对应 Problem Statement 带多模态参考这个设定，所以在实验矩阵里作为独立一维（纯文本需求对文本加参考视角图）来测。

同一条纪律的另一面是断言不得依赖参考解的实现细节。[SWE-bench](https://arxiv.org/abs/2310.06770) 原始规则里就排除了「测试调用了解法新建的函数或类」的实例，因为命名任意、无法从题面推出。需要的锚点必须写进对模型公开的观察接口里：交互元素的标识约定、状态结构的 schema、必须保留的对象名。锚点公开，断言隐藏。

<a class="anchor" id="tk-6"></a>

## 6 The Admission Test Cannot See Its Own Two Blind Spots

前面那三条准入闸——参考解必过、破坏版必挂、被替换的片段唯一——挡掉了 Verifier 看不见的破坏。它们挡不住另外两件事，而且结构上挡不住。

**第一件：三条闸全过的任务仍然可能无解。**

闸的逻辑摆出来就清楚了。参考解当然过，它就是答案；破坏版当然挂，它就是故意做坏的；片段唯一只管别改错地方。没有任何一条在问「只拿着题面，这道题能做出来吗」。

本项目的实测频率不低：桌子那批 9 个任务里 2 个不可解（[实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §5），Blender 留出集 7 个里 1 个（[Blender 记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/10_blender_tasks.md) §3.3）。合计 3/16，按两成算，十万任务里就有两万道持续向 RL 注入噪声。

更糟的是它和难度筛选形成正反馈。不可解题的通过率稳定在 0 附近，看起来就像「很有挑战性」，于是难度带筛选不但不会剔掉它们，反而会优先保留（本项目在一道 0% 题上撞到过这种情况，见[实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §6.3）。

**修法是加第四条闸，查题面的可解性，而不是查产物。** 下面四步是本项目设计、尚未实现（相关的 ceiling check 设计见 [13 规模化](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/13_scaling_tasks.md) §2.3.6）：

1. 让一个与 Verifier 无关的模型只看 Problem Statement，枚举「你觉得验收会查哪些点」，输出一张清单。
2. 和真实断言集做匹配，算召回：被猜到的断言数除以断言总数。
3. 召回低于某个线的任务退回，未被猜到的那几条断言要么删掉，要么把对应信息补进题面。
4. 先在已有任务上校准——三道已知不可解的题是现成的金标准，这条闸抓不出它们就说明实现有问题。

成本是每道题多一次模型调用。按[本项目成本模型](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/13_scaling_tasks.md) §5.6，每个候选平均约 4.5 次调用（121 万次 / 26.9 万候选），这条闸的增量约两成。

**第二件：准入测试会把训练集偏向 Verifier 已经擅长的那类错误。**

被丢掉的破坏，是 Verifier 看不见的那些。留下来的破坏，是 Verifier 看得见的那些。一轮下来数据集很干净，代价是它系统性地不含「Verifier 的盲区」这一类问题。拿它训出来的模型，学会的是修 Verifier 看得见的毛病。

这件事没有干净的解法，但有一个便宜的体检：关掉某一层信号，重跑一遍准入，看收下来的任务少了多少、少的是哪一类。少得越多，说明数据集越依赖那一层，也就越偏向那一层能看见的错误。

核心发现：两个场景上各做一次留一层消融，依赖集中在体素层与部件层，而且它们各自独占了一部分任务类型。

| 关掉哪一层 | 桌面工作台（16 个提议） | 桌子加杯子（10 个提议） |
|---|---|---|
| 不关，全部信号 | 收 16 | 收 9 |
| 多视角剪影 | 收 16 | 收 9 |
| 体素占据 | 收 14 | 收 8 |
| 自洽性 | 收 16 | 收 9 |
| 部件与拓扑 | 收 14 | 收 9 |

来源：[本项目实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §8，脚本 [ablate.py](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/ablate.py)。

数据解读：关掉多视角剪影和自洽性，收下来的任务一个不少——不是因为这两层没用，而是它们抓的那些粗错误，别的层也能抓到。真正不可替代的是体素占据和部件与拓扑：各自独占两道题。换句话说，**如果当初没有加部件与拓扑这一层，训练集里就会少掉「细长部件缺失」这一类问题，而模型永远学不到修它。** 这个消融应该在每次改动 Verifier 之后都跑一遍，它量的不是判别力，是数据集的偏向。

<a class="anchor" id="tk-7"></a>

## 7 Data Quality Is a Set of Numbers, Not a Review Meeting

可解率只证明「参考解能过」，判别力证明「错的过不了」。两者都要，而判别力是最常被跳过的那一项。

| 指标 | 怎么算 | 门槛 | 依据 |
|---|---|---|---|
| 可解率 | 参考解通过全部断言，3 次重复取交 | 每题 100% | [SWE-bench](https://arxiv.org/abs/2310.06770) 的 gold patch 规则；[GameDevBench](https://arxiv.org/abs/2602.11103) 每题带已验证参考解 |
| 非平凡率 | fail-to-pass 断言在初态上全部失败；空解与静态截图解也必须失败 | 每题 100% | [SWE-bench](https://arxiv.org/abs/2310.06770) 的 fail-to-pass 定义 |
| 变异杀死率 | 被断言判失败的变异体占比 | 不低于 95%，未杀死的逐个审 | [WorldCoder-Bench](https://arxiv.org/abs/2606.01869) 的契约准入 |
| 替代实现通过率 | 已知正确的不同实现通过断言的比例 | 不低于 90%，过低说明断言绑了实现细节 | [CodeContests+](https://arxiv.org/abs/2506.05817) 的 TPR / TNR 口径 |
| 单条断言区分度 | 能区分最终判对与判错 rollout 的断言占比 | 为 0 的断言删除或改写 | [R2E-Gym](https://arxiv.org/abs/2504.07164)：多数任务里有区分力的测试不到 20% |
| 难度分布 | 当前 policy 采 k 次的通过率分桶 | 训练池以通过率严格落在 0 与 1 之间为主 | [DAPO](https://arxiv.org/abs/2503.14476) 的动态采样 |
| 重测一致性 | 同一产物重复验证 3 次结果不一致的比例 | 不超过 1%，超出先修时钟、种子与软件光栅 | [本地 Harness 的确定性实测](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/06_harness.md) §4.1 |
| 人审缺陷率 | 抽样人审中大问题比例 | 不超过 5% | [GameDevBench](https://arxiv.org/abs/2602.11103) 首轮人审 41 题：43% 无问题、50% 小问题、7% 大问题 |
| 污染率 | 与评测集的 n-gram 与 embedding 相似度超阈值比例，外加时间切分 | 0，命中即删 | [SWE-rebench](https://arxiv.org/abs/2505.20411) 的持续更新去污染 |

数据解读：R2E-Gym 的那一行是全表最该警惕的——「有测试」和「测试能分对错」是两件事，多数任务里能区分正误补丁的测试不到 20%（[R2E-Gym](https://arxiv.org/abs/2504.07164) 图 5 与正文），这些任务在 RL 里贡献的梯度接近噪声。[GameDevBench](https://arxiv.org/abs/2602.11103) 的 43% 则给出了自动出题的现实基线（首轮人审 41 题）：agent 出的题首轮只有 43% 完全干净，一半有小问题（场景跑到镜头外、断言了指令没要求的东西）。两个数字合起来说明一件事：造题环节的产出必须当候选看，准入测试才是真正的生产线。

这些指标还要周期重算。policy 变强后，原本通过率在 0 与 1 之间的题会变成全对；新的作弊方式也会出现，变异算子集需要跟着补。没有一组固定的 reward 能随 policy 能力增长一直有效（[The Verification Horizon](https://arxiv.org/abs/2606.26300) 引言的核心结论：「no fixed reward function can remain effective as policy capability continues to grow」）。

<a class="anchor" id="tk-8"></a>

## 8 Combinatorial Space Is Not Effective Diversity

程序化生成器报出来的「规模」几乎全是组合计数。[Infinigen](https://arxiv.org/abs/2306.09310) 自报 182 个生成器、1,070 个可解释自由度，论文自己把这个计数称作总体多样性的 proxy（表 2），全文没有做任何覆盖度、最近邻距离或成对相似度度量。[ProcTHOR](https://arxiv.org/abs/2206.06994) 自报可出 1,000 亿种以上 layout，同样零多样性度量。

核心发现：组合计数不但无信息量，还和下游收益脱钩——而且脱钩的方向是反的。

| 证据 | 数字 | 说明 |
|---|---|---|
| [ProcTHOR](https://arxiv.org/abs/2206.06994) 自己的规模消融（表 3） | 房屋数 10 / 100 / 1,000 / 10,000 对应 HM3D 零样本成功率 1.60% / 10.4% / 4.65% / 9.70% | 非单调，1,000 房比 100 房更差 |
| [HSSD-200](https://arxiv.org/abs/2306.11290v1) 对照 | 122 个高保真场景的 HM3DSem 零样本成功率 19%，ProcTHOR 的 10,000 个是 17%（v1 正文；v3 表 5 修订为 19.2% 对 12.5%） | 场景数差 82 倍，方向相反 |
| ProcTHOR 自己扩产的微调收益（[HSSD v3](https://arxiv.org/abs/2306.11290) 表 6） | 122 扩到 10,000 后，微调成功率 / SPL 从 48.48 / 22.79 变 48.32 / 21.80 | 82 倍扩张零增益甚至退化 |
| 本项目 Blender 槽位表算术（[记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/13_scaling_tasks.md) §1.3.5） | 组合空间 7.0e8，渲染后能被 Verifier 分开的等价类约 1.6 万 | 折损 4.4 万倍 |

数据解读：组合空间与有效多样性有干净的定义差别，就是 Hill number 的 q=0 与 q=1（[Cousins of the Vendi Score](https://arxiv.org/abs/2310.12952)），后者即 [Vendi Score](https://arxiv.org/abs/2210.02410)。前者只数有多少种取值组合，后者按实际分布加权，等价于「有效类别数」。本项目槽位表里最极端的一个槽位是灯泡功率：采样空间有 19 档，而在 Workbench 渲染下 Verifier 一档也分不出来，有效档数是 0（[记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/13_scaling_tasks.md) §1.3.5）。这类「采样空间里有、渲染后看不见」的槽位必须禁止进入场景规格，否则它直接制造上一节那种不可解任务。4.4 万倍的折损同时给出一个工程结论：单模板做不到十万，十万量级必须靠模板数与跨模板组合，而跨模板组合的价值在于它造出的空间关系不在任何单模板的槽位域里。

度量这件事本身有个陷阱：不要用通用视觉嵌入做多样性或去重判据。[DataComp](https://arxiv.org/abs/2304.14108) 实测，copy-detection 专用描述子在精确率 0.9 时召回 0.8，而 CLIP ViT-B/32 在同样精确率下召回只有 0.02。Density 与 Coverage 这一代指标的[原作者](https://arxiv.org/abs/2002.09797v1)也给了同向结论：在远离 ImageNet 统计的域上，随机初始化的 64 维嵌入比预训练特征更合理——MNIST 上 Coverage 从 0.108 升到 0.714，音频域从 0.020 升到 0.653（v1 表 1）。程序化 3D 场景离自然图像分布很远，预训练视觉特征会把一切压成一团。这与 Verifier 一侧「别拿嵌入相似度当质量闸」是同一条纪律的两个面。可用的替代是探针已经产出的几何标量：mesh 数、顶点数分位、包围盒体积比、颜色多重集直方图、连通块数、开放边界边数、层级深度，拼成二三十维的低维特征，去重与多样性验收共用一组。

在讨论怎么分桶之前，先看一下自动生成的任务**实际上**是什么难度分布。先看一个跨模型汇总的版本（10 道题，每道题汇总 23 到 32 次首轮尝试，跨 4 个模型、两种问题描述，[实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §9）——注意这个口径后面会被推翻：

核心发现：单处破坏型任务的难度分布是双峰的，中间是空的。

| 通过率 | 任务数 |
|---|---|
| 0 到 0.1 | 2 |
| 0.1 到 0.3 | 2 |
| 0.3 到 0.7 | **0** |
| 0.7 到 0.9 | 2 |
| 0.9 到 1.0 | 4 |

来源：[本项目实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §9。

数据解读：十道题的通过率依次是 0、0.04、0.26、0.27、0.73、0.77、0.91、0.93、1.0、1.0。模型要么会修，要么完全不会，中间带是空的。这对课程规划有两个直接后果。第一，剔除全对与全错之后还剩七成，这个数看着健康；但如果按常见的 0.3 到 0.7 收紧，**一道题都留不下**。第二，成本模型里「难度带留存」这个最敏感的外推项，取值完全由带宽决定，不是一个可以拍的常数（逐题数据见[实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §9）。

但上面那个口径对成本模型是错的，而且错的方向固定是乐观。零梯度是按组判的，组内全是**同一个策略**，所以要用的量是单一策略的 pass@k。跨模型汇总会把「强模型会、弱模型不会」混成一个中间通过率，**凭空制造出并不存在的中等难度**。

换成严格的 pass@8（16 道题、单一模型、温度 1.0、每题独立采 8 次，共 128 次，[实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §15，脚本 [passk.py](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/passk.py)）：

核心发现：13 道题是全有或全无，0.3 到 0.7 带内一道都没有（[实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §15）。

| 通过次数 | 任务数 |
|---|---|
| 0/8 | 5 |
| 1/8 | 2 |
| 2/8 到 6/8 | 1 |
| 7/8 | 0 |
| 8/8 | 8 |

来源：[本项目实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §15，脚本 [passk.py](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/passk.py)。

数据解读：剔除全对与全错后只剩 3/16 = 19%，Wilson 95% 区间是 6.6% 到 43.0%（[实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §15；区间本轮按 Wilson 公式复算一致）。**即便取上界 43%，也仍低于成本模型假设的 60%**——这个假设站不住不是因为样本少，是方向就错了。两种口径差约 3.7 倍（70% 对 19%），所以估 RL 的零梯度比例只能用**将要训的那个策略自己**的 pass@k，不能用跨模型汇总。

根因在任务的造法：只改一处的破坏，要么模型看出来了就改对，要么没看出来就全错，不存在「部分做对」的中间态。要拿到中间难度，得换造法——多处缺陷叠加、或者从零构建而不是修复。这一条在规划十万任务之前就得定下来，因为它决定的是任务形态，不是筛选参数。

需要打的折扣：这十道题的样本是跨模型汇总的，混进了模型强弱；真正的 pass@k 要逐模型算，而每个模型每题只有 7 到 8 次，不够。但「中间带是空的」这个形状在逐模型的数据里同样成立（[实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §9 的折扣说明）。

分桶本身还有一个数学事实：硬边界的桶做不到。

| 真实通过率 | n=4 | n=8 | n=16 | n=32 | n=64 |
|---|---|---|---|---|---|
| 0.10 | 5.2% | 3.8% | 1.7% | 0.1% | 0.0% |
| 0.25 | 26.2% | 32.1% | 37.0% | 26.3% | 15.6% |
| 0.35 | 68.9% | 45.3% | 29.1% | 26.8% | 22.5% |
| 0.50 | 62.5% | 28.9% | 7.7% | 2.0% | 0.2% |
| 0.75 | 26.2% | 32.1% | 37.0% | 26.3% | 15.6% |
| 0.90 | 5.2% | 3.8% | 1.7% | 0.1% | 0.0% |

数据解读：表里是三档桶（易、中、难按 0.3 与 0.7 切）的误分率，本项目精确枚举（[记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/13_scaling_tasks.md) §2.1 表 C）。桶中心和桶外都能分准，桶边界附近分不准：真实通过率 0.35 时，n=8 的误分率 45.3%，n=64 仍有 22.5%，而且几乎不随采样次数下降。原因很直接——真值恰在边界上时本来就是 50 比 50，这部分方差不可能靠加采样消除。公开对照印证同一结论：[难度标签可靠性研究](https://arxiv.org/abs/2609.40115)实测 n=16 的难度集合在两次独立构建之间的 Jaccard 复现性只有 0.727，要到 0.90 需要 242 次采样（外推）。所以难度标定只做粗闸，两段式先 n=2 筛掉全对全错、存活者补到 n=8，之后用软权重而不是硬桶。

课程学习里真正值钱的是双边过滤。[DAPO](https://arxiv.org/abs/2503.14476) 的动态采样在累加消融路径上值 8 分（表 1，42 到 50），是单个改动里最大的一项；唯一做了完整阈值扫描的工作（[Online Difficulty Filtering](https://arxiv.org/abs/2504.03380) 表 1）给出更细的拆解：只剔除全对全错值 1.0 个点（26.3 到 27.3），再把保留区间收紧到通过率 0.3 到 0.7 多拿 2.8 个点（27.3 到 30.1），收到 0.4 到 0.6 回落到 29.9。而只切一边的五个设置（23.8 到 25.9）全部低于不过滤的 26.3；训练前一次性离线筛题（用外部模型或初始模型当难度代理）只到 26.3 到 28.4，低于在线双边过滤的 30.1。还有一个容易自相矛盾的配置：标准差归一化会给几乎全对或几乎全错的题加权（[Dr. GRPO](https://arxiv.org/abs/2503.20783)），方向与动态采样正好相反，两者同时开而不自觉，等于一边筛掉一边加权。

最后一条纪律是把「难」和「坏」分开，而且不能靠人工标注。人判「这题欠规约吗」的 Krippendorff α 只有 0.24（[SPICE](https://arxiv.org/abs/2507.09108) 重算 OpenAI 公开的 SWE-bench Verified 标注），而判「这题多难」是 Fleiss kappa 0.78（[SWE-bench Multimodal](https://arxiv.org/abs/2410.03859) 的难度标注），低了一个量级。可用的替代是响应模式统计：用难度标定已经采出的 rollout 算 item-total 相关，低或负的相关说明单维假设被违反、该题可疑；[实测](https://arxiv.org/abs/2511.16842)在九个 benchmark 上送审前 50 题的精确率最高 84%，1,000 题跑一分钟，而且复用现成 rollout，零额外采样。本项目自己撞过这条线的另一面：桌子那批任务里两道没过的题，查下来不是题难，是 Verifier 查了题干没给的字段（[实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §5）；Blender 留出集 7 个里也有 1 个同因（[Blender 记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/10_blender_tasks.md) §3.3）。单看通过率会把它们判成「超难题」留在池里，持续注入噪声。

<a class="anchor" id="tk-9"></a>

## 9 The Bottleneck Is Not Compute

真实素材挖掘的端到端留存率是千分之几到百分之几，这个量级是文献共识，不是悲观假设。

| 管线 | 起点 | 端到端留存 | 产出 |
|---|---|---|---|
| [SWE-bench](https://arxiv.org/abs/2310.06770)（表 10） | 93,139 个 PR | 2.46% | 2,294 |
| [SWE-rebench](https://arxiv.org/abs/2505.20411) | 约 45 万个下载的 PR | 4.74% | 21,336 |
| [SWE-Gym](https://arxiv.org/abs/2412.21139) | 64,689 条候选 | 3.77% | 2,438 |
| [Design2Code](https://arxiv.org/abs/2403.03163) | 127.9k 个网页 | 0.38% | 484 |
| ShaderMatch（[Shadereval](https://huggingface.co/datasets/Vipitis/Shadereval-inputs)） | 20.2 万个未过滤函数 | 0.23% | 467 |
| [SWE-smith](https://arxiv.org/abs/2504.21798)（合成变异） | 100,074 个 bug 候选 | 50.1% | 50,137 |
| [本项目自动造题准入](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) | 26 条破坏提案 | 88% 到 96% | 25 |

数据解读：瓶颈不在筛选质量，在「能不能跑起来」。SWE-rebench 自己点名安装与执行验证这一步只有约 14% 通过，只有 31% 的仓库能装成至少一个任务。按本项目口径把这条漏斗算到 three.js 上（[记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/13_scaling_tasks.md) §4.2.5）：2,401 个仓库（GitHub 搜索 `topic:threejs stars:>10` 实测），抽自包含页面约 20%，无头浏览器能跑起来并渲出至少一个 mesh 约 60%，场景捕获成功约 95%，冻结时钟后两次渲染逐字节一致约 70%，自动造题加准入约 90%，去重与难度带约 45%，端到端约 3.2%。按每仓库平均挖出 3 个可用页面估，只能出约 230 个任务——三位数，不是五位数。除仓库数与准入率外，这条漏斗的各步留存都是估计值。

所以真实素材与合成的配比不是选择题。真实素材客观上只能占千分之几的条数，合成必然在 95% 以上。collapse 一线的理论对这件事不直接适用：最悲观的结论（[Strong Model Collapse](https://arxiv.org/abs/2410.04840)）说合成占 1% 即可触发退化，但前提是替换式自噬迭代且不做筛选；有界误差的那篇（[Is Model Collapse Inevitable?](https://arxiv.org/abs/2404.01413)）给出的决定性变量是协议而非比例——累加而不是替换，加上 Verifier 筛选（[Beyond Model Collapse](https://arxiv.org/abs/2406.07515)），两条满足时工程上约 30% 的合成占比仍不掉点（[Nemotron-CC](https://arxiv.org/abs/2412.02595)：全量 6.3T token 里 1.9T 为合成，MMLU 与 DCLM 持平）。本项目这两条天然满足：标签来自程序化信号而不是模型，模型只提供破坏提案和题干措辞；准入测试本身就是 Verifier 筛选。所以真实素材的 KPI 应该改成「在有效多样性口径下贡献至少 20%」，而不是条数占比；达不到就说明反推需求做烂了，只是把真实素材重新表述成了模板本来就能出的东西。

成本模型是推算，假设逐条写明（[记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/13_scaling_tasks.md) §5.2）。准入三条取 0.97 / 0.90 / 0.95，去重 0.85，可解性闸 0.88——这五步合计留存 62%。最后一项「难度带留存」原先按 0.60 外推，**本项目实测把它打到了 0.19**（见上，[实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §15）。

| 项 | 按 0.60 外推 | 按实测 0.19 |
|---|---|---|
| 漏斗总留存 | 37.2% | 11.8% |
| 造 10 万任务需要的候选 | 26.9 万 | **84.8 万** |
| 探针调用 | 约 160 万次 | 约 500 万次 |

数据解读：按单处破坏这一种造法，规模化成本要乘以 3.2（37.2% / 11.8%，[实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §15，原口径见 [13 规模化](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/13_scaling_tasks.md) §5.2），而多花的那部分全部花在生成最后会被丢掉的任务上。下面的资源表仍按原先的 26.9 万口径列，**要按实测口径读就把 CPU、存储、LLM 调用三行各乘 3.2**；人工那一行不乘，因为抽检量是按最终任务数定的。

| 项 | three.js 线 | Blender 线 | 口径 |
|---|---|---|---|
| CPU | 1,480 核时 | 1,064 核时 | 按复用浏览器池 14.3 任务每秒（[Harness 实测](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/06_harness.md) §4.1）、Blender 单任务 1.21 秒墙钟（[Blender 记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/10_blender_tasks.md) §3.5 外推）外推 |
| 折算整机 | 31 台机小时 | 22 台机小时 | 48 核机器 |
| 存储 | 约 20 GB | 约 100 GB | 单任务 0.2 MB 对 1 MB |
| LLM 调用 | 约 95 万次 | 约 95 万次 | 优化后；优化前 121 万次里难度标定占 65% |
| 人工 | 约 360 人时 | 约 360 人时 | 抽检 240、一致性标定 50、欠规格仲裁 67 |

来源：[本项目成本模型](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/13_scaling_tasks.md) §5.3 到 §5.8。

数据解读：两条线合计约 2,500 核时，一台 48 核机器两天跑完，算力不构成瓶颈。瓶颈是 LLM 调用和人工。LLM 调用里 65% 花在难度标定上，所以唯一值得反复优化的旋钮就是「难度要采样多少次」：一次性 n=8 要 133 万次标定调用，两段式先 n=2 筛掉 55% 再补 6 次只要 78 万次，LLM 总调用从 176 万降到 121 万，省 31%。还有一个反直觉的结论：Blender 比 three.js 便宜。Workbench 稳态渲染 0.065 秒一个视角（[Blender 记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/10_blender_tasks.md) §3.5），比软件光栅下的 WebGL 快；three.js 贵在浏览器本身。代价是扩产阶段只能渲 Workbench 剪影加算几何，不能渲 Cycles。

成本模型里最敏感的一项就是这个难度带留存，而本项目实测 0.19 与公开实测方向一致，都说明 0.60 偏乐观。[Skywork-OR1](https://arxiv.org/abs/2505.22312) 实测开训前就有 54%（7B）到 63%（32B）的数学题是零梯度（全对或全错），[GRESO](https://arxiv.org/abs/2506.02177) 实测训练后期有效 prompt 比例会掉到约 20%，而理论上界在通过率服从均匀分布时 G=16 只该丢 11.8%（[本项目推算](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/13_scaling_tasks.md) §2.2.2）——这个差距正是「通过率极度堆在两端」的量化体现。如果实际留存是 0.30，候选数从 26.9 万翻到 53.8 万，LLM 调用从 95 万翻到 190 万。本项目已在 16 道题上跑过一次单模型 pass@8（128 次调用，[实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §15）；把样本扩到现有全部 47 个任务只需 376 次调用、几十分钟，是收窄区间最便宜的办法。

去重的单位是场景图，不是代码语法树。主流代码数据集普遍不用语法树等价做去重——[The Stack](https://arxiv.org/abs/2211.15533)、[StarCoder](https://arxiv.org/abs/2305.06161) 等都是 token 或字符 n-gram 的 MinHash，本项目检索到的唯一结构哈希是 LLVM 中间表示那一家（[ComPile](https://arxiv.org/abs/2309.15432)，[检索记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/13_scaling_tasks.md) §3.1.1）。本项目的实测给出了更直接的理由：换一条实现路径写出世界几何逐点相同的场景，几何信号全部放行（分部件 F-score 0.9993），只有按代码比的判据会误杀（[Blender 记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/10_blender_tasks.md) §3.2）。所以指纹分三级：场景图规范化哈希抓完全同构，低维几何特征的近邻抓「同模板换种子」，而最该自建的是第三级——断言集合的 Jaccard，它抓的是「考的点重复」。程序化生成最容易塌缩的不是场景长得一样，而是十万个任务里有三万个都在考某个部件缺失。

去重还会过头。[FineWeb](https://arxiv.org/abs/2406.17557) 实测（§3.4）对 96 个快照做全局去重后只剩 4T token，下游相比不去重几乎没有提升，最老的快照被删掉 90%；逐快照独立去重保留 20T，才与 RefinedWeb 持平并逐步受益。收益来自删掉跨全部快照的巨型重复簇，对只有几十个副本的小簇继续去重反而有害。所以只打巨型同构簇加 benchmark 去污，不要把去重率当 KPI。去污这一路只有收益没有损失，但要注意 n-gram 挡不住改写：[LMSYS 实测](https://arxiv.org/abs/2311.04850) 10-gram 对改写样本的 F1 是 0，而嵌入召回加 LLM 逐对判定能到 0.94 以上。场景图哈希在这里是结构化产物相对文本数据集的优势——它比的是产物几何，改写代码、换语言、换实现路径都不影响；而如果几何变了，那就不是同一道题。

分阶段的骨架是五步（[记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/13_scaling_tasks.md) §6）：S0 校准，3 到 10 个场景、200 个任务，只验阈值在没见过的结构类别上迁移得住；S1 模板化，8 个槽位模板、2,000 个任务，核心交付物不是任务而是 8 张过了可见性审计的槽位表；S2 多样性扩张，40 个模板、2 万个任务，第一次上两段式难度标定与三路去重；S3 真实素材注入，到 5 万，许可与污染都在这一阶段出问题；S4 满产，10 万以上，加分布漂移监控与训练侧回归。三条原则贯穿全程：每个阶段的验收必须包含一条留出指标且阈值进入前定死；规模每翻十倍就重新校准一次 Verifier，因为盲区是被具体 case 逼出来的；每个阶段只放大一个变量，否则出问题分不清是谁的锅。一条红线：任何阶段都不许用正在调阈值的那个集合做验收。本项目犯过一次——第一组 13 个变异既当调参集又当验收集，颜色容差是看到误杀后才加的（[实验记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) §2.4）。扩到十万量级时这个错误的代价是整个数据集在一个看不见的方向上过拟合，而且因为指标都很漂亮，不会有人发现。

## 参考文献

1. [SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://arxiv.org/abs/2310.06770) — Jimenez 等，Princeton，2023-10-10
2. [mrdoob/three.js：examples/screenshots 与 test/e2e](https://github.com/mrdoob/three.js/tree/dev/examples/screenshots) — three.js 项目，GitHub 仓库（2026-10-15 读取）
3. [BabylonJS/Babylon.js：visualization tests](https://github.com/BabylonJS/Babylon.js/tree/master/packages/tools/tests/test/visualization) — Babylon.js 项目，GitHub 仓库（2026-10-15 读取）
4. [blender/blender：tests/files/render（GitHub 镜像）](https://github.com/blender/blender/tree/main/tests/files/render) — Blender Foundation，GitHub 仓库（2026-10-15 读取）
5. [maplibre/maplibre-gl-js：test/integration/render](https://github.com/maplibre/maplibre-gl-js/tree/main/test/integration/render) — MapLibre，GitHub 仓库（2026-10-15 读取）
6. [pixijs/pixijs：tests/visual](https://github.com/pixijs/pixijs/tree/dev/tests/visual) — PixiJS，GitHub 仓库（2026-10-15 读取）
7. [primer/react：.playwright/snapshots](https://github.com/primer/react/tree/main/.playwright/snapshots) — GitHub Primer，GitHub 仓库（2026-10-15 读取）
8. [chartjs/Chart.js：test/fixtures](https://github.com/chartjs/Chart.js/tree/master/test/fixtures) — Chart.js，GitHub 仓库（2026-10-15 读取）
9. [processing/p5.js：test/unit/visual](https://github.com/processing/p5.js/tree/main/test/unit/visual) — Processing Foundation，GitHub 仓库（2026-10-15 读取）
10. [openlayers/openlayers：test/rendering/cases](https://github.com/openlayers/openlayers/tree/main/test/rendering/cases) — OpenLayers，GitHub 仓库（2026-10-15 读取）
11. [visgl/deck.gl：test/render/golden-images](https://github.com/visgl/deck.gl/tree/master/test/render/golden-images) — vis.gl，GitHub 仓库（2026-10-15 读取）
12. [plotly/plotly.js：test/image/baselines](https://github.com/plotly/plotly.js/tree/master/test/image/baselines) — Plotly，GitHub 仓库（2026-10-15 读取）
13. [SWE-bench Multimodal: Do AI Systems Generalize to Visual Software Domains?](https://arxiv.org/abs/2410.03859) — Yang 等，Princeton / Stanford，2024-10-04
14. [Infinite Photorealistic Worlds using Procedural Generation（Infinigen）](https://arxiv.org/abs/2306.09310) — Raistrick 等，Princeton，2023-06-15
15. [princeton-vl/infinigen](https://github.com/princeton-vl/infinigen) — Princeton Vision & Learning Lab，GitHub 仓库
16. [10,000,000 Pens](https://blog.codepen.io/2016/11/25/10000000/) — CodePen 官方博客，2016-11-25
17. [Licensing](https://blog.codepen.io/documentation/licensing/) — CodePen 官方文档
18. [js13kGames sitemap](https://js13kgames.com/sitemap.xml) — js13kGames（2026-10-15 读取）
19. [Shadertoy](https://www.shadertoy.com/) 与 [Terms](https://www.shadertoy.com/terms) — Shadertoy 官方站（CLI 403，未能实测）
20. [Procedural Image Programs for Representation Learning（shaders21k）](https://arxiv.org/abs/2211.16412) — Baradad 等，MIT，2022-11-29
21. [Stack Exchange API：Blender 站 python / scripting 标签计数](https://api.stackexchange.com/2.3/tags/python;scripting/info?site=blender) — Stack Exchange（2026-10-15 读取）
22. [Stack Exchange restricts data access for generative AI and the rest of the world](https://heise.de/-9823083) — heise online，2024-08-03
23. [Figma robots.txt](https://www.figma.com/robots.txt) — Figma（2026-10-15 读取）
24. [Frontend Mentor FAQs](https://www.frontendmentor.io/faqs) — Frontend Mentor（2026-10-15 读取）
25. [Chromatic](https://www.chromatic.com/) — Chromatic 产品页
26. [Percy](https://percy.io/) — BrowserStack Percy 产品页
27. [WebCode2M: A Real-World Dataset for Code Generation from Webpage Designs](https://arxiv.org/abs/2404.06369) — Gui 等，2024-04-09
28. [xcodemind/webcode2m](https://huggingface.co/datasets/xcodemind/webcode2m) 与 [webcode2m_purified](https://huggingface.co/datasets/xcodemind/webcode2m_purified) — WebCode2M 作者，HuggingFace 数据集
29. [Unlocking the conversion of Web Screenshots into HTML Code with the WebSight Dataset](https://arxiv.org/abs/2403.09029) — Laurençon 等，Hugging Face，2024-03-14
30. [Design2Code: Benchmarking Multimodal Code Generation for Automated Front-End Engineering](https://arxiv.org/abs/2403.03163) — Si 等，Stanford，2024-03-05
31. [HuggingFaceM4/WebSight](https://huggingface.co/datasets/HuggingFaceM4/WebSight) — Hugging Face，HuggingFace 数据集
32. [Objaverse-XL: A Universe of 10M+ 3D Objects](https://arxiv.org/abs/2307.05663) — Deitke 等，AI2，2023-07-11
33. [allenai/objaverse-xl](https://github.com/allenai/objaverse-xl) — AI2，GitHub 仓库
34. [CAD-Coder: Text-to-CAD Generation with Chain-of-Thought and Geometric Reward](https://arxiv.org/abs/2505.19713) — Guan 等，2025-05-26
35. [Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains](https://arxiv.org/abs/2507.17746) — Gunjal 等，Scale AI，2025-07-23
36. [WorldCoder-Bench: Benchmarking Physically Grounded 3D World Synthesis](https://arxiv.org/abs/2606.01869) — Lu 等，2026-06-01
37. [GameDevBench: Evaluating Agentic Capabilities Through Game Development](https://arxiv.org/abs/2602.11103) — Chi 等，2026-02-11
38. [CodeContests+: High-Quality Test Case Generation for Competitive Programming](https://arxiv.org/abs/2506.05817) — Wang 等，2025-06-06
39. [R2E-Gym: Procedural Environments and Hybrid Verifiers for Scaling Open-Weights SWE Agents](https://arxiv.org/abs/2504.07164) — Jain 等，UC Berkeley，2025-04-09
40. [DAPO: An Open-Source LLM Reinforcement Learning System at Scale](https://arxiv.org/abs/2503.14476) — Yu 等，ByteDance Seed / 清华 AIR，2025-03-18
41. [SWE-rebench: An Automated Pipeline for Task Collection and Decontaminated Evaluation of Software Engineering Agents](https://arxiv.org/abs/2505.20411) — Badertdinov 等，Nebius，2025-05-26
42. [ProcTHOR: Large-Scale Embodied AI Using Procedural Generation](https://arxiv.org/abs/2206.06994) — Deitke 等，AI2，2022-06-14
43. [Habitat Synthetic Scenes Dataset (HSSD-200)](https://arxiv.org/abs/2306.11290) — Khanna 等，Meta / Simon Fraser，2023-06-20
44. [Cousins Of The Vendi Score: A Family Of Similarity-Based Diversity Metrics](https://arxiv.org/abs/2310.12952) — Pasarkar、Dieng，Princeton，2023-10-19
45. [The Vendi Score: A Diversity Evaluation Metric for Machine Learning](https://arxiv.org/abs/2210.02410) — Friedman、Dieng，Princeton，2022-10-05
46. [DataComp: In search of the next generation of multimodal datasets](https://arxiv.org/abs/2304.14108) — Gadre 等，2023-04-27
47. [Reliable Fidelity and Diversity Metrics for Generative Models](https://arxiv.org/abs/2002.09797v1) — Naeem 等，2020-02-23
48. [Unlearnable, or Unmeasured? On the Reliability of Difficulty Labels in RLVR](https://arxiv.org/abs/2609.40115) — Chakma 等，2026-09-30
49. [Online Difficulty Filtering for Reasoning Oriented Reinforcement Learning](https://arxiv.org/abs/2504.03380) — Bae 等，2025-04-04
50. [Understanding R1-Zero-Like Training: A Critical Perspective（Dr. GRPO）](https://arxiv.org/abs/2503.20783) — Liu 等，Sea AI Lab，2025-03-26
51. [SPICE: An Automated SWE-Bench Labeling Pipeline for Issue Clarity, Test Coverage, and Effort Estimation](https://arxiv.org/abs/2507.09108) — Oliva 等，2025-07-12
52. [Fantastic Bugs and Where to Find Them in AI Benchmarks](https://arxiv.org/abs/2511.16842) — Truong 等，Stanford，2025-11-20
53. [Training Software Engineering Agents and Verifiers with SWE-Gym](https://arxiv.org/abs/2412.21139) — Pan 等，UC Berkeley，2024-12-30
54. [Vipitis/Shadereval-inputs](https://huggingface.co/datasets/Vipitis/Shadereval-inputs) — Vipitis，HuggingFace 数据集
55. [SWE-smith: Scaling Data for Software Engineering Agents](https://arxiv.org/abs/2504.21798) — Yang 等，Stanford，2025-04-30
56. [Strong Model Collapse](https://arxiv.org/abs/2410.04840) — Dohmatob 等，Meta，2024-10-07
57. [Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accumulating Real and Synthetic Data](https://arxiv.org/abs/2404.01413) — Gerstgrasser 等，2024-04-01
58. [Beyond Model Collapse: Scaling Up with Synthesized Data Requires Verification](https://arxiv.org/abs/2406.07515) — Feng 等，NYU / Meta，2024-06-11
59. [Nemotron-CC: Transforming Common Crawl into a Refined Long-Horizon Pretraining Dataset](https://arxiv.org/abs/2412.02595) — Su 等，NVIDIA，2024-12-03
60. [Skywork Open Reasoner 1 Technical Report](https://arxiv.org/abs/2505.22312) — He 等，Skywork AI，2025-05-28
61. [Act Only When It Pays: Efficient Reinforcement Learning for LLM Reasoning via Selective Rollouts（GRESO）](https://arxiv.org/abs/2506.02177) — Zheng 等，2025-06-02
62. [The Stack: 3 TB of permissively licensed source code](https://arxiv.org/abs/2211.15533) — Kocetkov 等，BigCode，2022-11-20
63. [StarCoder: may the source be with you!](https://arxiv.org/abs/2305.06161) — Li 等，BigCode，2023-05-09
64. [ComPile: A Large IR Dataset from Production Sources](https://arxiv.org/abs/2309.15432) — Grossman 等，2023-09-27
65. [The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale](https://arxiv.org/abs/2406.17557) — Penedo 等，Hugging Face，2024-06-25
66. [Rethinking Benchmark and Contamination for Language Models with Rephrased Samples](https://arxiv.org/abs/2311.04850) — Yang 等，LMSYS，2023-11-08

本项目内部记录（不计入上表）：[02 任务来源](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/02_task_sources.md)、[06 Harness](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/06_harness.md)、[09 预训练数据](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/09_pretrain_data.md)、[10 Blender 任务](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/10_blender_tasks.md)、[13 规模化](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/13_scaling_tasks.md)、[90 本地实验](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)、[92 数字复核](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/92_number_audit.md)，以及脚本 [gen_tasks.py](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/gen_tasks.py)、[mutate.py](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/mutate.py)、[ablate.py](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/ablate.py)、[passk.py](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/passk.py)。

