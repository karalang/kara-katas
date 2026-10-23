#!/usr/bin/env python3
"""Writes data/jobs.tsv: the tables an operations team's command-line tools
print (a server inventory, a cost report, benchmark runs, a translation
status board, a CSV import with bad rows), as calls on texttable's
Texttable.

Each line is one op: its name, then its arguments, tab-separated. A value
is "s:<hex>" (a str, UTF-8 in hex), "y:<hex>" (bytes), "i:<int>",
"f:<float repr>", "b:0" or "b:1" (a bool) or "n" (None). In a "rows" op
the first value is the header flag and "/" separates the rows. A line
"job<TAB>name" starts a job with a fresh Texttable().

Run: python3 -s -P -B mk.py"""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LINES = []


def enc(v):
    if v is None:
        return "n"
    if isinstance(v, bool):
        return "b:1" if v else "b:0"
    if isinstance(v, int):
        return "i:%d" % v
    if isinstance(v, float):
        return "f:" + repr(v)
    if isinstance(v, bytes):
        return "y:" + v.hex()
    assert isinstance(v, str), v
    return "s:" + v.encode("utf-8").hex()


def job(name):
    LINES.append("job\t" + name)


def op(name, *vals):
    LINES.append("\t".join([name] + [enc(v) for v in vals]))


def rows(header, rs):
    fields = ["rows", enc(header)]
    for k, r in enumerate(rs):
        if k:
            fields.append("/")
        fields.extend(enc(v) for v in r)
    LINES.append("\t".join(fields))


# ---------------------------------------------------------------- the demo

job("module demo")
op("align", "l", "r", "c")
op("valign", "t", "m", "b")
rows(True, [["Name", "Age", "Nickname"],
            ["Mr\nXavier\nHuon", 32, "Xav'"],
            ["Mr\nBaptiste\nClement", 1, "Baby"],
            ["Mme\nLouise\nBourgeau", 28, "Lou\n \nLoue"]])
op("draw")
op("new")
op("deco", 2)
op("dtype", "t", "f", "e", "i", "a")
op("align", "l", "r", "r", "r", "l")
rows(True, [["text", "float", "exp", "int", "auto"],
            ["abcd", "67", 654, 89, 128.001],
            ["efghijk", 67.5434, .654, 89.6, 12800000000000000000000.00023],
            ["lmn", 5e-78, 5e-78, 89.4, .000000000000128],
            ["opqrstu", .023, 5e+78, 92., 12800000000000000000000]])
op("draw")

# ---------------------------------------------------------------- inventory

job("server inventory")
op("header", "host", "role", "cpus", "mem GiB", "load", "up")
op("row", "web-01", "nginx", 8, 31.25, 0.42, True)
op("row", "web-02", "nginx", 8, 31.25, 1.5, True)
op("row", "db-01", "postgres primary", 32, 251.8, 12.0625, True)
op("row", "db-02", "postgres replica", 32, 251.8, None, False)
op("row", "cache-01", "redis", 4, 15.6, "0.07", True)
op("row", "batch-07", "nightly jobs\n(spot)", 64, 503.5, 63.999, False)
op("draw")
op("header_align", "l", "l", "r", "r", "r", "c")
op("align", "l", "l", "r", "r", "r", "c")
op("draw")
op("deco", 1 | 2)
op("draw")
op("max_width", 50)
op("draw")
op("max_width", 0)
op("deco", 0)
op("draw")

# ---------------------------------------------------------------- formatting

job("auto formatting")
op("header", "input", "auto")
op("dtype", "t", "a")
for v in [0, 1, -1, 7, 100000000, 100000001, 123456789, -987654321,
          2 ** 53 + 1, 0.0, -0.0, 0.5, 1.5, 2.5, -2.5,
          0.0005, 0.0004999, 12.0, 1e8, 1.0000001e8, 1e-5, 3.14159,
          float("inf"), float("-inf"), float("nan"), True, False, None,
          "", "abc", "12", " 42 ", "-0", "+7", "1_000", "1__0", "_1",
          "12.5", "1e9", "1E-3", ".5", "5.", ".", "1e", "inf", "-Infinity",
          "nan", "NaN", "0x10", "1,5", "\t3\n", "\u00a07\u2003", "١٢", "１２.５", "-٣e٢",
          b"12", b"3.75", b"x", b"", 1e22, 1e300, 5e-324]:
    op("row", repr(v) if not isinstance(v, str) else "str " + ascii(v), v)
op("draw")

