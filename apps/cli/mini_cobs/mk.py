#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_cobs: COBS / COBS-R encode and decode jobs.

    <op> \t <hex>

`op` is cobs_enc / cobs_dec / cobsr_enc / cobsr_dec. For an `enc` job the hex is
the raw payload to encode; for a `dec` job it is an encoded frame to decode.

The decode inputs are built here: the valid ones by encoding a payload with the
vendored cobs (so decode round-trips it), plus a handful of deliberately broken
frames (an embedded zero byte, a length code running past the end) to exercise
the DecodeError paths. The payloads walk the length-code boundaries COBS and
COBS/R branch on (runs of 0xFD / 0xFE non-zero bytes), embedded and trailing
zeros, and the empty string.
"""
import os
import sys

sys.path.insert(0, "vendor")
from cobs import cobs, cobsr  # noqa: E402

PAYLOADS = [
    b"",
    b"\x00",
    b"\x01",
    b"\x2a",
    b"hello",
    b"he\x00llo",
    b"\x00\x00\x00",
    b"abc\x00",
    b"\x00abc",
    b"\xff\xfe\x00\x01",
    bytes(range(1, 16)),
    bytes(range(1, 255)),       # 254 non-zero bytes
    bytes(range(1, 256)),       # 255 non-zero bytes (0xFD / 0xFE boundaries)
    b"\x11" * 253,
    b"\x11" * 254,
    b"\x11" * 255,
    bytes([0] * 6),
    bytes(range(250, 256)),     # trailing high byte, for COBS/R reduction
]
# Deliberately malformed frames, to exercise the DecodeError paths.
BAD = [
    bytes([0x01, 0x00, 0x02]),  # zero byte inside the frame
    bytes([0x03, 0x11]),        # length code runs past the end
    bytes([0xFF]),              # length 0xFF but no following data
    bytes([0x05, 0x11, 0x22]),  # length code runs past the end
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for p in PAYLOADS:
        fh.write("cobs_enc\t%s\n" % p.hex())
    for p in PAYLOADS:
        fh.write("cobsr_enc\t%s\n" % p.hex())
    for p in PAYLOADS:
        fh.write("cobs_dec\t%s\n" % cobs.encode(p).hex())
    for p in PAYLOADS:
        fh.write("cobsr_dec\t%s\n" % cobsr.encode(p).hex())
    for b in BAD:
        fh.write("cobs_dec\t%s\n" % b.hex())
    for b in BAD:
        fh.write("cobsr_dec\t%s\n" % b.hex())
