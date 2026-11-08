#!/bin/bash
# 等主矩阵收尾 -> 用修好的 verifier 重做参考探测与准入 -> 归档旧结果 -> 重跑五个反馈臂
cd "$(dirname "$0")"
while pgrep -f "[p]ython3 solve\.py" >/dev/null; do sleep 30; done
echo "[chain] 主矩阵结束 $(date)"
python3 - <<'PY'
import json
from pathlib import Path
import compare, verify
runs=Path('runs/desk_gen')
ref=compare.probe(Path('tasks/desk_gen/ref.html'), runs/'ref'); json.dump(ref, open(runs/'ref/probe.json','w'))
assert verify.verify(runs/'ref', ref, runs/'ref', ref)['verdict']=='pass'
spec=json.load(open('tasks/desk_gen/tasks.json')); bad=[]
for t in spec['tasks']:
    v=verify.probe_and_verify(runs/'ref', ref, Path(t['start']), runs/f"b4_{t['id']}")
    t['admit']['broken_fail_at']=v['layer']
    if v['verdict']!='fail': bad.append(t['id'])
json.dump(spec, open('tasks/desk_gen/tasks.json','w'), indent=1, ensure_ascii=False)
print('[chain] 准入复查，仍不挂的:', bad)
PY
mv runs/desk_gen_solve/results.jsonl runs/desk_gen_solve/results_prefix_bug.jsonl
echo "[chain] 重跑五臂 $(date)"
python3 solve.py tasks/desk_gen --rounds 3 --workers 36 --conds none,page,multi,graph,oracle
echo "[chain] 全部完成 $(date)"

