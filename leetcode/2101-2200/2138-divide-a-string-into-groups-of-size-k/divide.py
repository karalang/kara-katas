# LeetCode #2138: Divide a String Into Groups of Size k -- the Python
# mirror of divide.kara's ★ arm.


def divide_string(s, k, fill):
    n = len(s)
    groups = []
    start = 0
    while start < n:
        group = s[start:min(start + k, n)]
        while len(group) < k:
            group += fill
        groups.append(group)
        start += k
    return groups


seed = 2138


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letters(n, kinds):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    s = ""
    for _ in range(n):
        at = next_random() % kinds
        s += alphabet[at]
    return s


def fmt(groups):
    return "[" + ", ".join(groups) + "]"


def show(s, k, fill):
    print(f'"{s}" {k} {fill} -> {fmt(divide_string(s, k, fill))}')


def main():
    show("abcdefghi", 3, "x")
    show("abcdefghij", 3, "x")
    show("abc", 1, "q")
    show("ab", 5, "z")
    show("kara", 4, "y")
    show("aabba", 2, "a")
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % 20 + 1
        s = letters(n, [2, 5, 26][rnd % 3])
        k = next_random() % 8 + 1
        fill = letters(1, 26)[0]
        groups = divide_string(s, k, fill)
        total += len(groups)
        for g in groups:
            for b in g.encode():
                check = (check * 131 + b) % 1000000007
            check = (check * 131 + 1) % 1000000007
    print(f"2000 strings: {total} groups, checksum {check}")
    s = letters(100, 26)
    ones = divide_string(s, 1, "x")
    sevens = divide_string(s, 7, "x")
    whole = divide_string(s, 100, "x")
    print(f"100 letters: {len(ones)} groups of 1, {len(sevens)} of 7 ending {sevens[-1]}, {len(whole)} of 100")


main()
