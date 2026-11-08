// probe.js —— Web/DOM 侧确定性探针
//   node probe.js <page_dir> <out.json>
// 做四件事：多视口盒模型读数 / 注入 axe-core / 控制台与网络错误 / 性能读数 + 交互状态机。
// 不做任何像素比较，不调 VLM。
const fs = require('fs'), path = require('path');
const puppeteer = require('puppeteer-core');

const CHROME = '/root/.cache/puppeteer/chrome/linux64-148.0.7778.97/chrome-linux64/chrome';
const HERE = __dirname;
const AXE = fs.readFileSync(path.join(HERE, 'vendor/axe.min.js'), 'utf8');
const ORIGIN = 'http://vc.sandbox';
const VIEWPORTS = [{ w: 375, h: 667 }, { w: 768, h: 1024 }, { w: 1440, h: 900 }];

// 题面钉死的交互元素清单：verifier 只能查这些（信息量 <= problem statement，见 90 节 5）
const SPEC = {
  interactive: ['nav-home', 'nav-pricing', 'nav-docs', 'open-demo', 'toggle-theme',
    'tab-web', 'tab-ios', 'tab-svr', 'email', 'seats', 'submit-btn'],
  // 必须可见且有尺寸的关键元素
  visible: ['hero-title', 'open-demo', 'toggle-theme', 'tabs-title', 'signup-title', 'submit-btn', 'email', 'seats'],
  // 两两不许遮挡的元素（取中心点做命中测试）
  hitTest: ['open-demo', 'toggle-theme', 'tab-web', 'tab-ios', 'tab-svr', 'submit-btn'],
};

const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.json': 'application/json' };

// ---- 确定性注入：固定随机数、固定日期、禁动画（performance.now 保持真实，性能读数要用）----
const DETERMINISM = `(() => {
  Math.random = (s => () => (s = (s * 16807) % 2147483647) / 2147483647)(42);
  const FIXED = 1767225600000; // 2026-01-01T00:00:00Z
  const RealDate = Date;
  window.Date = class extends RealDate { constructor(...a){ super(...(a.length ? a : [FIXED])); } static now(){ return FIXED; } };
  window.Date.parse = RealDate.parse; window.Date.UTC = RealDate.UTC;
  window.__vcLongTasks = []; window.__vcShifts = [];
  try { new PerformanceObserver(l => { for (const e of l.getEntries()) window.__vcLongTasks.push(+e.duration.toFixed(1)); }).observe({ type: 'longtask', buffered: true }); } catch (e) {}
  try { new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__vcShifts.push(+e.value.toFixed(5)); }).observe({ type: 'layout-shift', buffered: true }); } catch (e) {}
  window.__vcRejections = 0;
  window.addEventListener('unhandledrejection', () => { window.__vcRejections++; });
})();`;

