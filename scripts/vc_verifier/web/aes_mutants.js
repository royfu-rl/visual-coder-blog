// aes_mutants.js —— 只针对「审美」的变异集。
// 规则与 mutants.js 一致：
//   1 每条 search 片段在目标文件中必须唯一出现；
//   2 参考页必须全过；
//   3 should_fail 的变异必须至少被一条审美判据抓到，否则该变异不可验证，剔除而不是调阈值。
// 关键区别：这些缺陷**全部不触发** W0~W4（能跑、无报错、不溢出、不遮挡、axe 通过），
// 也就是说它们是「现有程序化 verifier 的盲区」，正是本轮要回答的那一块。
// expect 字段是设计时认为该挂在哪条判据上，事后对账，不参与判定。

module.exports = [
  // ============ 该挂：审美缺陷 11 个 ============
  { id: 'A01_hier_inverted', fail: true, expect: ['hier'], why: 'h2 比 h1 大，视觉层级反了（功能完好）',
    edits: [['styles.css', '.hero h1{font-size:2rem;margin:0 0 8px}', '.hero h1{font-size:1.1rem;margin:0 0 8px}']] },

  { id: 'A02_scale_destroyed', fail: true, expect: ['scale'], why: '字号变成一堆相近的随机值，没有尺度',
    edits: [['styles.css', '.hero h1{font-size:2rem;margin:0 0 8px}', '.hero h1{font-size:1.43rem;margin:0 0 8px}'],
      ['styles.css', '.card h3{margin:0 0 6px;font-size:1.05rem}', '.card h3{margin:0 0 6px;font-size:1.37rem}'],
      ['styles.css', '.card p{margin:0;color:var(--muted);font-size:0.95rem}', '.card p{margin:0;color:var(--muted);font-size:1.21rem}'],
      ['styles.css', '.card .badge{', '.card .badge{font-size:1.09rem;']] },

  { id: 'A03_font_soup', fail: true, expect: ['family'], why: '四种字体混用',
    edits: [['styles.css', '.hero h1{font-size:2rem;margin:0 0 8px}', '.hero h1{font-size:2rem;margin:0 0 8px;font-family:"Liberation Serif",Georgia,serif}'],
      ['styles.css', '.card h3{margin:0 0 6px;font-size:1.05rem}', '.card h3{margin:0 0 6px;font-size:1.05rem;font-family:"Liberation Mono",monospace}'],
      ['styles.css', '.site-nav a{color:var(--brand);text-decoration:none;padding:6px 8px;border-radius:6px}',
        '.site-nav a{color:var(--brand);text-decoration:none;padding:6px 8px;border-radius:6px;font-family:"DejaVu Serif",serif}']] },

  { id: 'A04_line_height_tight', fail: true, expect: ['lh'], why: '正文行高压到 1.02，挤成一团',
    edits: [['styles.css', '  font-size:1rem; line-height:1.5;', '  font-size:1rem; line-height:1.02;']] },

  // A05 经实测判定为**无效变异**：参考页最长段落只有 46 个字符，去掉限宽后实际行长 46ch，
  // 不构成「行太长」这个缺陷。按冻结规则剔除该变异，而不是把阈值调到 46 以下。
  // 含义：行长这条判据需要有真实正文的题面才能验证，本参考页验不了。
  { id: 'A05_line_too_long', invalid: true, fail: true, expect: ['len'], why: '去掉 60ch 限宽（参考页正文太短，缺陷不成立 → 无效变异）',
    edits: [['styles.css', '.hero{padding:28px 20px;max-width:900px}', '.hero{padding:28px 20px}'],
      ['styles.css', '.hero p{color:var(--muted);margin:0 0 16px;max-width:60ch}', '.hero p{color:var(--muted);margin:0 0 16px}']] },

  { id: 'A06_color_riot', fail: true, expect: ['hue'], why: '塞进五个互不相关的色相',
    edits: [['styles.css', '  --brand:#0b5cad; --brand-fg:#ffffff; --card:#f6f8fa; --danger:#9b1c1c;',
      '  --brand:#0b5cad; --brand-fg:#ffffff; --card:#fff3c4; --danger:#9b1c1c;'],
      ['styles.css', '.card h3{margin:0 0 6px;font-size:1.05rem}', '.card h3{margin:0 0 6px;font-size:1.05rem;color:#0f7a3d}'],
      ['styles.css', '.btn-ghost{background:transparent;color:var(--brand);border:1px solid var(--line);border-radius:8px;padding:9px 14px}',
        '.btn-ghost{background:#7b2fd4;color:#ffffff;border:1px solid #7b2fd4;border-radius:8px;padding:9px 14px}'],
      ['styles.css', '.site-header{display:flex;align-items:center;gap:var(--gap);padding:12px 20px;border-bottom:1px solid var(--line);flex-wrap:wrap}',
        '.site-header{display:flex;align-items:center;gap:var(--gap);padding:12px 20px;border-bottom:1px solid var(--line);flex-wrap:wrap;background:#e8731a}']] },

  { id: 'A07_spacing_chaos', fail: true, expect: ['spacing'], why: '间距全换成互不相关的奇数值',
    edits: [['styles.css', '  --gap:16px; --radius:10px;', '  --gap:13px; --radius:10px;'],
      ['styles.css', '.site-header{display:flex;align-items:center;gap:var(--gap);padding:12px 20px;', '.site-header{display:flex;align-items:center;gap:var(--gap);padding:7px 23px;'],
      ['styles.css', '.hero{padding:28px 20px;max-width:900px}', '.hero{padding:31px 17px;max-width:900px}'],
      ['styles.css', 'border-radius:var(--radius);padding:16px;', 'border-radius:var(--radius);padding:11px 19px 27px 5px;'],
      ['styles.css', '.cards{display:flex;flex-wrap:wrap;gap:var(--gap);padding:0 20px 24px;margin:0;list-style:none}',
        '.cards{display:flex;flex-wrap:wrap;gap:var(--gap);padding:0 9px 29px;margin:0;list-style:none}'],
      ['styles.css', '.hero-actions{display:flex;gap:12px;flex-wrap:wrap}', '.hero-actions{display:flex;gap:21px;flex-wrap:wrap}'],
      ['styles.css', '.site-nav{display:flex;gap:12px;margin-left:auto;flex-wrap:wrap}', '.site-nav{display:flex;gap:7px;margin-left:auto;flex-wrap:wrap}'],
      ['styles.css', '.btn{background:var(--brand);color:var(--brand-fg);border:1px solid var(--brand);border-radius:8px;padding:9px 14px}',
        '.btn{background:var(--brand);color:var(--brand-fg);border:1px solid var(--brand);border-radius:8px;padding:5px 23px}']] },

  { id: 'A08_radius_chaos', fail: true, expect: ['radius'], why: '每个组件一个圆角值',
    edits: [['styles.css', '.btn{background:var(--brand);color:var(--brand-fg);border:1px solid var(--brand);border-radius:8px;padding:9px 14px}',
      '.btn{background:var(--brand);color:var(--brand-fg);border:1px solid var(--brand);border-radius:3px;padding:9px 14px}'],
      ['styles.css', '.btn-ghost{background:transparent;color:var(--brand);border:1px solid var(--line);border-radius:8px;padding:9px 14px}',
        '.btn-ghost{background:transparent;color:var(--brand);border:1px solid var(--line);border-radius:17px;padding:9px 14px}'],
      ['styles.css', '.site-nav a{color:var(--brand);text-decoration:none;padding:6px 8px;border-radius:6px}',
        '.site-nav a{color:var(--brand);text-decoration:none;padding:6px 8px;border-radius:21px}'],
      ['styles.css', '  --gap:16px; --radius:10px;', '  --gap:16px; --radius:27px;'],
      ['styles.css', '.card .badge{', '.card .badge{border-radius:4px;']] },

  { id: 'A09_grid_misaligned', fail: true, expect: ['grid'], why: '各区块左边距各不相同，版面没有垂线',
    edits: [['styles.css', '.hero{padding:28px 20px;max-width:900px}', '.hero{padding:28px 20px 28px 47px;max-width:900px}'],
      ['styles.css', '.cards{display:flex;flex-wrap:wrap;gap:var(--gap);padding:0 20px 24px;margin:0;list-style:none}',
        '.cards{display:flex;flex-wrap:wrap;gap:var(--gap);padding:0 20px 24px 9px;margin:0;list-style:none}'],
      ['styles.css', '.site-header{display:flex;align-items:center;gap:var(--gap);padding:12px 20px;', '.site-header{display:flex;align-items:center;gap:var(--gap);padding:12px 20px 12px 63px;']] },

  { id: 'A10_cramped', fail: true, expect: ['ink'], why: '把所有内外边距抹掉，内容糊满整页',
    edits: [['styles.css', '*{box-sizing:border-box}', '*{box-sizing:border-box;margin:0 !important;padding:0 !important;gap:0 !important}']] },

  { id: 'A12_size_zoo', fail: true, expect: ['scale'], why: '非标题元素各用一个随机字号，字号种类爆到 13 种且没有尺度（层级不变）',
    edits: [['styles.css', '.site-nav a{color:var(--brand);text-decoration:none;padding:6px 8px;border-radius:6px}',
      '.site-nav a{color:var(--brand);text-decoration:none;padding:6px 8px;border-radius:6px;font-size:0.81rem}'],
      ['styles.css', '.btn{background:var(--brand);color:var(--brand-fg);border:1px solid var(--brand);border-radius:8px;padding:9px 14px}',
        '.btn{background:var(--brand);color:var(--brand-fg);border:1px solid var(--brand);border-radius:8px;padding:9px 14px;font-size:0.67rem}'],
      ['styles.css', '.btn-ghost{background:transparent;color:var(--brand);border:1px solid var(--line);border-radius:8px;padding:9px 14px}',
        '.btn-ghost{background:transparent;color:var(--brand);border:1px solid var(--line);border-radius:8px;padding:9px 14px;font-size:1.13rem}'],
      ['styles.css', '.tablist button{background:transparent;border:1px solid transparent;border-bottom:none;padding:8px 14px;color:var(--muted);border-radius:8px 8px 0 0}',
        '.tablist button{background:transparent;border:1px solid transparent;border-bottom:none;padding:8px 14px;color:var(--muted);border-radius:8px 8px 0 0;font-size:0.58rem}'],
      ['styles.css', '.field label{font-weight:600}', '.field label{font-weight:600;font-size:1.31rem}'],
      ['styles.css', '.field .hint{color:var(--muted);font-size:0.85rem}', '.field .hint{color:var(--muted);font-size:0.52rem}'],
      ['styles.css', '.err{color:var(--danger);font-size:0.9rem;min-height:1.2em}', '.err{color:var(--danger);font-size:1.19rem;min-height:1.2em}'],
      ['styles.css', '.ok{color:#14532d;font-weight:600}', '.ok{color:#14532d;font-weight:600;font-size:0.74rem}'],
      ['styles.css', '.brand{display:flex;align-items:center;gap:8px;font-weight:700}', '.brand{display:flex;align-items:center;gap:8px;font-weight:700;font-size:1.07rem}']] },

  { id: 'A11_ai_slop', fail: true, expect: ['tell'], why: 'Inter 字体 + 白卡上的紫色渐变（Anthropic 博客点名的那一组）',
    edits: [['styles.css', '  font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif;', '  font-family:Inter,"DejaVu Sans","Liberation Sans",Arial,sans-serif;'],
      ['styles.css', '.hero{padding:28px 20px;max-width:900px}',
        '.hero{padding:28px 20px;max-width:900px;background:linear-gradient(135deg,#7c3aed 0%,#a855f7 100%)}'],
      ['styles.css', '.hero h1{font-size:2rem;margin:0 0 8px}', '.hero h1{font-size:2rem;margin:0 0 8px;color:#ffffff}'],
      ['styles.css', '.hero p{color:var(--muted);margin:0 0 16px;max-width:60ch}', '.hero p{color:#f3e8ff;margin:0 0 16px;max-width:60ch}']] },

  // ============ 不该挂：合法改版 / 等价重写 8 个 ============
  { id: 'P01_rebrand_green', fail: false, expect: [], why: '品牌色换成同样深的绿，结构与对比度不变（合法改版）',
    edits: [['styles.css', '  --brand:#0b5cad; --brand-fg:#ffffff;', '  --brand:#0a6b3d; --brand-fg:#ffffff;'],
      ['styles.css', ':focus-visible{outline:3px solid #0b5cad;outline-offset:2px}', ':focus-visible{outline:3px solid #0a6b3d;outline-offset:2px}']] },

  { id: 'P02_other_type_scale', fail: false, expect: [], why: '换成另一套自洽的等比尺度（1.25 比例）',
    edits: [['styles.css', '.hero h1{font-size:2rem;margin:0 0 8px}', '.hero h1{font-size:1.953rem;margin:0 0 8px}'],
      ['styles.css', '.card h3{margin:0 0 6px;font-size:1.05rem}', '.card h3{margin:0 0 6px;font-size:1.25rem}'],
      ['styles.css', '.card p{margin:0;color:var(--muted);font-size:0.95rem}', '.card p{margin:0;color:var(--muted);font-size:0.8rem}']] },

  { id: 'P03_spacing_base8', fail: false, expect: [], why: '间距全部规整到 8 的倍数（比参考页更整齐，必须判过）',
    edits: [['styles.css', '  --gap:16px; --radius:10px;', '  --gap:16px; --radius:8px;'],
      ['styles.css', '.site-header{display:flex;align-items:center;gap:var(--gap);padding:12px 20px;', '.site-header{display:flex;align-items:center;gap:var(--gap);padding:16px 24px;'],
      ['styles.css', '.hero{padding:28px 20px;max-width:900px}', '.hero{padding:32px 24px;max-width:900px}'],
      ['styles.css', '.site-nav a{color:var(--brand);text-decoration:none;padding:6px 8px;border-radius:6px}',
        '.site-nav a{color:var(--brand);text-decoration:none;padding:8px 8px;border-radius:8px}'],
      ['styles.css', '.btn{background:var(--brand);color:var(--brand-fg);border:1px solid var(--brand);border-radius:8px;padding:9px 14px}',
        '.btn{background:var(--brand);color:var(--brand-fg);border:1px solid var(--brand);border-radius:8px;padding:8px 16px}'],
      ['styles.css', '.btn-ghost{background:transparent;color:var(--brand);border:1px solid var(--line);border-radius:8px;padding:9px 14px}',
        '.btn-ghost{background:transparent;color:var(--brand);border:1px solid var(--line);border-radius:8px;padding:8px 16px}']] },

  { id: 'P04_brand_gradient', fire: 'tell', fail: false, expect: [], why: '品牌蓝的单个渐变（有品味的用法，不是紫渐变）',
    edits: [['styles.css', '.hero{padding:28px 20px;max-width:900px}',
      '.hero{padding:28px 20px;max-width:900px;background:linear-gradient(135deg,#eaf2fb 0%,#ffffff 100%)}']] },

  { id: 'P05_dark_theme', fail: false, expect: [], why: '深色主题，对比度仍然合规',
    edits: [['styles.css', '  --bg:#ffffff; --fg:#1b1f24; --muted:#4a5560; --line:#d7dde3;',
      '  --bg:#11151a; --fg:#eef2f6; --muted:#b3bdc7; --line:#2c343d;'],
      ['styles.css', '  --brand:#0b5cad; --brand-fg:#ffffff; --card:#f6f8fa; --danger:#9b1c1c;',
        '  --brand:#64b5ff; --brand-fg:#0a1017; --card:#1a2028; --danger:#ff8f8f;'],
      ['styles.css', ':focus-visible{outline:3px solid #0b5cad;outline-offset:2px}', ':focus-visible{outline:3px solid #64b5ff;outline-offset:2px}']] },

  { id: 'P06_more_whitespace', fail: false, expect: [], why: '整体留白加大（审美上更好，必须判过）',
    edits: [['styles.css', '  --gap:16px; --radius:10px;', '  --gap:24px; --radius:10px;'],
      ['styles.css', '.hero{padding:28px 20px;max-width:900px}', '.hero{padding:56px 20px;max-width:900px}']] },

  { id: 'P07_class_rename', fail: false, expect: [], why: '类名重命名（纯等价重写）',
    rename: { card: 'tile', hero: 'lede', 'hero-actions': 'lede-cta', btn: 'cta', 'btn-ghost': 'cta-alt' } },

  { id: 'P08_minify', fail: false, expect: [], why: 'HTML 压缩（纯等价重写）', minifyHtml: true },
];

