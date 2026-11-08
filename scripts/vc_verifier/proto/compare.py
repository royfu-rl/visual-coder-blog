"""python3 compare.py <task_dir>
对一个任务目录：先跑参考解 ref.html 定下相机和体素网格，再在同一组相机/网格下跑每个候选解，
输出四类信号，看哪类能把「对的」和「错的」分开：
  page   只看页面自带相机的一张截图（最常见的 2D verifier）
  mv     verifier 自己摆 9 个相机的剪影 IoU（多视角）
  vox    按颜色分的体素 IoU（3D 占据，和用什么几何类无关）
  naive  按 API 名字数物体（「SphereGeometry 恰好 3 个」这种断言）
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).parent


def probe(page, out, ref=None):
    cmd = ['node', str(HERE / 'harness.js'), str(page), str(out)] + ([str(ref)] if ref else [])
    subprocess.run(cmd, check=True, capture_output=True, timeout=180)
    return json.load(open(out / 'probe.json'))


def img(d, kind, i):
    return np.asarray(Image.open(d / f'{kind}_{i}.png').convert('RGB'), dtype=np.float32)


def iou(a, b):
    return (a & b).sum() / max((a | b).sum(), 1)


def snap(vox, palette, tol=60):
    """候选体素颜色就近归到参考调色板（RGB 距离 < tol），轻微调色不算错，换色仍然算错"""
    rgb = lambda h: np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)])
    pal = {p: rgb(p) for p in palette}
    def near(h):
        if not h or h in pal: return h
        p, d = min(((p, np.linalg.norm(v - rgb(h))) for p, v in pal.items()), key=lambda x: x[1])
        return p if d < tol else h
    cache = {h: near(h) for h in set(vox)}
    return [cache[h] for h in vox]


def score(ref_dir, ref, c_dir, c):
    page = 1 - np.abs(img(ref_dir, 'rgb', 0) - img(c_dir, 'rgb', 0)).mean() / 255
    rng = range(1, len(ref['views']) + 1)
    masks = [iou(img(ref_dir, 'mask', i)[..., 0] > 127, img(c_dir, 'mask', i)[..., 0] > 127) for i in rng]
    faces = [iou(img(ref_dir, 'face', i)[..., 0] > 127, img(c_dir, 'face', i)[..., 0] > 127) for i in rng]
    rv, cv = np.array(ref['vox']), np.array(snap(c['vox'], set(ref['vox']) - {''}))
    vox = {col: round(float(iou(rv == col, cv == col)), 3) for col in sorted(set(ref['vox']) - {''})}
    # 「按 API 名字数物体」式的朴素断言：几何类型多重集必须和参考完全一致
    gt = lambda d: sorted(m['geo'] for m in d['meshes'])
    naive = gt(ref) == gt(c)
    return dict(page=round(float(page), 3), mv_mean=round(float(np.mean(masks)), 3), mv_min=round(float(min(masks)), 3),
                face_min=round(float(min(faces)), 3),
                vox=vox, naive_pass=naive, errors=c['errors'])


def main(task):
    task = Path(task); runs = HERE / 'runs' / task.name
    ref_dir = runs / 'ref'; ref = probe(task / 'ref.html', ref_dir)
    rows = {}
    for page in sorted(task.glob('*.html')):
        out = runs / page.stem
        c = ref if page.stem == 'ref' else probe(page, out, ref_dir / 'probe.json')
        rows[page.stem] = score(ref_dir, ref, out, c)
        print(page.stem, json.dumps(rows[page.stem], ensure_ascii=False))
    json.dump(rows, open(runs / 'scores.json', 'w'), indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main(sys.argv[1])

