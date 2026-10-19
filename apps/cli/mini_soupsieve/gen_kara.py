# Prints the data section at the end of mini_soupsieve.kara: the files
# under data/ (mk.PAGES and mk.JOBS), soupsieve's PSEUDO_SELECTORS
# sources, and the code point ranges whose unicodedata.bidirectional()
# is L, R or AL (Unicode 15.1, as Python 3.13 has it).
import os
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import mk  # noqa: E402
from soupsieve import css_parser  # noqa: E402


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
        elif ord(ch) < 0x20 or ord(ch) == 0x7F:
            out.append("\\u{%x}" % ord(ch))
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


files = [("pages/" + n, t) for n, t in mk.PAGES.items()]
files.append(("jobs.tsv", mk.JOBS))
for i, (name, text) in enumerate(files):
    lines = text.split("\n")
    parts = [line + "\n" for line in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
    chunks = [parts[k:k + 150] for k in range(0, len(parts), 150)] or [[]]
    for c, chunk in enumerate(chunks):
        print("fn file_%d_%d(s: mut ref String) {" % (i, c))
        for p in chunk:
            print("    s.push_str(%s);" % lit(p))
        print("}")
        print()
    print("fn file_%d() -> String {" % i)
    print("    let mut s = String.new();")
    for c in range(len(chunks)):
        print("    file_%d_%d(mut s);" % (i, c))
    print("    s")
    print("}")
    print()
print("fn data_files() -> Vec[(String, String)] {")
print("    let mut v: Vec[(String, String)] = Vec.new();")
for i, (name, _) in enumerate(files):
    print("    v.push((%s.to_string(), file_%d()));" % (lit(name), i))
print("    v")
print("}")
print()

print("// CSSParser.PSEUDO_SELECTORS: the source and parse flags of each.")
print("fn pseudo_source(name: ref String) -> Option[(String, i64)] {")
for k, v in css_parser.CSSParser.PSEUDO_SELECTORS.data.items():
    print("    if name == %s {" % lit(k))
    print("        return Some((%s.to_string(), %d));" % (lit(v.selector), v.flags))
    print("    }")
print("    None")
print("}")
print()

runs = []
for c in range(0x110000):
    k = {"L": 1, "R": 2, "AL": 3}.get(unicodedata.bidirectional(chr(c)), 0)
    if runs and runs[-1][2] == k and runs[-1][1] == c - 1:
        runs[-1][1] = c
    else:
        runs.append([c, c, k])
runs = [r for r in runs if r[2]]
print("// start-end-class runs, hex, for bidi_class().")
print("fn bidi_text() -> String {")
print("    let mut s = String.new();")
for k in range(0, len(runs), 40):
    print("    s.push_str(%s);" % lit("".join("%x-%x-%d," % tuple(r) for r in runs[k:k + 40])))
print("    s")
print("}")
print()
print("""fn hex_value(s: ref String) -> i64 {
    let mut n = 0;
    for c in s.chars() {
        n = n * 16 + (if c >= 'a' { c as i64 - 87 } else { c as i64 - 48 });
    }
    n
}

fn bidi_table() -> Vec[(i64, i64, i64)] {
    let mut out: Vec[(i64, i64, i64)] = Vec.new();
    for run in bidi_text().split(",") {
        if run.is_empty() {
            continue;
        }
        let p: Vec[String] = run.split("-").map(|x| x.to_string()).collect();
        out.push((hex_value(p[0]), hex_value(p[1]), hex_value(p[2])));
    }
    out
}""")
