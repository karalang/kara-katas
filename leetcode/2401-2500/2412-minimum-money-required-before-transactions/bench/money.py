# LeetCode #2412: Minimum Money Required Before Transactions -- the bench,
# the ★ arm in Python: the total loss, and the largest of the losing
# transactions' cashbacks and the gaining ones' costs.

seed = 2412


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def minimum_money(transactions):
    loss = 0
    extra = 0
    for cost, cashback in transactions:
        if cost > cashback:
            loss += cost - cashback
            extra = max(extra, cashback)
        else:
            extra = max(extra, cost)
    return loss + extra


def main():
    lists = []
    top = 1
    for _ in range(10):
        top *= 7
        ts = []
        for _ in range(100000):
            cost = (next_random() * 32768 + next_random()) % (top + 1)
            ts.append((cost, (next_random() * 32768 + next_random()) % (top + 1)))
        lists.append(ts)
    check = 0
    for p in range(100):
        for ts in lists:
            check = (check * 31 + minimum_money(ts) + p) % 1000000007
    print(f"100 passes over 10 lists of 10^5 transactions: checksum {check}")


main()
