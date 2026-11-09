# LeetCode #2040: Kth Smallest Product of Two Sorted Arrays -- Python mirror
# of the ★ arm (product.kara): binary search on the answer, the products at
# most `x` counted for each `a` by a partition point over the sorted `nums2`.


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


# ---- test harness ---------------------------------------------------------

seed = 2040


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, answer):
    return (check * 31 + answer % 1000000007) % 1000000007


def sorted_values(n, top):
    v = []
    for _ in range(n):
        hi = next_random()
        v.append((hi * 32768 + next_random()) % (2 * top + 1) - top)
    v.sort()
    return v


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    examples = [
        ([2, 5], [3, 4], 2),
        ([-4, -2, 0, 3], [2, 4], 6),
        ([-2, -1, 0, 1, 2], [-3, -1, 2, 4, 5], 3),
        ([7], [-6], 1),
        ([-100000, 100000], [-100000, 100000], 4),
        ([-100000, 100000], [-100000, 100000], 1),
        ([0, 0, 0], [-1, 1], 4),
        ([-5, -3, -1], [-4, -2], 5),
    ]
    for a, b, k in examples:
        print(f"{show(a)} {show(b)} {k} -> {kth_smallest_product(a, b, k)}")
    total = 0
    check = 0
    for _ in range(2000):
        top = next_random() % 20 + 1
        a = sorted_values(next_random() % 8 + 1, top)
        b = sorted_values(next_random() % 8 + 1, top)
        k = next_random() % (len(a) * len(b)) + 1
        answer = kth_smallest_product(a, b, k)
        total += answer
        check = mix(check, answer)
    print(f"2000 problems of up to 8 values a side: sum {total}, checksum {check}")
    total = 0
    check = 0
    for r in range(4):
        top = [100000, 3, 1000, 100000][r]
        n = [50000, 10000, 5000, 1000][r]
        a = sorted_values(n, top)
        b = sorted_values(n, top)
        hi = next_random()
        k = (hi * 32768 + next_random()) * 76293 % (n * n) + 1
        answer = kth_smallest_product(a, b, k)
        total += answer
        check = mix(check, answer)
    print(f"4 large problems: sum {total}, checksum {check}")


main()
