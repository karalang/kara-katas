"""Benchmark workload for LeetCode #326 — Python mirror of power_of_three.kara."""

LEN = 300000
PUNCHES = 40
MODULUS = 1073741789
I32_MIN = -2147483648


def is_power_of_three(n):
    if n <= 0:
        return False
    m = n
    while m % 3 == 0:
        m //= 3
    return m == 1


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def power(k):
    p = 1
    for _ in range(k):
        p *= 3
    return p


def value(r):
    kind = r.next() % 3
    if kind == 0:
        return power(r.next() % 20)
    if kind == 1:
        p = power(r.next() % 20)
        if r.next() % 2 == 0:
            return p + 1
        return p - 1
    hi = r.next() * 32768 + r.next()
    return hi * 4 + r.next() % 4 + I32_MIN


def main():
    r = Rng(326)
    a = [value(r) for _ in range(LEN)]
    sink = 0
    for _ in range(PUNCHES):
        pos = (r.next() * 32768 + r.next()) % LEN
        a[pos] = value(r)
        count = 0
        total = 0
        for x in a:
            if is_power_of_three(x):
                count += 1
                total += x
        sink = (sink * 31 + count + total % MODULUS) % MODULUS
    print(f"sink {sink}")


main()
