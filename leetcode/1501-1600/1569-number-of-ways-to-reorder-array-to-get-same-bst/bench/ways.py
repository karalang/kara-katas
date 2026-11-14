# LeetCode #1569: Number of Ways to Reorder Array to Get Same BST -- bench:
# the ★ arm (the interleavings, by recursion and Pascal's triangle) over 20
# permutations of 1 to 1000, built once; 15 passes, each first swapping two
# values of every permutation.

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


seed = 1569


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    n = 1000
    perms = []
    for _ in range(20):
        nums = list(range(1, n + 1))
        for i in range(n - 1, 0, -1):
            j = (next_random() * 32768 + next_random()) % (i + 1)
            nums[i], nums[j] = nums[j], nums[i]
        perms.append(nums)
    check = 0
    total = 0
    for p in range(15):
        for q in range(len(perms)):
            i = (p * 7919 + q * 104729) % n
            j = (p * 104729 + q * 7919 + 1) % n
            perms[q][i], perms[q][j] = perms[q][j], perms[q][i]
            w = num_of_ways(perms[q])
            total = (total + w) % MOD
            check = mix(check, w)
    print(f"15 passes over 20 permutations of 1000 values: ways sum {total}, checksum {check}")


main()
