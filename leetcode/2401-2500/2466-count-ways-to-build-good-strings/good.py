MOD = 1000000007


def count_good_strings(low, high, zero, one):
    ways = [0] * (high + 1)
    ways[0] = 1
    total = 0
    for length in range(1, high + 1):
        if length >= zero:
            ways[length] = (ways[length] + ways[length - zero]) % MOD
        if length >= one:
            ways[length] = (ways[length] + ways[length - one]) % MOD
        if length >= low:
            total = (total + ways[length]) % MOD
    return total


# ---- test harness ---------------------------------------------------------

seed = 2466


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = [
        (3, 3, 1, 1),
        (2, 3, 1, 2),
        (1, 1, 1, 1),
        (5, 5, 2, 2),
        (4, 9, 2, 2),
        (6, 20, 6, 6),
        (7, 30, 3, 7),
    ]
    for low, high, zero, one in cases:
        print(f"({low}, {high}, {zero}, {one}) -> {count_good_strings(low, high, zero, one)}")
    for low, high, zero, one in [(1, 100000, 1, 1), (100000, 100000, 1, 1), (100000, 100000, 1, 100000), (50000, 100000, 3, 7)]:
        print(f"({low}, {high}, {zero}, {one}) -> {count_good_strings(low, high, zero, one)}")
    check = 0
    for _ in range(3000):
        a = 1 + next_random() % 300
        b = 1 + next_random() % 300
        low = min(a, b)
        high = max(a, b)
        zero = 1 + next_random() % low
        one = 1 + next_random() % low
        check = (check * 31 + count_good_strings(low, high, zero, one)) % 1000000007
    print(f"3000 random: checksum {check}")


if __name__ == "__main__":
    main()
