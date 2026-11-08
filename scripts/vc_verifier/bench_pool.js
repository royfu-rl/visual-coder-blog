// 复用浏览器：B 个 chrome × P 个 page，每个 page 反复做「reload 场景 + 8 视角 jpeg + scene graph」，测稳态吞吐
// 用法: node bench_pool.js B P ROUNDS
const puppeteer = require('puppeteer-core'); const http = require('http'), fs = require('fs'), path = require('path');
const CHROME = '/root/.cache/puppeteer/chrome/linux64-148.0.7778.97/chrome-linux64/chrome';
const ROOT = __dirname; const [B, P, R] = process.argv.slice(2).map(Number);
const srv = http.createServer((q, r) => { const p = path.join(ROOT, q.url === '/' ? 'scene/index.html' : q.url.split('?')[0]);
  fs.readFile(p, (e, b) => { if (e) { r.writeHead(404); return r.end(); } r.writeHead(200, {'content-type': p.endsWith('.html') ? 'text/html' : 'text/javascript'}); r.end(b); }); }).listen(0);
(async () => {
  const url = `http://127.0.0.1:${srv.address().port}/`;
  const args = ['--no-sandbox', '--disable-dev-shm-usage', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'];
  const browsers = await Promise.all([...Array(B)].map(() => puppeteer.launch({executablePath: CHROME, headless: true, args})));
  const t0 = performance.now(); const lat = [];
  await Promise.all(browsers.flatMap(br => [...Array(P)].map(async () => {
    const pg = await br.newPage(); await pg.setViewport({width: 1024, height: 768, deviceScaleFactor: 1});
    for (let i = 0; i < R; i++) { const t = performance.now();
      await pg.goto(url, {waitUntil: 'load'}); await pg.waitForFunction('window.__vc && __vc.ready');
      await pg.evaluate(() => { const r = []; for (let k = 0; k < 8; k++) { __vc.view(k * 45, 25); r.push(__vc.renderer.domElement.toDataURL('image/jpeg', .85).length); } return [r, __vc.graph().length]; });
      lat.push(performance.now() - t); }
  })));
  const wall = (performance.now() - t0) / 1000; lat.sort((a, b) => a - b);
  console.log(`B=${B} P=${P} R=${R} tasks=${lat.length} wall=${wall.toFixed(1)}s throughput=${(lat.length / wall).toFixed(1)} task/s p50=${lat[lat.length >> 1].toFixed(0)}ms p95=${lat[Math.floor(lat.length * .95)].toFixed(0)}ms`);
  await Promise.all(browsers.map(b => b.close())); srv.close();
})();

