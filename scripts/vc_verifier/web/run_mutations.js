// run_mutations.js —— 应用变异 → 跑探针 → 套冻结阈值 → 汇总判别力
//   node run_mutations.js            全跑
//   node run_mutations.js F1 P3      只跑指定几个
const fs = require('fs'), path = require('path');
const { run } = require('./probe.js');
const { verify } = require('./verify.js');
const MUT = require(process.env.MUT_FILE || './mutants.js');

const HERE = __dirname, REF = path.join(HERE, 'tasks/ref'), WORK = path.join(HERE, 'out/' + (process.env.OUT_TAG === 'hacks' ? 'hack' : 'mut')), RES = path.join(HERE, 'out/' + (process.env.OUT_TAG || 'results') + '.json');

function build(m) {
  const dir = path.join(WORK, m.id);
  fs.rmSync(dir, { recursive: true, force: true });
  fs.mkdirSync(dir, { recursive: true });
  const files = {};
  for (const f of fs.readdirSync(REF)) files[f] = fs.readFileSync(path.join(REF, f), 'utf8');

  // 准入条件 1：每条 search 片段必须在目标文件里唯一出现
  for (const [f, s, r] of (m.edits || [])) {
    const n = files[f].split(s).length - 1;
    if (n !== 1) throw new Error(`${m.id}: edit on ${f} matched ${n} times, need exactly 1 -> ${JSON.stringify(s.slice(0, 60))}`);
    files[f] = files[f].replace(s, r);
  }
  // 类名重命名：只能改 HTML 的 class="..." 里的 token 和 CSS 的 .name 选择器。
  //   第一版用的是全文正则，把 role="tablist" 一起改掉了 —— 那不是等价重写，是真的破坏 ARIA。
  if (m.rename) {
    const map = m.rename;
    let hit = 0;
    files['index.html'] = files['index.html'].replace(/class="([^"]*)"/g, (all, v) =>
      'class="' + v.split(/\s+/).map(t => (map[t] ? (hit++, map[t]) : t)).join(' ') + '"');
    for (const f of Object.keys(files)) {
      if (!f.endsWith('.css')) continue;
      for (const [a, b] of Object.entries(map)) {
        const re = new RegExp('\\.' + a + '(?![\\w-])', 'g');
        const c = files[f].match(re); if (c) hit += c.length;
        files[f] = files[f].replace(re, '.' + b);
      }
    }
    if (!hit) throw new Error(`${m.id}: rename matched nothing`);
  }
  if (m.minifyHtml) files['index.html'] = files['index.html']
    .replace(/>\s+</g, '><').replace(/\n\s+/g, '\n').replace(/<!--[\s\S]*?-->/g, '');
  for (const [f, c] of Object.entries(files)) fs.writeFileSync(path.join(dir, f), c);
  return dir;
}

(async () => {
  const only = process.argv.slice(2);
  const list = only.length ? MUT.filter(m => only.some(o => m.id.startsWith(o))) : MUT;
  const out = [];
  const T0 = Date.now();
  for (const m of list) {
    let dir, rep, vr, err = null;
    const t = Date.now();
    try { dir = build(m); rep = await run(dir, path.join(WORK, m.id + '.json')); vr = verify(rep); }
    catch (e) { err = String(e.message || e); }
    const row = { id: m.id, holdout: !!m.holdout, should_fail: m.fail, expect: m.expect, why: m.why,
      err, judged_fail: err ? null : !vr.pass, layers: err ? null : vr.layers,
      detail: err ? null : vr.detail, ms: Date.now() - t };
    row.correct = err ? null : (row.judged_fail === m.fail);
    out.push(row);
    console.log([m.id, m.fail ? '该挂' : '不该挂', err ? 'ERR:' + err.slice(0, 80) : (row.judged_fail ? '挂@' + vr.layers.join('+') : '过'), row.correct === null ? '?' : (row.correct ? '✔' : '✘'), row.ms + 'ms'].join('  '));
  }
  const tot = Date.now() - T0;
  fs.writeFileSync(RES, JSON.stringify({ ms: tot, rows: out }, null, 1));
  const ok = out.filter(r => r.correct === true).length;
  console.log(`\n合计 ${ok}/${out.length}  耗时 ${(tot / 1000).toFixed(1)}s  平均 ${(tot / out.length / 1000).toFixed(1)}s/个`);
})();

