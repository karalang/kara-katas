# LeetCode #2838: Maximum Coins Heroes Can Collect -- the bench, mirrored
# from coins.kara: sorted monsters, prefix sums, a binary search a hero.

from bisect import bisect_right


def maximum_coins(heroes, monsters, coins):
    pairs = sorted(zip(monsters, coins))
    prefix = [0]
    for _, c in pairs:
        prefix.append(prefix[-1] + c)
    powers = [p for p, _ in pairs]
    return [prefix[bisect_right(powers, h)] for h in heroes]


seed = 2838


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def main():
    count, rounds, n = 10, 5, 100000
    battles = []
    for _ in range(count):
        heroes = [wide() % 1000000000 + 1 for _ in range(n)]
        monsters = [wide() % 1000000000 + 1 for _ in range(n)]
        coins = [wide() % 1000000000 + 1 for _ in range(n)]
        battles.append((heroes, monsters, coins))
    check = 0
    for r in range(rounds):
        for heroes, monsters, coins in battles:
            for x in maximum_coins(heroes, monsters, coins):
                check = (check * 31 + x % 1000000007 + r) % 1000000007
    print(f"{count} battles of {n}, {rounds} rounds: checksum {check}")


main()
