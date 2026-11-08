# 06 Harness：visual coding RL 的执行环境与视觉自检工具

调研日期 2026-10-15。star 数为当日 GitHub API 实查。本机实测脚本见 /mmu_mllm_hdd_4/deep-research/visual-coder-blog/scripts/vc_verifier/（命令清单 BENCH_LOG.md）。

## 0. 结论速览

- 纯 CPU 就够用
  - three.js：Chrome headless + SwANGLE（SwiftShader 上的 ANGLE）。本机 8 视角转台约 0.2 s。复用浏览器后，48 核配额下稳态约 14 任务/s
  - Blender：apt 版 4.0 和 pip 版 bpy 4.5 都能在无 GPU、无显示的环境里跑 Workbench / EEVEE / Cycles。EEVEE 走 Mesa 的 surfaceless swrast（llvmpipe）
  - 结论：RL rollout 的视觉验证不必上 GPU 沙箱
- 确定性要靠 harness 主动控制
  - three.js 侧要冻结时钟、固定随机种子、固定 DPR
  - 只调 Playwright clock.install、不调 pauseAt，3/3 次截图都不同；加上 pauseAt 后仍有两个模式（11/9），推测是 rAF 的帧相位
  - 最稳的做法：在任务契约里要求页面暴露 setTime / view 钩子，并用 canvas.toDataURL 直读像素。直读 3/3 逐字节一致
- 自检工具的核心不是截图
  - 应同时给结构化观测：scene graph、console、bbox。返回 JSON 的成本是毫秒级，看图要 token
  - 多视角最好拼成一张 contact sheet，token 是逐张发送的 1/8 左右
- 训练与评测的工具要同构
  - 同一模型换 scaffold，分差可以达到数个百分点
  - 建议训练时就用「一套 MCP 工具 + 两种 transport」，评测时原样复用

## 1. Docker 镜像与渲染

### 1.1 无头浏览器渲染 WebGL / three.js

- 渲染后端
  - SwANGLE：`--use-gl=angle --use-angle=swiftshader(-webgl) --enable-unsafe-swiftshader`
    - Chrome 官方文档：https://chromium.googlesource.com/chromium/src/+/main/docs/gpu/swiftshader.md
  - SwiftShader 回退被弃用
    - Chrome 130 起打警告：https://groups.google.com/a/chromium.org/g/blink-dev/c/yhFguWS_3pM/m/oLrB5up_BwAJ
    - M139 起，不显式 opt-in 就建不了 WebGL：https://developer.samsung.com/browser/policy/enable-unsafe-swift-shader.html
    - 所以 `--enable-unsafe-swiftshader` 是必加 flag。本机 Chrome 148 实测：不加就没有 WebGL
  - 不要加 `--disable-gpu`。它会把 SwANGLE 也关掉
    - 出处：chromedp v0.14.1 的提交说明 https://chromium.googlesource.com/external/github.com/chromedp/chromedp/+/refs/tags/v0.14.1
  - 真 GPU（EGL/Vulkan）的 flag 组合：未核实。CPU 已经够用，可以不追
- headless 模式
  - Chrome 112 起，新 headless 与正式版 Chrome 同源
  - 132 起，旧 headless 独立成 `chrome-headless-shell`（Puppeteer 里对应 `headless:'shell'`）
  - 出处：https://developer.chrome.com/docs/chromium/headless
- 确定性手段
  - 固定 viewport、deviceScaleFactor=1，加 `--font-render-hinting=none --disable-lcd-text`
    - 出处：https://argos-ci.com/docs/learn/reliability-and-flakiness/flaky-tests/stabilize-text-rendering
  - 字体：镜像里打包固定字体集，禁止页面联网拉 Google Fonts。fontconfig 的细节：未核实
  - 时间：Playwright Clock API（1.45 引入），包括 install / pauseAt / runFor / fastForward
    - 出处：https://playwright.dev/python/docs/clock
  - 随机：用 addInitScript 注入带种子的 Math.random。属常规做法，未找到官方出处
  - 虚拟时间：`--deterministic-mode`、`--virtual-time-budget`、`--run-all-compositor-stages-before-draw` 都只在 headless-shell 里有，属实验性
    - 出处：https://chromium.googlesource.com/chromium/src/+/main/headless/public/switches.h
    - ArchiveBox 因兼容问题删掉了 virtual-time-budget：https://git.causa-arcana.com/forks/archivebox/commit/9f05cf82831127e2bb2d2e08b62cbad1abf1d2e5
  - 实测结论见 4.1.4：clock 只能把方差压下来，压不到零。逐字节一致要靠页面钩子

