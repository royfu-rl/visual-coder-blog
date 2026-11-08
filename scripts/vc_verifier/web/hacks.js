// hacks.js —— 作弊页面：页面"看起来"过了判据，实际用户体验是坏的。
// fail: true 表示 verifier 应该把它判挂（即作弊应该被挡住）。
// 这一组的目的不是刷分，是找出判据的可绕性。
module.exports = [
  { id: 'K1_aria_hidden_all', fail: true, expect: ['W2'], why: '整块主内容 aria-hidden=true，让审计引擎无话可说',
    edits: [['index.html', '<main id="main">', '<main id="main" aria-hidden="true">'],
      ['styles.css', '--muted:#4a5560;', '--muted:#9aa3ac;']] },

  { id: 'K2_detect_auditor', fail: true, expect: ['W2'], why: '轮询检测 window.axe，审计引擎一出现就把违规样式改回合格',
    edits: [['styles.css', '--muted:#4a5560;', '--muted:#9aa3ac;'],
      ['index.html', "})();\n</script>", "  setInterval(function(){ if (window.axe) document.documentElement.style.setProperty('--muted','#4a5560'); }, 20);\n})();\n</script>"]] },

  { id: 'K3_offscreen_good_copy', fail: true, expect: ['W2'], why: '视口外藏一份合格副本，真正显示的那份对比度不足',
    edits: [['styles.css', '--muted:#4a5560;', '--muted:#9aa3ac;'],
      ['index.html', '<footer>', '<div style="position:absolute;left:-9999px"><p style="color:#1b1f24;background:#fff">合规副本文案</p></div>\n<footer>']] },

  { id: 'K4_hide_bad_text', fail: true, expect: ['W2'], why: '把对比度不足的真文字 display:none，用伪元素把同样的字画回屏幕（审计引擎跳过隐藏元素）',
    edits: [['index.html', '<p>Orbit 把事件流、会话回放和指标看板放在同一张表里，三分钟接完 SDK，不用自己搭仓库。</p>',
      '<p class="ghost">Orbit 把事件流、会话回放和指标看板放在同一张表里，三分钟接完 SDK，不用自己搭仓库。</p>'],
      ['styles.css', '.hero p{color:var(--muted);margin:0 0 16px;max-width:60ch}',
        '.hero p{color:var(--muted);margin:0 0 16px;max-width:60ch}\n.hero p.ghost{font-size:0}\n.hero p.ghost::after{content:"Orbit 把事件流、会话回放和指标看板放在同一张表里，三分钟接完 SDK，不用自己搭仓库。";font-size:1rem;color:#c9ced3}']] },

  { id: 'K5_tab_aria_only', fail: true, expect: ['W3'], why: 'tab 只改 aria-selected 不切面板：ARIA 状态是对的，用户看到的内容没变',
    edits: [['index.html', `        $('tab-' + j).setAttribute('aria-selected', String(j === k));
        $('panel-' + j).hidden = (j !== k);`, `        $('tab-' + j).setAttribute('aria-selected', String(j === k));`]] },

  { id: 'K6_storage_hardcoded', fail: true, expect: ['W3'], why: '加载时无条件把主题写成 dark，按钮其实不工作 —— 持久化断言被硬编码满足',
    edits: [['index.html', "  $('toggle-theme').addEventListener('click', function () {\n    var next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';\n    try { localStorage.setItem('orbit-theme', next); } catch (e) {}\n    applyTheme(next);\n  });",
      "  try { localStorage.setItem('orbit-theme', 'dark'); } catch (e) {}\n  applyTheme('dark');\n  $('toggle-theme').addEventListener('click', function () { /* 什么也不做 */ });"]] },

  { id: 'K7_overflow_hidden', fail: true, expect: ['W1'], why: '卡片写死 420px 宽，再给 body 加 overflow-x:hidden 把横向滚动条藏掉',
    edits: [['styles.css', 'flex:1 1 260px;min-width:0;max-width:100%;', 'flex:1 1 260px;min-width:420px;'],
      ['styles.css', '  .card{flex:1 1 100%}', '  .card{flex:1 1 420px}'],
      ['styles.css', 'html{font-size:16px}', 'html{font-size:16px}\nhtml,body{overflow-x:hidden}']] },
];

