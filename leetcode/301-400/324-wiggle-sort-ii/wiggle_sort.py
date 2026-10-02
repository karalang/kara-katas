# LeetCode #324: Wiggle Sort II — mirror of wiggle_sort.kara (sort, then
# interleave both halves from the top). Same cases, same LCG, same output.


def wiggle_sort(nums):
    n = len(nums)
    s = sorted(nums)
    lo = (n + 1) // 2 - 1
    hi = n - 1
    for i in range(n):
        if i % 2 == 0:
            nums[i] = s[lo]
            lo -= 1
        else:
            nums[i] = s[hi]
            hi -= 1


def is_wiggle(a):
    for i in range(1, len(a)):
        if i % 2 == 1 and a[i] <= a[i - 1]:
            return False
        if i % 2 == 0 and a[i] >= a[i - 1]:
            return False
    return True


def verdict(out, inp):
    if sorted(out) != sorted(inp):
        return "NOT A PERMUTATION"
    if not is_wiggle(out):
        return "NOT A WIGGLE"
    return "ok"


def show(a):
    return "[" + ", ".join(str(x) for x in a) + "]"


def report(inp):
    nums = list(inp)
    wiggle_sort(nums)
    print(f"{show(inp)} -> {show(nums)} {verdict(nums, inp)}")


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def wiggle_input(n, k, rng):
    a = []
    for i in range(n):
        if i % 2 == 0:
            a.append(rng.next() % k)
        else:
            a.append(k + rng.next() % k)
    i = n - 1
    while i > 0:
        j = rng.next() % (i + 1)
        a[i], a[j] = a[j], a[i]
        i -= 1
    return a


def checksum(a):
    h = 0
    for x in a:
        h = (h * 31 + x + 1) % 1000000007
    return h


def main():
    report([1, 5, 1, 1, 6, 4])
    report([1, 3, 2, 2, 3, 1])
    report([7])
    report([2, 1])
    report([1, 1, 2])
    report([4, 5, 5, 6])
    report([5, 6, 5, 6, 5, 6])
    report([1, 1, 2, 2, 2, 3])
    report([0, 5000, 0, 5000, 4999])
    report([1, 3, 2, 4, 3, 5])
    report([9, 8, 7, 6, 5, 4, 3])
    rng = Rng(324)
    for t, n in enumerate([5, 8, 11]):
        report(wiggle_input(n, 2 + t, rng))
    for n, k in zip([1000, 20001, 50000], [3, 50, 2500]):
        inp = wiggle_input(n, k, rng)
        nums = list(inp)
        wiggle_sort(nums)
        print(f"n={n} k={k} -> {checksum(nums)} {verdict(nums, inp)}")


main()
