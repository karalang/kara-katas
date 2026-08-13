"""Benchmark workload for LeetCode #265 — Paint House II (Python mirror).

Mirrors paint_ii.kara algorithm-for-algorithm. Correctness oracle only —
Python is not a measured lane (see BENCHMARKS.md).
"""

INF = 1000000000000


def main():
    n = 4000
    k = 32
    rounds = 1300

    cost = []
    state = 265265
    for _ in range(n * k):
        state = (state * 1103515245 + 12345) & 2147483647
        cost.append((state // 65536) % 40 + 1)

    prev = [0] * k
    cur = [0] * k

    sink = 0
    for r in range(rounds):
        start = (r * 7919) % n

        for c in range(k):
            prev[c] = cost[start * k + c]

        for i in range(1, n):
            min1, idx1, min2 = INF, -1, INF
            for j in range(k):
                v = prev[j]
                if v < min1:
                    min2 = min1
                    min1 = v
                    idx1 = j
                elif v < min2:
                    min2 = v

            row = ((start + i) % n) * k
            for t in range(k):
                best = min2 if t == idx1 else min1
                cur[t] = cost[row + t] + best

            prev, cur = cur, prev

        answer = INF
        fold = 0
        for p in range(k):
            v = prev[p]
            if v < answer:
                answer = v
            fold = (fold * 31 + v) % 1000000007
        sink = (sink * 131 + answer + fold) % 1000000007

    print(sink)


main()