// ---- 页面内：盒模型 / 溢出 / 重叠 / 语义结构 ----
function measure(SPEC) {
  const vw = window.innerWidth, vh = window.innerHeight;
  const doc = document.scrollingElement || document.documentElement;
  const R = id => { const e = document.getElementById(id); if (!e) return null; const r = e.getBoundingClientRect(); return { x: +r.x.toFixed(1), y: +r.y.toFixed(1), w: +r.width.toFixed(1), h: +r.height.toFixed(1) }; };

  // 1 横向溢出：标准写法 scrollWidth > clientWidth
  const hOverflow = Math.max(0, doc.scrollWidth - doc.clientWidth);

  // 2 哪些元素越界（右边界超出视口 1px 以上）
  const out = [];
  for (const e of document.querySelectorAll('body *')) {
    const st = getComputedStyle(e);
    if (st.display === 'none' || st.visibility === 'hidden' || st.position === 'fixed') continue;
    const r = e.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    // 左边完全在视口外（经典 .skip 隐藏手法 left:-9999px）不算溢出；只算「有一部分在视口内、另一部分越界」
    if (r.right > vw + 1 || (r.left < -1 && r.right > 0)) out.push({ sel: e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/)[0] : ''), right: +r.right.toFixed(1), left: +r.left.toFixed(1) });
    if (out.length > 40) break;
  }

  // 3 文字截断：内容宽度超过盒子且 overflow 不可见
  const clipped = [];
  for (const e of document.querySelectorAll('h1,h2,h3,p,span,a,button,label,li,td')) {
    const st = getComputedStyle(e);
    if (st.display === 'none') continue;
    if (e.scrollWidth > e.clientWidth + 1 && st.overflowX !== 'visible') clipped.push(e.tagName.toLowerCase() + (e.id ? '#' + e.id : ''));
    if (e.scrollHeight > e.clientHeight + 1 && st.overflowY === 'hidden' && st.display !== 'inline') clipped.push('v:' + e.tagName.toLowerCase() + (e.id ? '#' + e.id : ''));
  }

  // 4 关键元素可见且有尺寸
  const missing = [], zero = [];
  for (const id of SPEC.visible) {
    const e = document.getElementById(id);
    if (!e) { missing.push(id); continue; }
    const r = e.getBoundingClientRect(), st = getComputedStyle(e);
    if (r.width < 1 || r.height < 1 || st.visibility === 'hidden' || +st.opacity < 0.05) zero.push(id);
  }

  // 5 遮挡：中心点命中测试必须命中自己或后代
  const occluded = [];
  for (const id of SPEC.hitTest) {
    const e = document.getElementById(id); if (!e) continue;
    const r = e.getBoundingClientRect(); if (r.width < 1) continue;
    const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    if (cx < 0 || cy < 0 || cx > vw || cy > vh) continue;   // 不在首屏不算
    const hit = document.elementFromPoint(cx, cy);
    if (!hit || !(hit === e || e.contains(hit))) occluded.push({ id, by: hit ? hit.tagName.toLowerCase() + (hit.className && typeof hit.className === 'string' ? '.' + hit.className.trim().split(/\s+/)[0] : '') : null });
  }

  // 6 关键元素两两矩形重叠面积比（文本/按钮不该叠）
  let maxPairOverlap = 0, pairWorst = null;
  const boxes = SPEC.hitTest.concat(['hero-title']).map(id => [id, R(id)]).filter(x => x[1] && x[1].w > 0);
  for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
    const a = boxes[i][1], b = boxes[j][1];
    const ow = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x), oh = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
    if (ow <= 0 || oh <= 0) continue;
    const ratio = (ow * oh) / Math.min(a.w * a.h, b.w * b.h);
    if (ratio > maxPairOverlap) { maxPairOverlap = +ratio.toFixed(3); pairWorst = boxes[i][0] + '|' + boxes[j][0]; }
  }

  // 7 断点行为：卡片分几列（同一 top 的卡片数）
  //   取「主内容里第一个有 >=2 个子元素的列表」的条目做结构化定位。
  //   第一版用的是 .card 类选择器，被 P2_rename_classes 打成误判 —— 判据绝不能绑在表现型类名上。
  const list = [...document.querySelectorAll('main ul, main ol, [role=main] ul, [role=main] ol, #main ul, #main ol')]
    .find(u => u.children.length >= 2);
  const cards = list ? [...list.children].map(e => e.getBoundingClientRect()) : [];
  let cols = 0;
  if (cards.length) { const top = Math.min(...cards.map(r => Math.round(r.top))); cols = cards.filter(r => Math.abs(Math.round(r.top) - top) <= 2).length; }

  // 8 语义结构
  const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(e => +e.tagName[1]);
  let skip = 0; for (let i = 1; i < hs.length; i++) if (hs[i] - hs[i - 1] > 1) skip++;
  const sem = {
    lang: document.documentElement.getAttribute('lang') || null,
    title: (document.title || '').trim(),
    h1: document.querySelectorAll('h1').length,
    headingSkips: skip,
    landmarks: { main: document.querySelectorAll('main,[role=main]').length, nav: document.querySelectorAll('nav,[role=navigation]').length, header: document.querySelectorAll('header,[role=banner]').length },
    imgNoAlt: [...document.querySelectorAll('img')].filter(e => !e.hasAttribute('alt')).length,
    buttonsNoName: [...document.querySelectorAll('button,[role=button]')].filter(e => !(e.textContent || '').trim() && !e.getAttribute('aria-label')).length,
    inputsNoLabel: [...document.querySelectorAll('input:not([type=hidden])')].filter(e => {
      if (e.getAttribute('aria-label') || e.getAttribute('aria-labelledby')) return false;
      return !(e.id && document.querySelector('label[for="' + e.id + '"]'));
    }).length,
    // 交互语义：被当按钮用但不是原生按钮/链接且没有 role+tabindex
    fakeButtons: [...document.querySelectorAll('[onclick], .btn, .btn-ghost')].filter(e => {
      const t = e.tagName.toLowerCase();
      if (t === 'button' || t === 'a' || t === 'input') return false;
      return !(e.getAttribute('role') === 'button' && e.hasAttribute('tabindex'));
    }).map(e => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '')),
    ariaBadRef: [...document.querySelectorAll('[aria-labelledby],[aria-controls],[aria-describedby]')].filter(e =>
      ['aria-labelledby', 'aria-controls', 'aria-describedby'].some(a => (e.getAttribute(a) || '').split(/\s+/).filter(Boolean).some(id => !document.getElementById(id)))).length,
    // 不安全子资源（混合内容代理：绝对 http:// 且不是沙箱源）
    insecureSubresources: [...document.querySelectorAll('[src],[href]')].map(e => e.getAttribute('src') || e.getAttribute('href'))
      .filter(u => u && /^http:\/\//i.test(u) && !u.startsWith('http://vc.sandbox')).length,
  };

  return { vw, vh, scrollWidth: doc.scrollWidth, clientWidth: doc.clientWidth, hOverflow, out, clipped, missing, zero, occluded, maxPairOverlap, pairWorst, cols, sem, rects: Object.fromEntries(SPEC.visible.map(id => [id, R(id)])) };
}

