# Benchmark workload for LeetCode #334 — Python mirror of increasing_triplet.kara.

VALUES = 1000000
PUNCHES = 100
MODULUS = 1073741789


def increasing_triplet(nums):
    first = None
    second = None
    for x in nums:
        if second is not None and x > second:
            return True
        if first is not None and x > first:
            second = x
        else:
            first = x
    return False


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536

    def wide(self):
        hi = self.next()
        return hi * 32768 + self.next()


def main():
    nums = []
    top = 2 * VALUES
    for _ in range(VALUES // 2):
        nums.append(top - 1)
        nums.append(top)
        top -= 2
    rng = Rng(334)
    sink = 0
    for p in range(PUNCHES):
        at = 2 + 2 * (rng.wide() % (VALUES // 2 - 1))
        old = nums[at]
        if p % 2 == 0:
            nums[at] = nums[at - 1] + 1
        answer = 1 if increasing_triplet(nums) else 0
        nums[at] = old
        sink = (sink * 1000003 + answer * 2000003 + at) % MODULUS
    print(sink)


main()
