# LeetCode #1186: Maximum Subarray Sum with One Deletion -- mirror of the
# ★ arm (kept / cut bests ending at each element), checked against the
# statement read literally on every random array.
import sys

MIN = -(2 ** 63)


def maximum_sum(arr):
    kept = arr[0]
    cut = MIN
    best = arr[0]
    for x in arr[1:]:
        cut = kept if cut == MIN else max(cut + x, kept)
        kept = max(kept + x, x)
        best = max(best, kept, cut)
    return best


def literal(arr):
    # Every non-empty subarray, kept whole or with one element deleted while
    # one is left.
    best = None
    n = len(arr)
    for i in range(n):
        for j in range(i, n):
            sub = arr[i:j + 1]
            sums = [sum(sub)]
            if len(sub) > 1:
                sums += [sum(sub) - y for y in sub]
            m = max(sums)
            best = m if best is None else max(best, m)
    return best


class Seed:
    def __init__(self, v):
        self.v = v

    def next(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


def values(seed, n, span):
    return [seed.next() % (2 * span + 1) - span for _ in range(n)]


def main():
    print(f"example 1: {maximum_sum([1, -2, 0, 3])}")
    print(f"example 2: {maximum_sum([1, -2, -2, 3])}")
    print(f"example 3: {maximum_sum([-1, -1, -1, -1])}")
    print(f"small 1: {maximum_sum([-7])}")
    print(f"small 2: {maximum_sum([5, -100, 6])}")
    print(f"small 3: {maximum_sum([-3, -9])}")
    print(f"small 4: {maximum_sum([2, -1, -1, 2])}")
    seed = Seed(1182)
    checksum = 0
    for t in range(2000):
        n = 1 + seed.next() % 12
        arr = values(seed, n, 10)
        got = maximum_sum(arr)
        assert got == literal(arr), (arr, got, literal(arr))
        checksum = (checksum * 31 + got + 1000 + t) % 1000000007
    print(f"2000 random arrays: checksum {checksum}")
    big = values(seed, 100000, 10000)
    print(f"100000 values: {maximum_sum(big)}")


main()
