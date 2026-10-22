#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored `bitstruct` library and writes
expected.out. See mk.py for the op grammar. mini_bitstruct.kara reproduces
this byte-for-byte on every backend.

Only the integer / bool / text / raw / padding surface with bit-order (<>) and
byte-order (<>) markers is exercised, plus calcsize, byteswap, unpack_from and
allow_truncated, and the exact Error messages. The float ('f') format and the
dict / pack_into APIs are out of scope (see README)."""
import sys

sys.path.insert(0, "vendor")
import bitstruct  # noqa: E402
from bitstruct import (  # noqa: E402
    _parse_format, _Boolean, _UnsignedInteger, _SignedInteger,
    _Text, _Raw, _Padding, _Float, Error,
)


def tchar(info):
    if isinstance(info, _Boolean):
        return "b"
    if isinstance(info, _UnsignedInteger):
        return "u"
    if isinstance(info, _SignedInteger):
        return "s"
    if isinstance(info, _Text):
        return "t"
    if isinstance(info, _Raw):
        return "r"
    if isinstance(info, _Float):
        return "f"
    if isinstance(info, _Padding):
        return "p"
    return "?"


def typed_args(fmt, argstr):
    infos, _ = _parse_format(fmt, None, "utf-8", "strict")
    toks = argstr.split(" ") if argstr != "" else []
    args = []
    ti = 0
    for info in infos:
        c = tchar(info)
        if c == "p":
            continue
        tok = toks[ti]
        ti += 1
        if c in "us":
            args.append(int(tok))
        elif c == "b":
            args.append(int(tok))
        elif c == "t":
            args.append(tok)
        elif c == "r":
            args.append(bytes.fromhex(tok))
    return args


def value_types(fmt):
    infos, _ = _parse_format(fmt, None, "utf-8", "strict")
    return [tchar(i) for i in infos if not isinstance(i, _Padding)]


def render(fmt, values):
    toks = []
    for c, v in zip(value_types(fmt), values):
        if c == "b":
            toks.append("True" if v else "False")
        elif c == "t":
            toks.append(v)
        elif c == "r":
            toks.append(v.hex())
        else:
            toks.append(str(v))
    return " ".join(toks)


def run_line(fields):
    op = fields[0]
    if op == "pack":
        fmt, argstr = fields[1], fields[2]
        try:
            data = bitstruct.pack(fmt, *typed_args(fmt, argstr))
            return data.hex()
        except Error as e:
            return str(e)
    if op in ("unpack", "unpackt"):
        fmt, hexd = fields[1], fields[2]
        trunc = op == "unpackt"
        try:
            vals = bitstruct.unpack(fmt, bytes.fromhex(hexd),
                                    allow_truncated=trunc)
            return render(fmt, vals)
        except Error as e:
            return str(e)
    if op == "unpackfrom":
        fmt, off, hexd = fields[1], int(fields[2]), fields[3]
        try:
            vals = bitstruct.unpack_from(fmt, bytes.fromhex(hexd), off)
            return render(fmt, vals)
        except Error as e:
            return str(e)
    if op == "calcsize":
        fmt = fields[1]
        try:
            return str(bitstruct.calcsize(fmt))
        except Error as e:
            return str(e)
    if op == "byteswap":
        fmt, hexd = fields[1], fields[2]
        return bitstruct.byteswap(fmt, bytes.fromhex(hexd)).hex()
    raise SystemExit("unknown op %r" % op)


def main():
    out = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
        if line == "":
            continue
        out.append(run_line(line.split("\t")))
    sys.stdout.write("\n".join(out) + "\n")


main()
