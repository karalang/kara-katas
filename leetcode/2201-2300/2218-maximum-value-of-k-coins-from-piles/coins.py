# LeetCode #2218: Maximum Value of K Coins From Piles -- mirror of
# coins.kara: a knapsack over the piles, best[j] the most j coins are
# worth so far, each pile tried at every count of its top coins with j
# running down. O(k * total).


def max_value_of_coins(piles, k):
    best = [0] * (k + 1)
    for pile in piles:
        prefix = [0]
        for coin in pile:
            prefix.append(prefix[-1] + coin)
        for j in range(k, 0, -1):
            for t in range(1, min(len(pile), j) + 1):
                best[j] = max(best[j], best[j - t] + prefix[t])
    return best[k]


seed = 2218


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# a draw of 30 bits, since one draw stops at 32767
def wide_random():
    return next_random() * 32768 + next_random()


def show(piles, k):
    print(f"{piles} with k = {k} -> {max_value_of_coins(piles, k)}")


# piles of 1 to `most` coins, worth 1 to `top` each
def draw_piles(n, most, top):
    piles = []
    for _ in range(n):
        size = next_random() % most + 1
        piles.append([wide_random() % top + 1 for _ in range(size)])
    return piles


def main():
    # LeetCode's two examples, then four more: one pile, every coin
    # taken, a deep coin worth the shallow ones above it, and one coin
    show([[1, 100, 3], [7, 8, 9]], 2)
    show([[100], [100], [100], [100], [100], [100], [1, 1, 1, 1, 1, 1, 700]], 7)
    show([[5, 4, 3, 2, 1]], 3)
    show([[1, 2], [3]], 3)
    show([[9, 9], [1, 1, 30]], 3)
    show([[42]], 1)
    # 3000 random cases of 1 to 6 piles of 1 to 5 coins, worth up to
    # 10, 1000 and 10^5 in turn, k from 1 to every coin
    check = 0
    for c in range(3000):
        n = next_random() % 6 + 1
        piles = draw_piles(n, 5, [10, 1000, 100000][c % 3])
        total = sum(len(pile) for pile in piles)
        k = next_random() % total + 1
        check = (check * 31 + max_value_of_coins(piles, k)) % 1000000007
    print(f"3000 cases: checksum {check}")
    # the constraints' largest: 1000 piles of 2 coins with k = 1999, and
    # 10 piles of 200 with k = 1000, coins up to 10^5
    pairs = []
    for _ in range(1000):
        a = wide_random() % 100000 + 1
        pairs.append([a, wide_random() % 100000 + 1])
    tall = [[wide_random() % 100000 + 1 for _ in range(200)] for _ in range(10)]
    print(f"1000 piles of 2, k = 1999: {max_value_of_coins(pairs, 1999)}; 10 piles of 200, k = 1000: {max_value_of_coins(tall, 1000)}")


main()
