# Writes data/: jobs.tsv (snippets for tokenize.generate_tokens, one a
# line as a Python str literal after "snippet\t") and project/, a small
# Python code base, and broken/, files that each stop the tokenizer
# somewhere, for the programs. Run it from the app directory.
import os
import shutil

SNIPPETS = [
    # layout: indents, dedents, blank and comment lines, continuations
    "def f(a, b=2):\n    \"\"\"doc\"\"\"\n    # comment\n    x = a + b  # trailing\n\n    if x:\n        return x\n    return 0\n",
    "if a:\n    b\n# c\n  # d\nc\n",
    "def f():\n    pass\n  # x\n",
    "x = 1 # c\n   # c2\ny\n",
    "x = 1\n    \n  \ny\n",
    "if x:\n  y = (1,\n2)\n  z\n",
    "x = [\n  1, # one\n  2,\n]\n",
    "a = 1\\\n  + 2\n",
    "x = 1 \\\n\n",
    "x = 0\n\x0c\ny = 1\n",
    "if a:\n    b\n\n\n",
    "\n  x\n",
    "  x = 1\n",
    "  # c\nx\n",
    "def f():\n  pass\n\n# end",
    "x = 1",
    "x = 1\n\n\n# c",
    "x = 1\r\ny = 2\r\n",
    "x = 1\r\n# c\r\n",
    "\n\n",
    "",
    "# only\n",
    "#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n",
    "def f():\n\tif x:\n\t\ty\n\tz\n",
    "class C:\n    def m(self):\n        return f'{self!r}'\n",
    "async def f():\n    await x\n",
    "match x:\n    case [a, *_]: pass\n",
    # names, numbers, operators
    "x = 1if y else 2\n",
    "x = .5 + 5. + 1j + 0o17 + 0xfg\n",
    "x = 0xFF_FF + 0o7_7 + 0b1_0 + 1_0.0_1e1_0\n",
    "x = 0x_1 + 1.e5 + 1e+5j + 1.5_2 + 1._5 + 00 + 007 + 0_0 + 01\n",
    "x = 1j2 + 0x1for + 1or 2\n",
    "x = 0b1and 1.0e5if 12abc\n",
    "x = 3.14.15 + ..5 + 1..2 + 1. .2\n",
    "x = 0e0 + 0E-0_1 + 1_2.3_4e5_6J + 0j + 09.5 + 09j + 09e1 + 0_9\n",
    "x = 0B1 + 0XFF + 1L + 1e_5 + 1e\n",
    "x = a->b; c @= d ** e // f != g <> h\n",
    "x = 1 $ 2 ? 3 ! 4\n",
    "x = a<<=b>>=c//=d**=e...f:=g\n",
    "@dec\nclass A(B, metaclass=M): ...\n",
    "x: int = 5\nif (n := 10) > 5: pass\n",
    "lambda *a, **k: a\n",
    "x = {'a': [1, (2, 3)]}\n",
    "x = )\n",
    "x = (]\n",
    "\u00e9 = '\u00fc'\n",
    "\u03c0 = 3.14 # \u00e9\n",
    # strings
    "x = 'a' 'b'\n",
    "x = rb'\\d' + Rb\"x\" + br'' + U'u'\n",
    "x = 'a\\'b' \"c\\\"d\"\n",
    "x = '\\N{BULLET}'\n",
    "s = '''a\nb''' + 'c'\n",
    "x = '\\\n'\n",
    "'''\n'''\n",
    # f-strings
    "return f\"v={x!r:>{b}} {{lit}}\"\n",
    "f'{x!r}' f\"{'a'}\" rf'\\{x}' F'{{}}' f'{x:>10}' f'{3.5:.2f}'\n",
    "print(f'{x=}', f'{x = !r}', f'{x:{w}.{p}f}', f'''a\n{b}''')\n",
    "f'''{\nx\n}'''\n",
    "f'{x:{y}}'\n",
    "f'a{b}c{d:e}f'\n",
    "f'{}'\n",
    "f'{\"a\" if x else \"b\"}'\n",
    "f'{x}' 'y' f'z{w}'\n",
    "f'\\N{BULLET} {x}'\n",
    "f'{x!r:^{w}}'\n",
    "x = f'{a}' f''\n",
    "x = f'{a!}' f'{a!r x}' f'{a b}'\n",
    "x = f'{lambda x: 1}'\n",
    "x = f\"{d['k']}\" f'{d[\"k\"]}'\n",
    "x = f'{f'{1}'}'\n",
    "x = f'''{x\n}'''\n",
    "x = f'{x:%H:%M}' f'{x:{y}d}' f'{x:a{{b}}c}'\n",
    # errors
    "x = 'abc\n",
    "x = '''abc\n",
    "s = 1\nt = '''ab\ncd\n",
    "s = 1\nt = f'''ab\ncd\n",
    "x = 'abc\\'\n",
    "x = b'\\xff' rb'\\'\n",
    "x = f'ab\n",
    "if x:\n    y\n  z\n",
    "if x:\n\ty\n        z\n",
    "if x:\n        y\n\tz\n",
    "x = (1,\n",
    "x = (1,",
    "x = (1,\n\n",
    "x = (1,\n  2,\n",
    "x = 5 if a else\\\n",
    "y = 1\nx = 1 \\",
    "x = 1 \\ y\n",
    "x = 1 \\ \n",
    "x = 0b102\n",
    "x = 0o8\n",
    "x = 1__0\n",
    "x = 1_000_\n",
    "x = 0x\n",
    "x = 0b\n",
    "x = 0o\n",
    "x = 0b1_\n",
    "x = 1e+\n",
    "x = 1_a\n",
    "x = 0xg\n",
    "x = 1e5_\n",
    "x = 0x1_\n",
    "x = 0__1\n",
    "x = f'{a'\n",
    "x = f'{'\n",
    "x = f'{x}}'\n",
    "x = f'{x:'\n",
    "x = f'{a:\n",
    # more f-string corners
    "f'''{x:a\nb}'''\n",
    "f'''ab\ncd{x}\nef'''\n",
    "f'{{{x}}}' f'{x!r:{y}}'\n",
    "f'''a''b'''\n",
    "f'{x:{y:{z}}}'\n",
    "f'{a:=^10}' f'{(a:=1)}'\n",
    "f'{x}' rf\"\\N{{y}}\"\n",
    # more layout
    "if x:\n  \\\n    y\n",
    "x = a`b\n",
    "x = 1;\n",
    "class A:\n  def f(): pass\n\n\n  def g(): pass\n",
]

