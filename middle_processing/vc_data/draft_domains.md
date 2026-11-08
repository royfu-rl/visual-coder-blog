<a class="anchor" id="dm-1"></a>

## 1 Charts Are the Output Where Tolerance Disappears

前面讲 3D Verifier 时，每一条判据都带着容差：剪影 IoU 要大于 0.9，体素 IoU 要大于 0.5，颜色距离要小于 60（[3D 本机实验记录 第 2 节](../middle_processing/vc_data/90_local_experiments.md)）。容差是被迫的，因为「画得对不对」没有数值真值可比。换到图表和矢量图，这个前提消失了：输入数据已知，产物能被还原成数值再逐个比对。判定可以不带容差。

本机实测给出了这条路的噪声地板（下文本节数字均出自[图表 Verifier 实验记录](../middle_processing/vc_data/17_chart_verifier.md)第 4 节，Chart.js 4.4.6 单任务）。同一个参考页面重复渲染 5 次，几何回读的柱子坐标与坐标轴刻度像素位置逐位完全相同，截图的摘要值只有 1 种。这不是「噪声很小」，是这一环确实为零。参考解自己跟自己比，逐值回读的最大相对误差是 0.15%，而这 0.15% 每次都一样，来自图表库把柱子底边画在零线下方约半个像素的固定偏置，不是随机抖动。判据的容差定在 1%，对它有 6 倍余量。

核心发现：三类程序化信号在同一批变异上的判别力差了一个档，而像素比对的失败不在阈值。

| 信号 | 判对 | 漏判 | 误杀 |
|---|---|---|---|
| 逐值回读 | 13/16 | 3 | 0 |
| 像素比对 | 9/16 | 3 | 4 |
| 结构断言 | 14/16 | 2 | 0 |
| 逐值回读或结构断言 | 16/16 | 0 | 0 |

来源：[图表 Verifier 实验记录 §4](../middle_processing/vc_data/17_chart_verifier.md)，16 个带标签变异，无留出。

数据解读：逐值回读漏掉的三个变异全部不是数据错，分别是轴截断、图表类型画错、轴标题连单位一起丢掉。轴截断那一个尤其说明职责边界：y 轴从 500 起画，柱子的几何仍然精确编码着原数值，线性拟合外推到零线之下读出 0.00% 误差，这是正确行为而不是失灵。轴范围归结构断言管。结构断言漏掉的两个全部是纯数据错，整列缩放 1.3 倍和单点把 1510 画成 1150，结构完全合法。两边盲区精确互补，所以取或就是 16/16（[图表 Verifier 实验记录 §4.3 逐变异表](../middle_processing/vc_data/17_chart_verifier.md)）。

像素比对不是不够准，是在这件事上不存在可用的工作点。它漏掉的单点画错只让 0.75% 的像素发生变化，图例与数据错位只让 0.01% 的像素变化；而它误杀的四个全是纯外观改动，换配色让 30.51% 的像素变化，柱子变窄 14.13%，图例挪到底部 11.32%（[实验记录 逐变异表](../middle_processing/vc_data/17_chart_verifier.md)）。要抓住 0.01% 就得把阈值压到千分之一以下，那时 30.51% 会被误杀得更彻底。信号与噪声在量纲上直接重叠，中间没有空隙。

成本也站在回读这边。17 个页面各起一次浏览器，单页全流程中位 840 毫秒，其中渲染约 470 毫秒、截图约 110 毫秒，而回读只要 1 到 4 毫秒，是渲染耗时的千分之四（[实验记录 耗时表](../middle_processing/vc_data/17_chart_verifier.md)）。这个比例决定了回读可以放进 RL 的每一步，而截图不行。

这一节要立住的判断只有一条：图表与矢量图是目前唯一能把 Verifier 这一环的噪声压到零的产出形态。零噪声是质量上的优势，不等于它该排第一——入场顺序还要看工程成本和供给规模，后面那一节会给出完整排序。它不是「像素比对的更严格版本」，而是换了一个被测量——像素比对量的是两张图有多像，逐值回读量的是屏幕上那根柱子到底有多高。

<a class="anchor" id="dm-2"></a>

## 2 Read the Drawn Geometry, Not the Configuration Object

零容差的前提是回读读的是真东西。读图表库的配置对象做不到这一点：那里的数值是模型自己写进去的，模型画错了，读回来的还是那份对的数字。同样的道理在 Tasks 视图里已经出现过一次——判据必须落在状态上而不是落在代码上——换成图表，落点从场景图变成绘制几何。

正确的通道是从绘制结果反推。先由两个坐标轴刻度的像素位置拟合出数值与像素的线性映射，再取柱子顶边和底边两个像素反算它代表的数值。矢量图这边更直接，读图元自身的高度属性，配合两个刻度文本的位置换算。两条路都不读任何源码常量（判据定义见[图表 Verifier 实验记录 §1.1](../middle_processing/vc_data/17_chart_verifier.md)）。

核心发现：注入一个已知倍率的错误，回读报出来的偏差与理论值对得上。

| 被测页面 | 逐值回读最大相对误差 | 注入的错误 |
|---|---|---|
| 矢量图参考版 | 0.02% | 无 |
| 矢量图问题版 | 24.99% | 柱高统一乘 0.75，理论偏差 25% |
| 画布参考版 | 0.15% | 无，残差来自底边半像素偏置 |

