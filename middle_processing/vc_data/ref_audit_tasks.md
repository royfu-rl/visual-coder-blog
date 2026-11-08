# draft_tasks.md 引用审计（2026-10-15）

- 改动文件：`/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/vc_data/draft_tasks.md`
- 改前备份：`middle_processing/alg_draft_backup/1015-2300-before-refs/draft_tasks.md`
- 节标题、`tk-1` 到 `tk-9` 锚点、demo iframe 均未动；文末新增 `## 参考文献`（不带编号）

## 1 统计

| 项 | 数 |
|---|---|
| 链接总数（`](http` 出现次数） | 207 |
| 其中外部链接 / 内部 `/view` 链接 | 151 / 56 |
| 不同 URL | 81（外部 70，内部 11） |
| 参考文献条目（外部来源） | 66 |
| arXiv 论文 | 40 篇，全部用 export API 核对过标题与 v1 日期，无编号错位 |
| 外部 URL 实测 | 70 个里 68 个返回 200（objaverse-xl 仓库首测 504，重试 200）；2 个 CLI 403 |
| 内部 `/view` 链接 | 11 个目标文件都在盘上；网关拒 IDC 网段，未做 HTTP 实测 |

- 数字核对方式
  - 本地有全文的：`papers/<id>.txt` 逐处 grep（SWE-bench、SWE-bench M、WorldCoder、RaR、R2E-Gym、DAPO、SWE-Gym、SWE-smith、Design2Code、WebCode2M）
  - 本地没有的：经代理下载 arXiv HTML 后 grep（Infinigen、ProcTHOR、HSSD v1/v3、DataComp、Density&Coverage v1/v2、2609.40115、Online Difficulty Filtering、SPICE、Fantastic Bugs、SWE-rebench、Skywork-OR1、GRESO、FineWeb、LMSYS 去污、Strong Collapse、Nemotron-CC、GameDevBench、CAD-Coder、CodeContests+）
  - 非论文：js13k sitemap 重新计数（2,799，2026 年 317）、Stack Exchange 标签接口重查（python 13,632 + scripting 6,738）、Shadereval HF 卡片（202k 未过滤函数、467 条）、CodePen 许可页（公开 pen 为 MIT）、Figma robots（点名 GPTBot / ClaudeBot / CCBot）

## 2 改正过的数字与表述

