"""python3 analyze.py [judge|solve]

把两个实验的原始结果汇总成可直接引用的数字。
judge: VLM 判定的准确率、单图与多视角的配对比较（McNemar）、重测一致率、按错误类型拆开
solve: 四种反馈 × 两种问题描述下的修复通过率、每题难度分布
"""
import collections, json, math, sys
from pathlib import Path

HERE = Path(__file__).parent
R = HERE / 'runs'


def mcnemar(b, c):
    """配对二分类的 McNemar 检验，b/c 是两种条件下结论相反的两类计数"""
    n = b + c
    if n == 0: return 1.0
    chi = (abs(b - c) - 1) ** 2 / n          # 连续性校正
    return math.erfc(math.sqrt(chi / 2))     # 卡方 1 自由度的双侧 p


def judge():
    rows = [json.loads(l) for l in open(R / 'vlm_judge.jsonl')]
    models = sorted({r['model'] for r in rows})
    fam = {}   # case -> 来源任务
    for r in rows: fam[r['name']] = r['task']

    print('== 每个 judge 的准确率（单图 vs 多视角拼图）==')
    print(f"{'judge':20s} {'单图':>12s} {'多视角':>12s} {'单对多错':>8s} {'单错多对':>8s} {'p':>7s}")
    agg = collections.Counter()
    for m in models:
        acc, byc = {}, {}
        for c in ['single', 'multi']:
            rs = [r for r in rows if r['model'] == m and r['cond'] == c and r['verdict']]
            acc[c] = (sum(r['verdict'] == r['should'] for r in rs), len(rs))
            byc[c] = {}
            for r in rs: byc[c].setdefault(r['name'], []).append(r['verdict'] == r['should'])
        b = c2 = 0
        for name in set(byc['single']) & set(byc['multi']):
            s = sum(byc['single'][name]) / len(byc['single'][name])
            t = sum(byc['multi'][name]) / len(byc['multi'][name])
            if s > t: b += 1
            elif t > s: c2 += 1
        agg['b'] += b; agg['c'] += c2
        print(f"{m:20s} {acc['single'][0]:4d}/{acc['single'][1]:<7d} {acc['multi'][0]:4d}/{acc['multi'][1]:<7d}"
              f" {b:8d} {c2:8d} {mcnemar(b, c2):7.3f}")
    print(f"{'合计':20s} {'':12s} {'':12s} {agg['b']:8d} {agg['c']:8d} {mcnemar(agg['b'], agg['c']):7.3f}")

    print('\n== 重测一致率（同一 judge、同一 case、两次 temperature 0）==')
    for m in models:
        for c in ['single', 'multi']:
            p = {}
            for r in rows:
                if r['model'] == m and r['cond'] == c: p.setdefault(r['name'], []).append(r['verdict'])
            pairs = [v for v in p.values() if len(v) == 2]
            same = sum(v[0] == v[1] for v in pairs)
            print(f'  {m:20s} {c:6s} {same}/{len(pairs)}  翻面率 {1 - same / max(len(pairs), 1):.1%}')

    print('\n== 多模型多数投票 ==')
    for c in ['single', 'multi']:
        ok = tot = 0
        for name in sorted({r['name'] for r in rows}):
            vs = [r['verdict'] for r in rows if r['name'] == name and r['cond'] == c and r['verdict']]
            if not vs: continue
            sh = next(r['should'] for r in rows if r['name'] == name)
            v = 'pass' if vs.count('pass') > vs.count('fail') else 'fail'
            ok += v == sh; tot += 1
        print(f'  {c:6s} {ok}/{tot}')

    print('\n== 按来源任务拆开（多数投票）==')
    for task in sorted(set(fam.values())):
        line = [f'  {task:14s}']
        for c in ['single', 'multi']:
            ok = tot = 0
            for name in sorted({r['name'] for r in rows if fam[r['name']] == task}):
                vs = [r['verdict'] for r in rows if r['name'] == name and r['cond'] == c and r['verdict']]
                if not vs: continue
                sh = next(r['should'] for r in rows if r['name'] == name)
                v = 'pass' if vs.count('pass') > vs.count('fail') else 'fail'
                ok += v == sh; tot += 1
            line.append(f'{c} {ok}/{tot}')
        print('  '.join(line))


