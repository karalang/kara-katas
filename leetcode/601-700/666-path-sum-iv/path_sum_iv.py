# LeetCode #666: Path Sum IV -- a map of places, walked from the root.
# Mirrors the ★ arm (path_sum_iv.kara) and its test harness.


def path_sum(nums):
    values = {x // 10: x % 10 for x in nums}

    def walk(key, above):
        if key not in values:
            return 0
        s = above + values[key]
        depth, position = key // 10, key % 10
        left = (depth + 1) * 10 + 2 * position - 1
        right = left + 1
        if left not in values and right not in values:
            return s
        return walk(left, s) + walk(right, s)

    return walk(11, 0)


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_tree(levels, chance, rng):
    nums = [110 + rng.next() % 10]
    level = [1]
    for depth in range(2, levels + 1):
        nxt = []
        for p in level:
            for c in range(2 * p - 1, 2 * p + 1):
                if rng.next() % 100 < chance:
                    nxt.append(c)
                    nums.append(depth * 100 + c * 10 + rng.next() % 10)
        level = nxt
    return nums


def show(nums):
    print(f"[{','.join(str(x) for x in nums)}]: {path_sum(nums)}")


def main():
    show([113, 215, 221])
    show([113, 221])
    show([115])
    show([111, 212, 313, 414])
    show([119, 228, 347, 486])
    nines = []
    zeros = []
    for depth in range(1, 5):
        for p in range(1, (1 << (depth - 1)) + 1):
            nines.append(depth * 100 + p * 10 + 9)
            zeros.append(depth * 100 + p * 10)
    show(nines)
    show(zeros)
    rng = Rng(666)
    s = 0
    most = 0
    for _ in range(2000):
        levels = 1 + rng.next() % 4
        chance = 30 + rng.next() % 71
        v = path_sum(random_tree(levels, chance, rng))
        most = max(most, v)
        s = (s * 31 + v) % 1000000007
    print(f"2000 random trees: largest {most}, checksum {s}")


main()
