#!/usr/bin/env python3
"""Writes data/jobs.tsv: one job per line, tab-separated <op>\t<arg>.

The ULID string, hex, int and uuid arguments are minted here from fixed
(timestamp_ms, randomness) pairs through the vendored python-ulid, so every
argument is a genuine canonical form. <op> selects the operation the port and
oracle both run; the set covers the base32 codec, every from_*/to_* conversion,
the parse() dispatch, ordering and the error paths.
"""
import os
import sys

sys.path.insert(0, "vendor")
from ulid import ULID  # noqa: E402


def mk(ms, rand_hex):
    return str(ULID.from_bytes(ms.to_bytes(6, "big") + bytes.fromhex(rand_hex)))


# (timestamp_ms, 10-byte randomness) -> canonical 26-char ULID strings.
A = mk(1588257207560, "0102030405060708090a")   # sub-second ms
B = mk(1700000000000, "ffeeddccbbaa99887766")   # whole second
C = mk(0, "00000000000000000000")               # min
D = mk((1 << 48) - 1, "ffffffffffffffffffff")   # max timestamp
E = "01ARZ3NDEKTSV4RRFFQ69G5FAV"                 # ulid spec example
F = mk(1262304000000, "123456789abcdef0fedc")   # whole second, 2010-01-01

aint = str(int(ULID.from_str(A)))                # 39-digit int form
ahex = ULID.from_str(A).hex                       # 32 hex
auuid = str(ULID.from_str(A).to_uuid())           # dashed uuid
auuid7 = str(ULID.from_str(A).to_uuid7())         # non-compliant uuid7 (round-trips)
aint37 = "1234567890123456789012345678901234567"  # 37 digits -> parse() uses from_int

JOBS = [
    # --- base32 decode + accessors ---
    ("s2int", A), ("s2int", E), ("s2int", C), ("s2int", D),
    ("s2hex", A), ("s2hex", E), ("s2hex", D),
    ("ms", A), ("ms", B), ("ms", C), ("ms", D), ("ms", F),
    ("iso", B), ("iso", C), ("iso", F),
    # --- to_uuid family ---
    ("uuid", A), ("uuid", B), ("uuid", D),
    ("uuid4", A), ("uuid4", D),
    ("uuid7", A),
    ("uuid7c", A), ("uuid7c", C),
    # --- construct from other forms (round-trips) ---
    ("int2str", aint),
    ("hex2str", ahex),
    ("fromuuid", auuid),
    ("fromuuid7", auuid7),
    # --- parse() dispatch ---
    ("parse", A),          # 26 chars -> from_str
    ("parse", ahex),       # 32 chars -> from_hex
    ("parse", auuid),      # 36 chars -> from_uuid
    ("parse", aint37),     # 37-digit int -> from_int
    # --- ordering ---
    ("sort", C + "," + D + "," + A + "," + B),
    ("cmp", A + "," + B),
    ("cmp", D + "," + C),
    ("cmp", A + "," + A),
    # --- error paths ---
    ("s2int", "TOOSHORT"),                        # wrong length
    ("s2int", "01ARZ3NDEKTSV4RRFFQ69G5FAI"),      # 'I' not in alphabet
    ("s2int", "8ZZZZZZZZZZZZZZZZZZZZZZZZZ"),      # 128-bit overflow
    ("hex2str", "0102030405060708090a0b0c0d0e"),  # 14 bytes -> length error
    ("int2str", "9" * 39),                        # > 2**128 -> OverflowError
    ("parse", "SHORTVALUE"),                      # unparseable length
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w") as fh:
    for op, arg in JOBS:
        fh.write(op + "\t" + arg + "\n")
print("wrote data/jobs.tsv:", len(JOBS), "jobs")
