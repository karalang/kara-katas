# LeetCode #1227 bench: the running-sum arm in Python, over the same 1000
# random n up to 10^5 as the Kāra bench.


def nth_person_gets_nth_seat(n):
    f = 1.0
    s = 0.0
    for m in range(2, n + 1):
        f = (1.0 + s) / m
        s += f
    return f


def main():
    seed = 1227

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    total = 0.0
    for _ in range(1000):
        n = next_random() % 30000 * 3 + next_random() % 10000 + 1
        total += nth_person_gets_nth_seat(n)
    print(f"1000 random n up to 10^5: total {total:.5f}")


main()
