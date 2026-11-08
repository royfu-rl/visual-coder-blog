// verify.js —— 把 probe.js 的读数套上冻结阈值，输出五层判定
//   node verify.js out/ref.json
const fs = require('fs');
const TH = JSON.parse(fs.readFileSync(require('path').join(__dirname, 'thresholds.json'), 'utf8'));

function verify(r) {
  const L = { W0: [], W1: [], W2: [], W3: [], W4: [] };
  const hit = (layer, name, bad, detail) => { if (bad) L[layer].push(detail ? name + '=' + detail : name); };
  const t0 = TH.W0_correctness, t1 = TH.W1_layout, t2 = TH.W2_a11y, t4 = TH.W4_perf;
  const vps = Object.entries(r.viewports || {});
  const anySem = vps.length ? vps[0][1].sem || {} : {};

  // ---- W0 正确性 ----
  hit('W0', 'console_error', (r.console.error || []).length > t0.console_error_max, (r.console.error || []).length);
  hit('W0', 'pageerror', (r.pageerrors || []).length > t0.pageerror_max, (r.pageerrors || []).length);
  hit('W0', 'unhandled_rejection', (r.rejections || 0) > t0.unhandled_rejection_max, r.rejections);
  hit('W0', 'http_4xx5xx', (r.network.bad || []).length > t0.http_status_ge400_max, (r.network.bad || []).length);
  hit('W0', 'request_failed', (r.network.failed || []).length > t0.request_failed_max, (r.network.failed || []).length);
  hit('W0', 'insecure_subresource', (anySem.insecureSubresources || 0) > t0.insecure_subresource_max);

  // ---- W1 布局与响应式（逐视口）----
  for (const [w, v] of vps) {
    if (v.err) { L.W1.push('probe_err@' + w); continue; }
    hit('W1', 'h_overflow@' + w, v.hOverflow > t1.h_overflow_px_max, v.hOverflow);
    hit('W1', 'out_of_viewport@' + w, (v.out || []).length > t1.elements_out_of_viewport_max, (v.out || []).length);
    hit('W1', 'text_clipped@' + w, (v.clipped || []).length > t1.text_clipped_max, (v.clipped || []).join('|'));
    hit('W1', 'missing@' + w, (v.missing || []).length > t1.key_element_missing_max, (v.missing || []).join('|'));
    hit('W1', 'zero_size@' + w, (v.zero || []).length > t1.key_element_zero_size_max, (v.zero || []).join('|'));
    hit('W1', 'occluded@' + w, (v.occluded || []).length > t1.occluded_key_elements_max, (v.occluded || []).map(o => o.id + '<-' + o.by).join('|'));
    hit('W1', 'pair_overlap@' + w, (v.maxPairOverlap || 0) > t1.pair_overlap_ratio_max, v.maxPairOverlap + ':' + v.pairWorst);
  }
  const v375 = r.viewports['375'], v1440 = r.viewports['1440'];
  if (v375) hit('W1', 'breakpoint_375_cols', v375.cols !== t1.cols_at_375, v375.cols);
  if (v1440) hit('W1', 'breakpoint_1440_cols', v1440.cols < t1.cols_at_1440_min, v1440.cols);

  // ---- W2 可访问性 ----
  const ax = r.axe || {};
  const vio = ax.v || [];
  const n = f => vio.filter(f).reduce((a, v) => a + v.n, 0);
  hit('W2', 'axe_critical_serious', n(v => v.impact === 'critical' || v.impact === 'serious') > t2.axe_critical_plus_serious_max, vio.filter(v => v.impact === 'critical' || v.impact === 'serious').map(v => v.id).join('|'));
  hit('W2', 'axe_wcag', n(v => v.tags.some(t => /^wcag/.test(t))) > t2.axe_wcag_tagged_max, vio.filter(v => v.tags.some(t => /^wcag/.test(t))).map(v => v.id).join('|'));
  hit('W2', 'axe_any', n(() => true) > t2.axe_total_max, vio.map(v => v.id + ':' + v.n).join('|'));
  // needs review 也当闸：axe 对渐变背景、图片背景、伪元素内容、半透明前景一律不判 violation 而落 incomplete，
  // 只看 violations 的话「把不合格文字藏起来再用伪元素画回屏幕」可以直接绕过（见 hacks.js K4）。
  const inc = (ax.inc || []).filter(v => (t2.axe_incomplete_gate_rules || []).includes(v.id));
  hit('W2', 'axe_incomplete', inc.reduce((a, v) => a + v.n, 0) > (t2.axe_incomplete_max || 0), inc.map(v => v.id + ':' + v.n).join('|'));
  hit('W2', 'html_lang', t2.html_lang_required && !anySem.lang);
  hit('W2', 'h1_count', anySem.h1 !== t2.h1_count, anySem.h1);
  hit('W2', 'heading_skip', (anySem.headingSkips || 0) > t2.heading_skips_max, anySem.headingSkips);
  hit('W2', 'landmark_main', (anySem.landmarks || {}).main < t2.landmark_main_min);
  hit('W2', 'landmark_nav', (anySem.landmarks || {}).nav < t2.landmark_nav_min);
  hit('W2', 'img_no_alt', (anySem.imgNoAlt || 0) > t2.img_without_alt_max, anySem.imgNoAlt);
  hit('W2', 'button_no_name', (anySem.buttonsNoName || 0) > t2.button_without_name_max);
  hit('W2', 'input_no_label', (anySem.inputsNoLabel || 0) > t2.input_without_label_max);
  hit('W2', 'aria_dangling', (anySem.ariaBadRef || 0) > t2.aria_dangling_ref_max);
  hit('W2', 'fake_button', (anySem.fakeButtons || []).length > t2.fake_buttons_max, (anySem.fakeButtons || []).join('|'));
  hit('W2', 'kbd_unreachable', (r.keyboard.unreachable || []).length > t2.kbd_unreachable_max, (r.keyboard.unreachable || []).join('|'));
  hit('W2', 'kbd_no_focus_ring', (r.keyboard.noFocusRing || []).length > t2.kbd_no_focus_ring_max, (r.keyboard.noFocusRing || []).join('|'));

  // ---- W3 交互与状态 ----
  for (const k of TH.W3_interaction.must_pass) {
    const s = (r.interaction || {})[k];
    hit('W3', 'state_' + k, !(s && s.pass === true));
  }

  // ---- W4 性能预算 ----
  const p = r.perf || {};
  hit('W4', 'resource_count', p.resources > t4.resource_count_max, p.resources);
  hit('W4', 'transfer_bytes', p.bytes > t4.transfer_bytes_max, p.bytes);
  hit('W4', 'long_task', Math.max(0, ...(p.longTasks || [0])) > t4.long_task_ms_max, Math.max(0, ...(p.longTasks || [0])));
  hit('W4', 'frames_p95', (p.framesP95 || 0) > t4.frames_p95_ms_max, p.framesP95);
  hit('W4', 'cls', (p.cls || 0) > t4.cls_max, p.cls);
  hit('W4', 'dom_nodes', (p.nodes || 0) > t4.dom_nodes_max, p.nodes);
  hit('W4', 'js_heap', (p.jsHeapMB || 0) > t4.js_heap_mb_max, p.jsHeapMB);
  hit('W4', 'layout_count', (p.layoutDelta || 0) > t4.layout_count_delta_max, p.layoutDelta);
  hit('W4', 'recalc_style', (p.recalcDelta || 0) > t4.recalc_style_delta_max, p.recalcDelta);

  const layers = Object.keys(L).filter(k => L[k].length);
  return { pass: layers.length === 0, layers, detail: L };
}

if (require.main === module) {
  const r = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  console.log(JSON.stringify(verify(r), null, 1));
}
module.exports = { verify, TH };

