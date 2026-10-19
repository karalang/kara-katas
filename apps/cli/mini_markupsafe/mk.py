# Writes data/jobs.tsv, the operations to run through markupsafe, and
# data/unicode.txt, what Python's str methods need to know about the
# characters those operations reach.
#
# jobs.tsv: a line `== name` starts a job; every other line is an
# operation and its arguments, separated by tabs. Each argument is a
# Python expression over literals (str, int, float, None, True, False,
# lists, tuples and dicts) and four constructors: Markup(x), User(name,
# email, id), Badge(label) and Plain(text).
import html
import os
import random
import struct
import unicodedata

jobs = []


def job(name, ops):
    jobs.append((name, ops))


VALUES = [
    "'plain text'", "'<script>alert(\"x\")</script>'", "'Tom & Jerry'", "\"it's\"",
    "'a < b > c'", "''", "'&amp; already'", "'caf\\xe9 \\u2014 \\xab\\xbb'", "'tab\\tnew\\nline'",
    "None", "True", "False", "0", "42", "-7", "3.25", "0.1", "-0.0", "1e16", "1.5e-07", "123456789.125",
    "1e+300", "2.5e-05", "100.0", "[1, '<b>', None]", "('a&b', 2)", "{'k': '<v>', 1: [2.5]}",
    "Markup('<em>safe</em>')", "Markup('')", "Markup(42)", "Markup(None)", "Markup(Badge('new'))",
    "User('Ann <admin>', 'ann@example.com', 7)", "Badge('hot & new')", "Plain('<raw>')",
    "[Markup('<i>'), Badge('x')]", "'\\x00\\x7f\\u200b\\xa0'", "'\\U0001f600 emoji'",
]
ops = []
for v in VALUES:
    for f in ("escape", "escape_silent", "soft_str", "markup", "str", "repr"):
        ops.append([f, v])
job("escape", ops)

ops = []
for a, b in [
    ("Markup('<em>Hello</em> ')", "'<foo>'"), ("'<foo>'", "Markup('<em>Hello</em>')"),
    ("Markup('a')", "Markup('<b>')"), ("Markup('a')", "Badge('<x>')"), ("Badge('<x>')", "Markup('a')"),
    ("Markup('a')", "3"), ("3", "Markup('a')"), ("Markup('a')", "None"), ("'x'", "'<y>'"),
    ("Markup('a')", "User('B&B', 'b@x', 2)"), ("Markup('')", "''"), ("Markup('&')", "'&'"),
]:
    ops.append(["add", a, b])
for a, n in [("Markup('<br>')", "3"), ("Markup('ab')", "0"), ("Markup('ab')", "-2"), ("Markup('<')", "True")]:
    ops.append(["mul", a, n])
    ops.append(["rmul", n, a])
job("concat", ops)

PCT = [
    ("Markup('<em>%s</em>')", "('foo & bar',)"),
    ("Markup('%d|%.2f|%s|%r|%5s|%-4s|%i')", "(5, 2.5, '<a>', '<b>', 'x', 'y', 7.9)"),
    ("Markup('%c')", "(65,)"), ("Markup('%d')", "('5',)"), ("Markup('%d')", "('x',)"),
    ("Markup('%f')", "('x',)"), ("Markup('%.1f')", "('2.25',)"), ("Markup('%x')", "(255,)"),
    ("Markup('%(a)s %(b)d')", "{'a': '<', 'b': 3}"), ("Markup('%(a)s')", "{'b': '<'}"),
    ("Markup('%s %s')", "('a',)"), ("Markup('%s')", "('a', 'b')"), ("Markup('%s')", "[1, '<']"),
    ("Markup('%s')", "'x'"), ("Markup('%z')", "'x'"), ("Markup('%s%%')", "5"),
    ("Markup('%*d')", "(5, 3)"), ("Markup('%05d|%+d|% d|%-5d|')", "(42, 42, 42, 42)"),
    ("Markup('%d')", "(True,)"), ("Markup('%s')", "(None,)"), ("Markup('%.3s')", "('<<<<',)"),
    ("Markup('%s by %s')", "(Markup('<b>x</b>'), User('Zoë', 'z@x', 1))"),
    ("Markup('%s')", "Badge('a<b')"), ("Markup('%r')", "Badge('a<b')"), ("Markup('%r')", "(Plain('<p>'),)"),
    ("Markup('%s')", "Plain('<p>')"), ("Markup('%(u)s')", "{'u': User('Q', 'q@x', 9)}"),
    ("Markup('%5.1f%%')", "(99.95,)"), ("Markup('%.0f %.0f %.0f')", "(0.5, 1.5, 2.5)"),
    ("Markup('%f')", "(1e+22,)"), ("Markup('%.3f')", "(-0.0005,)"), ("Markup('%d items')", "(3.99,)"),
    ("Markup('%s')", "()"), ("Markup('%s')", "((),)"), ("Markup('no fields')", "()"),
    ("Markup('no fields')", "('x',)"), ("Markup('no fields')", "{'a': 1}"), ("Markup('%(a)s %s')", "{'a': 1}"),
    ("Markup('%')", "()"), ("Markup('%(a')", "{'a': 1}"), ("Markup('%10.4s|')", "('<tag>',)"),
    ("Markup('%-+6d|%06.2f')", "(7, -1.5)"), ("Markup('%s')", "1e16"), ("Markup('%s')", "(0.1,)"),
    ("Markup('%r')", "(2.5,)"), ("Markup('%d')", "(None,)"), ("Markup('%f')", "(None,)"),
]
job("percent", [["mod", a, b] for a, b in PCT])

