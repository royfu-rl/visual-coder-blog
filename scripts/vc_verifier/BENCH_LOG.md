# vc_verifier 实测记录（2026-10-15，本机 KML pod）

机器：384 逻辑核，cgroup 配额 cpu.max=4787500/100000（约 47.9 核），无 GPU、无 /dev/dri、无 DISPLAY

## three.js（Chrome 148 headless + SwANGLE）
- 依赖：npm i puppeteer-core@23 three@0.169.0 playwright-core@1.48.2（49s + 39s）
- 场景：scene/index.html（暴露 window.__vc：view / graph / setTime / gl）
- node bench_threejs.js 1024 768 8 → 单进程跑全流程（3 次）
- ./bench_concurrency.sh 1 8 32 64 → 每任务独立起 chrome
- node bench_pool.js B P R → 复用 chrome 的稳态吞吐
- node bench_clock.js 20 → 时钟控制下的逐字节确定性

## Blender
- 系统 apt：/usr/bin/blender 4.0.2（EEVEE Legacy）
  - blender -b --factory-startup --python bench_blender.py -- ENGINE N RES SPP THREADS
  - ./bench_blender_conc.sh ENGINE SPP N... → 多进程并发
- pip bpy 4.5.14 LTS（EEVEE Next）：.venv_bpy（uv python 3.11.14）
  - 内网镜像 bpy 4.2~4.4 均 502（未缓存）→ 走海外代理 uv pip install "bpy==4.5.*"，121s，包体 784MB
  - .venv_bpy/bin/python bench_blender.py -- BLENDER_EEVEE_NEXT 8 512 16 0
- 结果数字汇总见 middle_processing/vc_data/06_harness.md 第 4 节；原始日志 out/*.log、out/*.json

