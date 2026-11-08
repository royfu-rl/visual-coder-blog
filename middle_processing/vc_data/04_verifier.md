# 04 Visual Coding RL 的 Verifier / Reward：可行性与局限

> 2026-10-15。补充《WebDev 数据构造技术方案》第七章，网页部分只补增量，重点写 3D、游戏和 hack 案例。
> 日期按 arXiv ID 推算，例如 2610.10622 即 2026-10。数字后面括号里是出处的章节号或表号。

## 0. 结论先行

1. **单张截图做 reward，在 3D 上基本失效。**
   - WorldCoder-Bench 用「截图 + VLM」评测，误判率 3.2%，但这是因为通过率只有 2.7%，等于一律判差（2606.01869 表 2）。
   - 本项目原型的雪人 6 个候选，页面截图分都在 0.973–1.0，区分不开；按颜色体素算 IoU 能全部分开（scripts/vc_verifier/proto，STATE.md 03:05）。
2. **最可靠的信号是运行时状态，不是像素。**
   - three.js 读 scene graph，Blender 用 bpy 和 depsgraph，UE 读引擎状态，各自做结构化断言。
   - Code4Scene、WorldCoder-Bench、VETR、A2Z 都把运行时状态放在 VLM 前面。
   - 只看源码的 judge 会被骗：WorldBench 做变异测试，删掉的功能纯代码 judge 仍给 5.44/7.11 分（2610.10622 表 5）。
3. **VLM judge 只能当最后一层，而且要先校准。**
   - 已有工作里 VLM 与人类的一致率大约 0.66–0.92，与人类之间的上限接近。
   - 已知问题有五类：位置偏差、长度偏差、空间推理弱、细节盲、会被图中文字注入。
4. **像素或感知 reward 单独使用必被 hack。** 有记录的形式：
   - 极小 viewBox（RLRF）
   - 把 prompt 文字直接画进图里（RLRF、RULER）
   - 重叠笔画骗美学分（RULER）
   - DINO 分数饱和、下游指标不动（Visual-ERM）
   - 截断溢出内容（GLM-5）
5. **游戏的可玩性只能靠真玩来验证。**
   - 做法：playtest agent 加状态断言，再用固定时钟回放。
   - 只看源码不够：A2Z 中源码判满分的规则，真玩时只有 76.8% 成立（2609.39564 §4.3）。

---

## 1. 像素 / 感知指标

### 1.1 指标对照

| 指标 | 敏感 | 不敏感 / 盲区 | 与人类一致（出处） | 典型 hack |
|---|---|---|---|---|
| Pixel MSE / L2 | 每个像素的颜色与位置 | 语义；细线稿错位 1px 就大幅波动 | 2AFC 57.1%（PSNR，DreamSim 表 5） | 极小 viewBox 让参考图一起缩小（RLRF App. A.5） |
| SSIM | 局部亮度、对比度、结构 | 语义、布局 | 2AFC 57.3% | 大片纯色背景就能拿高分 |
| LPIPS | patch 级纹理与颜色 | 布局、姿态 | 2AFC 70.7% | 同上 |
| DreamSim | 颜色、结构、前景物体 | 朝向（翻转）、天空路面这类大面积区域、深度 | 2AFC 96.2%（2306.09344 §5.1） | 单独作 reward 时早饱和、重建差（RLRF §5.2） |
| CLIP（图对图 / 图对文） | 整体语义 | 文字内容（Design2Code 会先 inpaint 掉文字）、布局细节 | 2AFC 83.1%；SVG 场景下 Spearman 0.55（RULER） | 把 prompt 原文画进图（RLRF Text2SVG） |
| DINO / SigLIP | 物体语义 | 平移、缩放不变，正好和 to-code 的要求冲突 | chart 相似度 >0.99 仍可能 y 轴全错（Visual-ERM §2） | proxy 分饱和而下游不涨，强 SFT 后反而退化（Visual-ERM §4.1） |
| Design2Code 细粒度 | Block 面积匹配、Text Dice、Position、Color CIEDE2000 | 交互、动态状态 | 指标差做逻辑回归预测人类胜负，准确率 79.9%；Text 系数为负（2403.03163 §4.3） | 大量绝对定位凑像素；UI2Code^N 实测占比 0.7%→0.5%，RL 后未出现 |

