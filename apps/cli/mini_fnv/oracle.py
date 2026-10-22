#!/usr/bin/env python3
r"""Replays data/jobs.tsv through the vendored `fnvhash` library and writes
expected.out. Each line is `variant<TAB>input`; the input's UTF-8 bytes are
hashed with the named 32-bit FNV variant and the result is printed as 8
lowercase hex digits. mini_fnv.kara reproduces this byte-for-byte on every
backend.

Only the 32-bit variants (fnv0_32, fnv1_32, fnv1a_32) are exercised; the 64-bit
variants need a 64-bit accumulator that overflows Kara's i64 and are out of
scope (see README)."""
import sys

sys.path.insert(0, "vendor")
import fnvhash  # noqa: E402

FN = {
    "fnv0_32": fnvhash.fnv0_32,
    "fnv1_32": fnvhash.fnv1_32,
    "fnv1a_32": fnvhash.fnv1a_32,
}


def to_hex8(n):
    return "%08x" % n


def main():
    out = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
        if line == "":
            continue
        variant, _, inp = line.partition("\t")
        h = FN[variant](inp.encode("utf-8"))
        out.append(variant + " " + to_hex8(h))
    sys.stdout.write("\n".join(out) + "\n")


main()
