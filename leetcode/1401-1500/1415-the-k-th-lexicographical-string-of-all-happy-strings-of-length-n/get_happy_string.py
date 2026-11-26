# LeetCode #1415, Python mirror of get_happy_string.kara: the first letter
# from (k - 1) / 2^(n - 1), and each letter after it the lower or the
# higher of the two that differ from the one before, by the bits of the
# rest of k - 1.


def get_happy_string(n, k):
    per_first = 1 << (n - 1)
    if k > 3 * per_first:
        return ""
    letters = "abc"
    rest = k - 1
    last = letters[rest // per_first]
    rest %= per_first
    s = [last]
    bit = per_first // 2
    while bit > 0:
        options = [c for c in letters if c != last]
        last = options[1 if rest >= bit else 0]
        if rest >= bit:
            rest -= bit
        s.append(last)
        bit //= 2
    return "".join(s)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def shown(s):
    return s if s else "-"


def main():
    global seed
    print(" ".join(shown(get_happy_string(n, k)) for n, k in [(1, 3), (1, 4), (3, 9), (2, 7), (1, 1), (2, 6), (4, 24)]))
    every = " ".join(shown(get_happy_string(3, k)) for k in range(1, 14))
    print(f"n = 10: {get_happy_string(10, 100)} {get_happy_string(10, 1)} | n = 3: {every}")
    seed = 1415
    check = 0
    empty = 0
    for _ in range(2000):
        n = 1 + next_random() % 10
        k = 1 + next_random() % 100
        s = get_happy_string(n, k)
        if not s:
            empty += 1
        for b in s.encode():
            check = (check * 131 + b) % 1000000007
        check = (check * 131 + 7) % 1000000007
    print(f"2000 random cases: {empty} empty, checksum {check}")


main()
