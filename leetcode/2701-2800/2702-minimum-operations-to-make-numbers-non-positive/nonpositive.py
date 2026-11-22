# LeetCode #2702: Minimum Operations to Make Numbers Non-positive -- the
# Python mirror of the star arm (nonpositive.kara): a binary search on
# the number of operations t. After t operations every number has lost
# t * y, and each chosen one x - y more, so t operations suffice exactly
# when the numbers still above t * y need, each rounded up, at most t
# extra shares of x - y.


def min_operations(nums, x, y):
    low = 0
    high = max(nums) // y + 1
    while low < high:
        t = (low + high) // 2
        need = 0
        for v in nums:
            if v > t * y:
                need += (v - t * y + x - y - 1) // (x - y)
                if need > t:
                    break
        if need <= t:
            high = t
        else:
            low = t + 1
    return low


seed = 2702


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    return next_random() * 32768 + next_random()


print(min_operations([3, 4, 1, 7, 6], 4, 2))
print(min_operations([1, 2, 1], 2, 1))
print(min_operations([1], 2, 1))
print(min_operations([1000000000], 1000000000, 1))
print(min_operations([1000000000] * 100000, 1000000000, 999999999))
print(min_operations([1000000000] * 100000, 2, 1))
print(min_operations([1000000000 - i for i in range(100000)], 1000000000, 1))
total = 0
check = 0
for _ in range(2000):
    n = next_random() % 8 + 1
    nums = [next_random() % 100 + 1 for _ in range(n)]
    y = next_random() % 20 + 1
    x = y + next_random() % 30 + 1
    t = min_operations(nums, x, y)
    total += t
    check = (check * 31 + t) % 1000000007
print(f"2000 cases up to 100: operations sum to {total}, checksum {check}")
total = 0
check = 0
for _ in range(200):
    n = next_random() % 1000 + 1
    nums = [wide() % 1000000000 + 1 for _ in range(n)]
    y = wide() % 999999999 + 1
    if next_random() % 2 == 0:
        y = next_random() % 1000 + 1
    x = y + wide() % (1000000000 - y) + 1
    t = min_operations(nums, x, y)
    total += t
    check = (check * 31 + t) % 1000000007
print(f"200 cases up to 1000000000: operations sum to {total}, checksum {check}")
