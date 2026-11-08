# LeetCode #2028: Find Missing Observations -- a Python mirror of the ★ arm
# (observe.kara): the total the missing rolls need, spread evenly. Same
# output, byte for byte.


def missing_rolls(rolls, mean, n):
    m = len(rolls)
    need = mean * (m + n) - sum(rolls)
    if need < n or need > 6 * n:
        return []
    q, r = need // n, need % n
    return [q + 1 if i < r else q for i in range(n)]


seed = 2028


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def verdict(rolls, mean, n, got):
    need = mean * (len(rolls) + n) - sum(rolls)
    fits = n <= need <= 6 * n
    if not got:
        return "WRONG: none" if fits else "none"
    if len(got) == n and all(1 <= r <= 6 for r in got) and sum(got) == need:
        return f"{n} rolls adding to {sum(got)}"
    return f"WRONG: {show(got)}"


def fold(check, text):
    for b in text.encode():
        check = (check * 31 + b) % 1000000007
    return check


def main():
    examples = [
        ([3, 2, 4, 3], 4, 2),
        ([1, 5, 6], 3, 4),
        ([1, 2, 3, 4], 6, 4),
        ([6, 6], 6, 3),
        ([1], 1, 1),
        ([6, 6, 6], 1, 2),
        ([4, 5, 6, 2, 3, 6, 5, 4, 6, 4, 5, 1, 6, 3, 1, 4, 5, 5, 3, 2, 3, 5, 3, 2, 1, 5, 4, 3, 5, 1, 5], 4, 40),
        ([2], 4, 1),
    ]
    for rolls, mean, n in examples:
        got = missing_rolls(rolls, mean, n)
        print(f"{show(rolls)}, {mean}, {n} -> {verdict(rolls, mean, n, got)}")
    found = 0
    check = 0
    for _ in range(3000):
        m = next_random() % 20 + 1
        rolls = [next_random() % 6 + 1 for _ in range(m)]
        mean = next_random() % 6 + 1
        n = next_random() % 20 + 1
        got = missing_rolls(rolls, mean, n)
        if got:
            found += 1
        check = fold(check, verdict(rolls, mean, n, got))
    print(f"3000 problems of up to 20 rolls: {found} answered, checksum {check}")
    found = 0
    check = 0
    for a in range(5):
        rolls = [next_random() % 6 + 1 for _ in range(100000)]
        mean = [1, 3, 4, 6, 2][a]
        got = missing_rolls(rolls, mean, 100000)
        if got:
            found += 1
        check = fold(check, verdict(rolls, mean, 100000, got))
    print(f"5 problems of 100000 rolls: {found} answered, checksum {check}")


main()
