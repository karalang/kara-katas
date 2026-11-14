# LeetCode #1569: Number of Ways to Reorder Array to Get Same BST -- the
# Python mirror of the ★ arm (ways.kara): the interleavings of the two
# subtrees' orders, a binomial from Pascal's triangle, times each side's
# own count, by recursion. O(n^2)

MOD = 1000000007


def ways(nums, choose):
    if len(nums) <= 2:
        return 1
    root = nums[0]
    left = [x for x in nums[1:] if x < root]
    right = [x for x in nums[1:] if x > root]
    return choose[len(nums) - 1][len(left)] * ways(left, choose) % MOD * ways(right, choose) % MOD


def num_of_ways(nums):
    n = len(nums)
    choose = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        choose[i][0] = 1
        for j in range(1, i + 1):
            choose[i][j] = (choose[i - 1][j - 1] + choose[i - 1][j]) % MOD
    return (ways(nums, choose) - 1 + MOD) % MOD


# ---- the harness: the same in every arm

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most):
    check = 0
    none = 0
    for _ in range(count):
        n = next_random() % most + 1
        nums = list(range(1, n + 1))
        for i in range(n - 1, 0, -1):
            j = (next_random() * 32768 + next_random()) % (i + 1)
            nums[i], nums[j] = nums[j], nums[i]
        w = num_of_ways(nums)
        if w == 0:
            none += 1
        check = mix(check, w)
    print(f"{count} permutations of up to {most} values: {none} with no other order, checksum {check}")


def main():
    global seed
    examples = [
        [2, 1, 3],
        [3, 4, 5, 1, 2],
        [1, 2, 3],
        [1],
        [3, 1, 2, 5, 4],
        [4, 2, 6, 1, 3, 5, 7],
        [5, 1, 2, 3, 4, 6, 7, 8, 9],
        [10, 5, 15, 3, 7, 12, 18, 1, 4, 6, 8, 11, 13, 17, 19, 2, 9, 14, 16, 20],
    ]
    for nums in examples:
        print(f"{nums} -> {num_of_ways(nums)}")
    wide = [500 - i // 2 if i % 2 == 0 else 501 + i // 2 for i in range(1000)]
    print(f"500, 501, 499, 502, .. -> {num_of_ways(wide)}")
    seed = 1569
    batch(3000, 8)
    batch(300, 100)
    batch(30, 1000)


main()
