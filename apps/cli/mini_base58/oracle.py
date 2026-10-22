#!/usr/bin/env python3
r"""Replays data/jobs.tsv through the vendored base58 library and writes
expected.out. Each input line is a lowercase hex string; the job base58-encodes
those bytes (Bitcoin alphabet) and decodes the result back, printing:

    enc <base58 string>
    dec <hex of the decoded bytes>

mini_base58.kara reproduces this byte-for-byte on every backend. Only the
plain b58encode / b58decode path is exercised (not the SHA256-based
b58encode_check / b58decode_check, nor alternate alphabets or autofix)."""
import sys

sys.path.insert(0, "vendor")
import base58  # noqa: E402


def row(data):
    enc = base58.b58encode(data).decode("ascii")
    dec = base58.b58decode(enc)
    return "enc " + enc + "\ndec " + dec.hex()


def main():
    out = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
        if line == "":
            continue
        data = bytes.fromhex(line)
        out.append(row(data))
    sys.stdout.write("\n".join(out) + "\n")


main()
