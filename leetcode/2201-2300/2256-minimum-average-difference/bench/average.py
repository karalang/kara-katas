# LeetCode #2256: Minimum Average Difference -- the benchmark's Python
# mirror of average.kara: one pass with the total known, the first index
# whose two rounded-down averages are nearest.


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


seed = 2256


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def main():
    check = 0
    for _ in range(20):
        nums = [wide_random() % 100001 for _ in range(100000)]
        check = (check * 31 + minimum_average_difference(nums) + 1) % 1000000007
    print(f"20 cases of 10^5 values: checksum {check}")


main()
