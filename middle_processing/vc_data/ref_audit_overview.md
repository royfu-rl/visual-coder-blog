# draft_overview.md 补引用审计（2026-10-15）

备份：`middle_processing/alg_draft_backup/1015-2300-before-refs/`

## 1 统计

| 项 | 数 |
|---|---|
| 正文内联链接 | 129 |
| 参考文献条目（外部来源） | 58 |
| 链接总数（`](http` 出现次数） | 187 |
| 不同 URL | 74（外部 58，本项目记录 16，含本文件） |
| arXiv 来源 | 32 篇，全部用 export.arxiv.org API 核对标题与 v1 日期，编号无错位 |
| 外部 URL 实测 | 57 个 200；1 个 CLI 403（见 §5） |
| 本项目 /view 链接 | 16 个，目标文件均在盘上存在；/view 在 IDC 网段 403 属正常，未实测 |
| 改正的数字或归属 | 11 条（§2） |
| 删除 / 弱化 | 6 条（§3） |

## 2 改正过的数字与归属

| 原文 | 改为 | 依据 |
|---|---|---|
| SigLIP2 相似度 Astra 与 Opus 5.5「只差 0.002」 | 约 0.001（0.1081 对 0.1067） | 3JSBench 站点 bundle 里的原始均值；0.002 是 91 记录里两个四舍五入的相对值（+0.011、+0.009）相减 |
| 「10 个模型」SigLIP 落在 0.0774 到 0.1081 | 11 个模型（含 inkling，不在主榜 10 个里） | 同上，SigLIP 面板含 11 个模型 |
| Design2Code 判据「像素与 DOM 四项」 | o4-mini 看图打 0 到 100 相似分，标为非确定性对照 | Qwen3-VL 报告附录 B.10 的评测 prompt「Design2Code (GPT-o4-mini Evaluation)」 |
| AutoLab「kimi-k2.6 加 0.43」（与其他模型同为相对 terminus-2 的增益） | kimi-k2.6 在三个 harness 间最多差 0.43（pi-mono 0.21 到 mini-swe-agent* 0.64） | AutoLab 原文：「shift by as much as Δ=0.43 … kimi-k2.6: 0.21→0.64 from pi-mono to mini-swe-agent*」；相对 terminus-2 的增益只列了 deepseek-v4-flash +0.13、mimo-v2.5 +0.20、gpt-5.4 −0.03 |
| 判别力「RewardBench 2 上只差 0.5」 | RewardBench 2 上权重公开的专用 RM 反而领先 4.6（Skywork-Reward-V2-Llama-3.1-8B 84.1 对 gemini-2.5-pro 79.5） | RewardBench 2 表 3：gemini-2.5-flash 是 77.7 不是 77.2；QRM-Gemma-2-27B 76.7 也不是开源最好 |
| 「ProcessBench 上差 16.4」（无模型名） | 补出 o1-mini 87.9 对 QwQ-32B-Preview 71.5，并注明是 2024 年模型 | ProcessBench 表 3 |
| Design Arena「约差 69 Elo」（1392 对 deepseek-v4-1-flash 1323） | 约差 29（1392 对 kimi-k3 1363） | Design Arena 2026-10-15 直读；Kimi K3 是开放权重（vals.ai 原文「the first open-weight model to reach the top tier」，K3 报告标题「Open Frontier Intelligence」） |
| Code Arena WebDev「约差 139」（1813 对 Qwen3.8-Max 1674） | 约差 159（1813 对 Kimi K3 1654） | 镜像快照 2026-10-08；Qwen3.8-Max 的权重是否公开无出处，不能当「开源最好」 |
| Vibe Code Bench「开源最高 85.22%」（MiMo V2.6 Pro） | 权重公开的最高 Kimi K3 84.97%，差约 7 点不变 | vals.ai 原文只把 Kimi K3 称为开放权重；MiMo V2.6 Pro 的权重状态没有出处 |
| 「这两行本身也没有独立核验过」（3DHarnessBench） | 已回原文表 1 逐值核对一致 | 92_number_audit §二；本次再读表 1 UNI3D 列：Qwen 0.740 → 0.809，Opus 5 0.725 → 0.871 |
| 「对照组里同一批标注员无 rubric 65.0% → 92.0%」（读起来像 AUV-Bench 的数） | 归到 WebDevJudge 表 1，注明 100 条对另 50 条、不是受控对比 | WebDevJudge 表 1；19_aesthetics §5.1 |
| §7「图表与 Web 都没有做留出」 | Web 的 6 个留出变异与开发集同属一个任务，图表没有做留出 | STATE.md「22 个变异（开发 16 + 留出 6）」；14_web_verifier §2.4 |
| 平局率 24.3% / 17.0% 未注明口径 | 注明是 webdev-arena-preference-10k（10,501 条）实算，不是博客的 26% | 19_aesthetics §5 |

（共 13 行，其中前 11 行是数字或归属的实质改正，后 2 行是口径补注。）

核对一致、未改的关键数字：WorldCoder 表 2 四行、27.8 / 25.3 / 「no system exceeds 30%」；3JSBench 80.0 / 49.0 / 23.0；WorldBench 5.44 / 7.11；MTAC 78.6 / 80.4 / 60.6 / 12.7 → 6.7；A11yn 0.13 / 0.05 / 0.35 / 0.26 / 1,330 / 64.7%；Vision2Web 开源全栈 0.0；Vibe Code 82.72 / 77.48 / 69.85 / 67.39 / 58.19；VISTA 73.0 / 44.5 / 8.3 / 8,487；RubSE −2.73；FronTalk 56.0 → 65.3、+5.9、+0.8；AutoLab 0.68 / 0.50 / 0.46 / 0.36；GPT-6 Astra 30.9 / 3.6 分钟；JAMER 80.4% / 5.7%；Opus 5 SWE-MM 59.4；Qwen3.8-27B SWE-MM 38.6；GLM-5V-Turbo Design2Code 94.8；M2.5 超 20 万环境；axe-core 105 条规则；CriticGPT 约 30 倍；AUV-Bench 51 / 1,395 / 0.368 / 0.637；judge 共识 0.21 / 3.5 / 28%；Animation2Code 0.31；SWE-Master 57.8 / 61.4 / 70.2 / 70.8；本地审美实验 12 / 9 / 8（out/aes_results.json）。