### 1.2 Blender 无头

- 调用方式
  - `blender -b --factory-startup --python x.py -- args`
  - 或者 `pip install bpy`，在 python 里直接 import
- EEVEE 能否无头
  - Blender 3.4 起，Linux 的 `-b` 模式有 headless EGL 后端，其他后端失败时自动回退
    - 提交 D15555：https://developer.blender.org/rB3195a38
    - 报道：https://www.phoronix.com/news/Blender-3.4
  - EEVEE Next（4.2+）官方要求 OpenGL 4.3，外加 GL_ARB_shader_draw_parameters 和 GL_ARB_clip_control
    - 出处：https://www.blender.org/download/requirements/
  - 官方没说 llvmpipe 能不能跑。本机实测：能跑，但慢（见 4.2）
    - 实测路径：Mesa 25.2.8，`DRI2: failed to load driver`，然后 `Falling back to surfaceless swrast without DRM`
- Cycles CPU
  - 不依赖 GL，最稳
  - 坑：`-E CYCLES` 只改当前场景。.blend 里其他 EEVEE 场景照样会要显示
    - 出处：https://devtalk.blender.org/t/blender-2-8-unable-to-open-a-display-by-the-rendering-on-the-background-cycles/8607/18
- Workbench
  - 同样走 GPU 模块，在 EGL swrast 下实测可用，是最快的「看形状」引擎
- pip bpy 与 Python 版本（PyPI JSON：https://pypi.org/pypi/bpy/json）
  - 4.0 → 3.10；4.1 ~ 5.0 → 3.11；5.1 / 5.2 → 3.13
  - 每个版本只支持一个 Python 小版本
  - 4.0、4.1 已从 PyPI 下架，要到 https://download.blender.org/pypi/bpy/ 取
  - 本机 Python 是 3.12，所以用 uv 装 3.11 建 venv
- 官方或社区 docker 镜像
  - nytimes/blender：约 514MB，已停更 3 年以上
    - 出处：https://hub.docker.com/r/nytimes/blender
  - linuxserver/blender：在维护，有 5.1.0 tag，约 1.3GB（镜像站数字）
    - 这是 KasmVNC 桌面镜像，不是批处理镜像，也不支持 GPU 渲染
    - 出处：https://docs.linuxserver.io/images/docker-blender/
  - 自建建议：ubuntu 24.04 + libegl-mesa0 + libgl1-mesa-dri，再加 bpy wheel 或官方 tar 包
    - 体积量级：bpy 4.5 的 site-packages 实测 784MB；apt blender 加 blender-data 约 181MB 安装体积

### 1.3 游戏引擎

- Godot 4
  - `--headless` 等于 dummy 渲染器，读不回贴图，不能截图
    - 出处：https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html
  - 能截图的做法：不加 --headless，用 `xvfb-run` 跑，加 `--rendering-driver opengl3`，再用 viewport.get_texture().get_image() 存图
  - 确定性：`--write-movie` 配 `--fixed-fps`
  - 4.x 后续版本有没有原生离屏渲染：未核实
- Unity
  - `-batchmode -nographics` 不初始化图形设备，不能渲染或截图
    - 出处：https://docs.unity3d.com/Manual/EditorCommandLineArguments.html
  - 许可
    - Personal 许可不能用 serial 激活。GameCI 的做法是导出 .ulf，再配 UNITY_LICENSE / EMAIL / PASSWORD
      - 出处：https://game.ci/docs/github/activation
      - 出处：https://docs.unity3d.com/Manual/ManagingYourUnityLicense.html
    - 在大规模 RL 集群上，许可合规是硬阻塞
  - 结论：游戏类任务优先用 Web 引擎（three.js / Phaser / Babylon），其次 Godot，尽量不要 Unity

