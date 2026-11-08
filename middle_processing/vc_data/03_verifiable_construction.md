# 03 把「描述 + 参考代码」变成可验证任务：构造范式与数据质量

> 课题：visual coding（Web / three.js / Blender）RL 任务怎么构造成「验证效果」而不是「模仿参考代码」；任务数据质量怎么量化。
> 与 `webdev-data/WebDev 数据构造技术方案.html` 的分工：第四章（四条任务来源、query 过滤、需求编译为 rubric）和第七章（V0–V5 分层验证、视觉奖励拆分、聚合、防 hack、校准）已覆盖 Web 侧，本文不重复，只写
> - SWE 系自动造任务方法迁移到视觉任务的具体形态（视觉版 F2P / P2P）
> - 3D（three.js / Blender）特有的观察接口、断言和变异算子
> - 参考代码的定位，以及可计算的数据质量指标
>
> 日期按 arXiv ID 推（2504.xxxxx = 2025-04）。数字均带出处；标「推导」的是本文基于文献的设计，不是已发表做法。

---

## 0. 结论先行

1. **验证对象是状态，不是代码**
   - 任务统一写成 `(初态 S0, 需求 Q, 观察接口 I, 隐藏断言 A, 参考解 R)`；reward 只看任意实现能否把 S0 推到满足 A 的状态，不看它和 R 的代码像不像
   - 证据：多份 CadQuery 脚本可得到几何等价的模型，SFT 难以覆盖，CAD-Coder 因此改用 Chamfer 距离做 GRPO 奖励（2505.19713）；RaR 直接拿参考答案做 Likert 对照只有 31.7%，用参考答案生成 rubric 再打分为 35.9%（2507.17746 表 1）
2. **3D 的关键是「打穿 canvas」**
   - three.js 画在 `<canvas>` 里，DOM 打分与隐藏状态正确性几乎不相关（Kendall τb = −0.02，1,434 对），8 步 agent 检查仍放过 45.6% 的严重缺陷（WorldCoder-Bench 2606.01869）
   - 必须有运行时状态接口：模型侧暴露（`window.__3D_STATE__`）或 harness 侧注入（hook renderer 拿 scene graph，推导）
3. **SWE 系的 F2P / P2P 可以原样迁移**，只是 test 换成「状态断言 + 渲染断言」
   - F2P：在 S0 上失败、在 R 上通过的断言（证明任务非平凡、可解）
   - P2P：在 S0 和 R 上都通过的断言（证明没有改坏无关部分）
4. **断言集本身要过变异测试**：对 R 注入缺陷，断言必须杀死变异体才准入（WorldCoder StateProbe 的 mutation-hardened contracts；WorldBench 用「按构造删除特征」测出纯读代码的 judge 对 5 个被删特征中 4 个给满分，2610.10622）
5. **参考代码的五个用途**：证明可解、生成断言与 rubric、作为变异母本、作为 verifier 的 sanity check、SFT 冷启动；它不应作为 RL 的相似度目标，且应被视为「下界」而非「标准答案」
6. **数据质量用一组可计算指标管住**：可解率、非平凡率、判别力（对 R 的 TPR、对变异体的杀死率）、难度分布（pass@k 落在 0 与 1 之间）、稳定性（重复验证 flaky 率）、多样性、污染率、规格对齐度

---

## 1. 统一抽象：一个可验证 visual coding 任务长什么样

```
Task
├── S0  初态：空模板 / 已有工程 / .blend 起始场景 / three.js 起始页面
├── Q   需求：文字 + 可选参考图 / 录屏 / 草图（只描述可观察效果，不泄露实现）
├── I   观察接口（模型可见）：DOM id、window.__3D_STATE__ schema、必须保留的对象名
├── A   断言集（模型不可见）
│   ├── F2P：S0 失败、R 通过
│   ├── P2P：S0 通过、R 通过
│   └── 每条断言带 观察层 / 容差 / 权重
├── R   参考解（只用于造任务和校验 verifier，不进 reward 的相似度项）
└── M   变异体集合：由 R 注入缺陷得到，用于校准 A
```

观察层从弱到强：

| 层 | Web | three.js | Blender | 能看到 | 看不到 |
|---|---|---|---|---|---|
| 像素 | 截图、录屏 | canvas 截图、多视角 | 多视角渲染 | 外观、构图 | 屏外对象、隐藏状态、物理量 |
| 结构 | DOM / a11y 树 / computed style | 外围 DOM（按钮、HUD） | — | 文本、布局、控件 | canvas 内一切 |
| 运行时状态 | JS 全局状态、network | scene graph、`window.__3D_STATE__`、相机/灯光参数 | `bpy.data`：mesh、modifier、材质节点、渲染设置 | 坐标、速度、拓扑、参数 | 美观度、风格 |
| 几何 | — | 导出 glTF 后算 | 导出 mesh 算 Chamfer / IoU / Betti 数 | 形状误差、拓扑 | 语义是否「像」 |

- 外观类需求落在像素层，用 VLM 或感知相似度；机制类需求（物理、交互、参数）必须落在状态层
- 同一任务的断言要按需求类型分到不同层，而不是全部交给截图 + VLM

---

## 2. 八种构造范式

### 2.1 SWE 借鉴：F2P / P2P 与自动造任务

**原理**
- SWE-bench：从 PR 抽 issue + gold patch + test patch，只保留至少有一个 fail-to-pass 测试的实例；排除测试里调用了 solution 新建函数/类的实例（命名任意，无法从 issue 推出）；约 90,000 个 PR 筛到 2,294 个实例（2310.06770 §2）
- 后续工作把「依赖真实 PR」这一瓶颈拆掉：

