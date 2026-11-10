# LeetCode #2091: Removing Minimum and Maximum From Array -- Python mirror
# of the ★ arm (deletions.kara): one walk for the places of the least and
# the greatest, then the fewest of the three ways. Output is byte-identical.

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


def show(v):
    return "[" + ",".join(str(x) for x in v) + "]"


def shuffled(n, low, step):
    v = [low + i * step for i in range(n)]
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        v[i], v[j] = v[j], v[i]
    return v


def main():
    examples = [
        [2, 10, 7, 5, 4, 1, 8, 6],
        [0, -4, 19, 1, 8, -2, -3, 5],
        [101],
        [1, 2],
        [5, 1, 9, 3, 7],
        [3, 1, 2],
        [4, 9, 1, 6, 2, 8, 3, 7, 5],
    ]
    for nums in examples:
        print(f"{show(nums)} -> {minimum_deletions(nums)}")
    total = check = 0
    for _ in range(2000):
        n = next_random() % 100 + 1
        step = next_random() % 2000 + 1
        nums = shuffled(n, -100000, step)
        d = minimum_deletions(nums)
        total += d
        check = (check * 31 + d) % 1000000007
    print(f"2000 arrays: sum {total}, checksum {check}")
    big = shuffled(100000, -100000, 2)
    print(f"100000 values: {minimum_deletions(big)}")
    ends = list(range(100000))
    middle = list(range(100000))
    middle[0], middle[49999] = middle[49999], middle[0]
    middle[99999], middle[50000] = middle[50000], middle[99999]
    print(f"least first, greatest last: {minimum_deletions(ends)}; both in the middle: {minimum_deletions(middle)}")


main()
