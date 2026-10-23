#!/usr/bin/env python3
r"""Appends a jobs_text() function to mini_geohash.kara carrying data/jobs.tsv
verbatim, so the kata reads no files at run time. Preserves blank lines (a
list/code body can span lines) by emitting empty lines as s.push_str("\n").
Run after mk.py; idempotent. Run: python3 -s -P -B gen_kara.py"""
MARK = "\n// data/jobs.tsv, as mk.py writes it.\n"

with open("data/jobs.tsv", encoding="utf-8") as fh:
    content = fh.read()
lines = content.split("\n")
# Drop the single phantom trailing "" from the file's final newline; keep every
# internal blank line.
if lines and lines[-1] == "":
    lines.pop()

with open("mini_geohash.kara", encoding="utf-8") as fh:
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

with open("mini_geohash.kara", "w", encoding="utf-8") as fh:
    fh.write(src + "".join(body))
