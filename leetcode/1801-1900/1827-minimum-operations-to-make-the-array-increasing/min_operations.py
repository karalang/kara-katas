# LeetCode #1827: Minimum Operations to Make the Array Increasing -- the ★
# arm in Python


def min_operations(nums):
    operations = 0
    last = 0
    for x in nums:
        if x <= last:
            last += 1
            operations += last - x
        else:
            last = x
    return operations


seed = 1827


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


print(min_operations([1, 1, 1]), min_operations([1, 5, 2, 4, 1]), min_operations([8]))
print(min_operations([3, 3]), min_operations([1, 2, 3, 4]), min_operations([5, 4, 3, 2, 1]), min_operations([1, 9, 1, 1, 10]), min_operations([10000, 1]))
print(f"the most: {min_operations([1] * 5000)} {min_operations([10000] * 5000)} {min_operations([10000 - i for i in range(5000)])}")
check = 0
for _ in range(3000):
    n = 1 + next_random() % 12
    nums = [1 + next_random() % 20 for _ in range(n)]
    check = (check * 31 + min_operations(nums)) % 1000000007
print(f"3000 random cases: checksum {check}")
