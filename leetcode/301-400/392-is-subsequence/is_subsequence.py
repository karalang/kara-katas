# LeetCode #392: Is Subsequence -- Python mirror of is_subsequence.kara.


def is_subsequence(s, t):
    a = s.encode()
    i = 0
    for b in t.encode():
        if i < len(a) and a[i] == b:
            i += 1
    return i == len(a)


seed = 392


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(s, t):
    r = "true" if is_subsequence(s, t) else "false"
    print(f's = "{s}", t = "{t}": {r}')


def main():
    show("abc", "ahbgdc")
    show("axc", "ahbgdc")
    show("", "")
    show("", "abc")
    show("a", "")
    show("abc", "abc")
    show("aaa", "aa")
    show("aa", "baba")
    show("cba", "abc")
    show("ace", "abcde")
    yes = 0
    checksum = 0
    for _ in range(3000):
        t = "".join(chr(step() % 3 + 97) for _ in range(step() % 41))
        s = "".join(chr(step() % 3 + 97) for _ in range(step() % 16))
        r = is_subsequence(s, t)
        if r:
            yes += 1
        checksum = (checksum * 3 + (1 if r else 2)) % 1000000007
    print(f"3000 random pairs: {yes} subsequences, checksum {checksum}")


main()
