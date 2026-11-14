# LeetCode #1561: Maximum Number of Coins You Can Get -- the Python mirror
# of coins.kara, the ★ arm: sorted, the n smallest left to Bob, and every
# other pile of the rest from the bottom. Prints byte-identical output.


def max_coins(piles):
    ordered = sorted(piles)
    n = len(ordered) // 3
    return sum(ordered[n::2])


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, top):
    check = 0
    total = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        piles = [next_random() % top + 1 for _ in range(3 * n)]
        coins = max_coins(piles)
        total += coins
        check = mix(check, coins)
    print(f"{count} lists of up to {3 * most} piles of up to {top}: {total} coins, checksum {check}")


def main():
    global seed
    examples = [
        [2, 4, 1, 2, 7, 8],
        [2, 4, 5],
        [9, 8, 7, 6, 5, 1, 2, 3, 4],
        [1, 1, 1],
        [5, 5, 5, 5, 5, 5],
        [1, 2, 3, 4, 5, 6],
        [10000, 10000, 10000],
        [1, 10000, 1, 10000, 1, 10000],
    ]
    for piles in examples:
        print(f"{piles} -> {max_coins(piles)}")
    seed = 1561
    batch(3000, 3, 10)
    batch(300, 1000, 10000)
    batch(30, 33333, 10000)


main()
