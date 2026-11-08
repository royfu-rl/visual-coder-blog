# visual-coder-blog

参照 kat-coder-rl-blog / critic-blog 的单文件博客：md → build.py → index.html。

## 目录

- `overview.md`：Overview
- `env/env.md`：Environment（Web / 3D / Game 三视图，由脚本生成，别手改）
- `env/{web,3d,game}.md`：各视图的正文，按 `<!--ANALYSIS-->` 等标记切段；写作规范见 `/mmu_mllm_hdd_4/deep-research/deep-research/reference/write.md`
- `alg/alg.md`：Algorithm（五视图，由脚本生成，别手改）
- `middle_processing/vc_data/draft_{overview,tasks,verifier,training,domains}.md`：Algorithm 各视图的正文，改这里
- `middle_processing/vc_data/01~20_*.md`：Algorithm 的调研笔记；`90`、`91`、`92` 是本地实验与核验记录
- `scripts/gen_alg_page.py`：draft_*.md → alg/alg.md（加视图切换与每视图的目录）
- `scripts/vc_verifier/`：可验证任务的原型（three.js / Blender / 图表 / Web 四条线），见该目录 README
- `alg/demos/`：Algorithm 页的可交互 demo 与它们的静态资源
- `eval/eval.md`：Evaluation
- `middle_processing/`：调研原始表与元数据（benchmarks.md、pipelines.md、*_meta*.json、orgs_*.json、deep_*.md），改数据改这里
- `scripts/gen_env_page.py`：原始表 → env/env.md
- `template.html` + `assets/`：页面骨架（来自 critic-blog）与 marked / KaTeX

## 重建

```bash
python3 scripts/gen_env_page.py   # 改了 middle_processing/ 的 env 原始表时
python3 scripts/gen_alg_page.py   # 改了 middle_processing/vc_data/draft_*.md 时
python3 build.py                  # 任意 md 改动后
```

深链：`index.html#env/web`、`#env/3d`、`#env/game`；Algorithm 五视图为 `#alg`（切换在页内）

