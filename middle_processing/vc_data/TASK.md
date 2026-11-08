# 任务书（watchdog 续跑用）session=5e87912a-7389-48d5-9678-a18573730936
执行窗口：北京时间 2026-10-15 02:22 ~ 11:00。每轮先 `TZ=Asia/Shanghai date`。11:00 前禁止回复 WATCHDOG_TASK_COMPLETE。
用户在睡觉，不要停下来确认，不要提问。

## 目标
深度调研并推导：前沿模型（Anthropic Claude、OpenAI GPT-6/"astra" 等）如何构造 visual coding（Web / WebDev / three.js / Blender）的可验证训练数据。
Verified Task = Problem Statement（多模态参考）+ Harness（docker 镜像，含 blender/浏览器）+ Verifier（产物→reward）。
必须回答：
1. 任务来源：GitHub 里有没有高质量可用任务；开发者社区网站（CodePen/ShaderToy/Sketchfab/Blender StackExchange…）
2. 怎么把「描述+开发者写死的代码」变成可验证任务而不是模仿任务；如何评估数据质量（开发者代码不一定最好）
3. verifier 方案：学高质量代码 vs VLM judge vs 程序化检查；VLM 局限（three.js 截图只看到 2D）；给最有落地价值方案
4. 长程轨迹（150 步里 30 步试错）怎么修：剪枝成更短更高质量轨迹，是否保留纠错
## 产物位置
- 调研笔记：middle_processing/vc_data/*.md（agent 写）
- 原型：scripts/vc_verifier/（three.js 场景图 verifier + 多视角渲染，能跑）
- 成稿：alg/alg.md（Algorithm tab），python3 build.py 重建，截图自查
- 进度：middle_processing/vc_data/STATE.md（每完成一步追加一行）
## 规则
- 写作：简洁、层级清晰、无 $ 符号（写「美元」）；数字要有来源
- 大文件分段写，单次 Write 不超过 300 行
- 主目标提前完成 ≠ 收工：继续核验引用、补原型、润色，到 11:00 再交付并回复 WATCHDOG_TASK_COMPLETE
- 交付链接：https://kml-dtmachine-100001395-prod-web-server.kce-aip-wlf1-hb2az1.corp.kuaishou.com/view/mmu_mllm_hdd_4/deep-research/visual-coder-blog/index.html#alg

