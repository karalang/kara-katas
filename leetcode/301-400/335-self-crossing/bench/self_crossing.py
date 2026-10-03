# Benchmark workload for LeetCode #335 — Python mirror of
# self_crossing.kara (same spiral, same punches, same sink).

MOVES = 1000000
PUNCHES = 100
MODULUS = 1073741789


def is_self_crossing(d):
    for i in range(3, len(d)):
        if d[i] >= d[i - 2] and d[i - 1] <= d[i - 3]:
            return True
        if i >= 4 and d[i - 1] == d[i - 3] and d[i] + d[i - 4] >= d[i - 2]:
            return True
        if (
            i >= 5
            and d[i - 2] >= d[i - 4]
            and d[i] + d[i - 4] >= d[i - 2]
            and d[i - 1] <= d[i - 3]
            and d[i - 1] + d[i - 5] >= d[i - 3]
        ):
            return True
    return False


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536

    def wide(self):
        hi = self.next()
        return hi * 32768 + self.next()


def main():
    rng = Rng(335)
    d = []
    for i in range(MOVES):
        two_back = d[i - 2] if i >= 2 else 0
        d.append(two_back + 1 + rng.next() % 3)
    sink = 0
    for p in range(PUNCHES):
        at = 2 + rng.wide() % (MOVES - 2)
        old = d[at]
        if p % 2 == 0:
            d[at] = 1
        answer = 1 if is_self_crossing(d) else 0
        d[at] = old
        sink = (sink * 1000003 + answer * 2000003 + at) % MODULUS
    print(sink)


main()