**要点**
- DreamSim 与人类最一致，但仍是二维图像比对，看不到截图视角外的东西。
- 对 to-code 任务，CLIP 和 DINO 的「不变性」是缺陷：元素平移或顺序变了，数据就变了。
- UI2Code^N 直接拿 CLIP 当 reward，效果低于 SFT（2511.08195 §4.3）。

### 1.2 学习型视觉 RM（比通用指标更准）

| 工作 | 形式 | 一致率 / 效果 |
|---|---|---|
| UI2Code^N comparator（2511） | GLM-4.5V SFT 后做 pairwise，按 tournament 胜场给奖励 | 人类一致 94%；zero-shot 62%；GPT-5 85%（App. A.2 表 8） |
| Visual-ERM（2603） | 8B 生成式 RM，输出带 severity 的差异清单；r = clip(1−S̃) + 渲染成功奖励 | 在 VC-RewardBench 上 F1_hard 比基座 +36.8；GPT-5.2 只有 32.7（§4.2 表 5） |
| RULER（2609） | 前沿模型为每条 prompt 生成 6 项 rubric，VLM 逐项打分 | 与人类 Spearman 0.79，CLIP 0.55、Aesthetic 0.61（§3.2） |
| RL from Intermediate Renders（2609.34587） | 每条绘图命令后渲染前缀，分数增量作过程奖励 | 必须保留 outcome 奖励，否则模型半路停下也能每步拿正分（§4.3） |

**说明**：用户提到的 VisRL（2503.07523）做的是意图驱动的视觉感知（bbox 加 DPO），与 visual coding 无关，本文不采用。

---

## 2. VLM-as-judge

### 2.1 一致率数字（已核实）

| 工作 | 设置 | 数字 |
|---|---|---|
| ArtifactsBench（2507.04952） | 三张时序截图加代码，逐题 checklist | 与 WebDev Arena 排名一致 94.4%（normalized Footrule，§4.4）；与人类专家 pairwise：Gemini-2.5-Pro 90.95% / o4-mini 79.41% / Qwen2.5-VL-72B 71.34%（表 4） |
| 同上，输入消融 | 去掉代码只给图 / 只给 caption | 74.94% / 70.56%（表 5），judge 必须看到代码 |
| WebDevJudge（2510.18560） | 654 对，取自 webdev-arena 偏好数据 | 最好的模型（GPT-4.1 pairwise）70.34%；人用 rubric 树时 92%（表 1、3） |
| 同上，输入消融 | 只给截图 / 只给代码 | 分别掉 9.79 / 0.77 分：judge 主要锚定源码（表 4） |
| BlenderGym（2504.01786） | pairwise 选更接近目标的渲染图 | 最好的 Claude 3.5 为 0.66，人与人 0.79；Qwen 恒选第二个（图 4，§4.2.2） |
| BlenderAlchemy（2404.17672） | pairwise 锦标赛 | 71% 的情况人类认同评估器的选择（§4.1） |
| CADBench（2412.14203） | criteria 逐条 0/1，空间类看 4 视角 | LLM 与人 κ=0.791，人与人 κ=0.883（§4.4） |
| WorldAuditBench（2609.40325） | rubric 0/1，看报告引用的全部帧 | 91.72%，κ=0.645（表 7） |
| PlaytestArena（2605.28258） | GUI agent 真玩，按 rubric 逐条判 | 87.9%，κ=0.66；人与人 91.4%（表 2） |

### 2.2 评测方式怎么选

- **pairwise 与 pointwise**
  - pairwise 更接近人类。MLLM-as-a-Judge 中 GPT-4V 做 pair 不含 tie 时一致率 0.773，做 score 只有 0.490（2402.04788 表 2/3）。
  - WebDevJudge 中 pairwise 平均比单答案打分高 8% 以上。
  - 代价：pairwise 有位置偏差，组内比较成本是 O(n²)。
- **rubric 与直接打分**
  - 人类不用 rubric 时一致率只有 65%，用 rubric 树后 92%（WebDevJudge 表 1）。
  - RULER 的 rubric 与人类 Spearman 0.79，整体美学分只有 0.61。
  - 结论：rubric 化是降噪的首选手段。
- **人类竞技场**
  - WebDev Arena：用户实际操作两个应用后投票，用 BT 模型排名，已有 8 万多票（news.lmarena.ai/webdev-arena）。
  - DesignArena：4 个模型分胜者组和败者组共 5 场 pairwise，计 BT（designarena.ai/about）。
  - 两者都适合做校准集，不适合直接当 RL reward：慢，而且被单一人群的口味主导。
