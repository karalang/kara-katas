# Prints the Kara functions that hold data/ (as mk.py writes it), for
# mini_htmlparser.kara's data section: each file's path under data/ and its
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

# html.entities.html5, the table html.unescape reads.
from html.entities import html5


def ulit(s):
    out = []
    for ch in s:
        if ch in "\\\"" or not (32 <= ord(ch) < 127):
            out.append("\\u{%x}" % ord(ch))
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


print()
# One function per 250 names: under mir-llvm-asan a function's build time
# grows with the square of its length (B-2026-10-18-29).
names = sorted(html5)
parts = [names[k:k + 250] for k in range(0, len(names), 250)]
print("// html.entities.html5: each name (with or without its ';') and its text.")
print("fn html5_entities() -> Map[String, String] {")
print("    let mut m: Map[String, String] = Map.new();")
for k in range(len(parts)):
    print("    add_entities_%d(mut m);" % k)
print("    m")
print("}")
for k, part in enumerate(parts):
    print()
    print("fn add_entities_%d(m: mut ref Map[String, String]) {" % k)
    for name in part:
        print("    m.insert(%s.to_string(), %s.to_string());" % (ulit(name), ulit(html5[name])))
    print("}")
