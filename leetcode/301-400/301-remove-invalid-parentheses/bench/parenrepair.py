"""Benchmark mirror of parenrepair.kara - LeetCode #301, unique-by-construction
repair. Same recursion, same depth-indexed scratch buffer, same sink.

The scratch buffer is a flat bytearray indexed by depth * SLOT, matching the
other four mirrors rather than reaching for Python's slicing - the point is to
time the same algorithm, not to find the fastest way to say it in Python.
"""

import sys

NCASES = 2000
SLEN = 24
PASSES = 64
SLOT = 32
MAXDEPTH = 32
MOD = 1000000007

sys.setrecursionlimit(10000)

scratch = bytearray(MAXDEPTH * SLOT)
state = [0, 0]  # results, checksum


def repair(depth: int, length: int, last_i: int, last_j: int, open_c: int, close_c: int) -> None:
    base = depth * SLOT
    child = base + SLOT

    count = 0
    i = last_i
    while i < length:
        c = scratch[base + i]
        if c == open_c:
            count += 1
        elif c == close_c:
            count -= 1
        if count < 0:
            j = last_j
            while j <= i:
                if scratch[base + j] == close_c and (j == last_j or scratch[base + j - 1] != close_c):
                    w = 0
                    for k in range(length):
                        if k != j:
                            scratch[child + w] = scratch[base + k]
                            w += 1
                    repair(depth + 1, length - 1, i, j, open_c, close_c)
                j += 1
            return
        i += 1

    for r in range(length):
        scratch[child + r] = scratch[base + length - 1 - r]

    if open_c == 0x28:  # '('
        repair(depth + 1, length, 0, 0, 0x29, 0x28)
    else:
        h = 0
        for t in range(length):
            h = (h * 31 + scratch[child + t]) % MOD
        state[0] += 1
        state[1] = (state[1] + h) % MOD


def main() -> None:
    corpus = bytearray(NCASES * SLEN)
    s = 12345
    for n in range(NCASES * SLEN):
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        r = (s // 65536) % 3
        corpus[n] = 0x28 if r == 0 else (0x29 if r == 1 else 0x61)

    for _ in range(PASSES):
        for ci in range(NCASES):
            src = ci * SLEN
            scratch[0:SLEN] = corpus[src:src + SLEN]
            repair(0, SLEN, 0, 0, 0x28, 0x29)

    print(f"results {state[0]}")
    print(f"checksum {state[1]}")


if __name__ == "__main__":
    main()
