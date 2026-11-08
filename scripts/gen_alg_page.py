#!/usr/bin/env python3
"""middle_processing/vc_data/draft_*.md -> alg/alg.md

每个 draft 是一个视图的正文（只含 ## 级标题和锚点），这里补上视图切换、每视图的 TOC 和页面主标题。
加新视图只要在 VIEWS 里加一行。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'middle_processing/vc_data'
OUT = ROOT / 'alg/alg.md'

VIEWS = [
    ('overview', 'Overview', 'ov'),
    ('tasks',    'Tasks',    'tk'),
    ('verifier', 'Verifier', 'vf'),
    ('training', 'Training', 'tr'),
    ('domains',  'Domains',  'dm'),
]

HEAD = """# Algorithm

<style>
/* 窄屏下视图切换横向可滚，否则第五个视图会被截掉（与 Market 页同一处理） */
@media (max-width:720px){
  .doc .view-switch{display:flex;max-width:100%;overflow-x:auto;scrollbar-width:none}
  .doc .view-switch button{white-space:nowrap;padding:7px 14px;flex:none}
  .doc table{display:block;overflow-x:auto}
}
</style>

<div class="view-switch"></div>

"""


def toc(body, prefix):
    items = []
    for m in re.finditer(r'^## (\d+)\s+(.+)$', body, re.M):
        items.append(f'<li class="l2"><a href="#{prefix}-{m.group(1)}">'
                     f'<span class="num">{m.group(1)}</span> {m.group(2).strip()}</a></li>')
    return '<nav class="toc view-toc"><h2>Contents</h2><ul>' + ''.join(items) + '</ul></nav>'


def main():
    parts = [HEAD]
    for name, label, prefix in VIEWS:
        f = SRC / f'draft_{name}.md'
        if not f.exists():
            print(f'  跳过 {name}（草稿还没写）')
            continue
        body = f.read_text().strip()
        parts.append(f'<div class="env-view" data-view="{name}" data-label="{label}">\n\n'
                     + toc(body, prefix) + '\n\n' + body + '\n\n</div>\n')
        print(f'  收 {name}: {len(body)} 字符, {body.count(chr(10) + "## ") + body.startswith("## ")} 节')
    OUT.write_text('\n'.join(parts))
    print(f'写出 {OUT} ({OUT.stat().st_size} 字节)')


if __name__ == '__main__':
    main()

