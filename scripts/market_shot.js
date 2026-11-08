// market_demos.py verify 之后跑：对「原站被脚本拒绝」或「没拿到封面」的条目，
// 用真浏览器打开原站——能打开就标 browser_ok；封面缺失就截一张首屏当封面（shot_ok）。
// 用法：NODE_PATH=<含 puppeteer-core 的 node_modules> node scripts/market_shot.js
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const STATUS = path.join(ROOT, 'middle_processing/market/demos_verify.json');
const POSTERS = path.join(ROOT, 'market/posters');
const CHROME = '/root/.cache/puppeteer/chrome/linux64-148.0.7778.97/chrome-linux64/chrome';

(async () => {
  const st = JSON.parse(fs.readFileSync(STATUS, 'utf8'));
  const todo = Object.entries(st).filter(([, v]) => !v.page_ok || !['ok', 'shot'].includes(v.img));
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: 'new',
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--hide-scrollbars',
      '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist',
      '--proxy-server=http://oversea-squid1.jp.txyun:11080'],
  });
  for (const [key, v] of todo) {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0 Safari/537.36');
    let code = 0;
    try {
      const resp = await page.goto(v.url, { waitUntil: 'networkidle2', timeout: 45000 });
      code = resp ? resp.status() : 0;
    } catch (e) { code = String(e.message).slice(0, 40); }
    v.browser_code = code;
    v.browser_ok = typeof code === 'number' && code > 0 && code < 400;
    v.page_ok = v.page_ok || v.browser_ok;
    if (v.browser_ok && !['ok', 'shot'].includes(v.img)) {
      await new Promise(r => setTimeout(r, 5000));   // 等 WebGL 场景 / 首屏动画
      await page.screenshot({ path: path.join(POSTERS, key + '.jpg'), type: 'jpeg', quality: 80 });
      v.shot_ok = true;
      v.img = 'shot';
    }
    console.log(key, code, v.browser_ok ? 'OK' : 'FAIL', v.shot_ok ? 'shot' : '', v.title);
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(STATUS, JSON.stringify(st, null, 1));
})();

