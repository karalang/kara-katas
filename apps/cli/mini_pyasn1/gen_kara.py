# Prints the Kara functions that hold data/ (as mk.py writes it), for
# mini_pyasn1.kara's data section: each file's path under data/
# and its contents (hex for the binary ones). No function gets more than
# about 200 lines; a longer file is filled in by helper functions.
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
    # data/out is what the programs write.
    if root == "data":
        dirs[:] = [d for d in dirs if d != "out"]
    for f in files:
        names.append(os.path.relpath(os.path.join(root, f), "data"))
names.sort()

chunks = [[]]
helpers = []
for n in names:
    b = open(os.path.join("data", n), "rb").read()
    text = is_text(b)
    if text:
        pieces = b.decode("utf-8").splitlines(keepends=True)
    else:
        h = b.hex()
        pieces = [h[i:i + 96] for i in range(0, len(h), 96)]
    pushes = ["    t.push_str(%s);" % lit(x) for x in pieces]
    body = ["    let mut t = String.new();"]
    if len(pushes) > 190:
        for i in range(0, len(pushes), 190):
            k = len(helpers)
            helpers.append(pushes[i:i + 190])
            body.append("    data_text_%d(mut t);" % k)
    else:
        body.extend(pushes)
    body.append("    v.push(DataFile { path: %s.to_string(), hex: %s, body: t });"
                % (lit(n), "false" if text else "true"))
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
for k, body in enumerate(helpers):
    print()
    print("fn data_text_%d(t: mut ref String) {" % k)
    for line in body:
        print(line)
    print("}")
