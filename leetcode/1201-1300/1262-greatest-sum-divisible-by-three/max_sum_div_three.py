# LeetCode #1262: Greatest Sum Divisible by Three -- Python mirror of the ★
# arm (the best sum with each remainder modulo 3, every number added to
# each in turn), with the same harness.


def max_sum_div_three(nums):
    best = [0, -1, -1]
    for x in nums:
        before = best[:]
        for r in range(3):
            if before[r] >= 0:
                s = before[r] + x
                if s > best[s % 3]:
                    best[s % 3] = s
    return best[0]


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_nums(n, top, rng):
    return [rng.next() % top + 1 for _ in range(n)]


def main():
    print(f"{max_sum_div_three([3, 6, 5, 1, 8])} {max_sum_div_three([4])} {max_sum_div_three([1, 2, 3, 4, 4])}")
    rng = Rng(1262)
    total = 0
    check = 0
    for rnd in range(2000):
        if rnd < 1000:
            n, top = rng.next() % 10 + 1, 9
        else:
            n, top = rng.next() % 200 + 1, 10000
        best = max_sum_div_three(random_nums(n, top, rng))
        total += best
        check = (check * 131 + best) % 1000000007
    print(f"2000 random lists: total {total}, checksum {check}")
    all_ = [10000] * 40000
    mixed = random_nums(40000, 10000, rng)
    twos = [2] * 40000
    twos[20000] = 1
    print(f"{max_sum_div_three(all_)} {max_sum_div_three(mixed)} {max_sum_div_three(twos)}")


main()
