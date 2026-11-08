// naive_baselines.js —— 朴素基线：拿来和分层确定性信号对比
//   1 DOM 标签序列一致  2 类名序列一致  3 可见文本一致  4 单张截图逐像素相似度（1440 首屏）
//   node naive_baselines.js  → out/naive.json
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const puppeteer = require('puppeteer-core');
const MUT = require('./mutants.js');
const CHROME = '/root/.cache/puppeteer/chrome/linux64-148.0.7778.97/chrome-linux64/chrome';
const HERE = __dirname, ORIGIN = 'http://vc.sandbox';
const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.svg': 'image/svg+xml' };

async function sigs(browser, dir) {
  const files = new Map();
  for (const f of fs.readdirSync(dir)) if (fs.statSync(path.join(dir, f)).isFile()) files.set('/' + f, fs.readFileSync(path.join(dir, f)));
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
  await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }]);
  await page.setRequestInterception(true);
  page.on('request', r => {
    const u = r.url(); if (!u.startsWith(ORIGIN)) return r.abort('blockedbyclient');
    const b = files.get(new URL(u).pathname);
    if (!b) return r.respond({ status: 404, contentType: 'text/plain', body: 'x' });
    r.respond({ status: 200, contentType: MIME[path.extname(new URL(u).pathname)] || 'application/octet-stream', body: b });
  });
  await page.goto(ORIGIN + '/index.html', { waitUntil: 'load', timeout: 30000 }).catch(() => {});
  await new Promise(r => setTimeout(r, 300));
  const s = await page.evaluate(() => {
    const tags = [], cls = [];
    const walk = e => { tags.push(e.tagName); cls.push(typeof e.className === 'string' ? e.className : ''); for (const c of e.children) walk(c); };
    walk(document.body);
    return { tags: tags.join(','), cls: cls.join(','), text: (document.body.innerText || '').replace(/\s+/g, ' ').trim() };
  }).catch(() => ({ tags: '', cls: '', text: '' }));
  const shot = await page.screenshot({ encoding: 'base64', clip: { x: 0, y: 0, width: 1440, height: 900 } });
  await page.close();
  const h = x => crypto.createHash('sha1').update(x).digest('hex').slice(0, 12);
  return { tagSig: h(s.tags), clsSig: h(s.cls), textSig: h(s.text), shot };
}

(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage', '--font-render-hinting=none', '--force-color-profile=srgb', '--disable-lcd-text', '--enable-unsafe-swiftshader'] });
  const ref = await sigs(browser, path.join(HERE, 'tasks/ref'));
  const rows = [];
  // 像素比较：开一个空白页，用 canvas 算两张图的平均绝对差与「相同像素占比」
  const diffPage = await browser.newPage();
  await diffPage.goto('data:text/html,<body>');
  const diff = (a, b) => diffPage.evaluate(async (a, b) => {
    const ld = s => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.src = 'data:image/png;base64,' + s; });
    const [A, B] = await Promise.all([ld(a), ld(b)]);
    const W = Math.min(A.width, B.width), H = Math.min(A.height, B.height);
    const c = document.createElement('canvas'); c.width = W; c.height = H; const x = c.getContext('2d', { willReadFrequently: true });
    x.drawImage(A, 0, 0); const da = x.getImageData(0, 0, W, H).data;
    x.clearRect(0, 0, W, H); x.drawImage(B, 0, 0); const db = x.getImageData(0, 0, W, H).data;
    let sum = 0, same = 0, n = W * H;
    for (let i = 0; i < da.length; i += 4) {
      const d = Math.abs(da[i] - db[i]) + Math.abs(da[i + 1] - db[i + 1]) + Math.abs(da[i + 2] - db[i + 2]);
      sum += d; if (d <= 6) same++;
    }
    return { mad: +(sum / n / 3).toFixed(3), same: +(same / n).toFixed(4) };
  }, a, b);

  for (const m of MUT) {
    const dir = path.join(HERE, 'out/mut', m.id);
    if (!fs.existsSync(dir)) { console.log(m.id, 'missing'); continue; }
    const s = await sigs(browser, dir);
    const d = await diff(ref.shot, s.shot);
    rows.push({ id: m.id, should_fail: m.fail, holdout: !!m.holdout,
      tagSame: s.tagSig === ref.tagSig, clsSame: s.clsSig === ref.clsSig, textSame: s.textSig === ref.textSig,
      pixelSame: d.same, pixelMad: d.mad });
    console.log([m.id, m.fail ? '该挂' : '不该挂', 'tag=' + (s.tagSig === ref.tagSig), 'cls=' + (s.clsSig === ref.clsSig), 'text=' + (s.textSig === ref.textSig), 'px_same=' + d.same, 'mad=' + d.mad].join('  '));
  }
  // 自比自：参考页重跑一次，给出像素信号的噪声地板
  const ref2 = await sigs(browser, path.join(HERE, 'tasks/ref'));
  const self = await diff(ref.shot, ref2.shot);
  fs.writeFileSync(path.join(HERE, 'out/naive.json'), JSON.stringify({ selfPixel: self, refSigs: { tagSig: ref.tagSig, clsSig: ref.clsSig, textSig: ref.textSig }, rows }, null, 1));
  console.log('\n参考页自比自（噪声地板）:', JSON.stringify(self));
  await browser.close();
})();

