# LeetCode #2351: First Letter to Appear Twice -- the bench, the ★ arm in
# Python: a table of 26 marks, one per letter, the first letter already
# marked is the answer.


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
    # string t is the first 2 to 26 letters of the alphabet shuffled, then
    # one of them again
    strings = []
    for _ in range(100000):
        k = 2 + next_random() % 25
        letters = [chr(97 + i) for i in range(k)]
        for i in range(k - 1, 0, -1):
            j = next_random() % (i + 1)
            letters[i], letters[j] = letters[j], letters[i]
        letters.append(letters[next_random() % k])
        strings.append("".join(letters))
    check = 0
    for p in range(50):
        for s in strings:
            check = (check * 31 + ord(repeated_character(s)) + p) % 1000000007
    print(f"50 passes over 10^5 strings: checksum {check}")


main()
