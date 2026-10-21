# LeetCode 823 — Binary Trees With Factors, by counts in a map.
#
# Mirrors num_factored_binary_trees.kara: sort the values, so that both
# factors of a value come before it, and count each value's trees from
# its factors' counts, looked up by value in a map.


def num_factored_binary_trees(arr):
    modulus = 1000000007
    values = sorted(arr)
    trees = {}
    total = 0
    for i, x in enumerate(values):
        count = 1
        for j in range(i):
            left = values[j]
            if x % left == 0 and x // left in trees:
                count = (count + trees[left] * trees[x // left]) % modulus
        trees[x] = count
        total = (total + count) % modulus
    return total


class Random:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(arr):
    print(f"[{', '.join(map(str, arr))}] -> {num_factored_binary_trees(arr)}")


def main():
    show([2, 4])
    show([2, 4, 5, 10])
    show([2])
    show([2, 4, 8])
    show([2, 4, 8, 16])
    show([12, 6, 3, 2, 4])
    show([18, 3, 6, 2, 9])
    show([1000000000, 31622, 100000, 10000, 10])
    smooth = []
    p2 = 1
    while p2 <= 60000000:
        p3 = p2
        while p3 <= 60000000:
            p5 = p3
            while p5 <= 60000000:
                if p5 > 1:
                    smooth.append(p5)
                p5 *= 5
            p3 *= 3
        p2 *= 2
    smooth = sorted(smooth)[:1000]
    print(f"1000 values 2^a 3^b 5^c up to {smooth[999]} -> {num_factored_binary_trees(smooth)}")
    odd = [999999999 - 2 * k * 7919 for k in range(1000)]
    print(f"1000 odd values -> {num_factored_binary_trees(odd)}")
    rng = Random(823)
    total = 0
    check = 0
    for _ in range(300):
        count = 1 + rng.next() % 15
        arr = []
        while len(arr) < count:
            v = 2 + rng.next() % 59
            if v not in arr:
                arr.append(v)
        answer = num_factored_binary_trees(arr)
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"300 random sets: total {total}, checksum {check}")


main()
