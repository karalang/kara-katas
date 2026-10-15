# Benchmark for #666: a map of places, walked from the root, as the Kara
# ★ arm.


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


def main():
    rng = Rng(666)
    trees = []
    for _ in range(256):
        chance = 50 + rng.next() % 51
        trees.append(random_tree(4, chance, rng))
    rounds = 1000000
    s = 0
    for r in range(rounds):
        s = (s * 31 + path_sum(trees[r % 256]) + r) % 1000000007
    print(f"256 trees, {rounds} rounds: checksum {s}")


main()