FMT = [
    ("Markup('<em>{}</em>')", "('foo & bar',)", "{}"),
    ("Markup('{0!s} {0!r} {0}')", "(Markup('<b>'),)", "{}"),
    ("Markup('{0:>5}')", "(Markup('<b>'),)", "{}"), ("Markup('{0:>5}')", "('<b>',)", "{}"),
    ("Markup('{}')", "(3.25,)", "{}"), ("Markup('{:.2f}')", "(3.255,)", "{}"),
    ("Markup('{x}')", "()", "{}"), ("Markup('{0}{1}')", "('a',)", "{}"),
    ("Markup('{user:link} wrote')", "()", "{'user': User('Ann <a>', 'ann@x', 7)}"),
    ("Markup('{user:name} | {user}')", "()", "{'user': User('Ann <a>', 'ann@x', 7)}"),
    ("Markup('{user:bogus}')", "()", "{'user': User('Ann', 'a@x', 7)}"),
    ("Markup('{0.name} <{0.email}> #{0.id:03d}')", "(User('B&B', 'b@x', 5),)", "{}"),
    ("Markup('{0.nope}')", "(User('B', 'b@x', 5),)", "{}"),
    ("Markup('{b} {b:x}')", "()", "{'b': Badge('<hot>')}"),
    ("Markup('{p} {p!r}')", "()", "{'p': Plain('<p>')}"),
    ("Markup('{0[name]} {0[n]:,}')", "({'name': '<N>', 'n': 1234567},)", "{}"),
    ("Markup('{0[1]} {0[0]}')", "(['<a>', '<b>'],)", "{}"),
    ("Markup('{0[2]}')", "(['<a>'],)", "{}"), ("Markup('{0[k]}')", "({},)", "{}"),
    ("Markup('{} {1}')", "('a', 'b')", "{}"), ("Markup('{0} {}')", "('a', 'b')", "{}"),
    ("Markup('{:{w}}|')", "('<x>',)", "{'w': 8}"), ("Markup('{:^{w}.{p}}|')", "('<xyz>',)", "{'w': 9, 'p': 2}"),
    ("Markup('{{literal}} {}')", "('<',)", "{}"), ("Markup('{0!x}')", "('a',)", "{}"),
    ("Markup('}')", "()", "{}"), ("Markup('{')", "()", "{}"), ("Markup('{0')", "('a',)", "{}"),
    ("Markup('{:d}')", "('5',)", "{}"), ("Markup('{:s}')", "(5,)", "{}"), ("Markup('{:+.1%}')", "(0.256,)", "{}"),
    ("Markup('{:,.2f} {:_d} {:#x} {:08.3f}')", "(1234567.891, 1000000, 255, -3.14159)", "{}"),
    ("Markup('{!a}')", "('caf\\xe9 <',)", "{}"), ("Markup('{:*<6}|{:=+6d}')", "('ab', 42)", "{}"),
    ("Markup('{0:{1}}')", "(Markup('<i>'), '')", "{}"), ("Markup('{a.b}')", "()", "{'a': 1}"),
    ("Markup('{}')", "(None,)", "{}"), ("Markup('{} {}')", "(True, [Markup('<i>')])", "{}"),
    ("Markup('{0:.3}')", "('<abcdef>',)", "{}"), ("Markup('{:e}')", "(5,)", "{}"),
]
ops = [["format", m, a, k] for m, a, k in FMT]
ops += [["format_map", "Markup('{a} & {b}')", "{'a': '<', 'b': Markup('<')}"],
        ["format_map", "Markup('{missing}')", "{'a': 1}"]]
job("format", ops)

