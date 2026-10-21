# Prints mini_configobj.kara's generated section: the text and flags of
# every regex configobj and validate compile (from the copies in
# configobj/), and the files under data/ (as mk.py writes them). No
# function gets more than about 200 lines.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

import configobj  # noqa: E402
from configobj import validate  # noqa: E402


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


C = configobj.ConfigObj
V = validate.Validator
PATTERNS = [
    ("keyword", C._keyword),
    ("sectionmarker", C._sectionmarker),
    ("valueexp", C._valueexp),
    ("listvalueexp", C._listvalueexp),
    ("nolistvalue", C._nolistvalue),
    ("single_line_single", C._single_line_single),
    ("single_line_double", C._single_line_double),
    ("multi_line_single", C._multi_line_single),
    ("multi_line_double", C._multi_line_double),
    ("cp_keycre", configobj.ConfigParserInterpolation._KEYCRE),
    ("tp_keycre", configobj.TemplateInterpolation._KEYCRE),
    ("func_re", V._func_re),
    ("key_arg", V._key_arg),
    ("list_arg", V._list_arg),
    ("list_members", V._list_members),
    ("paramfinder", V._paramfinder),
]

out = []
out.append("// ------------------------------------------------------------ generated")
out.append("")
out.append("// The pattern text and flags of each regex configobj and validate compile.")
out.append("fn pattern_source(name: Str) -> (String, i64) {")
out.append("    let mut t = String.new();")
out.append("    let mut flags = 0;")
first = True
for name, pat in PATTERNS:
    fns = text_fn("pattern_" + name, pat.pattern.splitlines(keepends=True))
    out.append("    %s name == %s {" % ("if" if first else "} else if", lit(name)))
    first = False
    for fn in fns:
        out.append("        %s(mut t);" % fn)
    out.append("        flags = %d;" % pat.flags)
out.append("    }")
out.append("    (t, flags)")
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
    with open(os.path.join(HERE, "data", n), encoding="utf-8", newline="") as f:
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