来源：[图表 Verifier 实验记录 §4.5](../middle_processing/vc_data/17_chart_verifier.md)。

数据解读：24.99% 对上理论值 25%，说明回读量到的是真实绘制几何，而不是任何中间变量。矢量图路线的残差比画布路线低一个档，因为它没有底边偏置。0.02% 的残差意味着这条通道几乎没有系统误差可言（[图表 Verifier 实验记录 §4.5](../middle_processing/vc_data/17_chart_verifier.md)）。

抗伪造同样靠这个落点。把正确数据写进配置、再用自定义绘制画出错误的柱子，配置回读会放行，几何回读不会。把数值用文字写对、柱子画错，交叉检查会抓住：数据标签的文本必须与同位置柱子的几何回读值自洽。在离屏画布上另画一张正确的图，也骗不过「只认挂在文档里、有尺寸、未隐藏的那块画布」这条规则，这条规则是从 3D 线原样搬过来的（[3D 本机实验记录](../middle_processing/vc_data/90_local_experiments.md)）。

Harness 不要求模型配合暴露任何东西，理由和 3D 线相同：训练时模型只会学会写那一行，换一套 Harness 就失效。图表这边有两条不需要页面配合的替代路径。第一条是图表库由环境提供，Harness 自己起本地服务下发，页面不许访问外网，库在谁手里实例注册表就在谁手里。第二条是在页面脚本之前接管画布文字绘制接口——所有画布文字都必须经过它，拦住就拿到全部文字，与用哪个图表库无关。本机参考解抓到 33 段文字，包括轴标题、图例、刻度、主标题和 12 个数据标签，一段不漏（[图表 Verifier 实验记录 §2.2](../middle_processing/vc_data/17_chart_verifier.md)）。

