# LeetCode #2357: Make Array Zero by Subtracting Equal Amounts -- the
# Python mirror of the ★ arm: each operation clears the least positive
# value and keeps the others distinct, so the answer is the number of
# distinct positive values, counted in a set.


def minimum_operations(nums):
    return len({x for x in nums if x > 0})


SEED = [2357]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # LeetCode's two examples; all zeros; 1 to 100; 100 copies of 100
    print(minimum_operations([1, 5, 0, 3, 5]))
    print(minimum_operations([0]))
    print(minimum_operations([0] * 100))
    print(minimum_operations(list(range(1, 101))))
    print(minimum_operations([100] * 100))
    # 5000 random arrays of 1 to 100 values from 0 to 1 up to 0 to 100
    check = 0
    total = 0
    zero = 0
    for _ in range(5000):
        n = 1 + next_random() % 100
        top = 2 + next_random() % 100
        nums = [next_random() % top for _ in range(n)]
        m = minimum_operations(nums)
        check = (check * 31 + m) % 1000000007
        total += m
        if m == 0:
            zero += 1
    print(f"5000 arrays: checksum {check}, operations {total}, {zero} already zero")


main()
