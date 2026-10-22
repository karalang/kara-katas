#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored reedsolo and prints expected.out.
mini_reedsolo.kara must reproduce this byte-for-byte on every backend.

  == enc <nsym> <message>
  <full codeword as hex>

  == dec <nsym> <hex codeword>
  ok msg=<hex> ecc=<hex> errs=<n> pos=<p,p,...>

`pos` lists the corrected byte positions in the codeword, ascending. `msg` is
the recovered message and `ecc` the corrected ECC block, both as hex.
"""
import sys

sys.path.insert(0, "vendor")
import reedsolo  # noqa: E402

reedsolo.init_tables(0x11D)


def main():
    out = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().splitlines():
        if not line:
            continue
        op, nsym_s, rest = line.split("\t", 2)
        nsym = int(nsym_s)
        out.append("== " + op + " " + nsym_s + " " + rest + "\n")
        if op == "enc":
            cw = reedsolo.rs_encode_msg(bytearray(rest.encode()), nsym)
            out.append(bytes(cw).hex() + "\n")
        else:
            cw = bytearray.fromhex(rest)
            msg, ecc, pos = reedsolo.rs_correct_msg(cw, nsym)
            pos_s = ",".join(str(p) for p in sorted(pos))
            out.append("ok msg=%s ecc=%s errs=%d pos=%s\n"
                       % (bytes(msg).hex(), bytes(ecc).hex(), len(pos), pos_s))
    sys.stdout.write("".join(out))


if __name__ == "__main__":
    main()
