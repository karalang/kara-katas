# LeetCode #2358: Maximum Number of Groups Entering a Competition -- the
# Python mirror of the ★ arm: with the grades sorted, groups of 1, 2, 3, ...
# students in order meet both conditions, so the answer is the largest k
# with 1 + 2 + ... + k <= n, found by adding group sizes.


def maximum_groups(grades):
    n = len(grades)
    k = 0
    used = 0
    while used + k + 1 <= n:
        k += 1
        used += k
    return k


SEED = [2358]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # LeetCode's two examples; one student; three; 10^5 students
    print(maximum_groups([10, 6, 12, 7, 3, 5]))
    print(maximum_groups([8, 8]))
    print(maximum_groups([1]))
    print(maximum_groups([3, 2, 1]))
    print(maximum_groups([i * 7919 % 100000 + 1 for i in range(100000)]))
    # 3000 random classes of 1 to 300 students graded 1 to 10^5
    check = 0
    total = 0
    for _ in range(3000):
        n = 1 + next_random() % 300
        grades = [1 + next_random() % 100000 for _ in range(n)]
        k = maximum_groups(grades)
        check = (check * 31 + k) % 1000000007
        total += k
    print(f"3000 classes: checksum {check}, groups {total}")


main()
