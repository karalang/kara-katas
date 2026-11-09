# LeetCode #2044: Count Number of Maximum Bitwise-OR Subsets -- the ★ arm
# in Python, the same algorithm and workload as subsets.kara: the target is
# the OR of every value, and a take-or-skip search counts the subsets that
# reach it.
import sys

sys.setrecursionlimit(100)


def count_from(nums, i, acc, target):
    if i == len(nums):
        return 1 if acc == target else 0
    return count_from(nums, i + 1, acc | nums[i], target) + count_from(nums, i + 1, acc, target)


def count_max_or_subsets(nums):
    target = 0
    for x in nums:
        target |= x
    return count_from(nums, 0, 0, target)


seed = 2044


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    tops = [100000, 1024, 16, 2]
    arrays = [[next_random() % tops[r % 4] + 1 for _ in range(16)] for r in range(2000)]
    calls = total = check = 0
    for nums in arrays:
        answer = count_max_or_subsets(nums)
        calls += 1
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"{calls} calls: sum {total}, checksum {check}")


main()
