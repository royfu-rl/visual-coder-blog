# 数据集样例组件规范

给 visual-coder-blog 细讲（2.4 Deep Dives）里有公开下载的数据集，各做一个「数据样例」组件：抓 2–3 条真实样本，展示数据长什么样。

## 1. 取样本

- 优先用 HF datasets-server：
  - `https://datasets-server.huggingface.co/splits?dataset=<id>` 看 config / split
  - `https://datasets-server.huggingface.co/rows?dataset=<id>&config=<c>&split=<s>&offset=<n>&length=3`
  - 图片字段返回的是带签名的临时 URL，**必须立即下载到本地**
- 数据不在 HF（GitHub 仓库、zip）就抓仓库里的样例文件；实在拿不到就写 `samples/<slug>.html` 为一句说明（见第 4 节），不要编造
- 网络：`curl -x http://oversea-squid1.jp.txyun:11080`
- 样本挑「有代表性、画面完整」的，可以用 offset 跳过前几条
- **不要下载整个数据集**，只取需要的几条

## 2. 本地素材

- 图片放 `/mmu_mllm_hdd_4/deep-research/visual-coder-blog/assets/samples/<slug>/<n>.jpg`（或 .png）
- 每张 ≤ 300KB：用 `python3 -c "from PIL import Image"` 缩到长边 ≤ 900px、JPEG quality 85
- 3D 数据（mesh / 点云）：不要放原始 3D 文件，放数据集自带的渲染图或缩略图；没有就只展示文本字段与元数据
- 用 Read 打开每张图确认内容正确

## 3. 组件 HTML

写到 `/mmu_mllm_hdd_4/deep-research/visual-coder-blog/middle_processing/samples/<slug>.html`，结构固定：

```html
<div class="ds-demo"><div class="ds-head"><b>数据样例</b> · <a href="HF或仓库链接">数据集id</a> · 总规模一句话 · 展示字段：image、text</div><div class="ds-grid"><div class="ds-card"><img class="ds-img" src="../assets/samples/<slug>/1.jpg" alt="..."><div class="ds-meta">一句中文说明这条样本（例如 llm_generated_idea 的中文概括，或题目/类别）</div><details class="ds-code"><summary>text（HTML，共 N 行，展示前 60 行）</summary><pre>转义后的内容</pre></details></div><div class="ds-card">…</div></div></div>
```

硬性要求（违反会让页面渲染出错）：

1. **整个组件写在一行里**，文件内不能有任何换行或空行（markdown 遇到空行会截断 HTML 块）
2. `<pre>` 里的内容：
   - 先做 HTML 转义：`&`→`&amp;`、`<`→`&lt;`、`>`→`&gt;`
   - 换行写成 `&#10;`
   - `$` 写成 `&#36;`（页面会把 `$...$` 当公式）
   - `~` 写成 `&#126;`（生成器会把 `~` 全局替换）
   - `|` 写成 `&#124;`
   - 超过 60 行截断，末尾加一行 `…（截断，原文共 N 行）`
3. 文本字段（caption、问答、指令）也放进 `<details class="ds-code">`，同样转义
4. 图片路径一律写 `../assets/samples/<slug>/...`（相对 env/ 目录）
5. 没有图片的数据集（纯文本 / 代码）：去掉 `<img>`，卡片里只放 `ds-meta` + `ds-code`
6. 拿不到样本时，文件内容写成一行：`<div class="ds-demo"><div class="ds-head"><b>数据样例</b> · 未能取到样本：原因一句话</div></div>`

## 4. 自检

- `python3 -c "s=open(f).read(); assert '\n' not in s.strip() and '$' not in s and '~' not in s"`
- 用 Read 打开每张图片
- 在最终回复里列出：每个数据集用了哪个 config/split/offset、每条样本一句话说明

