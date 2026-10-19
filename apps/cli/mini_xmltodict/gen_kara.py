# Prints the Kara functions that hold data/ (as mk.py writes it), for
# mini_xmltodict.kara's data section: each file's path under data/ and, for
# a binary one, its bytes as hex.
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

# Each file's text is pushed by helpers of at most 180 lines, so no
# function gets long however big the file is.
print("// The files under data/, in path order.")
print("fn data_files() -> Vec[DataFile] {")
print("    let mut v: Vec[DataFile] = Vec.new();")
helpers = []
for k, n in enumerate(names):
    b = open(os.path.join("data", n), "rb").read()
    if is_text(b):
        pieces = [lit(line) for line in b.decode("utf-8").splitlines(keepends=True)]
        hexed = "false"
    else:
        h = b.hex()
        pieces = [lit(h[i:i + 96]) for i in range(0, len(h), 96)]
        hexed = "true"
    print("    let mut t%d = String.new();" % k)
    for j in range(0, len(pieces), 180):
        name = "data_file_%d_%d" % (k, j // 180)
        print("    %s(mut t%d);" % (name, k))
        helpers.append((name, pieces[j:j + 180]))
    print("    v.push(DataFile { path: %s.to_string(), hex: %s, body: t%d });" % (lit(n), hexed, k))
print("    v")
print("}")
for name, body in helpers:
    print()
    print("fn %s(t: mut ref String) {" % name)
    for piece in body:
        print("    t.push_str(%s);" % piece)
    print("}")

