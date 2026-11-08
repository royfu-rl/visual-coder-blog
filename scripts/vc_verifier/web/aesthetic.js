// aesthetic.js —— 审美维度里「可程序化那一半」的确定性探针
//   node aesthetic.js <page_dir> <out.json>
// 只读 computed style 与几何，不做像素比较，不调 VLM。
// 设计原则：先测量参考页，再定阈值。不预设「4px 栅格」这类教条。
const fs = require('fs'), path = require('path');
const puppeteer = require('puppeteer-core');

const CHROME = '/root/.cache/puppeteer/chrome/linux64-148.0.7778.97/chrome-linux64/chrome';
const ORIGIN = 'http://vc.sandbox';
const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.json': 'application/json' };
const VIEWPORTS = [{ w: 375, h: 667 }, { w: 1440, h: 900 }];

const DETERMINISM = `(() => {
  Math.random = (s => () => (s = (s * 16807) % 2147483647) / 2147483647)(42);
  const FIXED = 1767225600000; const RealDate = Date;
  window.Date = class extends RealDate { constructor(...a){ super(...(a.length ? a : [FIXED])); } static now(){ return FIXED; } };
  window.Date.parse = RealDate.parse; window.Date.UTC = RealDate.UTC;
})();`;

// ============ 页面内测量 ============
function measureAesthetic() {
  // ---- 小工具 ----
  const srgbToLin = c => (c /= 255) <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  const relLum = ([r, g, b]) => 0.2126 * srgbToLin(r) + 0.7152 * srgbToLin(g) + 0.0722 * srgbToLin(b);
  const contrast = (a, b) => { const l1 = relLum(a), l2 = relLum(b); const hi = Math.max(l1, l2), lo = Math.min(l1, l2); return (hi + 0.05) / (lo + 0.05); };
  const parseRGB = s => { const m = /rgba?\(([^)]+)\)/.exec(s || ''); if (!m) return null; const p = m[1].split(/[,\s/]+/).filter(Boolean).map(Number); return { rgb: [p[0], p[1], p[2]], a: p.length > 3 ? p[3] : 1 }; };
  // sRGB -> OKLab -> OKLCH（色相/色度，用于「配色关系」而不是「像素相似」）
  function oklch([R, G, B]) {
    const r = srgbToLin(R), g = srgbToLin(G), b = srgbToLin(B);
    const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
    const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
    const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
    const L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s;
    const A = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s;
    const Bb = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s;
    const C = Math.hypot(A, Bb);
    let H = Math.atan2(Bb, A) * 180 / Math.PI; if (H < 0) H += 360;
    return { L: +L.toFixed(4), C: +C.toFixed(4), H: +H.toFixed(1) };
  }
  const entropy = counts => { const n = counts.reduce((a, b) => a + b, 0); if (!n) return 0; let e = 0; for (const c of counts) { if (!c) continue; const p = c / n; e -= p * Math.log2(p); } return +e.toFixed(3); };
  const cv = arr => { if (arr.length < 2) return 0; const m = arr.reduce((a, b) => a + b, 0) / arr.length; if (!m) return 0; const v = arr.reduce((a, b) => a + (b - m) ** 2, 0) / arr.length; return +(Math.sqrt(v) / m).toFixed(4); };

  const vw = window.innerWidth, vh = window.innerHeight;
  const els = [...document.querySelectorAll('body *')];

  // ---- 收集可见元素的 computed style ----
  const vis = [];
  for (const e of els) {
    const st = getComputedStyle(e);
    if (st.display === 'none' || st.visibility === 'hidden' || +st.opacity === 0) continue;
    const r = e.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    if (r.left < -1000) continue; // .skip 式离屏
    vis.push({ e, st, r });
  }

  // ================= 1 排版 =================
  const fsizes = new Map(), families = new Map(), weights = new Map();
  const textNodes = [];
  for (const { e, st, r } of vis) {
    const own = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1);
    const fs = Math.round(parseFloat(st.fontSize) * 10) / 10;
    if (own) {
      fsizes.set(fs, (fsizes.get(fs) || 0) + 1);
      const fam = st.fontFamily.split(',')[0].replace(/["']/g, '').trim();
      families.set(fam, (families.get(fam) || 0) + 1);
      weights.set(st.fontWeight, (weights.get(st.fontWeight) || 0) + 1);
      const lh = st.lineHeight === 'normal' ? 1.2 * fs : parseFloat(st.lineHeight);
      // 行长：CJK 按 1em、拉丁按 0.5em 估平均字宽（CJK 全角，否则行长会被高估一倍）
      const txt = [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim();
      const cjk = (txt.match(/[\u3000-\u9fff\uff00-\uffef]/g) || []).length;
      const avgEm = txt.length ? (cjk * 1.0 + (txt.length - cjk) * 0.5) / txt.length : 0.5;
      // 每行字符数不可能超过总字符数：容器宽但文本短时，widthCh 会被高估（参考页上曾算出 200ch）
      const capacity = r.width / (fs * avgEm);
      textNodes.push({ tag: e.tagName.toLowerCase(), fs, lhRatio: +(lh / fs).toFixed(3), widthCh: +Math.min(capacity, txt.length).toFixed(1), chars: txt.length });
    }
  }
  const sizeList = [...fsizes.keys()].sort((a, b) => a - b);
  // 等比尺度一致性：相邻字号比值的变异系数。越小越像一套 modular scale
  const ratios = []; for (let i = 1; i < sizeList.length; i++) ratios.push(+(sizeList[i] / sizeList[i - 1]).toFixed(4));
  // 视觉层级单调性：h1..h6 的中位字号必须单调不增，且都 >= 正文
  const hMed = {};
  for (let lv = 1; lv <= 6; lv++) {
    const a = vis.filter(x => x.e.tagName === 'H' + lv).map(x => Math.round(parseFloat(x.st.fontSize) * 10) / 10).sort((a, b) => a - b);
    if (a.length) hMed['h' + lv] = a[Math.floor(a.length / 2)];
  }
  const hKeys = Object.keys(hMed);
  let hierViolations = 0;
  for (let i = 1; i < hKeys.length; i++) if (hMed[hKeys[i]] > hMed[hKeys[i - 1]] + 0.05) hierViolations++;
  const bodyFs = Math.round(parseFloat(getComputedStyle(document.body).fontSize) * 10) / 10;
  for (const k of hKeys) if (hMed[k] < bodyFs - 0.05) hierViolations++;

  const paras = textNodes.filter(t => t.chars >= 20);
  const lhBad = paras.filter(t => t.lhRatio < 1.35 || t.lhRatio > 1.8).length;
  const lineLenBad = paras.filter(t => t.widthCh > 95 || t.widthCh < 18).length;
  // 行长的主信号用最大值：单段 150ch 就是缺陷，计数法会被「只有一段超长」稀释
  const lineLenMax = paras.length ? Math.max(...paras.map(t => t.widthCh)) : 0;

  // ================= 2 颜色 =================
  const fgCount = new Map(), bgCount = new Map(), allColors = new Map();
  const contrasts = [];
  for (const { e, st, r } of vis) {
    const own = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1);
    const fg = parseRGB(st.color);
    if (own && fg && fg.a > 0.1) {
      fgCount.set(st.color, (fgCount.get(st.color) || 0) + 1);
      allColors.set(st.color, (allColors.get(st.color) || 0) + 1);
      // 向上找第一个不透明背景
      let node = e, bg = null;
      while (node && node !== document.documentElement) {
        const b = parseRGB(getComputedStyle(node).backgroundColor);
        if (b && b.a > 0.9) { bg = b.rgb; break; }
        node = node.parentElement;
      }
      if (!bg) bg = parseRGB(getComputedStyle(document.body).backgroundColor)?.rgb || [255, 255, 255];
      const fsz = parseFloat(st.fontSize), wt = +st.fontWeight || 400;
      const large = fsz >= 24 || (fsz >= 18.66 && wt >= 700);
      contrasts.push({ ratio: +contrast(fg.rgb, bg).toFixed(2), need: large ? 3 : 4.5 });
    }
    const bb = parseRGB(st.backgroundColor);
    if (bb && bb.a > 0.1 && r.width * r.height > 400) {
      bgCount.set(st.backgroundColor, (bgCount.get(st.backgroundColor) || 0) + 1);
      allColors.set(st.backgroundColor, (allColors.get(st.backgroundColor) || 0) + 1);
    }
  }
  const contrastFails = contrasts.filter(c => c.ratio < c.need).length;
  const contrastMin = contrasts.length ? Math.min(...contrasts.map(c => c.ratio)) : null;

  // 色相聚类：只统计「有色」的颜色（C >= 0.03），色相按 15 度分箱
  const chroma = [...allColors.entries()].map(([c, n]) => { const p = parseRGB(c); return p ? { ...oklch(p.rgb), n } : null; }).filter(Boolean);
  const hued = chroma.filter(x => x.C >= 0.03);
  const hueBins = new Map();
  for (const x of hued) { const b = Math.floor(x.H / 15); hueBins.set(b, (hueBins.get(b) || 0) + x.n); }
  // 相邻分箱合并成「色相家族」
  const bins = [...hueBins.keys()].sort((a, b) => a - b);
  let hueFamilies = 0; for (let i = 0; i < bins.length; i++) if (i === 0 || bins[i] - bins[i - 1] > 1) hueFamilies++;
  const hueEntropy = entropy([...hueBins.values()]);
  // 导出实际色相分箱（15 度一箱的箱号），批次级集中度要用取值本身，不能只用家族数
  const hueBinList = [...hueBins.keys()].sort((a, b) => a - b).map(b => b * 15);
  const neutralRatio = +((chroma.length - hued.length) / Math.max(1, chroma.length)).toFixed(3);

  // ================= 3 间距节奏 =================
  const spacings = [];
  for (const { st } of vis) {
    for (const k of ['marginTop', 'marginBottom', 'marginLeft', 'marginRight', 'paddingTop', 'paddingBottom', 'paddingLeft', 'paddingRight', 'rowGap', 'columnGap']) {
      const v = parseFloat(st[k]); if (Number.isFinite(v) && v > 0.5 && v < 400) spacings.push(Math.round(v * 10) / 10);
    }
  }
  // 自动找基数：取使「是其倍数的占比」最大的 base，不预设
  const baseFit = {};
  for (const base of [2, 4, 6, 8, 10, 12, 16]) {
    const hit = spacings.filter(v => Math.abs(v / base - Math.round(v / base)) < 0.06).length;
    baseFit[base] = +(hit / Math.max(1, spacings.length)).toFixed(3);
  }
  const bestBase = Object.entries(baseFit).sort((a, b) => b[1] - a[1] || b[0] - a[0])[0];
  const spacingVals = [...new Set(spacings)].sort((a, b) => a - b);

  const radii = [];
  for (const { st } of vis) { const v = parseFloat(st.borderTopLeftRadius); if (Number.isFinite(v) && v > 0.5) radii.push(Math.round(v * 10) / 10); }

  // ================= 4 栅格对齐 =================
  // 只看「块级、宽度 > 视口 20%」的元素左边界：这些才构成版面的垂线
  const lefts = vis.filter(x => x.r.width > vw * 0.2).map(x => Math.round(x.r.left));
  const leftBins = new Map(); for (const l of lefts) { const k = Math.round(l / 4) * 4; leftBins.set(k, (leftBins.get(k) || 0) + 1); }
  const sortedLeft = [...leftBins.entries()].sort((a, b) => b[1] - a[1]);
  const top2Share = +(sortedLeft.slice(0, 2).reduce((a, b) => a + b[1], 0) / Math.max(1, lefts.length)).toFixed(3);
  const top3Share = +(sortedLeft.slice(0, 3).reduce((a, b) => a + b[1], 0) / Math.max(1, lefts.length)).toFixed(3);
  // 对齐残差：以出现最多的 3 条垂线为基准，每个块到最近垂线的距离；取中位数与「2px 内占比」
  const anchors = sortedLeft.slice(0, 3).map(x => x[0]);
  const resid = lefts.map(l => Math.min(...anchors.map(a => Math.abs(l - a)))).sort((a, b) => a - b);
  const alignResidMed = resid.length ? resid[Math.floor(resid.length / 2)] : 0;
  const alignWithin2 = +(resid.filter(r => r <= 2).length / Math.max(1, resid.length)).toFixed(3);

  // ================= 5 留白 =================
  // 墨水覆盖率的几何近似：有不透明背景或有自有文本的元素面积并集 / 文档面积（按行扫描近似）
  const doc = document.scrollingElement || document.documentElement;
  const docH = doc.scrollHeight;
  const boxes = [];
  for (const { e, st, r } of vis) {
    const bb = parseRGB(st.backgroundColor);
    const own = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1);
    const painted = (bb && bb.a > 0.1 && !(bb.rgb[0] === 255 && bb.rgb[1] === 255 && bb.rgb[2] === 255)) || own || e.tagName === 'IMG' || e.tagName === 'SVG';
    if (!painted) continue;
    const y = r.top + window.scrollY;
    boxes.push([Math.max(0, r.left), Math.max(0, y), Math.min(vw, r.right), Math.min(docH, y + r.height)]);
  }
  // 行扫描：每 8px 一行，算该行被覆盖的水平区间并集
  let inkArea = 0;
  for (let y = 0; y < docH; y += 8) {
    const segs = boxes.filter(b => b[1] <= y && b[3] > y).map(b => [b[0], b[2]]).sort((a, b) => a[0] - b[0]);
    let cur = -1, covered = 0;
    for (const [a, b] of segs) { const s = Math.max(a, cur); if (b > s) { covered += b - s; cur = b; } }
    inkArea += covered * 8;
  }
  const inkRatio = +(inkArea / Math.max(1, vw * docH)).toFixed(3);

  // ================= 6 「AI 味」已知 tell（只能查具名特征，不是分布度量）=================
  const cssText = [...document.styleSheets].map(ss => { try { return [...ss.cssRules].map(r => r.cssText).join('\n'); } catch (e) { return ''; } }).join('\n');
  const inlineStyle = [...document.querySelectorAll('[style]')].map(e => e.getAttribute('style')).join(';');
  const allCss = cssText + ';' + inlineStyle;
  const famSet = new Set([...families.keys()].map(f => f.toLowerCase()));
  const tells = {
    // 字体 tell：Anthropic 博客点名 Inter
    font_inter: famSet.has('inter') || /font-family[^;]*inter/i.test(allCss),
    font_common_ai: [...famSet].filter(f => ['inter', 'space grotesk', 'poppins', 'montserrat', 'dm sans', 'plus jakarta sans'].includes(f)).length,
    // 紫渐变 tell：找 linear-gradient 里色相落在 265~310 的颜色
    gradient_count: (allCss.match(/linear-gradient|radial-gradient|conic-gradient/g) || []).length,
    purple_gradient: 0,
    // 白卡 + 紫渐变组合
    white_card_count: [...bgCount.entries()].filter(([c]) => { const p = parseRGB(c); return p && p.rgb[0] > 248 && p.rgb[1] > 248 && p.rgb[2] > 248; }).reduce((a, b) => a + b[1], 0),
  };
  for (const m of allCss.match(/(linear|radial|conic)-gradient\([^)]*\)/g) || []) {
    for (const h of m.match(/#[0-9a-fA-F]{6}|rgba?\([^)]*\)/g) || []) {
      let rgb = null;
      if (h[0] === '#') rgb = [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
      else { const p = parseRGB(h); if (p) rgb = p.rgb; }
      if (!rgb) continue;
      const o = oklch(rgb);
      if (o.C >= 0.05 && o.H >= 265 && o.H <= 310) { tells.purple_gradient++; break; }
    }
  }

  return {
    vw, vh, docH, nVisible: vis.length,
    type: {
      sizeCount: sizeList.length, sizes: sizeList, scaleRatioCV: cv(ratios),
      familyCount: families.size, families: [...families.keys()], weightCount: weights.size,
      hMedian: hMed, hierViolations, bodyFs,
      paraCount: paras.length, lineHeightBad: lhBad, lineLenBad, lineLenMax,
    },
    color: {
      fgCount: fgCount.size, bgCount: bgCount.size, totalColors: allColors.size,
      contrastSamples: contrasts.length, contrastFails, contrastMin,
      hueFamilies, hueEntropy, neutralRatio, hueBins: hueBinList,
    },
    spacing: {
      nValues: spacings.length, distinct: spacingVals.length, values: spacingVals,
      baseFit, bestBase: +bestBase[0], bestBaseShare: bestBase[1],
      radiusDistinct: [...new Set(radii)].length, radii: [...new Set(radii)].sort((a, b) => a - b),
    },
    grid: { nBlocks: lefts.length, distinctLefts: leftBins.size, top2Share, top3Share, alignResidMed, alignWithin2 },
    whitespace: { inkRatio },
    tells,
  };
}

// ============ 跑 ============
async function run(pageDir, outPath) {
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: 'shell',
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--use-gl=angle', '--use-angle=swiftshader', '--font-render-hinting=none', '--force-color-profile=srgb', '--disable-lcd-text'],
  });
  const report = { viewports: {} };
  try {
    for (const vp of VIEWPORTS) {
      const page = await browser.newPage();
      await page.setViewport({ width: vp.w, height: vp.h, deviceScaleFactor: 1 });
      await page.evaluateOnNewDocument(DETERMINISM);
      await page.setRequestInterception(true);
      page.on('request', req => {
        const u = new URL(req.url());
        if (u.origin !== ORIGIN) return req.abort();
        const rel = decodeURIComponent(u.pathname) === '/' ? '/index.html' : decodeURIComponent(u.pathname);
        const fp = path.join(pageDir, rel.replace(/^\/+/, ''));
        if (!fp.startsWith(pageDir) || !fs.existsSync(fp)) return req.respond({ status: 404, contentType: 'text/plain', body: 'nf' });
        req.respond({ status: 200, contentType: MIME[path.extname(fp)] || 'application/octet-stream', body: fs.readFileSync(fp) });
      });
      await page.goto(ORIGIN + '/index.html', { waitUntil: 'load', timeout: 30000 });
      await new Promise(r => setTimeout(r, 150));
      report.viewports[vp.w] = await page.evaluate(measureAesthetic);
      await page.close();
    }
  } finally { await browser.close(); }
  if (outPath) fs.writeFileSync(outPath, JSON.stringify(report, null, 1));
  return report;
}

module.exports = { run };
if (require.main === module) {
  const [dir, out] = process.argv.slice(2);
  run(path.resolve(dir), out ? path.resolve(out) : null).then(r => console.log(JSON.stringify(r, null, 1))).catch(e => { console.error(e); process.exit(1); });
}

