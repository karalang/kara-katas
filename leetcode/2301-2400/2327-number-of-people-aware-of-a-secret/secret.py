# LeetCode #2327: Number of People Aware of a Secret -- the Python mirror
# of the ★ arm: a running count of the people sharing, gaining those who
# learned the secret `delay` days back and losing those who learned it
# `forget` days back.

MOD = 1000000007


def people_aware_of_secret(n, delay, forget):
    learned = [0] * (n + 1)
    learned[1] = 1
    sharing = 0
    for day in range(2, n + 1):
        if day - delay >= 1:
            sharing = (sharing + learned[day - delay]) % MOD
        if day - forget >= 1:
            sharing = (sharing - learned[day - forget] + MOD) % MOD
        learned[day] = sharing
    aware = 0
    for day in range(n - forget + 1, n + 1):
        aware = (aware + learned[day]) % MOD
    return aware


seed = 2327


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(people_aware_of_secret(6, 2, 4))
    print(people_aware_of_secret(4, 1, 3))
    print(people_aware_of_secret(2, 1, 2))
    print(people_aware_of_secret(1000, 1, 1000))
    print(people_aware_of_secret(1000, 999, 1000))
    print(people_aware_of_secret(1000, 3, 7))
    check = 0
    total = 0
    for _ in range(2000):
        n = next_random() % 299 + 2
        forget = next_random() % (n - 1) + 2
        delay = next_random() % (forget - 1) + 1
        aware = people_aware_of_secret(n, delay, forget)
        check = (check * 31 + aware) % 1000000007
        total = (total + aware) % 1000000007
    print(f"2000 cases: checksum {check}, total {total}")


main()
