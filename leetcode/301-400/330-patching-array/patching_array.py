# LeetCode #330: Patching Array — Python mirror of patching_array.kara.


def min_patches(nums, n):
    miss = 1
    i = 0
    patches = 0
    while miss <= n:
        if i < len(nums) and nums[i] <= miss:
            miss += nums[i]
            i += 1
        else:
            miss += miss
            patches += 1
    return patches


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_sorted(rng, length, mx):
    return sorted(rng.next() % mx + 1 for _ in range(length))


def fmt(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def show(nums, n):
    print(f"{fmt(nums)} n={n} -> {min_patches(nums, n)}")


def main():
    show([1, 3], 6)
    show([1, 5, 10], 20)
    show([1, 2, 2], 5)
    show([], 1)
    show([], 8)
    show([], 2147483647)
    show([1], 1)
    show([2], 1)
    show([1, 2, 31, 33], 2147483647)
    show([1, 1, 1, 1, 1, 1, 1, 1], 8)
    show([5, 6, 7], 100)
    show([1000000], 999999)
    rng = Rng(330)
    for rnd in range(4):
        length = 5 + rnd * 5
        v = random_sorted(rng, length, 50 * (rnd + 1))
        n = rng.next() % 5000 + 1
        print(f"random {rnd}: len {length} n={n} -> {min_patches(v, n)}")
    big = random_sorted(rng, 1000, 1000000)
    print(f"big: len 1000 n=2147483647 -> {min_patches(big, 2147483647)}")


main()
