# LeetCode #518: Coin Change II -- one row, coins on the outside.
# Mirrors change.kara (the star arm) and its harness.


def change(amount, coins):
    ways = [0] * (amount + 1)
    ways[0] = 1
    for c in coins:
        for a in range(c, amount + 1):
            ways[a] += ways[a - c]
    return ways[amount]


# ---- test harness ---------------------------------------------------------

seed = 518


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(amount, coins):
    print(f"{amount}, [{', '.join(str(c) for c in coins)}]: {change(amount, coins)}")


def main():
    show(5, [1, 2, 5])
    show(3, [2])
    show(10, [10])
    show(0, [7])
    show(7, [2, 4])
    show(500, [1, 2, 5, 10, 20, 50, 100, 200])
    show(5000, [11, 24, 37, 50])
    count = 300
    none = 0
    checksum = 0
    for _ in range(count):
        amount = next_random() % 301
        k = 1 + next_random() % 8
        coins = []
        while len(coins) < k:
            c = 1 + next_random() % 60
            if c not in coins:
                coins.append(c)
        v = change(amount, coins)
        if v == 0:
            none += 1
        checksum = (checksum * 31 + v % 1000000007) % 1000000007
    print(f"{count} random amounts: {none} cannot be made, checksum {checksum}")


main()
