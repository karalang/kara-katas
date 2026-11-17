# LeetCode #2256: Minimum Average Difference -- Python mirror of
# average.kara: one pass with the total known, each side's average its
# sum floor-divided by its count (0 for an empty side), the first index
# with the nearest averages kept by a strict <.


def minimum_average_difference(nums):
    n = len(nums)
    total = sum(nums)
    left = 0
    best = 0
    best_gap = -1
    for i in range(n):
        left += nums[i]
        right = total - left
        left_average = left // (i + 1)
        right_average = 0 if i + 1 == n else right // (n - i - 1)
        gap = abs(left_average - right_average)
        if best_gap < 0 or gap < best_gap:
            best_gap = gap
            best = i
    return best


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    examples = [
        [2, 5, 3, 9, 5, 3],
        [0],
        [4, 4, 4, 4],
        [1, 3, 2],
        [9, 1, 1, 1, 30],
        [100000, 0, 100000, 100000],
    ]
    for nums in examples:
        print(f"{show(nums)} -> {minimum_average_difference(nums)}")
    seed = 2256
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 12 + 1
        nums = [next_random() % 11 for _ in range(n)]
        index = minimum_average_difference(nums)
        total += index
        check = (check * 31 + index + 1) % 1000000007
    print(f"2000 cases: indices summing to {total}, checksum {check}")
    any_ = [wide_random() % 100001 for _ in range(100000)]
    high = [100000 - next_random() % 3 for _ in range(100000)]
    rising = [i + 1 for i in range(100000)]
    print(f"10^5 values: {minimum_average_difference(any_)}, {minimum_average_difference(high)}, {minimum_average_difference(rising)}")


main()
