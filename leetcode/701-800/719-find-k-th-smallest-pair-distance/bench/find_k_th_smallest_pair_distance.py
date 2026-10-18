# LeetCode #719: Find K-th Smallest Pair Distance -- binary search on
# the distance. Benchmark mirror of the Kara star arm: sort a copy,
# then find the least distance with at least k pairs, counting pairs
# with two pointers.


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def smallest_distance_pair(nums, k):
    s = sorted(nums)
    n = len(s)
    lo, hi = 0, s[-1] - s[0]
    while lo < hi:
        mid = (lo + hi) // 2
        count = 0
        left = 0
        for right in range(n):
            while s[right] - s[left] > mid:
                left += 1
            count += right - left
        if count >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def random_num(seed):
    hi = next_random(seed)
    lo = next_random(seed)
    return (hi * 32768 + lo) % 1000001


def main():
    seed = [719]
    arrays = [[random_num(seed) for _ in range(5000)] for _ in range(40)]
    pairs = 5000 * 4999 // 2
    total = 0
    for rnd in range(25):
        for a in range(40):
            k = 1 + (rnd * 7919 + a * 104729) % pairs
            total += smallest_distance_pair(arrays[a], k)
    print(f"25 rounds of 40 arrays of 5000 numbers: sum {total}")


main()
