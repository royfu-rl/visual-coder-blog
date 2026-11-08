// 给 gallery 的每个 three.js demo 拍一张海报截图 -> gallery/posters/<slug>.jpg
// 用法(本机已有 puppeteer chrome 缓存 + node)：
//   1) 起本地服务：  cd <项目根> && python3 -m http.server 8781 --bind 127.0.0.1 &
//   2) 装依赖(一次)：mkdir -p /tmp/cap && cd /tmp/cap && npm i puppeteer-core@23
//   3) 跑：NODE_PATH=/tmp/cap/node_modules SLUGS="tiny-planet,snow-globe,..." \
//          node <项目根>/scripts/capture_posters.js
// three.js 从 unpkg 经海外代理取(见下 --proxy-server)，localhost 绕过；软件 WebGL(SwiftShader)。
// 无头 Chrome + SwiftShader 软件 WebGL；demo 本体走本地 http，three.js 从 unpkg 经海外代理取。
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const CHROME = '/root/.cache/puppeteer/chrome/linux64-148.0.7778.97/chrome-linux64/chrome';
const BASE = process.env.BASE || 'http://127.0.0.1:8781';
const OUT = process.env.OUT || '/mmu_mllm_hdd_4/deep-research/visual-coder-blog/gallery/posters';
const WAIT = parseInt(process.env.WAIT || '4200', 10);   // 等场景建好 + 跑几帧
const SLUGS = (process.env.SLUGS || '').split(',').filter(Boolean);

fs.mkdirSync(OUT, { recursive: true });

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    args: [
      '--no-sandbox', '--disable-dev-shm-usage', '--hide-scrollbars',
      '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
      '--ignore-gpu-blocklist', '--enable-webgl', '--disable-web-security',
      '--proxy-server=http://oversea-squid1.jp.txyun:11080',
      '--proxy-bypass-list=127.0.0.1,localhost',
    ],
  });
  const report = [];
  for (const slug of SLUGS) {
    const page = await browser.newPage();
    await page.setViewport({ width: 1200, height: 900, deviceScaleFactor: 1.5 });
    let err = '';
    page.on('pageerror', e => { err = String(e).slice(0, 160); });
    const url = `${BASE}/gallery/demos/${slug}.html`;
    try {
      await page.goto(url, { waitUntil: 'load', timeout: 45000 });
      // 等到出现一个有尺寸的 canvas（three 已初始化）
      await page.waitForFunction(() => {
        const c = document.querySelector('canvas');
        return c && c.width > 10 && c.height > 10;
      }, { timeout: 40000 }).catch(() => {});
      await new Promise(r => setTimeout(r, WAIT));  // 让场景建好并跑若干帧
      const out = path.join(OUT, `${slug}.jpg`);
      await page.screenshot({ path: out, type: 'jpeg', quality: 84 });
      const kb = Math.round(fs.statSync(out).size / 1024);
      report.push(`  OK   ${slug.padEnd(16)} ${kb}KB${err ? '  (pageerror: ' + err + ')' : ''}`);
    } catch (e) {
      report.push(`  FAIL ${slug.padEnd(16)} ${String(e).slice(0, 120)}`);
    }
    await page.close();
  }
  await browser.close();
  console.log(report.join('\n'));
})();

