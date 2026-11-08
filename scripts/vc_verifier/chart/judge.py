#!/usr/bin/env python3
# python3 judge.py  —— 三类信号各自独立判定，阈值见 THRESHOLDS.md（跑之前写死）
import json, os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = json.load(open(f'{HERE}/task.json'))
CASES = json.load(open(f'{HERE}/cases.json'))

# ---- 阈值（与 THRESHOLDS.md 一致，不要在这里随手改）----
S1_REL_TOL = 0.01      # 逐值回读：相对误差上限
S2_CH_TOL = 8          # 像素比对：单通道差异阈值
S2_PIX_FRAC = 0.02     # 像素比对：差异像素占比上限
MIN_FONT_PX = 9        # 可读性：字号下限（本次只报告，不参与三类信号统计）


def load(cid):
    return json.load(open(f'{HERE}/out/{cid}/readback.json'))


def linfit(pts):
    """由 (px, value) 点对拟合 value = a*px + b"""
    n = len(pts)
    sx = sum(p[0] for p in pts); sy = sum(p[1] for p in pts)
    sxx = sum(p[0] * p[0] for p in pts); sxy = sum(p[0] * p[1] for p in pts)
    den = n * sxx - sx * sx
    a = (n * sxy - sx * sy) / den
    return a, (sy - a * sx) / n


def readback_values(d):
    """从绘制几何里逐值回读，返回 {(系列名, 类别名): 数值} 以及诊断信息"""
    ch = d['chartjs']['charts']
    if not ch:
        return None, 'no chart instance'
    c = ch[0]
    ys = c['scales'].get('y')
    xs = c['scales'].get('x')
    if not ys or len(ys['ticks']) < 2:
        return None, 'y scale ticks < 2'
    a, b = linfit([(t['px'], t['value']) for t in ys['ticks']])
    cats = [t['label'] for t in xs['ticks']]
    out = {}
    for ds in c['datasets']:
        if ds['hidden']:
            continue
        for j, el in enumerate(ds['elements']):
            if j >= len(cats):
                break
            top = a * el['y'] + b
            base = a * el['base'] + b if el.get('base') is not None else 0.0
            out[(ds['label'], cats[j])] = top - base
    return out, None


def s1_value(d):
    """S1 逐值回读"""
    got, err = readback_values(d)
    if err:
        return False, err
    want = {}
    for s in TASK['series']:
        for i, cat in enumerate(TASK['categories']):
            want[(s['name'], cat)] = s['data'][i]
    if set(got.keys()) != set(want.keys()):
        miss = set(want) - set(got); extra = set(got) - set(want)
        return False, f'键不匹配 缺{len(miss)} 多{len(extra)}'
    worst, worst_k = 0.0, None
    for k, v in want.items():
        scale = max(abs(x) for x in next(s['data'] for s in TASK['series'] if s['name'] == k[0]))
        rel = abs(got[k] - v) / scale
        if rel > worst:
            worst, worst_k = rel, k
    return worst <= S1_REL_TOL, f'最大相对误差 {worst*100:.2f}% @ {worst_k}'


def s2_pixel(cid):
    """S2 像素比对"""
    ref = Image.open(f'{HERE}/out/ref/shot.png').convert('RGB')
    cur = Image.open(f'{HERE}/out/{cid}/shot.png').convert('RGB')
    if ref.size != cur.size:
        return False, 'size mismatch'
    rp, cp = ref.load(), cur.load()
    w, h = ref.size
    bad = 0
    for y in range(h):
        for x in range(w):
            r1, g1, b1 = rp[x, y]; r2, g2, b2 = cp[x, y]
            if max(abs(r1 - r2), abs(g1 - g2), abs(b1 - b2)) > S2_CH_TOL:
                bad += 1
    frac = bad / (w * h)
    return frac <= S2_PIX_FRAC, f'差异像素 {frac*100:.2f}%'