位图回读是另一条路，但它不够格。公开工作的天花板是 [DePlot](https://arxiv.org/abs/2212.10505) 在 PlotQA 合成图上 94.2 的 RMS_F1（[论文 表 4](https://arxiv.org/abs/2212.10505)），在分布外的 TaTa 真实图上掉到平均约 78%（[论文 §6.2](https://arxiv.org/abs/2212.10505)，只标注了 10 张图）。拿这个当 reward，噪声地板比要测的效应还大。做 RLVR 只能走文档对象或运行时通道。

<a class="anchor" id="dm-3"></a>

## 3 The Mutation Set Audits the Verifier Before It Rates the Model

本机实测跑出 16/16 之前，Verifier 自己出了三个 bug（[图表 Verifier 实验记录 §4.4](../middle_processing/vc_data/17_chart_verifier.md)）。三个都制造假阳性，也就是把正确的产物判挂；三个都不是阈值问题，调阈值一个也修不掉。

核心发现：假阳性的真因全部在坐标系和帧，不在判据的松紧。

| 症状 | 真因 | 修法 |
|---|---|---|
| 参考解报告数据标签 360 个而不是 12 个，动画变异被误杀 | 每帧重绘都把所有文字重画一遍，文字钩子把 240 帧的记录全存了下来 | 给每条记录打帧号，只取最后一个画了字的帧 |
| 动画变异的逐值回读误差 2.70%，超过 1% 判据 | 只推了 30 帧虚拟时间 480 毫秒，而动画时长 800 毫秒，读到的是中间态 | 推到 240 帧，虚拟时间 3.84 秒 |
| 参考解报告 171 对文字重叠，实际 0 对 | 图表库普遍先平移旋转再在局部坐标里写字，钩子记的是局部坐标，旋转文本全堆在原点 | 文字包围盒四角过一遍当前变换矩阵；矢量图侧改用页面坐标接口 |

来源：[图表 Verifier 实验记录 §4.4](../middle_processing/vc_data/17_chart_verifier.md)。

数据解读：修掉这三个 bug 之后，逐值回读从 12/16 变 13/16，结构断言从 13/16 变 14/16。两个提升全部来自消除假阳性，而判据里的四个阈值从写下到最终结果一个没动（[图表 Verifier 实验记录 §4.4](../middle_processing/vc_data/17_chart_verifier.md)）。

三条推论。第一，假阳性比假阴性难发现得多。前两个 bug 的表现都是「某个不该挂的变异挂了」，如果变异集里没有「不该挂」的那一半，它们会一直潜伏到 RL 里变成纯噪声。该挂与该放行各占一半的变异集，第一价值是体检 Verifier，不是评模型。第二，坐标系是这类 Verifier 的头号坑：表里两个 bug 出在帧，一个出在坐标系，而矢量图的值回读又踩了第二次坐标系的坑。凡是位置参与判定的检查，都要先问这个坐标在哪个系里。矢量图的值回读还要再分一层：刻度位置必须用图形自身坐标系，页面坐标只能给重叠和溢出用，混用会凭空多出一个缩放因子，本机实测把 25% 的偏差读成了 75%（[实验记录 §4.4](../middle_processing/vc_data/17_chart_verifier.md)）。第三，修的是 Harness，不是阈值。

这条推论反过来约束了准入测试的设计。Tasks 视图讲过，准入测试决定任务从哪来；这里补一句：准入测试的第一个被测对象是 Verifier 自己。

<a class="anchor" id="dm-4"></a>

## 4 On the Web the Errors Are Not Visual Errors

Web 侧没有「像素噪声淹没信号」这个问题。参考页自己跟自己比，截图的平均绝对差是 0.000，相同像素占比 1.0000，噪声地板为零（下文本节本机数字均出自 [Web Verifier 实验记录](../middle_processing/vc_data/14_web_verifier.md) 第 4 节）。问题出在另一头：11 个该挂的变异里有 7 个在桌面宽度的首屏截图上与参考完全相同，相似度 1.0。零噪声加四成检出，说明截图这个观测口就是看不到这些错误。

状态本来就可读，所以确定性信号比 3D 侧更强。本机参考页是一个带地标结构、导航、卡片网格、标签页、表单校验、模态框、哈希路由和主题持久化的单页，判据分五层：正确性、布局与响应式、可访问性、交互状态机、性能预算，门控是乘法的，任一层挂即判挂（[Web Verifier 实验记录 §1、§4.1](../middle_processing/vc_data/14_web_verifier.md)）。

核心发现：五层组合在 22 个带标签变异上零漏零误，而单一观测口无论怎么选阈值都到不了（[Web Verifier 实验记录 §4.4~4.5](../middle_processing/vc_data/14_web_verifier.md)）。

| 信号 | 判对 | 检出 11 个该挂 | 误杀 11 个不该挂 |
|---|---|---|---|
| 单张截图逐像素，阈值取最优 | 14/22 | 4 | 1 |
| DOM 标签序列一致 | 11/22 | 2 | 2 |
| 类名序列一致 | 8/22 | 0 | 3 |
| 可见文本一致 | 11/22 | 0 | 0 |
| 正确性层 | 13/22 | 2 | 0 |
| 布局与响应式层，三视口 | 13/22 | 2 | 0 |
| 可访问性层 | 15/22 | 4 | 0 |
| 交互状态机层 | 14/22 | 3 | 0 |
| 性能预算层 | 12/22 | 1 | 0 |
| 五层组合 | 22/22 | 11 | 0 |

来源：[Web Verifier 实验记录 §4.5 判别力表](../middle_processing/vc_data/14_web_verifier.md)。

数据解读：22 个变异里 16 个是开发集、6 个是留出集，标签先写死，阈值只在参考页的 5 次重复上校准、在任何变异体上一次都没调（[Web Verifier 实验记录 §4.3](../middle_processing/vc_data/14_web_verifier.md)）。11 条该挂的全部挂在设计时预期的那一层（[同上 §4.5](../middle_processing/vc_data/14_web_verifier.md)）。类名序列这个朴素判据检出 0/11、误杀 3/11，比随机还差——它只能抓到「换了类名」这件事本身，而换类名正是最常见的等价重写。可见文本一致同样检出 0/11。朴素结构判据失效的原因是它们绑在实现手法上，而类名、标签名、CSS 写法、事件绑定方式、单位、字体栈、是否压缩这七样都可以在视觉与功能完全等价的前提下任意更换（[同上 §5.3](../middle_processing/vc_data/14_web_verifier.md)）。

像素信号的阈值无处可放。要抓住对比度降级那一条，阈值必须设在 0.9883 以上；但换配色这个合法重写的像素差是 0.9002，内联图标那条是 0.9999（[实验记录 逐变异表](../middle_processing/vc_data/14_web_verifier.md)）。合法重写的像素差比大多数真缺陷都大。这与 3D 侧的情况不同：3D 侧是逐像素 12/29，而单个 VLM judge 在 48 例上的判对率是 79% 到 96%（[3D 本机实验记录 §2.1、§3](../middle_processing/vc_data/90_local_experiments.md)），VLM 比像素强得多；Web 侧那 7 个该挂的变异在视觉上和参考完全一样——删掉替代文本、按钮换成普通容器、摘掉表单校验、启动时同步忙等、脚本尾部未定义变量、主题不落存储，图上都没有任何痕迹。VLM 在这里的替代空间比 3D 侧更小，不是因为 VLM 弱，是因为这些错误压根不是视觉错误。

核心发现：五层各有不可替代的贡献，没有一层是摆设。

| 层 | 只有它抓到的真缺陷 | 是哪几条 |
|---|---|---|
| 可访问性 | 4 | 对比度降级、缺替代文本、按钮换成普通容器、标题跳级加地标丢失 |
| 正确性 | 2 | 资源 404、运行时未捕获异常 |
| 交互状态机 | 2 | 表单校验被摘掉、主题不持久化 |
| 布局与响应式 | 1 | 窄视口横向溢出 |
| 性能预算 | 1 | 启动时的长任务 |

来源：[Web Verifier 实验记录 §4.5 唯一贡献表](../middle_processing/vc_data/14_web_verifier.md)。

数据解读：多视口是必需的一维而不是锦上添花。只看桌面单视口是 12/22、检出 1/11，加上手机与平板两档后是 13/22、检出 2/11（[实验记录 §4.7](../middle_processing/vc_data/14_web_verifier.md)）。差的那一条是卡片写死固定宽度：它在桌面宽度下一切正常，三列、无溢出、无越界，到手机宽度才暴露出 65 像素的横向溢出和 10 个越界元素。检索到的公开 benchmark 里没有一家把多视口一致性做成确定性判据：[Vision2Web](https://arxiv.org/abs/2603.26648) 对桌面、平板、手机三套原型用 VLM judge 打分，[WebGen-Bench](https://arxiv.org/abs/2505.03733) 的响应式用例由 UI agent 判是非，[MV-Bench](https://arxiv.org/abs/2607.19910) 只用固定 1920×1080 单视口（检索过程见 [Web Verifier 实验记录 §3.6](../middle_processing/vc_data/14_web_verifier.md)）；而本机实测里它贡献了 11 个真缺陷中其它四层都抓不到的那一个。

可访问性是整张能力表里唯一「确定性 reward 加 RL 就能赢闭源」已被公开验证的维度。[A11yn](https://arxiv.org/abs/2510.13914) 用规则引擎 axe-core 的严重度加权违例做 GRPO 的 reward，把 Qwen2.5-Coder-7B 的违例率 IR_Axe 从 0.40 压到 0.05，低于 GPT-5.1 的 0.13、Gemini 3 Pro 的 0.24 和 Claude Sonnet 4.6 的 0.45（[论文 v2 表 2](https://arxiv.org/abs/2510.13914)）。这个数要打折：reward 与评测主指标是同一个量，所以 0.05 对 0.13 是「直接优化的量对零样本」而不是公平比较；它真正的独立证据是换一个规则引擎后的 IR_AChecker 0.26 对 0.35（同表），以及人工两两比较的胜 39.3%、平 39.3%、负 21.4%（[论文 附录 E 表 7](https://arxiv.org/abs/2510.13914)）。规则引擎本身也没有大家以为的那么自动：[axe-core 4.14.0 规则表](https://github.com/dequelabs/axe-core/blob/v4.14.0/doc/rule-descriptions.md)共 105 条规则，64 条的问题类型带 needs review，纯自动判定的只有 41 条，占 39%（本次按该表逐行重数）。

作弊是真能作弊的。手写 7 个作弊页，第一版判据挡住 5 个（[实验记录 §4.9](../middle_processing/vc_data/14_web_verifier.md)）。漏掉的两个分别是「加载时无条件把主题写成深色、切换按钮其实什么都不做」和「把不合格文字的字号设为 0、再用伪元素把同样的字画回屏幕」。第一个靠补判据修掉：每条状态机断言必须带前置态、终态和往返三段，清空存储后的初始态、操作后的终态、刷新后仍然保持、再操作一次能回去，硬编码的页面在第一条和第四条上同时挂掉。第二个修不掉——审计引擎对这个页面的输出是零违例、零需要复核、45 条通过，伪元素承载的文字它根本不检查，字号为 0 的真元素又被当成无文本跳过，两头都落空。这条对应的上游问题 [axe-core issue #2680](https://github.com/dequelabs/axe-core/issues/2680) 自 2020-12 提出至今仍是 open。纯 DOM 侧的确定性信号在这里到顶了，只能靠静态代码闸或者看屏幕上实际显示了什么。补完两条判据后做了全量回归，仍然 22/22，零新增误杀；改的全是判据，不是阈值。

第一遍跑出来的其实是 21/22，唯一误判拆开是两个性质完全不同的问题（[实验记录 §4.10](../middle_processing/vc_data/14_web_verifier.md)）。一个是 Verifier 的真 bug：列数测量用了表现型类名做选择器，类名一换就读成 0 列，修法是改成结构化定位，取主内容里第一个有两个以上子项的列表。另一个是人工标签错了：重命名脚本用全文正则，把 ARIA 角色名一起改掉了，那不是等价重写而是真的破坏了无障碍结构，审计引擎判对了。这和 3D 侧那次标注翻案是同一类事（[3D 本机实验记录 §3.4](../middle_processing/vc_data/90_local_experiments.md)）——判据判错之前，先怀疑标签。

成本可以忽略。单次完整探针 4.9 秒，但其中工具开销不到 0.5 秒：浏览器启动 181 毫秒、新开页加载 61 毫秒、注入审计引擎 72 毫秒、跑一次审计 30 到 71 毫秒、复用浏览器开页约 50 毫秒（[实验记录 §4.11](../middle_processing/vc_data/14_web_verifier.md)）。剩下全是固定的稳定等待和 40 帧采样，去掉帧采样、把等待改成事件驱动、状态机复用同一个页面上下文，可以压到 1 秒以内（推算，未实测）。22 个变异全量两遍跑完 114 到 117 秒，平均 5.2 秒一个。两遍全量重跑的判定翻面 0 条，层级列表与明细逐字节一致——确定性信号不需要多次投票，这直接省掉乘在成本上的那个系数；对照是 3D 侧的 VLM judge，最差一档温度 0 重判有 20.8% 的 case 翻面（[3D 本机实验记录 §3](../middle_processing/vc_data/90_local_experiments.md)）。

<a class="anchor" id="dm-5"></a>

## 5 Playability Fails on Coverage, Not on Accuracy

网页游戏这边，判据准不准已经不是瓶颈。[PlaytestArena](https://arxiv.org/abs/2605.28258) 的 GUI judge 与人的条目级一致率是 87.9%，而人与人之间是 91.4%，差 3.5 个百分点（[论文「Is the GUI Evaluator Reliable?」一节](https://arxiv.org/abs/2605.28258)）；[PlaySuite](https://arxiv.org/abs/2610.07127) 的里程碑式 judge 与人的「相差一级以内」一致率 90.4%，人与人 93.0%，人自己的 Krippendorff α 只有 0.624（[论文 §3](https://arxiv.org/abs/2610.07127)）。继续优化 judge 的收益已经很小。

真正卡住的是验得到验不到。

核心发现：同样的 playtest 预算，花在「再玩一遍」上几乎没有回报，花在「把状态摆到规则的前置条件上」才有。

| playtest 策略 | 能给出结论的规则占比 |
|---|---|
| 第一遍正常玩 | 40.5% |
| 再加一遍正常玩 | 41.0% |
| 把状态直接注入到规则的前置条件 | 48.5% |

来源：[A2Z GameSpec-Bench 表 4(c)](https://arxiv.org/abs/2609.39564)，50 个游戏的 86 条依赖规则，预算对齐。

数据解读：加一遍正常玩只涨 0.5 个百分点，换成状态注入涨 8.0 个百分点。逐 agent 看差距更大：正常玩的覆盖率在 13.1% 到 29.0% 之间，加状态注入后是 53.3% 到 88.0%（[A2Z 附录 F.3](https://arxiv.org/abs/2609.39564)）。碰不到的规则就是 0 信号，判据再准也没用。所以钱该花在「状态能摆到任意位置」上，而不是「训一个会玩的 agent」上——同一批十个游戏上，一个在线游戏 agent 的里程碑达成率只有 0.0% 到 42.2%，而加上对抗式注入后的判定覆盖率合计是 73.4%（[A2Z 附录 G.4 表 S20](https://arxiv.org/abs/2609.39564)；两者分母不同，论文注明不能直接相比）。

只读源码会被骗，骗的量级是可测的。源码判满分的规则，真玩时只有 76.8% 成立；反过来，源码判零分的规则里有 25.7% 真玩是对的（[A2Z §4.3](https://arxiv.org/abs/2609.39564)）。同一来源还给了一条更狠的：规则的局部通过率是 72.4%，但要求它的所有上游规则也通过，就只剩 22.7%，差 49.7 个百分点（[A2Z 附录 B.7](https://arxiv.org/abs/2609.39564)）。能跑和能玩是两个几乎正交的量，另一组消融给出了同样的方向——[Code2Games](https://arxiv.org/abs/2610.05033) 只给编译与运行诊断，构建成功率从 78.5 涨到 88.7，交互符合度只从 58.0 挪到 59.0；加了玩法断言反馈才从 59.0 涨到 75.8（[论文 表 3](https://arxiv.org/abs/2610.05033)）。

录屏加 VLM judge 这条路更直接地证伪了自己。[V-GameGym](https://arxiv.org/abs/2509.20136) 把交互代码改写成 10 秒自动演示再录屏打分，而录屏评分表里仍然留着「用户输入响应性」这一项（[论文 附录 R](https://arxiv.org/abs/2509.20136)）——全程没有发过任何一次输入。这不是实现瑕疵，是「用录屏当可玩性证据」本身的归谬。

可玩性并不是只能靠人。把「能玩」拆成 6 族 33 条子命题之后，24 条能做成纯程序判据，6 条需要 agent 真玩，3 条只能靠人（本项目的拆解设计，见[游戏 Verifier 调研记录 §1](../middle_processing/vc_data/15_game_verifier.md)，未实测）。只能靠人的那三条是好不好玩、审美和创意，而人与人在逐条 rubric 上的整体一致性本来就只有 κ=0.68（[PlaytestArena 评测可靠性一节](https://arxiv.org/abs/2605.28258)）。所以「可玩性只能靠真玩」是错的，对的说法是「可玩性不能只靠看源码和看截图」。

<a class="anchor" id="dm-6"></a>

## 6 The State Interface Cannot Depend on the Model's Cooperation

代表性的公开游戏 playtest 系统都要求游戏自己暴露状态接口：[A2Z](https://arxiv.org/abs/2609.39564) 要求每个构建提供状态设置入口与场景变更器，而且这个注入面被显式排除在不变量检查之外（[论文 附录 D.1.2](https://arxiv.org/abs/2609.39564)）；[UI-TARS-2](https://arxiv.org/abs/2509.02544) 的合成游戏同样被要求暴露显式状态接口供验证脚本读取（[技术报告 §2.5.1](https://arxiv.org/abs/2509.02544)）。训练时照搬，模型学到的就是「写那一行」。这和 3D 线不要求页面暴露场景变量是同一条原则，换了领域没有变。

核心发现：五条拿状态的路线按抗欺骗强度排序，最强的那条反而不需要知道游戏内部任何东西。

| 路线 | 怎么拿 | 骗得过吗 | 覆盖面 |
|---|---|---|---|
| 输入重放加状态差分 | 固定种子固定时钟跑多条输入轨迹，比较产物或帧哈希序列 | 最难骗，要骗必须真的实现一个会按规则响应输入的系统 | 全部 |
| 绘制调用拦截 | 预加载时接管渲染循环与绘制接口 | 几乎骗不过，这就是玩家看到的东西 | 全部画布游戏 |
| 引擎自带钩子 | 引擎自己派发的全局事件或实例注册表 | 难骗，事件由引擎发不是作者写的 | 取决于引擎 |
| 像素与音频弱监督 | 帧差与音效事件探测 | 容易骗，背景动画会让每帧都不同 | 全部 |
| 要求模型暴露接口 | 脚手架规定必须写 | 骗得过，训练时一定会被骗 | 强制 100% |

来源：本项目的路线设计，见[游戏 Verifier 调研记录 §3.1~3.2](../middle_processing/vc_data/15_game_verifier.md)，属分析结论，未实测。

数据解读：排序的依据不是强度而是性质。输入重放加状态差分把「可玩性」转成了一个不需要语义的差分问题——一条空输入轨迹、一条有输入轨迹、几条不同强度的策略轨迹，剩下的全是序列比较。3D 线的冻结时钟部分可以原样复用（[3D 本机实验记录](../middle_processing/vc_data/90_local_experiments.md)），要新建的只有输入重放。

引擎钩子这一层的现实比文档描述的糟。逐引擎读发行包源码的结果是（[游戏 Verifier 调研记录 §3.3](../middle_processing/vc_data/15_game_verifier.md)）：[three.js](https://github.com/mrdoob/three.js)、[PixiJS](https://github.com/pixijs/pixijs) v8、[Babylon.js](https://github.com/BabylonJS/Babylon.js) 的钩子由引擎自己创建，只要在页面脚本之前注入就能用；[p5.js](https://github.com/processing/p5.js) 在全局模式下连作者自己的分数变量都挂在全局对象上，但实例模式下拿不到。网页小游戏常用的 [Phaser](https://github.com/phaserjs/phaser) 3（A2Z 的 100 个任务全部基于 Phaser）恰好是最不可用的那个——它的调试全局在 3.60 到 3.90 的八个发行文件里一次都没有出现，唯一通用路子是在页面脚本前劫持它的游戏构造函数。Unity 的网页导出只给单向的 [SendMessage 消息发送接口](https://docs.unity3d.com/Manual/web-interacting-browser-js-to-unity.html)，没有返回值；Godot 的网页桥接 [JavaScriptBridge](https://docs.godotengine.org/en/stable/classes/class_javascriptbridge.html) 官方文档写明可以在构建时关掉。

还有一条比可用性更要命的限制：没有一个引擎钩子给得出游戏逻辑状态（[游戏 Verifier 调研记录 §3.3](../middle_processing/vc_data/15_game_verifier.md)）。它们给的是渲染图与场景图，分数和生命仍然在作者的闭包里。性价比最高的补法不在引擎层——拦截画布的文字绘制接口，直接从参数里读出屏幕上的分数、生命和关卡文本，完全不需要 OCR。这条路在图表线上已经实测可行（33 段文字一段不漏，[图表 Verifier 实验记录](../middle_processing/vc_data/17_chart_verifier.md)），在游戏线上尚未实测；画布游戏的 HUD 文字多半走这个接口，但这一点没有做过统计。它能把「分数会涨」从需要 agent 真玩降级成纯程序判据。

确定性回放是这一切的地基，而地基有两个硬漏点。第一个是 Web Worker 里的时钟拦截不住：[PlaySuite](https://arxiv.org/abs/2610.07127) 为此排除了 225 个 Construct 3 游戏，这是它技术性排除里最大的一类，多于「只支持拖拽」的 72 个和「多人」的 25 个（[论文 表 5](https://arxiv.org/abs/2610.07127)）。第二个是超越函数跨引擎版本会分叉：[ECMAScript 规范](https://tc39.es/ecma262/#sec-math.sin)把 Math.sin 等定为 implementation-approximated，不规定精度；调研时记录到一个物理库的现存 issue，同一份刚体仿真在两个不同版本的 V8 下结果不同（[游戏 Verifier 调研记录 §4.2](../middle_processing/vc_data/15_game_verifier.md)；原 issue 链接本次实测被对方站点拒绝访问，未能复核）。这两条决定了准入测试必须加一条硬闸：同一份代码双跑，产物不一致就不进数据集。不确定的任务进了 RL 就是纯噪声。

<a class="anchor" id="dm-7"></a>

## 7 Web First, Charts Second, Games Third

三个维度决定入场顺序：判定的确定性、工程成本、供给规模。三个领域在这三个维度上的位置并不一致，所以排序不是按「哪个最干净」排的。

核心发现：Web 在三个维度上同时占优，而且它是唯一已有公开验证的那一个。

| 领域 | 判定确定性 | 工程成本 | 供给规模 | 顺序 |
|---|---|---|---|---|
| Web 前端 | 五层组合 22/22，检出 11/11、误杀 0/11；两遍全量重跑判定翻面 0、明细逐字节一致（[Web 实验记录](../middle_processing/vc_data/14_web_verifier.md)） | 单次探针 4.9 秒，其中工具开销不到 0.5 秒，推算可压到 1 秒以内；读数全是浏览器原生接口 | 开源仓库自带大量视觉回归基线（[任务来源记录 §1](../middle_processing/vc_data/02_task_sources.md)）；可访问性这一维已有公开的确定性 reward 加 RL 结果（[A11yn](https://arxiv.org/abs/2510.13914)） | 第一 |
| 图表与矢量图 | 零容差，噪声地板实测为 0；逐值回读或结构断言 16/16（[图表实验记录](../middle_processing/vc_data/17_chart_verifier.md)） | 回读 1 到 4 毫秒；无需多视角渲染；判据只有四个阈值；与 Web 共用同一套浏览器 Harness | 渲染库自带的像素基线有 [Chart.js](https://github.com/chartjs/Chart.js/tree/master/test/fixtures) 约 667 张、[plotly.js](https://github.com/plotly/plotly.js/tree/master/test/image/baselines) 1,324 张、[p5.js](https://github.com/processing/p5.js/tree/main/test/unit/visual) 604 张、[deck.gl](https://github.com/visgl/deck.gl/tree/master/test/render/golden-images) 252 张、[OpenLayers](https://github.com/openlayers/openlayers/tree/main/test/rendering/cases) 235 个用例（GitHub API 计数，见[任务来源记录 §1](../middle_processing/vc_data/02_task_sources.md)） | 第二 |
| 网页游戏 | 24 条子命题设计上可做确定性判据，方差未测，6 条要 agent，3 条靠人（[游戏调研记录 §1](../middle_processing/vc_data/15_game_verifier.md)） | 要新建输入重放、绘制调用拦截、难度判据三件；Phaser 3 还要自己劫持构造函数 | [js13kGames](https://js13kgames.com/sitemap.xml) 2,799 个自包含作品（sitemap 实测，见[任务来源记录](../middle_processing/vc_data/02_task_sources.md)）；[PlaySuite](https://arxiv.org/abs/2610.07127) 从约 170 万个 itch.io 游戏加 1,460 个 PyWeek 游戏里筛出约 1.75 万个可执行环境，评测用其中 5,734 个；[V-GameGym](https://arxiv.org/abs/2509.20136) 收了 2,219 个 Pygame 样本 | 第三 |

数据解读：Web 排第一的理由不是它的判据最干净——图表才是唯一能把容差去掉的形态。Web 排第一是因为三件事同时成立：判别力在 22 个带标签变异上零漏零误；Verifier 的成本低到可以忽略；可访问性这一维已经有人用确定性 reward 把一个 7B 模型训到违例率低于闭源模型（[A11yn 表 2](https://arxiv.org/abs/2510.13914)）。

还有第四件，是做完上面三件之后才发现的：**审美里可程序化的那一半也挂在同一套 Web Harness 上。** 构造了 12 个只破坏审美不破坏功能的变异，其中 1 个判为无效，剩下 11 个里功能侧判据只顺带抓到 2 个，而新加的审美判据抓到 9 个、8 个合法改版零误杀，单页约 0.8 秒，是功能侧 4.9 秒的六分之一左右（[审美调研记录 §6.2](../middle_processing/vc_data/19_aesthetics.md)）。这意味着 Web 这条线一次性覆盖了两个维度——功能正确性和工艺质量——而其它两条线目前都只覆盖前者。

这四件各有折扣。零漏零误是第二遍的结果，第一遍 21/22，而且只有单参考页、6 个留出（[Web 实验记录](../middle_processing/vc_data/14_web_verifier.md)）。那项可访问性工作的训练 reward 与评测主指标是同一个量，所以它证明的是「这条链路能跑通」，不是「开源因此超过了闭源」；它的人工两两比较只有 5 名评测员、共 1,330 次判断，论文没有给显著性检验（[A11yn 附录 E](https://arxiv.org/abs/2510.13914)），稳妥的说法是人类偏好没有退化。即便都打完折，Web 仍然是目前唯一三件都有现成证据的领域，所以它是整条链路最便宜的验证实验。

图表排第二而不是第一，是因为它的优势在质不在量。零噪声意味着 reward 的方差全部来自题面歧义和模型自己，不来自判据，这正是乘法门控能够成立的前提；但它的供给面比 Web 窄，本机证据也只有单任务。把它放在 Web 之后还有一条工程理由：两者共用同一套浏览器 Harness，Web 先落地之后图表的边际成本接近零。

游戏排第三，不是因为它的判据差。24 条确定性判据同样不需要容差，但要先补三件新基础设施，而覆盖率这个瓶颈没有便宜的解法——同样的预算花在「再玩一遍」上只涨 0.5 个百分点，花在「把状态摆到前置条件上」才涨 8.0 个百分点（[A2Z 表 4(c)](https://arxiv.org/abs/2609.39564)），而后者本身就是一套要逐游戏投入的工程。

四个要打折扣的地方必须先说清楚。Web 侧是单参考页、22 个变异、其中 6 个留出，而且 22/22 是第二遍的结果，第一遍是 21/22；阈值一个没动，改的是一条测量实现和一条变异生成实现。Web 侧的作弊集补判据发生在作弊测试之后，「补完 6/7」这个数要和「第一版 5/7」一起看，剩下那一个是审计引擎的结构性盲区（[axe-core issue #2680](https://github.com/dequelabs/axe-core/issues/2680)），不是阈值能修的。图表侧的 16/16 只有 1 个任务、16 个变异，没有做留出验证，而且只测了一个图表库。游戏侧的全部数字来自公开文献，本机一行代码都没跑过，拆出来的 33 条子命题是设计而不是结论。

下一步三件事，按顺序做。第一，跑可访问性的确定性 reward 复现实验，这是整条链路最便宜也是唯一有公开背书的入口；但要把最佳实践规则和无障碍标准规则分开记账，并换第二个规则引擎做独立验证，避免 reward 和评测主指标是同一个量。第二，把 Web 的 Harness 扩成跨领域公共件，补上画布文字绘制拦截和输入重放两样——前者同时服务图表的数据标签自洽检查和游戏的分数读数，后者是游戏线唯一无法从现有组件复用的核心新件。第三，给三个领域各补一个留出被试：Web 换第二个参考页，图表补折线和饼图两个任务，游戏做第一个本机变异集；三处的阈值都一个不动，验证判别力能不能迁移。

## 参考文献

外部来源（按首次出现顺序）

1. [DePlot: One-shot visual language reasoning by plot-to-table translation](https://arxiv.org/abs/2212.10505) — Google Research，Fangyu Liu 等，2022-12-20
2. [Vision2Web: A Hierarchical Benchmark for Visual Website Development with Agent Verification](https://arxiv.org/abs/2603.26648) — Zehai He 等（智谱），2026-03-27
3. [WebGen-Bench: Evaluating LLMs on Generating Interactive and Functional Websites from Scratch](https://arxiv.org/abs/2505.03733) — Zimu Lu 等，2025-05-06
4. [MV-Bench: Benchmarking Multimodal Large Language Models for Coordinated Multi-View Interface Construction](https://arxiv.org/abs/2607.19910) — Yue Zhao 等，2026-07-22
5. [A11yn: Aligning LLMs for Web Accessibility-Aware UI Generation](https://arxiv.org/abs/2510.13914) — Janghan Yoon 等（延世大学、首尔大学），2025-10-15（引用数字取 v2，2026-09-07）
6. [axe-core 4.14.0 Rule Descriptions](https://github.com/dequelabs/axe-core/blob/v4.14.0/doc/rule-descriptions.md) — Deque Systems，v4.14.0
7. [axe-core issue #2680: Pseudo elements without position:absolute not picked up by color contrast](https://github.com/dequelabs/axe-core/issues/2680) — Deque Systems GitHub，2020-12-07 提出，仍 open
8. [GUI Agents for Continual Game Generation（PlaytestArena / Play2Code）](https://arxiv.org/abs/2605.28258) — Yixu Huang 等，2026-05-27
9. [PlaySuite: A Large-Scale Benchmark for Interactive Visual Intelligence](https://arxiv.org/abs/2610.07127) — Dheeraj Varghese 等，2026-10-05
10. [A2Z GameSpec-Bench: How Faithfully Can Coding Agents Generate Games from Game Design Specifications?](https://arxiv.org/abs/2609.39564) — Seonho Lee 等，2026-09-30
11. [Code2Games: Enabling Coding Agents for Gaming World Generation](https://arxiv.org/abs/2610.05033) — Wei Wu 等，2026-10-04
12. [V-GameGym: Visual Game Generation for Code Large Language Models](https://arxiv.org/abs/2509.20136) — Wei Zhang 等，2025-09-24
13. [UI-TARS-2 Technical Report: Advancing GUI Agent with Multi-Turn Reinforcement Learning](https://arxiv.org/abs/2509.02544) — ByteDance Seed，Haoming Wang 等，2025-09-02
14. [three.js](https://github.com/mrdoob/three.js) — mrdoob 等，GitHub 仓库
15. [PixiJS](https://github.com/pixijs/pixijs) — PixiJS 团队，GitHub 仓库
16. [Babylon.js](https://github.com/BabylonJS/Babylon.js) — Babylon.js 团队，GitHub 仓库
17. [p5.js](https://github.com/processing/p5.js) — Processing Foundation，GitHub 仓库
18. [Phaser](https://github.com/phaserjs/phaser) — Phaser Studio，GitHub 仓库
19. [Unity Manual: Call Unity C# script functions from JavaScript](https://docs.unity3d.com/Manual/web-interacting-browser-js-to-unity.html) — Unity Technologies，官方文档
20. [Godot Docs: JavaScriptBridge](https://docs.godotengine.org/en/stable/classes/class_javascriptbridge.html) — Godot Engine，官方文档（stable）
21. [ECMAScript Language Specification: Math.sin](https://tc39.es/ecma262/#sec-math.sin) — Ecma TC39，现行草案
22. [Chart.js test/fixtures](https://github.com/chartjs/Chart.js/tree/master/test/fixtures) — Chart.js 团队，GitHub 仓库目录
23. [plotly.js test/image/baselines](https://github.com/plotly/plotly.js/tree/master/test/image/baselines) — Plotly，GitHub 仓库目录
24. [p5.js test/unit/visual](https://github.com/processing/p5.js/tree/main/test/unit/visual) — Processing Foundation，GitHub 仓库目录
25. [deck.gl test/render/golden-images](https://github.com/visgl/deck.gl/tree/master/test/render/golden-images) — vis.gl，GitHub 仓库目录
26. [OpenLayers test/rendering/cases](https://github.com/openlayers/openlayers/tree/main/test/rendering/cases) — OpenLayers，GitHub 仓库目录
27. [js13kGames sitemap](https://js13kgames.com/sitemap.xml) — js13kGames，站点地图

本项目实验与调研记录

- [3D 本机实验记录（90_local_experiments）](../middle_processing/vc_data/90_local_experiments.md)
- [图表 Verifier 实验记录（17_chart_verifier）](../middle_processing/vc_data/17_chart_verifier.md)
- [Web Verifier 实验记录（14_web_verifier）](../middle_processing/vc_data/14_web_verifier.md)
- [游戏 Verifier 调研记录（15_game_verifier）](../middle_processing/vc_data/15_game_verifier.md)
- [审美调研与实验记录（19_aesthetics）](../middle_processing/vc_data/19_aesthetics.md)
- [任务来源调研记录（02_task_sources）](../middle_processing/vc_data/02_task_sources.md)

