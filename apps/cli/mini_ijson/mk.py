#!/usr/bin/env python3
"""Writes the inputs of mini_ijson to data/: a shop's order export, a
product catalog, a JSON-lines event log with a good and a corrupt copy,
sensor readings with exponents, files with a byte-order mark, Latin-1
bytes, a cut-off UTF-8 character and raw control characters, and the
job script data/jobs.tsv. data/files.txt lists the files written.

Run: python3 -s -P -B mk.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
written = []


def put(name, data):
    path = os.path.join(DATA, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if isinstance(data, str):
        data = data.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    written.append(name)


class Lcg:
    def __init__(self, seed):
        self.s = seed

    def next(self, n):
        self.s = (self.s * 1103515245 + 12345) % 2147483648
        return (self.s >> 8) % n


def jstr(s):
    """A JSON string literal, keeping non-ASCII text as UTF-8."""
    out = ['"']
    for c in s:
        if c == '"':
            out.append('\\"')
        elif c == "\\":
            out.append("\\\\")
        elif c == "\n":
            out.append("\\n")
        elif c == "\t":
            out.append("\\t")
        else:
            out.append(c)
    out.append('"')
    return "".join(out)


CUSTOMERS = ["Acme Tools", "Zoë Martin", "Łukasz Nowak", "東京ストア",
             "O'Brien & Sons", "Nordwind GmbH", "Café Olé"]
SKUS = [("sku-1001", "Hex key set", "12.50"), ("sku-1002", "Cordless drill", "89.00"),
        ("sku-1003", "Wood glue", "4.95"), ("sku-1004", "Safety goggles", "7.20"),
        ("sku-1005", "Tape measure 5 m", "9.99"), ("sku-1006", "Router bits", "34.10"),
        ("sku-1007", "Sandpaper pack", "3.05"), ("sku-1008", "Clamp 300 mm", "15.75")]
STATUS = ["paid", "paid", "paid", "pending", "refunded", "paid", "shipped"]
NOTES = ["", "Leave at the back door", "Rechnung bitte per E-Mail",
         "fragile \U0001F4E6 handle with care", "Tab\tseparated\tnote",
         'Says "urgent"', "Line one\nLine two", "Path C:\\shop\\in"]


def orders():
    r = Lcg(2024)
    out = []
    for i in range(30):
        n = 1 + r.next(3)
        lines = []
        total = 0
        for _ in range(n):
            sku, name, price = SKUS[r.next(len(SKUS))]
            qty = 1 + r.next(4)
            cents = int(price.replace(".", ""))
            total += cents * qty
            lines.append((sku, name, qty, price))
        # A few orders carry a total that disagrees with their lines,
        # as exports from a hand-edited spreadsheet do.
        if i in (7, 19):
            total += 10
        status = STATUS[r.next(len(STATUS))]
        note = NOTES[r.next(len(NOTES))]
        o = ['    {\n',
             '      "id": %d,\n' % (5000 + i),
             '      "customer": %s,\n' % jstr(CUSTOMERS[r.next(len(CUSTOMERS))]),
             '      "status": %s,\n' % jstr(status),
             '      "placed": "2024-03-%02dT%02d:%02d:00Z",\n' % (1 + i % 28, r.next(24), r.next(60)),
             '      "lines": [\n']
        for j, (sku, name, qty, price) in enumerate(lines):
            sep = "," if j + 1 < len(lines) else ""
            o.append('        {"sku": "%s", "name": %s, "qty": %d, "price": %s}%s\n'
                     % (sku, jstr(name), qty, price, sep))
        o.append('      ],\n')
        o.append('      "total": %d.%02d,\n' % (total // 100, total % 100))
        if i % 5 == 3:
            o.append('      "discount": 0.15,\n')
        if i % 9 == 4:
            o.append('      "weight_kg": 1.2e-1,\n')
        o.append('      "gift": %s,\n' % ("true" if i % 4 == 1 else "false"))
        o.append('      "coupon": %s,\n' % ('"SPRING24"' if i % 6 == 2 else "null"))
        o.append('      "note": %s\n' % jstr(note))
        o.append('    }')
        out.append("".join(o))
    return ('{\n  "export": {"source": "shop-eu", "generated": "2024-04-01T06:00:00Z",'
            ' "schema": 3, "batch": 18446744073709551617},\n'
            '  "orders": [\n' + ",\n".join(out) + '\n  ],\n'
            '  "summary": {"count": 30, "currency": "EUR", "checksum": "\\u00e9t\\u00e9 \\ud83d\\udce6"}\n}\n')


def catalog():
    r = Lcg(77)
    items = []
    tags = ["tools", "power", "glue", "safety", "measure", "wood", "abrasive", "clamps"]
    for k, (sku, name, price) in enumerate(SKUS):
        t = ", ".join('"%s"' % tags[(k + d) % len(tags)] for d in range(1 + k % 3))
        stock = r.next(200) - 20
        items.append('  "%s": {"name": %s, "price": %s, "stock": %d, "tags": [%s], '
                     '"dims": {"w": %d, "h": %d}}' % (sku, jstr(name), price, stock, t,
                                                      10 + r.next(90), 5 + r.next(40)))
    return "{\n" + ",\n".join(items) + "\n}\n"


def events(corrupt):
    r = Lcg(5)
    kinds = ["click", "view", "search", "checkout"]
    lines = []
    for i in range(24):
        kind = kinds[r.next(len(kinds))]
        ms = r.next(4000) / 8
        extra = ''
        if kind == "search":
            extra = ', "q": %s' % jstr(["drill", "glue gun", "Schraube", "клей"][r.next(4)])
        lines.append('{"ts": "2024-03-04T10:%02d:%02dZ", "type": "%s", "user": %d, "ms": %r%s}'
                     % (i * 2 % 60, r.next(60), kind, 100 + r.next(20), ms, extra))
    if corrupt:
        lines[15] = lines[15][:31] + lines[15][45:]
    return "\n".join(lines) + "\n"


def sensors():
    vals = ["21.5", "2.15e1", "-0.0", "1E-3", "6.02214076e23", "1e-400", "123456789.123456789",
            "0.1", "3", "-17", "1e308", "4.9e-324"]
    rows = []
    for i, v in enumerate(vals):
        rows.append('  {"id": "s%d", "v": %s}' % (i, v))
    return "[\n" + ",\n".join(rows) + "\n]\n"


def main():
    put("shop/orders.json", orders())
    put("shop/catalog.json", catalog())
    put("shop/events.jsonl", events(False))
    put("shop/events_bad.jsonl", events(True))
    put("shop/sensors.json", sensors())
    put("odd/bom.json", b"\xef\xbb\xbf" + b'{"ok": true}\n')
    put("odd/latin1.json", '{"name": "Café", "city": "Köln"}\n'.encode("latin-1"))
    put("odd/cut_char.json", b'{"ok": true}\n\xe2\x82')
    put("odd/control.json", '{"note": "tab\there"}\n')
    put("odd/newline.json", '["one\ntwo"]\n')
    put("odd/spaces.json", "[1,\u00a02,\u30003,\u2028 4]\r\n")
    put("odd/deep.json", "[" * 40 + "7" + "]" * 40 + "\n")
    put("odd/empty.json", b"")
    put("odd/blank.json", " \n\t\n")
    put("odd/two_docs.json", '{"a": 1}\n{"a": 2}\n[3]\n"four"\n')

    jobs = []

    def j(*f):
        jobs.append("\t".join(f))

    j("version")
    # The basic events, with every scalar form.
    j("basic", '=[1, -2, 3.50, 1e5, 1E-2, -0, -0.0, 0e0, +7, true, false, null, "s", [], {}]')
    j("basic", '=[1, -2, 3.50, 1e5, 1E-2, -0, -0.0, 0e0, +7]', "float=1")
    j("basic", "=[+007, -.5, 1.e3, 12345678901234567890123, 0.000001, 123e-9]")
    j("basic", "=[1e400, 1e-400]")
    j("basic", "=[1e400]", "float=1")
    j("basic", "=[1e-400, 2.5E+2]", "float=1")
    j("basic", '={"a": {"b": [1, {"c": null}]}, "d": "x"}')
    j("basic", '=  "just a string"  ')
    j("basic", "=42")
    j("basic", "=4.20")
    j("basic", '=["\\u00e9\\u00E9", "\\ud83d\\ude00", "a\\"b", "a\\\\b", "\\/", "\\b\\f\\n\\r\\t"]')
    j("basic", '=["caf\u00e9", "\u6771\u4eac", "\U0001F600", "nb\u00a0sp", "ls\u2028x"]')
    # Errors from the lexer and the parser.
    for doc in ["", "   ", "[1, 2,", "[1 2]", '{"a" 1}', '{"a":1,}', "{1:2}", "[01]", "[-01]",
                "[00]", "[-00]", "[1.]", "[.5]", "[-]", "[+]", "[e5]", "[1e]", "[1.5.5]",
                "[tru]", "[t]", "[nul", "[fals", "[True]", "[nan]", "[inf]", "[0x1F]", "[1x]",
                "[1]]", "]", '{"a":}', '{"a":1', "[[[]]", "@", "[1]x", "1 2", "[1,,2]",
                '{"a",1}', '{"a":1 "b":2}', "[1] [2]", '"unterminated', '["ok", "nope',
                "[-0.e1]", "[0.]", "[1e+]", "[1e5.5]", "[--1]", "[+-1]", "[1-2]", "[1_000]"]:
        j("basic", "=" + doc)
    j("basic", "=1 2", "multi=1")
    j("basic", "=[1]x", "multi=1")
    j("basic", "=[1] [2] {} 3 \"s\" null", "multi=1")
    j("basic", "=[1] [2", "multi=1")
    j("basic", "=", "multi=1")
    j("basic", "=[1]", "comments=1")
    # Strings go through json.decoder.scanstring, so its errors and
    # positions are relative to the string lexeme.
    for doc in ['["a\\x"]', '["ab\\u12"]', '["\\u12zz"]', '["\\uD83D\\uZZZZ"]', '["\\"]',
                '["a\\\\"]', '["a\\\\\\"b"]', '[1, "x\\q"]', '["\\u0041\\u004"]',
                '["\\ud83d\\ude00\\u0021"]']:
        j("basic", "=" + doc)
    j("basic", "data/odd/control.json")
    j("basic", "data/odd/newline.json")
    j("basic", "data/odd/spaces.json")
    j("basic", "data/odd/bom.json")
    j("basic", "data/odd/latin1.json")
    j("basic", "data/odd/latin1.json", "buf=5")
    j("basic", "data/odd/latin1.json", "buf=13")
    j("basic", "data/odd/cut_char.json")
    j("basic", "data/odd/empty.json")
    j("basic", "data/odd/blank.json")
    j("basic", "data/odd/two_docs.json")
    j("basic", "data/odd/two_docs.json", "multi=1")
    j("basic", "data/odd/deep.json", "take=3")
    j("basic", "data/missing.json")
    # The chunk size decides which events come out before an error:
    # the events of the chunk that fails are lost.
    for b in ["1", "3", "8", "64"]:
        j("basic", '=[10, 20, 30, 40, 50, 60, oops, 80]', "buf=" + b)
    j("basic", '=[1, 2, "a long string that crosses several chunks", 3]', "buf=4")
    j("basic", '=[123456, 7, "\\u00e9\\"x", true]', "buf=2")
    j("basic", '=["\u00e9\u00e9\u00e9", "\U0001F600"]', "buf=1")
    # parse(): the prefixes.
    j("parse", '={"a": {"b": [1, {"c": null}]}, "d": "x"}')
    j("parse", '={"a.b": {"c": 1}, "a": {"b": {"c": 2}}}')
    j("parse", '=[[1, [2]], {"k": [3]}]')
    j("parse", '={"": {"": 1}, "item": [2]}')
    j("parse", "=[1] {\"a\": 2}", "multi=1")
    j("parse", "data/shop/catalog.json", "take=24")
    j("parse", "data/shop/orders.json", "take=40", "buf=16")
    j("parse", "data/shop/orders.json", "take=40", "float=1")
    # items() and kvitems().
    j("items", "data/shop/orders.json", "orders.item.customer")
    j("items", "data/shop/orders.json", "orders.item.lines.item", "take=12")
    j("items", "data/shop/orders.json", "orders.item", "take=2")
    j("items", "data/shop/orders.json", "orders.item", "take=2", "map=od")
    j("items", "data/shop/orders.json", "export")
    j("items", "data/shop/orders.json", "summary")
    j("items", "data/shop/orders.json", "summary.checksum")
    j("items", "data/shop/orders.json", "nothing.here")
    j("items", "data/shop/orders.json", "orders.item.discount")
    j("items", "data/shop/orders.json", "orders.item.weight_kg", "float=1")
    j("items", "data/shop/catalog.json", "")
    j("items", "data/shop/catalog.json", "", "map=od")
    j("items", "data/shop/catalog.json", "sku-1004.tags.item")
    j("items", "data/shop/catalog.json", "sku-1004.dims")
    j("items", "data/shop/sensors.json", "item.v")
    j("items", "data/shop/sensors.json", "item.v", "float=1")
    j("items", "data/shop/events.jsonl", "", "multi=1", "take=3")
    j("items", "data/shop/events.jsonl", "", "take=3")
    j("items", "data/shop/events.jsonl", "type", "multi=1", "take=6")
    j("items", "data/shop/events_bad.jsonl", "", "multi=1", "buf=256")
    j("items", "data/shop/events_bad.jsonl", "", "multi=1", "buf=64")
    j("items", "data/odd/two_docs.json", "", "multi=1")
    j("items", "data/odd/two_docs.json", "a", "multi=1")
    j("items", '={"a": 1, "b": 2, "a": {"x": [1, 2]}, "c": {}}', "")
    j("items", '={"a": 1, "b": 2, "a": {"x": [1, 2]}, "c": {}}', "", "map=od")
    j("items", '=[[], [[]], {}, [{}], {"a": []}]', "item")
    j("items", '=[1, [2, 3], {"a": 4}]', "item.item")
    j("items", '={"a": [1, 2, 3, "x", 4]}', "a.item", "buf=3")
    j("items", "data/odd/deep.json", "item.item.item.item.item.item.item.item.item.item")
    j("count", "data/shop/orders.json", "orders.item")
    j("count", "data/shop/orders.json", "orders.item.lines.item", "buf=1")
    j("count", "data/shop/orders.json", "orders.item.lines.item", "buf=7")
    j("count", "data/shop/catalog.json", "sku-1002.tags.item")
    j("kvitems", "data/shop/catalog.json", "", "take=3")
    j("kvitems", "data/shop/catalog.json", "sku-1001")
    j("kvitems", "data/shop/catalog.json", "sku-1001.dims", "map=od")
    j("kvitems", "data/shop/orders.json", "export")
    j("kvitems", "data/shop/orders.json", "orders.item", "take=11")
    j("kvitems", '={"a": [1, {"b": 2}], "c": {"d": {"e": 3}}, "f": null}', "")
    j("kvitems", '=[{"x": 1}, 5, {"y": [2]}, [], {"z": {}}]', "item")
    j("kvitems", '={"a": 1}', "a")
    j("kvitems", '={"a": {"k": 1, "k": 2}}', "a")
    j("kvitems", '={"a": {"b": 1}', "a")
    # The push interface, as a network reader would drive it.
    j("push", "items", '=[{"name": "caf\u00e9"}, {"name": "na\u00efve"}, 3]', "item", "cuts=4,15,16,30")
    j("push", "basic_parse", '=[1, 2, 3]', "", "cuts=2,2,5")
    j("push", "basic_parse", '={"ok": true}', "", "cuts=6")
    j("push", "parse", '={"a": [1, 2], "b": {"c": "\u00e9"}}', "", "cuts=1,8,24,26")
    j("push", "kvitems", '={"a": 1, "b": [2, 3], "c": {"d": 4}}', "", "cuts=10,20")
    j("push", "items", "data/odd/cut_char.json", "", "cuts=")
    j("push", "items", '=[1, 2', "item", "cuts=3")
    j("push", "basic_parse", '=[1, oops]', "", "cuts=3")
    j("push", "basic_parse", "x:" + b"[1, 25\xff]".hex(), "", "cuts=6")
    j("basic", "x:" + b"[1, 25\xff]".hex())
    j("basic", "x:" + b"[1, 25\xff]".hex(), "buf=6")
    j("push", "items", "data/shop/events.jsonl", "type", "cuts=100,200,300", "multi=1", "take=8")
    # The dump command-line tool.
    j("dump", '={"a": [1, 2.5, "x"], "b": {"c": null}}')
    j("dump", '={"a": [1, 2.5, "x"], "b": {"c": null}}', "method=parse")
    j("dump", '={"a": [1, 2.5, "x"], "b": {"c": null}}', "method=items", "prefix=a.item")
    j("dump", '={"a": [1, 2.5, "x"], "b": {"c": null}}', "method=kvitems", "prefix=b")
    j("dump", '={"a": [1, 2.5, "x"], "b": {"c": true}}', "method=items")
    j("dump", "data/odd/two_docs.json", "method=items", "multi=1")
    j("dump", "data/odd/two_docs.json", "method=kvitems")
    j("dump", "data/shop/sensors.json", "method=items", "prefix=item")
    # Programs.
    j("report", "data/shop/orders.json", "data/out/report.txt")
    j("cat", "data/out/report.txt")
    j("latency", "data/shop/events.jsonl", "data/out/latency.csv")
    j("cat", "data/out/latency.csv")
    j("latency", "data/shop/events_bad.jsonl", "data/out/latency_bad.csv")
    j("cat", "data/out/latency_bad.csv")
    j("schema", "data/shop/catalog.json")
    j("schema", "data/shop/orders.json")
    j("extract", "data/shop/orders.json", "orders.item.lines.item", "data/out/lines.jsonl")
    j("cat", "data/out/lines.jsonl")
    j("extract", "data/shop/sensors.json", "item", "data/out/sensors.jsonl")
    j("cat", "data/out/sensors.jsonl")
    j("extract", "data/shop/orders.json", "summary", "data/out/summary.jsonl")
    j("cat", "data/out/summary.jsonl")

    with open(os.path.join(DATA, "jobs.tsv"), "w", encoding="utf-8") as f:
        f.write("\n".join(jobs) + "\n")
    with open(os.path.join(DATA, "files.txt"), "w") as f:
        f.write("\n".join(written) + "\n")
    print(len(written), "files,", len(jobs), "jobs")


main()
