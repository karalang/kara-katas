# Rewrites the data section at the end of mini_pandas_io.kara, after the MARK
# line: the functions that hold data/ (as mk.py writes it), each file's
# path under data/ and its text, so the program carries its own inputs.
# Anything outside printable ASCII is written as a \u{...} escape. No
# data function gets more than about 200 lines.
#
# Run from this directory: python3 -I -B gen_kara.py

import os

BS = chr(92)
MARK = "\n// ============================================================ data\n"


def lit(s):
    out = []
    for ch in s:
        if ch == BS:
            out.append(BS + BS)
        elif ch == '"':
            out.append(BS + '"')
        elif ch == "\n":
            out.append(BS + "n")
        elif ch == "\r":
            out.append(BS + "r")
        elif ch == "\t":
            out.append(BS + "t")
        elif " " <= ch <= "~":
            out.append(ch)
        else:
            out.append(BS + "u{%x}" % ord(ch))
    return '"' + "".join(out) + '"'


def read(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return fh.read()


src = read("mini_pandas_io.kara")
src = src[:src.index(MARK)]

names = []
for root, dirs, files in os.walk("data"):
    for f in files:
        names.append(os.path.relpath(os.path.join(root, f), "data"))
names.sort()

chunks = [[]]
for n in names:
    text = read(os.path.join("data", n))
    body = ["    let mut t = String.new();"]
    for line in text.splitlines(keepends=True):
        body.append("    t.push_str(%s);" % lit(line))
    body.append("    v.push(DataFile { path: %s.to_string(), body: t });" % lit(n))
    if len(chunks[-1]) + len(body) > 200 and chunks[-1]:
        chunks.append([])
    chunks[-1].extend(body)

d = ["", "// The files under data/, in path order.",
     "fn data_files() -> Vec[DataFile] {",
     "    let mut v: Vec[DataFile] = Vec.new();"]
for k in range(len(chunks)):
    d.append("    data_part_%d(mut v);" % k)
d += ["    v", "}"]
for k, body in enumerate(chunks):
    d += ["", "fn data_part_%d(v: mut ref Vec[DataFile]) {" % k] + body + ["}"]
with open("mini_pandas_io.kara", "w", encoding="utf-8", newline="") as fh:
    fh.write(src + MARK + "\n".join(d) + "\n")
