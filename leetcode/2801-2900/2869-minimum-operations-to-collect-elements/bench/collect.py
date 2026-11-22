# LeetCode #2869: Minimum Operations to Collect Elements -- the bench,
# as collect.kara: 50000 arrays of 50 values, each answered 20 times by
# the bit-mask arm.


def min_operations(nums, k):
    full = (1 << k) - 1
    mask = 0
    n = len(nums)
    for i in range(n - 1, -1, -1):
        if nums[i] <= k:
            mask |= 1 << (nums[i] - 1)
        if mask == full:
            return n - i
    return n


seed = 2869


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds, n = 50000, 20, 50
    cases = []
    for _ in range(count):
        nums = [next_random() % n + 1 for _ in range(n)]
        nums[next_random() % n] = 1
        reach = 1
        while reach + 1 in nums:
            reach += 1
        cases.append((nums, next_random() % reach + 1))
    total = 0
    check = 0
    for r in range(rounds):
        for nums, k in cases:
            ops = min_operations(nums, k)
            total += ops
            check = (check * 31 + ops + r) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: {total} operations, checksum {check}")


main()
