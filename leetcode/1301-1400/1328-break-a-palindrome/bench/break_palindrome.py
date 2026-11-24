# LeetCode #1328 bench, Python mirror of the Kāra bench: the ★ arm (the
# letters into a list, the first half searched for a letter that is not an
# a, the answer joined back into a string) on 20 palindromes of 10^5 letters
# built once, in four kinds: all a; a until the last tenth of the half, then
# random letters; a with a rare b; and random letters. Then 800 passes,
# each setting one mirrored pair of every palindrome from the checksum so
# far, answering it and folding two of the answer's letters plus the pass
# into the checksum.


def break_palindrome(palindrome):
    chars = list(palindrome)
    n = len(chars)
    if n == 1:
        return ""
    for i in range(n // 2):
        if chars[i] != "a":
            chars[i] = "a"
            return "".join(chars)
    chars[n - 1] = "b"
    return "".join(chars)


seed = 1328


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 100000
    letters = b"abcdefghijklmnopqrstuvwxyz"
    texts = []
    for t in range(20):
        kind = t % 4
        b = bytearray(b"a" * n)
        for i in range(n // 2):
            if kind == 0:
                c = 97
            elif kind == 1:
                c = 97 if i < n // 2 - n // 20 else letters[next_random() % 26]
            elif kind == 2:
                c = 98 if next_random() % 2000 == 0 else 97
            else:
                c = letters[next_random() % 26]
            b[i] = c
            b[n - 1 - i] = c
        texts.append(b)
    check = 0
    for p in range(800):
        for t in range(20):
            j = check % (n // 2)
            c = 98 if (check // 7) % 4 == 0 else 97
            texts[t][j] = c
            texts[t][n - 1 - j] = c
            got = break_palindrome(bytes(texts[t]).decode()).encode()
            check = (check * 31 + got[j] + got[n - 1] + p) % 1000000007
    print(f"800 passes over 20 palindromes of 10^5: checksum {check}")


main()
