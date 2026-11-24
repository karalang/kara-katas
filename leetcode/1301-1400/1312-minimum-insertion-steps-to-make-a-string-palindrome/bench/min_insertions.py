# LeetCode #1312 bench, Python: the ★ arm (the interval costs kept in one
# row) on the same 20 strings and 50 passes.


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
    letters = "abcdefghijklmnopqrstuvwxyz"
    n = 500
    strings = []
    for g in range(20):
        k = 2 if g % 3 == 0 else 4 if g % 3 == 1 else 26
        strings.append([letters[next_random() % k] for _ in range(n)])
    check = 0
    for p in range(50):
        for g in range(20):
            k = 2 if g % 3 == 0 else 4 if g % 3 == 1 else 26
            strings[g][check % n] = letters[(check // 7) % k]
            got = min_insertions("".join(strings[g]))
            check = (check * 31 + got + p) % 1000000007
    print(f"50 passes over 20 strings of 500: checksum {check}")


main()
