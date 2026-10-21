# Prints mini_pyhcl.kara's generated section: the master regexes PLY's
# lex builds for pyhcl's Lexer in each state, with the rule each group
# belongs to; the LALR tables PLY's yacc builds for HclParser (the copy in
# hcl/, with the ply/ it bundles); and the files under data/ (as mk.py
# writes them). No function gets more than about 200 lines.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

from hcl.lexer import Lexer  # noqa: E402
from hcl.parser import HclParser  # noqa: E402


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
        elif ch == "\f":
            out.append("\\u{c}")
        elif ch == "\v":
            out.append("\\u{b}")
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


def text_fn(name, lines):
    out = ["fn %s() -> String {" % name, "    let mut t = String.new();"]
    for fn in chunked(name + "_part", lines):
        out.append("    %s(mut t);" % fn)
    out.append("    t")
    out.append("}")
    return out


lx = Lexer().lex
lex_lines = []
for state, rules in lx.lexstatere.items():
    # one master regex per state: PLY only splits it when re refuses it
    assert len(rules) == 1, state
    regex, index = rules[0]
    errorf = lx.lexstateerrorf.get(state)
    eoff = lx.lexstateeoff.get(state)
    lex_lines.append("S\t%s\t%d\t%s\t%s\t%s\n" % (
        state, regex.flags, lx.lexstateignore.get(state, "").encode("unicode_escape").decode("ascii"),
        errorf.__name__ if errorf else "-", eoff.__name__ if eoff else "-"))
    lex_lines.append("X\t%s\n" % regex.pattern)
    for i, entry in enumerate(index):
        if entry is not None:
            func, ty = entry
            lex_lines.append("I\t%d\t%s\t%s\n" % (i, func.__name__ if func else "-", ty or "-"))

p = HclParser().yacc
par_lines = []
for pr in p.productions:
    par_lines.append("P %s %d %s%s\n" % (pr.name, pr.len, pr.func or "-", "".join(" " + x for x in pr.prod)))
for st in sorted(p.action):
    # in the table's own order, which p_error's "expected" list shows
    par_lines.append("A %d %s\n" % (st, " ".join("%s=%d" % (t, a) for t, a in p.action[st].items())))
for st in sorted(p.goto):
    if p.goto[st]:
        par_lines.append("G %d %s\n" % (st, " ".join("%s=%d" % (t, a) for t, a in p.goto[st].items())))
for st in sorted(p.defaulted_states):
    par_lines.append("D %d %d\n" % (st, p.defaulted_states[st]))

out = []
out.append("// ------------------------------------------------------------ generated")
out.append("")
out.append("// PLY's lexer for each state: S name, flags, ignored characters, error")
out.append("// and eof functions; X the master regex; I a group and its rule.")
out.extend(text_fn("lex_tables", lex_lines))
out.append("")
out.append("// PLY's LALR tables: productions, actions, gotos, defaulted states.")
out.extend(text_fn("parse_tables", par_lines))
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
