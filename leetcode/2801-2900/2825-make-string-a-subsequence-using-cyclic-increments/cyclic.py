# LeetCode #2825: Make String a Subsequence Using Cyclic Increments --
# the Python mirror of the ★ arm: two pointers over the bytes, each
# letter of str1 as it is or once incremented taking str2's next letter.


def can_make_subsequence(str1, str2):
    a, b = str1.encode(), str2.encode()
    j = 0
    for c in a:
        if j == len(b):
            break
        nxt = ord("a") if c == ord("z") else c + 1
        if c == b[j] or nxt == b[j]:
            j += 1
    return j == len(b)


# ---- the harness: the same in every arm --------------------------------

seed = 2825


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letters(n, start, width):
    return "".join(chr((start + next_random() % width) % 26 + 97) for _ in range(n))


def show(b):
    return "true" if b else "false"


def main():
    print(show(can_make_subsequence("abc", "ad")))
    print(show(can_make_subsequence("zc", "ad")))
    print(show(can_make_subsequence("ab", "d")))
    print(show(can_make_subsequence("ab", "abc")))
    print(show(can_make_subsequence("z", "a")))
    print(show(can_make_subsequence("z" * 100000, "a" * 100000)))
    print(show(can_make_subsequence("a" * 99999, "b" * 100000)))
    yes = 0
    check = 0
    for _ in range(3000):
        s1 = letters(next_random() % 10 + 1, 24, 4)
        s2 = letters(next_random() % 5 + 1, 24, 4)
        a = can_make_subsequence(s1, s2)
        yes += a
        check = (check * 31 + (1 if a else 0)) % 1000000007
    print(f"3000 short pairs: {yes} true, checksum {check}")
    yes = 0
    check = 0
    for _ in range(50):
        s1 = letters(10000, 23, 6)
        s2 = letters(next_random() % 5000 + 1, 23, 6)
        a = can_make_subsequence(s1, s2)
        yes += a
        check = (check * 31 + (1 if a else 0) + len(s2)) % 1000000007
    print(f"50 long pairs: {yes} true, checksum {check}")


main()
