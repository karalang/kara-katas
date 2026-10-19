# Prints the Kara functions that hold the tables, for mini_wcwidth.kara's
# table section:
# - the Unicode versions wcwidth 0.2.13 knows, in its order;
# - its ZERO_WIDTH and WIDE_EASTASIAN tables for each version, and the
#   VS16_NARROW_TO_WIDE table, as text: ranges written "start-end" (or
#   "start" when they are one code point) in hex, split by commas;
# - the code points that Python 3.13's str.isprintable() says are not
#   printable, from U+0080 up, in the same form, for repr().
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wcwidth import list_versions  # noqa: E402
from wcwidth.table_vs16 import VS16_NARROW_TO_WIDE  # noqa: E402
from wcwidth.table_wide import WIDE_EASTASIAN  # noqa: E402
from wcwidth.table_zero import ZERO_WIDTH  # noqa: E402


def text(table):
    parts = []
    for a, b in table:
        parts.append("%x" % a if a == b else "%x-%x" % (a, b))
    return ",".join(parts)


def unprintable():
    out = []
    start = None
    for c in range(0x80, 0x110000):
        bad = not chr(c).isprintable()
        if bad and start is None:
            start = c
        if not bad and start is not None:
            out.append((start, c - 1))
            start = None
    if start is not None:
        out.append((start, 0x10FFFF))
    return out


def function(name, s):
    print("fn %s() -> String {" % name)
    print("    let mut t = String.new();")
    for i in range(0, len(s), 100):
        print('    t.push_str("%s");' % s[i:i + 100])
    print("    t")
    print("}")
    print()


vs = list_versions()
print("// The Unicode versions the tables are for, oldest first.")
print("fn versions() -> Vec[String] {")
print("    vec![%s]" % ", ".join('"%s".to_string()' % v for v in vs))
print("}")
print()
print("// The table text for version k of versions(): zero width when `zero`,")
print("// else wide.")
print("fn table_text(zero: bool, k: i64) -> String {")
print("    match (zero, k) {")
for z in [True, False]:
    for k in range(len(vs)):
        print("        (%s, %d) => %s_%d()," % ("true" if z else "false", k, "zero" if z else "wide", k))
print('        _ => String.new(),')
print("    }")
print("}")
print()
for k, v in enumerate(vs):
    function("zero_%d" % k, text(ZERO_WIDTH[v]))
    function("wide_%d" % k, text(WIDE_EASTASIAN[v]))
function("vs16_text", text(VS16_NARROW_TO_WIDE["9.0.0"]))
function("unprintable_text", text(unprintable()))
