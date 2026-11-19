# LeetCode #2327: Number of People Aware of a Secret -- the bench, the ★
# arm in Python. A running count of the people sharing gains those who
# learned the secret `delay` days back and loses those who learned it
# `forget` days back, and that many learn it each day. O(n).

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


def main():
    seed = 2327

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    cases = []
    for _ in range(3000):
        forget = next_random() % 989 + 2
        delay = next_random() % (forget - 1) + 1
        cases.append((delay, forget))
    check = 0
    for p in range(10):
        for k in range(3000):
            delay, forget = cases[k]
            n = 990 + (k + p) % 11
            check = (check * 31 + people_aware_of_secret(n, delay, forget)) % 1000000007
    print(f"10 passes over 3000 cases of up to 1000 days: checksum {check}")


main()
