"""Benchmark workload for LeetCode #343 — Python mirror of integer_break.kara."""

LEN = 20000
PUNCHES = 20
MODULUS = 1073741789


def integer_break(n):
    best = [0] * (n + 1)
    for i in range(2, n + 1):
        for j in range(1, i):
            whole = j * (i - j)
            broken = j * best[i - j]
            if whole > best[i]:
                best[i] = whole
            if broken > best[i]:
                best[i] = broken
    return best[n]


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def main():
    rng = Rng(343)
    a = [2 + rng.next() % 57 for _ in range(LEN)]
    sink = 0
    for _ in range(PUNCHES):
        x = rng.next()
        y = rng.next()
        pos = (x * 32768 + y) % LEN
        a[pos] = 2 + rng.next() % 57
        total = 0
        for n in a:
            total = (total + integer_break(n)) % MODULUS
        sink = (sink * 31 + total) % MODULUS
    print(f"sink {sink}")


main()
