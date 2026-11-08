# Algorithm 页引用复核

- 链接 924 处，不同 URL 240 个，实测通过 234，未通过 6

## 未通过的链接

| 状态 | URL | 出现在 |
|---|---|---|
| cli403 403 | https://doi.org/10.1145/3569889 | verifier, verifier |
| bad 503 | https://github.com/NVIDIA-NeMo/RL/blob/main/docs/guides/async-grpo.md | training, training |
| bad 503 | https://github.com/dequelabs/axe-core/blob/v4.14.0/doc/rule-descriptions.md | domains, domains |
| cli403 403 | https://openai.com/index/gpt-5-6/ | overview |
| cli403 403 | https://www.shadertoy.com/ | tasks, tasks |
| cli403 403 | https://www.shadertoy.com/terms | tasks, tasks |

## arXiv 标题（人工核对与引用名是否同一篇）

| 引用名 | 编号 | 实测标题 |
|---|---|---|
| Reliable Fidelity and Diversity Metrics for Generative Model | 2002.09797v1 | Reliable Fidelity and Diversity Metrics for Generative Models |
| ProcTHOR / ProcTHOR: Large-Scale Embodied AI Using Procedura | 2206.06994 | ProcTHOR: Large-Scale Embodied AI Using Procedural Generation |
| The Vendi Score: A Diversity Evaluation Metric for Machine L | 2210.02410 | The Vendi Score: A Diversity Evaluation Metric for Machine Learning |
| The Stack / The Stack: 3 TB of permissively licensed source  | 2211.15533 | The Stack: 3 TB of permissively licensed source code |
| Procedural Image Programs for Representation Learning（shader | 2211.16412 | Procedural Image Programs for Representation Learning |
| DePlot / DePlot: One-shot visual language reasoning by plot- | 2212.10505 | DePlot: One-shot visual language reasoning by plot-to-table translation |
| DataComp / DataComp: In search of the next generation of mul | 2304.14108 | DataComp: In search of the next generation of multimodal datasets |
| StarCoder / StarCoder: may the source be with you! | 2305.06161 | StarCoder: may the source be with you! |
| Infinigen / Infinite Photorealistic Worlds using Procedural  | 2306.09310 | Infinite Photorealistic Worlds using Procedural Generation |
| HSSD v3 / Habitat Synthetic Scenes Dataset (HSSD-200) | 2306.11290 | Habitat Synthetic Scenes Dataset (HSSD-200): An Analysis of 3D Scene Scale and Realism Tra |
| HSSD-200 | 2306.11290v1 | Habitat Synthetic Scenes Dataset (HSSD-200): An Analysis of 3D Scene Scale and Realism Tra |
| Objaverse-XL / Objaverse-XL: A Universe of 10M+ 3D Objects | 2307.05663 | Objaverse-XL: A Universe of 10M+ 3D Objects |
| ComPile / ComPile: A Large IR Dataset from Production Source | 2309.15432 | ComPile: A Large IR Dataset from Production Sources |
| SWE-bench / SWE-bench: Can Language Models Resolve Real-Worl | 2310.06770 | SWE-bench: Can Language Models Resolve Real-World GitHub Issues? |
| Cousins Of The Vendi Score: A Family Of Similarity-Based Div | 2310.12952 | Cousins Of The Vendi Score: A Family Of Similarity-Based Diversity Metrics For Science And |
| LMSYS 实测 / Rethinking Benchmark and Contamination for Langua | 2311.04850 | Rethinking Benchmark and Contamination for Language Models with Rephrased Samples |
| Monkey / Monkey: Image Resolution and Text Label Are Importa | 2311.06607 | Monkey: Image Resolution and Text Label Are Important Things for Large Multi-modal Models |
| GPT-4V(ision) is a Generalist Web Agent, if Grounded（SeeAct） | 2401.01614 | GPT-4V(ision) is a Generalist Web Agent, if Grounded |
| WebVoyager 表 1 / WebVoyager: Building an End-to-End Web Agen | 2401.13919 | WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models |
| MLLM-as-a-Judge / MLLM-as-a-Judge: Assessing Multimodal LLM- | 2402.04788 | MLLM-as-a-Judge: Assessing Multimodal LLM-as-a-Judge with Vision-Language Benchmark |
| Design2Code / Design2Code 表 1 / Design2Code: Benchmarking Mu | 2403.03163 | Design2Code: Benchmarking Multimodal Code Generation for Automated Front-End Engineering |
| TextMonkey / TextMonkey: An OCR-Free Large Multimodal Model  | 2403.04473 | TextMonkey: An OCR-Free Large Multimodal Model for Understanding Document |
| WorkArena 表 2 / WorkArena: How Capable Are Web Agents at Sol | 2403.07718 | WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks? |
| Unlocking the conversion of Web Screenshots into HTML Code w | 2403.09029 | Unlocking the conversion of Web Screenshots into HTML Code with the WebSight Dataset |
| MM1 / MM1: Methods, Analysis & Insights from Multimodal LLM  | 2403.09611 | MM1: Methods, Analysis &amp; Insights from Multimodal LLM Pre-training |
| Duan et al. CHI 2024 / Generating Automatic Feedback on UI M | 2403.13139 | Generating Automatic Feedback on UI Mockups with Large Language Models |
| Is Model Collapse Inevitable? / Is Model Collapse Inevitable | 2404.01413 | Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accumulating Real and Syn |
| WebCode2M / WebCode2M: A Real-World Dataset for Code Generat | 2404.06369 | WebCode2M: A Real-World Dataset for Code Generation from Webpage Designs |
| BlenderAlchemy / BlenderAlchemy: Editing 3D Graphics with Vi | 2404.17672 | BlenderAlchemy: Editing 3D Graphics with Vision-Language Models |
| Plot2Code / Plot2Code: A Comprehensive Benchmark for Evaluat | 2405.07990 | Plot2Code: A Comprehensive Benchmark for Evaluating Multi-modal Large Language Models in C |
| Beyond Model Collapse / Beyond Model Collapse: Scaling Up wi | 2406.07515 | Beyond Model Collapse: Scaling Up with Synthesized Data Requires Verification |
| Judging the Judges / Judging the Judges: A Systematic Study  | 2406.07791 | Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge |
| ChartMimic / ChartMimic 表 5 / ChartMimic: Evaluating LMM's C | 2406.09961 | ChartMimic: Evaluating LMM&#39;s Cross-Modal Reasoning Capability via Chart-to-Code Genera |
| Automatically Generating UI Code from Screenshot: A Divide-a | 2406.16386 | Automatically Generating UI Code from Screenshot: A Divide-and-Conquer-Based Approach |
| FineWeb / The FineWeb Datasets: Decanting the Web for the Fi | 2406.17557 | The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale |
| CriticGPT / LLM Critics Help Catch LLM Bugs（CriticGPT） | 2407.00215 | LLM Critics Help Catch LLM Bugs |
| SWE-bench Multimodal / SWE-bench Multimodal: Do AI Systems G | 2410.03859 | SWE-bench Multimodal: Do AI Systems Generalize to Visual Software Domains? |
| Strong Model Collapse | 2410.04840 | Strong Model Collapse |
| Self-Preference Bias / Self-Preference Bias in LLM-as-a-Judg | 2410.21819 | Self-Preference Bias in LLM-as-a-Judge |
| VL-RewardBench / VL-RewardBench: A Challenging Benchmark for | 2411.17451 | VL-RewardBench: A Challenging Benchmark for Vision-Language Generative Reward Models |
| Nemotron-CC / Nemotron-CC: Transforming Common Crawl into a  | 2412.02595 | Nemotron-CC: Transforming Common Crawl into a Refined Long-Horizon Pretraining Dataset |
| PaliGemma 2 表 13 / PaliGemma 2: A Family of Versatile VLMs f | 2412.03555 | PaliGemma 2: A Family of Versatile VLMs for Transfer |
| ProcessBench 表 3 / ProcessBench: Identifying Process Errors  | 2412.06559 | ProcessBench: Identifying Process Errors in Mathematical Reasoning |
| GraphEQA 表 2 / GraphEQA: Using 3D Semantic Scene Graphs for  | 2412.14480 | GraphEQA: Using 3D Semantic Scene Graphs for Real-time Embodied Question Answering |
| SWE-Gym / SWE-Gym 表 6 / Training Software Engineering Agents | 2412.21139 | Training Software Engineering Agents and Verifiers with SWE-Gym |
| AgentRefine / AgentRefine 表 2 / AgentRefine: Enhancing Agent | 2501.01702 | AgentRefine: Enhancing Agent Generalization through Refinement Tuning |
| Agent-R / Agent-R: Training Language Model Agents to Reflect | 2501.11425 | Agent-R: Training Language Model Agents to Reflect via Iterative Self-Training |
| SigLIP 2 / SigLIP 2: Multilingual Vision-Language Encoders w | 2502.14786 | SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Loca |
| Advancing vision-language models in front-end development vi | 2503.01619 | Advancing vision-language models in front-end development via data synthesis |
| L1 / L1 附录 A.7 / L1: Controlling How Long A Reasoning Model  | 2503.04697 | L1: Controlling How Long A Reasoning Model Thinks With Reinforcement Learning |
| DAPO / DAPO 表 1 / DAPO: An Open-Source LLM Reinforcement Lea | 2503.14476 | DAPO: An Open-Source LLM Reinforcement Learning System at Scale |
| Dr. GRPO / Understanding R1-Zero-Like Training: A Critical P | 2503.20783 | Understanding R1-Zero-Like Training: A Critical Perspective |
| Online Difficulty Filtering / Online Difficulty Filtering fo | 2504.03380 | Online Difficulty Filtering for Reasoning Oriented Reinforcement Learning |
| R2E-Gym / R2E-Gym: Procedural Environments and Hybrid Verifi | 2504.07164 | R2E-Gym: Procedural Environments and Hybrid Verifiers for Scaling Open-Weights SWE Agents |
| Acting Less is Reasoning More! Teaching Model to Act Efficie | 2504.14870 | Acting Less is Reasoning More! Teaching Model to Act Efficiently |
| SWE-smith / SWE-smith: Scaling Data for Software Engineering | 2504.21798 | SWE-smith: Scaling Data for Software Engineering Agents |
| WebGen-Bench / WebGen-Bench: Evaluating LLMs on Generating I | 2505.03733 | WebGen-Bench: Evaluating LLMs on Generating Interactive and Functional Websites from Scrat |
| Skywork-VL Reward 表 3 与 §3 / Skywork-VL Reward: An Effective | 2505.07263 | Skywork-VL Reward: An Effective Reward Model for Multimodal Understanding and Reasoning |
| Qwen3 / Qwen3 Technical Report / Qwen3 技术报告 / Qwen3 表 21 | 2505.09388 | Qwen3 Technical Report |
| 2505.11821 表 3 / Reinforcing Multi-Turn Reasoning in LLM Age | 2505.11821 | Reinforcing Multi-Turn Reasoning in LLM Agents via Fine-Grained Reward Structure and Credi |
| CAD-Coder / CAD-Coder 附录 B / CAD-Coder: Text-to-CAD Generati | 2505.19713 | CAD-Coder: Text-to-CAD Generation with Chain-of-Thought and Geometric Reward |
| SWE-rebench / SWE-rebench: An Automated Pipeline for Task Co | 2505.20411 | SWE-rebench: An Automated Pipeline for Task Collection and Decontaminated Evaluation of So |
| RLRF 表 5 / Rendering-Aware Reinforcement Learning for Vector | 2505.20793 | Rendering-Aware Reinforcement Learning for Vector Graphics Generation |
| Skywork Open Reasoner 1 Technical Report / Skywork-OR1 | 2505.22312 | Skywork Open Reasoner 1 Technical Report |
| AReaL / AReaL: A Large-Scale Asynchronous Reinforcement Lear | 2505.24298 | AReaL: A Large-Scale Asynchronous Reinforcement Learning System for Language Reasoning |
| RewardBench 2 表 3 / RewardBench 2: Advancing Reward Model Ev | 2506.01937 | RewardBench 2: Advancing Reward Model Evaluation |
| Act Only When It Pays: Efficient Reinforcement Learning for  | 2506.02177 | Act Only When It Pays: Efficient Reinforcement Learning for LLM Reasoning via Selective Ro |
| CodeContests+ / CodeContests+: High-Quality Test Case Genera | 2506.05817 | CodeContests+: High-Quality Test Case Generation for Competitive Programming |
| GLM-4.5V and GLM-4.1V-Thinking: Towards Versatile Multimodal | 2507.01006 | GLM-4.5V and GLM-4.1V-Thinking: Towards Versatile Multimodal Reasoning with Scalable Reinf |
| ArtifactsBench / ArtifactsBench: Bridging the Visual-Interac | 2507.04952 | ArtifactsBench: Bridging the Visual-Interactive Gap in LLM Code Generation Evaluation |
| Gemini 2.5 技术报告 / Gemini 2.5: Pushing the Frontier with Adva | 2507.06261 | Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and |
| SPICE / SPICE: An Automated SWE-Bench Labeling Pipeline for  | 2507.09108 | SPICE: An Automated SWE-Bench Labeling Pipeline for Issue Clarity, Test Coverage, and Effo |
| Rubrics as Rewards / Rubrics as Rewards: Reinforcement Learn | 2507.17746 | Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains |
| ScreenCoder 表 2 / ScreenCoder: Advancing Visual-to-Code Gene | 2507.22827 | ScreenCoder: Advancing Visual-to-Code Generation for Front-End Automation via Modular Mult |
| GLM-4.5 / GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foun | 2508.06471 | GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models |
| OpenCUA / OpenCUA 表 6 / OpenCUA: Open Foundations for Comput | 2508.09123 | OpenCUA: Open Foundations for Computer-Use Agents |
| UI-TARS-2 / UI-TARS-2 Technical Report: Advancing GUI Agent  | 2509.02544 | UI-TARS-2 Technical Report: Advancing GUI Agent with Multi-Turn Reinforcement Learning |
| V-GameGym / V-GameGym: Visual Game Generation for Code Large | 2509.20136 | V-GameGym: Visual Game Generation for Code Large Language Models |
| AgentTypo / AgentTypo: Adaptive Typographic Prompt Injection | 2510.04257 | AgentTypo: Adaptive Typographic Prompt Injection Attacks against Black-box Multimodal Agen |
| Reinforce-Ada §2 / Reinforce-Ada: An Adaptive Sampling Frame | 2510.04996 | Reinforce-Ada: An Adaptive Sampling Framework under Non-linear RL Objectives |
| Part II: ROLL Flash – Accelerating RLVR and Agentic Training | 2510.11345 | Part II: ROLL Flash -- Accelerating RLVR and Agentic Training with Asynchrony |
| ReLook / ReLook: Vision-Grounded RL with a Multimodal LLM Cr | 2510.11498 | ReLook: Vision-Grounded RL with a Multimodal LLM Critic for Agentic Web Coding |
| ScaleRL 附录表 1 / The Art of Scaling Reinforcement Learning Co | 2510.13786 | The Art of Scaling Reinforcement Learning Compute for LLMs |
| A11yn / A11yn 表 2 / A11yn 附录 E / A11yn: Aligning LLMs for We | 2510.13914 | A11yn: Aligning LLMs for Web Accessibility-Aware UI Generation |
| WebDevJudge 表 1 / WebDevJudge: Evaluating (M)LLMs as Critiqu | 2510.18560 | WebDevJudge: Evaluating (M)LLMs as Critiques for Web Development Quality |
| UI2Code^N §4.3 / UI2Code^N 表 12 / UI2Code^N 表 2 / UI2Code^N  | 2511.08195 | UI2Code^N: UI-to-Code Generation as Interactive Visual Optimization |
| Fantastic Bugs and Where to Find Them in AI Benchmarks / 实测 | 2511.16842 | Fantastic Bugs and Where to Find Them in AI Benchmarks |
| DesignPref / DesignPref: Capturing Personal Preferences in V | 2511.20513 | DesignPref: Capturing Personal Preferences in Visual Design Generation |
| Qwen3-VL / Qwen3-VL Technical Report / Qwen3-VL 报告 表 2 | 2511.21631 | Qwen3-VL Technical Report |
| MiMo-V2-Flash / MiMo-V2-Flash Technical Report | 2601.02780 | MiMo-V2-Flash Technical Report |
| FronTalk 表 4 / FronTalk: Benchmarking Front-End Development  | 2601.04203 | FronTalk: Benchmarking Front-End Development as Conversational Code Generation with Multi- |
| ARA / ARA §5.1 / Adversarial Reward Auditing for Active Dete | 2602.01750 | Adversarial Reward Auditing for Active Detection and Mitigation of Reward Hacking |
| Kimi K2.5 / Kimi K2.5: Visual Agentic Intelligence | 2602.02276 | Kimi K2.5: Visual Agentic Intelligence |
| SWE-Master / SWE-Master §6.3 图 12 / SWE-Master 主表与 §5 / SWE- | 2602.03411 | SWE-Master: Unleashing the Potential of Software Engineering Agents via Post-Training |
| GameDevBench / GameDevBench: Evaluating Agentic Capabilities | 2602.11103 | GameDevBench: Evaluating Agentic Capabilities Through Game Development |
| WebClipper / WebClipper 表 1 / WebClipper: Efficient Evolutio | 2602.12852 | WebClipper: Efficient Evolution of Web Agents with Graph-based Trajectory Pruning |
| Vision2Web / Vision2Web 表 3 / Vision2Web: A Hierarchical Ben | 2603.26648 | Vision2Web: A Hierarchical Benchmark for Visual Website Development with Agent Verificatio |
| Generative UI / Generative UI: LLMs are Effective UI Generat | 2604.09577 | Generative UI: LLMs are Effective UI Generators |
| GLM-5V-Turbo 报告 / GLM-5V-Turbo: Toward a Native Foundation M | 2604.26752 | GLM-5V-Turbo: Toward a Native Foundation Model for Multimodal Agents |
| 2605.12474 / Reward Hacking in Rubric-Based Reinforcement Le | 2605.12474 | Reward Hacking in Rubric-Based Reinforcement Learning |
| VISTA / VISTA §5.2 / VISTA: An End-to-End Benchmark for Visu | 2605.26144 | VISTA: An End-to-End Benchmark for Visual Spec-to-Web-App Coding Agents |
| MiniMax-M2 / The MiniMax-M2 Series: Mini Activations Unleash | 2605.26494 | The MiniMax-M2 Series: Mini Activations Unleashing Max Real-World Intelligence |
| GUI Agents for Continual Game Generation（PlaytestArena / Pla | 2605.28258 | GUI Agents for Continual Game Generation |
| WorldCoder-Bench / WorldCoder-Bench 判定范式对照 / WorldCoder-Benc | 2606.01869 | WorldCoder-Bench: Benchmarking Physically Grounded 3D World Synthesis |
| CHERRL / CHERRL 附录 A / Reproducing, Analyzing, and Detecting | 2606.04923 | Reproducing, Analyzing, and Detecting Reward Hacking in Rubric-Based Reinforcement Learnin |
| AutoLab / AutoLab 主表 / AutoLab 的 harness 消融 / AutoLab: Can F | 2606.05080 | AutoLab: Can Frontier Models Solve Long-Horizon Auto Research and Engineering Tasks? |
| JAMER / JAMER: Project-Level Code Framework Dataset and Benc | 2606.19830 | JAMER: Project-Level Code Framework Dataset and Benchmark on Professional Game Engines |
| The Verification Horizon / The Verification Horizon: No Silv | 2606.26300 | The Verification Horizon: No Silver Bullet for Coding Agent Rewards |
| Animation2Code / Animation2Code: Evaluating Temporal Visual  | 2606.28593 | Animation2Code: Evaluating Temporal Visual Reasoning in Video-to-Code Generation |
| MV-Bench / MV-Bench: Benchmarking Multimodal Large Language  | 2607.19910 | MV-Bench: Benchmarking Multimodal Large Language Models for Coordinated Multi-View Interfa |
| Kimi K3 / Kimi K3: Open Frontier Intelligence | 2607.24653 | Kimi K3: Open Frontier Intelligence |
| TCPO / TCPO: Turn-Level Credit Policy Optimization | 2608.01667 | TCPO: Turn-Level Credit Policy Optimization |
| Real-Time Detection and Repair of LLM Agent Failures / Real- | 2608.02464 | Real-Time Detection and Repair of LLM Agent Failures |
| FACTOR / How Much, Then Where: Credit-Conserving Action-to-T | 2608.07118 | How Much, Then Where: Credit-Conserving Action-to-Token Allocation for Multi-Turn Agent Re |
| CrEST / Teach the Magnitude, Not the Direction: Verifier-Bou | 2608.13179 | Teach the Magnitude, Not the Direction: Verifier-Bounded Credit Assignment for Multi-Turn  |
| RubSE / Rubrics as Visual-Repair Context for Self-Evolving U | 2608.24138 | Rubrics as Visual-Repair Context for Self-Evolving UI-to-Code Generation |
| Repair or Resample / Repair or Resample? Rethinking Failure  | 2608.25920 | Repair or Resample? Rethinking Failure Debugging in LLM Multi-Agent Systems |
| 3DHarnessBench / 3DHarnessBench 表 1 / 3DHarnessBench 表 3 / 3 | 2609.06535 | 3DHarnessBench: Probing Agentic 3D-to-Code Capabilities of Frontier Vision-Language Models |
| MTAC-IFBench / MTAC-IFBench 表 2 / MTAC-IFBench: Benchmarking | 2609.14992 | MTAC-IFBench: Benchmarking Instruction-Following in Multi-Turn Agentic Coding |
| Agreement Overstates Evidence: Error Dependence in LLM Judge | 2609.22512 | Agreement Overstates Evidence: Error Dependence in LLM Judge Consensus |
| RULER / RULER 表 4 / RULER: Instance-aware Rubric Rewards for | 2609.25270 | RULER: Instance-aware Rubric Rewards for SVG Generation |
| AUV-Bench / AUV-Bench 表 8 / AUV-Bench: Aesthetic Understandi | 2609.34854 | AUV-Bench: Aesthetic Understanding and Generation Evaluation for User Interfaces |
| A2Z / A2Z GameSpec-Bench 表 4(c) / A2Z GameSpec-Bench: How Fa | 2609.39564 | A2Z GameSpec-Bench: How Faithfully Can Coding Agents Generate Games from Game Design Speci |
| Unlearnable, or Unmeasured? On the Reliability of Difficulty | 2609.40115 | Unlearnable, or Unmeasured? On the Reliability of Difficulty Labels in RLVR |
| Code2Games / Code2Games: Enabling Coding Agents for Gaming W | 2610.05033 | Code2Games: Enabling Coding Agents for Gaming World Generation |
| PlaySuite / PlaySuite: A Large-Scale Benchmark for Interacti | 2610.07127 | PlaySuite: A Large-Scale Benchmark for Interactive Visual Intelligence |
| VETTA / VETTA: Coordinating Turn- and Token-Level Credit Ass | 2610.08402 | VETTA: Coordinating Turn- and Token-Level Credit Assignment for Multi-Turn LLM Agents |
| WorldBench / WorldBench 表 5 / WorldBench: Evaluating LLMs on | 2610.10622 | WorldBench: Evaluating LLMs on Three.js Voxel World Generation |
| ReTerm / ReTerm: Recovery Training for Self-Improving Termin | 2610.18484 | ReTerm: Recovery Training for Self-Improving Terminal Agents |

