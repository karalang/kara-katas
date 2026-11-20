# LeetCode #1208 bench, in Python: the ★ arm (a window over the letters,
# widened one letter a step and shrunk from the left while it costs more
# than the budget) on 16 pairs of strings of 100000 letters drawn once,
# then 10 rounds over the pairs with the budgets 0, 1000, 100000 and
# 1000000, every answer folded into a checksum.

seed = 1208


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def equal_substring(s, t, max_cost):
    a = s.encode()
    b = t.encode()
    best = 0
    cost = 0
    left = 0
    for right in range(len(a)):
        cost += abs(a[right] - b[right])
        while cost > max_cost:
            cost -= abs(a[left] - b[left])
            left += 1
        best = max(best, right - left + 1)
    return best


def main():
    pairs = []
    for _ in range(16):
        s = []
        t = []
        spread = 2
        for i in range(100000):
            if i % 1000 == 0:
                spread = 2 if next_random() % 2 == 0 else 25
            x = next_random() % 26
            y = (x + next_random() % (spread + 1)) % 26
            s.append(chr(97 + x))
            t.append(chr(97 + y))
        pairs.append(("".join(s), "".join(t)))
    budgets = [0, 1000, 100000, 1000000]
    check = 0
    for rnd in range(10):
        for s, t in pairs:
            for c in budgets:
                check = (check * 131 + equal_substring(s, t, c) + rnd) % 1000000007
    print(f"10 rounds over 16 pairs of 100000 letters: checksum {check}")


main()
