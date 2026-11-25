# LeetCode #1352 bench -- Python: the running products since the last zero,
# after a leading 1.


class ProductOfNumbers:
    def __init__(self):
        self.prefix = [1]

    def add(self, num):
        if num == 0:
            self.prefix = [1]
        else:
            self.prefix.append(self.prefix[-1] * num)

    def get_product(self, k):
        n = len(self.prefix)
        if k >= n:
            return 0
        return self.prefix[n - 1] // self.prefix[n - 1 - k]


def main():
    seed = 1352
    since = 1
    p = ProductOfNumbers()
    check = 0
    for r in range(10000000):
        num = 1
        seed = (seed * 1103515245 + 12345) % 2147483648
        if (seed // 65536) % 1000 == 0:
            num = 0
            since = 1
        else:
            seed = (seed * 1103515245 + 12345) % 2147483648
            if (seed // 65536) % 20 == 0:
                seed = (seed * 1103515245 + 12345) % 2147483648
                num = 2 + (seed // 65536) % 99
            if since * num >= 2147483648:
                num = 1
            since *= num
        p.add(num)
        k = 1 + check % min(50000, r + 1)
        check = (check * 31 + p.get_product(k) + r) % 1000000007
    print(f"10000000 rounds: checksum {check}")


main()
