// aes_concentration.js —— 「AI 味」的批次级指标：样式集中度指纹
//   node aes_concentration.js <glob-dir-with-html> [out.json]
// 为什么不是 per-page：AI 味的数学表述是「每个输出都挺原创，但彼此雷同」，
// 它只能在 N 份产物上定义。本脚本对一批页面算每一类可见样式属性的
//   Shannon 熵 H、归一化熵 H/log2(k)、HHI（赫芬达尔指数）、top1 占比
// 并给出页面级直方图的平均 Jensen-Shannon 距离。
// 只统计「人能看见」的属性，防止 z-index / letter-spacing 这类不可感知维度刷熵。
const fs = require('fs'), path = require('path'), os = require('os');
const aes = require('./aesthetic.js');

const VISIBLE_KEYS = ['fontFamily', 'fontSize', 'hue', 'radius', 'spacing'];

function H(counts) {
  const n = counts.reduce((a, b) => a + b, 0); if (!n) return 0;
  let e = 0; for (const c of counts) { if (!c) continue; const p = c / n; e -= p * Math.log2(p); }
  return e;
}
function HHI(counts) {
  const n = counts.reduce((a, b) => a + b, 0); if (!n) return 1;
  return counts.reduce((a, c) => a + (c / n) ** 2, 0);
}
function jsd(p, q) {
  const keys = new Set([...Object.keys(p), ...Object.keys(q)]);
  const sp = Object.values(p).reduce((a, b) => a + b, 0) || 1;
  const sq = Object.values(q).reduce((a, b) => a + b, 0) || 1;
  let d = 0;
  for (const k of keys) {
    const a = (p[k] || 0) / sp, b = (q[k] || 0) / sq, m = (a + b) / 2;
    if (a > 0) d += a * Math.log2(a / m) / 2;
    if (b > 0) d += b * Math.log2(b / m) / 2;
  }
  return d;
}

// 从一个页面的审美报告里抽出「可见样式属性」的取值集合（用 1440 档）
function featuresOf(rep) {
  const v = rep.viewports['1440'] || Object.values(rep.viewports)[0];
  return {
    fontFamily: v.type.families.map(f => f.toLowerCase()),
    fontSize: v.type.sizes.map(String),
    // 色相按 15 度分箱；中性色单独一类
    // 实际色相分箱（15 度一箱）；中性色占主导时单列一类
    hue: (v.color.hueBins || []).map(h => 'h' + h).concat(v.color.neutralRatio > 0.5 ? ['neutral'] : []),
    radius: v.spacing.radii.map(String),
    spacing: v.spacing.values.map(String),
    _tells: v.tells,
    _nColors: v.color.totalColors,
  };
}

(async () => {
  const dir = path.resolve(process.argv[2]);
  const outPath = process.argv[3] ? path.resolve(process.argv[3]) : null;
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort();
  if (!files.length) { console.error('no html in ' + dir); process.exit(1); }

  const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'aesconc-'));
  const feats = [];
  for (const f of files) {
    // aesthetic.js 以目录为单位服务，所以每页放进独立目录并改名 index.html
    const d = path.join(tmpRoot, path.basename(f, '.html'));
    fs.mkdirSync(d, { recursive: true });
    fs.copyFileSync(path.join(dir, f), path.join(d, 'index.html'));
    // 同目录的资源一并拷（样式表、图片等）
    for (const g of fs.readdirSync(dir)) {
      if (g === f || g.endsWith('.html')) continue;
      const src = path.join(dir, g);
      if (fs.statSync(src).isFile()) fs.copyFileSync(src, path.join(d, g));
    }
    try {
      const rep = await aes.run(d, null);
      feats.push({ file: f, ...featuresOf(rep) });
      process.stdout.write('.');
    } catch (e) { process.stdout.write('x'); feats.push({ file: f, err: String(e.message || e) }); }
  }
  process.stdout.write('\n');
  const ok = feats.filter(x => !x.err);

  const summary = { dir, nPages: files.length, nOk: ok.length, perKey: {}, tells: {} };
  for (const key of VISIBLE_KEYS) {
    // 语料级：每个取值被多少个页面用到
    const docFreq = {};
    for (const x of ok) for (const v of new Set(x[key])) docFreq[v] = (docFreq[v] || 0) + 1;
    const counts = Object.values(docFreq).sort((a, b) => b - a);
    const k = counts.length;
    const h = H(counts);
    // 页面级直方图之间的平均 JS 距离
    let sum = 0, pairs = 0;
    for (let i = 0; i < ok.length; i++) for (let j = i + 1; j < ok.length; j++) {
      const pi = {}, pj = {};
      for (const v of ok[i][key]) pi[v] = (pi[v] || 0) + 1;
      for (const v of ok[j][key]) pj[v] = (pj[v] || 0) + 1;
      sum += jsd(pi, pj); pairs++;
    }
    summary.perKey[key] = {
      distinctValues: k,
      entropy: +h.toFixed(3),
      normEntropy: k > 1 ? +(h / Math.log2(k)).toFixed(3) : 0,
      HHI: +HHI(counts).toFixed(3),
      top1Share: +(counts[0] / ok.length).toFixed(3),
      top1Value: Object.entries(docFreq).sort((a, b) => b[1] - a[1])[0]?.[0],
      meanPairJSD: pairs ? +(sum / pairs).toFixed(3) : 0,
    };
  }
  // tell 命中率
  summary.tells = {
    interShare: +(ok.filter(x => x._tells.font_inter).length / Math.max(1, ok.length)).toFixed(3),
    purpleGradientShare: +(ok.filter(x => x._tells.purple_gradient > 0).length / Math.max(1, ok.length)).toFixed(3),
    anyGradientShare: +(ok.filter(x => x._tells.gradient_count > 0).length / Math.max(1, ok.length)).toFixed(3),
    aiFontShare: +(ok.filter(x => x._tells.font_common_ai > 0).length / Math.max(1, ok.length)).toFixed(3),
  };
  if (outPath) fs.writeFileSync(outPath, JSON.stringify({ summary, feats }, null, 1));
  console.log(JSON.stringify(summary, null, 1));
  fs.rmSync(tmpRoot, { recursive: true, force: true });
})();

