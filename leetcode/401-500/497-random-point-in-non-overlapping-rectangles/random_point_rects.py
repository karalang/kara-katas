# LeetCode #497: Random Point in Non-overlapping Rectangles -- prefix sums.
# Mirrors random_point_rects.kara (the ★ arm) and draws the same points;
# output is byte-identical.
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
    def __init__(self, rects, seed):
        self.rects = rects
        self.ends = []
        total = 0
        for r in rects:
            total += (r[2] - r[0] + 1) * (r[3] - r[1] + 1)
            self.ends.append(total)
        self.draw = Draw(seed)

    def pick(self):
        k = self.draw.below(self.ends[-1])
        low = 0
        high = len(self.ends) - 1
        while low < high:
            mid = (low + high) // 2
            if self.ends[mid] > k:
                high = mid
            else:
                low = mid + 1
        r = self.rects[low]
        before = 0 if low == 0 else self.ends[low - 1]
        at = k - before
        width = r[2] - r[0] + 1
        return [r[0] + at % width, r[1] + at // width]


def number_of(rects, p):
    before = 0
    for r in rects:
        if r[0] <= p[0] <= r[2] and r[1] <= p[1] <= r[3]:
            return before + (p[1] - r[1]) * (r[2] - r[0] + 1) + p[0] - r[0]
        before += (r[2] - r[0] + 1) * (r[3] - r[1] + 1)
    return -1


def fair(counts, weights, total, n, sds):
    for i in range(len(counts)):
        p = weights[i] / total
        expect = n * p
        sd = math.sqrt(n * p * (1.0 - p))
        if abs(counts[i] - expect) > sds * sd + 0.000001:
            return False
    return True


def b(v):
    return "true" if v else "false"


def check(name, rects, n, seed):
    total = 0
    for r in rects:
        total += (r[2] - r[0] + 1) * (r[3] - r[1] + 1)
    solution = Solution([list(r) for r in rects], seed)
    counts = [0] * total
    inside = True
    for _ in range(n):
        p = solution.pick()
        k = number_of(rects, p)
        if len(p) != 2 or k < 0:
            inside = False
        else:
            counts[k] += 1
    even = inside and fair(counts, [1] * total, total, n, 5.0)
    print(f"{name}: {total} points, {n} picks, all covered {b(inside)}, each point its share {b(even)}")


seed = 497


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check("example", [[-2, -2, 1, 1], [2, 2, 4, 6]], 31000, 1)
    check("one point", [[7, -3, 7, -3]], 100, 2)
    check("a column", [[5, 1, 5, 9]], 9000, 3)
    check("a row and a column", [[0, 0, 9, 0], [20, 0, 20, 9]], 20000, 4)
    check("squares 1 to 16", [[0, 0, 0, 0], [10, 0, 11, 1], [20, 0, 22, 2], [30, 0, 33, 3]], 30000, 5)
    check("far corners", [[-1000000000, -1000000000, -999999999, -999999999], [999999998, 999999998, 1000000000, 1000000000]], 13000, 6)
    rects = []
    for i in range(100):
        x = -1000000000 + i * 19000000
        y = 999997999 - i * 17000000
        rects.append([x, y, x + 2000, y + 2000])
    solution = Solution([list(r) for r in rects], 7)
    n = 40000
    by_rect = [0] * 100
    by_column = [0] * 20
    by_row = [0] * 20
    inside = True
    for _ in range(n):
        p = solution.pick()
        k = number_of(rects, p)
        if len(p) != 2 or k < 0:
            inside = False
        else:
            r = k // 4004001
            by_rect[r] += 1
            by_column[min((p[0] - rects[r][0]) // 100, 19)] += 1
            by_row[min((p[1] - rects[r][1]) // 100, 19)] += 1
    band = [100] * 19 + [101]
    print(f"largest: 400400100 points, {n} picks, all covered {b(inside)}, each rectangle its share {b(fair(by_rect, [1] * 100, 100, n, 5.0))}, columns even {b(fair(by_column, band, 2001, n, 5.0))}, rows even {b(fair(by_row, band, 2001, n, 5.0))}")
    some = []
    for i in range(10):
        x = i * 100 + next_random() % 50
        y = next_random() % 1000 - 500
        some.append([x, y, x + next_random() % 40, y + next_random() % 40])
    a = Solution([list(r) for r in some], 11)
    bb = Solution([list(r) for r in some], 11)
    c = Solution([list(r) for r in some], 12)
    same = True
    differ = False
    for _ in range(1000):
        pa = a.pick()
        if bb.pick() != pa:
            same = False
        if c.pick() != pa:
            differ = True
    print(f"one seed twice the same {b(same)}, another seed other picks {b(differ)}")


main()
