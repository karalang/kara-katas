# LeetCode #1283 bench, Python: the same binary search, workload and
# checksum as smallest_divisor.kara.


def total(nums, d):
    s = 0
    for x in nums:
        s += (x + d - 1) // d
    return s


def smallest_divisor(nums, threshold):
    lo, hi = 1, max(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if total(nums, mid) <= threshold:
            hi = mid
        else:
            lo = mid + 1
    return lo


def main():
    seed = 1283
    nums = []
    for _ in range(50000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        nums.append(1 + seed % 1000000)
    check = 0
    for r in range(150):
        threshold = 50000 + (check + r * 7919) % 950001
        check = (check * 131 + smallest_divisor(nums, threshold)) % 1000000007
    print(f"150 rounds over 5 * 10^4 numbers: checksum {check}")


main()
