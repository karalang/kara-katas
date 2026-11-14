# LeetCode #2144: Minimum Cost of Buying Candies With Discount -- the
# benchmark, the same algorithm as candies.kara.

seed = 2144


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def minimum_cost(cost):
    dearest_first = sorted(cost, reverse=True)
    return sum(c for i, c in enumerate(dearest_first) if i % 3 != 2)


def main():
    baskets = [[next_random() % 100 + 1 for _ in range(100)] for _ in range(1000)]
    total = check = 0
    for rnd in range(100):
        for b in range(1000):
            at = next_random() % 100
            baskets[b][at] = next_random() % 100 + 1
            paid = minimum_cost(baskets[b])
            total += paid
            check = (check * 31 + paid + rnd) % 1000000007
    print(f"100000 solves: {total} paid in all, checksum {check}")


main()
