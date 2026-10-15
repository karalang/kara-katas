# LeetCode #643: Maximum Average Subarray I -- Python mirror of the ★
# arm.
#
# A sliding sum: the first window added up once, then each step adding
# the value taken in and taking off the one left behind.


def find_max_average(nums, k):
    s = sum(nums[:k])
    best = s
    for i in range(k, len(nums)):
        s += nums[i] - nums[i - k]
        if s > best:
            best = s
    return best / k


# ---- test harness ----------------------------------------------------------

class Random:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(nums, k):
    text = ",".join(str(x) for x in nums)
    print(f"[{text}], k = {k} -> {find_max_average(nums, k):.5f}")


def random_values(n, most, rng):
    return [rng.next() % (2 * most + 1) - most for _ in range(n)]


def main():
    show([1, 12, -5, -6, 50, 3], 4)
    show([5], 1)
    show([-3, -1, -4, -1, -5], 2)
    show([4, -2, 7, 1], 4)
    show([3, -8, 9, 2, 9, -1], 1)
    show([10, 9, 1, 2, 3], 2)
    show([1, 2, 3, 9, 10], 2)
    show([1, 2, 1, 1, 3], 3)
    show([-10000, 10000, -10000, 10000], 3)
    rng = Random(643)
    total = 0.0
    whole = 0
    for _ in range(300):
        n = 1 + rng.next() % 30
        k = 1 + rng.next() % n
        nums = random_values(n, 20, rng)
        a = find_max_average(nums, k)
        total += a
        if a == float(int(a // 1)):
            whole += 1
    print(f"300 random arrays: sum of answers {total:.5f}, {whole} whole")
    nums = random_values(100000, 10000, rng)
    for k in [1, 1000, 50000, 100000]:
        print(f"100000 values, k = {k}: {find_max_average(nums, k):.5f}")


main()
