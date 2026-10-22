#!/usr/bin/env python3
"""Appends the country table and jobs_text() to mini_iso3166.kara.

The 250 ISO 3166-1 records are packed one per Vec entry as
    name|alpha2|alpha3|numeric|apolitical|NAME_UP|APOLITICAL_UP
where NAME_UP / APOLITICAL_UP are Python's str.upper() of the name and
apolitical_name (the keys the library's name indexes use). Packing as one
string per row keeps the builder at 250 push statements instead of 1750, and
the `.kara` splits each row on '|' at startup. The uppercase keys are computed
here, so the port never has to uppercase non-ASCII stored data at run time.
"""
import sys

sys.path.insert(0, "vendor")
from iso3166 import _records  # noqa: E402

DELIM = "|"


def kstr(s):
    # no record contains a double quote or backslash (checked), so a plain
    # double-quoted Kara literal is exact.
    return '"' + s + '"'


lines = []
lines.append("")
lines.append("fn rows() -> Vec[String] {")
lines.append("    let mut v: Vec[String] = Vec.new();")
for r in _records:
    packed = DELIM.join(
        [r.name, r.alpha2, r.alpha3, r.numeric, r.apolitical_name,
         r.name.upper(), r.apolitical_name.upper()]
    )
    lines.append("    v.push(" + kstr(packed) + ");")
lines.append("    return v;")
lines.append("}")

# jobs_text(): the data/jobs.tsv contents as one embedded literal.
with open("data/jobs.tsv") as fh:
    jobs = fh.read()
lines.append("")
lines.append("fn jobs_text() -> String {")
lines.append("    return " + kstr(jobs.replace("\n", "\\n").replace("\t", "\\t")) + ";")
lines.append("}")

sys.stdout.write("\n".join(lines) + "\n")
