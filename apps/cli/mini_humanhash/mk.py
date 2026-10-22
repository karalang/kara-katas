#!/usr/bin/env python3
"""Writes data/jobs.tsv for mini_humanhash: one `h <words> <hexdigest>` job per
line (tab-separated), asking for the human-readable rendering of a hex digest
with that many words. oracle.py replays each against the vendored humanhash
library; mini_humanhash.kara reproduces it. See README.md."""
import os
os.makedirs("data", exist_ok=True)

digests = [
    "60ad8d0d871b6095808297",                               # the library docstring digest (11 bytes)
    "0cd9a2ff",
    "deadbeefcafe0123456789ab",
    "ffffffffffffffffffffffffffffffff",
    "00000000000000000000000000000000",
    "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
    "a94a8fe5ccb19ba61c4c0873d391e987982fbbd3",             # sha1('test')
    "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",  # sha256('test')
    "0102",
    "abcdef",
]
counts = [2, 3, 4, 6, 8, 1]
# (words, hexdigest) that hit the cases where float floor(i/(L/t)) differs from
# integer (i*t)//L, so the f64 segmentation path is exercised:
div = []
for (blen, w) in [(18, 14), (27, 21), (42, 18), (44, 20)]:
    div.append((w, "".join("%02x" % ((k * 37 + 11) % 256) for k in range(blen))))
# passthrough: words >= byte length returns one word per input byte
pass_cases = [(4, "0102"), (10, "abcdef"), (20, "60ad8d0d871b6095808297")]

lines = []
for h in digests:
    for w in counts:
        lines.append("h\t%d\t%s" % (w, h))
for (w, h) in div:
    lines.append("h\t%d\t%s" % (w, h))
for (w, h) in pass_cases:
    lines.append("h\t%d\t%s" % (w, h))

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
