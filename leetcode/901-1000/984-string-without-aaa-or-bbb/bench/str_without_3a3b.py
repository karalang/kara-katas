# Benchmark: LeetCode #984 String Without AAA or BBB -- the ★ arm, greedy,
# reading the tail, on every pair of counts up to LeetCode's 100.
# Mirrors str_without_3a3b.kara, .rs, .c and go-seq/.


def str_without_3a3b(a, b):
    s = ""
    left_a, left_b = a, b
    while left_a > 0 or left_b > 0:
        if s.endswith("aa"):
            write_a = False
        elif s.endswith("bb"):
            write_a = True
        else:
            write_a = left_a >= left_b
        if write_a:
            s += "a"
            left_a -= 1
        else:
            s += "b"
            left_b -= 1
    return s


def main():
    rounds = 100
    pairs = [(a, b) for a in range(101) for b in range(101)
             if a + b > 0 and a <= 2 * b + 2 and b <= 2 * a + 2]
    n = len(pairs)
    letters = 0
    check = 0
    for r in range(rounds):
        for i in range(n):
            a, b = pairs[(r + i) % n]
            s = str_without_3a3b(a, b)
            length = len(s)
            middle = 1 if s[length // 2] == "a" else 2
            letters += length
            check = (check * 31 + length * 3 + middle) % 1000000007
    print(f"{rounds} rounds over {n} pairs up to 100: {letters} letters, checksum {check}")


main()