## overview：带数字但没有链接（44 处）

- L15: | 隐藏运行时状态契约 | Kendall τ_b 1.000 | 0 | 约 2 倍 |
- L16: | 八步 agent 自主探查 | +0.111 | 45.6% | 约 400 倍 |
- L17: | 只读 DOM | −0.021 | 33.7% | 1 倍（基线） |
- L18: | 截图加 VLM judge | −0.068 | 3.2% | 约 50 倍 |
- L20: 而同一批尝试的 SigLIP2 相似度均值，Astra 0.1081 对 Opus 5.5 0.1067，只差约 0.001（站点页面数据），站方自己把这个信号标为不参与判定的描述性指标。
- L26: 截图加 VLM judge 的假阳率并不高，只有 3.2%，问题出在它与真值的相关性是负的——它不是「乱放行」，而是排序方向错了，而且比读运行时状态贵 25 倍（约 50 倍对约 2 倍）。
- L26: 只读 DOM 更糟，三分之一的坏产物被它放过（33.7%）。
- L44: Design2Code 反过来，头部模型挤在 93 以上的天花板，差距同样被压扁（而且这一行的判据本身是模型打分，只能当量程的对照）；
- L44: 只有 3JSBench 的最高分到了 80%，有足够的量程，差距才张得开。
- L65: - 人工两两比较，5 名评测员共 1,330 次判定，非平局里 64.7% 偏向它（表 7）。
- L69: 复刻 Astra 与 Opus 5.5 的第一件事，是先把量尺造出来。
- L89: GPT-5.5 在 OpenHands、Factory、Codex 三个脚手架上分别是 69.85%、67.39%、58.19%，极差 11.7 点。
- L95: 单个 VLM 重判会翻面，最差的一档两次一致只有 38/48，翻面率 20.8%。
- L95: 本项目的一次翻案正是这样发生的（同一记录 §3.4）：用车床几何转出的雪人头顶没有封口，四个 VLM 都看出来了，而当时的程序化信号全部失明，修法不是调阈值，是补一个不随缺陷尺寸衰减的拓扑量。
- L110: | 3DHarnessBench，Claude Opus 5 | 0.725 | 0.871 | 加 20.1% | 同上 |
- L135: 两组都是 2024 到 2025 年的模型，只能说明测法敏感，不能代表当前代际。
- L163: | 4 | 3D 空间推理 | 几个 3D 与 CAD 评测集上，权重公开的模型基本没有报分 | 不是能力差距已证实，是测不出来，先建测法比先提能力重要 |
- L165: | 6 | 可访问性与性能预算 | 性能预算零公开 benchmark | 不是差距，是空白，自建成本最低 |
- L223: 采样噪声给出 SE(S) ≤ 0.5 / sqrt(M·n)。
- L226: 程序化信号                      MDE = 1.98 / sqrt(M·n)
- L227: VLM judge 三票多数              MDE = 2.38 / sqrt(M·n)
- L236: | 15 乘 8 | 120 | 18.1 | 21.7 |
- L237: | 30 乘 8 | 240 | 12.8 | 15.4 |
- L238: | 40 乘 16 | 640 | 7.8 | 9.4 |
- L239: | 100 乘 8 | 800 | 7.0 | 8.4 |
- L240: | 150 乘 16 | 2,400 | 4.0 | 4.9 |
- L241: | 300 乘 16 | 4,800 | 2.9 | 3.4 |
- L245: 1. 很多内部实验报出的「这个改动涨了 5 个点」是在 18 点分辨率下读出来的，它是噪声（15 乘 8 一行）。
- L246: 2. 要在单维度上读出 5 个百分点，需要 M 乘 n 约 1,600（程序化信号）或 2,260（VLM judge），即 40 题乘 40 次或 100 题乘 16 次（1.98/√1600 ≈ 4.95，2.38/
- L247: 3. 在单条 case 上比两个方案的优劣，每臂至少 63 次；
- L247: n 等于 5 时单题只有 6 个可能取值，MDE 是 0.89，等于什么也没测（单题 MDE = 1.98/√n，要到 0.25 需 n ≥ 63；
- L249: 硬闸档只给 4 次采样是因为那几维的 Verifier 是确定性的，作用是过与不过，不需要 3 个点的分辨率。
- L251: 新加的审美判据抓到 9 个，8 个合法改版零误杀，成本只有功能侧的六分之一。
- L258: 但把标注者从 3 个加到 16 个，人力乘以 5.3，检测同样的分差所需题量只从 185 降到 130，省三成。
- L264: | 一、先能测 | 约 3 个月 | 自建 harness 复现公开分，内部 430 题集上线，Verifier 准入全过 | 与公开数字差 ≤ 2 点；全集实测 MDE ≤ 3.5 点；变异杀死率 ≥ 95%、正确解通
- L279: 1. **先把 Web 这条线接进 RL 环境。
- L280: 2. **补留出验证，而不是补新信号。
- L281: 3. **把三个真空白做成首发**：多视口一致性当确定性判据、性能预算当判据、动画的时间正确性当通用子分。
- L282: 4. **拿到差距向量再决定投入。
- L284: 两者都做也只比单做选择多 0.6 分（70.8）。
- L308: 成本模型原先按 60% 外推，换成实测，造 10 万个任务要从 26.9 万候选变成 84.8 万，**成本乘 3.2**。
- L310: 这里还有一个口径陷阱值得单独记住：同一批题用**跨模型汇总**的通过率算，可用率是 70%；
- L316: 两条经验：抽查的命中率不是 100%，所以必须做；
- L318: 几个公开榜单已经停更，上面标的 2026 年数字多数是厂商自报。

