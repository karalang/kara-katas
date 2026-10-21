# Benchmark for #823: Binary Trees With Factors -- the ★ arm (counts in a map).
#
# Mirrors num_factored_binary_trees.kara: sort a copy of the values, so
# that both factors of a value come before it, and count each value's
# trees from its factors' counts, looked up by value in a map.


def num_factored_binary_trees(arr):
    modulus = 1000000007
    values = sorted(arr)
    trees = {}
    total = 0
    for i in range(len(values)):
        x = values[i]
        count = 1
        for j in range(i):
            left = values[j]
            if x % left == 0:
                right = trees.get(x // left)
                if right is not None:
                    count = (count + trees[left] * right) % modulus
        trees[x] = count
        total = (total + count) % modulus
    return total


class Random:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def main():
    limit = 1000000000
    smooth = []
    p2 = 1
    while p2 <= limit:
        p3 = p2
        while p3 <= limit:
            p5 = p3
            while p5 <= limit:
                p7 = p5
                while p7 <= limit:
                    if p7 > 1:
                        smooth.append(p7)
                    p7 *= 7
                p5 *= 5
            p3 *= 3
        p2 *= 2
    smooth.sort()
    count = 64
    rounds = 1000
    rng = Random(823)
    sets = []
    for _ in range(count):
        taken = [False] * len(smooth)
        chosen = []
        while len(chosen) < 1000:
            k = rng.next() % len(smooth)
            if not taken[k]:
                taken[k] = True
                chosen.append(smooth[k])
        sets.append(chosen)
    total = 0
    checksum = 0
    for r in range(rounds):
        answer = num_factored_binary_trees(sets[r % count])
        total += answer
        checksum = (checksum * 131 + answer) % 1000000007
    print(f"{len(smooth)} values, {rounds} rounds of {count} sets: total {total}, checksum {checksum}")


main()
