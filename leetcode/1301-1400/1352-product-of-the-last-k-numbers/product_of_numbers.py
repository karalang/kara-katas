# LeetCode #1352 -- Python mirror of the ★ arm: the running products since
# the last zero, after a leading 1.


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


seed = [1352]


def next_random():
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def draw(since, zero, big):
    if next_random() % zero == 0:
        since[0] = 1
        return 0
    num = 1
    if next_random() % big == 0:
        num = 2 + next_random() % 99
    if since[0] * num >= 2147483648:
        num = 1
    since[0] *= num
    return num


def main():
    p = ProductOfNumbers()
    for x in (3, 0, 2, 5, 4):
        p.add(x)
    a, b, c = p.get_product(2), p.get_product(3), p.get_product(4)
    p.add(8)
    print(a, b, c, p.get_product(2))
    p = ProductOfNumbers()
    p.add(7)
    one = p.get_product(1)
    p.add(6)
    all_ = p.get_product(2)
    p.add(0)
    p.add(9)
    past = p.get_product(2)
    after = p.get_product(1)
    q = ProductOfNumbers()
    q.add(65536)
    q.add(32767)
    q.add(1)
    print(one, all_, past, after, q.get_product(3))
    since = [1]
    p = ProductOfNumbers()
    for _ in range(39000):
        p.add(draw(since, 5000, 30))
    check = 0
    for _ in range(1000):
        k = 1 + next_random() % 40000
        check = (check * 131 + p.get_product(k)) % 1000000007
    print(f"4 * 10^4 calls: checksum {check}")
    check = 0
    total = 0
    for c in range(500):
        p = ProductOfNumbers()
        since = [1]
        added = 0
        calls = 1 + next_random() % 60
        zero, big = (8, 3) if c % 2 == 0 else (30, 2)
        for _ in range(calls):
            if added == 0 or next_random() % 3 > 0:
                p.add(draw(since, zero, big))
                added += 1
            else:
                got = p.get_product(1 + next_random() % added)
                total += got
                check = (check * 131 + got) % 1000000007
    print(f"500 random sessions: products total {total}, checksum {check}")


main()
