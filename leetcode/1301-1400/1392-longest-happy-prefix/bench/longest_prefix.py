# LeetCode #1392 bench, Python mirror of the ★ arm.


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


seed = 1392


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    n = 100000
    block = b"abacaba"
    letters = bytearray(block[i % 7] for i in range(n))
    check = 0
    for _ in range(2000):
        seed = (seed + check) % 2147483648
        at = next_random() % n
        was = letters[at]
        letters[at] = 97 + next_random() % 3
        s = letters.decode()
        got = longest_prefix(s)
        letters[at] = was
        check = (check * 131 + len(got) * 7 + at) % 1000000007
    print(f"2000 rounds over 10^5 letters: checksum {check}")


main()