### 1.4 吞吐、成本与沙箱平台

- 本机 CPU 吞吐（详见第 4 节）
  - three.js：8 视角加 scene graph，复用 chrome 后约 14 任务/s（48 核）
  - Blender Workbench 约 15.5 视角/s；EEVEE Legacy 约 6.4 视角/s（512x384，32 进程并发）
- 沙箱平台

  | 平台 | GPU | 图形 / 显示 | 冷启动 | 计费 |
  |---|---|---|---|---|
  | E2B | 无 | Desktop 模板（Xvfb + XFCE + noVNC），有 e2b-desktop SDK | 300 ~ 500ms（自报） | vCPU 0.000014 美元/s；Pro 150 美元/月；会话 Pro 24h |
  | Modal | 有，T4 0.000164 ~ B300 0.001972 美元/s（H100 约 3.95 美元/h） | 未核实 | 未核实 | Sandbox 用 GPU 须 runtime=gvisor；CPU 约为函数价 3 倍；默认 5min 超时，最长 24h |
  | Daytona | 有，每沙箱独占一卡，VFIO 直通（H100 / H200 / RTX Pro 6000 / 4090 / 5090） | 未核实 | 未核实 | 未核实 |
  | Runloop | 无 | Browser / Computer add-on | 未核实 | 0.08 ~ 1.68 美元/h |
  | Morph Cloud | 无 | 未核实 | snapshot / branch < 250ms | 0.05 美元/MCU |

  - 出处
    - E2B：https://e2b.dev/pricing ，https://docs.e2b.dev/template/examples/desktop
    - Modal：https://modal.com/pricing ，https://modal.com/docs/guide/sandbox
    - Daytona：https://www.daytona.io/docs/en/sandboxes/gpu-sandboxes
    - Runloop：https://docs.runloop.ai/docs/devboxes/configuration/sizes
    - Morph：https://cloud.morph.so/docs/documentation/setup/plans
  - 含义：目前没有一家平台写明「GPU + OpenGL/Vulkan 图形栈」。要真 GPU 光栅，得自己做 NVIDIA graphics capability 和 EGL 镜像。CPU 方案能省掉这一整套

## 2. Agent 的视觉自检工具

### 2.1 现有产品与开源

- 浏览器类
  - Playwright MCP（microsoft/playwright-mcp，★38,140）
    - 默认 snapshot 模式：读可访问性树，按元素 ref 操作
    - `--caps=vision`：开放坐标点击、拖拽、滚轮
    - browser_take_screenshot 参数：element / target、type（png/jpeg/webp）、fullPage、scale（css/device）
    - browser_console_messages 参数：level
    - 出处：https://github.com/microsoft/playwright-mcp
  - Chrome DevTools MCP（ChromeDevTools/chrome-devtools-mcp，★53,531）
    - 59 个工具：take_screenshot、take_snapshot、list_console_messages、evaluate_script、performance trace、lighthouse_audit、screencast_start/stop、network 等
    - 有 `--slim` 精简集
    - 出处：https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md
- 3D / 引擎类
  - Blender MCP（ahujasid/blender-mcp，★30,814；仓库已改名 mcp-for-blender）
    - 当前工具：execute_blender_code、look（视口 / 相机 / 多角度自动取景 / 渲染图）、get_scene_info（可按 root / query 下钻）、generate_3d（Tripo / Hunyuan3D / Rodin）、search_assets / import_asset（Poly Haven / Sketchfab / Poly Pizza）
    - 旧版的 get_object_info 和 get_viewport_screenshot 已并入上面这些
    - 架构：插件起 socket server，JSON over TCP，监听 localhost:9876，无鉴权；可设 BLENDER_MCP_SAFE_MODE=1
    - 出处：https://github.com/ahujasid/blender-mcp
  - three.js MCP 生态很小
    - DmitriyGolub/threejs-devtools-mcp（★119）：注入 bridge，能查场景树、材质、draw call，能截图
      - 出处：https://github.com/DmitriyGolub/threejs-devtools-mcp
  - Godot MCP（Coding-Solo/godot-mcp，★6,081）：run_project + get_debug_output，README 没写截图
  - Unity MCP（CoplayDev/unity-mcp，★14,947）：约 50 个工具，README 没写截图
