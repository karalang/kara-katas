# LeetCode #528: Random Pick with Weight -- Python mirror of the ★ arm
# (prefix sums and a binary search); see random_pick_with_weight.kara.
# The same seeded generator, so the same picks; same harness, same
# output.
import math


class Draw:
    def __init__(self, seed):
        self.seed = seed

    def step(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536

    def below(self, n):
        limit = 1073741824 // n * n
        while True:
            high = self.step()
            low = self.step()
            r = high * 32768 + low
            if r < limit:
                return r % n


class Solution:
    def __init__(self, w, seed):
        self.ends = []
        total = 0
        for x in w:
            total += x
            self.ends.append(total)
        self.draw = Draw(seed)

    def pick_index(self):
        r = self.draw.below(self.ends[-1])
        low, high = 0, len(self.ends) - 1
        while low < high:
            mid = (low + high) // 2
            if self.ends[mid] > r:
                high = mid
            else:
                low = mid + 1
        return low


def fair(counts, w, picks):
    total = sum(w)
    for i in range(len(counts)):
        p = w[i] / total
        mean = picks * p
        sd = math.sqrt(picks * p * (1.0 - p))
        off = counts[i] - mean
        if off > 5.0 * sd + 1.0 or off < -5.0 * sd - 1.0:
            return False
    return True


def fmt(xs):
    return "[" + ", ".join(map(str, xs)) + "]"


def b(x):
    return "true" if x else "false"


def picks(w, seed, count):
    solution = Solution(w, seed)
    return [solution.pick_index() for _ in range(count)]


def main():
    print(f"[1]: {fmt(picks([1], 1, 5))}")
    print(f"[1, 3]: {fmt(picks([1, 3], 2, 12))}")
    print(f"[1, 1, 1, 1, 100]: {fmt(picks([1, 1, 1, 1, 100], 3, 12))}")
    print(f"[100, 1, 1]: {fmt(picks([100, 1, 1], 4, 12))}")
    print(f"[5; 6]: {fmt(picks([5] * 6, 5, 12))}")
    w = [1, 2, 3, 4]
    solution = Solution(w, 6)
    counts = [0] * 4
    for _ in range(100000):
        counts[solution.pick_index()] += 1
    print(f"[1, 2, 3, 4], 100000 picks: {fmt(counts)}, fair {b(fair(counts, w, 100000))}")
    seed = 528
    checksum = 0
    in_range = True
    for c in range(300):
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = 1 + seed // 65536 % 50
        w = []
        for _ in range(n):
            seed = (seed * 1103515245 + 12345) % 2147483648
            w.append(1 + seed // 65536 % 100)
        solution = Solution(w, 1000 + c)
        for _ in range(200):
            i = solution.pick_index()
            if i < 0 or i >= n:
                in_range = False
            checksum = (checksum * 31 + i) % 1000000007
    print(f"300 random lists, 200 picks each: in range {b(in_range)}, checksum {checksum}")
    w = []
    for _ in range(10000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        high = seed // 65536
        seed = (seed * 1103515245 + 12345) % 2147483648
        w.append(1 + (high * 32768 + seed // 65536) % 100000)
    band_weights = [0] * 10
    for i in range(10000):
        band_weights[i // 1000] += w[i]
    solution = Solution(w, 9)
    bands = [0] * 10
    checksum = 0
    for _ in range(10000):
        i = solution.pick_index()
        bands[i // 1000] += 1
        checksum = (checksum * 31 + i) % 1000000007
    print(f"10000 weights, 10000 picks: bands {fmt(bands)}, fair {b(fair(bands, band_weights, 10000))}, checksum {checksum}")


main()
