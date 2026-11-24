# LeetCode #1312: Minimum Insertion Steps to Make a String Palindrome --
# Python mirror of the ★ arm: the interval table kept in one row.


def min_insertions(s):
    b = s.encode()
    n = len(b)
    row = [0] * n
    for i in range(n - 1, -1, -1):
        inside = 0
        for j in range(i + 1, n):
            keep = row[j]
            row[j] = inside if b[i] == b[j] else 1 + min(keep, row[j - 1])
            inside = keep
    return row[n - 1]


seed = 1312


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    asks = ["zzazz", "mbadm", "leetcode", "a", "ab", "abcd", "racecr"]
    print(" ".join(str(min_insertions(s)) for s in asks))
    letters = "abcdefghijklmnopqrstuvwxyz"
    total = 0
    check = 0
    for t in range(600):
        n = 1 + next_random() % 500
        k = 2 if t % 3 == 0 else 4 if t % 3 == 1 else 26
        chars = [letters[next_random() % k] for _ in range(n)]
        if t % 2 == 0:
            for i in range(n // 2):
                chars[n - 1 - i] = chars[i]
            cuts = next_random() % 21
            for _ in range(cuts):
                if len(chars) > 1:
                    del chars[next_random() % len(chars)]
        got = min_insertions("".join(chars))
        total += got
        check = (check * 31 + got) % 1000000007
    print(f"600 random strings: insertions total {total}, checksum {check}")


main()
