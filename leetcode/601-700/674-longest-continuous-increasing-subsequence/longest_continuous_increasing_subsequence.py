# LeetCode #674: Longest Continuous Increasing Subsequence -- one pass
# with a running length.
# Mirrors the ★ arm (longest_continuous_increasing_subsequence.kara) and
# its test harness.


def find_length_of_lcis(nums):
    best = 0
    run = 0
    for i in range(len(nums)):
        if i > 0 and nums[i - 1] < nums[i]:
            run += 1
        else:
            run = 1
        best = max(best, run)
    return best


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(nums):
    if len(nums) <= 10:
        body = ", ".join(str(v) for v in nums)
        return f"[{body}]"
    return f"{len(nums)} numbers"


def main():
    cases = [[1, 3, 5, 4, 7], [2, 2, 2, 2, 2], [7], [1, 2], [2, 1],
             [1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1], [1, 1, 2, 2, 3, 3],
             [-3, -1, -2, 0, 5], [5, 1, 2, 3, 0, 1], [1, 3, 5, 7, 2, 4, 6, 8, 10],
             [-1000000000, 1000000000, -1000000000, 1000000000]]
    rising = []
    falling = []
    saw = []
    for i in range(10000):
        rising.append(i * 200000 - 1000000000)
        falling.append(1000000000 - i * 200000)
        saw.append(i % 100)
    cases.append(rising)
    cases.append(falling)
    cases.append(saw)
    for nums in cases:
        print(f"{show(nums)}: {find_length_of_lcis(nums)}")
    rng = Rng(674)
    s = 0
    most = 0
    for c in range(1000):
        size = 1 + rng.next() % 1000
        spread = [3, 30, 2000000001][c % 3]
        nums = []
        for _ in range(size):
            nums.append((rng.next() * 32768 + rng.next()) % spread - spread // 2)
        got = find_length_of_lcis(nums)
        most = max(most, got)
        s = (s * 31 + got) % 1000000007
    print(f"1000 random: longest {most}, checksum {s}")


main()
