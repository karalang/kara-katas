# LeetCode #1416 bench, Python: ways[i] counts the arrays the digits from i
# on can be read as, workload and checksum as number_of_arrays.kara.

MODULUS = 1000000007


def number_of_arrays(s, k):
    n = len(s)
    ways = [0] * (n + 1)
    ways[n] = 1
    for i in range(n - 1, -1, -1):
        if s[i] == "0":
            continue
        number = 0
        j = i
        while j < n:
            number = number * 10 + ord(s[j]) - 48
            if number > k:
                break
            ways[i] = (ways[i] + ways[j + 1]) % MODULUS
            j += 1
    return ways[0]


def main():
    seed = 1416
    parts = []
    last_zero = True
    for _ in range(200000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        r = seed // 65536
        zero = not last_zero and r % 10 == 0
        parts.append("0" if zero else str(1 + r % 9))
        last_zero = zero
    pool = "".join(parts)
    check = 0
    for _ in range(100):
        seed = (seed * 1103515245 + 12345) % 2147483648
        start = seed // 65536 % 100000
        while pool[start] == "0":
            start += 1
        seed = (seed * 1103515245 + 12345) % 2147483648
        k = 1 + seed % 1000000000
        check = (check * 131 + number_of_arrays(pool[start:start + 100000], k)) % 1000000007
    print(f"100 windows of 10^5 digits: checksum {check}")


main()