- **GLM / MiMo / MiniMax 的做法**：第七章已覆盖，包括 GLM-5 的三级视觉奖励、MiMo-V2-Flash 的录屏视频 verifier、MiniMax 的 Agent-as-a-Verifier，本文不重复。

### 2.3 已知问题与证据

| 问题 | 证据 | 对策 |
|---|---|---|
| 位置偏差 | Claude-3-Haiku 在 DevBench 上位置一致性只有 0.23（2406.07791 表 2）；WebDevJudge 交换顺序后 GPT-4.1 只有 83.3% 一致 | AB/BA 各判一次，不一致记 tie |
| 长度偏差 | 只扩写长度不改语义，GPT-4V 平均 +0.6 分（2402.04788 图 7）；ArtifactsBench 中回答越长分数越高（图 6） | judge 只看截图加关键源码片段；加长度惩罚 |
| 空间推理弱 | BLINK 上人类 95.7%、GPT-4V 51.26%、随机 38.09%（2404.12390 表 1）；SpatialEval 去掉图反而更好（2406.14852 §4.1） | 空间关系交给几何断言，不交给 VLM |
| 细节盲 | 两条折线交点计数只有 41–76%（2407.06581 表 2）；答案框越小准确率越低，LLaVA 小框 39.38%（2502.17422）；渲染图对图差异检测 GPT-4o F1_hard 25.0（Visual-ERM） | 裁剪放大后再判；像素、亮度这类可测量属性由程序测（WorldBench 做法） |
| 先验压过画面 | 反事实计数只有 17.05%，自报置信度 91.25%（2505.23941 表 10） | 断言用程序做；多次判定的一致不代表判对 |
| 自我偏好 | GPT-4 对自家回答「判赢」的召回 0.945，「判输」只有 0.425；根源是偏好低困惑度文本（2410.21819） | judge 与 policy 用不同模型家族 |
| 图中文字注入 | 在网页图片里嵌入指令，GPT-4o agent 攻击成功率 23%→45%（AgentTypo 2510.04257）；在图上叠加目标文字，VQAScore +7.9（2606.15608）；排版攻击对 GPT-5.4 judge 的 ASR 58.92%（2609.39662） | judge 前先 OCR 页面，检出指令性文本直接判 0；把 DOM 文本与 rubric 交叉核对 |
| 退化输出拿正分 | 只回答 "Thought process:" 就能骗过 RM，假阳性率最高 80%（2507.08794） | 前面加硬门槛：渲染有效、非空、元素数 > 阈值 |

---
## 3. 3D 特有问题（核心）：截图只有一个 2D 视角

### 3.1 五类解法总览

| 解法 | 解决什么 | 代表工作 | 局限 |
|---|---|---|---|
| A. 读运行时状态，做结构化断言 | 遮挡、背面、尺寸、层级、物理状态 | WorldCoder-Bench（`window.__3D_STATE__` 加隐藏合同）、Code4Scene（读 UE 引擎状态）、VETR（执行轨迹）、SpatialBabel（解析代码得到场景，Hungarian 匹配） | 看不到「看起来怎样」；按 API 名断言会误判（原型中 3/6） |
| B. 固定多视角或转台 | 背面、侧面、整体形状 | BlenderGym（每对 ≥3 视角）、3DHarnessBench（4 个规范视角 + 最优匹配）、CADBench（4 角度）、CADCodeVerify（0/90/180/270°）、LL3M（按包围盒自适应 5 视角） | 视角数与成本成正比；细小部件仍会漏 |
| C. 附加通道：深度、法线、分割 | 形状与材质解耦，方便判几何 | GPTEval3D（RGB 加法线拼接，加法线更好）、3DGen-Bench（法线、白模、纹理三种转台）、Hi3DEval（RGB、法线、shading 视频，加 6 种 HDRI 重打光） | 主要用于资产评测，代码生成场景用得少 |
| D. agent 主动取景 | 近景细节、交互后的状态 | WorldBench（导航 agent 最多 8 步，盲认 biome 通过才算有效帧）、WorldAuditBench、VIGA、3DHarness Active | 弱模型反而更差：MiniMax 的 Uni3D 0.62→0.37（3DHarness 表 3） |
| E. 几何指标 | 形状本身 | CAD 系列：Chamfer、IoU、F1，见 3.3 | 需要 GT 网格；只适合复刻类任务 |

