"""统一 verifier 接口：verify(ref_dir, ref, cand_dir, cand) -> {verdict, signals}

分三层，任一层挂即判 fail：
  L0 执行门     页面有没有报错、有没有真的渲染出东西
  L1 多视角剪影  verifier 自己的 9 个相机，双面剪影（外轮廓）与单面剪影（破洞、反面片）各取最差一视角
  L2 体素占据    按颜色分的全局 IoU + 分块最差 IoU（抓局部缺陷）
  L2b 自洽性     整体穿插比例、改变绘制顺序后的像素变化（共面重叠会在这里暴露）
  L3 部件与拓扑  按颜色的体积比与连通块数（抓细长部件）；开放边界边数（抓破洞与开口面片）
阈值在 snowman 上定，在 table 上复验未调（blk 阈值在两任务上扫过 0.5/0.6/0.7，取 0.5）。
"""
import collections
import numpy as np
import compare
from blockiou import blocks
from parts import compare_parts, open_edges_ok

TH = dict(mv_min=0.9, face_min=0.9, vox_main=0.9, vox_other=0.5, blk_min=0.5,
          overlap_margin=0.10, flicker_px=64)
# pair_overlap（两两穿插占较小部件的比例）只当诊断量，不参与判定：
# 48 的体素分辨率下，薄部件会被量化成一层，看起来像被完全包含，参考解自己就是 1.0。


def verify(ref_dir, ref, cand_dir, cand, th=TH):
    sig = compare.score(ref_dir, ref, cand_dir, cand)
    if cand['errors'] or not cand.get('meshes'):
        return dict(verdict='fail', layer='L0', signals=sig)
    main = collections.Counter(c for c in ref['vox'] if c).most_common(1)[0][0]
    bl = blocks(ref['vox'], cand['vox'])
    sig['blk_min'] = round(float(min(bl)), 3)
    if sig['mv_min'] < th['mv_min'] or sig['face_min'] < th['face_min']:
        return dict(verdict='fail', layer='L1', signals=sig)
    sig['overlap'] = cand.get('overlap'); sig['flicker'] = cand.get('flicker')
    # 渲染计数器目前只作诊断，不参与判定：还没有在带标签变异集上量过它的判别力
    if cand.get('counters') and ref.get('counters'):
        sig['counters'] = {k: (ref['counters'][k], cand['counters'][k]) for k in cand['counters']}
    if (cand.get('overlap') or 0) > (ref.get('overlap') or 0) + th['overlap_margin'] or (cand.get('flicker') or 0) > th['flicker_px']:
        return dict(verdict='fail', layer='L2b', signals=sig)
    bad = [c for c, v in sig['vox'].items() if v < (th['vox_main'] if c == main else th['vox_other'])]
    if bad or sig['blk_min'] < th['blk_min']:
        return dict(verdict='fail', layer='L2', signals=sig, bad_colors=bad)
    oe, orow = open_edges_ok(ref, cand)
    sig['open_edges'] = orow
    if not oe:
        return dict(verdict='fail', layer='L3', signals=sig)
    ok, prows = compare_parts(ref['vox'], cand['vox'])
    sig['parts_bad'] = {k: v for k, v in prows.items() if v['vol_ratio'] != 1.0 or v['ref_n'] != v['cand_n']}
    if not ok:
        return dict(verdict='fail', layer='L3', signals=sig)
    return dict(verdict='pass', layer='-', signals=sig)


def probe_and_verify(ref_dir, ref, page, out_dir):
    cand = compare.probe(page, out_dir, ref_dir / 'probe.json')
    return verify(ref_dir, ref, out_dir, cand)

