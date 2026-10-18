# LeetCode 747 — Largest Number At Least Twice of Others, one pass.
# Mirror of dominant_index.kara (the ★ arm); same output, byte for byte.


def dominant_index(nums):
    best = 0
    second = -1
    for i in range(1, len(nums)):
        if nums[i] > nums[best]:
            second = nums[best]
            best = i
        elif nums[i] > second:
            second = nums[i]
    return best if nums[best] >= 2 * second else -1


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(nums):
    print(f"[{', '.join(map(str, nums))}] -> {dominant_index(nums)}")


def random_nums(rng, n, m, small):
    at = rng.next() % n
    limit = m // 2 + 1 if small else m
    return [m if i == at else rng.next() % limit for i in range(n)]


def main():
    show([3, 6, 1, 0])
    show([1, 2, 3, 4])
    show([0, 1])
    show([1, 0])
    show([2, 4])
    show([2, 5])
    show([100, 50, 50, 49])
    show([0, 0, 0, 1, 0])

    rng = Rng(747)
    wide = random_nums(rng, 50, 100, False)
    print(f"50 random values below 100 and one 100: {dominant_index(wide)}")
    narrow = random_nums(rng, 50, 100, True)
    print(f"50 random values up to 50 and one 100: {dominant_index(narrow)}")

    found = 0
    check = 0
    for _ in range(300):
        n = 2 + rng.next() % 10
        m = 1 + rng.next() % 100
        small = rng.next() % 2 == 0
        nums = random_nums(rng, n, m, small)
        got = dominant_index(nums)
        if got != -1:
            found += 1
        check = (check * 31 + got + 1) % 1000000007
    print(f"300 random lists: {found} have a dominant value, checksum {check}")


main()