job("datatypes")
op("deco", 2 | 8)
op("header", "value", "a", "t", "f", "e", "i", "b")
op("dtype", "t", "a", "t", "f", "e", "i", "b")
for v in [0, 3, -12, 2.5, 3.5, -0.5, 0.125, 2.675, 1.0005, 123456.789,
          1e16, 1e20, 2.0 ** 70, -1.5e-7, True, None, "", "7", " 2.5 ",
          "x", "-0", b"8", b""]:
    op("row", repr(v), v, v, v, v, v, v)
op("draw")
op("row", "inf", float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), True)
op("row", "nan", float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), True)
op("row", "str inf", "inf", "inf", "inf", "inf", "inf", "x")
op("draw")

job("precision")
op("dtype", "f", "e", "a")
op("header", "f", "e", "auto")
op("row", 2.0 / 3, 2.0 / 3, 2.0 / 3)
op("row", 0.1, 0.1, 0.1)
op("row", 1234.5, 1234.5, 1234.5)
op("draw")
for p in [0, 1, 6, 20, -1, 1.5, True, "2", None, 2]:
    op("precision", p)
    op("row", 2.0 / 3, 2.0 / 3, 2.0 / 3)
    op("row", 0.5, 2.5, 1e-9)
op("draw")

job("cost report")
op("deco", 1 | 2 | 8)
op("dtype", "t", "i", "f", "f", "e")
op("align", "l", "r", "r", "r", "r")
op("precision", 2)
op("header", "service", "hours", "rate", "total", "share")
op("row", "compute", 7302, 0.0416, 7302 * 0.0416, 0.61)
op("row", "storage", 744.0, 0.023, 17.112, 0.0014)
op("row", "egress", "1488.6", "0.09", 133.974, 0.011)
op("row", "support", 1, 100, 100.005, 0.0083)
op("row", "credits", -1, 250, -250.0, -0.0209)
op("draw")

# ---------------------------------------------------------------- decoration

job("decorations")
op("header", "id", "name", "state")
op("row", 1, "alpha", "ok")
op("row", 2, "beta\nb", "failed")
op("row", 3, "gamma", "ok")
for d in range(16):
    op("deco", d)
    op("draw")
op("deco", -1)
op("draw")
op("deco", 32)
op("draw")

job("drawing characters")
op("header", "k", "v")
op("row", "a", 1)
op("row", "b", 2)
for cs in [["*", "#", "@", "~"], ["--", "||", "++", "=="], [1, 2, 3, 4],
           ["", "", "", ""], [None, True, 0.5, b"x"], ["─", "│", "┼", "═"],
           ["＝", "｜", "＋", "＝"], ["-", "|", "+"], ["-", "|", "+", "=", "#"]]:
    op("chars", *cs)
    op("draw")
op("deco", 1 | 2)
op("chars", "-", "!", "+", "=")
op("draw")

# ---------------------------------------------------------------- alignment

job("alignment")
op("header", "left", "centre", "right", "other")
op("row", "a", "b", "c", "d")
op("row", "wide cell", "wide cell!", "wide cell!!", "x")
op("row", "two\nlines", "one", "three\nline\ncell", "")
op("draw")
op("align", "l", "c", "r", "x")
op("valign", "t", "m", "b", "?")
op("draw")
op("header_align", "r", "l", "c", "z")
op("valign", "b", "b", "m", "m")
op("draw")
op("align", "c", "c", "c", "c")
op("row", "odd", "even", "x", "xy")
op("draw")
op("align", "l", "c")

# ---------------------------------------------------------------- wrapping

job("wrapping")
op("header", "ticket", "summary", "owner")
op("row", "OPS-1412", "Rotate the TLS certificates on the edge proxies before they expire on Friday", "sre")
op("row", "OPS-1420", "Disk on db-02 is 91% full; move the WAL archive to object storage", "dba team")
op("row", "OPS-1433", "https://status.example.com/incidents/2026-10-23-api-latency-regression", "on-call")
op("row", "OPS-1441", "well-known self-service re-provisioning", "platform")
for w in [80, 60, 45, 30, 22, 12]:
    op("max_width", w)
    op("draw")
op("max_width", -5)
op("draw")

job("explicit widths")
op("header", "key", "value")
op("row", "motd", "Welcome to the build farm. Jobs over 2h are killed.")
op("row", "path", "/usr/local/bin:/usr/bin:/bin")
op("width", 6, 20)
op("draw")
op("width", "4", 2.7)
op("draw")
op("width", 1, 1)
op("draw")
for bad in [[0, 5], [-2, 5], ["x", 5], [5, " 7 "], [5, "7.5"], [None, 5],
            [5, float("nan")], [5, float("inf")], [5, True], [5]]:
    op("width", *bad)
op("draw")
op("width", 3, 4, 5)
op("draw")

# ---------------------------------------------------------------- whitespace

