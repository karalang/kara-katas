# Prints mini_jsonpath.kara's generated section: the parse tables PLY
# builds for jsonpath-ng's two grammars (the copy in jsonpath_ng/, with
# the ply/ it is built on), and the files under data/ (as mk.py writes
# them). No function gets more than about 200 lines.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

from jsonpath_ng.parser import JsonPathParser  # noqa: E402
from jsonpath_ng.ext.parser import ExtentedJsonPathParser  # noqa: E402


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
        elif ch == "{":
            out.append("{")
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


def table_lines(cls):
    p = cls().parser
    lines = []
    for pr in p.productions:
        lines.append("P %s %d %s" % (pr.name, pr.len, pr.func or "-"))
    for st in sorted(p.action):
        acts = p.action[st]
        lines.append("A %d %s" % (st, " ".join("%s=%d" % (t, a) for t, a in sorted(acts.items()))))
    for st in sorted(p.goto):
        gs = p.goto[st]
        if gs:
            lines.append("G %d %s" % (st, " ".join("%s=%d" % (t, a) for t, a in sorted(gs.items()))))
    for st in sorted(p.defaulted_states):
        lines.append("D %d %d" % (st, p.defaulted_states[st]))
    return lines


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
out.append("// PLY's LALR tables for the base grammar (jsonpath_ng.parser) and the")
out.append("// extended one (jsonpath_ng.ext.parser): productions, actions, gotos and")
out.append("// the states that reduce without reading a token.")
for name, cls in (("base_tables", JsonPathParser), ("ext_tables", ExtentedJsonPathParser)):
    fns = text_fn(name + "_text", [l + "\n" for l in table_lines(cls)])
    out.append("fn %s() -> String {" % name)
    out.append("    let mut t = String.new();")
    for f in fns:
        out.append("    %s(mut t);" % f)
    out.append("    t")
    out.append("}")
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
