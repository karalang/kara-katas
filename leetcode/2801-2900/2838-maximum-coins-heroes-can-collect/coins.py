# LeetCode #2838: Maximum Coins Heroes Can Collect -- the Python mirror of
# the ★ arm: the monsters sorted with their coins, prefix sums, and a
# binary search for each hero.

from bisect import bisect_right


def maximum_coins(heroes, monsters, coins):
    pairs = sorted(zip(monsters, coins))
    prefix = [0]
    for _, c in pairs:
        prefix.append(prefix[-1] + c)
    powers = [p for p, _ in pairs]
    return [prefix[bisect_right(powers, h)] for h in heroes]


# ---- the harness: the same in every arm --------------------------------

seed = 2838


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def digest(xs):
    h = 0
    for x in xs:
        h = (h * 131 + x) % 1000000007
    return h


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    print(show(maximum_coins([1, 4, 2], [1, 1, 5, 2, 3], [2, 3, 4, 5, 6])))
    print(show(maximum_coins([5], [2, 3, 1, 2], [10, 6, 5, 2])))
    print(show(maximum_coins([4, 4], [5, 7, 8], [1, 1, 1])))
    print(show(maximum_coins([1000000000, 1], [1000000000, 999999999, 2], [1000000000, 1000000000, 1000000000])))
    check = 0
    for _ in range(3000):
        n = next_random() % 6 + 1
        m = next_random() % 6 + 1
        heroes = [next_random() % 8 + 1 for _ in range(n)]
        monsters = [next_random() % 8 + 1 for _ in range(m)]
        coins = [next_random() % 10 + 1 for _ in range(m)]
        check = (check * 31 + digest(maximum_coins(heroes, monsters, coins))) % 1000000007
    print(f"3000 small battles: checksum {check}")
    check = 0
    total = 0
    for _ in range(50):
        n = next_random() % 1000 + 1
        m = next_random() % 1000 + 1
        heroes = [wide() % 1000000000 + 1 for _ in range(n)]
        monsters = [wide() % 1000000000 + 1 for _ in range(m)]
        coins = [wide() % 1000000000 + 1 for _ in range(m)]
        out = maximum_coins(heroes, monsters, coins)
        total += sum(out)
        check = (check * 31 + digest(out)) % 1000000007
    print(f"50 large battles: coins total {total}, checksum {check}")


main()
