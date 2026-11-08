// node run_all.js  —— 对参考解和 16 个变异各跑一遍 harness，记录耗时
const { execFileSync } = require('child_process'); const fs = require('fs'), path = require('path');
const HERE = __dirname, cases = JSON.parse(fs.readFileSync(path.join(HERE, 'cases.json')));
const jobs = [{ id: 'ref', page: 'pages/ref.html' }, ...cases.map(c => ({ id: c.id, page: `pages/cases/${c.id}.html` }))];
const t0 = Date.now(); const rows = [];
for (const j of jobs) {
  const t = Date.now();
  const out = execFileSync('node', [path.join(HERE, 'harness.js'), path.join(HERE, j.page), path.join(HERE, 'out', j.id)], { encoding: 'utf8' });
  rows.push({ id: j.id, wall_ms: Date.now() - t, ...JSON.parse(out) });
}
fs.writeFileSync(path.join(HERE, 'out/timing.json'), JSON.stringify(rows, null, 1));
const tot = Date.now() - t0, w = rows.map(r => r.wall_ms).sort((a, b) => a - b);
console.log(`${rows.length} 个页面，总耗时 ${(tot / 1000).toFixed(1)}s，单页中位 ${w[w.length >> 1]}ms，最慢 ${w[w.length - 1]}ms`);
console.log('回读耗时(ms):', rows.map(r => r.readback_ms).join(','));

