// aes_verify.js —— 审美判据。阈值在任何一次变异测试之前就冻结，来源是参考页实测 + 余量。
// 参考页实测（out/aes_ref.json，375 与 1440 两档）：
//   sizeCount 6~7、scaleRatioCV 0.133、familyCount 1、lineHeightBad 0、lineLenBad 0~1、
//   hueFamilies 1、hueEntropy 0、spacing distinct 12、bestBaseShare 0.914(base=2)、
//   radiusDistinct 4、grid top2Share 0.765~0.78、inkRatio 0.296~0.526
// 注意三件事：
//   1 参考页只有 57.8% 的间距值落在 4 的倍数上 —— 所以判据用「自动选基数后的占比」，不预设 4px 栅格；
//   2 参考页在 1440 档本来就有 1 个行长超标 —— 所以 len 的容差是 2 不是 0；
//   3 tell（Inter / 紫渐变）**单独报，不进 pass/fail**：它度量的是「像不像 AI 默认」，不是「好不好」。

const T = {
  sizeCountMax: 11,        // 参考 7，留 4 档余量
  scaleCV: 0.35,           // 参考 0.133
  familyMax: 2,            // 参考 1，允许正文 + 标题两种
  lineHeightBadMax: 0,     // 参考 0
  lineLenBadMax: 0,        // 参考 0（修掉 widthCh 高估 bug 后）
  lineLenMaxCh: 90,        // 参考 42.8（1440 档）
  hueFamiliesMax: 3,       // 参考 1
  hueEntropyMax: 2.0,      // 参考 0
  spacingDistinctMax: 20,  // 参考 12
  spacingBaseShareMin: 0.70, // 参考 0.914
  // radius 信号已作废：参考页本来就有 4 种圆角（6/8/10/999），判别余量不足，见 19_aesthetics.md
  inkMax: 0.78,            // 参考最高 0.526（375 档）
  inkMin: 0.06,
};

function verify(report) {
  const vps = Object.values(report.viewports || {});
  if (!vps.length) return { pass: false, layers: ['noop'], detail: { err: 'no viewport' } };
  const worst = (f) => Math.max(...vps.map(f));
  const least = (f) => Math.min(...vps.map(f));
  const d = {};
  const fails = [];
  const chk = (name, bad, val) => { d[name] = val; if (bad) fails.push(name); };

  chk('hier', worst(v => v.type.hierViolations) > 0, worst(v => v.type.hierViolations));
  chk('scale', worst(v => v.type.sizeCount) > T.sizeCountMax || worst(v => v.type.scaleRatioCV) > T.scaleCV,
    { sizeCount: worst(v => v.type.sizeCount), cv: worst(v => v.type.scaleRatioCV) });
  chk('family', worst(v => v.type.familyCount) > T.familyMax, worst(v => v.type.familyCount));
  chk('lh', worst(v => v.type.lineHeightBad) > T.lineHeightBadMax, worst(v => v.type.lineHeightBad));
  chk('len', worst(v => v.type.lineLenBad) > T.lineLenBadMax || worst(v => v.type.lineLenMax) > T.lineLenMaxCh,
    { bad: worst(v => v.type.lineLenBad), max: worst(v => v.type.lineLenMax) });
  chk('hue', worst(v => v.color.hueFamilies) > T.hueFamiliesMax || worst(v => v.color.hueEntropy) > T.hueEntropyMax,
    { fam: worst(v => v.color.hueFamilies), ent: worst(v => v.color.hueEntropy) });
  chk('contrast', worst(v => v.color.contrastFails) > 0, worst(v => v.color.contrastFails));
  chk('spacing', worst(v => v.spacing.distinct) > T.spacingDistinctMax || least(v => v.spacing.bestBaseShare) < T.spacingBaseShareMin,
    { distinct: worst(v => v.spacing.distinct), base: vps[0].spacing.bestBase, share: least(v => v.spacing.bestBaseShare) });
  // 以下两条只记录、不判定（信号作废，理由见 19_aesthetics.md §6.3）：
  //   radius：参考页本来就有 4 种圆角，变异只推到 6，余量不足；
  //   grid  ：A09（该挂）alignWithin2=0.707，而 P03（不该挂、且审美更好）=0.765，
  //           可分离阈值只有 0.058 的余量，且 P03 比多数该挂项更接近失败 —— 不能当闸。
  d.radiusDistinct_INFO = worst(v => v.spacing.radiusDistinct);
  d.gridAlignWithin2_INFO = least(v => v.grid.alignWithin2);
  chk('ink', worst(v => v.whitespace.inkRatio) > T.inkMax || least(v => v.whitespace.inkRatio) < T.inkMin,
    { max: worst(v => v.whitespace.inkRatio), min: least(v => v.whitespace.inkRatio) });

  // tell 单独算，不进 fails
  const tell = {
    inter: vps.some(v => v.tells.font_inter),
    aiFonts: worst(v => v.tells.font_common_ai),
    purpleGradient: worst(v => v.tells.purple_gradient),
    gradients: worst(v => v.tells.gradient_count),
  };
  const tellHit = tell.inter || tell.purpleGradient > 0 || tell.aiFonts > 0;

  return { pass: fails.length === 0, layers: fails, detail: d, tell, tellHit };
}

module.exports = { verify, T };