M = "Markup('  <b>Hello</b>,  World &amp; Co.  ')"
ops = []
for meth, args in [
    ("split", ""), ("split", "','"), ("split", "None, 1"), ("rsplit", "None, 1"), ("rsplit", "'o'"),
    ("splitlines", ""), ("strip", ""), ("lstrip", ""), ("rstrip", "' .'"), ("strip", "' <>'"),
    ("lower", ""), ("upper", ""), ("title", ""), ("capitalize", ""), ("swapcase", ""), ("casefold", ""),
    ("replace", "'World', '<Earth>'"), ("replace", "'l', Markup('<L>'), 2"), ("ljust", "40, '*'"),
    ("rjust", "40, '<'"), ("center", "41, '&'"), ("zfill", "40"), ("expandtabs", ""),
    ("removeprefix", "'  <b>'"), ("removesuffix", "'Co.  '"), ("partition", "'</b>'"),
    ("rpartition", "' '"), ("partition", "'zzz'"), ("rpartition", "'zzz'"), ("unescape", ""),
    ("striptags", ""), ("getitem", "2"), ("getitem", "-1"), ("getitem", "40"), ("slice", "2, 10"),
    ("slice", "None, None, -1"), ("slice", "1, None, 3"), ("join", "['<a>', Markup('<b>'), 3]"),
    ("join", "['x', 'y']"), ("join", "[]"), ("center", "5"), ("ljust", "40, 'ab'"),
]:
    ops.append(["call", M, meth, args])
for m2, meth, args in [
    ("Markup('line one\\nline two\\r\\nthree\\x0bfour\\u2028five')", "splitlines", ""),
    ("Markup('a\\nb\\n')", "splitlines", "True"), ("Markup('\\tx\\ty\\t')", "expandtabs", "4"),
    ("Markup('stra\\xdfe \\u0130stanbul \\u01c6ungla')", "upper", ""),
    ("Markup('stra\\xdfe \\u0130stanbul \\u01c6ungla')", "lower", ""),
    ("Markup('stra\\xdfe \\u0130stanbul \\u01c6ungla')", "title", ""),
    ("Markup('stra\\xdfe \\u0130stanbul \\u01c6ungla')", "casefold", ""),
    ("Markup('stra\\xdfe \\u0130stanbul \\u01c6ungla')", "swapcase", ""),
    ("Markup('\\u03a3\\u039f\\u03a6\\u039f\\u03a3 \\u03a3')", "lower", ""),
    ("Markup('-42')", "zfill", "6"), ("Markup('+')", "zfill", "3"),
    ("Markup('a\\u3000b\\xa0c\\x1cd  e')", "split", ""), ("Markup('a,,b,')", "split", "','"),
    ("Markup('a,,b,')", "rsplit", "',', 1"), ("Markup('abc')", "split", "''"),
    ("Markup('xxhixx')", "strip", "'x'"), ("Markup('<a>')", "replace", "'', '-'"),
]:
    ops.append(["call", m2, meth, args])
job("methods", ops)

SNIPS = [
    "Main &raquo;\\t<em>About</em>", "<p>Hello <b>World</b></p>", "a <!-- hidden <b> --> b",
    "a <!-- never closed", "x < y and y > z", "<a href='/x' title=\"a>b\">link</a>",
    "&lt;tag&gt; &amp;amp; &#39; &#x27; &#34; &quot;", "&copy 2024 &copy; &COPY", "&notit; &notin; &not",
    "&#128512; &#x1F600; &#0; &#129; &#xD800; &#1114112; &#65534;", "&;&#;&#x;&abc", "&AMP;&ampx",
    "line\\n\\n  two   three\\r\\n", "<br/><br />text<hr>", "unclosed <tag text", "<<<>>>", "",
    "Caf&eacute; &mdash; cr&egrave;me &frac12; &hellip;", "<script>evil()</script>Safe", "&#9;&#10;&#13;",
    "\\u3000wide\\u3000space\\u3000", "<p>a</p><p>b</p>", "<!---->x<!-- -->y",
]
ops = []
for s in SNIPS:
    ops.append(["striptags", "Markup(%r)" % s.encode().decode("unicode_escape")])
    ops.append(["unescape", "Markup(%r)" % s.encode().decode("unicode_escape")])
job("striptags", ops)

