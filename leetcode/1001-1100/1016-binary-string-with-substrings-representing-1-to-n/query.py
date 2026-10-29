# LeetCode #1016: Binary String With Substrings Representing 1 To N --
# the upper half (mirror of query.kara)


def query_string(s, n):
    if n - n // 2 > 2 * len(s):
        return False
    x = n
    while x > n // 2:
        if f"{x:b}" not in s:
            return False
        x -= 1
    return True


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_bits(seed, length, ones):
    return "".join("1" if next_random(seed) % 8 < ones else "0" for _ in range(length))


def main():
    examples = [
        ("0110", 3),
        ("0110", 4),
        ("1", 1),
        ("0", 1),
        ("10", 2),
        ("110", 3),
        ("1101100", 6),
        ("11011100", 6),
        ("1111000101", 5),
        ("1111000101", 6),
        ("10010111011", 7),
        ("1", 1000000000),
    ]
    for s, n in examples:
        print(f's = "{s}", n = {n} -> {str(query_string(s, n)).lower()}')
    seed = [1016]
    groups = [(300, 8, 4, 12), (300, 30, 4, 40), (30, 200, 4, 100), (3, 1000, 4, 300), (3, 1000, 7, 40), (3, 1000, 1, 40)]
    for count, length, ones, most in groups:
        holds = 0
        largest = 0
        check = 0
        for _ in range(count):
            s = random_bits(seed, length, ones)
            for n in range(1, most + 1):
                answer = query_string(s, n)
                if answer:
                    holds += 1
                    largest = max(largest, n)
                check = (check * 2 + (1 if answer else 0)) % 1000000007
        print(f"{count} random strings of {length} bits ({ones}/8 ones), n = 1..{most}: {holds} hold, largest {largest}, checksum {check}")
    built = 0
    cut = 0
    for m in range(1, 301):
        s = "".join(f"{x:b}" for x in range(1, m + 1))
        if query_string(s, m):
            built += 1
        shorter = s[: len(s) - len(f"{m:b}")]
        if query_string(shorter, m):
            cut += 1
    print(f"300 built strings: {built} hold; with the last form cut off: {cut} hold")


main()
