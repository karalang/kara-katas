# Prints the Kara functions that hold data/ (as mk.py writes it), for
# mini_tabulate.kara's data section: each file's path under data/ and its
# text. No function gets more than about 200 lines.
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
        elif ord(ch) < 0x20:
            out.append("\\u{%x}" % ord(ch))
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


names = []
for root, dirs, files in os.walk("data"):
    for f in files:
        names.append(os.path.relpath(os.path.join(root, f), "data"))
names.sort()

chunks = [[]]
for n in names:
    s = open(os.path.join("data", n), encoding="utf-8").read()
    body = ["    let mut t = String.new();"]
    for line in s.splitlines(keepends=True):
        body.append("    t.push_str(%s);" % lit(line))
    body.append("    v.push(DataFile { path: %s.to_string(), body: t });" % lit(n))
    if len(chunks[-1]) + len(body) > 200 and chunks[-1]:
        chunks.append([])
    chunks[-1].extend(body)

print("// The files under data/, in path order.")
print("fn data_files() -> Vec[DataFile] {")
print("    let mut v: Vec[DataFile] = Vec.new();")
for k in range(len(chunks)):
    print("    data_part_%d(mut v);" % k)
print("    v")
print("}")
for k, body in enumerate(chunks):
    print()
    print("fn data_part_%d(v: mut ref Vec[DataFile]) {" % k)
    for line in body:
        print(line)
    print("}")