- 编程 agent 产品
  - Claude Code
    - `claude --chrome` 接 Claude in Chrome 扩展，可读 console / DOM、截图、录 GIF
    - 也可以自己挂 Playwright MCP
    - 出处：https://code.claude.com/docs/en/chrome
  - Cursor
    - 内置浏览器，截图交给读文件工具，模型「actually sees the browser state as images」
    - console 写成文件，按需 grep
    - 出处：https://cursor.com/docs/agent/browser
  - Codex
    - 官方原话：「Codex can spin up its own browser, look at what it built, iterate, and attach a screenshot」
    - 出处：https://openai.com/index/introducing-upgrades-to-codex/
- 生成类产品
  - v0：能打开自己做的 app 使用并 critique，检测到错误后在生成循环里自动修
    - 出处：https://v0.app/docs/agentic-features
  - Lovable：在虚拟环境里开真浏览器，截图、点击、读 console 和网络。但只在需要时用，默认先走更快的验证
    - 出处：https://docs.lovable.dev/features/browser-testing
  - bolt.new：没找到官方写的看图自修 loop。官方承认部分运行时错误检测不到，要用户贴 console
    - 出处：https://support.bolt.new/troubleshooting/preview-issues
  - 共性：产品端是「编译和 console 错误自动修 + 选择性看图」，而不是每步都截图

### 2.2 工具 schema 设计（建议）

- 观测类工具：先给结构，再给像素
  - `get_scene_graph(filter?)`
    - 返回：name / type / parent / material / color / 世界 bbox / 三角面数
    - three.js 用 scene.traverse，Blender 用 bpy.data.objects
    - 实测耗时 1.8ms（three.js，13 个 mesh）、0.2ms（Blender，10 个物体）
  - `console_logs(level>=warning)`：加上 pageerror 和 404 资源。最便宜、信号最强的自检
  - `screenshot(url, viewport=1024x768, wait="ready_hook|ms", dpr=1)`
    - wait 优先等页面的 ready 钩子，不要固定睡几秒
  - `render_views(n=8, elevation=25, radius=auto, res=512, layout="grid")`
    - 转台多视角，默认拼成一张 contact sheet
    - radius=auto 按场景 bbox 取景
  - `interact(actions[], record_every_ms)`
    - 返回关键帧：前、中、后 3 帧（ArtifactsBench 的做法），或每隔 N ms 一帧
- 图像 token 成本（决定工具默认分辨率）
  - Claude：⌈w/28⌉×⌈h/28⌉
    - 标准档长边上限 1568，4.7 及之后的高分辨率档上限 2576
    - 超限的 tool_result 图片直接报错，不会自动缩放
    - 出处：https://platform.claude.com/docs/en/build-with-claude/vision
  - OpenAI 有两种计法
    - tile 计法：gpt-5 / 5.1 是 70 + 140×(512 tile 数)；gpt-4o 是 85 + 170×tile
    - patch 计法（GPT-5.2 及之后）：⌈w/32⌉×⌈h/32⌉×1.2
    - 出处：https://developers.openai.com/api/docs/guides/images-vision
  - Gemini：两边都 ≤384 时 258 token，否则按 768 切块，每块 258
    - Gemini 3 按 media_resolution 档位：280 / 560 / 1120 / 2240
    - 出处：https://ai.google.dev/gemini-api/docs/image-understanding
  - 按 Claude 公式算的几组例子

    | 图像 | 单张 token | 8 张合计 |
    |---|---|---|
    | 1024×768 | 1,036 | 8,288 |
    | 512×384 | 266 | 2,128 |
    | 8 视角拼成一张 1024×512 contact sheet（每格 256×256） | 703 | — |

    - 结论：多视角默认用 contact sheet；局部细节再按需放大