PROJECT = {}

PROJECT["inventory/models.py"] = '''"""Data model for the inventory service."""
from __future__ import annotations

import dataclasses
from decimal import Decimal
from typing import Optional

LOW_STOCK = 5  # reorder below this


@dataclasses.dataclass(frozen=True)
class Item:
    """One stock-keeping unit."""

    sku: str
    name: str
    price: Decimal
    qty: int = 0
    tags: tuple[str, ...] = ()

    @property
    def low(self) -> bool:
        return self.qty < LOW_STOCK

    def label(self, width: int = 30) -> str:
        # TODO: truncate long names with an ellipsis
        return f"{self.sku:<8} {self.name:{width}.{width}} {self.price:>8.2f}"

    def __repr__(self) -> str:
        return f"Item({self.sku!r}, qty={self.qty})"


class Store:
    def __init__(self, items: Optional[list[Item]] = None):
        self.items = {i.sku: i for i in items or []}

    def total(self) -> Decimal:
        return sum((i.price * i.qty for i in self.items.values()),
                   Decimal("0"))

    def restock(self, sku: str, n: int) -> Item:
        item = self.items[sku]
        if n <= 0:
            raise ValueError(f"bad quantity {n} for {sku}")
        self.items[sku] = dataclasses.replace(item, qty=item.qty + n)
        return self.items[sku]
'''

PROJECT["inventory/db.py"] = '''import sqlite3
import contextlib

SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
    sku   TEXT PRIMARY KEY,
    name  TEXT NOT NULL,
    price TEXT NOT NULL,
    qty   INTEGER DEFAULT 0
);
"""


@contextlib.contextmanager
def connect(path=":memory:"):
    conn = sqlite3.connect(path)
    try:
        conn.executescript(SCHEMA)
        yield conn
    finally:
        conn.close()


def fetch_rows(conn, low_only=False):
    sql = "SELECT sku, name, price, qty FROM items"
    if low_only:
        sql += " WHERE qty < ?"  # FIXME: use the LOW_STOCK constant
    rows = conn.execute(sql, (5,) if low_only else ()).fetchall()
    return [dict(zip(("sku", "name", "price", "qty"), r)) for r in rows]


def count(conn):
    (n,), = conn.execute("SELECT count(*) FROM items")
    return n


async def fetch_rows_async(pool, low_only=False):
    async with pool.acquire() as conn:
        return await conn.run_sync(lambda c: fetch_rows(c, low_only))
'''

