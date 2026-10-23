#!/usr/bin/env python3
"""Writes data/: a dependency licence list and an allow-list, access rules
and users, and data/jobs.tsv, the script oracle.py and mini_boolean.kara
both replay. A job line is "job<TAB>title"; every other line is an
operation and its fields, with \\ \\t \\n \\r escapes in expression text.

Run: python3 -s -P -B mk.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def esc(s):
    return s.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r")


FILES = {
    "licences/packages.txt": """\
# name: SPDX licence expression, as a lock file's metadata reports it
requests: Apache-2.0
leftpad: MIT OR Apache-2.0
fontkit: (MIT AND OFL-1.1) OR GPL-3.0-or-later
cryptolib: Apache-2.0 AND (MIT OR BSD-3-Clause) AND ISC
jdk-shim: GPL-2.0-only WITH Classpath-exception-2.0
rustls: Apache-2.0 OR ISC OR MIT
spice: GPL-3.0-only
dual: MIT and mit-0 or (Zlib OR BSL-1.0)
nested: ((MIT OR Apache-2.0) AND (BSD-2-Clause OR BSD-3-Clause)) OR AGPL-3.0-only
oddball: MIT AND
twin: MIT OR MIT
bracketed: (Apache-2.0)
weird: MIT WITH
nolicence: NOASSERTION
alone: WITH foo
redundant: (MIT AND Apache-2.0) OR MIT
three: (Unlicense OR 0BSD) AND (MIT OR CC0-1.0) AND (Zlib OR ISC)
""",
    "licences/allowed.txt": "MIT\nApache-2.0\nBSD-2-Clause\nBSD-3-Clause\nISC\nZlib\n0BSD\nUnlicense\n",
    "access/rules.txt": """\
# action: who may do it
read: role:viewer or role:editor or role:admin
write: (role:editor or role:admin) and not suspended
delete: role:admin and mfa and not suspended
deploy: team:ops and mfa and (on_call or role:admin)
billing: role:admin and (team:finance or team:ops) and mfa
audit: role:auditor or role:admin and not role:admin
open: mfa or not mfa
closed: mfa and ~mfa
broken: role:admin and and mfa
legacy: role:admin & !suspended | role:root
""",
    "access/users.txt": """\
