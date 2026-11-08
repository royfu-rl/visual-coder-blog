// run_aes.js —— 应用审美变异 → 跑审美探针 → 套冻结阈值 → 汇总判别力
//   node run_aes.js           全跑
//   node run_aes.js A01 P03   只跑指定几个
// 同时跑一遍功能侧 probe/verify（W0~W4），用来证明「这些审美缺陷不会被现有判据抓到」。
const fs = require('fs'), path = require('path');
const aes = require('./aesthetic.js');
const { verify } = require('./aes_verify.js');
const MUT = require('./aes_mutants.js');
let fnProbe = null, fnVerify = null;
try { fnProbe = require('./probe.js').run; fnVerify = require('./verify.js').verify; } catch (e) { }

const HERE = __dirname, REF = path.join(HERE, 'tasks/ref'), WORK = path.join(HERE, 'out/aes'), RES = path.join(HERE, 'out/aes_results.json');

function build(m) {
  const dir = path.join(WORK, m.id);
  fs.rmSync(dir, { recursive: true, force: true });
  fs.mkdirSync(dir, { recursive: true });
  const files = {};
  for (const f of fs.readdirSync(REF)) files[f] = fs.readFileSync(path.join(REF, f), 'utf8');
  for (const [f, s, r] of (m.edits || [])) {
    const n = files[f].split(s).length - 1;
    if (n !== 1) throw new Error(`${m.id}: edit on ${f} matched ${n} times, need exactly 1 -> ${JSON.stringify(s.slice(0, 60))}`);
    files[f] = files[f].replace(s, r);
  }
  if (m.rename) {
    const map = m.rename; let hit = 0;
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
  const withFn = process.env.WITH_FN === '1';
  const out = [];
  const T0 = Date.now();

  // 先验参考页必须全过
  const refRep = await aes.run(REF, path.join(HERE, 'out/aes_ref.json'));
  const refVr = verify(refRep);
  console.log(`参考页: ${refVr.pass ? '全过 ✔' : '挂@' + refVr.layers.join('+') + ' ✘（阈值不合法，先修阈值）'}  tellHit=${refVr.tellHit}`);

  for (const m of list) {
    let dir, rep, vr, fnr = null, err = null;
    const t = Date.now();
    try {
      dir = build(m);
      rep = await aes.run(dir, path.join(WORK, m.id + '.json'));
      vr = verify(rep);
      if (withFn && fnProbe) { try { fnr = fnVerify(await fnProbe(dir, path.join(WORK, m.id + '.fn.json'))); } catch (e) { fnr = { err: String(e.message || e) }; } }
    } catch (e) { err = String(e.message || e); }
    const row = {
      id: m.id, should_fail: m.fail, expect: m.expect, why: m.why, err,
      judged_fail: err ? null : !vr.pass, layers: err ? null : vr.layers,
      detail: err ? null : vr.detail, tell: err ? null : vr.tell, tellHit: err ? null : vr.tellHit,
      fn_fail: fnr ? (fnr.err ? null : !fnr.pass) : undefined, fn_layers: fnr && !fnr.err ? fnr.layers : undefined,
      ms: Date.now() - t,
    };
    row.correct = err ? null : (row.judged_fail === m.fail);
    out.push(row);
    console.log([m.id.padEnd(20), m.fail ? '该挂  ' : '不该挂',
      err ? 'ERR:' + err.slice(0, 70) : (row.judged_fail ? '挂@' + vr.layers.join('+') : '过   ').padEnd(26),
      row.correct === null ? '?' : (row.correct ? '✔' : '✘'),
      (row.tellHit ? 'tell' : '    '),
      withFn ? (row.fn_fail === null ? 'fn:ERR' : row.fn_fail ? 'fn挂@' + row.fn_layers.join('+') : 'fn过') : '',
      row.ms + 'ms'].join('  '));
  }
  const tot = Date.now() - T0;
  fs.writeFileSync(RES, JSON.stringify({ ms: tot, ref: { pass: refVr.pass, layers: refVr.layers, detail: refVr.detail }, rows: out }, null, 1));
  const ok = out.filter(r => r.correct === true).length;
  const tp = out.filter(r => r.should_fail && r.correct === true).length, nf = out.filter(r => r.should_fail).length;
  const tn = out.filter(r => !r.should_fail && r.correct === true).length, np = out.filter(r => !r.should_fail).length;
  console.log(`\n合计 ${ok}/${out.length}   该挂抓到 ${tp}/${nf}（TNR 判别力）   不该挂判过 ${tn}/${np}（TPR 不误杀）   耗时 ${(tot / 1000).toFixed(1)}s`);
})();

