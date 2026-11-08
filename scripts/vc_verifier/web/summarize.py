#!/usr/bin/env python3
"""汇总判别力：每类信号单独判对多少 / 分层组合 / 朴素基线（阈值给基线开最优，对自己不开）。"""
import json, os, itertools
H = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(H, 'out/results.json')))['rows']
N = json.load(open(os.path.join(H, 'out/naive.json')))
NAIVE = {r['id']: r for r in N['rows']}

rows = [r for r in R if r['err'] is None]
dev = [r for r in rows if not r['holdout']]
hold = [r for r in rows if r['holdout']]


def acc(pred, subset):
    """pred(row)->bool 判挂；返回 (判对数, 总数, 检出数/该挂数, 误杀数)"""
    ok = sum(1 for r in subset if pred(r) == r['should_fail'])
    f = [r for r in subset if r['should_fail']]
    p = [r for r in subset if not r['should_fail']]
    return ok, len(subset), sum(1 for r in f if pred(r)), len(f), sum(1 for r in p if pred(r)), len(p)


def layer(name):
    return lambda r: len(r['detail'][name]) > 0


def layer_vp(name, vp):
    """只用某个视口的布局信号"""
    def f(r):
        bases = [h.split('=')[0] for h in r['detail'][name]]
        hits = [b for b in bases if ('@' not in b) or b.endswith('@' + vp)]
        # 断点列数判据的名字里自带视口号（breakpoint_375_cols / breakpoint_1440_cols）
        hits = [b for b in hits if not (b.startswith('breakpoint') and vp not in b)]
        return len(hits) > 0
    return f


def sig(key):
    return lambda r: not NAIVE[r['id']][key]


def pixel(t):
    return lambda r: NAIVE[r['id']]['pixelSame'] < t


SIGNALS = [
    ('朴素①单张截图逐像素（1440 首屏，阈值取最优）', None),
    ('朴素②DOM 标签序列一致', sig('tagSame')),
    ('朴素③类名序列一致', sig('clsSame')),
    ('朴素④可见文本一致', sig('textSame')),
    ('W0 正确性（控制台/网络/未捕获）', layer('W0')),
    ('W1 布局与响应式（三视口）', layer('W1')),
    ('  └ W1 只看 1440 单视口', layer_vp('W1', '1440')),
    ('  └ W1 只看 375 单视口', layer_vp('W1', '375')),
    ('W2 可访问性（axe + 语义 + 键盘）', layer('W2')),
    ('  └ W2 只跑 axe 默认规则', lambda r: any(h.startswith('axe_') for h in r['detail']['W2'])),
    ('  └ W2 只看语义/键盘自查项', lambda r: any(not h.startswith('axe_') for h in r['detail']['W2'])),
    ('W3 交互与状态机', layer('W3')),
    ('W4 性能预算', layer('W4')),
]

print('=== 每类信号单独的判别力（开发集 16 / 留出集 6 / 合计 22）===')
print(f"{'信号':46} {'开发16':>8} {'留出6':>7} {'合计':>7} {'检出':>8} {'误杀':>8}")
best_px = None
for name, p in SIGNALS:
    if p is None:
        cand = sorted({NAIVE[r['id']]['pixelSame'] for r in rows} | {1.0000001})
        best = max(((acc(pixel(t), rows)[0], t) for t in cand))
        best_px = best[1]
        p = pixel(best_px)
        name += f' t={best_px}'
    a = acc(p, dev); b = acc(p, hold); c = acc(p, rows)
    print(f'{name:46} {a[0]:>4}/{a[1]:<3} {b[0]:>3}/{b[1]:<3} {c[0]:>3}/{c[1]:<3} {c[2]:>4}/{c[3]:<3} {c[4]:>4}/{c[5]:<3}')

allp = lambda r: not r['judged_fail'] is False
comb = lambda r: r['judged_fail']
a, b, c = acc(comb, dev), acc(comb, hold), acc(comb, rows)
print(f"{'五层组合 W0+W1+W2+W3+W4':46} {a[0]:>4}/{a[1]:<3} {b[0]:>3}/{b[1]:<3} {c[0]:>3}/{c[1]:<3} {c[2]:>4}/{c[3]:<3} {c[4]:>4}/{c[5]:<3}")

print('\n=== 每条变异挂在哪一层（该挂的要有、不该挂的要空）===')
print(f"{'变异':26} {'标签':6} {'集合':5} {'判定':6} {'挂在':14} {'预期':8} 像素相似")
for r in rows:
    print(f"{r['id']:26} {'该挂' if r['should_fail'] else '不该挂':6} {'留出' if r['holdout'] else '开发':5} "
          f"{'挂' if r['judged_fail'] else '过':6} {'+'.join(r['layers']) or '-':14} {'+'.join(r['expect']) or '-':8} {NAIVE[r['id']]['pixelSame']}")

print('\n=== 每层在留出集上的独立贡献（去掉这一层还抓不抓得到）===')
layers = ['W0', 'W1', 'W2', 'W3', 'W4']
for L in layers:
    only = [r['id'] for r in rows if r['should_fail'] and r['layers'] == [L]]
    print(f'  {L}: 唯一抓到的变异 {len(only)} 个 -> {", ".join(only) or "无"}')

print('\n=== 像素信号的噪声地板 ===')
print('  参考页自比自:', N['selfPixel'])
print('  该挂变异里像素完全一致(=1.0)的个数:',
      sum(1 for r in rows if r['should_fail'] and NAIVE[r['id']]['pixelSame'] == 1), '/',
      sum(1 for r in rows if r['should_fail']))
print('  不该挂变异里像素差异最大的:', min((NAIVE[r['id']]['pixelSame'], r['id']) for r in rows if not r['should_fail']))

print('\n耗时: 变异集总 %.1fs，平均 %.1fs/个' % (
    json.load(open(os.path.join(H, 'out/results.json')))['ms'] / 1000,
    json.load(open(os.path.join(H, 'out/results.json')))['ms'] / 1000 / len(R)))

