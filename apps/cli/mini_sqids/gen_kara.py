#!/usr/bin/env python3
"""Appends jobs_text() and blocklist_text() to mini_sqids.kara, carrying
data/jobs.tsv and data/blocklist.txt verbatim, so the kata reads no files at
run time. Run after mk.py; idempotent. Run: python3 -s -P -B gen_kara.py"""
MARK = "\n// data/jobs.tsv and data/blocklist.txt, as mk.py writes them.\n"


def emit(name, path):
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    body = ["fn %s() -> String {\n" % name, "    let mut s = String.new();\n"]
    for ln in lines:
        esc = ln.replace("\\", "\\\\").replace('"', '\\"').replace("\t", "\\t")
        body.append('    s.push_str("%s\\n");\n' % esc)
    body.append("    s\n}\n")
    return "".join(body)


with open("mini_sqids.kara", encoding="utf-8") as fh:
    src = fh.read()
cut = src.find(MARK)
if cut != -1:
    src = src[:cut]
src = src.rstrip("\n") + "\n"

with open("mini_sqids.kara", "w", encoding="utf-8") as fh:
    fh.write(src + MARK + emit("jobs_text", "data/jobs.tsv") + "\n"
             + emit("blocklist_text", "data/blocklist.txt"))