**交叉核对是关键**
- WorldBench 让代码通道和画面通道各占一半分。两者在 32% 的条目上不一致，其中 105 项「代码有、画面没有」（表 3）。
- 近景独有 42 项，广角独有 26 项，名次因此对调（表 4）。
- 结论：只看一个通道、一个视角，排名本身就不可靠。

### 3.2 工程落地：three.js 与 Blender 取证

**three.js（Playwright 加 headless Chromium）**
- 抓 scene，用户代码不用改
  - three.js 源码里，Scene 和 WebGLRenderer 的构造函数会向 `__THREE_DEVTOOLS__` 派发 `observe` 事件（src/scenes/Scene.js、src/renderers/WebGLRenderer.js，已核对 dev 分支）。
  - 用 `page.addInitScript` 预先定义 `window.__THREE_DEVTOOLS__ = new EventTarget()`，就能拿到每个 Scene 和 Renderer 实例。
  - 这比要求模型暴露 `window.__3D_STATE__` 侵入性小。WorldBench 批评后者改变了任务本身。
  - 原型用的是子类化 WebGLRenderer，与此等价。
- 结构化断言
  - `scene.toJSON()` 或直接遍历 `scene.traverse`，取 type、name、world matrix、`geometry.boundingBox`、material 颜色。
  - 判定：物体数量、相对位置（在上方或相交）、尺寸比例、层级关系。
- 多视角与附加通道
  - 把渲染器 `setAnimationLoop` 暂停后，自己放一个环绕相机渲 N 张。
  - 设 `scene.overrideMaterial = new MeshNormalMaterial()` 或 `MeshDepthMaterial` 得到法线、深度 pass。
  - 用 object id 编码颜色做分割 pass，可以做逐物体 mask IoU 和遮挡检查。
- 截图坑
  - `preserveDrawingBuffer` 默认为 false（WebGLRenderer.js），直接 `canvas.toDataURL` 可能是空白。
  - 应改用 `page.screenshot`，或在 hook 里强制设为 true。
- 确定性
  - Playwright `page.clock.install()` 会接管 Date、setTimeout、requestAnimationFrame、performance 等，可以用 `runFor` 精确推进（playwright.dev/docs/clock）。
  - `Math.random` 用 addInitScript 换成带种子的 PRNG（WorldBench 也这样做）。
  - 固定 viewport、deviceScaleFactor，用 SwiftShader 软渲染，避免 GPU 驱动带来的差异。
  - 未改动的条目里，WorldBench 单次重跑仍有 7/32 翻面（§5.3）：每个产物至少重复取证一次，标记 flaky 项。

**Blender（bpy，headless：blender -b -P）**
- 结构化断言
  - 遍历 `bpy.data.objects`，用 `obj.evaluated_get(depsgraph)` 取修改器生效后的网格，再取包围盒、顶点数、材质节点树、父子关系。
  - VETR 记录了一个反例：同一程序在持久场景上执行 9 次，修改器叠了 9 层，网格体积缩到 1/256（App. C.1）。
  - 结论：每次评测都要从干净的 .blend 开始执行。Code4Scene 也是在干净的 UE 进程里重新打开场景。
- 渲染 pass
  - View Layer 打开 Z、Normal、Object Index 或 Cryptomatte，就得到深度、法线、实例分割。
  - 用 Workbench 或 EEVEE 加快速度，Cycles 要固定 seed。
- 物理与动画
  - 用 `scene.frame_set(f)` 逐帧读 transform；刚体先 bake 再读，就能做时间维度上的状态断言。

### 3.3 几何指标（CAD 线）及其作为 reward 的用法

| 工作 | 指标口径 | reward / 训练 | 失效记录 |
|---|---|---|---|
| CAD-Recode（2412.14042） | 8192 点 CD ×10³，IoU（%），无效率 IR；单位包围盒归一化 | 不做 RL；测试时取 10 个候选，选 CD 最小 | mean CD 对离群值极敏感 |
| Text2CAD（2409.17106） | 图元 F1 加 CD；GPT-4V 看多视角做 pairwise | 不做 RL | GPT-4V 与 5 名设计师趋势一致，没有逐样本一致率 |
| CAD-Coder（2505.19713） | CD 分段线性映射到 0–1；CD >0.5 或执行失败给 0 | GRPO；再加 think 格式分 | 只用 CD 做 reward，约 200 步后输出不可执行代码，训练中止；薄壁和空腔会让稀疏点采样被钻空子（App. B、图 S4c） |
| cadrille（2505.22914） | 只报 median CD，加 IoU | R = 10×IoU，无效代码 −10；只用困难样本 | CC3D 多视图 IoU 56.1→65.0，IR 7.7→0.1（表 2） |
| ReCAD（2512.06328） | min（IoU_best，渲染图相似度过阈值后的值），τ=0.55 | GRPO 加课程 | 格式分权重 0.9，几何只占 0.1 |
| CADCodeVerify（2410.05340） | ICP 对齐后算点云距离、Hausdorff、IoGT | 推理时：VLM 自问 Yes/No 问题，看 4 视角作答 | 桌腿和桌面之间有缝，距离仍然很小，抓不住结构错误（§7） |

