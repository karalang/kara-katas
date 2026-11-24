# LeetCode #2426: Number of Pairs Satisfying Inequality -- the bench, the
# ★ arm: with `a[i] = nums1[i] - nums2[i]`, a merge sort counting the
# pairs `i < j` with `a[i] <= a[j] + diff`.

seed = 2426


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def count_pairs(a, lo, hi, diff):
    if hi - lo < 2:
        return 0
    mid = (lo + hi) // 2
    count = count_pairs(a, lo, mid, diff) + count_pairs(a, mid, hi, diff)
    p = lo
    for j in range(mid, hi):
        while p < mid and a[p] <= a[j] + diff:
            p += 1
        count += p - lo
    merged = []
    i, j = lo, mid
    while i < mid or j < hi:
        if j == hi or (i < mid and a[i] <= a[j]):
            merged.append(a[i])
            i += 1
        else:
            merged.append(a[j])
            j += 1
    a[lo:hi] = merged
    return count


def number_of_pairs(nums1, nums2, diff):
    a = [x - y for x, y in zip(nums1, nums2)]
    return count_pairs(a, 0, len(a), diff)


def main():
    firsts = []
    seconds = []
    for _ in range(10):
        nums1 = []
        nums2 = []
        for _ in range(100000):
            nums1.append(next_random() % 20001 - 10000)
            nums2.append(next_random() % 20001 - 10000)
        firsts.append(nums1)
        seconds.append(nums2)
    check = 0
    for p in range(4):
        for c in range(10):
            diff = 2000 * c - 10000 + p - 2
            check = (check * 31 + number_of_pairs(firsts[c], seconds[c], diff) + p) % 1000000007
    print(f"4 passes over 10 cases of 10^5 values: checksum {check}")


main()
