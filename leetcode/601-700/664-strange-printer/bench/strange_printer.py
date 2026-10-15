# Benchmark for #664: intervals, by their last letter, as the Kara ★ arm.


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


def main():
    rng = Rng(664)
    texts = []
    for t in range(64):
        letters = 2 + t % 25
        texts.append("".join(chr(97 + rng.next() % letters) for _ in range(100)))
    rounds = 2000
    s = 0
    for r in range(rounds):
        t = strange_printer(texts[r % 64])
        s = (s * 31 + t + r) % 1000000007
    print(f"64 texts of 100 letters, {rounds} rounds: checksum {s}")


main()
