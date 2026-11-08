// mutants.js —— 变异集定义。标签（should_fail）与「预期被哪一层抓到」在任何一次运行之前就写死。
// 规则（照搬 3D 侧的准入测试）：
//   1 每条 search 片段在目标文件中必须唯一出现；
//   2 参考解必须全过（已验，5/5）；
//   3 should_fail 的变异必须至少被一层抓到，否则这条变异不可验证，要从数据集里剔除（不是调阈值）。
// expect 字段是「设计时认为该挂在哪层」，用来事后对账，不参与判定。

module.exports = [
  // ================= 开发集：该挂（功能性缺陷）8 个 =================
  { id: 'F1_contrast_low', fail: true, expect: ['W2'], why: '正文灰阶提亮到对比度不足（WCAG 1.4.3 不过）',
    edits: [['styles.css', '--muted:#4a5560;', '--muted:#9aa3ac;']] },

  { id: 'F2_img_alt_removed', fail: true, expect: ['W2'], why: 'logo 的替代文本被删，屏幕阅读器读不出',
    edits: [['index.html', '<img src="logo.svg" alt="Orbit Analytics 标志">', '<img src="logo.svg">']] },

  { id: 'F3_button_to_div', fail: true, expect: ['W2'], why: '按钮换成 div+onclick，鼠标能点但键盘到不了',
    edits: [['index.html', '<button class="btn" id="open-demo" type="button">预约演示</button>',
      '<div class="btn" id="open-demo">预约演示</div>']] },

  { id: 'F4_card_fixed_width', fail: true, expect: ['W1'], why: '卡片写死最小宽度 420px，窄视口横向溢出',
    edits: [['styles.css', 'flex:1 1 260px;min-width:0;max-width:100%;', 'flex:1 1 260px;min-width:420px;'],
      ['styles.css', '  .card{flex:1 1 100%}', '  .card{flex:1 1 420px}']] },

  { id: 'F5_hero_behind_header', fail: true, expect: ['W1'], why: '负边距 + z-index 用错，页头压在主按钮上，点不到',
    edits: [['styles.css', '.hero{padding:28px 20px;max-width:900px}',
      '.hero{padding:28px 20px;max-width:900px;margin-top:-72px;position:relative;z-index:-1}']] },

  { id: 'F6_form_validation_off', fail: true, expect: ['W3'], why: '邮箱校验被摘掉，非法邮箱也能提交成功',
    edits: [['index.html', 'type="email" required\n               pattern="[^@\\s]+@[^@\\s]+\\.[^@\\s]+" aria-describedby="email-hint email-err"',
      'type="text" aria-describedby="email-hint email-err"'],
      ['index.html', "if (!email.value || !email.checkValidity()) {", 'if (!email.value) {']] },

  { id: 'F7_broken_img_404', fail: true, expect: ['W0'], why: '图片路径写错，线上 404，控制台报错',
    edits: [['index.html', '<img src="logo.svg" alt="Orbit Analytics 标志">', '<img src="logo-v2.svg" alt="Orbit Analytics 标志">']] },

  { id: 'F8_sync_busy_loop', fail: true, expect: ['W4'], why: '启动时同步忙等 300ms，主线程被长任务占住',
    edits: [['index.html', "  var $ = function (id) { return document.getElementById(id); };",
      "  var $ = function (id) { return document.getElementById(id); };\n  (function(){var t=performance.now(),s=0;while(performance.now()-t<300){s+=Math.sqrt(t);}window.__sink=s;})();"]] },

  // ================= 开发集：不该挂（等价重写）8 个 =================
  { id: 'P1_flex_to_grid', fail: false, expect: [], why: '卡片布局从 flex 改成 grid auto-fit，渲染等价',
    edits: [['styles.css', '.cards{display:flex;flex-wrap:wrap;gap:var(--gap);padding:0 20px 24px;margin:0;list-style:none}',
      '.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:var(--gap);padding:0 20px 24px;margin:0;list-style:none}'],
      ['styles.css', '  .card{flex:1 1 100%}', '  .cards{grid-template-columns:1fr}']] },

  { id: 'P2_rename_classes', fail: false, expect: [], why: '全部类名换成哈希名（模拟 CSS Modules / 构建产物）',
    rename: { 'site-header': 'x7a1', 'site-nav': 'x7a2', 'hero-actions': 'x7a3', 'cards': 'x7a4', 'card': 'x7a5', 'badge': 'x7a6', 'tablist': 'x7a7', 'tabpanel': 'x7a8', 'signup': 'x7a9', 'field': 'x7b1', 'modal-box': 'x7b2', 'brand': 'x7b3', 'hint': 'x7b4' } },

  { id: 'P3_recolor_keep_contrast', fail: false, expect: [], why: '整套配色换成紫+暖灰，对比度仍达标',
    edits: [['styles.css', '--brand:#0b5cad;', '--brand:#6b21a8;'],
      ['styles.css', '--card:#f6f8fa;', '--card:#faf5ff;'],
      ['styles.css', '--fg:#1b1f24;', '--fg:#1f1b24;'],
      ['styles.css', ':focus-visible{outline:3px solid #0b5cad;', ':focus-visible{outline:3px solid #6b21a8;']] },

  { id: 'P4_px_to_rem', fail: false, expect: [], why: '间距单位 px 改成 rem，16px 基准下渲染等价',
    edits: [['styles.css', '--gap:16px; --radius:10px;', '--gap:1rem; --radius:0.625rem;'],
      ['styles.css', '.hero{padding:28px 20px;max-width:900px}', '.hero{padding:1.75rem 1.25rem;max-width:56.25rem}'],
      ['styles.css', '.btn{background:var(--brand);color:var(--brand-fg);border:1px solid var(--brand);border-radius:8px;padding:9px 14px}',
        '.btn{background:var(--brand);color:var(--brand-fg);border:0.0625rem solid var(--brand);border-radius:0.5rem;padding:0.5625rem 0.875rem}']] },

  { id: 'P5_utility_classes', fail: false, expect: [], why: '把一组规则拆成原子类（Tailwind 风格），结构不动',
    edits: [['styles.css', '.hero-actions{display:flex;gap:12px;flex-wrap:wrap}',
      '.d-flex{display:flex}.g-12{gap:12px}.fw-wrap{flex-wrap:wrap}'],
      ['index.html', '<div class="hero-actions">', '<div class="d-flex g-12 fw-wrap">']] },

  { id: 'P6_inline_svg_logo', fail: false, expect: [], why: '外链 logo 换成内联 svg（少一个请求），可访问名保留',
    edits: [['index.html', '<img src="logo.svg" alt="Orbit Analytics 标志">',
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="28" height="28" role="img" aria-label="Orbit Analytics 标志"><circle cx="16" cy="16" r="6" fill="#0b5cad"/></svg>']] },

  { id: 'P7_section_to_div_role', fail: false, expect: [], why: 'section 换成 div[role=region]，语义等价',
    edits: [['index.html', '<section class="signup" aria-labelledby="signup-title">', '<div class="signup" role="region" aria-labelledby="signup-title">'],
      ['index.html', '  </section>\n</main>', '  </div>\n</main>']] },

  { id: 'P8_font_stack', fail: false, expect: [], why: '换另一组系统字体栈',
    edits: [['styles.css', 'font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif;',
      'font-family:"Liberation Sans","Nimbus Sans",Helvetica,"DejaVu Sans",sans-serif;']] },

  // ================= 留出集（标签与阈值都不动，只跑一次）6 个 =================
  { id: 'H1_js_error_tail', fail: true, holdout: true, expect: ['W0'], why: '脚本尾部一个未定义变量，交互全部绑完才炸，只有控制台能看到',
    edits: [['index.html', "})();\n</script>", "  window.__cfg = __missingConfig.flag;\n})();\n</script>"]] },

  { id: 'H2_heading_and_landmark', fail: true, holdout: true, expect: ['W2'], why: '标题层级跳级 + main 换成普通 div，辅助技术失去结构',
    edits: [['index.html', '<main id="main">', '<div id="main">'], ['index.html', '</main>', '</div>'],
      ['index.html', '<h2 id="tabs-title">接入方式</h2>', '<h4 id="tabs-title">接入方式</h4>']] },

  { id: 'H3_theme_not_persisted', fail: true, holdout: true, expect: ['W3'], why: '主题切换不落盘，刷新就回到浅色',
    edits: [['index.html', "    try { localStorage.setItem('orbit-theme', next); } catch (e) {}\n", '']] },

  { id: 'H4_event_delegation', fail: false, holdout: true, expect: [], why: 'tab 的逐个绑定改成事件委托',
    edits: [['index.html', `  var tabs = ['web', 'ios', 'svr'];
  tabs.forEach(function (k) {
    $('tab-' + k).addEventListener('click', function () {
      tabs.forEach(function (j) {
        $('tab-' + j).setAttribute('aria-selected', String(j === k));
        $('panel-' + j).hidden = (j !== k);
      });
    });
  });`, `  var tabs = ['web', 'ios', 'svr'];
  document.querySelector('.tablist').addEventListener('click', function (e) {
    var b = e.target.closest('[role=tab]'); if (!b) return;
    var k = b.id.replace('tab-', '');
    tabs.forEach(function (j) {
      $('tab-' + j).setAttribute('aria-selected', String(j === k));
      $('panel-' + j).hidden = (j !== k);
    });
  });`]] },

  { id: 'H5_minified_html', fail: false, holdout: true, expect: [], why: 'HTML 压缩（去标签间空白与缩进）', minifyHtml: true },

  { id: 'H6_css_shorthand', fail: false, holdout: true, expect: [], why: 'CSS 改写成简写与逻辑属性',
    edits: [['styles.css', '.card{\n  position:relative;flex:1 1 260px;min-width:0;max-width:100%;\n  background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:16px;\n}',
      '.card{position:relative;flex:1 1 260px;min-inline-size:0;max-inline-size:100%;background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding-block:16px;padding-inline:16px}'],
      ['styles.css', '.field{display:flex;flex-direction:column;gap:6px;margin-bottom:14px}', '.field{display:flex;flex-flow:column nowrap;gap:6px;margin-block-end:14px}']] },
];

