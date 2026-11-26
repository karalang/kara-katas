# Mirror of longest_diverse_string.kara: the letter with the most left that
# would not make three in a row goes next.


def longest_diverse_string(a, b, c):
    left = [(a, "a"), (b, "b"), (c, "c")]
    out = ""
    while True:
        left.sort(key=lambda x: -x[0])
        placed = False
        for i in range(3):
            n, ch = left[i]
            if n == 0:
                break
            if out.endswith(ch + ch):
                continue
            out += ch
            left[i] = (n - 1, ch)
            placed = True
            break
        if not placed:
            return out


def happy(s, a, b, c):
    no_three = all(not (s[i] == s[i - 1] == s[i - 2]) for i in range(2, len(s)))
    return no_three and set(s) <= set("abc") and s.count("a") <= a and s.count("b") <= b and s.count("c") <= c


unhappy = 0


def tried(a, b, c):
    global unhappy
    s = longest_diverse_string(a, b, c)
    if not happy(s, a, b, c):
        unhappy += 1
    return len(s)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    print(" ".join(str(tried(*t)) for t in [(1, 1, 7), (7, 1, 0), (2, 2, 1), (0, 0, 1), (4, 0, 0), (3, 3, 3)]))
    corners = [(100, 100, 100), (100, 0, 0), (0, 100, 0), (1, 100, 1), (100, 10, 0), (0, 49, 100)]
    print("corners: " + " ".join(str(tried(*t)) for t in corners))
    total = 0
    check = 0
    for a in range(13):
        for b in range(13):
            for c in range(13):
                if a + b + c > 0:
                    n = tried(a, b, c)
                    total += n
                    check = (check * 131 + n) % 1000000007
    seed = 1405
    for _ in range(2000):
        a = next_random() % 101
        b = next_random() % 101
        c = 1 + next_random() % 100
        n = tried(a, b, c)
        total += n
        check = (check * 131 + n) % 1000000007
    print(f"4196 cases: {total} letters in all, checksum {check}, {unhappy} not happy")


main()
