// node build_cases.js
//   以 pages/ref.html 为参考解，用 SEARCH/REPLACE 造 16 个变异，标签先写死。
//   该挂 8 个（数据 / 轴 / 系列 / 图例 / 类型 / 结构），不该挂 8 个（纯外观）。
const fs = require('fs'), path = require('path');
const HERE = __dirname;
const REF = fs.readFileSync(path.join(HERE, 'pages/ref.html'), 'utf8');

const M = [
  // ---------- 该挂：画出来的东西和数据对不上 ----------
  { id: 'data_scale_q2', fail: true, why: 'Q2 整个系列乘 1.3',
    s: 'const Q2 = [1430, 1520, 1180, 1690, 1120, 980];',
    r: 'const Q2 = [1859, 1976, 1534, 2197, 1456, 1274];' },
  { id: 'data_one_point', fail: true, why: 'Q1 深圳 1510 画成 1150',
    s: 'const Q1 = [1280, 1640, 920, 1510, 760, 1050];',
    r: 'const Q1 = [1280, 1640, 920, 1150, 760, 1050];' },
  { id: 'series_drop', fail: true, why: '只画了 Q1，漏掉 Q2',
    s: `      { label: 'Q2', data: Q2, backgroundColor: COLORS[1], borderRadius: RADIUS }\n`, r: '' },
  { id: 'legend_swap', fail: true, why: '两个系列的图例标签互换，图例与数据错位',
    s: `{ label: 'Q1', data: Q1, backgroundColor: COLORS[0], borderRadius: RADIUS },`,
    r: `{ label: 'Q2', data: Q1, backgroundColor: COLORS[0], borderRadius: RADIUS },` ,
    s2: `{ label: 'Q2', data: Q2, backgroundColor: COLORS[1], borderRadius: RADIUS }`,
    r2: `{ label: 'Q1', data: Q2, backgroundColor: COLORS[1], borderRadius: RADIUS }` },
  { id: 'axis_min_500', fail: true, why: 'y 轴从 500 起，柱状图被截断，视觉上放大差异',
    s: 'const Y_MIN = 0;', r: 'const Y_MIN = 500;' },
  { id: 'type_line', fail: true, why: '题面要柱状图，画成折线图',
    s: `const CHART_TYPE = 'bar';`, r: `const CHART_TYPE = 'line';` },
  { id: 'cats_shuffle', fail: true, why: '类别标签换了顺序，数据没跟着换',
    s: `const CATS = ['北京', '上海', '广州', '深圳', '成都', '杭州'];`,
    r: `const CATS = ['上海', '北京', '深圳', '广州', '杭州', '成都'];` },
  { id: 'ytitle_missing', fail: true, why: 'y 轴标题与单位丢了',
    s: `title: { display: true, text: '新增充电桩数量（台）', font: { family: FONT, size: 13 } },`,
    r: `title: { display: false, text: '' },` },

  // ---------- 不该挂：只改外观 ----------
  { id: 'recolor', fail: false, why: '换一套配色',
    s: `const COLORS = ['#4e79a7', '#f28e2b'];`, r: `const COLORS = ['#59a14f', '#b07aa1'];` },
  { id: 'font_swap', fail: false, why: '换字体',
    s: `const FONT = 'DejaVu Sans';`, r: `const FONT = 'Liberation Serif, serif';` },
  { id: 'bar_radius', fail: false, why: '柱子加圆角',
    s: 'const RADIUS = 0;', r: 'const RADIUS = 8;' },
  { id: 'animation', fail: false, why: '加动画时长（时钟已冻结，应当不影响终态）',
    s: 'const ANIM = 0;', r: 'const ANIM = 800;' },
  { id: 'legend_bottom', fail: false, why: '图例从顶部移到底部',
    s: `const LEGEND_POS = 'top';`, r: `const LEGEND_POS = 'bottom';` },
  { id: 'grid_dashed', fail: false, why: 'y 轴网格线改虚线',
    s: `y: { min: Y_MIN, beginAtZero: true,`, r: `y: { min: Y_MIN, beginAtZero: true, grid: { color: '#ddd', borderDash: [4, 4] },` },
  { id: 'bar_thinner', fail: false, why: '柱子变窄',
    s: `    scales: {`, r: `    datasets: { bar: { barPercentage: 0.6, categoryPercentage: 0.7 } },\n    scales: {` },
  { id: 'tooltip_off', fail: false, why: '关掉提示框（静态图上看不出来）',
    s: `tooltip: { enabled: true }`, r: `tooltip: { enabled: false }` },
];

const outDir = path.join(HERE, 'pages/cases');
fs.mkdirSync(outDir, { recursive: true });
const meta = [];
for (const m of M) {
  if (!REF.includes(m.s)) throw new Error(`search 片段不唯一或不存在: ${m.id}`);
  if (REF.split(m.s).length !== 2) throw new Error(`search 片段出现多次: ${m.id}`);
  let src = REF.replace(m.s, m.r);
  if (m.s2) { if (!src.includes(m.s2)) throw new Error(`search2 缺失: ${m.id}`); src = src.replace(m.s2, m.r2); }
  fs.writeFileSync(path.join(outDir, m.id + '.html'), src);
  meta.push({ id: m.id, should_fail: m.fail, why: m.why });
}
fs.writeFileSync(path.join(HERE, 'cases.json'), JSON.stringify(meta, null, 1));
console.log(`生成 ${meta.length} 个变异：该挂 ${meta.filter(x => x.should_fail).length}，不该挂 ${meta.filter(x => !x.should_fail).length}`);

