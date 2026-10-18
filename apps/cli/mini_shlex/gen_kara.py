# Prints the Kara functions that hold data/ (as mk.py writes it), for
# mini_shlex.kara's data section: the tree's paths (each file holds its own
# path and a newline; a path ending in "/" is an empty directory) and
# jobs.tsv.
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

paths = []
for root, dirs, files in os.walk("data/tree"):
    rel = os.path.relpath(root, "data/tree")
    if not dirs and not files:
        paths.append(rel + "/")
    for f in files:
        paths.append(os.path.normpath(os.path.join(rel, f)))
paths.sort()
print("// The tree's paths under data/tree. A file holds its path and a")
print("// newline; a path ending in a slash is an empty directory.")
print("fn tree_paths() -> Vec[String] {")
print("    let mut v: Vec[String] = Vec.new();")
for p in paths:
    print("    v.push(%s.to_string());" % lit(p))
print("    v")
print("}")
print()
print("fn jobs_text() -> String {")
print("    let mut s = String.new();")
for line in open("data/jobs.tsv", encoding="utf-8").read().splitlines():
    print("    s.push_str(%s);" % lit(line + "\n"))
print("    s")
print("}")
