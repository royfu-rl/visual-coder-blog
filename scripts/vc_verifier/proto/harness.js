// node harness.js <page.html> <outdir> [ref_views.json]
//   打开一个 agent 产出的 three.js 页面，冻结时钟，读场景图，按 verifier 自己的相机多视角重渲。
//   ref_views.json 给定时用它的相机（来自参考解），保证候选解和参考解在同一组相机下比较。
const fs = require('fs'), path = require('path');
const puppeteer = require('puppeteer-core');

const CHROME = '/root/.cache/puppeteer/chrome/linux64-148.0.7778.97/chrome-linux64/chrome';
const HERE = __dirname;
const THREE_REAL = fs.readFileSync(path.join(HERE, 'node_modules/three/build/three.module.js'));
// 经典 <script> 的 UMD 构建：模型不一定用 ES 模块，harness 覆盖不全会把正常解判成执行失败
const THREE_UMD = fs.readFileSync(path.join(HERE, 'node_modules/three/build/three.js'));
const W = 320, PAGE_URL = 'http://vc.sandbox/index.html';

// 冻结时钟：rAF 只在 harness 调 __vcStep 时执行，时间按固定步长前进 → 同一页面每次渲染逐像素一致
const CLOCK = `(() => {
  // 捕获场景：three 的 Scene 和 WebGLRenderer 构造时都会向 __THREE_DEVTOOLS__ 派发 observe 事件，
  // 所以不管页面怎么引入 three（CDN、打包、压缩）都能抓到，不需要页面配合暴露任何全局变量。
  const vc = (window.__vc = { scene: null, camera: null, renderer: null, renders: 0, offscreen: 0, scenes: [] });
  const bus = new EventTarget(); window.__THREE_DEVTOOLS__ = bus;
  bus.addEventListener('observe', e => {
    const o = e.detail; if (!o) return;
    if (o.isScene) vc.scenes.push(o);
    if (o.domElement && o.getContext && typeof o.render === 'function') {
      const orig = o.render.bind(o);
      o.render = (s, c) => {
        // 只认「用户真正看得到的那块画布」：必须挂在文档里、有实际尺寸、没被隐藏。
        // 否则页面可以另起一个离屏 renderer 渲染一个正确场景来骗过 verifier（实测可行，见 11 节）。
        const e = o.domElement, st = e.isConnected ? getComputedStyle(e) : null;
        const shown = !!st && e.getBoundingClientRect().width > 1 && st.visibility !== 'hidden' && +st.opacity > 0.01;
        if (!vc.busy) { vc.offscreen += shown ? 0 : 1;
          if (shown) Object.assign(vc, { scene: s, camera: c, renderer: o, renders: vc.renders + 1 }); }
        return orig(s, c);
      };
    }
  });
  let t = 0, q = [];
  performance.now = () => t; Date.now = () => 1.7e12 + t;
  window.requestAnimationFrame = cb => q.push(cb);
  window.__vcStep = (n, dt) => { for (let i = 0; i < n; i++) { t += dt; const c = q; q = []; c.forEach(f => f(t)); } };
  Math.random = (s => () => (s = (s * 16807) % 2147483647) / 2147483647)(42);
})();`;

