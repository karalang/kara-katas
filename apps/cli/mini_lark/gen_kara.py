# Prints two sections of mini_lark.kara:
# - the tables lark's grammar loader is built from, read from the copy of
#   lark in lark/ (load_grammar.TERMINALS, RULES, _TERMINAL_NAMES and
#   GRAMMAR_ERRORS), so the port parses grammars with lark's own grammar;
# - the functions that hold data/ (as mk.py writes it): each file's path
#   under data/ and its text. No function gets more than about 200 lines.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
os.chdir(HERE)

from lark import load_grammar  # noqa: E402


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
        elif ord(ch) < 32 or ord(ch) > 126:
            out.append("\\u{%x}" % ord(ch))
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


def tables():
    print("// ------------------------------------------------------------ tables")
    print()
    print("// lark's grammar of grammars, as gen_kara.py read it from")
    print("// lark/load_grammar.py.")
    print("fn meta_terminals() -> Vec[(String, String)] {")
    print("    let mut v: Vec[(String, String)] = Vec.new();")
    for k, p in load_grammar.TERMINALS.items():
        print("    v.push((%s.to_string(), %s.to_string()));" % (lit(k), lit(p)))
    print("    v")
    print("}")
    print()
    print("fn meta_rules() -> Vec[(String, Vec[String])] {")
    print("    let mut v: Vec[(String, Vec[String])] = Vec.new();")
    for k, alts in load_grammar.RULES.items():
        print("    let mut a: Vec[String] = Vec.new();")
        for x in alts:
            print("    a.push(%s.to_string());" % lit(x))
        print("    v.push((%s.to_string(), a));" % lit(k))
    print("    v")
    print("}")
    print()
    print("// _TERMINAL_NAMES: the names of punctuation terminals.")
    print("fn terminal_names() -> Vec[(String, String)] {")
    print("    let mut v: Vec[(String, String)] = Vec.new();")
    for k, n in load_grammar._TERMINAL_NAMES.items():
        print("    v.push((%s.to_string(), %s.to_string()));" % (lit(k), lit(n)))
    print("    v")
    print("}")
    print()
    print("fn grammar_error_examples() -> Vec[(String, Vec[String])] {")
    print("    let mut v: Vec[(String, Vec[String])] = Vec.new();")
    for label, exs in load_grammar.GRAMMAR_ERRORS:
        print("    let mut a: Vec[String] = Vec.new();")
        for x in exs:
            print("    a.push(%s.to_string());" % lit(x))
        print("    v.push((%s.to_string(), a));" % lit(label))
    print("    v")
    print("}")


def is_text(b):
    try:
        s = b.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return all(c >= " " or c in "\n\t" for c in s)


def datafiles():
    names = []
    for root, dirs, files in os.walk("data"):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), "data")
            if not rel.startswith("out" + os.sep):
                names.append(rel)
    names.sort()
    chunks = [[]]
    for n in names:
        b = open(os.path.join("data", n), "rb").read()
        assert is_text(b), n
        body = ["    let mut t = String.new();"]
        for line in b.decode("utf-8").splitlines(keepends=True):
            body.append("    t.push_str(%s);" % lit(line))
        body.append("    v.push(DataFile { path: %s.to_string(), body: t });" % lit(n))
        if len(chunks[-1]) + len(body) > 190 and chunks[-1]:
            chunks.append([])
        chunks[-1].extend(body)
    print("// ------------------------------------------------------------ data")
    print()
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


if sys.argv[1:] == ["tables"]:
    tables()
else:
    datafiles()
