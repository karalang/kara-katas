"""LeetCode 265 — differential harness (Python mirror / oracle).

Mirrors differential.kara draw-for-draw: the same LCG, the same order of seed
advances, the same ten families, so the printed digest must match byte for byte.
"""

MASK = 2147483647
INF = 1000000000000
DIGEST_MOD = 1000000007


def min_cost_quad(costs, k):
    n = len(costs)
    if n == 0:
        return 0
    prev = [costs[0][c] for c in range(k)]
    for i in range(1, n):
        cur = []
        for t in range(k):
            best = INF
            for j in range(k):
                if j != t and prev[j] < best:
                    best = prev[j]
            cur.append(costs[i][t] + best)
        prev = cur
    answer = min(prev)
    return -1 if answer >= INF else answer


def min_cost_minmin(costs, k):
    n = len(costs)
    if n == 0:
        return 0
    prev = [costs[0][c] for c in range(k)]
    for i in range(1, n):
        min1, idx1, min2 = INF, -1, INF
        for j in range(k):
            if prev[j] < min1:
                min2 = min1
                min1 = prev[j]
                idx1 = j
            elif prev[j] < min2:
                min2 = prev[j]
        prev = [costs[i][t] + (min2 if t == idx1 else min1) for t in range(k)]
    answer = min(prev)
    return -1 if answer >= INF else answer


def min_cost_prefix(costs, k):
    n = len(costs)
    if n == 0:
        return 0
    prev = [costs[0][c] for c in range(k)]
    for i in range(1, n):
        pre = []
        running = INF
        for j in range(k):
            if prev[j] < running:
                running = prev[j]
            pre.append(running)
        suf = [INF] * k
        running = INF
        for b in range(k - 1, -1, -1):
            if prev[b] < running:
                running = prev[b]
            suf[b] = running
        cur = []
        for t in range(k):
            best = INF
            if t > 0 and pre[t - 1] < best:
                best = pre[t - 1]
            if t + 1 < k and suf[t + 1] < best:
                best = suf[t + 1]
            cur.append(costs[i][t] + best)
        prev = cur
    answer = min(prev)
    return -1 if answer >= INF else answer


def main():
    cases = 4000
    seed = 265265

    mismatches = 0
    impossible = 0
    tied_rows = 0
    total_rows = 0
    digest = 0

    for _ in range(cases):
        seed = (seed * 1103515245 + 12345) & MASK
        family = (seed // 65536) % 10

        span = 3
        if family == 8:
            span = 10
        if family == 9:
            span = 1000

        seed = (seed * 1103515245 + 12345) & MASK
        n = (seed // 65536) % 13
        seed = (seed * 1103515245 + 12345) & MASK
        k = (seed // 65536) % 6 + 1
        if family == 6:
            k = 1
            if n < 2:
                n = 2
        if family == 7:
            k = 2

        costs = []
        for _i in range(n):
            row = []
            for _j in range(k):
                seed = (seed * 1103515245 + 12345) & MASK
                row.append((seed // 65536) % span + 1)
            costs.append(row)

        for row in costs:
            lo = min(row)
            if sum(1 for v in row if v == lo) > 1:
                tied_rows += 1
            total_rows += 1

        a = min_cost_quad(costs, k)
        b = min_cost_minmin(costs, k)
        d = min_cost_prefix(costs, k)

        if a != b or a != d:
            mismatches += 1
        if a == -1:
            impossible += 1
        digest = (digest * 131 + a + 3) % DIGEST_MOD

    print(f"cases {cases}")
    print(f"rows generated {total_rows}")
    print(f"rows with a tied minimum {tied_rows}")
    print(f"impossible (k=1, n>=2) {impossible}")
    print(f"digest {digest}")
    print(f"mismatches {mismatches}")


main()
