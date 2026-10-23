#!/usr/bin/env python3
r"""Appends a jobs_text() function to mini_textfsm.kara carrying data/jobs.tsv
verbatim, so the kata reads no files at run time. Unlike the polyline base this
must PRESERVE blank lines — a template's Value/State separator and an input's
record-terminating blank line are significant — so empty lines are emitted as
`s.push_str("\n")` rather than skipped. Run after mk.py; idempotent."""
MARK = "\n// data/jobs.tsv, as mk.py writes it.\n"

with open("data/jobs.tsv", encoding="utf-8") as fh:
    content = fh.read()
lines = content.split("\n")
# Drop the single phantom trailing "" from the file's final newline; keep every
# internal blank line.
if lines and lines[-1] == "":
    lines.pop()

with open("mini_textfsm.kara", encoding="utf-8") as fh:
    src = fh.read()

cut = src.find(MARK)
if cut != -1:
    src = src[:cut]
src = src.rstrip("\n") + "\n"

body = [MARK, "fn jobs_text() -> String {\n", "    let mut s = String.new();\n"]
for ln in lines:
    esc = ln.replace("\\", "\\\\").replace('"', '\\"').replace("\t", "\\t")
    body.append('    s.push_str("%s\\n");\n' % esc)
body.append("    s\n}\n")

with open("mini_textfsm.kara", "w", encoding="utf-8") as fh:
    fh.write(src + "".join(body))
