# LeetCode #2790: Maximum Number of Groups With Increasing Length -- the
# bench in Python: the ★ arm over 20 arrays of 10^5 limits up to 10^9,
# all drawn first, then each answered 10 times, each answer sorting its
# own copy.


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
    count = 20
    rounds = 10
    cases = []
    for c in range(count):
        top = 1000000000 if c % 2 == 0 else 100000
        cases.append([wide() % top + 1 for _ in range(100000)])
    total = 0
    check = 0
    for r in range(rounds):
        for limits in cases:
            a = max_increasing_groups(limits)
            total += a
            check = (check * 31 + a + r) % 1000000007
    print(f"{count} arrays of 10^5, {rounds} rounds: groups sum to {total}, checksum {check}")


main()
