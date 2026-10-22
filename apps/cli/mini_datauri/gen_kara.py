#!/usr/bin/env python3
r"""Appends a jobs_text() function to mini_datauri.kara carrying data/jobs.tsv
verbatim (tabs as \t, newlines as \n), so the kata is self-contained and reads
no files at run time. Run after mk.py; idempotent (it strips any prior copy)."""
MARK = "\n// data/jobs.tsv, as mk.py writes it.\n"

with open("data/jobs.tsv", encoding="utf-8") as fh:
    lines = fh.read().split("\n")

with open("mini_datauri.kara", encoding="utf-8") as fh:
    src = fh.read()

cut = src.find(MARK)
if cut != -1:
    src = src[:cut]
src = src.rstrip("\n") + "\n"

body = [MARK, "fn jobs_text() -> String {\n", "    let mut s = String.new();\n"]
for ln in lines:
    if ln == "":
        continue
    esc = ln.replace("\\", "\\\\").replace('"', '\\"').replace("\t", "\\t")
    body.append('    s.push_str("%s\\n");\n' % esc)
body.append("    s\n}\n")

with open("mini_datauri.kara", "w", encoding="utf-8") as fh:
    fh.write(src + "".join(body))
