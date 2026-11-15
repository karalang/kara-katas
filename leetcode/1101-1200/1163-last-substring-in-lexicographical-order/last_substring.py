# LeetCode #1163: Last Substring in Lexicographical Order -- a Python mirror
# of the ★ arm (two pointers) and its test harness; the output is
# byte-identical to last_substring.kara's.


def last_substring(s):
    b = s.encode()
    n = len(b)
    i, j, k = 0, 1, 0
    while j + k < n:
        if b[i + k] == b[j + k]:
            k += 1
        elif b[i + k] > b[j + k]:
            j = j + k + 1
            k = 0
        else:
            i = max(i + k + 1, j)
            j = i + 1
            k = 0
    return s[i:]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word(length, k):
    return "".join(chr(ord("a") + next_random() % k) for _ in range(length))


def main(solve, big=True):
    global seed
    for c in ["abab", "leetcode", "a", "zzz", "aaab", "abcabcabc", "zazzab", "zyzyzyz", "cbabc"]:
        print(f"{c} -> {solve(c)}")
    seed = 1163
    starts = 0
    check = 0
    for _ in range(2000):
        k = [1, 2, 3, 4, 26][next_random() % 5]
        s = word(1 + next_random() % 30, k)
        t = solve(s)
        starts += len(s) - len(t)
        for ch in t.encode():
            check = (check * 31 + ch) % 1000000007
    print(f"2000 random strings: starts {starts}, checksum {check}")
    n = 400000
    for s in ["z" * n, "ab" * (n // 2), word(n, 3), "a" * (n - 1) + "b"]:
        t = solve(s)
        print(f"{n} letters: starts at {len(s) - len(t)}, {len(t)} long")


if __name__ == "__main__":
    main(last_substring)
