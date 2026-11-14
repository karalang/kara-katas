# LeetCode #1561: Maximum Number of Coins You Can Get -- bench: the ★ arm
# (sorted, every other pile past the n smallest) over 20 lists of 99999
# piles of 1 to 10000 coins, built once, each asked 10 times.
# Python mirror of coins.kara.


def max_coins(piles):
    ordered = sorted(piles)
    n = len(ordered) // 3
    return sum(ordered[n::2])


seed = 1561


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    lists = [[next_random() % 10000 + 1 for _ in range(99999)] for _ in range(20)]
    check = 0
    total = 0
    for _ in range(10):
        for piles in lists:
            coins = max_coins(piles)
            total += coins
            check = mix(check, coins)
    print(f"10 passes over 20 lists of 99999 piles: {total} coins, checksum {check}")


main()
