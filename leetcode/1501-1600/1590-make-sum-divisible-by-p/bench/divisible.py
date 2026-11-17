# LeetCode #1590: Make Sum Divisible by P -- the bench in Python,
# mirroring divisible.kara.


def min_subarray(nums, p):
    need = sum(nums) % p
    if need == 0:
        return 0
    last = {0: -1}
    prefix = 0
    best = len(nums)
    for j, v in enumerate(nums):
        prefix = (prefix + v) % p
        i = last.get((prefix - need + p) % p)
        if i is not None:
            best = min(best, j - i)
        last[prefix] = j
    return -1 if best == len(nums) else best


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536

    def wide(self):
        a = self.next()
        return a * 32768 + self.next()


def main():
    rng = Rng(1590)
    problems = []
    for _ in range(40):
        nums = [rng.wide() % 1000000000 + 1 for _ in range(100000)]
        p = rng.wide() % 100000 + 1
        problems.append((nums, p))
    check = 0
    total = 0
    for nums, p in problems:
        answer = min_subarray(nums, p)
        total += answer
        check = (check * 31 + answer + 1) % 1000000007
    print(f"40 problems of 100000 values: lengths {total}, checksum {check}")


main()
