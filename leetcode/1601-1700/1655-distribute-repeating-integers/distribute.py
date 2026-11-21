# LeetCode #1655: Distribute Repeating Integers -- the Python mirror of
# the ★ arm: a subset DP over the customers, one value's count at a time.

from collections import Counter


def can_distribute(nums, quantity):
    counts = Counter(nums)
    m = len(quantity)
    full = (1 << m) - 1
    want = [0] * (1 << m)
    for mask in range(1, full + 1):
        low = (mask & -mask).bit_length() - 1
        want[mask] = want[mask & (mask - 1)] + quantity[low]
    can = [False] * (1 << m)
    can[0] = True
    for count in counts.values():
        before = can[:]
        for mask in range(full + 1):
            if not before[mask]:
                continue
            rest = full & ~mask
            sub = rest
            while sub > 0:
                if want[sub] <= count:
                    can[mask | sub] = True
                sub = (sub - 1) & rest
    return can[full]


# ---- the harness: the same as every arm's ---------------------------------

seed = 1655


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, size, values, customers, most):
    check = 0
    served = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % size + 1
        distinct = next_random() % values + 1
        nums = [next_random() % distinct + 1 for _ in range(n)]
        m = next_random() % customers + 1
        quantity = [next_random() % most + 1 for _ in range(m)]
        answer = can_distribute(nums, quantity)
        if answer:
            served += 1
        check = (check * 31 + (2 if answer else 1)) % 1000000007
    print(f"{count} problems of up to {size} numbers and {customers} customers: {served} served, checksum {check}")


print(str(can_distribute([1, 2, 3, 4], [2])).lower())
print(str(can_distribute([1, 2, 3, 3], [2])).lower())
print(str(can_distribute([1, 1, 2, 2], [2, 2])).lower())
print(str(can_distribute([7, 7, 7], [3])).lower())
print(str(can_distribute([1, 1, 1, 2, 2], [2, 2, 1])).lower())
batch(3000, 12, 4, 4, 4)
batch(300, 1000, 50, 10, 30)
batch(30, 100000, 50, 10, 1000)
