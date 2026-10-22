#!/usr/bin/env python3
"""Writes data/jobs.tsv: one hardware-address operation per line, tab-separated.

op and arg. Encodings inside arg:
  parse <string>        the raw address string to parse against all classes
  int   CLASS,DECIMAL   build CLASS from an integer value
  oui   CLASS,STRING    build CLASS from STRING, then take its .oui
  cmp   A|B             A and B are CLASS=STRING; report lt and eq
  sort  C=S,C=S,...     build each and print the sorted reprs
"""
import os

JOBS = [
    # parse: each distinct format length / separator picks a class
    ("parse", "01-23-45-67-89-AB"),       # EUI48 dashed
    ("parse", "01:23:45:67:89:ab"),       # EUI48 coloned
    ("parse", "0123.4567.89AB"),          # EUI48 dotted
    ("parse", "0123456789abcdef"),        # EUI64 bare (16 hex)
    ("parse", "01-23-45"),                # OUI dashed
    ("parse", "01:23:45"),                # OUI coloned
    ("parse", "abcdef"),                  # OUI bare (6 hex)
    ("parse", "01-23-45-67"),             # CDI32 dashed
    ("parse", "01-23-45-67-89"),          # CDI40 dashed (narrows vs EUI48 dotted)
    ("parse", "0123456789"),              # CDI40 bare (10 hex)
    ("parse", "01-23-45-67-89-ab-cd-ef"), # EUI64 dashed
    ("parse", ""),                        # error: empty string
    ("parse", "zz"),                      # error: no format of length 2
    ("parse", "0123"),                    # error: no format of length 4
    ("parse", "01-23-4Z"),                # error: bad hex digit in a real length
    # int construction + overflow / sign errors
    ("int", "OUI,0"),
    ("int", "OUI,16777215"),              # 2^24 - 1, max OUI
    ("int", "OUI,16777216"),              # error: too big for OUI
    ("int", "EUI48,1"),
    ("int", "EUI64,255"),
    ("int", "EUI60,1"),                   # dotted 15-nibble format
    ("int", "CDI40,4294967296"),          # 2^32 fits CDI40
    ("int", "CDI32,-1"),                  # error: negative
    # oui property of the StartsWithOUI subclasses
    ("oui", "EUI48,01-23-45-67-89-AB"),
    ("oui", "EUI64,0123456789abcdef"),
    ("oui", "CDI32,AA-BB-CC-DD"),
    # comparison: aligned-bits then size ordering
    ("cmp", "OUI=00-00-00|CDI32=00-00-00-00"),
    ("cmp", "OUI=00-00-01|CDI32=00-00-00-00"),
    ("cmp", "EUI48=01-23-45-67-89-AB|EUI48=01-23-45-67-89-AB"),
    ("cmp", "EUI48=01-23-45-67-89-AB|EUI48=01-23-45-67-89-AC"),
    ("cmp", "OUI=FF-FF-FF|EUI64=00-00-00-00-00-00-00-01"),
    # sort a mixed bag
    ("sort", "CDI32=00-00-00-00,OUI=00-00-01,OUI=00-00-00,EUI48=00-00-01-00-00-00"),
    ("sort", "EUI64=00-00-00-00-00-00-00-02,OUI=00-00-00,EUI48=00-00-00-00-00-01"),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w") as fh:
    for op, arg in JOBS:
        fh.write(op + "\t" + arg + "\n")
