#!/usr/bin/env python3
# python3 extras.py —— 两项补充检查的实证：
#   (a) SVG 特有检查：路径可解析、viewBox 合理、无光栅图冒充矢量、逐值回读（矩形高度 → 数值）
#   (b) 可读性检查：文字重叠、溢出绘图区、字号下限
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = json.load(open(f'{HERE}/task.json'))
CATS, Q1 = TASK['categories'], TASK['series'][0]['data']
MIN_FONT_PX = 9


def load(c):
    return json.load(open(f'{HERE}/out/{c}/readback.json'))


def parse_path(d):
    """能否解析：命令字母 + 数字流；返回 (命令数, 坐标数) 或 None"""
    toks = re.findall(r'[MmLlHhVvCcSsQqTtAaZz]|-?\d*\.?\d+(?:e-?\d+)?', d or '')
    if not toks or not re.match(r'[MmLlHhVvCcSsQqTtAaZz]', toks[0]):
        return None
    cmds = sum(1 for t in toks if re.match(r'^[A-Za-z]$', t))
    return cmds, len(toks) - cmds


def svg_checks(cid):
    d = load(cid)
    s = d['svg'][0]
    r = {}
    vb = [float(x) for x in re.split(r'[ ,]+', s['viewBox'].strip())] if s['viewBox'] else None
    r['viewBox'] = s['viewBox']
    # viewBox 与实际渲染尺寸的长宽比偏差 > 1% 就算不合理（会导致整体非等比缩放）
    if vb and vb[2] > 0 and vb[3] > 0:
        ar_vb, ar_px = vb[2] / vb[3], s['rect']['w'] / s['rect']['h']
        r['aspect_ok'] = abs(ar_vb - ar_px) / ar_px < 0.01
        # viewBox 比实际画布小很多 → 内容被放大，等于偷偷降分辨率
        r['viewBox_scale'] = round(s['rect']['w'] / vb[2], 3)
    r['has_raster'] = s['hasRaster']
    paths = [n for n in s['nodes'] if n['tag'] == 'path']
    r['paths'] = len(paths)
    r['paths_parse_ok'] = all(parse_path(p.get('d')) for p in paths)
    # 逐值回读：矩形高度 → 数值。比例尺由两个 y 刻度文本的位置定，不读任何源码常量
    # 刻度位置要用 bboxLocal（SVG 自身坐标系），因为柱子的 height 属性也是自身坐标系；
    # 页面坐标的 bbox 留给重叠/溢出检查用。两者混用会凭空多出一个 viewBox 缩放因子。
    ticks = sorted([(float(n['bboxLocal'][3] + n['bboxLocal'][1]) / 2, float(n['text']))
                    for n in s['nodes'] if n['tag'] == 'text' and re.fullmatch(r'\d+', n['text'] or '')],
                   key=lambda t: t[0])
    bars = [n for n in s['nodes'] if n['tag'] == 'rect']
    r['bars'] = len(bars)
    if len(ticks) >= 2 and bars:
        (y1, v1), (y2, v2) = ticks[0], ticks[-1]
        a = (v2 - v1) / (y2 - y1)
        got = [abs(float(b['height']) * a) for b in bars]
        worst = max(abs(g - v) / max(Q1) for g, v in zip(got, Q1)) if len(got) == len(Q1) else 1.0
        r['readback_worst_rel'] = round(worst * 100, 2)
        r['readback_sample'] = [round(x) for x in got]
    return r


def readability(cid, area=None):
    d = load(cid)
    ch = d['chartjs']['charts']
    if ch:
        ts = [t for t in d['text'] if t['fontPx'] > 0]
        area = ch[0]['area']
    else:
        s = d['svg'][0]
        ts = [{'text': n['text'], 'fontPx': n['fontPx'], 'box': n['bbox']}
              for n in s['nodes'] if n['tag'] == 'text' and n.get('bbox')]
        area = {'left': 0, 'top': 0, 'right': s['rect']['w'], 'bottom': s['rect']['h']}
    small = [t['text'] for t in ts if t['fontPx'] < MIN_FONT_PX]
    ov = []
    for i in range(len(ts)):
        for j in range(i + 1, len(ts)):
            a, b = ts[i]['box'], ts[j]['box']
            if min(a[2], b[2]) - max(a[0], b[0]) > 1 and min(a[3], b[3]) - max(a[1], b[1]) > 1:
                ov.append((ts[i]['text'], ts[j]['text']))
    out = [t['text'] for t in ts
           if t['box'][0] < -1 or t['box'][2] > area['right'] + 1 or t['box'][3] > area['bottom'] + 60]
    return dict(n_text=len(ts), small_font=small, overlap=len(ov), overlap_sample=ov[:3], overflow=out[:5])


print('== SVG 特有检查 ==')
for c in ['x_svg_ref', 'x_svg_bad']:
    print(f'  {c:<12}', json.dumps(svg_checks(c), ensure_ascii=False))
print('\n== 可读性检查 ==')
for c in ['ref', 'x_crowded', 'x_svg_ref', 'x_svg_bad']:
    print(f'  {c:<12}', json.dumps(readability(c), ensure_ascii=False))

