#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_schwifty: one IBAN job per line.

    <op> \t <iban>

Three ops exercise the vendored ``schwifty.IBAN``:

  valid <iban>   validate an IBAN (prints VALID or the exact error message);
  fmt   <iban>   the IBAN formatted in blocks of four;
  parts <iban>   the BBAN's bank / branch / account components.

For a spread of countries whose BBAN specs differ (all-numeric, alphabetic
bank codes like GB, alphanumeric ``c`` fields like AD, with and without a
branch code) a spec-conforming BBAN is built from the country's ``bban_spec``
and handed to ``IBAN.from_bban``, which computes the correct mod-97 check
digits. Some IBANs are written with spaces to exercise whitespace cleaning.
The invalid cases walk each error path in ``validate``: bad characters, an
unknown country, a wrong length, a malformed BBAN, and a broken checksum.
"""
import os
import re
import sys

sys.path.insert(0, "vendor")
from schwifty import IBAN, registry  # noqa: E402

COUNTRIES = ["DE", "GB", "FR", "NL", "BE", "CH", "ES", "IT", "AT", "NO", "SE", "PL", "AD", "MT"]

_seg = re.compile(r"(\d+)!([nac])")


def make_bban(spec):
    """Build a BBAN matching bban_spec: n->digits, a->letters, c->alphanumerics."""
    out = []
    digits = "0123456789"
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for m in _seg.finditer(spec):
        n, t = int(m.group(1)), m.group(2)
        for i in range(n):
            if t == "n":
                out.append(digits[i % 10])
            elif t == "a":
                out.append(letters[i % 26])
            else:  # c: alternate letter/digit
                out.append(letters[i % 26] if i % 2 == 0 else digits[i % 10])
    return "".join(out)


os.makedirs("data", exist_ok=True)
lines = []

valids = []
for cc in COUNTRIES:
    spec = registry.get_iban_spec(cc)
    bban = make_bban(spec.bban_spec)
    valids.append(str(IBAN.from_bban(cc, bban)))

SPACED = [
    " ".join(valids[0][i : i + 4] for i in range(0, len(valids[0]), 4)),
    valids[1].lower(),  # lower-cased; cleaning upper-cases it
]

for v in valids:
    lines.append("valid\t" + v)
for s in SPACED:
    lines.append("valid\t" + s)
for v in valids:
    lines.append("fmt\t" + v)
for v in valids:
    lines.append("parts\t" + v)

de = valids[0]
INVALID = [
    de[:-1] + ("1" if de[-1] != "1" else "2"),  # broken checksum
    de[:-1],                                      # wrong (short) length
    "ZZ" + de[2:],                                # unknown country
    de[:4] + "AB" + de[6:],                       # letters where BBAN wants digits
    de[:2] + "AB" + de[4:],                       # letters in the check-digit slot
    "DE-9370400440532013000",                     # a stray punctuation char
    "",                                           # empty
]
for b in INVALID:
    lines.append("valid\t" + b)

with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")