- 训练与评测的工具一致性（多 scaffold）
  - 证据：Anthropic 原话「performance of an agent on SWE-bench can vary significantly based on this scaffolding」，他们只用 Bash + Edit
    - 出处：https://www.anthropic.com/research/swe-bench-sonnet
  - 同模型换 scaffold 的分差：OpenSWE-32B 在 OpenHands 上 59.8%，在 SWE-agent 上 62.4%（二手转述，待回原表核实）
  - 做法
    - 工具语义层固定：同名、同参数、同返回结构
    - transport 可替换：训练时进程内直调，评测和产品时走 MCP
    - 训练时随机化工具子集或参数默认值（分辨率、视角数），防止过拟合某一个 scaffold
    - 保留一个 bash-only 退化通道（mini-swe-agent 风格），保证没有专用工具时也能自己写 puppeteer 或 bpy 脚本截图
    - 图像预算写进环境：每条轨迹的视觉 token 上限，超了就强制降分辨率。这是 RL 成本的主要旋钮

## 3. 已有开源 harness 怎么搭

- 通用 coding agent
  - OpenHands（★90,893）
    - 每个任务一个 Docker sandbox，容器内的 ActionExecutor 通过 REST 收发动作和观察
    - 浏览器用 BrowserGym（★1,402），默认读可访问性树；VisualBrowsingAgent 和 OpenHands-Versa 支持截图 + Set-of-Marks
    - 出处：https://docs.openhands.dev/openhands/usage/architecture/runtime ，https://arxiv.org/abs/2506.03011
  - SWE-agent（★20,553）：沙箱用 SWE-ReX
  - mini-swe-agent（★8,516）
    - 只用 bash，每个动作一次 subprocess，换成 docker exec 就能沙箱化
    - 历史是线性的，适合拿来做 RL
    - SWE-bench 官方 bash-only 榜用的就是它
    - 出处：https://github.com/SWE-agent/mini-swe-agent
  - 训练 harness 的规模
    - SWE-Gym：2,438 个实例，每个实例一个预构建镜像
    - R2E-Gym：8.1K 题
    - SWE-smith：50k 实例
    - OpenSWE：45,320 个 Docker 环境
    - 出处：https://github.com/SWE-Gym/SWE-Gym ，https://arxiv.org/abs/2504.21798 ，https://arxiv.org/abs/2603.13023
- 视觉类 benchmark 的执行框架
  - BlenderGym（CVPR 2025，代码 BlenderGym-Open ★45）
    - 245 对起始 / 目标场景，覆盖几何、光照、材质、blend shape、摆放
    - 每对至少 3 个固定机位
    - 指标：Photometric loss、N-CLIP、Chamfer。Blender 版本没写明
    - 出处：https://arxiv.org/abs/2504.01786
  - WebGen-Bench（★60）
    - 101 条指令、647 个测试用例
    - WebVoyager agent（Qwen2.5-VL-32B）最多交互 15 步，判 YES / PARTIAL / NO；外观分由 GPT-4o 打 1 ~ 5
    - 出处：https://arxiv.org/abs/2505.03733
  - ArtifactsBench（腾讯，★280）
    - 1,825 个任务
    - Playwright 无头 Chromium，1024×768，交互前、中、后各截 1 张
    - judge 用 Gemini-2.5-Pro 或 Qwen2.5-VL-72B，按 10 维 checklist 打分
    - 与 WebDev Arena 排名一致 94.4%
    - 出处：https://arxiv.org/abs/2507.04952
  - Vision2Web（ICML 2026，★82）
    - 193 个任务、918 张原型图、1,255 个测试用例
    - GUI agent 验证器 + VLM judge，出视觉分和功能分
    - 出处：https://arxiv.org/abs/2603.26648
  - VideoGameBench（★375）
    - GB 用 PyBoy，DOS 用浏览器里的 JS-DOS + Playwright，只给截图
    - Lite 模式在模型思考时暂停游戏
    - 最好的模型完成度 0.48%
    - 出处：https://arxiv.org/abs/2505.18134
  - 共性
    - 都是「Docker 内无头渲染 + 固定机位或固定时刻截图 + VLM 或像素指标」
    - 没有一家把 scene graph 当作 verifier 的一等输入，这是空位

