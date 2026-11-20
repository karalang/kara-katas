# LeetCode #1712: Ways to Split Array Into Three Subarrays -- the Python
# mirror of the ★ arm (split.kara): prefix sums, and for each end of the
# left part the range of ends of the middle found by two binary searches.

from bisect import bisect_left, bisect_right


def ways_to_split(nums):
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]
    total = prefix[n]
    ways = 0
    for i in range(1, n - 1):
        left = prefix[i]
        # the middle ends at j, i < j < n: left <= mid, and mid <= right
        lo = max(bisect_left(prefix, 2 * left), i + 1)
        hi = min(bisect_right(prefix, (total + left) // 2), n)
        if hi > lo:
            ways += hi - lo
    return ways % 1000000007


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def batch(count, most, top, seed):
    total = 0
    check = 0
    for _ in range(count):
        n = next_random(seed) % (most - 2) + 3
        nums = [next_random(seed) % (top + 1) for _ in range(n)]
        answer = ways_to_split(nums)
        total += answer
        check = (check * 31 + answer + n) % 1000000007
    print(f"{count} arrays of up to {most} values up to {top}: answers sum to {total}, checksum {check}")


def main():
    # LeetCode's three examples, then all zeros, and the largest array
    # of the largest values
    print(ways_to_split([1, 1, 1]))
    print(ways_to_split([1, 2, 2, 2, 5, 0]))
    print(ways_to_split([3, 2, 1]))
    print(ways_to_split([0, 0, 0, 0, 0]))
    print(ways_to_split([10000] * 100000))
    seed = [1712]
    batch(3000, 12, 4, seed)
    batch(300, 1000, 10000, seed)
    batch(10, 100000, 3, seed)


main()
