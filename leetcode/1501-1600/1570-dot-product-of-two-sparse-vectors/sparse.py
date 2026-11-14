# LeetCode #1570: Dot Product of Two Sparse Vectors -- the Python mirror of
# the ★ arm (sparse.kara): each vector kept as its values other than 0 with
# their indices, and the product a merge by two pointers. O(a + b)


class SparseVector:
    def __init__(self, nums):
        self.pairs = [(i, x) for i, x in enumerate(nums) if x != 0]

    def dot_product(self, other):
        i = 0
        j = 0
        total = 0
        while i < len(self.pairs) and j < len(other.pairs):
            a, x = self.pairs[i]
            b, y = other.pairs[j]
            if a == b:
                total += x * y
                i += 1
                j += 1
            elif a < b:
                i += 1
            else:
                j += 1
        return total


def dot(a, b):
    return SparseVector(a).dot_product(SparseVector(b))


# ---- the harness: the same in every arm

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, sparse, top):
    check = 0
    total = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        pair = []
        for _ in range(2):
            odds = next_random() % sparse + 1
            nums = []
            for _ in range(n):
                draw = next_random()
                nums.append(draw // odds % top + 1 if draw % odds == 0 else 0)
            pair.append(nums)
        product = dot(pair[0], pair[1])
        total += product
        check = mix(check, product % 1000000007)
    print(f"{count} pairs of up to {most} values: products sum {total}, checksum {check}")


def main():
    global seed
    examples = [
        ([1, 0, 0, 2, 3], [0, 3, 0, 4, 0]),
        ([0, 1, 0, 0, 0], [0, 0, 0, 0, 2]),
        ([0, 1, 0, 0, 2, 0, 0], [1, 0, 0, 0, 3, 0, 4]),
        ([0], [0]),
        ([7], [6]),
        ([100, 100, 100], [100, 100, 100]),
        ([0, 0, 5, 0], [0, 0, 0, 5]),
    ]
    for a, b in examples:
        print(f"{a} . {b} -> {dot(a, b)}")
    seed = 1570
    batch(3000, 10, 3, 3)
    batch(300, 1000, 20, 100)
    batch(30, 100000, 100, 100)


main()