// ---- 页面内：帧间隔 ----
function frames(n) {
  return new Promise(res => {
    const ts = []; let last = performance.now();
    const step = t => { ts.push(+(t - last).toFixed(2)); last = t; if (ts.length < n) requestAnimationFrame(step); else res(ts); };
    requestAnimationFrame(step);
  });
}

async function run(dir, outPath) {
  const t0 = Date.now();
  const files = new Map();
  for (const f of fs.readdirSync(dir)) files.set('/' + f, fs.readFileSync(path.join(dir, f)));

  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: true,
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--font-render-hinting=none',
      '--force-color-profile=srgb', '--disable-lcd-text', '--hide-scrollbars=false',
      '--enable-unsafe-swiftshader', '--disable-features=PaintHolding'],
  });
  const MARK=[]; let _t=Date.now(); const mark=n=>{MARK.push([n,Date.now()-_t]);_t=Date.now();};
  const rep = { dir, marks: MARK, viewports: {}, axe: {}, console: { error: [], warning: [] }, pageerrors: [], rejections: 0, network: { failed: [], bad: [], served: 0, bytes: 0, external: 0 }, perf: {}, interaction: {}, keyboard: {}, ms: 0 };

  const page = await browser.newPage();
  await page.setCacheEnabled(false);
  await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }]);
  await page.evaluateOnNewDocument(DETERMINISM);
  await page.setRequestInterception(true);
  page.on('request', req => {
    const u = req.url();
    if (!u.startsWith(ORIGIN)) { rep.network.external++; return req.abort('blockedbyclient'); }
    const p = new URL(u).pathname;
    const body = files.get(p);
    if (!body) return req.respond({ status: 404, contentType: 'text/plain', body: 'not found' });
    rep.network.served++; rep.network.bytes += body.length;
    req.respond({ status: 200, contentType: MIME[path.extname(p)] || 'application/octet-stream', body });
  });
  page.on('console', m => { const t = m.type(); if (t === 'error') rep.console.error.push(m.text().slice(0, 300)); else if (t === 'warning') rep.console.warning.push(m.text().slice(0, 200)); });
  page.on('pageerror', e => rep.pageerrors.push(String(e.message || e).slice(0, 300)));
  page.on('requestfailed', r => rep.network.failed.push({ url: r.url().slice(0, 160), err: r.failure() && r.failure().errorText }));
  page.on('response', r => { if (r.status() >= 400) rep.network.bad.push({ url: r.url().slice(0, 160), status: r.status() }); });

  // ---- 多视口读数 ----
  for (const v of VIEWPORTS) {
    await page.setViewport({ width: v.w, height: v.h, deviceScaleFactor: 1 });
    await page.goto(ORIGIN + '/index.html', { waitUntil: 'load', timeout: 30000 }).catch(e => rep.pageerrors.push('goto:' + e.message));
    await new Promise(r => setTimeout(r, 250));
    rep.viewports[v.w] = await page.evaluate(measure, SPEC).catch(e => ({ err: String(e) }));
  }

  mark('viewports');
  // ---- 性能读数（在 1440 下）----
  await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
  const cdp = await page.target().createCDPSession();
  await cdp.send('Performance.enable');
  const tNav = Date.now();
  await page.goto(ORIGIN + '/index.html', { waitUntil: 'load', timeout: 30000 }).catch(() => {});
  const loadMs = Date.now() - tNav;
  await new Promise(r => setTimeout(r, 400));
  const m1 = Object.fromEntries((await cdp.send('Performance.getMetrics')).metrics.map(x => [x.name, x.value]));
  const fr = await page.evaluate(frames, 40).catch(() => []);
  // 交互前后的 Layout/RecalcStyle 计数差分 = 一次完整交互脚本引起的重排重绘
  const before = { L: m1.LayoutCount, R: m1.RecalcStyleCount };
  for (const id of ['toggle-theme', 'tab-ios', 'tab-web', 'open-demo', 'close-demo']) {
    await page.evaluate(i => { const e = document.getElementById(i); if (e) e.click(); }, id);
  }
  await new Promise(r => setTimeout(r, 200));
  const m2 = Object.fromEntries((await cdp.send('Performance.getMetrics')).metrics.map(x => [x.name, x.value]));
  const sorted = fr.slice(2).sort((a, b) => a - b);
  rep.perf = {
    loadMs, resources: rep.network.served, bytes: rep.network.bytes,
    longTasks: await page.evaluate(() => window.__vcLongTasks || []),
    cls: +(await page.evaluate(() => (window.__vcShifts || []).reduce((a, b) => a + b, 0))).toFixed(4),
    framesP95: sorted.length ? sorted[Math.floor(sorted.length * 0.95)] : null,
    framesMedian: sorted.length ? sorted[Math.floor(sorted.length / 2)] : null,
    nodes: m2.Nodes, jsHeapMB: +(m2.JSHeapUsedSize / 1048576).toFixed(2),
    layoutDelta: m2.LayoutCount - before.L, recalcDelta: m2.RecalcStyleCount - before.R,
    layoutDurTotal: +(m2.LayoutDuration || 0).toFixed(4),
  };
  rep.rejections = await page.evaluate(() => window.__vcRejections || 0);

  mark('perf');
  // ---- axe-core（浅色 + 深色各跑一遍；主题状态先清干净，否则上一阶段点过的 toggle 会污染）----
  await page.evaluate(() => { try { localStorage.clear(); } catch (e) {} }).catch(() => {});
  await page.goto(ORIGIN + '/index.html', { waitUntil: 'load', timeout: 30000 }).catch(() => {});
  await page.evaluate(AXE);
  const axeRun = () => page.evaluate(async () => {
    const r = await axe.run(document, { resultTypes: ['violations', 'incomplete'], reporter: 'v2' });
    const pick = a => a.map(v => ({ id: v.id, impact: v.impact, tags: v.tags.filter(t => /^wcag|best-practice/.test(t)), n: v.nodes.length }));
    return { v: pick(r.violations), inc: pick(r.incomplete), passes: r.passes ? r.passes.length : null, axeVersion: axe.version };
  }).catch(e => ({ err: String(e), v: [] }));
  const axLight = await axeRun();
  await page.evaluate(() => { const b = document.getElementById('toggle-theme'); if (b) b.click(); }).catch(() => {});
  await new Promise(r => setTimeout(r, 120));
  const axDark = await axeRun();
  await page.evaluate(() => { try { localStorage.clear(); } catch (e) {} }).catch(() => {});
  // 合并：取两套主题的并集（深色下才出现的对比度问题也算问题）
  const merged = new Map();
  for (const v of [...(axLight.v || []), ...(axDark.v || [])]) {
    const prev = merged.get(v.id);
    if (!prev || v.n > prev.n) merged.set(v.id, v);
  }
  const mergedInc = new Map();
  for (const v of [...(axLight.inc || []), ...(axDark.inc || [])]) {
    const prev = mergedInc.get(v.id);
    if (!prev || v.n > prev.n) mergedInc.set(v.id, v);
  }
  const ax = { v: [...merged.values()], inc: [...mergedInc.values()], passes: axLight.passes, axeVersion: axLight.axeVersion,
    light: (axLight.v || []).reduce((a, v) => a + v.n, 0), dark: (axDark.v || []).reduce((a, v) => a + v.n, 0) };
  rep.axe = ax;
  if (ax.v) {
    const imp = { critical: 0, serious: 0, moderate: 0, minor: 0 };
    for (const v of ax.v) imp[v.impact || 'minor'] = (imp[v.impact || 'minor'] || 0) + v.n;
    rep.axe.byImpact = imp;
    rep.axe.total = ax.v.reduce((a, v) => a + v.n, 0);
    rep.axe.wcagViolations = ax.v.filter(v => v.tags.some(t => /^wcag/.test(t))).reduce((a, v) => a + v.n, 0);
    rep.axe.contrast = ax.v.filter(v => v.id === 'color-contrast').reduce((a, v) => a + v.n, 0);
  }

  mark('axe');
  // ---- 键盘可达 ----
  rep.keyboard = await (async () => {
    await page.goto(ORIGIN + '/index.html', { waitUntil: 'load', timeout: 30000 }).catch(() => {});
    await page.evaluate(() => document.body.focus());
    const order = [], seen = new Set();
    for (let i = 0; i < 40; i++) {
      await page.keyboard.press('Tab');
      const info = await page.evaluate(() => {
        const a = document.activeElement; if (!a || a === document.body) return null;
        const st = getComputedStyle(a);
        return { id: a.id || null, tag: a.tagName.toLowerCase(), outline: st.outlineWidth + '/' + st.outlineStyle, shadow: st.boxShadow !== 'none' };
      });
      if (!info) continue;
      const k = info.id || info.tag + ':' + i;
      if (seen.has(k)) break;
      seen.add(k); order.push(info);
    }
    const reached = new Set(order.map(o => o.id).filter(Boolean));
    const unreachable = SPEC.interactive.filter(id => !reached.has(id));
    const noFocusRing = order.filter(o => o.id && (o.outline === '0px/none' || o.outline.startsWith('0px')) && !o.shadow).map(o => o.id);
    return { order: order.map(o => o.id || o.tag), count: order.length, unreachable, noFocusRing };
  })();

  mark('keyboard');
  // ---- 交互状态机 ----
  rep.interaction = await (async () => {
    const res = {};
    const S = async (name, fn) => { try { res[name] = await fn(); } catch (e) { res[name] = { pass: false, err: String(e.message || e).slice(0, 160) }; } };
    const reload = async () => { await page.goto(ORIGIN + '/index.html', { waitUntil: 'load', timeout: 30000 }); await new Promise(r => setTimeout(r, 120)); };

    await S('modal', async () => {
      await reload();
      const before = await page.evaluate(() => document.getElementById('demo-modal') && !document.getElementById('demo-modal').hidden);
      await page.click('#open-demo');
      await new Promise(r => setTimeout(r, 120));
      const opened = await page.evaluate(() => { const m = document.getElementById('demo-modal'); if (!m) return false; const r = m.getBoundingClientRect(); return !m.hidden && r.width > 10 && r.height > 10 && getComputedStyle(m).display !== 'none'; });
      await page.click('#close-demo').catch(() => {});
      await new Promise(r => setTimeout(r, 120));
      const closed = await page.evaluate(() => { const m = document.getElementById('demo-modal'); return !m || m.hidden || getComputedStyle(m).display === 'none'; });
      return { pass: before === false && opened === true && closed === true, before, opened, closed };
    });

    await S('tabs', async () => {
      await reload();
      await page.click('#tab-ios'); await new Promise(r => setTimeout(r, 120));
      const s = await page.evaluate(() => ({
        sel: ['web', 'ios', 'svr'].map(k => document.getElementById('tab-' + k).getAttribute('aria-selected')),
        vis: ['web', 'ios', 'svr'].map(k => { const p = document.getElementById('panel-' + k); return !p.hidden && getComputedStyle(p).display !== 'none'; }),
      }));
      return { pass: s.sel.join() === 'false,true,false' && s.vis.join() === 'false,true,false', ...s };
    });

    await S('formInvalid', async () => {
      await reload();
      await page.evaluate(() => { document.getElementById('email').value = 'not-an-email'; document.getElementById('seats').value = '5'; });
      await page.click('#submit-btn'); await new Promise(r => setTimeout(r, 150));
      const s = await page.evaluate(() => ({
        err: (document.getElementById('email-err').textContent || '').trim().length,
        ok: !document.getElementById('form-ok').hidden,
        native: document.getElementById('email').checkValidity(),
      }));
      return { pass: s.err > 0 && s.ok === false && s.native === false, ...s };
    });

    await S('formValid', async () => {
      await reload();
      await page.evaluate(() => { document.getElementById('email').value = 'ann@corp.com'; document.getElementById('seats').value = '7'; });
      await page.click('#submit-btn'); await new Promise(r => setTimeout(r, 150));
      const s = await page.evaluate(() => ({
        ok: !document.getElementById('form-ok').hidden,
        err: (document.getElementById('email-err').textContent || '').trim().length + (document.getElementById('seats-err').textContent || '').trim().length,
      }));
      return { pass: s.ok === true && s.err === 0, ...s };
    });

    await S('formRange', async () => {
      await reload();
      await page.evaluate(() => { document.getElementById('email').value = 'ann@corp.com'; document.getElementById('seats').value = '9999'; });
      await page.click('#submit-btn'); await new Promise(r => setTimeout(r, 150));
      const s = await page.evaluate(() => ({ err: (document.getElementById('seats-err').textContent || '').trim().length, ok: !document.getElementById('form-ok').hidden }));
      return { pass: s.err > 0 && s.ok === false, ...s };
    });

    await S('themePersist', async () => {
      await page.evaluate(() => { try { localStorage.clear(); } catch (e) {} });
      await reload();
      const snap = () => page.evaluate(() => ({ attr: document.documentElement.dataset.theme || 'light', ls: (() => { try { return localStorage.getItem('orbit-theme'); } catch (e) { return null; } })() }));
      const z = await snap();                                  // 前置：清空存储后必须是浅色
      await page.click('#toggle-theme'); await new Promise(r => setTimeout(r, 120));
      const a = await snap();
      await reload();
      const b = await snap();                                  // 刷新后仍是深色
      await page.click('#toggle-theme'); await new Promise(r => setTimeout(r, 120));
      const c = await snap();                                  // 往返：再点一次要回到浅色
      return { pass: z.attr === 'light' && z.ls === null && a.attr === 'dark' && a.ls === 'dark'
        && b.attr === 'dark' && b.ls === 'dark' && c.attr === 'light' && c.ls === 'light', z, a, b, c };
    });

    await S('route', async () => {
      await reload();
      await page.evaluate(() => { location.hash = '#/pricing'; });
      await new Promise(r => setTimeout(r, 150));
      const s = await page.evaluate(() => ({
        cur: ['home', 'pricing', 'docs'].map(k => document.getElementById('nav-' + k).getAttribute('aria-current')),
        hash: location.hash,
      }));
      return { pass: s.cur.join() === ',page,' && s.hash === '#/pricing', ...s };
    });

    return res;
  })();

  mark('interaction');
  rep.ms = Date.now() - t0;
  await browser.close();
  if (outPath) fs.writeFileSync(outPath, JSON.stringify(rep, null, 1));
  return rep;
}

if (require.main === module) {
  run(process.argv[2], process.argv[3]).then(r => {
    console.log(JSON.stringify({ ms: r.ms, axe: r.axe.total, consoleErr: r.console.error.length, pageerr: r.pageerrors.length, bad404: r.network.bad.length, hOverflow: Object.fromEntries(Object.entries(r.viewports).map(([k, v]) => [k, v.hOverflow])), interaction: Object.fromEntries(Object.entries(r.interaction).map(([k, v]) => [k, v.pass])), kbd: r.keyboard.unreachable, perf: r.perf }, null, 1));
  }).catch(e => { console.error(e); process.exit(1); });
}
module.exports = { run, SPEC, VIEWPORTS };

