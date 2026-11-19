# LeetCode #1655: Distribute Repeating Integers -- the bench's Python
# mirror: the ★ arm on 200 random problems of 100000 numbers from 50
# values and 10 customers wanting 1 to 3000 each, all drawn first.

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


seed = 1655


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


problems = []
for _ in range(200):
    nums = [next_random() % 50 + 1 for _ in range(100000)]
    quantity = [next_random() % 3000 + 1 for _ in range(10)]
    problems.append((nums, quantity))
check = 0
served = 0
for nums, quantity in problems:
    answer = can_distribute(nums, quantity)
    if answer:
        served += 1
    check = (check * 31 + (2 if answer else 1)) % 1000000007
print(f"200 problems of 100000 numbers and 10 customers: {served} served, checksum {check}")
