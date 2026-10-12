# Benchmark for #398: mirror of random_pick_index.kara (reservoir sampling).
import sys


class Solution:
    def __init__(self, nums):
        self.nums = nums
        self.seed = 398

    def below(self, n):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return (self.seed // 65536) % n

    def pick(self, target):
        kept = -1
        seen = 0
        for i in range(len(self.nums)):
            if self.nums[i] == target:
                seen += 1
                if self.below(seen) == 0:
                    kept = i
        return kept


def main():
    picks = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    seed = 3980
    nums = []
    for _ in range(20000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        nums.append((seed // 65536) % 10)
    s = Solution(nums)
    total = 0
    checksum = 0
    for p in range(picks):
        r = s.pick(p % 10)
        total += r
        checksum = (checksum * 31 + r) % 1000000007
    print(f"{picks} picks: total {total}, checksum {checksum}")


main()
