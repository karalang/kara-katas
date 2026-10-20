# Writes data/: jobs.tsv, one job a line as "<op>\t<python str literal>",
# where op is `parse` (ast.parse, then ast.dump and ast.unparse), `attrs`
# (ast.dump with the positions) or `eval` (ast.literal_eval); and
# project/, a small package for the programs. Run it from the app
# directory.
import os
import shutil

PARSE = [
    # statements
    "x = 1",
    "a = b = c",
    "x, = y",
    "a, *b = c",
    "*a, b = c",
    "x @= y",
    "x //= 2; y **= 3; z >>= 1",
    "x: int",
    "x: list[int] = []",
    "(x): int = 1",
    "x.y: int",
    "del a[0], b.c, (d, e)",
    "pass; break; continue",
    "return",
    "return *a, b",
    "raise",
    "raise E from c",
    "assert x, 'm'",
    "global a, b",
    "nonlocal x",
    "import a.b.c as d, e",
    "from ... import x",
    "from .a.b import *",
    "from x import (a, b as c,)",
    "from . import mod",
    "if a:\n    pass\nelif b:\n    pass\nelif c:\n    x\nelse:\n    y",
    "if a:\n    pass\nelse:\n    if b:\n        pass",
    "while x:\n    break\nelse:\n    continue",
    "for i, j in x: pass",
    "for x in *a, *b: pass",
    "for (a, b) in c:\n    pass\nelse:\n    d",
    "try:\n  pass\nexcept E as e:\n  pass\nexcept (A, B):\n  pass\nexcept:\n  raise\nelse:\n  pass\nfinally:\n  pass",
    "try:\n  pass\nfinally:\n  pass",
    "try:\n  pass\nexcept* E: pass",
    "with a as b, c: pass",
    "with (a as b, c as d): pass",
    "with (a, b): pass",
    "with (yield): pass",
    "with open(p) as f, lock:\n    data = f.read()",
    "def f(): pass",
    "def f(a, /, b=2, *c, d, e=3, **g) -> int:\n    \"doc\"\n    return a",
    "def f(a, b=1, /, c=2): pass",
    "def f(*, a, b=1): pass",
    "def f(a: int = 0, *args: str, **kw: 'T') -> None: ...",
    "@d\n@e.f(1)\ndef g(): pass",
    "@property\ndef x(self): return self._x",
    "async def f():\n    async for x in y: pass\n    async with a: pass\n    await b\n    return [i async for i in z]",
    "class C: pass",
    "class C(B, metaclass=M):\n    '''Doc.'''\n    x = 1\n\n    def m(self): pass",
    "class C(*bases, **kw): pass",
    "@dataclass\nclass P:\n    x: int\n    y: int = 0",
    "def f():\n    yield\n    yield x\n    yield x, y\n    yield from z\n    x = yield",
    "x = (yield)",
    "if x:\n    pass\n\n# comment\ny = 2  # trailing",
    "x = [\n    1,\n    2,  # two\n]",
    "x = 1 + \\\n    2",
    # expressions
    "x = 1_000 + 0x_ff + 0o17 + 0b101 + 1e-3 + 2.5j + 1E5 + .5 + 5. + 0j",
    "x = 10**100 + 0xffffffffffffffffffffffff + 18446744073709551616",
    "x = 1e400 + 1.5e-320 + 3.14159265358979323846 + 0.1 + 1e16 + 1e-05 + 123456789012345678.0",
    "...",
    "x[...]",
    "True, False, None",
    "not a or b and c",
    "a and b and c or d or e",
    "(a or b) and c",
    "not not x",
    "-x ** 2",
    "(-x) ** 2",
    "a ** b ** c",
    "(a ** b) ** c",
    "a - b - c",
    "a - (b - c)",
    "a * b + c * d",
    "(a + b) * c",
    "a << b + c & d | e ^ f",
    "~a + -b * +c",
    "a @ b / c // d % e",
    "a < b < c",
    "a is not b, a not in b, a in b, a is b",
    "a == b != c <= d >= e > f",
    "(a < b) < c",
    "x if y else z",
    "a if b else c if d else e",
    "(a if b else c) if d else e",
    "lambda: 0",
    "lambda x, *y, z=1, **w: x",
    "lambda x=1, /, y=2: (x, y)",
    "lambda *, k: k",
    "f(lambda x: x + 1, key=lambda y: -y)",
    "x = [y := 1, y**2]",
    "if (n := len(a)) > 10: pass",
    "f(x := 1)",
    "a.b.c(d)[e](f)",
    "f(a)(b)",
    "f(a, *b, k=1, **c)",
    "f(*a, *b, **c, **d)",
    "f(x for x in y)",
    "f(a, b=1, *c)",
    "print(*a, sep='')",
    "x[1:2, ::3]",
    "x[a:b:c, d]",
    "x[:]",
    "x[::]",
    "x[1:]",
    "x[i, j]",
    "x[(i, j)]",
    "x[*a]",
    "x[()]",
    "3 .real",
    "(3).real",
    "1.5.real",
    "'a'.join(b)",
    "[*a, *b]",
    "[]",
    "[1, [2, [3]]]",
    "{**a, 'b': 1}",
    "{1, 2}",
    "{1: 2, **{3: 4}}",
    "{}",
    "()",
    "(1,)",
    "(1, 2)",
    "(x)",
    "((x, y), z)",
    "[x for x in y]",
    "[x for x in y if x if not z for w in x]",
    "{x for x in y}",
    "{k: v for k, v in d.items()}",
    "(x for x in y)",
    "[(a, b) for a, b in c]",
    "[x async for x in y]",
    "[await x for x in y]",
    "[i for i in (yield)]",
    "x = *a, *b",
    "a, b = b, a",
    "x = yield from y",
    # strings
    "'a' 'b'",
    "x = 'a' 'b'",
    "b'a' b'b'",
    "u'a' 'b'",
    "'a' u'b'",
    "x = '''a\nb'''",
    "x = 'it''s'",
    "x = \"it's\"",
    "x = 'say \"hi\"'",
    "x = 'both \\' and \"'",
    "x = '\\x41\\101\\u00e9\\U0001F600\\n\\t\\0'",
    "x = r'\\d+\\.' + R\"\\w\"",
    "x = b'\\x00\\xff' + rb'\\x'",
    "x = '\\\\'",
    "x = 'tab\\there'",
    "x = 'line\\\nbreak'",
    "x = '\u00e9\u4e2d'",
    "x = '\\x7f\\x80\\xa0'",
    "x = '''one\ntwo''' + \"\"\"three\"\"\"",
    "x = \"ends with quote'\"",
    "x = '''ends with '\"'''",
    # f-strings
    "f'{x}'",
    "f'a{b}c'",
    "f\"{x=}\"",
    "f\"{x = !s:>3}\"",
    "f'{x!r}'",
    "f'{x!a}'",
    "f'{x:{y}}'",
    "f'{x:>{w}.{p}f}'",
    "f'{x:%H:%M}'",
    "f'{x:{{}}>3}'",
    "f'a' 'b' f'{c}'",
    "f'{x!r}' ''",
    "''f'{x}'",
    "f''",
    "f'{{x}}'",
    "f'{{'",
    "f'{x}}}'",
    "f'{a}{b}'",
    "f'{\"q\"}'",
    "f\"{'q'}\"",
    "f'{x}\\n'",
    "f'''{x}\n'''",
    "f'{x:\\n}'",
    "f'{ x }'",
    "f'{x,y}'",
    "f'{(x, y)}'",
    "f'{ {1: 2}[1] }'",
    "f'{x if y else z}'",
    "f'{lambda: 1}'",
    "f'{(lambda: 1)()}'",
    "f'{3.14:.2f} {n:,} {s!r:^10}'",
    "f'{f\"{x}\"}'",
    "rf'\\d{x}'",
    "f'{x}' f'{y}'",
    "f'quote \\' {x}'",
    "f'\"{x}\"'",
    "f'{x:{y:{z}}}'",
    "print(f'{name}: {value!r:>{width}}')",
    "u'a' f'{b}'",
    "f'{x=!r:10}'",
    "f'{x=:10}'",
    "f'{ x = }'",
]

