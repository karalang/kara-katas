# Benchmark for #528: Python mirror of the ★ arm (prefix sums and a
# binary search); see random_pick_with_weight.kara. The same seeded
# generator, so the same picks.


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


def main():
    seed = 528
    lists = []
    for _ in range(20):
        w = []
        for _ in range(10000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            high = seed // 65536
            seed = (seed * 1103515245 + 12345) % 2147483648
            w.append(1 + (high * 32768 + seed // 65536) % 100000)
        lists.append(w)
    total = 0
    checksum = 0
    for round_ in range(50):
        for l in range(len(lists)):
            solution = Solution(lists[l], round_ * 20 + l)
            for _ in range(10000):
                i = solution.pick_index()
                total += i
                checksum = (checksum * 31 + i) % 1000000007
    print(f"20 lists of 10000, 50 rounds of 10000 picks: total {total}, checksum {checksum}")


main()
