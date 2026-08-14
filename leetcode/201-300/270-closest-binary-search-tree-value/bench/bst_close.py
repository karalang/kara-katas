"""Benchmark workload for LeetCode #270 — Closest BST Value (Python mirror).

Mirrors bst_close.kara algorithm-for-algorithm. Correctness oracle only —
Python is not a measured lane (see BENCHMARKS.md).

Verified at a reduced `ROUNDS` rather than at full scale: the per-query answers
do not depend on the round count and the sink is a deterministic fold over
identical passes, so agreement at a small count is agreement at any.
"""

N = 30000
QUERIES = 100000
ROUNDS = 22


def main():
    val, left, right = [], [], []
    state = 270270

    for _ in range(N):
        state = (state * 1103515245 + 12345) & 2147483647
        hi = state // 65536
        state = (state * 1103515245 + 12345) & 2147483647
        v = (hi * 32768 + state // 65536) % 1000000
        if not val:
            val.append(v)
            left.append(-1)
            right.append(-1)
        else:
            cur = 0
            while True:
                if v < val[cur]:
                    if left[cur] < 0:
                        val.append(v)
                        left.append(-1)
                        right.append(-1)
                        left[cur] = len(val) - 1
                        break
                    cur = left[cur]
                else:
                    if right[cur] < 0:
                        val.append(v)
                        left.append(-1)
                        right.append(-1)
                        right[cur] = len(val) - 1
                        break
                    cur = right[cur]

    targets = []
    for _ in range(QUERIES):
        state = (state * 1103515245 + 12345) & 2147483647
        th = state // 65536
        state = (state * 1103515245 + 12345) & 2147483647
        whole = (th * 32768 + state // 65536) % 1100000 - 50000
        state = (state * 1103515245 + 12345) & 2147483647
        frac = ((state // 65536) % 1000) / 1000.0
        targets.append(whole + frac)

    sink = 0
    for _ in range(ROUNDS):
        for t in range(QUERIES):
            target = targets[t]
            best = val[0]
            best_diff = abs(val[0] - target)
            cur = 0
            while cur >= 0:
                v = val[cur]
                d = abs(v - target)
                if d < best_diff or (d == best_diff and v < best):
                    best = v
                    best_diff = d
                cur = right[cur] if v < target else left[cur]
            sink = (sink * 31 + best) % 1000000007

    print(sink)


main()
