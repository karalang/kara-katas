#!/usr/bin/env python3
"""Emits the Kara data functions for mini_hijri from the vendored library:
the Umm al-Qura MONTH_STARTS table (encoded as one digit per month-length
delta, delta-28) and the en/ar/bn month, Gregorian-month and day name tables.
Appended to mini_hijri.kara ahead of jobs_text().
"""
import sys

sys.path.insert(0, "vendor")
from hijri_converter import ummalqura as U  # noqa: E402
from hijri_converter import locales as L  # noqa: E402


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


def emit_vec(name, items):
    print(f"fn {name}() -> Vec[String] {{")
    print("    let mut v = Vec.new();")
    for it in items:
        print(f"    v.push({lit(it)}.to_string());")
    print("    v")
    print("}")
    print()


ms = U.MONTH_STARTS
deltas = [ms[i + 1] - ms[i] for i in range(len(ms) - 1)]
assert all(28 <= d <= 31 for d in deltas)
enc = "".join(str(d - 28) for d in deltas)

print(f"fn ms_base() -> i64 {{ {ms[0]} }}")
print()
print("fn ms_deltas() -> String {")
print("    let mut s = String.new();")
# chunk the encoded string so no single push_str line is enormous
for i in range(0, len(enc), 120):
    print(f"    s.push_str({lit(enc[i:i+120])});")
print("    s")
print("}")
print()

en = L.EnglishLocale
ar = L.ArabicLocale
bn = L.BengaliLocale
emit_vec("hmon_en", en.month_names)
emit_vec("hmon_ar", ar.month_names)
emit_vec("hmon_bn", bn.month_names)
emit_vec("gmon_en", en.gregorian_month_names)
emit_vec("gmon_ar", ar.gregorian_month_names)
emit_vec("day_en", en.day_names)
emit_vec("day_ar", ar.day_names)