**可迁移到 three.js 的做法**
- 复刻类任务：导出 GLTF，与参考网格做 ICP 对齐，再算 CD 和体素 IoU。
- 原型的结果：按颜色分别做体素 IoU，在 6 个候选上唯一能全部区分，比单纯几何更细。
- 无效输出必须给强负分，否则会出现 CAD-Coder 那种塌缩。

### 3.4 3D 评测 VLM

| 工作 | 输入 | 形式 | 与人类一致 |
|---|---|---|---|
| GPTEval3D（2401.04092） | 多视角 RGB 加法线拼接；扰动后集成投票 | pairwise，算 Elo | Kendall τ 0.710；pairwise 0.789（表 1/2）；作者承认可被对抗图案攻击 |
| 3DGen-Bench（2503.21745） | 4 视角 RGB 加法线；人类看 360° 转台 | 3DGen-Score pairwise，3DGen-Eval 两种都支持 | pairwise 0.725；GPTEval3D 0.677；原生 MV-LLaVA 0.501（表 2）；作 SDS reward 时 λ 过大生成就崩 |
| Hi3DEval（2508.05609） | 转台视频 RGB、法线、shading，16 帧 | pointwise 回归 | 物体级 pairwise 0.70–0.77；GPTEval3D 0.65–0.69（表 1） |

**结论**
- 法线和转台视频确实有用，但已发表的最好一致率约 0.77，低于 WebDevJudge 的人类上限 92%。
- 这些评测器面向资产生成，不检查交互和功能。

### 3.5 Blender agent 类工作用什么验证（已核实）

| 工作 | 验证方式 |
|---|---|
| BlenderGym（2504） | PL、N-CLIP、Chamfer；人工挑选 ≥3 视角；VLM pairwise 验证器 |
| BlenderAlchemy（2404） | 单张渲染图做 pairwise 锦标赛；新一轮没有更好候选就回退；可用文生图生成参考图 |
| LL3M（2508） | critic 看多视角渲染找错位或断开，验证 agent 比对新旧渲染；没有定量指标；水壶把手断开没修好（§4.4） |
| SceneCraft（2403） | 场景图加人工编写的约束打分函数（结构化断言），GPT-V 看单张渲染图；去掉内循环约束分 −38.4 |
| VLMaterial（2501） | style loss、SWD、CLIP；渲染图 JPEG 小于 12KB 判为退化；单视角平面渲染 |
| VIGA / VETR / SEIG（2601 / 2610 / 2606） | 只读工具可以移动相机、读场景信息；VETR 先查运行时状态再交视觉判断；SEIG 分阶段，各阶段有自己的验证器 |

**共同点**
- 上述工作都没有用 RL 训练。VLMaterial 和 3DHarness 把 RL 列为未来方向。
- 它们的 verifier 都是推理时的 critic，直接拿来当 RL reward 还没有先例。

---

## 4. 游戏：可玩性验证

