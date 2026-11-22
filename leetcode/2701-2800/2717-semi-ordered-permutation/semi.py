# LeetCode #2717: Semi-Ordered Permutation -- the ★ arm (semi.kara) in
# Python: 1's index plus n's distance from the end, less one when 1
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


def random_permutation(n):
    nums = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        nums[i], nums[j] = nums[j], nums[i]
    return nums


print(semi_ordered_permutation([2, 1, 4, 3]))
print(semi_ordered_permutation([2, 4, 1, 3]))
print(semi_ordered_permutation([1, 3, 4, 2, 5]))
print(semi_ordered_permutation([1, 2]))
print(semi_ordered_permutation([2, 1]))
print(semi_ordered_permutation(list(range(50, 0, -1))))
traded = list(range(1, 51))
traded[0], traded[49] = traded[49], traded[0]
print(semi_ordered_permutation(traded))
middle = list(range(1, 51))
middle[0], middle[24] = middle[24], middle[0]
middle[49], middle[25] = middle[25], middle[49]
print(semi_ordered_permutation(middle))
middle[24], middle[25] = middle[25], middle[24]
print(semi_ordered_permutation(middle))
total = 0
check = 0
for _ in range(10000):
    n = next_random() % 49 + 2
    swaps = semi_ordered_permutation(random_permutation(n))
    total += swaps
    check = (check * 31 + swaps) % 1000000007
print(f"10000 permutations: swaps sum to {total}, checksum {check}")
