# LeetCode #2040: Kth Smallest Product of Two Sorted Arrays -- the ★ arm in
# Python, the same algorithm and workload as product.kara: binary search on
# the answer, the products at most `x` counted by a hand-written partition
# point.


def partition_point(v, pred):
    lo, hi = 0, len(v)
    while lo < hi:
        mid = (lo + hi) // 2
        if pred(v[mid]):
            lo = mid + 1
        else:
            hi = mid
    return lo


def count_at_most(nums1, nums2, x):
    count = 0
    for a in nums1:
        if a > 0:
            count += partition_point(nums2, lambda b: a * b <= x)
        elif a < 0:
            count += len(nums2) - partition_point(nums2, lambda b: a * b > x)
        elif x >= 0:
            count += len(nums2)
    return count


def kth_smallest_product(nums1, nums2, k):
    lo, hi = -10000000000, 10000000000
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if count_at_most(nums1, nums2, mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


seed = 2040


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def sorted_values(n, top):
    v = []
    for _ in range(n):
        hi = next_random()
        v.append((hi * 32768 + next_random()) % (2 * top + 1) - top)
    v.sort()
    return v


def main():
    n = 50000
    pairs = []
    for top in [100000, 3, 1000, 100000]:
        a = sorted_values(n, top)
        b = sorted_values(n, top)
        pairs.append((a, b))
    calls = total = check = 0
    for rnd in range(3):
        for r in range(4):
            k = (rnd * 4 + r + 1) * (n * n // 13) + 1
            answer = kth_smallest_product(pairs[r][0], pairs[r][1], k)
            calls += 1
            total += answer
            check = (check * 31 + answer % 1000000007) % 1000000007
    print(f"{calls} calls: sum {total}, checksum {check}")


main()
