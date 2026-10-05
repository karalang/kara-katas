"""Benchmark workload for LeetCode #342 — Python mirror of power_of_four.kara."""

LEN = 500000
PUNCHES = 100
MODULUS = 1073741789
I32_MIN = -2147483648


def is_power_of_four(n):
    return n > 0 and (n & (n - 1)) == 0 and (n & 0x55555555) != 0


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def two_to(k):
    p = 1
    for _ in range(k):
        p *= 2
    return p


def value(rng):
    kind = rng.next() % 3
    if kind == 0:
        return two_to(2 * (rng.next() % 16))
    if kind == 1:
        r = rng.next() % 3
        if r == 0:
            return two_to(2 * (rng.next() % 15) + 1)
        p = two_to(2 * (rng.next() % 16))
        if r == 1:
            return p + 1
        return p - 1
    hi = rng.next() * 32768
    hi += rng.next()
    return hi * 4 + rng.next() % 4 + I32_MIN


def main():
    rng = Rng(342)
    a = [value(rng) for _ in range(LEN)]
    sink = 0
    for _ in range(PUNCHES):
        x = rng.next()
        y = rng.next()
        pos = (x * 32768 + y) % LEN
        a[pos] = value(rng)
        count = 0
        total = 0
        for v in a:
            if is_power_of_four(v):
                count += 1
                total += v
        sink = (sink * 31 + count + total % MODULUS) % MODULUS
    print(f"sink {sink}")


main()
