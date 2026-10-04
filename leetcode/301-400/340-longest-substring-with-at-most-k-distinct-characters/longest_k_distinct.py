# LeetCode #340: Longest Substring with At Most K Distinct Characters.
# Mirrors longest_k_distinct.kara (the ★ arm) and prints the same lines.


def longest_k_distinct(s, k):
    counts = {}
    left = 0
    best = 0
    for right, c in enumerate(s):
        counts[c] = counts.get(c, 0) + 1
        while len(counts) > k:
            d = s[left]
            counts[d] -= 1
            if counts[d] == 0:
                del counts[d]
            left += 1
        best = max(best, right - left + 1)
    return best


LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def gen_text(seed, n, alpha):
    state = seed
    out = []
    for _ in range(n):
        state = (state * 1103515245 + 12345) % 2147483648
        out.append(LETTERS[(state >> 8) % alpha])
    return "".join(out)


def show(s, k):
    print(f'"{s}" k={k} -> {longest_k_distinct(s, k)}')


def summary(seed, n, alpha, k):
    s = gen_text(seed, n, alpha)
    print(f"seed {seed}, {n} letters from {alpha}, k={k}: {longest_k_distinct(s, k)}")


show("eceba", 2)
show("aa", 1)
show("", 3)
show("abc", 0)
show("a", 5)
show("abaccc", 2)
show("aabbcc", 1)
show("abcadcacacaca", 3)
summary(1, 20, 3, 2)
summary(7, 1000, 5, 3)
summary(42, 50000, 26, 10)
summary(2026, 50000, 4, 3)
summary(99, 50000, 52, 40)
