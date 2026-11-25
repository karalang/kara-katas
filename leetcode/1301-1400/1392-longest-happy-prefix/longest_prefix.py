# LeetCode #1392: Longest Happy Prefix -- Python mirror of the ★ arm: the
# prefix function over the bytes, the answer the border it gives the
# whole string.


def longest_prefix(s):
    b = s.encode()
    n = len(b)
    border = [0] * n
    k = 0
    for i in range(1, n):
        while k > 0 and b[i] != b[k]:
            k = border[k - 1]
        if b[i] == b[k]:
            k += 1
        border[i] = k
    return s[:border[n - 1]]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# a string of n letters: either a random block of 1 to 8 letters repeated,
# with one letter then changed half the time, or n random letters, from
# the first `letters` of the alphabet
def drawn(n, letters, repeated):
    if repeated:
        block = [chr(97 + next_random() % letters) for _ in range(1 + next_random() % 8)]
        out = [block[i % len(block)] for i in range(n)]
        if next_random() % 2 == 0:
            at = next_random() % n
            out[at] = chr(97 + next_random() % letters)
    else:
        out = [chr(97 + next_random() % letters) for _ in range(n)]
    return "".join(out)


def main():
    global seed
    shown = [longest_prefix(s) for s in ["level", "ababab", "a", "aaaa", "abcab", "abcd"]]
    print(" ".join(f'"{x}"' for x in shown))
    seed = 1392
    big = [
        "a" * 100000,
        "a" * 99999 + "b",
        "abcabca" * 14285 + "abcab",
        drawn(100000, 2, False),
        drawn(100000, 3, True),
    ]
    print("10^5 letters: " + " ".join(str(len(longest_prefix(s))) for s in big))
    check = 0
    total = 0
    for c in range(2000):
        n = 1 + next_random() % 60
        letters = 1 + next_random() % 3
        got = longest_prefix(drawn(n, letters, c % 2 == 0))
        total += len(got)
        for ch in got:
            check = (check * 131 + ord(ch)) % 1000000007
        check = (check * 131 + len(got)) % 1000000007
    print(f"2000 random strings: {total} letters in all, checksum {check}")


main()
