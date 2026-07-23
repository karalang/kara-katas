"""LeetCode 220 — Contains Duplicate III (Python mirror / oracle).

Bucketing sliding window: buckets of width t+1 (same bucket => within t), check
own + adjacent buckets, evict on window exit. Floor-division bucket ids handle
negatives. Mirrors the Kara version.
"""


def bucket_of(x, w):
    # Match Kara's shift-based floor division (Kara `/` truncates toward zero).
    if x >= 0:
        return x // w
    return (x + 1) // w - 1


def near_value(m, b, x, t):
    if b in m and abs(x - m[b]) <= t:
        return True
    return False


def contains_nearby_almost_duplicate(nums, k, t):
    if k <= 0:
        return False
    w = t + 1
    buckets = {}
    for i, x in enumerate(nums):
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


def report(nums, k, t):
    print("true" if contains_nearby_almost_duplicate(nums, k, t) else "false")


def main():
    report([1, 2, 3, 1], 3, 0)
    report([1, 5, 9, 1, 5, 9], 2, 3)
    report([1, 2, 3, 1], 3, 0)
    report([8, 2, 4], 2, 1)
    report([-1, -1], 1, 0)
    report([1, 2], 0, 3)
    report([7, 1, 3, 9, 5], 3, 2)
    report([-3, 3, 0, 10], 3, 3)


main()
