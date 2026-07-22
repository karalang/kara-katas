"""LeetCode 152 — Maximum Product Subarray (Python mirror / oracle).

O(n) DP tracking both the max and min running product ending at each index (a
negative element swaps their roles). Mirrors the Kāra version exactly.
"""


def max_product(nums):
    n = len(nums)
    if n == 0:
        return 0
    best = cur_max = cur_min = nums[0]
    for i in range(1, n):
        x = nums[i]
        if x < 0:
            cur_max, cur_min = cur_min, cur_max
        cur_max = max(x, cur_max * x)
        cur_min = min(x, cur_min * x)
        if cur_max > best:
            best = cur_max
    return best


def run(nums):
    print(max_product(nums))


def main():
    run([2, 3, -2, 4])
    run([-2, 0, -1])
    run([-2, 3, -4])
    run([2, -5, -2, -4, 3])
    run([-2])
    run([0, 2])


main()
