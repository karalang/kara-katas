# LeetCode #1755: Closest Subsequence Sum -- the bench (closest.kara in
# Python): meet in the middle with binary search.
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


count, n = 8, 40
problems = []
for _ in range(count):
    nums = [wide() % 20000001 - 10000000 for _ in range(n)]
    goal = wide() % 200000001 - 100000000
    problems.append((nums, goal))
total = 0
check = 0
for nums, goal in problems:
    answer = min_abs_difference(nums, goal)
    total += answer
    check = (check * 31 + answer) % 1000000007
print(f"{count} problems of {n} values: differences add to {total}, checksum {check}")
