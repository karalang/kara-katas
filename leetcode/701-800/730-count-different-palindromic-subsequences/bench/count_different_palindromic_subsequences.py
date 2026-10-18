# LeetCode #730: Count Different Palindromic Subsequences -- by
# interval, with the next and previous copy of the end letter.
# Benchmark mirror of the Kara star arm: the count for each interval
# from the ones inside it.

M = 1000000007


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def count_palindromic_subsequences(s):
    n = len(s)
    next_same = [n] * n
    prev_same = [-1] * n
    last = {}
    for i, ch in enumerate(s):
        prev_same[i] = last.get(ch, -1)
        if ch in last:
            next_same[last[ch]] = i
        last[ch] = i
    count = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        count[i][i] = 1
        row, below = count[i], count[i + 1] if i + 1 < n else None
        for j in range(i + 1, n):
            inner = below[j - 1] if i + 1 <= j - 1 else 0
            if s[i] != s[j]:
                v = below[j] + row[j - 1] - inner
            else:
                lo, hi = next_same[i], prev_same[j]
                if lo > hi:
                    v = 2 * inner + 2
                elif lo == hi:
                    v = 2 * inner + 1
                else:
                    twice = count[lo + 1][hi - 1] if lo + 1 <= hi - 1 else 0
                    v = 2 * inner - twice
            row[j] = v % M
    return count[0][n - 1]


def main():
    seed = [730]
    total = 0
    for _ in range(200):
        s = "".join(chr(ord("a") + next_random(seed) % 4) for _ in range(1000))
        total = (total + count_palindromic_subsequences(s)) % M
    print(f"200 strings of 1000 letters: sum {total}")


main()
