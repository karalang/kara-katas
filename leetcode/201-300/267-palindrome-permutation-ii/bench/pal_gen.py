"""Benchmark workload for LeetCode #267 — Palindrome Permutation II (Python mirror).

Mirrors pal_gen.kara algorithm-for-algorithm, including the hoisted output
buffer. Correctness oracle only — Python is not a measured lane.
"""


def build(counts, half, half_len, middle, buf, acc):
    if len(half) == half_len:
        n = 0
        for i in range(half_len):
            buf[n] = half[i]
            n += 1
        if middle >= 0:
            buf[n] = middle
            n += 1
        for j in range(half_len - 1, -1, -1):
            buf[n] = half[j]
            n += 1
        a = acc[0]
        for k in range(n):
            a = (a * 31 + buf[k]) % 1000000007
        acc[0] = a
        return
    for c in range(128):
        if counts[c] > 0:
            counts[c] -= 1
            half.append(c)
            build(counts, half, half_len, middle, buf, acc)
            half.pop()
            counts[c] += 1


def main():
    pairs = 8
    rounds = 44
    buf = [0] * 64

    sink = 0
    for r in range(rounds):
        counts = [0] * 128
        for p in range(pairs):
            counts[97 + p] = 2
        counts[97 + r % pairs] += 1

        middle = -1
        half_len = 0
        for c in range(128):
            if counts[c] % 2 == 1:
                middle = c
            counts[c] //= 2
            half_len += counts[c]

        acc = [0]
        build(counts, [], half_len, middle, buf, acc)
        sink = (sink * 131 + acc[0]) % 1000000007

    print(sink)


main()
