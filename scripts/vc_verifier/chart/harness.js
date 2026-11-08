// node harness.js <page.html> <outdir>
//   渲染一个图表页面，做两路「不要求页面配合」的回读，再截图。
//   路 A：图表库内部模型（Chart.js 实例注册表），拿到柱子的像素几何与坐标轴刻度像素位置。
//   路 B：canvas 文本钩子，接管 CanvasRenderingContext2D.fillText/strokeText，
//         记下页面画出来的每一段文字、位置、字号、颜色。这一路与图表库无关，任何 canvas 库都能用。
const fs = require('fs'), path = require('path'), http = require('http');
const puppeteer = require('puppeteer-core');

const CHROME = '/root/.cache/puppeteer/chrome/linux64-148.0.7778.97/chrome-linux64/chrome';
const HERE = __dirname;

// 在页面任何脚本之前注入：文本钩子 + 冻结时钟 + 固定随机
const PRELUDE = `(() => {
  const rec = (window.__vcText = []);
  window.__vcFrame = 0;
  const P = CanvasRenderingContext2D.prototype;
  for (const fn of ['fillText', 'strokeText']) {
    const orig = P[fn];
    P[fn] = function (text, x, y, maxW) {
      try {
        const m = this.measureText(text);
        // 字号从 font 串里取（'12px DejaVu Sans' → 12）
        const fs = parseFloat((this.font.match(/([\\d.]+)px/) || [0, 0])[1]) || 0;
        const asc = m.actualBoundingBoxAscent || fs * 0.8, desc = m.actualBoundingBoxDescent || fs * 0.2;
        let left = x;
        if (this.textAlign === 'center') left = x - m.width / 2;
        else if (this.textAlign === 'right' || this.textAlign === 'end') left = x - m.width;
        // 图表库普遍先 translate/rotate 再在局部坐标里 fillText（Chart.js 的斜刻度标签就是），
        // 所以必须把文字盒的四角过一遍当前变换矩阵，否则所有旋转文本都会堆在原点，重叠检查全是假阳性。
        const M = this.getTransform();
        const pt = (px, py) => [M.a * px + M.c * py + M.e, M.b * px + M.d * py + M.f];
        const cs = [pt(left, y - asc), pt(left + m.width, y - asc), pt(left, y + desc), pt(left + m.width, y + desc)];
        const box = [Math.min(...cs.map(c => c[0])), Math.min(...cs.map(c => c[1])),
                     Math.max(...cs.map(c => c[0])), Math.max(...cs.map(c => c[1]))];
        const [gx, gy] = pt(x, y);
        rec.push({ frame: window.__vcFrame, text: String(text), x: gx, y: gy, fontPx: fs * Math.hypot(M.a, M.b), font: this.font,
          fill: String(this.fillStyle), align: this.textAlign, baseline: this.textBaseline, box });
      } catch (e) {}
      return orig.call(this, text, x, y, maxW);
    };
  }
  // 冻结时钟：动画不会让截图抖动
  let t = 0, q = [];
  performance.now = () => t; Date.now = () => 1.7e12 + t;
  window.requestAnimationFrame = cb => { q.push(cb); return q.length; };
  window.__vcStep = (n, dt) => { for (let i = 0; i < n; i++) { window.__vcFrame++; t += dt; const c = q; q = []; c.forEach(f => { try { f(t); } catch (e) {} }); } };
  Math.random = (s => () => (s = (s * 16807) % 2147483647) / 2147483647)(42);
})();`;

// 在页面里执行：从 Chart.js 实例注册表读几何
function readChartJs() {
  const out = { lib: null, charts: [], errors: [] };
  const C = window.Chart;
  if (!C) { out.errors.push('no Chart global'); return out; }
  out.lib = 'chart.js ' + (C.version || '?');
  const insts = C.instances ? Object.values(C.instances) : [];
  for (const ch of insts) {
    const rec = { type: ch.config.type, datasets: [], scales: {}, legend: null, area: null };
    const ca = ch.chartArea;
    if (ca) rec.area = { left: ca.left, right: ca.right, top: ca.top, bottom: ca.bottom };
    for (const [id, sc] of Object.entries(ch.scales || {})) {
      const ticks = (sc.ticks || []).map((t, i) => ({ value: t.value, label: String(t.label), px: sc.getPixelForTick(i) }));
      rec.scales[id] = { axis: sc.axis, type: sc.type, min: sc.min, max: sc.max, ticks,
        title: (sc.options && sc.options.title && sc.options.title.display) ? String(sc.options.title.text || '') : '' };
    }
    ch.data.datasets.forEach((ds, i) => {
      const meta = ch.getDatasetMeta(i);
      // 元素的像素几何：柱子是 {x, y, base, width}；点是 {x, y}
      const els = (meta.data || []).map(e => ({ x: e.x, y: e.y, base: e.base, w: e.width,
        skip: !!(e.skip), type: e.constructor && e.constructor.name }));
      rec.datasets.push({ label: ds.label, hidden: !!meta.hidden, elementType: meta.type || meta.dataset && meta.dataset.type,
        configData: ds.data, elements: els, yAxisID: meta.yAxisID || 'y', xAxisID: meta.xAxisID || 'x' });
    });
    if (ch.legend) rec.legend = { display: !!ch.legend.options.display, position: ch.legend.options.position,
      items: (ch.legend.legendItems || []).map(it => ({ text: it.text, hidden: !!it.hidden })) };
    rec.canvas = { w: ch.canvas.width, h: ch.canvas.height };
    out.charts.push(rec);
  }
  return out;
}

