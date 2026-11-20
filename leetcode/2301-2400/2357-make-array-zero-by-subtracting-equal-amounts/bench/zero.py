# LeetCode #2357: Make Array Zero by Subtracting Equal Amounts -- the
# bench, the ★ arm in Python: the distinct positive values gathered in a
# set.


def minimum_operations(nums):
    seen = set()
    for x in nums:
        if x > 0:
            seen.add(x)
    return len(seen)


SEED = [2357]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # 2 * 10^4 arrays of 100 values from 0 to 1 up to 0 to 100
    arrays = []
    for _ in range(20000):
        top = 2 + next_random() % 100
        arrays.append([next_random() % top for _ in range(100)])
    check = 0
    for p in range(50):
        for nums in arrays:
            check = (check * 31 + minimum_operations(nums) + p) % 1000000007
    print(f"50 passes over 2 * 10^4 arrays of 100 values: checksum {check}")


main()
