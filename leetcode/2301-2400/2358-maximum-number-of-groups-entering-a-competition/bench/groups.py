# LeetCode #2358: Maximum Number of Groups Entering a Competition -- the
# bench, the ★ arm in Python: group sizes 1, 2, 3, ... added while the next
# still fits in the class.


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
    # class a holds 10^4 (a + 1) - a students graded 1 to 10^5
    classes = []
    for a in range(10):
        classes.append([1 + next_random() % 100000 for _ in range(10000 * (a + 1) - a)])
    check = 0
    for p in range(20000):
        for grades in classes:
            check = (check * 31 + maximum_groups(grades) + p) % 1000000007
    print(f"20000 passes over 10 classes: checksum {check}")


main()
