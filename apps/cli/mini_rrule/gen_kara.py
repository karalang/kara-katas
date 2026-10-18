# Prints the Kara functions that hold data/ (as mk.py writes it), for
# mini_rrule.kara's data section: each file's path under data/ and its
# text (or its bytes as hex, for a binary file). No function gets more than
# about 200 lines.
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
        names.append(os.path.relpath(os.path.join(root, f), "data"))
names.sort()

chunks = [[]]
for n in names:
    b = open(os.path.join("data", n), "rb").read()
    body = []
    if is_text(b):
        body.append("    let mut t = String.new();")
        for line in b.decode("utf-8").splitlines(keepends=True):
            body.append("    t.push_str(%s);" % lit(line))
        body.append("    v.push(DataFile { path: %s.to_string(), hex: false, body: t });" % lit(n))
    else:
        h = b.hex()
        body.append("    let mut t = String.new();")
        for i in range(0, len(h), 96):
            body.append("    t.push_str(%s);" % lit(h[i:i + 96]))
        body.append("    v.push(DataFile { path: %s.to_string(), hex: true, body: t });" % lit(n))
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
