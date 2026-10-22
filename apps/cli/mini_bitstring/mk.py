#!/usr/bin/env python3
"""Writes data/jobs.tsv: one bitstring operation per line, tab-separated.

op and arg. INIT is a bitstring auto-init string (0x.., 0b.., 0o.., uint:N=V,
int:N=V, or a comma-joined list). arg encodings:
  bin/hex/oct/uint/int/len/reverse/invert/tobytes/all/any/str   INIT
  slice     INIT|A|B          python slice INIT[A:B]
  index     INIT|I            python INIT[I] -> bool
  concat    INIT1|INIT2       (INIT1 + INIT2).bin
  eq        INIT1|INIT2       INIT1 == INIT2
  count     INIT|BIT          BIT in {0,1}
  find      INIT|SUB          INIT.find(SUB) -> tuple
  findall   INIT|SUB          list(INIT.findall(SUB)), overlapping
  unpack    INIT|FMT          INIT.unpack(FMT) -> list
"""
import os

JOBS = [
    # interpretations of the three radices and the integer tokens
    ("bin", "0x3f"),
    ("bin", "0o17"),
    ("bin", "uint:8=255"),
    ("bin", "int:8=-1"),
    ("bin", "int:5=-3"),
    ("bin", "uint:3=5"),
    ("hex", "0b1010"),
    ("hex", "uint:16=4096"),
    ("hex", "0xABCD"),
    ("oct", "0o17"),
    ("uint", "0xff"),
    ("int", "0xff"),
    ("int", "int:8=-1"),
    ("uint", "int:8=-1"),      # reinterpret the bits as unsigned
    ("len", "0x3f"),
    ("len", ""),
    ("str", "0xdead"),
    # token lists and whitespace
    ("bin", "0b1, 0x0f"),
    ("bin", " 0x0f , 0b1 "),
    ("bin", ""),
    # slicing and indexing (python semantics, negatives, a>b)
    ("slice", "0b11001010|2|6"),
    ("slice", "0b11001010|-4|8"),
    ("slice", "0b1100|3|1"),
    ("index", "0b10|0"),
    ("index", "0b10|1"),
    ("index", "0b10|-1"),
    ("index", "0b10|5"),       # out of range -> error
    # concat / equality
    ("concat", "0b10|0b11"),
    ("eq", "0x0f|0b00001111"),
    ("eq", "0x0f|0b0000111"),
    # counting, searching
    ("count", "0b10110|1"),
    ("count", "0b10110|0"),
    ("find", "0b00011000|0b11"),
    ("find", "0b0000|0b1"),    # no match -> ()
    ("find", "0b101|0b1"),
    ("findall", "0b1010101|0b1"),
    ("findall", "0b1111|0b11"),  # overlapping -> [0, 1, 2]
    # in-place transforms
    ("reverse", "0b1100"),
    ("invert", "0b1100"),
    # bytes and predicates
    ("tobytes", "0xabcd"),
    ("tobytes", "0b1"),        # padded on the right
    ("all", "0b111"),
    ("any", "0b000"),
    # unpack
    ("unpack", "0xabcd|uint:8, uint:8"),
    ("unpack", "0xff0f|int:8, uint:8"),
    ("unpack", "0xff|uint:16"),  # reads off the end -> error
    # the well-defined error paths
    ("oct", "0b1010"),         # not a multiple of 3 bits
    ("hex", "0b10101"),        # not a multiple of 4 bits
    ("int", ""),               # zero-length integer
    ("uint", "uint:4=16"),     # unsigned overflow
    ("int", "int:4=8"),        # signed overflow
    ("bin", "uint:8=-1"),      # negative unsigned
    ("bin", "0xzz"),           # bad hex symbol
    ("bin", "0b1012"),         # bad binary character
    ("bin", "0o18"),           # bad octal symbol
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w") as fh:
    for op, arg in JOBS:
        fh.write(op + "\t" + arg + "\n")
