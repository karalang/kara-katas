# LeetCode #2134: Minimum Swaps to Group All 1's Together II -- the
# benchmark, the same algorithm as swaps.kara.


def min_swaps(nums):
    n = len(nums)
    k = sum(nums)
    inside = 0
    for i in range(k):
        inside += nums[i]
    most = inside
    for i in range(k, n + k):
        inside += nums[i % n] - nums[(i - k) % n]
        most = max(most, inside)
    return k - most


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [2134]
    arrays = []
    for a in range(20):
        arrays.append([1 if next_random(seed) % (a + 2) == 0 else 0 for _ in range(100000)])
    total = 0
    check = 0
    for rnd in range(10):
        for a in range(20):
            hi = next_random(seed)
            at = (hi * 32768 + next_random(seed)) % 100000
            arrays[a][at] = 1 - arrays[a][at]
            swaps = min_swaps(arrays[a])
            total += swaps
            check = (check * 31 + swaps + rnd) % 1000000007
    print(f"200 solves: {total} swaps in all, checksum {check}")


main()
