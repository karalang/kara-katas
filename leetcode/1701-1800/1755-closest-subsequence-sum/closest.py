# LeetCode #1755: Closest Subsequence Sum -- mirrors closest.kara (the ★
# arm): meet in the middle with binary search.
from bisect import bisect_left


def subset_sums(values):
    count = 1 << len(values)
    sums = [0] * count
    for mask in range(1, count):
        low = (mask & -mask).bit_length() - 1
        sums[mask] = sums[mask & (mask - 1)] + values[low]
    return sums


def min_abs_difference(nums, goal):
    half = len(nums) // 2
    left = subset_sums(nums[:half])
    right = sorted(subset_sums(nums[half:]))
    best = 2**31 - 1
    for l in left:
        rest = goal - l
        at = bisect_left(right, rest)
        if at < len(right):
            best = min(best, right[at] - rest)
        if at > 0:
            best = min(best, rest - right[at - 1])
    return best


seed = 1755


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    high = next_random()
    return high * 32768 + next_random()


def batch(count, most, top, reach):
    total = 0
    check = 0
    for _ in range(count):
        n = next_random() % most + 1
        nums = [wide() % (2 * top + 1) - top for _ in range(n)]
        goal = wide() % (2 * reach + 1) - reach
        answer = min_abs_difference(nums, goal)
        total += answer
        check = (check * 31 + answer + n) % 1000000007
    print(f"{count} problems of up to {most} values within {top}: differences add to {total}, checksum {check}")


print(min_abs_difference([5, -7, 3, 5], 6))
print(min_abs_difference([7, -9, 15, -2], -5))
print(min_abs_difference([1, 2, 3], -7))
print(min_abs_difference([4], 9))
print(min_abs_difference([50, 60], 20))
print(min_abs_difference([10000000, -10000000, 10000000], -1000000000))
batch(3000, 6, 5, 20)
batch(300, 20, 10000000, 100000000)
batch(10, 40, 10000000, 1000000000)
