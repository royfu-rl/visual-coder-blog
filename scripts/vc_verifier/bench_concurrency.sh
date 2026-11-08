#!/bin/bash
# 并发 N 个独立 chrome 各跑一次 bench_threejs.js（启动+加载+单视角+8视角+scene graph），看总墙钟与单任务耗时
cd "$(dirname "$0")"
for N in "$@"; do
  s=$(date +%s%N)
  for i in $(seq $N); do node bench_threejs.js 1024 768 8 > out/conc_${N}_$i.json & done; wait
  e=$(date +%s%N)
  python3 - "$N" "$(( (e-s)/1000000 ))" <<'PY'
import json,sys,glob,statistics as st
n,wall=int(sys.argv[1]),int(sys.argv[2])
d=[json.load(open(f)) for f in glob.glob(f'out/conc_{n}_*.json')]
k='turntable_8_inpage_jpeg_ms'
print(f'N={n} wall={wall}ms throughput={n/wall*1000:.1f} task/s  turntable8_inpage median={st.median(x[k] for x in d):.0f}ms max={max(x[k] for x in d):.0f}ms  load median={st.median(x["load_ms"] for x in d):.0f}ms')
PY
done

