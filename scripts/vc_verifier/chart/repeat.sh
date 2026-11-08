#!/bin/bash
# 重复 N 次渲染同一个参考解，检查「逐值回读」和「截图」各自是否逐次一致 → 量 verifier 的噪声地板
cd "$(dirname "$0")"; N=${1:-5}
for i in $(seq $N); do node harness.js pages/ref.html out/rep_$i >/dev/null; done
python3 - "$N" <<'PY'
import json,sys,hashlib
N=int(sys.argv[1])
def vals(c):
    d=json.load(open(f'out/rep_{c}/readback.json')); ch=d['chartjs']['charts'][0]
    return [(ds['label'],[ (e['x'],e['y'],e['base']) for e in ds['elements']]) for ds in ch['datasets']], \
           [ (t['value'],t['px']) for t in ch['scales']['y']['ticks'] ]
geo=[vals(i) for i in range(1,N+1)]
png=[hashlib.md5(open(f'out/rep_{i}/shot.png','rb').read()).hexdigest()[:8] for i in range(1,N+1)]
print(f'{N} 次重复：几何回读完全相同 = {all(g==geo[0] for g in geo)}；截图 md5 种类数 = {len(set(png))} {sorted(set(png))}')
PY

