# LeetCode #2869: Minimum Operations to Collect Elements -- the Python
# mirror of the ★ arm (collect.kara): a bit mask filled from the right.


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


# ---- the harness: the same in every arm --------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    print(f"{min_operations([3, 1, 5, 4, 2], 2)} {min_operations([3, 1, 5, 4, 2], 5)} {min_operations([3, 2, 5, 3, 1], 3)}")
    print(f"{min_operations(list(range(50, 0, -1)), 50)} {min_operations(list(range(1, 51)), 25)}")
    seed = 2869
    total = 0
    check = 0
    for c in range(6000):
        n = next_random() % 8 + 1 if c < 3000 else 50
        nums = [next_random() % n + 1 for _ in range(n)]
        nums[next_random() % n] = 1
        reach = 1
        while reach + 1 in nums:
            reach += 1
        k = next_random() % reach + 1
        ops = min_operations(nums, k)
        total += ops
        check = (check * 31 + ops) % 1000000007
        if c == 2999 or c == 5999:
            print(f"3000 {'short' if c < 3000 else 'long'} arrays: {total} operations, checksum {check}")
            total = 0
            check = 0


main()
