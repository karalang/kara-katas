# LeetCode #870: Advantage Shuffle -- greedy from the largest; a mirror of
# advantage_shuffle.kara, its output byte-identical.


def advantage_count(nums1, nums2):
    n = len(nums1)
    srt = sorted(nums1)
    order = sorted(range(n), key=lambda i: -nums2[i])
    result = [0] * n
    lo, hi = 0, n - 1
    for i in order:
        if srt[hi] > nums2[i]:
            result[i] = srt[hi]
            hi -= 1
        else:
            result[i] = srt[lo]
            lo += 1
    return result


# ---- test harness ----------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_below(limit):
    hi = next_random()
    lo = next_random()
    return (hi * 32768 + lo) % limit


def random_vec(n, limit):
    return [random_below(limit) for _ in range(n)]


def advantage(result, nums2):
    return sum(1 for i in range(len(nums2)) if result[i] > nums2[i])


def score(nums1, nums2):
    result = advantage_count(nums1, nums2)
    if len(result) == len(nums1) and sorted(result) == sorted(nums1):
        return advantage(result, nums2)
    return -1


def fmt(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def show(nums1, nums2):
    s = score(nums1, nums2)
    if s < 0:
        print(f"nums1 = {fmt(nums1)}, nums2 = {fmt(nums2)} -> not a permutation of nums1")
    else:
        print(f"nums1 = {fmt(nums1)}, nums2 = {fmt(nums2)} -> advantage {s}")


def main():
    global seed
    show([2, 7, 11, 15], [1, 10, 4, 11])
    show([12, 24, 8, 32], [13, 25, 32, 11])
    show([5], [5])
    show([6], [5])
    show([0], [1000000000])
    show([3, 3, 3, 3], [3, 3, 3, 3])
    show([4, 4, 4, 4], [3, 3, 3, 3])
    show([1, 2, 3, 4], [4, 3, 2, 1])
    show([1, 2, 3, 4], [1, 2, 3, 4])
    show([2, 0, 4, 1, 2], [1, 3, 0, 0, 2])
    show([9, 1, 2, 4, 5], [6, 2, 9, 1, 4])
    show([1000000000, 0, 999999999], [999999999, 1000000000, 0])
    seed = 870
    total = 0
    bad = 0
    for t in range(3000):
        n = t % 8 + 1
        nums1 = random_vec(n, 10)
        nums2 = random_vec(n, 10)
        s = score(nums1, nums2)
        if s < 0:
            bad += 1
        else:
            total += s
    print(f"3000 arrays of 1 to 8 values below 10: advantages sum to {total}, {bad} not permutations")
    total = 0
    bad = 0
    check = 0
    for t in range(60):
        n = random_below(1000) + 1
        limit = 1000000001 if t % 2 == 0 else n
        nums1 = random_vec(n, limit)
        nums2 = random_vec(n, limit)
        s = score(nums1, nums2)
        if s < 0:
            bad += 1
        else:
            total += s
            check = (check * 1009 + s) % 1000000007
    print(f"60 arrays of up to 1000 values: advantages sum to {total}, checksum {check}, {bad} not permutations")
    for limit in [1000000001, 100]:
        nums1 = random_vec(100000, limit)
        nums2 = random_vec(100000, limit)
        s = score(nums1, nums2)
        print(f"100000 values below {limit}: advantage {s}")


main()
