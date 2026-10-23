#!/usr/bin/env python3
r"""Writes data/jobs.tsv: one lowercase hex string per line, the raw input
bytes for an LZW job. For each line the job LZW-compresses the bytes (lzw3's
.Z-style variable-width code stream) and then decompresses the result back,
printing:

    enc <hex of the compressed bytes>
    dec <hex of the decompressed bytes>   (equals the input)

No lzw3 import here (only literal inputs); oracle.py replays each line through
the vendored library to produce expected.out. Inputs include small-alphabet
runs long enough to force the code width to grow past 9 bits."""

INPUTS = [
    "61",                                   # 'a'
    "6162",                                 # 'ab'
    "61616161",                             # 'aaaa'
    "6162726163616461627261",               # 'abracadabra'
    "6d69737369737369707069",               # 'mississippi'
    "544f42454f524e4f54544f42454f52544f42454f524e4f54",  # TOBEOR...
    "68656c6c6f20776f726c64",               # 'hello world'
    "74686520717569636b2062726f776e20666f78",            # 'the quick brown fox'
    "000000",                               # three NULs
    "ffffffffffffffffffffffff",             # 12x 0xff
    "62616e616e612062616e616e612062616e616e61",          # 'banana banana banana'
    "414141414141414142",                   # 'AAAAAAAAB'
    # 'ab' x 60 -> dictionary grows, 9->10-bit width transition
    "6162" * 60,
    # 'abc' x 50
    "616263" * 50,
    # 5-symbol cycle 0..4 x 180 (900 bytes) -> past 512 and 1024 dict entries
    "0001020304" * 180,
    # 16-symbol ramp
    "000102030405060708090a0b0c0d0e0f" * 12,
    "0102030405",
    "48656c6c6f2c20576f726c6421",           # 'Hello, World!'
    "7a" * 100,                             # 'z' x 100
    "6d6973737320" * 20,                    # 'miss ' x 20
]


def main():
    import os
    os.makedirs("data", exist_ok=True)
    with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
        for s in INPUTS:
            fh.write(s + "\n")


main()
