#!/usr/bin/env python3
r"""Writes data/jobs.tsv: one lowercase hex string per line, the hex of a
JavaScript source snippet (ASCII). For each line the job minifies the decoded
source with jsmin's algorithm and prints the hex of the minified bytes:

    min <hex of the minified source>

No jsmin import here (only literal source strings, hex-encoded); oracle.py
replays each line through the vendored library to produce expected.out. The
snippets cover line and block comments, the /*! preserved-comment rule, single-
and double-quoted strings with escapes, regular-expression literals (including
character classes and the `return /re/` case), the +/- and newline spacing
rules, and nested structures."""

SNIPPETS = [
    "var x = 1;",
    "function f(a, b) {\n    return a + b;\n}\n",
    "// line comment\nvar y = 2;",
    "/* block */ var z = 3;",
    "/*! keep me */\nvar w = 4;",
    "var s = 'hello world';",
    'var d = "a\\"b";',
    "var r = /ab+c/g;",
    "var r2 = /[/]/;",
    "if (a) { b = c / d; }",
    "return /re/.test(x);",
    "a = b + + c;",
    "x = y - -z;",
    "var long = 1 +\n    2 +\n    3;",
    "obj = { a: 1,\n b: 2 };",
    "var q = 'it\\'s';",
    'var nested = "say \\"hi\\"";',
    "for (var i = 0; i < 10; i++) {\n  console.log(i);\n}",
    "a   =   1 ;",
    "var e = a===b ? 1 : 2;",
    "s = '';\nt = \"\";",
    "x=/foo\\/bar/;",
    "var m = a /b/ c;",
    "function g(){return}",
    "// c1\n// c2\nvar v=5;",
    "/* multi\nline\ncomment */code();",
    "a=1\nb=2\nc=3",
    "var arr = [1,2,3];\narr.map(function(x){return x*2;});",
    "label: for(;;){break label;}",
    "var re = /\\d+/;",
]


def main():
    import os
    os.makedirs("data", exist_ok=True)
    with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
        for s in SNIPPETS:
            fh.write(s.encode("ascii").hex() + "\n")


main()
