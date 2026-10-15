# LeetCode #664: Strange Printer -- intervals, by their last letter.
# Mirrors the ★ arm (strange_printer.kara) and its test harness.


def strange_printer(s):
    b = s.encode()
    n = len(b)
    if n == 0:
        return 0
    turns = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        turns[i][i] = 1
        for j in range(i + 1, n):
            best = turns[i][j - 1] + 1
            for k in range(i, j):
                if b[k] == b[j]:
                    between = turns[k + 1][j - 1] if k + 1 <= j - 1 else 0
                    best = min(best, turns[i][k] + between)
            turns[i][j] = best
    return turns[0][n - 1]


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_text(n, letters, rng):
    return "".join(chr(97 + rng.next() % letters) for _ in range(n))


def show(s):
    if len(s) <= 30:
        print(f'"{s}": {strange_printer(s)}')
    else:
        print(f'"{s[:12]}..." ({len(s)} letters): {strange_printer(s)}')


def main():
    for s in ["aaabbb", "aba", "z", "abcba", "abab", "tbgtgb", "abcabc"]:
        show(s)
    same = "q" * 100
    pairs = "".join("a" if i % 2 == 0 else "b" for i in range(100))
    alphabet = "".join(chr(97 + i % 26) for i in range(100))
    mountain = ""
    for i in range(100):
        up = i % 50
        at = up if up < 25 else 49 - up
        mountain += chr(97 + at)
    for s in [same, pairs, alphabet, mountain]:
        show(s)
    rng = Rng(664)
    total = 0
    most = 0
    for _ in range(300):
        n = 1 + rng.next() % 20
        letters = 2 + rng.next() % 4
        t = strange_printer(random_text(n, letters, rng))
        most = max(most, t)
        total = (total * 31 + t) % 1000000007
    print(f"300 random texts: most {most} turns, checksum {total}")
    show(random_text(100, 3, rng))
    show(random_text(100, 26, rng))


main()
