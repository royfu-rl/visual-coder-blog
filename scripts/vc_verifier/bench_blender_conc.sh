#!/bin/bash
# N 个 blender 进程并发，各渲 8 视角 512x384，看总吞吐。用法: ./bench_blender_conc.sh ENGINE SPP N...
cd "$(dirname "$0")"; E=$1; SPP=$2; shift 2
for N in "$@"; do
  s=$(date +%s%N)
  for i in $(seq $N); do blender -b --factory-startup --python bench_blender.py -- $E 8 512 $SPP 4 > out/blc_${E}_${N}_$i.log 2>&1 & done; wait
  w=$(( ($(date +%s%N)-s)/1000000 ))
  ok=$(grep -l VCJSON out/blc_${E}_${N}_*.log | wc -l)
  echo "$E N=$N ok=$ok wall=${w}ms  => $(python3 -c "print(round($ok*8/($w/1000),1))") views/s"
done

