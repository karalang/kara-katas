# LeetCode #1590: Make Sum Divisible by P -- the Python mirror of
# divisible.kara: the latest prefix with each remainder, in a dict.


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


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, top, most_p, rng):
    check = 0
    none = 0
    for _ in range(count):
        n = rng.wide() % most + 1
        nums = [rng.wide() % top + 1 for _ in range(n)]
        p = rng.wide() % most_p + 1
        answer = min_subarray(nums, p)
        if answer == -1:
            none += 1
        check = mix(check, answer)
    print(f"{count} problems of up to {most} values, p up to {most_p}: {none} impossible, checksum {check}")


def main():
    examples = [
        ([3, 1, 4, 2], 6),
        ([6, 3, 5, 2], 9),
        ([1, 2, 3], 3),
        ([1, 2, 3], 7),
        ([1000000000, 1000000000, 1000000000], 3),
        ([4, 4, 2], 7),
        ([5], 5),
        ([5], 3),
    ]
    for nums, p in examples:
        print(f"{nums} {p} -> {min_subarray(nums, p)}")
    rng = Rng(1590)
    batch(3000, 8, 9, 12, rng)
    batch(300, 1000, 1000000000, 1000, rng)
    batch(10, 100000, 1000000000, 100000, rng)


main()