def solve():
    f = R / 'desk_gen_solve/results.jsonl'
    rows = [json.loads(l) for l in open(f)]
    rows = {(r['task'], r['model'], r['cond'], r.get('spec', 'text')): r for r in rows}.values()
    # 基础设施故障（网关断连、返回体缺字段、沙箱出错）不是模型失败，按口径剔除而不是算挂
    bad = [r for r in rows if any('error' in h for h in r['hist'])]
    rows = [r for r in rows if r not in bad]
    print(f'剔除基础设施故障 {len(bad)} 组，剩 {len(rows)} 组参与统计')
    models = sorted({r['model'] for r in rows}); conds = ['none', 'page', 'multi', 'graph', 'oracle']

    print(f'== 修复通过率：首轮 -> 末轮（{len(rows)} 组）==')
    print(f"{'模型':20s} {'描述':6s} " + ' '.join(f'{c:>14s}' for c in conds))
    for m in models:
        for sp in ['text', 'img']:
            cells = []
            for c in conds:
                rs = [r for r in rows if r['model'] == m and r['cond'] == c and r.get('spec', 'text') == sp]
                if not rs: cells.append(f'{"-":>14s}'); continue
                cells.append(f"{sum(r['first'] == 'pass' for r in rs)}->{sum(r['final'] == 'pass' for r in rs)}/{len(rs)}".rjust(14))
            print(f'{m:20s} {sp:6s} ' + ' '.join(cells))

    print('\n== 合并所有模型 ==')
    for sp in ['text', 'img']:
        for c in conds:
            rs = [r for r in rows if r['cond'] == c and r.get('spec', 'text') == sp]
            if not rs: continue
            fi = sum(r['first'] == 'pass' for r in rs); fn = sum(r['final'] == 'pass' for r in rs)
            print(f'  描述={sp:5s} 反馈={c:6s}  首轮 {fi}/{len(rs)} = {fi / len(rs):.1%}   末轮 {fn}/{len(rs)} = {fn / len(rs):.1%}')

    print('\n== 有没有参考图对「救回来」的影响 ==')
    for sp in ['text', 'img']:
        for c in ['page', 'multi', 'graph', 'oracle']:
            rs = [r for r in rows if r['cond'] == c and r.get('spec', 'text') == sp and r['first'] == 'fail']
            if rs: print(f"  描述={sp:5s} 反馈={c:6s}  救回 {sum(r['final'] == 'pass' for r in rs)}/{len(rs)}")

    print('\n== 自我修正的净效果（首轮挂的里面，后面救回来多少）==')
    for c in ['page', 'multi', 'graph', 'oracle']:
        rs = [r for r in rows if r['cond'] == c and r['first'] == 'fail']
        if rs: print(f'  {c:6s} {sum(r["final"] == "pass" for r in rs)}/{len(rs)} = {sum(r["final"] == "pass" for r in rs) / len(rs):.1%}')
    rs = [r for r in rows if r['cond'] == 'none']
    print(f"  （对照）无反馈一次成型的通过率 {sum(r['final'] == 'pass' for r in rs)}/{len(rs)}")

    print('\n== 每道题的难度（所有模型所有条件合并）==')
    per = collections.Counter(); tot = collections.Counter()
    for r in rows: tot[r['task']] += 1; per[r['task']] += r['final'] == 'pass'
    for t in sorted(tot, key=lambda t: per[t] / tot[t]):
        print(f'  {t:24s} {per[t]:3d}/{tot[t]:<3d} = {per[t] / tot[t]:.0%}')


if __name__ == '__main__':
    (judge if sys.argv[1:2] == ['judge'] else solve)()

