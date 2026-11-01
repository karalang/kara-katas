# LeetCode #1031: Maximum Sum of Two Non-Overlapping Subarrays -- one pass over prefix sums
# Mirrors max_two.kara (the ★ arm) and prints the same output.


def max_sum_two_no_overlap(nums, first_len, second_len):
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]
    best = best_first = best_second = 0
    for i in range(first_len + second_len, n + 1):
        best_first = max(best_first, prefix[i - second_len] - prefix[i - second_len - first_len])
        best_second = max(best_second, prefix[i - first_len] - prefix[i - first_len - second_len])
        best = max(best, best_first + prefix[i] - prefix[i - second_len],
                   best_second + prefix[i] - prefix[i - first_len])
    return best


seed = 1031


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    return "[" + ",".join(str(x) for x in nums) + "]"


def main():
    examples = [
        ([0, 6, 5, 2, 2, 5, 1, 9, 4], 1, 2),
        ([3, 8, 1, 3, 2, 1, 8, 9, 0], 3, 2),
        ([2, 1, 5, 6, 0, 9, 5, 0, 3, 8], 4, 3),
        ([1, 2], 1, 1),
        ([5, 5, 5, 5, 5], 2, 3),
        ([0, 0, 0, 0], 1, 2),
        ([9, 0, 0, 0, 0, 9], 1, 1),
        ([1, 9, 9, 1, 1, 1, 8, 8], 2, 2),
    ]
    for nums, first_len, second_len in examples:
        print(f"{show(nums)}, {first_len}, {second_len} -> {max_sum_two_no_overlap(nums, first_len, second_len)}")
    groups = [(3000, 4, 9), (1000, 12, 1000), (300, 40, 100), (60, 200, 1000), (10, 1000, 1000), (200, 30, 1)]
    for count, n, top in groups:
        total = 0
        check = 0
        for _ in range(count):
            nums = [next_random() % (top + 1) for _ in range(n)]
            first_len = next_random() % (n - 1) + 1
            second_len = next_random() % (n - first_len) + 1
            answer = max_sum_two_no_overlap(nums, first_len, second_len)
            total += answer
            check = (check * 131 + answer) % 1000000007
        print(f"{count} arrays of {n} values (0 to {top}): sum {total}, checksum {check}")
    full = [1000] * 1000
    rising = list(range(1000))
    print(f"1000 values of 1000, lengths 1 and 999: {max_sum_two_no_overlap(full, 1, 999)}")
    print(f"1000 values of 1000, lengths 500 and 500: {max_sum_two_no_overlap(full, 500, 500)}")
    print(f"0 to 999, lengths 10 and 300: {max_sum_two_no_overlap(rising, 10, 300)}")
    print(f"0 to 999, lengths 300 and 10: {max_sum_two_no_overlap(rising, 300, 10)}")


main()
