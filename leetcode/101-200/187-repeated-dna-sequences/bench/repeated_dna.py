"""Benchmark workload for LeetCode #187 — Repeated DNA Sequences (Python; scale lane)."""

import sys


def scan(bases, stamp, cnt, n, pass_id):
    mask = 1048575  # 2^20 - 1
    hash_ = 0
    dups = 0
    for i in range(n):
        hash_ = ((hash_ << 2) | bases[i]) & mask
        if i >= 9:
            key = hash_
            if stamp[key] != pass_id:
                stamp[key] = pass_id
                cnt[key] = 0
            c = cnt[key] + 1
            cnt[key] = c
            if c == 2:
                dups += 1
    return dups


def main():
    n = 1000000
    passes = 30
    tablesize = 1048576  # 2^20

    bases = [0] * n
    state = 12345
    for b in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        bases[b] = (state >> 16) % 4

    stamp = [-1] * tablesize
    cnt = [0] * tablesize

    sink = 0
    for p in range(passes):
        state = (state * 1103515245 + 12345) & 2147483647
        idx = state % n
        bases[idx] = (state >> 16) % 4
        sink += scan(bases, stamp, cnt, n, p)
    print(sink)


main()