## tasks：带数字但没有链接（77 处）

- L25: 这个 3,413 是**上界，不是可用任务数**，原因有两条。
- L25: 结论是先做这一层：环境脚本现成、Verifier 确定、许可干净，three.js 加 Babylon.js 合计约 1,500 个 commit，Blender 另有 839 个场景。
- L46: 数据解读：带截图的 issue 数量看着有 30 万，但端到端转化率是千分之几。
- L46: 按同样的转化率，30 万候选只能出约 1,400 个任务，是千量级不是万量级。
- L48: 同架构同规模对照下，合成数据训练后在真实测试集上的 TreeBLEU 是 0.06，真实数据是 0.35（WebCode2M 表 3）。
- L71: 严重缺陷的误放率，DOM 33.7%、8 步 agent 式检查 45.6%、状态契约为 0（表 2）。
- L78: 2. **生成断言与 rubric**。
- L78: 从参考解的运行状态抽断言，把它的渲染结果交给 rubric 生成器，产出「桌面上有 4 把椅子、间距大致相等」这类可观察条目，而不是「和参考截图一样」。
- L79: 3. **当可破坏的底子**。
- L80: 4. **校验 Verifier**。
- L81: 5. **SFT 冷启动**。
- L99: | 桌子加杯子 | 10 | 9 | 1 | 杯子倒置：杯子是圆台，翻转后占据几乎不变 |
- L100: | 桌面工作台（13 个 mesh，带层级和旋转） | 16 | 14 → 16 | 2 → 0 | 立杆缺失、灯臂镜像；补上连通块统计后都能抓到 |
- L112: 预实验里 opus-5.5 在 9 个桌子任务上一轮过 7 个。
- L116: | 杯子颜色 | 杯子应使用有别于桌面木色的独立颜色 | 必须恰好是参考里那一种蓝 | 模型换了另一种颜色，该色体素 IoU 为 0，判挂 |
- L117: | 桌腿位置 | 桌腿应位于桌面四个角落附近 | 腿的位置要和参考几乎重合 | 模型把腿放到角上但缩进量不同，剪影 0.885 差一点点，判挂 |
- L133: 合计 3/16，按两成算，十万任务里就有两万道持续向 RL 注入噪声。
- L139: 1. 让一个与 Verifier 无关的模型只看 Problem Statement，枚举「你觉得验收会查哪些点」，输出一张清单。
- L140: 2. 和真实断言集做匹配，算召回：被猜到的断言数除以断言总数。
- L141: 3. 召回低于某个线的任务退回，未被猜到的那几条断言要么删掉，要么把对应信息补进题面。
- L142: 4. 先在已有任务上校准——三道已知不可解的题是现成的金标准，这条闸抓不出它们就说明实现有问题。
- L154: | 关掉哪一层 | 桌面工作台（16 个提议） | 桌子加杯子（10 个提议） |
- L156: | 不关，全部信号 | 收 16 | 收 9 |
- L157: | 多视角剪影 | 收 16 | 收 9 |
- L158: | 体素占据 | 收 14 | 收 8 |
- L159: | 自洽性 | 收 16 | 收 9 |
- L160: | 部件与拓扑 | 收 14 | 收 9 |
- L186: policy 变强后，原本通过率在 0 与 1 之间的题会变成全对；
- L203: 4.4 万倍的折损同时给出一个工程结论：单模板做不到十万，十万量级必须靠模板数与跨模板组合，而跨模板组合的价值在于它造出的空间关系不在任何单模板的槽位域里。
- L205: 程序化 3D 场景离自然图像分布很远，预训练视觉特征会把一切压成一团。
- L213: | 0 到 0.1 | 2 |
- L214: | 0.1 到 0.3 | 2 |
- L215: | 0.3 到 0.7 | **0** |
- L216: | 0.7 到 0.9 | 2 |
- L217: | 0.9 到 1.0 | 4 |
- L221: 数据解读：十道题的通过率依次是 0、0.04、0.26、0.27、0.73、0.77、0.91、0.93、1.0、1.0。
- L221: 但如果按常见的 0.3 到 0.7 收紧，**一道题都留不下**。
- L233: | 2/8 到 6/8 | 1 |
- L239: **即便取上界 43%，也仍低于成本模型假设的 60%**——这个假设站不住不是因为样本少，是方向就错了。
- L239: 两种口径差约 3.7 倍（70% 对 19%），所以估 RL 的零梯度比例只能用**将要训的那个策略自己**的 pass@k，不能用跨模型汇总。
- L243: 真正的 pass@k 要逐模型算，而每个模型每题只有 7 到 8 次，不够。
- L247: | 真实通过率 | n=4 | n=8 | n=16 | n=32 | n=64 |
- L249: | 0.10 | 5.2% | 3.8% | 1.7% | 0.1% | 0.0% |
- L250: | 0.25 | 26.2% | 32.1% | 37.0% | 26.3% | 15.6% |
- L251: | 0.35 | 68.9% | 45.3% | 29.1% | 26.8% | 22.5% |
- L252: | 0.50 | 62.5% | 28.9% | 7.7% | 2.0% | 0.2% |
- L253: | 0.75 | 26.2% | 32.1% | 37.0% | 26.3% | 15.6% |
- L254: | 0.90 | 5.2% | 3.8% | 1.7% | 0.1% | 0.0% |
- L256: 桶中心和桶外都能分准，桶边界附近分不准：真实通过率 0.35 时，n=8 的误分率 45.3%，n=64 仍有 22.5%，而且几乎不随采样次数下降。
- L256: 原因很直接——真值恰在边界上时本来就是 50 比 50，这部分方差不可能靠加采样消除。
- L256: 所以难度标定只做粗闸，两段式先 n=2 筛掉全对全错、存活者补到 n=8，之后用软权重而不是硬桶。
- L258: 而只切一边的五个设置（23.8 到 25.9）全部低于不过滤的 26.3；
- L258: 训练前一次性离线筛题（用外部模型或初始模型当难度代理）只到 26.3 到 28.4，低于在线双边过滤的 30.1。
- L278: SWE-rebench 自己点名安装与执行验证这一步只有约 14% 通过，只有 31% 的仓库能装成至少一个任务。
- L278: 按每仓库平均挖出 3 个可用页面估，只能出约 230 个任务——三位数，不是五位数。
- L280: 真实素材客观上只能占千分之几的条数，合成必然在 95% 以上。
- L280: 所以真实素材的 KPI 应该改成「在有效多样性口径下贡献至少 20%」，而不是条数占比；
- L282: 准入三条取 0.97 / 0.90 / 0.95，去重 0.85，可解性闸 0.88——这五步合计留存 62%。
- L284: | 项 | 按 0.60 外推 | 按实测 0.19 |
- L286: | 漏斗总留存 | 37.2% | 11.8% |
- L287: | 造 10 万任务需要的候选 | 26.9 万 | **84.8 万** |
- L288: | 探针调用 | 约 160 万次 | 约 500 万次 |
- L290: 下面的资源表仍按原先的 26.9 万口径列，**要按实测口径读就把 CPU、存储、LLM 调用三行各乘 3.2**；
- L295: | 折算整机 | 31 台机小时 | 22 台机小时 | 48 核机器 |
- L296: | 存储 | 约 20 GB | 约 100 GB | 单任务 0.2 MB 对 1 MB |
- L297: | LLM 调用 | 约 95 万次 | 约 95 万次 | 优化后；优化前 121 万次里难度标定占 65% |
- L298: | 人工 | 约 360 人时 | 约 360 人时 | 抽检 240、一致性标定 50、欠规格仲裁 67 |
- L302: 数据解读：两条线合计约 2,500 核时，一台 48 核机器两天跑完，算力不构成瓶颈。
- L302: LLM 调用里 65% 花在难度标定上，所以唯一值得反复优化的旋钮就是「难度要采样多少次」：一次性 n=8 要 133 万次标定调用，两段式先 n=2 筛掉 55% 再补 6 次只要 78 万次，LLM 总调用从 176
- L304: 成本模型里最敏感的一项就是这个难度带留存，而本项目实测 0.19 与公开实测方向一致，都说明 0.60 偏乐观。
- L304: 如果实际留存是 0.30，候选数从 26.9 万翻到 53.8 万，LLM 调用从 95 万翻到 190 万。
- L304: 把样本扩到现有全部 47 个任务只需 376 次调用、几十分钟，是收窄区间最便宜的办法。
- L308: 逐快照独立去重保留 20T，才与 RefinedWeb 持平并逐步受益。
- L310: S1 模板化，8 个槽位模板、2,000 个任务，核心交付物不是任务而是 8 张过了可见性审计的槽位表；
- L310: S2 多样性扩张，40 个模板、2 万个任务，第一次上两段式难度标定与三路去重；
- L310: S3 真实素材注入，到 5 万，许可与污染都在这一阶段出问题；
- L310: S4 满产，10 万以上，加分布漂移监控与训练侧回归。

