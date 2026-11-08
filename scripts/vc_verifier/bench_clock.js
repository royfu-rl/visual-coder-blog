// 确定性对照：同一个「用真实时钟+Math.random」的动画页，截两次看是否逐字节一致
//   A 组：直接截（无控制）  B 组：Playwright clock.install + pauseAt + runFor + 注入种子 Math.random
//   实测坑：只 install 不 pauseAt 仍然 3/3 不一致（load 耗时 113~432ms 漏进 performance.now）
const {chromium} = require('playwright-core'); const http = require('http'), fs = require('fs'), path = require('path'), crypto = require('crypto');
const CHROME = '/root/.cache/puppeteer/chrome/linux64-148.0.7778.97/chrome-linux64/chrome';
const srv = http.createServer((q, r) => { const p = path.join(__dirname, q.url.split('?')[0]); fs.readFile(p, (e, b) => { if (e) { r.writeHead(404); return r.end(); } r.writeHead(200, {'content-type': p.endsWith('.html') ? 'text/html' : 'text/javascript'}); r.end(b); }); }).listen(0);
const h = b => crypto.createHash('md5').update(b).digest('hex').slice(0, 8);
(async () => {
  const url = `http://127.0.0.1:${srv.address().port}/scene/anim.html`;
  const br = await chromium.launch({executablePath: CHROME, args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']});
  const shot = async (ctrl) => {
    const ctx = await br.newContext({viewport: {width: 512, height: 384}, deviceScaleFactor: 1}); const pg = await ctx.newPage();
    if (ctrl) {
      await pg.addInitScript(() => { let s = 42; Math.random = () => (s = (s * 16807) % 2147483647) / 2147483647; });
      await pg.clock.install({time: new Date('2026-01-01T00:00:00Z')});
      await pg.clock.pauseAt(new Date('2026-01-01T00:00:01Z'));   // 关键：install 后时钟仍按真实时间走，必须 pauseAt 冻结，否则页面加载耗时会漏进动画
    }
    await pg.goto(url); await pg.waitForSelector('canvas');
    if (ctrl) await pg.clock.runFor(1500); else await pg.waitForTimeout(1500);   // 动画推进 1.5s
    const b = await pg.locator('canvas').screenshot(); await ctx.close(); return h(b);
  };
  const N = +(process.argv[2] || 3); const A = [], B = [];
  for (let i = 0; i < N; i++) A.push(await shot(false));
  for (let i = 0; i < N; i++) B.push(await shot(true));
  console.log(JSON.stringify({uncontrolled_md5: A, uncontrolled_unique: new Set(A).size, controlled_md5: B, controlled_unique: new Set(B).size}));
  await br.close(); srv.close();
})();

