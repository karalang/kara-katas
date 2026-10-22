#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored pyfiglet and prints expected.out.
mini_pyfiglet.kara must reproduce this byte-for-byte on every backend.

Each job is `render\t<text>`. The output is:

  == render <text>
  <the FIGlet rendering of <text> in the standard font, verbatim>

The rendering keeps its trailing spaces and ends in a newline, so the next
header follows directly.
"""
import sys

sys.path.insert(0, "vendor")
from pyfiglet import Figlet  # noqa: E402


def main():
    fig = Figlet(font="standard")
    out = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().splitlines():
        if not line:
            continue
        op, payload = line.split("\t", 1)
        out.append("== " + op + " " + payload + "\n")
        out.append(fig.renderText(payload))
    sys.stdout.write("".join(out))


if __name__ == "__main__":
    main()
