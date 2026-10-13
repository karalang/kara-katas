# Benchmark for #497: Python mirror of the ★ arm (prefix sums); see
# random_point_rects.kara.


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


seed = 497


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 500 sets of 100 rectangles (the problem's most) of 1 to 2,001 on
    # a side, spread across the whole range, built once. Then each set
    # gets a fresh solution and 10,000 picks (the problem's most).
    sets = 500
    all_sets = []
    for _ in range(sets):
        rects = []
        for i in range(100):
            x = -1000000000 + i * 19000000 + next_random() % 1000
            y = next_random() % 30000 * 60000 - 999000000
            w = 1 + next_random() % 2001
            h = 1 + next_random() % 2001
            rects.append([x, y, x + w - 1, y + h - 1])
        all_sets.append(rects)
    total = 0
    checksum = 0
    for k in range(sets):
        solution = Solution([list(r) for r in all_sets[k]], k)
        for _ in range(10000):
            # Moved up by 10^9 so that every coordinate is at least 0.
            p = solution.pick()
            x = p[0] + 1000000000
            y = p[1] + 1000000000
            total += x % 1000 + y % 1000
            checksum = (checksum * 31 + x + 2 * y) % 1000000007
    print(f"{sets} sets of 100, 10000 picks each: sum of last three digits {total}, checksum {checksum}")


main()