ATTRS = [
    "x = 1",
    "x = 'é' + y",
    "if a:\n    b = [1,\n         2]",
    "f'{x}' + f'a{y!r}'",
    "def f(a, *, b): return a",
    "class C:\n    @d\n    def m(self): pass",
]

ERRORS = [
    "x = (1, 2",
    "f(a,\n  b",
    "x = {1: 2",
    "x = 1)",
    "x = (1]",
    "x = (\n1]",
    "x = 'abc",
    "x = '''abc",
    "f\"{a\"",
    "x = 0777",
    "x = 1 +",
    "x = 1 2",
    "def f(:\n pass",
    "x =\n",
    "return return",
    "a b",
    "nonlocal",
    "for x in : pass",
    "import a.b as",
    "from . import *, a",
    "x = [i for i in]",
    "class C(x for x in y): pass",
    "x := 1",
    "if x\n  pass",
    "while x\n  pass",
    "def f()\n  pass",
    "class C\n  pass",
    "if x:\npass",
    "def f():\nreturn",
    "for x in y:\n\nz",
    "class C:\n    def m(self):\n    pass",
    "try:\nx",
    "if a:\n  b\nelse:\nc",
    "    x = 1",
    "x = 1\n  y = 2",
    "if x:\n    a\n        b",
    "if x:\n  pass\n else:\n  pass",
    "1 = x",
    "f() = 1",
    "a + 1 = 2",
    "x.y + 1 = 2",
    "[a, 1] = b",
    "for 1 in x: pass",
    "del f()",
    "del a + b",
    "True = 1",
    "(a, b) += 1",
    "f() += 1",
    "f(k=1, a)",
    "f(**k, a)",
    "f(a for a in b, c)",
    "def f(a=1, b): pass",
    "lambda x=1, y: 0",
    "x = 1 if y",
    "import",
]

