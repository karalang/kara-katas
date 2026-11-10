# LeetCode #2091: Removing Minimum and Maximum From Array -- Python mirror
# of the ★ arm's benchmark (deletions.kara): the same 20 shuffled arrays,
# each answered 20 times by the same walk over a `list`.

seed = 2091


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def minimum_deletions(nums):
    n = len(nums)
    lo = hi = 0
    for k in range(1, n):
        if nums[k] < nums[lo]:
            lo = k
        if nums[k] > nums[hi]:
            hi = k
    i, j = min(lo, hi), max(lo, hi)
    return min(j + 1, n - i, i + 1 + n - j)


def main():
    arrays = []
    for _ in range(20):
        v = [2 * i - 100000 for i in range(100000)]
        for i in range(99999, 0, -1):
            j = next_random() % (i + 1)
            v[i], v[j] = v[j], v[i]
        arrays.append(v)
    total = check = 0
    for rnd in range(20):
        for t in range(20):
            d = minimum_deletions(arrays[(t + rnd) % 20])
            total += d
            check = (check * 31 + d) % 1000000007
    print(f"400 answers: sum {total}, checksum {check}")


main()
