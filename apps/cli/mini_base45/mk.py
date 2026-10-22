#!/usr/bin/env python3
"""Writes data/jobs.tsv: one `enc <hex>` or `dec <base45>` job per line
(tab-separated). `enc` asks for the Base45 (RFC 9285) encoding of the bytes
given as hex; `dec` asks for the bytes decoded from a Base45 string, emitted as
hex, or ERR when the string is not valid Base45. See oracle.py / README.md."""
import os

os.makedirs("data", exist_ok=True)

enc_hex = [
    "41", "4142", "48656c6c6f2121", "626173652d3435", "00", "ff", "0000",
    "ffff", "00ff", "ff00", "010203", "deadbeef",
    "00010203040506070809", "69657466", "666f6f626172", "7f8081", "aa55",
    "10", "54686520717569636b2062726f776e20666f78",
    "000102030405060708090a0b0c0d0e0f10111213",
]
dec_str = [
    "BB8", "%69 VD92EX0", "UJCLQE7W581", "U5", "00", "42",
    "0", "0000", "ZZZ", "::", "ab", "!!", ":0", "G6", "FGW", "QED8WEX0",
    " ", "000", "/:/", "GGW",
]

lines = []
for h in enc_hex:
    lines.append("enc\t" + h)
for s in dec_str:
    lines.append("dec\t" + s)

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