// SVG 图表的回读：直接解析 DOM
function readSvg() {
  const svgs = [...document.querySelectorAll('svg')];
  return svgs.map(s => {
    const vb = s.getAttribute('viewBox');
    const bb = s.getBoundingClientRect();
    const node = el => {
      const r = { tag: el.tagName.toLowerCase() };
      for (const a of ['x', 'y', 'width', 'height', 'd', 'fill', 'stroke', 'points', 'cx', 'cy', 'r', 'transform', 'font-size', 'class', 'id'])
        if (el.hasAttribute(a)) r[a] = el.getAttribute(a);
      if (el.tagName.toLowerCase() === 'text') {
        r.text = el.textContent;
        // getBBox() 返回的是「未经 transform 的局部坐标」，旋转过的轴标题会落到负坐标上。
        // 要判重叠和溢出必须用 getBoundingClientRect()（含 transform），再换算回 svg 自己的坐标系。
        try {
          const b = el.getBoundingClientRect(), o = el.ownerSVGElement.getBoundingClientRect();
          r.bbox = [b.left - o.left, b.top - o.top, b.right - o.left, b.bottom - o.top];
          const raw = el.getBBox(); r.bboxLocal = [raw.x, raw.y, raw.x + raw.width, raw.y + raw.height];
        } catch (e) {}
        r.fontPx = parseFloat(getComputedStyle(el).fontSize) || 0;
        r.fillC = getComputedStyle(el).fill;
      }
      if (el.__data__ !== undefined) { try { r.bound = JSON.parse(JSON.stringify(el.__data__)); } catch (e) {} }
      return r;
    };
    return { viewBox: vb, rect: { w: bb.width, h: bb.height },
      hasRaster: !!s.querySelector('image'),
      nodes: [...s.querySelectorAll('rect,path,circle,line,polyline,polygon,text')].map(node) };
  });
}

(async () => {
  const [page_, outDir] = process.argv.slice(2);
  fs.mkdirSync(outDir, { recursive: true });
  const pageSrc = fs.readFileSync(page_);
  // 本地服务：/ 给页面，/lib/* 给图表库。页面不许访问外网。
  const srv = http.createServer((q, r) => {
    if (q.url === '/' || q.url === '/index.html') { r.writeHead(200, { 'content-type': 'text/html' }); return r.end(pageSrc); }
    const m = q.url.match(/^\/lib\/(.+)$/);
    if (m) {
      for (const p of [`node_modules/chart.js/dist/${m[1]}`, `node_modules/echarts/dist/${m[1]}`, `node_modules/d3/dist/${m[1]}`]) {
        const f = path.join(HERE, p);
        if (fs.existsSync(f)) { r.writeHead(200, { 'content-type': 'text/javascript' }); return r.end(fs.readFileSync(f)); }
      }
    }
    r.writeHead(404); r.end();
  }).listen(0);

  const t0 = Date.now();
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: true,
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--use-gl=angle', '--use-angle=swiftshader',
      '--enable-unsafe-swiftshader', '--hide-scrollbars', '--font-render-hinting=none', '--disable-lcd-text'] });
  const pg = await browser.newPage();
  const logs = [];
  pg.on('console', m => { if (m.type() === 'error') logs.push(m.text()); });
  pg.on('pageerror', e => logs.push('pageerror: ' + e.message));
  pg.on('request', req => { if (!req.url().startsWith('http://127.0.0.1')) logs.push('EXTERNAL ' + req.url()); });
  await pg.setViewport({ width: 940, height: 560, deviceScaleFactor: 1 });
  await pg.evaluateOnNewDocument(PRELUDE);
  await pg.goto(`http://127.0.0.1:${srv.address().port}/`, { waitUntil: 'load' });
  await pg.evaluate(() => window.__vcStep(240, 16));         // 推进 240 帧（虚拟 3.84s），保证动画走完再读
  const tRender = Date.now() - t0;

  const t1 = Date.now();
  const data = await pg.evaluate(`(() => { const a = (${readChartJs})(); const b = (${readSvg})();
     const all = window.__vcText;
     // 每次重绘会把所有文字重画一遍，所以按帧分组，只取最后一个画了字的帧，否则文本会跨帧累加
     const last = all.length ? Math.max(...all.map(t => t.frame)) : 0;
     return { chartjs: a, svg: b, text: all.filter(t => t.frame === last), textFrames: new Set(all.map(t => t.frame)).size }; })()`);
  const tRead = Date.now() - t1;

  const t2 = Date.now();
  await pg.screenshot({ path: path.join(outDir, 'shot.png') });
  const tShot = Date.now() - t2;

  data.console = logs;
  data.timing = { render_ms: tRender, readback_ms: tRead, screenshot_ms: tShot };
  fs.writeFileSync(path.join(outDir, 'readback.json'), JSON.stringify(data, null, 1));
  await browser.close(); srv.close();
  console.log(JSON.stringify({ page: path.basename(page_), ...data.timing,
    charts: data.chartjs.charts.length, texts: data.text.length, errors: logs.length }));
})();

