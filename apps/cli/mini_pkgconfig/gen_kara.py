# Prints the Kara functions that hold data/ and jobs.tsv (as mk.py
# writes them), for mini_pkgconfig.kara's data section.
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
        elif ch == "\0":
            out.append("\\0")
        elif ord(ch) < 32 or ord(ch) == 127:
            out.append("\\u{%x}" % ord(ch))
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'

files = []
for root, dirs, names in os.walk("data"):
    dirs.sort()
    for n in sorted(names):
        files.append(os.path.join(root, n)[len("data/"):])
files.sort()
files.append("../jobs.tsv")
for i, n in enumerate(files):
    text = open(os.path.join("data", n)).read()
    print("fn file_%d() -> String {" % i)
    lines = text.split("\n")
    parts = [l + "\n" for l in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
    print("    let mut s = String.new();")
    for p in parts:
        print("    s.push_str(%s);" % lit(p))
    print("    s")
    print("}")
    print()
print("// Each input file's path under data/, and its text.")
print("fn data_files() -> Vec[(String, String)] {")
print("    let mut v: Vec[(String, String)] = Vec.new();")
for i, n in enumerate(files):
    print('    v.push((%s.to_string(), file_%d()));' % (lit(n), i))
print("    v")
print("}")
