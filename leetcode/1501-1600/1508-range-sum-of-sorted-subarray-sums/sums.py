# LeetCode #1508: Range Sum of Sorted Subarray Sums -- the Python mirror of
# the ★ arm: the sum of the k smallest subarray sums by a binary search
# and a two-pointer sweep, the answer the difference of two of them.

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


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most):
    check = 0
    for _ in range(count):
        n = next_random() % most + 1
        nums = [next_random() % 100 + 1 for _ in range(n)]
        total = n * (n + 1) // 2
        a = next_random() % total + 1
        b = next_random() % total + 1
        check = mix(check, range_sum(nums, n, min(a, b), max(a, b)))
    return check


print(f"[1, 2, 3, 4], 1 to 5 -> {range_sum([1, 2, 3, 4], 4, 1, 5)}")
print(f"[1, 2, 3, 4], 3 to 4 -> {range_sum([1, 2, 3, 4], 4, 3, 4)}")
print(f"[1, 2, 3, 4], 1 to 10 -> {range_sum([1, 2, 3, 4], 4, 1, 10)}")
print(f"[7], 1 to 1 -> {range_sum([7], 1, 1, 1)}")
print(f"[5, 5, 5], 2 to 5 -> {range_sum([5, 5, 5], 3, 2, 5)}")
big = [100 - i % 7 for i in range(1000)]
print(f"1000 numbers, 1 to 500500 -> {range_sum(big, 1000, 1, 500500)}")
print(f"3000 arrays of 1 to 8 numbers: checksum {batch(3000, 8)}")
print(f"300 arrays of 1 to 100 numbers: checksum {batch(300, 100)}")
print(f"3 arrays of 1 to 1000 numbers: checksum {batch(3, 1000)}")
