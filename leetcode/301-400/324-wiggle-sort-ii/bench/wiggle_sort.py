# Benchmark mirror of LeetCode #324 — same select arm as
# bench/wiggle_sort.kara.

LEN = 1000000
PASSES = 16
STRIDE = 9973
MODULUS = 1073741789


def median3(x, y, z):
    if (x <= y and y <= z) or (z <= y and y <= x):
        return y
    if (y <= x and x <= z) or (z <= x and x <= y):
        return x
    return z


def select(a, k):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        pivot = median3(a[lo], a[mid], a[hi])
        lt = i = lo
        gt = hi
        while i <= gt:
            if a[i] < pivot:
                a[lt], a[i] = a[i], a[lt]
                lt += 1
                i += 1
            elif a[i] > pivot:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:
                i += 1
        if k < lt:
            hi = lt - 1
        elif k > gt:
            lo = gt + 1
        else:
            return pivot
    return a[k]


def wiggle_sort(nums):
    n = len(nums)
    median = select(nums, n // 2)
    m = n | 1
    left = i = 0
    right = n - 1
    while i <= right:
        vi = (1 + 2 * i) % m
        if nums[vi] > median:
            l = (1 + 2 * left) % m
            nums[l], nums[vi] = nums[vi], nums[l]
            left += 1
            i += 1
        elif nums[vi] < median:
            r = (1 + 2 * right) % m
            nums[vi], nums[r] = nums[r], nums[vi]
            right -= 1
        else:
            i += 1


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536

    def draw(self, bound):
        hi = self.next()
        lo = self.next()
        return (hi * 32768 + lo) % bound


def refill(nums, k, rng):
    n = len(nums)
    for i in range(n):
        if i % 2 == 0:
            nums[i] = rng.draw(k)
        else:
            nums[i] = k + rng.draw(k)
    i = n - 1
    while i > 0:
        j = rng.draw(i + 1)
        nums[i], nums[j] = nums[j], nums[i]
        i -= 1


def violations(a):
    bad = 0
    for i in range(1, len(a)):
        if i % 2 == 1:
            if a[i] <= a[i - 1]:
                bad += 1
        elif a[i] >= a[i - 1]:
            bad += 1
    return bad


def main():
    rng = Rng(324)
    sink = 0
    nums = [0] * LEN
    ks = [2, 3, 50, 2500]
    bad = 0
    for p in range(PASSES):
        refill(nums, ks[p % 4], rng)
        wiggle_sort(nums)
        bad = violations(nums)
        probe = 0
        for i in range(0, LEN, STRIDE):
            probe = (probe * 31 + nums[i]) % MODULUS
        sink = (sink * 131 + bad * 7 + probe) % MODULUS
    print(f"sink {sink} violations {bad}")


main()
