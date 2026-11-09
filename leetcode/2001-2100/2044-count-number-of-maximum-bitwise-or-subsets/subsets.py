# LeetCode #2044: Count Number of Maximum Bitwise-OR Subsets -- Python
# mirror of the ★ arm (subsets.kara): the OR of every value is the target,
# and a take-or-skip search counts the subsets that reach it.


def count_from(nums, i, acc, target):
    if i == len(nums):
        return 1 if acc == target else 0
    return count_from(nums, i + 1, acc | nums[i], target) + count_from(nums, i + 1, acc, target)


def count_max_or_subsets(nums):
    target = 0
    for x in nums:
        target |= x
    return count_from(nums, 0, 0, target)


# ---- test harness ---------------------------------------------------------

seed = 2044


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    examples = [
        [3, 1],
        [2, 2, 2],
        [3, 2, 1, 5],
        [7],
        [1, 2, 4, 8],
        [100000, 100000, 1],
        [1] * 16,
        [5, 3, 6, 4, 1],
    ]
    for nums in examples:
        print(f"[{', '.join(map(str, nums))}] -> {count_max_or_subsets(nums)}")
    total = check = 0
    for _ in range(2000):
        n = next_random() % 12 + 1
        top = next_random() % 64 + 1
        nums = [next_random() % top + 1 for _ in range(n)]
        answer = count_max_or_subsets(nums)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"2000 arrays of up to 12 values: sum {total}, checksum {check}")
    total = check = 0
    for r in range(20):
        top = [100000, 1024, 16, 2][r % 4]
        nums = [next_random() % top + 1 for _ in range(16)]
        answer = count_max_or_subsets(nums)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"20 arrays of 16 values: sum {total}, checksum {check}")


main()
