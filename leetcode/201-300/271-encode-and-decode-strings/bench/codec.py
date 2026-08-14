#!/usr/bin/env python3
"""Benchmark workload for LeetCode #271 — Encode and Decode Strings.

Algorithm-for-algorithm mirror of codec.kara. Kept as a CORRECTNESS ORACLE,
not a timed lane: Python is excluded from the measured comparison
(KARA_BENCH_INCLUDE_PY defaults to 0 in scripts/bench-lib.sh).
"""

COUNT = 50000
ROUNDS = 250


def main() -> None:
    # ---- build once: a flat corpus --------------------------------------
    src = bytearray()
    off = []
    length = []
    state = 271271
    for _ in range(COUNT):
        state = (state * 1103515245 + 12345) & 2147483647
        n = (state // 65536) % 25
        off.append(len(src))
        length.append(n)
        for _ in range(n):
            state = (state * 1103515245 + 12345) & 2147483647
            src.append(97 + (state // 65536) % 26)

    # ---- hoisted working buffers ----------------------------------------
    enc = bytearray(len(src) + COUNT * 3)
    dout = bytearray(len(src))

    # ---- punch -----------------------------------------------------------
    sink = 0
    for _ in range(ROUNDS):
        w = 0
        for k in range(COUNT):
            n = length[k]
            if n >= 10:
                enc[w] = 48 + n // 10
                w += 1
            enc[w] = 48 + n % 10
            w += 1
            enc[w] = 35  # '#'
            w += 1
            base = off[k]
            for p in range(n):
                enc[w + p] = src[base + p]
            w += n
        encoded_len = w

        rp = dp = items = check = 0
        while rp < encoded_len:
            n = 0
            while enc[rp] != 35:
                n = n * 10 + (enc[rp] - 48)
                rp += 1
            rp += 1
            for p in range(n):
                dout[dp + p] = enc[rp + p]
            check = (check * 31 + n) % 1000000007
            rp += n
            dp += n
            items += 1
        sink = (sink * 131 + check + items) % 1000000007

    print(sink)


main()
