# LeetCode #1508: Range Sum of Sorted Subarray Sums -- the bench: 40 arrays
# of 1000 numbers built once, then 25 ranges of places asked of each, by
# the ★ arm.

MOD = 1000000007


def at_most(prefix, twice, bound):
    n = len(prefix) - 1
    count = total = i = 0
    for j in range(1, n + 1):
        while prefix[j] - prefix[i] > bound:
            i += 1
        count += j - i
        total += (j - i) * prefix[j] - (twice[j] - twice[i])
    return count, total


def smallest(prefix, twice, k):
    if k == 0:
        return 0
    lo, hi = 1, prefix[-1]
    while lo < hi:
        mid = (lo + hi) // 2
        if at_most(prefix, twice, mid)[0] >= k:
            hi = mid
        else:
            lo = mid + 1
    count, total = at_most(prefix, twice, lo)
    return total - (count - k) * lo


def range_sum(nums, n, left, right):
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]
    twice = [0] * (n + 1)
    for i in range(n):
        twice[i + 1] = twice[i] + prefix[i]
    return (smallest(prefix, twice, right) - smallest(prefix, twice, left - 1)) % MOD


seed = 1508


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


arrays = [[next_random() % 100 + 1 for _ in range(1000)] for _ in range(40)]
total = 1000 * 1001 // 2
check = 0
for _ in range(25):
    for nums in arrays:
        a = next_random() % total + 1
        b = next_random() % total + 1
        check = (check * 31 + range_sum(nums, 1000, min(a, b), max(a, b)) + 1) % 1000000007
print(f"1000 ranges over 40 arrays of 1000 numbers: checksum {check}")
