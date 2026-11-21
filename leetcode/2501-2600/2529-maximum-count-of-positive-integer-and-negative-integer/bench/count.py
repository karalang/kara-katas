# LeetCode #2529: Maximum Count of Positive Integer and Negative Integer
# -- benchmark mirror of the ★ arm (count.kara): 1000 sorted lists built
# once, then the passes, each asking every list from an offset the
# checksum picks.


def first_where(nums, above):
    lo = 0
    hi = len(nums)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] > above:
            hi = mid
        else:
            lo = mid + 1
    return lo


def maximum_count(nums):
    negatives = first_where(nums, -1)
    positives = len(nums) - first_where(nums, 0)
    return max(negatives, positives)


seed = 2529


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = []
    for _ in range(1000):
        shift = next_random() % 4001 - 2000
        nums = [min(max(next_random() % 4001 - 2000 + shift, -2000), 2000) for _ in range(2000)]
        nums.sort()
        lists.append(nums)
    passes = 3000
    check = 0
    for p in range(passes):
        start = check % 1000
        for i in range(1000):
            check = (check * 31 + maximum_count(lists[(start + i) % 1000]) + p) % 1000000007
    print(f"{passes} passes over 1000 lists of 2000 numbers: checksum {check}")


main()