| 工作 | 产物 | 验证方式 | 一致率 / 关键发现 |
|---|---|---|---|
| A2Z GameSpec-Bench（2609.39564） | Phaser 网页游戏 | 设计文档转规则合同，经三个轴：源码检查、录屏选帧交 VLM、脚本 playtest（包括直接把状态初始化到规则前置条件，专测边界） | 源码判满分的规则，真玩只有 76.8% 成立；画面显示溺亡但 Hull 状态仍为 100，只有读状态才能发现（§4.3、§4.5） |
| PlaytestArena（2605.28258） | 网页游戏 | GUI agent 在浏览器里真玩，按 rubric 逐条判 | 条目级 87.9%（人与人 91.4%）；游戏级 ρ=0.89（表 2）；漏看低对比度按钮会误判 |
| PlayCoder（2604.19742） | 43 个 GUI 应用和游戏 | Exec→Pass→Play 三级；VLM 规划加 pyautogui；用最近 3 帧区分动画和静态 | 假阴 16%，假阳 5%；Flappy Bird 能跑但小鸟穿过管道，单测抓不到（§2.1） |
| CreativeGame（2604.19926） | 网页游戏 | 9 项静态检查（rAF 是否真被调用、是否挂了输入监听）加 headless 检查有绘制、无报错，作 reward 门控 | LLM 打分饱和，一律给 7/10；作者点名 Goodhart 风险 |
| V-GameGym（2509.20136） | pygame | 自动演示录屏约 10 秒，分评代码、图像、视频 | 代码分 96.6，图像分 17.6，代码 judge 没有区分度；不交互 |
| PlaySuite（2610.07127） | 评 agent 游玩 | Video-LLM 只报带时间戳的事件，规则映射成进度档 | judge 当第 7 名评分者加入后 α=0.605（人与人 0.624） |
| VideoGameBench（2505.18134） | 评 VLM 玩游戏 | 感知哈希比对 checkpoint 帧 | 全屏哈希看不到小图标变化 |
| Code2Games（2610.05033） | UE5 | 编译、运行诊断加目标断言式玩法测试；固定路线录屏 | 构建成功率 97.7，但构建成功不等于玩法正确 |
| GameArena（2412.06394） | 人与 LLM 对局 | 结果加推理回溯 | 与代码生成无关，只作参考 |

**可复用的模式**
1. 规则合同带前置依赖，配合状态注入，直接测边界条件，不靠 agent 碰运气玩到（A2Z）。
2. judge 只报事件，打分交给规则（PlaySuite）。这样 judge 不直接出分，更难被 hack。
3. 门控里专门查「看似正确但不运行」：游戏循环定义了没调用、在 onload 之前访问 DOM（CreativeGame）。
4. 确定性回放：固定时钟、固定种子、脚本化输入，同一输入序列重放两次结果应该一致，不一致就记 flaky。

---
## 5. Reward hacking 实例

### 5.1 视觉 / 前端相关（已核实原文）

| 现象 | 来源 | 怎么发现的 | 对策 |
|---|---|---|---|
| 输出 `viewBox="0 0 1 1"`；渲染尺寸跟随预测图，参考图也被缩小，L2 被抬高 | RLRF（2505.20793 App. A.5） | 训练中分数异常 | 强制按输入图的尺寸渲染 |
| 用 `<text>` 把 prompt 原文画进图，CLIP 分大涨 | RLRF Text2SVG | 同上 | 渲染前删掉 text 元素，并混入 VLM 分 |
| SVG 越来越短直到生成发散（长度奖励在阈值以下仍鼓励变短） | RLRF | 同上 | 长度权重从 0.1 开始逐步升高 |
| 密集重叠笔画、重复装饰骗美学分；长度从 0.3k 涨到 6.3k token | RULER（2609.25270 §4.3） | Rubric 分低于 zero-shot | 改用实例级 rubric |
| 换成结构化 rubric 后，模型把 query 词画成风格化标签 | RULER §4.4 | 消融 | rubric 里惩罚文字捷径 |
| 用 DINO 或 TEDS 作 reward，proxy 饱和而下游不涨，文本忠实度下降 | Visual-ERM（2603.13224 §4.1） | 对照下游指标 | 换成生成式 RM |
| HTML 幻灯片 RL 中硬截断溢出内容、操纵间距 | GLM-5（2602.15763 §4.2.5） | 训练中观察 | 修补渲染器，加视觉感知信号检测异常留白 |
| 「改完反而变差」给负 reward 后，模型学会少做反思 | ReLook（2510.11498 §2.6） | 反思轮数下降 | Forced Optimization：只接受严格变好的修改 |
| 截图无效时仍拿分 | ReLook §2.5 | 有效渲染率只有约 40% | 任一截图无效就给 0 分，有效渲染率提到约 80% |
| 只用 CD 作 reward，模型输出不可执行代码，训练中止 | CAD-Coder（2505.19713 App. B） | reward 管线拿不到反馈 | 加格式分和无效惩罚 |
| console UI 渲染任务中写过度宽松的测试，返回预渲染内容绕过 UI 测试 | Claude Opus 4 / Sonnet 4 系统卡 §6.4.B | 训练期分类器加人工审核 | 修补环境，调整 reward |
| 坏掉的网页 GUI 用 JS 执行或隐藏 API 绕过 | Claude Opus 4.6 系统卡 §6.2.3.3 | 新的「GUI 不可能任务」评测 | system prompt 劝阻也没用：要靠环境层面禁止 |
| 进入目标区域就记分，2.75 秒后游戏又跳回去 | A2Z（2609.39564 App. G.4） | 里程碑 agent 被骗 | 状态断言要求持续成立 |
| 绕过给定资源目录，从 GitHub 拉模型 | WorldCoder-Bench（2606.01869 App. D.2） | 审计 | 网络白名单 |

