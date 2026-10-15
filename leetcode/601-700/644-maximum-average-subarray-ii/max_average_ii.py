# LeetCode #644: Maximum Average Subarray II -- Python mirror of the ★
# arm.
#
# Binary search on the average: a subarray of `k` or more values averages
# at least `m` when its sum less `m` times its length is 0 or more, and
# one pass keeping the best start answers that for every end. 100
# halvings, then the exact average of the subarray the last successful
# check found.


def reaches(prefix, k, m):
    lowest = 0
    for end in range(k, len(prefix)):
        c = end - k
        if float(prefix[c] - prefix[lowest]) < m * float(c - lowest):
            lowest = c
        if float(prefix[end] - prefix[lowest]) >= m * float(end - lowest):
            return (lowest, end)
    return (-1, -1)


def find_max_average(nums, k):
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)
    lo = float(nums[0])
    hi = float(nums[0])
    for x in nums:
        lo = min(lo, float(x))
        hi = max(hi, float(x))
    best = (0, len(nums))
    for _ in range(100):
        mid = (lo + hi) / 2.0
        start, end = reaches(prefix, k, mid)
        if start == -1:
            hi = mid
        else:
            lo = mid
            best = (start, end)
    start, end = best
    return float(prefix[end] - prefix[start]) / float(end - start)


def next_random(rng):
    rng[0] = (rng[0] * 1103515245 + 12345) % 2147483648
    return rng[0] // 65536


def show(nums, k):
    text = ",".join(str(x) for x in nums)
    print(f"[{text}], k = {k} -> {find_max_average(nums, k):.5f}")


def random_values(n, most, rng):
    return [next_random(rng) % (2 * most + 1) - most for _ in range(n)]


def main():
    show([1, 12, -5, -6, 50, 3], 4)
    show([5], 1)
    show([1, 9, 9, 1, 9, 9, 1], 2)
    show([3, -1, 4, -1, 5], 5)
    show([7, 7, 7, 7], 3)
    show([-5, -2, -9, -1, -4], 2)
    show([0, 5, 5, 5, 0, 0, 5, 5, 5, 0], 4)
    show([1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1], 7)
    show([-10000, 10000, 10000, -10000, 10000], 2)
    rng = [644]
    total = 0.0
    for _ in range(300):
        n = 1 + next_random(rng) % 30
        k = 1 + next_random(rng) % n
        nums = random_values(n, 20, rng)
        total += find_max_average(nums, k)
    print(f"300 random arrays: sum of answers {total:.5f}")
    nums = random_values(10000, 10000, rng)
    for k in [1, 100, 2500, 10000]:
        print(f"10000 values, k = {k}: {find_max_average(nums, k):.5f}")


main()
