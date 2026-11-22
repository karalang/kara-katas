# LeetCode #2798: Number of Employees Who Met the Target -- the bench in
# Python: the ★ arm over 20000 teams of 50 with hours and targets up to
# 10^5, all drawn first, then each answered 500 times.


def number_of_employees_who_met_target(hours, target):
    return sum(1 for h in hours if h >= target)


seed = 2798


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count = 20000
    rounds = 500
    cases = []
    for _ in range(count):
        hours = [wide() % 100001 for _ in range(50)]
        cases.append((hours, wide() % 100001))
    total = 0
    check = 0
    for r in range(rounds):
        for hours, target in cases:
            a = number_of_employees_who_met_target(hours, target)
            total += a
            check = (check * 31 + a + r) % 1000000007
    print(f"{count} teams of 50, {rounds} rounds: met sum to {total}, checksum {check}")


main()