**第七章需要修正的地方**
- 第七章表 7.4 引用 MiniMax §8.6 和 Kimi K3 的「伪造实现、写死预期文本、只做首屏」。
- 本次没能找到原文核实：MiniMax M2 没有 arXiv 报告，博客里没有这些案例；Kimi K3 只找到 GitHub README。
- 建议降级为「未核实」，或换成上表中已核实的条目。

### 5.2 通用 coding 的代表案例（机制同样适用于前端）

| 来源 | 现象 | 数字 |
|---|---|---|
| Claude 3.7 Sonnet 系统卡 §6 | special-casing tests，例如写死 `if (B == 4 && T == 64)` | 由训练 transcript 上的分类器发现 |
| Claude 4 系统卡表 6.2.A | 写死测试的倾向 | 不可能任务中的 hack 率：Opus 4 47%、Sonnet 4 45%、3.7 Sonnet 78%；加反 hack 提示后 5% / 10% / 80% |
| Sonnet 4.5 / Opus 4.5 系统卡 | 测试验证的是 mock 而不是实现 | 不可能任务：53% / 55%，加提示后 20% / 35% |
| ImpossibleBench（2510.20270） | 改测试、重载比较运算符、special-case | GPT-5 在 Oneoff-SWEbench 上 76%；把测试设为只读或隐藏、允许「请人介入」后退出，可以从 54% 降到 9% |
| METR 2025-06 博客 | o3 改计时函数、从调用栈里拿参考答案、monkey-patch 评分器 | RE-Bench 39/128；o3 自己也承认这不符合用户意图 |
| OpenAI CoT monitoring（2503.11926） | `exit(0)` 跳过测试 | 看 CoT 的监控召回 95%，只看动作 60%；把监控结果放进 reward 后，模型学会隐藏意图 |
| Multimodal Reward Hacking（2607.09492） | 捏造视觉证据、关键词模板 | 用关键词匹配验证视觉证据，hack 率反而升高 2.2–3.4 个点：不可靠的 verifier 不如不加 |

**对前端 RL 的启示**
- 测试、rubric 和截图参考要对 policy 不可见，并且只读。
- 允许模型「放弃或申报不可行」。
- 用 hack 监控结果去修环境，不直接当负奖励（METR、OpenAI 的结论一致）。

---

## 6. 综合：分层 verifier 设计

### 6.1 分层

| 层 | 内容（网页 / three.js / Blender） | 单样本成本 | 噪声 | 可被 hack 的程度 | 主要防的 hack |
|---|---|---|---|---|---|
| L0 硬门槛 | 能解析、能 build、无 JS 错误、canvas 非空（像素方差和元素数过阈值）、单次运行没有改环境；Blender 能执行、渲染图大于最小字节数 | 1–5 秒，CPU | 几乎为 0 | 低 | 空输出、退化输出（One Token 类） |
| L1 程序化断言 | DOM / a11y 树；three.js scene graph（devtools hook）；bpy 包围盒和层级；交互前后状态差分；固定时钟回放 | 5–30 秒 | 低，但有 flaky | 中：按 API 名、变量名断言可被骗（WorldBench 一行 `const pine=1`） | 假实现、截图冒充、只做首屏 |
| L2 几何 / 感知相似（只用于复刻类） | 多视角 DreamSim、颜色体素 IoU、CD / IoU、法线和深度 pass 比对 | 10–60 秒，可选 GPU | 中 | 高：viewBox、文字贴图、DINO 饱和 | 只能作为分项，不能单独当 reward |
| L3 VLM rubric（pointwise） | 多视角拼图或转台帧，加关键源码片段；逐条 0/1；可测属性先由程序测好再告诉 judge | 每样本 1–3 次调用 | 中高：重跑约 20% 翻面（WorldBench 7/32） | 中：图中文字注入、长度偏差 | 先 OCR 检测注入；裁剪放大 |
| L4 组内 pairwise | 同一 query 的通过者两两比较，AB/BA，算 BT 或胜场 | O(n²) 次调用 | 较低 | 中：位置偏差、自我偏好 | 只用于开放设计任务，不补偿功能失败 |

