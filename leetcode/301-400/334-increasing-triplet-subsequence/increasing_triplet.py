# LeetCode #334: Increasing Triplet Subsequence — two running thresholds.
# Python mirror of increasing_triplet.kara; prints the same lines.


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


def show(nums):
    shown = ", ".join(str(x) for x in nums)
    print(f"[{shown}] -> {'true' if increasing_triplet(nums) else 'false'}")


def main():
    show([1, 2, 3, 4, 5])
    show([5, 4, 3, 2, 1])
    show([2, 1, 5, 0, 4, 6])
    show([])
    show([1])
    show([1, 2])
    show([1, 1, 1])
    show([1, 2, 2, 2])
    show([2, 1, 5, 0, 3])
    show([5, 1, 6, 0, 7])
    show([20, 100, 10, 12, 5, 13])
    show([1, 5, 0, 4, 1, 3])
    show([-9223372036854775808, 0, 9223372036854775807])
    show([9223372036854775807, 9223372036854775807, 9223372036854775807])
    rng = Rng(334)
    for rnd in range(8):
        n = 3 + rnd * 3
        show([rng.next() % (2 + rnd) for _ in range(n)])
    pairs = []
    top = 2000000
    for _ in range(50000):
        pairs.append(top - 1)
        pairs.append(top)
        top -= 2
    count = len(pairs)
    no = increasing_triplet(pairs)
    pairs.append(top + 3)
    yes = increasing_triplet(pairs)
    print(f"pairs: {count} values -> {'true' if no else 'false'}, one more -> {'true' if yes else 'false'}")


main()
