# LeetCode #1570: Dot Product of Two Sparse Vectors -- bench: the ★ arm
# (index-ordered pairs merged by two pointers) over 20 vectors of 500000
# values, one in 10 of them from 1 to 100 and the rest 0, each made sparse
# once; then the product of every ordered pair of them, 400 products.


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


seed = 1570


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    n = 500000
    vectors = []
    for _ in range(20):
        nums = []
        for _ in range(n):
            draw = next_random()
            nums.append(draw // 10 % 100 + 1 if draw % 10 == 0 else 0)
        vectors.append(SparseVector(nums))
    check = 0
    total = 0
    for i in range(len(vectors)):
        for j in range(len(vectors)):
            product = vectors[i].dot_product(vectors[j])
            total += product
            check = mix(check, product)
    print(f"400 products of 20 vectors of 500000 values: products sum {total}, checksum {check}")


main()