EVALS = [
    "1",
    "-1",
    "+2.5",
    "1+2j",
    "-1-2j",
    "3j",
    "'abc'",
    "b'x\\x00'",
    "[1, 'two', (3, 4.0), None, True]",
    "{'a': 1, 'b': [2, 3], 'c': {'d': None}}",
    "(1,)",
    "()",
    "{}",
    "set()",
    "  [1, 2]",
    "{'k': -0.5, 'j': 1e100, 'big': 123456789012345678901234567890}",
    "'multi' 'part'",
    "[1, 2,]",
    "1 + 2",
    "x",
    "f(1)",
    "-'a'",
    "{**a}",
    "[1, 2] + [3]",
    "(1, [2, (3, {'x': ()})])",
]

PROJECT = {
    "shop/__init__.py": '''"""A small shop: products, carts and prices."""

from .models import Product, Cart
from .pricing import total, apply_discount

__all__ = ["Product", "Cart", "total", "apply_discount"]
__version__ = "1.4.0"
''',
    "shop/models.py": '''"""The data the shop keeps."""
from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Iterator, Optional
import json, os


@dataclass(frozen=True)
class Product:
    """A thing for sale.

    Prices are in cents, so sums stay exact.
    """

    sku: str
    name: str
    price: int
    tags: tuple[str, ...] = ()

    def label(self, *, currency: str = "EUR") -> str:
        return f"{self.name} ({self.price / 100:.2f} {currency})"


@dataclass
class Line:
    product: Product
    qty: int = 1


class Cart:
    """Lines by SKU."""

    def __init__(self, owner: Optional[str] = None) -> None:
        self.owner = owner
        self._lines: dict[str, Line] = {}

    def add(self, product: Product, qty: int = 1) -> None:
        if qty <= 0:
            raise ValueError(f"bad quantity {qty!r}")
        line = self._lines.get(product.sku)
        if line is None:
            self._lines[product.sku] = Line(product, qty)
        else:
            line.qty += qty

    def remove(self, sku: str) -> bool:
        return self._lines.pop(sku, None) is not None

    def __iter__(self) -> Iterator[Line]:
        yield from sorted(self._lines.values(), key=lambda l: l.product.sku)

    def __len__(self):
        return sum(l.qty for l in self._lines.values())

    @property
    def empty(self) -> bool:
        return not self._lines
''',
    "shop/pricing.py": '''"""Totals, discounts and tax."""
import math
from decimal import Decimal, ROUND_HALF_UP
from .models import Cart, Line

TAX_RATES = {"standard": 0.21, "reduced": 0.09, "zero": 0.0}
BULK = [(100, 0.15), (50, 0.10), (10, 0.05)]


def line_price(line: Line) -> int:
    for threshold, rate in BULK:
        if line.qty >= threshold:
            return round(line.product.price * line.qty * (1 - rate))
    return line.product.price * line.qty


def total(cart: Cart, tax: str = "standard") -> int:
    """The cart's total in cents, tax included."""
    try:
        rate = TAX_RATES[tax]
    except KeyError:
        raise ValueError(f"unknown tax class: {tax}") from None
    net = sum(line_price(l) for l in cart)
    return int(Decimal(net * (1 + rate)).quantize(Decimal(1), ROUND_HALF_UP))


def apply_discount(amount, code=None, *, codes=None):
    codes = codes or {}
    if not code:
        return amount
    elif code in codes and codes[code] > 0:
        pct = codes[code]
        return amount - amount * pct // 100
    elif code.startswith("FLAT") and code[4:].isdigit():
        return max(0, amount - int(code[4:]))
    else:
        return amount


def split(amount: int, ways: int) -> list[int]:
    base, extra = divmod(amount, ways)
    return [base + (1 if i < extra else 0) for i in range(ways)]
''',
    "shop/cli.py": '''#!/usr/bin/env python3
"""Command line: shop add SKU QTY, shop total."""
import argparse
import sys
import logging as log
from pathlib import Path
from . import models
from .pricing import total, split as split_amount

CATALOG = {
    "A1": models.Product("A1", "Mug", 850, ("kitchen",)),
    "B2": models.Product("B2", "Tea", 1299),
}


def parse_args(argv=None):
    p = argparse.ArgumentParser(prog="shop")
    sub = p.add_subparsers(dest="cmd", required=True)
    add = sub.add_parser("add")
    add.add_argument("sku")
    add.add_argument("qty", type=int, nargs="?", default=1)
    sub.add_parser("total")
    return p.parse_args(argv)


async def fetch_rates(session, url):
    async with session.get(url) as resp:
        async for chunk in resp.content:
            yield chunk


def main(argv=None) -> int:
    args = parse_args(argv)
    cart = models.Cart()
    while True:
        try:
            if args.cmd == "add":
                cart.add(CATALOG[args.sku], args.qty)
            break
        except KeyError as e:
            print(f"no such product: {e}", file=sys.stderr)
            return 1
        finally:
            log.debug("done")
    with open(Path("cart.txt"), "w") as out, open("log", "a"):
        for line in cart:
            out.write(f"{line.product.sku}\\t{line.qty}\\n")
    print(total(cart), *split_amount(total(cart), 3), sep=", ")
    return 0 if len(cart) else 2


if __name__ == "__main__":
    sys.exit(main())
''',
    "shop/util/text.py": '''"""Text helpers."""
import re
import unicodedata as ud

_WS = re.compile(r"\\s+")


def slug(s: str, sep="-") -> str:
    s = ud.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return sep.join(w for w in _WS.split(s.lower()) if w.isalnum())


def wrap(text, width=70):
    words, line, out = text.split(), [], []
    for w in words:
        if line and len(" ".join(line + [w])) > width:
            out.append(" ".join(line))
            line = [w]
        else:
            line.append(w)
    if line:
        out.append(" ".join(line))
    return "\\n".join(out)


def ellipsis(s, n):
    return s if len(s) <= n else s[: n - 1] + "\\u2026"


def counts(words):
    seen = {}
    for w in words:
        seen[w] = seen.get(w, 0) + 1
    return {k: v for k, v in sorted(seen.items(), key=lambda kv: (-kv[1], kv[0])) if v > 1}
''',
    "shop/util/__init__.py": '',
}


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


if os.path.exists("data"):
    shutil.rmtree("data")
os.makedirs("data")
with open("data/jobs.tsv", "w", encoding="utf-8", newline="") as f:
    for op, items in (("parse", PARSE), ("attrs", ATTRS), ("parse", ERRORS), ("eval", EVALS)):
        for s in items:
            f.write("%s\t%r\n" % (op, s))
for name, text in PROJECT.items():
    write("data/project/" + name, text)