# A forum thread rendered the way a Jinja template with autoescape
# renders it: authors, bodies, scores, badges, previews of HTML bodies.
THREAD = """[
 (User('Ann <admin>', 'ann@example.com', 1), 'First!\\nCheck <this> & that.', 12, ['op', 'mod'], None),
 (User("O'Brien", 'ob@example.com', 2), 'Quotes "here" and \\'there\\'', -3, [], '<p>Edited: <b>bold</b> &amp; <i>italic</i></p>'),
 (User('Zo\\xeb', 'zoe@example.com', 3), 'Unicode: caf\\xe9 \\u2014 na\\xefve \\U0001f600', 0, ['new & shiny'], None),
 (User('<script>', 'x@example.com', 4), 'Line one\\nLine two\\n\\nLine four', 7, ['<b>'], '<div><!-- note --><p>A long body that goes on and on, well past forty characters of text.</p></div>'),
 (User('Bob', 'bob@example.com', 5), '', 100, ['a', 'b', 'c'], 'Plain &copy; text &notin; set'),
]"""
job("thread", [["thread", "'Re: <Kara> & friends'", THREAD.replace("\n", " ")]])


# Prices, ratios and measurements as a report formats them, and random
# doubles across the whole range (subnormals included), through repr,
# % and format.
random.seed(124)
floats = [0.5, 1.5, 2.5, 0.125, 0.375, 2.675, 1.005, 1e-05, 9.995, 99.995, 1234.5678, 5e-324,
          2.2250738585072014e-308, 1.7976931348623157e+308, 0.30000000000000004, 1e+22, 1e+23,
          123456789012345.6, 0.0001, 1e-07, 4.35, 0.045, 1.0, 10.0, 9007199254740993.0]
for _ in range(60):
    floats.append(round(random.uniform(0, 10 ** random.randint(0, 9)), random.randint(0, 6)))
for _ in range(16):
    floats.append(struct.unpack("<d", struct.pack("<Q", random.getrandbits(63)))[0])
ops = []
for i, x in enumerate(floats):
    if x != x or x in (float("inf"), float("-inf")):
        continue
    v = repr(-x if i % 3 == 1 else x)
    ops.append(["escape", v])
    ops.append(["mod", "Markup('%.3f|%e|%12.2f|%-+10.1f|%.0f')", "(%s, %s, %s, %s, %s)" % (v, v, v, v, v)])
    ops.append(["format", "Markup('{0:,.4f} {0:.3e} {0:+.1%} {0} {0:>14}')", "(%s,)" % v, "{}"])
job("numbers", ops)


def esc(s):
    return s.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n")


os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for name, ops in jobs:
        fh.write("== " + name + "\n")
        for op in ops:
            fh.write("\t".join(esc(x) for x in op) + "\n")

# The characters the jobs reach, closed under the case mappings.
covered = set(chr(c) for c in range(0, 256)) | {"\u03c2", "\u2028", "\u2029", "\u3000", "\u200b"}
for name, ops in jobs:
    for op in ops:
        for x in op[1:]:
            covered.update(x)
            try:
                covered.update(str(eval(x, {"Markup": str, "User": lambda *a: a, "Badge": str, "Plain": str})))
            except Exception:
                pass
# and what unescape makes of the snippets
for x in SNIPS:
    covered.update(html.unescape(x.encode().decode("unicode_escape")))
covered.add("\ufffd")
todo = list(covered)
while todo:
    c = todo.pop()
    for m in (c.lower(), c.upper(), c.title(), c.casefold(), c.swapcase()):
        for d in m:
            if d not in covered:
                covered.add(d)
                todo.append(d)

WB = {0x27, 0x2E, 0x3A, 0xB7, 0x387, 0x55F, 0x5F4, 0x2018, 0x2019, 0x2024, 0x2027,
      0xFE13, 0xFE52, 0xFE55, 0xFF07, 0xFF0E, 0xFF1A}


def hexs(s):
    return " ".join("%x" % ord(d) for d in s)


with open("data/unicode.txt", "w", encoding="utf-8") as fh:
    fh.write("# cp;lower;upper;title;casefold;flags (c cased, i case-ignorable, u isupper, l islower,"
             " s isspace, b line break, p printable)\n")
    for c in sorted(covered):
        cp = ord(c)
        if 0xD800 <= cp <= 0xDFFF:
            continue
        flags = ""
        if c.islower() or c.isupper() or c.istitle():
            flags += "c"
        if unicodedata.category(c) in ("Mn", "Me", "Cf", "Lm", "Sk") or cp in WB:
            flags += "i"
        if c.isupper():
            flags += "u"
        if c.islower():
            flags += "l"
        if c.isspace():
            flags += "s"
        if len(("x" + c + "x").splitlines()) > 1:
            flags += "b"
        if c.isprintable():
            flags += "p"
        fh.write("%x;%s;%s;%s;%s;%s\n" % (cp, hexs(c.lower()), hexs(c.upper()), hexs(c.title()),
                                          hexs(c.casefold()), flags))
print(len(jobs), "jobs,", sum(len(o) for _, o in jobs), "operations,", len(covered), "characters")
