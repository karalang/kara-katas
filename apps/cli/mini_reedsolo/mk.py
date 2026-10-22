#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_reedsolo: encode and decode jobs.

    enc \t <nsym> \t <ascii message>
    dec \t <nsym> \t <hex codeword, possibly corrupted>

An `enc` job Reed-Solomon-encodes the ASCII message with `nsym` ECC symbols
and prints the full codeword as hex. A `dec` job decodes a codeword (whose
bytes may have been flipped) back to the message, reporting the corrected
message, the corrected ECC, how many errors were found and where.

The `dec` inputs are built here by encoding a message with the vendored
reedsolo and then flipping a fixed, deterministic set of byte positions (no
RNG), from zero errors up to the correction bound `nsym // 2`. Every `dec`
job here is within the bound, so decoding always succeeds — reporting of
over-the-bound decode failures is out of scope (see README).
"""
import os
import sys

sys.path.insert(0, "vendor")
import reedsolo  # noqa: E402

reedsolo.init_tables(0x11D)

# (message, nsym, list of (position, xor-delta) corruptions) per decode job.
CASES = [
    ("Hello, Reed-Solomon!", 10, []),
    ("Hello, Reed-Solomon!", 10, [(0, 0x5A)]),
    ("Hello, Reed-Solomon!", 10, [(3, 0x01), (19, 0xFF)]),
    ("Hello, Reed-Solomon!", 10, [(0, 0x7F), (10, 0x11), (25, 0x80)]),
    ("Hello, Reed-Solomon!", 10, [(1, 0x22), (8, 0x44), (16, 0x88), (29, 0x10)]),
    ("Hello, Reed-Solomon!", 10, [(2, 0x13), (6, 0x24), (12, 0x35),
                                  (20, 0x46), (28, 0x57)]),
    ("QR codes use this.", 10, [(5, 0xAB), (9, 0xCD)]),
    ("short", 6, []),
    ("short", 6, [(1, 0x3C)]),
    ("short", 6, [(0, 0x0F), (7, 0xF0), (10, 0x99)]),
    ("0123456789abcdef", 8, [(4, 0x55), (15, 0xAA)]),
]
ENC = [
    ("Hello, Reed-Solomon!", 10),
    ("QR codes use this.", 10),
    ("short", 6),
    ("0123456789abcdef", 8),
    ("", 10),
    ("a", 4),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for msg, nsym in ENC:
        fh.write("enc\t%d\t%s\n" % (nsym, msg))
    for msg, nsym, corruptions in CASES:
        cw = bytearray(reedsolo.rs_encode_msg(bytearray(msg.encode()), nsym))
        for pos, delta in corruptions:
            cw[pos] ^= delta
        fh.write("dec\t%d\t%s\n" % (nsym, cw.hex()))