PROJECT["inventory/report.py"] = '''\ufeff# Prints the stock report.
import sys
from .db import connect, fetch_rows, count

WIDTH = 72
HEADER = f"{'SKU':<8} {'Name':<30} {'Price':>8} {'Qty':>5}"


def money(x: float) -> str:
    return f"${x:,.2f}" if x >= 0 else f"-${-x:,.2f}"


def bar(n, scale=0.5):
    return "#" * int(n * scale) + ("+" if n % 2 else "")


def report(path, out=sys.stdout, *, low_only=False):
    with connect(path) as conn:
        rows = fetch_rows(conn, low_only=low_only)
        print(HEADER, file=out)
        print("-" * WIDTH, file=out)
        for row in rows:
            match row:
                case {"qty": 0}:
                    status = "out"
                case {"qty": q} if q < 5:
                    status = "low"
                case _:
                    status = "ok"
            price = float(row["price"])
            print(f"{row['sku']:<8} {row['name'][:30]:<30} "
                  f"{money(price):>8} {row['qty']:>5} {status} "
                  f"{bar(row['qty'])}", file=out)
        total = sum(float(r["price"]) * r["qty"] for r in rows)
        print(f"""
{count(conn)} items, {len(rows)} shown
total value {money(total)}""", file=out)
        if (n := len(rows)) > 0x10:
            print(f"note: {n} rows; use --low for a short list", file=out)


if __name__ == "__main__":
    report(sys.argv[1] if len(sys.argv) > 1 else ":memory:",
           low_only="--low" in sys.argv[2:])
'''

PROJECT["inventory/cli.py"] = '''#!/usr/bin/env python3
"""Command line for the inventory service."""
import argparse
import logging

from .db import connect, fetch_rows
from .report import report

log = logging.getLogger(__name__)


def build_parser():
    p = argparse.ArgumentParser(prog="inv")
    p.add_argument("db", nargs="?", default="inventory.sqlite3")
    p.add_argument("-v", "--verbose", action="count", default=0)
    p.add_argument("--format", choices=("text", "json", "csv"), default="text", help="report format")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("report").add_argument("--low", action="store_true")
    s = sub.add_parser("show")
    s.add_argument("sku")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.WARNING - 10 * args.verbose)
    if args.cmd == "report":
        report(args.db, low_only=args.low)
    elif args.cmd == "show":
        with connect(args.db) as conn:
            for row in fetch_rows(conn):
                if row["sku"] == args.sku:
                    print(f"{row}")
                    break
            else:
                log.error("no such sku: %s", args.sku)
                return 1
    return 0
'''

# Latin-1 with a coding cookie, tabs, and the habits of old code.
PROJECT["legacy/convert.py"] = '''# -*- coding: latin-1 -*-
# Old price converter; kept for the nightly job.  XXX remove after 2027
import string

RATE = 1.0825 #EUR->GBP
SYMBOL = "\u00a3"   # pound sign, stored as Latin-1


def convert(rows):
\tout = []
\tfor r in rows:
\t\ttry:
\t\t\tp = float(r[2]) * RATE
\t\texcept:
\t\t\tp = None
\t\tif p == None:
\t\t\tprint("skip %s" % r[0])
\t\t\tcontinue
\t\tout.append("%s;%s;%s%.2f" % (r[0], r[1], SYMBOL, p))
\treturn out


def caf\u00e9(name):
\treturn f"caf\u00e9 {name}" + f"no placeholders here"
'''

BROKEN = {
    "unterminated.py": "name = 'inventory\nprint(name)\n",
    "triple.py": 'def f():\n    """Never closed.\n    return 1\n',
    "paren.py": "items = [\n    'a',\n    'b',\n",
    "dedent.py": "def f():\n        x = 1\n    return x\n",
    "tabs.py": "def f():\n\tif x:\n\t\treturn 1\n        return 0\n",
    "number.py": "MASK = 0b1012\n",
    "fstring.py": "msg = f'{user.name'\n",
    "backslash.py": "total = a + \\ b\n",
    "brace.py": "msg = f'{x}}'\n",
}

if os.path.exists("data"):
    shutil.rmtree("data")
os.makedirs("data")


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


write("data/jobs.tsv", "".join("snippet\t%r\n" % s for s in SNIPPETS).encode("utf-8"))
for name, text in PROJECT.items():
    enc = "latin-1" if name.startswith("legacy/") else "utf-8"
    write("data/project/" + name, text.encode(enc))
for name, text in BROKEN.items():
    write("data/broken/" + name, text.encode("utf-8"))
