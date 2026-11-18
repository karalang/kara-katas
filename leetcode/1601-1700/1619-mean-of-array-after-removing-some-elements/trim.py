"""LeetCode #1619: Mean of Array After Removing Some Elements -- Python
mirror of the ★ arm (trim.kara): sort, then the middle 90%."""
import math


def trim_mean(arr):
    s = sorted(arr)
    k = len(s) // 20
    kept = s[k:len(s) - k]
    return sum(kept) / len(kept)


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536

    def wide(self, bound):
        return (self.next() * 32768 + self.next()) % bound


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def kround(x):
    # Kāra's f64.round: half away from zero
    return math.floor(x + 0.5) if x >= 0 else math.ceil(x - 0.5)


def batch(count, most, top, rng):
    check = 0
    total = 0.0
    values = 0
    for _ in range(count):
        n = (rng.next() % (most // 20) + 1) * 20
        arr = [rng.wide(top + 1) for _ in range(n)]
        mean = trim_mean(arr)
        total += mean
        check = mix(check, int(kround(mean * 100000.0)))
        values += n
    print(f"{count} arrays of up to {most} values below {top + 1}: {values} values, means sum to {total:.5f}, checksum {check}")


def main():
    print(f"{trim_mean([1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3]):.5f}")
    print(f"{trim_mean([6, 2, 7, 5, 1, 2, 0, 3, 10, 2, 5, 0, 5, 5, 0, 8, 7, 6, 8, 0]):.5f}")
    print(f"{trim_mean([6, 0, 7, 0, 7, 5, 7, 8, 3, 4, 0, 7, 8, 1, 6, 8, 1, 1, 2, 4, 8, 1, 9, 5, 4, 3, 8, 5, 10, 8, 6, 6, 1, 0, 6, 10, 8, 2, 3, 4]):.5f}")
    rng = Rng(1619)
    batch(3000, 40, 10, rng)
    batch(300, 1000, 100000, rng)
    batch(30, 1000, 5, rng)


main()
