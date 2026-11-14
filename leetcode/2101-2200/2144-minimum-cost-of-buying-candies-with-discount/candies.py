# LeetCode #2144: Minimum Cost of Buying Candies With Discount -- the
# Python mirror of candies.kara's ★ arm.


def minimum_cost(cost):
    dearest_first = sorted(cost, reverse=True)
    return sum(c for i, c in enumerate(dearest_first) if i % 3 != 2)


seed = 2144


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(cost):
    print(f"[{', '.join(map(str, cost))}] -> {minimum_cost(cost)}")


def main():
    show([1, 2, 3])
    show([6, 5, 7, 9, 2, 2])
    show([5, 5])
    show([1])
    show([3, 3, 3])
    show([100, 1, 1])
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % 20 + 1
        top = [100, 5][rnd % 2]
        cost = [next_random() % top + 1 for _ in range(n)]
        paid = minimum_cost(cost)
        total += paid
        check = (check * 31 + paid + n) % 1000000007
    print(f"2000 baskets: {total} paid in all, checksum {check}")
    full = [100] * 100
    every = list(range(1, 101))
    rand = [next_random() % 100 + 1 for _ in range(100)]
    print(f"100 candies: {minimum_cost(full)} all 100, {minimum_cost(every)} one of each, {minimum_cost(rand)} at random")


main()
