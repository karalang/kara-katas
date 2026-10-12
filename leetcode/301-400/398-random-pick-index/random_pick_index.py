# LeetCode #398: Random Pick Index -- mirror of random_pick_index.kara
# (reservoir sampling), drawing the same random numbers.
import math


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


def b(x):
    return "true" if x else "false"


def fair(nums, target, draws):
    n = len(nums)
    count = sum(1 for v in nums if v == target)
    got = [0] * n
    s = Solution(list(nums))
    for _ in range(draws):
        x = s.pick(target)
        if x < 0 or x >= n or nums[x] != target:
            return False
        got[x] += 1
    e = draws / count
    chi = 0.0
    for i in range(n):
        if nums[i] == target:
            d = got[i] - e
            chi += d * d / e
    dof = float(count - 1)
    return chi <= dof + 6.0 * math.sqrt(2.0 * dof) + 12.0


def main():
    example = [1, 2, 3, 3, 3]
    print(f"example [1, 2, 3, 3, 3], pick(3) 30000 draws: fair {b(fair(example, 3, 30000))}")
    s = Solution(list(example))
    always = True
    for _ in range(100):
        always = always and s.pick(1) == 0
    print(f"example, pick(1): always 0 {b(always)}")
    one = Solution([7])
    only = True
    for _ in range(100):
        only = only and one.pick(7) == 0
    print(f"one value [7], pick(7): always 0 {b(only)}")
    print(f"ten equal values, pick(5): fair {b(fair([5] * 10, 5, 30000))}")
    mixed = [-1, 4, -1, -1, 4]
    print(f"[-1, 4, -1, -1, 4], pick(-1): fair {b(fair(mixed, -1, 30000))}, pick(4): fair {b(fair(mixed, 4, 30000))}")
    long = [i * i % 7 for i in range(1000)]
    print(f"1000 values of 4 kinds, pick(2): fair {b(fair(long, 2, 5000))}")
    seed = 398
    passed = 0
    values = 0
    for _ in range(200):
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = 1 + (seed // 65536) % 60
        nums = []
        for _ in range(n):
            seed = (seed * 1103515245 + 12345) % 2147483648
            nums.append((seed // 65536) % 10 - 5)
        seed = (seed * 1103515245 + 12345) % 2147483648
        target = nums[(seed // 65536) % n]
        values += n
        if fair(nums, target, 20 * n):
            passed += 1
    print(f"200 random arrays, {values} values: {passed} fair")


main()