| 位置 | 原文 | 改为 | 依据 |
|---|---|---|---|
| §2 表 Infinigen 行 | 约 246 个生成器 | 论文自报 182 个生成器 | Infinigen 表 2；246 是本项目按测试清单数的，13_scaling_tasks §7.2 第 16 条已注明对外用论文口径 |
| §2 预训练段 | Objaverse-XL 的 1,085 万个对象 | 论文自报 1,020 万个去重对象（HF 元数据 1,085 万行） | 2307.05663 标题与摘要「10M+」；09_pretrain_data §1.3 |
| §2 预训练段 | 「真实页面清洗后 5,366 token…原始页面更是 31,216」 | 明确前者是 WebCode2M、后者是 Design2Code 收的 C4 页面 | WebCode2M 表 2 |
| §4 核心发现 | LLM 提的破坏里有 6% 到 12% 看不出 | 约一成（桌子 1/10，工作台补层前 2/16） | 90_local_experiments §4 表：10% 与 12.5%，找不到 6% 的出处 |
| §6 第四条闸成本 | 相对造题开销是一成左右的增量 | 约两成（每候选平均 4.5 次调用，121 万 / 26.9 万） | 13_scaling_tasks §5.6 |
| §8 表 HSSD 行 | 19% 对 17% | 保留，并注明是 v1 正文；v3 表 5 修订为 19.2% 对 12.5% | 2306.11290v1 正文、v3 表 5 |
| §8 表「ProcTHOR 自己扩产」行 | 122 扩到 10,000 后微调指标 46/21 变 45/21 | 48.48 / 22.79 变 48.32 / 21.80 | 46/22 对 45/21 是 v1 表 6 里 HSSD-122 对 ProcTHOR-10K，不是 ProcTHOR 自己扩产；ProcTHOR-122 对 ProcTHOR-10K 只在 v3 表 6 |
| §8 pass@8 解读 | 两种口径差 3.2 倍（70% 对 19%） | 差约 3.7 倍 | 0.70 / 0.19 = 3.7；3.2 是成本放大倍数（37.2% / 11.8%），原文把两个数混了 |
| §8 双边过滤 | 同一区间离线做（用外部模型当难度代理）也是负收益 | 离线筛题只到 26.3 到 28.4，低于在线的 30.1 | 2504.03380 表 1：外部模型离线 curation 28.4，高于 plain 26.3，不是负收益 |
| §8 末段 | 桌子那批任务里两道全军覆没的题 | 两道没过的题 | 90 §5：是 opus-5.5 一轮没过；全军覆没（32 组全挂）的是 §6 另一道题，原因不同 |
| §9 首句 | 端到端留存率是千分之几 | 千分之几到百分之几 | 同表 SWE-bench 2.46%、SWE-rebench 4.74%、SWE-Gym 3.77% |
| §9 资源表 LLM 行 | 难度标定占 65% | 优化前 121 万次里难度标定占 65% | 13 §5.6：65% 是优化前口径，优化后 95 万次口径下不成立 |
| §9 两段式省多少 | 133 万降到 78 万……省 31% | LLM 总调用从 176 万降到 121 万，省 31% | 13 §5.6：31% 是总调用口径；只算标定是省 41% |
| §9 合成占比 | 工程实测 30% 到 45% 的合成占比仍是正收益 | 约 30% 的合成占比仍不掉点（6.3T 里 1.9T 合成，MMLU 与 DCLM 持平） | Nemotron-CC 摘要与贡献列表；45% 来自 HQ 子集构成表，HTML 里取不到表 4，未能核实 |
| §9 Skywork | 54%（7B）到 63%（32B）的题 | 加限定「数学题」 | Skywork-OR1：21.4+32.4 与 20.7+42.0 是 math 列，code 列不同 |
| §9 GRESO | 训练中 | 训练后期 | 2506.02177 原文「at the late stage of training」 |
| §9 钉死难度带 | 最便宜的办法是在 47 个任务上先跑一次 pass@8 | 已在 16 道题上跑过（128 次）；扩到 47 个才是 376 次 | 同节上文已引用 90 §15 的实测，原句是过期的待办 |
| §9 FineWeb | 全局去重把 20T 砍到 4T | 全局去重后只剩 4T，逐快照独立去重是 20T | 2406.17557 §3.4：20T 是另一种做法的产出，不是全局去重的起点 |

以下数字回原文核对一致，未改：SWE-bench M 135k → 1,478 → 617 与 Fleiss 0.78；WorldCoder τb −0.021 / −0.068 / 1.000 与误放率 33.7% / 45.6% / 0（1,434 对）；RaR 31.7% / 35.9%；SWE-bench 93,139 → 2,294（表 10）；SWE-rebench 450K、14%、31%、21,336；SWE-Gym 64,689 → 2,438；SWE-smith 100,074 → 50,137（50.1%）；Design2Code 127.9k → 484；Infinigen 182 / 1,070 / 「proxy」；ProcTHOR 100 billion 与 1.60 / 10.4 / 4.65 / 9.70；DataComp 0.9 / 0.8 / 0.02；D&C v1 0.108 → 0.714、0.020 → 0.653；Jaccard 0.7265 与 242；ODF 26.3 / 27.3 / 30.1 / 29.9；DAPO 42 → 50；SPICE α 0.24；Fantastic Bugs 84%、1 分钟；GameDevBench 41 题 43 / 50 / 7；R2E-Gym 不到 20%；FineWeb 4T / 20T / 90%；LMSYS 10-gram F1 0；Strong Collapse 1%。

## 3 删除或弱化的无出处陈述

| 位置 | 原文 | 处理 | 原因 |
|---|---|---|---|
| §2 表 ShaderToy 行 | 规模 5 万以上 | 改为「shaders21k 约 2.1 万个程序；ShaderToy 全站总数未能核实」 | 调研笔记的 5.2 万来自 Wikipedia 2021 年口径，当前 Wikipedia 页面已无该数字；ShaderToy 官网对 CLI 403 |
| §2 表 ShaderToy 行 | 默认 NC-SA | 保留，标「二手口径，官方 terms 未能实测」 | 官方 terms 页 403，未找到可打开的一手来源 |
| §2 表 Blender SE 行 | 约 2 万个问题 | 改为「`python` 加 `scripting` 两个标签约 2 万个」 | 写明口径；两标签可能重叠，按上界读 |
| §9 去重段 | The Stack、StarCoder、CodeGen、AlphaCode、OpenCoder 全部是 MinHash，唯一的结构哈希是 LLVM 中间表示那一家 | 改为「The Stack、StarCoder 等……本项目检索到的唯一结构哈希是 ComPile」 | CodeGen / AlphaCode / OpenCoder 的去重方式本轮未回原文核对，不再点名；「唯一」改为检索范围内的结论 |
| §9 three.js 漏斗 | 各步留存直接给数 | 加一句「除仓库数与准入率外，各步留存都是估计值」 | 13 §4.2.5 原文就标了【估】 |
| §9 Nemotron-CC | 45% 上界 | 删掉 | 见上表，HQ 子集构成未能核实 |