## verifier：带数字但没有链接（114 处）

- L9: - 截图加 VLM 与真值的 Kendall τ_b 是 −0.068，即负相关，成本是 DOM 基线的约 50 倍。
- L10: - 读取隐藏的运行时状态契约，τ_b 是 1.000、假阳率 0，成本约 2 倍。
- L10: 注意它本身就是该基准的真值，τ=1 是定义使然；
- L11: - 一个贵 25 倍而且方向都不对的信号，不该进 reward。
- L13: 三个 three.js 场景、47 个带人工标签的变异，只看页面自带相机的一张截图做逐像素相似度，在前两个场景的 29 个变异上判对 12 个。
- L13: 它不是不够准，它是在量纲上失明：雪人的胡萝卜鼻子只占几十个像素，把它挪到后脑勺，页面截图相似度仍然是 0.999。
- L21: 不该挂的是网格精细度、光照强弱、背景色、相机机位、轻微色差、尺寸正负 5%。
- L25: | 程序化信号 | 雪人 13 例 | 桌子 16 例 | 合计 |
- L27: | 页面单张截图逐像素相似度 | 5 | 7 | 12/29 |
- L28: | 几何类名多重集一致 | 6 | 8 | 14/29 |
- L29: | 多视角剪影 IoU | 9 | 10 | 19/29 |
- L30: | 按色体素 IoU | 11 | 14 | 25/29 |
- L31: | 分层组合 | 13 | 16 | 29/29 |
- L35: 数据解读：按 API 名字断言「场景里有几个球、几个圆柱」只能到 14/29，因为它查的是实现路径而不是结果，换一种建模手法做出同一个形状就会误杀。
- L35: 多视角剪影补上了单视角看不见的方位错误，按色体素补上了形状对而颜色错的情况，两者叠起来仍漏 4 个，缺的是部件级拓扑。
- L37: 新场景是一辆小车，9 个 mesh；
- L37: 18 个变异和它们的标签先写死再跑，阈值沿用前两个场景，一个没动，只跑一次。
- L47: | 前灯少一个 | 部件连通块数 | 剪影 0.998、分块 0.924、该色体素 0.5 全在阈值之上 |
- L48: | 风挡挪到车尾 | 按色体素 | 剪影 0.992，外轮廓几乎没变，但玻璃色体素 IoU 为 0 |
- L49: | 风挡改成车身色 | 按色体素 | 剪影和分块都是 1.0，形状完全没动 |
- L50: | 少一个轮子 | 分块体素 | 全局剪影 0.903 刚好过线，分块最差块是 0.0 |
- L51: | 轮子轴向转 90 度 | 多视角剪影 | 外轮廓直接变了 |
- L55: 最接近误杀的一例是「轮子半径加 4%」，分块最差块 0.727，阈值 0.5，还留着余量。
- L61: Blender 侧的场景是一张木桌加台灯加陶瓷杯，22 个变异，11 个该挂、11 个不该挂；
- L61: 其中 15 个是开发集，7 个是选完判据之后才造的留出集。
- L65: | 信号 | 总判对 | 检出 11 个该挂 | 保真 11 个不该挂 |
- L67: | 只看一张截图 | 12/22 | 2 | 10 |
- L68: | 多视角剪影 IoU | 14/22 | 3 | 11 |
- L69: | 全局 Chamfer | 13/22 | 2 | 11 |
- L70: | 全局 F-score | 11/22 | 0 | 11 |
- L71: | 分部件 F-score | 18/22 | 7 | 11 |
- L72: | 全量状态断言 | 11/22 | 11 | 0 |
- L73: | 分部件几何加四族断言 | 21/22 | 11 | 10 |
- L77: 数据解读：全量状态断言把 11 个真错全抓住了，代价是 11 个语义未变的改写全被误杀，净判别力等于零。
- L77: 误杀集中在两类写法差异：把边长 1 的立方体放大 1.2 倍，改写成边长 2 的立方体缩小 0.6 倍，世界几何逐点相同而物体自身的缩放值差一倍；
- L77: 圆柱从 16 段改 32 段，顶点数全变而形状不变。
- L79: 全局 F-score 更极端，11 个该挂的一个都没检出。
- L87: 把参考与候选的渲染图上下拼成一张交给模型判 pass 还是 fail，48 个 case、4 个 judge、每种看图条件每例两次、温度 0，共 768 次判定，单模型判对 74 到 92 次（分母 84 到 96，少掉
- L87: 而逐像素相似度在其中 29 个变异上只有 12/29。
- L89: 最早只跑了 18 个 case，看到多视角拼图的判对率不升反降，于是写下「多视角对 VLM 无效」。
- L89: 把样本扩到 48 例、并修正一处人工标注错误之后，结论反过来了。
- L95: | gpt-6-astra | 84/95 | 92/96 | 16.7% | 4.2% |
- L96: | gemini-3.8-flash | 88/96 | 92/96 | 8.3% | 0.0% |
- L97: | doubao-seed-2.1-pro | 78/91 | 81/84 | 6.2% | 8.3% |
- L98: | claude-opus-5-5 | 76/96 | 74/93 | 16.7% | 20.8% |
- L99: | 4 模型 8 票多数投票 | 44/48 | 46/48 | — | — |
- L103: 数据解读：逐 case 配对比较，单视角赢 11 例、多视角赢 27 例；
- L105: 同一个模型、同一张图、温度 0 跑两次，最差一档有 20.8% 的 case 会翻面。
- L105: 而多视角把两个最强 judge 的翻面率从 16.7% 压到 4.2% 和从 8.3% 压到 0。
- L107: 4 个模型 8 票多数投票在 48 例上单视角 44 对、多视角 46 对。
- L107: 拿它和程序化信号的 47/47 直接比是不成立的——两个集合不同、组成不同，而且其中一个是程序化信号自己调过阈值的集合；
- L107: 能比的只有定性的那一面：投票漏掉的那几例全是同一类——**定量的几何偏差**：一条桌腿缩短到 70%，8 票全判通过；
- L107: 桌面厚度减到原来的三分之一，5 票判通过。
- L107: 这两例程序化信号都抓到了，前者靠分块体素 0.167，后者靠按色体素 0.528。
- L115: | 有参考图，单视角 | 94% | 58/63 | 43/44 |
- L116: | 有参考图，四视角 | 97% | 61/64 | 44/44 |
- L117: | 无参考图，单视角 | 68% | 35/56 | 30/40 |
- L118: | 无参考图，四视角 | 76% | 34/56 | 39/40 |
- L122: 数据解读：检出从九成二掉到六成上下，而四视角下的保真仍有 39/40——没有参考的 judge 变成了一个偏宽松的放行器，不怎么冤枉好人，但一多半的缺陷放了过去。
- L122: 单视角下连保真也只剩 30/40，说明没有参照时它两头都在猜。
- L124: 生成方在没有可比对象时，首轮挂掉后只能救回 2/37；
- L126: 多视角条件下 8 票里有 7 票说它有问题，而单视角条件下投票判它通过。
- L128: 换成单面剪影，IoU 也只从 0.997 掉到 0.958，因为洞只占几十个像素，被全局 IoU 淹没；
- L128: 体素 IoU 是 0.995，同理。
- L128: 修法不是把阈值从 0.96 调到 0.97——那样会立刻误杀一批合法改写。
- L130: 这个信号是**在它要验证的那个 case 上造出来的**，而那个 case 就在雪人那 13 例里面。
- L130: 所以「加上这个信号之后两个变异集仍然是 13/13 和 16/16」不是独立验证，是在调参集上报调参集的成绩，违反了本文自己在讲任务构造时定下的红线——不许用正在调阈值的集合做验收。
- L132: ** 它也不是人工标签的替代品：标注者和自动指标会在同一个地方同时瞎掉，这次就是 4 个 VLM 对、一个人错。
- L144: 修完之后 7 个作弊页面全挡。
- L146: 把判据的构成原原本本告诉它，要求写一个「能过验收但实际不满足需求」的页面，三个场景乘四个模型共 12 次请求，其中两个模型全程没有产出，实际拿到 5 份可判定的作弊页，**verifier 判过 0 份**，全部挂在多视
- L146: 它们试的路子是：用贴图画出看起来对的东西（3 份）、往约定好的全局变量里塞一个正确场景（1 份）、直接操作画布读写（3 份）、玩绘制顺序（1 份）；
- L148: 分母只有 5，而且模型只试了一次、没有梯度、也看不到判定反馈；
- L150: 7 个作弊页面全挡，说明的是这 7 条路径被堵住了，不是「不可 hack」——其中一条在修补之前真的骗过了 Verifier，同类漏洞一定还会有。
- L170: 只冻结时钟不够：对一个用动画帧回调加随机数的页面，仅安装虚拟时钟时三次截图三个结果，加上暂停与定点推进之后 20 次里仍有 2 种。
- L194: 部件计数 223 条、结构 160 条、空间关系 157 条，三族合计占 78%，全部是「有几个、接在哪、挨着谁」。
- L196: 3000 次尝试里最常见的五类失败是物体互相穿插 20%、可见背面 19%、表面闪烁 17%、朝向与题面不符 16%、部件断开 16%。
- L198: 把桌面正上方零距离再铺一块同样大的面，整体穿插比例从参考的 0.053 涨到 0.762，改变绘制顺序后有 5534 个像素发生变化，两个信号都把它判挂。
- L198: 三个变异集回归后仍是 13/13、16/16、18/18，没有新增误杀。
- L200: 按部件两两算穿插比例，在 48 的体素分辨率下不可用：薄部件会被量化成单层，看起来像被另一个部件完全包含，参考解自己的最大值就是 1.0。
- L202: 通过率差 53 个百分点，嵌入相似度只差 0.004。
- L214: | 硬门槛 | 能执行、无运行时报错、渲染发生过、可见画布非空 | 1 到 5 秒，纯 CPU | 几乎为 0 | 低 |
- L216: | 感知与几何相似 | 多视角剪影、按色体素 IoU、分部件 Chamfer 与 F-score | 10 到 60 秒 | 中 | 高：视口尺寸、贴图文字、特征饱和 |
- L220: 本机实测的单次探测是 0.8 到 1.0 秒（见第 6 节）。
- L224: 感知相似只能作分项，因为它的失效模式是被尺寸稀释（杯子挪 30 厘米、头顶一个洞都在这一层逃掉）。
- L230: 47/47 里只有 18 个是真正留出的，其余 29 个的阈值在同一批变异上看过一眼。
- L232: - VLM judge 的数字来自 48 个 case、4 个模型、两种看图条件各 2 次，合计 768 次判定。
- L232: 它支撑「单次判定不可用」和「多视角不差于单视角」，但支撑不了「8 票投票就够了」这种配置级结论——逐模型的配对检验没有一个到显著，合计那一次又高估了独立性。
- L247: 1. Verifier 对某一类几何有系统性盲区，例如开口曲面的体素填充无效。
- L248: 2. 这一类的**参考解自己**就过不了准入。
- L249: 3. 整类任务被静默丢弃，一条都不进数据集。
- L250: 4. 数据集的各项指标反而更漂亮，因为留下来的全是 Verifier 看得准的那些。
- L251: 5. 缺失不以噪声的形式出现，而以**某个几何类别从分布里消失**的形式出现。
- L284: | 纯文本需求 | 0/13 | 0/13 |
- L285: | 文本加参考图 | 0/13 | 0/13 |
- L295: 部件计数 223 条、结构 160 条、空间关系 157 条，三族占 78%，查的全是有几个、接在哪、挨着谁。
- L301: | 本文现有判据 | 适用，三场景 47/47 | 不适用，0/26 |
- L316: | 从零搭建的每一次尝试（80 次） | 0/80 | 13/80 |
- L317: | 三个场景的带标签变异（47 例） | 47/47 | 35/47 |
- L321: 但代价是实打实的：变异集从 47/47 掉到 35/47，漏掉的十二个有共同点，相对结构没变，腿还连在桌面上、杯子还接触桌面、比例还在容差内。
- L321: 部件最多的那个场景仍然是 0，因为部件一多，匹配本身就不稳。
- L331: 然后造 20 个变异——12 个只破坏审美不破坏功能（页面照跑、不报错、不溢出、不遮挡），其中 1 个事后判为无效变异；
- L331: 8 个是合法改版（换品牌色、换一套自洽的等比尺度、深色主题、加留白、类名重命名、压缩 HTML）。
- L337: | 参考页 | 11 条全过 | 全过 |
- L338: | 纯审美缺陷（11 个有效变异） | 抓到 9 | 抓到 2，且都是顺带 |
- L339: | 合法改版（8 个） | 误杀 0 | 误杀 0 |
- L340: | 单个变异耗时 | 约 0.8 秒，两个视口 | 约 4.9 秒 |
- L344: 数据解读：标题层级反了、字号变成一堆相近的随机值、四种字体混用、行高压到 1.02、间距全换成奇数、抹掉所有内外边距——这六类功能侧一个都看不见，而它们正是「这页看着不像人做的」的主要来源。
- L349: - **栅格对齐**：该挂的那个变异对齐率是 0.707，而一个**不该挂、而且审美更好**的改版是 0.765，可分离区间只剩 0.058。
- L349: 更要命的是它在极端处会翻向——把所有内外边距抹掉之后，对齐率反而是 1.000。
- L351: 还有一条预设要去掉：不要假定页面按 4 像素栅格排布。
- L361: 拿本站两批页面算字体维度的集中度：一批 100% 用了那个被点名的字体，集中度 0.50；
- L361: 另一批一次都没用，集中度却是 1.00，也就是更坍塌。
- L365: 20 位设计师各评同样 600 对设计，二元一致率只有 0.624，Krippendorff α 是 0.248，28.5% 的对子两两分歧率达到 96% 及以上；
- L365: 用 20 倍数据训练出来的偏好模型也只有 57.45%，做了个性化才到 60.16%。

