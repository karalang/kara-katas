#!/usr/bin/env python3
r"""Replays data/jobs.tsv through the vendored lzw3 library and writes
expected.out. Each input line is a lowercase hex string; the job LZW-compresses
those bytes and decompresses the result back, printing:

    enc <hex of the compressed bytes>
    dec <hex of the decompressed bytes>

mini_lzw.kara reproduces this byte-for-byte on every backend.

lzw3's compressor/decompressor are file-based, so each job round-trips through
temp files. lzw3 0.4 predates Python 3.10's move of collections.Callable to
collections.abc; we restore that one stdlib alias before importing it (a name
relocation, not a behaviour change) and leave vendor/ untouched."""
import collections
import collections.abc
import os
import sys
import tempfile

if not hasattr(collections, "Callable"):  # Python 3.10 moved it to collections.abc
    collections.Callable = collections.abc.Callable

sys.path.insert(0, "vendor")
from lzw3.commons.log import Logger  # noqa: E402
from lzw3.compressor import LZWCompressor  # noqa: E402
from lzw3.decompressor import LZWDecompressor  # noqa: E402

Logger.enable_logger(False)  # silence the compressor's diagnostic prints to stdout


def row(data, tmp):
    inp = os.path.join(tmp, "in.bin")
    comp = os.path.join(tmp, "c.Z")
    back = os.path.join(tmp, "back.bin")
    with open(inp, "wb") as f:
        f.write(data)
    LZWCompressor().compress(inp, comp)
    LZWDecompressor().decompress(comp, back)
    with open(comp, "rb") as f:
        cbytes = f.read()
    with open(back, "rb") as f:
        bbytes = f.read()
    assert bbytes == data, "library round-trip mismatch"
    return "enc " + cbytes.hex() + "\ndec " + bbytes.hex()


def main():
    out = []
    with tempfile.TemporaryDirectory() as tmp:
        for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
            if line == "":
                continue
            out.append(row(bytes.fromhex(line), tmp))
    sys.stdout.write("\n".join(out) + "\n")


main()
