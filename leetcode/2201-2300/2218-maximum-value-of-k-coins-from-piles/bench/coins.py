# LeetCode #2218: Maximum Value of K Coins From Piles -- bench mirror of
# coins.kara: a knapsack over the piles, best[j] the most j coins are
# worth so far, each pile tried at every count of its top coins with j
# running down.


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


def main():
    # 100 piles of 10 coins worth up to 10^5
    chests = [[[wide_random() % 100000 + 1 for _ in range(10)] for _ in range(100)] for _ in range(20)]
    check = 0
    for a in range(20):
        for r in range(4):
            # punch: one coin is drawn again before each answer
            chests[a][r * 31 % 100][r] = wide_random() % 100000 + 1
            check = (check * 31 + max_value_of_coins(chests[a], 600)) % 1000000007
    print(f"20 sets of 100 piles of 10, k = 600, 4 punches: checksum {check}")


main()
