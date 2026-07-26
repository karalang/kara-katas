"""Benchmark harness for LeetCode #239 — Sliding Window Maximum.

Mirrors sliding_window_max.kara algorithm-for-algorithm, including the
list-plus-head-cursor deque rather than collections.deque, so the measured work
matches. Committed as the correctness oracle; not a measured lane.
"""

NP = 8
N = 50000
CAPV = 100000
K = 64
ITERS = 300


def max_sliding_window(nums, k):
    n = len(nums)
    out = []
    dq = []
    head = 0

    for i in range(n):
        while len(dq) > head:
            back = dq[-1]
            if nums[back] <= nums[i]:
                dq.pop()
            else:
                break
        dq.append(i)

        if dq[head] <= i - k:
            head += 1

        if i >= k - 1:
            out.append(nums[dq[head]])
    return out


def lcg(seed, n, cap):
    out = []
    x = seed
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append(x % cap)
    return out


def main():
    arrays = [lcg(j + 1, N, CAPV) for j in range(NP)]

    sink = 0
    for it in range(ITERS):
        idx = (it * 3) % NP
        res = max_sliding_window(arrays[idx], K)
        for v, val in enumerate(res):
            sink = (sink + (v + 1) * val) % 1000000007
    print(sink)


if __name__ == "__main__":
    main()
