#!/usr/bin/env python3
r"""Writes data/jobs.tsv: one lowercase hex string per line, the raw input
bytes for a base58 job. For each line the job base58-encodes the bytes
(Bitcoin alphabet) and then decodes the result back, printing:

    enc <base58 string>
    dec <hex of the decoded bytes>   (equals the input)

No base58 import here (only literal inputs); oracle.py replays each line
through the vendored library to produce expected.out."""

INPUTS = [
    "",                       # skipped (empty line) but kept for intent
    "00",                     # one leading zero -> "1"
    "0000",                   # "11"
    "000000",                 # "111"
    "01",
    "ff",
    "ffff",
    "00ff",
    "0000ff00",
    "61",                     # 'a'
    "616263",                 # 'abc'
    "68656c6c6f20776f726c64",            # 'hello world'
    "48656c6c6f2c20426974636f696e21",    # 'Hello, Bitcoin!'
    "00112233445566778899aabbccddeeff",
    "0011111111111111111111111111111111111111deadbeef",  # p2pkh-shaped 25 bytes
    "deadbeef",
    "cafebabe",
    "0001020304050607",
    "fffefdfcfbfa",
    "7f80",
    "80",
    "0080",
    "123456789abcdef0",
    "000000000000000001",
    "ffffffffffffffffffffffffffffffff",
    "10",
    "0010",
    "6162636465666768696a6b6c6d6e6f70",  # 'abcdefghijklmnop'
    "00000000deadbeefcafe",
    "2a",
]


def main():
    import os
    os.makedirs("data", exist_ok=True)
    with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
        for s in INPUTS:
            fh.write(s + "\n")


main()
