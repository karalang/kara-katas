# LeetCode #2708: Maximum Strength of a Group -- the Python mirror of the
# star arm (strength.kara): every number but zeros taken, and of the
# negatives an odd one out, the one nearest zero, left behind; a group
# that ends up empty takes a zero if there is one.


def max_strength(nums):
    if len(nums) == 1:
        return nums[0]
    product = 1
    taken = 0
    negatives = 0
    nearest = -10
    for v in nums:
        if v != 0:
            product *= v
            taken += 1
        if v < 0:
            negatives += 1
            nearest = max(nearest, v)
    if negatives % 2 == 1:
        product //= nearest
        taken -= 1
    return product if taken > 0 else 0


seed = 2708


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


print(max_strength([3, -1, -5, 2, 5, -9]))
print(max_strength([-4, -5, -4]))
print(max_strength([-9]))
print(max_strength([0]))
print(max_strength([-1, 0]))
print(max_strength([-9, 0, 0]))
print(max_strength([9] * 13))
print(max_strength([-9] * 13))
print(max_strength([0, 0, -1, 0]))
total = 0
check = 0
for _ in range(1000):
    n = next_random() % 13 + 1
    nums = [next_random() % 19 - 9 for _ in range(n)]
    strength = max_strength(nums)
    total += strength
    check = (check * 31 + strength % 1000000007) % 1000000007
print(f"1000 groups: strengths sum to {total}, checksum {check}")
total = 0
check = 0
for _ in range(5000):
    n = next_random() % 4 + 1
    nums = [next_random() % 5 - 3 for _ in range(n)]
    strength = max_strength(nums)
    total += strength
    check = (check * 31 + strength % 1000000007) % 1000000007
print(f"5000 groups of 1 to 4 from -3 to 1: strengths sum to {total}, checksum {check}")
