# LeetCode #2344: Minimum Deletions to Make Array Divisible -- the Python
# mirror of the ★ arm: the gcd of numsDivide, then nums sorted and the
# first value that divides it; every value before it is deleted.


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def min_operations(nums, nums_divide):
    g = 0
    for x in nums_divide:
        g = gcd(g, x)
    for i, x in enumerate(sorted(nums)):
        if g % x == 0:
            return i
    return -1


SEED = [2344]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    print(min_operations([2, 3, 2, 4, 3], [9, 6, 9, 3, 15]))
    print(min_operations([4, 3, 6], [8, 2, 6, 10]))
    print(min_operations([1], [1000000000]))
    print(min_operations([7, 7, 7], [6]))
    print(min_operations([1000000000, 999999999, 3, 7], [1000000000]))
    nums = [(i * 7919) % 100000 + 11 for i in range(2000)]
    print(min_operations(nums, [x * 4 * 9 * 5 for x in range(1, 200)]))
    check = 0
    total = 0
    possible = 0
    for _ in range(2000):
        n = 1 + next_random() % 12
        m = 1 + next_random() % 6
        spread = 2 + next_random() % 30
        nums = [1 + next_random() % spread for _ in range(n)]
        base = 1 + next_random() % 12
        nums_divide = [base * (1 + next_random() % 10) for _ in range(m)]
        answer = min_operations(nums, nums_divide)
        check = (check * 31 + answer + 1) % 1000000007
        total += answer
        if answer >= 0:
            possible += 1
    print(f"2000 cases: checksum {check}, sum {total}, possible {possible}")


main()
