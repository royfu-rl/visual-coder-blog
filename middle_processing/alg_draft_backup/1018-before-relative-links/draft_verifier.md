<a class="anchor" id="vf-1"></a>

## 1 A Screenshot Is Not a Reward Signal

[WorldCoder-Bench](https://arxiv.org/abs/2606.01869) 把「截图加 VLM（GPT-5.4）」当作对照判据，在 1,434 个〈模型，任务〉对上重打分，通过率只有 2.7%（[WorldCoder-Bench 表 2](https://arxiv.org/abs/2606.01869)）。这个数字不说明模型差，它说明判据坏了：原文的解释是它「不加区分地惩罚视觉差异」，等于一律判差，所以这套 reward 对策略的改进完全不敏感。换个方向偷懒同样失效：[WorldBench](https://arxiv.org/abs/2610.10622) 从一个世界里删掉或禁用 5 个功能（满分合计 7.11），只读源码的 judge 仍给出 5.44 分，因为源码里那段逻辑还在、看上去写得很完整（[WorldBench 表 5](https://arxiv.org/abs/2610.10622)）。

把几条通道放在同一个真值上比，差距是数量级的（均出自 [WorldCoder-Bench 表 2](https://arxiv.org/abs/2606.01869)）：

- 截图加 VLM 与真值的 Kendall τ_b 是 −0.068，即负相关，成本是 DOM 基线的约 50 倍。（[表 2](https://arxiv.org/abs/2606.01869)）
- 读取隐藏的运行时状态契约，τ_b 是 1.000、假阳率 0，成本约 2 倍。注意它本身就是该基准的真值，τ=1 是定义使然；有意义的是另外三条通道都复现不了它的排序。（[表 2](https://arxiv.org/abs/2606.01869)）
- 一个贵 25 倍而且方向都不对的信号，不该进 reward。（50 倍对 2 倍，[表 2](https://arxiv.org/abs/2606.01869)）

我们自己的实验给出了同一方向的数据（[本项目实验记录 §2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。三个 three.js 场景、47 个带人工标签的变异，只看页面自带相机的一张截图做逐像素相似度，在前两个场景的 29 个变异上判对 12 个。它不是不够准，它是在量纲上失明：雪人的胡萝卜鼻子只占几十个像素，把它挪到后脑勺，页面截图相似度仍然是 0.999。

这一节要立住的判断只有一条：**视觉产出的 reward，不能由一张图决定。** 它不是说图没用，而是说图只能作为分项，不能作为判据。

<a class="anchor" id="vf-2"></a>

## 2 Reliable Signal Comes From Runtime State

把 Verifier 拆成互相独立的几层，每层查一个不同的量，判别力才涨得上来。我们在两个场景（雪人、桌子加杯子）上各写一组变异，人工标注「该挂」还是「不该挂」（[实验记录 §2.1](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)，变异脚本 [mutate.py](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/mutate.py)）。该挂的是部件缺失、挪位、朝向反、比例变、颜色换、杯子悬空或陷进桌面；不该挂的是网格精细度、光照强弱、背景色、相机机位、轻微色差、尺寸正负 5%。

核心发现：判别力随信号层数单调上升，方向可信，但「上升」这件事在这个样本量下并不显著——分层组合 29/29 对按色体素 25/29，4 个不一致对全部同向，配对精确检验 p 为 0.125（[红队复核](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/18_redteam.md)）。

| 程序化信号 | 雪人 13 例 | 桌子 16 例 | 合计 |
|---|---|---|---|
| 页面单张截图逐像素相似度 | 5 | 7 | 12/29 |
| 几何类名多重集一致 | 6 | 8 | 14/29 |
| 多视角剪影 IoU | 9 | 10 | 19/29 |
| 按色体素 IoU | 11 | 14 | 25/29 |
| 分层组合 | 13 | 16 | 29/29 |

来源：[实验记录 §2.1](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)。

数据解读：按 API 名字断言「场景里有几个球、几个圆柱」只能到 14/29，因为它查的是实现路径而不是结果，换一种建模手法做出同一个形状就会误杀。多视角剪影补上了单视角看不见的方位错误，按色体素补上了形状对而颜色错的情况，两者叠起来仍漏 4 个，缺的是部件级拓扑。这条曲线说明一件事：加视角、加分辨率都不如加一个量纲不同的新量。（[实验记录 §2.2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）

前两个场景的 29/29 必须打折扣，因为阈值在它们身上看过一眼：分块 IoU 的下限在这两个变异集上扫过三档，颜色容差是看到「轻微调色被误杀」之后加的（[实验记录 §2.4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。所以我们又做了一次干净的留出测试。新场景是一辆小车，9 个 mesh；18 个变异和它们的标签先写死再跑，阈值沿用前两个场景，一个没动，只跑一次。结果 18/18（[实验记录 §2.3](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)，逐例数值见 [car_mut/mutation.json](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/runs/car_mut/mutation.json)）。

下面这个 demo 用的就是这组留出数据，图是真实渲染，数字是真实测得。点一个变异，左边五张图里第一张是页面自带相机，其余四张是 Verifier 自己摆的机位。demo 里四个该挂的变异，第一张的相似度都在 0.996 以上（[mutation.json](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/runs/car_mut/mutation.json)），单看它分不出对错。

<iframe class="demo-frame" style="height:470px" src="demos/verifier-layers.html" loading="lazy"></iframe>

留出集同时证明了每一层都不是摆设：

| 留出变异 | 挂在哪一层 | 为什么别的层抓不到 |
|---|---|---|
| 前灯少一个 | 部件连通块数 | 剪影 0.998、分块 0.924、该色体素 0.5 全在阈值之上 |
| 风挡挪到车尾 | 按色体素 | 剪影 0.992，外轮廓几乎没变，但玻璃色体素 IoU 为 0 |
| 风挡改成车身色 | 按色体素 | 剪影和分块都是 1.0，形状完全没动 |
| 少一个轮子 | 分块体素 | 全局剪影 0.903 刚好过线，分块最差块是 0.0 |
| 轮子轴向转 90 度 | 多视角剪影 | 外轮廓直接变了 |

来源：[实验记录 §2.3](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)。

数据解读：五个变异挂在四个不同的层上，没有任何一层能独自覆盖。最接近误杀的一例是「轮子半径加 4%」，分块最差块 0.727，阈值 0.5，还留着余量。这意味着分层不是为了堆保险，而是因为错误本身分布在不同的量纲上。（[实验记录 §2.3](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）

<a class="anchor" id="vf-3"></a>

## 3 Blender Reproduces the Same Conclusion

同样的方法换一个技术栈重做一遍（[Blender 实验记录 §3](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/10_blender_tasks.md)，判据代码 [blender/verify.py](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/blender/verify.py)）。Blender 侧的场景是一张木桌加台灯加陶瓷杯，22 个变异，11 个该挂、11 个不该挂；其中 15 个是开发集，7 个是选完判据之后才造的留出集。

核心发现：两个极端都不成立，中间那条路才对。

| 信号 | 总判对 | 检出 11 个该挂 | 保真 11 个不该挂 |
|---|---|---|---|
| 只看一张截图 | 12/22 | 2 | 10 |
| 多视角剪影 IoU | 14/22 | 3 | 11 |
| 全局 Chamfer | 13/22 | 2 | 11 |
| 全局 F-score | 11/22 | 0 | 11 |
| 分部件 F-score | 18/22 | 7 | 11 |
| 全量状态断言 | 11/22 | 11 | 0 |
| 分部件几何加四族断言 | 21/22 | 11 | 10 |

来源：[Blender 实验记录 §3.4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/10_blender_tasks.md)。

数据解读：全量状态断言把 11 个真错全抓住了，代价是 11 个语义未变的改写全被误杀，净判别力等于零。误杀集中在两类写法差异：把边长 1 的立方体放大 1.2 倍，改写成边长 2 的立方体缩小 0.6 倍，世界几何逐点相同而物体自身的缩放值差一倍；圆柱从 16 段改 32 段，顶点数全变而形状不变。断言查的是代码留下的痕迹，不是结果。（[Blender 实验记录 §0、§3.4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/10_blender_tasks.md)）

几何指标则栽在另一个地方：平均量会把局部错误稀释掉。杯子只占全场表面积约 2%，把它在桌面上挪 30 厘米，全局 Chamfer 只从 0 涨到 0.00018，分部件算是 0.084，差 460 倍（[Blender 实验记录 §4.3](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/10_blender_tasks.md)）。全局 F-score 更极端，11 个该挂的一个都没检出。

所以可迁移的规律有两条，而且在 three.js 和 Blender 两侧各自独立成立：**几何指标必须分部件算；断言只能查任务描述钉死的字段。** 第二条的证据是留出集上唯一的误杀——日光功率从 3.0 调成 3.5 被判挂，而 Problem Statement 里根本没写功率（[Blender 实验记录 §3.3](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/10_blender_tasks.md)）。修法不是放宽容差，是在造题时就产出被钉死的字段清单，Verifier 只查清单内的字段。Verifier 能查的信息量必须小于等于 Problem Statement 给出的信息量，否则这道题进了 RL 就是纯噪声；three.js 侧预实验里两次失败也是同一个原因（[实验记录 §5](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。

<a class="anchor" id="vf-4"></a>

## 4 A VLM Judge Finds the Check You Forgot

VLM judge 远强于像素指标（[实验记录 §3](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)，脚本 [vlm_judge.py](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/vlm_judge.py)）。把参考与候选的渲染图上下拼成一张交给模型判 pass 还是 fail，48 个 case、4 个 judge、每种看图条件每例两次、温度 0，共 768 次判定，单模型判对 74 到 92 次（分母 84 到 96，少掉的是没解析出结论的）；而逐像素相似度在其中 29 个变异上只有 12/29。像素指标判不出「鼻子不见了」，VLM 一眼就说出来。

这一节的结论推翻过一次，过程值得写出来（[实验记录 §3.1](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。最早只跑了 18 个 case，看到多视角拼图的判对率不升反降，于是写下「多视角对 VLM 无效」。把样本扩到 48 例、并修正一处人工标注错误之后，结论反过来了。

核心发现：多视角对 VLM 有效，但它买到的不是判对率，而是稳定性。

| judge | 单视角判对 | 多视角判对 | 单视角重测翻面 | 多视角重测翻面 |
|---|---|---|---|---|
| gpt-6-astra | 84/95 | 92/96 | 16.7% | 4.2% |
| gemini-3.8-flash | 88/96 | 92/96 | 8.3% | 0.0% |
| doubao-seed-2.1-pro | 78/91 | 81/84 | 6.2% | 8.3% |
| claude-opus-5-5 | 76/96 | 74/93 | 16.7% | 20.8% |
| 4 模型 8 票多数投票 | 44/48 | 46/48 | — | — |

来源：[实验记录 §3](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)。

数据解读：逐 case 配对比较，单视角赢 11 例、多视角赢 27 例；把每个 judge 的每个 case 当成独立配对做 McNemar 得 p=0.015，但这样算高估了独立性（四个 judge 判的是同一批 case），逐模型单独看没有一个到显著（p 从 0.13 到 0.61，[实验记录 §3.1](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。所以这张表支持的说法是「多视角不差于单视角，对强 judge 更好」，不支持「多视角一定更好」。

真正稳的结论是第三、四列。同一个模型、同一张图、温度 0 跑两次，最差一档有 20.8% 的 case 会翻面。单次 VLM 判定不能当 reward，这和用几视角无关。而多视角把两个最强 judge 的翻面率从 16.7% 压到 4.2% 和从 8.3% 压到 0。（[实验记录 §3.2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）

投票也救不回全部（[实验记录 §3.3](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。4 个模型 8 票多数投票在 48 例上单视角 44 对、多视角 46 对。拿它和程序化信号的 47/47 直接比是不成立的——两个集合不同、组成不同，而且其中一个是程序化信号自己调过阈值的集合；按配对检验，这个差别完全不显著。能比的只有定性的那一面：投票漏掉的那几例全是同一类——**定量的几何偏差**：一条桌腿缩短到 70%，8 票全判通过；桌面厚度减到原来的三分之一，5 票判通过。这两例程序化信号都抓到了，前者靠分块体素 0.167，后者靠按色体素 0.528。

还有一个对照更能说明 VLM judge 在靠什么判。把参考图拿掉，只给候选的渲染图加一段文字需求，其余全部不变——同样两个 judge、同样的 case、同样的候选图（[实验记录 §14](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)，脚本 [judge_noref.py](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/judge_noref.py)）。

45 个带标签的 case，两个 judge（[实验记录 §14](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。核心发现：拿掉参考图，判别力从九成五掉到七成上下，掉的主要是检出。

| 条件 | 总判对 | 检出 | 保真 |
|---|---|---|---|
| 有参考图，单视角 | 94% | 58/63 | 43/44 |
| 有参考图，四视角 | 97% | 61/64 | 44/44 |
| 无参考图，单视角 | 68% | 35/56 | 30/40 |
| 无参考图，四视角 | 76% | 34/56 | 39/40 |

来源：[实验记录 §14](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)。

数据解读：检出从九成二掉到六成上下，而四视角下的保真仍有 39/40——没有参考的 judge 变成了一个偏宽松的放行器，不怎么冤枉好人，但一多半的缺陷放了过去。单视角下连保真也只剩 30/40，说明没有参照时它两头都在猜。机制很直接——拿掉参考之后它只能对着那段几十个字的需求判，而需求没写桌子多高、杯子多大，于是尺寸与位置类的缺陷全都「不违反需求」。**这正是本文那条规则从 judge 这一侧看到的样子**：判据能查的信息量，不会超过题面给出的信息量；并排放上参考图，等于把题面的信息量提高到逐像素，judge 这才有东西可查。（[实验记录 §14](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）

这和训练那一侧的实验是同一件事（[实验记录 §7](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。生成方在没有可比对象时，首轮挂掉后只能救回 2/37；判别方在没有可比对象时，检出从九成二掉到六成。**模型缺的不是能力，是参照。**

真正体现 VLM 价值的是那次翻案（[实验记录 §3.4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。最早被记成「多视角投票判错」的那一例，是我们自己标成「正确改写」的版本：它用旋转成型几何（LatheGeometry）把三个球的轮廓一次转出来，外观和参考一致，只是建模手法不同。多视角条件下 8 票里有 7 票说它有问题，而单视角条件下投票判它通过。后来把俯视图放大看，它头顶真的有一个洞，旋转成型在极点没有封口——那个洞只在俯视图里看得见。标签改成了「该挂」，上面那张表用的是改正后的标签。

当时的程序化 Verifier 对它是结构性失明的。双面剪影把洞填上了；换成单面剪影，IoU 也只从 0.997 掉到 0.958，因为洞只占几十个像素，被全局 IoU 淹没；体素 IoU 是 0.995，同理。修法不是把阈值从 0.96 调到 0.97——那样会立刻误杀一批合法改写。修法是换一个不随尺寸衰减的量：只被一个三角面用到的边，也就是开放边界边数。闭合实体是 0，这个版本是 64，直接判挂（[实验记录 §2.2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。

这里必须自曝一处方法学问题。这个信号是**在它要验证的那个 case 上造出来的**，而那个 case 就在雪人那 13 例里面。所以「加上这个信号之后两个变异集仍然是 13/13 和 16/16」不是独立验证，是在调参集上报调参集的成绩，违反了本文自己在讲任务构造时定下的红线——不许用正在调阈值的集合做验收。它唯一算得上独立的证据，是后来那个小车留出集上没有因为这个信号产生新的误杀。要真正验证它，得另造一组专门含破洞与开口面的变异，标签先写死再跑。（[实验记录 §3.4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)；红线违反的复核见 [红队审查 §1.4–§1.5](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/18_redteam.md)）

这件事定义了 VLM judge 的位置。它能发现「这里不对劲」但说不清是什么；程序化信号能精确指出哪一项超了，但要先有人想到查这一项。**VLM judge 的价值是帮你找到该加哪条程序化检查，不是直接当 reward。** 它也不是人工标签的替代品：标注者和自动指标会在同一个地方同时瞎掉，这次就是 4 个 VLM 对、一个人错。（[实验记录 §3.4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）

<a class="anchor" id="vf-5"></a>

## 5 Capture the Scene Without the Model's Cooperation

常见做法是在任务契约里要求模型把场景对象挂到一个约定好的全局变量上，例如 [WorldCoder-Bench](https://arxiv.org/abs/2606.01869) 的 `window.__3D_STATE__`。这条路不能走，两个原因都是机制层面的：训练时模型会学会「写这一行就行」，评测换一套 Harness 立刻失效；而且那个对象是模型自己造的，它可以伪造。WorldCoder-Bench 自己就记录了有模型不按约定挂出全局引用的失败（[WorldCoder-Bench 附录 D.2](https://arxiv.org/abs/2606.01869)）。

我们改用 three.js 自带的 devtools 事件通道。场景与渲染器的构造函数本身会向这个通道派发事件（见 three.js r160 源码 [Scene.js](https://github.com/mrdoob/three.js/blob/r160/src/scenes/Scene.js)），在页面脚本执行之前预先把接收端定义好，就能拿到每一个场景和渲染器实例（实现见 [harness.js](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/harness.js)）。它不要求模型配合，事件由库自己发出。伪造并非不可能——页面可以把接收端整个换掉——但那样我们一个场景也收不到，直接挂在硬门槛上，是向安全侧失败。实测页面无论用 CDN、importmap，还是把整个库内联打包进去、完全不发网络请求，抓到的 mesh 数和体素结果都一致（[实验记录 §1.3](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。

光是拿到场景还不够，Verifier 必须确认看到的画面就是页面真正交付的画面。我们手写了 7 个作弊页面做攻击测试，6 个被挡，有一个一度成功骗过 Verifier：它另起一个离屏渲染器，渲染一份正确的场景，而文档里那块可见画布画的是别的东西（[项目日志 STATE.md](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/STATE.md)）。

修法是两条一起上（同上；离屏计数见 [harness.js](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/harness.js)）。第一条，只认挂在文档里、有实际尺寸、未被隐藏的那块画布，离屏的一律不计入判定。第二条，把离屏渲染的次数本身当成蜜罐信号——正常解法不需要它，一旦出现就是明确的行为标记，而不是等着某条断言恰好识破。修完之后 7 个作弊页面全挡。

手写攻击只能覆盖想得到的路径，所以又让模型自己来找（[实验记录 §13](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)，脚本 [hack_probe.py](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/hack_probe.py)）。把判据的构成原原本本告诉它，要求写一个「能过验收但实际不满足需求」的页面，三个场景乘四个模型共 12 次请求，其中两个模型全程没有产出，实际拿到 5 份可判定的作弊页，**verifier 判过 0 份**，全部挂在多视角剪影那一层。它们试的路子是：用贴图画出看起来对的东西（3 份）、往约定好的全局变量里塞一个正确场景（1 份）、直接操作画布读写（3 份）、玩绘制顺序（1 份）；一份作弊页可以同时用几条路子。

这个零要克制地读。分母只有 5，而且模型只试了一次、没有梯度、也看不到判定反馈；RL 里的策略有成千上万次尝试和明确的分数信号。它还说明一件事：模型找的路子和我们手写的七条高度重合，两边受限于同一套直觉。**真正有价值的对抗样本只能从训练里来**，所以防 hack 的工程重点不是上线前想全，而是上线后抽检高分样本。（[实验记录 §13](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）

这两件事合起来说明：取证通道的可信度不能依赖产物的自觉。Verifier 要从库的内部机制和可见画布这类外部事实取证，不要从模型写的约定取证。7 个作弊页面全挡，说明的是这 7 条路径被堵住了，不是「不可 hack」——其中一条在修补之前真的骗过了 Verifier，同类漏洞一定还会有。（手写攻击见 [STATE.md](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/STATE.md)，取证实现见 [harness.js](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/harness.js)，攻击面分析见 [Reward hacking 防御笔记 §1.3](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/11_hacking_defense.md)）

<a class="anchor" id="vf-6"></a>

## 6 All of This Runs on CPU

视觉验证常被当成需要 GPU 沙箱的脏活。本机的实测结论相反：整套流程只用 CPU 就够。

核心发现：取证成本在秒级以下，塞得进 RL rollout 的每步观测。

| 环节 | 实测吞吐 | 来源 |
|---|---|---|
| 单次 three.js 探测，含启动浏览器 | 0.8 到 1.0 秒 | [实验记录 §1.5](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) |
| 复用浏览器（8 浏览器乘 8 页），每任务含重载加 8 视角加场景图 | 约 14 任务每秒 | [Harness 实测 §4.1.3](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/06_harness.md)，[bench_pool.js](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/bench_pool.js) |
| 读场景图（13 个 mesh，含世界包围盒） | 1.8 毫秒 | [Harness 实测 §4.1.1](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/06_harness.md) |
| Blender Workbench 渲染（32 进程并发） | 15.5 视角每秒 | [Harness 实测 §4.2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/06_harness.md) |
| Blender 几何指标全套（6 万点采样加三项指标） | 约 0.4 秒每候选 | [Blender 实验记录 §4.4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/10_blender_tasks.md) |

数据解读：机器无 GPU，Chrome 走无头加软件渲染。结构化观测比图像便宜一到两个数量级——读一次场景图 1.8 毫秒，单视角截图 62 到 85 毫秒，8 视角转台约 0.2 到 0.5 秒（[Harness 实测 §4.1.1](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/06_harness.md)），所以「先给结构、再给像素」不只是精度上的选择，也是成本上的选择。Blender 侧的几何指标比渲染便宜约 3 倍，而判别力更高（分部件 F-score 检出 7/11，多视角剪影只有 3/11，[Blender 实验记录 §4.4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/10_blender_tasks.md)）。如果只能留一个视觉信号，留几何，不留渲染。

确定性要靠 Harness 主动控制，不能指望页面（[Harness 实测 §4.1.4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/06_harness.md)，[bench_clock.js](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/bench_clock.js)）。只冻结时钟不够：对一个用动画帧回调加随机数的页面，仅安装虚拟时钟时三次截图三个结果，加上暂停与定点推进之后 20 次里仍有 2 种。能做到逐字节一致的只有「由页面钩子或 Harness 显式推进帧，并直读画布像素」（同上；Harness 接管帧调度与随机源的做法见 [实验记录 §1.1](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。拿不到这种控制时，Verifier 必须用感知容差比对，不能比哈希。

<a class="anchor" id="vf-7"></a>

## 7 An Independent Benchmark Converged on the Same Design

[3JSBench](https://3jsbench.com/) 是本项目检索范围内唯一把 Astra 与 Claude Opus 5.5 放进同一套确定性几何判据的公开评测：100 道题、每题三次一次成型的尝试、10 个模型（[3JSBench 榜单](https://3jsbench.com/)，2026-10-15 读取，站方注明 2026-10-14 改判；读取过程见 [核实记录](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/91_3jsbench_verified.md)）。它的管线是独立做出来的，结构却和本项目几乎逐项重合。

核心发现：两边在不知道对方的情况下选了同一套取证方式，连视角数都一样。

| 它的做法（[3JSBench 方法页](https://3jsbench.com/methodology)） | 本项目 | 是否一致 |
|---|---|---|
| 隔离的无头浏览器跑模型写的程序 | 无头浏览器，断网，页面从内存加载 | 一致 |
| 记录场景并渲染九个固定视角 | 捕获场景，Verifier 自己摆九个相机 | 一致 |
| 在捕获到的场景上做确定性测量 | 读场景图、体素、部件、拓扑 | 一致 |
| 全部必查项通过才算通过 | 分层，任一层否决即判失败 | 一致 |
| 咨询性诊断不参与判定 | 感知相似只作分项 | 一致 |
| 基础设施故障的尝试单独排除 | 硬门槛单列，不混进判定 | 一致 |
| 用一个绑定模型把题面点名的部件对到场景的网格上 | 按颜色分部件，没有这一层 | 不一致 |

本项目一列的依据：[实验记录 §1–§2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)。

数据解读：唯一的结构差异是部件绑定。它让模型只做绑定、不做打分，这是一个比两边现有方案都好的折中——语言模型负责把「题面说的那个盖子」对到具体网格，判定本身仍然是确定性的。本项目按颜色分部件在颜色复用的场景上会失效，这条该抄。

它的 695 条必查项分六族，分布很说明问题（[3JSBench 方法页](https://3jsbench.com/methodology)）。部件计数 223 条、结构 160 条、空间关系 157 条，三族合计占 78%，全部是「有几个、接在哪、挨着谁」。没有一条查「像不像」。

同样值得抄的是它的失败统计（[3JSBench](https://3jsbench.com/)）。3000 次尝试里最常见的五类失败是物体互相穿插 20%、可见背面 19%、表面闪烁 17%、朝向与题面不符 16%、部件断开 16%。前三类全是渲染层面的物理不自洽，而本项目的判据里只覆盖了可见背面一项。

按这个清单补了两个信号，各用一个故意做坏的场景验证（[项目日志 STATE.md](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/STATE.md)，判据代码 [verify.py](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/verify.py)）。把桌面正上方零距离再铺一块同样大的面，整体穿插比例从参考的 0.053 涨到 0.762，改变绘制顺序后有 5534 个像素发生变化，两个信号都把它判挂。三个变异集回归后仍是 13/13、16/16、18/18，没有新增误杀。

有一个信号没能做成（[STATE.md](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/STATE.md)，判据代码 [verify.py](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/verify.py) 里 pair_overlap 只作诊断量）。按部件两两算穿插比例，在 48 的体素分辨率下不可用：薄部件会被量化成单层，看起来像被另一个部件完全包含，参考解自己的最大值就是 1.0。所以它只能当诊断量。这条限制本身是有用的——体素分辨率决定了能查什么，细部件的接触判定得换别的办法，比如包围层次加精确相交测试。

另外一个数字替嵌入相似度盖了棺（[3JSBench 方法页](https://3jsbench.com/methodology)）。站方把 [SigLIP 2](https://arxiv.org/abs/2502.14786) 相似度明确标注为不参与判定的描述性信号，而三个模型的均值差是 Astra 加 0.011、Opus 5.5 加 0.009、GPT-6 Sol 加 0.007，对应的通过率却是 80.0%、49.0%、27.0%。通过率差 53 个百分点，嵌入相似度只差 0.004。

<a class="anchor" id="vf-8"></a>

## 8 How the Layers Divide the Work

把上面的结论装成一套可执行的分层判据。前一层失败就截断，后层不再计算；靠前的层给出的否决，后面的分数再高也不能补回来。

核心发现：成本、噪声和可 hack 程度三者沿着层次同向上升，所以越靠后的层越不能单独定生死。

| 层 | 查什么 | 单样本成本 | 噪声 | 可被 hack 的程度 |
|---|---|---|---|---|
| 硬门槛 | 能执行、无运行时报错、渲染发生过、可见画布非空 | 1 到 5 秒，纯 CPU | 几乎为 0 | 低 |
| 程序化断言 | 运行时状态：部件存在与数量、世界包围盒、层级、拓扑量、修改器与动画通道 | 5 到 30 秒 | 低，有少量 flaky | 中：按 API 名或变量名断言可被骗（[WorldBench](https://arxiv.org/abs/2610.10622)） |
| 感知与几何相似 | 多视角剪影、按色体素 IoU、分部件 Chamfer 与 F-score | 10 到 60 秒 | 中 | 高：视口尺寸、贴图文字、特征饱和 |
| VLM rubric | 多视角拼图加关键源码片段，逐条 0/1；可测属性先由程序测好再告诉 judge | 每样本 1 到 3 次调用 | 中高，本项目重测最差一档 20.8% 翻面（[实验记录 §3](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)） | 中：图中文字注入（[AgentTypo](https://arxiv.org/abs/2510.04257)）、长度偏差（[MLLM-as-a-Judge](https://arxiv.org/abs/2402.04788)） |
| 组内 pairwise | 同一 Problem Statement 的通过者两两比较，顺序正反各判一次 | 比较次数随通过者数量平方增长 | 较低 | 中：位置偏差（[Judging the Judges](https://arxiv.org/abs/2406.07791)）、自我偏好（[Self-Preference Bias](https://arxiv.org/abs/2410.21819)） |

来源：分层结构与成本、噪声档位是调研笔记里的设计估计（[Verifier 调研 §6.1](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/04_verifier.md)），不是本机逐层实测；本机实测的单次探测是 0.8 到 1.0 秒（见第 6 节）。

这套判据的重复性也量过（[实验记录 §12](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)，脚本 [flaky.py](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/flaky.py)）：9 个产物各探测 3 次，判定零翻面、信号值逐位相同。做到零靠三件事——冻结时钟让帧只在取证方推进时前进、固定随机种子、除了库本身断掉所有外部请求。限制是这只覆盖同一机器同一浏览器版本，跨版本的确定性没测过，镜像升级后要重新量。

数据解读：硬门槛和程序化断言占掉了判别力的绝大部分，而成本在秒级、噪声接近零，所以它们应该承担否决权。感知相似只能作分项，因为它的失效模式是被尺寸稀释（杯子挪 30 厘米、头顶一个洞都在这一层逃掉）。VLM rubric 和 pairwise 只适合开放设计类的排序，不能用来补偿功能失败。（判别力依据 [实验记录 §2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)、[Blender 实验记录 §3.4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/10_blender_tasks.md)；分层原则见 [Verifier 调研 §6.1](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/04_verifier.md)）

每次改动 Verifier，先跑变异测试和注入测试，过了才上线。被准入测试弃掉的 case 比新造的任务更值钱：它们精确指出了 Verifier 的盲区（[实验记录 §4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。两个场景的造题里，被弃的「杯子倒置」暴露了圆台翻转不改变占据，被弃的「细长部件缺失」直接催生了部件连通块这一层。先造题再补 Verifier，比先定 Verifier 再造题有效，因为盲区是被具体 case 逼出来的，不是设计阶段想出来的。

还要说清楚哪些结论现在不该拿去外推。

- 三个 three.js 场景和一个 Blender 场景，变异都是我们自己造的单处改动，真实策略产出的错误分布不一定长这样。47/47 里只有 18 个是真正留出的，其余 29 个的阈值在同一批变异上看过一眼。（[实验记录 §2.3–§2.4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)，[红队审查 §1.4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/18_redteam.md)）
- 判别力是在「单处改动」上测的。多处错误同时出现时各层会不会互相掩盖，没有测过。
- VLM judge 的数字来自 48 个 case、4 个模型、两种看图条件各 2 次，合计 768 次判定。它支撑「单次判定不可用」和「多视角不差于单视角」，但支撑不了「8 票投票就够了」这种配置级结论——逐模型的配对检验没有一个到显著，合计那一次又高估了独立性。（[实验记录 §3、§3.1](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）
- 分部件几何的阈值是按「该放行那一档的下沿」取的，这个取法在部件数更多、尺度差更大的场景上会怎么退化，未测。

还有一族信号成本近乎为零却还没接：渲染器自己的计数器。绘制调用数、三角面数、几何体与贴图的实例数，这些数字在拿到渲染器的那一刻就能直接读出来，不需要额外渲染。它对应 [3JSBench](https://3jsbench.com/methodology) 六族判据里渲染质量那一族中的网格预算，也对应 OpenAI 官方 [Frontend prompt 指南](https://developers.openai.com/api/docs/guides/frontend-prompt)里 three.js 验收的「资源渲染不重叠」那条。它能抓的那类错误很具体：同一个形状被重复加载成几百个实例、贴图没有复用、三角面数比参考高一个数量级。3JSBench 的实测给出了量级——Muse Spark 1.3 中位数用 995 个网格、177000 个三角面，而最强的两个只用 45 个和 24 个，而且堆网格的那一个有 33% 的尝试出现绘制顺序闪烁（[3JSBench](https://3jsbench.com/)）。堆实例与闪烁同时出现，指向同一个成因。

下一步的三件事都指向同一个缺口——现在的证据全部来自我们自己构造的变异，而不是策略真实的失败模式。一是把 Verifier 接到完整的 rollout 上，统计每一层在真实产物上的触发分布与假阳率；二是把被钉死字段的清单做成造题阶段的强制产物，让 Verifier 的信息量与 Problem Statement 严格对齐；三是把开放边界边数这类不随尺寸衰减的拓扑量补成一组，因为目前只验证了一个这样的量，而它一次就救回了四层信号同时失明的那一例。

<a class="anchor" id="vf-9"></a>

## 9 At Scale, a Blind Spot Becomes Missing Data

前面所有判别力数字都在回答同一个问题：Verifier 判错的概率有多大。到了十万任务的量级，这个问题问错了。

准入测试的第一条是「参考解必须通过 Verifier」（[实验记录 §4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。把它和一个系统性盲区放在一起，后果不是多一点噪声。下面这条机制链是**本项目推断**，第 1、2 步有实测（下表第一行），第 3 到 5 步是外推，没有在十万量级上量过（推断过程见 [红队审查 F1](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/18_redteam.md)，相关的留一层消融见 [实验记录 §8](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）：

1. Verifier 对某一类几何有系统性盲区，例如开口曲面的体素填充无效。（实测，[实验记录 §6.1](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）
2. 这一类的**参考解自己**就过不了准入。（实测，[实验记录 §6.1](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）
3. 整类任务被静默丢弃，一条都不进数据集。（推断，[红队审查 F1](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/18_redteam.md)）
4. 数据集的各项指标反而更漂亮，因为留下来的全是 Verifier 看得准的那些。（推断，[红队审查 F1](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/18_redteam.md)）
5. 缺失不以噪声的形式出现，而以**某个几何类别从分布里消失**的形式出现。（推断，[红队审查 F1](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/18_redteam.md)）

核心发现：本项目已经实测到的六个盲区，每一个都对应一整类会被成批排除的场景。

| 已实测的盲区 | 怎么发现的 | 会被静默丢掉的场景类别 | 记录 |
|---|---|---|---|
| 开口曲面的体素填充无效 | 一道任务 32 组全挂，包围盒与参考逐位接近而该色体素 IoU 只有 0.017 | 一切用旋转成型、挤出、开壳、单面片建模的场景 | [实验记录 §6.1](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) |
| 小部件上的占据类指标退化成等值判断 | 同一道题修完上一条仍然 0%：那个部件只占 20 个体素，任何可见的朝向差都让 IoU 掉到 0 附近 | 一切以小部件的朝向或位置为考点的任务 | [实验记录 §6.2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) |
| 文本记录跨帧累加 | 图表线的参考解报出 360 个数据标签，实际只有 12 个 | 一切带动画的图表与页面 | [图表实验 §4.4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/17_chart_verifier.md) |
| 文字包围盒没过变换矩阵 | 图表线的参考解报出 171 对文字重叠，实际 0 对 | 一切含旋转、含嵌套层级的场景 | [图表实验 §4.4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/17_chart_verifier.md) |
| 体素分辨率下薄部件被量化成单层 | 按部件两两算穿插时，参考解自己的最大值就是 1.0 | 一切以薄壳、薄板、细杆为主的场景 | [STATE.md](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/STATE.md) |
| Harness 的库加载覆盖不全 | 连撞三处：只认 ES 模块、拦截规则写死了路径结构、断网把官方 addon 一起拦了 | 一切不用 ES 模块写法、换一个 CDN、或用到 addon 的产物 | [实验记录 §11](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md) |

最后那一条是做对抗测试时撞出来的，性质和前五条一样但来源不同：它不在判据里，在取证链路里（[实验记录 §11](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。我们的 Harness 原先只拦 ES 模块那一条引入路径；放开之后又发现拦截规则把路径结构写死了，换个 CDN 就漏；再放开之后又发现断网把官方 addon 一起拦了。三处都是正常写法。结果是正常的产物在执行门上就挂了，看起来像「模型连页面都写不对」。**取证链路覆盖不全，是一类特别容易被误读成模型能力问题的假阳性。**

数据解读：六条叠起来，带动画、含旋转、薄壳、开口面、小部件、不用 ES 模块写法的场景几乎会被成批排除——而这正是真实前端与 three.js 作品的主流形态。六个盲区全部是假阳性，也就是把正确产物判挂；六个全部不是阈值问题，调阈值一个也修不掉；真因分三类——坐标系、帧、取证链路的覆盖面，没有一类是随机失效，全是整类失效。

所以 Verifier 的验收指标要多一条，而且它不是准确率：**准入拒绝率按场景特征分层之后必须是均匀的**。本项目目前的准入拒绝在两个场景上是 1/10 和 2/16（补上部件连通块层之后后者降为 0/16，[实验记录 §4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)），但从来没有按「有没有开口面、有没有动画、有没有嵌套旋转、部件厚不厚、用哪种方式引库」分层看过。只要某一层的拒绝率显著高出，那一层就是盲区，而不是「那类任务本来就难造」。

这条检查很便宜：复用已有任务，按特征打标，做一次分布检验。它比再多造一万个任务重要，因为在它做之前，数据集的任何分布统计都是幸存者统计。

<a class="anchor" id="vf-10"></a>

## 10 This Verifier Only Works for Repair Tasks

前面九节的判别力数字全部来自「修复单处破坏」。真实需求不长这样，真实需求是「按描述搭出来」。换成从零搭建重测，结果是零（[实验记录 §10](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)，脚本 [scratch.py](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/scratch.py)）。

做法很直接：起始页只保留渲染器、相机、灯光和材质，没有任何物体；需求用一段自然语言描述场景；另一档额外给参考解的四视角图。四个场景、四个模型、最多三轮。

核心发现：26 组全挂，23 组挂在第一层，而产物在人看来都是对的（[实验记录 §10、§10.1](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）。

| 问题描述 | 首轮通过 | 末轮通过 |
|---|---|---|
| 纯文本需求 | 0/13 | 0/13 |
| 文本加参考图 | 0/13 | 0/13 |

来源：[实验记录 §10](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)。

数据解读：把其中一道题的四个产物和参考并排渲染，四个都是木色桌面加四条腿加桌上一个蓝色圆柱杯，差别只在比例——桌子的高宽比、腿的粗细、杯子的大小与位置各不相同。Verifier 判挂的理由是它们和参考不够重合，而不是它们不满足需求。

原因不在阈值，在这套判据量的东西。它量的是**绝对几何的重合度**。这在修复任务上成立，是因为修复任务的初始状态除了一处之外全都和参考一致，所以「和参考重合」等价于「那一处改对了」。换到从零搭建，这个等价关系就断了：需求没有钉死任何尺寸，模型凭什么搭出和参考同样高的桌子。

这是前面那条规则的又一次应用——Verifier 能查的信息量必须小于等于题面给出的信息量。只不过这次不是某一道题越界，是整套判据的适用范围被越界使用了。

从零搭建该怎么判，[3JSBench](https://3jsbench.com/methodology) 已经给了答案，因为它本来就是一个从零搭建的评测：695 条必查项分六族，**没有一条查绝对位置**。部件计数 223 条、结构 160 条、空间关系 157 条，三族占 78%，查的全是有几个、接在哪、挨着谁。

| | 修复型任务 | 从零搭建型任务 |
|---|---|---|
| 初始状态 | 除一处外与参考一致 | 空场景 |
| 可以查 | 与参考的绝对几何重合度 | 部件计数、连接与间隙、接触与支撑、相对比例、拓扑 |
| 本文现有判据 | 适用，三场景 47/47 | 不适用，0/26 |
| 放松阈值能不能救 | — | 不能。松到让这四个都过，等价于把第一层关掉 |

来源：[实验记录 §10.3](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)。

这条限制比它看起来严重，因为它同时解释了另外两件事。自动造题之所以只造「修复单处破坏」，不是因为那样方便，是因为现有判据只支持那一种；前面量到的难度分布之所以双峰、中间带是空的（[实验记录 §9、§15](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)），根源也在这里——单处破坏天然没有「部分做对」。

所以补相对关系那一族判据，是比再造一万道题更靠前的事。在补齐之前，用这套数据训出来的模型学到的是「照着参考改对一处」，不是「按描述搭出来」。

照着这张表写了一个只看相对关系的原型（[relational.py](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/proto/relational.py)）：先把场景整体归一化，再从体素里按颜色取连通块当部件，查部件个数、体量占比、相对尺度、上下关系、接触关系和开放边界，全部是比例或序关系。

核心发现：方向确实对，但做到可用的工作量和当初做绝对判据那一套相当。

| 测试集 | 绝对重合度判据 | 相对关系判据 |
|---|---|---|
| 从零搭建的每一次尝试（80 次） | 0/80 | 13/80 |
| 三个场景的带标签变异（47 例） | 47/47 | 35/47 |

来源：[实验记录 §10.5](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)。

数据解读：方向立住了——同一批人看都对的从零产物，从一次都过不了变成能过一部分。但代价是实打实的：变异集从 47/47 掉到 35/47，漏掉的十二个有共同点，相对结构没变，腿还连在桌面上、杯子还接触桌面、比例还在容差内。**这不是实现不好，是定义上的交换**：换来对整体尺度的不变性，就放弃了对绝对位置与绝对尺寸的敏感。部件最多的那个场景仍然是 0，因为部件一多，匹配本身就不稳。（[实验记录 §10.5](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/90_local_experiments.md)）

所以本文的结论要收得更紧一点：**前面九节量出来的判别力，只覆盖了两类任务里的一类。** 另一类的判据还停在原型阶段，而真实需求主要落在另一类上。

<a class="anchor" id="vf-11"></a>

## 11 Half of Aesthetics Is a Deterministic Check

审美通常被当成「只能靠人或靠模型」的那一类，于是整个推迟到最后。实测下来这个划分太粗：审美里有一半能做成零噪声的程序化判据，而且**现有的功能侧判据对这一半几乎完全瞎**。

做法（[审美调研 §6](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/19_aesthetics.md)，跑测脚本 [run_aes.js](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/web/run_aes.js)）：在 Web 那套 harness 上加一个只读计算样式与几何的探针，不比像素、不调模型，查排版层级、字号尺度、字体族数、行高、间距节奏、色相数量、对比度等十一条。阈值先在参考页上测出来再加余量冻结。然后造 20 个变异——12 个只破坏审美不破坏功能（页面照跑、不报错、不溢出、不遮挡），其中 1 个事后判为无效变异；8 个是合法改版（换品牌色、换一套自洽的等比尺度、深色主题、加留白、类名重命名、压缩 HTML）。

核心发现：11 个有效的纯审美缺陷里，功能侧判据只「抓到」2 个，而那 2 个还是因为改色顺带破坏了对比度才被规则引擎抓到的（[审美调研 §6.2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/19_aesthetics.md)）。

| 口径 | 审美判据 | 功能侧判据 |
|---|---|---|
| 参考页 | 11 条全过 | 全过 |
| 纯审美缺陷（11 个有效变异） | 抓到 9 | 抓到 2，且都是顺带 |
| 合法改版（8 个） | 误杀 0 | 误杀 0 |
| 单个变异耗时 | 约 0.8 秒，两个视口 | 约 4.9 秒 |

来源：[审美调研 §6.2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/19_aesthetics.md)；功能侧耗时见 [Web verifier 实测](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/14_web_verifier.md)。

数据解读：标题层级反了、字号变成一堆相近的随机值、四种字体混用、行高压到 1.02、间距全换成奇数、抹掉所有内外边距——这六类功能侧一个都看不见，而它们正是「这页看着不像人做的」的主要来源。审美判据把其中大部分补上了，成本还只有功能侧的六分之一。（[审美调研 §6.2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/19_aesthetics.md)）

两条必须放弃当闸，这比抓到几个更值得记（[审美调研 §6.3](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/19_aesthetics.md)）：

- **圆角一致性**：参考页本来就有四种圆角，变异推到六种，判别余量不够。
- **栅格对齐**：该挂的那个变异对齐率是 0.707，而一个**不该挂、而且审美更好**的改版是 0.765，可分离区间只剩 0.058。更要命的是它在极端处会翻向——把所有内外边距抹掉之后，对齐率反而是 1.000。**能把好坏分开，不等于能当闸。**（[审美调研 §6.3](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/19_aesthetics.md)）

还有一条预设要去掉：不要假定页面按 4 像素栅格排布。参考页是手写的、规则引擎全过，但它的间距只有 57.8% 落在 4 的倍数上，最合适的基数是 2，命中 91.4%（[STATE.md](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/STATE.md)）。基数应该从页面自己身上测出来，不是写死。

更大的一个陷阱在经典的计算美学指标上（[审美调研](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/19_aesthetics.md)）。那一批指标（对称性、平衡、密度之类）**全部单调可刷**，拿它们当 reward，最优解是一张空白单列页。公开实测也不支持它们：

- 非单调：一项 72 人的偏好实验里，Ngo 那一族指标得分最高的布局反而最不受欢迎，最受偏好的是中等对称度（[Salimun 2013 博士论文](https://theses.gla.ac.uk/4256)）。
- 真实网页上失效：把 14 项指标做成工具输入完整网页，只有 1 项和审美吸引力对得上（[Purchase et al. 2011](https://eprints.gla.ac.uk/54578)）。
- 越接近好越不准：用 GPT-4 给 UI 设计稿提反馈，设计师按反馈迭代、界面变好之后，反馈被评为准确的比例从首轮的 52% 降到后续轮的 39%（[Duan et al. CHI 2024](https://arxiv.org/abs/2403.13139)）。**这类信号在接近最优时会反向。**

还有一条划了边界：「AI 味」在单页尺度上测不出来。单页能查的只是**具名特征**——Inter 字体、白底紫渐变这一类已知默认（[Anthropic 前端设计博客](https://claude.com/blog/improving-frontend-design-through-skills)点名的就是这几个）。在本项目 20 个页面里，注入了这组默认的那一页被命中、品牌蓝渐变的改版不误报（[审美调研 §6.2](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/19_aesthetics.md)），但它量的是「像不像那几个已知模板」，不是「平庸不平庸」。

这不是推断，是实测出来的反证（[审美调研 §4](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/19_aesthetics.md)）。拿本站两批页面算字体维度的集中度：一批 100% 用了那个被点名的字体，集中度 0.50；另一批一次都没用，集中度却是 1.00，也就是更坍塌。**一条「禁用某字体」的规则会让后者满分通过，而它恰恰是更单调的那一批。** 规则表只能查已知的默认值，查不到「收敛」本身。

真正的平庸度是分布量，要在一批产物上算集中度或熵，所以它天然不能当逐样本的 reward，只能当批次级诊断。顺带一提，收敛有一部分是被 prompt 规定出来的——Google 的 [Generative UI](https://arxiv.org/abs/2604.09577) 专门有一节把「跨次生成保持视觉一致」当成可选特性，公开的系统指令里点名推荐字体、鼓励渐变（§2.1 与附录）。这部分不用训练就能改回来。

凭人判的那一半有一个硬天花板（[DesignPref](https://arxiv.org/abs/2511.20513)）。20 位设计师各评同样 600 对设计，二元一致率只有 0.624，Krippendorff α 是 0.248，28.5% 的对子两两分歧率达到 96% 及以上；用 20 倍数据训练出来的偏好模型也只有 57.45%，做了个性化才到 60.16%。**超过这个数就该先怀疑数据泄漏**——Webthetics 广为引用的 r≈0.85，后续 [TOCHI 工作](https://doi.org/10.1145/3569889)（Eisbach et al.）报出自己模型的交叉验证 LCC 为 0.752，并指出前者原代码有训练集与验证集重叠（后一点转述自[审美调研笔记](https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/19_aesthetics.md)，ACM 全文对本机访问受限，未能复核原句）。

这反过来说明程序化那一半的价值被低估了：它不受这个天花板约束，因为它测的根本不是「谁更好看」。

最后一条和前沿的做法正好拧着。Anthropic 那套四维评审器里（[Anthropic 工程博客：Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)），工艺这一维（排版层级、间距一致性、配色和谐、对比度）几乎整维可程序化，而官方把它**降权**，理由是模型默认就及格、没有区分力。这个判断在他们的生成分布下成立；但进了 RL 之后，恰恰是这一维能当硬闸而不会被刷——因为它查的是可测量的事实，不是偏好。可降权的是它在**排序**里的比重，不该降的是它在**门控**里的位置。

## 参考文献

1. [WorldCoder-Bench: Benchmarking Physically Grounded 3D World Synthesis](https://arxiv.org/abs/2606.01869) — Shuo Lu 等，arXiv 2026-06-01
2. [WorldBench: Evaluating LLMs on Three.js Voxel World Generation](https://arxiv.org/abs/2610.10622) — Krish Bakshi，arXiv 2026-10-07
3. [three.js r160 源码 src/scenes/Scene.js](https://github.com/mrdoob/three.js/blob/r160/src/scenes/Scene.js) — mrdoob/three.js，r160 版本
4. [3JSBench 榜单](https://3jsbench.com/) — 3JSBench 站方，2026-10-14 改判版（2026-10-15 读取）
5. [3JSBench Methodology](https://3jsbench.com/methodology) — 3JSBench 站方，2026-10-15 读取
6. [SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features](https://arxiv.org/abs/2502.14786) — Michael Tschannen 等（Google DeepMind），arXiv 2025-02-20
7. [AgentTypo: Adaptive Typographic Prompt Injection Attacks against Black-box Multimodal Agents](https://arxiv.org/abs/2510.04257) — Yanjie Li 等，arXiv 2025-10-05
8. [MLLM-as-a-Judge: Assessing Multimodal LLM-as-a-Judge with Vision-Language Benchmark](https://arxiv.org/abs/2402.04788) — Dongping Chen 等，arXiv 2024-02-07
9. [Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge](https://arxiv.org/abs/2406.07791) — Lin Shi 等，arXiv 2024-06-12
10. [Self-Preference Bias in LLM-as-a-Judge](https://arxiv.org/abs/2410.21819) — Koki Wataoka 等，arXiv 2024-10-29
11. [Frontend prompt instructions](https://developers.openai.com/api/docs/guides/frontend-prompt) — OpenAI 开发者文档（面向 GPT-5.5），2026-10-15 读取
12. [The relationship between visual interface aesthetics, task performance, and preference](https://theses.gla.ac.uk/4256) — Carolyn Salimun，University of Glasgow 博士论文，2013
13. [Investigating objective measures of web page aesthetics and usability](https://eprints.gla.ac.uk/54578) — Helen C. Purchase 等，AUIC 2011
14. [Generating Automatic Feedback on UI Mockups with Large Language Models](https://arxiv.org/abs/2403.13139) — Peitong Duan 等，CHI 2024，arXiv 2024-03-19
15. [Improving frontend design through Skills](https://claude.com/blog/improving-frontend-design-through-skills) — Anthropic，2025-11-12
16. [Generative UI: LLMs are Effective UI Generators](https://arxiv.org/abs/2604.09577) — Yaniv Leviathan 等（Google Research），arXiv v1 2026-02-24
17. [DesignPref: Capturing Personal Preferences in Visual Design Generation](https://arxiv.org/abs/2511.20513) — Yi-Hao Peng 等，arXiv 2025-11-25
18. [Predicting Rating Distributions of Website Aesthetics with Deep Learning for AI-Based Research](https://doi.org/10.1145/3569889) — Eisbach 等，ACM TOCHI，2023
19. [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Anthropic Engineering，2026-03-24