## training：带数字但没有链接（96 处）

- L5: 换成 on-policy 蒸馏，1,800 GPU 小时得 74.4。
- L20: 反过来，3D 开放设计这一族两道闸都亮红灯。
- L24: 均值同样 10 秒而标准差 1 秒，只有 1.16 倍；
- L24: 均值 50 秒标准差 5 秒，也只有 1.20 倍。
- L24: 真实任务同向（图 11），软件工程类 10.22 小时降到 8.32 小时，ALFWorld 13.37 小时降到 8.44 小时。
- L26: 判据写成一个数（本文给的经验判据，不是文献值）：先量 verify 延迟的标准差与均值之比，小于 0.3 就别上异步，直接同步加多并发摊平。
- L32: 组大小 8、题目通过率 0.1 时，一组全 0 的概率是 0.9 的 8 次方，即 43.1%；
- L32: 通过率落在 5% 到 10% 这一段时，组大小 8 有四成到七成的组拿不到任何梯度。
- L32: 把组大小加到 16 才把 0.1 那一档压到 18.5%。
- L32: ）同一篇给了实测：Qwen2.5-Math-1.5B 在 Open-R1 子集上 pass@1 只有 26.5% 而 pass@256 高达 81.3%——原文的结论是信号塌缩是欠采样的统计假象，不是模型上限。
- L38: | 朴素 GRPO | 30 | — |
- L39: | 加超长过滤 | 36 | +6 |
- L40: | 加 clip-higher | 38 | +2 |
- L41: | 加超长软惩罚 | 41 | +3 |
- L42: | 加 token 级 loss | 42 | +1 |
- L43: | 加动态采样 | 50 | +8 |
- L45: 数据解读：动态采样加 8、超长过滤加 6，两项合计 14 分；
- L47: 固定总 batch 时，组大小 8、16、24、32 的渐近性能是 0.585、0.610、0.590、0.595，基本分不开；
- L49: 再加事后重标与反事实参照到 65.2，又值 6.2。
- L73: 细节断言、几何相似、rubric 分只在两道闸都过之后进加权，而且几何相似的权重压在 0.3 以内。
- L75: 模型自己的错（代码报错、渲染空白、断言不过）给 0 或负分并正常进梯度，这是要学的信号。
- L77: 另一侧的边界同样硬：格式错与不可执行不能和「执行了但很差」混成同一个 0，否则两者失去区分度。
- L83: 用 Agent-R 的纠错轨迹迭代三轮后是 46.75（表 3）。
- L96: 更反直觉的是，55 条带数值发现的提示里有 26 条直接带了正确答案，这一档恢复率 36%，反而不如只说「哪条校验失败」的 45%。
- L106: 视觉通道的总增益 2.5 分（25.7 到 28.2），其中只给评估器看图拿回 2.1 分（84%），再给生成器看图只多 0.4 分（16%）。
- L106: 两条附带曲线同样重要：生成器与评估器都看不见图时，四轮迭代的分数是 27.4、26.1、26.5、25.7，一路走低，没有一轮回到起点；
- L106: 只要评估器能看见图，曲线就不再下跌（27.6、27.6、27.6、27.8），哪怕改法是闭着眼猜的。
- L108: 283 组有效运行，四种反馈乘两种问题描述，每轮都用同一个 Verifier 判定，模型看不到判定理由。
- L114: | 纯文本需求 | 1/14 | 0/12 | 1/11 |
- L115: | 文本加参考渲染图 | 4/12 | 6/10 | 1/9 |
- L117: 数据解读：纯文本描述下三种反馈合计救回 2/37，约 5%；
- L117: 给了参考图之后是 11/31，约 35%。
- L117: 四视角拼图那一格从 0/12 变成 6/10。
- L117: 每格分母只有 9 到 14，单格之间的比较要打折扣，合计那一行才站得住。
- L125: | 纯文本 | 四视角拼图 | 1/10 |
- L126: | 纯文本 | 拼图加层名 | 5/22 |
- L127: | 文本加参考图 | 四视角拼图 | 3/11 |
- L128: | 文本加参考图 | 拼图加层名 | 9/23 |
- L140: | GPT-4V | 85.8 | 87.6 | 88.8 |
- L141: | GPT-4o | 93.0 | 92.4 | 92.7 |
- L142: | DeepSeek-VL-7B | 39.7 | 66.1 | 30.1 |
- L143: | Idefics2-8B | 46.7 | 23.6 | 12.3 |
- L145: 数据解读：Design2Code 的 484 个真实网页上，自我修订是在文本增强那一版的产物上改的。
- L147: 一次 refinement 只在 reward 严格超过本轨迹内历史最佳时才接受，不达标就重采（每轮最多 10 次），10 次都不行就终止反思并采用历史最佳。
- L147: 效果是单调改进的轨迹，ArtifactsBench-Lite 三个随机种子平均 25.84 涨到 27.88（表 2），而且反思频率自然收敛到约 2 轮（图 5）。
- L153: 在最便宜的那一档配置下，图像只占一条 40 步轨迹累计输入的 8%，文本历史才是大头；
- L153: **换成「文字还看得清」的配置，图像占比升到 16% 到 36%。
- L161: | 1440 宽、900 高的一屏 | 约 1,550 | 高 |
- L162: | 1440 宽、8000 高的整页长图 | 约 616 | 约 20%，被压到 282 像素宽 |
- L163: | 同一张长图切成 9 片 | 约 13,950 | 约 96% |
- L165: 要文字可读就得切片，代价是 token 涨 22 倍。
- L169: 顺带纠正一个容易用错的口径：「多视角拼图比分开发图省 8 倍」不是同口径比较——那两个数字的像素量本身就差 12 倍。
- L175: GPT-4 作检测器 0.78 对 0.34，差 0.44；
- L175: 专训的 Auditor 0.82 对 0.19，差 0.63。
- L190: | 单项 rubric 饱和 | 任一分项通过率不低于 0.95 且 100 步内增幅不低于 0.15，而 gold 总分增幅不超过 0.02 | 建议值，上线前校基线 |
- L192: | verifier 通过率与人工抽检 | 自动通过率落在人工抽检的 Wilson 95% 区间之外 | 建议值 |
- L195: 所有阈值都按 100 步滚动窗口算，并先对指标做 5 步中心平滑（CHERRL 附录 A.1 的做法）。
- L195: 而 onset 之后 100 步内捷径行为的发生率至少再涨 40%——从告警到灾难只有约 100 步，告警必须自动化。
- L197: 规划的 400 步落在 onset 分布的中段，必须全程监控：六个设定里有四个的 onset 在 400 步以内（68、91、116、301 步）；
- L207: 阶段 0 不产出模型，但跳过它后面全部白做。
- L207: 出闸条件：同一产物取证两次关键断言 100% 一致；
- L207: 在 50 条已标注轨迹上量出噪声地板并写进配置；
- L213: | S1 冷启动 SFT | 8K 到 15K 条轨迹，three.js、Blender、前端各约三分之一，平均 10 到 20 步 | 纯 SFT；错误轮留上下文不算 loss，负例 token 权重 0.8 | 格式
- L214: | S2 拒绝采样 | 3K 到 5K 个任务各采 8 到 16 次，保留率预期 10% 到 35%，出 5K 到 20K 条 | 按分层 Verifier 筛，每题留 2 到 3 条择短 | 每题 pass@N 分布、
- L215: | S3 RL | 3K 到 8K 个任务，取 S2 里 pass@N 落在 0 与 0.9 之间的那些；batch 64、组大小 8 到 16、300 到 500 步 | 单轮用 DAPO 四件套；10 到 40 步多
- L216: | S4 迭代 | 用 S3 的 ckpt 重做 S2，再训一轮 | 迭代自蒸馏：RL 模型的输出替换冷启动数据重做 SFT | 每轮重算 pass@N 与 Verifier 校准 | 新一轮的 held-out 人工分
- L220: 但 S1 那一行的量级要重新想。
- L220: S1 规划的 8K 到 15K 只走到饱和点的两成到三成，也就是说**曲线最陡的那一段被跳过了**，然后用 RL 去追本来加数据就能拿到的分——而同一篇的 RL 增益只有 3.6 个点（32B）到 5.8 个点（4B），
- L228: | 零 SFT 数据（扩数据曲线的起点） | 6.2 | — |
- L229: | SFT 到约 60K 条轨迹 | 57.8 | 基线 |
- L230: | 再加 RL | 61.4 | 加 3.6 |
- L231: | 不加 RL，改成采 8 次再用验证器选 | 70.2 | 加 12.4 |
- L232: | 既加 RL 又做推理时选择 | 70.8 | 加 13.0 |
- L234: 数据解读：最后两行只差 0.6 分，也就是说在这个设定下，RL 的那点增益几乎被推理时选择吃掉了。
- L238: 所以正确的做法不是直接把 S1 加到 48K，而是先用一次多臂实验把这三件事的边际增益量出来：15K 加 RL、48K 不加 RL、48K 加推理时选择、48K 加 RL 加推理时选择。
- L238: 在它出结果之前，S3 的预算都是拍的。
- L240: 零 SFT 直接上 RL 在本场景不可行（本文判断）——要学的是工具调用协议加多轮自检行为，基座完全没有这个格式，绝大多数 rollout 会卡在格式错得 0 分，组内无方差。
- L242: 任一代理指标的分布出现双峰，或 95 分位数相对 S2 基线涨 3 倍以上，停下抽 20 条人工看。
- L242: 环境故障率超过 5%，暂停修基础设施，不要在高故障率下继续训，因为组基线遭污染之后差答案也能拿到正优势。
- L248: | 多轮 three.js | 43 核 | 0.9 台 |
- L249: | 多轮 Blender（自检走 Workbench，终局走 Cycles） | 365 核 | 7.6 台 |
- L250: | 单轮 three.js | 129 核 | 2.7 台 |
- L251: | 单轮 Blender | 1,670 核 | 34.9 台 |
- L253: 假设有五条：每条轨迹 40 个模型步、其中 12 步带渲染自检、终局取证重复 3 次测 flaky、轨迹墙钟 1200 秒（单序列约 25 token 每秒）、单位成本取本机 48 核配额下的实测吞吐（three.js 
- L253: 常驻 worker 能省掉每进程约 1 秒的启动与加载，这里不扣，算保守。
- L255: 一轮 RL 的总量同样是推算，而且这里有一个容易漏掉的放大项：动态采样会把「全对或全错」的组丢掉重采，通过率落在 5% 到 10% 这一段时，组大小 8 下实际要采的轨迹是名义值的 1.76 到 2.97 倍（即 1 除
- L255: 先给名义值：400 个优化步乘 64 个 prompt 乘组大小 8，等于 204,800 条轨迹；
- L255: 渲染 CPU 折 2.5 机日（多轮 three.js）到 21 机日（多轮 Blender）；
- L255: GPU 按 64 张做 rollout 加 64 张做训练算，名义上约 12,800 GPU 小时，计入重采放大后是 2.2 万到 3.8 万。
- L255: 这里的 GPU 假设是一个 30B 量级的 MoE 在 8 卡上服务约 128 条并发序列，本机未实测。
- L257: 而精度风险是超线性的——不开解耦 PPO 时，staleness 4 把 AIME24 从 42.0 砍到 23.3，近乎腰斩（表 2）。
- L259: 一是把前端、复刻、开放设计三族分开立项，前端那族先只做蒸馏对照，用它量出「判定模糊的任务族上 RL 到底亏多少」，目前这个判断只有 Qwen3 一组跨域数字支撑。
- L283: 让模型先把截图描述一遍再写码，是减 0.1 到减 0.9（上表第一行的两例）。
- L300: 前端整页截图长边常在 3000 到 10000 像素（本文估计），属于高分辨率文档那一侧，不能按小图基准外推。
- L304: 同文统计的冗余 token 占比随分辨率从 448 档的 26.6% 涨到 1334 档的 59.5%。
- L308: 当前视口给一张 1440 宽的截图，历史只留三张低分辨率；

