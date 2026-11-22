# LeetCode #2702: Minimum Operations to Make Numbers Non-positive -- the
# bench (nonpositive.kara in Python): a binary search on the count, each
# trial summing the extra shares the numbers still above t * y need.


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


arrays, n, rounds = 100, 10000, 5
problems = []
for _ in range(arrays):
    nums = [wide() % 1000000000 + 1 for _ in range(n)]
    y = next_random() % 1000 + 1
    x = y + wide() % 1000000 + 1
    problems.append((nums, x, y))
total = 0
check = 0
for r in range(rounds):
    for nums, x, y in problems:
        t = min_operations(nums, x, y)
        total += t
        check = (check * 31 + t + r) % 1000000007
print(f"{arrays} arrays of {n} numbers up to 1000000000, {rounds} rounds: operations sum to {total}, checksum {check}")
