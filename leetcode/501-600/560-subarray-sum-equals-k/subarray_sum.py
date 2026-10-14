# LeetCode #560: Subarray Sum Equals K -- Python mirror of the ★ arm
# (prefix sums in a dict); see subarray_sum.kara.


def subarray_sum(nums, k):
    seen = {0: 1}
    total = 0
    count = 0
    for x in nums:
        total += x
        count += seen.get(total - k, 0)
        seen[total] = seen.get(total, 0) + 1
    return count


# ---- test harness ----------------------------------------------------------


class Seed:
    def __init__(self, v):
        self.v = v

    def step(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


def show(nums, k):
    print(f"{nums} k={k}: {subarray_sum(nums, k)}")


def main():
    show([1, 1, 1], 2)
    show([1, 2, 3], 3)
    show([5], 5)
    show([5], -5)
    show([0, 0, 0, 0], 0)
    show([1, -1, 1, -1], 0)
    show([-3, 1, 2, -3, 4], -3)
    show([1000, -1, 1000, -1, 1000], 2998)
    seed = Seed(560)
    total = 0
    checksum = 0
    for _ in range(300):
        n = 1 + seed.step() % 40
        nums = [seed.step() % 11 - 5 for _ in range(n)]
        k = seed.step() % 17 - 8
        c = subarray_sum(nums, k)
        total += c
        checksum = (checksum * 31 + c) % 1000000007
    print(f"300 random arrays: {total} subarrays, checksum {checksum}")
    print(f"5000 zeros, k=0: {subarray_sum([0] * 5000, 0)}")
    big = [seed.step() % 2001 - 1000 for _ in range(5000)]
    print(f"5000 values, k=0: {subarray_sum(big, 0)}")


main()
