"""Benchmark harness for LeetCode #347 — scalar-keyed Map approach.

Mirrors top_k_frequent.kara algorithm-for-algorithm, including the hand-written
insertion sort (rather than list.sort) so the measured work matches.
"""

N = 8000
D = 200
ITERS = 300
K = 10


def top_k_frequent(nums, k):
    counts = {}
    for v in nums:
        counts[v] = counts.get(v, 0) + 1

    vals = list(counts.keys())

    for a in range(1, len(vals)):
        cur = vals[a]
        cur_c = counts.get(cur, 0)
        b = a - 1
        while b >= 0:
            prev = vals[b]
            prev_c = counts.get(prev, 0)
            shift = False
            if prev_c < cur_c:
                shift = True
            if prev_c == cur_c and prev > cur:
                shift = True
            if not shift:
                break
            vals[b + 1] = prev
            b -= 1
        vals[b + 1] = cur

    limit = min(k, len(vals))
    return vals[:limit]


def main():
    bs = []
    for i in range(N):
        v = i % D
        if i % 5 == 0:
            v = i % 13
        bs.append(v)

    sink = 0
    for it in range(ITERS):
        p = (it * 7919) % N
        bs[p] = (it * 37) % D
        for v in top_k_frequent(bs, K):
            sink += v
    print(sink)


if __name__ == "__main__":
    main()
