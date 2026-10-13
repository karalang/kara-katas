# Benchmark for #518: Python mirror of the ★ arm (one row, coins on the
# outside); see change.kara.


def change(amount, coins):
    ways = [0] * (amount + 1)
    ways[0] = 1
    for c in coins:
        for a in range(c, amount + 1):
            ways[a] += ways[a - c]
    return ways[amount]


seed = 518


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 3,000 random sets of 100 different coins from 500 to 5,000, each
    # with an amount from 4,000 to 5,000 (the problem's most), solved
    # once each. Coins of at least 500 keep every count well inside an
    # i64.
    sets = 3000
    checksum = 0
    for _ in range(sets):
        amount = 4000 + next_random() % 1001
        coins = []
        taken = [False] * 5001
        while len(coins) < 100:
            c = 500 + next_random() % 4501
            if not taken[c]:
                taken[c] = True
                coins.append(c)
        checksum = (checksum * 31 + change(amount, coins) % 1000000007) % 1000000007
    print(f"{sets} sets of 100 coins: checksum {checksum}")


main()
