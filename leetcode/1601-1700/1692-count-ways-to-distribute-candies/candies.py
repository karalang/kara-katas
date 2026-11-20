# LeetCode #1692: Count Ways to Distribute Candies -- mirrors candies.kara,
# the ★ arm: one row of the Stirling numbers at a time.


def ways_to_distribute(n, k):
    modulus = 1000000007
    ways = [0] * (k + 1)
    ways[0] = 1
    for i in range(1, n + 1):
        for j in range(min(i, k), 0, -1):
            ways[j] = (j * ways[j] + ways[j - 1]) % modulus
        ways[0] = 0
    return ways[k]


class Seed:
    def __init__(self, v):
        self.v = v

    def next(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


def batch(count, most, seed):
    total = 0
    check = 0
    for _ in range(count):
        n = seed.next() % most + 1
        k = seed.next() % n + 1
        answer = ways_to_distribute(n, k)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"{count} problems of n up to {most}: answers sum to {total}, checksum {check}")


def main():
    print(ways_to_distribute(3, 2))
    print(ways_to_distribute(4, 2))
    print(ways_to_distribute(20, 5))
    print(ways_to_distribute(1, 1))
    print(ways_to_distribute(1000, 1000))
    print(ways_to_distribute(1000, 1))
    seed = Seed(1692)
    batch(3000, 10, seed)
    batch(300, 100, seed)
    batch(10, 1000, seed)


main()
