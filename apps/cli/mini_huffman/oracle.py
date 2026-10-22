#!/usr/bin/env python3
r"""Replays data/jobs.tsv through the vendored dahuffman library and writes
expected.out. For each input line, a Huffman code is built from the line's
UTF-8 bytes; the job prints two lines:

    enc <hex of the encoded bytes>
    tab <sym>:<bits>:<value> ...   (symbols sorted ascending, EOF shown as E, first)

mini_huffman.kara reproduces this byte-for-byte on every backend. Only the
from_data / encode / get_code_table path is exercised (not save/load)."""
import sys

sys.path.insert(0, "vendor")
from dahuffman import HuffmanCodec  # noqa: E402


def row(data):
    codec = HuffmanCodec.from_data(data)
    table = codec.get_code_table()
    enc = codec.encode(data)
    hexs = "".join("%02x" % b for b in enc)
    items = []
    for s, (b, v) in table.items():
        key = s if isinstance(s, int) else -1  # _EOF -> -1
        items.append((key, b, v))
    items.sort()
    tab = " ".join(("E" if k == -1 else str(k)) + ":" + str(b) + ":" + str(v) for k, b, v in items)
    return "enc " + hexs + "\ntab " + tab


def main():
    out = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
        if line == "":
            continue
        out.append(row(line.encode("utf-8")))
    sys.stdout.write("\n".join(out) + "\n")


main()