job("tabs and blank lines")
op("header", "col\tA", "B")
op("row", "a\tb", "x")
op("row", "1234567\t8", "tab\tat\tstops")
op("row", "12345678\t9", "\t")
op("row", "para one\n\npara two", " \n \n")
op("row", "trailing\n", "\nleading")
op("row", "cr\rin\x0bcell", "ff\x0cx")
op("row", "\u00a0", "\u3000wide space")
op("draw")
op("max_width", 22)
op("draw")

# ---------------------------------------------------------------- unicode

job("translations")
op("header", "key", "en", "ja", "zh", "de")
op("row", "save", "Save", "保存", "保存", "Speichern")
op("row", "cancel", "Cancel", "キャンセル", "取消", "Abbrechen")
op("row", "greeting", "Good morning", "おはようございます", "早上好", "Guten Morgen")
op("row", "status.ok", "✅ OK", "✅ 正常", "✅ 正常", "✅ In Ordnung")
op("row", "accents", "cafe\u0301", "ｶﾀｶﾅ", "全角ＡＢＣ", "Stra\u00dfe")
op("draw")
op("max_width", 50)
op("draw")
op("max_width", 40)
op("draw")
op("align", "l", "c", "r", "c", "r")
op("draw")

job("bytes cells")
op("header", b"name", "data")
op("row", b"plain", b"hello")
op("row", "utf-8", "日本".encode("utf-8"))
op("row", "bad start", b"\xffab")
op("row", "bad cont", b"ab\xe6\x97x")
op("row", "truncated", b"tail\xe6\x97")
op("row", "number", b"42")
op("row", "float", b" 2.5 ")
op("dtype", "t", "t")
op("row", "text", b"7")
op("row", "bad text", b"\xc3")
op("draw")

# ---------------------------------------------------------------- errors

job("row sizes")
op("draw")
op("header", "a", "b", "c")
op("row", 1, 2)
op("row", 1, 2, 3, 4)
op("align", "l", "r")
op("valign", "t")
op("dtype", "a", "a")
op("header_align", "l")
op("chars", "-", "|")
op("row", 1, 2, 3)
op("draw")
op("reset")
op("draw")
op("header", "only", "header")
op("draw")

job("add_rows")
rows(True, [])
rows(True, [["h1", "h2"], [1, 2], [3]])
op("draw")
op("reset")
rows(False, [["x", 1], ["y", 2]])
op("draw")
op("reset")
rows(True, [["lonely", "header"]])
op("draw")
op("new", 30)
rows(True, [["a", "b"], [1, 2], [3, 4], [5, 6]])
op("draw")

job("reset keeps settings")
op("header", "a", "b", "c")
op("align", "r", "c", "l")
op("valign", "b", "m", "t")
op("dtype", "i", "f", "t")
op("row", 1.5, 2, "x\ny")
op("draw")
op("width", 5, 7, 5)
op("draw")
op("reset")
op("header", "p", "q")
op("row", 2.5, 3)
op("draw")
op("reset")
op("header", "p", "q", "r", "s")
op("row", "a\nb", 2, 3, 4)
op("draw")
op("reset")
op("dtype", "a", "a", "a", "a")
op("header", "p", "q", "r", "s")
op("row", "a\nb", 2, 3, 4)
op("draw")
op("reset")
op("width", 3, 3)
op("header", "p", "q")
op("draw")
op("header", "one", "two", "three")
op("draw")

job("bad dtype and align")
op("dtype", "a", "x")
op("row", 1, 2)
op("row", 3, "t")
op("dtype", "a", "t")
op("row", 4, 5)
op("draw")
op("new")
op("header", "a", "b")
op("valign", "t")
op("row", "x\ny", "z")
op("valign", "t", "t")
op("draw")
op("new")
op("width", 0)
op("width")
op("header", "x")
op("draw")
op("new")
op("header")
op("row", 1, 2)
op("draw")

job("max_width too low")
op("header", "a", "b", "c")
op("row", "xxxx", "yyyy", "zzzz")
for w in [21, 16, 15, 14, 13, 12]:
    op("max_width", w)
    op("draw")
op("deco", 0)
for w in [9, 8, 6, 2]:
    op("max_width", w)
    op("draw")

job("max_width constructor")
op("new", 10)
op("header", "name", "value")
op("row", "x", 1)
op("draw")
op("new", 0)
op("header", "a long header that would wrap", "v")
op("row", "x", 2)
op("draw")
op("new", -1)
op("header", "unlimited too", "v")
op("draw")
op("new", 18)
op("deco", 1)
op("row", "abc def ghi", "jkl")
op("draw")

os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
with open(os.path.join(HERE, "data", "jobs.tsv"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(LINES) + "\n")
assert math.isfinite(1.0)
