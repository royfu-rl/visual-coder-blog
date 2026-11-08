// 无头 Chrome + SwiftShader 下的 three.js verifier 实测
// 用法: node bench_threejs.js [W] [H] [N_VIEWS]
const puppeteer = require('puppeteer-core');
const http = require('http'), fs = require('fs'), path = require('path');
const CHROME = '/root/.cache/puppeteer/chrome/linux64-148.0.7778.97/chrome-linux64/chrome';
const ROOT = __dirname, OUT = path.join(ROOT, 'out');
const [W, H, NV] = [+(process.argv[2] || 1024), +(process.argv[3] || 768), +(process.argv[4] || 8)];
const types = {'.html': 'text/html', '.js': 'text/javascript'};
const srv = http.createServer((q, r) => {
  const p = path.join(ROOT, q.url === '/' ? 'scene/index.html' : decodeURIComponent(q.url.split('?')[0]));
  fs.readFile(p, (e, b) => { if (e) { r.writeHead(404); return r.end(); } r.writeHead(200, {'content-type': types[path.extname(p)] || 'application/octet-stream'}); r.end(b); });
}).listen(0);
const ms = t => +(performance.now() - t).toFixed(1);
(async () => {
  const port = srv.address().port, T = {};
  let t = performance.now();
  const browser = await puppeteer.launch({executablePath: CHROME, headless: true,
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--use-gl=angle', '--use-angle=swiftshader',
      '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--hide-scrollbars', '--font-render-hinting=none']});
  T.launch_ms = ms(t);
  const page = await browser.newPage();
  const logs = []; page.on('console', m => logs.push(`[${m.type()}] ${m.text()}`)); page.on('pageerror', e => logs.push('[pageerror] ' + e.message));
  await page.setViewport({width: W, height: H, deviceScaleFactor: 1});
  t = performance.now();
  await page.goto(`http://127.0.0.1:${port}/`, {waitUntil: 'load'});
  await page.waitForFunction('window.__vc && window.__vc.ready', {timeout: 30000});
  T.load_ms = ms(t);
  T.gl = await page.evaluate(() => __vc.gl());
  // 单视角
  t = performance.now();
  await page.screenshot({path: path.join(OUT, 'single.png')});
  T.single_shot_ms = ms(t);
  // 也测 canvas.toDataURL 直读（绕开合成器截图）
  t = performance.now();
  const durl = await page.evaluate(() => { __vc.view(30, 25); return __vc.renderer.domElement.toDataURL('image/png'); });
  T.single_toDataURL_ms = ms(t);
  // 8 视角转台：page.screenshot 路线
  t = performance.now();
  for (let i = 0; i < NV; i++) {
    await page.evaluate(az => __vc.view(az, 25), i * 360 / NV);
    await page.screenshot({path: path.join(OUT, `turn_${i}.png`)});
  }
  T[`turntable_${NV}_screenshot_ms`] = ms(t);
  // 8 视角转台：一次 evaluate 内渲染+toDataURL（更快）
  t = performance.now();
  const urls = await page.evaluate(n => { const r = []; for (let i = 0; i < n; i++) { __vc.view(i * 360 / n, 25); r.push(__vc.renderer.domElement.toDataURL('image/jpeg', .85)); } return r; }, NV);
  T[`turntable_${NV}_inpage_jpeg_ms`] = ms(t);
  urls.forEach((u, i) => fs.writeFileSync(path.join(OUT, `turn_js_${i}.jpg`), Buffer.from(u.split(',')[1], 'base64')));
  // scene graph
  t = performance.now();
  const g = await page.evaluate(() => __vc.graph());
  T.scene_graph_ms = ms(t); T.scene_graph_nodes = g.length;
  fs.writeFileSync(path.join(OUT, 'scene_graph.json'), JSON.stringify(g, null, 1));
  // 确定性：同视角渲两次逐字节比较
  const a = await page.evaluate(() => { __vc.setTime(0); __vc.view(30, 25); return __vc.renderer.domElement.toDataURL('image/png'); });
  const b = await page.evaluate(() => { __vc.setTime(0); __vc.view(30, 25); return __vc.renderer.domElement.toDataURL('image/png'); });
  T.same_view_png_identical = a === b && a === durl;
  T.png_kb = +(fs.statSync(path.join(OUT, 'single.png')).size / 1024).toFixed(1);
  T.console = logs.slice(0, 5);
  await browser.close(); srv.close();
  T.W = W; T.H = H;
  console.log(JSON.stringify(T, null, 1));
})();

