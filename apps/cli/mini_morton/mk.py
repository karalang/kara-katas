#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_morton: Morton / Z-order interleave jobs.

Lines are one of:

    il2 \t <x> \t <y>          2-D interleave (16-bit coords)
    dl2 \t <n>                 2-D de-interleave
    il3 \t <x> \t <y> \t <z>   3-D interleave (10-bit coords)
    dl3 \t <n>                 3-D de-interleave

The coordinate grids and boundary values walk the bit-spreading masks the
library branches on (byte / nibble / crumb / bit boundaries) and include values
above the 16-bit (il2) and 10-bit (il3) coordinate range, to exercise the
leading `& 0xffff` / `& 0x3ff` masking. The `dl*` inputs are the codes the
vendored interleave produced, so each de-interleave round-trips; a few arbitrary
codes are added as well.
"""
import os
import sys

sys.path.insert(0, "vendor/pymorton3/..")
import pymorton3 as m  # noqa: E402

il2_pairs = []
# dense low grid
for x in range(0, 9):
    for y in range(0, 9):
        il2_pairs.append((x, y))
# boundary / power-of-two coordinates against a few fixed partners
coords2 = [0, 1, 2, 3, 4, 7, 8, 15, 16, 31, 255, 256, 257, 1023, 1024, 4095,
           32767, 32768, 65535]
for x in coords2:
    for y in [0, 1, 255, 65535]:
        il2_pairs.append((x, y))
# above 16 bits: the library masks to the low 16 (0x12345 -> 0x2345)
for x in [0x10000, 0x1FFFF, 0x12345]:
    il2_pairs.append((x, 0xABCD))

il3_triples = []
for x in range(0, 6):
    for y in range(0, 6):
        for z in range(0, 6):
            il3_triples.append((x, y, z))
coords3 = [0, 1, 2, 7, 8, 255, 256, 511, 512, 1023]
for x in coords3:
    il3_triples.append((x, 500, 1000))
# above 10 bits: masked to the low 10 (0x400 -> 0, 0xFFF -> 0x3FF)
for t in [(0x400, 0x3FF, 1), (0xFFF, 0, 1023), (0x7FF, 0x801, 2)]:
    il3_triples.append(t)

dl2_codes = [m.interleave2(x, y) for (x, y) in il2_pairs]
dl2_codes += [0, 1, 2, 3, 42, 147, 1000000, 0xFFFFFFFF, 0xAAAAAAAA, 0x55555555]
dl3_codes = [m.interleave3(x, y, z) for (x, y, z) in il3_triples]
dl3_codes += [0, 1, 7, 53, 1000000, 0x09249249, 0x3FFFFFFF]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for (x, y) in il2_pairs:
        fh.write("il2\t%d\t%d\n" % (x, y))
    for (x, y, z) in il3_triples:
        fh.write("il3\t%d\t%d\t%d\n" % (x, y, z))
    for n in dl2_codes:
        fh.write("dl2\t%d\n" % n)
    for n in dl3_codes:
        fh.write("dl3\t%d\n" % n)
