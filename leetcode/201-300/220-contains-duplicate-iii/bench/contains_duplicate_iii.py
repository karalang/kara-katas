"""Benchmark workload for LeetCode #220 — Contains Duplicate III (Python; scale lane)."""


def bucket_of(x, w):
    # True floor division. Python's `//` already floors for either sign, which is
    # exactly what the compiled versions' truncating-`/` shift formula computes
    # (verified equal across signs) — so this stays byte-identical to them.
    return x // w


def near_value(m, b, x, t):
    v = m.get(b)
    if v is not None and abs(x - v) <= t:
        return True
    return False


def contains(nums, n, k, t):
    if k <= 0:
        return False
    w = t + 1
    buckets = {}
    for i in range(n):
        x = nums[i]
        b = bucket_of(x, w)
        if near_value(buckets, b, x, t):
            return True
        if near_value(buckets, b - 1, x, t):
            return True
        if near_value(buckets, b + 1, x, t):
            return True
        buckets[b] = x
        if i >= k:
            old = nums[i - k]
            buckets.pop(bucket_of(old, w), None)
    return False


def main():
    n = 20000
    pairs = 800
    valrange = 8000000
    half = 4000000

    nums = []
    state = 12345
    for _ in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        nums.append((state % valrange) - half)

    sink = 0
    for p in range(pairs):
        k = 32 + (p % 512)
        t = p % 3
        if contains(nums, n, k, t):
            sink += 1
    print(sink)


main()