// 在页面里执行：读场景图 + 多视角渲染（普通 / 剪影两种）
function probe(ref, size) {
  let views = ref && ref.views, grid = ref && ref.grid;
  // 开放边界边数：只被一个三角面用到的边。闭合实体为 0，破洞 / 开口面片 > 0。
  // 这是拓扑量，不随洞的大小衰减，所以能抓住全局 IoU 淹没掉的小破洞。
  function openEdges(g) {
    const pos = g.attributes.position, idx = g.index;
    const n = idx ? idx.count : pos.count, key = new Map();
    const vid = i => {
      const j = idx ? idx.getX(i) : i;
      const q = v => (Math.round(v * 1e4) / 1e4 + 0).toFixed(4);   // +0 把 -0 归一成 0，否则接缝处会被当成两个点
      return `${q(pos.getX(j))},${q(pos.getY(j))},${q(pos.getZ(j))}`;
    };
    for (let t = 0; t + 2 < n; t += 3) {
      const a = vid(t), b = vid(t + 1), c = vid(t + 2);
      for (const [u, v] of [[a, b], [b, c], [c, a]]) {
        if (u === v) continue;
        const k = u < v ? u + '|' + v : v + '|' + u;
        key.set(k, (key.get(k) || 0) + 1);
      }
    }
    let o = 0; key.forEach(v => { if (v === 1) o++; });
    return o;
  }

  const { T, scene, renderer } = window.__vc;
  const meshes = [], lights = [];
  scene.updateMatrixWorld(true);
  scene.traverseVisible(o => {
    if (o.isLight) lights.push(o.type);
    if (!o.isMesh) return;
    const b = new T.Box3().setFromObject(o), s = b.getSize(new T.Vector3());
    const m = Array.isArray(o.material) ? o.material[0] : o.material;
    meshes.push({ name: o.name, geo: o.geometry.type, verts: o.geometry.attributes.position.count, open: openEdges(o.geometry),
      min: b.min.toArray(), max: b.max.toArray(), size: s.toArray(), color: m.color ? '#' + m.color.getHexString() : null });
  });
  const box = new T.Box3().setFromObject(scene), c = box.getCenter(new T.Vector3()), r = box.getSize(new T.Vector3()).length() / 2;
  // 没给相机就以本场景包围盒定一组：8 个方位角 × 仰角 15° + 1 个俯视
  views = views || [...[0, 45, 90, 135, 180, 225, 270, 315].map(a => [a, 15]), [0, 85]].map(([az, el]) => {
    const A = az * Math.PI / 180, E = el * Math.PI / 180, d = r * 3.2;
    return { pos: [c.x + d * Math.cos(E) * Math.sin(A), c.y + d * Math.sin(E), c.z + d * Math.cos(E) * Math.cos(A)], target: c.toArray() };
  });
  window.__vc.busy = true;
  const keep = { bg: scene.background, ov: scene.overrideMaterial, w: renderer.domElement.width, h: renderer.domElement.height, pr: renderer.getPixelRatio() };
  renderer.setPixelRatio(1); renderer.setSize(size, size, false);
  // 两种剪影：双面只看外轮廓；单面会把朝外的面之外的地方露出背景，所以能看见破洞和反面的片
  const white = new T.MeshBasicMaterial({ color: 0xffffff, side: T.DoubleSide });
  const whiteF = new T.MeshBasicMaterial({ color: 0xffffff, side: T.FrontSide });
  const pageCam = window.__vc.camera.clone(); pageCam.aspect = 1; pageCam.updateProjectionMatrix();
  const shots = [null, ...views].map(v => {
    let cam = pageCam;
    if (v) { cam = new T.PerspectiveCamera(40, 1, 0.01, 1000);
      cam.position.fromArray(v.pos); cam.lookAt(new T.Vector3().fromArray(v.target)); cam.updateMatrixWorld(); }
    scene.background = new T.Color(0x808080); scene.overrideMaterial = null;
    renderer.render(scene, cam); const rgb = renderer.domElement.toDataURL();
    scene.background = new T.Color(0x000000); scene.overrideMaterial = white;
    renderer.render(scene, cam); const mask = renderer.domElement.toDataURL();
    scene.overrideMaterial = whiteF;
    renderer.render(scene, cam); const face = renderer.domElement.toDataURL();
    return { rgb, mask, face };
  });
  Object.assign(scene, { background: keep.bg, overrideMaterial: keep.ov });
  const N = 48;
  grid = grid || (() => { const g = box.clone().expandByScalar(r * 0.05); return { min: g.min.toArray(), max: g.max.toArray() }; })();
  const gmin = new T.Vector3().fromArray(grid.min), gs = new T.Vector3().fromArray(grid.max).sub(gmin).divideScalar(N);
  const vox = new Array(N * N * N).fill(''), hits = new Array(N * N * N).fill(0), cells = [];
  const rc = new T.Raycaster(), dir = new T.Vector3(0, 0, 1);
  scene.traverseVisible(o => {
    if (!o.isMesh) return;
    const mine = []; cells.push(mine);
    // 不封闭的面（开口锥、单片平面、破壳）没有「内部」，射线奇偶判内外会给出任意结果：
    // 实测中一个开口灯罩的包围盒与参考几乎重合，按色体素 IoU 却只有 0.017。
    // 这类网格改成记录表面经过的体素。
    const isOpen = openEdges(o.geometry) > 0;
    const mats = [].concat(o.material), side = mats.map(m => m.side); mats.forEach(m => m.side = T.DoubleSide);
    const col = mats[0].color ? mats[0].color.getHexString() : 'x';
    for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) {
      const x = gmin.x + (i + .5) * gs.x, y = gmin.y + (j + .5) * gs.y;
      rc.set(new T.Vector3(x, y, gmin.z - 1), dir);
      const zs = rc.intersectObject(o, false).map(h => h.point.z);
      const mark = k => { if (k < 0 || k >= N) return; const q = i + N * (j + N * k); vox[q] = col; hits[q]++; mine.push(q); };
      if (isOpen) { for (const z0 of zs) mark(Math.floor((z0 - gmin.z) / gs.z)); }
      else for (let k = 0; k < N; k++) {
        const z = gmin.z + (k + .5) * gs.z;
        if (zs.filter(v => v < z).length % 2) mark(k);
      }
    }
    mats.forEach((m, n) => m.side = side[n]);
  });
  renderer.setPixelRatio(keep.pr); renderer.setSize(keep.w / keep.pr, keep.h / keep.pr, false);
  window.__vc.busy = false;
  // 互相穿插：被两个以上 mesh 同时占据的体素占比。参考解本身可能有合理的接缝重叠，所以比的是和参考的差
  const occ = hits.filter(h => h > 0).length, inter = hits.filter(h => h > 1).length;
  const overlap = occ ? inter / occ : 0;
  // 两两穿插：共享体素占较小那个部件体积的比例，取最大。全局比率会被大部件稀释，两两不会
  let pairMax = 0, pairWho = null;
  const sets = cells.map(c => new Set(c));
  for (let a = 0; a < cells.length; a++) for (let b = a + 1; b < cells.length; b++) {
    const small = cells[a].length < cells[b].length ? a : b, big = small === a ? b : a;
    if (cells[small].length < 16) continue;   // 细到只占十几个体素的部件，比例没意义
    let sh = 0; for (const q of cells[small]) if (sets[big].has(q)) sh++;
    const f = sh / cells[small].length;
    if (f > pairMax) { pairMax = f; pairWho = [meshes[a] && meshes[a].geo, meshes[b] && meshes[b].geo, cells[small].length]; }
  }

  // 绘制顺序闪烁：把 renderOrder 反过来再渲一次，比较像素。共面重叠会在这里暴露出来
  window.__vc.busy = true;
  const cam0 = new T.PerspectiveCamera(40, 1, 0.01, 1000);
  cam0.position.fromArray(views[0].pos); cam0.lookAt(new T.Vector3().fromArray(views[0].target)); cam0.updateMatrixWorld();
  renderer.setPixelRatio(1); renderer.setSize(size, size, false);
  scene.background = new T.Color(0x808080); scene.overrideMaterial = null;
  const grab = () => { renderer.render(scene, cam0); const c = document.createElement('canvas');
    c.width = c.height = size; c.getContext('2d').drawImage(renderer.domElement, 0, 0);
    return c.getContext('2d').getImageData(0, 0, size, size).data; };
  const a0 = grab();
  const ord = []; let n = 0;
  scene.traverseVisible(o => { if (o.isMesh) { ord.push([o, o.renderOrder]); o.renderOrder = -(n++); } });
  const a1 = grab();
  ord.forEach(([o, r]) => o.renderOrder = r);
  let flicker = 0;
  for (let q = 0; q < a0.length; q += 4) if (Math.abs(a0[q] - a1[q]) + Math.abs(a0[q + 1] - a1[q + 1]) + Math.abs(a0[q + 2] - a1[q + 2]) > 24) flicker++;
  Object.assign(scene, { background: keep.bg, overrideMaterial: keep.ov });
  renderer.setPixelRatio(keep.pr); renderer.setSize(keep.w / keep.pr, keep.h / keep.pr, false);
  window.__vc.busy = false;

  // 渲染器自己的计数器：绘制调用、三角面、几何体与贴图实例。拿到渲染器就能直接读，成本为零。
  // 对应「同一个形状被重复加载成几百个实例」「贴图没复用」这类错误，剪影和体素都看不见。
  const ri = renderer.info;
  const counters = { calls: ri.render.calls, tris: ri.render.triangles,
                     geometries: ri.memory.geometries, textures: ri.memory.textures };

  return { meshes, lights, views, grid, vox, counters, overlap: Math.round(overlap * 1e4) / 1e4, pair_overlap: Math.round(pairMax * 1e4) / 1e4, pair_who: pairWho, flicker, shots };
}

