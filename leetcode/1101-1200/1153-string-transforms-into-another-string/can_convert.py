# LeetCode #1153 -- mirrors can_convert.kara (the ★ arm): each letter of
# str1 must go to one letter of str2, and unless the strings are equal,
# str2 must leave some letter unused.


def can_convert(str1, str2):
    if str1 == str2:
        return True
    to = [-1] * 26
    used = [False] * 26
    letters = 0
    for p, q in zip(str1, str2):
        x, y = ord(p) - 97, ord(q) - 97
        if to[x] == -1:
            to[x] = y
        elif to[x] != y:
            return False
        if not used[y]:
            used[y] = True
            letters += 1
    return letters < 26


SEED = [0]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def show(str1, str2):
    print(f"{str1} {str2}  ->  {'true' if can_convert(str1, str2) else 'false'}")


def pair(n, k, m, noise):
    to = [next_random() % m for _ in range(k)]
    a, b = [], []
    for _ in range(n):
        x = next_random() % k
        a.append(97 + x)
        b.append(97 + to[x])
    if next_random() % 8 < noise:
        at = next_random() % n
        b[at] = 97 + next_random() % 26
    return bytes(a).decode(), bytes(b).decode()


def main():
    show("aabcc", "ccdee")
    show("leetcode", "codeleet")
    show("ab", "ba")
    show("aa", "ab")
    show("abc", "abc")
    abc = "abcdefghijklmnopqrstuvwxyz"
    show(abc, abc)
    show(abc, abc[1:] + "a")
    show(abc[:25], abc[1:25] + "a")
    show(abc, "b" + abc[1:])
    show(abc + "a", abc[1:] + "ab")

    SEED[0] = 1153
    yes = 0
    check = 0
    for i in range(2000):
        n = 1 + next_random() % 60
        k = 1 + next_random() % 26
        m = 1 + next_random() % 26
        a, b = pair(n, k, m, i % 8)
        ok = can_convert(a, b)
        if ok:
            yes += 1
        check = (check * 31 + (2 if ok else 1) + n) % 1000000007
    print(f"2000 random pairs: {yes} convertible, checksum {check}")

    tf = lambda v: "true" if v else "false"
    alls = "".join(chr(97 + i % 26) for i in range(10000))
    rot = "".join(chr(97 + (i + 1) % 26) for i in range(10000))
    free = "".join(chr(97 + (i + 1) % 26 % 25) for i in range(10000))
    print(f"26 letters in turn, sent one on: {tf(can_convert(alls, rot))}")
    print(f"26 letters in turn, sent one on, z and y onto a: {tf(can_convert(alls, free))}")
    a, b = pair(10000, 26, 25, 0)
    print(f"random over 26 sent onto 25: {tf(can_convert(a, b))}")
    at = next(i for i in range(1, 10000) if a[i] == a[0])
    bl = list(b)
    bl[at] = "b" if bl[at] == "a" else "a"
    print(f"the same with one place broken: {tf(can_convert(a, ''.join(bl)))}")


main()
