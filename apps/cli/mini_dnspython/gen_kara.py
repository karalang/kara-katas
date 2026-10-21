# Prints mini_dnspython.kara's generated section: dnspython's rdata type
# names (the RdataType members, aliases included, from the copy in dns/)
# and the files under data/ (as mk.py writes them). No function gets more
# than about 200 lines.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

import dns.rdatatype  # noqa: E402


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


def chunked(name, lines, per=180):
    names = []
    for k in range(0, max(len(lines), 1), per):
        fn = "%s_%d" % (name, k // per)
        names.append(fn)
        body = ["fn %s(t: mut ref String) {" % fn]
        body.extend("    t.push_str(%s);" % lit(line) for line in lines[k:k + per])
        body.append("}")
        FUNCS.append("\n".join(body))
    return names


out = []
out.append("// ------------------------------------------------------------ generated")
out.append("")
members = list(dns.rdatatype.RdataType.__members__.items())
out.append("// RdataType[name]: every member name, aliases included; -1 for none.")
out.append("fn type_by_name(s: ref String) -> i64 {")
parts = [members[k:k + 50] for k in range(0, len(members), 50)]
for k in range(len(parts)):
    out.append("    let v%d = type_by_name_%d(s);" % (k, k))
    out.append("    if v%d >= 0 {" % k)
    out.append("        return v%d;" % k)
    out.append("    }")
out.append("    -1")
out.append("}")
out.append("")
for k, part in enumerate(parts):
    out.append("fn type_by_name_%d(s: ref String) -> i64 {" % k)
    for name, value in part:
        out.append("    if s == %s {" % lit(name))
        out.append("        return %d;" % int(value))
        out.append("    }")
    out.append("    -1")
    out.append("}")
    out.append("")
out.append("// RdataType(value).name: the first member with the value; empty for none.")
out.append("fn type_name(v: i64) -> String {")
seen = set()
for name, value in members:
    if int(value) in seen:
        continue
    seen.add(int(value))
    out.append("    if v == %d {" % int(value))
    out.append("        return %s.to_string();" % lit(name))
    out.append("    }")
out.append("    String.new()")
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
    fns = chunked(stem, text.splitlines(keepends=True))
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