## domains：带数字但没有链接（65 处）

- L7: 同一个参考页面重复渲染 5 次，几何回读的柱子坐标与坐标轴刻度像素位置逐位完全相同，截图的摘要值只有 1 种。
- L7: 参考解自己跟自己比，逐值回读的最大相对误差是 0.15%，而这 0.15% 每次都一样，来自图表库把柱子底边画在零线下方约半个像素的固定偏置，不是随机抖动。
- L7: 判据的容差定在 1%，对它有 6 倍余量。
- L13: | 逐值回读 | 13/16 | 3 | 0 |
- L14: | 像素比对 | 9/16 | 3 | 4 |
- L15: | 结构断言 | 14/16 | 2 | 0 |
- L16: | 逐值回读或结构断言 | 16/16 | 0 | 0 |
- L20: 轴截断那一个尤其说明职责边界：y 轴从 500 起画，柱子的几何仍然精确编码着原数值，线性拟合外推到零线之下读出 0.00% 误差，这是正确行为而不是失灵。
- L20: 结构断言漏掉的两个全部是纯数据错，整列缩放 1.3 倍和单点把 1510 画成 1150，结构完全合法。
- L22: 它漏掉的单点画错只让 0.75% 的像素发生变化，图例与数据错位只让 0.01% 的像素变化；
- L22: 要抓住 0.01% 就得把阈值压到千分之一以下，那时 30.51% 会被误杀得更彻底。
- L40: | 矢量图参考版 | 0.02% | 无 |
- L41: | 矢量图问题版 | 24.99% | 柱高统一乘 0.75，理论偏差 25% |
- L42: | 画布参考版 | 0.15% | 无，残差来自底边半像素偏置 |
- L46: 数据解读：24.99% 对上理论值 25%，说明回读量到的是真实绘制几何，而不是任何中间变量。
- L50: Harness 不要求模型配合暴露任何东西，理由和 3D 线相同：训练时模型只会学会写那一行，换一套 Harness 就失效。
- L64: | 参考解报告数据标签 360 个而不是 12 个，动画变异被误杀 | 每帧重绘都把所有文字重画一遍，文字钩子把 240 帧的记录全存了下来 | 给每条记录打帧号，只取最后一个画了字的帧 |
- L65: | 动画变异的逐值回读误差 2.70%，超过 1% 判据 | 只推了 30 帧虚拟时间 480 毫秒，而动画时长 800 毫秒，读到的是中间态 | 推到 240 帧，虚拟时间 3.84 秒 |
- L66: | 参考解报告 171 对文字重叠，实际 0 对 | 图表库普遍先平移旋转再在局部坐标里写字，钩子记的是局部坐标，旋转文本全堆在原点 | 文字包围盒四角过一遍当前变换矩阵；矢量图侧改用页面坐标接口 |
- L70: 数据解读：修掉这三个 bug 之后，逐值回读从 12/16 变 13/16，结构断言从 13/16 变 14/16。
- L80: 问题出在另一头：11 个该挂的变异里有 7 个在桌面宽度的首屏截图上与参考完全相同，相似度 1.0。
- L82: 状态本来就可读，所以确定性信号比 3D 侧更强。
- L86: | 信号 | 判对 | 检出 11 个该挂 | 误杀 11 个不该挂 |
- L88: | 单张截图逐像素，阈值取最优 | 14/22 | 4 | 1 |
- L89: | DOM 标签序列一致 | 11/22 | 2 | 2 |
- L90: | 类名序列一致 | 8/22 | 0 | 3 |
- L91: | 可见文本一致 | 11/22 | 0 | 0 |
- L92: | 正确性层 | 13/22 | 2 | 0 |
- L93: | 布局与响应式层，三视口 | 13/22 | 2 | 0 |
- L94: | 可访问性层 | 15/22 | 4 | 0 |
- L95: | 交互状态机层 | 14/22 | 3 | 0 |
- L96: | 性能预算层 | 12/22 | 1 | 0 |
- L97: | 五层组合 | 22/22 | 11 | 0 |
- L101: 类名序列这个朴素判据检出 0/11、误杀 3/11，比随机还差——它只能抓到「换了类名」这件事本身，而换类名正是最常见的等价重写。
- L101: 可见文本一致同样检出 0/11。
- L103: 要抓住对比度降级那一条，阈值必须设在 0.9883 以上；
- L103: Web 侧那 7 个该挂的变异在视觉上和参考完全一样——删掉替代文本、按钮换成普通容器、摘掉表单校验、启动时同步忙等、脚本尾部未定义变量、主题不落存储，图上都没有任何痕迹。
- L103: VLM 在这里的替代空间比 3D 侧更小，不是因为 VLM 弱，是因为这些错误压根不是视觉错误。
- L109: | 可访问性 | 4 | 对比度降级、缺替代文本、按钮换成普通容器、标题跳级加地标丢失 |
- L110: | 正确性 | 2 | 资源 404、运行时未捕获异常 |
- L111: | 交互状态机 | 2 | 表单校验被摘掉、主题不持久化 |
- L112: | 布局与响应式 | 1 | 窄视口横向溢出 |
- L113: | 性能预算 | 1 | 启动时的长任务 |
- L117: 差的那一条是卡片写死固定宽度：它在桌面宽度下一切正常，三列、无溢出、无越界，到手机宽度才暴露出 65 像素的横向溢出和 10 个越界元素。
- L117: 而本机实测里它贡献了 11 个真缺陷中其它四层都抓不到的那一个。
- L119: 这个数要打折：reward 与评测主指标是同一个量，所以 0.05 对 0.13 是「直接优化的量对零样本」而不是公平比较；
- L121: 漏掉的两个分别是「加载时无条件把主题写成深色、切换按钮其实什么都不做」和「把不合格文字的字号设为 0、再用伪元素把同样的字画回屏幕」。
- L121: 第二个修不掉——审计引擎对这个页面的输出是零违例、零需要复核、45 条通过，伪元素承载的文字它根本不检查，字号为 0 的真元素又被当成无文本跳过，两头都落空。
- L121: 补完两条判据后做了全量回归，仍然 22/22，零新增误杀；
- L123: 一个是 Verifier 的真 bug：列数测量用了表现型类名做选择器，类名一换就读成 0 列，修法是改成结构化定位，取主内容里第一个有两个以上子项的列表。
- L125: 剩下全是固定的稳定等待和 40 帧采样，去掉帧采样、把等待改成事件驱动、状态机复用同一个页面上下文，可以压到 1 秒以内（推算，未实测）。
- L125: 22 个变异全量两遍跑完 114 到 117 秒，平均 5.2 秒一个。
- L125: 两遍全量重跑的判定翻面 0 条，层级列表与明细逐字节一致——确定性信号不需要多次投票，这直接省掉乘在成本上的那个系数；
- L139: | 第一遍正常玩 | 40.5% |
- L140: | 再加一遍正常玩 | 41.0% |
- L141: | 把状态直接注入到规则的前置条件 | 48.5% |
- L145: 数据解读：加一遍正常玩只涨 0.5 个百分点，换成状态注入涨 8.0 个百分点。
- L145: 碰不到的规则就是 0 信号，判据再准也没用。
- L147: 源码判满分的规则，真玩时只有 76.8% 成立；
- L157: 这和 3D 线不要求页面暴露场景变量是同一条原则，换了领域没有变。
- L167: | 要求模型暴露接口 | 脚手架规定必须写 | 骗得过，训练时一定会被骗 | 强制 100% |
- L193: Web 排第一是因为三件事同时成立：判别力在 22 个带标签变异上零漏零误；
- L203: Web 侧是单参考页、22 个变异、其中 6 个留出，而且 22/22 是第二遍的结果，第一遍是 21/22；
- L203: 图表侧的 16/16 只有 1 个任务、16 个变异，没有做留出验证，而且只测了一个图表库。
- L203: 游戏侧的全部数字来自公开文献，本机一行代码都没跑过，拆出来的 33 条子命题是设计而不是结论。

