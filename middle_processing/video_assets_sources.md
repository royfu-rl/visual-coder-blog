# Video 视图 · 下载素材来源（可复现）

全部观测于 2026-10-12；配图经 PIL 缩到长边 ≤1000px、≤300KB；样例图缩到长边 ≤900px、JPEG q85。

## 细讲配图（assets/papers/）

| 文件 | 原始下载地址 |
|---|---|
| `code2video-fig.png` | https://arxiv.org/html/2510.01174v1/approach.png |
| `theoremexplainagent-fig.png` | https://arxiv.org/html/2502.19400v2/teaser_v3.png |
| `paper2video-fig.png` | https://arxiv.org/html/2510.05096v2/teaser.png |
| `omnilottie-fig.png` | https://arxiv.org/html/2603.02138v1/teaser_v2.png |
| `keyframer-fig.png` | https://arxiv.org/html/2402.06071v2/fig-1.png |
| `vectorprism-fig.png` | https://yeolj00.github.io/research/vector-prism/assets/method_main.png（arXiv 2512.14336 的 HTML 404，取自项目页） |
| `vanim-fig.png` | https://arxiv.org/html/2605.01517v1/teaser.png |
| `manimagent-fig.png` | https://arxiv.org/html/2606.30296v2/pipeline.png |
| `simuscene-fig.png` | https://arxiv.org/html/2602.10840v2/imgs/data_pipeline.png（备用，未在细讲引用） |
| `pptagent-fig.png` | https://arxiv.org/html/2501.03936v2/fig1.png（备用，未在细讲引用） |

## 数据样例（assets/samples/ + middle_processing/samples/）

| slug | 来源 | config / split / offset | 字段 |
|---|---|---|---|
| `omnilottie` | HF `OmniLottie/MMLottie-2M` | Lottie / train / 0,1,2 | 渲染预览图 + lottie_json |
| `code2video` | HF `YanzheChen/MMMC` | default / train / 0,30,33 | 主题、学科（纯文本，无图） |
| `theoremexplainagent` | HF `TIGER-Lab/TheoremExplainBench` | default / train / 0,80,160 | 定理名、描述、学科、难度（纯文本） |
| `paper2video` | HF `ZaynZhu/Paper2Video`（data/paper2video.xlsx 元数据表） | 101 行 / 取 3 | 论文、会议、年份（视频为外链，无静帧） |
| `keyframer` | GitHub `apple/ml-keyframer`（components/defaultSVGs.js + 生成提示词） | 示例 SVG galaxy/rocket | SVG 源码 + CSS 生成提示词（SVG 渲染为 png） |
| `vectorprism` | GitHub `YeolJ00/Vector-Prism`（svg/ + svg/test.jsonl） | bunny/windmill/christmas-tree | 输入 SVG + 自然语言动画指令（SVG 渲染为 png） |

