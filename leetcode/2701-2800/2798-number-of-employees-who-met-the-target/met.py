# LeetCode #2798: Number of Employees Who Met the Target -- the ★ arm in
# Python (met.kara): the hours at or above the target counted.


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
    print(number_of_employees_who_met_target([0, 1, 2, 3, 4], 2))
    print(number_of_employees_who_met_target([5, 1, 4, 2, 2], 6))
    print(number_of_employees_who_met_target([0, 0, 7], 0))
    most = [100000] * 50
    print(number_of_employees_who_met_target(most, 100000))
    print(number_of_employees_who_met_target(most, 100001))
    for top in [20, 100000]:
        total = 0
        check = 0
        for _ in range(3000):
            n = next_random() % 50 + 1
            hours = [wide() % (top + 1) for _ in range(n)]
            target = wide() % (top + 1)
            a = number_of_employees_who_met_target(hours, target)
            total += a
            check = (check * 31 + a) % 1000000007
        print(f"3000 teams, hours up to {top}: met sum to {total}, checksum {check}")


main()
