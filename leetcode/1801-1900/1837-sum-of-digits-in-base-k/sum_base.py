# LeetCode #1837: Sum of Digits in Base K -- the ★ arm in Python


def sum_base(n, k):
    left = n
    total = 0
    while left > 0:
        total += left % k
        left //= k
    return total


seed = 1837


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(f"{sum_base(34, 6)} {sum_base(10, 10)}")
    print(f"{sum_base(1, 2)} {sum_base(7, 7)} {sum_base(6, 7)} {sum_base(81, 3)} {sum_base(100, 2)} {sum_base(100, 10)} {sum_base(99, 10)}")
    every = 0
    most = 0
    for n in range(1, 101):
        for k in range(2, 11):
            s = sum_base(n, k)
            every = (every * 31 + s) % 1000000007
            most = max(most, s)
    print(f"every case: checksum {every}, the most {most}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 100
        k = 2 + next_random() % 9
        check = (check * 31 + sum_base(n, k)) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
