# LeetCode #1346: Check If N and Its Double Exist -- Python mirror of the ★
# arm: a set of the values seen so far, each new value checked for its
# double and, when even, its half, before it is added.


def check_if_exist(arr):
    seen = set()
    for x in arr:
        if 2 * x in seen or (x % 2 == 0 and x // 2 in seen):
            return True
        seen.add(x)
    return False


seed = 1346


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def b(v):
    return "true" if v else "false"


def main():
    e1 = check_if_exist([10, 2, 5, 3])
    e2 = check_if_exist([3, 1, 7, 11])
    one_zero = check_if_exist([0, 5])
    two_zeros = check_if_exist([0, 5, 0])
    negative = check_if_exist([-2, 3, -4])
    far = [7] + [2 * k - 999 for k in range(498)] + [14]
    odds = [2 * k - 499 for k in range(500)]
    odds_and = [2 * k - 499 for k in range(499)] + [994]
    print(" ".join(b(x) for x in (e1, e2, one_zero, two_zeros, negative, check_if_exist(far), check_if_exist(odds), check_if_exist(odds_and))))
    found = 0
    check = 0
    for t in range(2000):
        n = 2 + next_random() % 499 if t % 10 == 0 else 2 + next_random() % 15
        arr = []
        for _ in range(n):
            if t % 3 == 0:
                v = next_random() % 21 - 10
            elif t % 3 == 1:
                v = next_random() % 2001 - 1000
            else:
                v = 2 * (next_random() % 1000) - 999
            arr.append(v)
        yes = check_if_exist(arr)
        if yes:
            found += 1
        check = (check * 131 + (2 if yes else 1)) % 1000000007
    print(f"2000 random arrays: {found} with a double, checksum {check}")


main()
