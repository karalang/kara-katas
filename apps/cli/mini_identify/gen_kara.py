# Prints the Kara tables_text() (the identify lookup tables) and jobs_text()
# (data/jobs.tsv) functions for mini_identify.kara's data section.
import sys

sys.path.insert(0, "vendor")
from identify import extensions as e  # noqa: E402
from identify import interpreters as it  # noqa: E402


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


def rows(kind, table):
    lines = []
    for key in sorted(table):
        tags = " ".join(sorted(table[key]))
        assert "\t" not in key and "\n" not in key, repr(key)
        assert "\t" not in tags and "\n" not in tags, repr(tags)
        lines.append(kind + "\t" + key + "\t" + tags)
    return lines


print("// identify lookup tables (EXTENSIONS, EXTENSIONS_NEED_BINARY_CHECK,")
print("// NAMES, INTERPRETERS), one `kind<TAB>key<TAB>sorted tags` row each.")
print("fn tables_text() -> String {")
print("    let mut s = String.new();")
for kind, table in (
    ("E", e.EXTENSIONS),
    ("B", e.EXTENSIONS_NEED_BINARY_CHECK),
    ("N", e.NAMES),
    ("I", it.INTERPRETERS),
):
    for row in rows(kind, table):
        print("    s.push_str(%s);" % lit(row + "\n"))
print("    s")
print("}")

print("// data/jobs.tsv, as mk.py writes it.")
print("fn jobs_text() -> String {")
print("    let mut s = String.new();")
for line in open("data/jobs.tsv", encoding="utf-8").read().splitlines():
    print("    s.push_str(%s);" % lit(line + "\n"))
print("    s")
print("}")