## 4 未能实测的 URL

| URL | 结果 | 处理 |
|---|---|---|
| https://www.shadertoy.com/ | CLI 403（海外代理与 WebFetch 都被拦） | 保留，作为站点本身的指代 |
| https://www.shadertoy.com/terms | CLI 403 | 保留，正文标「未能实测」 |
| https://projects.blender.org/blender/blender/src/branch/main/tests | CLI 403（挑战页） | 不用，换成 GitHub 镜像 https://github.com/blender/blender/tree/main/tests/files/render（200） |
| https://www.frontendmentor.io/faq | 404 | 不用，换成 https://www.frontendmentor.io/faqs（200，原文有「please don't distribute the design files」） |
| 11 个 KML `/view` 内部链接 | 网关禁 IDC 网段，训练机上无法 HTTP 实测 | 已确认目标文件都在盘上 |

## 5 仍不确定的地方

1. HSSD 的两个版本数字不一致（v1 19% 对 17%，v3 19.2% 对 12.5%），正文两版都列了；如果只想留一个，建议用 v3
2. WorldCoder「状态契约 1.000」是契约自己对真值的相关，定义上就是 1，正文已注明「契约本身就是真值」，但仍可能被读成实测结果
3. 「公开可复用的配对总量约 1,000 万条」是本项目把 WebSight、WebCode2M、DaTikZ、SVG-Stack、CAD 系加起来的汇总，没有单一外部出处，只链到了 09_pretrain_data

## 第二轮（按 ref_gaps_tasks.md 的 20 处）

- 链接总数 207 → 227；新增外部来源 1 个：[The Verification Horizon](https://arxiv.org/abs/2606.26300)（abs 页 `<title>` 核对一致，原文 grep 到「no fixed reward function can remain effective as policy capability continues to grow」）
- 本轮用到的其余 arXiv（2310.06770、2504.07164、2602.11103、2505.19713）都在 abs 页核过 `<title>`
- 20 处全部处理，没有剩余

| 清单行 | 类型 | 处理 |
|---|---|---|
| L25 3,413 commit / 1.9 万张 | 本项目 API 实测 | 链 02_task_sources §1.1，写明 `commits?path=` 末页页码与 `git/trees` 计数的查询方法；补「上表除 Blender、plotly.js」口径 |
| L77–81 参考代码五个用途 | 本项目设计 | 列表前加「本项目设计」并链 03 §3.1 与 gen_tasks.py；第 1 步链 SWE-bench、GameDevBench，第 5 步链 CAD-Coder（引用了文献做法） |
| L135 难度筛选正反馈 | 本项目观察 | 链 90 §6.3（一道 0% 题会被难度筛选优先保留） |
| L139–142 可解性闸四步 | 本项目设计 | 列表前加「本项目设计、尚未实现」并链 13 §2.3.6 ceiling check |
| L184 R2E-Gym 不到 20%、GameDevBench 43% | 外部事实 | 链 R2E-Gym 图 5 与正文（papers/2504.07164.txt 原文「typically less than 20% of tests」）；链 GameDevBench（原文 41 题、43% / 50% / 7%） |
| L186 指标周期重算 | 外部结论 | 链 The Verification Horizon 引言原句 |
| L207 / L221 / L243 十道题通过率 | 本项目实验 | 链 90 §9 |
| L225 / L227 / L239 pass@8 16 题、3/16、Wilson | 本项目实验 | 链 90 §15 与 passk.py；Wilson 区间按公式复算为 6.6% 到 43.0%，一致 |
| L290 成本乘 3.2 | 本项目推算 | 写明 37.2% / 11.8%，链 90 §15 与 13 §5.2 |

- 没有发现新的数字错误
- R2E-Gym 原稿笔记写的是「§4.2」，全文里这句的位置不在 4.2 小节，所以正文改成「图 5 与正文」，不写节号

