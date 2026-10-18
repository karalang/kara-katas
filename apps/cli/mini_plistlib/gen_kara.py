# Prints the Kara functions that hold data/ (as mk.py writes it), for
# mini_plistlib.kara's data section: each text file's path under data/
# and its contents, each binary file's path and its bytes in hex, and
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
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


def is_text(b):
    if b.startswith(b"\xef\xbb\xbf"):
        return False
    try:
        s = b.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return all(c >= " " or c in "\n\r\t" for c in s)


names = []
for root, dirs, files in os.walk("data"):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), "data")
        if rel != "jobs.tsv":
            names.append(rel)
names.sort()
texts = []
blobs = []
for n in names:
    b = open(os.path.join("data", n), "rb").read()
    (texts if is_text(b) else blobs).append((n, b))
print("// The text files under data/, as (path, contents).")
print("fn text_files() -> Vec[(String, String)] {")
print("    let mut v: Vec[(String, String)] = Vec.new();")
for n, b in texts:
    text = b.decode("utf-8")
    print("    let mut t = String.new();")
    for line in text.splitlines(keepends=True):
        print("    t.push_str(%s);" % lit(line))
    print("    v.push((%s.to_string(), t));" % lit(n))
print("    v")
print("}")
print()
print("// The binary files under data/, as (path, hex of the bytes).")
print("fn binary_files() -> Vec[(String, String)] {")
print("    let mut v: Vec[(String, String)] = Vec.new();")
for n, b in blobs:
    h = b.hex()
    print("    let mut t = String.new();")
    for i in range(0, len(h), 96):
        print("    t.push_str(%s);" % lit(h[i:i + 96]))
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
