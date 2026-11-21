# LeetCode #2478: Number of Beautiful Partitions -- bench, Python mirror
# of beauty.kara.

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


seed = 2478


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_digits(n):
    return "2" + "".join(str(1 + next_random() % 9) for _ in range(n - 2)) + "1"


def main():
    strings = [random_digits(1000) for _ in range(20)]
    check = 0
    for p in range(90):
        for s in strings:
            k = 1 + check % 100
            m = 1 + check % 5
            check = (check * 31 + beautiful_partitions(s, k, m) + p) % MOD
    print(f"90 passes over 20 strings of 1000: checksum {check}")


main()
