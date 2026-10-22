#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_baseconv: one job per line, `op \t base \t value`.

`op` is encode or decode; `base` names an alphabet (base2/16/36/56/58/62/64, plus
the two custom converters myconv and altsign); `value` is the input string. The
jobs cover the small round-trips from the library's docstring, a negative with
the default `-` sign and with a custom `$` sign, the zero case, the big-number
base64 example that overflows a machine integer, and the four invalid-digit
errors (a float dot, a base58 confusable, an out-of-range base2 bit, and an
uppercase letter decoded against the lowercase base36 alphabet).
"""
import os

JOBS = [
    ("encode", "base2", "1234"),
    ("decode", "base2", "10011010010"),
    ("encode", "base2", "0"),
    ("encode", "base16", "255"),
    ("encode", "base16", "4096"),
    ("decode", "base16", "DEADBEEF"),
    ("encode", "base36", "123456789"),
    ("decode", "base36", "zz"),
    ("encode", "base56", "1000000"),
    ("encode", "base58", "100"),
    ("encode", "base58", "-255"),
    ("decode", "base58", "2TX"),
    ("encode", "base62", "999999"),
    ("encode", "base64", "100000000000000000000000000000000000"),
    ("decode", "base64", "4q9XSiTDWYk7Z-W00000"),
    ("encode", "base64", "-5"),
    ("encode", "myconv", "1234"),
    ("decode", "myconv", "wy1"),
    ("encode", "myconv", "-1234"),
    ("decode", "myconv", "-wy1"),
    ("encode", "altsign", "-1000000"),
    ("decode", "altsign", "$cc-aaaaaa"),
    ("encode", "base56", "3.14"),
    ("decode", "base58", "0IOl"),
    ("decode", "base2", "102"),
    ("decode", "base36", "ZZZ"),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for op, base, value in JOBS:
        fh.write(op + "\t" + base + "\t" + value + "\n")
