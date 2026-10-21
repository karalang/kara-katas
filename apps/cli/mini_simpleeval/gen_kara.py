# Prints mini_simpleeval.kara's generated section: the files under
# data/ (as mk.py writes them). No function gets more than about 200
# lines.
import os

HERE = os.path.dirname(os.path.abspath(__file__))


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


FUNCS = []


def text_fn(name, lines):
    # one function per 200 lines, each appending to t
    parts = [lines[i:i + 190] for i in range(0, max(len(lines), 1), 190)]
    names = []
    for k, part in enumerate(parts):
        fn = "%s_%d" % (name, k)
        names.append(fn)
        body = ["fn %s(t: mut ref String) {" % fn]
        for line in part:
            body.append("    t.push_str(%s);" % lit(line))
        body.append("}")
        FUNCS.append("\n".join(body))
    return names


out = []
out.append("// ------------------------------------------------------------ generated")
out.append("")
names = []
for root, dirs, files in os.walk(os.path.join(HERE, "data")):
    for f in files:
        names.append(os.path.relpath(os.path.join(root, f), os.path.join(HERE, "data")))
names.sort()
out.append("// The files under data/, in path order.")
out.append("fn data_files() -> Vec[DataFile] {")
out.append("    let mut v: Vec[DataFile] = Vec.new();")
for n in names:
    with open(os.path.join(HERE, "data", n), encoding="utf-8") as f:
        text = f.read()
    stem = "file_" + "".join(c if c.isalnum() else "_" for c in n)
    fns = text_fn(stem, text.splitlines(keepends=True))
    out.append("    {")
    out.append("        let mut t = String.new();")
    for fn in fns:
        out.append("        %s(mut t);" % fn)
    out.append("        v.push(DataFile { path: %s.to_string(), body: t });" % lit(n))
    out.append("    }")
out.append("    v")
out.append("}")
out.append("")
print("\n".join(out))
print("\n\n".join(FUNCS))
