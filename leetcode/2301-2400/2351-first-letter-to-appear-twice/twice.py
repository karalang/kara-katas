# LeetCode #2351: First Letter to Appear Twice -- the Python mirror of the
# ★ arm: a table of 26 letters seen, and the first letter met when it is
# already in the table.


def repeated_character(s):
    seen = [False] * 26
    for c in s:
        i = ord(c) - 97
        if seen[i]:
            return c
        seen[i] = True
    return " "


SEED = [2351]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # LeetCode's two examples; then two letters, the alphabet then its
    # first letter, the alphabet backwards then m, and 100 letters
    print(repeated_character("abccbaacz"))
    print(repeated_character("abcdd"))
    print(repeated_character("aa"))
    print(repeated_character("abcdefghijklmnopqrstuvwxyza"))
    print(repeated_character("zyxwvutsrqponmlkjihgfedcbam"))
    print(repeated_character("".join(chr(97 + (i * 7) % 26) for i in range(100))))
    # 2000 random strings of 2 to 30 letters from the first 2 to 26 of the
    # alphabet; one with no letter twice gets a copy of one of its letters
    check = 0
    counts = [0] * 26
    for _ in range(2000):
        n = 2 + next_random() % 29
        alphabet = 2 + next_random() % 25
        s = "".join(chr(97 + next_random() % alphabet) for _ in range(n))
        if len(set(s)) == len(s):
            s += s[next_random() % len(s)]
        c = repeated_character(s)
        check = (check * 31 + ord(c)) % 1000000007
        counts[ord(c) - 97] += 1
    print(f"2000 strings: checksum {check}, a {counts[0]}, b {counts[1]}, z {counts[25]}")


main()
