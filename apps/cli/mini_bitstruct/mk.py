#!/usr/bin/env python3
r"""Writes data/jobs.tsv: one bitstruct operation per line, tab-separated.
Only literal inputs here (no bitstruct import); oracle.py replays each line
against the vendored library to produce expected.out.

Grammar (op in column 1):
  pack       <fmt>  <args>     args = space-joined tokens, one per non-pad field
                               (u/s decimal, b 0/1, t text, r lowercase-hex)
  unpack     <fmt>  <hexdata>
  unpackt    <fmt>  <hexdata>  (allow_truncated=True)
  unpackfrom <fmt>  <offset>  <hexdata>
  calcsize   <fmt>
  byteswap   <digits> <hexdata>

A field that raises bitstruct.Error (out-of-range int, bad format/char,
insufficient bits) prints the exact library message instead of a result."""

JOBS = [
    # --- pack: integers, bit widths, signedness ---
    ("pack", "u4u4", "3 7"),
    ("pack", "u1u3u4", "1 5 10"),
    ("pack", "s8", "-1"),
    ("pack", "s16", "-1000"),
    ("pack", "u8s8", "200 -50"),
    ("pack", "u7", "100"),
    ("pack", "u12u4", "2730 5"),
    # --- pack: booleans ---
    ("pack", "b1b1b1b1u4", "1 0 1 1 0"),
    # --- pack: padding (zeros / ones), ignored on unpack ---
    ("pack", "u5p3u8", "17 42"),
    ("pack", "u5P3u8", "17 42"),
    # --- pack: text and raw ---
    ("pack", "t16", "Hi"),
    ("pack", "t24", "abc"),
    ("pack", "r16", "dead"),
    ("pack", "r24", "cafe00"),
    # --- pack: bit order (<>) and byte order (<>) ---
    ("pack", "u4u4<", "3 7"),
    ("pack", "<u4u4", "3 7"),
    ("pack", "u12u4<", "2730 5"),
    ("pack", "u1<u2u3", "1 2 5"),
    ("pack", "u16<", "258"),
    ("pack", "u24<", "66051"),
    ("pack", "u8u8u8<", "1 2 3"),
    ("pack", "u1u3p7s16", "1 5 -1000"),
    ("pack", "u1u3p7s16<", "1 5 -1000"),
    ("pack", "<u1u3p7s16<", "1 5 -1000"),
    ("pack", "", ""),
    # --- unpack ---
    ("unpack", "u4u4", "37"),
    ("unpack", "s8", "ff"),
    ("unpack", "s16", "fc18"),
    ("unpack", "u8s8", "c8ce"),
    ("unpack", "b1b1b1b1u4", "b0"),
    ("unpack", "t16", "4869"),
    ("unpack", "r16", "dead"),
    ("unpack", "u4u4<", "37"),
    ("unpack", "u16<", "0201"),
    ("unpack", "u8u8u8<", "010203"),
    ("unpack", "u1u3p7s16", "d01f8300"),
    ("unpack", "u12u4<", "aaa5"),
    ("unpack", "u1<u2u3", "b4"),
    # --- unpackt: allow_truncated stops at the last whole field ---
    ("unpackt", "u8u8u8", "abcd"),
    ("unpackt", "u8u8", "ab"),
    # --- unpackfrom: read starting at a bit offset ---
    ("unpackfrom", "u4u4", "4", "0370"),
    # --- calcsize ---
    ("calcsize", "u1s3p4"),
    ("calcsize", "u12u4"),
    ("calcsize", "t24r16"),
    ("calcsize", ""),
    # --- byteswap: each digit a byte-group to reverse, in order ---
    ("byteswap", "24", "001122334455"),
    ("byteswap", "1234", "00112233445566778899"),
    ("byteswap", "8", "0011223344556677"),
    # --- errors: exact library messages ---
    ("pack", "u8", "256"),
    ("pack", "u8", "-1"),
    ("pack", "s4", "8"),
    ("pack", "s4", "-9"),
    ("calcsize", "q3"),
    ("calcsize", "u0"),
    ("calcsize", "u3x"),
    ("unpack", "u16", "00"),
]


def main():
    import os
    os.makedirs("data", exist_ok=True)
    with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
        for job in JOBS:
            fh.write("\t".join(job) + "\n")


main()