def s3_struct(d):
    """S3 结构断言"""
    ch = d['chartjs']['charts']
    if not ch:
        return False, 'no chart'
    c = ch[0]
    bad = []
    if c['type'] != TASK['chart_type']:
        bad.append(f"类型 {c['type']}!={TASK['chart_type']}")
    names = [ds['label'] for ds in c['datasets'] if not ds['hidden']]
    leg = [i['text'] for i in (c['legend']['items'] if c['legend'] else [])]
    want_names = [s['name'] for s in TASK['series']]
    if leg != want_names:
        bad.append(f'图例 {leg}!={want_names}')
    if len(names) != len(want_names):
        bad.append(f'系列数 {len(names)}')
    ys = c['scales'].get('y', {})
    if TASK['y_axis_start_zero'] and ys.get('min') != 0:
        bad.append(f"y.min={ys.get('min')}")
    xs = c['scales'].get('x', {})
    cats = [t['label'] for t in xs.get('ticks', [])]
    if cats != TASK['categories']:
        bad.append(f'类别 {cats}')
    yt = ys.get('title', '')
    if not yt or not any(u in yt for u in ['台', '(', '（']):
        bad.append(f'y 轴标题/单位 "{yt}"')
    area = c['area']
    inside = [t for t in d['text']
              if area['left'] <= (t['box'][0] + t['box'][2]) / 2 <= area['right']
              and area['top'] <= (t['box'][1] + t['box'][3]) / 2 <= area['bottom']]
    npts = sum(len(s['data']) for s in TASK['series'])
    if len(inside) != npts:
        bad.append(f'数据标签 {len(inside)}!={npts}')
    return len(bad) == 0, '; '.join(bad) if bad else 'ok'


def readability(d):
    """可读性诊断：字号下限 + 文字重叠（本次只报告）"""
    ts = [t for t in d['text'] if t['fontPx'] > 0]
    small = [t for t in ts if t['fontPx'] < MIN_FONT_PX]
    ov = 0
    for i in range(len(ts)):
        for j in range(i + 1, len(ts)):
            a, b = ts[i]['box'], ts[j]['box']
            ix = min(a[2], b[2]) - max(a[0], b[0])
            iy = min(a[3], b[3]) - max(a[1], b[1])
            if ix > 1 and iy > 1:
                ov += 1
    return len(small), ov


def main():
    rows = []
    for c in CASES:
        d = load(c['id'])
        p1, i1 = s1_value(d)
        p2, i2 = s2_pixel(c['id'])
        p3, i3 = s3_struct(d)
        rows.append(dict(id=c['id'], should_fail=c['should_fail'], why=c['why'],
                         s1=not p1, s1i=i1, s2=not p2, s2i=i2, s3=not p3, s3i=i3))
    ref = load('ref')
    r1, ri1 = s1_value(ref); r3, ri3 = s3_struct(ref)
    small, ov = readability(ref)
    print(f'参考解自比自：S1 {"pass" if r1 else "FAIL"} ({ri1})  S3 {"pass" if r3 else "FAIL"} ({ri3})')
    print(f'参考解可读性：字号 < {MIN_FONT_PX}px 的文本 {small} 条，文字重叠对 {ov} 对\n')
    hdr = f'{"变异":<16}{"标签":<7}{"S1逐值":<9}{"S2像素":<9}{"S3结构":<9}说明'
    print(hdr); print('-' * 100)
    acc = {'s1': 0, 's2': 0, 's3': 0, 'comb': 0}
    for r in rows:
        lab = '该挂' if r['should_fail'] else '不该挂'
        mark = lambda k: ('挂' if r[k] else '过') + ('✓' if r[k] == r['should_fail'] else '✗')
        comb = r['s1'] or r['s3']
        for k in ('s1', 's2', 's3'):
            acc[k] += (r[k] == r['should_fail'])
        acc['comb'] += (comb == r['should_fail'])
        print(f'{r["id"]:<18}{lab:<9}{mark("s1"):<11}{mark("s2"):<11}{mark("s3"):<11}{r["why"]}')
    n = len(rows)
    print('-' * 100)
    print(f'判对数：S1 逐值回读 {acc["s1"]}/{n}  S2 像素比对 {acc["s2"]}/{n}  S3 结构断言 {acc["s3"]}/{n}  S1 或 S3 组合 {acc["comb"]}/{n}')
    json.dump(rows, open(f'{HERE}/out/verdicts.json', 'w'), ensure_ascii=False, indent=1)
    print('\n逐条诊断：')
    for r in rows:
        print(f'  {r["id"]:<18} S1[{r["s1i"]}] S2[{r["s2i"]}] S3[{r["s3i"]}]')


main()