## 4. 本机可行性实测

环境：KML pod，cgroup 配额约 47.9 核（cpu.max=4787500/100000），384 逻辑核，无 GPU、无 /dev/dri、无 DISPLAY。脚本都在 scripts/vc_verifier/。

### 4.1 three.js：Chrome 148 headless + SwANGLE

- 4.1.1 单进程全流程（bench_threejs.js，1024×768，3 次）
  - WebGL 上下文：「ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero)))」，WebGL2 可用

  | 步骤 | 耗时 |
  |---|---|
  | 启动 chrome | 172 ~ 191 ms |
  | 加载场景直到 ready 钩子 | 401 ~ 420 ms |
  | 单视角 page.screenshot | 64 ~ 85 ms |
  | 单视角 canvas.toDataURL | 62 ms |
  | 8 视角转台，逐张 page.screenshot | 477 ~ 540 ms |
  | 8 视角转台，一次 evaluate 内渲染 + toDataURL(jpeg) | 192 ~ 202 ms |
  | 读 scene graph（13 个 mesh，含世界 bbox） | 1.8 ms |

  - 同视角渲两次，PNG 逐字节一致 3/3（页面钩子驱动，不走 rAF）
  - console 抓到 1 条 404（favicon），说明 console 通道是通的
- 4.1.2 每个任务独立起 chrome（bench_concurrency.sh）

  | 并发 N | 总墙钟 | 吞吐 |
  |---|---|---|
  | 1 | 1.8 s | 0.6 任务/s |
  | 8 | 2.2 s | 3.6 任务/s |
  | 32 | 8.9 s | 3.6 任务/s |
  | 64 | 19.7 s | 3.2 任务/s |

  - N≥8 就饱和，瓶颈是 chrome 启动
- 4.1.3 复用 chrome（bench_pool.js，每个任务 = reload + 8 视角 + scene graph）

  | 配置 | 吞吐 | p50 | p95 |
  |---|---|---|---|
  | 1 浏览器 × 1 页 | 2.4 任务/s | 383 ms | — |
  | 1 浏览器 × 8 页 | 3.4 任务/s | — | — |
  | 4 浏览器 × 8 页 | 11.6 任务/s | — | — |
  | 8 浏览器 × 8 页 | 14.3 任务/s | 4.1 s | 4.9 s |

  - 判断：每个浏览器只有一个 GPU 进程，SwiftShader 在里面串行，所以要多浏览器 × 多页
- 4.1.4 确定性（bench_clock.js，动画页用 rAF + performance.now + Math.random，不暴露钩子）

  | 方案 | 截图 md5 种类数 |
  |---|---|
  | 不控制 | 3/3、20/20 全不同 |
  | 只调 clock.install | 3/3 不同（加载耗时 113 ~ 432 ms 漏进了 performance.now） |
  | install + pauseAt + runFor(1500) + 种子 random | 20 次里有 2 种，11/9 |

  - 第 3 行的两种结果，推测是 rAF 帧相位差一帧，未核实
  - 结论
    - 能逐字节复现的只有「页面钩子 setTime + 直读 canvas」
    - 对模型自由写的页面，verifier 要用感知容差（SSIM 或 pHash），不能比 hash
- 4.1.5 体积
  - chrome-linux64 目录 552MB
  - node_modules（puppeteer-core + three + playwright-core）65MB

### 4.2 Blender

- 本机已有 /usr/bin/blender 4.0.2（apt，EEVEE Legacy）。另用 uv 建了 Python 3.11.14 venv，装 bpy 4.5.14 LTS（EEVEE Next）
  - 内网 pypi 镜像列出了 bpy 4.2 ~ 4.4，但下载都返回 502
  - 改走海外代理 uv pip install，用时 121 s，包体 784MB