## 3 删除 / 弱化的陈述

| 原陈述 | 处理 | 原因 |
|---|---|---|
| 「Design2Code 所有模型挤在 93 以上」 | 改为「头部模型挤在 93 以上」 | 只引了两个模型的分数 |
| SWE-bench Multimodal「Opus 5 59.4 对 Qwen3.8-27B 38.6」 | 保留，加注两边都是自报、harness 不同 | Opus 5 用内部 harness，Qwen 用 Claude Code harness |
| Kimi K3 / K2.5 / Qwen3-VL / MiniMax-M2 / MiMo / Gemini 2.5 的章节号（§3.1、§4.2.7、附录 B.3 等） | 删掉章节号，只留论文链接 | 引文原句已核到，章节号只来自调研笔记，未逐个核 |
| FronTalk「AceCoder 子项」 | 改为「它提出的 AceCoder（agent 批判后重写）」 | AceCoder 是该文提出的方法，不是榜单子项 |
| OpenAI「交互测试规程」挂在前端提示文档名下 | 改挂到 playwright-interactive skill | 三方清单制度出自该 skill，不在前端提示文档里 |
| 「grader hacking 高风险」未注明出处文件 | 指向 Fable 5 / Mythos 5 system card | primary_src 里只有这份 card 含此原句 |

## 4 仍然只有单一来源、没能逐值核到的

| 陈述 | 现状 |
|---|---|
| Qwen3-VL-235B-Thinking 在 Design2Code 上 93.4 | 报告表 2 是图片，HTML 抽不出数字；数字来自 frontier_evals_cn.md 的转录 |
| SWE-bench Verified 同 harness 76.8 对 75.8 | 官方站数据里两个数都在，但同分条目多，模型与条目的一一对应沿用笔记（快照 2026-02-17） |
| 审美判据「成本只有功能侧的六分之一」 | 出自 STATE.md 实验日志，结果 json 里没有直接的成本字段 |

## 5 未能实测或有保留的 URL

| URL | 情况 | 处理 |
|---|---|---|
| https://openai.com/index/gpt-5-6/ | CLI 走代理返回 403（Cloudflare），未能实测 | 保留；primary_src/oai_gpt56.txt 经 r.jina.ai 读到原文「inspect and refine the rendered result」 |
| https://lmarena.ai/leaderboard/webdev | CLI 403 | 未使用，改用 respan 镜像 |
| https://projects.blender.org/blender/blender/src/branch/main/tests/files/render | CLI 403 | 未使用，改用 GitHub 镜像（200） |
| 16 个 KML /view 链接 | IDC 网段访问 403 属正常 | 只核了目标文件在盘上存在 |

## 第二轮（ref_gaps_overview.md 的 24 处）

新增链接 22 条，链接总数 187 → 209。新增外部 URL 0 个（都复用第一轮已实测 200 的地址）；arXiv 标题改用 abs 页 `<title>` 复核：2609.06535、2510.13914、2310.06770 均一致。

| 行（生成时） | 处理 |
|---|---|
| L22、L36、L49 | 核心发现 / 结论句句末回指 3JSBench、WorldCoder-Bench 表 1 |
| L62 | **弱化**：删掉「76.8 已接近饱和区」「优化了两年」两处无出处说法，改为「SWE-bench 2023-10 发布（arXiv v1 日期），是被针对性优化最久的公开榜之一，头部分数挤在一起」，链 SWE-bench 论文与官方榜 |
| L64 | 「表 2」明确为 A11yn 表 2 的 IR_AChecker 列（0.26 对 GPT-5.1 0.35，第一轮已从 HTML 表格逐值核对） |
| L103 | 回指 3DHarnessBench 表 1 |
| L130 | 无数字；补回指到反转证据表与 07 §2.1 |
| L136 | 1.0 点链 SWE-bench Bash Only 榜 |
| L146 | 14 维切分链 07_capability_spec §1.1、§1.2 |
| L150、L151 | 逐条链 3DHarnessBench 表 3，并注明 10 个实例、UNI3D 列（papers/2609.06535.txt 表 3/表 11 核对：0.3722 → 0.6148，0.6776 → 0.7605，一致） |
| L196 | 链 hillclimb 博客原句「not a 1-to-5 scale」 |
| L221、L230、L232、表 L234 | 链 07_capability_spec §4.1（公式推导）与 §4.3（MDE 表） |
| L226、L227 | 代码块内不能放链接；由紧邻上一句的 §4.1 链接覆盖 |
| L245–L247 | 逐条给出算式与 07 §4.3 链接；本轮复算全部一致（1.98/√120 = 18.1，2.38/√120 = 21.7，……，1.98/√63 = 0.249，1.98/√5 = 0.885） |
| L282 | 观点；补回指 07 §2.1「最终归因」（原文标为推断） |
| L310 | 「同上」换成 90_local_experiments §15 的直接链接，补出 70% 的口径（跨 4 个模型汇总）与 19% 的分子分母（3/16） |
| L69 | 纯观点、无数字，按规则不加链接 |

未解决：0 条。L69 有意不加链接（纯观点）；L226/L227 的公式在代码块里，由紧邻那一句的 07 链接覆盖。

