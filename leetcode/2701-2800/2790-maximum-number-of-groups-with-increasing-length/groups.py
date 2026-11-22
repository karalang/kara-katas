# LeetCode #2790: Maximum Number of Groups With Increasing Length -- the
# ★ arm in Python (groups.kara): the limits sorted, a running sum of
# places, one more group whenever it reaches the next triangular number.


def max_increasing_groups(usage_limits):
    groups = 0
    places = 0
    for u in sorted(usage_limits):
        places += u
        if places >= (groups + 1) * (groups + 2) // 2:
            groups += 1
    return groups


seed = 2790


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    print(max_increasing_groups([1, 2, 5]))
    print(max_increasing_groups([2, 1, 2]))
    print(max_increasing_groups([1, 1]))
    print(max_increasing_groups([1000000000]))
    n = 100000
    print(max_increasing_groups([1000000000] * n))
    print(max_increasing_groups([1] * n))
    total = 0
    check = 0
    for _ in range(3000):
        m = next_random() % 12 + 1
        limits = [next_random() % 10 + 1 for _ in range(m)]
        a = max_increasing_groups(limits)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"3000 small arrays: groups sum to {total}, checksum {check}")
    total = 0
    check = 0
    for _ in range(20):
        limits = [wide() % 1000000000 + 1 for _ in range(n)]
        a = max_increasing_groups(limits)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"20 arrays of 10^5: groups sum to {total}, checksum {check}")


main()
