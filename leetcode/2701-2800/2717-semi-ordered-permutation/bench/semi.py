# LeetCode #2717: Semi-Ordered Permutation -- the bench (semi.kara in
# Python): 1's index plus n's distance from the end, less one when 1
# starts right of n.


def semi_ordered_permutation(nums):
    n = len(nums)
    first = nums.index(1)
    last = nums.index(n)
    swaps = first + (n - 1 - last)
    return swaps - 1 if first > last else swaps


seed = 2717


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


count, rounds = 200000, 20
perms = []
for _ in range(count):
    nums = list(range(1, 51))
    for i in range(49, 0, -1):
        j = next_random() % (i + 1)
        nums[i], nums[j] = nums[j], nums[i]
    perms.append(nums)
total = 0
check = 0
for r in range(rounds):
    for nums in perms:
        swaps = semi_ordered_permutation(nums)
        total += swaps
        check = (check * 31 + swaps + r) % 1000000007
print(f"{count} permutations of 50, {rounds} rounds: swaps sum to {total}, checksum {check}")
