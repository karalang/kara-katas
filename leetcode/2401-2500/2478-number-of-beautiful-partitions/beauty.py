# LeetCode #2478: Number of Beautiful Partitions -- Python mirror of
# beauty.kara: by cuts, a running sum per part count.

MOD = 1000000007


def is_prime_digit(c):
    return c == 2 or c == 3 or c == 5 or c == 7


def beautiful_partitions(s, k, min_length):
    digits = [ord(c) - ord('0') for c in s]
    n = len(digits)
    if not is_prime_digit(digits[0]) or is_prime_digit(digits[n - 1]):
        return 0
    cut = [i == n or (i > 0 and not is_prime_digit(digits[i - 1]) and is_prime_digit(digits[i])) for i in range(n + 1)]
    ways = [0] * (n + 1)
    ways[0] = 1
    for _ in range(k):
        nxt = [0] * (n + 1)
        running = 0
        for i in range(min_length, n + 1):
            start = i - min_length
            if start == 0 or (cut[start] and start < n):
                running = (running + ways[start]) % MOD
            if cut[i] and i > 0:
                nxt[i] = running
        ways = nxt
    return ways[n]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_digits(n):
    return "".join(str(1 + next_random() % 9) for _ in range(n))


def main():
    global seed
    cases = [("23542185131", 3, 2), ("23542185131", 3, 3), ("3312958", 3, 1), ("2", 1, 1), ("1", 1, 1),
             ("12", 1, 1), ("23", 1, 1), ("2121", 2, 3), ("212121", 3, 2), ("2222111", 2, 1)]
    for s, k, m in cases:
        print(f'"{s}", {k}, {m} -> {beautiful_partitions(s, k, m)}')
    alternating = "21" * 500
    print(f'"21" x 500, 500, 2 -> {beautiful_partitions(alternating, 500, 2)}')
    print(f'"21" x 500, 250, 4 -> {beautiful_partitions(alternating, 250, 4)}')
    print(f'"21" x 500, 100, 3 -> {beautiful_partitions(alternating, 100, 3)}')
    seed = 2478
    long = "2" + random_digits(998) + "1"
    for k in [1, 10, 100, 300]:
        for m in [1, 2, 3]:
            print(f"random 1000, {k}, {m} -> {beautiful_partitions(long, k, m)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 40
        s = random_digits(n)
        k = 1 + next_random() % n
        m = 1 + next_random() % n
        check = (check * 31 + beautiful_partitions(s, k, m)) % MOD
    print(f"3000 random: checksum {check}")


if __name__ == "__main__":
    main()
