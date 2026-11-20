# LeetCode #1208: Get Equal Substrings Within Budget -- the ★ arm in
# Python: a sliding window over the costs |s[i] - t[i]|, its left end
# stepping on while the window's cost is over the budget, and the longest
# window kept.


def equal_substring(s, t, max_cost):
    a, b = s.encode(), t.encode()
    best = cost = left = 0
    for right in range(len(a)):
        cost += abs(a[right] - b[right])
        while cost > max_cost:
            cost -= abs(a[left] - b[left])
            left += 1
        best = max(best, right - left + 1)
    return best


# ---- test harness ---------------------------------------------------------

seed = 1208


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, letters):
    return "".join(chr(ord("a") + next_random() % letters) for _ in range(n))


def main():
    cases = [
        ("abcd", "bcdf", 3),
        ("abcd", "cdef", 3),
        ("abcd", "acde", 0),
        ("a", "z", 25),
        ("a", "z", 24),
        ("krrgw", "zjxss", 19),
        ("pxezla", "loewbi", 25),
        ("abc", "abc", 0),
        ("zzzz", "aaaa", 100),
    ]
    for s, t, c in cases:
        print(f"{s} {t} {c}: {equal_substring(s, t, c)}")
    total = check = 0
    for _ in range(1000):
        n = next_random() % 12 + 1
        letters = [2, 5, 26][next_random() % 3]
        s = random_text(n, letters)
        t = random_text(n, letters)
        c = next_random() % 40
        answer = equal_substring(s, t, c)
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"1000 small cases: total {total}, checksum {check}")
    s = random_text(100000, 26)
    t = random_text(100000, 26)
    for c in [0, 1000, 1000000]:
        print(f"100000 random letters, budget {c}: {equal_substring(s, t, c)}")
    flat = random_text(100000, 2)
    print(f"100000 of a and b against themselves, budget 0: {equal_substring(flat, flat, 0)}")


main()
