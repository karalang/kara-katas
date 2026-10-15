# Cross-check: every document and case renders exactly as markdown-it-py's
# CommonMark preset renders it (pip install markdown-it-py).
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from markdown_it import MarkdownIt
import md_render as m

md = MarkdownIt("commonmark")
bad = 0
items = list(m.DOCS.items()) + [(f"case {i:02}", c) for i, c in enumerate(m.CASES)]
for name, text in items:
    mine, _, _ = m.render_md(text)
    ref = md.render(text)
    if mine != ref:
        bad += 1
        print(f"MISMATCH {name}")
        a, b = mine.split("\n"), ref.split("\n")
        for x, y in zip(a, b):
            if x != y:
                print("  mine:      ", x)
                print("  markdown-it:", y)
                break
print(f"{len(items) - bad} of {len(items)} match markdown-it")
sys.exit(1 if bad else 0)
