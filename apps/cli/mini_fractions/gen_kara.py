# Prints the Kara functions that hold data/ (as mk.py writes it), for
# mini_fractions.kara's data section: each file's path under data/ and its
# contents, and jobs.tsv.
import os

def lit(s):
    out = []
    for ch in s:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\t":
            out.append("\\t")
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'

names = []
for root, dirs, files in os.walk("data"):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), "data")
        if rel != "jobs.tsv":
            names.append(rel)
names.sort()
print("// The files under data/, as (path, contents).")
print("fn data_files() -> Vec[(String, String)] {")
print("    let mut v: Vec[(String, String)] = Vec.new();")
for n in names:
    text = open(os.path.join("data", n), encoding="utf-8").read()
    print("    let mut t = String.new();")
    for line in text.splitlines(keepends=True):
        print("    t.push_str(%s);" % lit(line))
    print("    v.push((%s.to_string(), t));" % lit(n))
print("    v")
print("}")
print()
print("fn jobs_text() -> String {")
print("    let mut s = String.new();")
for line in open("data/jobs.tsv", encoding="utf-8").read().splitlines():
    print("    s.push_str(%s);" % lit(line + "\n"))
print("    s")
print("}")