alice: role:admin mfa team:ops
bob: role:editor team:finance
carol: role:viewer
dave: role:editor suspended mfa
erin: team:ops mfa on_call
frank: role:root suspended
grace: role:auditor
heidi:
""",
}

JOBS = []


def job(title):
    JOBS.append(["job", title])


def step(*fields):
    JOBS.append([str(f) for f in fields])


# The examples of the library's README and user guide.
job("the documentation's examples")
for e in [
    "x & y",
    "(apple or banana and (orange or pineapple and (lemon or cherry)))",
    "x&~x", "x|~x", "x|x", "x&x", "x&(x|y)", "(x&y) | (x&~y)",
    "(((x|y)&z)|x&y)",
    "apple and (banana or orange)",
    "not a and not b and not (a and ba and c) and c or c",
]:
    step("parse", esc(e))
    step("simplify")
step("parse", "apple and (oranges or banana) and not banana")
step("simplify")
step("parse", "apple and (oranges or banana) and not banana", "s")
step("parse", "~(a&b)")
step("demorgan")
step("parse", "a & (b | c)")
step("cnf")
step("parse", "a | (b & c)")
step("dnf")
step("parse", "(a|b)&(c|d)")
step("dnf")

job("the grammar")
for e in [
    "a", "a and b", "a AND b", "a And b", "a * b", "a & b",
    "a or b", "a OR b", "a + b", "a | b",
    "not a", "NOT a", "~a", "!a", "~~a", "not not not a",
    "[a | b] & c", "(a)", "((a))", "(((a & b)))",
    "true", "TRUE", "1", "false", "False", "0", "none", "None",
    "a & 1", "a | 0", "~1", "~0", "1 & 0", "1|0",
    "a & b & c & d", "a | b | c", "a & b | c & d", "a | b & c | d",
    "a & ~b | ~c & d", "~(a | b) & c", "~a & (b | ~c)",
    "a.b & c:d & e_f & _g", "x1 & 2x & 42", "foo.bar.baz | a:b:c",
    "a\nand\tb\r\nor c", "  a   ", "café and thé",
    "apple AND NOT banana OR cherry",
    "a & (b | (c & (d | (e & f))))",
    "a or b and c or d and e and f or g",
]:
    step("parse", esc(e))
step("parse", "a & b | c & d", "s")
step("parse", "~(a & ~b) | ~~c", "s")

job("broken expressions")
for e in [
    "", "   ", "a b", "a &", "& a", "a & | b", "a | | b", "(a", "a)", "()",
    "(a & b))", "a & (b", "a (b)", "a & b c", "~", "~ & a", "a & ~",
    "(~)", "( & a)", "(a ~b)", "a & - b", "a $ b", "a ^ b", "a == b",
    "'a' & b", "a & \"b\"", "a\fb", "a & (b | c", "((a)", "a | b)",
    ")", "a & ()", "( | a & b", "x & (y z)", "1 1", "a ~", "(a)(b)",
    "~(a", "a & ~(b c)", "or", "and a", "a and or b",
]:
    step("parse", esc(e))

job("the tokenizer")
for e in [
    "a & b", "abc", "a.b:c_d", "not x or y", "(a|b)&c", "[x]", "1 0 true FALSE none",
    "  spaced  out  ", "x1 & 2x", "a\nb", "a - b", "_x & y_", "AnD oR NoT",
    "a&&b", "café",
]:
    step("tokens", esc(e))

job("simplifying")
for e in [
    "a & a", "a | a", "a & b & a", "a & ~a", "a | ~a", "a & 1", "a & 0",
    "a | 1", "a | 0", "~~a", "~~~a", "~(~a & ~b)", "~1", "~0", "~(1 & a)",
    "a & (a | b)", "a | (a & b)", "a & (~a | b)", "a | (~a & b)",
    "(a & b) | (a & ~b)", "(a | b) & (a | ~b)", "(a & b & c) | (a & b & ~c)",
    "c & b & a", "c | b | a", "~c & b & ~a", "(b|a) & (d|c)",
    "a & (b & (c & d))", "a | (b | (c | d))", "(a & b) | (c & d) | (a & b)",
    "x & y | x & ~y | ~x & y", "(a | b) & (a | c) & (b | c)",
    "a & b | a & c | b & c", "~(a & b) | (a & b)", "(a|b)&~(a|b)",
    "a & (b | ~b)", "(a & ~b) | (~a & b) | (a & b)",
    "~(a | ~(b & ~c))", "(a | 0) & (b | 1)", "a & b & c & ~a",
]:
    step("parse", esc(e))
    step("simplify")
step("parse", "a & (b | c)")
step("flags")
step("simplify")
step("flags")
step("simplify")
step("flags")

job("normal forms")
for e in [
    "a & (b | c)", "a | (b & c)", "(a | b) & (c | d)", "(a & b) | (c & d)",
    "~(a & b)", "~(a | b) | c", "a & ~(b | ~c)", "(a & b) | (a & c) | (b & c)",
    "~(a & (b | ~c))", "a | ~a", "a & ~a", "1", "0", "a",
    "(a | b) & ~a", "x & (y | (z & w))", "(p | q) & (r | s) & (t | u)",
    "~(x & y & z)", "a ^ b",
]:
    step("parse", esc(e))
    step("keep", "orig")
    step("cnf")
    step("use", "orig")
    step("dnf")
step("parse", "a & (b | c)", "s")
step("keep", "e")
step("cnf")
step("use", "e")
step("str")
step("parse", "(a | b) & (c | d)", "s")
step("keep", "e")
step("dnf")
step("use", "e")
step("debug")

job("the methods one at a time")
step("parse", "a & ~(b | c)")
step("literalize")
step("parse", "~(~(a & b))")
step("cancel")
step("parse", "~~~(a | b)")
step("cancel")
step("demorgan")
step("parse", "~(a | ~(b & c))")
step("demorgan")
step("literalize")
step("parse", "a & b")
step("demorgan")
step("parse", "a & (b & c) & (d & e)")
step("flatten")
step("parse", "a | (b & c) | (d | e)")
step("flatten")
step("parse", "a")
step("flatten")
step("parse", "a & (b | c)")
step("distributive")
step("parse", "(a | b) & (c | d)")
step("distributive")
step("parse", "a | (b & c) | (d & e)")
step("distributive")
step("parse", "a & b & c")
step("subtract", "b")
step("subtract", "a")
step("subtract", "c")
step("parse", "a & b & c")
step("subtract", "a & c")
step("parse", "a & b & c")
step("subtract", "a & d")
step("parse", "a & b")
step("subtract", "a & b")
step("parse", "a & (b | c) & b")
step("subtract", "b", "s")
step("parse", "~a")
step("subtract", "a")
step("parse", "1")
step("demorgan")
step("parse", "~1")
step("demorgan")

job("pretty printing")
for e in [
    "a", "~a", "1", "a & b", "~(a & b)",
    "not a and not b and not (a and ba and c) and c or c",
    "a & (b | ~c) & ~(d | e)",
]:
    step("parse", esc(e))
    step("pretty")
    step("debug")
step("parse", "a & (b | c)", "s")
step("debug")

job("symbols and literals")
for e in [
    "a & b & ~a", "x | ~y | ~~z", "1 & 0", "a & (b | (c & ~a)) & ~~b",
    "role:admin and team:ops or role:admin",
]:
    step("parse", esc(e))
    step("literals")
    step("symbols")
    step("objects")
    step("get_literals")
    step("get_symbols")

job("equality and order")
pairs = [
    ("a & b", "b & a"), ("a & b", "a & b & a"), ("a & b", "a | b"),
    ("~a", "~a"), ("~a", "a"), ("a", "a"), ("a", "b"), ("1", "1"),
    ("1", "0"), ("0", "1"), ("a", "1"), ("1", "a"), ("a", "~b"), ("~b", "a"),
    ("~a", "a"), ("a & b", "c"), ("a & b", "a | b"), ("a | b", "a & b"),
    ("a & b", "a & c"), ("a & c", "a & b"), ("a & b", "a & b & c"),
    ("~(a & b)", "a & b"), ("a & b", "~(a & b)"), ("(a | b) & c", "c & (b | a)"),
    ("0", "0"), ("~a", "~b"), ("~b", "~a"), ("b", "a"), ("aa", "a"),
    ("B", "a"), ("a & b", "a & b"),
]
for x, y in pairs:
    step("parse", esc(y))
    step("keep", "y")
    step("parse", esc(x))
    step("eq", "y")
    step("lt", "y")

job("membership")
for e, x in [
    ("a & b & c", "a"), ("a & b & c", "d"), ("a & b & c", "a & c"),
    ("a & b & c", "a & d"), ("a & b & c", "a | b"), ("a | b", "b"),
    ("a & (b | c)", "b | c"), ("a & (b | c)", "c | b"), ("a & (b | c)", "b"),
    ("~a", "a"), ("a", "a"), ("1", "a"), ("a & ~b", "~b"), ("a & ~b", "b"),
]:
    step("parse", esc(e))
    step("in", esc(x))

job("building expressions")
step("parse", "a")
step("keep", "a")
step("parse", "b | c")
step("keep", "bc")
step("and", "a")
step("keep", "e1")
step("or", "bc")
step("invert")
step("simplify")
step("use", "e1")
step("invert")
step("invert")
step("simplify")
step("parse", "1")
step("and", "a")
step("simplify")

job("evaluating")
for e, kw in [
    ("a & b", "a=1,b=1"), ("a & b", "a=1,b=0"), ("a | b", "a=0,b=0"),
    ("~a", "a=0"), ("~~a", "a=1"), ("a & (b | ~c)", "a=1,b=0,c=0"),
    ("a & b", "a=1"), ("a | b", "b=1"), ("a | b", "a=1,b=1,c=0"),
    ("1", ""), ("0", ""), ("1", "a=1"), ("a & 1", "a=1"), ("1 & a", "a=1"),
    ("~1", ""), ("~(a & b)", "a=1,b=1"), ("1 & 0", ""), ("1 | 0 | 1", ""),
    ("1 & a", ""), ("~(1 & 0)", ""), ("role:admin & mfa", "role:admin=1,mfa=1"),
]:
    step("parse", esc(e))
    step("eval", kw)

job("substitution")
for e, s, d, simp in [
    ("a & b", "a=c", "-", ""), ("a & b", "a=c | d", "-", ""),
    ("a & b | c", "b=1", "-", ""), ("a & b | c", "b=1", "-", "s"),
    ("a & b | c", "b=0", "-", "s"), ("a & (b | c)", "b | c=x", "-", ""),
    ("a & (b | c)", "c | b=x", "-", ""), ("a & b", "z=1", "-", ""),
    ("a & b & c", "a=1", "0", ""), ("a & b & c", "a=1", "0", "s"),
    ("a & b", "a & b=q", "-", ""), ("~a | b", "a=b;b=a", "-", ""),
    ("a", "a=b", "-", ""), ("a", "z=b", "-", ""), ("a", "z=b", "1", ""),
    ("1 & a", "a=b", "-", ""), ("~(a & b)", "a=0", "-", "s"),
    ("a & b", "a=b", "-", "s"),
]:
    step("parse", esc(e))
    if simp:
        step("subs", esc(s), d, simp)
    else:
        step("subs", esc(s), d)

job("an SPDX licence check")
step("licences", "licences/packages.txt", "licences/allowed.txt")

job("an access-rule matrix")
step("access", "access/rules.txt", "access/users.txt")

job("truth tables")
for e in [
    "a & (b | c)", "(a & b) | (a & ~b)", "~(a | b) | c", "a | ~a",
    "x & ~x", "(p | q) & (~p | r)", "a & 1", "(a & b) | (b & c) | (c & a)",
]:
    step("truthtable", esc(e))


def main():
    for rel, text in FILES.items():
        path = os.path.join(DATA, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    with open(os.path.join(DATA, "jobs.tsv"), "w", encoding="utf-8") as f:
        for fields in JOBS:
            f.write("\t".join(fields) + "\n")


main()
