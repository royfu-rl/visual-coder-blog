# Web/DOM 确定性 verifier：本机实测日志

机器：无 GPU，Chrome 148.0.7778.97 无头 + SwiftShader；node v20.18.0；axe-core 4.12.1（cdnjs，走国内代理拉下来存 `vendor/`）。

## 代码
| 文件 | 作用 |
|---|---|
| `tasks/ref/` | 参考页（index.html + styles.css + logo.svg）。有 landmark/nav/hero/卡片网格/tabs/表单校验/模态框/hash 路由/主题持久化 |
| `probe.js` | 探针：三视口盒模型与溢出、axe-core（浅色+深色）、控制台与网络错误、性能读数、键盘可达、7 条交互状态机断言 |
| `thresholds.json` | **冻结阈值**。只在参考页 5 次重复上校准，变异集上一次没调 |
| `verify.js` | 读数 + 冻结阈值 → 五层判定 W0~W4 |
| `mutants.js` | 22 个变异（开发 16 + 留出 6），标签与「预期挂在哪层」跑之前写死 |
| `run_mutations.js` | 应用变异（含唯一性准入检查）→ 探针 → 判定 → 汇总 |
| `naive_baselines.js` | 朴素基线：DOM 标签序列 / 类名序列 / 可见文本 / 单张截图逐像素 |
| `summarize.py` | 判别力表 |

复跑：
```
node probe.js tasks/ref out/ref.json && node verify.js out/ref.json
node run_mutations.js
node naive_baselines.js
python3 summarize.py
```

## 关键读数
- 参考页 5 次重复：231 个字段里只有 4 个变（`ms` / `loadMs` / `framesP95` / `layoutDurTotal`，全是墙钟），判定字段 100% 逐字节一致。
- 参考页 5/5 全过（准入条件 1）。
- 22 变异：第一遍 21/22；修两个 bug 后第二遍 22/22（检出 11/11，误杀 0/11）。两遍判定翻面 0，明细逐字节一致。
- 耗时：5.2s/个（22 个共 114s）。单次探针 4.9s 的分解：三视口 0.85s（含启动浏览器）/ 性能读数 1.26s / axe 双主题 0.31s / 键盘 40 次 Tab 0.04s / 7 条状态机（8 次重载）2.27s。
- 零件成本：浏览器启动 181ms、新开页+加载 61ms、注入 axe 72ms、`axe.run` 30~71ms、复用浏览器开 5 个页 248ms（约 50ms/页）。
  → 4.9s 里绝大部分是我自己写的固定 settle 等待和 40 帧 rAF 采样，不是工具开销。要吞吐可以压到 1s 以内。
- 作弊测试 `hacks.js`（7 个页，`MUT_FILE=./hacks.js OUT_TAG=hacks node run_mutations.js`）：第一版挡 5/7。
  补两条判据（axe 的 incomplete 里对比度一族也当闸；状态机断言加「前置态 + 往返」）后 6/7，22 变异全量回归仍 22/22。
  仍漏的 K4（`font-size:0` 真文字 + `::after` 画回屏幕）是 axe 的结构性盲区：实测 `violations:[] incomplete:[]`，
  连 needs review 都不报（axe issue #2680，至今 open）。只能靠代码闸或 OCR/VLM。

