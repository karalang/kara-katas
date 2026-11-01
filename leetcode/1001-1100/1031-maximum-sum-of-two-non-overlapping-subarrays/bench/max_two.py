# LeetCode #1031: Maximum Sum of Two Non-Overlapping Subarrays -- bench
# Mirrors ./max_two.kara; see ../README.md § Benchmarks.


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


def main():
    count, rounds = 1000, 200
    cases = []
    for _ in range(count):
        nums = [next_random() % 1001 for _ in range(1000)]
        first_len = next_random() % 999 + 1
        second_len = next_random() % (1000 - first_len) + 1
        cases.append((nums, first_len, second_len))
    total = 0
    check = 0
    for _ in range(rounds):
        for nums, first_len, second_len in cases:
            answer = max_sum_two_no_overlap(nums, first_len, second_len)
            total += answer
            check = (check * 131 + answer) % 1000000007
    print(f"{count} arrays of 1000 values, {rounds} rounds: sum {total}, checksum {check}")


main()