| 工作 | 造任务方式 | 规模 / 结果 | 对视觉任务的启示 |
|---|---|---|---|
| [SWE-bench Multimodal](https://arxiv.org/abs/2410.03859)（2024-10） | 5,000+ star、500+ PR 的 JS 仓库，人工选 17 个带视觉面的库；只留 issue 或测试里带图片/视频的 PR；135k PR → 1,478 候选 → 617 实例 | 人工核验 83.5% 的实例图像对解题必要；69 个实例用像素级截图测试判功能 | 视觉 F2P 的雏形就是「渲染 + 逐像素对比」；Docker 里要补 Node.js + Chrome |
| [SWE-Gym](https://arxiv.org/abs/2412.21139)（2024-12） | 11 个 Python 仓库的真实 PR，预装依赖 + 专家核验测试 | 2,438 实例；同时训练 verifier | 人工搭环境贵，规模上不去 |
| [R2E-Gym](https://arxiv.org/abs/2504.07164)（2025-04） | SWE-Gen：直接从 commit 生成测试 + 反向翻译出 issue，不依赖人写 issue | 8.1K+ 任务；32B 模型 34.4%，hybrid verifier 到 51.0% | 基于测试的 verifier 区分度低：多数题目里能区分正误 patch 的测试不到 20%（§4.2） |
| [SWE-smith](https://arxiv.org/abs/2504.21798)（2025-04） | 在能跑的仓库里**合成 bug**：LM Modify / LM Rewrite / AST 程序化变换 / PR Mirror（反做 PR）/ 组合 bug；保留能打破 ≥1 个已有测试的候选 | 128 仓库 50,137 实例；各策略产出率 33.8%–96.9%，单条成本 0–5.53 美分（表 1） | 「先有正确产物，再破坏」可无限造题；但 issue 文本要另生成 |
| [SWE-rebench](https://arxiv.org/abs/2505.20411)（2025-05） | 全自动从 GitHub Archive 挖任务，自动配安装脚本，执行验证；用 SWE-bench Verified 人工标注微调 Qwen2.5-72B 打 Issue Clarity / Task Complexity / Test Patch Correctness 三个质量标签 | 3,468 仓库 21,336 任务；按时间持续更新做去污染榜单 | 质量标签可以学出来，用作自动过滤器 |
| [BugPilot](https://arxiv.org/abs/2510.19898)（2025-10） | 让 SWE agent **加新功能**，顺带把已有测试弄挂的状态即为一个 bug（FeatAdd）；对比故意注入（BugInstruct、SWE-smith） | 1.2k 条 FeatAdd 比 3k 条其他 bug 的 SFT 高 2%；RL 32B 到 52.4%，全量 54.6% | 无意引入的 bug 分布更像真实，比故意注入的训练效率高 |

**视觉版 F2P / P2P 应该长什么样（推导）**

| 栈 | F2P 断言（S0 失败、R 通过） | P2P 断言（S0 与 R 都通过） |
|---|---|---|
| Web | DOM / a11y 断言（元素存在、文本、角色）；computed style 落在容差内；Playwright 动作序列后的状态差分（列表多一项、弹窗出现、URL 变化） | 编辑区域外的截图像素差低于阈值（mask SSIM）；原有 Playwright 用例；console 无新报错；多 viewport 无横向溢出 |
| three.js | scene graph 断言（对象按名字存在、数量、包围盒、材质颜色 ΔE、灯光强度、相机 fov）；`window.__3D_STATE__` 在动作前后的差分（速度、计数器、模式） | 未涉及对象的变换与几何哈希不变；固定种子 + 固定时钟下未涉及区域的多视角渲染不变；帧率 / draw call 不劣化超过阈值 |
| Blender | `bpy` 断言（对象存在、modifier 栈、顶点数区间、流形、材质节点参数、渲染引擎与采样数）；与目标场景的几何距离（Chamfer）低于阈值 | 其他对象的 transform 与 mesh 哈希不变；held-out 视角渲染差低于阈值（BlenderGym 的 evaluation-only 视角） |

- 任务准入三条（照搬 SWE-bench 的逻辑）
  1. F2P 在 S0 上全部失败，否则题目平凡
  2. F2P 与 P2P 在 R 上全部通过，且重复 3 次稳定，否则题目不可解或 verifier 不稳
  3. 不允许断言依赖 R 的实现细节（变量名、类名、函数拆分），对应 SWE-bench 排除「测试调用 solution 新建函数」的规则；需要的锚点必须写进 I 里让模型可见
- 能验证：需求是否被实现、是否改坏无关部分，二值、可复现、可被 GRPO 直接用
- 不能验证：审美、「比参考更好」；断言覆盖不到的需求一律漏检（R2E-Gym 的低区分度问题在视觉任务上会更严重）

---

### 2.2 逆向构造：从渲染结果出发

**原理**：先有真实或合成的产物（页面、场景），渲染出图或录屏作为题面，让模型复现；产物本身给出目标状态，不需要人写需求。

| 工作 | 构造 | 规模 | 验证 |
|---|---|---|---|
| [Design2Code](https://arxiv.org/abs/2403.03163)（2024-03） | 爬 C4 验证集网页，CSS 内联、去外链、多媒体换占位；自动过滤到 14k，再人工筛 | 484 页 | Block / Text / Position / Color 匹配 + CLIP |
| [WebSight](https://arxiv.org/abs/2403.09029)（2024-03） | Mistral-7B 生成网站概念 → 代码 LLM 写 Tailwind HTML → 截图 | 2M 对 | 只做 SFT 配对，无 verifier |
| [Sketch2Code](https://arxiv.org/abs/2410.16232)（2024-10） | 723 人里选 21 名标注员，为 Design2Code 的 484 页手绘 731 张草图；一部分页面由 2–3+ 人画以覆盖风格 | 731 张 | 组件 IoU 加权的 layout similarity；多轮反馈 / 提问 |
| [Interaction2Code](https://arxiv.org/abs/2411.03292)（2024-11） | 4 名博士生在真实网页上挑交互，截交互前后两张图做原型；给交互元素打 `id="interact1"` | 127 页、374 个交互 | 评测时 selenium 按 id 定位交互元素，自动操作后截图对比 |
| [BlenderGym](https://arxiv.org/abs/2504.01786)（2025-04） | 手工做 start / goal 场景对，模型改 bpy 脚本把 start 变成 goal；五类：物体摆放、灯光、程序化材质、blend shape、程序化几何 | 245 对 | 材质：photometric loss + CLIP；几何：Chamfer + PL + CLIP；视角分 VLM-input 与 evaluation-only 两组 |
| [3DHarnessBench](https://arxiv.org/abs/2609.06535)（2026-09） | 从 3DCodeBench 的 212 个程序化物体抽 100 个，只给渲染图和 GLB，**原始程序化源码不暴露**；四档访问：单视图 / 多视图 / 主动视角 / Blender MCP 全交互 | 100 物体 | SigLIP-2、DINOv2/v3、Chamfer、Uni3D、Betti 数归一 L1 |

**在 visual coding 上怎么落地（推导）**
- Web：真实页面 → 截图 + 交互录屏为题面；原页面只用来产出断言（DOM 结构、文本、交互前后状态），不用来比代码
- three.js：程序化生成器（随机参数）跑出场景 → 多视角渲染 + 一段交互录屏为题面；生成器参数即真值，直接编译成 scene graph 断言
- Blender：Infinigen 类程序化工厂（[2306.09310](https://arxiv.org/abs/2306.09310)）或 3DCodeBench 的「工厂 → 独立脚本」流水线产出 (prompt, code, mesh) 三元组；题面给渲染图，评测用几何距离 + held-out 视角
- 两个关键设计
  - **held-out 视角**：BlenderGym 把视角分成给模型看的和只用于评测的两组，所有目标对象至少在一个输入视角里出现（附录 S5），防止只对齐看得见的面
  - **交互锚点**：Interaction2Code 的 `id` 约定与 WorldCoder 的 `window.__3D_STATE__` 是同一思路：锚点写进题面，断言藏起来

**能验证 / 不能验证**
- 能：外观与结构的保真度、几何误差；目标状态唯一时可以给连续奖励
- 不能
  - 渲染图看不到的机制（物理、状态机、屏外对象）
  - 「一图多解」：同一截图可由完全不同的 DOM / scene graph 实现，结构类指标（DOM 相似度）会惩罚合法替代实现，只能用于辅助
  - BlenderGym 自己指出的两点：指标不捕捉物理合理性（球卡在篮筐上反而分数更好），不同任务的指标尺度不可比（附录 S4）

---

### 2.3 变异 / 扰动：破坏正确产物，任务是修回去

**原理**：R 是正确状态；对 R 施加变异得到 S0，任务 =「把 S0 修到满足需求」。参考的是**状态**，不是 R 的代码，因此任何能回到正确状态的修法都得分。SWE-smith 是代码层的版本，DesignBench repair 是 Web 层的版本（第四章 D 已覆盖 Web 的缺陷类别）。

**3D 变异算子（推导，参照 WorldCoder 校准用的缺陷类别：stale state update、物理常数被篡改、资源加载坏、事件目标错位、HUD 不一致）**

| 类别 | three.js | Blender | 对应 F2P 断言 |
|---|---|---|---|
| 几何 | 删对象、换 geometry 参数、错 scale | 删 modifier、改 subdivision 级数、翻法线、产生非流形 | 对象存在、bbox、顶点数区间、流形 |
| 空间 | 平移 / 旋转 / 改父子关系 | 改 location / rotation / parent | transform 容差、相对关系（在…上、对齐、间距） |
| 材质 | 改 color / roughness / metalness、换 map | 改 BSDF 节点参数、断开节点连线 | 参数容差、节点连通性、渲染区域色差 |
| 光照与相机 | 改 intensity、删阴影、改 fov | 改灯光能量 / 色温、改相机焦距 | 参数容差、亮度直方图 |
| 动画与交互 | 删 animate 里的状态更新、改时间步长、换事件绑定目标 | 删关键帧、改帧范围 | 动作前后状态差分、指定帧的状态 |
| 渲染设置 | 关 antialias、改 toneMapping | 改引擎、采样数、分辨率 | 设置值断言 |

- 变异体两种用途
  1. 当题目：S0 = 变异体，F2P = 杀死该变异体的断言
  2. 校准 verifier：所有变异体都必须被 A 判失败（见 2.6、3.2）
- 借鉴 BugPilot：与其写规则注入，不如让 agent 在 R 上「加一个功能」，顺带打破已有 P2P 断言的状态就是一个自然缺陷；分布更真实

**能验证 / 不能验证**
- 能：定点修复、局部编辑能力；因果链清楚，断言天然只覆盖变异处
- 不能：从零构建能力；变异分布与真实错误分布不一致时会练偏（BugPilot 的对比正说明这一点）

---

### 2.4 需求 → rubric：把自然语言编译成可检查条目

**原理**：强模型把需求拆成逐条可观察的检查项，judge 逐条判；Web 侧的写法（initial / dynamic / visual 类型、O/A/V 三元组、15–30 项）见第四章 4.3，本节只补三点增量。

| 工作 | 要点 | 数字 |
|---|---|---|
| [Rubrics as Rewards](https://arxiv.org/abs/2507.17746)（2025-07） | 参考答案作为「专家代理」喂给 rubric 生成器；显式加权聚合 vs 交给 judge 隐式聚合 | HealthBench-1k：Reference-Likert 31.7%，无参考生成的 rubric 32.0%，有参考生成的 rubric 35.9%（表 1）；无参考时换任何生成模型都不超过 34.2%（表 3） |
| [ArtifactsBench](https://arxiv.org/abs/2507.04952)（2025-07） | 每题 10 维 checklist；沙箱运行，截三张时序截图，MLLM 双 referee | 1,825 题、9 个领域（含游戏 413、SVG 123、模拟 75）；与 WebDev Arena 排名一致 94.4%；280 例专家研究成对一致最高 90.95% |
| [WebGen-Bench](https://arxiv.org/abs/2505.03733)（2025-05） | GPT-4o 按功能生成测试用例，人工过滤调整；WebVoyager 代理执行；生成指令时明确排除技术实现细节 | 647 条用例；人工执行全部约 10.8 小时、377.8 美元；训练集 WebGen-Instruct 6,667 条，32B 微调后 9.5% → 38.2% |
| [Vision2Web](https://arxiv.org/abs/2603.26648)（2026-03） | 三级任务（静态页 / 交互多页 / 全栈），workflow 式 agent 验证 = GUI agent + VLM judge | 193 题、918 张原型图、1,255 条测试用例 |
| [RCCA](https://arxiv.org/abs/2608.27906)（2026-08） | 每题围绕显式功能 rubric 构造；分层奖励区分格式 / 源码 / 运行时 / 功能失败；把 rubric 失败归因到代码片段做 token 级加权 | MiniAppBench 41.25（比 Ling-3.0-Flash 高 32.20） |

**增量一：参考解的正确用法是「生成 rubric」而不是「当对照」**
- RaR 的消融说明：同样有参考答案，拿它让 judge 做整体对照（31.7%）不如用它生成逐条 rubric（35.9%）
- 迁移到 visual coding：R 的渲染结果、scene graph、bpy 数据交给 rubric 生成器，产出「可观察」的条目（「桌面上有 4 把椅子，间距大致相等」），而不是「和参考截图一样」

**增量二：3D rubric 要标注观察层（推导）**
- 每条 rubric 加字段 `layer: pixel | structure | state | geometry`
- 规则：能落到 state / geometry 层的条目不交给 VLM；只有风格、审美、「像不像」才走 pixel 层 VLM
- 依据：WorldBench 在 5 个前沿模型生成的世界上发现，看渲染的 VLM 与读代码的 LM 对 32% 的必需条目判断不一致，主要是「代码写了但没有一帧画出来」（2610.10622）

**增量三：rubric 也要过变异测试**
- 用 R 生成的 rubric 去判 R 的变异体，杀不死的条目说明过松，改写或删除（与 2.6 相同的准入规则）

**能验证 / 不能验证**
- 能：开放需求的覆盖面，比单一总分可解释；可直接作为 GRPO 奖励
- 不能：judge 本身的幻觉；条目写成实现细节时会惩罚合法替代实现（第四章已要求 implementation-agnostic）

---

### 2.5 交互 / 行为测试

**原理**：脚本或 agent 驱动产物，比较动作前后的状态。Web 侧 Interactive Judge（Qwen Team 的 The Verification Horizon，[2606.26300](https://arxiv.org/abs/2606.26300) §3.2：planner 一次生成动作表 → Playwright 执行录屏 → judge 看帧 + 源码 + checklist）已在第七章 V3 覆盖；本节写 3D 与游戏的增量。

| 工作 | 构造 | 验证方式 | 关键数字 |
|---|---|---|---|
| [WorldCoder-Bench](https://arxiv.org/abs/2606.01869)（2026-06） | 5 名 3D 方向博士花两个月手写种子 → LLM 扩成 10,000+ 候选 → 人工丢弃含糊 / 平凡 / 无法落成确定性检查的 → 浏览器验证 → 专家写隐藏行为契约 → 2,026 题；另做 615 个扰动物理常数、对象数、初态、资源的 Robust 变体 | StateProbe：Playwright + 本地锁版本 three.js；先查能加载、有 WebGL context、render loop 在跑、无早期异常；再按脚本动作逐步快照 `window.__3D_STATE__` 并对隐藏契约断言；schema 对模型可见，动作序列 / 阈值 / 断言不可见 | 最好模型 Core 27.8%、Robust 19.9%；外部评测范式与真值的 Kendall τb：DOM −0.021、截图 + VLM −0.068、8 步 agent +0.111；严重缺陷误放率 33.7% / 3.2% / 45.6% |
| [WorldBench](https://arxiv.org/abs/2610.10622)（2026-10） | 一个固定 prompt（漂浮体素岛，10 个生物群系、物理、昼夜与季节），280 分逐条阶梯 | judge 接管世界时钟、环绕拍摄、派导航 agent 进近景；代码引用必须是源码里真实存在的文本，视觉声明在可测处用实测像素核对 | 删除特征的变异测试：纯读代码的 judge 对 5 个被删特征中 4 个给满分；新 judge 把被删特征上保留的分数从 5.44 降到 3.55（满分 7.11） |
| [PlayCoder / PlayEval](https://arxiv.org/abs/2604.19742)（2026-04） | 43 个多语言 GUI 应用（6 大类） | PlayTester agent 按任务做通关式游玩，检查逻辑违例；指标 Play@k = k 个候选里至少一个能端到端玩通 | 10 个代码模型编译率高但 Play@3 接近 0；PlayCoder 到 Exec@3 38.1%、Play@3 20.3% |
| [GameDevBench](https://arxiv.org/abs/2602.11103)（2026-02） | 从网页和视频教程提炼 Godot 任务；agent 依据教程的完整工程出题、写单测；只测指令里明确要求的功能 | Godot 脚本框架内的单测（可逐帧检查动画状态、物理、多边形形状）；每题带已验证的参考解 | 333 题；最好 53.8%；agent 出题首轮人审 41 题：43% 无问题、50% 小问题（场景出镜外、断言了指令没要求的东西）、7% 大问题 |

**在 visual coding 上怎么落地（推导）**
- 状态接口两条路
  1. 模型侧暴露：题面给 `window.__3D_STATE__` schema（WorldCoder 做法）；缺点是模型可以只更新状态不更新画面，需要配一条像素层断言兜底
  2. harness 侧注入：用本地锁版本的 three.js，harness 在页面加载前 patch `WebGLRenderer.prototype.render`，每帧拿到 `(scene, camera)` 引用，直接遍历 scene graph；不需要模型配合，也无法伪造
- 确定性：接管 `requestAnimationFrame` 与 `performance.now`，按固定步长推进时钟（WorldBench 也接管世界时钟）；固定随机种子；软件光栅（SwiftShader）保证跨机器像素一致
- 游戏可玩性：脚本化动作序列为主，LLM playtest agent 只做探索性补充；Play@k 只适合做评测，RL 奖励要用逐条行为断言

**能验证 / 不能验证**
- 能：机制正确性（物理守恒、状态同步、交互链路），这是截图和 DOM 都看不到的
- 不能：没有写进契约的行为；agent 式测试成本高（WorldCoder 中约为 DOM 的 400 倍）且不稳定

---

### 2.6 属性 / 不变量检查

**原理**：不比较目标，只检查任何正确解都必须满足的性质。比 2.1 的断言更「通用」，可跨任务复用，适合作为 P2P 和硬门槛。

**three.js scene graph 探针（推导，harness 注入）**
```js
// 页面加载前注入；three.js 为本地锁定版本
const orig = THREE.WebGLRenderer.prototype.render;
THREE.WebGLRenderer.prototype.render = function (scene, camera) {
  window.__probe = { scene, camera, frames: (window.__probe?.frames || 0) + 1 };
  return orig.call(this, scene, camera);
};
// 评测时：遍历 scene 输出对象名、类型、世界坐标 bbox、材质参数、灯光、相机
```

| 类别 | three.js | Blender（`bpy`） |
|---|---|---|
| 存在与数量 | 按 name / userData 计数；Mesh / Light / Camera 数 | `bpy.data.objects` 按类型计数 |
| 几何 | 世界坐标 bbox、无 NaN 顶点、不穿地面 | 顶点 / 面数区间、流形检查、无重叠面、连通分量数（防漂浮碎片） |
| 空间关系 | 「A 在 B 上」= bbox 接触 + 垂直顺序；对齐 / 间距 | 同左；可复用 SceneCraft 的关系打分函数（proximity、alignment、parallelism…，[2403.01248](https://arxiv.org/abs/2403.01248)） |
| 材质 | color ΔE、roughness / metalness 容差、贴图是否加载 | BSDF 节点参数、节点图连通 |
| 光照与相机 | 灯光数、强度、阴影开关、fov、相机朝向目标 | 灯光能量、相机焦距、目标物体在画面内 |
| 渲染与性能 | draw call 数、三角形数、帧率下限、无 WebGL 报错 | 渲染引擎、采样数、渲染时长上限 |
| 拓扑 | — | Betti 数（3DHarnessBench 用 Betti Norm. L1 评拓扑） |

- 3DCodeBench（[2606.01057](https://arxiv.org/abs/2606.01057)）的观察支持这类检查的价值：失败主要是 API 不匹配，渲染成功的产物仍常有「断开或漂浮的几何部件」；其造数流水线里专门有 Mesh Analyzer 查无效几何、非流形、顶点数异常
- **shader 参数扫描（推导）**：shader 没有 scene graph，可把 uniform 当输入做性质测试
  - 对时间 uniform 扫 N 个值，检查帧间差异非零（确实在动）且有界（不闪爆）
  - 对颜色 / 强度 uniform 做单调性检查（强度增大，平均亮度不降）
  - 固定输入下多次渲染像素一致（确定性）；NaN / 全黑 / 全白帧判失败

**能验证 / 不能验证**
- 能：结构健康度、明显作弊（空场景、静态截图冒充、对象堆在原点）、性能回归；成本极低，可做 V1 硬门槛
- 不能：需求是否被满足；性质过于宽松时什么都放过，所以只能与 2.1 / 2.4 组合用

---

### 2.7 无参考的开放任务：只能偏好 / 对比

**原理**：「做一个好看的太阳系」这类任务没有目标状态，只能比较。要点是把偏好变成组内相对奖励。

| 工作 | 做法 | 数字 / 结论 |
|---|---|---|
| [BigCodeArena](https://arxiv.org/abs/2510.08697)（2025-10） | 在 Chatbot Arena 上加实时执行环境，人可以操作运行结果后再投票 | 14K+ 会话、10 个模型；4.7K+ 条多轮成对偏好；React 3,107 会话、Core Web 1,699、PyGame 964 |
| [3DCodeBench / 3DCodeArena](https://arxiv.org/abs/2606.01057)（2026-06） | 对生成的 3D 物体做成对人类偏好 Elo；与自动指标对照 | 12 个模型上 SigLIP-2 多视角相似度与 Elo 的 Pearson r = 0.964，DINOv3 的 Spearman ρ = 0.972（注意是模型级相关，不是样本级） |
| [Pref-GRPO](https://arxiv.org/abs/2508.20751)（2025-08） | 组内两两比较，用每个样本的胜率当 reward，替代点式打分 | 点式分数在组内挤在一起时除以小标准差会放大噪声（illusory advantage），导致 reward hacking；胜率方差更大、对小偏差更稳 |

**落地（推导）**
- 先过硬门槛：2.6 的不变量 + 运行门槛，不过直接 0 分，不进比较
- 组内比较：同一 prompt 的 G 个通过者两两比，胜率做 GRPO advantage；第七章 7.2 的 tournament / Bradley–Terry 聚合同理
- 把参考解放进比较池当「锚」：R 参与组内比较但不参与更新；policy 解对 R 的胜率是一个跨 prompt 可比的指标，也能发现「参考不如 policy」的题（见 3.1）
- 3D 的比较证据要多视角 + 一段录屏，避免单视角把屏外内容漏掉

**能验证 / 不能验证**
- 能：审美、整体完成度这类不可分解的偏好
- 不能：功能正确性（偏好 judge 会被好看但不能用的产物骗过，第七章 7.4 已列）；成对比较的成本是 G 的平方

---

### 2.8 难度与质量筛选

| 手段 | 做法 | 出处 |
|---|---|---|
| pass@k 过滤 | 用当前 policy 采 G 个，剔除全对与全错的 prompt（组内 advantage 为 0，梯度为 0），持续采样直到 batch 填满 | DAPO Dynamic Sampling（[2503.14476](https://arxiv.org/abs/2503.14476) §3.2） |
| 难题挖掘 | 只保留 SFT 模型 3 次采样平均 reward 低于阈值的样本做 RL | cadrille（[2505.22914](https://arxiv.org/abs/2505.22914)，阈值 7.5，奖励 = 10×IoU，无效输出 −10） |
| 不让难题被误删 | 自验证失败的难题最多给 10 次尝试，而不是直接丢弃，避免数据偏向简单题 | KodCode（[2503.02951](https://arxiv.org/abs/2503.02951)，447K 三元组） |
| 参考解必须过自己的 verifier | gold patch 必须让 F2P 由失败变通过；每题带已验证参考解 | SWE-bench；GameDevBench |
| verifier 必须杀死变异体 | 从已验证实现注入缺陷，契约拒绝全部变异体才准入，否则修改或丢弃该题 | WorldCoder-Bench §3.2 |
| 测试质量用 TPR / TNR 量化 | 用大量已标注正确 / 错误的解测每题的测试；同样阈值下 CodeContests+ 的合格题数是原版两倍 | CodeContests+（[2506.05817](https://arxiv.org/abs/2506.05817)，172 万条标注解） |
| 测试要「难」 | 有 oracle 程序时合成测试，precision 高 11.3 个点、recall 高 17.5 个点；旧合成测试在难题上假阳性超过 90% | HardTests（[2505.24098](https://arxiv.org/abs/2505.24098)，47,136 题） |
| 规格–测试对齐审查 | agentic 质量 judge 进 Docker 环境读代码跑命令，判 instruct_clear 与 instruct_ut_align；给 gt patch 能提高后者召回 | Verification Horizon §2.2（instruct_clear F1 约 92–95，instruct_ut_align F1 约 75–78） |
| 学出来的质量标签 | 用人工标注微调模型预测 Issue Clarity / Task Complexity / Test Patch Correctness | SWE-rebench |
| 人审抽检 | agent 出题后先人审小样本，按常见错误写 checklist 让 agent 自修，最后全量人审 | GameDevBench（41 题样本，43 / 50 / 7） |
| 去重与污染隔离 | 按时间切（只用模型发布后的任务）；对 benchmark 做 Jaccard + Sentence-Transformer 相似度过滤；契约隐藏 + 参数扰动变体 | SWE-rebench；WebGen-Instruct；WorldCoder-Robust |
| 多样性 | 对种子代码聚类后按簇取样 | V-GameGym（[2509.20136](https://arxiv.org/abs/2509.20136)，2,219 条、100 个簇） |

---

### 2.9 八种范式一览

| 范式 | 目标来源 | 主要观察层 | 适合的任务 | 最大短板 |
|---|---|---|---|---|
| SWE 式 F2P / P2P | R 的状态 | state + structure | 已有工程上的功能 / 修复 | 断言覆盖不到即漏检 |
| 逆向构造 | 已有产物渲染 | pixel + geometry | 复刻、图生 3D | 机制不可见、一图多解 |
| 变异 / 扰动 | R 的状态 | state | 定点修复、编辑 | 变异分布偏离真实错误 |
| 需求 → rubric | 需求 + R 辅助 | 全部（逐条标层） | 开放需求 | judge 幻觉 |
| 交互 / 行为 | 隐藏契约 | state（动作前后） | 交互、物理、游戏 | 契约编写成本高 |
| 属性 / 不变量 | 通用性质 | state + geometry | 硬门槛、防作弊 | 不判需求是否满足 |
| 开放偏好 | 组内比较 | pixel + 录屏 | 审美、创意 | 不判功能、成本 G² |
| 难度与质量筛选 | — | — | 所有 | 依赖 policy 当前能力，需周期重跑 |

---

## 3. 重点问题

### 3.1 「参考代码只是一种解」：验证状态 / 效果，参考代码做什么

**为什么不能拿参考代码当目标**
- 等价实现极多：CAD-Coder 指出多份不同的 CadQuery 脚本能产出几何等价的模型，SFT 难以学到这一点，所以 RL 阶段用 Chamfer 距离分段线性奖励（CD < 1e-5 得 1.0，CD > 0.5 或执行失败得 0，[2505.19713](https://arxiv.org/abs/2505.19713)）
- 拿参考当整体对照的效果差：RaR 中 Reference-Likert 31.7%，低于用参考生成 rubric 的 35.9%
- 参考不一定最优：开发者代码可能有冗余、性能差、写法过时；以代码相似度为奖励会把这些缺点一起学进去

**参考代码的五个正确用途**

| 用途 | 怎么用 | 出处 |
|---|---|---|
| 1. 证明可解 | R 必须在 harness 里跑通并通过全部 F2P / P2P，重复 3 次稳定 | SWE-bench gold patch；GameDevBench 每题带已验证参考解 |
| 2. 生成断言与 rubric | 从 R 的运行状态（scene graph、bpy 数据、DOM、交互前后差分）抽断言；把 R 的渲染交给 rubric 生成器 | RaR；BlenderGym 的 goal 场景；WorldCoder 契约由专家依据任务写成 |
| 3. 变异母本 | 对 R 做 2.3 的变异，得到修复题和 verifier 校准集 | SWE-smith；WorldCoder「从已验证实现注入缺陷」 |
| 4. verifier 的 sanity check | R 必过、S0 必挂、变异体必挂；三条任一不满足，问题在 verifier 或题目，不在 policy | SWE-bench 准入规则；WorldCoder 契约准入 |
| 5. SFT 冷启动 | R 可作为一条示范轨迹，但只是多条合格轨迹之一；RL 阶段不出现在 reward 里 | CAD-Coder（SFT → GRPO 两阶段）；cadrille |

**「参考不是最优」的处理（推导）**
- 把 R 当**下界**：reward 只要求满足 A，不要求接近 R，超过 R 不受惩罚
- 开放维度用 2.7 的组内比较，把 R 放进比较池当锚；统计每题 policy 解对 R 的胜率
- 胜率持续很高的题，说明 R 已不是好参考：用通过全部断言且胜率最高的 rollout 替换 R，并重跑 3.2 的准入检查（CAD-Coder 造数时在多个候选里按几何误差取最优，思路相同）
- R 自身也要打分：通过率、性能（帧率、draw call、渲染时长）、代码体量；分数低的 R 不进 SFT 池，只保留它产出的断言
- 题面不得泄露 R 的实现：只描述可观察效果；锚点（DOM id、状态 schema、对象名）写进 I 并对模型公开，不靠模型猜 R 的命名（对应 SWE-bench 排除「测试调用 solution 新建函数」）

### 3.2 数据质量的可计算指标

记：R = 参考解，S0 = 初态，M = 变异体集合，P = 当前 policy，A = 断言集。

| 指标 | 计算 | 建议门槛（推导初值） | 依据 |
|---|---|---|---|
| 可解率 | R 通过全部 A 的比例，3 次重复取交 | 每题 100%，否则剔除 | SWE-bench；GameDevBench |
| 非平凡率 | F2P 在 S0 上全部失败的比例；另加「空解 / 静态截图解」基线也必须失败 | 每题 100% | SWE-bench F2P 定义 |
| 变异杀死率（判别力 TNR） | 被 A 判失败的变异体 / 全部变异体 | ≥ 95%；未杀死的变异体逐个审，补断言 | WorldCoder 契约准入 |
| 正确解通过率（判别力 TPR） | 已知正确的替代实现（不同 policy、人写、R 的等价改写）通过 A 的比例 | ≥ 90%；过低说明断言绑了实现细节 | CodeContests+ TPR / TNR |
| 单条断言区分度 | 能区分「最终判对」与「最终判错」rollout 的断言占比 | 区分度为 0 的断言删除或改写 | R2E-Gym：多数题不到 20% 的测试有区分力 |
| 外部范式误放率 | 已知严重缺陷的产物被判通过的比例 | 状态层 verifier 应接近 0 | WorldCoder：DOM 33.7%、8 步 agent 45.6% |
| 难度分布 | P 采 k 次的通过率 p；按 p 分桶统计 | 训练池以 0 < p < 1 为主；p = 0 的题先查可解率和判别力，再决定是否留作课程 | DAPO；cadrille；KodCode |
| 稳定性 | 同一产物重复验证 3 次结果不一致的比例（flaky） | ≤ 1%；超出先修确定性（时钟、种子、软件光栅） | 第七章 7.5 |
| 规格对齐度 | judge 判 instruct_clear 与 instruct_ut_align 的通过率 | 两项都通过才进池 | Verification Horizon §2.2 |
| 人审缺陷率 | 抽样人审中「小问题 / 大问题」比例 | 大问题 ≤ 5%；超出时按缺陷类型写 checklist 让 agent 自修后重审 | GameDevBench 43 / 50 / 7 |
| judge–人一致率 | 偏好或 rubric 判决与人工标注一致的比例；看样本级而不只看模型级 | 第七章 7.5 已给目标值 | 3DCodeBench 只给了模型级相关（r = 0.964） |
| 多样性 | 需求文本 embedding 聚类覆盖；用到的 three.js 类 / bpy 算子覆盖；渲染图 embedding 覆盖 | 每簇设上限，长尾簇定向补题 | V-GameGym 100 簇 |
| 污染率 | 与评测集的 n-gram / embedding 相似度超阈值比例；时间切分 | 0（命中即删） | SWE-rebench；WebGen-Instruct |

- 判别力是最容易被忽略的一项：可解率只证明「R 能过」，判别力证明「错的过不了」；两者都要
- 指标要周期重算：policy 变强后，原本 0 < p < 1 的题会变成全对，变异杀死率也需要针对新的作弊方式补变异算子（Verification Horizon 的结论：没有固定 reward 能随 policy 能力增长一直有效）

### 3.3 推荐流水线（three.js / Blender，推导）

```
种子
├── 程序化生成器（Infinigen 类工厂、参数化 three.js 场景）
├── 开发者参考工程（CodePen / GitHub / .blend）
└── 教程（GameDevBench 式：用教程的完整工程出题）
        │
        ▼
构造 R 与 S0
├── 从零类：S0 = 空模板
├── 编辑类：S0 = R 的前一版本 / 去掉某功能
└── 修复类：S0 = R 的变异体（规则变异 + agent 加功能产生的自然缺陷）
        │
        ▼
编译断言 A（模型不可见）
├── state 层：scene graph / bpy / window.__3D_STATE__ 断言（F2P + P2P）
├── geometry 层：Chamfer / IoU / Betti，对目标几何
├── pixel 层：held-out 视角渲染 + VLM rubric（只放风格类条目）
└── 不变量：存在性、流形、连通分量、性能下限
        │
        ▼
准入检查（3.2 前五项）
├── R 必过 ×3、S0 必挂、空解必挂
├── 变异杀死率 ≥ 95%，替代实现通过率 ≥ 90%
└── 规格对齐 judge + 人审抽样
        │
        ▼
难度标定与入池
├── P 采 k 次得 p，按桶配比
├── 去重、去污染、按簇限额
└── 周期重跑：p 漂移、新作弊方式 → 补变异算子与断言
```

---

## 4. 参考文献

| 日期 | 工作 | 链接 |
|---|---|---|
| 2023-06 | Infinigen | https://arxiv.org/abs/2306.09310 |
| 2023-10 | SWE-bench | https://arxiv.org/abs/2310.06770 |
| 2024-03 | SceneCraft | https://arxiv.org/abs/2403.01248 |
| 2024-03 | Design2Code | https://arxiv.org/abs/2403.03163 |
| 2024-03 | WebSight | https://arxiv.org/abs/2403.09029 |
| 2024-10 | SWE-bench Multimodal | https://arxiv.org/abs/2410.03859 |
| 2024-10 | Sketch2Code | https://arxiv.org/abs/2410.16232 |
| 2024-11 | Interaction2Code | https://arxiv.org/abs/2411.03292 |
| 2024-12 | SWE-Gym | https://arxiv.org/abs/2412.21139 |
| 2025-03 | KodCode | https://arxiv.org/abs/2503.02951 |
| 2025-03 | DAPO | https://arxiv.org/abs/2503.14476 |
| 2025-04 | BlenderGym | https://arxiv.org/abs/2504.01786 |
| 2025-04 | R2E-Gym | https://arxiv.org/abs/2504.07164 |
| 2025-04 | SWE-smith | https://arxiv.org/abs/2504.21798 |
| 2025-05 | WebGen-Bench | https://arxiv.org/abs/2505.03733 |
| 2025-05 | CAD-Coder | https://arxiv.org/abs/2505.19713 |
| 2025-05 | SWE-rebench | https://arxiv.org/abs/2505.20411 |
| 2025-05 | cadrille | https://arxiv.org/abs/2505.22914 |
| 2025-05 | HardTests | https://arxiv.org/abs/2505.24098 |
| 2025-06 | CodeContests+ | https://arxiv.org/abs/2506.05817 |
| 2025-07 | ArtifactsBench | https://arxiv.org/abs/2507.04952 |
| 2025-07 | Rubrics as Rewards | https://arxiv.org/abs/2507.17746 |
| 2025-08 | Pref-GRPO | https://arxiv.org/abs/2508.20751 |
| 2025-09 | V-GameGym | https://arxiv.org/abs/2509.20136 |
| 2025-10 | BigCodeArena | https://arxiv.org/abs/2510.08697 |
| 2025-10 | BugPilot | https://arxiv.org/abs/2510.19898 |
| 2026-02 | GameDevBench | https://arxiv.org/abs/2602.11103 |
| 2026-03 | Vision2Web | https://arxiv.org/abs/2603.26648 |
| 2026-04 | PlayCoder / PlayEval | https://arxiv.org/abs/2604.19742 |
| 2026-06 | 3DCodeBench / 3DCodeArena | https://arxiv.org/abs/2606.01057 |
| 2026-06 | WorldCoder-Bench / StateProbe | https://arxiv.org/abs/2606.01869 |
| 2026-06 | The Verification Horizon（Qwen Team） | https://arxiv.org/abs/2606.26300 |
| 2026-08 | RCCA | https://arxiv.org/abs/2608.27906 |
| 2026-09 | 3DHarnessBench | https://arxiv.org/abs/2609.06535 |
| 2026-10 | WorldBench | https://arxiv.org/abs/2610.10622 |

