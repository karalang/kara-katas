"""Benchmark harness for LeetCode #387 — Map (general-alphabet) approach.

Mirrors first_unique_char.kara algorithm-for-algorithm.
"""

N = 4000
ITERS = 2000


def first_uniq_char(bs):
    counts = {}
    for c in bs:
        counts[c] = counts.get(c, 0) + 1

    for j, c in enumerate(bs):
        if counts.get(c, 0) == 1:
            return j
    return -1


def unique_count(bs):
    counts = {}
    for c in bs:
        counts[c] = counts.get(c, 0) + 1
    uniq = 0
    for k in counts:
        if counts.get(k, 0) == 1:
            uniq += 1
    return uniq


def main():
    bs = [97 + (i % 25) for i in range(N)]
    bs[N - 1] = 122

    sink = 0
    for it in range(ITERS):
        p = (it * 7919) % N
        bs[p] = 97 + (it % 25)
        sink += first_uniq_char(bs)
        sink += unique_count(bs)
    print(sink)


if __name__ == "__main__":
    main()