- 场景：同一张桌子 + 环面 + 太阳光，8 视角转台。命令：bench_blender.py
  - 表中「首帧」是第一个视角，包含 shader 编译；「之后每视角」是后续视角的单张耗时

  | 版本 / 引擎 | 分辨率 / 采样 | 首帧 | 之后每视角 | 8 视角合计 |
  |---|---|---|---|---|
  | 4.0 Workbench | 512×384 | 1.26 s | 0.10 s | 2.0 s |
  | 4.0 Workbench | 1024×768 | 0.52 s | 0.22 s | 2.1 s |
  | 4.0 EEVEE Legacy | 512, 16 spp | 3.2 s | 0.6 s | 7.3 s |
  | 4.0 EEVEE Legacy | 1024, 64 spp | 1.6 s | 1.35 s | 11.2 s |
  | 4.0 Cycles CPU 8 线程 | 512, 32 spp | 0.9 s | 0.78 s | 6.3 s |
  | 4.0 Cycles CPU 48 线程 | 1024, 128 spp | 1.8 s | 1.6 s | 12.9 s |
  | 4.0 Cycles CPU 8 线程 | 1024, 128 spp | 8.7 s | 8.2 s | 65.2 s |
  | bpy 4.5 Workbench | 512 | 0.85 s | 0.07 s | 1.35 s |
  | bpy 4.5 EEVEE Next | 512, 16 spp | 13.3 s | 2.8 s | 33.1 s |
  | bpy 4.5 Cycles CPU 8 线程 | 512, 32 spp | 0.96 s | 0.88 s | 7.1 s |

  - EEVEE Next 在 llvmpipe 上能出正确图像（非黑帧，像素标准差约 45）
    - 比 Legacy 慢 4 ~ 5 倍
    - 首帧 shader 编译 13 s，适合常驻进程复用
  - 读 scene graph（10 个物体）：0.1 ~ 1 ms
- 多进程并发，512×384，8 视角（bench_blender_conc.sh）

  | 引擎 | N=1 | N=8 | N=32 |
  |---|---|---|---|
  | Workbench | 5.2 视角/s | 9.7 视角/s | 15.5 视角/s |
  | EEVEE Legacy 16 spp | 1.4 视角/s | 5.4 视角/s | 6.4 视角/s |

  - 每个进程启动和加载约 1 s
- 结论
  - verifier 的「看形状」用 Workbench：每视角 0.1 s，可以塞进 RL 的每步观测
  - 「看材质和光照」用 Cycles CPU，低 spp + 低分辨率：约 1 s / 视角，留给最终 reward
  - EEVEE Next 在 CPU 上性价比最低

### 4.3 Godot / Unity

- 本机两者都没装，未实测。可行路径见 1.3

## 5. 推荐方案（给 visual coding RL）

- 镜像分层
  - 基础层：ubuntu 24.04、Mesa（EGL swrast）、固定字体包
  - Web 层：Node 20、chrome-for-testing 固定版本、puppeteer-core 或 playwright-core、three 固定版本，并且离线 vendored（防止页面联网）
  - 3D 层：bpy 4.5 LTS wheel 或官方 tar 包（约 0.8GB）
  - 整套全用 CPU，不依赖 GPU 沙箱
- 渲染服务
  - 常驻浏览器池，按「多浏览器 × 多页」组织
  - 常驻 bpy worker，避免每次付 1 s 启动和 13 s shader 编译
  - harness 在 rollout 外调度，按需限流
- 任务契约
  - 要求产物暴露钩子：three.js 暴露 window.__vc 的 scene / setTime / ready；Blender 约定物体命名或 collection
  - 拿不到钩子时退到时钟冻结 + 感知容差比对
- 工具集（训练和评测同构）
  - get_scene_graph
  - console_logs
  - render_views（默认 contact sheet，512 档）
  - screenshot
  - interact（3 帧）
  - bash 兜底
  - 外加每条轨迹的视觉 token 预算
- reward 侧
  - scene graph 程序化检查（对象存在、相对位置、bbox 尺度）
  - console 无错
  - 多视角 VLM judge
  - 三者组合
  - 详见 verifier 章节