async function run(page, outdir, refViews) {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new',
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage(); await p.setViewport({ width: 640, height: 480 });
  const errors = [];
  p.on('pageerror', e => errors.push(e.message));
  p.on('console', m => process.env.VC_DEBUG && console.log('console:', m.text()));
  p.on('requestfailed', q => process.env.VC_DEBUG && console.log('failed:', q.url()));
  await p.setRequestInterception(true);
  p.on('request', q => {
    const u = q.url(); if (process.env.VC_DEBUG) console.log('req:', u);
    const js = body => q.respond({ contentType: 'text/javascript', headers: { 'Access-Control-Allow-Origin': '*' }, body });
    // 路径不要写死：模型会从 unpkg、jsdelivr、cdnjs、skypack 等各种地方引库，路径结构各不相同。
    // 只按文件名判，模块版给 ES 构建，经典脚本给 UMD 构建。
    if (/(^|\/)three\.module(\.min)?\.js$/.test(u) || /\/__vc\/three\.module\.js$/.test(u)) return js(THREE_REAL);
    if (/(^|\/)three(\.min)?\.js$/.test(u)) return js(THREE_UMD);
    // three 的 addon（控制器、几何工具、加载器等）是正常用法，本地有现成的，别让断网把它们拦成执行失败
    const ad = u.match(/examples\/(?:jsm|js)\/(.+\.js)$/);
    if (ad) {
      const f = path.join(HERE, 'node_modules/three/examples/jsm', ad[1]);
      // 旧版 examples/js 是经典脚本，新版包里已经没有了，直接把 ES 模块喂过去会语法错。
      // 这类 addon 多数只影响交互（相机控制器之类），不影响几何，给个空壳让页面跑下去即可。
      const legacy = /examples\/js\//.test(u);
      if (!legacy && fs.existsSync(f)) return js(fs.readFileSync(f));
      const name = ad[1].split('/').pop().replace(/\.js$/, '');
      return js(`;(function(){var T=window.THREE;if(!T)return;if(!T[${JSON.stringify(name)}])` +
                `T[${JSON.stringify(name)}]=function(){this.update=function(){};this.dispose=function(){};` +
                `this.addEventListener=function(){};this.target={set:function(){}};};})();`);
    }
    if (u === PAGE_URL) return q.respond({ contentType: 'text/html', body: fs.readFileSync(page) });
    q.abort();                                   // 沙箱不出网：除了 three 之外的外链一律拦掉
  });
  await p.evaluateOnNewDocument(CLOCK);
  const t0 = Date.now();
  await p.goto(PAGE_URL, { waitUntil: 'load', timeout: 30000 }).catch(e => errors.push(e.message));
  await p.waitForFunction(() => window.__vc && window.__vc.renders > 0, { timeout: 15000 }).catch(() => errors.push('no render within 15s'));
  await p.evaluate(() => new Promise(ok => {
    const s = document.createElement('script'); s.type = 'module';
    s.textContent = "import * as T from '/__vc/three.module.js'; window.__vc.T = T; window.__vcReady = 1;";
    document.head.appendChild(s); const t = setInterval(() => { if (window.__vcReady) { clearInterval(t); ok(); } }, 10);
  })).catch(e => errors.push('three inject: ' + e.message));
  await p.evaluate(() => window.__vcStep && window.__vcStep(30, 1000 / 60));   // 推进 30 帧（0.5 秒虚拟时间）
  if (process.env.VC_DEBUG) console.log('dbg:', await p.evaluate(() => JSON.stringify({ vc: typeof window.__vc, renders: window.__vc && window.__vc.renders, canv: document.querySelectorAll('canvas').length })));
  const ok = await p.evaluate(() => !!(window.__vc && window.__vc.scene));
  let res = { renders: 0 };
  if (ok) res = await p.evaluate(probe, refViews, W);
  Object.assign(res, await p.evaluate(() => window.__vc ? { renders: window.__vc.renders, offscreen: window.__vc.offscreen } : { renders: 0, offscreen: 0 }));
  await b.close();
  fs.mkdirSync(outdir, { recursive: true });
  (res.shots || []).forEach((s, i) => ['rgb', 'mask', 'face'].forEach(k =>
    fs.writeFileSync(path.join(outdir, `${k}_${i}.png`), Buffer.from(s[k].split(',')[1], 'base64'))));
  delete res.shots;
  Object.assign(res, { errors, ms: Date.now() - t0 });
  fs.writeFileSync(path.join(outdir, 'probe.json'), JSON.stringify(res, null, 1));
  return res;
}

if (require.main === module) {
  const [page, outdir, refv] = process.argv.slice(2);
  run(page, outdir, refv ? JSON.parse(fs.readFileSync(refv)) : undefined)
    .then(r => console.log(JSON.stringify({ meshes: r.meshes && r.meshes.length, renders: r.renders, errors: r.errors, ms: r.ms })));
}
module.exports = { run };

