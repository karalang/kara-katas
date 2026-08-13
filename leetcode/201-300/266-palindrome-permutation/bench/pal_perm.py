"""Benchmark workload for LeetCode #266 — Palindrome Permutation (Python mirror).

Mirrors pal_perm.kara algorithm-for-algorithm. Correctness oracle only —
Python is not a measured lane (see BENCHMARKS.md).
"""


def main():
    n = 200000
    rounds = 4000
    span = 1000
    width = n - span

    data = []
    state = 266266
    for _ in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        data.append(97 + (state // 65536) % 26)

    counts = [0] * 256

    sink = 0
    for r in range(rounds):
        for c in range(256):
            counts[c] = 0

        start = (r * 7919) % span
        stop = start + width
        for i in range(start, stop):
            counts[data[i]] += 1

        odd = 0
        for k in range(256):
            if counts[k] % 2 == 1:
                odd += 1
        verdict = 1 if odd <= 1 else 0
        sink = (sink * 131 + odd * 7 + verdict) % 1000000007

    print(sink)


main()
