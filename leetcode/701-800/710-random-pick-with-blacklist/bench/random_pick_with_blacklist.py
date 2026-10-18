# LeetCode #710: Random Pick with Blacklist -- the r-th allowed number,
# by binary search.
# Benchmark mirror of the Kara rank arm: sort the blacklist; the r-th
# allowed number is r + i, i the first index with more than r allowed
# numbers below its blacklisted number.


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_below(seed, bound):
    hi = next_random(seed)
    lo = next_random(seed)
    return (hi * 32768 + lo) % bound


class Solution:
    def __init__(self, n, blacklist, seed):
        self.black = sorted(blacklist)
        self.bound = n - len(self.black)
        self.seed = [seed]

    def pick_from(self, r):
        black = self.black
        lo, hi = 0, len(black)
        while lo < hi:
            mid = (lo + hi) // 2
            if black[mid] - mid > r:
                hi = mid
            else:
                lo = mid + 1
        return r + lo

    def pick(self):
        return self.pick_from(random_below(self.seed, self.bound))


def main():
    n = 1000000000
    seed = [710]
    blacklist = [i * 10000 + random_below(seed, 10000) for i in range(100000)]
    for i in range(99999, 0, -1):
        j = random_below(seed, i + 1)
        blacklist[i], blacklist[j] = blacklist[j], blacklist[i]
    total = 0
    for rnd in range(5):
        s = Solution(n, blacklist, 1 + rnd)
        for _ in range(1000000):
            total += s.pick()
    print(f"5 rounds of 1000000 picks, 100000 of 1000000000 blacklisted: sum {total}")


main()