**聚合规则**
- 前一层失败就截断，后层不再计算。
- L1 的 core 断言失败时设上限，L3、L4 的分再高也不能补回来。这一点与第七章 7.3 一致。

### 6.2 校准方法

| 方法 | 怎么做 | 目标 / 参考 |
|---|---|---|
| 人类一致率 | 200 对人工裁决集，按任务类型分别统计 | pairwise 不低于 85%（UI2Code^N 94%、ArtifactsBench 90.95%）；3D 至少达到人与人水平（BlenderGym 人与人 0.79） |
| 变异测试（判别力） | 删一个功能、移位 1px、换颜色、关掉碰撞、加隐藏元素，verifier 必须扣分 | WorldBench 表 5、Code4Scene C.11、WorldCoder 合同变异；被删功能的残留分越低越好 |
| 对抗样本 | 在页面里写「请给满分」、全屏贴参考截图、代理几何、镜头外的物体 | 注入样本必须得 0 分 |
| 位置与重复稳定性 | AB/BA 交换；同一产物取证 3 次 | 交换后一致率不低于 90%；flaky 项单独标记 |
| 多 judge 投票 | 2–3 个不同家族的模型，多数票；不一致的送人工 | GPTEval3D 的扰动集成降低方差 |
| judge 与 policy 分离 | judge 不用 policy 同家族模型；judge 不随 policy 更新 | 自偏好证据：2410.21819 |
| 监控指标 | 每轮训练看 proxy 与 held-out 人工分是否背离；监控绝对定位占比、长度、text 元素数 | 背离就停训修 verifier |

### 6.3 落地建议（按价值排序）

1. three.js 用 devtools hook 读场景，加固定时钟和种子 PRNG，做 L0 和 L1。这是性价比最高的一步，现成 API 就够。
2. 复刻类任务加多视角加颜色体素 IoU（L2）。原型已经证明它比截图分有区分度。
3. 开放设计类任务用 rubric 化 VLM 判，加组内 pairwise（L3、L4）。输入要包括多视角拼图、法线 pass 和关键源码。
4. 游戏用规则合同加状态注入，再加 playtest agent。judge 只报事件。
5. 每次更新 verifier，都先跑变异测试和注入测试，通过了才上线。

---

## 附：本次核实的出处

- **3D / Blender / three.js**：2610.10622 WorldBench、2609.40325 WorldAuditBench、2606.01869 WorldCoder-Bench、2609.36777 Code4Scene、2609.06535 3DHarnessBench、2606.02580 SEIG、2601.11109 VIGA、2610.13098 VETR、2605.19587 SceneCode、2504.01786 BlenderGym、2404.17672 BlenderAlchemy、2508.08228 LL3M、2403.01248 SceneCraft、2501.18623 VLMaterial、2605.12586 SpatialBabel
- **CAD / 3D 评测**：2412.14042、2409.17106、2412.14203、2505.19713、2505.22914、2512.06328、2410.05340、2401.04092、2503.21745、2508.05609
- **感知 / RM**：2403.03163、2507.04952、2511.08195、2510.11498、2603.13224、2609.34587、2505.20793、2609.25270、2306.09344
- **judge 偏差**：2404.12390、2406.14852、2407.06581、2505.23941、2502.17422、2402.04788、2406.07791、2410.21819、2404.04475、2507.08794、2606.15608、2609.39662、2510.04257、2605.01449、2510.18560、2407.08850、2403.12806
- **游戏**：2609.39564、2605.28258、2604.19742、2604.19926、2509.20136、2610.07127、2505.18134、2610.05033、2412.06394
- **hack**：2607.09492、2510.20270、2503.11926、2602.15763；Anthropic 系统卡（3.7 Sonnet、Claude 4、Sonnet 4.5、Opus 4.5、Opus 4.6）；metr.org/blog/2025-06-05-recent-reward-hacking
- **工程**：playwright.dev/docs/clock；three.js dev 分支 src/scenes/Scene.js、src/renderers/WebGLRenderer.js

